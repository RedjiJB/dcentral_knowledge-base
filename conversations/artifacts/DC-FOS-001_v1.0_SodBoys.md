---
source_conversation_uuid: 7963735d-a671-4b42-806e-651377fd29b2
conversation_title: 'Fixing operational visibility in decentralized construction'
created_at: 2026-06-10T01:34:30.970459Z
doc_id: DC-FOS-001
description: 'D-Central Field Operations Stack architecture document for Sod Boys Ottawa'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# D-FIELD: D-Central Field Operations Stack
## Reference Implementation: Sod Boys Ottawa
**Registry ID:** DC-FOS-001 v1.0  
**Classification:** D-Central Field Cooperative Layer  
**Status:** Architecture Draft  
**Date:** 2026-06-09  

---

## 1. Executive Summary

Sod Boys Ottawa presents with six operational failures: missing equipment, low productivity, missed deadlines, underutilized heavy machinery, client miscommunication, and broken crew logistics. These are not six separate problems. They share one root cause: **centralized star topology**.

All coordination routes through the owner. Every crew, asset, and job is a leaf node that cannot communicate with any other leaf without routing through the centre. The owner is not failing to manage — the architecture itself is the failure.

**D-FIELD** replaces that topology with a **cooperative operational mesh**. Information and decisions live at the edge. Every node publishes its own status. The owner becomes an exception handler rather than the default router. This is the first D-Central Field Operations Stack deployment — the same sovereign cooperative principles applied at the field operations scale.

---

## 2. The Problem as Architecture

```
CURRENT STATE (broken star topology):

            OWNER
           / | \ \
         /   |  \  \
     Crew  Crew  Machine  Client
      ↑                     ↑
      └──── no direct ───────┘
            comms

Every decision, every update, every question routes through one person.
Owner unavailable = full network degradation.
```

```
TARGET STATE (D-FIELD cooperative mesh):

  OWNER [exception handler only]
            ↕
     [D-FIELD Operational Hub]
      ↕         ↕         ↕
  Crew Nodes ←→ Asset Nodes ←→ Job Sites
      ↕               ↕            ↕
  D-MOVE          D-SUPPLY      D-CLIENT
  (mobility)      (materials)   (client portal)

No single point of failure.
Any node added or removed without breaking the mesh.
Owner sees exceptions, not routine updates.
```

---

## 3. Seven Operational Layers

### Layer 1 — D-MESH: Crew Node Network
*"Every crew member is a sovereign edge node."*

Each crew member runs a **mobile Progressive Web App (PWA)**. No app store, works offline, syncs automatically when connected. The app is their identity, their comms channel, and their real-time window into the full operational picture.

**Each node publishes:**
- Current status: `yard | in-transit | on-site | off-shift`
- Current location (on-shift only, auto-off at shift end, opt-in)
- Current job assignment
- Any active blocker flag

**Each node reads:**
- All active job cards with live status
- Every crew member's current status
- Every machine and tool's location and state
- Incoming mobility requests from D-MOVE
- D-CRED balance and leaderboard

**Design constraint:** Works with muddy gloves. One-handed. 30-second maximum interaction. Tolerant of dead zones (offline-first). If the crew doesn't get something back — fewer calls, less confusion — they route around it. Every screen earns its place.

---

### Layer 2 — D-MOVE: Cooperative Mobility Protocol
*"No crew member and no material gets stranded."*

This is the carpool, equipment transport, and material logistics layer. Sod Boys' workforce is physically distributed every morning and every evening. D-MOVE coordinates that flow without a dispatcher.

#### 2a. Crew Carpool Matching

Sod Boys runs multiple sites simultaneously. Not every crew member has a vehicle. D-MOVE handles the pickup mesh automatically.

**How it works:**
1. Each shift generates a **Mobility Event** per job site
2. Drivers register their vehicle: available seats, trailer hitch Y/N, can carry tools Y/N
3. Crew without transport post their pickup point and window ("6:45am, corner of X and Y")
4. D-MOVE generates optimal **pickup chains** — not just one-to-one pairs, but full chains: one driver can collect 2–3 people on the way to site with a single optimized route
5. Driver receives turn-by-turn routing with all stops loaded
6. Each pickup confirmed by both: driver taps "Loaded", crew taps "On board"
7. System knows when every crew member is confirmed en-route

**D-MOVE carpool earns D-Credits** (see Layer 7) — driving others is a cooperative contribution.

#### 2b. Equipment Transport

