---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: 57d57db8-093c-4170-afe9-a9c7b11ce4a9
original_filename: OS-GUARDIAN_Network_Topology.md
created_at: 2026-03-04T20:35:38.221617+00:00
content_hash: a82423bf1ca1topic: retrieval-scenarios-warm
topic: opensecure-guardian-sentinel-topology
---

# OS-GUARDIAN Network Topology
## Security Personnel Network & Body Camera Infrastructure

**Document Type**: Network Topology Specification  
**Version**: 1.0  
**Date**: December 2024  
**Classification**: Technical Documentation  
**Audience**: Network Architects, Security Directors, IT Operations

---

## Executive Summary

### Network Architecture Philosophy

OS-GUARDIAN implements a **secure, evidence-grade network architecture** designed specifically for law enforcement and security operations. Core principles:

- **Chain of Custody**: Cryptographic verification of all evidence from capture to storage
- **High Bandwidth**: Support for real-time video streaming from multiple body cameras
- **Offline Resilience**: Officers record for full shifts without network connectivity
- **Secure Upload**: Encrypted transfer with integrity verification
- **Compliance-Ready**: Meets CJIS, HIPAA, and legal discovery requirements

### Network Scale Characteristics

| Deployment Size | Officers | Cameras | Daily Data | Storage | Annual Cost |
|-----------------|----------|---------|------------|---------|-------------|
| Small (10-50) | 10-50 | 10-50 | 500 GB | 20 TB | $50,000 |
| Medium (50-200) | 50-200 | 50-200 | 2 TB | 80 TB | $200,000 |
| Large (200-1000) | 200-1,000 | 200-1,000 | 10 TB | 400 TB | $1,000,000 |
| Enterprise (1000+) | 1,000+ | 1,000+ | 50+ TB | 2+ PB | $5,000,000+ |

---

## Network Architecture Overview

### Three-Tier Evidence Management Design

```
┌────────────────────────────────────────────────────────────────────┐
│                    TIER 1: FIELD OPERATIONS                         │
│                    (On-Officer Equipment)                           │
└────────────────────────────────────────────────────────────────────┘

Body Camera (Worn by Officer)
├── Hardware: Axon Body 3 or Wolfcom Halo Police Cam
├── Storage: 128GB internal (12-16 hours HD video)
├── Connectivity:
│   ├── WiFi (802.11ac): Auto-upload at station
│   ├── 4G LTE (optional): Live streaming
│   └── Bluetooth: Pair with officer phone/radio
├── GPS: Embedded (logs location with video)
└── Encryption: AES-256 (hardware-accelerated)

Officer Workstation (Patrol Vehicle)
├── Laptop: Panasonic Toughbook
├── Network: 4G LTE modem + WiFi hotspot
├── VPN: WireGuard tunnel to HQ
├── Software:
│   ├── Report writing application
│   ├── Evidence upload client
│   └── CAD integration (dispatch)
└── IP: 10.9.{vehicle_id}.10 (via VPN)

Mobile Device (Officer's Phone)
├── OS: iOS / Android
├── App: Guardian Mobile
├── Features:
│   ├── Camera control (start/stop recording)
│   ├── Upload status monitoring
│   └── Case management
└── Network: Carrier 4G/5G + WiFi

┌────────────────────────────────────────────────────────────────────┐
│                    TIER 2: STATION INFRASTRUCTURE                   │
│                    (Evidence Upload & Local Storage)                │
└────────────────────────────────────────────────────────────────────┘

Docking Station Network (Each Station)
├── VLAN 10: Body Camera Docking (10.10.10.0/24)
│   ├── Docking Stations: 10.10.10.10-100 (up to 90 cameras)
│   ├── Each dock:
│   │   ├── USB 3.0 data transfer (5 Gbps)
│   │   ├── Power charging (15W per camera)
│   │   └── Ethernet uplink (Gigabit)
│   └── Bandwidth: 10 Gbps aggregate switch uplink
│
├── VLAN 20: Evidence Processing (10.10.20.0/24)
│   ├── Evidence Management Servers (×3)
│   ├── Video transcoding servers (×2)
│   └── Local storage cache (NAS, 100 TB)
│
├── VLAN 30: Officer Workstations (10.10.30.0/24)
│   ├── Report writing PCs
│   ├── Evidence review stations
│   └── Investigator workstations
│
└── VLAN 40: Management (10.10.40.0/24)
    ├── Network monitoring
    ├── Backup servers
    └── Administrative systems

┌────────────────────────────────────────────────────────────────────┐
│                    TIER 3: CENTRAL DATA CENTER                      │
│                    (Long-Term Evidence Storage & Analytics)         │
└────────────────────────────────────────────────────────────────────┘

Data Center Network (10.0.0.0/16)
├── VLAN 10: Application Tier (10.0.10.0/24)
│   ├── Guardian API Gateway (×3)
│   ├── Evidence ingestion service (×5)
│   ├── Video analytics (AI processing) (×10)
│   └── Web portal (evidence.department.gov)
│
├── VLAN 20: Database Tier (10.0.20.0/24)
│   ├── PostgreSQL cluster (metadata, chain of custody)
│   ├── MongoDB (video analytics results)
│   └── Elasticsearch (full-text search)
│
├── VLAN 30: Storage Tier (10.0.30.0/24)
│   ├── MinIO object storage (primary, 500 TB)
│   ├── AWS S3 Glacier (archival, unlimited)
│   └── WORM storage (compliance, 100 TB)
│
└── VLAN 40: Security Tier (10.0.40.0/24)
    ├── HSM (Hardware Security Module) for encryption keys
    ├── SIEM (Security Information Event Management)
    ├── Audit log servers
    └── Intrusion detection/prevention

External Integrations:
├── RMS (Records Management System)
├── CAD (Computer-Aided Dispatch)
├── Court E-Filing Systems
└── District Attorney Case Management
```

