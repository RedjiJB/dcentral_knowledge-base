# DC-TAXONOMY-003: Missing Verticals + Open-Source Project Tags
### Extends DC-TAXONOMY-001 and DC-TAXONOMY-002

---

## 1. Missing verticals added

### 1.1 Messaging (WhatsApp / TextNow / Signal) → **MeshTalk, split into two apps**

DC-TAXONOMY-002 put messaging inside MeshTalk as a Discord/Slack equivalent. Splitting further — DM-first messaging is a different product from server/community chat:

| Platform | D-Central equivalent | Core loop | Notes |
|---|---|---|---|
| **WhatsApp** | **MeshDM** | 1:1 and small-group encrypted messaging, voice/video calls, status updates | Rides on `dc-identity` DID keys for E2E encryption by default — no separate key-exchange system |
| **Signal** | **MeshDM** (same app, not a separate one) | Same as above — Signal and WhatsApp are the same primitive (E2E messaging) with different trust/business models | D-Central collapses them into one app since the sovereign/cooperative model removes the "who owns the metadata" distinction that separates them today |
| **TextNow** | **MeshLine** | Free/low-cost SMS-equivalent + a phone-number-like DID handle for people without a traditional carrier plan | Useful specifically for the Haiti/no-barriers-identity use case already in early D-Central design docs (SMS-based access for non-smartphone users) — MeshLine is the bridge between DID-native messaging and the traditional phone network via SMS gateway nodes |
| Discord/Slack (community chat) | **MeshTalk** (unchanged from 002) | Server/channel-based group coordination | Distinct from MeshDM — many-to-many community structure, not 1:1 |

### 1.2 Banking, finance & fintech → **MeshBank** (a proper vertical, not just "D-Credit exists")

DC-TAXONOMY-001 §4.9d waved at this in one line. It deserves the same treatment as MeshShop or MeshEats:

**Architectural base: Wealthfolio, not Mifos X.** This is a meaningful shift, not a cosmetic swap. Mifos X is a centralized core-banking ledger (institution holds the books, member holds an account record). Wealthfolio is a **local-first, privacy-preserving personal portfolio/net-worth tracker** — data lives on the user's own device by default, nothing phones home. That matches D-Central's sovereignty model far better than a core-banking system does: MeshBank should track *your* finances on *your* SHI node, and only sync out the minimum attestation the network actually needs (proof of balance, proof of payment, proof of income for lending) rather than housing your full financial history in a shared ledger. `dc-credit` still does the actual settlement/transfer/escrow plumbing — Wealthfolio's role is the sovereign, node-local visualization/tracking layer sitting on top, not a replacement for the ledger itself.

| Fintech primitive | D-Central equivalent | Built from |
|---|---|---|
| Checking/savings account | D-Credit wallet, held at the SHI node or a custodial cooperative node for those who want it | `dc-credit` ledger |
| Personal net-worth / portfolio dashboard | **Local-first dashboard on the SHI node's Identity/Services tier**, forked from Wealthfolio — aggregates D-Credit balances, cooperative equity stakes, and (optionally) external account snapshots the user manually imports, all stored and rendered locally, never uploaded to a shared backend | Wealthfolio fork (local SQLite-equivalent store) + `dc-identity` (device-bound, DID-linked but not DID-published) |
| Peer-to-peer transfer (Venmo/Cash App/Interac e-Transfer) | Direct `dc-credit` transfer, DID-to-DID | `dc-credit` ledger + `dc-identity` |
| Debit/credit card | A physical or virtual card that draws against the D-Credit wallet via `fiat-offramp` at point of sale | `dc-credit` fiat-offramp |
| Investment tracking (stocks, crypto, cooperative equity) | Wealthfolio's existing multi-asset tracking model (manual + API import), extended with a native asset class for D-Credit and Lakou cooperative-equity holdings | Wealthfolio fork |
| Lending/credit scoring | Reputation + attestation history (completed jobs, on-time payments, held credentials) forms a portable, user-controlled credit profile instead of an opaque third-party score. The Wealthfolio-style local dashboard is where the user *sees* this score forming; only a selective-disclosure proof of it ever leaves the device | `dc-attestation` + `dc-identity` selective disclosure |
| Investment/brokerage | Cooperative investment pools governed by `dc-governance`, e.g. members pool D-Credit into a SHI-cluster expansion fund and vote on allocation; shows up in the Wealthfolio-style dashboard as a held asset | `dc-governance` treasury-manager |
| Insurance | Already covered as DC-RISKPOOL-001 in taxonomy 001 | `mesh-sensors` + `dc-attestation` + `dc-governance` |
| Remittances (Haiti-Diaspora Sovereign Value Loop) | Cross-border D-Credit transfer with local fiat off-ramp at a Haiti-side gateway node — this is the single most directly-relevant fintech use case to the whole ecosystem, since it's already named as a core Haiti component | `dc-credit` fiat on/off-ramp, cross-region |
| Payroll / gig payouts | Automatic settlement on attestation of completed work (MeshEats delivery, Lakou Marketplace task, mesh-compute job) | `dc-credit` micropayment-channel |
| Tax reporting | NorthLedger (already an existing named D-Central component — AI-powered tax platform for CPAs) consumes the `dc-credit` ledger directly, with the Wealthfolio-style dashboard as the human-facing view of the same data | `dc-credit` ledger export |

