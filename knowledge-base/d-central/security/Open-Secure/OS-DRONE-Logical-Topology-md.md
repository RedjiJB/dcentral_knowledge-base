---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: bdb960b4-7b31-48db-92d0-f44f210c441f
original_filename: OS-DRONE_Logical_Topology.md
created_at: 2026-03-05T13:51:16.081774+00:00
content_hash: 3ffcdc34cf45
topic: opensecure-os-drone-subsystem
topic: "opensecure-topology-documentation-suite"
consolidated_into: [docs/DC-OPENSECURE-OS-DRONE-RECONCILED-001.md, docs/DC-OPENSECURE-TOPOLOGY-DOCUMENTATION-SUITE-RECONCILED-001.md]
---

# OS-DRONE Logical Topology
## Autonomous Aerial Security Platform — System Architecture & Data Flows

**Document Type**: Logical Topology Specification
**Version**: 1.0
**Date**: March 2026
**Classification**: Technical Documentation
**Audience**: System Architects, Software Engineers, DevOps, Integration Teams

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Five-Layer Architecture](#five-layer-architecture)
3. [Core Components](#core-components)
4. [Drone State Machine](#drone-state-machine)
5. [Mission Planning & Dispatch Flow](#mission-planning--dispatch-flow)
6. [Video Pipeline & AI Analytics](#video-pipeline--ai-analytics)
7. [Telemetry Data Model](#telemetry-data-model)
8. [Evidence Chain of Custody](#evidence-chain-of-custody)
9. [Event-Driven Integration](#event-driven-integration)
10. [REST API Reference](#rest-api-reference)
11. [WebSocket Real-Time Streams](#websocket-real-time-streams)
12. [Scalability Design](#scalability-design)
13. [Technology Stack](#technology-stack)

---

## Executive Summary

### Logical Architecture Summary

OS-DRONE is built on the same **five-layer edge-cloud hybrid architecture** used across all OpenSecure platforms. The system separates concerns cleanly:

- **Presentation Layer**: Web dashboard, mobile app, Hub integration UI
- **Application Layer**: Mission control, dispatch, alert engine, API gateway
- **Data Layer**: PostgreSQL + TimescaleDB (telemetry), MinIO (video), Redis (live cache)
- **Edge Layer**: Drone firmware, on-board AI, ground station logic
- **Physical Layer**: Drones, docks, radios, cameras, GPS

### Key Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Dispatch to airborne | < 90 seconds | From alert → drone in air |
| C2 latency (4G) | < 150 ms | MAVLink round-trip |
| Video stream latency | < 500 ms | 1080p H.265 live stream |
| Geofence response | < 500 ms | Alert → drone reroutes |
| AI detection latency | < 200 ms | Camera → alert |
| Evidence upload hash verify | < 30 s | Per video segment |
| Mission planning time | < 60 s | Automated waypoint gen |
| Fleet Ops availability | 99.9% | HA with failover |

---

## Five-Layer Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                    LAYER 5: PRESENTATION                          │
│  Web Dashboard │ Mobile App │ Hub Integration │ VMS Overlay      │
│  React/Vue SPA │ iOS/Android│ OpenSecure Hub  │ OS-SENTINEL feed │
└──────────────────────────────────────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────┐
│                    LAYER 4: APPLICATION                           │
│  Mission Control  │ Dispatch Engine │ Alert Engine │ API Gateway  │
│  Waypoint planner │ Auto-dispatch   │ Rule engine  │ Kong/NGINX   │
│  Flight scheduler │ Nearest drone   │ AI events    │ Auth/rate    │
│  LAANC checker    │ assignment      │ Hub events   │ limiting     │
└──────────────────────────────────────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────┐
│                    LAYER 3: DATA                                  │
│  PostgreSQL+TS    │ MinIO S3         │ Redis           │ Kafka    │
│  Telemetry events │ Video evidence   │ Live telemetry  │ Events   │
│  Missions, fleet  │ Photos, reports  │ Drone positions │ Streams  │
│  Evidence records │ Chain-of-custody │ Dashboard cache │ Pub/sub  │
└──────────────────────────────────────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────┐
│                    LAYER 2: EDGE                                  │
│  Ground Station          │  Drone On-Board Agent                  │
│  Local NVR (AI inference)│  mavros + OS-DRONE agent              │
│  Dock controller         │  WireGuard VPN client                 │
│  Weather station         │  RTSP server                          │
│  C2 radio relay          │  Local mission executor               │
└──────────────────────────────────────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────┐
│                    LAYER 1: PHYSICAL                              │
│  Drone Airframe  │ Cameras   │ GPS/RTK  │ Docking Stations       │
│  Flight controller│ Gimbal   │ Barometer│ Charging hardware      │
│  Li-Po Battery   │ Thermal   │ Compass  │ Precision landing      │
└──────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### Mission Control Server (MCS)

```
Responsibilities:
├── Maintain real-time state of all drones (positions, battery, status)
├── Receive and validate mission requests from Hub or operators
├── Generate flight plans (waypoints, altitudes, speeds)
├── Check LAANC/airspace authorization before launch
├── Monitor active flights and detect anomalies
├── Coordinate drone handoffs between ground stations
└── Log all events to PostgreSQL/TimescaleDB

Technology:
├── Language: Python 3.11 (asyncio, FastAPI)
├── MAVLink: pymavlink 2.4 (flight controller comms)
├── Async: asyncio event loop (handles 100+ concurrent drones)
├── Cache: Redis (live drone state, 1s TTL)
├── Database: PostgreSQL 15 + TimescaleDB
└── Messaging: Kafka producer (events to Hub)

MCS Startup Sequence:
1. Connect to PostgreSQL (load fleet config)
2. Connect to Redis (restore in-memory state)
3. Connect to WireGuard VPN pool (open drone connections)
4. Start MAVLink multiplexer (mavproxy)
5. Subscribe to Kafka topics (OS-PATROL, OS-SENTINEL events)
6. Start FastAPI HTTP server (port 8080)
7. Start WebSocket server (port 8443, live telemetry)
8. Report healthy to Prometheus (/metrics endpoint)
```

### Drone On-Board Agent (OS-DRONE Agent)

```
Responsibilities (running on Jetson Orin NX):
├── Establish and maintain WireGuard VPN tunnel
├── Bridge MAVLink serial → UDP to MCS via VPN
├── Stream RTSP video to Fleet Ops (live)
├── Record full-quality video locally to NVMe
├── Run YOLOv8 object detection (onboard inference)
├── Publish detection events via MQTT
├── Execute local mission plans (autonomous operation)
└── Manage connectivity failover (LTE → radio)

Python Pseudocode — Main Loop:
```python
async def drone_agent_main():
    # Initialize connections
    vpn = await connect_wireguard(drone_id, fleet_ops_endpoint)
    mavlink = await connect_flight_controller("/dev/ttyUSB0", 115200)
    rtsp = RTSPStreamer(camera="/dev/video0", bitrate=4_000_000)
    recorder = LocalRecorder(path="/data/nvme", format="H265")
    ai = YOLOv8Inference(model="yolov8s.pt", device="cuda")

    while True:
        # Read telemetry (10 Hz)
        telem = await mavlink.get_telemetry()
        await vpn.publish("telemetry", telem)

        # Stream video + record locally (concurrent)
        frame = await camera.get_frame()
        await rtsp.push(frame)
        await recorder.write(frame)

        # AI detection (every 3rd frame = 10fps)
        if frame.index % 3 == 0:
            detections = await ai.infer(frame)
            if detections.has_threats():
                await vpn.publish("alert", detections)

        # Handle commands from MCS
        cmd = await vpn.receive_command()
        if cmd:
            await mavlink.send_command(cmd)
```

---

## Drone State Machine

```
States and Transitions:

OFFLINE ──────────────────────► ONLINE
(VPN disconnected)              (VPN connected, heartbeat OK)
                                    │
                                    ├─── DOCKED (charging/ready)
                                    │       │
                                    │       │ MISSION_ASSIGNED
                                    │       ▼
                                    │    PREFLIGHT
                                    │    (LAANC check, motors
                                    │     arm, GPS lock wait)
                                    │       │
                                    │       │ MOTORS_ARMED
                                    │       ▼
                                    │    TAKING_OFF
                                    │    (climb to safe altitude)
                                    │       │
                                    │       │ ALTITUDE_REACHED
                                    │       ▼
                                    │    ENROUTE
                                    │    (flying to mission)
                                    │       │
                                    │       │ ARRIVED_AT_ZONE
                                    │       ▼
                                    │    ON_MISSION
                                    │    (patrolling/surveilling)
                                    │       │
                                    │       ├── INCIDENT_RESPONSE
                                    │       │   (drone redirected
                                    │       │    to active alert)
                                    │       │
                                    │       │ MISSION_COMPLETE or LOW_BATTERY
                                    │       ▼
                                    │    RETURNING
                                    │    (RTH to nearest dock)
                                    │       │
                                    │       │ DOCK_DETECTED
                                    │       ▼
                                    │    LANDING
                                    │       │
                                    │       │ LANDED
                                    │       ▼
                                    └──► DOCKED

FAILSAFE STATES (from any state):
├── C2_LOST (no MAVLink >5s): → HOVER then RTH
├── GPS_LOST: → HOVER, wait for GPS recovery
├── LOW_BATTERY (<20%): → RTH immediately
├── GEOFENCE_BREACH: → Stop, RTH immediately
└── MOTOR_FAILURE: → Emergency descent (controlled)
```

---

## Mission Planning & Dispatch Flow

### Automated Dispatch Pipeline

```
TRIGGER: Hub alert received (from any OpenSecure service)
         OR: Scheduled patrol mission
         OR: Manual operator dispatch

Step 1: Alert Ingestion (< 5ms)
    ├── Kafka consumer receives event from Hub
    ├── Event decoded: { type, location, priority, timestamp }
    └── Dispatch Engine triggered

Step 2: Drone Selection Algorithm (< 100ms)
    ├── Query Redis: all drones with state = DOCKED or ON_MISSION
    ├── Filter: sufficient battery (>40%), available, within range
    ├── Score each candidate:
    │   ├── Distance to incident (weighted 60%)
    │   ├── Battery level (weighted 30%)
    │   └── Last mission time (weighted 10%)
    └── Select highest score → ASSIGNED_DRONE

Step 3: Airspace Check (< 5 seconds)
    ├── Call LAANC API: check authorization for zone + altitude
    ├── Check active NOTAMs (via FAA API)
    ├── Check for conflicting drone traffic in UTM system
    └── If approved → proceed │ If denied → select different altitude/time

Step 4: Flight Plan Generation (< 1 second)
    ├── Calculate optimal route: takeoff → incident → RTH
    ├── Set altitude: 120m AGL (below FAA 400ft limit)
    ├── Generate waypoints: MAVLink MISSION_ITEM format
    ├── Add geofence: bounding box around site
    └── Apply speed limits: max 15 m/s transit, 5 m/s survey

Step 5: Mission Upload (< 2 seconds)
    ├── POST mission via VPN to drone: /api/mission/upload
    ├── Drone acknowledges receipt (MAVLink MISSION_ACK)
    ├── Log mission to PostgreSQL: { mission_id, drone_id, plan, timestamp }
    └── Notify Hub: DRONE_DISPATCHED event (Kafka)

Step 6: Launch Sequence (< 90 seconds total)
    ├── Dock opens (5s)
    ├── Pre-arm checks: GPS fix, battery OK, compass calibrated (10s)
    ├── Motors arm + throttle up (10s)
    ├── Takeoff: climb to 30m (20s)
    ├── Transition to autonomous flight (5s)
    └── Hub notified: DRONE_AIRBORNE event

Step 7: On-Scene (continuous)
    ├── Drone circles incident area (configurable radius, speed)
    ├── Live video streamed to Fleet Ops + Hub
    ├── AI detects persons, vehicles, behaviors
    ├── Events published to Hub every detection
    └── Operator can take manual control at any time

Total: Alert → Drone On-Scene in approximately 90 seconds
```

---

## Video Pipeline & AI Analytics

### Full Video Processing Architecture

```
ONBOARD (Jetson Orin NX):

Step 1: Frame Capture
├── Camera: Sony IMX577 4K sensor
├── Interface: MIPI CSI-2 → ISP → NVMM memory
└── Frame rate: 30fps (4K) or 60fps (1080p)

Step 2: Parallel Processing
├── Thread A: NVENC hardware encode → H.265 → local NVMe record
└── Thread B: Inference pipeline (every 3rd frame)

Step 3: Edge AI Inference (Thread B)
├── Model: YOLOv8-small (int8 quantized for Jetson)
├── Classes: person, vehicle, bicycle, animal, weapon
├── Latency: 15ms per frame on Jetson Orin NX
└── Output: detections[] { class, confidence, bbox, timestamp }

Step 4: Tracking
├── DeepSORT tracker assigns persistent IDs
├── Tracks trajectories across frames
└── Events: "person entered zone", "vehicle stopped 3+ min"

Step 5: Live Stream
├── RTSP server: rtsp://{drone_vpn_ip}:8554/live
├── Bitrate: 4 Mbps (1080p H.265)
└── Latency: <500ms glass-to-glass

CLOUD (Fleet Ops, VLAN 30 GPU servers):

Step 6: Cloud Re-processing (on upload)
├── Full-quality 4K → advanced AI models
├── YOLOv8-large (higher accuracy, more classes)
├── DeepFace: face recognition (authorized personnel)
├── LPR: license plate recognition (links to OS-PATROL)
└── Behavior analysis: running, fighting, trespassing

Step 7: Analytics Storage
INSERT INTO drone_detections (
    drone_id, mission_id,
    timestamp, gps_lat, gps_lon, altitude,
    object_class, confidence,
    bbox_x, bbox_y, bbox_w, bbox_h,
    track_id, event_type,
    video_clip_url
);

Step 8: Event Generation + Hub Notification
IF event_type IN ('intrusion', 'weapon', 'vehicle_stopped'):
    → Kafka publish: drone.alert.{severity}
    → Hub event correlation engine
    → Potential OS-SENTINEL PTZ camera activation
    → Potential OS-PATROL unit dispatch

Total pipeline: Frame captured → Hub alert: 200-500ms
```

---

## Telemetry Data Model

### PostgreSQL Schema

```sql
-- Core tables (TimescaleDB hypertables for time-series)

-- Drone fleet registry
CREATE TABLE drones (
    id          UUID PRIMARY KEY,
    serial_no   TEXT UNIQUE NOT NULL,
    model       TEXT,
    site_id     UUID REFERENCES sites(id),
    wireguard_pubkey TEXT,
    status      TEXT DEFAULT 'OFFLINE',
    created_at  TIMESTAMPTZ DEFAULT now()
);

-- High-frequency telemetry (hypertable, 5s retention bucket)
CREATE TABLE drone_telemetry (
    time        TIMESTAMPTZ NOT NULL,
    drone_id    UUID REFERENCES drones(id),
    lat         DOUBLE PRECISION,
    lon         DOUBLE PRECISION,
    altitude    FLOAT,          -- meters AGL
    heading     FLOAT,          -- degrees
    speed       FLOAT,          -- m/s
    battery_pct SMALLINT,
    flight_mode TEXT,
    satellites  SMALLINT,
    hdop        FLOAT,
    rssi_lte    SMALLINT,
    rssi_radio  SMALLINT
);
SELECT create_hypertable('drone_telemetry', 'time');
-- Compress chunks older than 7 days
SELECT add_compression_policy('drone_telemetry', INTERVAL '7 days');

-- Mission records
CREATE TABLE missions (
    id          UUID PRIMARY KEY,
    drone_id    UUID REFERENCES drones(id),
    trigger_event_id UUID,     -- link to Hub event that caused dispatch
    type        TEXT,          -- 'patrol', 'incident_response', 'scheduled'
    status      TEXT,          -- 'planned', 'active', 'complete', 'aborted'
    waypoints   JSONB,
    started_at  TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    total_flight_time INTERVAL,
    distance_km FLOAT,
    video_urls  TEXT[]         -- MinIO S3 keys
);

-- AI detection events
CREATE TABLE drone_detections (
    id          UUID PRIMARY KEY,
    time        TIMESTAMPTZ NOT NULL,
    drone_id    UUID REFERENCES drones(id),
    mission_id  UUID REFERENCES missions(id),
    lat         DOUBLE PRECISION,
    lon         DOUBLE PRECISION,
    altitude    FLOAT,
    object_class TEXT,
    confidence  FLOAT,
    bbox        JSONB,
    track_id    INTEGER,
    event_type  TEXT,
    video_clip_url TEXT,       -- MinIO S3 key
    hub_event_id UUID          -- correlated Hub event
);
SELECT create_hypertable('drone_detections', 'time');

-- Evidence chain of custody
CREATE TABLE drone_evidence (
    id          UUID PRIMARY KEY,
    drone_id    UUID REFERENCES drones(id),
    mission_id  UUID REFERENCES missions(id),
    recorded_at TIMESTAMPTZ,
    uploaded_at TIMESTAMPTZ,
    duration_s  INTEGER,
    size_bytes  BIGINT,
    sha256      TEXT NOT NULL,  -- integrity hash
    s3_bucket   TEXT,
    s3_key      TEXT,
    bc_tx_hash  TEXT            -- blockchain transaction (chain-of-custody)
);
```

---

## Evidence Chain of Custody

### Same System as OS-GUARDIAN (Shared Infrastructure)

```
Evidence Flow (identical to OS-GUARDIAN):

Step 1: On-drone recording
├── Video segments: 5-minute H.265 files
├── Each segment: SHA256 hashed immediately after write
└── GPS + timestamp embedded in video metadata (EXIF)

Step 2: Upload to MinIO (on dock WiFi)
├── TLS upload: drone → dock WiFi → VPN → MinIO
├── S3 bucket: drone-evidence/{site_id}/{drone_id}/{date}/
├── Server-side hash verification (compare drone hash vs received)
└── Upload rejected if hashes don't match (integrity failure alert)

Step 3: Blockchain Chain of Custody
├── Same Hyperledger Fabric network as OS-GUARDIAN
├── Transaction recorded: {
│     drone_id, mission_id, sha256,
│     recorded_at, uploaded_at,
│     operator_id, site_id
│   }
├── Immutable record: cannot be altered without detection
└── Court admissibility: cryptographic proof of authenticity

Step 4: Retention Management
├── Default: 90 days (configurable per customer)
├── Legal hold: exempt from auto-deletion (Court orders)
├── Export: signed download URL with audit log entry
└── Deletion: logged with operator ID, reason, timestamp

Python pseudocode:
def upload_evidence(video_file, drone_id, mission_id):
    sha256 = hash_file(video_file)
    s3_key = f"drone-evidence/{site_id}/{drone_id}/{date}/{sha256[:8]}.mp4"

    # Upload to MinIO
    minio.upload(s3_key, video_file)
    server_hash = minio.get_object_hash(s3_key)

    assert sha256 == server_hash, "INTEGRITY FAILURE — video tampered"

    # Record in database
    db.insert("drone_evidence", {
        "sha256": sha256, "s3_key": s3_key,
        "drone_id": drone_id, "mission_id": mission_id
    })

    # Blockchain immutable record
    blockchain.record_evidence(sha256, drone_id, mission_id, timestamp)

    return {"status": "ok", "sha256": sha256, "bc_tx": blockchain.last_tx}
```

---

## Event-Driven Integration

### Kafka Topics & Cross-Service Events

```
OS-DRONE Kafka Topics:

PRODUCES (publishes to Hub):
├── drone.telemetry.{drone_id}
│   └── 5Hz position updates (lat, lon, alt, battery, speed)
├── drone.status.{drone_id}
│   └── State changes (DOCKED → TAKING_OFF → ON_MISSION...)
├── drone.alert.high / drone.alert.medium / drone.alert.low
│   └── AI detections requiring human attention
├── drone.mission.{drone_id}
│   └── Mission lifecycle events (assigned, started, completed)
└── drone.evidence.{drone_id}
    └── Evidence upload completions (with SHA256, S3 key)

CONSUMES (reacts to Hub):
├── sentinel.alert.*         → Dispatch drone to camera alert location
├── patrol.lpr.hit           → Dispatch drone to track vehicle
├── pacs.access.denied       → Dispatch drone to access point
├── pacs.intrusion.detected  → Dispatch drone to breach location
└── hub.mission.drone.*      → Direct mission commands from Hub operators

Cross-Service Event Examples:

SCENARIO 1: OS-SENTINEL Intrusion → OS-DRONE Response
┌─────────────────────────────────────────────────────────┐
│ 23:15:42 - OS-SENTINEL camera 34 detects person        │
│            in restricted zone (Building C, north side)  │
│ 23:15:42 - Hub event: sentinel.alert.high published     │
│ 23:15:43 - OS-DRONE dispatch engine receives event      │
│ 23:15:43 - Nearest drone selected: DRONE-07 (82% batt) │
│ 23:15:45 - LAANC checked: approved                     │
│ 23:15:46 - Mission uploaded to DRONE-07                 │
│ 23:16:12 - DRONE-07 airborne                           │
│ 23:17:15 - DRONE-07 arrives at Building C north        │
│ 23:17:16 - Live video feed on Hub dashboard            │
│ 23:17:20 - AI detects: 2 persons, 1 carrying bag       │
│ 23:17:20 - OS-PATROL dispatch: nearest patrol unit     │
│ 23:18:00 - Patrol unit arrives, DRONE-07 illuminates   │
└─────────────────────────────────────────────────────────┘

SCENARIO 2: OS-PATROL LPR Hit → Aerial Follow
┌─────────────────────────────────────────────────────────┐
│ 14:32:10 - OS-PATROL vehicle 3 scans plate: ABC-1234   │
│ 14:32:11 - Hot-list match: stolen vehicle              │
│ 14:32:11 - Hub event: patrol.lpr.hit published          │
│ 14:32:12 - OS-DRONE: nearest drone dispatched          │
│ 14:32:12 - OS-PATROL: unit dispatched (separate)       │
│ 14:33:05 - Drone airborne, tracks vehicle from 80m     │
│ 14:33:06 - Real-time GPS: drone telemetry updates       │
│            Hub dashboard (vehicle + drone on same map) │
│ 14:34:00 - Vehicle stops: drone maintains overhead     │
│ 14:34:30 - Patrol unit arrives                         │
│ 14:35:00 - Incident resolved, evidence uploaded        │
└─────────────────────────────────────────────────────────┘
```

---

## REST API Reference

### OS-DRONE API Endpoints

```
Base URL: https://api.opensecure.com/drone/v1/

FLEET MANAGEMENT
GET    /fleet                          List all drones + status
GET    /fleet/{drone_id}               Single drone detail
POST   /fleet                          Register new drone
PUT    /fleet/{drone_id}               Update drone config
DELETE /fleet/{drone_id}               Decommission drone
GET    /fleet/{drone_id}/telemetry     Last 24h telemetry
GET    /fleet/{drone_id}/battery       Battery history + predictions

MISSIONS
GET    /missions                       List missions (filter by date, drone, type)
POST   /missions                       Create manual mission
GET    /missions/{mission_id}          Mission detail + waypoints
PUT    /missions/{mission_id}/abort    Abort active mission (drone RTH)
GET    /missions/{mission_id}/track    GPS track for completed mission

DISPATCH
POST   /dispatch/alert                 Dispatch drone to GPS coordinates
POST   /dispatch/scheduled             Create recurring patrol mission
GET    /dispatch/coverage              Coverage map (all active drones)

VIDEO
GET    /video/live/{drone_id}          Live RTSP stream URL
GET    /video/recordings/{drone_id}    List recorded videos
GET    /video/{recording_id}           Signed download URL (with COC)
POST   /video/{recording_id}/redact    Request AI-assisted redaction

EVIDENCE
GET    /evidence                       List evidence records
GET    /evidence/{id}                  Evidence detail + COC
GET    /evidence/{id}/download         Signed URL with audit log
GET    /evidence/{id}/blockchain       Blockchain COC verification
POST   /evidence/{id}/legal-hold       Mark for legal hold (prevent deletion)

EVENTS & ALERTS
GET    /events                         All events (filterable)
GET    /events/active                  Active unacknowledged alerts
PUT    /events/{id}/acknowledge        Acknowledge alert
GET    /events/{id}/video              Video clip for event

COMPLIANCE
GET    /compliance/remoteid/{date}     Remote ID broadcast log
GET    /compliance/laanc               LAANC authorization log
GET    /compliance/flights             Flight log (FAA format export)
POST   /compliance/report              Generate compliance report

SITES & DOCKS
GET    /sites                          List deployment sites
GET    /sites/{site_id}/docks          List docks at site
GET    /sites/{site_id}/docks/{id}     Dock status (battery level, occupied)
POST   /sites/{site_id}/docks/{id}/open  Manual dock open command

Response format (standard across all endpoints):
{
    "status": "ok" | "error",
    "data": { ... },
    "meta": {
        "timestamp": "2026-03-04T12:00:00Z",
        "request_id": "uuid",
        "pagination": { "page": 1, "total": 100 }
    }
}
```

---

## WebSocket Real-Time Streams

### Live Telemetry via WebSocket

```javascript
// Connect to live drone telemetry
const ws = new WebSocket('wss://api.opensecure.com/drone/v1/ws');
ws.send(JSON.stringify({ auth: 'Bearer <token>' }));

// Subscribe to topics
ws.send(JSON.stringify({
    action: 'subscribe',
    topics: [
        'drones/*',            // All drone position updates (5Hz)
        'alerts/drone/*',      // All drone AI alerts
        'missions/*/status',   // Mission status changes
        'docks/*/status',      // Dock status changes
    ]
}));

// Incoming message format
{
    "topic": "drones/DRONE-07/telemetry",
    "timestamp": "2026-03-04T23:17:15.123Z",
    "data": {
        "drone_id": "DRONE-07",
        "lat": 45.4215,
        "lon": -75.6972,
        "altitude": 80.5,
        "heading": 270,
        "speed": 12.3,
        "battery_pct": 74,
        "flight_mode": "AUTO",
        "rssi_lte": -78,
        "state": "ON_MISSION"
    }
}

// Alert message format
{
    "topic": "alerts/drone/high",
    "timestamp": "2026-03-04T23:17:20.456Z",
    "data": {
        "drone_id": "DRONE-07",
        "mission_id": "uuid",
        "alert_type": "PERSON_DETECTED",
        "confidence": 0.94,
        "location": { "lat": 45.4215, "lon": -75.6972 },
        "video_clip_url": "https://...",
        "thumbnail_url": "https://..."
    }
}
```

---

## Scalability Design

### Horizontal Scaling Patterns

```
COMPONENT          SCALE METHOD              CAPACITY PER UNIT
─────────────────────────────────────────────────────────────
MCS Application    Add replica instances     50 drones per instance
WireGuard VPN      Add VPN gateway nodes     200 tunnels per node
AI GPU Workers     Add GPU servers           20 streams per RTX 4090
PostgreSQL         Read replicas             Write: primary, Read: replicas
MinIO Storage      Add nodes (EC 4+2)        80 TB usable per 4-node set
Redis              Cluster (3 shards ×2)     10M ops/sec per cluster
Kafka              Add brokers               Unlimited with partitioning
RTSP Re-stream     Add media relay servers   50 streams per server

Scaling Triggers (Prometheus rules):
├── MCS CPU > 80%: scale out 1 replica
├── VPN connections > 150/node: add VPN node
├── GPU utilization > 85%: add GPU worker
├── MinIO < 20% free: add storage node
└── Kafka lag > 10k messages: add consumer instances

Maximum Validated Scale:
├── 1,000 concurrent drones
├── 1,000 simultaneous RTSP streams (1080p)
├── 50 TB/day ingest (video evidence)
└── 10 million telemetry points/day
```

---

## Technology Stack

### Complete Stack (Matching OpenSecure Conventions)

| Layer | Component | Technology | Notes |
|-------|-----------|-----------|-------|
| Drone OS | Companion computer | Ubuntu 22.04 LTS | Jetson Orin NX |
| Flight SW | Autopilot | ArduPilot/PX4 | Open-source, MAVLink 2.0 |
| Drone agent | On-board software | Python 3.11 + asyncio | OS-DRONE Agent |
| AI (edge) | Object detection | YOLOv8 + TensorRT | int8 quantized for Jetson |
| AI (cloud) | Advanced analytics | YOLOv8L + DeepFace | NVIDIA GPU servers |
| Video encode | On-drone | NVENC (H.265) | Hardware accelerated |
| VPN | Drone ↔ Hub | WireGuard | Same as OS-PATROL |
| C2 protocol | MAVLink 2.0 | pymavlink | Industry standard |
| Backend | MCS server | FastAPI + asyncio | Python 3.11 |
| Database | Telemetry | PostgreSQL 15 + TimescaleDB | Same as OS-PATROL |
| Storage | Video evidence | MinIO (S3-compatible) | Same as OS-GUARDIAN |
| Cache | Live state | Redis 7 Cluster | Same as OS-PATROL |
| Messaging | Event bus | Apache Kafka | Same as all OpenSecure |
| Monitoring | Metrics | Prometheus + Grafana | Same as all OpenSecure |
| Logs | Aggregation | Loki + Grafana | Same as all OpenSecure |
| Container | Orchestration | Docker + Kubernetes | Same as all OpenSecure |
| Compliance | Blockchain COC | Hyperledger Fabric | Same as OS-GUARDIAN |
| Auth | Identity | Keycloak (SSO) | Same as OpenSecure Hub |
| API | Gateway | Kong / NGINX | Same as all OpenSecure |

**Open-Source Dependencies (Zero Vendor Lock-In):**
- ArduPilot: Apache 2.0
- pymavlink: LGPL
- YOLOv8 (Ultralytics): AGPL-3.0
- DeepFace: MIT
- RTSP server: GStreamer (LGPL)
- MAVProxy: GPL
- OpenDroneID: Apache 2.0

---

**Document Version**: 1.0
**Platform**: OS-DRONE v1.0
**Compatible with**: OpenSecure Hub 1.x
**Companion Document**: OS-DRONE_Network_Topology.md
