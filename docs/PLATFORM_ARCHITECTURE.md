# FieldOps Platform — Technical Architecture

**From**: `dcentral-fieldops`, a single-tenant backend built for one client (Sod Boys Ltd)
**To**: a multi-tenant field-operations platform serving landscaping, general construction, and infrastructure companies, with generative scheduling and (later) generative design

This document describes the target architecture and the concrete engineering work required to get there. It assumes the reader has the current single-tenant codebase in front of them — file paths below refer to it directly.

---

## 1. Current state (verified against the codebase)

Before designing the platform, it's worth being precise about what exists today, because the platform design either reuses or replaces each of these:

| Component | Current shape |
|---|---|
| Tenancy | None. One deployment = one company. `NODE_DID_DOMAIN` is a single env var for the whole system. No `tenant_id` column anywhere in the schema. |
| Identity | `did:web` per deployment, one root node identity, path-based sub-DIDs for agents and crew members. Custom JWT-VC implementation (`src/identity/`), no external framework. |
| Authorization | 5-tier capability model (0 read-only → 4 admin), enforced per MCP tool call and per REST route via a standing capability grant re-checked against Postgres on every request — not trusted from a JWT claim. |
| Data | Single Postgres database, 42 migrations, 41 domain modules. |
| API surface | REST façade (20 routes) for the web dashboard + 30 MCP tools for the AI agent. Both call the same `src/domain/*.ts` functions directly. |
| Frontend | A pruned fork of OpenConstructionERP (AGPL), cut from ~200 routes to 8 domain modules, vendored as a git submodule. |
| Provisioning | Manual (`npm run bootstrap:*` scripts run by hand over SSH). No self-serve signup. |
| Hosting | One Oracle Cloud VM, one Cloudflare zone, one domain. |

This is a strong foundation for a platform specifically *because* of the identity model — a system built around "one root identity issuing scoped credentials to sub-identities" generalizes into "one platform issuing scoped credentials to tenants" without a conceptual rewrite, only an extension.

---

## 2. Product shape: PaaS core, SaaS apps on top

Landscaping, general construction, and infrastructure companies don't want the same screens, the same terminology, or the same workflows — but they do share the same underlying operational primitives (crew, scheduling, assets, cost). The right shape is a layered platform, not one universal app:

- **Core platform (PaaS)**: identity, multi-tenant data isolation, the MCP/agent framework, the scheduling engine. Industry-agnostic. Could eventually be exposed to third-party developers building their own vertical apps.
- **Vertical modules**: industry-specific configuration — job types, asset categories, terminology, seasonal patterns — for landscaping, construction, and infrastructure.
- **Client apps (SaaS)**: a branded dashboard and an AI agent per vertical (and eventually per tenant), consumed by the actual end customers.

```
┌─────────────────────────────────────────────┐
│ Client apps        (web dashboard, AI agent) │  ← what customers touch
├─────────────────────────────────────────────┤
│ Vertical modules    (landscaping, const,     │  ← industry configuration
│                       infrastructure)         │
├─────────────────────────────────────────────┤
│ Domain primitives    (crew, assets, payroll) │  ← shared business logic
├─────────────────────────────────────────────┤
│ Core platform    (identity, tenancy, MCP)    │  ← foundation
└─────────────────────────────────────────────┘
```

---

## 3. Multi-tenancy design

### 3.1 Data isolation

Given this system already handles payroll and financial data, the isolation model matters more than almost anything else in this document. Three real options, in order of increasing isolation and increasing operational cost:

1. **Shared tables + `tenant_id` + application-level filtering.** Cheapest, fastest to build, highest risk — a single missed `WHERE tenant_id = $1` is a cross-tenant data leak. Not recommended as the sole control for a system already handling payroll.
2. **Shared tables + `tenant_id` + Postgres Row-Level Security (RLS).** The database itself refuses to return rows outside the current session's tenant, even if application code forgets the filter. Recommended baseline — defense in depth on top of (1), not a replacement for correct application code.
3. **Schema-per-tenant or database-per-tenant.** Strongest isolation, more operational overhead (migrations run N times, connection pooling gets more complex). Worth reserving for larger/enterprise customers as a paid tier, rather than the default for every signup.

