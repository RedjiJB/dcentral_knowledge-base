# DC-TAXONOMY-005: Car Rental/Delivery & Contracting Verticals, mesh-vpn Mechanics, Recursive DAO-Agent Governance
### Extends DC-TAXONOMY-001/002/003/004

---

## 1. New verticals

### 1.1 MeshCar (Turo/Zipcar/Hertz-equivalent car rental)

| Primitive | D-Central equivalent | Built from |
|---|---|---|
| Vehicle listing | Owner lists their car as a rentable asset — same listing pattern as a Lakou Marketplace/Airbnb-equivalent item, vehicle-specific fields (make/model/insurance-VC) | Lakou Marketplace + `dc-identity` (insurance credential) |
| Keyless unlock | The car itself carries a mobile node (same hardware class already used for delivery/TrafficMesh); it verifies a renter's booking-VC locally to unlock, no cellular dependency | `mesh-sensors` mobile node + `dc-attestation` booking-VC check |
| Usage-based billing | Meter runs off the mobile node's own telemetry (mileage, time), settled automatically at drop-off | `dc-credit` micropayment-channel |
| Damage/condition disputes | Before/after photo + sensor attestations (any dashcam-equivalent sensor data) feed the same `dc-governance` dispute-jury pattern as any marketplace dispute | `dc-attestation` + `dc-governance` |
| Fleet operator (vs. peer-to-peer owner) | A cooperative-owned vehicle pool works identically, just with `dc-governance` treasury owning the asset instead of an individual DID | `dc-governance` treasury-manager |

### 1.2 MeshCarDelivery (vehicle transport/delivery — think Amazon's car-buying delivery, or a car-hauler/logistics service)

| Primitive | D-Central equivalent | Built from |
|---|---|---|
| Book a vehicle transport (dealer-to-buyer, or relocation) | Lakou Marketplace listing, vehicle-class freight — same primitive as the Uber Freight-equivalent listing already specified for cargo, matched via `dc-registry` capability-index to car-hauler-class mobile nodes | Lakou Marketplace + `dc-registry` |
| Chain-of-custody / condition verification | Each handoff point (pickup, hauler, drop-off) generates a signed condition-attestation, so a dispute over transport damage has a full attestation trail instead of a he-said-she-said | `dc-attestation` |
| Escrow release on confirmed delivery | Buyer confirms receipt (or an automated GPS/geofence + condition-match attestation triggers it) | `dc-credit` escrow-engine |

### 1.3 General contracting services (plumbers, electricians, HVAC, home renovation — beyond Lakou Marketplace's lighter gig-task scope)

This deserves its own named vertical rather than folding entirely into Lakou Marketplace, because licensed-trade work has requirements gig tasks don't: license verification, permits, multi-milestone payment, and liability that actually matters legally.

| Primitive | D-Central equivalent | Built from |
|---|---|---|
| Licensed contractor directory | DID + license-VC (issued by whatever licensing body — municipal, provincial/state — acts as the VC issuer, same pattern as an insurance-VC) | `dc-identity` |
| Multi-milestone project (e.g., a kitchen renovation) | Escrow with staged releases per milestone-attestation (framing done → inspection-VC → next draw released), rather than one lump 120%-lock like a simple task | `dc-credit` escrow-engine, extended for multi-stage release |
| Permit/inspection | Municipal inspector issues a pass/fail attestation directly into the project's attestation trail — this is a natural extension point for a city government to become a `dc-attestation` issuer without adopting the whole stack | `dc-attestation` |
| Liability/insurance | Contractor's insurance-VC checked before a job can even be posted as accepted | `dc-identity` selective disclosure |
| Group/cooperative buying (materials) | Same cooperative bulk-purchase pattern already native to Lakou Protocol | `dc-governance` |

Suggested name: **MeshBuild**, sitting alongside Lakou Marketplace as a sibling vertical (shared escrow/reputation primitives, different milestone/licensing logic) rather than a Lakou Marketplace listing type.

---

## 2. How mesh-vpn works if it deliberately doesn't use DIDs

Good catch — worth being precise here, because "doesn't use DID" needs to mean something specific, not "has no structure at all." Tor itself doesn't use identity for anonymity either — it uses **onion-wrapped routing plus per-circuit ephemeral keys**, and D-Central's `mesh-vpn` mode works the same way, just riding on mesh relays instead of dedicated Tor relays. Two separate questions collapse into one if you're not careful, so splitting them:

### 2.1 How do relay nodes get paid/rewarded if they can't attest what they carried?

They don't attest *content* — they attest *relay activity itself*, which is a different, deliberately shallow claim:

