---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: 174bd9b4-9ff3-412f-8c00-b110635d87cd
original_filename: OpenPIV_OS-PACS_Deployment_Checklist.md
created_at: 2026-03-04T20:36:55.958704+00:00
content_hash: 973154d82b46
topic: "openpiv-pacs-integration-suite"
consolidated_into: docs/DC-OPENPIV-PACS-INTEGRATION-RECONCILED-001.md
---

# OpenPIV + OS-PACS Deployment Checklist
## Complete Hardware, Software & Task List

**Version**: 1.0  
**Purpose**: Step-by-step deployment guide for integrated system  
**Target**: 50-door facility, 500 users

---

## Pre-Deployment Planning (Week -2 to -1)

### Site Survey

```
FACILITY ASSESSMENT
☐ Total doors requiring access control: _____
☐ Total expected users: _____
☐ Door types identified:
  ☐ Standard single doors: _____
  ☐ Double doors: _____
  ☐ Glass doors: _____
  ☐ Fire-rated doors: _____
  ☐ Turnstiles/gates: _____

NETWORK INFRASTRUCTURE
☐ Network drops available at doors: _____ / _____
☐ PoE switch capacity: _____ available ports
☐ Internet bandwidth: _____ Mbps
☐ Server rack space: _____ U available
☐ UPS capacity: _____ VA
☐ VLAN support: Yes / No

POWER REQUIREMENTS
☐ 120V outlets near doors: _____ / _____
☐ Dedicated circuits for controllers: Yes / No
☐ Backup generator: Yes / No
☐ Expected load: _____ watts

ENROLLMENT SPACE
☐ Private enrollment room available: Yes / No
☐ Computer workstation: Available / Need to procure
☐ Desk space for enrollment: _____ sq ft
☐ Secure storage for cards/equipment: Yes / No
```

---

## Hardware Bill of Materials

### OpenPIV Equipment

#### Identity & Enrollment (One-time Setup)

| Item | Model/Spec | Qty | Unit Price | Total | Vendor |
|------|------------|-----|------------|-------|--------|
| **PKI/Enrollment Server** | | | | | |
| Dell PowerEdge R250 | Xeon E-2314, 16GB RAM, 2x1TB SSD RAID-1 | 1 | $1,800 | $1,800 | Dell |
| *OR* Custom Build | Ubuntu Server, Similar specs | 1 | $1,200 | $1,200 | DIY |
| **Smart Card Equipment** | | | | | |
| Java Cards (JCOP3 J3H145) | 144KB, Java Card 3.0.4 | 550 | $5 | $2,750 | SmartCardFocus |
| Card Printer (optional) | Fargo DTC1250e | 1 | $1,500 | $1,500 | Fargo |
| Card Reader/Writers | ACR38U-I1 USB | 2 | $35 | $70 | Amazon |
| **Biometric Capture** | | | | | |
| Fingerprint Scanner | Digital Persona U.are.U 4500 | 2 | $250 | $500 | Cross Match |
| Webcam | Logitech Brio 4K | 2 | $150 | $300 | Logitech |
| **Enrollment Workstation** | | | | | |
| Desktop PC | Dell OptiPlex 7000, i5, 16GB RAM | 2 | $900 | $1,800 | Dell |
| Monitor 24" | Dell P2422H | 2 | $200 | $400 | Dell |
| **Subtotal OpenPIV** | | | | **$8,320** | |

#### Annual Recurring (Cards)

| Item | Qty/Year | Unit Price | Annual Cost |
|------|----------|------------|-------------|
| Replacement Cards | 50 (10%) | $5 | $250 |
| New Hire Cards | 100 (20% turnover) | $5 | $500 |
| **Annual OpenPIV** | | | **$750** |

---

### OS-PACS Equipment

#### Per-Door Hardware (50 doors)