---

## Body Camera Docking Network

### Docking Station Architecture

```
┌────────────────────────────────────────────────────────────────┐
│              DOCKING STATION INFRASTRUCTURE                     │
└────────────────────────────────────────────────────────────────┘

Physical Layout (Locker Room / Evidence Room):
┌──────────────────────────────────────────────────────────────┐
│                                                               │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐         │
│  │Dock 1│  │Dock 2│  │Dock 3│  │Dock 4│  │Dock 5│         │
│  │  USB │  │  USB │  │  USB │  │  USB │  │  USB │         │
│  └───┬──┘  └───┬──┘  └───┬──┘  └───┬──┘  └───┬──┘         │
│      │         │         │         │         │             │
│      └─────────┴─────────┴─────────┴─────────┘             │
│                        │                                    │
│                 ┌──────▼──────┐                            │
│                 │ USB Hub     │                            │
│                 │ 10-port     │                            │
│                 │ Powered     │                            │
│                 └──────┬──────┘                            │
│                        │ USB 3.0 to Ethernet Adapter       │
│                        │                                    │
│                 ┌──────▼──────────┐                        │
│                 │ Network Switch  │                        │
│                 │ Gigabit Ethernet│                        │
│                 │ (VLAN 10)       │                        │
│                 └──────┬──────────┘                        │
│                        │                                    │
│                        │ 10 Gbps Uplink                     │
│                        ▼                                    │
│                  Core Switch                                │
│                  ↓                                          │
│            Evidence Servers                                 │
└──────────────────────────────────────────────────────────────┘

Data Flow: Camera Dock → Evidence Server

Step 1: Officer Returns from Shift
Officer docks body camera in charging station
        │
        │ USB 3.0 connection established
        │ Camera detected by docking management software
        ▼
Step 2: Authentication
System verifies:
├── Officer badge ID (NFC/RFID)
├── Camera serial number
├── Cryptographic signature (tamper-proof)
└── Last sync timestamp
        │
        │ IF authentication fails → Alert + manual review
        ▼
Step 3: Data Transfer
Camera → Dock → Switch → Evidence Server
        │
        │ Transfer specs:
        │ • Protocol: USB Mass Storage (MTP)
        │ • Speed: 300 MB/s (USB 3.0)
        │ • Typical: 10 GB (HD video, 8-hour shift)
        │ • Duration: ~30-40 seconds
        │
        │ Progress tracked:
        │ • LED indicator on dock (blue = transferring)
        │ • Dashboard shows: "Officer 123 - 45% uploaded"
        ▼
Step 4: Integrity Verification
Evidence server calculates:
├── SHA-256 hash of each video file
├── Compares with camera's embedded hash
└── IF mismatch → Flag as corrupted, retry
        │
        │ Store metadata:
        │ {
        │   officer_id, camera_id, timestamp,
        │   file_hash, file_size, location_gps,
        │   upload_station, upload_time
        │ }
        ▼
Step 5: Cloud Upload (Background)
Evidence server → Data center MinIO
        │
        │ Upload bandwidth: 1 Gbps shared
        │ Priority queue:
        │   1. Critical incidents (flagged)
        │   2. Recent footage (<24 hours)
        │   3. Bulk backlog
        │
        │ Encryption: TLS 1.3 in transit, AES-256 at rest
        ▼
Step 6: Dock Complete
LED indicator: Green (success) or Red (error)
Officer notified via mobile app: "Upload complete"
Camera remains docked for charging (next shift)
```