- Each relay node still holds a DID and is still `dc-registry`-listed as "mesh-vpn relay capable" — **the node's own participation is identity-linked**, that part doesn't disappear.
- What's exempted from attestation is the *traffic the node forwards*, not the node's existence or its willingness to relay. The node proves "I forwarded N encrypted bytes this period" (a bandwidth/uptime claim, verifiable via the same PoC-style witness mechanism `mesh-connectivity` already uses for coverage proofs) without anyone — including the relay operator — being able to prove *what* those bytes contained or where they ultimately went.
- So `dc-credit` payment flows to a known, DID-linked relay operator for a content-blind bandwidth claim. This is exactly the distinction Tor doesn't have to solve (its relays are usually run by donation/goodwill, not paid per-byte) — D-Central's cooperative economics require it, so `mesh-vpn` needs this two-layer split: **operator identity is known; traffic content is not.**

### 2.2 How does the traffic itself move without DID-based routing?

This is the actual onion-routing mechanic, independent of `dc-identity`:

1. **Circuit construction uses ephemeral session keys, not DIDs.** When a user's device builds a 3-hop circuit, it does standard Diffie-Hellman-style key exchange with each relay in turn — these are throwaway keys generated per-circuit, unlinkable to the user's DID or to each other across circuits. The relay nodes know "someone built a circuit through me," not who.
2. **Relay selection still uses `dc-registry`'s capability-index** (which nodes are relay-capable, roughly where they are for latency purposes) — that's public, coarse-grained infrastructure discovery, not a privacy leak, same as knowing which gas stations exist without knowing who's filling up.
3. **The user's own device is still DID-holding for everything else it does** — `mesh-vpn` isn't a separate identity-less device, it's a mode the same DID-holding device switches into for specific traffic. The DID simply never enters the onion-routing protocol itself, the way your passport doesn't get shown at every step of a phone call even though you own the phone.
4. **Exit traffic (leaving the mesh to the open internet) is where identity genuinely can't follow** — by the time traffic reaches a gateway-node exit, three layers of unlinkable relaying have already stripped any path back to the originating DID, which is the entire point and also the source of the exit-node legal exposure flagged earlier.

**Net:** `mesh-vpn` doesn't operate DID-free at the node/economic layer (operators are still known, still paid, still `dc-registry`-listed) — it operates DID-free at the *circuit/traffic* layer, using standard onion-routing ephemeral keys instead. That's the same split real-world Tor has (relay operators are often known/donors; traffic is anonymous) — D-Central just adds a payment layer Tor doesn't have.

---

## 3. Recursive DAO-directed AI research & proposal loop

This is a meaningfully different kind of component from everything else in the taxonomy — the others are *services the network provides to users*; this is **infrastructure for the network to improve itself**, governed the same way everything else is. Worth being careful and explicit about the loop structure, since "AI proposes changes to its own system, DAO approves, recurse" is exactly the kind of design that needs guardrails stated up front, not bolted on after.

### 3.1 The basic loop

```
1. RESEARCH TASK ASSIGNMENT
   dc-governance issues a research mandate (via proposal-engine) —
   e.g. "identify underused DePIN categories," "propose a fix for
   MeshBank's remittance latency," "audit mesh-vpn's exit-node exposure"

2. AGENT RESEARCH
   An assigned agent (Opus-class model or a fleet of narrower agents)
   researches within the mandate's scope: reads the current DC-XXX-001
   specs (mesh-storage's own store, effectively — this taxonomy IS
   the agent's grounding context), searches prior art, drafts a
   proposal: new feature, treasury allocation, module change, or a
   net-new vertical

3. PROPOSAL SUBMISSION
   The agent's output becomes a formal dc-governance proposal —
   same proposal-engine/voting-engine pipeline any human member uses.
   The agent is a proposer, not a decider. No special authority.

4. HUMAN + STAKED-MEMBER VOTE
   voting-engine runs the normal quorum/threshold process.
   Nothing the agent proposes executes without this vote passing.

5. EXECUTION + ATTESTATION
   If passed: treasury-manager releases funds / the module spec
   updates / the new vertical gets registered in the taxonomy.
   The execution itself is attested (dc-attestation), creating a
   permanent, auditable record of what the agent proposed, what
   the vote decided, and what actually happened.

6. RECURSION
   The next research mandate can explicitly include "review the
   outcome of proposal N" — did the funded feature actually improve
   the metric it targeted? This is what makes it recursive: agents
   are tasked with evaluating the consequences of prior agent-originated
   proposals, not just generating new ones in a vacuum.
```

### 3.2 Where this maps onto existing D-Central primitives (nothing new needed at the core)

| Loop stage | Existing primitive |
|---|---|
| Research mandate issuance | `dc-governance` proposal-engine (a mandate is just a specific proposal type: "commission research") |
| Agent identity | Agents get their own DID — `dc-identity` doesn't distinguish human and agent principals architecturally, it just needs an explicit **agent-class credential** flagging "this DID is an AI agent, operating under mandate N, with these scope limits" |
| Proposal submission | `dc-governance` proposal-engine, same pipeline |
| Vote | `dc-governance` voting-engine — **unchanged**, humans/staked members retain sole decision authority |
| Treasury execution | `dc-governance` treasury-manager |
| Audit trail | `dc-attestation` — every agent research output, proposal, and outcome review is a permanent attestation, so the whole recursive history is inspectable |
| Fresh grounding each cycle | The agent's context for each research task should literally be the current state of this taxonomy + the relevant DC-XXX-001 specs, i.e. this document series becomes the agent's living knowledge base — worth keeping it in a `mesh-storage`-hosted, version-controlled form specifically so agents (and humans) always research against the current architecture, not a stale copy |

