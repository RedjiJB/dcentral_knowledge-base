# DC-TAXONOMY-001: D-Central Service Taxonomy & Dependency Map
### Mapping AWS, Amazon Marketplace, Amazon Logistics, UberEats, social media, and other major platforms onto the D-Central DePIN architecture

---

## 0. How to read this document

Every major consumer/enterprise platform decomposes into a small number of **primitive services**. D-Central already has (or has specified) a sovereign, cooperative equivalent of nearly every primitive, because the eight mesh modules + `dcentral-core` were designed as general-purpose infrastructure, not single-purpose apps.

The rule used throughout: **no vertical gets its own identity system, payment rail, storage layer, or trust mechanism.** Every vertical is a thin application layer that composes existing primitives. This is the same discipline SkyLedger already applies (an AWS-style `sky.*` service catalogue sitting on the same DID/D-Credit/attestation base) — this document generalizes that pattern across the entire ecosystem.

```
Layer 4: VERTICALS        MeshEats · MeshRide · MeshSocial · MeshShop · SkyLedger · classIQ · Lakou Fraternity · TrafficMesh · DC-AGD ...
Layer 3: PLATFORM SVCS    Compute · Storage · AI/Inference · Sensors/Geo · Bandwidth · Energy · Connectivity  (the 8 mesh modules)
Layer 2: CORE PRIMITIVES  Identity (DID/VC) · D-Credit payments · Lakou DAO governance · Attestation Envelope · Node Registry  (dcentral-core)
Layer 1: PHYSICAL SUBSTRATE   SHI node (5 tiers) · Gateway nodes · Mobile nodes · Campus infrastructure
```

---

## 1. Layer 1 — Physical Substrate

| Component | Spec | Role |
|---|---|---|
| SHI node (5 tiers: Power/Energy, Connectivity/Networking, Compute/Storage, Physical Security/Sensors, Identity/Services) | DC-SHI-SPEC-001 | Household-scale root of DID, credentials, vault, DAO participation |
| Gateway node | (mesh-connectivity) | High-capacity relay bridging local mesh to internet backhaul |
| Mobile node | (mesh-sensors / TrafficMesh) | Vehicle-mounted transceiver; same hardware class serves delivery, rideshare, and traffic-sensing verticals |
| Campus infrastructure | DC-CAMPUS-001 | Multi-district civic-scale deployment: NOC, Civic Spine, teaching/research testbed |
| NexNode tiers | (SkyLedger ecosystem) | ESP32 sensor node → Pi home node → community tower server → regional rack cluster |

This is the AWS "region/availability zone/rack" equivalent — except every rack is owned by the household or cooperative it sits in.

---

## 2. Layer 2 — `dcentral-core` (the only shared dependency)

| Primitive | Function | Equivalent to |
|---|---|---|
| **Identity & Verification** (W3C DID/VC) | Issues each node/person a DID; mints VCs for enrollment, hardware, governance participation, transactions | AWS IAM + Amazon/Google account system + Facebook Login |
| **D-Credit** | Universal settlement token replacing AKT/GLM/HNT/TAO/EWT per-module tokens | AWS billing + Stripe + Amazon Pay |
| **Lakou Protocol DAO** | Proposal/vote/slash; node registry (who is a staked, active node) | AWS Organizations/IAM policy + corporate governance, but member-owned |
| **Attestation Envelope** | Standardized `proof of X` wrapper — coverage, storage, compute, energy, sensor data, inventory, delivery, content moderation | AWS CloudTrail/audit logs + blockchain attestation, generalized to *any* claim type |
| **Node Registry** | Canonical list of active, staked DIDs per module | Service discovery / AWS resource inventory |

**Key discipline:** private vendor catalogs, inventory proofs, content moderation proofs, delivery proofs — all of these are just new **Attestation Envelope types**, not new subsystems. This was the correction made to the MeshEats/marketplace design: don't invent a bespoke ZK inventory scheme, issue an inventory-attestation VC through the identity layer already built.

---

## 3. Layer 3 — The Eight Mesh Modules (the "AWS service catalogue")

