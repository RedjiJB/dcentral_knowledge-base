---
source_conversation_uuid: 7963735d-a671-4b42-806e-651377fd29b2
conversation_title: 'Fixing operational visibility in decentralized construction'
created_at: 2026-06-10T01:34:30.970459Z
doc_id: DC-COOP-001
description: 'Complete D-Central cooperative transformation blueprint for Sod Boys Ottawa - DC-COOP-001'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-COOP-001: D-Central Cooperative Transformation Protocol
## Complete Company Reconstruction — Sod Boys Ottawa
**Registry ID:** DC-COOP-001 v1.0  
**Classification:** D-Central Field Cooperative — Reference Implementation  
**Parent Documents:** DC-FOS-001 (Field Operations Stack), DC-MONETARY-001, DC-LKB-001  
**Status:** Architecture Draft v1.0  
**Date:** 2026-06-09  

---

## Transformation Thesis

The Sod Boys as they exist today are a **resource pool organized as a monarchy**. The owner holds all capital, all knowledge, all relationships, all authority, and all risk. The crew executes. The company cannot grow beyond what one person can supervise, and it cannot survive anything that person cannot absorb.

D-Central does not add software to this company. D-Central **restructures its power topology** — redistributing ownership, decision-making, economic upside, and operational intelligence across every node in the network. The result is not a better-managed sod company. It is a **sovereign cooperative field enterprise** that happens to lay sod.

This document is organized in ten tiers, from the legal foundation to the network growth layer. Every tier builds on the one below it. Remove any tier and the structure above it becomes unstable. The owner decides which tiers to implement and which to defer — but the dependencies are documented so the costs of deferral are visible.

---

## Tier 0: Entity Reconstruction

### 0.1 Current State
Standard small business structure: owner as sole authority, crew as employees. All equity, liability, and profit concentrated in one person.

### 0.2 Target Structure: Ontario Worker Cooperative

Under the **Ontario Co-operative Corporations Act (R.S.O. 1990, c. C.35)**, Sod Boys incorporates as a **worker cooperative**. This is a legal entity in which the workers are the members and the owners.

**Why this structure:**
- Crew become co-owners with a genuine stake in company performance
- Profit sharing is legally structured, not discretionary
- Decision-making authority is distributed by design, not by goodwill
- Qualifies for cooperative development grants (Ontario Cooperative Development Fund, federal supports)
- Preserves the founder's management role and majority stake during transition

**Founding Member Classes:**
| Class | Who | Rights |
|-------|-----|--------|
| Founder Share | Original owner | Management authority, veto rights (5-year sunset), premium profit share, founding equity |
| Worker Member | Full crew members (post-probation) | Voting rights, equity accumulation, profit share, proposal rights |
| Candidate Member | First-season crew | Base pay, D-Credit earning, no vote, path to full membership |
| Community Member | Clients, suppliers, community partners | Advisory, loyalty D-Credits, no governance rights |

**Transition timeline:**
- Year 1: Owner retains founder authority; crew enters as candidate members
- Year 2: First crew cohort achieves full worker membership
- Year 3: First cooperative assembly with full voting rights
- Year 5: Founder veto right sunsets; fully cooperative governance

### 0.3 Founding Charter Principles

```
SODB-CHARTER-001 (encoded in DC-COOP-001)

1. One mission: deliver excellent field work while building shared wealth.
2. Every member's labor is capital. Time logged builds equity.
3. All operational data belongs to the cooperative, not any individual.
4. No member may hold information that gives them structural advantage over others.
5. The cooperative's machines are held in common.
6. Growth must not dilute founding member equity without consent.
7. Every season ends with a public account: what we earned, what we spent, what we share.
```

---

## Tier 1: Identity Infrastructure

### 1.1 D-ID: Sovereign Member Identity

Every participant in the Sod Boys cooperative network receives a **W3C Decentralized Identifier (DID)**. This is not a user account in a database — it is a portable, self-sovereign identity controlled by the individual, anchored on a lightweight DID registry.

