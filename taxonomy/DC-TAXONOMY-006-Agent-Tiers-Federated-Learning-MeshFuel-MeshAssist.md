   # DC-TAXONOMY-006: Multi-Tier Agent Commissioning, Federated Learning, MeshFuel & MeshAssist
### Extends DC-TAXONOMY-001–005

---

## 1. Who can commission agents

DC-TAXONOMY-005 assumed one implicit commissioner: the DAO itself, at the ecosystem level. That's actually the top of a three-tier structure, and each tier needs the same loop from §3 of 005 (mandate → research → proposal → vote → execution → attested outcome) but with different commissioners, different treasuries paying for the work, and different scopes of what the agent is allowed to propose into.

### 1.1 Ecosystem-tier agents (unchanged from 005)

Commissioned by `dc-governance` at the whole-network level. Mandate scope: cross-cutting architecture (new modules, core primitive changes, ecosystem-wide treasury allocation). Funded from the main DAO treasury. Proposals go to the full staked-member vote.

### 1.2 Coop/service-tier agents (new)

Any individual mesh service, cooperative, or vertical — a MeshEats regional co-op, a MeshBank remittance corridor, a single OpenSecure OS-SENTINEL deployment, a Lakou Marketplace regional chapter — can commission its own agent(s), scoped to that service's own improvement.

- **Commissioning body:** the service's own `dc-governance` *scoped instance* (same mini-DAO pattern already used for MeshBoard community moderation in DC-TAXONOMY-004 §2.6) — a coop doesn't need ecosystem-wide DAO permission to hire a research agent for its own operations.
- **Funding:** the coop's own treasury sub-account (`dc-credit` treasury-manager already supports scoped/sub-treasuries — this is the same mechanism a MeshBoard community or a MeshCircle professional group would use for its own funds).
- **Proposal destination:** by default, votes at the coop's own scoped-instance level (a MeshEats regional co-op's members vote on their own delivery-routing improvement). Only if a coop-tier proposal requests something outside the coop's own treasury or touches a shared core primitive does it escalate to the ecosystem-tier vote — same escalation logic a human-originated proposal would follow.
- **Example:** a MeshBank Haiti-corridor cooperative commissions an agent specifically to reduce remittance settlement latency; the agent researches within that corridor's own transaction history and proposes a routing change; the corridor's own members vote; if it works, a later ecosystem-tier research mandate can ask "should this become the default for all corridors" — which is where coop-tier learning becomes ecosystem-tier proposal, addressed properly in §3 below.

### 1.3 Individual/private-tier agents (new)

Any DID holder can commission a private agent, personally funded, to research and draft proposals on their behalf — into any governance body they're a member of (their MeshBoard community, their coop, the ecosystem DAO if they're staked there).

- **Commissioning body:** the individual DID, directly — no scoped-instance permission needed, since they're spending their own D-Credit.
- **Funding:** the individual's own `dc-credit` balance (from their MeshBank/Wealthfolio-tracked wallet).
- **Proposal destination:** whichever governance body the mandate targets — the agent still submits through that body's normal proposal-engine, it doesn't get a side channel. A private agent has no more authority than the human who commissioned it would have submitting the same proposal manually.
- **Example:** Toussaint personally commissions an agent to research and draft a MeshBuild spec improvement (multi-milestone escrow edge case he keeps hitting), submits it to the MeshBuild scoped-instance vote himself.

### 1.4 Compensation flow — this is the part that needs a real mechanism

The compensation question ("the commissioner gets paid when their proposal's vote is approved") needs its own primitive, since nothing in `dcentral-core` currently ties proposal-approval to a payout *to the proposer* — approval currently just triggers execution of whatever the proposal asked for (fund the feature, change the spec). A **proposal-bounty** mechanism is the missing piece:

