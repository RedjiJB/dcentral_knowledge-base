---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: 2dd85708-4ee7-4439-b2c2-f71252ca298f
original_filename: OS-CONCIERGE_Network_Topology.md
created_at: 2026-03-04T20:35:00.334637+00:00
content_hash: 5c73d1f049b9
---

# OS-CONCIERGE Network Topology
## Intelligent Concierge Network Architecture & Multi-Property Infrastructure

**Document Type**: Network Topology Specification  
**Version**: 1.0  
**Date**: December 2024  
**Classification**: Technical Documentation  
**Audience**: Network Architects, Property Managers, IT Operations

---

## Executive Summary

### Network Architecture Philosophy

OS-CONCIERGE implements a **distributed multi-property architecture** where each building operates autonomously while connecting to a centralized management platform. The system prioritizes:

- **High Availability**: 99.9% uptime for critical concierge services
- **Multi-Tenant Isolation**: Each property has isolated network segments
- **Hybrid Deployment**: On-premise kiosks + cloud AI services
- **Scalable Design**: Supports 1-1,000+ properties per deployment

### Network Scale Characteristics

| Deployment Size | Properties | Kiosks | Monthly Data | Servers | Annual Cost |
|----------------|------------|--------|--------------|---------|-------------|
| Single Property | 1 | 1-3 | 500 GB | 1 | $5,000 |
| Small Portfolio | 5-10 | 10-30 | 2.5 TB | 2 | $25,000 |
| Medium Portfolio | 10-50 | 50-150 | 12.5 TB | 3-5 | $100,000 |
| Enterprise | 50-500 | 500-1,500 | 125 TB | 10+ | $500,000 |

---

## Multi-Property Network Architecture

### Three-Tier Distributed Design

```
┌────────────────────────────────────────────────────────────────────┐
│                    TIER 1: PROPERTY EDGE                            │
│                    (Per-Building Infrastructure)                    │
└────────────────────────────────────────────────────────────────────┘

PROPERTY A (123 Main St)
├── Building Network: 10.100.0.0/16
├── VLANs:
│   ├── VLAN 10: Concierge Kiosks (10.100.10.0/24)
│   ├── VLAN 20: Smart Building (10.100.20.0/24)
│   ├── VLAN 30: Guest WiFi (10.100.30.0/24)
│   └── VLAN 40: Management (10.100.40.0/24)
└── Devices:
    ├── Kiosk #1 (Lobby): 10.100.10.10
    ├── Kiosk #2 (Amenity): 10.100.10.11
    ├── Smart Lock Bridge: 10.100.20.20
    ├── Access Control: 10.100.20.21
    └── VPN Gateway: 10.100.40.1 → Cloud

PROPERTY B (456 Oak Ave)
├── Building Network: 10.101.0.0/16
├── VLANs: (Same structure as Property A)
└── VPN Tunnel → Cloud

PROPERTY C (789 Elm Rd)
├── Building Network: 10.102.0.0/16
└── VPN Tunnel → Cloud

... (up to 254 properties with /16 networks)

┌────────────────────────────────────────────────────────────────────┐
│                    TIER 2: CLOUD PLATFORM                           │
│                    (Centralized Services)                           │
└────────────────────────────────────────────────────────────────────┘

Data Center Network: 10.0.0.0/16
├── VLAN 10: Application Tier (10.0.10.0/24)
│   ├── AI Chatbot Service (Rasa) - 3 servers
│   ├── CRM Integration (HubSpot API) - 2 servers
│   ├── Visitor Management - 2 servers
│   └── API Gateway (Kong) - 3 servers
│
├── VLAN 20: Data Tier (10.0.20.0/24)
│   ├── PostgreSQL Cluster (Primary + 2 Replicas)
│   ├── MongoDB (Chatbot History) - 3 nodes
│   ├── Redis Cache - 3 nodes
│   └── Elasticsearch (Search) - 3 nodes
│
├── VLAN 30: Integration Tier (10.0.30.0/24)
│   ├── Smart Lock Controllers (API bridges)
│   ├── Access Control Integration
│   ├── Building Management Systems
│   └── Payment Gateway (Stripe/Square)
│
└── VLAN 40: VPN Concentrator (10.0.40.0/24)
    ├── WireGuard Gateways (×3)
    └── Property Tunnels (10.8.0.0/16)

┌────────────────────────────────────────────────────────────────────┐
│                    TIER 3: EXTERNAL INTEGRATIONS                    │
└────────────────────────────────────────────────────────────────────┘

├── OpenAI API (GPT-4) - AI chatbot intelligence
├── Google Maps API - Directions and local search
├── Stripe API - Payment processing
├── Twilio API - SMS notifications
├── SendGrid API - Email notifications
└── Property Management Systems (PMS)
    ├── Yardi Voyager
    ├── RealPage
    └── AppFolio
```