**D-ID types:**
- `did:dcoop:crew:{uuid}` — worker member or candidate
- `did:dcoop:client:{uuid}` — client community member
- `did:dcoop:asset:{uuid}` — machine or major tool
- `did:dcoop:site:{uuid}` — job site with persistent property record
- `did:dcoop:supplier:{uuid}` — supplier relationship identity

**Each crew DID contains verifiable credentials for:**
- Cooperative membership status and class
- D-Credit balance and history
- Certifications and training completed (WHMIS, equipment operation, pesticide application)
- Work history within the cooperative (seasons, hours, roles)
- Equity stake as of last season close

**Portability matters:** If a crew member leaves and joins another D-Central field cooperative in the network, their DID and its credentials travel with them. Their work history, their training, their D-Credits are theirs — not the company's property.

**Client DIDs (lite):**
Clients don't need to understand DIDs. They receive a persistent identity in the system that holds their property record, job history, preferences, and loyalty D-Credits. It behaves like a loyalty account. Under the hood it's sovereign identity infrastructure.

### 1.2 Credential Registry

| Credential | Issued By | Required For |
|-----------|----------|-------------|
| Cooperative Member | Sod Boys Cooperative | Full voting rights, profit share |
| Equipment Operator (Class A/B/C) | Foreman assessment | Operating assigned machines |
| WHMIS 2015 | Third-party or internal | Any crew role |
| Pesticide Applicator | Ontario Ministry | Weed/pest treatment sites |
| D-MOVE Driver | Platform (clean record + review) | Driving crew, hauling equipment |
| Site Lead | Foreman + member vote | Running a site independently |

All credentials are cryptographically signed, stored in the DID, and verified by the platform automatically when a crew member is assigned a task requiring them.

---

## Tier 2: Economic Architecture

### 2.1 Cooperative Treasury (Lakou Protocol Lite)

Revenue flows through a transparent cooperative treasury before any distribution. This is the **Lakou Protocol (DC-LKB-001)** scoped to a small field cooperative — same architecture, lite implementation.

**Revenue flow:**
```
CLIENT PAYMENT
      ↓
COOPERATIVE TREASURY
      ↓
┌─────────────────────────────────────────────┐
│  Operating Costs (materials, fuel, equip)   │ → paid first
│  Base Pay Pool (all crew, hourly rate)       │ → paid weekly
│  Equipment Reserve Fund (15%)                │ → machine replacement
│  Growth Fund (10%)                           │ → expansion capital
│  Cooperative Profit Pool (remainder)         │ → distributed quarterly
└─────────────────────────────────────────────┘
```

**Treasury transparency:** Every cooperative member can see the full treasury ledger in real time. Revenue per job, costs per job, crew hours logged, fund balances. No financial opacity — this is the founding charter principle in practice.

**Multi-signature treasury governance:**
Three keyholders required for disbursements over a threshold:
- Owner/Founder (key 1)
- Elected Crew Representative (key 2)
- Automated rule engine (key 3 — fires on payroll cycles, routine payments)

Large disbursements (equipment purchase, expansion) require all three.

### 2.2 D-Credit Economy

The **D-Credit** is the cooperative's internal value unit. It is not a cryptocurrency for v1 — it is a transparent point system with real economic consequences. It upgrades to on-chain D-Credit when the cooperative joins the broader D-Central network.

**Earning D-Credits (crew):**
| Action | Credits |
|--------|---------|
| Driving crew to site (per person delivered) | 10 |
| Completing pre-roll readiness gate | 15 |
| Logging milestone within 15 min | 5 |
| Confirming material delivery with photo | 10 |
| Flagging a blocker before it cascades | 20 |
| Perfect attendance (week) | 25 |
| Training a new crew member | 50 |
| Submitting a successful cost-saving proposal | 100 |
| Full season completion (candidate → member) | 500 |

**Earning D-Credits (clients):**
| Action | Credits |
|--------|---------|
| Referral that converts to job | 200 |
| Repeat booking within season | 50 |
| Early payment (before due date) | 25 |
| Community member upgrade | 100 |
| 5-star review posted | 30 |

**Redeeming D-Credits (crew):**
| Redemption | Cost |
|-----------|------|
| Schedule priority (first pick next week) | 50 |
| Bonus cash payout ($10) | 100 |
| Equity share conversion (end of season) | 1000 = 0.1% stake |
| Extra day off (owner approval) | 300 |
| Equipment purchase contribution vote | 500 |

