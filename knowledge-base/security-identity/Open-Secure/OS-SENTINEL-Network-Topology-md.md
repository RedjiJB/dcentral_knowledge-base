---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: 9cabf4fb-2d23-453e-a0b0-51f91cf7a17c
original_filename: OS-SENTINEL_Network_Topology.md
created_at: 2026-03-04T20:34:08.570122+00:00
content_hash: c4521ffbeea4topic: retrieval-scenarios-warm
topic: opensecure-guardian-sentinel-topology
---

# OS-SENTINEL Network Topology
## AI-Powered Surveillance Network & Video Analytics Infrastructure

**Document Type**: Network Topology Specification  
**Version**: 1.0  
**Date**: December 2024  
**Classification**: Technical Documentation  
**Audience**: Network Architects, Security Engineers, System Administrators

---

## Executive Summary

### Network Architecture Philosophy

OS-SENTINEL implements a **distributed AI-at-the-edge surveillance architecture** that combines traditional NVR functionality with cutting-edge computer vision. Design principles:

- **Edge AI Processing**: Object detection, facial recognition, behavior analysis at camera/NVR level
- **Bandwidth Optimization**: Only transmit alerts and metadata, not continuous video
- **Scalable Storage**: Tiered retention from days (local) to years (cloud)
- **Multi-Site Federation**: Central monitoring of distributed camera networks
- **Open Standards**: ONVIF, RTSP, HLS for maximum camera compatibility

### Network Scale Characteristics

| Deployment Size | Cameras | Sites | Daily Video | AI Processing | Annual Cost |
|-----------------|---------|-------|-------------|---------------|-------------|
| Small (10-50) | 10-50 | 1 | 500 GB | Basic | $25,000 |
| Medium (50-200) | 50-200 | 1-3 | 2 TB | Advanced | $100,000 |
| Large (200-1000) | 200-1,000 | 5-20 | 10 TB | Full AI Suite | $500,000 |
| Enterprise (1000+) | 1,000+ | 20+ | 50+ TB | Custom Models | $2,000,000+ |

---

## Network Architecture Overview

### Three-Tier Surveillance Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                    TIER 1: CAMERA LAYER                             │
│                    (Edge Devices & Acquisition)                     │
└────────────────────────────────────────────────────────────────────┘

VLAN 10: Camera Network (10.20.10.0/22)
├── IP Range: 10.20.10.1 - 10.20.13.254 (1,024 cameras max)
├── Subnet Mask: 255.255.252.0 (/22)
├── Gateway: 10.20.10.1 (Camera PoE Switch)
└── DNS: 10.0.20.53

Camera Types & Network Requirements:
┌──────────────────────────────────────────────────────────────┐
│ Fixed Dome Cameras (Indoor/Outdoor)                         │
│ ├── Model: Hikvision DS-2CD2143G0-I or Dahua IPC-HDW5231R  │
│ ├── Resolution: 4MP (2688×1520)                            │
│ ├── Frame Rate: 20 fps                                     │
│ ├── Bitrate: 6 Mbps (H.265)                                │
│ ├── Power: PoE (802.3af, 12W)                              │
│ └── Network: Gigabit Ethernet                              │
│                                                             │
│ PTZ Cameras (Pan-Tilt-Zoom)                                │
│ ├── Model: Axis Q6215-LE or Hanwha XNP-6120H              │
│ ├── Resolution: 1080p                                      │
│ ├── Optical Zoom: 30×                                      │
│ ├── Bitrate: 8 Mbps (H.265)                                │
│ ├── Power: PoE+ (802.3at, 30W)                             │
│ └── Network: Gigabit Ethernet                              │
│                                                             │
│ License Plate Recognition (LPR)                             │
│ ├── Model: OpenALPR Camera (custom)                        │
│ ├── Resolution: 4MP @ 60 fps                               │
│ ├── Lens: 6-22mm varifocal                                 │
│ ├── Bitrate: 10 Mbps (H.265)                               │
│ ├── Power: PoE+ (25W)                                      │
│ └── Network: Gigabit Ethernet + Edge AI processing         │
└──────────────────────────────────────────────────────────────┘