### IP Addressing Scheme

```
Global Allocation:
├── 10.0.0.0/16: Cloud Data Center
├── 10.8.0.0/16: VPN Tunnel Space
└── 10.100.0.0/12: Properties (10.100.0.0 - 10.111.255.255)
    ├── 10.100.0.0/16: Property 1
    ├── 10.101.0.0/16: Property 2
    ├── 10.102.0.0/16: Property 3
    └── ... (4,096 possible /16 networks = 4,096 properties)

Per-Property VLANs (Using Property 1 as example):
├── 10.100.10.0/24: Concierge Kiosks (254 kiosks max)
├── 10.100.20.0/24: Smart Building Devices (locks, sensors)
├── 10.100.30.0/24: Guest WiFi (DHCP pool)
└── 10.100.40.0/24: Management (cameras, monitoring)
```

---

## Kiosk Network Design

### Concierge Kiosk Architecture

```
┌────────────────────────────────────────────────────────────────┐
│               KIOSK HARDWARE & NETWORK                          │
└────────────────────────────────────────────────────────────────┘

Physical Kiosk:
├── Display: 27" Touchscreen (1920×1080)
├── Computer: Intel NUC (i5, 16GB RAM, 256GB SSD)
├── OS: Ubuntu 22.04 LTS
├── Network: Gigabit Ethernet (PoE optional)
├── Power: 120V AC or PoE+ (802.3at, 30W)
└── Peripherals:
    ├── QR Code Scanner (USB)
    ├── NFC Reader (USB)
    ├── Receipt Printer (optional)
    └── Camera (visitor photo, optional)

Network Configuration:
┌──────────────────────────────────────────────────┐
│ Kiosk #1 (10.100.10.10)                         │
│                                                  │
│ eth0: 10.100.10.10/24                           │
│ Gateway: 10.100.10.1 (Property Router)          │
│ DNS: 10.0.20.53, 8.8.8.8                        │
│                                                  │
│ VPN Tunnel: wg0                                  │
│ VPN IP: 10.8.100.10/32                          │
│ Peer: Cloud VPN Gateway (10.0.40.1)             │
│                                                  │
│ Services:                                        │
│ ├── Kiosk UI (React) - Port 3000                │
│ ├── Local API Cache (Node.js) - Port 8080       │
│ ├── MQTT Client - connects to 10.0.30.100:1883  │
│ └── Monitoring Agent (Prometheus) - Port 9090   │
└──────────────────────────────────────────────────┘
```

### Kiosk-to-Cloud Communication