| Item | Model/Spec | Qty per Door | Unit Price | Total (50 doors) | Vendor |
|------|------------|--------------|------------|------------------|--------|
| **Door Controller** | | | | | |
| Raspberry Pi 4 (8GB) | BCM2711, Quad-core, 8GB RAM | 1 | $75 | $3,750 | Adafruit/CanaKit |
| Industrial microSD | Samsung PRO Endurance 64GB | 1 | $15 | $750 | Amazon |
| Power Supply | 5V 3A USB-C, UL Listed | 1 | $10 | $500 | Amazon |
| **Smart Card Reader** | | | | | |
| HID Signo 40 (OSDP) | NFC + PIV, OSDP Secure Channel | 1 | $220 | $11,000 | HID Global |
| *OR* Identiv uTrust 3700 | NFC + PIV, Wiegand output | 1 | $160 | $8,000 | Identiv |
| **Lock Hardware** | | | | | |
| Electric Strike | Trine 4900 Series, 12/24VDC | 1 | $55 | $2,750 | Trine/Amazon |
| *OR* Mag Lock | 1,200 lbs holding force | 1 | $70 | $3,500 | Securitron |
| **Accessories** | | | | | |
| REX Button | Illuminated, NO/NC | 1 | $15 | $750 | Security Store |
| Door Contact | Magnetic, surface mount | 1 | $8 | $400 | Amazon |
| Relay Module | 4-channel, 5V | 1 | $6 | $300 | Amazon |
| Level Shifter | TXS0108E (5V ↔ 3.3V) | 1 | $3 | $150 | Adafruit |
| Enclosure | Weatherproof ABS, 10x8x4" | 1 | $18 | $900 | Hammond |
| Cable (per door) | 18/4 + Cat6, 100ft average | 1 | $25 | $1,250 | Cable supplier |
| **Subtotal per Door** | | | **~$430** | | |
| **Total 50 Doors** | | | | **$21,500** | |

#### Shared Infrastructure

| Item | Model/Spec | Qty | Unit Price | Total | Vendor |
|------|------------|-----|------------|-------|--------|
| **Network** | | | | | |
| PoE Switch 24-port | TP-Link TL-SG3428MP, 384W | 3 | $280 | $840 | TP-Link |
| Network Cables | Cat6 patch cables, various | 50 | $5 | $250 | Monoprice |
| **Management Server** | | | | | |
| Database Server | Ubuntu Server, i5, 32GB RAM, 2TB SSD | 1 | $1,200 | $1,200 | DIY/Dell |
| **UPS** | | | | | |
| Rack-mount UPS | APC Smart-UPS 1500VA | 2 | $600 | $1,200 | APC |
| **Tools & Misc** | | | | | |
| Crimping Tool | RJ45 + punch-down | 1 | $40 | $40 | Klein Tools |
| Cable Tester | Network cable tester | 1 | $30 | $30 | Amazon |
| Drill + Bits | For mounting | 1 | $100 | $100 | DeWalt |
| Conduit | 1" EMT, 500ft | 1 | $200 | $200 | Home Depot |
| Wire Pulling Tools | Fish tape, cable pulls | 1 | $60 | $60 | Klein Tools |
| **Subtotal Infrastructure** | | | | **$3,920** | |

---

### Complete System Costs

| Category | Cost |
|----------|------|
| OpenPIV Equipment | $8,320 |
| OS-PACS Door Hardware (50 doors @ $430) | $21,500 |
| OS-PACS Infrastructure | $3,920 |
| **Total Hardware** | **$33,740** |
| Labor (estimate, see below) | $8,000 |
| **Grand Total** | **$41,740** |
| **Cost per Door** | **$835** |
| **Cost per User (500)** | **$83** |

**Comparison:**
- Proprietary System (Lenel, HID): $75,000-$100,000
- **Savings: 60-70%**

---

## Software Requirements

### Server Software

```
PKI & ENROLLMENT SERVER
☐ Ubuntu Server 24.04 LTS
☐ Dogtag PKI 11.5+
  ☐ PostgreSQL 15
  ☐ Tomcat 9
☐ OpenFIPS201 build tools
  ☐ Java JDK 11
  ☐ Apache Ant
☐ GlobalPlatformPro
☐ Enrollment portal (FastAPI + React)
  ☐ Python 3.11+
  ☐ Node.js 20+
☐ OpenSC tools
  ☐ piv-tool
  ☐ pkcs11-tool

OS-PACS MANAGEMENT SERVER
☐ Ubuntu Server 24.04 LTS
☐ PostgreSQL 15 (OS-PACS database)
☐ Leosac management interface
☐ NGINX (reverse proxy)
☐ Monitoring stack:
  ☐ Prometheus
  ☐ Grafana
  ☐ Node Exporter
☐ Backup solution (Bareos/Bacula)
```

