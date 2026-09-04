# DC-TAXONOMY-004: Inter-Service Communication & End-to-End User Stories
### Extends DC-TAXONOMY-001/002/003

---

## 1. How everything actually talks to each other

Before the stories, the mechanics — because every story below is really just this same pattern replayed with different nouns.

### 1.1 The three channels

Every interaction in D-Central, regardless of vertical, moves over exactly three channels:

1. **Identity/credential calls** — synchronous-ish request/verify against `dc-identity` (issue a VC, verify a presented VC, run selective disclosure). Low bandwidth, latency-tolerant, can traverse multiple mesh hops fine.
2. **Event/data sync** — the event-sourced, store-and-forward pattern already established for inventory (§ mesh-storage). A local node writes to its own event log; the log replicates to relevant peers/gateway on next contact. This is how MeshEats order state, MeshBank ledger deltas, MeshSocial posts, and MeshMail delivery records all actually propagate — one mechanism, many payload types.
3. **Attestation broadcast** — when something needs to be *provable* to a third party (a DAO, an insurer, another vendor), the relevant node wraps the event in the standard Attestation Envelope (§ dc-attestation) and either publishes it to `dc-registry`-discoverable watchers or hands it directly to the counterparty.

### 1.2 The "operating system call" analogy

Think of `dcentral-core`'s five services as a kernel, and every mesh module + vertical as a userspace program making syscalls into it:

```
Vertical app (MeshEats, MeshBank, MeshFeed, ...)
        │
        ├─ calls dc-identity  → "who is this, what can they prove?"
        ├─ calls dc-credit    → "move/lock/release value"
        ├─ calls dc-governance→ "is this allowed, who decides disputes?"
        ├─ calls dc-attestation → "wrap this claim so others can trust it"
        └─ calls dc-registry  → "who/what nearby can serve this request?"
```

No vertical ever calls another vertical directly for these functions — MeshEats never implements its own identity check, it calls `dc-identity`. This is the single rule that keeps 20+ verticals from becoming 20+ incompatible silos: they're incompatible in UX and data model (a food order looks nothing like a bank transfer), but every one of them resolves "who are you / can you pay / is this trustworthy / who's nearby" through the identical five calls.

### 1.3 Cross-vertical composition (how one user action touches many services)

A single user action often fans out across several verticals automatically, because they share the address-VC, reputation, and ledger primitives. Example fan-out for "order a delivery":

```
User taps "order" in MeshEats
 → MeshEats calls dc-identity: resolve delivery-address VC (shared with MeshShop/MeshMail/MeshLocker)
 → MeshEats calls dc-credit: escrow-lock payment
 → mesh-connectivity: dispatch to nearest available mobile node (queried via dc-registry capability-index)
 → mesh-sensors: mobile node begins telemetry (feeds TrafficMesh too, opportunistically)
 → On delivery: dc-attestation wraps proof-of-delivery
 → dc-credit releases escrow to vendor + driver
 → (optional, opt-in) MeshFeed: "just ordered from [vendor]" social post, drawing on the same DID, same attestation
 → NorthLedger/MeshBank: transaction appears in the local Wealthfolio-style ledger view automatically, no separate entry
```

That's the pattern every story below follows — I'll keep them tight, but each one is really this same fan-out with different modules lighting up.

---

## 2. User stories by vertical

Format: **[Stakeholder] — [Story]**, tagged with which `dcentral-core` calls and mesh modules fire.

### 2.1 MeshShop (Amazon Marketplace)

- **Buyer** — Toussaint searches for a part, finds a vendor's private catalog via a shared `mesh-market://` link a friend sent him, presents his stored access-VC automatically, browses, checks out. *(dc-identity: selective disclosure; dc-credit: escrow; mesh-storage: catalog/order state)*
- **Vendor** — A hardware-store owner lists inventory once; it's visible on the public marketplace and, for wholesale buyers, gated behind a second private-catalog access code issued as a VC. Inventory deduction is attested without revealing stock levels to competitors. *(dc-attestation: inventory proof; dc-identity: VC-gated catalog)*
- **Node operator** — A neighbor hosting `mesh-storage` capacity earns D-Credit for hosting the vendor's catalog data and order-state shards, with no idea what's actually in them (erasure-coded, opaque). *(mesh-storage; dc-credit)*
- **DAO/dispute juror** — A buyer disputes a damaged item; `dc-governance`'s dispute-jury is randomly selected from staked members to review the attestation trail (order, delivery-condition photo attestation, vendor response) and rule on escrow release. *(dc-governance)*

### 2.2 MeshEats / MeshRide / Amazon-Logistics-equivalent delivery layer

