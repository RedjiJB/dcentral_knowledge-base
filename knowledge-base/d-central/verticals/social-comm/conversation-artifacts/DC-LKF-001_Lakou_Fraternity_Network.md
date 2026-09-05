---
source_conversation_uuid: fc020b40-bb25-4a3d-ba2f-108c10cbc480
conversation_title: 'Creating third places for men'
created_at: 2026-07-28T16:25:57.255969Z
doc_id: DC-LKF-001
description: "Full specification document for the D-Central men's fraternity/social club vertical"
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-LKF-001: Lakou Fraternity Network
**D-Central Ecosystem — Vertical Specification**
**Author:** Toussaint Redji Jean Baptiste
**Status:** Draft v1
**Prefix:** DC-LKF (Lakou Fraternity)

---

## 1. Purpose

Lakou Fraternity Network (LKF) is the D-Central vertical for men's social infrastructure — a
distributed network of physical spaces (homes, shops, gyms) where members gather for
traditional male-social activities (cigar lounges, bike/tool repair, boxing, card nights,
mentorship circles) that have largely disappeared from modern life.

LKF applies the Lakou compound principle — communal space, shared obligation, mutual
support — to physical third-place networking, governed through the existing D-Central
Fractal DAO structure rather than a centralized club or franchise model.

**Core problem addressed:** the collapse of traditional male third places (barbershops as
social anchors, workshops, fraternal lodges) and the resulting isolation/stress that
comes with losing them.

---

## 2. Position in the D-Central Ecosystem

| Layer | Existing D-Central Component | LKF Usage |
|---|---|---|
| Identity | W3C DID / VC | One credential works across every LKF node |
| Governance | Fractal DAO, Tier 1 (Local) | Activity proposals & votes at node/neighborhood level |
| Governance | Fractal DAO, Tier 2 (Regional) | City-wide coordination, node onboarding, disputes |
| Access Control | SHI node / HID-style access | Optional real-world door/lock integration for after-hours use |
| Economic | Lakou Protocol (banking) | Shared equipment fund, dues, host reimbursement vault |
| Reference Model | D-FIELD stakeholder-weighted voting | Space Contributor weighting reused for LKF hosts |

LKF does not require its own blockchain or new primitives — it is a **social/scheduling
application layer** on top of governance and identity systems that already exist.

---

## 3. Node Types

A "node" is any physical space hosting activities. Spaces are contributed voluntarily by
members, not owned by the network.

| Node Type | Example | Typical Activities |
|---|---|---|
| **Home Lakou** | A member's garage, basement, backyard | Cigar lounge, cards/dominoes, grilling, whiskey tasting |
| **Shop Lakou** | Bike shop, barbershop, auto garage, woodshop | Repair clinics, skill-trade nights, tool restoration |
| **Gym Lakou** | Boxing gym, martial arts club, weight room | Sparring, technical sessions, open mat, strength training |
| **Public Lakou** | Park, community hall, rented hall | Larger events — guest speakers, tournaments, cookouts |

Each node registers with:
- Host identity (DID)
- Location + capacity
- Available equipment/space type
- Recurring vs. one-off availability
- Access method (open, host-present-only, keyed/automated)

---

## 4. Membership & Identity

- Every member holds a **D-Central DID** — one identity across all nodes and all D-Central
  verticals (banking, ISP, LKF, etc.)
- No paperwork or app-switching to join an activity at a new node
- **Reputation score** accrues from attendance, hosting, and mentorship contribution —
  not from money. This determines proposal weight and priority access to
  gear/scheduling, not status or hierarchy.
- Verification tier options: open (self-attested), vouched (existing member vouches),
  or verified (ID-checked) — hosts can set minimum tier required to use their space.

---

## 5. Governance Model

Reuses the existing Fractal DAO Tier 1/Tier 2 structure — no new governance software
required.

### 5.1 Activity Proposals (Tier 1 — Local)
1. Any member proposes an activity: type, node, date/time, capacity.
2. Host of the proposed node gets **elevated voting weight** on proposals involving
   their own space (consistent with the Space Contributor model from D-FIELD).