### Controller Software (Each Raspberry Pi)

```
☐ Raspberry Pi OS Lite (64-bit)
☐ Leosac 1.0+ compiled for ARM
☐ Custom PIV Auth module (libpivauth.so)
☐ PostgreSQL client libraries
☐ OpenSSL 3.0+
☐ CURL (for OCSP)
☐ WireGuard (VPN, optional)
☐ Systemd services configured
```

---

## Installation Timeline (50 Doors, 2-Person Team)

### Week 1: Infrastructure Setup

**Day 1-2: Server Deployment**

```
PKI SERVER SETUP
☐ Rack mount server
☐ Install Ubuntu Server 24.04
☐ Configure network (static IP, firewall)
☐ Install Dogtag PKI
☐ Generate Root CA certificate
☐ Configure Issuing CA
☐ Set up OCSP responder
☐ Create PIV certificate profiles
☐ Test certificate issuance (manual)
☐ Install OpenFIPS201 build environment
☐ Install GlobalPlatformPro
☐ Test card personalization workflow

OS-PACS SERVER SETUP
☐ Rack mount server
☐ Install Ubuntu Server 24.04
☐ Install PostgreSQL 15
☐ Create database schemas
☐ Install Leosac management tools
☐ Configure monitoring (Prometheus/Grafana)
☐ Set up backup jobs
☐ Configure firewall rules
☐ Test database connectivity
```

**Day 3: Enrollment Workstation**

```
☐ Set up enrollment PCs
☐ Install Ubuntu Desktop 24.04
☐ Install enrollment portal software
☐ Connect fingerprint scanners
☐ Connect card readers
☐ Test biometric capture
☐ Test card programming
☐ Configure network access to PKI server
☐ Print test cards
☐ Create operator accounts
☐ Train enrollment operators
```

**Day 4-5: Network Infrastructure**

```
☐ Install PoE switches in rack
☐ Configure VLANs:
  ☐ VLAN 10: Management
  ☐ VLAN 20: Door Controllers
  ☐ VLAN 30: Enrollment
☐ Run network cables to door locations
☐ Label all cables
☐ Test connectivity to each drop
☐ Configure firewall rules between VLANs
☐ Set up UPS for rack equipment
```

---

### Week 2: Door Hardware Installation (Doors 1-25)

**Per Door Installation (2 hours average)**

```
ELECTRICAL WORK
☐ Mount electric strike or mag lock
☐ Run power wire from nearest outlet
☐ Connect lock to relay module
☐ Test lock operation (manual)

READER INSTALLATION
☐ Mount smart card reader (60" height)
☐ Run OSDP cable or Wiegand + power
☐ Connect to controller enclosure
☐ Test reader LED/beeper

CONTROLLER SETUP
☐ Mount Raspberry Pi in enclosure
☐ Connect GPIO to relay module
☐ Connect reader (OSDP/Wiegand)
☐ Connect door contact sensor
☐ Connect REX button
☐ Power up controller
☐ Connect Ethernet (PoE or injector)

RASPBERRY PI CONFIGURATION
☐ Boot Raspberry Pi
☐ Set static IP address
☐ Update system packages
☐ Install Leosac
☐ Configure Leosac kernel.xml
  ☐ Set reader type (OSDP/Wiegand)
  ☐ Configure GPIO pins
  ☐ Set door ID
  ☐ Database connection string
☐ Install PIV Auth module
☐ Start Leosac service
☐ Verify connectivity to management server

TESTING
☐ Test reader detection
☐ Test relay activation (unlock command)
☐ Test door sensor
☐ Test REX button
☐ Test emergency override
☐ Document door ID and IP address
```

---

### Week 3: Door Hardware Installation (Doors 26-50)

**Repeat installation process for remaining doors**

