# DC-HCCC-GRAPHRAG-RECONCILED-001 — HCCC GraphRAG/GraphQL System, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `haiti-graphrag-graphql-system` (2 docs).

## Current understanding

Two documents for the Haitian Cooperative Coordination Center (HCCC)'s GraphRAG/GraphQL system: the
"Comprehensive...Design Document" is the complete 15-section architecture spec; the "Complete...
Implementation Guide" is a step-by-step, code-heavy build walkthrough that is consistent with the
design document everywhere it overlaps, but is itself incomplete — its own table of contents promises
15 sections, and its actual content cuts off mid-code-block partway through section 9 of 15.

**System design (incorporated, from the Design Document):** the system coordinates 7 sectors (Personnel/
credentialing, Mesh Networking, SOPs, Security, Healthcare, Education, Agriculture & Finance) through a
unified Apollo Federation Gateway sitting in front of per-sector GraphQL APIs, backed by a Neo4j-based
"GraphRAG Knowledge Engine" doing entity extraction, multi-hop reasoning, and trust scoring, all gated
by a stated "Trust Fabric & Data Sovereignty" layer (community data vaults, democratic governance,
consent management, audit logs) [§2-3]. Core principles are stated explicitly: community sovereignty,
community-owned data with granular permissions, cultural preservation, transparency, resilience during
infrastructure failure, and interoperability [§2.2]. The technology stack names specific versions
throughout: Apollo Federation 2.x, Neo4j 5.x, Python 3.11+ with PyTorch/spaCy/Transformers for the
GraphRAG engine, Node.js 20.x/TypeScript 5.x/Express/Prisma/PostgreSQL 15.x for backend services, Redis
7.x + Kafka for real-time/messaging, Kubernetes 1.28+/Istio for orchestration, IPFS/Filecoin/MinIO for
distributed storage, Hyperledger Fabric + W3C DID for identity/governance, and a Raspberry Pi 4B (8GB)
+ K3s + LoRaWAN edge computing stack [§4].

**Implementation walkthrough (incorporated, from the Implementation Guide, as far as it goes):**
concrete hardware/software prerequisites (dev machine: 8+ cores, 32GB+ RAM, 8GB+ VRAM GPU; production:
a 6-20 node Kubernetes cluster with 2-4 GPU nodes, 50+ edge Raspberry Pi units with solar/battery power)
[§1] — see DC-COMPUTE-SILICON-ARCH-001 §2.2 for this GPU fleet as a candidate the discovery pipeline should watch; a full development-environment setup script (Node 20 via nvm, Python 3.11, Docker, kubectl, Helm,
Terraform) [§2]; and detailed build-out through project structure, core infrastructure, database layer,
the GraphQL federation gateway, the GraphRAG intelligence engine, microservices, and federated
social-media integration (Mastodon/Lemmy/Nextcloud/BigBlueButton) [§3-9]. Every named technology
version in this walkthrough (Node 20.x, Python 3.11+, Neo4j, PostgreSQL, Redis, Raspberry Pi 4B 8GB)
matches the Design Document's technology stack exactly — a consistency check across both documents
rather than a conflict.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| 7-sector system scope and core principles | Design Doc §2 | incorporated |
| High-level architecture and component-interaction flow | Design Doc §3 | incorporated |
| Full technology stack (all layers) | Design Doc §4 | incorporated (independently confirmed by the Implementation Guide's matching version numbers) |
| Core components, GraphQL federation layer, GraphRAG engine detail | Design Doc §5-7 | incorporated |
| System integrations, data architecture, security/privacy, deployment, performance, dev guidelines, testing, monitoring | Design Doc §8-15 | incorporated |
| Hardware/software prerequisites and dev-environment setup | Implementation Guide §1-2 | incorporated |
| Project structure, infrastructure, database, GraphQL gateway, GraphRAG engine, microservices, federated social build-out | Implementation Guide §3-9 | incorporated — document itself ends mid-section-9, see note below |

## Unresolved tensions

None identified as a conflict between the two documents — every overlapping technical detail (Node.js
20.x, Python 3.11+, Neo4j, PostgreSQL 15.x, Redis 7.x, Raspberry Pi 4B 8GB edge hardware) matches exactly
between them. One incompleteness is worth flagging, though it is a gap in a single source rather than a
disagreement between sources: the Implementation Guide's own table of contents lists 15 sections
(through "Operations & Maintenance"), but its actual content stops mid-code-block partway through
section 9 of 15 ("Federated Social Media Integration") — sections 10-15 (Edge Computing & Mesh Network,
Community Data Sovereignty Layer, Testing & QA, Deployment & Infrastructure, Post-Deployment
Configuration, Operations & Maintenance) are titled in the TOC but not actually written in this
document. The Design Document does cover the equivalent later-stage topics (deployment architecture,
performance requirements, testing strategy, monitoring) in its own §11-15, so the gap is in the
hands-on implementation walkthrough specifically, not in the overall documentation set.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/haiti-diaspora/Haiti-open-framework/Complete-HCCC-GraphRAG-GraphQL-System-Implementation-Guide-md.md`
- `knowledge-base/d-central/haiti-diaspora/Haiti-open-framework/Comprehensive-GraphRAG-GraphQL-System-Design-Document-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/haiti-diaspora/Haiti-open-framework/Complete-HCCC-GraphRAG-GraphQL-System-Implementation-Guide-md.md,
  knowledge-base/d-central/haiti-diaspora/Haiti-open-framework/Comprehensive-GraphRAG-GraphQL-System-Design-Document-md.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

Neither source doc is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

**Referenced by:**
- [[DC-COMPUTE-SILICON-ARCH-001|DC-COMPUTE-SILICON-ARCH-001 — Compute Silicon Class Architecture (v1, generated 2026-09-07)]]

<!-- AUTO-GENERATED RELATED END -->