---

## 2. Open-source project tags

For every vertical and microservice across DC-TAXONOMY-001/002/003, two existing open-source projects are tagged as architectural reference points — code, protocols, or data models worth studying/forking, the same way the eight mesh modules already fork Helium/Storj/Akash/etc. "Reference" means "study this codebase," not "this is a perfect fit" — most need the identity/token/governance layers stripped out and replaced with `dc-identity`/`dc-credit`/`dc-governance`, same discipline as the original eight modules.

### 2.1 `dcentral-core` services

| Service | OSS reference #1 | OSS reference #2 |
|---|---|---|
| `dc-identity` | **Hyperledger Aries / Indy** (DID/VC issuance and verification stack) | **Veramo** (modular TypeScript DID/VC framework, easy to fork the selective-disclosure-engine from) |
| `dc-credit` | **Interledger (ILP)** (settlement/routing between value systems) | **Hyperledger Fabric** or **Cosmos SDK** (ledger + token module, for the escrow-engine and fee-router) |
| `dc-governance` | **Aragon** (DAO proposal/voting/treasury framework) | **Snapshot** (off-chain voting, lightweight proposal-engine reference) |
| `dc-attestation` | **W3C Verifiable Credentials reference implementation (did-jwt-vc / vc-js)** | **zkSync / Semaphore** (zero-knowledge proof-service reference for the zk-proof-service microservice) |
| `dc-registry` | **libp2p** (peer/node discovery, capability-index pattern) | **Consul** (service registry + heartbeat-monitor pattern) |

### 2.2 Eight mesh modules (carried over from source docs, tagged formally here)

| Module | OSS reference #1 | OSS reference #2 |
|---|---|---|
| `mesh-connectivity` | **Helium** (already the fork base — PoC witness/challenge) | **BATMAN-adv / OLSR** (already referenced in early D-Central design docs for mesh routing itself) |
| `mesh-energy` | **Energy Web** (already the fork base) | **OpenEMS** (open energy management system, for the household DER-attestation logic) |
| `mesh-sensors` | **DIMO** (already the fork base) | **Home Assistant** (device/sensor integration layer, reference for the sensor-ingestion side) |
| `mesh-compute` | **Akash Network** (already the fork base) | **Golem** (already the fork base — sandboxing) |
| `mesh-storage` | **Storj** (already the fork base) | **IPFS / Filecoin** (content-addressing + alternate durability model, useful for the Arweave-style permanent-archive gap identified in 002) |
| `mesh-ai` | **Bittensor** (already the fork base) | **Ray / Ray Serve** (distributed inference scheduling, useful underneath the validator/miner logic) |
| `mesh-geo` | **Hivemapper** (already the fork base) | **OpenStreetMap** (base map data + community-contribution governance model) |
| `mesh-bandwidth` | **Meson Network** (already the fork base) | **libp2p / IPFS Bitswap** (content routing and caching primitives) |

### 2.3 Layer 4 verticals