```
1. Mandate issuance (coop, ecosystem, or individual) optionally
   attaches a bounty pool: "if a resulting proposal passes vote,
   the commissioner (coop treasury, or the individual who paid for
   the agent) receives X D-Credit from [ecosystem treasury / coop
   treasury / a dedicated research-incentive pool]."

2. Agent researches, drafts, submits proposal — mandate-bounty
   reference travels with it via dc-attestation (so the bounty
   terms are locked in before the vote, not negotiated after —
   prevents retroactive bounty-padding).

3. Vote passes → treasury-manager does TWO releases in one
   execution: (a) fund whatever the proposal itself requested
   (the feature/treasury-allocation/spec change), and
   (b) pay the bounty to the commissioner who funded the agent's
   research in the first place.

4. Vote fails → no bounty. The commissioner ate the cost of
   running the agent and got nothing — same risk/reward a human
   proposer already faces when they spend their own time drafting
   a proposal that doesn't pass.
```

This is genuinely the right incentive shape: it rewards *good* research (proposals that actually clear a vote) rather than *volume* of proposals, and it's symmetric across all three tiers — a coop and an individual both bear the agent-running cost and both only get paid on approval, which naturally discourages spam (the proposal-volume throttle from 005 §3.3 still applies on top of this as a backstop, not a replacement).

**Where the bounty comes from matters too:** ecosystem-tier bounties draw from the main DAO treasury (or a dedicated `DC-RESEARCH-INCENTIVE-POOL-001`, worth naming explicitly rather than raiding the general treasury ad hoc); coop-tier bounties draw from that coop's own sub-treasury; individual-tier proposals typically don't need an inbound bounty at all if the individual is proposing something that benefits their own coop/community (their reward is simply the improvement itself) — bounties matter most for *ecosystem-tier* contributions where an individual or coop-agent surfaces something valuable enough that the wider network should pay for it.

---

## 2. Agent research context — what the agent actually reads

This is where the loop becomes genuinely different from a human proposer drafting from memory. When an agent researches within a mandate's scope, its context should include every public artifact the target service/module actually publishes, not just the taxonomy specs:

| Context source | What it gives the agent |
|---|---|
| **The service's own repo** (code, if the module/vertical has an open codebase) | Ground-truth of what's actually implemented vs. what the spec says — agents should flag spec/implementation drift as part of their research, not just propose net-new features |
| **Module/vertical specs** (this taxonomy series + each DC-XXX-001 doc) | Architectural intent and prior design decisions, so an agent doesn't re-propose something already considered and rejected, or re-derive a primitive that already exists elsewhere (this is the exact mistake the original Gemini chat made with ZK-proof inventory, corrected back in the first taxonomy doc) |
| **On-chain/ledger transaction history** (`dc-credit` ledger, to whatever extent a given service publishes its aggregate flow — not individual users' private balances) | Real usage patterns: which services are actually earning/spending D-Credit, where bottlenecks or underused capacity show up |
| **dc-attestation public record** | The full attested history of proposals, executions, and outcome-reviews for that service — this is what makes the recursive outcome-review step (005 §3.3) actually possible; without reading this, an agent can't tell what was already tried |
| **dc-registry capability-index (public portion)** | Node/capacity distribution — useful for infrastructure-allocation proposals (e.g., "this region is under-served by mesh-storage capacity") |
| **Anything else the specific service publishes** (a coop's own public meeting minutes, a MeshBoard community's public moderation log, SkyLedger's public flight-imagery index) | Service-specific context an ecosystem-wide agent wouldn't otherwise have — this is exactly why coop-tier agents (§1.2) matter: they can specialize in reading their own service's specific public artifacts more deeply than an ecosystem-tier generalist agent would |

**Privacy boundary, stated explicitly:** "public ledger/whatever is public" is the operative constraint — agent research context is scoped to what the service *already publishes*, same disclosure boundary that governs everything else in this architecture (selective disclosure, attestation-not-raw-data). An agent researching MeshBank shouldn't get raw access to individual account balances any more than a human auditor would; it reads the same public/attested surface any member could read.

---

## 3. Federated learning across agents

This is the mechanism that lets coop-tier and individual-tier research actually compound into ecosystem-wide improvement, rather than each tier's agents re-learning the same lessons in isolation.

### 3.1 What gets federated

Not raw research data (that stays scoped per §2's privacy boundary) — what federates is **method improvement**: which research approaches, which proposal structures, which code-generation patterns actually correlated with proposals that passed a vote *and* whose outcome-review (005 §3.3 step 6) later confirmed they worked. Three separate model-improvement targets:

1. **Research methodology** — which context sources (§2) and research strategies tend to surface proposals that pass and hold up
2. **Proposal drafting/structure** — which proposal formats, scoping choices, and bounty-request sizing correlate with vote approval
3. **Code generation** — for proposals that include actual implementation (a module change, a new microservice), which generation patterns produce code that passes review/testing without rework

### 3.2 How it stays consistent with the rest of the architecture

Federated learning here means the standard thing: each tier's agents (a MeshEats coop's agent, a MeshBank corridor's agent, an individual's private agent) train/fine-tune locally on their own scoped research history, and only **aggregated model updates** — not the underlying proposals, transaction data, or private research — get shared back to a shared method-improvement model. This is the same privacy discipline the whole ecosystem already applies to everything else (selective disclosure over raw data), just applied to *how agents learn* instead of *how services transact*.

```
Coop-tier agent (MeshEats region A)     Individual agent (Toussaint's)
      │ local fine-tune on                  │ local fine-tune on
      │ region A's own outcome              │ own proposal history
      │ history                             │
      └──────────┬───────────────────────────┘
                 │  only aggregated weight
                 │  updates shared, not raw
                 │  research/proposals
                 ▼
        Shared "research method" model
        (governed by dc-governance —
        who can query it, how updates
        get accepted, same proposal/vote
        pattern as everything else)
                 │
                 ▼
     Improves the NEXT research cycle for
     every tier — ecosystem, coop, individual
```

- **Governance of the federated model itself follows the same rules as everything else** — updates to "how agents should research/propose/generate code" are themselves proposals that go through `dc-governance`, so the meta-question of "should we change how our agents work" doesn't get an exemption from the vote-based accountability everything else in this architecture has.
- **This closes the loop nicely with §1's tier structure**: a coop-tier agent that develops a genuinely better research method (say, better at reading its own service's repo for spec-drift) contributes that improvement upward without exposing the coop's private business; an ecosystem-tier agent benefits from lessons learned across every coop without needing raw access to any of them.

---

## 4. New verticals

### 4.1 MeshFuel (gas/EV-charging on demand — Yoshi/Booster-equivalent)

| Primitive | D-Central equivalent | Built from |
|---|---|---|
| Request fuel/charge delivery to your parked car | Lakou Marketplace listing type, matched to a nearby mobile-node-equipped fuel/charge provider via `dc-registry` capability-index | Lakou Marketplace + `dc-registry` |
| Provider (independent operator with a fuel truck, or a mobile EV-charging unit) | Same mobile-node hardware class as MeshEats/MeshCar — the vehicle reports its own fuel/charge inventory via `mesh-sensors` telemetry, so the marketplace listing's "available now" status is attested, not manually updated | `mesh-sensors` mobile node |
| Delivery/completion proof | Fuel-level or charge-state before/after attestation (an OBD-II-class sensor reading, same telemetry class as TrafficMesh) | `dc-attestation` |
| Payment | Metered by liters/kWh actually delivered, `dc-credit` micropayment on completion | `dc-credit` |
| EV-specific: cooperative charging network | A neighborhood's mesh-energy-generating households (already earning D-Credit for grid contribution under `mesh-energy`) can double as fixed charging points, not just mobile ones — a genuinely nice cross-module tie-in, since `mesh-energy` already tracks household energy production/attestation | `mesh-energy` + `mesh-sensors` |

### 4.2 MeshAssist (AAA/roadside assistance + on-demand mechanic — AAA/Urgent.ly-equivalent)

| Primitive | D-Central equivalent | Built from |
|---|---|---|
| Roadside breakdown request | Same dispatch pattern as MeshEats/MeshRide — request goes out over `mesh-connectivity` to nearby mobile-node-equipped tow/repair providers, works even with no cellular signal since it's mesh-local | `mesh-connectivity` + `dc-registry` |
| Mechanic-on-demand (comes to you, vs. tow to a shop) | Lakou Marketplace/MeshBuild-adjacent listing — a mechanic is functionally a licensed-trade contractor (license-VC, same as an electrician), just mobile | MeshBuild pattern (§1.3 of 005) + mobile-node dispatch |
| Diagnostic data sharing | The stranded vehicle's own mobile-node telemetry (OBD-II-class fault codes) can be shared with the responding mechanic *before* arrival, via a scoped selective-disclosure grant, so they arrive with the right part already in hand | `mesh-sensors` + `dc-identity` selective disclosure |
| Membership/subscription model (AAA-style) | A cooperative pool — members pay into a shared `dc-governance`-managed pool, draws covered up to a policy the DAO sets, same shape as DC-RISKPOOL-001's cooperative insurance model | `dc-governance` + `dc-credit` |
| Towing (if repair isn't roadside-fixable) | Same MeshCarDelivery vehicle-transport primitive (§1.2 of 005), just an unplanned/emergency-priority instance of it rather than a scheduled one | MeshCarDelivery |

Notably, MeshFuel and MeshAssist both compose almost entirely from primitives already specified — the mobile-node hardware class, `mesh-energy`'s attestation, `dc-registry` dispatch, and the MeshBuild licensed-trade pattern all get reused rather than anything new being invented, which is a good sign the taxonomy's underlying primitive set is actually general enough.

---

## 5. Updated gap registry addition

26. **DC-AGENT-TIERS-001** — formal spec for the three commissioning tiers (ecosystem/coop/individual), scoped-instance treasury sub-accounts, and escalation rules from coop-tier to ecosystem-tier
27. **DC-PROPOSAL-BOUNTY-001** — the compensation mechanism in §1.4: bounty attachment at mandate issuance, dc-attestation-locked terms, dual-release execution on vote pass
28. **DC-RESEARCH-INCENTIVE-POOL-001** — the dedicated ecosystem-tier treasury pool funding bounties, separate from general treasury
29. **DC-AGENT-FEDERATED-LEARNING-001** — the federated model-improvement spec from §3: what's shared (aggregated weights only) vs. what stays local (raw research/proposals), and how updates to the shared model are themselves governed by proposal/vote
30. **DC-MESHFUEL-001** — gas/EV-charging on demand
31. **DC-MESHASSIST-001** — roadside assistance / on-demand mechanic, with a cooperative membership-pool option

---

*DC-TAXONOMY-006 — extends 001–005. Establishes three agent-commissioning tiers (ecosystem DAO, coop/service scoped-instance, individual private) each following the same mandate→research→proposal→vote→execution→attested-outcome loop but with different commissioners, treasuries, and escalation paths; introduces a proposal-bounty mechanism paying the commissioner only on vote approval, locked in via dc-attestation before the vote to prevent retroactive padding; specifies agent research context (repo, specs, public ledger/attestation history, registry capability data — bounded by the same public/attested disclosure line as everything else) and a federated-learning layer that shares only aggregated method-improvement (research strategy, proposal structure, code-generation quality) across tiers without exposing raw private research. Adds MeshFuel (gas/EV-charging on demand) and MeshAssist (roadside assistance/mobile mechanic with a cooperative membership-pool option), both composing almost entirely from already-specified primitives.*