Network Switches (PoE):
├── Core Camera Switch: Cisco SG350X-48MP ($2,000)
│   ├── 48× Gigabit PoE+ ports (740W power budget)
│   ├── 4× 10 Gbps SFP+ uplinks
│   └── VLAN support, QoS, IGMP snooping
│
└── Access Switches: TP-Link TL-SG1024PE ($180 each)
    ├── 24× PoE ports (250W budget)
    ├── 2× Gigabit uplinks
    └── Connect to core switch

┌────────────────────────────────────────────────────────────────────┐
│                    TIER 2: NVR & EDGE INTELLIGENCE                  │
│                    (Recording, Storage, AI Processing)              │
└────────────────────────────────────────────────────────────────────┘

VLAN 20: NVR & Storage (10.20.20.0/24)

NVR Server (Network Video Recorder)
├── Hardware:
│   ├── CPU: Intel Xeon E-2386G (6-core, 3.5 GHz)
│   ├── RAM: 64 GB ECC
│   ├── Storage: 8× 8TB SATA HDDs (RAID 6) = 48 TB usable
│   ├── Network: 2× 10 Gbps Ethernet (bonded)
│   └── GPU: NVIDIA T4 (AI inference)
│
├── Software: Frigate NVR + OpenVision
│   ├── Video Management: 200 camera streams
│   ├── Recording: Continuous + motion-triggered
│   ├── AI: Object detection, face recognition
│   └── API: REST + WebSocket
│
├── Network Config:
│   ├── eth0: 10.20.20.10/24 (camera VLAN)
│   ├── eth1: 10.0.30.10/24 (management VLAN)
│   └── Bond: 20 Gbps aggregate bandwidth
│
└── IP Addressing:
    ├── Primary NVR: 10.20.20.10
    ├── Backup NVR: 10.20.20.11
    └── Storage NAS: 10.20.20.20 (expansion)

AI Processing Cluster (GPU Nodes)
├── Node 1: 10.20.20.30 (NVIDIA A100, 80GB VRAM)
├── Node 2: 10.20.20.31 (NVIDIA A100, 80GB VRAM)
├── Node 3: 10.20.20.32 (NVIDIA A100, 80GB VRAM)
└── Workload:
    ├── Real-time object detection (YOLOv8)
    ├── Facial recognition (ArcFace)
    ├── Behavior analysis (OpenPose, SlowFast)
    └── Natural language queries (CLIP)

┌────────────────────────────────────────────────────────────────────┐
│                    TIER 3: MANAGEMENT & MONITORING                  │
│                    (Central Command, Analytics, Integration)        │
└────────────────────────────────────────────────────────────────────┘

VLAN 30: Management Network (10.0.30.0/24)

Video Management System (VMS)
├── IP: 10.0.30.10
├── Software: OpenVision Dashboard (Web UI)
├── Features:
│   ├── Live view (1-64 cameras simultaneously)
│   ├── Playback & export
│   ├── Alert management
│   ├── PTZ control
│   └── User management (RBAC)

API Gateway
├── IP: 10.0.30.20
├── Software: Kong Gateway
├── Endpoints:
│   ├── /api/v1/cameras
│   ├── /api/v1/streams
│   ├── /api/v1/events
│   └── /api/v1/search

Database Cluster
├── PostgreSQL + TimescaleDB
│   ├── Primary: 10.0.30.40
│   ├── Replica 1: 10.0.30.41
│   └── Replica 2: 10.0.30.42
│
└── Data:
    ├── Camera metadata
    ├── Event logs (motion, objects, alerts)
    ├── Face recognition database
    └── Analytics results