```
Data Flow: User Request → Kiosk → Cloud

Step 1: User Interaction
User touches "Visitor Check-In" on kiosk
        │
        ▼
Step 2: Local Processing
Kiosk UI (React) captures input
Validates locally (name, company, reason)
        │
        │ HTTPS POST
        ▼
Step 3: Cloud API Request
POST https://api.concierge.company.com/api/visitors
{
  "property_id": 1,
  "visitor": {
    "name": "John Doe",
    "company": "ABC Corp",
    "host_unit": "12A",
    "photo_url": "data:image/jpeg;base64,..."
  }
}
        │
        │ VPN Tunnel (encrypted)
        │ 10.8.100.10 → 10.0.10.5
        ▼
Step 4: Cloud Processing
API Gateway (Kong) receives request
Routes to Visitor Management Service
        │
        ├─→ Lookup host in database
        ├─→ Send SMS notification to host
        ├─→ Generate temporary access code
        └─→ Log visit in audit trail
        │
        ▼
Step 5: Response to Kiosk
{
  "status": "success",
  "access_code": "1234#",
  "valid_until": "2024-12-08T18:00:00Z",
  "message": "Your host has been notified"
}
        │
        │ VPN Tunnel (encrypted)
        ▼
Step 6: Kiosk Display
Shows QR code with access code
Prints visitor badge (if printer available)
Displays "Please wait for host approval"

Total Latency: 2-5 seconds
- Local validation: 0.1s
- VPN transmission: 0.5-1s
- Cloud processing: 1-2s
- Database queries: 0.5-1s
- Response: 0.5-1s
```

---

## Smart Building Integration

### Smart Lock Network

```
┌────────────────────────────────────────────────────────────────┐
│           SMART LOCK INTEGRATION ARCHITECTURE                   │
└────────────────────────────────────────────────────────────────┘

Building Network (10.100.20.0/24)
        │
        ▼
┌──────────────────────────┐
│ Smart Lock Bridge        │  Translates cloud API → local protocol
│ 10.100.20.20             │  Supports:
│                          │  • Z-Wave (868 MHz)
│ Software:                │  • Zigbee (2.4 GHz)
│ • Home Assistant         │  • BLE (Bluetooth Low Energy)
│ • MQTT Broker            │  • WiFi (direct TCP/IP)
└────────┬─────────────────┘
         │
         ├──────────────┬──────────────┬──────────────┐
         │              │              │              │
    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
    │ Lock 1  │    │ Lock 2  │    │ Lock 3  │    │ Lock 4  │
    │ Unit A  │    │ Unit B  │    │ Gym     │    │ Roof    │
    │ Z-Wave  │    │ Z-Wave  │    │ Zigbee  │    │ WiFi    │
    └─────────┘    └─────────┘    └─────────┘    └─────────┘

Integration Protocol:
┌──────────────────────────────────────────────────────────────┐
│ Cloud → Property Lock Control                                │
│                                                               │
│ 1. Cloud receives access grant request                       │
│    (Visitor checked in, resident granted access)             │
│                                                               │
│ 2. Publish MQTT message:                                     │
│    Topic: property/100/locks/unit_a/unlock                   │
│    Payload: {                                                │
│      "code": "1234#",                                        │
│      "valid_until": "2024-12-08T18:00:00Z",                 │
│      "user": "visitor_john_doe"                              │
│    }                                                         │
│                                                               │
│ 3. Smart Lock Bridge subscribes to topic                     │
│    Receives message via VPN tunnel                           │
│                                                               │
│ 4. Bridge translates to local protocol                       │
│    Z-Wave command: "Set User Code #50 = 1234"               │
│    Expiration: Auto-delete at 6 PM                           │
│                                                               │
│ 5. Lock acknowledges                                         │
│    Bridge publishes confirmation:                            │
│    Topic: property/100/locks/unit_a/status                   │
│    Payload: {"code_added": true, "slot": 50}                │
│                                                               │
│ 6. Cloud receives confirmation                               │
│    Updates visitor record: "Access granted to Unit A"        │
└──────────────────────────────────────────────────────────────┘
```

---

## Guest WiFi Network

### Captive Portal Architecture

