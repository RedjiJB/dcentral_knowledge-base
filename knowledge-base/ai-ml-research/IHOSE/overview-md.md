---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: 01e8a63f-fcb8-4125-ba29-aabd46b4500e
original_filename: overview.md
created_at: 2025-12-02T00:47:55.827432+00:00
content_hash: 1503b4f28db6cross_category_duplicate_at: "security-identity/Open-Vision/overview-md.md"topic: person-vpn-mode
topic: ihose-architecture-deployment
---

# System Architecture Overview

## Table of Contents
1. [Architecture Principles](#architecture-principles)
2. [Layered Architecture](#layered-architecture)
3. [Component Breakdown](#component-breakdown)
4. [Data Flow](#data-flow)
5. [Scalability Design](#scalability-design)
6. [Security Architecture](#security-architecture)

## Architecture Principles

### 1. Edge-First Computing
Process data as close to the source as possible:
- Reduces bandwidth requirements (only send alerts/metadata to cloud)
- Improves latency (real-time analytics at edge)
- Enables offline operation (edge nodes function independently)
- Privacy-preserving (video stays local when possible)

### 2. Microservices Architecture
Each component is independently deployable:
- Services communicate via APIs and message queues
- Fault isolation (one service failure doesn't bring down system)
- Technology flexibility (use best tool for each job)
- Independent scaling (scale bottleneck components only)

### 3. Event-Driven Design
Asynchronous event processing:
- Loose coupling between components
- High throughput and scalability
- Natural fit for real-time surveillance
- Easy integration with external systems

### 4. API-First Development
Everything exposed via REST/GraphQL/gRPC:
- External integrations easy to build
- Custom UIs can be developed
- Third-party tools can consume data
- Testing and automation simplified

### 5. Infrastructure as Code
All infrastructure defined in version-controlled files:
- Reproducible deployments
- Easy rollback on failures
- Environment parity (dev/staging/prod identical)
- Documentation as code

## Layered Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Presentation Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Web UI     │  │  Mobile App  │  │  Grafana     │             │
│  │  (React)     │  │ (React Native)│  │  Dashboards  │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                                │ HTTPS/WSS
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                   Apache APISIX                               │  │
│  │  • Authentication (JWT/OAuth2)                                │  │
│  │  • Rate Limiting                                              │  │
│  │  • Service Routing                                            │  │
│  │  • API Versioning                                             │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                                │ Internal APIs
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Application Services Layer                       │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │   VMS     │  │ Analytics │  │Integration│  │  User     │       │
│  │  Service  │  │  Service  │  │  Service  │  │ Management│       │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘       │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │  Storage  │  │  Event    │  │  Workflow │  │  Digital  │       │
│  │  Service  │  │  Service  │  │  Service  │  │   Twin    │       │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘       │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                                │ Message Bus
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Message Broker Layer                             │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  NATS JetStream (Internal)  │  Mosquitto (IoT/MQTT)          │  │
│  │  • Event streaming           │  • Device connectivity         │  │
│  │  • Service-to-service        │  • Sensor data ingestion       │  │
│  │  • Request/Reply             │  • Command/Control             │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Data Layer                                   │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │PostgreSQL │  │   MinIO   │  │   Redis   │  │   Ceph    │       │
│  │+TimescaleDB│  │  Object   │  │  Cache    │  │Distributed│       │
│  │ Metadata  │  │  Storage  │  │           │  │  Storage  │       │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘       │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Edge Layer                                   │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    K3s Cluster                                │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐         │  │
│  │  │ Frigate │  │MediaMTX │  │  YOLO   │  │ EdgeX   │         │  │
│  │  │   VMS   │  │Streaming│  │Analytics│  │Foundry  │         │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘         │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                                │ RTSP/ONVIF/MQTT
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Device Layer                                   │
│    [IP Camera 1]  [IP Camera 2]  ...  [IP Camera N]                │
│    [IoT Sensor 1] [IoT Sensor 2] ... [IoT Sensor N]                │
│    [Access Control] [HVAC] [Fire Alarm] [Door Locks]               │
└─────────────────────────────────────────────────────────────────────┘
```

## Component Breakdown

### 1. Video Management System (VMS) Service

**Technology**: Frigate (primary), Shinobi (alternative)

**Responsibilities**:
- Camera connection management (RTSP/ONVIF)
- Video stream routing
- Recording orchestration
- Playback API
- Motion detection (basic)
- Snapshot generation

**APIs**:
```
GET  /api/v1/cameras                    # List all cameras
GET  /api/v1/cameras/{id}/stream        # Live stream URL
GET  /api/v1/recordings?camera=x&from=y  # Query recordings
POST /api/v1/cameras/{id}/snapshot      # Capture snapshot
PUT  /api/v1/cameras/{id}/config        # Update camera config
```

**Configuration**:
```yaml
cameras:
  front_door:
    ffmpeg:
      inputs:
        - path: rtsp://192.168.1.100/stream1
          roles: [detect, record]
    detect:
      width: 1920
      height: 1080
      fps: 5
    record:
      enabled: true
      retain:
        days: 30
        mode: motion
```

### 2. Analytics Service

**Technology**: Python + TensorFlow Serving + YOLO + OpenCV

**Responsibilities**:
- Object detection (person, vehicle, etc.)
- Face recognition
- License plate recognition (ALPR)
- Custom model inference
- Analytics pipeline orchestration
- Result aggregation

**Architecture**:
```
Analytics Coordinator
    ├─> Object Detection Module (YOLOv8)
    ├─> Face Recognition Module (CompreFace)
    ├─> ALPR Module (OpenALPR)
    ├─> Custom Module 1 (Client-specific)
    └─> Custom Module N
```

**Module Interface**:
```python
class AnalyticsModule:
    def initialize(self, config: Dict) -> None:
        """Initialize module with configuration"""
        
    def process_frame(self, frame: np.ndarray, metadata: Dict) -> List[Detection]:
        """Process single frame, return detections"""
        
    def process_stream(self, stream_url: str) -> Iterator[Detection]:
        """Process continuous stream"""
        
    def cleanup(self) -> None:
        """Cleanup resources"""
```

**Event Output**:
```json
{
  "timestamp": "2025-11-19T14:30:00Z",
  "camera_id": "front_door",
  "module": "yolo_v8",
  "detections": [
    {
      "class": "person",
      "confidence": 0.95,
      "bbox": [100, 200, 300, 500],
      "tracking_id": "person_1234"
    }
  ],
  "metadata": {
    "frame_number": 1234,
    "processing_time_ms": 45
  }
}
```

### 3. Integration Service

**Technology**: Node-RED + Apache Camel + Custom adapters

**Responsibilities**:
- IoT device communication (MQTT, Modbus, BACnet, OPC UA)
- Third-party API integrations
- Webhook management
- Protocol translation
- Data normalization

**Supported Protocols**:
- **MQTT**: Native via Mosquitto
- **ONVIF**: Camera discovery and control
- **Modbus TCP/RTU**: Industrial sensors
- **BACnet**: Building automation
- **OPC UA**: Industrial systems
- **HTTP/REST**: Generic APIs
- **WebSocket**: Real-time feeds
- **SNMP**: Network devices

**Integration Flow Example** (Node-RED):
```
[MQTT In] → [Parse JSON] → [Filter] → [Transform] → [NATS Out]
                                ↓
                          [PostgreSQL]
                                ↓
                          [Webhook Out]
```

### 4. Storage Service

**Technology**: MinIO + Ceph + PostgreSQL

**Responsibilities**:
- Video archive management
- Intelligent tiering (hot/warm/cold storage)
- Retention policy enforcement
- Deduplication
- Compression

**Storage Tiers**:
```
Tier 1 (Hot):  0-7 days    → NVMe SSD  → Full quality
Tier 2 (Warm): 7-30 days   → HDD       → High quality
Tier 3 (Cold): 30-365 days → Object    → Compressed
Tier 4 (Archive): 365+ days → Glacier  → Event-only
```

**API**:
```
GET  /api/v1/storage/stats               # Storage statistics
GET  /api/v1/storage/recordings/{id}     # Retrieve recording
POST /api/v1/storage/archive             # Manual archival
GET  /api/v1/storage/retention-policies  # List policies
```

### 5. Event Service

**Technology**: NATS JetStream + Apache Kafka (optional)

**Responsibilities**:
- Event stream management
- Complex event processing (CEP)
- Event correlation across sources
- Alert generation
- Audit logging

**Event Types**:
- `camera.online` / `camera.offline`
- `detection.person` / `detection.vehicle`
- `motion.detected`
- `analytics.alert`
- `system.error`
- `user.action`

**Event Processing Example**:
```
Scenario: Tailgating Detection

[Access Card Read] ────┐
                       ├──> [Correlation Engine]
[Person Detection] ────┘         ↓
                              [Alert]
                                 ↓
                    [Webhook] + [UI Notification]
```

### 6. Workflow Service

**Technology**: Temporal.io

**Responsibilities**:
- Long-running workflows
- Incident response automation
- Scheduled tasks
- Retry logic
- State management

**Example Workflow**:
```python
@workflow.defn
class IncidentResponseWorkflow:
    @workflow.run
    async def run(self, incident: Incident) -> None:
        # Step 1: Capture video evidence
        await workflow.execute_activity(
            capture_video,
            args=[incident.camera_id, incident.timestamp],
            start_to_close_timeout=timedelta(seconds=30)
        )
        
        # Step 2: Run additional analytics
        await workflow.execute_activity(
            enhanced_analytics,
            args=[incident.id],
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        # Step 3: Notify security team
        await workflow.execute_activity(
            send_notifications,
            args=[incident.id],
            start_to_close_timeout=timedelta(seconds=10)
        )
        
        # Step 4: Update case management system
        await workflow.execute_activity(
            update_case_system,
            args=[incident.id],
            start_to_close_timeout=timedelta(seconds=30)
        )
```

### 7. Digital Twin Service

**Technology**: Eclipse Ditto + PostGIS

**Responsibilities**:
- 3D building model management
- Device twin state synchronization
- Spatial queries
- Coverage analysis
- Simulation

**Data Model**:
```json
{
  "thingId": "camera:front_door_01",
  "policyId": "camera:default_policy",
  "attributes": {
    "location": {
      "latitude": 45.4215,
      "longitude": -75.6972,
      "elevation": 10.5,
      "building": "HQ",
      "floor": 1
    },
    "specs": {
      "model": "Hikvision DS-2CD2387G2",
      "resolution": "4K",
      "focal_length": "2.8mm",
      "field_of_view": 110
    }
  },
  "features": {
    "stream": {
      "properties": {
        "status": "online",
        "url": "rtsp://192.168.1.100/stream1",
        "fps": 20,
        "bitrate": 4096
      }
    },
    "health": {
      "properties": {
        "uptime": 86400,
        "temperature": 45,
        "frame_drops": 0
      }
    }
  }
}
```

**Spatial Queries** (PostGIS):
```sql
-- Find all cameras within 50m of a location
SELECT camera_id, ST_Distance(location, ST_MakePoint(-75.6972, 45.4215)) as distance
FROM cameras
WHERE ST_DWithin(
    location,
    ST_MakePoint(-75.6972, 45.4215)::geography,
    50
)
ORDER BY distance;

-- Find coverage gaps (areas with <2 overlapping cameras)
SELECT zone_id, COUNT(camera_id) as camera_count
FROM coverage_zones
LEFT JOIN camera_coverage ON ST_Intersects(zone.geom, coverage.geom)
GROUP BY zone_id
HAVING COUNT(camera_id) < 2;
```

### 8. User Management Service

**Technology**: Keycloak

**Responsibilities**:
- Authentication (JWT, OAuth2, SAML)
- Authorization (RBAC)
- User federation (LDAP/Active Directory)
- SSO
- Multi-tenancy

**Role Hierarchy**:
```
Super Admin
├─> Tenant Admin
    ├─> Site Administrator
        ├─> Security Manager
            ├─> Security Operator
            └─> Viewer
```

**Permissions**:
```yaml
roles:
  security_operator:
    permissions:
      - camera:view_live
      - camera:view_recordings
      - alert:acknowledge
      - alert:escalate
    restrictions:
      - cannot:camera:configure
      - cannot:user:manage
      - cannot:system:configure
  
  site_administrator:
    inherits: security_operator
    permissions:
      - camera:configure
      - camera:add
      - user:create
      - analytics:configure
```

## Data Flow

### 1. Live Video Streaming

```
IP Camera (RTSP)
    ↓
MediaMTX (Stream Router)
    ↓
┌───────────────┬───────────────┬───────────────┐
↓               ↓               ↓               ↓
Frigate      Analytics      Web Client    Recording
(Motion)     (AI/ML)        (WebRTC)      (Storage)
    ↓               ↓               
NATS Event   NATS Event
    ↓               ↓
Digital Twin    PostgreSQL
```

### 2. Analytics Pipeline

```
Video Frame
    ↓
Frame Buffer Queue (Redis)
    ↓
Analytics Coordinator
    ↓
┌────────────┬────────────┬────────────┐
↓            ↓            ↓            ↓
YOLO     CompreFace   ALPR    Custom Module
    ↓            ↓            ↓            ↓
    └────────────┴────────────┴────────────┘
                        ↓
              Detection Aggregator
                        ↓
              NATS Event Stream
                        ↓
        ┌───────────────┼───────────────┐
        ↓               ↓               ↓
  PostgreSQL      Grafana         Webhook
  (Storage)       (Display)      (External)
```

### 3. Event Correlation

```
Access Card Swipe (MQTT)
    ↓
NATS: event.access.door_01
    ↓
    │
Person Detection (Analytics) ───> NATS: event.detection.person
    ↓                                    ↓
    └──────────────┬─────────────────────┘
                   ↓
         Event Correlation Engine
         (Temporal Workflow)
                   ↓
    ┌──────────────┼──────────────┐
    ↓              ↓              ↓
Alert Gen    Video Clip    Case Creation
                           (External System)
```

### 4. Multi-Tenant Data Isolation

```
Incoming Request
    ↓
API Gateway (Extract tenant_id from JWT)
    ↓
┌─────────────────┬─────────────────┬─────────────────┐
↓                 ↓                 ↓                 ↓
Service A      Service B        Service C        Service D
tenant_id=123  tenant_id=123    tenant_id=123    tenant_id=123
    ↓                 ↓                 ↓                 ↓
PostgreSQL      PostgreSQL       PostgreSQL       MinIO
WHERE tenant_id WHERE tenant_id  WHERE tenant_id  bucket=tenant_123
```

## Scalability Design

### Horizontal Scaling

**Stateless Services** (can add unlimited replicas):
- API Gateway
- Analytics Service
- Integration Service
- Web UI

**Stateful Services** (require coordination):
- VMS Service (shard by camera)
- Storage Service (distributed storage)
- Database (read replicas)

### Vertical Scaling

**CPU-Intensive**:
- Analytics modules → GPU acceleration
- Video encoding → Hardware encoding (NVENC, QSV)

**Memory-Intensive**:
- Frame buffers → Larger Redis cluster
- ML models → Larger model servers

**Storage-Intensive**:
- Video archives → Add storage nodes

### Edge-Cloud Distribution

**Edge Node Responsibilities** (reduce cloud load):
- Video recording (local storage)
- Real-time analytics (edge AI)
- Immediate alerts
- Local viewing
- Store-and-forward queue

**Cloud Responsibilities**:
- Centralized management
- Long-term storage
- Cross-site analytics
- User management
- Advanced ML training

### Load Distribution Example

**500 cameras, 20 sites deployment**:

```
Site 1 (25 cameras)
├─> Edge Node 1: 15 cameras + analytics
└─> Edge Node 2: 10 cameras + analytics
    ↓ (metadata + alerts only)
    
Site 2 (25 cameras)
├─> Edge Node 3: 15 cameras + analytics
└─> Edge Node 4: 10 cameras + analytics
    ↓
    
... (sites 3-20)
    ↓
    ↓ (aggregated data)
    
Central Cloud (K8s Cluster)
├─> 3x VMS management pods
├─> 5x API gateway pods
├─> 10x Analytics aggregation pods
├─> 3x PostgreSQL read replicas
└─> Ceph storage cluster (200TB)

Load per edge node: 10-15 cameras, 5-10 TOPS AI
Load per cloud: Metadata only, ~100 events/sec
Bandwidth: ~10 Mbps per site (metadata + occasional video pull)
```

## Security Architecture

### Defense in Depth

**Layer 1: Network**
- Isolated VLANs (camera network, management network, edge network)
- Firewall rules (deny by default)
- VPN for remote access (WireGuard/Tailscale)
- mTLS between services

**Layer 2: Application**
- JWT authentication
- RBAC authorization (Keycloak)
- API rate limiting (API Gateway)
- Input validation (all endpoints)

**Layer 3: Data**
- Encryption at rest (LUKS, MinIO encryption)
- Encryption in transit (TLS 1.3)
- Database encryption (PostgreSQL)
- Secrets management (sealed secrets in K8s)

**Layer 4: Runtime**
- Container security (Falco)
- Pod security policies (OPA)
- Network policies (Kubernetes)
- Resource limits

### Zero-Trust Architecture

Every service must authenticate and authorize:

```
Service A → Service B request
    ↓
1. Service A obtains JWT from identity provider
2. Service A includes JWT in request to Service B
3. Service B validates JWT signature
4. Service B checks authorization (OPA policy)
5. Service B processes request if authorized
```

**Service Mesh** (Optional: Linkerd/Istio):
- Automatic mTLS between services
- Traffic encryption
- Service-to-service authentication
- Observability

### Audit Trail

**Immutable Audit Log** (Hyperledger Fabric):
- All video access logged
- Configuration changes recorded
- User actions tracked
- Cryptographically signed
- Tamper-evident

```
Audit Event → Hash → Append to blockchain
                ↓
        Store in PostgreSQL (queryable)
                ↓
        Replicate to Loki (searchable)
```

### Compliance Support

**GDPR**:
- Right to be forgotten (video redaction API)
- Data export (API for user data)
- Consent management
- Data retention policies

**SOC 2**:
- Access controls (RBAC)
- Encryption (at rest and in transit)
- Audit logging (comprehensive)
- Incident response (automated workflows)

## Deployment Topologies

### 1. Single-Site SMB

```
┌────────────────────────────────────┐
│         Edge Node (1x)             │
│  ┌──────────────────────────────┐  │
│  │  K3s                          │  │
│  │  ├─ Frigate (VMS)             │  │
│  │  ├─ MediaMTX (Streaming)      │  │
│  │  ├─ YOLO (Analytics)          │  │
│  │  ├─ PostgreSQL                │  │
│  │  ├─ MinIO (Local Storage)     │  │
│  │  └─ Grafana                   │  │
│  └──────────────────────────────┘  │
│                                    │
│  Cameras: 10-20                    │
│  Storage: 4TB local                │
│  Hardware: Orange Pi 5 + Coral    │
└────────────────────────────────────┘
```

### 2. Multi-Site Enterprise

```
┌──────── Site 1 ────────┐  ┌──────── Site 2 ────────┐
│  Edge Nodes (2x)       │  │  Edge Nodes (2x)       │
│  ├─ K3s Cluster        │  │  ├─ K3s Cluster        │
│  ├─ Local Processing   │  │  ├─ Local Processing   │
│  └─ 4TB Local Storage  │  │  └─ 4TB Local Storage  │
└────────────────────────┘  └────────────────────────┘
         ↓                           ↓
         └───────────────┬───────────┘
                         ↓
         ┌───────────────────────────────┐
         │     Central Cloud (K8s)       │
         │  ┌─────────────────────────┐  │
         │  │  Management Layer       │  │
         │  │  ├─ API Gateway          │  │
         │  │  ├─ User Management      │  │
         │  │  ├─ Cross-site analytics │  │
         │  │  └─ Digital Twin         │  │
         │  └─────────────────────────┘  │
         │  ┌─────────────────────────┐  │
         │  │  Data Layer             │  │
         │  │  ├─ PostgreSQL Cluster   │  │
         │  │  ├─ Ceph (200TB)         │  │
         │  │  └─ Redis Cluster        │  │
         │  └─────────────────────────┘  │
         └───────────────────────────────┘
```

### 3. SaaS Multi-Tenant

```
┌─────────────────────────────────────────┐
│      Regional Cloud (US-East)           │
│  ┌───────────────────────────────────┐  │
│  │  K8s Cluster (100+ nodes)         │  │
│  │  ├─ Namespace: tenant_1           │  │
│  │  ├─ Namespace: tenant_2           │  │
│  │  ├─ ...                           │  │
│  │  └─ Namespace: tenant_N           │  │
│  └───────────────────────────────────┘  │
│  ┌───────────────────────────────────┐  │
│  │  Shared Services                  │  │
│  │  ├─ Keycloak (Multi-tenant)       │  │
│  │  ├─ API Gateway                   │  │
│  │  └─ Monitoring                    │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
         ↕
┌─────────────────────────────────────────┐
│      Regional Cloud (EU-West)           │
│  (Same structure, geo-replicated)       │
└─────────────────────────────────────────┘
```

## Technology Selection Rationale

### Why Frigate?
- Modern, actively developed
- Excellent AI integration (YOLOv8, TensorFlow)
- MQTT-first design (IoT-friendly)
- Low resource usage
- Great documentation

### Why NATS over Kafka?
- Lighter weight (better for edge)
- JetStream provides persistence when needed
- Simpler operations
- Lower latency
- Built-in clustering

### Why K3s over full Kubernetes?
- 50% less memory usage
- Single binary installation
- Perfect for edge nodes
- Compatible with K8s (easy to upgrade)
- Includes Traefik, CoreDNS out-of-box

### Why PostgreSQL over MongoDB?
- ACID compliance (critical for metadata)
- TimescaleDB extension (time-series data)
- PostGIS extension (spatial queries)
- Mature replication
- Lower TCO

### Why MinIO over Swift?
- S3 API compatibility (standard)
- Better performance
- Simpler operations
- Excellent tiering support
- Kubernetes-native

## Performance Targets

### Latency
- Live streaming: <500ms glass-to-glass
- Analytics results: <2 seconds from detection
- API response: <100ms (95th percentile)
- Alert notification: <5 seconds end-to-end

### Throughput
- Video ingestion: 1000+ cameras per cluster
- Analytics: 500+ concurrent streams
- Events: 10,000 events/second
- API: 5,000 requests/second

### Availability
- Edge nodes: 99% (can operate offline)
- Cloud services: 99.9% uptime
- Data durability: 99.999999999% (11 nines)

### Resource Usage (per camera)
- Bandwidth: 2-4 Mbps (H.265)
- Storage: 2-5 GB/day (motion-based)
- CPU: 0.1-0.2 cores (without analytics)
- GPU: 0.5 TOPS (with analytics)

---

## Next Steps

See detailed documentation:
- [Edge Architecture](edge.md)
- [Cloud Architecture](cloud.md)
- [Multi-Tenant Design](multi-tenant.md)
- [Security Deep Dive](security.md)