Machines don't drive themselves. Trailers and tow vehicles are registered assets. Every equipment move generates a **Load Manifest**: machine ID, attached tools, destination site, driver, ETA.

- Driver confirms load at yard (QR scan on machine + trailer)
- Receiving crew at site confirms delivery (QR scan confirms arrival)
- End-of-day return logged separately
- **Machine stranded alert:** If a job closes and no return transport is logged within 2 hours, an alert fires — catches the "forgot the skid steer" problem before it becomes a missed deadline the next day

#### 2c. Material Transport

Supplier deliveries and inter-site material moves tracked end-to-end.

- **Inbound deliveries** entered with supplier, material type, quantity, expected ETA
- Crew at site confirms receipt: timestamp + photo (30 seconds)
- No confirmation within 1 hour of ETA → automatic alert fires before crew discovers it on arrival
- **Inter-site transfer:** "Site A has 40 leftover sod pallets, Site B is short" → D-MOVE identifies any driver routing nearby and assigns the transfer
- Waste and damage logged at delivery, not discovered after the fact

---

### Layer 3 — D-ASSET: Machine & Equipment Registry
*"Every asset has a digital twin with a real-time pulse."*

Every skid steer, sod cutter, roller, trailer, compactor, and major hand tool is a registered asset with a live status.

**Asset states:**
`yard | in-transit | on-site | maintenance | missing`

**Check-in/out:**
QR code (sticker on machine) or NFC tap. Scan at yard on departure, scan at site on arrival. 5-second interaction. Updates the asset's digital twin immediately.

**Machine dispatch:**
When a site needs a machine not currently assigned:
1. Site submits a **dispatch request** with urgency level
2. System scores available machines by: proximity + job urgency + current utilization
3. Owner or foreman approves with one tap
4. D-MOVE is notified to route a trailer and driver

**Maintenance flagging:**
Any crew member can flag a machine: "This skid steer is pulling left — needs inspection." Photo attached. Machine immediately shows a yellow status on all views. Owner sees it instantly without a phone call.

**Utilization report (weekly):**
Where every machine spent its hours. Identifies which assets are chronically underutilized (parked while other sites wait) and which are being overworked. This alone solves the "not at enough sites" problem — it reveals the scheduling gap rather than hiding it.

---

### Layer 4 — D-JOB: Site Operations Layer
*"Each active job is a temporary cooperative unit that spins up and winds down."*

Every active job has a **live job card** accessible to all crew. The job card is the shared operational truth for that site.

**Job card contains:**
- Site address + client name + access instructions
- Assigned crew (with real-time status from D-MESH)
- Assigned machines and tools (pulled from D-ASSET)
- Materials manifest (pulled from D-SUPPLY)
- Progress milestones with completion timestamps

**Standard milestone chain:**
```
Grading confirmed → Sod delivery confirmed → Install in progress
→ Install complete → Cleanup done → Client sign-off
```

- Active blockers (any crew member can post with photo)
- Client portal link (generated automatically, from D-CLIENT Layer 6)

**Pre-Roll Readiness Gate:**

Before any crew routes to a site, a 30-second readiness checklist must clear:

- [ ] Materials confirmed at site (from D-SUPPLY)
- [ ] Site access confirmed (gate code, contact number known)
- [ ] Machine assigned and en-route (from D-ASSET)
- [ ] Crew transport confirmed (from D-MOVE)

If the gate is incomplete, D-MOVE does not dispatch crew. This catches the single largest productivity killer in field operations: five people driving 40 minutes to a site that isn't ready. The gate is preventive, not punitive.

**Job lifecycle:**
Job opens → Pre-roll gate clears → Crew dispatched → Milestones logged → Client signs off → Job closes, assets released back to yard status.

---

### Layer 5 — D-SUPPLY: Material Flow Protocol
*"Nothing runs out on site without a warning firing first."*

Sod and materials tracked from purchase order through delivery through installation.

**Job manifests:** Every job has a required materials list: sod quantity (pallets), topsoil (cubic yards), edging, seed, accessories. This manifest is the benchmark everything is measured against.

**Delivery tracking:**
- Supplier deliveries matched against manifest quantity
- Shortfall detection: confirmed delivery < manifest requirement → alert fires before crew drives out
- Surplus logging: excess materials tracked for inter-site transfer via D-MOVE

**Yard inventory:**
- Stock levels updated as materials leave the yard
- Horizon alert: "Jobs booked for next week require 900 pallets of sod. Yard currently holds 180."
- Reorder trigger threshold set per material type (owner configures)