**Recommendation**: RLS-enforced shared schema for the self-serve tier, with schema-per-tenant available as an "isolated" add-on for larger accounts. This mirrors how most serious multi-tenant SaaS platforms (Supabase, many fintechs) actually do it.

### 3.2 Identity, extended not replaced

Today: one node DID (`did:web:id.sodboysltd.org`) is the root of trust for one company.

Platform model: the *platform itself* becomes the root, and each tenant becomes its own node identity underneath it:

```
did:web:platform.com                          (platform root)
  └── did:web:platform.com:tenants:acme-landscaping
        └── did:web:platform.com:tenants:acme-landscaping:crew:<uuid>
        └── did:web:platform.com:tenants:acme-landscaping:agents:whatsapp-gateway
  └── did:web:platform.com:tenants:bolt-construction
        └── ...
```

Capability grants stay exactly the model they are today (`capability_grants` rows, signed VCs, tier 0–4) — just scoped one level deeper. A tenant's admin can issue capability grants to their own crew and agents, but cannot issue grants outside their own tenant subtree. This is a genuine extension of `src/identity/`, not a rewrite: `did.ts`, `capabilities.ts`, and the JWT-VC machinery in `vc.ts` all stay conceptually the same; what changes is the DID path structure and adding a tenant-scope check to `verifyPresentedCapability`.

### 3.3 Self-serve provisioning

Replace the manual bootstrap scripts with an automated tenant-creation flow:

1. Signup form collects company name, industry vertical, admin email/password.
2. Backend mints the tenant's node DID, creates the initial `capability_grants` row for the admin (tier 4, scoped to that tenant only), seeds default sovereignty-tier policy and default job types for the chosen vertical.
3. Admin lands in an onboarding flow to invite crew, connect a WhatsApp number (via the agent gateway), and configure their first sites.

This is new code, not an extension of the existing `bootstrap*.ts` scripts — those were designed for a human running them once per deployment, not for repeatable, unattended execution.

---

## 4. Generative scheduling

This is the platform's near-term differentiator and the most technically tractable of the two "generative" asks.

### 4.1 What it actually is

Scheduling is fundamentally a **constraint-satisfaction / optimization problem**, not a task an LLM should be asked to solve end-to-end. Treating it as a prompt-engineering problem will produce schedules that look plausible and are wrong in ways that are expensive to discover in the field (double-booked crew, equipment sent to the wrong site, a shift that ignores a certification requirement).

### 4.2 Architecture

```
Natural language request
   ("reschedule Miller job around Thursday's storm")
        │
        ▼
LLM constraint translator   →  turns the request into structured constraints
        │                       the solver understands (job, window, blockers)
        ▼
Constraint solver            →  generates a candidate schedule satisfying hard
(OR-tools / constraint         constraints (crew availability, certifications,
 programming library)          equipment availability) and optimizing soft ones
        │                       (minimize drive time, balance workload)
        ▼
LLM explanation layer        →  explains the proposed schedule back in plain
                                 language, surfaces trade-offs it made
        │
        ▼
Confirm-before-execute        →  a human approves before anything is committed
(reuses the existing tier-2
 confirmation pattern)
```

### 4.3 Inputs the solver needs

