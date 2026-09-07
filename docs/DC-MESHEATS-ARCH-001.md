# DC-MESHEATS-ARCH-001 — MeshEats Complete Technical Architecture

**Provenance note (added 2026-09-07):** this doc previously existed only inside the `MeshEats` GitHub repo
(`RedjiJB/MeshEats`, cloned into `raw-export/external-repos/MeshEats/docs/DC-MESHEATS-ARCH-001.md` as part
of a broader external-source ingestion — see [DC-COMPUTE-SILICON-ARCH-001](DC-COMPUTE-SILICON-ARCH-001.md)'s
sibling checkpoint in `registry/DC-REG-001-Master-Registry.md` §0), not in this knowledge base. Content below
is unchanged from the source except for this note and the **Build status** annotation added to §4 — see that
section for why the annotation was necessary before this doc could be trusted at face value.

**One-line:** A decentralized food marketplace where certification (not a fixed menu) is the trust mechanism, delivery reuses the MeshRide Mobility Core, and chefs are onboarded through a guided recipe/training pipeline rather than left to figure it out alone.

**Positioning:** MeshEats is a sibling vertical to MeshRide, sharing one **Trust & Mobility Core** (identity, dispatch, settlement, governance). This doc specs the MeshEats-specific layers plus the shared Core reuse points.

---

## 1. Layered stack

```
┌──────────────────────────────────────────────────────┐
│ APP LAYER     Customer App · Chef App (+Training)     │
│               · Driver App (shared) · Admin/DAO panel │
├──────────────────────────────────────────────────────┤
│ DISPATCH      Order routing · storage-check           │
│               (reheat vs cook-fresh) · driver match    │
├──────────────────────────────────────────────────────┤
│ TRUST         DID/VC issuance · trust registry ·       │
│               revocation · batch attestation            │
├──────────────────────────────────────────────────────┤
│ TRAINING      Recipe library · practice log ·          │
│               skill certification review                │
├──────────────────────────────────────────────────────┤
│ SETTLEMENT    Escrow · dynamic weekly payout ·          │
│               DAO treasury cut                          │
├──────────────────────────────────────────────────────┤
│ GOVERNANCE    DAO: role-weight table, standards,        │
│               disputes, admission                       │
├──────────────────────────────────────────────────────┤
│ HARDWARE      Kitchen Node · Storage Node ·             │
│               Reheat Station · Transport-VC device      │
└──────────────────────────────────────────────────────┘
```

---

## 2. Frontend apps

### 2.1 Customer App
- Discovery: open browse (by cuisine/Skill-VC tag) or direct chef request
- Order-time toggle: **hot / cold / customer-reheats**
- Trust display: Kitchen-VC + Dish-VC + batch attestation shown as a verified badge, tap to see chain of custody
- Order tracking, wallet/order history, rating (overall + per-cuisine sub-score)

### 2.2 Chef App — the streamlined side (see Section 3 for the training module in full)
- **Order queue**: accept/ready/handoff, same UX pattern as a driver app
- **Capacity board**: declared ingredients on hand + free time slots (replaces a static menu)
- **Dish declaration at order time**: chef confirms what they're making + ingredients → mints per-order Dish-VC
- **Batch log**: photo + sensor read auto-attached from the Kitchen Node
- **Training Hub**: recipe library, practice mode, certification submission (Section 3)
- **Earnings view**: credits earned this cycle, running estimate against last week's Credit Value

### 2.3 Driver App
- Fully shared with MeshRide — same DID, same dispatch queue, delivery-mode-aware routing (pickup from kitchen vs. reheat hub)

### 2.4 Admin / DAO Panel
- Role-weight table editor, trust registry management, treasury/payout batch review, dispute queue, MEHKO-style jurisdiction config (which counties/regions are live)

---

## 3. Chef Recipe & Training Module (new — this is what makes onboarding streamlined)

This is the answer to "how does a chef learn, practice, and get certified without guesswork":