### Network Performance Requirements

```
Scenario: 50 Officers End-of-Shift Upload (Worst Case)

Assumptions:
├── 50 cameras dock simultaneously (6 PM shift change)
├── Average video per camera: 10 GB (8-hour shift, HD)
├── Total data: 500 GB
└── Target upload time: 30 minutes (acceptable wait)

Bandwidth Calculation:
500 GB / 30 minutes = 16.67 GB/min = 278 MB/s = 2.22 Gbps

Network Design:
├── Docking VLAN: 10 Gbps switch uplink (headroom: 4.5×)
├── Station-to-DC WAN: 10 Gbps fiber (dedicated)
└── Result: All 50 cameras upload in parallel without bottleneck

Actual Performance:
├── Parallel USB 3.0 transfers: 300 MB/s each (limited by camera)
├── Network not bottleneck (10 Gbps > 2.22 Gbps required)
├── Typical: 25-35 minutes for 50 simultaneous uploads
└── Peak: 60 cameras can upload concurrently
```

---

## Live Streaming Infrastructure

### 4G/5G Live Feed Architecture

```
┌────────────────────────────────────────────────────────────────┐
│            LIVE STREAMING NETWORK TOPOLOGY                      │
└────────────────────────────────────────────────────────────────┘

Critical Incident: Officer activates live stream

Body Camera
├── Records locally (always, even if no network)
├── IF live stream activated:
│   ├── Encodes video: H.264, 720p @ 15 fps, 1 Mbps
│   ├── Buffers: 5-second delay (for smoothing)
│   └── Transmits via: 4G LTE modem (embedded or tethered)
└── GPS: Embeds location metadata

        │ 4G LTE (1-10 Mbps uplink)
        ▼
Carrier Network (Verizon / AT&T)
        │
        │ VPN Tunnel (WireGuard)
        │ Encryption: ChaCha20-Poly1305
        ▼
VPN Gateway (Data Center)
10.0.40.10 - WireGuard endpoint
        │
        │ Forwards stream to media server
        ▼
Media Streaming Server (Wowza / Janus WebRTC)
├── IP: 10.0.10.50
├── Protocols: RTMP (ingest), WebRTC (playback)
├── Transcoding: 1080p → 720p, 480p, 360p (adaptive)
└── Storage: Record stream to disk (backup)
        │
        │ WebRTC (low latency: 1-3 seconds)
        │ OR HLS (higher latency: 10-30 seconds, better compatibility)
        ▼
Dispatch Console / Command Center
├── Web UI: https://command.department.gov/live
├── Map view: Shows officer location + live feed
├── Audio: Two-way (officer can hear dispatcher)
└── Recording: Automatically saved to evidence system

Use Cases:
├── Active Shooter: Command sees real-time situation
├── Pursuit: Supervisors monitor officer safety
├── Protest: Incident commanders coordinate response
└── Training: Review live feedback during exercises

Bandwidth Requirements:
├── Per stream: 1 Mbps (720p @ 15 fps)
├── Concurrent streams: Typically 5-10, max 50 (major incident)
├── Data center ingest: 50 Mbps (50 streams)
└── Playback: 50× viewers × 1 Mbps = 50 Mbps (internal network)

Cost:
├── Body camera with 4G: $150/camera premium
├── Cellular data plan: Unlimited ($50/month per camera)
├── 50 cameras: $2,500/month cellular costs
└── Media server: $500/month (cloud-hosted)
```

---

## Evidence Storage Network

### Tiered Storage Architecture

