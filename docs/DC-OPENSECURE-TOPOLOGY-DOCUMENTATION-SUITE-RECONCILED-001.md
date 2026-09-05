# DC-OPENSECURE-TOPOLOGY-DOCUMENTATION-SUITE-RECONCILED-001 — OpenSecure Topology Documentation Suite, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `opensecure-topology-documentation-suite` (16 docs).

## Current understanding

Sixteen production-ready network/logical/technical-architecture specifications for four OpenSecure
platform services (OS-DRONE, OS-GUARDIAN, OS-PATROL, OS-SENTINEL) and the central OpenSecure Hub, plus a
suite-level index document (TOPOLOGY-SUITE-SUMMARY). The index document itself contains a significant
discrepancy against this topic's actual membership — see Unresolved Tensions — which is the most
consequential finding in this consolidation.

**OS-DRONE (Logical Topology and Technical Architecture, both incorporated):** an Autonomous Aerial
Security Platform specification. The Logical Topology document covers a five-layer architecture, core
components, a drone state machine, mission planning/dispatch flow, video pipeline/AI analytics, a
telemetry data model, evidence chain-of-custody, event-driven integration, a REST API reference, WebSocket
real-time streams, scalability design, and technology stack. The Technical Architecture document covers
drone hardware architecture, the on-board software stack, ground-station architecture, a fleet-ops-center
architecture, the AI/computer-vision pipeline, a mission-automation engine, evidence/chain-of-custody
(restated at the hardware/deployment level rather than the data-model level), security architecture,
network architecture, and scalability/high-availability sections. Notably, OS-DRONE has no companion
Network Topology document in this topic's membership, unlike OS-GUARDIAN, OS-PATROL, and OS-SENTINEL,
each of which has one (see Unresolved Tensions).

**OS-GUARDIAN (Logical Topology, Network Topology, and Technical Architecture, all incorporated):** a
security-personnel and body-camera platform. Its Network Topology describes a wireless body-camera-
docking architecture (WiFi 6 primary, 4G LTE emergency-only upload, ~10GB per 4-hour shift), an air-gapped
body-camera VLAN separate from a restricted evidence-storage VLAN and a read-only analytics VLAN, MinIO
evidence storage with AES-256-at-rest/TLS-1.3-in-transit encryption and cryptographic chain-of-custody
signatures, and a real-time command-center network with live GPS tracking and panic-button integration.
Its Logical Topology describes an evidence lifecycle (record → buffer → upload → store → review →
archive/delete), a five-state body-camera state machine with a 30-second pre-event rolling buffer and
automatic triggers (weapon drawn, vehicle pursuit, officer down), immutable SHA-256 chain-of-custody
tracking with court-ready export formatting, YOLOv8-based weapon-detection integration, officer-safety
features (man-down detection, geo-fencing), a 30+-endpoint evidence-management API, and an automated PII
redaction workflow. The Technical Architecture document restates and deepens this same hardware/software
design at implementation depth.

**OS-PATROL (Logical Topology and Network Topology, both incorporated; no Technical Architecture document
in this topic):** a mobile patrol and fleet-management platform treating vehicles as autonomous mobile
nodes. Its Network Topology specifies a hybrid edge-cloud architecture with dual-SIM cellular failover
(Verizon primary, AT&T backup with 30-second failover, WiFi opportunistic tertiary), a per-vehicle internal
network (Raspberry Pi 4 controller, GPS, 4G modem, 4-6 dashcams, LPR camera, OBD-II, tablet) addressed via
WireGuard VPN, an intelligent upload-prioritization scheme (critical hot-list LPR hits transmit
immediately over 4G; bulk video waits for overnight WiFi), and a four-VLAN Fleet Operations Center. Its
Logical Topology specifies a five-layer edge-intelligence-plus-cloud-processing architecture, 5-second GPS
position updates with intelligent batching over a PostGIS spatial data model, an OpenALPR edge LPR
pipeline achieving under 7 seconds total latency from plate scan to officer notification, a 10,000-plate
local hot-list cache with O(1) lookup, a 72-hour local video ring buffer with event tagging, LibreDispatch
CAD integration with nearest-unit dispatch, a 6-state vehicle state machine, and multi-object tracking via
IoU-plus-appearance matching.