**Waste/damage log:**
Crew logs damaged or non-conforming material at receipt (photo + quantity). This feeds supplier accountability data and prevents disputes about what arrived vs what was used.

---

### Layer 6 — D-CLIENT: Cooperative Transparency Stack
*"The client is a read-only node on the network."*

Borrowed directly from the D-Central Cooperative Transparency Stack (CTS). Every client job generates a unique read-only URL at booking time. No login, no app download — just a link sent by text.

**Client view shows:**
- Crew status: `Crew confirmed → En-route → On site → Wrapping up → Complete`
- Current milestone (plain language: "Sod installation underway")
- ETA (derived from D-MOVE data when crew is en-route)
- Photo log: crew uploads a photo on each milestone (yard before, install in progress, cleanup complete)
- **Client sign-off button:** Client taps to confirm completion. This closes the job and triggers any invoicing workflow.

**What this eliminates:**
- "Where are your guys?" calls: answered by the link
- Missed expectations: client sees exact status in real time
- Disputed completions: photo evidence timestamped at each milestone
- Owner as comms relay: owner is removed from this loop entirely

---

### Layer 7 — D-CRED: Internal Credit Economy
*"Cooperative behavior gets reinforced, not just expected."*

A lightweight internal incentive layer to drive adoption and reward the behaviours the cooperative mesh depends on. This is the D-Credit concept scoped to a field team — same architecture, same philosophy, same upgrade path to a full on-chain layer as the company scales.

**Earn D-Credits for:**
| Action | Credits |
|--------|---------|
| Driving crew to site (per person) | 10 per person delivered |
| Completing pre-roll checklist on time | 15 |
| Logging milestone update within 15 min | 5 |
| Confirming material delivery with photo | 10 |
| Flagging a blocker before it becomes a miss | 20 |
| On-time site arrival (crew + machine) | 10 |
| End-of-day machine return logged | 10 |