```
┌────────────────────────────────────────────────────────────────┐
│              GUEST WIFI WITH CAPTIVE PORTAL                     │
└────────────────────────────────────────────────────────────────┘

VLAN 30: Guest WiFi (10.100.30.0/24)

Access Point (Ubiquiti UniFi)
├── SSID: "PropertyName_Guest"
├── Security: Open (captive portal)
├── Bandwidth: 100 Mbps per property
└── Isolation: Client-to-client blocking enabled

        │
        │ Guest device associates
        │ DHCP assigns: 10.100.30.X
        ▼
┌──────────────────────────┐
│ Captive Portal           │  pfSense with captive portal plugin
│ 10.100.30.1              │
│                          │
│ Detection:               │  • HTTP traffic intercepted
│ • Redirect to login page │  • HTTPS shows certificate warning
│                          │
│ Login Options:           │
│ 1. Self-registration     │  Name + email → 24hr access
│ 2. Voucher code          │  Front desk provides code
│ 3. Social auth (OAuth)   │  Login with Google/Facebook
└────────┬─────────────────┘
         │
         │ User authenticated
         ▼
Firewall Rules Applied:
├── Allow: HTTP (80), HTTPS (443)
├── Allow: DNS (53)
├── Block: All other ports
├── Block: Access to internal VLANs (10.100.10/20/40.0/24)
└── Rate Limit: 10 Mbps per device

User authenticated, internet access granted
Session stored in Redis (expires after 24 hours)
```

---

## AI Chatbot Network

### Chatbot Service Architecture

```
┌────────────────────────────────────────────────────────────────┐
│            AI CHATBOT SERVICE TOPOLOGY                          │
└────────────────────────────────────────────────────────────────┘

Kiosk User Interface
        │
        │ WebSocket connection
        │ wss://chat.concierge.company.com
        ▼
┌──────────────────────────┐
│ API Gateway (Kong)       │  Rate limiting, authentication
│ 10.0.10.10               │  Forwards to appropriate backend
└────────┬─────────────────┘
         │
         │ Load balanced (round-robin)
         │
    ┌────┼────┬────────────┬────────────┐
    │         │            │            │
┌───▼──┐  ┌───▼──┐  ┌─────▼─┐  ┌───────▼───┐
│Rasa  │  │Rasa  │  │ Rasa  │  │ OpenAI    │
│ NLU  │  │ NLU  │  │  NLU  │  │ Fallback  │
│  #1  │  │  #2  │  │   #3  │  │  (GPT-4)  │
└───┬──┘  └───┬──┘  └─────┬─┘  └───────┬───┘
    │         │            │            │
    └─────────┴────────────┴────────────┘
         │
         │ Query results
         ▼
┌──────────────────────────┐
│ Knowledge Base           │  • Property info (MongoDB)
│ • FAQs                   │  • Amenity schedules
│ • Amenities              │  • Service requests
│ • Local businesses       │  • Maintenance tickets
│ • Events calendar        │
└────────┬─────────────────┘
         │
         │ External API calls (if needed)
         │
    ┌────┼────┬────────────┬────────────┐
    │         │            │            │
┌───▼──────┐ ┌▼─────────┐ ┌▼──────────┐ ┌▼──────────┐
│ Google   │ │ Weather  │ │ Property  │ │ CRM       │
│ Maps API │ │  API     │ │ Mgmt Sys  │ │ (HubSpot) │
└──────────┘ └──────────┘ └───────────┘ └───────────┘

Sample Dialogue Flow:
User: "How do I get to the gym?"
  → Rasa NLU: Intent = "find_amenity", Entity = "gym"
  → Query Knowledge Base: Gym location = "2nd floor, west wing"
  → Response: "The gym is on the 2nd floor, west wing. 
              Take the elevator to Floor 2 and turn left."

User: "What's the weather today?"
  → Rasa NLU: Intent = "weather_query"
  → Call Weather API (property location)
  → Response: "Today in [City]: Sunny, 72°F. 
              Perfect day to use the rooftop terrace!"
```

---

## Visitor Management Data Flow

