---
source_conversation_uuid: 8f7a2740-7f7b-4f16-b483-d1e161ebb85e
conversation_title: '💬 I have an idea for the dcentra…'
created_at: 2026-08-08T03:34:00.540823Z
doc_id: DC-SIM-009
description: 'Architecture decision records resolving the six open decisions'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
reconciliation_note: "Supersedes DC-SIM-008's open status on items 1-6 only (verified accurate against its own header claim) -- DC-SIM-008's analysis is not restated here and remains necessary reading alongside these decision records."
topic: "dcentral-simulation-lab-programme"
---

# DC-SIM-009 — Architecture Decision Records

| Field | Value |
|---|---|
| Document ID | DC-SIM-009 |
| Version | v1.0 |
| Date | August 2026 |
| Author | Toussaint Redji Jean Baptiste |
| Status | **Decided** — resolves DC-SIM-008 items 1–6 |
| Supersedes | DC-SIM-008 §§1–6 (open status only; analysis retained) |

---

## 0. Decision summary

| ADR | Decision | Shape |
|---|---|---|
| 001 | Ontario ISP and Mesh ISP are **layers, not alternatives** | Both — A licenses, B rides |
| 002 | FCN splits into two namespaces by side-effect class | Both — `/x/` v1, `/q/` v2 |
| 003 | LI fork is per-node via issued VC; **ROOT only in v1** | Schema now, ALT deferred |
| 004 | Li-Fi deferred, interface preserved | v2 add-on |
| 005 | Raw frames never published; consent grants **local viewing** | Both — reframed |
| 006 | Three-profile node taxonomy **confirmed** | Unify into DC-SHI-SPEC-002 |

The general principle applied throughout: **where "both" is possible, sequence it so that
v1 is the restrictive case and v2 is additive.** Starting restrictive and loosening is a
migration; starting permissive and tightening is a rewrite.

---

## ADR-001 — The two ISPs are layers of one stack

### Decision

The Ontario D-Central ISP Initiative and the Mesh ISP/MNO layer are **not competing
designs and not sequential versions of the same thing.** They are two layers with a
clean interface.

- **Layer A — the licensed carrier.** Ontario D-Central ISP Initiative. Holds the CRTC
  Facilities-Based Provider registration, the transit contracts, the pole attachment
  agreements, the ARIN resources, and the legal liability. Conventional retail billing
  in fiat. This is Company Zero's first regulated product.
- **Layer B — the cooperative service layer.** Mesh ISP/MNO. Membership, metering,
  contribution accounting, revenue sharing, token economy. **Operates as a tenant of
  Layer A.**

### Rationale

This is how cooperative ISPs actually work: a licensed entity plus a member layer. The
separation has three properties that make it strictly better than either document alone.

1. **The token economy does not need regulatory approval,** because Layer A holds the
   licence and handles the regulated retail relationship. B's $WORK/$DATA accounting is
   internal member contribution accounting, not a telecommunications tariff.
2. **Liability is contained.** Layer A can operate and generate revenue with Layer B
   entirely unbuilt. Layer B failing does not endanger the licence.
3. **It resolves the billing conflict.** A bills subscribers in CAD under CRTC rules.
   B meters member contribution and distributes surplus. These stop competing.

### Interface

| Boundary | Definition |
|---|---|
| Identity | B members are A subscribers. One `SubscriberVC` issued by A; one `MemberVC` issued by B. |
| Traffic | All B traffic transits A. B never holds a carrier relationship. |
| Metering | B's metering agent measures member contribution. A's billing measures regulated retail consumption. Separate systems, separate ledgers. |
| Revenue | A collects retail revenue. Surplus flows to B's treasury by cooperative bylaw, not by protocol. |
| Governance | B governs its own membership and distribution. A is governed by corporate law and CRTC obligation. |

### Sequencing

- **v1:** Layer A only. No tokens, no DAO, no metering. A conventional small ISP.
- **v2:** Layer B introduced as a membership overlay on an operating Layer A.

### Consequences

The emulation programme models Layer A (already decided in DC-SIM-002). The 68/20/10
split, `FeeCollector` and `RevenueRouter` move entirely to v2 and out of the v1 contract
set in DC-SIM-007 §2.1.

---

## ADR-002 — FCN namespace split by side-effect class

### Decision

FCN carries **both** resolution models, separated by an explicit namespace that makes the
class unambiguous at every call site.

