# DC-IHOSE-ARCHITECTURE-DEPLOYMENT-RECONCILED-001 — IHOSE Architecture & OpenVision Deployment, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `ihose-architecture-deployment` (9 docs).

## Current understanding

Nine documents describing two nested systems: the overall Iron Horse Security Open Source Enterprise
Modernization Framework (IHOSE), a seven-layer enterprise architecture spanning infrastructure through
client interfaces; and OpenVision, IHOSE's video-intelligence/IoT subsystem, documented across five
overlapping architecture and deployment documents of increasing depth. None of the nine documents
reference each other explicitly, so the OpenVision documents' relationship to the parent IHOSE framework
is inferred from shared technology choices (Keycloak, Ceph, Kubernetes/K3s) rather than stated
cross-references.

**IHOSE C4 Architecture Models (Parts 1 and 2, both incorporated):** the primary architecture reference,
presented as C4-style container diagrams for IHOSE's seven layers — System Context, Infrastructure &
Networking (Layer 1), Security & Identity (Layer 2, Keycloak SSO/IAM), Platform Services (Layer 3, a Kong
API Gateway + Apache Kafka event bus + NGINX ingress), Business Applications (Layer 4), Field & IoT
Operations (Layer 5), AI & Analytics (Layer 6), and Client Interface (Layer 7) [Part 1 §1-7, Part 2 §8].
Part 2 additionally covers training/personnel development, a healthcare-sector implementation profile,
and deployment patterns/DevOps practices [Part 2 §9-11]. The Platform Services layer names Kong
specifically (not presented as one of several options) as the definitive API gateway and Apache Kafka
specifically as the definitive event bus, each with a fully worked container-diagram and configuration
detail (Kong 3.x on Kubernetes with PostgreSQL-backed config; a 3-5-broker Kafka cluster with named
topics including `patrol.checkpoint`, `incident.created`, `sensor.telemetry`, `cctv.alert`).

**Iron Horse IHOSE Technical Specification v2 (incorporated):** a narrative, non-diagrammatic
restatement of the same seven-layer architecture with added commercialization framing — each layer's
section pairs its technical components with a specific "Commercialization Potential" revenue model (e.g.
Infrastructure-as-a-Service offerings for Layer 1 projecting $500K-$1.2M ARR per service line; Security-
as-a-Service offerings for Layer 2 projecting up to $1.8M ARR for managed SOC monitoring) [§1.1-1.3+].
Layer 1 adds a concrete two-datacenter topology (Ottawa HQ primary, Toronto backup, 100+ edge sites) and
zero-trust networking detail (X.509 device identity via Vault-managed internal CA, mandatory mTLS, VLAN
segmentation via pfSense/OPNsense) not present in the C4 diagrams. Notably, this document's own Platform
Services section hedges its API-gateway and event-bus choices as **"Kong / NGINX"** and **"Kafka / NATS"**
respectively, rather than naming Kong and Kafka alone as the C4 Architecture Models documents do — see
Unresolved Tensions.

**OpenVision Platform architecture and deployment documents (all four incorporated):** four documents of
increasing depth and overlapping scope describing IHOSE's video-intelligence/IoT subsystem, likely
representing successive drafts of the same underlying design rather than four independently-scoped
specs (flagged as a possible Stage 4 dedup candidate below, not resolved here). **01-OpenVision-
Architecture** is the shortest, an executive-level architecture overview naming six key differentiators
(100% open-source stack, plugin architecture, edge-to-cloud operation, digital-twin integration, a
multi-protocol IoT hub spanning MQTT/OPC UA/Modbus/BACnet/LoRaWAN/Matter, and multi-tenancy). **03-
Technical-Architecture** ("Technical Architecture Overview") elaborates the same system with a full
technology-stack table spanning orchestration (Kubernetes/K3s), video management (Frigate primary VMS,
Shinobi as an explicitly-named scale alternative, MediaMTX), AI/analytics (YOLOv8, TensorFlow, PyTorch,
CompreFace, OpenALPR), storage (PostgreSQL/TimescaleDB/PostGIS, MinIO, Ceph), messaging (NATS JetStream
as primary with Apache Kafka named as a "high-throughput option"), and an API layer naming **Apache
APISIX** (not Kong) as the API gateway. **TECHNICAL-ARCHITECTURE** ("Complete Technical Architecture") is
the most detailed of the four, covering the same ten sections (executive summary through development/
operations) with fuller component, data, security, deployment, and scalability architecture detail.
**overview-md** ("System Architecture Overview") restates the architecture at a principles level (edge-
first computing, microservices, and further sections on layered architecture, component breakdown, data
flow, scalability, and security). Across the four, actual deployment guidance (**DEPLOYMENT-GUIDE**,
already covered under "Household," "Small Business," "Enterprise," and "SaaS Multi-Tenant" deployment
tiers with fully worked shell-command sequences for each — Kubernetes/Ceph/PostgreSQL/Keycloak/NATS/
EdgeX cluster bring-up, camera-configuration templates, Prometheus/Grafana observability setup, and
troubleshooting/maintenance runbooks) and **enterprise-md** ("Enterprise Deployment Guide," a more
detailed enterprise-tier walkthrough covering hardware requirements, Terraform-driven infrastructure
provisioning, a full Rook-Ceph/PostgreSQL-operator/NATS/Redis/Mosquitto/Eclipse-Ditto/Keycloak/APISIX
service stack, K3s edge-site bring-up, cost analysis, and troubleshooting) together provide the concrete
implementation path for the architecture the other documents describe.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Seven-layer IHOSE architecture, C4 diagrams, Kong/Kafka Platform Services layer | IHOSE C4 Architecture Models (Part 1, §1-7) | incorporated |
| Training/personnel, healthcare-sector profile, deployment patterns & DevOps | IHOSE C4 Architecture Models (Part 2, §8-11) | incorporated |
| Narrative seven-layer restatement with per-layer commercialization revenue models | Iron Horse IHOSE Technical Specification v2, full document | incorporated |
| Two-datacenter topology, zero-trust networking detail, RBAC role table | Iron Horse IHOSE Technical Specification v2, §1.2-1.3 | incorporated |
| OpenVision executive architecture overview and key differentiators | 01-OpenVision-Architecture | incorporated |
| OpenVision technology-stack table (APISIX API gateway, NATS/Kafka messaging) | 03-Technical-Architecture | incorporated |
| OpenVision complete technical architecture (component/data/security/deployment/scalability) | TECHNICAL-ARCHITECTURE | incorporated |
| OpenVision architecture principles, layered architecture, component/data-flow breakdown | overview-md | incorporated |
| Household/Small-Business/Enterprise/SaaS deployment runbooks, troubleshooting, maintenance | DEPLOYMENT-GUIDE, full document | incorporated |
| Enterprise-tier infrastructure provisioning, service stack, cost analysis | enterprise-md, full document | incorporated |