3. 48–72 hour voting window.
4. Simple majority passes for one-off events.
5. **Recurring activities** (weekly boxing, monthly cigar night) auto-approve after
   establishing a pattern — same auto-approve-on-policy-match logic as
   D-Central's Tier 1 policy engine.

### 5.2 Node Onboarding & Disputes (Tier 2 — Regional)
- New node registration reviewed at the city/regional level (prevents unsafe or
  bad-faith space listings).
- Disputes (property damage, conduct issues) escalate to Tier 2 for resolution —
  keeps day-to-day activity voting fast while reserving serious issues for a
  higher, slower-moving body.

### 5.3 Voting Method
- One member, one vote for general activity proposals (not stake-weighted —
  this is social infrastructure, not a financial vault).
- Host-weighting applies only to proposals concerning their own node.

---

## 6. Activity Taxonomy

| Category | Examples |
|---|---|
| **Craft / Hands** | Bike repair, small engine repair, woodworking, leatherworking, knife sharpening, tool restoration |
| **Social / Traditional** | Cigar lounge, whiskey/beer tasting, poker/dominoes/chess nights, barbershop hangout |
| **Physical / Stress Relief** | Boxing, Kali/martial arts, sparring nights, pickup sports, sauna/cold plunge |
| **Mentorship / Skill Transfer** | Trades night, fatherhood circles, career/finance talks, guest speakers |
| **Seasonal / Large Events** | Grilling competitions, tournaments, community cookouts |

Node hosts tag which categories their space supports; the app surfaces relevant
proposals to members based on interest and proximity.

---

## 7. Economic Layer (Optional, via Lakou Protocol)

- **Shared Equipment Fund** — a simple community vault module (reuses Lakou Protocol
  SavingsCircle/susu pattern) pooling small recurring dues.
- **Host Reimbursement** — hosts can request reimbursement for consumables
  (cigars, food, tool wear) from the fund via the same proposal/vote flow.
- Entirely optional per node/region — cash-free informal nodes (a guy's garage, no
  dues) are just as valid as funded ones.

---

## 8. Technical Components Needed

| Component | Reuse or Build |
|---|---|
| DID/VC identity | **Reuse** — existing D-Central identity layer |
| Fractal DAO proposal/vote engine | **Reuse** — existing Tier 1/2 governance contracts |
| Lakou Protocol vault (equipment fund) | **Reuse** — new vault type, existing module framework |
| Node registry + scheduling UI | **Build** — new lightweight app screen (calendar + map of nodes) |
| Access control integration | **Build (optional)** — bridges to SHI node / HID-style locks for automated after-hours access |
| Reputation/attendance tracking | **Build** — small service tracking check-ins via DID |

Roughly 80% of the governance/identity/economic backbone already exists in your
ecosystem. The new build surface is mainly the scheduling/map UI and the
attendance-tracking service.

---

## 9. Phased Rollout

1. **Phase 0 — Manual pilot:** 5–10 nodes (your own gym, a few homes, one shop),
   activities coordinated in a group chat, no app yet. Validates demand and
   activity mix.
2. **Phase 1 — Minimum app:** Node registry + proposal/vote flow + calendar view,
   using existing DID auth. No equipment fund yet.
3. **Phase 2 — Economic layer:** Turn on shared equipment fund vault for nodes that
   want it.
4. **Phase 3 — Access integration:** For shop/gym nodes wanting automated
   after-hours access, bridge to SHI-style access control.
5. **Phase 4 — Regional expansion:** Tier 2 governance activates once multiple
   neighborhoods/cities have active node clusters.

---

## 10. Open Questions for Next Iteration

- Should LKF be open membership or invite/vouch-only at launch (affects trust and
  liability for home-hosted nodes)?
- Insurance/liability model for home-hosted activities (especially anything involving
  tools, sparring, or alcohol)?
- Should Ottawa be the reference implementation city (parallel to Sod Boys Ottawa for
  D-FIELD)?
