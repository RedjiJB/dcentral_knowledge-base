# DC-OPENSECURE-OS-DRONE-RECONCILED-001 — OpenSecure OS-DRONE Subsystem, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `opensecure-os-drone-subsystem` (4 docs).

## Current understanding

Four documents specifying OS-DRONE, the sixth service in the OpenSecure ecosystem (autonomous aerial
security, alongside OS-SENTINEL/OS-PATROL/OS-GUARDIAN/OS-PACS/OS-CONCIERGE): an operational
implementation guide, a logical/software-architecture topology, a network topology, and a technical
architecture overview. All four consistently describe the same platform (shared Hub event bus, shared
identity/evidence/storage infrastructure with the other five OpenSecure services), but two documents'
own internal cost tables disagree with each other and, in one case, with themselves.

**OS-DRONE Implementation Guide (incorporated):** a 6-phase field deployment playbook — regulatory
registration (Transport Canada/FAA/EASA, each with named certificate/registration requirements),
hardware procurement (per-drone, per-dock, per-ground-station BOMs specifying DJI M30T or custom
Jetson Orin NX build, SIYI MK32 C2 radio, u-blox F9P GPS), software installation (Docker Compose fleet-
ops stack, drone provisioning script, Hub Kafka-topic/API-route/dispatch-rule integration), ground
station and dock installation, a pre-flight validation checklist (infrastructure/Hub-integration/
compliance/safety), and ongoing maintenance schedules (weekly/monthly/quarterly) [Phases 1-6].

**OS-DRONE Logical Topology (incorporated):** the five-layer edge-cloud architecture (presentation/
application/data/edge/physical) shared across all OpenSecure platforms, a Mission Control Server
(Python/FastAPI/asyncio) and drone on-board agent (Jetson Orin NX, MAVLink bridge, YOLOv8 edge
inference), a drone state machine (OFFLINE→ONLINE→DOCKED→PREFLIGHT→TAKING_OFF→ENROUTE→ON_MISSION→
RETURNING→LANDING→DOCKED, plus named failsafe states), a 7-step automated dispatch pipeline (alert
ingestion → drone selection scoring → LAANC airspace check → flight-plan generation → mission upload →
launch → on-scene, targeting ~90 seconds total), the full video/AI pipeline (edge YOLOv8-small →
cloud YOLOv8-large/DeepFace/LPR reprocessing), the PostgreSQL/TimescaleDB telemetry schema, the
evidence chain-of-custody flow (explicitly "same system as OS-GUARDIAN," SHA256 hash + Hyperledger
Fabric blockchain), Kafka topic list, REST API and WebSocket references, and scalability targets
(1,000 concurrent drones validated) [§1-13].

**OS-DRONE Network Topology (incorporated):** the physical/network design — a 10.150.0.0/16 subnet
following the same allocation convention as the other five OpenSecure services, a 6-VLAN Fleet Ops
Center design (application/data/AI/management/ground-station/dock-IoT), the three-tier network (drone
→ ground station → Fleet Ops), C2 link priority (4G LTE primary, 900 MHz radio backup, geofence+RTH as
emergency fallback, <10 kbps C2 bandwidth budget per drone), video bandwidth budgeting (4 Mbps/drone
live, ~12 GB/hour/drone full-quality local record), a 4-layer zero-trust security architecture, HA/
redundancy per component, FAA Remote-ID/LAANC/UTM compliance networking, and the full Hub-integration
event matrix mirroring the Logical Topology's dispatch scenarios [§1-13, Deployment Scenarios].