```
☐ Doors 26-30 (Day 1)
☐ Doors 31-35 (Day 2)
☐ Doors 36-40 (Day 3)
☐ Doors 41-45 (Day 4)
☐ Doors 46-50 (Day 5)
```

---

### Week 4: System Integration & Testing

**Day 1-2: Software Integration**

```
CERTIFICATE SYNC
☐ Deploy certificate sync script
☐ Set up cron job (every 5 minutes)
☐ Test sync from Dogtag to OS-PACS
☐ Verify certificates appear in database

ACCESS POLICIES
☐ Define access groups:
  ☐ Employees (all doors, business hours)
  ☐ IT (all doors, 24/7)
  ☐ Security (all doors, 24/7)
  ☐ Executives (executive floor, 24/7)
  ☐ Visitors (lobby only, escorted)
☐ Create schedule templates
☐ Map groups to doors
☐ Test policy evaluation queries

OCSP INTEGRATION
☐ Configure OCSP URL in controllers
☐ Test certificate validation
☐ Test revocation detection
☐ Measure response times
```

**Day 3: User Enrollment (Pilot)**

```
PILOT GROUP (20 USERS)
☐ Schedule enrollment appointments
☐ Enroll pilot users:
  ☐ Verify identity documents
  ☐ Capture biometrics
  ☐ Issue PIV cards
  ☐ Test card at multiple doors
  ☐ Test computer login (if implemented)
☐ Gather user feedback
☐ Refine enrollment workflow
```

**Day 4: System Testing**

```
FUNCTIONALITY TESTS
☐ Normal access (valid card)
☐ Denied access (expired card)
☐ Denied access (wrong door)
☐ Denied access (wrong time)
☐ Revoked certificate detection
☐ Offline mode (disconnect controller)
☐ Emergency override
☐ REX button operation
☐ Door forced open alarm
☐ Door held open alarm

PERFORMANCE TESTS
☐ Measure authentication latency
☐ Test 10 concurrent access attempts
☐ Measure OCSP response time
☐ Test database query performance
☐ Load test management server

FAILOVER TESTS
☐ Disconnect network from controller
☐ Verify offline cache works
☐ Reconnect and verify sync
☐ Stop Dogtag CA
☐ Verify controllers handle gracefully
☐ Stop PostgreSQL
☐ Verify controllers continue (cached)

SECURITY TESTS
☐ Attempt cloned card (should fail - cert based)
☐ Tamper with controller enclosure
☐ Network packet capture (verify TLS)
☐ SQL injection attempts
☐ Invalid certificate tests
```

**Day 5: Documentation & Training**

```
DOCUMENTATION
☐ Finalize system architecture diagram
☐ Document all door IPs and IDs
☐ Create troubleshooting guide
☐ Write operator manual
☐ Create user quick-start guide

TRAINING
☐ Train enrollment operators (3 people)
☐ Train help desk staff
☐ Train security team
☐ Train IT team (system maintenance)
```

---

### Week 5: Production Rollout

**Day 1-3: Mass Enrollment**

```
ENROLLMENT SCHEDULE (500 users)
☐ 80 users/day target
☐ 10 enrollments/hour per station
☐ 2 stations × 8 hours = 160 users/day
☐ ~3 days to complete

DAILY BREAKDOWN
Day 1: ☐ Users 1-160
Day 2: ☐ Users 161-320
Day 3: ☐ Users 321-480
Day 4: ☐ Users 481-500 + catch-up
```

**Day 4: System Hardening**

```
SECURITY HARDENING
☐ Change all default passwords
☐ Disable root SSH access
☐ Enable firewall on all systems
☐ Configure fail2ban
☐ Enable SELinux/AppArmor
☐ Set up log rotation
☐ Enable audit logging
☐ Review and minimize open ports

BACKUP VERIFICATION
☐ Test database backup
☐ Test database restore
☐ Test controller config backup
☐ Document recovery procedures
```

**Day 5: Go-Live & Monitoring**

```
GO-LIVE CHECKLIST
☐ All doors operational
☐ All users enrolled
☐ Help desk staffed
☐ Monitoring dashboards up
☐ Alert rules configured
☐ On-call rotation established
☐ Incident response plan ready

FIRST 24 HOURS
☐ Monitor access attempts
☐ Watch for error patterns
☐ Respond to user issues
☐ Document problems
☐ Deploy hotfixes as needed
```