## Unresolved tensions

**The parent IHOSE architecture and its own OpenVision subsystem name different, unreconciled API-gateway
and event-bus products for what is architecturally the same Platform Services layer.** The IHOSE C4
Architecture Models documents name Kong specifically (with a fully worked Kong 3.x container diagram) and
Apache Kafka specifically as the definitive choices. The Iron Horse IHOSE Technical Specification v2 — a
narrative restatement of the same seven-layer architecture — instead hedges both choices as "Kong / NGINX"
and "Kafka / NATS," never committing to one. The OpenVision subsystem's own Technical Architecture
document goes further, naming **Apache APISIX** (not Kong at all) as its API gateway, with NATS JetStream
as the primary event-streaming choice and Kafka relegated to a secondary "high-throughput option." None of
the three documents cross-references either of the other two, so there is no stated reconciliation (e.g.
"OpenVision uses APISIX because X, distinct from the platform-wide Kong instance") — a reader implementing
this architecture would need to decide which of Kong, NGINX, or APISIX is authoritative. This mirrors the
tooling-conflict pattern found in this pipeline's DION platform-architecture consolidation
([DC-DION-PLATFORM-TECHNICAL-ARCHITECTURE-RECONCILED-001](DC-DION-PLATFORM-TECHNICAL-ARCHITECTURE-RECONCILED-001.md)).

**Separately, the four OpenVision architecture/overview documents (01-OpenVision-Architecture, 03-
Technical-Architecture, TECHNICAL-ARCHITECTURE, and overview-md) describe the same system at
progressively greater depth with substantial content overlap** (all four cover the same component
categories — video management, AI/analytics, storage, security, deployment topology — using consistent
technology choices where they overlap). This looks like a series of successive drafts rather than four
distinct specifications, and may be a genuine duplicate-content candidate for Stage 4 dedup review; per
DC-CONSOLIDATOR-STD-001 §0 this Consolidator pass does not mark any of the four superseded and has
incorporated all four claim sets as stated.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/meta/platform-scaffolding/IHOSE/IHOSE-C4-Architecture-Models-Part2-md.md`
- `knowledge-base/d-central/meta/platform-scaffolding/IHOSE/IHOSE-C4-Architecture-Models-md.md`
- `knowledge-base/d-central/security/IHOSE/01-OpenVision-Architecture-docx.md`
- `knowledge-base/d-central/security/IHOSE/03-Technical-Architecture-md.md`
- `knowledge-base/d-central/security/IHOSE/DEPLOYMENT-GUIDE-md.md`
- `knowledge-base/d-central/security/IHOSE/TECHNICAL-ARCHITECTURE-md.md`
- `knowledge-base/d-central/security/IHOSE/enterprise-md.md`
- `knowledge-base/d-central/security/IHOSE/overview-md.md`
- `knowledge-base/d-central/meta/platform-scaffolding/IHOSE/Iron-Horse-IHOSE-Technical-Specification-v2-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/meta/platform-scaffolding/IHOSE/IHOSE-C4-Architecture-Models-Part2-md.md,
  knowledge-base/d-central/meta/platform-scaffolding/IHOSE/IHOSE-C4-Architecture-Models-md.md,
  knowledge-base/d-central/security/IHOSE/01-OpenVision-Architecture-docx.md,
  knowledge-base/d-central/security/IHOSE/03-Technical-Architecture-md.md,
  knowledge-base/d-central/security/IHOSE/DEPLOYMENT-GUIDE-md.md,
  knowledge-base/d-central/security/IHOSE/TECHNICAL-ARCHITECTURE-md.md,
  knowledge-base/d-central/security/IHOSE/enterprise-md.md,
  knowledge-base/d-central/security/IHOSE/overview-md.md,
  knowledge-base/d-central/meta/platform-scaffolding/IHOSE/Iron-Horse-IHOSE-Technical-Specification-v2-docx.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

**References:**
- [[DC-DION-PLATFORM-TECHNICAL-ARCHITECTURE-RECONCILED-001|DC-DION-PLATFORM-TECHNICAL-ARCHITECTURE-RECONCILED-001 — DION Platform Technical Architecture & Scaffolding, Consolidated (v1, generated 2026-09-05)]]

**Referenced by:**
- [[DC-IHOSE-OPENVISION-DOCUMENTATION-PACKAGE-RECONCILED-001|DC-IHOSE-OPENVISION-DOCUMENTATION-PACKAGE-RECONCILED-001 — IHOSE OpenVision Documentation Package, Consolidated (v1, generated 2026-09-05)]]

<!-- AUTO-GENERATED RELATED END -->