| Vertical | OSS reference #1 | OSS reference #2 |
|---|---|---|
| MeshShop (Amazon Marketplace) | **Medusa.js** (open-source headless commerce engine) | **Saleor** (GraphQL-native e-commerce platform) |
| MeshEats (UberEats/Amazon Logistics) | **DDS (Delivery Dispatch System)** projects like **Karrio** (multi-carrier shipping API, useful for the dispatch/attestation layer) | **Open Food Network** (cooperative food-distribution marketplace, closest existing philosophical match) |
| MeshRide (Uber/Lyft) | **Ride Austin's open codebase (legacy reference)** | **Open Mobility Foundation's MDS (Mobility Data Specification)** (trip data/attestation schema reference) |
| MeshLocker (Amazon Lockers) | **OpenWRT-based smart-lock firmware projects (e.g., ESPHome for the access-control peripheral)** | **KeyWe/Nuki open API patterns** (commercial but API-documented; used as a UX/protocol reference, not forked directly) |
| MeshMail (postal) | **Mailu** (self-hosted mail stack, reference for sorting/routing logic even though it's email not physical mail) | **OpenPGP / age** (encryption reference for certified-mail-equivalent attestations) |
| Lakou Marketplace (TaskRabbit/Instacart/Airbnb/Upwork) | **Sharetribe** (open-source multi-vendor marketplace framework) | **OpenBazaar** (defunct but architecturally relevant — P2P marketplace with built-in escrow/reputation, closest historical precedent) |
| MeshKit (HelloFresh) | **Open Food Network** (same as MeshEats — cooperative food-box logistics fit) | **Grocy** (self-hosted household inventory/meal-planning, reference for the recipe/ingredient data model) |
| MeshRescue (Too Good To Go) | **FoodKeeper / OpenFoodFacts** (food expiry and product data) | **Ampled**-style cooperative platform patterns (for the impact-ledger/cooperative-accounting piece) |
| MeshSocial apps — MeshFeed | **Mastodon** | **Bluesky (AT Protocol)** |
| MeshFrame (Instagram) | **Pixelfed** | **PeerTube** (for the media-transcoding pipeline reference, even though PeerTube is video-first) |
| MeshClip (TikTok) | **PeerTube** | **Owncast** (live/short-form streaming infra reference) |
| MeshCircle (LinkedIn) | **Humhub** (open-source social network framework with professional-network features) | **Funkwhale**-adjacent federation patterns *(weak fit — flag for better reference; LinkedIn-equivalents are thin in OSS)* |
| MeshBoard (Reddit) | **Lemmy** | **Discourse** |
| MeshTalk (Discord/Slack) | **Matrix (Element)** | **Rocket.Chat** |
| MeshWiki (Wikipedia) | **MediaWiki** | **XWiki** |
| MeshDate | **(no strong direct OSS reference exists — dating apps are almost uniformly closed-source)** | Flag as a genuine gap; closest architectural reference is **Matrix** for the chat layer once matched |
| MeshDM (WhatsApp/Signal) | **Signal Protocol (libsignal)** | **Matrix / Element** (federation model) |
| MeshLine (TextNow) | **Jasmin SMS Gateway** (open-source SMS gateway) | **Kannel** (SMS/WAP gateway, long-standing OSS project) |
| MeshBank (banking/fintech) | **Wealthfolio** (local-first portfolio/net-worth tracker — the sovereign, device-local dashboard layer; see §1.2 for why this replaces Mifos X as the primary reference) | **Interledger (ILP)** (cross-border settlement, directly relevant to the Haiti-Diaspora remittance use case, still needed underneath Wealthfolio's tracking layer since Wealthfolio itself doesn't move money) |
| MeshStream (Netflix/YouTube) | **PeerTube** | **Jellyfin** (self-hosted media server, reference for the storage/catalog side) |
| classIQ (education/AI) | **Moodle** (open-source LMS, credential/course-completion data model) | **Open edX** |
| DC-AGD (gunshot detection) | **ShotSpotter has no OSS equivalent; closest is** the open acoustic-event-detection research codebase **YAMNet-based community projects** | **OpenALPR**-adjacent (not gunshot-specific but the sensor-to-alert pipeline pattern is reusable) |
| OpenSecure (OS-PACS/GUARDIAN/SENTINEL/PATROL) | **Frigate NVR** (open-source AI security camera/NVR) | **Home Assistant** (again — for the sensor-orchestration layer) |
| SkyLedger | **OpenDroneMap** (drone imagery processing) | **PX4 / ArduPilot** (open drone autopilot stack) |
| TrafficMesh | **OpenTrafficCam** | **SUMO (Simulation of Urban Mobility)** — relevant for the DC-SIM validation work too |
| DC-RISKPOOL-001 (cooperative insurance) | **(no direct OSS insurance-core project; closest reference)** **Ethereum-based parametric insurance projects like Etherisc** | **Mifos X** (shared with MeshBank — core ledger/policy-tracking pattern) |

### 2.4 Additional DePIN gap modules (from 002 §4)

| Module | OSS reference #1 | OSS reference #2 |
|---|---|---|
| `mesh-render` (GPU rendering gap) | **Render Network's open components / general reference** | **Blender's distributed render-farm tooling (Flamenco)** |
| `mesh-vpn` (decentralized VPN gap) | **Orchid** | **WireGuard** (the underlying tunnel protocol both Sentinel and Orchid build on) |
| `mesh-positioning` (RTK gap) | **RTKLIB** (open-source RTK-GPS positioning library) | **GEODNET's underlying open reference stack where published** |

---

## 3. Updated gap registry addition

17. **DC-MESHDM-001** — WhatsApp/Signal-equivalent E2E messaging vertical
18. **DC-MESHLINE-001** — TextNow-equivalent SMS-bridge vertical, tied to the existing no-barriers-identity/SMS-access design goal
19. **DC-MESHBANK-001** — full banking/fintech vertical spec; should explicitly absorb the Haiti-Diaspora Sovereign Value Loop remittance flow and cross-reference NorthLedger for tax reporting
20. **MeshDate and MeshCircle OSS-reference gaps flagged** — both verticals have weak open-source precedent and may need more original design work rather than a fork-and-adapt approach

---

## 4. Onion routing / Tor integration — complexity analysis for the mesh network

This addresses whether `mesh-vpn` (flagged as a gap in 002 §4) should be built as Tor-style onion routing, and what that costs the rest of the architecture. Short answer: **it's compatible but not free — expect a real latency/complexity tax concentrated at the gateway-node tier, plus one genuine philosophical tension with `dc-registry`.**

### 4.1 What onion routing actually adds

Standard Tor: client picks a circuit of 3 relays (guard, middle, exit), wraps the payload in three layers of encryption, each relay peels one layer and forwards, so no single relay knows both origin and destination. A `.onion` hidden service skips the exit node entirely — both ends stay inside the network.

### 4.2 Where it fits the existing architecture

- **Mesh nodes as relays**: any SHI node already running `mesh-connectivity` is a natural Tor-relay candidate — it's already forwarding traffic for neighbors under Proof-of-Coverage. A `mesh-vpn` mode is close to "PoC, but the payload is onion-wrapped and the reward metric shifts from coverage-proof to relay-throughput-proof."
- **Gateway nodes as guard/exit candidates**: your existing two-tier design (local SHI nodes + high-capacity gateway nodes with real backhaul) maps almost exactly onto Tor's guard/exit role split. Gateway nodes are the ones with stable, high-bandwidth internet — they're the only sensible exit-node candidates; ordinary SHI nodes make fine middle/guard relays but shouldn't be exits.
- **`.onion`-style hidden services for D-Central's own services**: MeshShop private catalogs, MeshBank's local dashboard sync, MeshTalk servers — any of these could be exposed as hidden services reachable only through the mesh's own onion layer, which is a strong privacy upgrade with no new primitive needed (it's `mesh-connectivity` + a routing mode, not a new module).

