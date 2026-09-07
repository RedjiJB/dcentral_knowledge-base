# DC-AGENT-OBSERVABILITY-001: Real-Time Multi-Tier Agent Monitoring
### Extends DC-TAXONOMY-001–006 and DC-DAO-AGENT-LOOP-001. Resolves the observability-stack gap flagged in that document's closing note.

---

## 0. What changes from a conventional design

Earlier work in this reference set designed an observability stack assuming a centralized cloud trace backend, with sampling driven by per-GB billing cost. Neither assumption holds here: there is no central operator, and the actual constraint on a residential SHI node isn't a cloud bill — it's bandwidth and local resource burden, the same constraint already named for `mesh-vpn` relay traffic (003 §4.3.2). This document redesigns the stack around that reality, reusing the mesh's own existing patterns (local-first storage, event-sourced sync, federated aggregation) instead of importing a SaaS-shaped architecture wholesale.

---

## 1. Instrumentation

Unchanged in principle: agents emit OpenTelemetry-formatted spans for every tool call, decision, and call into any `dcentral-core` service. OTel is an open standard — no conflict with an open-source infrastructure mandate, and no reason to replace it.

---

## 2. Collection — local, not centralized

Each node hosting agent workloads (an SHI node, a coop's gateway node, an ecosystem-tier compute cluster) runs its **own** local OTel Collector. Spans are not streamed to one central backend. Sampling still happens at this layer, but the reasoning changes: it's not cost-driven, it's **bandwidth/relay-burden-driven** — the same discipline already established for `mesh-vpn` traffic applies here (running telemetry-relay for a busy agent fleet is a real resource cost on a modest home connection, not a free toggle).

---

## 3. Storage tiering — maps directly onto DC-MESHSTORAGE-ARCHIVE-001

| Data | Tier |
|---|---|
| Raw/sampled operational spans (tool calls, intermediate reasoning) | Standard tier — short retention, erasure-coded, not archived |
| Outcome-review verdicts, final proposal decisions, reputation attestations | Archive tier — permanent, Merkle-anchored |

This is the one part of the observability stack that genuinely needs permanence; the rest doesn't, and treating raw operational telemetry as archive-tier data would misuse a mechanism built for governance-grade records.

---

## 4. Indexing / query layer

Content-addressed storage isn't natively queryable at dashboard speed. Each node or coop runs a local, open-source indexing service that mirrors relevant span data out of local storage into a fast-query index — this index is a **derived, rebuildable cache**; the mesh-storage copy remains the source of truth, consistent with the event-sourced-sync pattern already used throughout this architecture (local DB + event log, per 001 §4.2). If the index is lost or corrupted, it's rebuilt from the durable copy, not restored from a backup.

---

## 5. Live views — federated, not global

Don't build one global topology view for "thousands of agents across many DAOs." Each coop-tier or ecosystem-tier governance instance gets its **own** local topology/waterfall view over its own scoped agent activity — this is a direct application of the three-tier structure already specified (006 §1). Cross-tier rollup uses the same discipline as the federated learning pattern (006 §3): only **aggregated summary statistics** (agent counts, proposal throughput, error rates) roll up to an ecosystem-wide view — never raw per-span data. Same privacy and bandwidth discipline as everything else in this architecture, applied to observability instead of research data.

---

## 6. Alerting

Evaluated locally, where the raw data already lives — same locality principle as §2. An alert that needs to be provably real and visible beyond the local node (e.g., "this agent exceeded its budget by 3x") is published as a lightweight attestation, discoverable through the registry service, rather than a proprietary alerting-platform webhook. This makes an alert auditable the same way a proposal outcome already is, instead of introducing a parallel notification system with no record.

---

## 7. Cost tracking — already native

This is the one place the decentralized pass genuinely simplifies the earlier design rather than complicating it. Every inference call already settles through the existing payment ledger's micropayment channel. "Cost per agent" is a direct query against that ledger for a given agent's DID — already attested, already auditable. No bespoke cost-computation layer is needed; the earlier design's cost-tracking component turns out to already exist inside the payment service.

---

## 8. Public / governance dashboard

Same pattern as DC-DAO-AGENT-LOOP-001 §5: rendered through the shared wiki space, drawing on the attestation service's public record for the permanent portion and the local index (§4) for live operational data, scoped per governance body per the three-tier structure. No separate "public audit portal" service — it's a view over data that already exists in the right places.

---

## 9. OSS reference

| Component | OSS reference #1 | OSS reference #2 |
|---|---|---|
| Instrumentation | **OpenTelemetry** | — |
| Local collector | **OpenTelemetry Collector** | — |
| Local index/query | **Arize Phoenix** (self-hosted) | **DuckDB** or **ClickHouse** |
| Topology/waterfall view | **LangWatch** | **Grafana** (metrics/cost panels) |

---

## 10. Gap registry status

**#33 `DC-AGENT-OBSERVABILITY-001` — specified, this document.**

---

*DC-AGENT-OBSERVABILITY-001 — extends 001–006 and DC-DAO-AGENT-LOOP-001. Redesigns the real-time monitoring stack for decentralized, content-addressed infrastructure: local-first OTel collection with bandwidth-driven (not cost-driven) sampling, storage tiering that reserves the permanent archive for governance-grade records only, a locally-indexed live-query layer that stays a rebuildable cache over the durable store, federated per-tier topology views with only aggregated statistics rolling up across tiers, attestation-based alerting, and cost tracking that turns out to require no new component at all — it's already native to the existing payment ledger.*


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

*No cross-references detected to/from other docs/*.md files.*

<!-- AUTO-GENERATED RELATED END -->