```
┌────────────────────────────────────────────────────────────────┐
│              EVIDENCE STORAGE TIERS                             │
└────────────────────────────────────────────────────────────────┘

Tier 1: Hot Storage (Immediate Access)
├── Technology: MinIO on NVMe SSD
├── Capacity: 500 TB (90 days of footage)
├── Access Time: <100ms
├── Use Case: Recent evidence, active investigations
├── Cost: $150/TB = $75,000
└── Network: 10 Gbps Ethernet

        │ After 90 days (automated)
        ▼
Tier 2: Warm Storage (Frequent Access)
├── Technology: MinIO on HDD (RAID 6)
├── Capacity: 2 PB (1-3 years of footage)
├── Access Time: <2 seconds
├── Use Case: Closed cases, occasional review
├── Cost: $30/TB = $60,000
└── Network: 10 Gbps Ethernet

        │ After 3 years (policy-based)
        ▼
Tier 3: Cold Storage (Archival)
├── Technology: AWS S3 Glacier Deep Archive
├── Capacity: Unlimited (10+ years retention)
├── Access Time: 12-48 hours (retrieval)
├── Use Case: Legal compliance, discovery
├── Cost: $1/TB/month = $1,000/month (for 1 PB)
└── Network: Internet (1 Gbps dedicated)

        │ After retention period (e.g., 7 years)
        ▼
Tier 4: Destruction (Secure Deletion)
├── Method: DoD 5220.22-M (7-pass overwrite)
├── Logging: Deletion certificates generated
├── Audit: Requires approval from legal/records
└── Compliance: CJIS, state retention laws

Storage Lifecycle Policy (Example):
{
  "rules": [
    {
      "id": "hot-to-warm",
      "filter": {"age_days": 90},
      "action": "move",
      "destination": "warm_storage",
      "priority": "low"
    },
    {
      "id": "warm-to-cold",
      "filter": {"age_days": 1095},  # 3 years
      "action": "move",
      "destination": "glacier",
      "priority": "low"
    },
    {
      "id": "critical-retain",
      "filter": {
        "tags": ["officer_involved_shooting", "homicide"]
      },
      "action": "retain",
      "duration": "permanent"
    }
  ]
}
```

### WORM Storage (Write-Once Read-Many)

```
Compliance Requirement: Evidence cannot be altered or deleted

Implementation:
├── Hardware: IBM TS4500 Tape Library (WORM LTO-9 tapes)
├── Capacity: 100 TB (critical incidents only)
├── Certification: SEC 17a-4, FINRA, CJIS
└── Retention: 25 years (permanent records)

WORM Write Process:
1. Critical incident identified (OIS, homicide, etc.)
2. Evidence flagged for WORM storage
3. Copy created: MinIO → WORM tape
4. Verification: Hash comparison (integrity check)
5. Certificate generated: Proof of immutability
6. Tape physically stored: Off-site vault

WORM Retrieval Process:
1. Legal request submitted (court order, discovery)
2. Tape retrieved from vault (2-4 hours)
3. Evidence copied: Tape → staging server
4. Provided to requester: Encrypted USB drive or secure FTP
5. Chain of custody logged: Who, when, why
```

---

## Security & Access Control

### Network Security Zones

```
Zone 0: Internet (Untrusted)
├── Threats: Attacks, unauthorized access
├── Protection: Cloud WAF (Cloudflare), DDoS mitigation
└── Allowed: HTTPS (443) to evidence portal only

        │ Firewall (pfSense)
        ▼
Zone 1: DMZ (Public-Facing Services)
├── Evidence Portal (10.0.10.20)
├── API Gateway (10.0.10.10)
└── Firewall Rules:
    • Allow: HTTPS (443) from Internet
    • Allow: SSH (22) from VPN only
    • Block: All other inbound

        │
        ▼
Zone 2: Application Tier (Internal Services)
├── Evidence Management (10.0.10.30-35)
├── Video Analytics (10.0.10.40-50)
├── Transcoding Servers (10.0.10.60-65)
└── Firewall Rules:
    • Allow: From Zone 1 (API Gateway) only
    • Allow: HTTPS (443), gRPC (50051)
    • Block: Direct internet access

        │
        ▼
Zone 3: Database Tier (Sensitive Data)
├── PostgreSQL (10.0.20.10-12)
├── MongoDB (10.0.20.20-22)
└── Firewall Rules:
    • Allow: From Zone 2 (Applications) only
    • Allow: PostgreSQL (5432), MongoDB (27017)
    • Block: All other access

        │
        ▼
Zone 4: Storage Tier (Evidence Files)
├── MinIO (10.0.30.10-20)
├── WORM Tape Library (10.0.30.100)
└── Firewall Rules:
    • Allow: From Zone 2 (Applications) only
    • Allow: S3 API (9000), Admin (9001)
    • Block: Direct file access

        │
        ▼
Zone 5: Security/Audit (High Security)
├── HSM (10.0.40.50)
├── SIEM (10.0.40.60)
├── Audit Servers (10.0.40.70)
└── Firewall Rules:
    • Allow: From all zones (read-only logs)
    • Allow: Admin access from jump host only
    • Block: All other access
```

### User Access Control