```
┌────────────────────────────────────────────────────────────────┐
│           VISITOR CHECK-IN FLOW                                 │
└────────────────────────────────────────────────────────────────┘

Step 1: Visitor Arrives at Kiosk
Kiosk displays: "Welcome! Touch to check in"
        │
        ▼
Step 2: Information Collection
Kiosk prompts:
├── Full Name: "John Doe"
├── Company: "ABC Corp"
├── Visiting Unit: "12A" or "John Smith"
├── Photo: Capture from kiosk camera
└── Purpose: "Business Meeting"
        │
        ▼
Step 3: Host Lookup
Query database:
SELECT * FROM units WHERE unit_number = '12A'
Returns: {
  resident_name: "John Smith",
  phone: "+1-555-123-4567",
  email: "john@example.com"
}
        │
        ▼
Step 4: Host Notification
PARALLEL execution:
├── SMS (Twilio API):
│   "Visitor John Doe from ABC Corp is here to see you.
│    Reply Y to approve, N to deny."
│
├── Email (SendGrid API):
│   Subject: "Visitor Waiting in Lobby"
│   Body: [Details + Approve/Deny buttons]
│
└── Push Notification (if resident app installed)
        │
        │ Wait for response (timeout: 5 minutes)
        ▼
Step 5: Host Approval
Host replies "Y" via SMS
  OR
Host clicks "Approve" in email
  OR  
Host approves in mobile app
        │
        ▼
Step 6: Access Code Generation
Generate temporary code:
├── Code: Random 4-digits (e.g., "1234#")
├── Valid Duration: 4 hours (configurable)
├── Scope: Main entrance + Unit 12A
└── Store in database for audit
        │
        ▼
Step 7: Visitor Badge
Kiosk displays/prints:
┌────────────────────────┐
│   VISITOR BADGE        │
│                        │
│   John Doe             │
│   ABC Corp             │
│   Visiting: Unit 12A   │
│   Host: John Smith     │
│                        │
│   [QR CODE]            │
│   Code: 1234#          │
│   Valid Until: 6:00 PM │
└────────────────────────┘
        │
        ▼
Step 8: Access Granted
Visitor uses code at:
├── Main entrance keypad
├── Elevator (floor restriction removed for Unit 12's floor)
└── Unit 12A door (if smart lock)

Step 9: Visitor Departure
Visitor presses "Check Out" at kiosk (optional)
  OR
System auto-expires code after valid duration
        │
        ▼
Step 10: Audit Log
Record stored:
{
  visitor_id: 12345,
  name: "John Doe",
  company: "ABC Corp",
  host_unit: "12A",
  check_in: "2024-12-08T14:00:00Z",
  check_out: "2024-12-08T16:30:00Z",
  access_code: "1234#",
  photo_url: "s3://bucket/visitors/12345.jpg"
}
```

---

## Network Security

### Segmentation & Firewalls