**Redeeming D-Credits (clients):**
| Redemption | Cost |
|-----------|------|
| 5% discount next job | 100 |
| Free lawn assessment | 150 |
| Priority scheduling (peak season) | 200 |
| Community member rate (co-op pricing) | 500/year |

### 2.3 Cooperative Profit Sharing

At the end of each quarter (and season final), the profit pool is distributed:

**Distribution formula:**
```
Member's share = (Member's labor hours / Total cooperative labor hours) × Profit Pool

Adjusted by:
  × D-Credit multiplier (credits earned / average crew credits, max 1.3×)
  × Tenure multiplier (year 1: 1.0×, year 2: 1.1×, year 3+: 1.2×)
```

The founder holds a **Founder Dividend** (fixed percentage of profit, declining over 10 years as crew equity builds up) plus their labor share.

### 2.4 Equipment Cooperative

Heavy machinery is held **cooperatively**, not by the owner personally.

**Equipment ownership model:**
- Existing equipment: appraised at market value → owner receives cooperative bonds (paid out of future profit) → equipment enters cooperative commons
- New equipment: financed through growth fund + cooperative bonds (members can invest)
- Depreciation: tracked transparently in the asset registry (D-ASSET)
- Fully depreciated machines: zero cost to operations, remain in cooperative commons
- Maintenance budget: line item in operating costs, visible to all members

**Equipment cooperative participation:**
Sod Boys can pool equipment with other D-Central field cooperatives in Ottawa. Machines not in use can be rented to partner cooperatives through the D-MARKET layer, generating passive revenue.

---

## Tier 3: Governance Architecture

### 3.1 D-AGORA: Cooperative Governance Layer

Every cooperative decision flows through **D-AGORA** — a structured but lightweight governance protocol adapted from the D-Central DAO architecture to the scale of a small seasonal cooperative.

**Four working groups:**
| Group | Mandate | Members |
|-------|---------|---------|
| Operations Circle | Day-to-day ops, job scheduling, equipment dispatch | Site leads + foreman |
| Finance Circle | Treasury management, cost controls, profit sharing | Owner + elected rep + bookkeeper |
| Growth Circle | New clients, new services, expansion | Owner + 2 crew reps |
| Stewardship Circle | Equipment maintenance, training, standards | Crew leads + equipment operators |

**Proposal → Vote → Execute flow:**

```
Any member submits a PROPOSAL
          ↓
2-day comment period (all members can annotate)
          ↓
Working Group reviews + recommends
          ↓
Vote:
  Minor ops decision → Operations Circle votes (majority)
  Financial decision → Finance Circle votes (supermajority)
  Major company direction → All members vote (weighted by hours)
          ↓
Approved → AUTO-EXECUTED (if within working group mandate)
         → FOUNDER APPROVAL (if in founder veto period, first 3 years)
```

**Seasonal Assembly (October — before winter layoff):**
- Full financial transparency: revenue, costs, profit pool disclosed
- Profit sharing distribution vote
- Next season planning (services, equipment, crew targets)
- Governance review (any charter changes)
- D-Credit season final tallied, equity conversions processed

**Governance on mobile:**
Proposals, comments, and votes all happen in the D-MESH app. No crew member should have to attend a formal meeting to participate in governance.

---

## Tier 4: Operations Architecture

*Full expansion of DC-FOS-001 with five additional systems.*

### 4.1 D-MESH — Crew Node Network
*(From DC-FOS-001 — unchanged)*
Each crew member is a sovereign edge node. PWA, offline-first, real-time status, full operational visibility.

### 4.2 D-MOVE — Cooperative Mobility Protocol
*(From DC-FOS-001 — unchanged)*
Crew carpool chains, equipment transport manifests, material inter-site transfer, D-Credit rewards for driving.

### 4.3 D-ASSET — Machine & Equipment Registry
*(From DC-FOS-001 — enhanced)*
Digital twin per asset. QR/NFC check-in/out. Dispatch scoring. Maintenance flags.