### 4.3 Real complexity costs

1. **Latency stacking on top of an already delay-tolerant network.** D-Central's mesh already tolerates DTN-style store-and-forward delay for many services (event-sourced sync, offline-first delivery apps). Onion routing adds *interactive* latency (3+ hop round trips) on top of that. Fine for MeshTalk chat or MeshBank dashboard sync; bad for anything latency-sensitive like MeshRide real-time dispatch or SkyLedger's low-latency drone control links — those should explicitly bypass onion routing rather than route through it by default.
2. **Bandwidth overhead compounds with mesh's existing constraints.** Every hop re-encrypts and forwards the full payload; on a bandwidth-constrained residential mesh (the SHI model assumes modest home-tier connectivity, not datacenter uplinks), running relay traffic for strangers on top of your own household's usage is a real resource cost, not just a software toggle — this needs its own line in the SHI financial model (a `mesh-vpn` revenue tier, paid in D-Credit per relayed byte, same reward-tier pattern as the other seven modules) or node operators will simply disable it.
3. **Circuit-building overhead on a partial-mesh, not a full internet-scale relay pool.** Tor's anonymity set depends on having thousands of relays to choose from. A D-Central deployment scales from 10-node GNS3 skeletons up toward city-scale — at small cluster sizes (the 10/20/50/100-node financial model you've already built), the anonymity set is small enough that traffic analysis becomes easier, not harder. Onion routing gives real protection only once a cluster is large enough (hundreds to thousands of active relay-capable nodes); below that it's mostly latency cost without much anonymity benefit. Worth stating explicitly in whatever spec covers this: **`mesh-vpn` is a value-add that activates meaningfully at scale, not from node one.**
4. **Tension with `dc-registry` and `dc-attestation`.** The rest of the architecture is built around DID-linked, attestable, accountable nodes — the opposite design goal from anonymity. A relay node forwarding onion traffic should *not* be attestable as to what it's carrying (that's the point), which means `mesh-vpn` traffic needs to be explicitly exempted from the attestation/audit patterns every other module uses. This is a genuine design fork, not just an engineering detail: you're choosing to run one mode of the network that is deliberately *not* accountable in the way DC-STATUS-001's honesty-discipline philosophy applies to everything else. Worth deciding early whether `mesh-vpn` is scoped narrowly (protecting *what* people are doing on top of the mesh — browsing, messaging — while the mesh operator layer itself stays fully attestable) rather than trying to make the whole network anonymous end to end.
5. **Exit-node legal exposure.** Whichever gateway nodes serve as Tor-style exits inherit the same liability profile real-world Tor exit operators face (traffic exiting to the open internet is attributed to the exit IP). Given your security background, this is the one item that needs a genuine legal/policy answer before deployment, not just an engineering one — likely resolved the same way Tor's ecosystem resolves it (informed, opt-in exit operation, possibly restricted to specific gateway nodes rather than every SHI node, with clear operator disclosure).