### 3.3 Guardrails worth stating explicitly, given the recursive framing

1. **Agents propose, they never execute unilaterally.** Every stage that moves funds or changes a spec passes through the *unchanged* human/staked-member voting-engine. This is the single most important guardrail and it requires no new mechanism — it's just a firm rule about which stage agents are allowed to participate in (1–3, 6) versus which they're categorically excluded from (4–5).
2. **Scope-limited mandates, not open-ended authority.** An agent-class credential should carry an explicit scope (which modules/verticals it's mandated to research) — same selective-disclosure/scoping pattern already used for every other credential type in this architecture, not a special case invented for agents.
3. **Recursion needs an explicit "review prior outcomes" step, not just "propose more."** Without stage 6 built in deliberately, a recursive agent loop tends toward generating novelty rather than checking whether previous novelty actually worked — the loop as specified above forces outcome-review to be a first-class research-mandate type, not an afterthought.
4. **Rate/quantity limits on proposal volume**, governed by `dc-governance` itself (the DAO can vote to throttle how many agent-originated proposals reach a vote in a given period) — protects against proposal-spam overwhelming human voting bandwidth, using the same throttling logic any DAO would apply to human proposal spam.
5. **The attestation trail is what makes this auditable rather than a black box.** Because every stage produces a `dc-attestation` record, a future review (human or agent) can reconstruct exactly which agent proposed what, under which mandate, and what happened — this is the same accountability discipline the rest of the architecture already insists on (DC-STATUS-001's honesty-discipline philosophy), just applied to the agents doing architecture work rather than to nodes doing infrastructure work.

### 3.4 A worked example, to make the loop concrete

```
Mandate: "Review mesh-vpn's exit-node legal exposure (flagged in
DC-TAXONOMY-003 §4.3) and propose a mitigation."

Agent research: surveys real-world Tor exit-node legal precedent,
reviews DC-TAXONOMY-003's existing scoping (exit role restricted to
gateway nodes only), proposes: exit-node operation requires an
explicit opt-in legal-disclosure-VC, and DAO treasury funds a legal
defense pool that any exit operator can draw from if challenged,
capped at X D-Credit per incident.

Proposal submitted to dc-governance: "Create DC-VPN-LEGAL-POOL-001;
allocate Y D-Credit from treasury to seed it; require
legal-disclosure-VC before a node can register as mesh-vpn exit-capable."

Vote: staked members review, vote passes (or doesn't).

Execution: treasury-manager seeds the pool; dc-registry's
capability-index now requires the new VC before listing a node
as exit-capable; dc-attestation logs the whole cycle.

Recursion (next cycle, months later): a new mandate asks "has the
legal pool actually reduced exit-node operator attrition, or is
adoption still low because the disclosure requirement itself is
the deterrent?" — agent researches actual `mesh-vpn` node-registry
data, proposes an adjustment or confirms the fix worked.
```

---

## 4. Updated gap registry addition

21. **DC-MESHCAR-001** — car rental vertical (Turo/Zipcar-equivalent)
22. **DC-MESHCARDELIVERY-001** — vehicle transport/logistics vertical
23. **DC-MESHBUILD-001** — licensed general-contracting vertical, sibling to Lakou Marketplace with multi-milestone escrow and municipal-inspector attestation issuance
24. **DC-AGENT-CREDENTIAL-001** — the agent-class DID credential spec (scope, mandate-binding, revocation) needed before the recursive DAO-agent loop in §3 can actually run
25. **DC-DAO-AGENT-LOOP-001** — formal spec for the research-mandate → proposal → vote → execution → outcome-review cycle described in §3, including the proposal-volume throttling rule

---

*DC-TAXONOMY-005 — extends 001–004. Adds MeshCar (rental), MeshCarDelivery (vehicle transport), and MeshBuild (licensed general contracting with multi-milestone escrow and municipal-inspector attestation). Clarifies mesh-vpn's two-layer identity split: relay operators remain DID-linked and paid for content-blind bandwidth claims, while circuit/traffic routing uses ephemeral onion-routing keys unlinkable to any DID. Specifies a recursive DAO-directed AI research/proposal loop (research mandate → agent research → proposal → human vote → execution → attested outcome → recursive review), built entirely from existing dc-governance/dc-identity/dc-attestation primitives plus one new agent-class credential, with explicit guardrails: agents propose but never execute unilaterally, mandates are scope-limited, recursion requires outcome-review as a first-class step, and proposal volume is DAO-throttled.*