| Module | Fork base | SHI tier | What it replaces |
|---|---|---|---|
| `mesh-connectivity` | Helium PoC | Connectivity & Networking | ISPs, Starlink, WiFi mesh vendors |
| `mesh-energy` | Energy Web + DER attestation | Power & Energy | Utility grid billing, VPP aggregators (Tesla Energy, Enel X) |
| `mesh-sensors` | DIMO SDK | Physical Security & Sensors | Ring/Nest, city IoT sensor networks, DIMO itself |
| `mesh-compute` | Akash + Golem | Compute & Storage | **AWS EC2 / Lambda**, Azure, GCP |
| `mesh-storage` | Storj V3 | Compute & Storage | **AWS S3/Glacier**, Dropbox, Backblaze |
| `mesh-ai` | Bittensor | Compute & Storage (compute subset) | AWS Bedrock/SageMaker, OpenAI API, Anthropic API |
| `mesh-geo` | Hivemapper | Physical Security & Sensors (geo subset) | Google Maps/Street View, aerial imagery vendors |
| `mesh-bandwidth` | Meson Network | (folds into connectivity) | CDNs — Cloudflare, Akamai, CloudFront |

This row-for-row is D-Central's answer to "how much infrastructure does AWS actually sell" — compute, storage, AI inference, networking/CDN, and (uniquely, because D-Central is physical-infrastructure-native rather than datacenter-native) energy, sensors, and geo/imagery, which AWS doesn't provide at all but which a household-node cooperative naturally can.

---

## 4. Layer 4 — Verticals mapped to major platforms

### 4.1 Amazon Marketplace (e-commerce) → **MeshShop**

| Amazon primitive | D-Central equivalent | Built from |
|---|---|---|
| Product catalog / search | Public vendor catalog, node-hosted | `mesh-storage` (listing data) + `dcentral-core` node registry |
| Private/wholesale catalogs (Amazon Business) | VC-gated private catalog, unlocked by code or `mesh-market://` deep link | Attestation Envelope (credential presentation), not a new access-control system |
| Checkout / payments | D-Credit settlement + escrow | `dcentral-core` D-Credit, milestone-based escrow (see §4.6 condo marketplace precedent) |
| Seller reputation | DID-linked review VCs | Identity & Verification layer |
| Fulfillment network | See Amazon Logistics below | — |
| Recommendation engine | Local inference on shopper's own compute, not centralized profiling | `mesh-ai` (edge inference, privacy-preserving) |

### 4.2 Amazon Logistics / delivery → **MeshEats + MeshRide (shared delivery layer)**

| Amazon Logistics primitive | D-Central equivalent | Built from |
|---|---|---|
| Delivery Station (regional sort hub) | Gateway node cluster | `mesh-connectivity` gateway tier |
| Driver app / route dispatch | Real-time mesh dispatch, offline-tolerant | `mesh-connectivity` (local mesh messaging) + event-sourced sync |
| Vehicle telematics | Mobile node in vehicle | `mesh-sensors` (DIMO fork) — same hardware class as TrafficMesh, dual-purpose: delivery status *and* mobility telemetry, earning D-Credit on both axes |
| Package/order state, inventory deduction | Local DB + event log, synced and merged on reconnect | `mesh-storage` (erasure-coded, audit/repair) |
| Proof of delivery | Signed delivery attestation | Attestation Envelope |
| "Where's my order" tracking | DID-scoped order VC, holder-controlled disclosure | Identity & Verification |

This directly resolves the earlier MeshEats design questions: gateway+local node topology, mobile node requirement, distributed inventory/storage, and zero-knowledge inventory verification are not bespoke — they're `mesh-connectivity` + `mesh-sensors` + `mesh-storage` + Attestation Envelope, already specified.

### 4.3 AWS (cloud infrastructure) → **`mesh-compute` + `mesh-storage` + `mesh-ai` directly, no separate vertical needed**

AWS *is* Layer 3 for D-Central — there's no additional vertical wrapper required beyond exposing an AWS-style SDK/API surface, which is the precedent already set by **SkyLedger's `sky.*` catalogue** (`sky.compute`, `sky.vault`, `sky.stream`, `sky.market`, etc.). The same pattern generalizes: a `dc.*` namespace (`dc.compute`, `dc.storage`, `dc.ai`) exposing the mesh modules as programmable resources, with SkyLedger as the aerial-specific instance of the identical pattern.

### 4.4 UberEats / Uber → **MeshEats (food) + MeshRide (mobility)**

| Uber primitive | D-Central equivalent | Built from |
|---|---|---|
| Driver matching | Node-registry lookup of nearby active mobile nodes | Node Registry + `mesh-connectivity` |
| Surge pricing | DAO-governed or algorithmic D-Credit rate adjustment | Lakou Protocol |
| Trip/order verification | Attestation of pickup/dropoff | Attestation Envelope |
| Rider/driver trust | DID-linked ratings | Identity & Verification |
| Fleet-scale routing (UberPool-equivalent, TrafficMesh) | Stigmergic swarm coordination | DC-SWARM-001 pattern (same coordination logic as drone swarms, reused for ground vehicle routing) |