**Enhancement: Cooperative asset bonds**
When a new machine is purchased, cooperative members can hold "equipment bonds" — they contribute to the purchase and receive a small share of the machine's utilization revenue back. Makes equipment ownership a community investment.

### 4.4 D-JOB — Site Operations Layer
*(From DC-FOS-001 — enhanced)*
Live job cards. Pre-roll readiness gate. Milestone tracking. Client portal.

**Enhancement: D-QUOTE integration**
Job quotes generated from D-JOB templates. Crew leads can issue quotes from the field. Quote → approved → auto-creates D-JOB card → assigned crew and assets.

### 4.5 D-SUPPLY — Material Flow Protocol
*(From DC-FOS-001 — enhanced)*
Delivery confirmation, shortage detection, inter-site transfers, waste logging.

**Enhancement: Cooperative purchasing**
Aggregate material orders across multiple jobs and across partner cooperatives to hit bulk pricing thresholds. The system automatically identifies when combining upcoming orders would hit a discount tier.

### 4.6 D-CLIENT — Cooperative Transparency Stack
*(From DC-FOS-001 — unchanged)*
Read-only client portal per job. Crew status, ETA, photos, client sign-off.

### 4.7 D-CRED — Internal Credit Economy
*(From DC-FOS-001 — promoted to Tier 2 Economic Architecture)*
Now integrated with equity accumulation and cooperative profit sharing.

### 4.8 D-QUOTE: Cooperative Pricing Engine

Quotes are currently generated by the owner from memory and experience. D-QUOTE captures that knowledge and distributes it.

**D-QUOTE contains:**
- Service catalog (sod installation, seeding, aeration, dethatching, grading — itemized)
- Material cost lookup (live — updated from D-SUPPLY pricing)
- Labor rate calculator (hours × rate × complexity multiplier)
- Site variables (access difficulty, soil type from D-RECORD, distance from yard)
- Margin targets (set by Finance Circle)

Any site lead can generate an accurate quote from a site visit. Quote is submitted for owner approval (one tap) before delivery to client. Over time, as the pricing model matures, site leads can auto-approve quotes under a threshold.

**Result:** The owner is no longer the sole quoting bottleneck. Revenue-generating activity scales.

### 4.9 D-ROUTE: Intelligent Job Routing

Ottawa-specific job routing that minimizes total drive time across the full job schedule.

**D-ROUTE does:**
- Takes all booked jobs for a given week
- Groups jobs by geography (Ottawa East, West, South, Orleans, Kanata, etc.)
- Assigns crew + machines to minimize total daily travel
- Accounts for machine-to-site constraints (which jobs need the skid steer)
- Recommends optimal day-of sequence (sod deliveries need to precede install crew)
- Integrates D-MOVE carpooling into the routing

**The Ottawa-specific problem it solves:**
Without routing, crews drive across the city because jobs are scheduled in the order they were booked. D-ROUTE clusters geographically, cutting total fuel costs by an estimated 25–40% and adding 1–2 additional jobs per crew-day.

### 4.10 D-TRAIN: Crew Development Registry

Tracks every crew member's training, certification, and competency progression.

- Certification tracking (WHMIS, pesticide, equipment operation — expiry alerts)
- Internal training records (equipment checkout sign-offs, site lead mentorship hours)
- Training content library (how to operate each machine, sod installation standards, client interaction protocols)
- Progression pathways: Candidate → Crew → Lead → Foreman → Member (with requirements for each)
- Cross-training incentives (D-Credits for becoming qualified on additional equipment)

**Why this matters:** Right now, if the foreman doesn't show up, the site is stuck. D-TRAIN builds redundancy — multiple crew qualified to lead, multiple crew qualified on every machine.

### 4.11 D-WEATHER: Ottawa Environmental Integration

Ottawa's climate has a direct effect on sod operations. D-WEATHER integrates environmental data into job planning.

- Weather forecast integration per job site (not just "Ottawa" — micro-weather per zone)
- Ground temperature tracking (sod installation viability window)
- Rain delay protocol: auto-flags jobs where rain within 24 hours affects soil prep or new install
- Frost window detection (spring and fall scheduling risk)
- Heat stress alerts (crew welfare in high-heat periods)
- Automatic client communication when weather triggers a delay