1. **Recipe Library** — structured recipe cards: ingredient list with quantities, step-by-step instructions with photos, required equipment, estimated time, allergen profile, safe storage/reheat spec. Sourced from community-contributed recipes (culturally significant dishes chefs submit) or platform-curated staples.
2. **Learning path** — a chef browses recipes inside their current Skill-VC scope, or picks a new cuisine/technique to expand into. This is explicitly *not* a fixed menu — it's a skill-building catalog.
3. **Practice mode** — chef logs a practice attempt (not for sale): photo, self-notes, optional mentor-chef review. Experienced chefs can mentor newer ones as a credited cooperative role, not just top-down QA.
4. **Certification submission** — once ready, the chef submits a real batch for review. A delegated auditor (or structured self-check against the recipe's defined safe-prep parameters — temps, allergens) approves it, which **expands the chef's Skill-VC** or unlocks that specific recipe as certified within their Kitchen-VC scope.
5. **Why this matters beyond onboarding**: it's also your quality-consistency mechanism. Without a corporate fixed menu, this is what gives a customer a reasonable guarantee that "chef X making dish Y" will taste like what's described — the recipe card sets the standard, the certification confirms the chef can hit it.

---

## 4. Backend services

**Build status (added 2026-09-07, not in the original doc):** a source-code inspection of the `MeshEats`
repo found **4 of these 7 services actually implemented** (Identity & Trust, Dispatch/Matching,
Certification/Compliance, Training — real TypeScript services, smoke-tested) and **3 speced but not yet
built** (Settlement, Governance, Notifications — no corresponding code found anywhere in the repo). The
table below is otherwise unchanged from the original spec; treat the "Suggested stack" column as intended
design for all 7, and the status column as the only guide to what actually exists right now.

| Service | Responsibility | Suggested stack | Status |
|---|---|---|---|
| **Identity & Trust** | DID issuance, VC minting (Kitchen/Operator/Skill/Dish-VC), trust registry, StatusList2021 revocation | Veramo or custom did:web/did:key implementation; signed append-only log, not a public blockchain | **Built** |
| **Dispatch/Matching** | Order routing, capacity-board matching, storage-check (pull-and-reheat vs. cook-fresh), driver assignment | Node/Python service, reuses MeshRide's matching engine | **Built** |
| **Certification/Compliance** | Sensor ingestion from Kitchen/Storage Nodes, batch-attestation hashing, HACCP log generation | MQTT ingestion → time-series store | **Built** |
| **Training** | Recipe CMS, practice-attempt logging, certification review workflow | Standard CRUD service + media storage | **Built** |
| **Settlement** | Two-sided weekly batch (customer billing resolves first, worker payout second) — see Section 9 | Scheduled job + ledger DB | **Not started** |
| **Governance** | DAO voting, weight-table config, treasury dashboard | Simple governance service; DAO logic doesn't need to live on-chain to function | **Not started** |
| **Notifications** | Order updates, certification results | WhatsApp Business API + push | **Not started** |

---

## 5. Data layer

- **PostgreSQL + PostGIS** — orders, users, locations, matching queries (same as the MeshRide MVP decision)
- **Time-series store** (TimescaleDB/InfluxDB) — continuous temp/humidity streams from Kitchen and Storage Nodes; this is what backs batch attestation and auto-revocation on an out-of-range reading
- **VC/credential records** — hash-referenced object storage, not a public chain; the trust registry is a DAO-governed signed list, not something that needs global blockchain consensus

---

## 6. Hardware summary

| Node | Core hardware | Role |
|---|---|---|
| **Kitchen Node** | Business-grade router/AP (segmented, see Section 10) + Pi 5 compute endpoint + ATECC608B secure element, temp/humidity probes, smart scale, smart outlets, CO₂ sensor, camera | Signs Kitchen-VC evidence, generates per-batch HACCP log, hosts the local DTN queue |
| **Storage Node** | Extends Kitchen Node + continuous temp logging, door-breach sensor, UPS/power-loss monitor, RFID/barcode | Continuous compliance stream per stored batch; auto-revokes on breach |
| **Reheat Station** | Same node class + induction/convection unit at the DAO-owned hub | Appends "reheated-at" event to batch log |
| **Transport-VC device** | Passive (insulated + temp logger) or active (heated bag) | Cold-chain/hot-chain proof during delivery |
| **Packaging** | Sealed/insulated containers, tamper-evident seal, printed QR/NFC tag | Physical anchor of the trust chain — see Section 11 |

---

## 7. Build sequence

1. **Web PWA first** — responsive, installable, zero App Store review risk. Chef App + basic Customer App only; skip Driver App (chef self-delivery/pickup at this stage).
2. **Prove it with 2–5 anchor chefs** inside one trusted community — Training Module doesn't need to be built yet if all early chefs already know their dishes; build it once you're recruiting chefs *beyond* your first trusted circle and need a standardized onboarding path.
3. **Add MeshRide-based dispatch** once order volume in one area exceeds what a chef can hand-deliver.
4. **Wrap as native app** (Capacitor/React Native) for App Store/Play Store once the web version is validated with real orders.
5. **DID/VC, DTN, and kitchen mesh build real from day one** — see Section 8. What still phases in is *which issuers are legally authoritative* behind the trust registry, not the technical layer itself.

---

## 8. Day-1 Sovereign Stack — DID/VC, DTN, and Kitchen Mesh

MeshEats is a reference deployment of the D-Central protocol itself, so the identity and networking layers get built real from the start — with one honest caveat: the *cryptographic infrastructure* can exist immediately, but the *legal weight* behind a signature still depends on real-world relationships (health-authority delegation, insurer sign-off) that take the time they take regardless of how early the code is written. Building the scaffolding now means it's ready the moment the legal layer catches up, instead of being retrofitted later — it doesn't make the credentials officially recognized any sooner.

**DID/VC from day one**
- Every Kitchen Node generates its own DID at first setup — `did:key` or a custom `did:dcentral` method, private key held in the ATECC608B secure element, never leaves the device.
- Kitchen-VC, Operator-VC, Skill-VC, and Dish-VC schemas are built and issued from day one. Early issuer is the DAO itself (community attestation) or a delegated volunteer inspector; later it upgrades to a real health-authority-recognized issuer — the credential's *structure* doesn't change when its *legal weight* does.
- The Trust Registry launches as a DAO-governed signed list from day one — this piece genuinely doesn't need to wait, since it's your own governance, not an external regulator's.

**DTN (Delay-Tolerant Networking) — why the kitchen layer specifically needs it**
Home kitchens run on consumer internet, which drops. A HACCP log or batch attestation can't stop recording because someone's Wi-Fi hiccuped mid-cook. So the Kitchen Node is local-first:
- Sensor logging, VC signing, and batch-record creation happen and get cryptographically sealed locally on the Pi, regardless of connectivity.
- A store-and-forward sync layer (bundle-protocol-style, or a simpler local MQTT broker with a persistent outbox) queues everything and pushes it to the coordination backend the moment connectivity returns. Nothing is lost to a dropped connection, and the chef is never blocked from cooking by a dead router.

**Mesh — scoped to the kitchen cluster, not the whole city**
- Kitchen Nodes within range mesh with each other and with the neighborhood Storage/Reheat hub over local wireless — Wi-Fi mesh for short range, or a low-power radio link (LoRa/Meshtastic) for a wider, low-bandwidth backbone.
- Purpose: if one kitchen's home internet is down, its node relays sync data through a neighboring node that still has connectivity, instead of going dark until the ISP comes back.
- This is the same mesh-compute philosophy as the rest of the D-Central network, deliberately scoped down to the kitchen cluster rather than the whole dispatch layer, which can still ride ordinary internet/cellular for now.
- Full router/AP/VLAN specification for the physical home network this all runs on: see Section 10.

---

## 9. Two-Sided Weekly Settlement

Customer billing and worker payout are two halves of one weekly batch process, and the order they run in is what makes the model self-balancing.

**Step 1 — Customer billing resolves first.** At week's end, each customer's stored payment method is charged (or captured, if using authorization holds) for their accumulated meals. Price per meal isn't a fixed menu price — see the three pricing models below.

**Step 2 — Real collected revenue becomes the distributable pool.** Only once Step 1 actually clears does the system know real revenue collected, not just projected system cost. Distributable Pool = Total Collected Revenue − DAO Treasury Cut.

**Step 3 — Worker payout resolves from the real pool.** Credit Value = Distributable Pool ÷ Total Credits Issued that week, same mechanism as your existing dynamic payout design.

**Why the sequencing matters:** a bad billing week (declined cards, non-payment) doesn't need a separate write-off process — it flows straight through as a smaller distributable pool, meaning a slightly lower Credit Value for everyone that week rather than a concentrated loss on one chef or driver. Bad debt gets absorbed the same way demand swings already are: thinly, across the whole membership.

**Payment capture mechanics**
- Preferred: stored card + weekly auto-charge, with retry/dunning logic and a "no new orders until resolved" rule on repeat failures — standard subscription-billing pattern, no hold-expiry timing to manage.
- Alternative: authorize-and-capture per order using an extended-authorization window (up to ~29 days on Visa/Mastercard/Amex/Discover via Stripe) rather than a standard hold, which typically expires around 7 days — too close to the edge of a full weekly cycle to rely on.

**Ecosystem price point — three models**

| Model | How it works | Tradeoff |
|---|---|---|
| **Pure cost-recovery pool** | Price/meal = Total System Costs ÷ Total Meals Consumed that week | Most "at-cost," but a slow week raises price and can suppress demand further — needs a treasury reserve to avoid a spiral |
| **Hybrid (recommended default)** | Chef's stable base price + a floating ecosystem fee for shared infrastructure, calculated the pool way | Protects chef earnings from system-wide swings while keeping shared costs transparent |
| **Declared-ingredient cost-plus** | Actual ingredient cost (already captured per Dish-VC) + a floating system-wide overhead multiplier | Most transparent to the customer, strongest differentiator vs. opaque delivery-app markup |

---

## 10. Kitchen Node Network Architecture — Full Segmented Home Network

The Kitchen Node isn't a Pi riding whatever Wi-Fi the household already has — it needs its own router/AP layer, segmented from the rest of the home, the same pattern as the rest of your SHI node deployments, with a business VLAN added on top.

**Hardware**
- A real small-business-grade router/AP (Ubiquiti UniFi/EdgeRouter class, or pfSense/OPNsense on dedicated hardware) — not a consumer router. This is the network's edge device, not the Pi.
- The Pi 5 Kitchen Node sits behind it as a compute/sensor endpoint.

**Segmentation — three VLANs minimum**
1. **Business VLAN** — Kitchen Node, sensors, camera, order-queue tablet, POS. This is what talks to the coordination backend and signs VC/batch data.
2. **Household VLAN** — the family's own devices, fully isolated from the business VLAN.
3. **Guest/IoT VLAN** — any existing home smart-home gear stays off both of the above; a compromised smart bulb shouldn't have a network path to signing keys, and business traffic shouldn't be visible to household personal devices.

**Why this matters beyond security**
- Liability: a home commercial food operation sharing a broadcast domain with a kid's game console or a guest's phone is a real insurance/audit question, not just a technical nicety.
- This router is also the local DTN store-and-forward node from Section 8 — it needs enough local storage to queue sensor/batch data through an internet outage, and it's the gateway for the kitchen-to-kitchen mesh backbone linking to neighboring Kitchen Nodes and the Storage/Reheat hub.
- A Kitchen Node is effectively a Tier 2/3 SHI node with commercial segmentation layered on top — same underlying pattern as the rest of your Mesh Home work, not a separate architecture built from scratch.

---

## 11. Packaging & Cooperative Supply Chain

Packaging is the physical anchor of the trust chain, and a genuine cooperative-economics lever — not just logistics.

**Packaging as part of the trust chain**
- Every sealed package carries a printed QR code or NFC tag, generated at pack time, linked to that order's batch attestation — scan it and see the full chain: Kitchen-VC, chef, Dish-VC, ingredients/allergens, batch sensor log, reheat instructions if delivered cold.
- Tamper-evident sealing doubles as a food-safety measure and a physical extension of the digital certification — a broken seal is visible evidence independent of anything in the app.
- Required label fields, matching the earlier regulatory findings: product name, ingredients, allergens, "made in a certified home kitchen" disclosure, batch ID.

**Packaging types**
- Insulated/thermal containers for hot delivery, compatible with the Transport-VC device from Section 6
- Leak-proof sealed containers, distinct specs for liquids/sauces vs. solids
- Compostable/eco-friendly material as the default — both a sustainability position and increasingly a jurisdictional expectation

**Cooperative angle**
- Packaging materials get bulk-purchased by the DAO, not sourced individually by each chef — this is the original cooperative bulk-purchasing concept from day one, applied to a real recurring cost every chef actually has.
- Stocked centrally at the Storage/Reheat hub, so chefs pick up standardized packaging rather than sourcing their own — this also keeps the QR/seal system consistent across the whole network instead of fragmenting across different containers per chef.
- Packaging cost is one more line in the "ecosystem cost" pool from Section 9 — a real component of what the floating ecosystem fee is recovering.

---

## 12. Distributed Storage Layer (Mesh Archive)

Not to be confused with the Storage Node in Section 6 (food cold storage) — this is data/media storage, a separate layer entirely.

**What it's for**
- Batch attestation evidence — photos and sensor-log bundles referenced by the trust chain
- Recipe Library media — training photos/videos from Section 3
- VC documents and supporting evidence too large to keep in the primary database

**What it's NOT for**
- Transactional/relational data — orders, users, the credit ledger, matching queries. That stays in PostgreSQL from Section 5.

**How it works**
- Content-addressed storage (IPFS-style) — a file's address is a hash of its own content, so tampering changes the address. A second, independent integrity check on top of the VC's digital signature, not a replacement for it.
- Run as a **private cluster**, not the public IPFS network — relying on strangers' altruism to keep food-safety evidence available is a real risk, not a theoretical one.
- Pinning nodes: a subset of Kitchen Nodes, the Storage/Reheat hubs, and a couple of dedicated low-cost archive boxes, each replicating a share of the data. Cooperative-owned storage capacity, same asset-pooling logic as everything else — no recurring cloud bill, no third party controlling access to your own evidence trail.

---

## 13. Contributor Equity Track (Marketing, Advertising, Development)

A third category, distinct from both the operational D-Credits (Section 9) and the investor capital shares discussed separately — worth keeping conceptually separate even though all three could sit on the same underlying co-op share infrastructure.

| Track | Who | Instrument | Liquidity |
|---|---|---|---|
| **Operational D-Credits** | Chefs, drivers | Non-transferable contribution points | Weekly cash-out via the two-sided settlement (Section 9) |
| **Investor capital shares** | People putting in money | Real co-op investment shares (Ontario Co-operative Corporations Act, via the NI 45-110 crowdfunding exemption) | Per exemption terms; no public market |
| **Contributor equity** | Marketers, advertisers, developers | Equity-like compensation for services, vesting over time | Deferred — requires a defined redemption mechanism, see below |

**What "paid now, cash out later" actually requires**
Compensating contributors with equity is a well-worn pattern ("sweat equity"), but it's still equity compensation — two things have to exist for the deferred cash-out to be real rather than a hope:

1. **A defined redemption mechanism, written into the bylaws.** No public market exists for a private co-op's shares, so "cash out" has to mean something concrete: the co-op buys back vested contributor shares at a formula-based valuation, on a defined schedule or milestone, subject to available treasury funds.
2. **Vesting tied to verified contribution, not just time** — marketing reach achieved, features shipped — tracked with the same auditable rigor as Skill-VC certification, not a flat grant.

**Tax reality worth flagging early**
Equity issued for services is generally taxable to the recipient at the moment it vests, based on fair market value — and establishing fair value for a private, non-traded co-op share is genuinely difficult with no market price to reference. This needs real accounting and legal input before anyone starts earning toward it, not after.

---

## 14. D-Central Synchronization Layer

**Smart contracts — substance, not the public-chain wrapper**
Deterministic, auditable rule execution — escrow release, weekly Credit Value calculation, revenue-split by role weight, revocation cascades — runs as DAO-governed logic on cooperative-owned infrastructure. Signed inputs, deterministic code, tamper-evident output record. This gets the real value of a smart contract without the token-classification and gas-cost questions already avoided in Sections 9 and 13.

**DAO governance — batch-synchronized, not live consensus**
Same shape as the weekly settlement: proposals open for a defined window, votes are locally signed and queued through the Section 8 DTN layer if a node is offline, tally resolves once the window closes. Real-time consensus across intermittently-connected kitchens fights the DTN design instead of using it.

**Cryptographic ledger — permissioned, not public**
The credit ledger, trust registry, and revocation list are a permissioned, hash-chained log replicated across DAO-owned nodes (Kitchen Nodes, hubs, the archive nodes from Section 12). Because every node belongs to a known, vetted cooperative member rather than an anonymous public participant, conflict resolution can be a simple DAO rule (latest-signed-timestamp-wins, audit flag on conflicts) rather than full Byzantine fault tolerance. A public/permissionless chain would reopen the regulatory questions Sections 9 and 13 were built to avoid.

**eBPF — kernel-level enforcement**
- **VLAN enforcement**: an eBPF-based networking layer (Cilium's pattern) continuously verifies business-VLAN traffic from Section 10 never reaches household devices, rather than trusting router config alone.
- **Tamper detection**: an eBPF-based runtime monitor (Falco's pattern) watches each Kitchen Node for anomalous behavior — a process probing the secure element, an unexpected outbound connection — and auto-quarantines that node's VC-issuing capability the moment it's detected.
- Both run cheap on constrained Pi hardware over unreliable links, consistent with the lean-sovereign-infrastructure approach throughout.

---

## 15. Ecosystem Integration — DC-OS, D-Central Services, and Agents

MeshEats is a vertical inside the ecosystem, not a standalone system — several pieces built earlier in this doc (dispatch, apps, agent-shaped work) already have a home in the existing D-Central stack.

**DC-OS**
The Customer/Chef/Driver apps in Section 2 aren't separate apps in the full sovereign version — they're DC-OS surfaces, rendered based on what a person's DID and VCs authorize. A chef's Kitchen-VC and Skill-VC determine what DC-OS shows them; a Kitchen Node can run DC-OS as its interface layer directly, node-native and orb-native, rather than a bolted-on custom app.

**Cross-vertical reuse**
- **DC-FRACTAL-001 / DC-TPL-000** — MeshEats should formalize as a DC-TPL template: a replicable venture pattern, consistent with the reference-deployment-instance-#001 model the rest of the portfolio follows, rather than a one-off build.
- **DC-SWARM-001 (stigmergic coordination)** — replaces bespoke dispatch logic in Section 4: chefs MARK availability on the capacity board like a pheromone trail, it DECAYs if unclaimed, drivers ALIGN toward active order density, a batch gets CLAIMed rather than centrally assigned.
- **DAO governance tiers** (household → campus → federation) — MeshEats' DAO structure slots into this existing tiering: kitchen-level decisions at household tier, hub-level at campus tier, cross-city standards at federation tier.

**AI and agents**
MeshEats plugs into the existing Unified Intelligence Interface as another vertical (intent parser → ecosystem router → multi-agent execution → optimization → response), on the same CrewAI/LangGraph/n8n stack already running Sod Boys FieldOps:
- **Dispatcher agent** — works alongside the DC-SWARM stigmergic layer, doesn't replace it
- **Inventory-checker agent** — capacity board and Storage Node stock levels
- **Exception-escalator agent** — failed payments, food-safety flags, the eBPF tamper alerts from Section 14
- **Training-mentor agent** — inside the Recipe/Training Hub from Section 3, walking a chef through a new dish and reviewing practice submissions

**Governance chain**: DAO decides → policy is written → OPA-style enforcement → agents act within those bounds. A dispatcher agent structurally cannot route around a revoked Kitchen-VC or override the role-weight table, because a policy layer sits between its intent and its execution — the mechanism that makes "the co-op governs the AI" real rather than aspirational.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

**References:**
- [[DC-COMPUTE-SILICON-ARCH-001|DC-COMPUTE-SILICON-ARCH-001 — Compute Silicon Class Architecture (v1, generated 2026-09-07)]]

<!-- AUTO-GENERATED RELATED END -->
