---
source_project: Open Vision
source_project_uuid: 019adc89-3095-77fb-a6f8-3f599d84699a
doc_uuid: 7da88c7c-eaac-41a8-a694-49eee18323a4
original_filename: 03-Technical-Architecture.md
created_at: 2025-12-02T00:49:42.947249+00:00
content_hash: f59e17b4196c
status: duplicate
duplicate_of: "knowledge-base/d-central/security/IHOSE/03-Technical-Architecture-md.md"
duplicate_reason: exact content_hash match, different category (same doc uploaded to multiple Claude Projects)
---

# OpenVision Platform
## Technical Architecture Overview

**Version:** 1.0  
**Audience:** CTO, Solution Architects, Technical Leaders  
**Classification:** Technical Specification

---

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture Principles](#architecture-principles)
3. [Technology Stack](#technology-stack)
4. [Component Architecture](#component-architecture)
5. [Data Architecture](#data-architecture)
6. [Security Architecture](#security-architecture)
7. [Scalability & Performance](#scalability--performance)
8. [Integration Architecture](#integration-architecture)

---

## System Overview

### High-Level Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │   Web UI     │  │  Mobile App  │  │  3rd Party   │            │
│  │   (React)    │  │ (React Native)│  │   Clients    │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
└────────────────────────────────────────────────────────────────────┘
                              ▲
                              │ HTTPS / WSS
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                       API GATEWAY LAYER                            │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │         Apache APISIX (Kong Alternative)                      │ │
│  │  • Authentication (JWT/OAuth2) • Rate Limiting                │ │
│  │  • Service Routing            • API Versioning                │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
                              ▲
                              │ gRPC / REST
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                    APPLICATION SERVICES LAYER                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │   VMS    │  │Analytics │  │Integration│ │  User    │         │
│  │ Service  │  │ Service  │  │ Service  │  │ Mgmt     │         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Storage  │  │  Event   │  │ Workflow │  │ Digital  │         │
│  │ Service  │  │ Service  │  │ Service  │  │  Twin    │         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
└────────────────────────────────────────────────────────────────────┘
                              ▲
                              │ Event Bus
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                     MESSAGE BROKER LAYER                           │
│  ┌────────────────────────┐  ┌────────────────────────┐          │
│  │  NATS JetStream        │  │  Eclipse Mosquitto     │          │
│  │  • Internal events     │  │  • IoT/MQTT devices    │          │
│  │  • Service mesh        │  │  • Sensors/actuators   │          │
│  └────────────────────────┘  └────────────────────────┘          │
└────────────────────────────────────────────────────────────────────┘
                              ▲
                              │
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │PostgreSQL│  │  MinIO   │  │  Redis   │  │   Ceph   │         │
│  │+TimescaleDB │ Object   │  │  Cache   │  │Distributed         │
│  │ Metadata │  │ Storage  │  │          │  │  Storage │         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
└────────────────────────────────────────────────────────────────────┘
                              ▲
                              │ RTSP / ONVIF / MQTT
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                         EDGE LAYER (K3s)                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Frigate  │  │ MediaMTX │  │   YOLO   │  │  EdgeX   │         │
│  │   VMS    │  │Streaming │  │Analytics │  │ Foundry  │         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
└────────────────────────────────────────────────────────────────────┘
                              ▲
                              │ RTSP / ONVIF
                              ▼
┌────────────────────────────────────────────────────────────────────┐
│                         DEVICE LAYER                               │
│  [IP Camera 1]  [IP Camera 2]  ...  [IP Camera N]                │
│  [IoT Sensor 1] [Access Control] [HVAC] [Fire Alarm]             │
└────────────────────────────────────────────────────────────────────┘
```

### Key Characteristics

- **Microservices Architecture** - Independently deployable services
- **Event-Driven** - Asynchronous communication via message brokers
- **Edge-First** - Intelligence at the edge, reduce cloud dependency
- **Cloud-Native** - Kubernetes orchestration, containerized services
- **API-First** - Everything accessible via REST/gRPC APIs
- **Open Standards** - ONVIF, MQTT, RTSP, OpenAPI

---

## Architecture Principles

### 1. Separation of Concerns
Each service has a single, well-defined responsibility:
- VMS Service → Camera management, recording
- Analytics Service → AI/ML processing
- Storage Service → Data lifecycle management
- Event Service → Event processing and correlation

### 2. Loose Coupling
Services communicate via:
- **Synchronous:** REST/gRPC for request-response
- **Asynchronous:** NATS/MQTT for events
- **No direct dependencies** between services

### 3. High Cohesion
Related functionality grouped together:
- All video operations in VMS Service
- All analytics in Analytics Service
- All storage operations in Storage Service

### 4. Scalability by Design
- **Horizontal scaling:** Add more service instances
- **Vertical scaling:** Increase resource allocation
- **Edge distribution:** Process at source
- **Sharding:** Partition data by camera, site, or tenant

### 5. Resilience & Fault Tolerance
- **Service mesh:** Automatic retry, circuit breaker
- **Health checks:** Continuous monitoring
- **Graceful degradation:** System continues with reduced capability
- **Backup/DR:** Multi-region replication

### 6. Security by Default
- **Zero-trust:** Authenticate and authorize everything
- **Encryption:** TLS 1.3 for transport, AES-256 for storage
- **Least privilege:** Services have minimal permissions
- **Audit logging:** Comprehensive, immutable logs

---

## Technology Stack

### Core Platform

**Orchestration:**
- Kubernetes 1.28+ (Cloud/Central)
- K3s 1.28+ (Edge nodes)
- Helm 3.x (Package management)

**Container Runtime:**
- containerd (Kubernetes default)
- Docker (Development)

**Service Mesh (Optional):**
- Linkerd 2.x (lightweight) OR
- Istio (feature-rich)

### Video Management

**VMS Core:**
- Frigate 0.13+ (Primary VMS)
- Shinobi (Alternative for scale)
- FFmpeg 6.0+ (Video processing)
- MediaMTX (RTSP/WebRTC server)

**Streaming:**
- WebRTC (Low-latency browser streaming)
- HLS (Adaptive bitrate streaming)
- RTSP (Device connectivity)

### AI & Analytics

**ML Frameworks:**
- YOLOv8 (Ultralytics) - Object detection
- TensorFlow 2.x - General ML
- PyTorch 2.x - Research/experimentation
- OpenCV 4.x - Computer vision

**Inference:**
- TensorFlow Serving
- TorchServe
- OpenVINO (Intel optimization)
- TensorRT (NVIDIA optimization)

**Models:**
- CompreFace (Face recognition)
- OpenALPR (License plates)
- Custom models (client-specific)

### Data Storage

**Structured Data:**
- PostgreSQL 15+ (Primary database)
- TimescaleDB 2.x (Time-series extension)
- PostGIS 3.x (Spatial extension)

**Object Storage:**
- MinIO (S3-compatible)
- Ceph RADOS (Distributed storage)

**Caching:**
- Redis 7.x (Cache, pub/sub, sessions)

**Search (Optional):**
- Elasticsearch 8.x (Log search)

### Messaging

**Event Streaming:**
- NATS JetStream (Internal events)
- Apache Kafka (High-throughput option)

**IoT Messaging:**
- Eclipse Mosquitto (MQTT broker)

**Queue (Optional):**
- RabbitMQ (Task queues)

### Security & Identity

**Authentication:**
- Keycloak 22+ (IdP, SSO)
- OAuth2/OIDC
- LDAP/Active Directory integration

**Secrets Management:**
- Sealed Secrets (Kubernetes)
- HashiCorp Vault (Enterprise)

**Runtime Security:**
- Falco (Container runtime security)
- OPA (Policy enforcement)

### Observability

**Metrics:**
- Prometheus (Collection)
- Grafana (Visualization)

**Logging:**
- Grafana Loki (Log aggregation)
- Promtail (Log collection)

**Tracing:**
- Jaeger (Distributed tracing)
- OpenTelemetry (Instrumentation)

**APM (Optional):**
- Elastic APM

### Integration & Workflow

**Workflow:**
- Node-RED (Visual programming)
- Apache NiFi (Dataflow)
- Temporal.io (Workflow orchestration)

**ETL/Integration:**
- Apache Camel (Enterprise integration)

**Digital Twin:**
- Eclipse Ditto (Device digital twins)

### Edge Computing

**Edge Framework:**
- EdgeX Foundry (IoT edge)
- KubeEdge (K8s edge extension)

**Edge AI:**
- Coral Edge TPU support
- Hailo-8 accelerator support
- NVIDIA Jetson (TX2, Nano, Orin)

### Development Tools

**API:**
- Apache APISIX (API Gateway)
- OpenAPI 3.0 (API specs)
- gRPC (High-performance RPC)

**Testing:**
- pytest (Python)
- Jest (JavaScript)
- k6 (Load testing)

**CI/CD:**
- GitHub Actions
- GitLab CI
- ArgoCD (GitOps)

---

## Component Architecture

### 1. VMS Service

**Technology:** Python + Frigate + FFmpeg

**Responsibilities:**
- Camera connection management (RTSP/ONVIF discovery)
- Video stream routing and transcoding
- Recording orchestration (motion/continuous)
- Snapshot generation
- Playback API

**Architecture:**
```
┌─────────────────────────────────────┐
│         VMS Service                 │
│  ┌─────────────────────────────┐   │
│  │  Camera Manager             │   │
│  │  • ONVIF discovery          │   │
│  │  • Connection pool          │   │
│  │  • Health monitoring        │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │  Recording Manager          │   │
│  │  • Motion detection         │   │
│  │  • Segment creation         │   │
│  │  • Storage coordination     │   │
│  └─────────────────────────────┘   │
│  ┌─────────────────────────────┐   │
│  │  Stream Router              │   │
│  │  • Multi-client support     │   │
│  │  • Format conversion        │   │
│  │  • Adaptive bitrate         │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
```

**APIs:**
- `GET /cameras` - List all cameras
- `GET /cameras/{id}/stream` - Get stream URL
- `POST /cameras/{id}/snapshot` - Capture snapshot
- `GET /recordings` - Query recordings
- `PUT /cameras/{id}/config` - Update configuration

**Data Model:**
```json
{
  "camera_id": "front_door_01",
  "name": "Front Entrance",
  "stream_url": "rtsp://192.168.1.100:554/stream1",
  "status": "online",
  "fps": 20,
  "resolution": "1920x1080",
  "codec": "h265",
  "record_mode": "motion",
  "retention_days": 30
}
```

### 2. Analytics Service

**Technology:** Python + TensorFlow/PyTorch + YOLO

**Architecture:**
```
┌──────────────────────────────────────┐
│      Analytics Coordinator           │
│  ┌────────────────────────────────┐  │
│  │   Frame Queue (Redis)          │  │
│  └────────────────────────────────┘  │
│            ↓          ↓         ↓    │
│  ┌────────┐  ┌────────┐  ┌────────┐ │
│  │ YOLO   │  │ Face   │  │ Custom │ │
│  │ Module │  │ Recog  │  │ Module │ │
│  └────────┘  └────────┘  └────────┘ │
│            ↓          ↓         ↓    │
│  ┌────────────────────────────────┐  │
│  │  Detection Aggregator          │  │
│  └────────────────────────────────┘  │
│            ↓                         │
│     NATS Event Stream                │
└──────────────────────────────────────┘
```

**Module Interface:**
```python
class AnalyticsModule:
    def initialize(self, config: dict) -> bool:
        """Load model, setup resources"""
        
    def process_frame(self, frame: np.ndarray, 
                     metadata: dict) -> List[Detection]:
        """Process single frame"""
        
    def cleanup(self):
        """Release resources"""
```

**Event Output:**
```json
{
  "timestamp": "2025-11-19T14:30:00Z",
  "camera_id": "front_door_01",
  "module": "yolo_v8",
  "detections": [
    {
      "class": "person",
      "confidence": 0.95,
      "bbox": {"x1": 100, "y1": 200, "x2": 300, "y2": 500},
      "tracking_id": "person_1234"
    }
  ]
}
```

### 3. Storage Service

**Technology:** Go + MinIO + PostgreSQL

**Architecture:**
```
┌──────────────────────────────────────┐
│        Storage Service               │
│  ┌────────────────────────────────┐  │
│  │   Tier Manager                 │  │
│  │  • Hot (NVMe): 0-7 days        │  │
│  │  • Warm (HDD): 7-30 days       │  │
│  │  • Cold (Object): 30-365 days  │  │
│  └────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │
│  │   Retention Manager            │  │
│  │  • Policy enforcement          │  │
│  │  • Automated cleanup           │  │
│  └────────────────────────────────┘  │
│  ┌────────────────────────────────┐  │
│  │   Compression Manager          │  │
│  │  • Re-encode old footage       │  │
│  │  • Deduplication               │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

**Storage Tiers:**
| Tier | Storage | Access | Retention | Cost/GB |
|------|---------|--------|-----------|---------|
| Hot | NVMe | <10ms | 0-7 days | $0.30 |
| Warm | HDD | <100ms | 7-30 days | $0.05 |
| Cold | Object | <1s | 30-365 days | $0.01 |
| Archive | Glacier | Minutes | 365+ days | $0.004 |

### 4. Event Service

**Technology:** Go + NATS JetStream

**Complex Event Processing:**
```
Event Stream → CEP Engine → Correlation Rules → Actions
                    ↓
              Time Windows
              Pattern Matching
              Aggregation
```

**Example Rule:**
```yaml
rule:
  name: tailgating_detection
  conditions:
    - event_type: access.badge_swipe
      location: door_01
    - event_type: analytics.person_detected
      location: near_door_01
      time_window: 10s
  logic: |
    badge_swipes = count(access.badge_swipe)
    persons = count(person_detected)
    if persons > badge_swipes:
      trigger_alert("tailgating", severity="high")
```

### 5. Integration Service

**Technology:** Node-RED + Apache Camel

**Supported Protocols:**
- MQTT (Native)
- Modbus TCP/RTU
- BACnet (Building automation)
- OPC UA (Industrial)
- HTTP/REST
- WebSocket
- SNMP

**Integration Flow:**
```
[MQTT In] → [Parse] → [Transform] → [NATS Out]
                ↓
          [PostgreSQL]
                ↓
          [Webhook]
```

### 6. Digital Twin Service

**Technology:** Eclipse Ditto + PostGIS

**Device Twin Model:**
```json
{
  "thingId": "camera:front_door_01",
  "attributes": {
    "location": {
      "latitude": 45.4215,
      "longitude": -75.6972,
      "building": "HQ",
      "floor": 1
    },
    "specs": {
      "model": "Hikvision",
      "resolution": "4K",
      "fov": 110
    }
  },
  "features": {
    "stream": {
      "properties": {
        "status": "online",
        "fps": 20,
        "bitrate": 4096
      }
    },
    "health": {
      "properties": {
        "uptime": 86400,
        "temperature": 45
      }
    }
  }
}
```

---

## Data Architecture

### Data Flow

**1. Video Recording Path:**
```
Camera (RTSP)
    ↓
MediaMTX (Stream Router)
    ↓
FFmpeg (Transcode)
    ↓
MinIO (Object Storage)
    ↓ (Metadata)
PostgreSQL (Index)
```

**2. Analytics Path:**
```
Camera → MediaMTX → Frame Buffer (Redis)
                         ↓
                   Analytics Module
                         ↓
                   NATS Event Stream
                   ↓          ↓
            PostgreSQL    Webhooks
```

**3. Event Correlation Path:**
```
Multiple Sources → NATS → CEP Engine → Correlated Events
(Cameras, IoT,              ↓
 Access Control)      Alert Generation
                           ↓
                     Notification Service
```

### Database Schema (Simplified)

**Cameras Table:**
```sql
CREATE TABLE cameras (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    stream_url VARCHAR(500) NOT NULL,
    location GEOGRAPHY(POINT),
    status VARCHAR(50),
    config JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_cameras_location ON cameras USING GIST(location);
CREATE INDEX idx_cameras_status ON cameras(status);
```

**Recordings Table (TimescaleDB Hypertable):**
```sql
CREATE TABLE recordings (
    id UUID PRIMARY KEY,
    camera_id UUID REFERENCES cameras(id),
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ,
    duration_seconds INT,
    size_bytes BIGINT,
    storage_path VARCHAR(1000),
    motion_detected BOOLEAN,
    event_count INT
);

SELECT create_hypertable('recordings', 'start_time');
CREATE INDEX idx_recordings_camera_time ON recordings(camera_id, start_time DESC);
```

**Detections Table (TimescaleDB Hypertable):**
```sql
CREATE TABLE detections (
    id UUID PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL,
    camera_id UUID REFERENCES cameras(id),
    detection_type VARCHAR(100),
    confidence FLOAT,
    bbox JSONB,
    metadata JSONB
);

SELECT create_hypertable('detections', 'timestamp');
CREATE INDEX idx_detections_camera_time ON detections(camera_id, timestamp DESC);
CREATE INDEX idx_detections_type ON detections(detection_type);
```

### Storage Architecture

**Ceph Architecture:**
```
┌────────────────────────────────────────┐
│          Ceph Cluster                  │
│  ┌──────────────────────────────────┐  │
│  │         MON (Monitors)           │  │
│  │  • Cluster state                 │  │
│  │  • Consensus (Paxos)             │  │
│  │  • 3+ nodes                      │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │         OSD (Object Storage)     │  │
│  │  • Data storage daemons          │  │
│  │  • 12 HDDs per node              │  │
│  │  • 6+ nodes                      │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │         MDS (Metadata)           │  │
│  │  • CephFS metadata               │  │
│  │  • Optional                      │  │
│  └──────────────────────────────────┘  │
└────────────────────────────────────────┘
```

**Replication:**
- 3x replication for critical data
- Erasure coding (8+3) for archival
- Cross-datacenter replication for DR

---

## Security Architecture

### Defense in Depth

**Layer 1: Network Security**
- VLANs (camera, management, edge networks)
- Firewall rules (deny by default)
- VPN (WireGuard/Tailscale)
- Network segmentation

**Layer 2: Transport Security**
- TLS 1.3 for all external communication
- mTLS for service-to-service
- Certificate rotation (Let's Encrypt)

**Layer 3: Application Security**
- JWT authentication
- OAuth2/OIDC
- RBAC (Keycloak)
- API rate limiting
- Input validation

**Layer 4: Data Security**
- Encryption at rest (LUKS, MinIO encryption)
- Database encryption (PostgreSQL)
- Secrets management (Sealed Secrets, Vault)

**Layer 5: Runtime Security**
- Container security (Falco)
- Pod security policies
- Network policies (Kubernetes)
- Resource limits

### Zero-Trust Architecture

**Every request must:**
1. Authenticate (Who are you?)
2. Authorize (What can you do?)
3. Audit (What did you do?)

```
Client Request
    ↓
API Gateway (JWT validation)
    ↓
Service A (Check OPA policy)
    ↓
Service B (Validate mTLS cert)
    ↓
Database (Row-level security)
    ↓
Audit Log (Immutable record)
```

### Audit Trail

**Blockchain-backed (Optional):**
```
Event → Hash → Append to Chain → Store in PostgreSQL
                ↓
         Replicate to Loki
```

**What's Logged:**
- All video access
- Configuration changes
- User actions
- System events
- API calls

---

## Scalability & Performance

### Horizontal Scaling

**Stateless Services** (Scale infinitely):
- API Gateway
- Analytics Service
- Integration Service
- Web UI

**Stateful Services** (Require coordination):
- VMS Service (shard by camera)
- Storage Service (distributed storage)
- Database (read replicas)

### Performance Targets

| Metric | Target | Measured |
|--------|--------|----------|
| Video latency | <500ms | Edge processing |
| Analytics latency | <2s | GPU acceleration |
| API response (p95) | <100ms | Load balancing |
| Alert delivery | <5s | Event streaming |
| Camera density | 1000/cluster | Tested |
| Analytics throughput | 500 streams | GPU-dependent |
| Event throughput | 10K/sec | NATS capacity |

### Caching Strategy

**Redis Layers:**
1. API response cache (30s-5min TTL)
2. Session storage
3. Frame buffer (analytics queue)
4. Real-time state

### Load Balancing

**APISIX:**
- Round-robin (default)
- Least connections
- Consistent hashing (sticky sessions)
- Health check-based

---

## Integration Architecture

### API Standards

**REST API:**
- OpenAPI 3.0 specification
- JSON payload
- HTTP/2 support
- Versioning (/v1/, /v2/)

**gRPC API:**
- Protocol Buffers
- Bi-directional streaming
- Lower latency than REST

**WebSocket:**
- Real-time event streaming
- Live video feed
- Bidirectional communication

### Event Schema

**CloudEvents Standard:**
```json
{
  "specversion": "1.0",
  "type": "com.openvision.detection.person",
  "source": "/cameras/front_door_01",
  "id": "A234-1234-1234",
  "time": "2025-11-19T14:30:00Z",
  "datacontenttype": "application/json",
  "data": {
    "confidence": 0.95,
    "bbox": {...}
  }
}
```

---

## Summary

OpenVision Platform provides:

✅ **Modern Architecture** - Microservices, event-driven, cloud-native  
✅ **Production-Ready** - HA, security, observability built-in  
✅ **Scalable** - Edge to cloud, 1 to 10,000+ cameras  
✅ **Flexible** - Plugin architecture, open APIs  
✅ **Performant** - <500ms latency, GPU acceleration  
✅ **Secure** - Zero-trust, encryption, audit logging  

**Status:** Architecture validated, core components proven in production environments

---

**Next Documents:**
- Deployment Guide (Technical)
- Module Development Guide (Developers)
- Operations Runbook (SRE/DevOps)
