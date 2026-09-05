---
source_conversation_uuid: 7963735d-a671-4b42-806e-651377fd29b2
conversation_title: 'Fixing operational visibility in decentralized construction'
created_at: 2026-06-10T01:34:30.970459Z
doc_id: DC-NETINFRA-001
description: 'DC-NETINFRA-001 - D-Central Network Infrastructure as a B2B platform - D-MOVE and supporting systems for other companies'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-NETINFRA-001 v1.0: D-Central Network Infrastructure Platform
## Cooperative Field Infrastructure as a Multi-Employer Service
**Registry ID:** DC-NETINFRA-001 v1.0  
**Parent Documents:** DC-COOP-001 v2.0, DC-B2B-001, DC-FOS-001  
**Status:** Architecture Draft v1.0  
**Date:** 2026-06-09  

---

## Infrastructure Thesis

Every field service company in Ottawa has the same operational problems that D-Central solves for Sod Boys:

- Workers scattered across the city with no coordinated mobility
- Tools and equipment sitting idle at one company while another company needs them
- Workers paying retail for food, PPE, and clothing because no one has buying power alone
- Certifications not recognized between employers so workers get re-trained repeatedly
- No portable work identity — every new job means starting from scratch

These companies are not going to build D-Central themselves. They do not have the engineering capacity, the cooperative structure, or the vision. But they have the operational pain, and they will pay to make it stop.

**DC-NETINFRA-001 opens the D-Central infrastructure stack as a multi-employer cooperative network.** Any field service company in Ottawa can subscribe. Their workers plug into D-MOVE, D-SUSTAIN, D-TOOLS, D-ASSET, D-CRED, and D-TRAIN as if those systems were built for them — because the architecture is universal.

This is not a gig platform. The distinction is structural:
- Workers accumulate equity in the network through D-CRED, not just fees
- The platform is cooperatively governed, not VC-extracted
- Pricing is transparent and cost-derived
- Workers own their data through D-ID — the platform does not
- Surplus flows back to participants, not to external shareholders

The cooperative infrastructure that makes Sod Boys sovereign is available to any company whose workers need the same flexibility.

---

## What "Flexibility" Means

A Sod Boys crew member has flexibility that workers at traditional companies do not:
- They can get to any job site in Ottawa without owning a car (D-MOVE)
- They can access food, tools, PPE, and water without paying retail (D-SUSTAIN)
- Their equipment is available where they need it without deadhead transit (D-ASSET)
- Their certifications are current, documented, and portable (D-TRAIN)
- Their earning history and credentials travel with them permanently (D-ID)
- They earn equity in the cooperative, not just wages (D-CRED)

That flexibility is what enables the cooperative to retain workers, attract better candidates, and build the operational mesh that makes zone pricing and cluster scheduling possible.

**Every field service company in Ottawa would benefit from giving their workers this flexibility.** Most cannot build it. D-NETINFRA sells them access to it.

---

## Layer 1: D-MOVE Network — Inter-Company Cooperative Mobility

### The Problem at Network Scale

A single company's mobility pool is limited. Sod Boys has 10 crew going to 4–6 sites. The matching space is small — maybe 2–3 good carpool chains per day. At 10 people the system works but it is not transformative.

When 50 companies join the network, the pool is 500–2,000 workers going to hundreds of Ottawa sites daily. Every worker has a dramatically better chance of finding a ride or filling a seat. The match quality improves non-linearly with network size. At sufficient scale, almost no worker needs a personal vehicle for the commute to a job site.

### D-MOVE Network Architecture

