# DC-OPENSECURE-OS-DRONE-ADVANCED-RECONCILED-001 — OS-DRONE Advanced Visual Intelligence & Spatial Federation, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `opensecure-os-drone-advanced-capabilities` (2 docs).

## Current understanding

Two companion advanced-capability specs for OS-DRONE, the drone product in the Open-Secure suite:
Advanced Visual Intelligence covers the onboard sensor/fusion/AR payload; Federation & 3D Spatial
Intelligence covers how that payload's output integrates with the rest of the OpenSecure ecosystem.
Advanced Visual Intelligence explicitly lists Federation & 3D Spatial as a companion document, and both
are internally consistent — no competing claims.

**Onboard sensor/fusion architecture (incorporated):** a "modular payload bus" design philosophy —
every sensor (EO/RGB, thermal LWIR, SWIR, LiDAR, hyperspectral) is a hot-swappable data source feeding
one unified sensor-fusion engine on an NVIDIA Jetson Orin NX, rather than bolting sensors on
independently [§Design Philosophy]. A full electromagnetic-spectrum sensor table maps wavelength bands
to specific hardware and use cases (e.g., SWIR 1000-1700nm sees through smoke/glass/wet surfaces; LWIR
8-14μm reveals body heat) [§Full-Spectrum Imaging Stack], with four named payload tiers from Standard
Security (+$4,000, EO+LWIR) to Intelligence/Critical-Infrastructure (+$60,000, adds MWIR+SWIR+radar)
[§Full-Spectrum Imaging Stack]. A night-vision fusion engine dynamically selects among four fusion modes
based on lux/smoke/rain conditions, with example Python pseudocode given [§Advanced Night Vision &
Fusion]. IMU/GPS tight coupling enables per-pixel geolocation of AI detections to ±3m accuracy
[§Sensor Fusion Engine]. A two-level AR system is specified: Level 1 on-stream HUD (baked into the
video feed itself) and Level 2 operator-side interactive AR (Fleet Ops dashboard, extending to AR
glasses like HoloLens 2) [§AR Overlay System]. LiDAR/3D-mapping, multispectral/hyperspectral, and
autonomous-survey/photogrammetry capabilities are each specified with hardware options, open-source
processing stacks (OpenDroneMap, PDAL, LIO-SAM), and worked code examples (NDVI computation, LiDAR
change detection) [§LiDAR & 3D Mapping through §Surveying & Photogrammetry Engine]. Five named "payload
profiles" (Night Security, Daytime Patrol, Smoke/Fire, Survey/Mapping, Inspection, Incident Response)
allow instant reconfiguration [§Payload Configuration Profiles]. A full hardware BOM table gives cost
and weight per sensor option, with a recommended starting configuration (EO+LWIR, $5,800/drone above
airframe) [§Hardware BOM by Capability Tier]. An integration section explicitly maps how OS-DRONE data
flows to OS-SENTINEL, OS-PATROL, OS-GUARDIAN, OS-PACS, and the Digital Twin [§Integration with
OpenSecure Ecosystem].

**Federation and 3D spatial architecture (incorporated):** frames OS-DRONE as the ecosystem's "spatial
intelligence layer" — the only component that continuously moves across a site, making it the natural
source for a continuously-updated ("living," not static-import) 3D digital twin [§The Vision]. A
four-plane federation architecture is specified: Control Plane (mTLS gRPC, dispatch/mission management,
<100ms), Event Plane (Kafka pub/sub, alerts/telemetry, <500ms), Media Plane (RTSP/HLS over WireGuard,
live video, <500ms glass-to-glass), and Spatial Plane (OGC API/3D Tiles/WMTS, 3D models/point clouds,
minutes-to-hours processing then tile-served) [§Secure Federation Architecture]. A dedicated Federation
Gateway enforces spatial scoping — every cross-service data request is checked against the requesting
organization's registered site-boundary geometry via PostGIS intersection, with responses clipped to
only the authorized overlap area [§Spatial Scoping]. Per-service federation protocols are specified in
detail for OS-DRONE↔OS-SENTINEL (camera-alert-triggers-drone-dispatch and drone-repositions-PTZ-cameras,
both ways) and OS-DRONE↔OS-PATROL (LPR hits trigger aerial intercept; aerial tracks feed patrol vehicle
routing), each with concrete Kafka topic names and message schemas [§Per-Service Federation Protocols].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Modular payload bus design and full-spectrum sensor stack/tiers | Advanced Visual Intelligence §Design Philosophy, §Full-Spectrum Imaging Stack | incorporated |
| Multi-mode night vision fusion engine | Advanced Visual Intelligence §Advanced Night Vision & Fusion | incorporated |
| Sensor fusion engine, IMU/GPS tight coupling for geolocation | Advanced Visual Intelligence §Sensor Fusion Engine | incorporated |
| Two-level AR overlay system (on-stream HUD + operator/glasses AR) | Advanced Visual Intelligence §AR Overlay System | incorporated |
| LiDAR/3D mapping, multispectral/hyperspectral, survey/photogrammetry capabilities | Advanced Visual Intelligence §LiDAR & 3D Mapping through §Surveying & Photogrammetry Engine | incorporated |
| Payload configuration profiles and Jetson onboard processing allocation | Advanced Visual Intelligence §Payload Configuration Profiles, §On-Board Processing Architecture | incorporated |
| Fleet Ops visual intelligence dashboard and hardware BOM | Advanced Visual Intelligence §Fleet Ops Visual Intelligence Dashboard, §Hardware BOM by Capability Tier | incorporated |
| Cross-ecosystem integration summary (→SENTINEL/PATROL/GUARDIAN/PACS/Digital Twin) | Advanced Visual Intelligence §Integration with OpenSecure Ecosystem | incorporated |
| Drone as ecosystem spatial-intelligence-layer vision | Federation & 3D Spatial §The Vision | incorporated |
| Four-plane federation architecture (Control/Event/Media/Spatial) | Federation & 3D Spatial §Secure Federation Architecture | incorporated |
| Federation Gateway and spatial-scoping access control | Federation & 3D Spatial §Secure Federation Architecture, §Spatial Scoping | incorporated |
| Per-service federation protocols (SENTINEL, PATROL) with Kafka schemas | Federation & 3D Spatial §Per-Service Federation Protocols | incorporated |

## Unresolved tensions

None identified in this pass — Federation & 3D Spatial is explicitly named as a companion document by
Advanced Visual Intelligence, the two cover non-overlapping architectural layers (onboard sensor/fusion
vs. cross-service federation), and every cross-reference to other OS-* products (SENTINEL, PATROL,
GUARDIAN, PACS) is consistent between the two documents.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/security/Open-Secure/OS-DRONE-Advanced-Visual-Intelligence-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-DRONE-Federation-3D-Spatial-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/security/Open-Secure/OS-DRONE-Advanced-Visual-Intelligence-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-DRONE-Federation-3D-Spatial-md.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

Neither source doc is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
