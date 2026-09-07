# DC-MESHSTORAGE-ARCHIVE-001: Permanent-Archive Tier of mesh-storage
### Extends DC-TAXONOMY-001–006 and DC-DAO-AGENT-LOOP-001. Resolves the open decision point flagged in DC-TAXONOMY-002 §4 and fulfills the new gap item raised in DC-DAO-AGENT-LOOP-001 §7.

---

## 0. The gap this closes

DC-TAXONOMY-002 §4 flagged it directly: `mesh-storage` as specified is Storj-style — repairable, erasure-coded, built for *durability under churn*, not permanence. Arweave's pay-once-store-forever model isn't covered, and the gap registry entry left it as an open decision rather than a spec. DC-DAO-AGENT-LOOP-001 needs exactly this for one specific workload — the attestation trail of agent proposals, votes, executions, and outcome-reviews — so this document resolves the open point using that workload as the concrete driver, rather than leaving it abstract.

**Scoping decision:** this is a **tier of `mesh-storage`**, not a ninth mesh module. Same pattern already used for `mesh-vpn` as a mode of `mesh-connectivity` (003 §4.4) — reuse the existing module's accounting/reward machinery, change the retention/replication behavior for one specific class of data.

**Sovereignty resolution (supersedes the "flagged, not resolved" item in DC-EXPERT-DAO-001 §6, §7):** `mesh-storage`'s own OSS reference entry already establishes the pattern this needed all along — Storj is tagged as *"already the fork base"* (003 §2.2), meaning `mesh-storage` runs as D-Central's own independent network built on Storj's open-source implementation, not a connection to the live public Storj network. The same logic resolves the archive tier cleanly: IPFS/Filecoin's content-addressing design and Arweave's endowment-funded permanence model are **patterns to fork and run on D-Central's own node infrastructure**, exactly like Storj — not external networks the ecosystem becomes a client of. This was never actually an open trade-off between sovereignty and permanence; it's the same fork discipline already applied everywhere else in this taxonomy, just not yet stated explicitly for this tier.

---

## 1. What goes in the archive tier vs. the standard tier

Not everything `mesh-storage` holds needs permanence, and forcing everything into permanent storage would be wasteful even under a "storage isn't the constraint" posture — permanence is a property that should be *chosen* for data where it matters, not applied by default.

| Data class | Tier | Why |
|---|---|---|
| Agent proposal drafts, working state, session context | Standard (erasure-coded, Storj-style) | Ephemeral by nature — superseded the moment the proposal is finalized |
| Per-role instruction templates, versioned specs | Standard, version-controlled | Get revised over time; version history matters, permanent immutability of every draft doesn't |
| **Final submitted proposals** | Archive | Once submitted to `voting-engine`, this becomes part of the permanent governance record |
| **Vote outcomes** | Archive | The DAO's decision itself is the thing accountability depends on |
| **Execution attestations** | Archive | What actually happened as a result of a vote |
| **Outcome-review findings** | Archive | The record that makes recursion (005 §3.1 step 6) meaningful — without a permanent prior record, "did this work" can't be checked later |
| **Reputation attestations** | Archive | Per DC-AGENT-CREDENTIAL-001 §4 — a track record that can be quietly pruned isn't a track record |
| Raw operational telemetry (agent tool-call traces, etc.) | Standard, short retention | See DC-AGENT-OBSERVABILITY-001 — operational data, not governance record |

The dividing line: **if it's the kind of thing `dc-attestation` would wrap in an envelope, it belongs in the archive tier. If it's working state that gets superseded, it doesn't.**

---

## 2. Mechanics