Object Storage (MinIO)
├── Video Archive (Long-term)
├── Nodes: 10.0.30.50-53 (4-node cluster)
├── Capacity: 200 TB (erasure coded EC 4+2)
└── Retention: 90 days → AWS S3 Glacier

Analytics & Reporting
├── IP: 10.0.30.60
├── Software: Grafana + Prometheus
├── Metrics:
│   ├── Camera uptime
│   ├── Object detection counts
│   ├── Storage usage
│   └── Alert frequency

External Integrations:
├── Access Control (OS-PACS): 10.0.10.x
├── Incident Management: 10.0.40.x
└── Video Walls: 10.0.50.x (HDMI over IP)
```

---

## Camera Network Design

### PoE Network Architecture

```
┌────────────────────────────────────────────────────────────────┐
│              CAMERA POE NETWORK TOPOLOGY                        │
└────────────────────────────────────────────────────────────────┘

Building Floor Plan: 50,000 sq ft office
├── Cameras Required: 80 (1 per 625 sq ft)
├── Camera Distribution:
│   ├── Perimeter: 20 cameras
│   ├── Interior: 40 cameras
│   ├── Parking: 15 cameras
│   └── Specialty (PTZ, LPR): 5 cameras
└── Total PoE Power: 80 cameras × 15W = 1,200W

Switch Layout:
┌──────────────────────────────────────────────────────────────┐
│                     CORE SWITCH                              │
│            Cisco SG350X-48MP (10.20.10.1)                   │
│       ┌──────────────────────────────────────┐              │
│       │  48× Gigabit PoE+ Ports (740W)       │              │
│       │  4× 10 Gbps SFP+ Uplinks             │              │
│       └─┬─────┬─────┬─────┬─────┬────────────┘              │
│         │     │     │     │     │                           │
└─────────┼─────┼─────┼─────┼─────┼───────────────────────────┘
          │     │     │     │     │
    ┌─────┴──┐  │     │     │  ┌──┴─────┐
    │Access 1│  │     │     │  │Access 2│
    │24 ports│  │     │     │  │24 ports│
    │Floor 1 │  │     │     │  │Floor 2 │
    └───┬────┘  │     │     │  └───┬────┘
        │       │     │     │      │
      20 cams   │     │     │    20 cams
                │     │     │
          ┌─────┴──┐  │  ┌──┴─────┐
          │Access 3│  │  │Access 4│
          │Parking │  │  │Floor 3 │
          └───┬────┘  │  └───┬────┘
              │       │      │
           15 cams    │    20 cams
                      │
                  ┌───┴────┐
                  │ NVR 1  │ 10 Gbps uplink
                  │ NVR 2  │ 10 Gbps uplink
                  └────────┘

Bandwidth Calculation:
├── Per camera: 6 Mbps (H.265, 4MP @ 20 fps)
├── 80 cameras: 480 Mbps total
├── Core uplink: 10 Gbps (20× headroom)
└── Recording: All streams simultaneously

Power Budget:
├── Total cameras: 80 × 15W = 1,200W
├── Core switch: 740W (48 ports on-switch)
├── Access switches: 4 × 250W = 1,000W
└── Total PoE capacity: 1,740W (45% headroom)
```

### IP Addressing Scheme

```
VLAN 10: Camera Network (10.20.10.0/22)