**Worker view (unchanged from D-MESH):**
- Worker opens D-MESH app with their D-ID
- Sets destination: job site address (employer's D-JOB feeds this automatically)
- Sets departure window: flexible ±30 min from required arrival time
- D-MOVE searches the full network pool, not just their employer's crew
- Match found, confirmed, turn-by-turn generated
- Cross-company ride completed, both parties confirm

**Employer view:**
- Employer sees their workers' mobility status in real time
- Knows which workers are confirmed en-route vs. still unmatched
- Can see network-level coverage: "8 of your 12 workers have confirmed rides"
- No employer sees another employer's workers' identities — only aggregate coverage data

**Privacy architecture:**
- Worker-to-worker: name and photo visible once a match is confirmed (like any rideshare)
- Employer-to-employer: aggregate data only — no employer sees another's workforce roster
- D-ID controls what each party sees — workers set their own disclosure preferences

### D-MOVE Material and Equipment Transport

**Multi-employer load matching:**
When Company A and Company B are both delivering to the same Ottawa zone on the same day, D-MOVE identifies the overlap and offers a coordinated delivery:
- Company A's truck is going to Kanata with a 40% empty load
- Company B needs a palette of materials delivered to the same zone
- D-MOVE matches them: Company B's materials ride with Company A's truck
- Both companies pay the cooperative transport rate
- D-MOVE coordinates pickup, delivery confirmation, and D-CREDIT settlement

This is most powerful for:
- Shared supplier deliveries (both companies ordering from same supplier → one trip)
- End-of-day equipment returns (multiple companies' machines consolidated on one trailer)
- Emergency supply runs (one company's urgent material delivery coordinated with another's scheduled run)

**Cross-company equipment transit:**
When Company A needs to move a machine to Site X and Company B has a truck going near Site X:
- D-MOVE matches equipment move to existing vehicle route
- Company A pays transit fee → Company B receives network credit
- D-ASSET updates machine location in real time
- Both companies benefit without additional trips

### D-MOVE Network Operator Model

The cooperative runs the network infrastructure. All participating employers pay access fees. The cooperative earns the margin between:
- What employers pay per worker per month
- What it costs to run the coordination infrastructure

No driver needs to be a Sod Boys employee. Any worker in the network with a registered vehicle, valid license, and D-ID verification can be a D-MOVE driver, earning D-Credits for routes completed.

**Driver earnings:**
- D-Credits per person-km driven (as in the Sod Boys internal model)
- Monthly D-Credit statement converts to cash payout option
- Drivers from any employer earn the same rate — the cooperative is the equalizer

---

## Layer 2: D-SUSTAIN Network — Worker Support Infrastructure

### Philosophy

Single companies cannot negotiate meaningful bulk pricing with food suppliers, PPE manufacturers, or tool vendors. But 500 workers aggregated through a cooperative can. D-SUSTAIN turns the cooperative's purchasing power into a benefit that every network worker accesses, regardless of which employer they work for today.

### D-FOOD Network

**How it works for employers:**
- Employer subscribes workers to D-FOOD
- Workers get daily access to cooperative bulk food purchasing
- Pre-shift meal coordination at network hubs (yard locations, community kitchens, partner restaurants)
- Employer can choose to subsidize partially (e.g., cover breakfast for all workers on active job days) or let workers pay cooperative cost directly

**The purchasing mechanics:**
- D-FOOD aggregates food orders across all network employers the night before
- Single consolidated order placed with suppliers
- Individual orders distributed at network hub locations or delivered to active job sites via D-MOVE coordination
- Cooperative purchasing margin (2–4%) returns to the cooperative treasury
- Workers pay below retail; the difference comes from volume, not subsidies

**The scale economics:**
| Network size | Daily food volume | Negotiating position |
|------------|-------------------|---------------------|
| 50 workers | ~$750/day | Bulk catering rate |
| 200 workers | ~$3,000/day | Wholesale supplier rate |
| 1,000 workers | ~$15,000/day | Direct processor contract |

**Partner integration:**
- Preferred Ottawa food partners: local caterers, Just Food CSA, cafeteria operators
- Partnership model: D-FOOD sends confirmed volume orders, partner delivers, cooperative earns margin
- Workers can also use D-CREDITS to pay at partner locations without pre-ordering

### D-WATER Network

**Site water infrastructure as a shared asset:**
- Portable water stations (20L coolers) registered in D-ASSET network pool
- Network-wide deployment: stations move between active job sites via D-MOVE
- Any participating employer can requisition a water station for their job site
- Station tracked in D-ASSET, returned at end of shift, sanitized, redeployed
- Employer pays daily usage fee; cooperative maintains the stations

**Hot weather protocol across all network employers:**
- D-WEATHER monitors heat index for all Ottawa zones
- When index exceeds 32°C: automatic hydration alert to all D-MESH users in that zone, regardless of employer
- Mandatory water break logged in D-MESH by worker
- Employers who do not confirm hydration compliance are flagged — this is an OH&S liability issue the cooperative actively helps them avoid

### D-WEAR Network

**Cooperative PPE purchasing pool:**
Every OH&S-regulated employer in Ottawa must provide PPE. The cost is significant and the supply chain is fragmented. D-WEAR aggregates purchasing across all network employers.

**Purchasing model:**
- D-WEAR maintains a catalog of approved PPE (CSA-certified, OH&S compliant)
- Employers submit seasonal orders through D-MESH portal
- Orders aggregated across all employers → single bulk order placed
- Employers pay D-WEAR cooperative price (15–30% below retail)
- The cooperative's purchasing margin funds operations

**Personal PPE allowance:**
Workers receive an annual D-CREDIT allocation from their employer toward the D-WEAR catalog. They choose what to purchase within the allowance. This is the cooperative version of a benefits card.

**Safety equipment commons:**
Shared PPE (hard hats, Hi-Vis vests, harnesses, rain gear) maintained in the D-ASSET pool:
- Available for checkout at network hub locations
- Used by workers who forget their personal gear or are in a transition period
- Tracked in D-ASSET by item, condition, last user, sanitization date

### D-TOOLS Network

**The cooperative tool library at Ottawa scale:**

Single companies maintain tool inventories that sit idle 60–80% of the time. The cooperative tool library aggregates those inventories into a shared commons that any network worker can access.

**What goes in the library:**
| Category | Examples | Typical utilization (single company) |
|----------|---------|-------------------------------------|
| Measuring & survey | Measuring wheels, levels, laser levels | 10–20% |
| Power tools | Drills, saws, grinders, compactors | 25–40% |
| Hand tools | Shovels, rakes, wrenches, bars | 30–50% |
| Safety equipment | First aid kits, extinguishers, signs | 5–15% |
| Specialty | Aerators, core drills, tile saws | 5–10% |

Network utilization target: 60–75% across all items (3–5× improvement)

**Hub locations:**
Tool library hubs at 3–5 Ottawa locations (north, south, east, west, central):
- Workers check out tools at the hub nearest their job site
- D-ASSET QR/NFC checkout system (5-second interaction)
- Return at any hub at end of shift
- Tools rotate between hubs via D-MOVE to balance availability
- Hubs staffed by cooperative members earning D-CREDITS for tool management duty

**Employer contribution model:**
- Employers can donate idle tools to the cooperative library
- Donated tools earn the employer D-CREDITS (credited against monthly subscription fee)
- Tools are appraised at market value; employer receives ongoing D-CREDIT for utilization
- This converts idle corporate assets into network revenue

**Revenue model:**
- Employers pay tool access fee included in subscription tier
- Individual worker direct membership: $20/month includes basic tool access
- Specialty tool booking fee: $15–$35/day for high-value items
- Tool rental revenue projected: $180,000/year at 500 active users

---

## Layer 3: D-ASSET Exchange — Cooperative Equipment Network

### What D-MARKET becomes at network scale

Within Sod Boys, D-MARKET lists idle equipment for rent. At network scale, D-ASSET Exchange becomes an **Ottawa-wide construction and field services equipment cooperative**.

**Equipment categories in the network:**
| Category | Examples | Typical network rental rate |
|---------|---------|---------------------------|
| Ground preparation | Skid steers, mini excavators, plate compactors | $350–$800/day |
| Turf and grounds | Sod cutters, aerators, dethatchers, rollers | $150–$350/day |
| Material handling | Forklifts (small), pallet jacks, hand trucks | $120–$200/day |
| Specialty | Hydroseeders, core drills, pipe cameras | $200–$600/day |
| Trailers | Utility, dump, equipment | $100–$180/day |

**How it works:**
1. Equipment owner (any network participant) lists idle asset with available dates, rate, and pickup location
2. Equipment requester finds and books through D-MESH
3. D-MOVE coordinates transit if equipment needs to move between sites
4. D-ASSET tracks location, usage hours, and condition throughout rental
5. Payment settled in D-CREDITS or cash, distributed through cooperative treasury
6. Equipment returned, condition logged, owner receives payment

**Cooperative equipment fund:**
When multiple network participants want to access a category of equipment that no one in the network owns:
- Finance Circles of multiple participating companies pool capital
- Cooperative purchases the equipment on behalf of the pool
- All pool contributors have priority access at cooperative rates
- Non-contributors can rent at standard network rates
- Purchase cost recovered over 18–24 months through rental revenue

This is cooperative capital formation applied to equipment. No single company needs to carry the full cost of a machine they use 30% of the time.

**D-MAINT at network scale:**
- Preventive maintenance scheduled across all network equipment
- Cooperative maintenance crew (dedicated D-Central maintenance workers) services all network machines
- Maintenance history in D-ASSET visible to any potential renter
- Pre-rental inspection logged — renters know the machine's condition before accepting it

---

## Layer 4: D-CRED Network — Portable Credit Economy

### Credits that cross employer boundaries

Within Sod Boys, D-CREDITS are earned at Sod Boys and redeemed at Sod Boys. This is valuable but limited. When the network has 50+ participating employers, D-CREDITS become a genuine cooperative currency:

**Earning D-CREDITS across the network:**
A worker earns D-CREDITS for cooperative behaviors at any employer:
- Driving another network worker to a job site
- Completing D-SUSTAIN behaviors (food check-in, hydration log, PPE return)
- Maintaining and returning tools correctly
- Sharing equipment through D-MARKET
- Training another worker
- Any employer-defined behavior in their D-CRED configuration

**Redeeming D-CREDITS across the network:**
- Food at any D-FOOD partner (any hub, any city)
- Tools at any D-TOOLS hub
- PPE from D-WEAR catalog
- D-MOVE transit credits (reduce or eliminate their own mobility costs)
- Equity in the cooperative network itself (accumulated credits → fractional ownership)

**The equity layer:**
This is what distinguishes D-NETINFRA from every other workforce platform:
- Every 1,000 D-CREDITS accumulated → 0.001% equity stake in the D-Central cooperative network
- Equity stake earns a proportional share of network surplus (profit sharing)
- Workers who use the network heavily for years accumulate meaningful equity
- If the network grows to 5,000 workers, the aggregate equity accumulated by those workers represents real financial participation in the infrastructure they built

**Employer D-CREDITS:**
Employers also earn D-CREDITS for:
- Subscribing at full-tier (cooperative commitment)
- Donating equipment to the commons
- Hiring network workers who carry good D-CREDIT histories
- Providing network hub space (if their yard becomes a tool or food hub)

Employer D-CREDITS reduce their monthly subscription fee and can be invested in cooperative bonds for capital returns.

---

## Layer 5: D-TRAIN Network — Cross-Employer Credentialing

### The credentialing problem in field services

A worker gets WHMIS-certified at Company A. They move to Company B. Company B makes them do WHMIS again. This happens across:
- WHMIS (done at every new employer, effectively)
- Equipment operation sign-offs
- First Aid
- Site orientation (partially redundant across similar companies)
- Forklift operator
- Aerial work platform
- Confined space entry

The redundancy costs money (training time), costs workers (lost day wages), and adds no safety value. A credential is a credential. If it was issued correctly, it should be portable.

**D-TRAIN Network credential registry:**
- All credentials issued through D-TRAIN are stored in the worker's D-ID
- Cryptographically signed by the issuer (Sod Boys, or any network employer who has assessor status)
- Any network employer can verify in seconds: scan worker's D-ID → see all valid credentials with expiry dates
- No re-training required if the credential is current and the scope matches

**Issuer tiers:**
| Issuer | What they can certify |
|--------|---------------------|
| Third-party (CCOHS, Red Cross, TC) | External certifications (WHMIS, First Aid, RPAS) |
| D-TRAIN Network Assessor | Internal competencies (equipment operation, site lead) |
| D-Central Cooperative | Network-specific credentials (D-MOVE driver, D-TOOLS hub operator) |

Any employer can apply to be a D-TRAIN Network Assessor. Requirements:
- Qualified in-house trainer or designated assessor
- Assessment protocol approved by D-TRAIN standards committee
- Credentials they issue are peer-reviewed (network audit rights)

**This creates a self-reinforcing training ecosystem:**
- Employers invest in training because credentials are portable and attract better workers
- Workers invest in training because credentials follow them across employers
- The network as a whole gets a more skilled, better-documented workforce

---

## Layer 6: D-HUB — The Connection Architecture

### How employers plug in

D-HUB is the multi-tenant connection layer that lets any employer access D-NETINFRA without building their own integration. It is the technical foundation for everything in this document.

**Employer onboarding:**
1. Employer signs cooperative participation agreement
2. D-EMPLOYER account created: legal entity, WSIB clearance, insurance verification
3. API key issued: connects employer's own systems (scheduling, HR) to D-HUB via webhook or REST API
4. Worker roster imported: workers receive D-ID invitation via D-MESH app
5. Services activated: D-MOVE, D-SUSTAIN tiers, D-ASSET access level
6. First invoice generated from D-TARIFF engine

**Employer API capabilities:**
```
POST /v1/jobs/create         — Create a job site in the D-MOVE network
GET  /v1/workers/status      — Check all your workers' mobility status
GET  /v1/workers/{id}/creds  — Verify a worker's D-TRAIN credentials
POST /v1/assets/request      — Request equipment from D-ASSET network
GET  /v1/food/orders         — Check your workers' D-FOOD orders for tomorrow
POST /v1/credits/issue       — Issue D-CREDITS to a worker for employer-defined behavior
GET  /v1/reports/monthly     — Pull monthly usage report for your account
```

**Worker onboarding:**
1. Worker receives D-MESH invitation from any network employer
2. Creates D-ID: phone number or email, basic profile, skills declaration
3. Existing credentials uploaded (photos, PDFs) → pending D-TRAIN verification
4. D-MOVE immediately active: can post rides, request rides
5. D-SUSTAIN active based on employer tier
6. D-CRED balance starts at 0, builds through cooperative behaviors

**Worker data sovereignty:**
- Workers control what each employer can see
- Default: employer sees name, photo, D-TRAIN credentials relevant to their work, D-MOVE status
- Worker can revoke employer data access at any time (e.g., after leaving)
- D-CRED history and D-TRAIN credentials remain permanently with the worker
- No employer can delete a worker's history

### D-HUB Hub Locations

Physical hubs at 4–5 locations across Ottawa are the backbone of D-SUSTAIN and D-TOOLS. Hub requirements:
- Secure storage space (tools, PPE, water stations)
- Loading dock or accessible parking
- Power outlet for battery charging
- Ideally: covered space for weather protection

**Hub partner model:**
Hub locations are hosted by cooperative network participants:
- A yard already has space → becomes a hub, earns D-CREDITS
- A community organization offers space → becomes a hub, earns community D-CREDITS
- Sod Boys' own yard is Hub 0 (the original, always active)

Target hubs by Year 2:
- Hub 0: Sod Boys yard (current location)
- Hub 1: Kanata/Stittsville (construction-heavy)
- Hub 2: Barrhaven/Nepean
- Hub 3: Orleans/East Ottawa
- Hub 4: Central Ottawa (near Centretown/Hintonburg)

---

## Network Tiers and Business Model

### Employer Subscription Tiers

| Tier | Includes | Monthly Fee | Per-Worker Fee |
|------|---------|------------|---------------|
| **D-MOVE** | Mobility coordination only | $150 | $4/worker |
| **D-SUSTAIN** | Mobility + food + water + PPE access | $350 | $8/worker |
| **D-COMMONS** | Sustain + tools library + equipment exchange | $600 | $12/worker |
| **D-FULL** | Everything + D-CRED + D-TRAIN + API access | $1,000 | $18/worker |

**Example:** A 25-worker construction company on D-COMMONS tier:
$600/month + (25 × $12) = $600 + $300 = **$900/month**

What they get: carpool coordination for all 25 workers, access to cooperative food purchasing, shared tool library at 5 Ottawa hubs, equipment exchange for idle assets, D-ASSET tracking for their machines.

At $900/month, if D-SUSTAIN saves each worker $6/day in food costs (conservative for bulk buying): 25 workers × $6 × 22 days = $3,300/month in worker savings. The subscription costs the employer $900 and generates $3,300 in visible worker benefit. Retention value far exceeds the fee.

### Worker Direct Membership

Workers without an employer sponsor can access D-NETINFRA independently:
- **D-CORE**: $20/month — D-MOVE + D-TOOLS access + D-CRED earning
- **D-FULL WORKER**: $35/month — everything including D-FOOD and D-WEAR catalog

This is for:
- Gig workers between employers
- Independent operators (sole proprietors, owner-operators)
- Workers whose employer hasn't joined yet

### Cooperative Premium

For employers who convert to worker cooperative structure (like Sod Boys):
- 30% discount on all tiers (cooperative-to-cooperative rate)
- Priority access to D-ASSET network (first right of refusal on equipment)
- Voting rights in D-NETINFRA governance (annual assembly)
- D-BOND investment access (invest in network infrastructure, earn returns)

---

## Network Effects

### Why this grows

D-NETINFRA has layered network effects that make it stronger with every additional participant:

**Mobility network effect (strongest):**
- 50 workers: marginal carpool match improvement
- 200 workers: most workers find matches within 10 min
- 1,000 workers: near-perfect matching, most commutes covered
- 5,000 workers: transit-level reliability for field workers across Ottawa

**Tool library utilization effect:**
- 100 tools, 50 users: 40% utilization → tool access acceptable
- 500 tools, 500 users: 65% utilization → tool access excellent
- The library gets more valuable as inventory grows with more employer donations

**Purchasing power effect:**
- 100 workers: moderate bulk pricing
- 500 workers: wholesale pricing from suppliers
- 2,000 workers: direct processor contracts for food, direct manufacturer for PPE

**Credential recognition effect:**
- 10 employers: credentials recognized at 10 places
- 50 employers: credentials recognized widely, workers stop getting re-trained
- 200 employers: D-TRAIN becomes the Ottawa field services credentialing standard

### The flywheel

```
More employers join →
  Better carpool matching (D-MOVE) →
    More workers adopt D-ID →
      More credentials in D-TRAIN →
        Workers more willing to invest in training →
          Better-skilled workforce attracts more employers →
            Larger purchasing pool (D-SUSTAIN) →
              Lower costs for workers and employers →
                Even more employers join
```

Each loop takes 3–6 months to tighten. By Year 3 the flywheel is self-sustaining.

---

## Ottawa-Specific Opportunity

**The construction sector:**
Ottawa's construction boom (LRT Phase 3, development in Barrhaven, Stittsville, Riverside South, Kanata North) employs 25,000–35,000 workers. The sector has:
- High worker turnover (seasonal, project-based)
- Significant commute burden (workers living east working west, etc.)
- OH&S certification requirements that create redundant training
- Tool theft problems (shared tool library reduces individual exposure)
- No existing cooperative infrastructure

**Target employer profile for Year 1 outreach:**
- General contractors with 15–50 workers
- Specialty subcontractors (electrical, plumbing, HVAC, drywall) with Ottawa presence
- Other landscaping/grounds maintenance companies (natural fit)
- Snow removal companies (natural winter complement to Sod Boys)
- Moving and delivery companies (D-MOVE is immediately compelling)

**The municipal angle:**
The City of Ottawa has sustainability and social procurement goals. A cooperative mobility network for construction workers:
- Reduces construction-phase traffic (relevant to community relations)
- Improves worker safety (certified, tracked, documented workforce)
- Creates good jobs (cooperative participation, not gig extraction)

The city could become a D-NETINFRA supporter through:
- Hub space at community centres or yards
- Reference in procurement evaluations
- Pilot funding (Ontario Trillium Foundation, federal cooperative development grants)

---

## Revenue Projections

### D-NETINFRA Revenue (standalone, Year 1–3)

| Source | Year 1 | Year 2 | Year 3 |
|--------|--------|--------|--------|
| Employer subscriptions (20→50 employers) | $108,000 | $216,000 | $360,000 |
| Worker direct memberships (50→300 workers) | $12,000 | $36,000 | $84,000 |
| D-TOOLS rental fees | $18,000 | $48,000 | $120,000 |
| D-ASSET equipment exchange margin | $24,000 | $72,000 | $180,000 |
| D-FOOD purchasing margin (2–3%) | $8,000 | $24,000 | $60,000 |
| D-WEAR purchasing margin (3–5%) | $6,000 | $18,000 | $45,000 |
| D-BOND interest income | $0 | $12,000 | $36,000 |
| **Total D-NETINFRA** | **$176,000** | **$426,000** | **$885,000** |

Year 3 D-NETINFRA revenue approaches $900K on top of Sod Boys' own $4.2M operation. Combined enterprise revenue approaches $5M by Year 3 before D-PLATFORM SaaS is included.

---

## New Systems Added to D-Central Registry

| ID | System | Function |
|----|--------|---------|
| 47 | D-HUB | Multi-tenant connection layer for network employers |
| 48 | D-EMPLOYER | Employer onboarding, roster, subscription management |
| 49 | D-WORKER-ID | Portable worker identity across all network employers |
| 50 | D-DISPATCH | Inter-company mobility optimization (extends D-MOVE) |
| 51 | D-COMMONS | Shared resource pool management (tools, PPE, water stations) |
| 52 | D-WELFARE | Worker benefits coordination across network |
| 53 | D-CREDENTIAL | Cross-employer credential registry (extends D-TRAIN) |
| 54 | D-TARIFF | Network billing, usage tracking, subscription invoicing |

**Total D-Central system count: 54**

---

## Technology Architecture

D-NETINFRA is a multi-tenant extension of the existing D-Central stack. No separate codebase — the same infrastructure serves Sod Boys and all network employers, with tenant isolation handled at the application layer.

| Component | D-NETINFRA Addition | Notes |
|-----------|-------------------|-------|
| D-MESH app | Multi-employer identity routing | Worker sees their employer's jobs + network opportunities |
| PostgreSQL | Row-level security per employer tenant | Data isolation without separate databases |
| D-ID | did:dcoop:worker:{uuid} portable across employers | Core to portability |
| D-MOVE engine | Pool expanded to all network workers | Query scoped to network, not single employer |
| D-ASSET registry | Network-wide machine pool with owner attribution | Rental state machine added |
| D-TRAIN | Credential issuance and verification API | External employers issue + verify |
| D-CRED engine | Multi-employer earning and redemption | Credits earn at any employer, spend anywhere |
| D-HUB API | REST/webhook integration for employer systems | OpenAPI 3.0 spec published |
| Hub management | Physical hub scheduling, inventory | Extension of D-TOOLS logistics |

**Infrastructure cost scaling:**
Current D-Central stack: $15–25/month for Sod Boys alone.
D-NETINFRA at 50 employers: $80–120/month (more compute, more storage, more bandwidth).
D-NETINFRA at 500 employers: $400–600/month.

The platform cost grows orders of magnitude more slowly than the revenue it generates.

---

## Registry Classification

```
Document ID:      DC-NETINFRA-001
Version:          1.0 (Architecture Draft)
Domain:           Cooperative Network Infrastructure Platform
New Systems:      8 (D-HUB, D-EMPLOYER, D-WORKER-ID, D-DISPATCH,
                     D-COMMONS, D-WELFARE, D-CREDENTIAL, D-TARIFF)
Total systems:    54
Parent docs:      DC-COOP-001 v2.0, DC-B2B-001, DC-FOS-001
Network target:   20 employers / 300 workers Year 1
                  200 employers / 3,000 workers Year 3
Revenue target:   $176k Year 1 · $885k Year 3 (standalone)
Upgrade path:     Ottawa → Ontario → National · D-PLATFORM SaaS
                  D-CRED on-chain when network reaches 1,000+ workers
                  Full Lakou Protocol treasury at network scale
```

---

*The cooperative built its infrastructure to serve itself. The infrastructure turned out to serve everyone. That is how cooperatives have always worked — and why they outlast the companies that ignored them.*