---

## Tier 5: Client Architecture

### 5.1 D-CLIENT — Live Job Portal
*(From DC-FOS-001)*
Read-only URL, crew status, ETA, photo log, sign-off.

### 5.2 D-MEMBER: Client Cooperative Community

Clients who join as **Community Members** enter the cooperative network:

- **Persistent property record (D-RECORD):** Every job done at that address is logged — soil quality notes, drainage issues, what sod variety was used, what failed and why. Next season's crew arrives already knowing the site.
- **Locked-in pricing:** Community members get a rate based on the season's cost structure, not market-rate quoting. They're inside the cooperative, not outside it.
- **Priority scheduling:** Community members get first access to peak-season slots (spring install rush, fall aeration)
- **D-Credits:** Earn for referrals, early payment, repeat booking, reviews
- **Neighborhood network effect:** If a community member's street has 3+ cooperative clients, D-ROUTE automatically schedules them together — crew comes to the street, not one house at a time. Each member benefits from their neighbors' membership.

**Community rate applications:**
- Community gardens → cooperative pricing (stewardship value to D-Central mission)
- Neighborhood associations → group contract with D-MEMBER benefits across all member properties
- Housing cooperatives → natural cooperative-to-cooperative relationship

### 5.3 D-RECORD: Property Intelligence

Every job site gets a persistent digital record anchored to its D-ID.

**D-RECORD contains:**
- Soil type and condition notes (drainage issues, compaction, slopes)
- Irrigation system notes (if applicable)
- Previous sod variety (so new install matches or improves on it)
- Pest or disease history
- What work was done, when, by which crew, with what materials
- Photos from each visit
- Client notes and preferences
- Access instructions (gate codes, contact, dog on property)

This is organizational memory that survives crew turnover. A new crew member arrives at a site and the D-JOB card tells them everything the cooperative knows about that address.

---

## Tier 6: Supply Chain Architecture

### 6.1 Supplier Relationship Registry

Every supplier gets a D-ID and a relationship record:
- Material quality ratings (per delivery, per crew)
- Delivery reliability score (on-time rate, shortfall rate)
- Price history (enables negotiation with data)
- Relationship status (preferred, standard, backup)

**Cooperative supplier terms:**
As the cooperative network grows, aggregate purchasing volume unlocks supplier negotiation. The Finance Circle tracks total volume per supplier and flags when volume justifies a renegotiated rate.

### 6.2 Cooperative Purchasing Pool

Across a season, Sod Boys orders predictable volumes of sod, topsoil, edging, seed, and accessories. D-SUPPLY aggregates upcoming orders and identifies bulk discount opportunities:

```
Upcoming orders (next 3 weeks):
  Job A: 80 pallets sod
  Job B: 120 pallets sod
  Job C: 60 pallets sod
  Total: 260 pallets

Supplier threshold for 8% bulk discount: 250 pallets
→ TRIGGER: Consolidate order for 260 pallets, dispatch across jobs
→ Savings this trigger: ~$1,560 at market rate
```

When Sod Boys joins the D-Central field cooperative network (Tier 9), purchasing pools across multiple companies, hitting even higher discount tiers.

### 6.3 Local Sourcing Protocol

Part of the cooperative identity is community rootedness. D-SUPPLY tracks:
- Percentage of materials sourced from Ottawa-region suppliers
- Carbon footprint of material sourcing (distance × weight)
- Indigenous-owned supplier relationships (Algonquin territory acknowledgment in practice, not just on paper)

This becomes a marketing differentiator and a community trust-builder.

---

## Tier 7: Data Sovereignty Architecture

### 7.1 What the Cooperative Owns

Every byte of operational data generated by the cooperative belongs to the cooperative:
- Job records, client records, property records
- Crew performance data, D-Credit histories
- Material costs, supplier pricing, route data
- Weather impact records

No third-party SaaS vendor holds this data. No subscription cancellation can delete the cooperative's operational memory.

### 7.2 Self-Hosted Infrastructure