### 4.4 Recommended scoping if pursued

- Treat as `mesh-vpn`, a **mode of `mesh-connectivity`**, not a ninth standalone module — it reuses PoC-style relay accounting, just with onion-wrapped payloads and a different reward metric.
- Guard/middle relay role: any SHI node, opt-in, D-Credit-rewarded per relayed byte.
- Exit role: gateway nodes only, opt-in, clearly disclosed, likely the one place in the whole ecosystem where legal counsel review matters before code.
- Default-on for specific service types (MeshTalk, MeshBank sync, MeshDM metadata protection) where latency tolerance is high; default-off for latency-sensitive real-time services (MeshRide dispatch, SkyLedger control links, TrafficMesh).
- Explicitly exempt from the standard attestation/audit pattern that governs every other module — document this as an intentional carve-out, not an oversight, given how central attestation is to the rest of the architecture.

---

*DC-TAXONOMY-003 — extends 001/002. Adds MeshDM (WhatsApp/Signal), MeshLine (TextNow), and MeshBank (full banking/fintech vertical rebuilt on Wealthfolio's local-first portfolio model rather than Mifos X's core-banking model, absorbing Haiti-Diaspora remittances and NorthLedger tax reporting). Tags two open-source reference projects for every dcentral-core service, mesh module, and Layer 4 vertical across the taxonomy; flags MeshDate and MeshCircle as having weak OSS precedent. Adds a complexity analysis for onion-routing/Tor-style `mesh-vpn` integration, scoping it as a `mesh-connectivity` mode with an explicit attestation carve-out.*