| Namespace | Model | Semantics |
|---|---|---|
| `/fcn/q/...` | Named Function Networking (Reading A) | Pure query or computation. Cacheable network-wide, ICN-resolvable, DTN-compatible. |
| `/fcn/x/...` | Service addressing (Reading B) | Execution with side effects or authority. Never cached. Requires a live host. |

### The classification rule

> **If it writes, actuates, spends, grants, or revokes — it is `/x/`.
> If it reads or computes — it is `/q/`.**

Examples under the existing endpoint set:

| Old | New | Class |
|---|---|---|
| `/fcn/infra.power` (actuation) | `/fcn/x/infra.power` | Never cacheable — safety-critical |
| `/fcn/sec.patrol` (dispatch) | `/fcn/x/sec.patrol` | Never cacheable — a stale patrol result is an incident |
| `/fcn/gov.treasury` (spend) | `/fcn/x/gov.treasury` | Never cacheable |
| `/fcn/tech.data` (aggregate) | `/fcn/q/tech.data` | Cacheable with TTL |
| `/fcn/agri.plant` (advisory computation) | `/fcn/q/agri.plant` | Cacheable |

### Purity enforcement

Classification by review is insufficient. `/q/` handlers execute as **WASM modules with
no host syscall access** — no network, no filesystem, no clock beyond an injected
timestamp. Purity becomes a property of the runtime rather than a convention. This uses
the WASM execution model already specified in the FCN compute layer.

Each `/q/` endpoint carries a manifest declaring TTL and cache scope. No TTL, no caching.

### Sequencing

- **v1:** `/x/` only. Ordinary services over gRPC or HTTP with DID/VC authorisation.
  Nothing is cached. This covers everything the system actually needs today.
- **v2:** `/q/` added over NDN/NFD or CCN-lite when partition-tolerant queries and DTN
  operation become live requirements.

### Rationale for that order

Starting with `/x/` means nothing is cached, so introducing caching later is **purely
additive**. Starting with `/q/` and retrofitting safety would require auditing every
endpoint for accidental side effects under a cache that is already in production —
a considerably worse position.

### Consequences

Unblocks node configuration and DC-SIM-002 build order. The DTN story becomes explicit:
DTN carries `/q/` natively in v2; `/x/` over DTN requires application-layer queuing with
idempotency keys, which is a separate design.

---

## ADR-003 — Lawful intercept fork: per-node VC, ROOT only in v1

### Decision

The fork is a **per-node property**, not a per-network one, signalled by a
`NetworkForkVC` issued at provisioning.

```
NetworkForkVC
  issuer:   the licensed carrier entity (Layer A) — never self-issued
  subject:  node DID
  fork:     ROOT | ALT
  scope:    the traffic classes the node is authorised to carry
  issued:   timestamp
  status:   revocable via status list
```

**Binding rule:** any node carrying regulated retail traffic must hold a `ROOT`
credential. A node without a valid `NetworkForkVC` carries no traffic at all — absence
fails closed.

### Sequencing

- **v1: ROOT only.** Every node is under the licensed carrier, so every node is ROOT.
  `ALT` is defined in the schema but not implemented.
- **v2:** `ALT` considered for member-to-member mesh traffic that does not transit the
  licensed carrier — **subject to legal advice, not to this document.**

The schema is defined now specifically so that the field exists and every node is
explicitly marked from day one. Retrofitting an identity field across a deployed fleet is
expensive; carrying an unused enum value is free.

### Legal caveat — read this before acting on it

Whether Canadian law treats cooperative member-to-member mesh traffic as
telecommunications subject to interception obligations is **not a question this document
can answer**, and my read should not be treated as advice. The interaction between CRTC
registration, the *Telecommunications Act*, and lawful access obligations needs a telecom
lawyer before any `ALT` node carries traffic.

Practical position: v1 is ROOT-only, which sidesteps the question entirely and is the
correct posture for a first regulated product.

---

## ADR-004 — Li-Fi deferred, interface preserved

### Decision

Li-Fi/VLC is **not in the v1 BOM and not in Phase 1.** Wi-Fi 6 is the sole in-home access
medium for v1.

The architectural requirement that survives: **nothing may be designed that assumes
Li-Fi.** In-home access is a pluggable medium behind a common gateway interface. Adding
VLC in v2 must be a new medium module, not a gateway redesign.

### Rationale

