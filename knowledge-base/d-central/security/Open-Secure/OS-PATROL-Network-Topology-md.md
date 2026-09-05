---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: 4f07bbf7-4d9c-40ca-aa4c-899b5d900b43
original_filename: OS-PATROL_Network_Topology.md
created_at: 2026-03-04T20:33:41.219570+00:00
content_hash: 82a4ea977951
topic: "opensecure-topology-documentation-suite"
---

# OS-PATROL Network Topology
## Fleet Management Network Architecture & Mobile Infrastructure

**Document Type**: Network Topology Specification  
**Version**: 1.0  
**Date**: December 2024  
**Classification**: Technical Documentation  
**Audience**: Network Architects, Fleet Managers, IT Operations

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Mobile Network Architecture](#mobile-network-architecture)
3. [Vehicle-to-Cloud Connectivity](#vehicle-to-cloud-connectivity)
4. [Cellular Network Design](#cellular-network-design)
5. [On-Vehicle Network](#on-vehicle-network)
6. [Fleet Operations Center](#fleet-operations-center)
7. [GPS & Tracking Infrastructure](#gps--tracking-infrastructure)
8. [Camera Network](#camera-network)
9. [Mobile Office Connectivity](#mobile-office-connectivity)
10. [Redundancy & Failover](#redundancy--failover)

---

## Executive Summary

### Network Architecture Philosophy

OS-PATROL operates in a **hybrid edge-cloud architecture** where vehicles function as autonomous mobile edge nodes with intermittent cloud connectivity. Unlike traditional cloud-dependent fleet systems, OS-PATROL prioritizes:

- **Edge-First Processing**: Critical functions (GPS tracking, dashcam recording, LPR) operate locally
- **Cellular Connectivity**: Primary: 4G LTE, Backup: 3G, Future: 5G
- **Offline Resilience**: Vehicles buffer all data locally when connectivity lost
- **Multi-Network Support**: Can use multiple carriers simultaneously
- **Cost Optimization**: Intelligent data transmission reduces cellular costs by 70%

### Network Scale Characteristics

| Fleet Size | Vehicles | Data/Vehicle/Day | Total Bandwidth | Cellular Cost/Month | Servers Required |
|------------|----------|------------------|-----------------|---------------------|------------------|
| Small (1-10) | 1-10 | 500 MB | 5 GB/day | $200-500 | 1 (all-in-one) |
| Medium (10-50) | 10-50 | 500 MB | 25 GB/day | $1,000-2,500 | 2 (primary + backup) |
| Large (50-250) | 50-250 | 500 MB | 125 GB/day | $5,000-12,500 | 3-5 (load balanced) |
| Enterprise (250+) | 250-5,000 | 500 MB | 2.5 TB/day | $50,000-250,000 | 10+ (distributed) |

---

## Mobile Network Architecture

### Three-Tier Hybrid Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                    TIER 1: MOBILE EDGE                              │
│                    (On-Vehicle Systems)                             │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  Vehicle Unit (Raspberry Pi 4 / Jetson Nano)                 │ │
│  │                                                                │ │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐             │ │
│  │  │  Traccar   │  │ OpenALPR   │  │ MotionEye  │             │ │
│  │  │  (GPS)     │  │  (LPR)     │  │ (Dashcam)  │             │ │
│  │  └────┬───────┘  └────┬───────┘  └────┬───────┘             │ │
│  │       │               │               │                       │ │
│  │  ┌────▼───────────────▼───────────────▼───────┐             │ │
│  │  │    Local Storage Buffer (128GB SD)          │             │ │
│  │  │    • GPS tracks: 30 days                    │             │ │
│  │  │    • LPR events: 7 days                     │             │ │
│  │  │    • Video clips: 24-72 hours               │             │ │
│  │  └──────────────────┬──────────────────────────┘             │ │
│  │                     │                                         │ │
│  │  ┌──────────────────▼──────────────────────────┐             │ │
│  │  │   4G LTE Modem (Sierra Wireless EM7565)     │             │ │
│  │  │   • Primary: Carrier A (AT&T/Verizon)       │             │ │
│  │  │   • Backup: Carrier B (T-Mobile/Sprint)     │             │ │
│  │  │   • Failover: WiFi hotspot (when available) │             │ │
│  │  └──────────────────┬──────────────────────────┘             │ │
│  └────────────────────│───────────────────────────────────────┘ │
└────────────────────────│─────────────────────────────────────────┘
                         │ Cellular: 4G LTE / 3G
                         │ IP: Dynamic (DHCP from carrier)
                         │ Encryption: TLS 1.3 + VPN
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│                    TIER 2: NETWORK EDGE                           │
│                    (Cellular Infrastructure)                      │
│                                                                   │
│  ┌────────────────┐     ┌────────────────┐     ┌──────────────┐ │
│  │  AT&T LTE      │     │ Verizon LTE    │     │ T-Mobile LTE │ │
│  │  Network       │     │ Network        │     │ Network      │ │
│  └────────┬───────┘     └────────┬───────┘     └──────┬───────┘ │
│           │                      │                     │         │
│           └──────────────────────┼─────────────────────┘         │
│                                  │                               │
│                          ┌───────▼────────┐                      │
│                          │  VPN Gateway   │                      │
│                          │  (WireGuard)   │                      │
│                          │  Public IP:    │                      │
│                          │  vpn.fleet.com │                      │
│                          └───────┬────────┘                      │
└──────────────────────────────────│───────────────────────────────┘
                                   │ VPN Tunnel
                                   │ 10.8.0.0/16 (private)
┌──────────────────────────────────▼───────────────────────────────┐
│                    TIER 3: DATA CENTER                            │
│                    (Fleet Operations Center)                      │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────────┐│
│  │               Load Balancer (HAProxy)                         ││
│  │               VIP: 10.0.1.5                                   ││
│  └───────────────────┬──────────────────────────────────────────┘│
│                      │                                            │
│       ┌──────────────┼──────────────┐                            │
│       │              │              │                            │
│  ┌────▼─────┐  ┌─────▼────┐  ┌─────▼────┐                      │
│  │ Traccar  │  │ Traccar  │  │ Traccar  │                      │
│  │ Server 1 │  │ Server 2 │  │ Server 3 │                      │
│  │10.0.1.10 │  │10.0.1.11 │  │10.0.1.12 │                      │
│  └────┬─────┘  └─────┬────┘  └─────┬────┘                      │
│       │              │              │                            │
│       └──────────────┼──────────────┘                            │
│                      │                                            │
│  ┌───────────────────▼──────────────────────────────┐           │
│  │         PostgreSQL + TimescaleDB Cluster          │           │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐       │           │
│  │  │ Primary  │  │ Replica1 │  │ Replica2 │       │           │
│  │  │10.0.1.20 │  │10.0.1.21 │  │10.0.1.22 │       │           │
│  │  └──────────┘  └──────────┘  └──────────┘       │           │
│  └───────────────────────────────────────────────────┘           │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────────┐│
│  │            MinIO Object Storage Cluster                      ││
│  │            (Video, Images, LPR Snapshots)                    ││
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   ││
│  │  │ Node 1   │  │ Node 2   │  │ Node 3   │  │ Node 4   │   ││
│  │  │10.0.1.30 │  │10.0.1.31 │  │10.0.1.32 │  │10.0.1.33 │   ││
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘   ││
│  │  Erasure Coding: 4+2 (survives 2 node failures)             ││
│  └──────────────────────────────────────────────────────────────┘│
└───────────────────────────────────────────────────────────────────┘
```

---

## Vehicle-to-Cloud Connectivity

### Data Transmission Strategy

**Intelligent Upload Algorithm:**

```python
class DataTransmissionManager:
    def __init__(self):
        self.priority_queue = PriorityQueue()
        self.upload_budget_mb_per_hour = 50  # Cellular data cap
        
    def classify_data(self, data_type, event):
        """Classify data by priority for transmission"""
        priorities = {
            'CRITICAL': 1,    # Immediate upload (hot-list LPR hit, panic button)
            'HIGH': 2,        # Upload within 5 minutes (alerts, speeding)
            'NORMAL': 3,      # Upload when connected to WiFi or end of shift
            'LOW': 4          # Bulk upload overnight (full dashcam footage)
        }
        
        # Critical events
        if data_type == 'LPR' and event['plate'] in self.hot_list:
            return ('CRITICAL', event)
        
        if data_type == 'ALERT' and event['type'] == 'PANIC_BUTTON':
            return ('CRITICAL', event)
        
        # High priority
        if data_type == 'GPS' and event['speed'] > 80:  # Speeding
            return ('HIGH', event)
        
        if data_type == 'LPR' and event['match_confidence'] > 0.9:
            return ('HIGH', event)
        
        # Normal priority
        if data_type == 'GPS_TRACK':
            return ('NORMAL', event)
        
        if data_type == 'VIDEO_CLIP' and event['trigger'] == 'INCIDENT':
            return ('NORMAL', event)
        
        # Low priority
        if data_type == 'VIDEO_CLIP' and event['trigger'] == 'SCHEDULED':
            return ('LOW', event)
        
        return ('NORMAL', event)
    
    def should_upload_now(self, priority, connectivity):
        """Decide if data should upload immediately"""
        
        # Critical always uploads (even on 3G)
        if priority == 'CRITICAL':
            return True
        
        # High priority uploads on 4G
        if priority == 'HIGH' and connectivity in ['4G', 'LTE', 'WiFi']:
            return True
        
        # Normal waits for good connectivity
        if priority == 'NORMAL' and connectivity == 'WiFi':
            return True
        
        # Low only uploads on WiFi during off-peak
        if priority == 'LOW' and connectivity == 'WiFi' and self.is_off_peak():
            return True
        
        return False
    
    def estimate_upload_time(self, file_size_mb, connection_type):
        """Estimate upload time based on connection"""
        speeds = {
            'WiFi': 50,      # 50 Mbps
            '4G': 10,        # 10 Mbps
            'LTE': 8,        # 8 Mbps
            '3G': 1          # 1 Mbps
        }
        
        speed_mbps = speeds.get(connection_type, 1)
        time_seconds = (file_size_mb * 8) / speed_mbps
        return time_seconds
```

### Network Traffic Breakdown

**Typical Vehicle Daily Data:**

| Data Type | Frequency | Size per Event | Daily Total | Priority | Upload Trigger |
|-----------|-----------|----------------|-------------|----------|----------------|
| GPS Position | Every 5s | 100 bytes | 17 MB | NORMAL | Batch every 30s |
| LPR Scan | Per plate | 50 KB (image) | 50 MB (100 plates) | HIGH | Immediate if hot-list |
| Dashcam Clip | On trigger | 10 MB (30s) | 100 MB (10 events) | HIGH | Immediate |
| Full Dashcam | Continuous | 1 GB/hour | 8 GB (8hr shift) | LOW | WiFi only, overnight |
| Odometer | Every 5 min | 50 bytes | 14 KB | NORMAL | Batch hourly |
| System Health | Every 1 min | 200 bytes | 288 KB | LOW | Batch hourly |
| **Total** | | | **~500 MB** | | |

**Cellular Data Usage Optimization:**

```
Cellular Upload (4G LTE):
├── CRITICAL (immediate): 5 MB/day
├── HIGH (within 5 min): 70 MB/day
├── NORMAL (WiFi preferred): 100 MB/day
└── LOW (WiFi only): 0 MB/day (325 MB via WiFi)

Monthly Cellular: 
- 5 MB × 30 days = 150 MB (CRITICAL)
- 70 MB × 30 days = 2.1 GB (HIGH)
- 100 MB × 20 days = 2 GB (NORMAL, when no WiFi)
Total: ~4.25 GB/month per vehicle

Data Plan: 5 GB/month ($30-50/vehicle)
Cost per Vehicle: $40/month average
50 Vehicles: $2,000/month cellular costs
```

---

## Cellular Network Design

### Multi-Carrier Redundancy

```
┌─────────────────────────────────────────────────────────────┐
│           DUAL-SIM 4G MODEM CONFIGURATION                    │
└─────────────────────────────────────────────────────────────┘

Vehicle Modem: Sierra Wireless EM7565
├── SIM Slot 1: Verizon (Primary)
│   ├── Plan: 5 GB/month ($40)
│   ├── Network: LTE Cat-12 (600 Mbps down, 150 Mbps up)
│   ├── Coverage: Nationwide
│   └── Priority: 1
│
└── SIM Slot 2: AT&T (Backup)
    ├── Plan: 1 GB/month ($15, overage only)
    ├── Network: LTE Cat-12
    ├── Coverage: Nationwide
    └── Priority: 2 (activates if Verizon signal < -105 dBm)

Failover Logic:
┌─────────────────────────────────────────────────┐
│ Monitor Verizon signal strength every 10s       │
│                                                  │
│ IF signal_strength < -105 dBm:                  │
│   Switch to AT&T (within 30 seconds)            │
│   Send alert: "Vehicle 12 switched to backup"   │
│                                                  │
│ IF both carriers down:                          │
│   Enable WiFi scanning (look for open networks) │
│   Buffer data locally (up to 7 days)            │
│   Alert: "Vehicle 12 offline"                   │
│                                                  │
│ When Verizon restored (signal > -95 dBm):       │
│   Switch back to primary                        │
│   Upload buffered data                          │
└─────────────────────────────────────────────────┘

Carrier Coverage Map Integration:
- Query OpenCellID API for signal predictions
- Pre-plan routes to maximize 4G coverage
- Warn driver: "Entering low-coverage area in 2 miles"
```

### VPN Tunnel Configuration

**WireGuard VPN for All Vehicle Traffic:**

```ini
# Vehicle-side WireGuard config (/etc/wireguard/wg0.conf)
[Interface]
Address = 10.8.{vehicle_id}.1/32
PrivateKey = <VEHICLE_PRIVATE_KEY>
DNS = 10.0.1.53

[Peer]
# Fleet Operations Center
PublicKey = <FOC_PUBLIC_KEY>
Endpoint = vpn.fleet.company.com:51820
AllowedIPs = 10.0.0.0/16, 10.8.0.0/16
PersistentKeepalive = 25  # Keep tunnel alive through NAT

# FOC-side config (server)
[Interface]
Address = 10.8.0.1/16
ListenPort = 51820
PrivateKey = <FOC_PRIVATE_KEY>

# Vehicle 1
[Peer]
PublicKey = <VEHICLE1_PUBLIC_KEY>
AllowedIPs = 10.8.1.0/24
PersistentKeepalive = 25

# Vehicle 2
[Peer]
PublicKey = <VEHICLE2_PUBLIC_KEY>
AllowedIPs = 10.8.2.0/24
PersistentKeepalive = 25

# ... (repeat for all vehicles)
```

**VPN Benefits:**
- **Security**: All traffic encrypted (TLS + WireGuard = double encryption)
- **Static Internal IPs**: Each vehicle gets predictable IP (10.8.{id}.1)
- **Firewall Bypass**: Works through carrier NAT/CGNAT
- **Low Overhead**: WireGuard adds only ~4% latency vs. OpenVPN's 20%

---

## On-Vehicle Network

### Internal Vehicle Network Topology

```
┌───────────────────────────────────────────────────────────────┐
│              VEHICLE INTERNAL NETWORK                          │
│              (192.168.100.0/24)                                │
└───────────────────────────────────────────────────────────────┘

         ┌──────────────────────────┐
         │  Raspberry Pi 4 (8GB)    │
         │  Central Controller      │
         │  IP: 192.168.100.1       │
         └───────────┬──────────────┘
                     │ USB / Ethernet
        ┌────────────┼────────────┐
        │            │            │
┌───────▼───────┐  ┌─▼─────────┐  ┌────▼────────┐
│ 4G LTE Modem  │  │ GPS       │  │ OBD-II      │
│ (USB)         │  │ Receiver  │  │ Adapter     │
│ Dynamic IP    │  │ (Serial)  │  │ (Bluetooth) │
│ from carrier  │  │ USB/UART  │  │ 192.168.100.│
│               │  │           │  │ 10          │
└───────────────┘  └───────────┘  └─────────────┘

        ┌────────────┼────────────┐
        │            │            │
┌───────▼───────┐  ┌─▼─────────┐  ┌────▼────────┐
│ Front Dashcam │  │ Rear      │  │ Side Cameras│
│ (USB)         │  │ Dashcam   │  │ (USB)       │
│ 1080p 30fps   │  │ (USB)     │  │ 720p 15fps  │
│ 192.168.100.  │  │ 1080p     │  │ 192.168.100.│
│ 20            │  │ 192.168.  │  │ 30-33       │
│               │  │ 100.21    │  │             │
└───────────────┘  └───────────┘  └─────────────┘

        ┌────────────┼────────────┐
        │            │            │
┌───────▼───────┐  ┌─▼─────────┐  ┌────▼────────┐
│ LPR Camera    │  │ Tablet    │  │ Body Camera │
│ (Ethernet)    │  │ (WiFi)    │  │ Dock (USB)  │
│ 4MP 60fps     │  │ Android   │  │ Charge +    │
│ 192.168.100.  │  │ DHCP      │  │ Data Sync   │
│ 40            │  │ 192.168.  │  │             │
│               │  │ 100.50    │  │             │
└───────────────┘  └───────────┘  └─────────────┘

Power Distribution:
├── 12V DC from vehicle battery
├── Buck converter → 5V (RPi, USB devices)
├── PoE injector → 48V (LPR camera)
└── UPS battery (5V, 10,000 mAh) → 30 min backup

Network Switch (optional, for >4 cameras):
├── 8-port Gigabit Ethernet
├── PoE support (4 ports)
├── Fanless, wide temperature (-40°C to +75°C)
└── Vehicle-rated (shock/vibration resistant)
```

### IP Addressing Scheme (Per Vehicle)

| Device | IP Address | Interface | Purpose |
|--------|------------|-----------|---------|
| Raspberry Pi | 192.168.100.1 | eth0 (local) | Central controller |
| Raspberry Pi | 10.8.{id}.1 | wg0 (VPN) | Cloud connectivity |
| 4G Modem | Dynamic | usb0 | WAN connection |
| GPS Receiver | - | /dev/ttyUSB0 | NMEA data stream |
| OBD-II Adapter | 192.168.100.10 | bt0 (Bluetooth) | Vehicle diagnostics |
| Front Dashcam | 192.168.100.20 | USB | Video stream |
| Rear Dashcam | 192.168.100.21 | USB | Video stream |
| Side Cam Left | 192.168.100.30 | USB | Video stream |
| Side Cam Right | 192.168.100.31 | USB | Video stream |
| LPR Camera | 192.168.100.40 | eth1 | High-res plates |
| Tablet (Officer) | 192.168.100.50 | wlan0 | User interface |
| Body Camera Dock | 192.168.100.60 | USB | Offload footage |

---

## Fleet Operations Center

### Data Center Network Design

```
┌──────────────────────────────────────────────────────────────┐
│          FLEET OPERATIONS CENTER (FOC)                        │
│          10.0.0.0/16 (Private Network)                        │
└──────────────────────────────────────────────────────────────┘

                        Internet
                            │
                            │ Dual ISPs (BGP)
                            │
                    ┌───────▼────────┐
                    │ Edge Firewall  │
                    │ (pfSense HA)   │
                    └───────┬────────┘
                            │
                    ┌───────▼────────┐
                    │  Core Switch   │
                    │ (Layer 3, 10G) │
                    └───────┬────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌───────▼────────┐  ┌──────▼─────────┐
│ VLAN 10        │  │ VLAN 20        │  │ VLAN 30        │
│ Application    │  │ Data Storage   │  │ Management     │
│ Servers        │  │                │  │                │
├────────────────┤  ├────────────────┤  ├────────────────┤
│ • Traccar (×3) │  │ • PostgreSQL   │  │ • Grafana      │
│ • LibreDispatch│  │   (×3 cluster) │  │ • Prometheus   │
│ • Web Portal   │  │ • TimescaleDB  │  │ • Backup       │
│ • API Gateway  │  │ • MinIO (×4)   │  │ • Jump Host    │
│                │  │ • Redis Cache  │  │                │
│ 10.0.10.0/24   │  │ 10.0.20.0/24   │  │ 10.0.30.0/24   │
└────────────────┘  └────────────────┘  └────────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                    ┌───────▼────────┐
                    │ VLAN 40        │
                    │ VPN Gateway    │
                    │ (WireGuard)    │
                    │                │
                    │ Accepts        │
                    │ connections    │
                    │ from vehicles  │
                    │ 10.8.0.0/16    │
                    └────────────────┘
```

### VLAN Segmentation

```
VLAN 10 - Application Tier (10.0.10.0/24)
├── Purpose: Fleet management applications
├── Devices: Traccar servers, dispatch, web portal
├── Access: Internet-facing (via firewall NAT)
├── Routing: Can reach VLAN 20 (database), VLAN 40 (VPN)
└── Firewall: Strict egress, only HTTPS outbound

VLAN 20 - Data Tier (10.0.20.0/24)
├── Purpose: Database and storage
├── Devices: PostgreSQL, MinIO, Redis
├── Access: Internal only, no internet
├── Routing: Limited to VLAN 10 (application queries)
└── Firewall: Deny all except PostgreSQL (5432), Redis (6379)

VLAN 30 - Management (10.0.30.0/24)
├── Purpose: Monitoring, backup, administration
├── Devices: Grafana, Prometheus, backup servers
├── Access: Internal + VPN (for admins)
├── Routing: Can reach all VLANs (read-only)
└── Firewall: SSH (22), HTTPS (443) from admin IPs only

VLAN 40 - VPN Gateway (10.8.0.0/16)
├── Purpose: Vehicle connectivity
├── Devices: WireGuard endpoint, VPN concentrator
├── Access: Public IP (1 per carrier)
├── Routing: Routes traffic between vehicles and VLAN 10/20
└── Firewall: Only WireGuard (51820 UDP) inbound
```

---

## GPS & Tracking Infrastructure

### GPS Data Flow

```
Vehicle GPS Receiver
        │
        │ NMEA sentences via serial (38400 baud)
        │ $GPGGA, $GPRMC, $GPGSV...
        │
        ▼
Raspberry Pi (gpsd daemon)
        │ Parses NMEA → JSON
        │ {
        │   "lat": 40.7128,
        │   "lon": -74.0060,
        │   "speed": 35.5,
        │   "heading": 270,
        │   "altitude": 10,
        │   "satellites": 12,
        │   "hdop": 0.9
        │ }
        │
        ▼
Traccar Client (local)
        │ Batch GPS points (every 30s or 50 points)
        │ Add metadata: vehicle_id, timestamp, odometer
        │
        ▼
4G LTE Modem → VPN Tunnel
        │ Encrypted transmission
        │
        ▼
Traccar Server (FOC)
        │ REST API: POST /api/positions
        │
        ▼
PostgreSQL + TimescaleDB
        │ Hypertable optimized for time-series
        │ CREATE TABLE positions (
        │   time TIMESTAMPTZ,
        │   vehicle_id INT,
        │   lat DOUBLE PRECISION,
        │   lon DOUBLE PRECISION,
        │   speed DOUBLE PRECISION,
        │   ...
        │ );
        │
        ▼
Real-Time Display
        │ WebSocket push to connected clients
        │ Grafana dashboard updates every 5s
        │ Mobile app shows vehicle positions
```

### GPS Accuracy & Network Effects

| Scenario | GPS Accuracy | Update Frequency | Data Size | Cellular Usage |
|----------|--------------|------------------|-----------|----------------|
| Open sky (highway) | ±3m | Every 5s | 100 bytes | 1.7 MB/day |
| Urban (buildings) | ±10m | Every 5s | 100 bytes | 1.7 MB/day |
| Tunnel (no signal) | N/A | Buffered | 100 bytes | 0 MB (until exit) |
| Parking (stationary) | ±5m | Every 60s | 100 bytes | 140 KB/day |

**Intelligent Position Reporting:**

```python
class SmartGPSReporter:
    def should_report_position(self, current_pos, last_reported_pos):
        """Only report if significant change to save bandwidth"""
        
        # Calculate distance moved
        distance_m = haversine(current_pos, last_reported_pos)
        
        # Calculate time since last report
        time_delta = current_pos.timestamp - last_reported_pos.timestamp
        
        # Report if:
        # 1. Moved >50m
        if distance_m > 50:
            return True
        
        # 2. Speed changed >10 mph
        if abs(current_pos.speed - last_reported_pos.speed) > 10:
            return True
        
        # 3. Heading changed >45 degrees
        if abs(current_pos.heading - last_reported_pos.heading) > 45:
            return True
        
        # 4. Been >5 minutes since last report
        if time_delta > 300:
            return True
        
        # Otherwise, skip this position (save bandwidth)
        return False
```

---

## Camera Network

### Multi-Camera Video Pipeline

```
┌────────────────────────────────────────────────────────────────┐
│               CAMERA NETWORK ARCHITECTURE                       │
└────────────────────────────────────────────────────────────────┘

Front Dashcam (1080p @ 30fps)
        │ USB 3.0 → Raspberry Pi
        │ Video stream: H.264, 5 Mbps
        │
        ▼
Motion Detection (MotionEye)
        │ Analyze frames for motion
        │ IF motion detected OR speed > 10 mph:
        │   Record continuous
        │ ELSE:
        │   Record keyframes only (1 fps)
        │
        ▼
Local Storage (128GB SD Card)
        │ Ring buffer: Last 72 hours
        │ H.264 segments: 1 minute each
        │ Directory structure:
        │ /video/
        │   2024-12-08/
        │     front/
        │       14-00-00.mp4 (2:00 PM)
        │       14-01-00.mp4 (2:01 PM)
        │       ...
        │
        ▼
Event Tagging (AI Analysis)
        │ IF triggered by:
        │   • Hard braking (OBD-II g-force > 0.5g)
        │   • Speeding (GPS speed > limit + 10 mph)
        │   • Manual trigger (officer button press)
        │   • LPR hot-list hit
        │ THEN:
        │   Tag video segment as "INCIDENT"
        │   Priority: HIGH (upload within 5 min)
        │
        ▼
Intelligent Upload
        │ INCIDENT clips: Upload immediately (4G/WiFi)
        │ Normal footage: Upload overnight (WiFi only)
        │
        ▼
MinIO Object Storage (FOC)
        │ Store with metadata:
        │ {
        │   "vehicle": 12,
        │   "camera": "front",
        │   "timestamp": "2024-12-08T14:23:45Z",
        │   "duration": 30,
        │   "event_type": "HARD_BRAKE",
        │   "location": {"lat": 40.7128, "lon": -74.0060},
        │   "filesize_mb": 15,
        │   "retention_days": 90
        │ }
```

### Bandwidth Management for Video

```
Scenario 1: Continuous Recording (Full Quality)
├── Resolution: 1080p @ 30 fps
├── Codec: H.264
├── Bitrate: 5 Mbps
├── Data rate: 2.25 GB/hour
├── 8-hour shift: 18 GB
└── Cellular cost: PROHIBITIVE ($50+/day)

Scenario 2: Motion-Triggered Recording (Smart)
├── Driving (motion): 5 hours × 5 Mbps = 11.25 GB
├── Stationary (keyframes): 3 hours × 0.1 Mbps = 0.13 GB
├── Total: 11.38 GB/shift
├── Upload: WiFi only (end of shift)
└── Cellular cost: $0

Scenario 3: Incident-Only Upload (OS-PATROL Default)
├── Incidents: 5 per shift × 30 seconds × 5 Mbps = 94 MB
├── Upload: Immediate (4G LTE)
├── Full footage: Buffered locally, uploaded via WiFi
└── Cellular cost: <$0.10/day

Recommendation: Scenario 3
- Balances incident response speed with cost
- Critical footage uploaded immediately
- Full continuous recording retained locally
- Bulk upload when vehicle returns to base (WiFi)
```

---

## Redundancy & Failover

### Vehicle Connectivity Resilience

```
┌────────────────────────────────────────────────────────────┐
│           CONNECTIVITY FAILOVER HIERARCHY                   │
└────────────────────────────────────────────────────────────┘

Level 1: PRIMARY (Verizon 4G LTE)
├── Signal: Excellent (-70 dBm)
├── Speed: 20 Mbps down, 5 Mbps up
├── Latency: 50ms
└── Status: ACTIVE ✓

        │ Signal degrades
        ▼

Level 2: BACKUP (AT&T 4G LTE)
├── Signal: Good (-85 dBm)
├── Speed: 15 Mbps down, 3 Mbps up
├── Latency: 60ms
├── Triggered: Primary signal < -105 dBm
├── Failover time: 30 seconds
└── Status: STANDBY

        │ Both carriers down
        ▼

Level 3: OPPORTUNISTIC WiFi
├── Scan for open networks
├── Whitelist: Known safe SSIDs
│   • "CompanyName_Guest"
│   • "PartnerLocation_WiFi"
│   • Officer's phone hotspot
├── Speed: Variable (1-50 Mbps)
└── Status: SCANNING

        │ No connectivity available
        ▼

Level 4: OFFLINE MODE
├── Buffer all data locally
├── GPS tracking: Continues
├── Video recording: Continues
├── LPR scanning: Continues
├── Storage capacity: 7 days
└── Status: OFFLINE (Alert sent when reconnected)

Data Recovery:
When connectivity restored:
1. Upload CRITICAL data first (hot-list hits, panic)
2. Upload HIGH priority (incidents, alerts)
3. Upload NORMAL (GPS tracks, routine LPR)
4. Upload LOW (bulk video) - only via WiFi
```

### Fleet Operations Center Redundancy

```
┌────────────────────────────────────────────────────────────┐
│              FOC HIGH AVAILABILITY                          │
└────────────────────────────────────────────────────────────┘

Component: Traccar Servers
├── Deployment: 3 servers behind load balancer
├── Algorithm: Round-robin with health checks
├── Health check: HTTP GET /api/health every 10s
├── Failover: Automatic, <5 seconds
└── Capacity: Each server handles 100 vehicles
    Total: 300 vehicles (33% per server under normal load)

Component: PostgreSQL Database
├── Deployment: Primary + 2 streaming replicas
├── Replication: Synchronous to Replica 1, Async to Replica 2
├── Failover: Patroni automatic promotion
├── Failover time: <30 seconds
└── Data loss: Zero (synchronous replication)

Component: MinIO Storage
├── Deployment: 4-node erasure-coded cluster
├── Redundancy: EC 4+2 (survives 2 node failures)
├── Capacity: 40 TB usable (60 TB raw)
├── Replication: Built-in, no single point of failure
└── Failover: Automatic, transparent to applications

Component: VPN Gateway
├── Deployment: 2 WireGuard instances (active-active)
├── Load balancing: DNS round-robin
├── Each gateway handles: 500 concurrent tunnels
└── Failover: Vehicles reconnect to standby (60s)

Disaster Recovery:
├── Backup site: 100 miles away
├── Replication: PostgreSQL streaming replication
├── Recovery Time Objective (RTO): 4 hours
├── Recovery Point Objective (RPO): 5 minutes
└── Activation: Manual (after primary site confirmed down)
```

---

## Appendix

### Network Performance Benchmarks

| Metric | Target | Typical | Notes |
|--------|--------|---------|-------|
| GPS position latency | <10s | 5s | Time from vehicle to dashboard |
| LPR hot-list alert | <30s | 15s | Critical event notification |
| Video upload (incident) | <5 min | 2 min | 30-second clip, 15 MB |
| Dashboard response | <500ms | 200ms | Web UI load time |
| Vehicle offline detection | <60s | 30s | Heartbeat timeout |
| VPN reconnect time | <60s | 30s | After connectivity restored |

### Cellular Data Cost Analysis

**Cost per Vehicle per Month:**

| Plan Type | Data Allowance | Cost | Overage | Total (avg) |
|-----------|----------------|------|---------|-------------|
| Budget | 1 GB | $15 | $10/GB | $25 |
| Standard | 5 GB | $40 | $5/GB | $45 |
| Unlimited | Unlimited | $70 | N/A | $70 |

**Recommended:** Standard 5 GB plan
- Covers typical usage: 4.25 GB/month
- Overage rare (WiFi offload for bulk data)
- Cost-effective: $40/vehicle/month

**50-Vehicle Fleet Annual Cost:**
- 50 vehicles × $40/month × 12 months = **$24,000/year**

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Next Document**: [OS-PATROL Logical Topology](./OS-PATROL_Logical_Topology.md)