```
Role-Based Access Control (RBAC):

Role: OFFICER
├── Permissions:
│   ├── Upload own body camera footage
│   ├── View own footage (after shift)
│   ├── Tag/flag incidents in own videos
│   └── Submit evidence for cases
├── Restrictions:
│   ├── Cannot view other officers' footage
│   ├── Cannot delete any footage
│   └── Cannot edit metadata (read-only)

Role: SUPERVISOR
├── Permissions:
│   ├── All OFFICER permissions
│   ├── View footage from officers under supervision
│   ├── Approve evidence release requests
│   └── Generate activity reports
├── Restrictions:
│   ├── Cannot delete footage (admin only)
│   └── Cannot access IA investigations

Role: INVESTIGATOR
├── Permissions:
│   ├── Search all footage by case number
│   ├── View footage related to assigned cases
│   ├── Export evidence clips for court
│   ├── Add case notes/timestamps
│   └── Request footage from other agencies
├── Restrictions:
│   ├── Cannot view unrelated footage
│   └── Cannot delete footage

Role: INTERNAL_AFFAIRS
├── Permissions:
│   ├── Access any footage (with case justification)
│   ├── View officer-disabled footage (privacy flags)
│   ├── Audit officer camera usage patterns
│   └── Generate compliance reports
├── Restrictions:
│   ├── All access logged and audited
│   └── Requires two-person integrity (co-approval)

Role: ADMIN
├── Permissions:
│   ├── Full system access
│   ├── User management
│   ├── Retention policy configuration
│   ├── Audit log access
│   └── Evidence deletion (with audit trail)
├── Restrictions:
│   ├── All actions logged (immutable)
│   ├── Deletion requires multi-factor auth
│   └── Regular background checks required

Role: PUBLIC (Redacted Access)
├── Permissions:
│   ├── Submit FOIA/public records request
│   ├── View redacted footage (approved only)
│   └── Download approved clips
├── Restrictions:
│   ├── Heavy redaction (faces, audio, PII)
│   ├── Watermarked videos
│   └── Usage tracking/logging
```

---

## Redundancy & Disaster Recovery

```
Component-Level Redundancy:

BODY CAMERAS
├── Local storage: 128 GB (12-16 hours)
├── Offline operation: Full shift without network
├── Failsafe: If upload fails, camera retains data
└── Recovery: Retry upload at next dock

DOCKING STATIONS
├── Deployment: 2× capacity (100% redundancy)
├── Failover: If dock fails, use adjacent dock
└── Maintenance: Hot-swappable, zero downtime

EVIDENCE SERVERS (Station-Level)
├── Deployment: 2 servers (active-active)
├── Replication: Real-time sync between servers
├── Storage: RAID 6 (survives 2 drive failures)
└── Failover: Automatic (<30 seconds)

DATABASE (Data Center)
├── PostgreSQL: Primary + 2 replicas
├── Replication: Synchronous (zero data loss)
├── Failover: Patroni auto-promotion (<30s)
└── Backup: Hourly incremental, daily full

OBJECT STORAGE (MinIO)
├── Deployment: 10-node erasure-coded cluster
├── Redundancy: EC 6+4 (survives 4 node failures)
├── Self-healing: Auto-rebuild on failure
└── Backup: Replicate to AWS S3 (nightly)

DISASTER RECOVERY
├── Backup Site: 100 miles from primary
├── RPO: 1 hour (max data loss)
├── RTO: 4 hours (max downtime)
├── Test: Quarterly failover drills
└── Evidence Priority: Critical incidents replicate real-time
```

---

## Deployment Scenarios

### Small Department (50 Officers)

**Equipment:**
- 50× Body cameras: $25,000
- 60× Docking stations (20% spare): $12,000
- 2× Evidence servers: $10,000
- Network switches: $5,000
- **Total Hardware: $52,000**

**Recurring:**
- Cloud storage (20 TB): $500/month
- Cellular data (optional): $2,500/month
- Software licenses: $200/month
- **Annual Operating: $38,400**

**Total First Year: $90,400**

### Large Department (500 Officers)

**Equipment:**
- 500× Body cameras: $250,000
- 600× Docking stations: $120,000
- 10× Evidence servers: $50,000
- Network infrastructure: $50,000
- **Total Hardware: $470,000**

**Recurring:**
- Cloud storage (200 TB): $5,000/month
- Cellular data: $25,000/month
- Software licenses: $2,000/month
- **Annual Operating: $384,000**

**Total First Year: $854,000**

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Next Document**: [OS-GUARDIAN Logical Topology](./OS-GUARDIAN_Logical_Topology.md)
