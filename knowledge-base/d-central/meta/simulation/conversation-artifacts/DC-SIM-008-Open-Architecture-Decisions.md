---
source_conversation_uuid: 8f7a2740-7f7b-4f16-b483-d1e161ebb85e
conversation_title: '💬 I have an idea for the dcentra…'
created_at: 2026-08-08T03:34:00.540823Z
doc_id: DC-SIM-008
description: 'Open architecture decisions blocking implementation'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
reconciliation_note: "DC-SIM-009 supersedes this document's OPEN STATUS on items 1-6 (each is now decided) but explicitly retains this document's analysis as necessary reading -- verified accurate on reading both; not marked status: superseded because the analysis here (the two-ISP finding, the FCN reading A/B distinction, etc.) is not restated in DC-SIM-009 and remains required context for the decisions it records."
---

# DC-SIM-008 — Open Architecture Decisions

| Field | Value |
|---|---|
| Document ID | DC-SIM-008 |
| Version | v1.0 |
| Date | August 2026 |
| Author | Toussaint Redji Jean Baptiste |
| Status | **Blocking** — items 1 and 2 gate the build |

---

## 0. Summary

| # | Decision | Blocks | Effort |
|---|---|---|---|
| 1 | Which ISP is being modelled | Topology design | Decided below |
| 2 | FCN resolution model | Node configuration, DTN story, caching | One page |
| 3 | Lawful intercept fork signalling VC | Any regulated MNO operation | One page |
| 4 | Li-Fi / VLC phase placement | Roadmap only | Low |
| 5 | Metaverse raw-camera privacy | Stage 5 of DC-SIM-006 | Medium |
| 6 | SHI / sensing / connectivity unification | Documentation coherence | Medium |

---

## 1. Two D-Central ISPs, unreconciled

**The finding.** Two distinct ISP architectures exist in the registry, developed in
separate sessions, sharing FSO/GPON vocabulary but differing in governance, billing and
legal footing.

**A — Ontario D-Central ISP Initiative** (DC-ISP-TECH-001, DC-ISP-ARCH-001,
DC-ISP-POC-001, April 2026). A regulated Ottawa business. FSO backhaul, GPON last mile,
ONTs, Wi-Fi 6 in-home, optional Li-Fi premium. CRTC Facilities-Based Provider
registration, Hydro Ottawa pole attachments, City ROW permits. Transit Option A
(IXP colocation, ARIN ASN, OttIX peering) or Option B (incumbent business fibre,
recommended for PoC). Costed at approximately CAD $16–30K (B) or $21–39K (A),
18-week timeline.

**B — Mesh ISP / MNO layer** (NexNode, MeshISPDAO). Token-metered cooperative telecom.
$WORK / $DATA / $COMM. DAO-governed. Revenue split 68% node operators / 20% RegionalDAO
/ 10% MetaDAO, 2% CoN fee to FeeCollector. Grew from the earlier community bandwidth-
sharing work.

**One is a company registered with the CRTC. The other is a protocol.**

**Decision for the emulation programme:** model **A**. It has an actual addressing plan,
routing architecture and defined failure domain — the emulation verifies a written
document rather than inventing a design. B is predominantly economic and governance
design, which GNS3 cannot evaluate (see DC-SIM-001 §5.2).

**Decision still required for the ecosystem:** the relationship between A and B. The
clean formulation, if it holds, is that **A is Company Zero's first regulated product
and B is v2.** This also has the property of pointing directly at the incorporation step
identified as ungated in DC-STATUS-001.

---

## 2. The FCN resolution issue — **blocking**

**The problem.** Registry documents use endpoints of the form `/fcn/gov.direct`,
`/fcn/infra.power`, `/fcn/tech.net`, `/fcn/agri.plant`, gated by VC level. Two
incompatible readings exist and the documents do not distinguish them.

### Reading A — literal Named Function Networking

The name *is* the computation. An ICN forwarder resolves the name, locates a node holding
the function, executes it, and caches the result **by name**.

- Resolution is network-layer
- Results are cacheable network-wide
- Works over DTN
- Implementations: CCN-lite (has NFN support), NDN/NFD