| Component | Hosting | Backup |
|-----------|---------|--------|
| D-FIELD application | $15/mo VPS (Hetzner or BuyVM) | Daily automated |
| Database (PostgreSQL) | Same VPS | Nightly encrypted off-site |
| Asset QR/NFC tags | Physical (no hosting) | N/A |
| D-RECORD archives | Cold storage (Backblaze B2) | Continuous sync |

**Total monthly infrastructure cost: $15–30.** No per-seat fees. No vendor lock-in.

### 7.3 Data Cooperative Participation

When the cooperative joins the D-Central network, it can opt-in to sharing anonymized operational data (routing efficiency, material pricing, weather impact, job duration) with the D-Central field operations dataset. This dataset helps all D-Central field cooperatives optimize. The cooperative earns D-Network Credits for participation.

---

## Tier 8: Community & Stewardship Architecture

### 8.1 Land Stewardship Protocol

Sod Boys operates on Algonquin Anishinaabe territory (unceded). The cooperative makes this material, not ceremonial:

- Land acknowledgment in all client communications
- Preferred supplier relationship with Indigenous-owned landscaping material companies
- 1% of cooperative profit allocated to Algonquin land stewardship fund (voted annually at Seasonal Assembly)
- Native grass and plant options in service catalog (not just Kentucky bluegrass monoculture)

### 8.2 Sustainability Tracking

| Metric | How Tracked |
|--------|------------|
| Total fuel consumed | D-ASSET vehicle logs |
| Total km driven | D-MOVE routing data |
| Routing efficiency (km per job) | D-ROUTE delta vs unoptimized baseline |
| Material waste per job | D-SUPPLY waste logs |
| Carbon offset (approximate) | Calculation from above metrics |

Annual sustainability report published to all members and clients. Cooperatives attract clients who care about this — the data builds trust.

### 8.3 Crew Welfare Protocol

**Pre-season:** Cooperative purchases group health benefits for all worker members (or contributes to a health spending account). Financed through operating costs line item.

**Heat protocol:** D-WEATHER triggers mandatory rest-and-water breaks when heat index exceeds threshold. Logged in D-JOB. Crew cannot be penalized for heat compliance.

**Off-season support:** The Growth Fund reserves a portion for off-season support payments to returning members (bridges the November–March gap). Amount voted at Seasonal Assembly.

---

## Tier 9: Network Growth Architecture

### 9.1 D-FRANCHISE: Cooperative Field Network

The Sod Boys cooperative becomes the **first node** in a D-Central Field Cooperative Network. Other landscaping, lawn care, and grounds maintenance companies can join the network under a cooperative franchise model.

**What joining the network means:**
- Access to the D-FIELD platform (shared infrastructure, cooperative cost)
- Equipment sharing pool (machines listed in D-ASSET available to network partners)
- Collective purchasing (aggregate volume across all network companies)
- Shared D-TRAIN credential library (training materials, certification tracking)
- Unified D-CLIENT portal design (trusted brand signal for clients)
- D-Credit interoperability (credits earned at one cooperative honored across the network)

**What it does not mean:**
- Network members are independent cooperatives. There is no franchisor extracting royalties.
- Each cooperative controls its own treasury, its own governance, its own client relationships.
- The network is a mesh, not a hierarchy.

**Incentive for Sod Boys to recruit network members:**
D-Network Credits earned for each cooperative onboarded. Equipment rental revenue from network partners. Collective purchasing discounts that benefit Sod Boys even when they don't directly need the other company's capacity.

### 9.2 D-MARKET: Cooperative Capacity Exchange

A marketplace internal to the D-Central field cooperative network:

- **Subcontracting:** Sod Boys has more work than capacity this week → post available work to network → partner cooperative picks it up → Sod Boys earns a coordination fee + D-Credits
- **Machine rental:** Sod Boys' skid steer is idle Thursday → listed on D-MARKET → partner rents it at hourly rate → goes into equipment cooperative revenue
- **Crew sharing:** Partner cooperative has certified machine operator sitting idle, Sod Boys needs one → D-MARKET matches → crew member works at partner for the day → revenue flows back correctly
- **Bulk purchasing trigger:** "If 3 cooperatives each need 100 pallets of sod, we hit the 300-pallet bulk tier" → D-MARKET triggers collective order