The client dongle requirement is a hard adoption blocker, and there is no reason to
absorb it during a proof of concept. Deferring costs nothing provided the interface stays
medium-agnostic.

Li-Fi is entirely unmodellable in emulation (DC-SIM-001 §3.3), so this decision has zero
impact on the simulation programme — it is a roadmap and BOM decision only.

### Sequencing

- **v1:** absent.
- **v2/v3:** optional in-home premium tier, as scoped in DC-ISP-TECH-001.

---

## ADR-005 — Raw frames are never published; consent grants local viewing

### Decision

The conflict is resolved by changing what consent *does*.

| Rule | Status |
|---|---|
| Metadata-only publication to ICN | **Always. Non-negotiable.** |
| Raw frames published to ICN | **Never, under any credential.** |
| Raw frames leaving the owning node | Only under a live, time-boxed session |

Rendering that requires raw frames happens **locally on the node that owns the camera**,
or does not happen.

### The reframe

`MetaverseConsentVC` does not unlock *publishing*. It unlocks a **local, time-boxed,
revocable viewing session**:

```
MetaverseConsentVC
  scope:      one camera, one requester
  duration:   explicit expiry, short by default
  revocation: immediate, unilateral, by the space owner
  logging:    every session start/end written to an append-only log
  transport:  direct session only — never content-addressed
```

### Rationale

This is the load-bearing distinction: **content-addressed raw video can never be
un-published.** Once a frame has a CID and has propagated, revocation is not
technically possible. Consent to publish is therefore irreversible consent, which is not
consent in any meaningful sense.

Consent to *view* is bounded and revocable. The metaverse feature works; the privacy
property holds; both survive.

### The unsolved part, stated plainly

**Bystander consent is not solvable technically.** Cameras capture people who never
agreed to anything — visitors, delivery workers, neighbours in frame. No credential
scheme addresses this.

This is why DC-SIM-006 stage 5 requires written policy, not just code: signage,
camera placement rules, field-of-view constraints that exclude public space and
neighbouring property, retention limits, and a deletion process. PIPEDA exposure begins
at first deployment with real users, not at scale.

### Sequencing

- **v1:** metadata only. No raw-frame path exists at all, not even a disabled one.
- **v2:** local viewing sessions under `MetaverseConsentVC`, after the written policy
  exists.

---

## ADR-006 — Three-profile node taxonomy confirmed

### Decision

The previously proposed taxonomy is **confirmed** and becomes canonical.

| Profile | Sensing | Connectivity | BOM |
|---|---|---|---|
| **P1 — Residential SHI** | Levels 1–3 | Wi-Fi 6; Li-Fi optional (v2) | Base SHI BOM |
| **P2 — Commercial / Campus** | Levels 1–5 | + FSO backhaul eligible | + DC-SENSE-SERVICE-001 |
| **P3 — High-security / Research** | Full stack | Per-deployment | Per-deployment |

Confirmed alongside it: the SHI node and the home node are **the same product**; Level 4/5
sensing belongs to P2 and P3 only; Li-Fi is a residential add-on outside the base BOM;
FSO is ISP-layer outdoor backhaul at neighbourhood scale, not a node-level medium.

### Action

Unify DC-SHI-SPEC-001, the spatial sensing taxonomy, and the Li-Fi/FSO connectivity
architecture into **DC-SHI-SPEC-002**, superseding all three. The three existing
documents are marked superseded rather than deleted.

---

## 7. Root cause note

ADR-001 and ADR-006 are the same failure: parallel design work across separate sessions
producing overlapping, unreconciled specifications that were never brought into contact.
With a registry of this size that recurs by default.

**Proposed registry convention, for DC-REG-001:** every new document must declare, in its
header, what it **supersedes**, what it **extends**, and what it **conflicts with**. A
document that declares none of these is asserting it occupies empty space — which should
be a deliberate claim rather than an accident.

---

## 8. What is now unblocked

| Was blocked on | Now |
|---|---|
| Node configuration | ADR-002 — `/x/` only, DID/VC auth |
| Topology subject | ADR-001 — Layer A |
| v1 contract set | ADR-001 — revenue contracts move to v2 |
| SHI documentation | ADR-006 — write DC-SHI-SPEC-002 |
| Stage 5 deployment | ADR-005 — policy required first, code second |
| Nothing | ADR-003, ADR-004 — schema and interface only |