Subnetting by Location/Function:
├── 10.20.10.0/25: Floor 1 Interior (128 IPs)
│   ├── Gateway: 10.20.10.1
│   └── Cameras: 10.20.10.10 - 10.20.10.30
│
├── 10.20.10.128/25: Floor 2 Interior (128 IPs)
│   ├── Gateway: 10.20.10.129
│   └── Cameras: 10.20.10.140 - 10.20.10.160
│
├── 10.20.11.0/25: Floor 3 Interior (128 IPs)
│   ├── Gateway: 10.20.11.1
│   └── Cameras: 10.20.11.10 - 10.20.11.30
│
├── 10.20.11.128/25: Parking Lot (128 IPs)
│   ├── Gateway: 10.20.11.129
│   └── Cameras: 10.20.11.140 - 10.20.11.155
│
├── 10.20.12.0/25: Perimeter (128 IPs)
│   ├── Gateway: 10.20.12.1
│   └── Cameras: 10.20.12.10 - 10.20.12.30
│
└── 10.20.12.128/25: Specialty (PTZ, LPR) (128 IPs)
    ├── Gateway: 10.20.12.129
    └── Cameras: 10.20.12.140 - 10.20.12.145

Reserved IPs:
├── .1: Gateway (switch)
├── .2-9: Reserved (future use)
├── .10+: Cameras
└── .250-254: Temporary (camera setup)
```

---

## Video Streaming Architecture

### Multi-Stream Configuration

```
┌────────────────────────────────────────────────────────────────┐
│              CAMERA MULTI-STREAM DESIGN                         │
└────────────────────────────────────────────────────────────────┘

Each camera provides 3 simultaneous streams:

Stream 1: Main Stream (High Quality)
├── Resolution: 4MP (2688×1520)
├── Frame Rate: 20 fps
├── Codec: H.265
├── Bitrate: 6 Mbps (VBR)
├── Use: Recording to NVR storage
└── Protocol: RTSP (rtsp://camera-ip/stream1)

Stream 2: Sub Stream (Live Viewing)
├── Resolution: 720p (1280×720)
├── Frame Rate: 15 fps
├── Codec: H.264
├── Bitrate: 1 Mbps (CBR)
├── Use: Live monitoring dashboards (low latency)
└── Protocol: RTSP (rtsp://camera-ip/stream2)

Stream 3: Mobile Stream (Remote Access)
├── Resolution: 480p (640×480)
├── Frame Rate: 10 fps
├── Codec: H.264
├── Bitrate: 256 Kbps (CBR)
├── Use: Mobile app, low-bandwidth clients
└── Protocol: HLS (https://api/camera-id/stream.m3u8)

Total Bandwidth per Camera:
├── Main: 6 Mbps
├── Sub: 1 Mbps (only when viewed)
├── Mobile: 0.256 Mbps (only when accessed)
└── Typical: 6 Mbps (recording only) + 1 Mbps when monitored
```

### Video Wall Integration

```
┌────────────────────────────────────────────────────────────────┐
│              VIDEO WALL ARCHITECTURE                            │
└────────────────────────────────────────────────────────────────┘

Security Operations Center (SOC)
├── Video Wall: 3×3 grid (9 displays)
│   ├── Resolution per display: 1920×1080
│   ├── Total pixels: 5760×3240 (18.6 MP)
│   └── Refresh: 60 Hz

Display Controller
├── Hardware: Datapath FX4 Display Wall Controller
├── Input: 4× 4K HDMI (from video server)
├── Output: 9× 1080p HDMI (to displays)
├── Network: Gigabit Ethernet (control)

Video Server (Decoding & Layout)
├── Hardware: GPU-accelerated server
│   ├── CPU: AMD EPYC 7763 (64-core)
│   ├── GPU: 4× NVIDIA A40 (48GB each)
│   ├── RAM: 256 GB
│   └── Network: 10 Gbps
│
├── Software: FFmpeg + custom video mosaic
├── Capabilities:
│   ├── Decode: 64 simultaneous camera streams
│   ├── Transcode: H.265 → H.264 (for compatibility)
│   ├── Compose: Grid layouts (4×4, 3×3, 2×2, etc.)
│   └── Output: 4× 4K streams to display controller
│
└── Bandwidth:
    ├── Input: 64 cameras × 1 Mbps = 64 Mbps
    ├── Output: 4× 4K @ 30fps × 20 Mbps = 80 Mbps
    └── Network: 10 Gbps (plenty of headroom)

Operator Console:
├── PTZ Control: Joystick for camera pan/tilt/zoom
├── Camera Selection: Click any display to change camera
├── Preset Tours: Auto-cycle through camera groups
└── Alert Overlay: Pop-up on motion/object detection
```

---

## Storage Architecture

### Tiered Video Retention

```
┌────────────────────────────────────────────────────────────────┐
│              VIDEO STORAGE TIERS                                │
└────────────────────────────────────────────────────────────────┘

Tier 1: HOT STORAGE (Local NVR)
├── Technology: RAID 6 HDD array
├── Capacity: 48 TB usable
├── Retention: 30 days
├── Access Speed: <100ms
├── Use Case: Recent footage, live playback
├── Cost: $50/TB = $2,400
└── Calculation:
    ├── 80 cameras × 6 Mbps × 24 hrs = 5.2 TB/day
    ├── 30 days × 5.2 TB = 156 TB required
    ├── With H.265 compression: ~45 TB actual
    └── RAID 6 overhead: 48 TB raw → 40 TB usable

        │ After 30 days (automated lifecycle)
        ▼

Tier 2: WARM STORAGE (NAS / Object Storage)
├── Technology: MinIO on JBOD
├── Capacity: 200 TB
├── Retention: 31-90 days (2 months)
├── Access Speed: 1-2 seconds
├── Use Case: Incident review, investigations
├── Cost: $30/TB = $6,000
└── Calculation:
    ├── 60 days × 5.2 TB/day = 312 TB
    ├── With deduplication: ~200 TB
    └── Erasure Coding EC 4+2: 200 TB usable

        │ After 90 days (policy-based)
        ▼

Tier 3: COLD STORAGE (Cloud Archive)
├── Technology: AWS S3 Glacier Deep Archive
├── Capacity: Unlimited
├── Retention: 91 days - 7 years
├── Access Speed: 12-48 hours (retrieval)
├── Use Case: Legal compliance, discovery
├── Cost: $1/TB/month
└── Calculation:
    ├── 7 years × 365 days × 5.2 TB = 13,300 TB (13 PB)
    ├── Monthly cost: 13,300 TB × $1 = $13,300/month
    └── Upload: Overnight batch (100 Mbps dedicated)

        │ After retention period (e.g., 7 years)
        ▼

Tier 4: DELETION (Secure Erasure)
├── Method: NIST 800-88 (overwrite + degauss)
├── Logging: Deletion certificates generated
├── Audit: Legal/compliance approval required
└── Compliance: State/federal retention laws

Motion-Triggered Recording (Optimization):
├── Continuous: 6 Mbps × 24 hrs = 64 GB/day/camera
├── Motion-Only: 6 Mbps × 2 hrs = 5.4 GB/day/camera
└── Savings: 91.5% reduction (suitable for low-traffic areas)
```

### Backup & Redundancy

```
Local Backup (On-Site):
├── Primary NVR: 10.20.20.10 (48 TB)
├── Backup NVR: 10.20.20.11 (48 TB, real-time replication)
├── Failover: Automatic (30 seconds)
└── Recovery: Zero data loss (synchronous replication)

Off-Site Backup (Cloud):
├── AWS S3 Standard (primary cloud backup)
├── Upload: Nightly incremental (last 24 hours)
├── Bandwidth: 100 Mbps dedicated circuit
├── Encryption: AES-256 in transit + at rest
└── Cost: $0.023/GB/month × 5,200 GB = $120/month

Disaster Recovery:
├── Backup Site: 50 miles from primary
├── Equipment: Replica NVR + storage
├── Replication: Asynchronous (15-min lag)
├── RPO: 15 minutes (max data loss)
├── RTO: 2 hours (switchover time)
└── Testing: Quarterly DR drills
```

---

## AI Processing Infrastructure

### Edge AI vs. Cloud AI

```
┌────────────────────────────────────────────────────────────────┐
│              AI PROCESSING DECISION TREE                        │
└────────────────────────────────────────────────────────────────┘

Camera with Edge AI (Embedded GPU)
├── Capabilities:
│   ├── Object detection (person, vehicle)
│   ├── Motion detection (advanced)
│   ├── Line crossing detection
│   └── Intrusion detection
├── Latency: <50ms
├── Privacy: No video leaves camera
└── Cost: +$200 per camera

        │ IF advanced AI needed
        ▼

NVR with GPU (NVIDIA T4)
├── Capabilities:
│   ├── All edge AI features
│   ├── Facial recognition
│   ├── License plate recognition
│   ├── Behavior analysis
│   └── Crowd counting
├── Latency: 100-500ms
├── Cameras: Process 50-100 streams
└── Cost: $2,000 (GPU card)

        │ IF custom models needed
        ▼

Cloud AI (GPU Cluster)
├── Capabilities:
│   ├── Custom trained models
│   ├── Natural language video search
│   ├── Advanced behavior prediction
│   └── Forensic video enhancement
├── Latency: 1-5 seconds
├── Cameras: Unlimited (scalable)
└── Cost: $5,000+/month (GPU instances)

Decision Matrix:
Use Edge AI for:
├── Real-time alerts (intrusion, line crossing)
├── Privacy-sensitive areas (no video upload)
└── Low-bandwidth locations

Use NVR GPU for:
├── Most deployments (best balance)
├── Facial recognition (known watchlist)
└── LPR (parking, access control)

Use Cloud AI for:
├── Post-event analysis
├── Custom model training
└── Large-scale deployments (1,000+ cameras)
```

### Object Detection Pipeline

```
Video Frame → AI Processing
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                 OBJECT DETECTION FLOW                        │
└─────────────────────────────────────────────────────────────┘

Step 1: Frame Extraction
Camera streams @ 20 fps
        │
        │ Sample: 1 fps (analyze every 20th frame)
        ▼
Step 2: Preprocessing
├── Resize: 2688×1520 → 640×640 (for YOLO input)
├── Normalize: Pixel values 0-255 → 0-1
└── Batch: Group 8 frames (GPU efficiency)
        │
        ▼
Step 3: Object Detection (YOLOv8)
Run inference on GPU:
├── Input: 640×640 × 3 channels (RGB)
├── Output: Bounding boxes + class labels + confidence
├── Classes: person, car, truck, bicycle, etc. (80 classes)
└── Latency: 10ms per frame (GPU)
        │
        ▼
Step 4: Filtering
├── Confidence threshold: >0.7 (reject low confidence)
├── NMS (Non-Max Suppression): Remove duplicate boxes
└── ROI (Region of Interest): Ignore certain areas
        │
        ▼
Step 5: Tracking
├── Assign unique ID to each object
├── Track across frames (Kalman filter)
├── Calculate trajectory, speed, dwell time
└── Detect events: loitering, wrong direction, etc.
        │
        ▼
Step 6: Event Generation
IF event detected:
  ├── Generate alert
  ├── Save video clip (10s before + 30s after)
  ├── Log to database
  └── Notify operators (push notification)
        │
        ▼
Step 7: Analytics Storage
INSERT INTO detections (
  camera_id,
  timestamp,
  object_type,
  confidence,
  bounding_box,
  track_id,
  event_type
);
        │
        ▼
Step 8: Dashboard Update
WebSocket push to connected clients:
"Camera 42: Person detected in restricted area"

Total Latency: 100-200ms (frame to alert)
```

---

## Network Security

### Camera Network Isolation

```
Security Zones:

ZONE 0: CAMERA VLAN (10.20.10.0/22)
├── Trust Level: Low (cameras are IoT devices)
├── Segmentation: Isolated from corporate network
├── Firewall Rules:
│   ├── ALLOW: Cameras → NVR (RTSP, ONVIF)
│   ├── ALLOW: NVR → Cameras (configuration, PTZ)
│   ├── BLOCK: Cameras → Internet
│   ├── BLOCK: Cameras → Corporate network
│   └── BLOCK: Camera-to-camera communication
└── Monitoring: IDS/IPS on VLAN

ZONE 1: NVR & STORAGE (10.20.20.0/24)
├── Trust Level: Medium (critical infrastructure)
├── Firewall Rules:
│   ├── ALLOW: Camera VLAN → NVR (inbound streams)
│   ├── ALLOW: NVR → Internet (cloud backup)
│   ├── ALLOW: Management VLAN → NVR (admin)
│   └── BLOCK: All other inbound
└── Hardening: OS patching, strong passwords, MFA

ZONE 2: MANAGEMENT (10.0.30.0/24)
├── Trust Level: High (authorized users only)
├── Firewall Rules:
│   ├── ALLOW: Authenticated users → VMS
│   ├── ALLOW: VMS → NVR (video retrieval)
│   ├── ALLOW: Admins → All systems (SSH, HTTPS)
│   └── REQUIRE: VPN for remote access
└── Access Control: Role-based (RBAC)

Camera Hardening Checklist:
├── Change default credentials
├── Disable unused services (Telnet, FTP)
├── Enable HTTPS for camera web interface
├── Use strong ONVIF passwords
├── Firmware updates (quarterly)
├── Certificate-based authentication (where supported)
└── VLAN isolation (no direct internet access)
```

---

## Redundancy & High Availability

```
Component-Level Redundancy:

CAMERAS
├── Critical areas: 2 overlapping cameras
├── Failover: If Camera A fails, Camera B covers area
└── Monitoring: Alert if camera offline >5 minutes

NETWORK SWITCHES
├── Core switch: Redundant power supplies
├── Access switches: Redundant uplinks (LACP)
└── Failover: Spanning Tree Protocol (STP) <30s

NVR SERVERS
├── Deployment: Active-active cluster (2 servers)
├── Load balancing: Each records 50% of cameras
├── Failover: If NVR1 fails, NVR2 takes over all cameras
├── Recording gap: <10 seconds (buffering)
└── Storage replication: Real-time sync between NVRs

STORAGE
├── RAID 6: Survives 2 drive failures
├── Hot spares: 2 spare drives per array
├── Backup: Nightly to cloud (AWS S3)
└── Monitoring: S.M.A.R.T. alerts for drive health

POWER
├── UPS: 1-hour battery backup for all equipment
├── Generator: Kicks in after 60 seconds
└── Critical cameras: Separate UPS per PoE switch

NETWORK CONNECTIVITY
├── Dual ISPs: Primary (1 Gbps fiber) + Backup (500 Mbps cable)
├── BGP: Automatic failover between ISPs
└── Downtime: <60 seconds during ISP failure
```

---

## Deployment Scenarios

### Small Business (50 Cameras)

**Equipment:**
- 50× IP Cameras (4MP): $7,500
- 2× PoE Switches (48-port): $2,500
- 1× NVR Server (48TB): $5,000
- **Total Hardware: $15,000**

**Recurring:**
- Cloud backup (2 TB): $50/month
- Support: $100/month
- **Annual Operating: $1,800**

**Total First Year: $16,800**

### Enterprise Campus (500 Cameras)

**Equipment:**
- 500× IP Cameras: $75,000
- 20× PoE Switches: $50,000
- 5× NVR Servers: $50,000
- 3× GPU Nodes (AI): $60,000
- **Total Hardware: $235,000**

**Recurring:**
- Cloud backup (50 TB): $1,200/month
- Support: $2,000/month
- **Annual Operating: $38,400**

**Total First Year: $273,400**

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Next Document**: [OS-SENTINEL Logical Topology](./OS-SENTINEL_Logical_Topology.md)