### 9.3 D-Central Ecosystem Integration

**D-Credit network integration:**
When the broader D-Central monetary architecture is ready, Sod Boys D-Credits become convertible with D-Credits earned across the D-Central ecosystem. A Sod Boys crew member's earned D-Credits can interact with cooperative housing programs, community gardens, and other D-Central network participants.

**Lakou Protocol full integration:**
When the cooperative reaches sufficient scale, the lite Lakou Protocol treasury upgrades to a full multi-vault Lakou Protocol implementation with on-chain anchoring, sub-1% payment processing fees, and access to D-Central cooperative capital pools for expansion financing.

**D-Central identity:**
Crew DIDs issued by Sod Boys are recognized across the D-Central network. A crew member who later joins a D-Central construction cooperative, housing cooperative, or other field cooperative carries their verified work history and cooperative membership credentials with them.

---

## Tier 10: Technology Architecture

### 10.1 Complete Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React PWA + Tailwind CSS | Offline-first mobile app, no app store |
| Offline sync | PouchDB ↔ CouchDB | Dead-zone resilience, seamless background sync |
| Backend API | Node.js + Fastify | Lightweight, fast, self-hostable |
| Database | PostgreSQL | Structured cooperative data, full backup |
| DID layer | did:key or did:web (v1), upgradeable to did:ion | Member sovereign identity |
| Credential issuance | OpenCerts or custom VC issuer | Verifiable training and membership credentials |
| Maps + routing | OpenStreetMap + OSRM (self-hosted) | Job routing, carpool chains, zero API fees |
| Weather | Open-Meteo API (free, no key required) | Ottawa site weather per coordinate |
| SMS fallback | Twilio or VoIP.ms (Canadian) | Crew alerts without data plan |
| QR tags | Printable QR per asset, Web NFC for Android | Asset check-in/out in 5 seconds |
| Auth v1 | 4-digit PIN + crew profile | Zero barrier; upgradeable to DID-auth |
| Treasury ledger | PostgreSQL with append-only audit log | Transparent cooperative finance |
| D-Credit engine | Custom rule engine (Node.js) | Credit earning, redemption, equity conversion |
| Governance (v1) | In-app proposal + vote module | Mobile-first cooperative governance |
| Hosting | Hetzner CAX11 ARM VPS ($5–10/mo) | Self-hosted, EU data protection, fast |
| Backup | Restic → Backblaze B2 | Encrypted nightly, off-site |
| Monitoring | Uptime Kuma (self-hosted) | Alerts if the system goes down |

**Total infrastructure cost: $15–25/month.**  
Full data sovereignty. No SaaS dependency. No per-seat fees.

### 10.2 Offline-First Architecture

Ottawa field conditions:
- Dead zones in rural job sites (east/west Ottawa fringe areas)
- Spotty LTE in basements and underground areas
- Crew uses phones actively while working — battery and data management matter

**D-FIELD offline behavior:**
- Full app loads and operates from local cache when offline
- All actions queued locally (IndexedDB via PouchDB)
- Syncs to server within 30 seconds of connectivity restored
- Conflict resolution: last-write-wins with server timestamp, manual resolution prompts for critical conflicts (e.g., two crew check the same machine out simultaneously)

### 10.3 Upgrade Path

```
D-COOP-001 v1.0 (NOW)
├── PIN auth → W3C DID (Year 1–2)
├── Internal D-Credits → Lakou Protocol lite (Year 2)
├── Lite treasury → Multi-sig cooperative treasury (Year 2)
├── Single-company → D-FRANCHISE network (Year 2–3)
├── Internal credits → D-Central D-Credit network (Year 3)
├── Lite Lakou → Full Lakou Protocol with on-chain anchoring (Year 3–4)
└── Field cooperative node → Full D-Central ecosystem participant (Year 4+)
```

Every decision made in v1.0 is made with the upgrade path in mind. Nothing built now needs to be thrown away. The architecture grows in place.

---

## Implementation Roadmap

### Phase 0 — Foundation (Months 1–2)
- Incorporate Ontario Worker Cooperative
- Draft founding charter with owner
- Issue candidate membership to current crew
- Provision self-hosted infrastructure
- Deploy D-MESH + D-JOB (Slice 1 of DC-FOS-001)