---

## Post-Deployment (Week 6+)

### Week 6: Stabilization

```
☐ Daily monitoring of access logs
☐ Weekly review of denied access
☐ User feedback collection
☐ Performance tuning
☐ Documentation updates
```

### Month 2: Optimization

```
☐ Analyze usage patterns
☐ Optimize access policies
☐ Fine-tune schedules
☐ Address recurring issues
☐ Plan enhancements
```

### Quarterly Tasks

```
☐ Security audit
☐ Backup restore test
☐ Disaster recovery drill
☐ Certificate expiration review
☐ Hardware maintenance
☐ User training refresher
```

### Annual Tasks

```
☐ Comprehensive security assessment
☐ Update all software packages
☐ Review and update policies
☐ Hardware refresh planning
☐ Budget planning for next year
```

---

## Maintenance Supplies

### Recurring Inventory

| Item | Qty | Reorder Point | Unit Cost |
|------|-----|---------------|-----------|
| Java Cards | 100 | 20 remaining | $5 |
| Spare Raspberry Pi 4 | 3 | 1 remaining | $75 |
| Spare microSD cards | 10 | 3 remaining | $15 |
| Spare readers | 2 | 0 remaining | $220 |
| Spare relays | 5 | 2 remaining | $6 |
| Network cables | 20 | 5 remaining | $5 |

---

## Support Contacts

### Vendors

| Vendor | Product | Contact | Phone |
|--------|---------|---------|-------|
| SmartCardFocus | Java Cards | sales@smartcardfocus.com | - |
| HID Global | Readers | - | 1-800-237-7769 |
| Adafruit | Raspberry Pi, components | - | - |
| Dell | Servers, workstations | - | - |

### Internal Contacts

| Role | Name | Phone | Email |
|------|------|-------|-------|
| Project Manager | _______ | _______ | _______ |
| Lead Technician | _______ | _______ | _______ |
| Network Admin | _______ | _______ | _______ |
| Security Manager | _______ | _______ | _______ |

---

## Emergency Procedures

### System Down

```
IMMEDIATE ACTIONS
☐ Check server status
☐ Check network connectivity
☐ Review recent logs
☐ Contact on-call engineer

MANUAL OVERRIDE
☐ Location of master keys: _____________
☐ Emergency unlock procedure: _____________
☐ Authorized personnel: _____________
```

### Security Incident

```
SUSPECTED BREACH
☐ Isolate affected systems
☐ Review audit logs
☐ Contact security team
☐ Preserve evidence
☐ Notify management

CARD COMPROMISE
☐ Immediately revoke certificate
☐ Issue replacement card
☐ Review access logs
☐ Update security procedures
```

---

## Success Metrics

### Week 1

- [ ] All servers operational
- [ ] Enrollment system functional
- [ ] PKI issuing certificates

### Month 1

- [ ] All 50 doors operational
- [ ] 500 users enrolled
- [ ] <2% support ticket rate
- [ ] Average auth time <1.5s

### Month 3

- [ ] Zero security incidents
- [ ] User satisfaction >85%
- [ ] System uptime >99.5%
- [ ] All training completed

### Month 6

- [ ] Full feature adoption
- [ ] ROI calculation documented
- [ ] Expansion plan developed

---

**Deployment Team Sign-Off**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Project Manager | _______ | _______ | __/__/__ |
| Lead Installer | _______ | _______ | __/__/__ |
| Network Admin | _______ | _______ | __/__/__ |
| Security Manager | _______ | _______ | __/__/__ |

---

**Document Version**: 1.0  
**Last Updated**: December 2025  
**Author**: Toussaint Louis  
**Next Review**: Q2 2026


<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Topics:**
- [[knowledge-base/_topics/openpiv-pacs-integration-suite|openpiv-pacs-integration-suite]]

**Consolidated into:**
- [[docs/DC-OPENPIV-PACS-INTEGRATION-RECONCILED-001]]

<!-- AUTO-GENERATED RELATED END -->