1. **Batching.** Archive-tier writes are not committed individually — they're batched over a fixed window (e.g., hourly, or every N attestations, whichever comes first) into a Merkle tree.
2. **Root anchoring.** The Merkle root of each batch is committed into a `dc-attestation` envelope, so the anchoring event itself is a first-class attested record, not a side channel.
3. **Internal witness quorum.** The root is additionally co-signed by an N-of-M set of node operators drawn from unaffiliated coops (per DC-EXPERT-DAO-001 §6) — not an external transparency log. "Independent" means no single internal party controls the witness set, achieved by drawing witnesses from enough different coops that no one operator or coalition plausibly controls a majority, rather than by stepping outside D-Central's own infrastructure. This is what protects against a scenario internal to the ecosystem's own infrastructure: if the same operators controlling `dc-attestation`'s signing keys also controlled the only copy of the anchor, they could in principle rewrite history undetected. A quorum drawn from unaffiliated coops closes that hole without leaving the ecosystem.
4. **Content storage.** The actual payloads (full proposal text, full outcome-review findings) are stored using content-addressing techniques forked from IPFS/Filecoin's open-source implementations — already `mesh-storage`'s tagged OSS reference (003 §2.2) — running on D-Central's own node infrastructure and pinned for permanence, rather than the live public IPFS/Filecoin networks and rather than subject to standard erasure-coded churn/repair economics.
5. **Verification.** Anyone holding a content hash can independently verify it against the publicly anchored Merkle root without needing to trust `dcentral-core`'s own infrastructure — the same "verify, don't trust" property the rest of this architecture already applies to attestations generally, now applied to the storage layer specifically.

```
Attestation events (proposal, vote, execution, outcome-review, reputation)
        │
        ▼
   Batch into Merkle tree (fixed window)
        │
        ├──→ Root committed into dc-attestation envelope
        │
        └──→ Root co-signed by internal witness quorum (unaffiliated coops)
        │
        ▼
   Full payloads pinned to forked IPFS/Filecoin-style content-addressed storage
        (mesh-storage archive tier, D-Central's own nodes)
```

---

## 3. Redaction and selective disclosure within the archive tier

