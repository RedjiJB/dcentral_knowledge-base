# DC-TAXONOMY-002: Microservice Decomposition, Fediverse-Style Social Split, Additional Platform Ideas & Full DePIN Sweep
### Extends DC-TAXONOMY-001

---

## 1. `dcentral-core` split into individual services

DC-TAXONOMY-001 treated `dcentral-core` as one dependency block. It isn't one service — it's five, each independently deployable/upgradeable, each with its own microservices underneath.

### 1.1 `dc-identity` (DID/VC)
Microservices:
- `did-registrar` — issues/resolves DIDs (did:key, did:web equivalents)
- `vc-issuer` — mints verifiable credentials (enrollment, hardware, governance, delivery-address, reputation)
- `vc-verifier` — validates presented credentials against issuer signatures + revocation status
- `revocation-registry` — tracks revoked/expired credentials
- `key-recovery` — social/threshold recovery for lost keys
- `selective-disclosure-engine` — builds minimal-disclosure proofs from a full credential (address without name, age-over-18 without birthdate, etc.)

### 1.2 `dc-credit` (payments/settlement)
Microservices:
- `ledger` — core balance/transaction ledger
- `escrow-engine` — locks/releases funds on milestone or attestation completion
- `fiat-onramp` — bank/card → D-Credit conversion
- `fiat-offramp` — D-Credit → bank/card
- `fee-router` — splits transaction fees to node operators, DAO treasury, referrers
- `micropayment-channel` — high-frequency small payments (per-API-call, per-second compute) without per-tx ledger writes

### 1.3 `dc-governance` (Lakou Protocol DAO)
Microservices:
- `proposal-engine` — drafts/tracks proposals
- `voting-engine` — vote casting, quorum/threshold logic
- `slashing-engine` — penalizes misbehaving nodes
- `treasury-manager` — DAO-controlled fund allocation
- `dispute-jury` — random/staked juror selection for marketplace disputes (referenced in Lakou Marketplace escrow flow)
- `delegation-registry` — liquid democracy / vote delegation

### 1.4 `dc-attestation` (Attestation Envelope)
Microservices:
- `attestation-schema-registry` — defines valid proof types per module (coverage, storage, delivery, inventory, moderation, sensor-reading, etc.)
- `attestation-issuer` — wraps a raw proof into the standard envelope
- `attestation-verifier` — checks envelope validity/signature/schema conformance
- `zk-proof-service` — generates/verifies zero-knowledge proofs where full disclosure isn't wanted (inventory counts, income-for-lending, health-data-for-insurance)

### 1.5 `dc-registry` (Node Registry)
Microservices:
- `node-directory` — canonical list of active/staked DIDs per module
- `staking-engine` — bonds/unbonds node stake
- `heartbeat-monitor` — liveness checks, feeds slashing-engine on prolonged downtime
- `capability-index` — what services/modules each node actually runs (so discovery queries — "nearest locker node," "nearest mesh-compute node" — are fast)

**Why split this:** every vertical currently listed in DC-TAXONOMY-001 as "built from dcentral-core" actually only depends on 2–3 of these five services, not all of them. E.g., MeshLocker mainly needs `dc-identity` (selective-disclosure-engine) + `dc-attestation`, not `dc-governance`. Splitting means each can be deployed, scaled, and versioned independently — the same reasoning that justified splitting the eight mesh modules in the first place.

---

## 2. Social media split — fediverse model instead of one MeshSocial

DC-TAXONOMY-001's "MeshSocial" was one monolithic vertical. The fediverse (Mastodon/ActivityPub, Bluesky/AT Protocol) proves the better pattern: **separate apps, one shared protocol + identity layer**, federated across independently-operated instances/nodes rather than one platform.