**OS-SENTINEL (Logical Topology, Network Topology, and Technical Architecture, all incorporated):** an
AI-powered surveillance platform. Its Network Topology specifies a hierarchical PoE camera network (24-port
edge switches, 48-port 10G-uplink core switch), GPU-accelerated NVR infrastructure (an NVIDIA RTX 4090
processing 20 cameras at 10fps analytics), a MinIO erasure-coded (4+2) storage cluster, three camera
tiers (indoor/outdoor/PTZ), configurable 30-90-day retention, and a documented $150K equipment BOM for a
100-camera deployment. Its Logical Topology specifies a five-layer AI architecture with a real-time video
pipeline (RTSP ingestion, every-3rd-frame extraction at 10fps, a four-model inference stack — YOLOv8,
DeepFace, ResNet, a custom CNN — totaling ~70ms per frame), multi-object tracking with loitering/running/
abnormal-behavior detection, a natural-language-query interface (GPT-4 plus CLIP embeddings resolving a
query like "show me when someone entered the parking lot this morning" in 3-5 seconds), a 512-dimension
DeepFace face-recognition gallery supporting 1,000+ enrolled faces, a conditional alert-rule engine with
spam-prevention cooldowns, a 60+-endpoint REST API, and linear scalability at one GPU worker per 20
cameras up to 1,000+ cameras. The Technical Architecture document restates this design at implementation
depth.

**OpenSecure Digital Twin Integration (incorporated):** a cross-cutting framework giving every camera,
door, vehicle, visitor, and officer in the OpenSecure ecosystem a real-time-updating virtual counterpart,
built on a visualization engine (Unity 3D for real-time rendering/VR-AR, Cesium for geospatial 3D outdoor
environments), enabling predictive analytics, pre-deployment scenario simulation, multi-perspective
historical incident replay, and AI-driven optimization of patrol routes, camera placement, and staffing —
explicitly framed as elevating OpenSecure from "operational tool" to "strategic security intelligence
platform."

**OpenSecure Hub (Implementation Guide, Logical Topology, and Network Topology, all incorporated):** the
central management platform tying the four service platforms together. The Implementation Guide specifies
a five-phase deployment procedure (infrastructure setup, core-services deployment, service integration,
testing/validation, go-live) plus post-deployment and troubleshooting guidance. The Logical Topology
specifies the Hub's own logical architecture, identity/access management, and a unified API gateway
federating the four service platforms' individual APIs. The Network Topology specifies the Hub's global
network architecture philosophy and infrastructure design connecting to each service platform's own
network topology.