### Phase 1 — Operations Mesh (Months 2–4)
- Deploy D-MOVE (carpool + equipment transport)
- Deploy D-ASSET (machine registry + QR tags)
- Deploy D-CLIENT (client portal)
- Deploy D-WEATHER integration
- First pre-roll readiness gates active

### Phase 2 — Economic Layer (Months 4–6)
- Launch D-Credit economy
- Activate cooperative treasury (transparent ledger)
- Deploy D-QUOTE (pricing engine distributed to site leads)
- Launch D-ROUTE (geographic job clustering)
- First quarterly profit share distribution

### Phase 3 — Intelligence Layer (Months 6–9)
- Deploy D-RECORD (property history)
- Deploy D-MEMBER (client cooperative community)
- Deploy D-TRAIN (crew development registry)
- Launch D-SUPPLY cooperative purchasing triggers
- First Seasonal Assembly (October)

### Phase 4 — Network Layer (Year 2)
- Launch D-FRANCHISE outreach to Ottawa landscaping companies
- Activate D-MARKET capacity exchange
- Issue W3C DIDs to all worker members
- Upgrade treasury to multi-signature governance
- Begin D-Credit network integration planning

### Phase 5 — Ecosystem Integration (Year 3–4)
- Full Lakou Protocol treasury upgrade
- D-Credit network interoperability
- D-Central field cooperative network operational
- Sod Boys as reference implementation and network hub

---

## Impact Summary

| Domain | Before | After |
|--------|--------|-------|
| Ownership | 1 person holds everything | Distributed cooperative equity |
| Decision-making | 1 person decides everything | Circle governance, member proposals |
| Financial transparency | Owner sees all, crew sees nothing | Full member visibility |
| Operational coordination | Star topology through owner | Cooperative mesh, autonomous nodes |
| Crew mobility | Ad-hoc, informal, unreliable | D-MOVE coordinated carpool chains |
| Equipment location | Unknown until someone calls | Real-time D-ASSET digital twin |
| Quoting capacity | Owner only | Any site lead with D-QUOTE |
| Client communication | Owner as relay | D-CLIENT read-only portal |
| Material tracking | Discovered on-site | D-SUPPLY pre-arrival alerts |
| Job routing | Order booked = order scheduled | D-ROUTE geographic clustering |
| Crew development | Informal, owner-dependent | D-TRAIN credential pathways |
| Company knowledge | In the owner's head | D-RECORD, D-SUPPLY, D-TRAIN |
| Growth ceiling | Owner's personal capacity | Cooperative network capacity |
| Infrastructure cost | SaaS fees scaling with size | $15–25/mo fixed, self-hosted |
| Exit for owner | Sell or close | Transfer cooperative stewardship |

---

## Registry Classification

```
Document ID:     DC-COOP-001
Version:         1.0 (Architecture Draft)
Domain:          Cooperative Company Reconstruction
Stack:           D-Central Cooperative Field Layer
Parent docs:     DC-FOS-001, DC-MONETARY-001, DC-LKB-001 (Lakou Protocol)
Implementation:  Sod Boys Ottawa (Reference Deployment)
Tiers:           10
Systems:         20 (D-MESH, D-MOVE, D-ASSET, D-JOB, D-SUPPLY, D-CLIENT,
                     D-CRED, D-QUOTE, D-ROUTE, D-TRAIN, D-WEATHER, D-RECORD,
                     D-MEMBER, D-AGORA, D-ID, D-FRANCHISE, D-MARKET, 
                     D-TREASURY, D-NETWORK, D-DATA)
Upgrade path:    Full D-Central sovereign ecosystem (Lakou Protocol, D-Credit
                 network, W3C DID infrastructure, D-FRANCHISE cooperative network)
```

---

*Sod Boys Ottawa is not a landscaping company that got a software upgrade.  
It is the first D-Central cooperative field enterprise — proof that the sovereign cooperative model works at the scale of ten people, two machines, and a yard full of sod.  
Every company the network adds after it is built on what Sod Boys proves.*