- **Customer** — Orders dinner; sees driver position via mesh-local dispatch even with no cellular signal, since the mobile node relays over the mesh, not the public internet. *(mesh-connectivity; mesh-sensors mobile node)*
- **Driver** — Same mobile-node hardware earns D-Credit three ways simultaneously: delivery fee, TrafficMesh mobility-telemetry reward, and — if idle between orders — spare `mesh-compute`/`mesh-bandwidth` relay income from the vehicle's onboard unit. *(mesh-sensors, mesh-connectivity, mesh-compute — one device, three revenue lines)*
- **Restaurant/vendor** — Lists a MeshRescue surplus item at 6pm (unsold food, time-boxed discount) using the same catalog the regular MeshEats listing uses, just with an expiry-attestation attached. *(dc-attestation; mesh-storage)*
- **Freight shipper (Uber Freight equivalent)** — Posts a cargo load on Lakou Marketplace; `dc-registry`'s capability-index matches it to nearby truck-class mobile nodes rather than passenger vehicles. *(dc-registry)*

### 2.3 MeshLocker + MeshMail

- **Recipient** — Orders something; MeshShop, MeshEats, and MeshMail all read the *same* stored delivery-address VC rather than each asking for the address again, and the recipient can revoke a sender's access to it without changing the underlying address. *(dc-identity: shared address-VC)*
- **Locker host** — A café hosts a smart-locker unit as an SHI Physical Security peripheral; earns per-package hosting fees; the locker firmware checks single-use pickup-VCs locally, no round-trip to a central server needed. *(mesh-sensors; dc-attestation)*
- **Mail carrier (mobile node)** — Same dispatch/mobile-node pattern as a MeshEats driver, generalized to lightweight mail items; certified-mail delivery gets a legally-meaningful signed attestation both sender and recipient can produce later. *(dc-attestation, timestamped, dual-DID-bound)*

### 2.4 Lakou Marketplace (TaskRabbit/Instacart/Airbnb/Upwork-equivalent)