**TOPOLOGY-SUITE-SUMMARY (incorporated as a claim, its accuracy assessed separately below):** a
documentation index claiming ten documents, 385KB, and "COMPLETE - All 10 Documents Generated" status,
covering Network Topology and Logical Topology pairs for five named services: **OS-PACS**, OS-PATROL,
**OS-CONCIERGE**, OS-GUARDIAN, and OS-SENTINEL — with detailed content summaries for each (e.g. OS-PACS's
three-tier/four-VLAN architecture and $230-$41,500 deployment-scenario pricing; OS-CONCIERGE's hub-and-
spoke multi-property architecture and BACnet/IP smart-building integration), a cross-service architecture-
pattern analysis (edge-cloud hybrid, VLAN segmentation, tiered storage, API-first design, event-driven
messaging), small/mid-market/enterprise deployment cost tables, and a consolidated technology-stack
summary.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| OS-DRONE logical architecture, state machine, evidence chain, API | OS-DRONE Logical Topology, full document | incorporated |
| OS-DRONE hardware, on-board software, fleet-ops, AI/CV pipeline | OS-DRONE Technical Architecture, full document | incorporated |
| OS-GUARDIAN network architecture, VLAN segmentation, evidence storage encryption | OS-GUARDIAN Network Topology, full document | incorporated |
| OS-GUARDIAN evidence lifecycle, state machine, weapon detection, redaction | OS-GUARDIAN Logical Topology, full document | incorporated |
| OS-GUARDIAN implementation-depth hardware/software architecture | OS-GUARDIAN Technical Architecture, full document | incorporated |
| OS-PATROL cellular/vehicle-network architecture, upload prioritization | OS-PATROL Network Topology, full document | incorporated |
| OS-PATROL GPS/LPR pipeline, hot-list cache, dispatch, vehicle state machine | OS-PATROL Logical Topology, full document | incorporated |
| OS-SENTINEL camera/NVR network architecture, storage, BOM | OS-SENTINEL Network Topology, full document | incorporated |
| OS-SENTINEL AI video pipeline, NLQ, face recognition, alert engine | OS-SENTINEL Logical Topology, full document | incorporated |
| OS-SENTINEL implementation-depth architecture | OS-SENTINEL Technical Architecture, full document | incorporated |
| Cross-platform digital-twin visualization, predictive analytics, simulation | OpenSecure Digital Twin Integration, full document | incorporated |
| Hub 5-phase deployment procedure | OpenSecure Hub Implementation Guide, full document | incorporated |
| Hub logical architecture, IAM, unified API gateway | OpenSecure Hub Logical Topology, full document | incorporated |
| Hub global network architecture and infrastructure | OpenSecure Hub Network Topology, full document | incorporated |
| Index claiming a 10-document suite for OS-PACS/PATROL/CONCIERGE/GUARDIAN/SENTINEL | TOPOLOGY-SUITE-SUMMARY, full document | incorporated (accuracy against this topic's actual membership assessed below) |

## Unresolved tensions

**The TOPOLOGY-SUITE-SUMMARY index document does not match this topic's actual membership, and this
mismatch is reported here rather than silently corrected** (per DC-CONSOLIDATOR-STD-001 §0, this
Consolidator pass does not alter topic membership or mark documents superseded). The summary claims
"COMPLETE - All 10 Documents Generated" for Network Topology and Logical Topology pairs covering five
services: **OS-PACS**, OS-PATROL, **OS-CONCIERGE**, OS-GUARDIAN, and OS-SENTINEL. But neither OS-PACS nor
OS-CONCIERGE topology documents are members of this topic, and the summary makes no mention whatsoever of
**OS-DRONE** (which has a full Logical Topology and Technical Architecture in this topic) or the four
**OpenSecure Hub** documents (Digital Twin Integration, Implementation Guide, Logical Topology, Network
Topology) — all of which are members here. Two explanations are consistent with the evidence and neither
can be confirmed from the documents alone: (a) the summary was generated for an earlier documentation
batch (OS-PACS/OS-CONCIERGE topology docs may exist elsewhere in the knowledge base under a different
topic, generated before OS-DRONE and the Hub documents were authored — OS-DRONE's own front matter shows a
March 2026 creation date versus the summary's December 2024 date, consistent with OS-DRONE being authored
later and the summary never having been regenerated to include it); or (b) the summary is simply
describing a different, overlapping-but-distinct documentation set than the one Stage 5's topic clustering
grouped together here. This is flagged as a documentation-currency issue for whoever maintains the
OpenSecure documentation set, not resolved by this pass.

**Separately, OS-DRONE has no companion Network Topology document in this topic's membership**, unlike
OS-GUARDIAN, OS-PATROL, and OS-SENTINEL, each of which has both a Network and a Logical Topology (plus a
Technical Architecture for three of the four services). This asymmetry may simply reflect that document
not yet existing, or it may exist elsewhere in the knowledge base under a different topic — this
consolidation does not have visibility into documents outside this topic's confirmed membership.

No numeric or architectural conflicts were found among the documents that are genuinely members of this
topic — where the same subsystem is described at two depths (e.g., OS-GUARDIAN's Logical Topology and
Technical Architecture), the two documents are consistent, one restating the other's design at greater
implementation detail rather than contradicting it.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/security/Open-Secure/OS-DRONE-Logical-Topology-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-DRONE-Network-Topology-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-DRONE-Technical-Architecture-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-GUARDIAN-Logical-Topology-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-GUARDIAN-Network-Topology-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-GUARDIAN-Technical-Architecture-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-PATROL-Logical-Topology-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-PATROL-Network-Topology-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Logical-Topology-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Network-Topology-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Technical-Architecture-md.md`
- `knowledge-base/d-central/security/Open-Secure/OpenSecure-Digital-Twin-Integration-md.md`
- `knowledge-base/d-central/security/Open-Secure/OpenSecure-Hub-Implementation-Guide-md.md`
- `knowledge-base/d-central/security/Open-Secure/OpenSecure-Hub-Logical-Topology-md.md`
- `knowledge-base/d-central/security/Open-Secure/OpenSecure-Hub-Network-Topology-md.md`
- `knowledge-base/d-central/meta/status-tracking/Open-Secure/TOPOLOGY-SUITE-SUMMARY-md.md`

Note: this list itself demonstrates the mismatch discussed above — I checked, and there is no
OS-PACS or OS-CONCIERGE topology document in this list, though the index document above claims both exist.

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/security/Open-Secure/OS-DRONE-Logical-Topology-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-DRONE-Network-Topology-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-DRONE-Technical-Architecture-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-GUARDIAN-Logical-Topology-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-GUARDIAN-Network-Topology-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-GUARDIAN-Technical-Architecture-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-PATROL-Logical-Topology-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-PATROL-Network-Topology-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Logical-Topology-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Network-Topology-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Technical-Architecture-md.md,
  knowledge-base/d-central/security/Open-Secure/OpenSecure-Digital-Twin-Integration-md.md,
  knowledge-base/d-central/security/Open-Secure/OpenSecure-Hub-Implementation-Guide-md.md,
  knowledge-base/d-central/security/Open-Secure/OpenSecure-Hub-Logical-Topology-md.md,
  knowledge-base/d-central/security/Open-Secure/OpenSecure-Hub-Network-Topology-md.md,
  knowledge-base/d-central/meta/status-tracking/Open-Secure/TOPOLOGY-SUITE-SUMMARY-md.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved by this pass — status assignment belongs to
DC-DEDUP-STD-001, not the Consolidator. Whether OS-PACS/OS-CONCIERGE topology documents exist elsewhere in
the knowledge base under a different topic, and whether TOPOLOGY-SUITE-SUMMARY should be regenerated to
reflect OS-DRONE and the Hub documents, is a documentation-maintenance question outside this Consolidator
pass's scope.