**Redeem D-Credits for:**
- First pick of next week's shift schedule
- Bonus pool share at end of season
- Extra PTO day
- Owner-set gift card redemptions (Tim's, tools, etc.)

**Visibility:**
- Each crew member sees their own balance and rank
- Opt-in leaderboard (crew can choose to show or hide ranking)
- Owner sees team-wide credit distribution — gives a clear picture of who's actually carrying cooperative weight

This layer makes the system self-sustaining. The crew has a reason to update milestones, confirm deliveries, and drive each other — beyond being told to.

---

## 4. Full System Topology

```
                    ┌─────────────────────────────────┐
                    │         OWNER DASHBOARD          │
                    │   [Exception handler only]        │
                    │   Sees: blockers, approvals,      │
                    │   dispatch requests, utilization  │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │         D-FIELD HUB              │
                    │     [Single source of truth]      │
                    │  All jobs · All assets · All crew │
                    └──┬──────┬──────┬──────┬──────┬──┘
                       │      │      │      │      │
              ┌────────▼┐ ┌───▼──┐ ┌▼────┐ ┌▼───┐ ┌▼───────┐
              │D-MESH   │ │D-JOB │ │D-   │ │D-  │ │D-      │
              │Crew     │ │Site  │ │MOVE │ │    │ │CLIENT  │
              │Nodes    │ │Ops   │ │Mobi │ │ASSE│ │Portal  │
              └────┬────┘ └──┬───┘ │lity │ │T   │ └────────┘
                   │         │     └──┬──┘ └─┬──┘
                   └────────►│◄───────┘       │
                             │◄───────────────┘
                    ┌────────▼───────────┐
                    │     D-SUPPLY       │
                    │  Material Flow     │
                    └────────────────────┘
```

---

## 5. Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Frontend | React PWA + Tailwind CSS | Offline-first, no app store, any phone |
| Offline sync | PouchDB ↔ CouchDB | Dead zones on site — crew keeps working, syncs later |
| Backend | Node.js + Fastify | Lightweight, fast, self-hostable |
| Database | PostgreSQL | Structured operational data, robust backup |
| Maps & routing | OpenStreetMap + OSRM | Free, self-hostable, zero API fees |
| SMS fallback | Twilio | For crew with limited data, sends alerts as SMS |
| QR asset tags | Web QR scan + NFC tap | 5-second check-in/out on any phone |
| Authentication | 4-digit PIN + crew profile | Zero barrier to entry; upgradeable to W3C DID |
| Push notifications | Web Push API | Fires even when app is closed |
| Hosting | $12–20/mo VPS or on-prem RPi 4 | Company owns their own data, no SaaS lock-in |

**Monthly infrastructure cost: $12–$25.**  
No per-seat fees. No vendor lock-in. The company owns the stack and all operational data.

---

## 6. Rollout: Vertical Slices

Each slice ships independently useful value. No slice requires the previous one to be fully adopted before deployment.

| Slice | D-Central Layer(s) | Delivers | Estimated Timeline |
|-------|-------------------|---------|-------------------|
| 1 | D-JOB + D-MESH | Live job board + crew status | Week 1–2 |
| 2 | D-MOVE | Carpool matching + equipment transport | Week 3–4 |
| 3 | D-ASSET | Machine & tool check-in/out (QR) | Week 5–6 |
| 4 | D-CLIENT | Client read-only portal + sign-off | Week 7 |
| 5 | D-SUPPLY | Material delivery tracking + alerts | Week 8–10 |
| 6 | D-CRED | Internal credit economy + leaderboard | Week 10–12 |

**Slice 2 (D-MOVE) is the unlock.** Solving crew transport and material logistics is the most visible day-one improvement for the crew. Ship it early.

---

## 7. Impact Matrix

| Original Problem | D-FIELD Layer | Mechanism |
|-----------------|--------------|-----------|
| Missing equipment | D-ASSET | Real-time location + QR check-in/out |
| Low productivity | D-JOB + D-CRED | Pre-roll gate blocks wasted drives; credits reward readiness |
| Missed deadlines | D-JOB + D-SUPPLY | Milestone tracking + shortfall alerts before crew deploys |
| Machines not at enough sites | D-ASSET + D-MOVE | Utilization reports + dispatch scoring |
| Client miscommunication | D-CLIENT | Real-time read-only portal eliminates phone relays |
| Crew can't get to sites | D-MOVE | Pickup chain matching, driver incentives via D-CRED |
| Material transport | D-MOVE + D-SUPPLY | Load manifests, inter-site transfer matching |
| Owner as central router | All layers | Every layer removes a category of decision from the owner's plate |

---

## 8. D-Central Ecosystem Alignment

| D-Central Concept | D-FIELD Application |
|------------------|-------------------|
| Sovereign edge nodes | Each crew member = autonomous node with local state |
| Cooperative mesh topology | Crew ↔ Asset ↔ Site ↔ Client direct communication |
| D-Credit micro-economy | Cooperative field behavior incentivized via internal credits |
| D-MOVE / DCOT | Crew carpool chains + equipment logistics protocol |
| Lakou Protocol principles | Community resource pooling (vehicles, machines, materials) |
| Cooperative Transparency Stack | D-CLIENT read-only portal layer |
| Sovereign data infrastructure | Self-hosted stack, no third-party data dependency |
| DAO-lite operations | Pre-roll readiness gate + collective issue flagging |
| No single point of failure | Owner removed from routine coordination entirely |
| Asset registry | D-ASSET digital twin per machine and tool |
| Upgrade path | PIN auth → W3C DID; internal credits → on-chain D-Credit |

---

## 9. What This Changes for the Owner

**Before D-FIELD:**
The owner is the central router. Every crew call, every "where's the machine" question, every client update, every schedule conflict routes through one phone. Unavailability degrades the entire network. Growth is impossible beyond what the owner can personally coordinate.

**After D-FIELD:**
The owner sees one dashboard. It shows:
- Jobs green / jobs with active blockers
- Machine dispatch requests pending
- Client sign-offs received
- Crew D-Credit leaderboard

That is a 5-minute morning check. Not 25 phone calls.

The owner's cognitive load drops from operational coordination to strategic oversight. That is the precondition for the company to scale.

---

## 10. Registry Classification

```
Document ID:     DC-FOS-001
Version:         1.0 (Architecture Draft)
Domain:          Field Operations
Stack:           D-Central Cooperative Field Layer
Implementation:  Sod Boys Ottawa (Reference Deployment)
Layers:          7 (D-MESH, D-MOVE, D-ASSET, D-JOB, D-SUPPLY, D-CLIENT, D-CRED)
Upgrade path:    Full D-Central sovereign infrastructure (D-Credit on-chain, W3C DID auth)
```

---

*D-FIELD is the field operations expression of D-Central's core principle: no single point of failure, every node sovereign, the cooperative stronger than any individual link.*
