---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: bf87aef2-9853-4f03-a532-262a03db3fd6
original_filename: TECHNICAL_ARCHITECTURE.md
created_at: 2025-12-02T00:47:53.908429+00:00
content_hash: 016ad5e12c19
topic: ihose-architecture-deployment
topic: "ihose-openvision-documentation-package"
---

# OpenVision Platform - Complete Technical Architecture

**Document Type**: Technical Architecture  
**Version**: 1.0  
**Date**: November 2024  
**Classification**: Technical Documentation  
**Audience**: Technical Leaders, Architects, Engineers

---

## Table of Contents

1. [Executive Technical Summary](#executive-technical-summary)
2. [System Architecture Overview](#system-architecture-overview)
3. [Component Architecture](#component-architecture)
4. [Data Architecture](#data-architecture)
5. [Security Architecture](#security-architecture)
6. [Deployment Architecture](#deployment-architecture)
7. [Scalability & Performance](#scalability-and-performance)
8. [Integration Architecture](#integration-architecture)
9. [Technology Stack](#technology-stack)
10. [Development & Operations](#development-and-operations)

---

## Executive Technical Summary

### Platform Overview

OpenVision Platform is an enterprise-grade, open-source video surveillance and IoT integration system built on modern cloud-native principles. The architecture is designed for:

- **Massive Scale**: 1 to 10,000+ cameras
- **Edge Computing**: Process video at the source
- **AI-First**: Native machine learning integration
- **Multi-Tenancy**: Isolated customer deployments
- **High Availability**: 99.9% uptime SLA capability
- **Hardware Agnostic**: Runs on x86, ARM, RISC-V

### Core Design Principles

1. **Microservices Architecture**: Independently deployable, scalable services
2. **Event-Driven**: Asynchronous communication via message brokers
3. **API-First**: Everything exposed via REST/GraphQL/gRPC
4. **Edge-Native**: Intelligent processing at data source
5. **Infrastructure as Code**: Reproducible, version-controlled deployments
6. **Security by Design**: Zero-trust, defense-in-depth
7. **Observable**: Built-in metrics, logging, tracing

### Technology Philosophy

- **Open Source First**: 100% FOSS components
- **Cloud Native**: Kubernetes-native design
- **Proven Technologies**: Battle-tested components
- **Vendor Neutral**: No proprietary lock-in
- **Standards Based**: ONVIF, MQTT, OpenAPI
- **Container First**: Docker/OCI containers
- **GitOps Friendly**: Declarative configuration

---

## System Architecture Overview

### Layered Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Presentation Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Web UI     │  │  Mobile App  │  │   Grafana    │             │
│  │  (React)     │  │(React Native)│  │  Dashboards  │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                        HTTPS/WSS (TLS 1.3)
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                   Apache APISIX                               │  │
│  │  • JWT/OAuth2 Authentication                                 │  │
│  │  • Rate Limiting & Throttling                                │  │
│  │  • Service Routing & Load Balancing                          │  │
│  │  • API Versioning & Transformation                           │  │
│  │  • mTLS for service-to-service                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                          Internal APIs
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Application Services Layer                        │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │   VMS     │  │ Analytics │  │Integration│  │   User    │       │
│  │  Service  │  │  Service  │  │  Service  │  │ Management│       │
│  │           │  │           │  │           │  │           │       │
│  │ • Camera  │  │ • YOLO    │  │ • MQTT    │  │ • Keycloak│       │
│  │ • Record  │  │ • Face    │  │ • Modbus  │  │ • RBAC    │       │
│  │ • Stream  │  │ • ALPR    │  │ • BACnet  │  │ • SSO     │       │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘       │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │  Storage  │  │   Event   │  │  Workflow │  │  Digital  │       │
│  │  Service  │  │  Service  │  │  Service  │  │   Twin    │       │
│  │           │  │           │  │           │  │           │       │
│  │ • MinIO   │  │ • NATS    │  │ • Temporal│  │ • Ditto   │       │
│  │ • Tiering │  │ • CEP     │  │ • Node-RED│  │ • PostGIS │       │
│  │ • Cleanup │  │ • Alerts  │  │ • Cron    │  │ • 3D Viz  │       │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘       │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                        Message Bus (NATS)
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Message Broker Layer                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  NATS JetStream         │  Eclipse Mosquitto (MQTT)          │  │
│  │  • Internal events       │  • IoT device connectivity        │  │
│  │  • Service messaging     │  • Sensor data ingestion          │  │
│  │  • Stream processing     │  • Camera commands                │  │
│  │  • Request/Reply         │  • Real-time pub/sub              │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                           Database APIs
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Data Layer                                   │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │PostgreSQL │  │   MinIO   │  │   Redis   │  │   Ceph    │       │
│  │   +       │  │  Object   │  │  Cache    │  │Distributed│       │
│  │TimescaleDB│  │  Storage  │  │  & Pub/Sub│  │  Storage  │       │
│  │           │  │           │  │           │  │           │       │
│  │ • Metadata│  │ • Video   │  │ • Sessions│  │ • Long-term│       │
│  │ • Users   │  │ • Snapshots│  │ • Frames  │  │ • Archival│       │
│  │ • Events  │  │ • S3 API  │  │ • Queues  │  │ • Replicated│      │
│  │ • Time-   │  │ • Tiered  │  │ • Real-time│  │ • Erasure │       │
│  │   series  │  │   storage │  │   state   │  │   coding  │       │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘       │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                          RTSP/ONVIF/MQTT
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Edge Layer                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    K3s Cluster (per site)                     │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐         │  │
│  │  │ Frigate │  │MediaMTX │  │  YOLO   │  │ EdgeX   │         │  │
│  │  │   VMS   │  │Streaming│  │Analytics│  │Foundry  │         │  │
│  │  │         │  │         │  │         │  │         │         │  │
│  │  │ • Local │  │ • RTSP  │  │ • GPU   │  │ • IoT   │         │  │
│  │  │   record│  │ • WebRTC│  │   accel │  │   hub   │         │  │
│  │  │ • Motion│  │ • HLS   │  │ • Edge  │  │ • Proto-│         │  │
│  │  │   detect│  │ • Proxy │  │   AI    │  │   cols  │         │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘         │  │
│  │                                                                │  │
│  │  Local Storage: NVMe SSD (7-14 days retention)                │  │
│  │  Network: 100+ Mbps internet, isolated camera VLAN            │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                          RTSP/ONVIF
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Device Layer                                   │
│    [IP Camera 1]  [IP Camera 2]  ...  [IP Camera N]                │
│    [IoT Sensor]   [Access Control]   [BMS]   [Fire Alarm]          │
│                                                                     │
│  Protocols: RTSP, ONVIF, MQTT, Modbus, BACnet, OPC UA             │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Architectural Decisions

| Decision | Rationale |
|----------|-----------|
| **Kubernetes** | Industry standard, self-healing, declarative, portable |
| **Microservices** | Independent scaling, technology flexibility, fault isolation |
| **Edge Computing** | Reduced bandwidth, lower latency, offline capability |
| **Event-Driven** | Loose coupling, async processing, scalability |
| **NATS over Kafka** | Lighter weight, lower latency, better for edge |
| **PostgreSQL** | ACID compliance, TimescaleDB for time-series, PostGIS for spatial |
| **MinIO** | S3 compatibility, enterprise features, Kubernetes-native |
| **Frigate** | Modern, AI-integrated, MQTT-native, active development |

---

## Component Architecture

### 1. Video Management System (VMS) Service

**Purpose**: Camera management, recording, playback

**Technology Stack**:
- Frigate (primary VMS)
- FFmpeg (video processing)
- MediaMTX (streaming server)
- OpenCV (video manipulation)

**Responsibilities**:
```
• Camera Discovery & Management
  - ONVIF device discovery
  - RTSP stream management
  - PTZ camera control
  - Camera configuration

• Recording & Storage
  - Motion-based recording
  - Continuous recording
  - Retention policy enforcement
  - Storage quota management

• Live Streaming
  - WebRTC low-latency streaming
  - HLS adaptive streaming
  - RTSP proxy
  - Multi-client streaming

• Playback & Export
  - Timeline-based playback
  - Event-based retrieval
  - Video export (MP4, AVI)
  - Snapshot generation
```

**API Endpoints**:
```
GET    /api/v1/cameras                  # List all cameras
POST   /api/v1/cameras                  # Add camera
GET    /api/v1/cameras/{id}             # Get camera details
PUT    /api/v1/cameras/{id}             # Update camera
DELETE /api/v1/cameras/{id}             # Remove camera
GET    /api/v1/cameras/{id}/stream      # Live stream URL
GET    /api/v1/cameras/{id}/snapshot    # Latest snapshot
POST   /api/v1/cameras/{id}/ptz         # PTZ control

GET    /api/v1/recordings               # List recordings
GET    /api/v1/recordings/{id}          # Get recording
GET    /api/v1/recordings/{id}/download # Download video
DELETE /api/v1/recordings/{id}          # Delete recording

GET    /api/v1/events                   # List events
GET    /api/v1/events/{id}              # Get event details
GET    /api/v1/events/{id}/video        # Event video clip
```

**Configuration**:
```yaml
cameras:
  front_door:
    ffmpeg:
      inputs:
        - path: rtsp://192.168.1.100:554/stream1
          roles: [detect, record]
    detect:
      enabled: true
      width: 1920
      height: 1080
      fps: 5
    record:
      enabled: true
      retain:
        days: 30
        mode: motion
    snapshots:
      enabled: true
      retain:
        days: 14
    objects:
      track:
        - person
        - car
        - truck
      filters:
        person:
          min_area: 5000
          max_area: 100000
          threshold: 0.7
```

**Resource Requirements**:
- CPU: 0.1-0.2 cores per camera (no analytics)
- CPU: 0.5-1.0 cores per camera (with motion detection)
- Memory: 100-200 MB per camera
- Storage: 2-5 GB/day per camera (motion-based, H.265)
- Network: 2-4 Mbps per camera (H.265, 1080p)

### 2. Analytics Service

**Purpose**: AI/ML video analytics

**Technology Stack**:
- YOLOv8 (object detection)
- CompreFace (face recognition)
- OpenALPR (license plates)
- TensorFlow/PyTorch (custom models)
- OpenVINO (inference optimization)

**Architecture**:
```
Analytics Coordinator
    ├─> Frame Acquisition (Redis queue)
    ├─> Model Router (determines which models to run)
    ├─> Inference Engines
    │   ├─> Object Detection (YOLO)
    │   ├─> Face Recognition (CompreFace)
    │   ├─> License Plate (ALPR)
    │   ├─> Custom Model 1
    │   └─> Custom Model N
    ├─> Result Aggregator
    └─> Event Publisher (NATS)
```

**Detection Pipeline**:
```python
1. Frame Acquisition
   - Subscribe to camera frame stream
   - Decode RTSP/MJPEG to numpy array
   - Resize/normalize for model input

2. Model Inference
   - GPU-accelerated processing
   - Batch processing when possible
   - Confidence filtering
   - Non-maximum suppression

3. Post-Processing
   - Bounding box refinement
   - Object tracking (assign IDs)
   - Zone filtering
   - Event correlation

4. Result Publishing
   - Publish to NATS (analytics.detections)
   - Store in PostgreSQL (structured)
   - Update Redis (real-time state)
   - Trigger webhooks
```

**Custom Module Interface**:
```python
from openvision.sdk import AnalyticsModule, Detection

class CustomDetector(AnalyticsModule):
    def initialize(self, config: dict) -> bool:
        """Load model, initialize resources"""
        self.model = load_model(config['model_path'])
        return True
    
    def process_frame(self, frame: np.ndarray, metadata: dict) -> List[Detection]:
        """Process single frame"""
        results = self.model(frame)
        detections = []
        
        for result in results:
            if result.confidence > self.threshold:
                detections.append(Detection(
                    class_name=result.class_name,
                    confidence=result.confidence,
                    bbox=result.bbox,
                    metadata=metadata
                ))
        
        return detections
    
    def cleanup(self):
        """Release resources"""
        del self.model
```

**Performance Targets**:
- Latency: <100ms per frame (GPU)
- Throughput: 30-60 FPS per GPU
- Accuracy: >90% mAP (COCO dataset)
- Concurrent cameras: 10-20 per GPU (1080p, 5 FPS)

### 3. Storage Service

**Purpose**: Video archive management, tiering, cleanup

**Technology Stack**:
- MinIO (hot/warm storage)
- Ceph (cold/archive storage)
- PostgreSQL (metadata)

**Storage Tiers**:
```
Tier 1 (Hot):    0-7 days      NVMe SSD      Full quality      Fast retrieval
Tier 2 (Warm):   7-30 days     HDD           High quality      Normal retrieval
Tier 3 (Cold):   30-365 days   Object        Compressed        Slow retrieval
Tier 4 (Archive): 365+ days    Glacier/Tape  Events only       Manual retrieval
```

**Automatic Tiering**:
```python
# Cron job runs hourly
def tier_videos():
    now = datetime.now()
    
    # Tier 1 → Tier 2 (7 days old)
    videos = get_videos(age_days=7, tier='hot')
    for video in videos:
        move_to_warm_storage(video)
        update_metadata(video, tier='warm')
    
    # Tier 2 → Tier 3 (30 days old)
    videos = get_videos(age_days=30, tier='warm')
    for video in videos:
        compress_and_move(video, tier='cold')
        update_metadata(video, tier='cold')
    
    # Tier 3 → Tier 4 (365 days old)
    videos = get_videos(age_days=365, tier='cold')
    for video in videos:
        archive_or_delete(video, policy='retain_events')
```

**Retention Policies**:
```yaml
retention:
  default:
    continuous: 7 days
    motion_events: 30 days
    analytics_events: 90 days
  
  critical_cameras:
    continuous: 30 days
    all_events: 180 days
  
  compliance:
    all_footage: 365 days
    immutable: true
```

**Deduplication**:
- Scene change detection (avoid storing static frames)
- Cross-camera deduplication (same scene, multiple views)
- Event-based selective retention

### 4. Integration Service

**Purpose**: External system integration

**Technology Stack**:
- Node-RED (visual workflows)
- Apache Camel (enterprise integration)
- Protocol adapters (Modbus, BACnet, OPC UA)

**Supported Protocols**:
```
• MQTT - Native via Mosquitto
• ONVIF - Camera discovery/control
• Modbus TCP/RTU - Industrial sensors
• BACnet - Building automation
• OPC UA - Industrial systems
• HTTP/REST - Web APIs
• WebSocket - Real-time feeds
• SNMP - Network devices
• Serial - Legacy systems
```

**Integration Patterns**:
```
1. Publish-Subscribe
   Camera event → MQTT topic → External subscriber

2. Request-Reply
   External system → REST API → Response

3. Event-Driven
   Detection → Webhook → External action

4. Bidirectional
   Access card swipe → Correlation → Camera lookup

5. Scheduled
   Daily reports → External BI system
```

**Example: Tailgating Detection**:
```javascript
// Node-RED flow
[Access Control] → [Parse Badge Swipe]
                         ↓
    [Camera Analytics] → [Correlate Events]
                         ↓
                   [Check Count Mismatch]
                         ↓
                    [Alert Security]
```

### 5. Event Service

**Purpose**: Complex event processing, alerting

**Technology Stack**:
- NATS JetStream (event streaming)
- Apache Flink (stream processing, optional)

**Event Types**:
```
System Events:
  - camera.online
  - camera.offline
  - storage.low_space
  - system.error

Detection Events:
  - detection.person
  - detection.vehicle
  - detection.face_recognized
  - detection.license_plate

Security Events:
  - security.intrusion
  - security.tailgating
  - security.loitering
  - security.perimeter_breach

User Events:
  - user.login
  - user.view_camera
  - user.export_video
  - user.configuration_change
```

**Complex Event Processing**:
```sql
-- CEP Example: Detect person in restricted area for >5 minutes
SELECT camera_id, object_id, first_seen, last_seen
FROM detections
WHERE zone = 'restricted'
  AND class = 'person'
  AND TIMESTAMPDIFF(last_seen, first_seen) > 300
GROUP BY camera_id, object_id
HAVING COUNT(*) > 10
```

**Alert Rules Engine**:
```yaml
rules:
  - name: "After Hours Intrusion"
    condition: |
      event.type == "detection.person" AND
      event.zone == "restricted" AND
      time.hour() BETWEEN 22 AND 6
    actions:
      - type: webhook
        url: "https://security.company.com/alerts"
      - type: email
        to: "security@company.com"
      - type: camera
        action: "start_recording_high_res"
```

### 6. Digital Twin Service

**Purpose**: Real-time facility visualization

**Technology Stack**:
- Eclipse Ditto (digital twin framework)
- PostGIS (spatial queries)
- Three.js (3D rendering)

**Data Model**:
```json
{
  "thingId": "camera:lobby_cam_01",
  "policyId": "camera:default_policy",
  "attributes": {
    "location": {
      "latitude": 45.4215,
      "longitude": -75.6972,
      "elevation": 10.5,
      "building": "HQ",
      "floor": 1,
      "zone": "lobby"
    },
    "specs": {
      "model": "Hikvision DS-2CD2387G2",
      "resolution": "4K",
      "focal_length": "2.8mm",
      "field_of_view": 110,
      "orientation": {
        "pan": 45,
        "tilt": -15,
        "roll": 0
      }
    }
  },
  "features": {
    "stream": {
      "properties": {
        "status": "online",
        "url": "rtsp://192.168.1.100/stream1",
        "fps": 20,
        "bitrate": 4096,
        "resolution": "3840x2160"
      }
    },
    "health": {
      "properties": {
        "uptime_seconds": 86400,
        "temperature_celsius": 45,
        "frame_drops": 0,
        "errors_last_hour": 0
      }
    },
    "coverage": {
      "properties": {
        "area_covered_m2": 150,
        "blind_spots": [],
        "overlapping_cameras": ["lobby_cam_02"]
      }
    }
  }
}
```

**Spatial Queries**:
```sql
-- Find cameras covering a specific location
SELECT thing_id, 
       ST_Distance(location, ST_MakePoint(-75.6972, 45.4215)) as distance
FROM camera_twins
WHERE ST_DWithin(
    location,
    ST_MakePoint(-75.6972, 45.4215)::geography,
    50  -- 50 meter radius
)
ORDER BY distance;

-- Find coverage gaps
SELECT zone_id,
       zone_area_m2,
       COUNT(camera_id) as camera_count,
       SUM(coverage_area_m2) as covered_area_m2,
       (zone_area_m2 - SUM(coverage_area_m2)) as uncovered_area_m2
FROM zones
LEFT JOIN camera_coverage ON ST_Intersects(zone.geom, coverage.geom)
GROUP BY zone_id
HAVING COUNT(camera_id) < 2 OR uncovered_area_m2 > 20;
```

**Use Cases**:
1. **Coverage Analysis**: Identify blind spots before deployment
2. **Incident Response**: Click on map → see all nearby cameras
3. **Predictive Maintenance**: Track device health over time
4. **Capacity Planning**: Simulate adding cameras
5. **Simulation**: "What if camera 5 fails?"

---

## Data Architecture

### Database Schema (PostgreSQL)

**Core Tables**:
```sql
-- Users and authentication
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    tenant_id UUID REFERENCES tenants(id),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tenants (multi-tenancy)
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) UNIQUE,
    max_cameras INTEGER DEFAULT 50,
    max_storage_gb INTEGER DEFAULT 1000,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Cameras
CREATE TABLE cameras (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id),
    name VARCHAR(255) NOT NULL,
    rtsp_url TEXT NOT NULL,
    location_lat DECIMAL(10, 8),
    location_lon DECIMAL(11, 8),
    status VARCHAR(50) DEFAULT 'offline',
    config JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Recordings
CREATE TABLE recordings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    camera_id UUID REFERENCES cameras(id),
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ NOT NULL,
    file_path TEXT NOT NULL,
    file_size_bytes BIGINT,
    storage_tier VARCHAR(50) DEFAULT 'hot',
    has_motion BOOLEAN DEFAULT false,
    has_objects BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Time-series events (TimescaleDB hypertable)
CREATE TABLE events (
    time TIMESTAMPTZ NOT NULL,
    camera_id UUID REFERENCES cameras(id),
    event_type VARCHAR(100) NOT NULL,
    object_class VARCHAR(50),
    confidence REAL,
    bbox JSONB,
    metadata JSONB
);

SELECT create_hypertable('events', 'time');

-- Analytics results
CREATE TABLE detections (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    camera_id UUID REFERENCES cameras(id),
    object_class VARCHAR(50) NOT NULL,
    confidence REAL NOT NULL,
    bbox_x1 INTEGER,
    bbox_y1 INTEGER,
    bbox_x2 INTEGER,
    bbox_y2 INTEGER,
    tracking_id VARCHAR(100),
    metadata JSONB
);

CREATE INDEX ON detections (camera_id, timestamp DESC);
CREATE INDEX ON detections (object_class, timestamp DESC);
```

**Indexes**:
```sql
-- Performance indexes
CREATE INDEX idx_cameras_tenant ON cameras(tenant_id);
CREATE INDEX idx_recordings_camera_time ON recordings(camera_id, start_time DESC);
CREATE INDEX idx_events_camera_time ON events(camera_id, time DESC);
CREATE INDEX idx_events_type_time ON events(event_type, time DESC);

-- Spatial index
CREATE INDEX idx_cameras_location ON cameras USING GIST(
    ll_to_earth(location_lat, location_lon)
);
```

### Object Storage Structure (MinIO/S3)

**Bucket Organization**:
```
openvision-recordings/
├── tenant_001/
│   ├── camera_001/
│   │   ├── 2024/
│   │   │   ├── 11/
│   │   │   │   ├── 19/
│   │   │   │   │   ├── 00-00-00_to_01-00-00.mp4
│   │   │   │   │   ├── 01-00-00_to_02-00-00.mp4
│   │   │   │   │   └── ...
│   │   │   │   └── ...
│   │   │   └── ...
│   │   └── snapshots/
│   │       └── 2024-11-19_14-30-15.jpg
│   └── camera_002/
│       └── ...
└── tenant_002/
    └── ...

openvision-analytics/
├── tenant_001/
│   ├── camera_001/
│   │   └── 2024-11-19/
│   │       ├── detections_00.json
│   │       └── ...
│   └── ...
└── ...
```

**Metadata Tags**:
```
- tenant-id: UUID
- camera-id: UUID
- timestamp: ISO8601
- duration: seconds
- has-motion: boolean
- has-objects: boolean
- storage-tier: hot|warm|cold
- codec: h264|h265
- resolution: 1920x1080
```

### Cache Strategy (Redis)

**Cache Types**:
```
1. Session Cache
   Key: session:{token}
   TTL: 24 hours
   Value: user_id, tenant_id, permissions

2. Frame Buffer
   Key: frame:{camera_id}:{timestamp}
   TTL: 60 seconds
   Value: JPEG binary

3. Real-time State
   Key: camera:{camera_id}:status
   TTL: None (persistent)
   Value: online|offline|error

4. Analytics Queue
   Key: analytics:queue:{camera_id}
   Type: List (FIFO)
   Value: Frame metadata

5. Rate Limiting
   Key: ratelimit:{user_id}:{endpoint}
   TTL: 60 seconds
   Value: request count
```

---

## Security Architecture

### Defense in Depth

**Layer 1: Network Security**
```
• VLANs
  - Camera network (isolated)
  - Management network
  - User access network

• Firewalls
  - Deny all by default
  - Explicit allow rules
  - Geo-blocking (optional)

• VPN Access
  - WireGuard or IPSec
  - Certificate-based auth
  - Limited IP ranges

• DDoS Protection
  - Rate limiting
  - Connection limits
  - Cloudflare/WAF
```

**Layer 2: Application Security**
```
• Authentication
  - JWT tokens (short-lived)
  - Refresh tokens (longer-lived)
  - OAuth2/OIDC (Keycloak)
  - MFA support

• Authorization
  - RBAC (role-based)
  - ABAC (attribute-based, optional)
  - Resource-level permissions
  - Tenant isolation

• API Security
  - Rate limiting (per user/IP)
  - Input validation
  - SQL injection prevention
  - XSS protection

• Session Management
  - Secure cookies (httpOnly, secure)
  - CSRF tokens
  - Session timeout
  - Concurrent session limits
```

**Layer 3: Data Security**
```
• Encryption at Rest
  - Database: PostgreSQL encryption
  - Object storage: MinIO encryption
  - File system: LUKS/dm-crypt

• Encryption in Transit
  - TLS 1.3 (client ↔ API)
  - mTLS (service ↔ service)
  - RTSP over TLS (cameras)

• Secrets Management
  - Kubernetes secrets (sealed-secrets)
  - HashiCorp Vault (optional)
  - No secrets in code/config

• Data Sanitization
  - Video redaction API
  - GDPR right to deletion
  - Secure deletion (shred)
```

**Layer 4: Runtime Security**
```
• Container Security
  - Non-root users
  - Read-only filesystems
  - No privileged containers
  - Resource limits

• Runtime Monitoring
  - Falco (anomaly detection)
  - Syscall monitoring
  - Network traffic analysis

• Vulnerability Scanning
  - Trivy (image scanning)
  - OWASP Dependency Check
  - Regular updates

• Audit Logging
  - All API calls logged
  - Video access logged
  - Config changes logged
  - Immutable logs
```

### Zero Trust Architecture

**Service-to-Service Authentication**:
```
Every request between services must:
1. Present valid JWT or certificate
2. Have explicit permission (OPA policy)
3. Use encrypted channel (mTLS)
4. Be logged and audited
```

**SPIFFE/SPIRE** (optional):
```
• Automatic service identity
• Certificate rotation
• Zero-trust networking
• Policy enforcement
```

**Open Policy Agent (OPA)**:
```rego
# Example policy
package authz

default allow = false

allow {
    input.method == "GET"
    input.path = ["api", "v1", "cameras", camera_id]
    camera_belongs_to_user(input.user, camera_id)
}

allow {
    input.method == "POST"
    input.path = ["api", "v1", recordings"]
    has_role(input.user, "operator")
}

camera_belongs_to_user(user, camera_id) {
    user.tenant_id == data.cameras[camera_id].tenant_id
}
```

### Compliance

**GDPR**:
```
• Right to Access: API for data export
• Right to Deletion: Secure video deletion
• Data Portability: Standard formats
• Consent Management: Opt-in tracking
• Data Minimization: Retention policies
• Privacy by Design: Defaults to minimal
```

**SOC 2**:
```
• Access Controls: RBAC, MFA
• Encryption: At rest and in transit
• Audit Logs: Immutable, tamper-evident
• Monitoring: 24/7 alerting
• Incident Response: Documented procedures
• Backup/Recovery: Regular testing
```

**ISO 27001**:
```
• Information Security Policy
• Risk Assessment Process
• Asset Management
• Access Control
• Cryptography
• Physical Security
• Operational Security
```

---

## Deployment Architecture

### Deployment Topologies

**1. Single-Site SMB**
```
┌───────────────────────────────────────┐
│     Single Server or Cloud Instance   │
│  ┌─────────────────────────────────┐  │
│  │  Docker Compose / K3s           │  │
│  │  ├─ Frigate (VMS)               │  │
│  │  ├─ MediaMTX (Streaming)        │  │
│  │  ├─ YOLO (Analytics)            │  │
│  │  ├─ PostgreSQL                  │  │
│  │  ├─ MinIO (Storage)             │  │
│  │  ├─ NATS (Messaging)            │  │
│  │  └─ Grafana (Monitoring)        │  │
│  └─────────────────────────────────┘  │
│                                        │
│  Cameras: 10-50                        │
│  Storage: 4TB local                    │
│  Hardware: Server or cloud VM          │
└───────────────────────────────────────┘
```

**2. Multi-Site Enterprise**
```
┌─────────── Site 1 ──────────┐  ┌─────────── Site 2 ──────────┐
│  Edge K3s Cluster (2 nodes) │  │  Edge K3s Cluster (2 nodes) │
│  ├─ Frigate                 │  │  ├─ Frigate                 │
│  ├─ Local Analytics         │  │  ├─ Local Analytics         │
│  ├─ 4TB Local Storage       │  │  ├─ 4TB Local Storage       │
│  └─ 25 cameras              │  │  └─ 25 cameras              │
└─────────────────────────────┘  └─────────────────────────────┘
         ↓                                   ↓
         └─────────────────┬─────────────────┘
                           ↓
         ┌─────────────────────────────────────┐
         │     Central Cloud (Kubernetes)      │
         │  ┌───────────────────────────────┐  │
         │  │  Control Plane (3 nodes)      │  │
         │  │  ├─ API Gateway               │  │
         │  │  ├─ User Management           │  │
         │  │  ├─ Cross-site Analytics      │  │
         │  │  └─ Digital Twin              │  │
         │  └───────────────────────────────┘  │
         │  ┌───────────────────────────────┐  │
         │  │  Data Layer                   │  │
         │  │  ├─ PostgreSQL HA (3 nodes)   │  │
         │  │  ├─ Ceph (6 nodes, 200TB)     │  │
         │  │  └─ Redis Cluster             │  │
         │  └───────────────────────────────┘  │
         └─────────────────────────────────────┘
```

**3. SaaS Multi-Tenant**
```
┌─────────────────────────────────────────────┐
│      Regional Cloud (US-East)               │
│  ┌───────────────────────────────────────┐  │
│  │  Kubernetes Cluster (100+ nodes)      │  │
│  │                                        │  │
│  │  ┌──────────────────────────────────┐ │  │
│  │  │  Tenant 1 (Namespace isolation)  │ │  │
│  │  │  ├─ VMS pods                     │ │  │
│  │  │  ├─ Analytics pods               │ │  │
│  │  │  └─ Storage quota: 1TB           │ │  │
│  │  └──────────────────────────────────┘ │  │
│  │                                        │  │
│  │  ┌──────────────────────────────────┐ │  │
│  │  │  Tenant 2                        │ │  │
│  │  └──────────────────────────────────┘ │  │
│  │  ...                                   │  │
│  │  ┌──────────────────────────────────┐ │  │
│  │  │  Tenant N                        │ │  │
│  │  └──────────────────────────────────┘ │  │
│  │                                        │  │
│  │  ┌──────────────────────────────────┐ │  │
│  │  │  Shared Services                 │ │  │
│  │  │  ├─ Keycloak (Multi-tenant)      │ │  │
│  │  │  ├─ API Gateway                  │ │  │
│  │  │  ├─ Monitoring                   │ │  │
│  │  │  └─ Billing                      │ │  │
│  │  └──────────────────────────────────┘ │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
                       ↕
┌─────────────────────────────────────────────┐
│      Regional Cloud (EU-West)               │
│  (Same structure, geo-replicated data)      │
└─────────────────────────────────────────────┘
```

### High Availability Design

**Control Plane HA** (3 nodes):
```
- Load balanced API endpoints
- etcd quorum (3-node cluster)
- Leader election for controllers
- Automatic failover (<30s)
```

**Data Layer HA**:
```
PostgreSQL:
  - Streaming replication (sync)
  - Automatic failover (pg_auto_failover)
  - Read replicas for scaling
  - Point-in-time recovery

Ceph:
  - 3x replication (default)
  - Self-healing on node failure
  - Distributed architecture
  - No single point of failure

Redis:
  - Redis Cluster (6 nodes min)
  - Hash slot distribution
  - Automatic failover
  - Persistence (AOF + RDB)
```

**Application HA**:
```
- Multiple pod replicas (2-5+)
- Pod anti-affinity (spread across nodes)
- Health checks (liveness, readiness)
- Graceful shutdown (SIGTERM handling)
- Circuit breakers (prevent cascading failures)
```

**Network HA**:
```
- Redundant network paths
- Multiple internet uplinks
- BGP routing (enterprise)
- DNS failover
- Load balancer HA pairs
```

---

## Scalability and Performance

### Horizontal Scaling

**Stateless Services** (unlimited scaling):
```
- API Gateway: Add more pods
- VMS Service: Shard by camera
- Analytics Service: GPU-per-pod, scale pods
- Integration Service: Scale workers
- Web UI: Scale behind CDN
```

**Stateful Services** (coordinated scaling):
```
- PostgreSQL: Read replicas + sharding
- Redis: Redis Cluster (add shards)
- Ceph: Add storage nodes
- NATS: Add server nodes to cluster
```

### Vertical Scaling

**CPU-Intensive**:
```
- Analytics: Larger GPU (T4 → A10 → A100)
- Video encoding: More CPU cores
- FFmpeg: Hardware encoding (NVENC, QSV)
```

**Memory-Intensive**:
```
- Frame buffers: More RAM
- Model caching: Larger memory
- PostgreSQL: Increase shared_buffers
```

**Storage-Intensive**:
```
- Video archives: Add drives to Ceph
- Hot storage: Larger/faster SSDs
- Database: Increase storage IOPS
```

### Performance Optimization

**Video Processing**:
```
• Hardware Encoding
  - NVIDIA NVENC (H.264/H.265)
  - Intel Quick Sync
  - Reduces CPU by 80%+

• Resolution Scaling
  - Record full resolution
  - Detect on downscaled (640x360)
  - Saves 10x compute

• Frame Skipping
  - Process every Nth frame
  - 5 FPS instead of 30 FPS
  - Still effective for analytics

• Codec Selection
  - H.265 (HEVC): 50% smaller than H.264
  - Hardware decoding essential
```

**Database Optimization**:
```
• Indexing
  - Covering indexes for common queries
  - Partial indexes for filtered data
  - Index maintenance (REINDEX)

• Partitioning
  - Time-based partitions (daily/weekly)
  - Automatic partition creation
  - Old partition archival

• Connection Pooling
  - PgBouncer (transaction pooling)
  - Limits: 10-50 connections per pod
  - Reduces connection overhead

• Query Optimization
  - Prepared statements
  - Batch operations
  - Avoid N+1 queries
```

**Caching Strategy**:
```
• Redis Cache
  - Hot data: User sessions, camera status
  - TTL: 60s-24h based on volatility
  - Invalidation: On write operations

• CDN Caching
  - Static assets: Web UI, images
  - Video snapshots: 5-minute TTL
  - API responses: Selected endpoints

• Application Cache
  - In-memory: Configuration, models
  - Local disk: Downloaded models
  - Shared: Redis for distributed cache
```

### Performance Targets

**Latency**:
```
- Live streaming: <500ms (glass-to-glass)
- API response: <100ms (p95)
- Analytics results: <2s from detection
- Search query: <500ms
- Playback start: <1s
```

**Throughput**:
```
- Video ingestion: 1000+ cameras per cluster
- Analytics: 500+ concurrent streams
- API requests: 5,000 req/sec
- Events: 10,000 events/sec
- Database writes: 100,000 rows/sec (TimescaleDB)
```

**Resource Usage** (per camera):
```
- CPU: 0.1-0.5 cores (depends on analytics)
- Memory: 100-300 MB
- Storage: 2-10 GB/day (motion, H.265)
- Network: 2-4 Mbps (H.265, 1080p)
- GPU: 0.05-0.1 TOPS (YOLO inference)
```

---

## Technology Stack

### Complete Technology Listing

**Video Management**:
```
- Frigate: Primary VMS
- FFmpeg: Video processing
- MediaMTX: Streaming server
- OpenCV: Computer vision operations
```

**AI/ML**:
```
- YOLOv8 (Ultralytics): Object detection
- CompreFace: Face recognition
- OpenALPR: License plate recognition
- TensorFlow: Custom model training
- PyTorch: Alternative ML framework
- OpenVINO: Inference optimization (Intel)
- TensorRT: Inference optimization (NVIDIA)
```

**Databases**:
```
- PostgreSQL 15: Primary database
- TimescaleDB: Time-series extension
- PostGIS: Spatial queries
- Redis 7: Cache and pub/sub
- MongoDB: Digital twin (Ditto backend)
```

**Storage**:
```
- MinIO: S3-compatible object storage
- Ceph: Distributed block/object storage
- Local: NVMe SSD for hot data
```

**Messaging**:
```
- NATS JetStream: Internal events
- Eclipse Mosquitto: MQTT broker
- Apache Kafka: Alternative (optional)
```

**Orchestration**:
```
- Kubernetes: Container orchestration
- K3s: Lightweight Kubernetes (edge)
- Docker: Container runtime
- Helm: Package manager
- ArgoCD: GitOps deployment (optional)
```

**Edge Computing**:
```
- EdgeX Foundry: IoT edge framework
- KubeEdge: Kubernetes edge extension
```

**Integration**:
```
- Node-RED: Visual workflow automation
- Apache NiFi: Data flow (optional)
- Apache Camel: Enterprise integration (optional)
```

**API & Gateway**:
```
- Apache APISIX: API gateway
- Traefik: Reverse proxy (alternative)
- Kong: API gateway (alternative)
```

**Security**:
```
- Keycloak: Identity & access management
- OAuth2/OIDC: Authentication protocols
- Falco: Runtime security monitoring
- OPA: Policy engine
- Trivy: Vulnerability scanning
- SPIFFE/SPIRE: Service identity (optional)
```

**Observability**:
```
- Grafana: Dashboards & visualization
- Prometheus: Metrics collection
- Grafana Loki: Log aggregation
- Jaeger: Distributed tracing
- OpenTelemetry: Telemetry standard
- Netdata: Real-time monitoring
```

**Digital Twin**:
```
- Eclipse Ditto: Digital twin framework
- PostGIS: Spatial database
- Three.js: 3D visualization
```

**Development**:
```
- Python 3.11: Primary language (analytics)
- Go: System services
- Node.js: Web services
- React: Web UI
- React Native: Mobile apps
```

**CI/CD**:
```
- GitLab CI or GitHub Actions
- Docker Registry: Image storage
- Helm: Chart repository
- ArgoCD: GitOps (optional)
```

---

## Development and Operations

### Development Workflow

**Local Development**:
```bash
# Prerequisites
- Docker Desktop
- kubectl
- Helm
- Python 3.11
- Node.js 18+

# Start local stack
docker-compose -f docker-compose.dev.yml up -d

# Develop custom module
cd modules/my-detector
python develop.py  # Hot reload
```

**Testing**:
```
Unit Tests:
  - pytest (Python)
  - Jest (JavaScript)
  - Coverage target: >80%

Integration Tests:
  - Docker Compose
  - Testcontainers
  - Real service interactions

E2E Tests:
  - Playwright/Cypress
  - Test against full stack
  - Camera simulators

Performance Tests:
  - k6 load testing
  - Locust (alternative)
  - Benchmark targets
```

**CI/CD Pipeline**:
```
1. Code Push
   ├─> Lint & Format Check
   ├─> Unit Tests
   ├─> Build Docker Images
   └─> Security Scan (Trivy)

2. Pull Request
   ├─> Integration Tests
   ├─> Code Review
   └─> Preview Deployment

3. Merge to Main
   ├─> Tag Release
   ├─> Build Production Images
   ├─> Push to Registry
   └─> Deploy to Staging

4. Manual Approval
   └─> Deploy to Production
       ├─> Canary Deployment (10%)
       ├─> Monitor Metrics
       └─> Rollout (100%) or Rollback
```

### Operations Playbooks

**Monitoring Dashboards**:
```
System Health:
  - CPU, Memory, Disk, Network
  - Pod status and restarts
  - Database connections
  - Storage usage

Application Metrics:
  - Camera online/offline count
  - Recording rate (GB/hour)
  - Analytics queue depth
  - API latency (p50, p95, p99)
  - Error rates

Business Metrics:
  - Active users
  - Video hours recorded
  - Detections per day
  - Storage costs
```

**Alert Rules**:
```
Critical (PagerDuty):
  - API unavailable
  - Database down
  - Storage >95% full
  - Camera cluster offline

Warning (Email):
  - High error rate (>1%)
  - Slow API response (>500ms p95)
  - Storage >80% full
  - Multiple cameras offline

Info (Slack):
  - Deployment completed
  - Certificate expiring (30 days)
  - Unusual traffic pattern
```

**Backup Procedures**:
```
Daily:
  - PostgreSQL dump (pg_dump)
  - Configuration backups
  - Retain: 30 days

Weekly:
  - Full system backup
  - Test restore procedure
  - Retain: 12 weeks

Monthly:
  - Archive to glacier
  - Retain: 1 year
```

**Disaster Recovery**:
```
RTO: 4 hours (Recovery Time Objective)
RPO: 1 hour (Recovery Point Objective)

Failure Scenarios:
  1. Single node failure → Automatic (K8s self-healing)
  2. Database failure → Failover to replica (<5 min)
  3. Storage node failure → Ceph self-healing (<30 min)
  4. Entire datacenter → Failover to DR site (2-4 hours)
```

**Upgrade Procedures**:
```
1. Pre-Upgrade
   - Review release notes
   - Backup all data
   - Test in staging
   - Schedule maintenance window

2. Upgrade
   - Kubernetes: Rolling update (node by node)
   - Applications: Canary deployment
   - Databases: Blue-green or in-place
   - Monitor metrics continuously

3. Post-Upgrade
   - Verify all services healthy
   - Run smoke tests
   - Monitor for 24 hours
   - Document any issues

4. Rollback Plan
   - Keep previous images tagged
   - Database migration rollback scripts
   - Automated rollback on critical errors
```

---

## Appendix: Technical Specifications

### Hardware Requirements

**Control Plane Nodes** (3x for HA):
```
CPU: 8 cores @ 2.5+ GHz
RAM: 32 GB
Storage: 500 GB SSD
Network: 10 Gbps
```

**Worker Nodes** (5+ nodes):
```
CPU: 16 cores @ 2.5+ GHz
RAM: 64 GB
Storage: 1 TB NVMe SSD
GPU: Optional (NVIDIA T4/A10 for ML)
Network: 10 Gbps
```

**Ceph Storage Nodes** (6+ nodes):
```
CPU: 8 cores per node
RAM: 64 GB per node (8 GB per OSD)
Storage: 12x 18TB HDDs per node
NVMe: 2x 1TB for metadata/cache
Network: 25 Gbps (separate storage network)
```

**Edge Nodes** (per site):
```
Option A: Orange Pi 5 Plus
  - CPU: Rockchip RK3588 (8-core, 2.4 GHz)
  - RAM: 16 GB
  - Storage: 2 TB NVMe
  - AI: Hailo-8 (26 TOPS)
  - Cost: ~$220 per node

Option B: NVIDIA Jetson Orin Nano
  - CPU: ARM Cortex-A78AE (6-core)
  - GPU: 1024-core Ampere
  - RAM: 8 GB
  - AI: 40 TOPS
  - Cost: ~$500 per node

Option C: NVIDIA Jetson Orin NX
  - CPU: ARM Cortex-A78AE (8-core)
  - GPU: 1024-core Ampere
  - RAM: 16 GB
  - AI: 100 TOPS
  - Cost: ~$800 per node
```

### Network Requirements

**Bandwidth**:
```
Per Camera: 2-4 Mbps (H.265, 1080p)
10 Cameras: 20-40 Mbps
100 Cameras: 200-400 Mbps
1000 Cameras: 2-4 Gbps

Edge to Cloud (metadata only): 10-50 Mbps
```

**Latency**:
```
Camera to Edge: <10ms
Edge to Cloud: <100ms
User to API: <50ms (same region)
```

**Protocols**:
```
RTSP: TCP 554
ONVIF: TCP 80/443
MQTT: TCP 1883 (or 8883 for TLS)
HTTP/HTTPS: TCP 80/443
WebRTC: UDP 50000-60000
```

### Software Versions

**Core Components**:
```
Kubernetes: 1.28+
K3s: 1.28+
Docker: 24.0+
PostgreSQL: 15+
TimescaleDB: 2.13+
Redis: 7.2+
MinIO: RELEASE.2024+
```

**Application Services**:
```
Frigate: 0.13+
YOLOv8: 8.0+
CompreFace: 1.2+
Grafana: 10.0+
Prometheus: 2.47+
NATS: 2.10+
Mosquitto: 2.0+
Keycloak: 23.0+
```

### API Versioning

**Current Version**: v1  
**Deprecation Policy**: 12 months notice  
**Breaking Changes**: New major version only  

**Version Format**: `/api/v{major}/{resource}`  
**Example**: `GET /api/v1/cameras`

---

**Document Version**: 1.0  
**Last Updated**: November 2024  
**Maintained By**: Technical Architecture Team  
**Next Review**: Q1 2025

---

## Quick Reference

**GitHub**: https://github.com/openvision-platform  
**Documentation**: https://docs.openvision.io  
**Community**: https://community.openvision.io  
**Discord**: https://discord.gg/openvision  
**Commercial Support**: support@openvision.io