- **Task poster** — Posts "need my gutters cleaned," funds escrow at 120%. *(dc-credit escrow-engine)*
- **Task provider** — A neighbor with a verified insurance-VC and 4.8-star DID-linked reputation (portable — earned doing MeshEats deliveries too, since reputation isn't platform-locked) takes the job. *(dc-identity: portable reputation)*
- **Shopper/errand-runner (Instacart-equivalent)** — Browses a MeshShop grocery catalog on the requester's behalf, buys, delivers via the same mobile-node/MeshEats dispatch layer — three verticals composing into one gig with no separate app. *(MeshShop + Lakou Marketplace escrow + mesh-sensors mobile node)*
- **Host (Airbnb-equivalent)** — Lists a guest room; guest's personhood-VC and past-stay attestations substitute for platform-run background checks. *(dc-identity)*

### 2.5 MeshBank (Wealthfolio-based)

- **Household member** — Opens the local Wealthfolio-style dashboard on their SHI node; sees D-Credit balance, cooperative equity in the neighborhood mesh cluster, and manually-imported outside accounts — all rendered locally, nothing uploaded. *(dc-credit ledger, read-only local view; no network call needed to just look at your own money)*
- **Lender** — A cooperative micro-lending pool reviews a borrower's selective-disclosure credit proof (on-time payment history, completed-job attestations) without ever seeing the borrower's full transaction history. *(dc-attestation: selective disclosure proof, not raw data)*
- **Remittance sender (Haiti-Diaspora loop)** — Sends D-Credit from a Canadian SHI node; a Haiti-side gateway node handles the fiat off-ramp; NorthLedger picks up both legs automatically for tax reporting. *(dc-credit cross-region fiat on/off-ramp)*
- **Cooperative treasurer** — Proposes reallocating DAO treasury funds toward a new gateway node; members vote via `dc-governance`; the resulting fund movement shows up automatically in every member's Wealthfolio-style dashboard as a shared-asset line. *(dc-governance treasury-manager + dc-credit)*

### 2.6 MeshSocial cluster (MeshFeed, MeshFrame, MeshClip, MeshCircle, MeshBoard, MeshTalk, MeshWiki, MeshDate)

- **Poster** — Publishes on MeshFeed; `dc-social-protocol` federates the post to followers' home nodes; content itself lives on `mesh-storage`, relayed via `mesh-bandwidth` caching so popular posts don't hammer the origin node. *(dc-social-protocol; mesh-storage; mesh-bandwidth)*
- **Cross-app identity continuity** — A user's MeshCircle professional credentials (skills VCs) are visible if they choose on their MeshFeed profile, since it's one DID across every app, not eight separate logins. *(dc-identity, one DID, selective disclosure per app)*
- **Moderator** — A MeshBoard community, scoped as a mini-DAO instance, votes on a moderation action; the decision itself is attested so users can see *why* content was removed, not just that it was. *(dc-governance scoped instance + dc-attestation)*
- **Creator (Patreon-equivalent, layered on any MeshSocial app)** — Gates bonus content behind a subscription VC; `dc-credit` runs the recurring micropayment; access check is the identical VC-gate mechanism as MeshShop's private catalog. *(dc-credit micropayment-channel; dc-attestation gate)*
- **MeshDate user** — Verified personhood-VC prevents bot/catfish profiles without a centralized ID database holding everyone's real identity; matches and messages ride on the MeshDM layer once connected. *(dc-identity personhood-VC; MeshDM)*

### 2.7 MeshDM / MeshLine (WhatsApp/Signal/TextNow)

- **Two DID holders messaging** — E2E encryption keys derive directly from their existing DID keypairs; no separate "generate a Signal key" step. *(dc-identity)*
- **Person without a smartphone (Haiti no-barriers case)** — Gets a MeshLine DID-linked phone-style handle; an SMS gateway node bridges messages between the traditional cellular network and the DID-native mesh, so they can reach and be reached by anyone on MeshDM despite having only a basic phone. *(mesh-connectivity SMS-gateway mode; dc-identity)*

### 2.8 mesh-sensors / DePIN-native verticals (TrafficMesh, DC-AGD, OpenSecure, DC-RISKPOOL)

- **Homeowner** — Structural-health and driving-telemetry sensors feed a cooperative risk pool instead of a private insurer; premium is recalculated from real attested data, and the homeowner can see exactly which attestations set their rate. *(mesh-sensors; dc-attestation; dc-governance pool rules)*
- **City/police (DC-AGD bounty payer)** — Pays a verified gunshot-detection alert bounty in D-Credit directly to the SHI node(s) whose sensors triggered a three-source-corroborated attestation, no manual invoicing. *(dc-attestation: multi-source corroboration; dc-credit)*
- **Drone operator (SkyLedger)** — Books `sky.compute`/`sky.radar` capacity through the same `dc.*` XaaS pattern as any other compute call, paid per job in D-Credit, imagery capture verified through `mesh-geo`'s capture-verification pipeline. *(mesh-geo; dc-credit; dc-registry capability-index for available drones)*

### 2.9 mesh-compute / mesh-storage / mesh-ai (the AWS-equivalent, `dc.*` namespace)

- **Developer** — Calls `dc.compute.run(job)` against the general-purpose XaaS SDK; the request is matched via `dc-registry` to available compute nodes, billed per-second through `dc-credit`'s micropayment-channel, exactly like calling AWS Lambda except the "cloud" is neighborhood hardware. *(mesh-compute; dc-registry; dc-credit)*
- **Node operator renting out spare capacity** — Sets a price floor for their SHI node's idle CPU; jobs auto-accept via Akash-style reverse auction; sandboxing (Golem-style) keeps the job isolated from the household's own network. *(mesh-compute)*
- **AI model trainer/validator (mesh-ai)** — Runs a classIQ inference subnet; validators check output quality via consensus and get paid proportionally, miners (inference providers) get paid per verified prediction. *(mesh-ai; dc-attestation validator consensus)*

### 2.10 Campus / civic (DCOT, Civic Spine, classIQ)

- **Student** — Roams across every campus district on one SSID; FreeRADIUS calls `dc-identity`'s verification API on each association, dynamically assigning the correct VLAN and service entitlements based on the student's DID — same credential works in the dorm, the lab, and the stadium. *(dc-identity; existing 802.1X/FreeRADIUS design)*
- **Instructor** — Issues a course-completion VC directly through classIQ; it's immediately usable as a credential on the student's MeshCircle profile or a job-matching Lakou Marketplace listing. *(dc-identity vc-issuer)*

---

## 3. What this reveals about the architecture

Reading all of these together surfaces one repeating structural fact: **most "features" people associate with a specific company (Amazon's checkout, Uber's dispatch, Instagram's feed, Chase's savings account) are not actually separate systems in D-Central — they're the same five `dcentral-core` calls, wearing different UI.** The genuine differentiators between verticals are narrow: the data model (a post vs. a parcel vs. a ledger entry) and which mesh module supplies the physical-world proof (sensors for delivery, geo for drones, compute for AI, storage for everything with state).

This is also where the earlier `mesh-vpn` carve-out becomes visible in practice: every story above assumes the actor is attestable and DID-linked — that's what makes reputation, escrow, and dispute resolution work across all of them. `mesh-vpn` traffic is the deliberate exception threaded through this whole system, and it's worth noting none of the stories above route through it by default; it's an opt-in privacy mode layered on top of an otherwise fully accountable network, not the default transport.

---

*DC-TAXONOMY-004 — extends 001/002/003. Documents the three communication channels (identity calls, event/data sync, attestation broadcast) and the "kernel/syscall" pattern by which every vertical resolves identity, payment, governance, attestation, and discovery through dcentral-core's five services rather than building its own. Provides end-to-end user stories for all major stakeholder roles across MeshShop, MeshEats/MeshRide, MeshLocker/MeshMail, Lakou Marketplace, MeshBank, the MeshSocial cluster, MeshDM/MeshLine, sensor/DePIN verticals, the compute/storage/AI XaaS layer, and campus/civic services.*