**OS-DRONE Technical Architecture (incorporated):** a comprehensive technical overview restating and
consolidating most of the other three documents' content in one place — hardware options (DJI Matrice
30T commercial at ~$8,000/drone vs. a ~$3,500 custom Pixhawk 6C + Jetson Orin NX build), the on-board
software container stack, ground-station and Fleet-Ops-Center server architecture, the multi-model AI
pipeline (YOLOv8, DeepSORT, DeepFace, LPR, thermal fusion) with a geolocation ray-casting method for
converting detected-object pixel coordinates to GPS, five named autonomous mission types (scheduled
patrol, incident response, perimeter survey, asset follow, manual control) with a worked waypoint-
generation algorithm, the zero-trust security model, Hub integration matrix, and three deployment
models (SaaS/small, on-premise/enterprise, multi-site federation/government) [§1-16].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Regulatory registration, site survey, hardware/software installation phases | Implementation Guide, Phases 1-4 | incorporated |
| Pre-flight validation and test-flight protocol | Implementation Guide, Phase 5 | incorporated |
| Ongoing maintenance schedule and troubleshooting | Implementation Guide, Phase 6 / Troubleshooting | incorporated |
| Five-layer architecture, MCS/agent design, drone state machine | Logical Topology, §1-4 | incorporated |
| Dispatch pipeline, video/AI pipeline, telemetry schema | Logical Topology, §5-7 | incorporated |
| Evidence chain of custody (shared with OS-GUARDIAN) | Logical Topology, §8 | incorporated |
| Event integration, REST/WebSocket APIs, scalability targets | Logical Topology, §9-12 | incorporated |
| Subnet/VLAN design, three-tier network, C2/video bandwidth budgets | Network Topology, §2-7 | incorporated |
| Ground station and dock network architecture | Network Topology, §8-9 | incorporated |
| Zero-trust security zones and HA/redundancy | Network Topology, §10-11 | incorporated |
| Remote ID/LAANC/UTM compliance networking | Network Topology, §12 | incorporated |
| Deployment scenarios (A/B/C) and 50-drone equipment BOM | Network Topology, §14, Equipment BOM | incorporated — see tension below |
| Hardware platform options (commercial vs. custom build) | Technical Architecture, §3 | incorporated |
| On-board/ground-station/Fleet-Ops software stacks | Technical Architecture, §4-6 | incorporated (consistent with Logical Topology's component list) |
| AI/CV pipeline detail and geolocation method | Technical Architecture, §7 | incorporated |
| Mission automation types and waypoint algorithm | Technical Architecture, §8 | incorporated |
| Security architecture, Hub integration matrix | Technical Architecture, §10, §14 | incorporated (consistent with Network Topology's zero-trust design) |
| Deployment models and cost-modeling-at-scale table | Technical Architecture, §16-17 | incorporated — see tension below |

## Unresolved tensions

**The Network Topology document's own deployment-scenario cost figure contradicts its own detailed
equipment BOM for the identical scale.** Its "Scenario B: Enterprise Campus (20-50 Drones)" states a
total investment of **$250,000**, but the same document's "Equipment BOM (50-Drone Deployment)" table —
itemizing 50 drones, 20 docks, ground stations, GPU servers, Fleet Ops servers, storage, and UPS — sums
to **~$800,000**, over three times higher. No note in the document explains the difference (e.g., a
lower-tier hardware substitution or partial deployment). Attempted reconciliation: none — this reads as
an inconsistency within the source document itself rather than a resolvable scope difference.

**The Technical Architecture document's cost table for the same drone counts doesn't line up with the
Network Topology document's figures either.** Technical Architecture's "Cost Modeling at Scale" table
gives "Large: 100 drones, $800,000 upfront hardware," while Network Topology's own BOM computes
$800,000 for only 50 drones — the same total cost attached to two different drone counts across the
two documents, with no cross-reference reconciling the discrepancy. Technical Architecture's own
"Model B: On-Premise" deployment model (10-100 drones, $250,000 hardware + $50,000 server) is closer to
Network Topology's stated Scenario-B figure ($250,000) than to either document's own BOM-derived total,
suggesting the $250,000 figure and the ~$800,000 BOM total may describe different hardware tiers within
the same 20-100-drone range rather than the same configuration — but no source states this explicitly.
Left unresolved rather than picking one total as authoritative.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/security/Open-Secure/OS-DRONE-Implementation-Guide-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-DRONE-Logical-Topology-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-DRONE-Network-Topology-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-DRONE-Technical-Architecture-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/security/Open-Secure/OS-DRONE-Implementation-Guide-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-DRONE-Logical-Topology-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-DRONE-Network-Topology-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-DRONE-Technical-Architecture-md.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

**Referenced by:**
- [[DC-OPENSECURE-PER-SERVICE-IMPL-GUIDES-RECONCILED-001|DC-OPENSECURE-PER-SERVICE-IMPL-GUIDES-RECONCILED-001 — OpenSecure Per-Service Implementation Guides, Consolidated (v1, generated 2026-09-05)]]

<!-- AUTO-GENERATED RELATED END -->