- Crew availability (shift patterns, time off, seasonal capacity)
- Skills/certifications per crew member (already partially modeled via `crewMembers.ts`)
- Equipment/vehicle availability (`assets.ts`, `vehicles.ts`)
- Site locations and travel time between them (real cost for landscaping/construction — a schedule that ignores drive time isn't usable)
- Job deadlines and priority
- Weather (already have `get_site_weather` as an MCP tool — directly reusable as a scheduling input, not just crew-facing information)
- Labor rules (max hours, required breaks — jurisdiction-dependent, becomes more important once tenants span multiple regions)

### 4.4 Why this reuses existing architecture well

The confirm-before-execute pattern already exists for tier-2 MCP actions (e.g. `submit_spend_record`). A generated schedule is a natural fit for the same pattern: propose, don't silently commit, especially while trust in an automated scheduler is being established with real customers.

---

## 5. Generative design (phased, expectations set deliberately low early)

"Generative design" is a much larger claim than scheduling — this section exists to scope it honestly rather than overpromise.

### Phase 1 — Takeoffs and estimating (near-term, tractable)
Automated material takeoffs and cost estimates from uploaded plans. Notably, the vendored OpenConstructionERP frontend already shipped takeoff/estimating modules that were pruned out during the single-tenant build (they didn't fit Sod Boys' domain). Reviving and adapting those for the platform version is a real head start rather than new development from zero.

### Phase 2 — Template-based generative layouts (mid-term)
Planting plans, hardscape layouts, site logistics plans generated from a library of patterns plus site-specific constraints (lot dimensions, sun exposure, soil type for landscaping; access routes and staging areas for construction). Tractable with current generative AI tooling combined with a constraint layer, similar in spirit to the scheduling engine.

### Phase 3 — True generative design (long-term, possibly not built in-house)
Genuine generative site design is adjacent to CAD/BIM-scale generative design tooling (the kind of R&D Autodesk invests heavily in). This is a real specialty. The honest options are: invest significant long-term R&D, or license/integrate existing generative-design technology rather than building it from scratch. Decide this later, with real usage data from Phases 1–2 informing whether customers actually want it enough to justify either path.

**Do not lead go-to-market messaging with Phase 3 capability before Phase 1 exists in production.** Overpromising here is a credibility risk with construction/infrastructure customers, who are typically less tolerant of vendor overreach than software buyers.

---

## 6. Vertical modules

Each vertical is configuration on top of the same domain primitives, not a fork of the codebase:

| Primitive | Landscaping | General construction | Infrastructure |
|---|---|---|---|
| Job types | Mowing, planting, irrigation install, snow removal | Framing, concrete pour, electrical rough-in | Utility trenching, conduit runs, civil grading |
| Asset categories | Mowers, sprayers, irrigation tools | Power tools, scaffolding, formwork | Heavy equipment, traffic control gear |
| Seasonal pattern | Spring/summer peak, winter (snow) secondary peak | Weather-gated year-round, regional variation | Weather-gated, often has regulatory seasonal windows |
| Terminology | "Sites" reads naturally | "Sites" → often "job sites" or "projects" | "Sites" → often "routes" or "segments" |

The `job_types`, `assets`, and terminology-facing labels should become tenant-configurable data (seeded from a per-vertical template at signup), not hardcoded TypeScript enums as they are today in the single-tenant build.

### Seasonal work handling

Not an edge case — a first-class domain requirement:

- **Seasonal capacity planning**: forecasted demand vs. available crew by month, informing the scheduling engine's constraints rather than being a separate report.
- **Seasonal rehire flows**: crew who return every season need a lighter-weight re-onboarding than a brand-new hire — reuse identity (DID persists), refresh capability grants and certifications.
- **Cross-season utilization**: a landscaping company doing snow removal in winter is really running two seasonal businesses through one crew/asset pool — the platform should support a tenant operating multiple concurrent "seasons" of job types.

---

## 7. Business model considerations

*(Product/pricing decisions — flagging the structural implications, not making the call.)*

- **SaaS tiers**: likely by crew size or site count, consistent with how most field-service SaaS (Jobber, ServiceTitan, BuildOps) price.
- **Usage-based add-ons**: AI/agent calls have real marginal cost (LLM API usage) — likely metered separately from the base subscription rather than bundled at every tier.
- **PaaS/platform tier**: exposing the core platform's APIs (identity, scheduling engine, domain primitives) to third-party developers building their own vertical apps is a later-stage option, not a v1 requirement — don't build platform-API polish before the SaaS product has paying customers validating the core.
- **Isolation as a paid tier**: schema-per-tenant or database-per-tenant (see §3.1) is a natural enterprise-tier differentiator, not something every customer needs to pay for by default.

---

## 8. Technology decisions carried forward

Everything below is inherited from the single-tenant build and remains the right choice at platform scale — no reason to revisit:

- **`did:web`**, not `did:webvh` — simpler, resolves over plain HTTPS, no key-rotation history needed for this system's actual requirements.
- **Custom JWT-VC (`jose` for JWS/JWT mechanics only)** — no DID/VC framework dependency, avoids the real, documented bugs found in the earlier Veramo-based attempt (missing JWT expiration enforcement, broken verifier requirements).
- **Postgres**, no separate graph DB — pgvector already available in the image for a future knowledge/RAG layer.
- **Official `@modelcontextprotocol` SDK** for the agent/tool layer — unaffected by any of the multi-tenancy work above.
- **Capability-grant JWTs**, not full UCAN — simpler to keep genuinely correct; revisit only if delegation chains beyond direct tenant→agent grants become necessary.

New for the platform:

- **Postgres Row-Level Security** for tenant isolation (see §3.1).
- **A tenant-provisioning service** replacing the manual bootstrap scripts (see §3.3).
- **A constraint-solving library** (e.g. Google OR-Tools or a comparable constraint-programming library) for the scheduling engine — this is new infrastructure, not an extension of anything in the current codebase.
- **Billing integration** (e.g. Stripe) — entirely new.

---

## 9. Implementation roadmap

| Phase | Scope | Why this order |
|---|---|---|
| 1 | Multi-tenancy refactor: `tenant_id` + RLS across all 41 domain modules, tenant-scoped DID hierarchy, automated provisioning | Nothing else is safe to build on a single-tenant data layer — this has to come first, not be retrofitted later |
| 2 | Self-serve signup + billing | Turns the platform from "something you SSH into" into something a second real customer can actually use |
| 3 | Second vertical live (pick landscaping + one other) | Validates the vertical-module abstraction against real data before committing to a third or fourth vertical on paper |
| 4 | Generative scheduling (constraint solver + LLM layer) | The clearest differentiator, and directly reuses the existing confirm-before-execute agent pattern |
| 5 | Seasonal capacity planning tooling | Real domain need once a second full season of data exists across tenants |
| 6 | Generative design Phase 1 (takeoffs/estimating, reviving pruned vendor modules) | Cheapest "generative design" win available, reuses existing vendored code |
| 7 | Generative design Phase 2+ (template layouts, evaluate build-vs-partner for true generative design) | Only after real customer demand signal from Phases 1–6, not built speculatively |

**Recommendation on sequencing**: don't attempt a third vertical, a full billing system, and the scheduling engine simultaneously. Multi-tenancy correctness (Phase 1) is the one piece that cannot be retrofitted cheaply if gotten wrong early — treat it as the gate before anything else on this list.

---

## 10. Open questions / risks

1. **Tenant data isolation is the single highest-consequence engineering decision in this document.** A cross-tenant data leak in a system holding payroll data would be an existential event for a platform business, not a bug to fix in a patch release. Disproportionate care here is warranted relative to every other item on this roadmap.
2. **AGPL frontend at platform scale**: the vendored OpenConstructionERP frontend's AGPL obligations (already navigated once for the single-tenant build, see the existing `docs/ARCHITECTURE.md` "Frontend" section) need re-evaluation once the frontend is served to paying third-party customers rather than one client — worth a real legal review before general availability, not just an engineering read of the license.
3. **What v1 data migration looks like** for the original Sod Boys deployment once the platform exists — does it become tenant zero, or stay a separate deployment indefinitely?
4. **Regulatory/labor law variation across regions** becomes real once tenants aren't all in one jurisdiction — the scheduling engine's "labor rules" constraint (§4.3) needs to be data, not hardcoded assumptions, from day one of the scheduling engine's design.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

*No cross-references detected to/from other docs/*.md files.*

<!-- AUTO-GENERATED RELATED END -->