```
Security Zones:
┌────────────────────────────────────────────────────────────────┐
│ ZONE 0: PERIMETER (Internet)                                   │
│ ├── Threats: DDoS, unauthorized access                         │
│ └── Protection: Cloud WAF (Cloudflare)                         │
└────────┬───────────────────────────────────────────────────────┘
         │
┌────────▼───────────────────────────────────────────────────────┐
│ ZONE 1: DMZ (Public-Facing Services)                           │
│ ├── API Gateway (10.0.10.10)                                   │
│ ├── Web Portal (10.0.10.20)                                    │
│ └── Firewall Rules:                                            │
│     • Allow: HTTPS (443) from Internet                         │
│     • Allow: HTTP (80) → redirect to HTTPS                     │
│     • Block: All other inbound                                 │
└────────┬───────────────────────────────────────────────────────┘
         │
┌────────▼───────────────────────────────────────────────────────┐
│ ZONE 2: APPLICATION TIER (Internal Services)                   │
│ ├── Chatbot (Rasa) - 10.0.10.30-32                            │
│ ├── Visitor Management - 10.0.10.40                           │
│ └── Firewall Rules:                                            │
│     • Allow: From ZONE 1 (API Gateway) only                    │
│     • Allow: HTTPS (443), HTTP (8080)                          │
│     • Block: Direct internet access                            │
└────────┬───────────────────────────────────────────────────────┘
         │
┌────────▼───────────────────────────────────────────────────────┐
│ ZONE 3: DATA TIER (Databases)                                  │
│ ├── PostgreSQL - 10.0.20.10-12                                │
│ ├── MongoDB - 10.0.20.20-22                                   │
│ ├── Redis - 10.0.20.30-32                                     │
│ └── Firewall Rules:                                            │
│     • Allow: From ZONE 2 (Application) only                    │
│     • Allow: PostgreSQL (5432), MongoDB (27017), Redis (6379)  │
│     • Block: All other access                                  │
└────────┬───────────────────────────────────────────────────────┘
         │
┌────────▼───────────────────────────────────────────────────────┐
│ ZONE 4: VPN GATEWAY (Property Connections)                     │
│ ├── WireGuard Concentrator - 10.0.40.1-3                      │
│ └── Firewall Rules:                                            │
│     • Allow: WireGuard (51820 UDP) from Internet               │
│     • Allow: VPN clients → ZONE 2 (Application) only           │
│     • Block: VPN clients → ZONE 3 (Database) direct            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Redundancy & High Availability

```
Component-Level Redundancy:

KIOSKS (Property-Level)
├── Deployment: 2+ kiosks per property
├── Failover: If Kiosk #1 offline, users use Kiosk #2
├── Offline Mode: Local cache (24hr visitor history)
└── Recovery: Auto-sync when connectivity restored

API GATEWAY (Cloud)
├── Deployment: 3 Kong instances (active-active)
├── Load Balancer: HAProxy (health checks every 10s)
├── Failover: Automatic (<5s downtime)
└── Capacity: Each handles 500 req/s (1500 req/s total)

CHATBOT SERVICE (Cloud)
├── Deployment: 3 Rasa servers (active-active)
├── Load Balancer: Round-robin
├── Fallback: OpenAI GPT-4 (if all Rasa instances down)
└── Session Persistence: Redis (shared state)

DATABASE (Cloud)
├── PostgreSQL: Primary + 2 streaming replicas
├── Replication: Synchronous (zero data loss)
├── Failover: Patroni auto-promotion (<30s)
└── Backup: Daily snapshots (30-day retention)

VPN GATEWAY (Cloud)
├── Deployment: 3 WireGuard instances (active-active)
├── Load Balancing: DNS round-robin
├── Each Gateway: 500 concurrent tunnels
└── Failover: Kiosks reconnect to next gateway (60s)

DISASTER RECOVERY
├── Backup Site: 100 miles from primary
├── Replication: PostgreSQL streaming (async)
├── RTO: 4 hours
├── RPO: 15 minutes
└── Activation: Manual (after primary confirmed down)
```

---

## Deployment Scenarios

### Single Property

**Network Equipment:**
- 1× Router/Firewall: $200
- 1× Managed Switch (8-port): $150
- 1× WiFi Access Point: $100
- **Total Hardware: $450**

**Servers:**
- 1× On-premise server (optional): $1,500
- Cloud subscription: $200/month

**Kiosks:**
- 2× Kiosks: $4,000

**Annual Cost: $7,350**

### Small Portfolio (10 Properties)

**Per-Property Equipment:** $450 × 10 = $4,500
**Kiosks:** $2,000 × 10 = $20,000
**Cloud Infrastructure:** $500/month × 12 = $6,000
**Annual Cost: $30,500**

### Enterprise (100 Properties)

**Per-Property Equipment:** $450 × 100 = $45,000
**Kiosks:** $2,000 × 100 = $200,000
**Cloud Infrastructure:** $2,000/month × 12 = $24,000
**Dedicated Support:** $50,000/year
**Annual Cost: $319,000**

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Next Document**: [OS-CONCIERGE Logical Topology](./OS-CONCIERGE_Logical_Topology.md)