### 4.5 Social Media (Facebook/Instagram/X equivalent) → **MeshSocial**

Already specified in earlier D-Central design work as part of the Integrated Profile system:

| Social platform primitive | D-Central equivalent | Built from |
|---|---|---|
| Profile | DID-linked selective-disclosure profile (health, finances, social, skills — user controls what's shared) | Identity & Verification |
| Feed / content distribution | `mesh-bandwidth` caching + relay, content stored on `mesh-storage` | `mesh-bandwidth`, `mesh-storage` |
| Content moderation | Community-governed moderation as a DAO function, with moderation-decision attestations | Lakou Protocol + Attestation Envelope |
| Algorithmic feed / recommendation | Local/edge inference (no centralized behavioral profiling) | `mesh-ai` |
| Monetization (creator payouts, ads) | D-Credit micropayments; no ad-auction data broker | `dcentral-core` D-Credit |
| Identity verification / anti-bot | VC-based personhood proof | Identity & Verification |

### 4.6 TaskRabbit / Thumbtack (services marketplace) → **Lakou Marketplace** (originally designed as the condo/building marketplace, generalizes to any cooperative service marketplace)

| Primitive | D-Central equivalent |
|---|---|
| Vetted provider directory | DID + credential VCs (license, insurance, background check) |
| Booking/scheduling | Mesh-local coordination app on top of `dcentral-core` |
| Escrow payments | D-Credit escrow: 120% locked at request → released on completion attestation → 24hr dispute window → DAO jury if escalated |
| Group/cooperative buying power | Lakou Protocol cooperative-rate negotiation |

### 4.7 Google Maps / Street View → **`mesh-geo`** directly (already Layer 3, no extra vertical needed — SkyLedger and TrafficMesh consume it)

### 4.8 AI providers (OpenAI/Anthropic API, healthcare AI) → **`mesh-ai` + classIQ**

| Primitive | D-Central equivalent |
|---|---|
| Model inference API | `mesh-ai` (Bittensor-fork subnets), miners paid in D-Credit |
| Model validation / safety | Validator consensus + formal verification research output (field 4) |
| Clinical decision support | classIQ, running on `mesh-compute`, privacy-preserving via ZK attestation of model accuracy without exposing patient data |

### 4.9a Amazon Lockers / parcel pickup infrastructure → **MeshLocker**

| Amazon Locker primitive | D-Central equivalent | Built from |
|---|---|---|
| Physical locker bank at a retail/transit location | SHI node (or gateway node) with an attached smart-locker peripheral — a Physical Security & Sensors tier device | `mesh-sensors` (access control), `mesh-connectivity` (local dispatch) |
| Pickup code / QR unlock | VC-scoped access credential, single-use, DID-bound | Attestation Envelope + Identity & Verification (same mechanism as MeshShop's private-catalog unlock) |
| Locker availability / routing to nearest open locker | Node Registry query for nearby locker-equipped nodes | `dcentral-core` Node Registry |
| Host revenue (business hosts a locker bank) | Per-package hosting fee in D-Credit | D-Credit — a new, small revenue line for any SHI node or business node willing to host physical locker hardware, same pattern as the SHI financial model's other revenue tiers |
| Cold-chain / refrigerated lockers (grocery pickup) | Sensor-attested temperature log attached to the pickup attestation | `mesh-sensors` + Attestation Envelope |

This is a genuinely new *physical* SHI peripheral, not just a software layer — worth noting as a hardware SKU alongside the SHI node itself (an optional "Locker Tier" add-on), since it's the one Amazon-equivalent primitive that requires dedicated hardware at a public/semi-public location rather than living entirely inside a household node.

### 4.9b Postal system (USPS/Canada Post equivalent) → **MeshMail**

Not previously named. USPS-class services decompose cleanly:

| Postal primitive | D-Central equivalent | Built from |
|---|---|---|
| Mail carrier route / last-mile delivery | Same mobile-node + dispatch pattern as MeshEats, generalized to lightweight mail items | `mesh-connectivity` (dispatch) + `mesh-sensors` (mobile node) |
| Sorting facility | Gateway node cluster, same role as an Amazon Logistics Delivery Station | `mesh-connectivity` gateway tier |
| Mailbox / community mailbox cluster | Physical SHI-adjacent hardware — same category as MeshLocker, could literally share the locker hardware SKU | `mesh-sensors` (access), Attestation Envelope (proof of delivery/receipt) |
| Certified mail / proof of delivery with legal standing | Signed delivery attestation VC, timestamped and DID-bound to both sender and recipient | Attestation Envelope + Identity & Verification |
| Change-of-address | DID profile update, propagated to any vertical that holds a delivery-address VC (MeshShop, MeshEats, MeshMail all read the same address credential rather than each storing their own copy) | Identity & Verification (Integrated Profile) |
| P.O. Box equivalent | Address-privacy service: recipient gets a stable DID-linked delivery handle without exposing home address to senders | Identity & Verification (selective disclosure) |

Note the address-VC pattern: this is the one piece that meaningfully improves on the legacy postal model — one address credential shared with selective disclosure across every delivery vertical (mail, packages, food, locker pickup), instead of every company independently storing and leaking the same home address.

### 4.9c General task/gig platforms (TaskRabbit already covered under §4.6; also covers Fiverr/Upwork-style remote gig work, Mechanical-Turk-style microtasks, Instacart-style shopping errands) → **Lakou Marketplace, extended**

| Gig-platform primitive | D-Central equivalent | Built from |
|---|---|---|
| Task posting / bidding | Local marketplace listing, node-hosted | `mesh-storage` + Node Registry |
| Remote digital microtasks (Mechanical Turk equivalent) | Same escrow/attestation pattern as physical tasks — a microtask is just a smaller-denomination service listing | Lakou Marketplace escrow (§4.6), no separate system needed |
| Shopper/errand-runner (Instacart equivalent) | MeshShop catalog browsing + Lakou Marketplace escrow + mobile-node delivery, i.e., a composition of three already-specified pieces rather than a new vertical | MeshShop + Lakou Marketplace + `mesh-sensors` mobile node |
| Freelance/portfolio reputation (Upwork equivalent) | DID-linked credential + completed-job attestation history, portable across every vertical instead of platform-locked | Identity & Verification |
| Labor classification / worker protections | Autonomous Systems Law research track (field 6) — this is a governance/legal question, not an infra one; Lakou DAO can encode minimum-payout or dispute-resolution rules directly | Lakou Protocol DAO |

The pattern across all three of these (Lockers, Mail, Gig work) is the same one already established for MeshEats: **nothing here needs a new subsystem.** Lockers and Mail need one new *physical hardware peripheral* (shared between them); gig work needs zero new infrastructure, only new marketplace listing types on top of Lakou Marketplace.

### 4.9d Other major consumer tech platforms, briefly mapped

| Platform | D-Central equivalent | Composed from |
|---|---|---|
| Airbnb / short-term rental | Lakou Marketplace listing type (space rental, already scoped in the original condo marketplace design: guest suite booking, storage rental) | Lakou Marketplace, Identity & Verification (host/guest trust) |
| Banking / fintech (Venmo, PayPal, Chase) | D-Credit wallet + fiat on/off-ramp; the SHI financial model's revenue/payment flows already are this | `dcentral-core` D-Credit |
| DoorDash / Instacart | Same as UberEats/MeshEats — identical primitive set, different catalog type (restaurant vs. grocery) | MeshEats |
| Yelp / Google Reviews | DID-linked review VCs attached to a vendor's node, portable across MeshShop/MeshEats/Lakou Marketplace instead of siloed per-platform | Identity & Verification |
| Zoom / video conferencing | `mesh-compute` (media relay/transcoding) + `mesh-bandwidth` (routing) — civic/campus use case already implied by the Civic Spine/NOC design | `mesh-compute`, `mesh-bandwidth` |
| Slack / Discord (community coordination) | Lakou DAO's community forum/digital-town-hall function, already named in the original service ecosystem design (Public Services: digital town halls, citizen engagement) | Lakou Protocol |
| Insurance (home/auto/health) | Sensor-attested risk data (structural-health sensors, driving telemetry) feeding cooperative risk pools instead of a for-profit insurer | `mesh-sensors` + Attestation Envelope + Lakou Protocol (pool governance) |

### 4.9 Streaming / content delivery (Netflix/YouTube equivalent) → not yet named as a standalone vertical

Gap: no dedicated "MeshStream" vertical currently exists in memory. It would compose `mesh-storage` (content hosting) + `mesh-bandwidth` (edge caching/CDN) + D-Credit (creator payouts) — same pattern as MeshSocial's content layer, just without the social graph. Worth registering formally if pursued (e.g., **DC-MESHSTREAM-001**).

### 4.10 Emergency/public safety (911, ADT/home security) → **DC-AGD + OpenSecure (OS-PACS/OS-GUARDIAN/OS-SENTINEL/OS-PATROL)**

Already specified: gunshot detection with three-DAO governance, physical-cyber convergence platform. Built on `mesh-sensors` (signed telemetry) + Attestation Envelope (verified alert = bounty payout to node operator).

---

## 5. Dependency graph (who depends on whom)

```
dcentral-core (Identity, D-Credit, DAO, Attestation, Registry)
   │
   ├── mesh-connectivity ──┬── MeshEats (dispatch)
   │                       ├── MeshRide (driver matching)
   │                       ├── MeshMail (carrier dispatch, sorting gateway)
   │                       └── MeshSocial (feed distribution, w/ mesh-bandwidth)
   │
   ├── mesh-energy ─────────── (standalone: household revenue tier, feeds no vertical directly)
   │
   ├── mesh-sensors ────────┬── MeshEats (mobile delivery node)
   │                        ├── TrafficMesh (mobility telemetry)
   │                        ├── DC-AGD (gunshot detection)
   │                        ├── MeshLocker (access control, cold-chain sensing)
   │                        ├── MeshMail (community mailbox access)
   │                        ├── DC-RISKPOOL (structural-health / driving telemetry)
   │                        └── OpenSecure (OS-SENTINEL)
   │
   ├── mesh-compute ────────┬── classIQ (inference execution)
   │                        ├── SkyLedger (sky.compute)
   │                        └── AWS-equivalent (dc.compute) — general purpose
   │
   ├── mesh-storage ────────┬── MeshShop (catalog, order state)
   │                        ├── MeshEats (inventory event log)
   │                        ├── Lakou Marketplace (listings — TaskRabbit/Instacart/Airbnb/Upwork equivalents)
   │                        ├── MeshSocial (content hosting)
   │                        └── AWS-equivalent (dc.storage / S3-equivalent)
   │
   ├── mesh-ai ──────────────┬── classIQ (clinical inference)
   │                         ├── MeshSocial (feed ranking, on-device)
   │                         └── AWS-equivalent (dc.ai / Bedrock-equivalent)
   │
   ├── mesh-geo ─────────────┬── SkyLedger (sky.radar / sky.lidar)
   │                         └── TrafficMesh (mapping)
   │
   └── mesh-bandwidth ───────┬── MeshSocial (feed/content CDN)
                              └── (fold-in candidate for mesh-connectivity, decision by P27)
```

---

## 6. Gaps / not-yet-registered as formal DC-XXX-001 documents

1. **DC-MESHEATS-PRIVATE-CATALOG-001** — VC-gated private vendor catalog + `mesh-market://` deep link (identified previously, still unwritten)
2. **DC-MESHSHOP-001** — Amazon Marketplace equivalent; catalog/checkout/escrow layer atop `mesh-storage` + D-Credit (implied by Lakou Marketplace precedent, not yet consolidated into its own spec)
3. **DC-MESHSOCIAL-001** — social media vertical; the Integrated Profile system exists in early design docs but hasn't been reconciled with the current 8-module + dcentral-core architecture
4. **DC-MESHSTREAM-001** — streaming/content-delivery vertical; no dedicated spec, composes existing modules
5. **DC-XAAS-CATALOG-001** — a general `dc.*` SDK/API namespace mirroring SkyLedger's `sky.*` catalogue, generalized beyond aerial infrastructure to compute/storage/AI directly (this is the actual AWS-equivalent developer-facing product; SkyLedger is currently the only vertical with this pattern fully specified)
6. **DC-MESHLOCKER-001** — smart-locker physical peripheral spec (hardware SKU, access-control firmware, shared design between locker pickup and community mailbox use cases)
7. **DC-MESHMAIL-001** — postal/mail vertical; introduces the cross-vertical shared address-VC pattern (one delivery-address credential, selectively disclosed to MeshShop/MeshEats/MeshMail/MeshLocker alike) — this address-VC concept doesn't exist elsewhere yet and is worth generalizing beyond just mail
8. **DC-LAKOU-MARKETPLACE-001** — the general escrow/reputation marketplace engine underlying TaskRabbit-equivalent, Instacart-equivalent, Airbnb-equivalent, and Upwork-equivalent verticals; currently scattered across the original condo marketplace design and this taxonomy rather than consolidated as its own core spec (arguably belongs closer to Layer 2/3 than Layer 4, since so many verticals depend on it)
9. **DC-RISKPOOL-001** — cooperative insurance vertical using sensor-attested risk data; only sketched here, no prior design work found

---

*DC-TAXONOMY-001 — compiled from D-Central memory files, Master Timeline V24, and prior conversation history (condo marketplace design, SkyLedger XaaS model, D-Central platform architecture, integrated identity/profile system). Cross-references: DC-SHI-SPEC-001, DC-MESHEATS-ARCH-001, DC-SKY-PLATFORM-001, DC-CAMPUS-001, DC-AGD, OpenSecure.*
