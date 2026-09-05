# DC-IHOSE-DEPLOYMENT-INFRA-RECONCILED-001 — OpenVision (IHOSE) Deployment Infrastructure, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `ihose-deployment-infrastructure` (4 docs).

## Current understanding

Four deployment-mechanics documents covering the same OpenVision Platform stack at increasing scale:
a Docker Compose file for small deployments, raw Kubernetes manifests for enterprise deployments, a
detailed enterprise deployment runbook (500 cameras/20 sites), and a complete deployment guide spanning
all five scale tiers. All four are technically consistent — the same core services (Shinobi VMS,
MediaMTX, Frigate, YOLO, NATS JetStream, PostgreSQL/TimescaleDB, Redis, MinIO, Keycloak, Grafana/
Prometheus/Loki) recur across every scale tier with matching image names and configuration patterns.

**Docker Compose deployment (incorporated):** a single-node stack for development/small-business
(5-20 cameras), 16GB RAM minimum. Fourteen services across six functional groups — video management
(MediaMTX, Shinobi), AI/analytics (YOLO with optional NVIDIA runtime, CompreFace, MLflow), message
brokers (NATS JetStream, Mosquitto MQTT), storage (PostgreSQL/TimescaleDB, Redis, MinIO), IoT (Node-RED),
API gateway (APISIX), observability (Prometheus, Grafana, Loki), and auth (Keycloak) — all on one
bridge network with named volumes. Inline security-hardening notes call out changing all default
passwords, enabling TLS, and network segmentation before production use, and explicitly point to the
Kubernetes manifests for scale beyond 20 cameras [docker-compose.yml].

**Kubernetes manifests (incorporated):** production manifests for 50+ camera enterprise deployments —
PostgreSQL/TimescaleDB as a 3-replica StatefulSet (primary + 2 replicas), a 6-node Redis cluster (3
master + 3 replica), a 3-node NATS JetStream StatefulSet, a 4-node distributed MinIO StatefulSet
(5TB/node, 20TB total), MediaMTX and Shinobi as separate Deployments, a GPU-node-scheduled YOLO
detector Deployment with a HorizontalPodAutoscaler (2-20 replicas, scaling on 70% CPU/80% memory), and
a default-deny NetworkPolicy with an explicit allow-rule for database access [Kubernetes manifests].

**Enterprise Deployment Guide (incorporated):** the most detailed operational runbook, targeting the
same 500-camera/20-site scale as the sibling [DC-IHOSE-CITY-FLEET / consolidations reference the
implementation roadmap directly] — central cloud (5+ K8s nodes, 6-node/1.2PB Ceph cluster, 3-node
PostgreSQL HA) plus 20 edge sites (2x K3s nodes each, 25 cameras/site, 14-day local retention), totaling
500 cameras / 40 edge compute nodes / 17 central servers / ~1PB usable storage, deployed over a 14-week
(3.5-month) timeline across 6 phases [Deployment Overview]. Concrete hardware BOMs for both central
(control-plane/worker/storage/PostgreSQL node specs, switch counts) and edge (compute node, NAS,
PoE switch, router) tiers [Prerequisites]. Step-by-step commands for kubeadm or RKE2 cluster bring-up,
Rook-Ceph block+object storage, CloudNativePG PostgreSQL HA with TimescaleDB/PostGIS extensions, and
Ansible-driven edge-site rollout across all 20 sites, plus WireGuard site-to-central VPN, Falco runtime
security, and Ceph/PostgreSQL backup procedures [Central Cloud Setup through Disaster Recovery].

**Complete Deployment Guide (incorporated):** a five-tier scenario overview (Development 1-5 cameras,
Small Business 5-25, Edge 10-50/site, Enterprise 100+, SaaS multi-tenant) matching the scale
progression the other three documents implement in detail [Deployment Scenarios]. Adds two elements
the other three don't cover: an Edge/K3s scenario using EdgeX Foundry plus Tailscale for edge-to-central
VPN (distinct from the Enterprise guide's WireGuard choice — both are presented as options for
different scale tiers, not a conflict), and a full SaaS multi-tenant provisioning model — per-tenant
Kubernetes namespace, PostgreSQL schema, MinIO bucket, and Keycloak realm, automated via a tenant-
creation API, with three subscription tiers (Home $29/mo 1-4 cameras, Professional $199/mo 5-25,
Enterprise custom 25+) [SaaS Multi-Tenant Deployment]. Closes with monitoring/alerting rules
(Prometheus AlertManager), a four-part backup strategy, and quarterly DR-drill guidance consistent with
the Enterprise Deployment Guide's disaster-recovery section [Operations & Maintenance].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Single-node Docker Compose service stack and hardening notes | docker-compose.yml | incorporated |
| Production Kubernetes StatefulSets/Deployments/autoscaling/network policy | 05-kubernetes-manifests.yml | incorporated (service images/configs consistent with docker-compose.yml) |
| 500-camera/20-site architecture, hardware BOM, phased rollout, VPN/security/backup procedures | 04-Enterprise-Deployment.md | incorporated |
| Five-tier scenario overview and quick-start steps | 06-Complete-Deployment-Guide.docx, Deployment Scenarios / Quick Start | incorporated (scenario boundaries match the scale progression across the other 3 docs) |
| Edge/K3s + EdgeX Foundry deployment with Tailscale VPN | 06-Complete-Deployment-Guide.docx, Edge Deployment with K3s | incorporated (a second, non-conflicting edge-VPN option alongside the Enterprise guide's WireGuard choice) |
| SaaS multi-tenant provisioning model and subscription tiers | 06-Complete-Deployment-Guide.docx, SaaS Multi-Tenant Deployment | incorporated |
| Monitoring, backup, and DR operations | 06-Complete-Deployment-Guide.docx, Operations & Maintenance | incorporated (consistent with 04-Enterprise-Deployment.md's own DR section) |

## Unresolved tensions

None identified in this pass — all four documents describe complementary deployment tiers of the same
platform using the same core service set and consistent configuration values (image names, ports,
resource patterns). The two edge-VPN choices (WireGuard in the Enterprise guide, Tailscale in the
Complete Deployment Guide) are presented as alternative options for different guides rather than a
stated single mandatory choice, so this is not treated as a conflict.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/security/IHOSE/04-Enterprise-Deployment-md.md`
- `knowledge-base/d-central/security/IHOSE/04-docker-compose-yml.md`
- `knowledge-base/d-central/security/IHOSE/05-kubernetes-manifests-yml.md`
- `knowledge-base/d-central/security/IHOSE/06-Complete-Deployment-Guide-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/security/IHOSE/04-Enterprise-Deployment-md.md,
  knowledge-base/d-central/security/IHOSE/04-docker-compose-yml.md,
  knowledge-base/d-central/security/IHOSE/05-kubernetes-manifests-yml.md,
  knowledge-base/d-central/security/IHOSE/06-Complete-Deployment-Guide-docx.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