### Reading B — service addressing convention

The name is an endpoint path. A gateway resolves it to a host and forwards. Effectively
gRPC or HTTP with a DID/VC authorisation layer.

- Resolution is application-layer
- Every call reaches a live host
- Ordinary, well-supported, boring in the useful sense

### Why this is not cosmetic

| | Reading A | Reading B |
|---|---|---|
| Caching | Network-wide by name | None, or application-managed |
| Partition behaviour | Serves cached results | Fails |
| Stale result | **Correctness bug** | Impossible |
| DTN compatibility | Native | Requires application-layer work |
| Side effects | Dangerous — a cached `/fcn/sec.patrol` or `/fcn/infra.power` is a safety issue | Safe |

Different failure modes, different code, different DTN story.

**Observation.** The existing endpoint list reads like B — the entries are organisational
roles with permission levels, not computations. But the naming and the placement beside
ICN in the stack imply A.

### Recommended resolution

**B for anything with side effects or authority; A for pure queries and computation.**

`/fcn/infra.power` writing to an actuator must never be cached. `/fcn/tech.data`
computing an aggregate should be. This is a coherent architecture rather than a
compromise — but it requires the naming scheme to distinguish the two classes, which it
currently does not.

**Deliverable:** one page defining the two endpoint classes, the naming convention that
separates them, and the caching and authorisation rules for each. Required before any
node configuration work begins.

---

## 3. Lawful intercept fork — signalling VC undefined

The CoN governance specification defines `NetworkDAO ROOT` (with lawful intercept) and
`NetworkDAO ALT` (without). Mesh ISP/MNO operations in regulated jurisdictions must
operate under ROOT.

**Undefined:** the verifiable credential that signals which fork a subscriber node is
operating under.

**Blocks:** any regulated MNO operation, and stage 6 of DC-SIM-006. Not blocking for the
v1 emulation programme.

---

## 4. Li-Fi / VLC phase placement

VLC is marked experimental in the CoN specification. DC-ISP-TECH-001 positions Li-Fi as
an optional in-home premium tier, not part of backhaul or distribution, with the client
dongle requirement acknowledged as a friction point.

**Undecided:** whether Phase 1 includes VLC or defers to Phase 3.

**Note:** Li-Fi is entirely unmodellable in GNS3 (DC-SIM-001 §3.3), so this decision has
no bearing on the emulation programme. Roadmap impact only.

---

## 5. Metaverse raw-camera privacy conflict

The `PrivacyPreservingSurveillance` design publishes **metadata only** to ICN, not raw
video. Metaverse scene rendering requires **raw frames**. These are incompatible as
written.

A `MetaverseConsentVC` was proposed as the mechanism but not specified.

**Blocks:** stage 5 of DC-SIM-006 (people-sensing hardware). PIPEDA exposure begins the
moment any people-sensing device is deployed with real users, and this conflict must be
resolved in writing before that.

---

## 6. SHI / sensing / connectivity documents never unified

Established previously: the SHI node specification, the spatial sensing taxonomy
(Levels 1–5), and the Li-Fi/FSO connectivity architecture were developed in separate
sessions and never reconciled into a single document.

Findings on record: the SHI node and the home node are the same product; the SHI BOM caps
residential sensing at Levels 1–3; Level 4/5 sensing belongs to campus and commercial
deployment under DC-SENSE-SERVICE-001; Li-Fi is an optional residential add-on not in the
base BOM; FSO is ISP-layer outdoor backhaul at neighbourhood scale.

A three-profile node taxonomy (residential SHI / commercial-campus / high-security-
research) was **proposed but not confirmed**. It remains a suggestion, not a decision.

**Impact on the emulation programme:** low. **Impact on documentation coherence:**
significant, and it is the same category of gap as item 1 — parallel design work in
separate sessions producing overlapping, unreconciled specifications.

---

## 7. Recommended order of resolution

1. **Item 2 (FCN)** — one page, blocks node configuration
2. **Item 1 (which ISP, and the A/B relationship)** — largely decided above; confirm
3. Items 3–6 — before their respective DC-SIM-006 stages, not before the v1 build
