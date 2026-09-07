# DC-OPENSECURE-PER-SERVICE-IMPL-GUIDES-RECONCILED-001 — OpenSecure Per-Service Implementation Guides, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `opensecure-per-service-implementation-guides` (5 docs).

## Current understanding

Five OpenSecure service implementation guides sharing one consistent template (Executive Summary with
phase-overview table → pre-deployment planning/BOM calculator → phased hardware/software build → testing
→ go-live → post-deployment maintenance → troubleshooting). One of the five (OS-DRONE) is already fully
detailed in a sibling consolidation; the other four (OS-CONCIERGE, OS-GUARDIAN, OS-PATROL, OS-SENTINEL)
are detailed here for the first time. All five are internally consistent — since each covers a distinct
OpenSecure service, there is no numeric overlap to conflict.

**OS-DRONE Implementation Guide (incorporated by reference):** already fully detailed in the sibling
[DC-OPENSECURE-OS-DRONE-RECONCILED-001](DC-OPENSECURE-OS-DRONE-RECONCILED-001.md) (regulatory prep,
hardware procurement, Fleet Ops software stack, ground-station/dock installation, pre-flight validation,
ongoing maintenance). Not re-derived here.

**OS-CONCIERGE Implementation Guide (incorporated):** visitor-management kiosk deployment — a 1-2-day/
property timeline, four kiosk hardware tiers ($1,500 basic through $4,500 weatherproof outdoor), a BOM
calculator with tiered cloud-hosting costs by kiosk count, and a 6-phase build (hardware assembly →
Ubuntu kiosk-mode software install with Chromium `--kiosk` auto-launch → cloud platform deployment
using a Node/MongoDB/Redis/Nginx Docker Compose stack with a full check-in/check-out/pre-registration
REST API and MongoDB visitor schema → React frontend with webcam photo capture, signature canvas, and
badge printing → testing including an async Python load-test script → go-live). Maintenance schedule and
a 4-issue troubleshooting guide (kiosk not booting to app, badge not printing, webcam quality, touchscreen
unresponsive).

**OS-GUARDIAN Implementation Guide (incorporated):** body-camera/evidence-management deployment — a
1-week/department timeline, a legal/policy pre-deployment framework (state body-camera law, retention
schedule by category — general 90 days, evidence 7 years, use-of-force/officer-involved-shooting
permanent), commercial camera options (Axon Body 3, WatchGuard V300, Motorola VB400) versus a DIY
Raspberry Pi build, and a BOM calculator scaling camera/docking/workstation/evidence-server cost by
officer count and sharing model. A 6-phase build: evidence server (MinIO S3-compatible object storage
with WORM/legal-hold retention via `mc retention set --default COMPLIANCE`, HashiCorp Vault KMS
encryption, PostgreSQL chain-of-custody audit logging) → camera configuration (commercial via
Evidence.com or a full DIY Raspberry Pi body-camera Python implementation with GPIO record button, a
30-second pre-event circular buffer, and GPS tagging) → docking-station auto-upload service (SHA-256
checksummed uploads with chain-of-custody logging, verify-then-delete-local semantics) → retention-
policy/RBAC database schema (category-based auto-delete triggers, six named roles from officer through
evidence custodian) → a detailed 2-day officer training curriculum (technical + legal/policy modules,
four role-play scenarios, a 20-question written test, practical assessment, signed acknowledgment) →
go-live. Maintenance schedule and a 4-issue troubleshooting guide.

**OS-PATROL Implementation Guide (incorporated):** fleet-management/mobile-patrol deployment — a 1-2-day/
vehicle timeline, four hardware configurations (basic GPS-only $210 through premium GPS+dashcam+LPR+
interior-camera+OBD-II $950), and a BOM/fleet-cost calculator. A 5-phase build: Traccar GPS server
(Dockerized, PostgreSQL-backed, with geofence creation via its REST API) → per-vehicle hardware
installation (Raspberry Pi GPS tracker with a worked Python `gpsd`-to-Traccar reporting script, dashcam
mounting/wiring guidance, LPR camera mounting/angle guidance, hardwire-vs-cigarette-lighter power
options) → software configuration (bulk vehicle registration script, geofence-exit/overspeed
notifications, an OpenALPR-based `LPRProcessor` class checking detected plates against a hot list and
alerting dispatch) → testing (GPS accuracy, geofence entry/exit, LPR detection) → go-live. A weekly
fleet-report generator and a 4-issue troubleshooting guide (GPS not reporting, poor accuracy, LPR not
reading, high data usage). Carries a secondary topic tag (`opensecure-patrol-sentinel-implementation`)
shared with the Sentinel guide below, suggesting these two may also be clustered together in a still-
unconfirmed Stage 5 topic.