### 2.1 Shared substrate (all social verticals sit on this, not on each other)
- `dc-social-protocol` — an ActivityPub-equivalent federation protocol: how posts/likes/follows propagate node-to-node
- `dc-identity` (from §1.1) — one DID per person, portable across every social app below (post history, followers, reputation move with the DID, not locked to one app)
- `mesh-storage` — content hosting
- `mesh-bandwidth` — feed/content relay and caching
- `mesh-ai` — optional, opt-in local feed ranking (never centralized behavioral profiling)
- `dc-attestation` — moderation-decision proofs, content-authenticity proofs

### 2.2 Individual apps (each independently forkable/operable, like separate Mastodon instances)

| App | Equivalent to | Core loop | Extra microservices beyond §2.1 |
|---|---|---|---|
| **MeshFeed** | Twitter/X, Mastodon | Short posts, follows, replies, boosts | `thread-engine`, `mention-router` |
| **MeshFrame** | Instagram | Photo/video posts, stories | `media-transcoder` (on `mesh-compute`), `story-expiry-service` |
| **MeshClip** | TikTok/Reels | Short-form video, algorithmic discovery feed | `media-transcoder`, opt-in `mesh-ai` ranking, `duet-remix-engine` |
| **MeshCircle** | LinkedIn | Professional profile, job posts, endorsements | Reads credential VCs from `dc-identity` directly (skills/certs are already verifiable credentials — no separate "endorsement" system needed) |
| **MeshBoard** | Reddit | Topic communities, threaded discussion, upvote ranking | `community-registry` (per-board governance, can literally be a scoped `dc-governance` instance), `ranking-engine` |
| **MeshTalk** | Discord/Slack | Real-time chat, voice/video rooms, servers | `mesh-compute` (voice/video relay), `presence-service` |
| **MeshWiki** | Wikipedia | Collaborative reference docs | `revision-history-engine`, `dc-governance`-based edit-dispute resolution |
| **MeshDate** | Dating apps (Hinge/Tinder) | Match, chat, verified profile | `dc-identity` personhood-VC prevents catfishing/bots without a centralized ID database |

**Why split it this way:** a person's identity, content storage, and moderation-governance are shared; but MeshFeed and MeshClip have completely different data models (text threads vs. short video) and shouldn't be forced into one app's schema. This mirrors why Mastodon, PeerTube, and Pixelfed are separate ActivityPub apps rather than one "fediverse app" — same protocol, different UX for different content types. Cross-posting between them is possible precisely because identity and federation protocol are shared.

---

## 3. New vertical ideas adopted from specific companies

### 3.1 HelloFresh (meal-kit subscription) → **MeshKit**
| Primitive | D-Central equivalent |
|---|---|
| Weekly recipe + pre-portioned ingredient box | Subscription listing type on Lakou Marketplace, fulfilled by local cooperative food-buying (bulk-purchase discount via `dc-governance`-coordinated group orders) |
| Recipe content | `mesh-storage` hosted, could federate into MeshWiki as a recipe-commons |
| Delivery | MeshEats delivery layer (mobile node + dispatch) — literally the same infra, different catalog |
| Subscription billing | `dc-credit` recurring micropayment-channel |

