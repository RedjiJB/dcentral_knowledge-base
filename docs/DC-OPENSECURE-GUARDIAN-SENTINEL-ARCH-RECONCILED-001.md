# DC-OPENSECURE-GUARDIAN-SENTINEL-ARCH-RECONCILED-001 — OS-GUARDIAN & OS-SENTINEL Technical Architecture, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `opensecure-guardian-sentinel-architecture` (2 docs).

## Current understanding

Two sibling Open-Secure product architecture specs sharing an identical 15+ section document template
(Executive Summary → System Architecture → Core Technology → Component Architecture →
[product-specific layer] → Data Architecture → Video Pipeline → Security → Network → Scalability → HA →
Integration → Deployment → Monitoring → Compliance → DR → Cost Modeling). Each product is a distinct
piece of the same open-source security suite: OS-GUARDIAN is body-worn-camera evidence management;
OS-SENTINEL is fixed-camera AI video surveillance/analytics. They share the same core storage stack but
serve genuinely different functions, not overlapping claims about the same system.

**OS-GUARDIAN — body camera & evidence management (incorporated):** an edge-recording body-camera
platform (Raspberry Pi Zero 2 W through Pi 4) with local microSD storage and WiFi auto-sync to an
evidence server, backed by PostgreSQL+TimescaleDB for metadata and MinIO for S3-compatible video
storage [§Executive Summary, §System Architecture]. Its core differentiator is a blockchain
chain-of-custody layer — every evidence action (uploaded, viewed, exported) writes an immutable,
cryptographically-signed ledger record, with three named blockchain implementation options
(Hyperledger Fabric for permissioned/enterprise use, public Ethereum for public verifiability,
OpenTimestamps/Bitcoin for lightweight timestamping-only) [§Blockchain Chain-of-Custody]. Three concrete
hardware tiers are specified with full BOMs: Budget ($75/camera, 8-10hr runtime, 1080p), Professional
($200/camera, 12-16hr, 4K, GPS, night vision), and Enterprise ($350/camera, 20-24hr swappable battery,
4G LTE real-time upload, IP67) [§Body Camera Hardware Architecture]. A full PostgreSQL schema (officers,
cameras, evidence as a TimescaleDB hypertable, chain_of_custody, incidents, redactions, audit_log
tables) and a legally-formatted chain-of-custody certificate export format are given in full [§Data
Architecture, §Blockchain Chain-of-Custody].

**OS-SENTINEL — AI video surveillance & analytics (incorporated):** built on Frigate NVR 0.13+ core
technology, emphasizing edge-first AI inference (sub-100ms latency) with GPU/TPU acceleration (NVIDIA
CUDA, Google Coral TPU, Intel OpenVINO) and model flexibility (YOLOv8, TensorFlow, PyTorch, ONNX,
custom models) [§Executive Summary]. Explicitly privacy-preserving by design — on-premise AI inference
with no cloud transmission of video. Shares the identical core data-layer stack with OS-GUARDIAN
(PostgreSQL+TimescaleDB for events, MinIO for video storage, MQTT/REST/WebSocket APIs), which is a
deliberate architectural consistency across the Open-Secure product suite rather than a coincidence
[§Executive Summary, Technology Stack].

**Shared architectural pattern across both (incorporated):** both products scale across the same four
deployment tiers (Small/Medium/Enterprise/Campus or Multi-Site), both name the same compliance
frameworks (CJIS, HIPAA, and — SENTINEL additionally — GDPR/CCPA/SOC2), and both are built container-
first (Docker/Docker Compose) with the same message-bus pattern (Eclipse Mosquitto MQTT) for event
distribution.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Body-camera edge-recording architecture and hardware tiers | OS-GUARDIAN §Executive Summary, §Body Camera Hardware Architecture | incorporated |
| Blockchain chain-of-custody design (3 implementation options) | OS-GUARDIAN §Blockchain Chain-of-Custody | incorporated |
| Evidence database schema and legal COC certificate format | OS-GUARDIAN §Data Architecture, §Blockchain Chain-of-Custody | incorporated |
| Security threat model and mitigations | OS-GUARDIAN §Security Architecture | incorporated |
| AI-powered surveillance platform on Frigate NVR core | OS-SENTINEL §Executive Summary | incorporated |
| Edge-first AI/GPU-TPU acceleration and model flexibility | OS-SENTINEL §Executive Summary | incorporated |
| Shared data-layer stack (PostgreSQL/TimescaleDB, MinIO, MQTT) | OS-GUARDIAN + OS-SENTINEL, both §Technology Stack | incorporated (deliberate suite-wide consistency) |
| Deployment-scale tiers and compliance framework alignment | OS-GUARDIAN + OS-SENTINEL, both §Executive Summary | incorporated |

## Unresolved tensions

None identified in this pass — the two products serve genuinely different functions (body-camera
evidence chain-of-custody vs. fixed-camera AI analytics) within one product suite, share a consistent
underlying data-layer stack by deliberate design, and make no competing claims about the same system.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/security/Open-Secure/OS-GUARDIAN-Technical-Architecture-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Technical-Architecture-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/security/Open-Secure/OS-GUARDIAN-Technical-Architecture-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Technical-Architecture-md.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

Neither source doc is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