**OS-SENTINEL Implementation Guide (incorporated):** video-surveillance/AI-analytics deployment — a
2-4-week (10-100 camera) timeline, a site-survey coverage-priority checklist, five camera-type
selections by use case (general surveillance, perimeter, LPR, PTZ, facial-recognition) with example
commercial models and price ranges, and a BOM calculator scaling camera/infrastructure/cabling/server
cost by camera count and quality tier. A 6-phase build: PoE switch/cabling infrastructure (with example
VLAN/QoS switch-config CLI and a UPS-sizing formula) → camera mounting/aiming/configuration (height and
lens-selection guidance by use case, a worked `curl`-based Dahua camera-config sequence) → Shinobi NVR
deployment (Dockerized with MariaDB, GPU passthrough for analytics, an API-driven bulk camera-add
script, SQL-driven recording/retention configuration) → AI analytics (a full YOLOv8-based
`SentinelAnalytics` Python class doing per-camera RTSP stream processing with polygon detection zones,
plus separate loitering/perimeter-breach/crowd-density detector classes) → testing (camera connectivity,
recording verification, AI-detection accuracy scenarios, load testing) → go-live. Maintenance schedule
and a 5-issue troubleshooting guide (camera offline, poor video quality, motion detection not
triggering, storage filling fast, inaccurate AI detections). Shares the same secondary topic tag as
OS-PATROL above.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Full OS-DRONE implementation guide content | OS-DRONE Implementation Guide | incorporated by reference — fully detailed in sibling [DC-OPENSECURE-OS-DRONE-RECONCILED-001](DC-OPENSECURE-OS-DRONE-RECONCILED-001.md) |
| Kiosk hardware tiers, BOM, 6-phase build | OS-CONCIERGE Implementation Guide, Executive Summary through Phase 6 | incorporated |
| Troubleshooting and maintenance | OS-CONCIERGE Implementation Guide, Post-Deployment / Troubleshooting Guide | incorporated |
| Legal/policy framework and retention schedule | OS-GUARDIAN Implementation Guide, Pre-Deployment Planning | incorporated |
| Evidence server (MinIO WORM/encryption/audit) and camera options | OS-GUARDIAN Implementation Guide, Phase 1-2 | incorporated |
| Docking auto-upload, retention/RBAC schema, officer training | OS-GUARDIAN Implementation Guide, Phase 3-5 | incorporated |
| Go-live and troubleshooting | OS-GUARDIAN Implementation Guide, Phase 6 / Troubleshooting Guide | incorporated |
| Fleet hardware tiers and Traccar server setup | OS-PATROL Implementation Guide, Executive Summary / Phase 1 | incorporated |
| Vehicle hardware install and software config (LPR hot-list) | OS-PATROL Implementation Guide, Phase 2-3 | incorporated |
| Testing, go-live, fleet reporting, troubleshooting | OS-PATROL Implementation Guide, Phase 4-5 / Post-Deployment | incorporated |
| Camera selection guide and BOM | OS-SENTINEL Implementation Guide, Pre-Deployment Planning | incorporated |
| Infrastructure, camera mounting/config, NVR deployment | OS-SENTINEL Implementation Guide, Phase 1-3 | incorporated |
| YOLOv8 AI analytics and detector classes | OS-SENTINEL Implementation Guide, Phase 4 | incorporated |
| Testing, go-live, maintenance, troubleshooting | OS-SENTINEL Implementation Guide, Phase 5-6 / Troubleshooting Guide | incorporated |

## Unresolved tensions

None identified — each of the four newly-detailed guides covers a distinct OpenSecure service with its
own hardware, software stack, and cost structure, so there is no numeric or claim overlap between them
to conflict. All five guides follow the same template structure consistently. The shared secondary
topic tag on OS-PATROL and OS-SENTINEL (`opensecure-patrol-sentinel-implementation`) is noted as a
possible additional Stage 5 topic pairing not yet confirmed/consolidated — flagged for awareness, not
acted on here.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/security/Open-Secure/OS-CONCIERGE-Implementation-Guide-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-DRONE-Implementation-Guide-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-GUARDIAN-Implementation-Guide-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-PATROL-Implementation-Guide-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Implementation-Guide-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/security/Open-Secure/OS-CONCIERGE-Implementation-Guide-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-DRONE-Implementation-Guide-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-GUARDIAN-Implementation-Guide-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-PATROL-Implementation-Guide-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Implementation-Guide-md.md,
]
reconciled_against: [DC-OPENSECURE-OS-DRONE-RECONCILED-001.md (sibling consolidation covering the OS-DRONE Implementation Guide in full)]
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

**References:**
- [[DC-OPENSECURE-OS-DRONE-RECONCILED-001|DC-OPENSECURE-OS-DRONE-RECONCILED-001 — OpenSecure OS-DRONE Subsystem, Consolidated (v1, generated 2026-09-05)]]

<!-- AUTO-GENERATED RELATED END -->