Permanent storage and the selective-disclosure discipline that governs everything else in this architecture (006 §2's privacy boundary) have to coexist here, not trade off against each other. A proposal or attestation that references anything short of fully public data follows the same rule as any other record: sensitive fields are committed (hashed) rather than stored raw in the publicly-anchored payload, with the underlying value accessible only through the normal `selective-disclosure-engine` grant — not through a general public read of the archive. What's permanently public by default is the *fact and integrity* of the record (that a proposal existed, that a vote happened, that an outcome-review concluded X), not necessarily every field inside it, exactly as it would be for any other attested claim in this taxonomy.

---

## 4. Queryable graph layer

DC-DAO-AGENT-LOOP-001 §3 flagged this as wanted but unspecified: content-addressed storage answers *"give me this specific record"* but not *"show me everything connected to this record"* — and 006 §2 already establishes that reading the full attested history of prior proposals, executions, and outcome-reviews is what makes recursive outcome-review possible at all. Walking that history one content-hash lookup at a time doesn't scale once a domain has hundreds of prior attestations.

**Pattern:** the same "local index mirrors durable storage, rebuildable, never the source of truth" discipline already specified for observability (DC-AGENT-OBSERVABILITY-001 §4) — applied here to relationships instead of spans. Each coop or the ecosystem tier runs a local, self-hosted graph/document index (a CRDT-based peer-to-peer database pattern, forked and run on D-Central's own infrastructure — same fork discipline as §0, not a connection to any public network) that indexes the edges between archive-tier records: mandate → agent → proposal → vote → execution → outcome-review → reputation attestation chains; expert credential → sign-off attestation chains; rollout registry → cohort → guardrail-attestation chains (DC-VERIFIABLE-ROLLOUT-001).

**Why it's safely rebuildable:** every archive-tier record already references the records it depends on by content hash — that's what makes it an attestation *chain* rather than a flat list. The graph index doesn't hold information that doesn't already exist in the archive tier; it just makes those implicit hash-references traversable at query speed instead of requiring a full re-walk for every lookup. If an index is lost or corrupted, it's rebuilt by re-walking the archive tier's hash references, not restored from a backup.

**Semantic retrieval is a separate concern from graph traversal**, worth naming explicitly rather than folding in: "what's connected to X" (graph) and "what's similar to X" (semantic search over content) solve different problems and want different indexes — see the brainstormed additions in DC-KNOWLEDGE-LAYERS-001 for the latter.

---

## 5. Reward/economics

Node operators hosting archive-tier content earn D-Credit for pinning/serving it, same reward-tier pattern as standard `mesh-storage` hosting — the difference is the payout structure reflects permanence rather than the ongoing repair-and-serve economics of the standard erasure-coded tier.

**Concrete mechanism, forked from Arweave's economic design rather than its network:** an **endowment model** — at the moment content enters the archive tier, a one-time D-Credit payment is calculated to cover its storage cost declining over time (as node storage capacity gets cheaper), and that endowment is paid out gradually to whichever node operators are actively pinning/serving the content, rather than requiring an ongoing subscription payment from whoever originated the record. This is what makes "permanent" actually mean something economically — the record doesn't go dark if its original committer stops paying, because the endowment already funds its hosting indefinitely, distributed entirely in D-Credit through D-Central's own treasury/reward mechanisms rather than any external token or network.

This needs its own line in the SHI financial model, the same way `mesh-vpn`'s relay-throughput reward needed one (003 §4.3.2) — the mechanism above is the shape it should take; the exact endowment-sizing formula (how storage-cost decline is modeled, what discount rate applies) is a follow-on calculation for whoever builds the financial model, not specified here.

**Related work:** DC-COMPUTE-SILICON-ARCH-001 §6.1 adapts this same endowment shape to compute-serving (mesh-compute/mesh-ai node operators, as distinct from mesh-storage's I/O-bound operators) — sized against projected serving volume rather than a fixed one-time payload, since compute has no direct equivalent of "content" to endow against.

---

## 6. OSS reference

| Component | Forked pattern #1 | Forked pattern #2 |
|---|---|---|
| Content-addressed permanent storage | **IPFS / Filecoin** content-addressing design (already `mesh-storage`'s tagged reference, 003 §2.2) — run on D-Central's own nodes, not the public networks | **Arweave** economic/endowment model (§5) — adapted into D-Credit, not connected to the Arweave network |
| Witness quorum for anchoring | (no single canonical OSS project — an N-of-M multi-signature pattern over unaffiliated coop node operators, per DC-EXPERT-DAO-001 §6) | — |
| Queryable graph layer | **OrbitDB**-style CRDT peer-to-peer database pattern (§4) — forked, run internally | — |
| Merkle-tree batching | (standard cryptographic primitive, no single canonical OSS project to tag — most attestation-anchoring implementations roll their own over a standard hash library) | — |

---

## 7. Gap registry status

**#32 `DC-MESHSTORAGE-ARCHIVE-001` — specified, this document. Resolves the open decision point in DC-TAXONOMY-002 §4, and resolves the sovereignty flag raised in DC-EXPERT-DAO-001 §6/§7 by establishing that the archive tier follows the same fork-not-connect discipline already used for mesh-storage's Storj base.**

---

*DC-MESHSTORAGE-ARCHIVE-001 — extends 001–006 and DC-DAO-AGENT-LOOP-001. Specifies mesh-storage's permanent-archive tier as a mode of the existing module (not a ninth), scoped to the class of data dc-attestation would envelope. Resolves the sovereignty question definitively: every technique used (content-addressing, endowment economics, witness-quorum anchoring) is forked and run on D-Central's own infrastructure, consistent with how Storj is already treated as mesh-storage's fork base — none of it depends on the live Arweave, IPFS, Filecoin, or any external transparency-log network. Also specifies the queryable graph layer DC-DAO-AGENT-LOOP-001 §3 left open, as a rebuildable local index over the archive tier's existing hash-reference chains, and reconciles permanence with the architecture's selective-disclosure discipline: what's permanently public is the fact and integrity of a record, not automatically every field within it.*


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

**Referenced by:**
- [[DC-COMPUTE-SILICON-ARCH-001|DC-COMPUTE-SILICON-ARCH-001 — Compute Silicon Class Architecture (v1, generated 2026-09-07)]]

<!-- AUTO-GENERATED RELATED END -->