### 3.2 Too Good To Go (surplus food / anti-waste marketplace) → **MeshRescue**
| Primitive | D-Central equivalent |
|---|---|
| Restaurant/grocer lists surplus food at discount, time-boxed | Time-limited listing type on MeshShop/Lakou Marketplace, with an expiry-attestation (`dc-attestation`) instead of a centralized app enforcing pickup windows |
| Anonymous "mystery bag" | Selective disclosure — buyer sees category/price, not full inventory, until pickup (reuses the same VC-gated catalog mechanism as MeshShop's private catalog, inverted: partial disclosure instead of full-gate) |
| Environmental impact tracking (CO2/food saved) | Sensor/attestation-derived impact ledger, could feed into cooperative sustainability reporting for a DAO/co-op's own accounting | 
| Notably: this is a genuinely good pattern to generalize — **any perishable-inventory vertical** (MeshShop groceries, MeshKit unused boxes, restaurant inventory) can auto-list surplus at discount via a scheduled `dc-governance`-less rule (simple smart-contract-style expiry logic), not a new subsystem |

### 3.3 Uber (beyond ride-hailing — Uber Freight, Uber Health) → extend MeshRide
| Uber product | D-Central equivalent |
|---|---|
| Uber Freight (trucking marketplace) | Lakou Marketplace listing type for freight capacity, matched via `dc-registry` capability-index (which mobile nodes are truck-class vehicles) |
| Uber Health (non-emergency medical transport) | MeshRide + `dc-identity` health-appointment VC (destination pre-verified, HIPAA-equivalent selective disclosure) |
| Uber Eats Grocery | Same as MeshEats/DoorDash — no new infra |

### 3.4 Other companies worth pulling ideas from

| Company | Idea worth adopting | D-Central equivalent |
|---|---|---|
| **Costco / Sam's Club** | Bulk cooperative buying membership | Native to Lakou Protocol already — cooperative bulk-purchase is a governance function, not a separate company needed |
| **Nextdoor** | Hyperlocal neighborhood feed | MeshBoard scoped to a geographic node cluster (a "board" can be geo-bound instead of topic-bound) |
| **Craigslist / Facebook Marketplace** | Peer-to-peer used-goods listings, no platform fee | Lakou Marketplace listing type, D-Credit settlement instead of cash-in-person |
| **GoFundMe / Kickstarter** | Crowdfunding | `dc-credit` escrow + `dc-governance` treasury-manager — milestone-released crowdfunding, already a natural extension of the escrow engine |
| **LinkedIn Learning / Coursera** | Credentialed online courses | classIQ + `dc-identity` VC issuance (a completed course *is* a verifiable credential, portable to MeshCircle/job-matching) |
| **Waze** | Crowdsourced traffic/hazard reporting | TrafficMesh + `mesh-sensors`, already covers this |
| **Ring Neighbors** | Crowdsourced security alerts | OpenSecure (OS-SENTINEL) + MeshBoard (geo-scoped) for community alert threads |
| **Patreon / OnlyFans** | Creator subscription/paywall content | `dc-credit` micropayment-channel + `dc-attestation`-gated content access (same VC-gate pattern as MeshShop private catalogs) — works for any MeshFeed/MeshFrame/MeshClip creator without a separate platform |
| **Venmo social feed** | Social payment visibility | Optional public/selective-disclosure toggle on `dc-credit` transactions, surfaced in MeshFeed if the user opts in |
| **Duolingo** | Gamified learning streaks | classIQ + `dc-attestation` streak/achievement proofs, portable credential |
| **Signal** | End-to-end encrypted messaging | MeshTalk's DM layer, encrypted by default since it rides on the same DID key infrastructure as everything else — no separate crypto system needed |
| **Nextdoor/Amazon Ring combo: package theft alerts** | Delivery-attestation + community alert | MeshEats/MeshLocker delivery-attestation feeding a MeshBoard/OpenSecure alert if a package attestation shows pickup without an authorized DID |

---

## 4. Full DePIN category sweep (beyond the original eight modules)

The original eight modules (`mesh-connectivity`, `mesh-energy`, `mesh-sensors`, `mesh-compute`, `mesh-storage`, `mesh-ai`, `mesh-geo`, `mesh-bandwidth`) cover the major current DePIN categories, but the broader DePIN industry has additional recognized categories worth checking against:

| DePIN category | Existing real-world projects | D-Central coverage |
|---|---|---|
| Wireless/connectivity | Helium, XNET, Wicrypt | ✅ `mesh-connectivity` |
| Energy | Energy Web, PowerLedger, Arkreen | ✅ `mesh-energy` |
| Compute | Akash, Golem, io.net, Render | ✅ `mesh-compute` (Render's GPU-rendering niche not yet split out — see below) |
| Storage | Storj, Filecoin, Arweave | ✅ `mesh-storage` (Arweave's permanent/archival storage model isn't explicitly covered — mesh-storage as specified is Storj-style repairable/erasure-coded, not permanent-archive; worth a decision point like the mesh-bandwidth fold-in question) |
| AI/ML compute & data | Bittensor, Ritual, Gensyn | ✅ `mesh-ai` |
| Mapping/geospatial | Hivemapper, GeoDB, DIMO (partially) | ✅ `mesh-geo` |
| Sensor/IoT | DIMO, WeatherXM, Natix | ✅ `mesh-sensors` (WeatherXM's weather-specific niche is covered by SkyLedger's WeatherMesh module rather than mesh-sensors directly — worth a cross-reference note in DC-SKY-MOD-001) |
| Bandwidth/CDN | Meson, Theta Network | ✅ `mesh-bandwidth` |
| **GPU rendering (distinct from general compute)** | Render Network | ⚠️ Gap — currently folded into `mesh-compute`; may deserve a `mesh-render` sub-mode the same way `mesh-bandwidth` was considered for folding into `mesh-connectivity` (same decision pattern, opposite direction) |
| **Mobile data/positioning** | GEODNET (RTK-GPS), Fleek | ⚠️ Partially covered by `mesh-geo` and mobile nodes but not explicitly named; high-precision positioning (GEODNET-style RTK) would matter for TrafficMesh and SkyLedger drone precision |
| **Physical security / access DePIN** | (emerging category) | ✅ Already native — this is essentially what MeshLocker + OpenSecure + `mesh-sensors` are |
| **Water/environmental monitoring DePIN** | Hivemapper-adjacent, various water-quality DePIN pilots | ⚠️ Named in early D-Central design docs ("environmental analytics," water quality sensor interpretation) but not formally folded into `mesh-sensors` spec — worth an explicit sub-category |
| **Decentralized VPN** | Sentinel, Orchid | ⚠️ Not covered — a `mesh-vpn` mode could sit on `mesh-connectivity`, privacy-routing traffic through multiple mesh hops the way Orchid/Sentinel do |

**Net new gap identified:** DePIN's GPU-rendering, decentralized-VPN, and high-precision-positioning niches aren't explicitly named as their own modules or sub-modes yet, even though the architecture could absorb all three without new core primitives — same fold-in-or-split decision pattern already used for `mesh-bandwidth`.

---

## 5. Updated gap registry (adds to DC-TAXONOMY-001 §6)

10. **DC-CORE-SPLIT-001** — formal spec splitting `dcentral-core` into its five independent services (`dc-identity`, `dc-credit`, `dc-governance`, `dc-attestation`, `dc-registry`) with defined inter-service APIs
11. **DC-SOCIAL-PROTOCOL-001** — the federation protocol (`dc-social-protocol`) underlying all MeshFeed/MeshFrame/MeshClip/MeshCircle/MeshBoard/MeshTalk/MeshWiki/MeshDate apps
12. **DC-MESHKIT-001** — meal-kit subscription vertical (HelloFresh-inspired)
13. **DC-MESHRESCUE-001** — surplus/anti-waste marketplace (Too Good To Go-inspired); includes the generalizable perishable-inventory auto-discount pattern
14. **DC-RENDER-MODE-001** (or fold-in decision) — GPU-rendering sub-mode of `mesh-compute`
15. **DC-VPN-MODE-001** (or fold-in decision) — decentralized VPN sub-mode of `mesh-connectivity`
16. **DC-POSITIONING-001** — high-precision RTK-style positioning, likely a `mesh-geo` sub-mode, feeding TrafficMesh and SkyLedger

---

*DC-TAXONOMY-002 — extends DC-TAXONOMY-001. Splits dcentral-core into dc-identity/dc-credit/dc-governance/dc-attestation/dc-registry; splits the social vertical into a fediverse-style multi-app model (MeshFeed, MeshFrame, MeshClip, MeshCircle, MeshBoard, MeshTalk, MeshWiki, MeshDate) sharing one federation protocol; adds HelloFresh/Too Good To Go/Uber-Freight-inspired verticals (MeshKit, MeshRescue, extended MeshRide); completes the DePIN category sweep against the broader industry taxonomy (GPU rendering, decentralized VPN, high-precision positioning identified as gaps).*
