---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: 5a296c4e-6e24-4b16-9e86-0c5dd6b31722
original_filename: Provincial_PIV_Infrastructure_Integration.md
created_at: 2026-03-04T20:38:02.587076+00:00
content_hash: 7d5cecfd93c1
topic: opensecure-provincial-security-network
---

# Provincial PIV Infrastructure Integration
## Unified Identity & Access Management Across 7-Pillar Security Ecosystem

**Document Name**: Provincial PIV Infrastructure Integration  
**Version**: 1.0  
**Date**: December 2025  
**Classification**: Public Safety & National Security Infrastructure  
**Scope**: Province-wide federated identity and access management

---

## Executive Summary

### The Vision

**"One Identity, Seven Systems, Infinite Cooperation"**

Create a **unified PIV-based identity infrastructure** that serves as the trust anchor for all seven provincial security ecosystem pillars (PSVN, PBCEN, PSVN-Fleet, PASSN, PXRSN, PISN, PSRFIP), enabling seamless authentication, authorization, and audit across organizational boundaries while maintaining privacy, security, and legal compliance.

### The Revolutionary Concept

```
┌─────────────────────────────────────────────────────────────────┐
│  Traditional Model (Fragmented Identity)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Security Guard at Company A:                                   │
│  ├─ Badge for building access                                  │
│  ├─ Username/password for camera system                        │
│  ├─ Different login for body camera upload                     │
│  ├─ Separate app for vehicle dispatch                          │
│  ├─ Another credential for evidence sharing                    │
│  └─ No access to other companies' systems                      │
│                                                                  │
│  Problems:                                                       │
│  • 5+ different credentials per person                         │
│  • Password fatigue → weak passwords                           │
│  • No cross-organization cooperation                           │
│  • Manual identity verification                                │
│  • No centralized audit trail                                  │
│  • Credential revocation problems                              │
│  • Emergency access delays                                     │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  PIV Model (Unified Identity)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
  One PIV Card = Universal Access:                              │
│  ✓ Building access (OS-PACS integration)                      │
│  ✓ Video system authentication                        │
│  ✓ Body camera activation                             │
│  ✓ Vehicle assignment                            │
│  ✓ Drone authorization                               │
│  ✓ AR glasses login                                    │
│  ✓ Service requests                                   │
│  ✓ Military mobilization                           │
│                                                                  │
│  All controlled by:                                            │
│  ✓ PKI-based authentication (FIPS 201 compliant)              │
│  ✓ Role-based authorization (RBAC)                            │
│  ✓ Organization-scoped permissions                             │
│  ✓ Time-based access windows                                  │
│  ✓ Biometric secondary factor (optional)                      │
│  ✓ Complete audit trail (every action)                        │
│  ✓ Instant revocation (compromised credentials)               │
└─────────────────────────────────────────────────────────────────┘
```

---

## PIV Infrastructure Architecture

### Core Components

#### 1. Provincial PIV Certificate Authority (CA)

**Purpose**: Trust anchor for all provincial security credentials

```
┌───────────────────────────────────────────────────────────────┐
│  Provincial PIV Certificate Authority                         │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  Root CA (Offline, Hardware Security Module)                 │
│  ├─ Provincial Root Certificate                              │
│  ├─ 4096-bit RSA key pair                                    │
│  ├─ Self-signed, 20-year validity                            │
│  └─ Stored in FIPS 140-2 Level 3 HSM                        │
│                                                               │
│  Issuing CA (Online, Air-Gapped Network)                     │
│  ├─ Signs end-entity certificates                            │
│  ├─ 24/7 availability (HA cluster)                           │
│  ├─ Certificate Revocation List (CRL) publishing             │
│  ├─ OCSP responder (real-time validation)                    │
│  └─ Audit logging (SIEM integration)                         │
│                                                               │
│  Registration Authority (RA)                                  │
│  ├─ Identity verification (in-person + background check)     │
│  ├─ Certificate enrollment workflow                          │
│  ├─ PIV card personalization                                 │
│  └─ Lifecycle management (renewal, revocation)               │
│                                                               │
│  Standards Compliance:                                        │
│  ✓ FIPS 201-3 (Personal Identity Verification)              │
│  ✓ FIPS 140-2 (Cryptographic Module Validation)             │
│  ✓ NIST SP 800-73-4 (PIV Cryptographic Algorithms)          │
│  ✓ NIST SP 800-78-4 (Cryptographic Algorithms)              │
│  ✓ X.509 v3 Certificate Standard                            │
│  ✓ RFC 5280 (Internet X.509 PKI Certificate)                │
└───────────────────────────────────────────────────────────────┘
```

**Hardware Requirements:**

```yaml
Root CA Infrastructure:
  Hardware Security Module (HSM):
    - Model: Thales Luna SA Network HSM 7
    - Certification: FIPS 140-2 Level 3
    - Key Storage: 100,000+ private keys
    - Performance: 10,000 RSA-2048 signatures/sec
    - Redundancy: Active-passive cluster (2 units)
    - Backup: Offline HSM in secure vault
  
  Root CA Server:
    - Server: Dell PowerEdge R750
    - CPU: Dual Intel Xeon Gold 6338 (64 cores)
    - RAM: 128GB ECC DDR4
    - Storage: 2TB NVMe SSD (RAID 1)
    - Network: Air-gapped (no internet connection)
    - Location: Tier IV data center, 24/7 physical security

Issuing CA Infrastructure:
  Load Balanced CA Cluster:
    - Servers: 3x Dell PowerEdge R650 (HA cluster)
    - CPU: Dual Intel Xeon Silver 4314 (32 cores each)
    - RAM: 64GB ECC DDR4 each
    - Storage: 1TB NVMe SSD RAID 1 each
    - Network: Dedicated security VLAN, 10Gbps redundant
    - Load Balancer: F5 BIG-IP (hardware appliance)
  
  OCSP Responders:
    - Servers: 2x Dell PowerEdge R450
    - Purpose: Real-time certificate validation
    - SLA: 99.99% uptime, <100ms response time
    - Capacity: 100,000 validation requests/sec

Registration Authority (RA) Workstations:
  Identity Verification Stations (10 locations):
    - Workstation: Dell OptiPlex 7090 Tower
    - PIV Card Reader: HID Omnikey 5427 CK (contact/contactless)
    - Fingerprint Scanner: Integrated Biometrics Columbo
    - Document Scanner: Canon DR-C225 II
    - Camera: Logitech Brio 4K (badge photo)
    - Printer: Zebra ZXP Series 7 (card printer)
    - Network: Dedicated RA network segment
```

#### 2. PIV Card Hardware Specifications

**Provincial Security PIV Card:**

```yaml
Physical Card Specifications:
  Standard: ISO/IEC 7816, ISO/IEC 14443 Type A
  Dimensions: 85.60mm × 53.98mm × 0.76mm (CR80)
  Material: Polycarbonate (PC) or PET composite
  Durability: 10-year lifespan, tamper-evident
  
Chip Specifications:
  Processor: Infineon SLE78 Secure Microcontroller
  Operating System: Java Card 3.0.4 (Global Platform 2.2.1)
  Memory:
    - ROM: 1MB (firmware)
    - EEPROM: 144KB (data storage)
    - RAM: 18KB (working memory)
  
  Cryptographic Capabilities:
    - RSA: 2048-bit, 3072-bit, 4096-bit
    - ECC: P-256, P-384 (NIST curves)
    - AES: 128-bit, 192-bit, 256-bit
    - 3DES: 168-bit (legacy support)
    - Hash: SHA-256, SHA-384, SHA-512
  
  Security Certifications:
    - Common Criteria EAL5+ (hardware)
    - FIPS 140-2 Level 3 (cryptographic module)
    - EMVCo Level 1 (contact interface)
    - NFC Forum Type 4 Tag (contactless)

Card Data Model (FIPS 201-3):
  Mandatory Data Objects:
    - Card Holder Unique Identifier (CHUID)
      └─ FASC-N: Federal Agency Smart Credential Number
    - Card Authentication Certificate (signed by Provincial CA)
    - PIV Authentication Certificate (digital signatures)
    - Cardholder Fingerprints (2 fingerprints, encrypted)
    - Cardholder Facial Image (JPEG2000, 300dpi minimum)
    - Security Object (digital signature over all data)
  
  Optional Data Objects:
    - Digital Signature Certificate (email, document signing)
    - Key Management Certificate (encryption)
    - Retired Certificates (up to 20 previous certs)
    - Cardholder Iris Images (biometric template)
    - Pairing Code (device binding)
    - Discovery Object (application directory)

Visual Design (Front):
  ┌────────────────────────────────────────────────────┐
  │ [Company Logo]    ONTARIO              │
  │                                                     │
  │  [Photo]     PROVINCIAL SECURITY                   │
  │  2x2"        IDENTIFICATION                        │
  │                                                     │
  │  Name: [LAST, First Middle]                        │
  │  ID: SG-ON-XXXXXX                                  │
  │  Role: Security Guard / Law Enforcement            │
  │  Employer: [Organization Name]                     │
  │  Issued: YYYY-MM-DD                                │
  │  Expires: YYYY-MM-DD                               │
  │                                                     │
  │  [Holographic Overlay]  [UV Features]  [Microtext] │
  └────────────────────────────────────────────────────┘

Visual Design (Back):
  ┌────────────────────────────────────────────────────┐
  │  [Barcode: Code 128]                               │
  │  [Magnetic Stripe - Legacy Support]                │
  │                                                     │
  │  [Contact Chip Contacts]    [NFC Antenna Pattern]  │
  │                                                     │                     │
  │                                                     │
  │  Emergency Contact: 1-XXX-XXX-XXXX                 │
  │  Card Number: [Number]           │
  └────────────────────────────────────────────────────┘

Security Features:
  Physical:
    - Guilloche patterns (intricate line art)
    - Microtext (requires magnification to read)
    - UV-reactive ink (visible under blacklight)
    - Holographic overlay (3D security image)
    - Laser engraving (cannot be removed)
    - Tactile features (raised text for visually impaired)
  
  Electronic:
    - Encrypted chip-to-reader communication
    - Mutual authentication (card ↔ reader)
    - Session keys (unique per transaction)
    - Anti-cloning (unique chip identifier)
    - Tamper detection (destroys keys if attacked)
```

#### 3. PIV Reader Infrastructure

**Required Reader Types Across Ecosystem:**

```yaml
Desktop/Wall-Mounted Readers (OS-PACS Integration):
  Primary Model: HID Omnikey 5427 CK Gen2
  Interface: USB Type-A
  Protocols: ISO 14443A/B, ISO 15693, ISO 7816
  Read Distance: Contact + contactless (up to 10cm)
  Certifications: FIPS 201 approved, TAA compliant
  Use Cases:
    - Building door access (OS-PACS readers)
    - Workstation login (desktop computers)
    - Time & attendance kiosks
    - Evidence upload stations (PBCEN)
  
  Quantity Required:
    - Per building: 2-20 readers (based on door count)
    - Per workstation: 1 reader (for system login)
    - Province-wide estimate: 50,000-100,000 readers

Mobile/Handheld Readers (Field Operations):
  Primary Model: Thursby TSS Wedge Bluetooth PIV Reader
  Interface: Bluetooth 5.0 LE
  Compatibility: iOS, Android, Windows
  Battery: 8 hours continuous use
  Certifications: FIPS 201 approved
  Use Cases:
    - Vehicle-mounted readers (PSVN-Fleet)
    - Body camera activation (PBCEN tap-to-activate)
    - AR glasses pairing (PXRSN)
    - Mobile evidence collection
    - Field identity verification
  
  Quantity Required:
    - Per patrol vehicle: 1 reader
    - Per body camera station: 1 reader  
    - Per mobile workstation: 1 reader
    - Province-wide estimate: 5,000-10,000 readers

Vehicle-Integrated Readers (PSVN-Fleet):
  Primary Model: Custom OEM integration (Panasonic Toughbook)
  Mounting: Dashboard-mounted, ruggedized housing
  Protocols: Contact + contactless PIV
  Integration: CAN bus vehicle integration
  Features:
    - Vehicle ignition interlock (PIV required to start)
    - Automatic driver logging
    - Multi-user support (shift changes)
    - Tamper alerts
  
  Quantity Required:
    - Per patrol vehicle: 1 integrated reader
    - Province-wide estimate: 2,000-3,000 readers

Specialized Readers:
  Body Camera Activation (PBCEN):
    - Model: Custom NFC reader integrated into docking station
    - Function: Tap PIV card to body cam to activate/upload
    - Security: Encrypted pairing with specific officer
  
  Drone Authorization (PASSN):
    - Model: Ruggedized contactless reader (outdoor rated)
    - Function: Tap PIV to authorize drone flight
    - Features: GPS location logging, weather sealed
  
  AR Glasses Pairing (PXRSN):
    - Model: Miniaturized NFC reader (wearable form factor)
    - Function: Tap PIV to pair glasses with user profile
    - Integration: Bluetooth LE to glasses

Reader Management Infrastructure:
  Reader Controller Software:
    - Platform: OS-PACS (Leosac) integration
    - Function: Centralized reader configuration
    - Features:
      └─ Firmware updates (OTA)
      └─ Health monitoring
      └─ Certificate distribution
      └─ Offline operation mode
  
  Network Requirements:
    - Dedicated security VLAN (802.1X authentication)
    - Power over Ethernet (PoE+, 30W per reader)
    - Managed switches (Cisco Catalyst or equivalent)
    - Redundant network paths (HA)
```

---

## Integration with Seven Provincial Pillars

### 1. OS-PACS + PIV Integration (Building Access Control)

**Capability**: PIV-authenticated physical access to buildings, rooms, and secure areas

```yaml
Integration Architecture:
  Authentication Flow:
    1. User presents PIV card to OS-PACS reader
    2. Reader extracts PIV Authentication Certificate
    3. Reader validates certificate chain (Provincial CA)
    4. Reader sends certificate to Leosac controller
    5. Leosac queries Provincial PIV Authority (OCSP check)
    6. Leosac matches certificate serial to user account
    7. Leosac evaluates access policy (role, time, location)
    8. Grant or deny access
    9. Log event with certificate serial number
  
  Leosac Configuration:
    auth_sources:
      - type: piv_card
        ca_certificate: /etc/leosac/provincial_ca.pem
        ocsp_responder: https://ocsp.provincial-piv.on.ca
        crl_url: https://crl.provincial-piv.on.ca/provincial.crl
        cache_timeout: 3600
        offline_grace_period: 86400  # 24 hours
    
    credential_format:
      - piv_auth:
          certificate_serial: required
          subject_dn: required
          issuer_dn: required
          fingerprint_sha256: required
    
    access_policies:
      - name: security_guard_standard
        subject_cn_pattern: "SG-ON-*"
        allowed_doors: [entrance, patrol_route, break_room]
        time_restrictions:
          - weekdays: 06:00-22:00
          - weekends: 08:00-20:00
      
      - name: security_supervisor
        subject_cn_pattern: "SG-ON-*-SUP"
        allowed_doors: all
        time_restrictions: none
        requires_pin: true  # Two-factor for supervisors

User Enrollment Process:
  1. Identity Verification (RA station):
     - Government-issued photo ID
     - Criminal background check (CPIC query)
     - Employer verification letter
     - Two-factor identity proofing
  
  2. PIV Card Issuance:
     - Capture biometrics (photo, 2 fingerprints)
     - Personalize PIV card (write certificates)
     - Print visual layout (photo, name, ID)
     - Activate card (PIN setup)
  
  3. OS-PACS Account Creation:
     - Extract certificate serial from PIV card
     - Create Leosac user account
     - Assign role (security_guard, supervisor, admin)
     - Grant door permissions
     - Set schedule (shift patterns)
  
  4. Credential Delivery:
     - Hand PIV card to user (in-person)
     - User signs receipt (audit trail)
     - User tests card at reader (validation)
     - User sets PIN (4-8 digits, complexity rules)

Dual Credential Support (Transition Period):
  Legacy Credentials:
    - Existing 125kHz proximity cards
    - HID iClass credentials
    - Mobile credentials (BLE)
  
  Migration Strategy:
    - Phase 1: PIV + legacy both accepted (12 months)
    - Phase 2: PIV required, legacy as backup (6 months)
    - Phase 3: PIV only (legacy disabled)
  
  Implementation:
    users:
      - id: john_doe
        credentials:
          - type: piv_card
            certificate_serial: "1A2B3C4D5E6F"
            primary: true
          - type: legacy_prox
            facility_code: 123
            card_number: 45678
            expires: 2026-06-01
```

### 2. PSVN + PIV Integration (Video Network Access)

**Capability**: PIV-authenticated access to live and recorded video across organizational boundaries

```yaml
Integration Architecture:
  Video Access Control Flow:
    1. Guard logs into PSVN portal (web or mobile app)
    2. Browser/app prompts for PIV card
    3. User inserts PIV card into reader
    4. Application extracts PIV Authentication Certificate
    5. Application validates certificate (OCSP check)
    6. Application sends certificate to PSVN Federation Hub
    7. Hub queries access control policy engine
    8. Policy engine checks:
       - Certificate validity (not revoked, not expired)
       - User role (guard, supervisor, law enforcement)
       - Organization membership
       - Site-specific grants (which cameras can user see?)
       - Time-based restrictions
    9. Hub returns authorized camera list
    10. User can view live/recorded video
    11. All access logged with certificate serial + timestamp
  
  PSVN Policy Engine:
    camera_access_policies:
      - role: security_guard
        scope: own_organization
        permissions:
          - live_view: cameras_at_assigned_sites
          - playback: last_7_days
          - download: clips_up_to_5_minutes
          - share: within_organization_only
      
      - role: security_supervisor
        scope: organization_wide
        permissions:
          - live_view: all_organization_cameras
          - playback: last_30_days
          - download: clips_up_to_30_minutes
          - share: cross_organization (audit logged)
      
      - role: law_enforcement
        scope: province_wide
        permissions:
          - live_view: all_participating_cameras
          - playback: unlimited (with warrant reference)
          - download: unlimited
          - share: evidence management system
          - emergency_override: true

Certificate-Based Access Control (PSVN):
  Authorization Token Generation:
    1. User authenticates with PIV certificate
    2. PSVN Hub generates JWT (JSON Web Token):
       - Header: { "alg": "RS256", "kid": "psvn-2025" }
       - Payload: {
           "sub": "SG-ON-123456",
           "cert_serial": "1A2B3C4D5E6F",
           "role": "security_guard",
           "org": "ABC_Security_Inc",
           "sites": ["site_001", "site_042", "site_193"],
           "permissions": ["live_view", "playback_7days"],
           "iat": 1703001234,
           "exp": 1703087634  # 24-hour expiration
         }
       - Signature: RS256(header + payload, PSVN private key)
    
    3. User includes JWT in all camera requests
    4. Camera validates JWT signature (PSVN public key)
    5. Camera grants/denies based on JWT permissions

Cross-Organization Video Sharing:
  Sharing Flow:
    1. Guard at Site A witnesses incident
    2. Guard exports 5-minute video clip
    3. System generates secure share link:
       - Link: https://psvn.on.ca/share/abc123xyz
       - Expiration: 48 hours
       - Access: PIV authentication required
       - Log: every view recorded (who, when, IP)
    
    4. Guard shares link with police officer
    5. Officer authenticates with their PIV card
    6. System validates officer role + jurisdiction
    7. Officer views clip (audit logged)
    8. Officer can download for evidence (chain-of-custody)
  
  Evidence Chain-of-Custody:
    video_evidence_metadata:
      - clip_id: VID-2025-001234
        source_camera: CAM-SITE042-012
        timestamp: 2025-12-15T14:23:45Z
        duration: 300  # 5 minutes
        exported_by:
            piv_serial: "1A2B3C4D5E6F"
            name: "John Doe"
            organization: "ABC Security Inc"
        accessed_by:
          - piv_serial: "9F8E7D6C5B4A"
            name: "Officer Jane Smith"
            badge_number: "12345"
            timestamp: 2025-12-15T15:01:12Z
            action: viewed
          - piv_serial: "9F8E7D6C5B4A"
            name: "Officer Jane Smith"
            timestamp: 2025-12-15T15:03:45Z
            action: downloaded
            case_number: "2025-CR-98765"
        hash_sha256: "a1b2c3d4e5f6..."
        signature: "-----BEGIN PGP SIGNATURE-----..."
```

### 3. PBCEN + PIV Integration (Body Camera Evidence Network)

**Capability**: PIV-authenticated body camera activation, evidence upload, and access control

```yaml
Integration Architecture:
  Body Camera Activation Flow (Tap-to-Activate):
    1. Officer taps PIV card to body camera docking station
    2. Docking station NFC reader extracts certificate
    3. Docking station validates certificate (offline cache OK)
    4. System pairs camera with officer:
       - Serial number: BC-2025-12345
       - Officer PIV: SG-ON-123456 (cert serial: 1A2B3C...)
       - Timestamp: 2025-12-15T08:00:00Z
       - Shift: Day shift (08:00-16:00)
    5. Camera is unlocked and ready for use
    6. All footage tagged with officer PIV serial
    7. At shift end, officer taps PIV to upload footage
    8. System verifies same officer (prevents tampering)
    9. Footage uploaded with chain-of-custody intact
  
  Body Camera Hardware Integration:
    Camera Model: Axon Body 4 (or equivalent)
    Modifications for PIV:
      - Add NFC reader to docking station
      - Integrate with Provincial PIV validation
      - Embed PIV serial in video metadata (watermark)
      - Encrypt footage with officer's PIV public key
    
    Docking Station:
      - Model: Axon Fleet 3 (modified)
      - PIV Reader: Integrated NFC (ISO 14443A)
      - Function: Charge + upload + PIV authentication
      - Network: Dedicated evidence VLAN
      - Storage: Temporary cache (uploads to PBCEN)

Evidence Upload & Access Control:
  Upload Process:
    1. Officer completes shift
    2. Officer docks body camera
    3. Officer taps PIV card to authorize upload
    4. System validates:
       - PIV serial matches camera assignment
       - Timestamp within shift window
       - No evidence of tampering (hash check)
    5. Footage uploaded to PBCEN storage
    6. Metadata recorded:
       metadata:
         - video_id: VID-BC-2025-001234
           camera_serial: BC-2025-12345
           officer_piv: "1A2B3C4D5E6F"
           officer_name: "John Doe"
           shift_start: 2025-12-15T08:00:00Z
           shift_end: 2025-12-15T16:00:00Z
           duration: 28800  # 8 hours
           upload_timestamp: 2025-12-15T16:15:23Z
           hash_sha256: "abc123..."
           encrypted: true
           encryption_key_id: "PIV-1A2B3C4D5E6F-PUB"
  
  Evidence Access Control:
    Roles & Permissions:
      - officer (owner): Can view own footage, cannot delete
      - supervisor: Can view subordinates' footage
      - investigator: Can view footage related to case
      - law_enforcement: Can request footage (audit logged)
      - court_order: Full access with legal authorization
    
    Access Request Flow:
      1. Detective needs footage for investigation
      2. Detective authenticates with PIV card
      3. Detective searches PBCEN: "incident at 123 Main St, Dec 15"
      4. System finds relevant footage
      5. System checks access policy:
         - Detective role: investigator
         - Case number required: Yes
         - Supervisor approval: Required for first access
      6. Detective enters case number: 2025-CR-98765
      7. System notifies supervisor (email + SMS)
      8. Supervisor approves (tap PIV card)
      9. Detective can now view footage
      10. All access logged:
          access_log:
            - video_id: VID-BC-2025-001234
              accessed_by_piv: "9F8E7D6C5B4A"
              accessed_by_name: "Det. Jane Smith"
              case_number: "2025-CR-98765"
              approved_by_piv: "2E3F4A5B6C7D"
              approved_by_name: "Sgt. Bob Johnson"
              timestamp: 2025-12-16T09:23:45Z
              action: viewed
              duration_watched: 1200  # 20 minutes

Privacy & Redaction:
  Automatic Redaction (AI-powered):
    - Face blurring (non-suspects, bystanders)
    - License plate obscuring (unless relevant)
    - Voice distortion (protect witnesses)
    - PII removal (SSN, credit cards shown on screen)
  
  Access Levels:
    - Level 1 (Unredacted): Investigator with case number
    - Level 2 (Semi-redacted): Supervisor review
    - Level 3 (Fully redacted): Public release (FOI request)
  
  Redaction Audit:
    - Every redaction logged
    - AI confidence scores recorded
    - Manual review required before Level 3 release
```

### 4. PSVN-Fleet + PIV Integration (Vehicle Network)

**Capability**: PIV-authenticated vehicle assignment, tracking, and cross-agency coordination

```yaml
Integration Architecture:
  Vehicle Assignment Flow:
    1. Officer reports for shift
    2. Officer taps PIV card to vehicle-mounted reader
    3. Vehicle system validates PIV certificate
    4. System checks:
       - Officer authorized to drive this vehicle class
       - Officer's driver's license valid (DMV integration)
       - Officer not flagged (suspension, investigation)
       - Vehicle available (not assigned to another officer)
    5. System assigns vehicle to officer:
       assignment:
         - vehicle_id: PATROL-2025-042
           officer_piv: "1A2B3C4D5E6F"
           officer_name: "John Doe"
           shift_start: 2025-12-15T08:00:00Z
           odometer_start: 125432
           fuel_level_start: 87%
    6. Vehicle ignition unlocked (PIV required to start)
    7. AVL/GPS tracking begins (officer location)
    8. Radio system auto-configures (officer callsign)
  
  Vehicle-Integrated PIV Reader:
    Hardware:
      - Panasonic Toughbook CF-33 (ruggedized laptop)
      - Integrated PIV card reader (HID Omnikey)
      - Dashboard mount (adjustable, lockable)
      - Vehicle power (hardwired, ignition-switched)
      - Backup battery (4-hour runtime)
    
    Software:
      - OS: Windows 10 IoT Enterprise LTSC
      - Application: PSVN-Fleet Mobile Client
      - Authentication: PIV-based login (no password)
      - Connectivity: 4G LTE + WiFi (vehicle hotspot)
    
    Integration:
      - CAN bus: Vehicle telemetry (speed, fuel, diagnostics)
      - Ignition interlock: PIV required to start vehicle
      - Dash camera: Auto-activate when PIV present
      - Radio: Auto-configure callsign from PIV

Cross-Agency Vehicle Sharing:
  Scenario: Officer from Agency A needs vehicle from Agency B
  
  Authorization Flow:
    1. Officer A arrives at Agency B's station
    2. Officer A taps PIV card to Agency B vehicle
    3. Vehicle system validates PIV certificate
    4. System recognizes cross-agency request
    5. System notifies Agency B supervisor (auto-approval rules)
    6. If approved:
       - Vehicle assigned to Officer A (temporary)
       - Officer A's agency billed (automatic)
       - GPS tracking shared with both agencies
       - Radio channels bridged
    7. Officer A completes task, returns vehicle
    8. System logs usage:
       usage_log:
         - vehicle_id: PATROL-AgencyB-015
           borrowing_officer_piv: "1A2B3C4D5E6F"
           borrowing_agency: "Agency_A"
           lending_agency: "Agency_B"
           authorized_by: "Supervisor PIV: 2E3F4A5B..."
           start_time: 2025-12-15T10:23:12Z
           end_time: 2025-12-15T12:45:56Z
           miles_driven: 47
           fuel_used: 2.3_gallons
           billing_rate: $50/hour
           total_charge: $125.00

Automated Suspect Vehicle Tracking:
  ALPR + PIV Integration:
    1. ALPR camera detects suspect vehicle (plate: ABC-1234)
    2. ALPR system alerts all patrol vehicles in PSVN-Fleet
    3. Officer in nearest vehicle receives alert:
       alert:
         - type: suspect_vehicle
           plate: "ABC-1234"
           vehicle_desc: "Black Honda Accord"
           last_seen: "Main St & 1st Ave, 2025-12-15T14:23:45Z"
           direction: "Northbound"
           case_number: "2025-CR-98765"
           officer_alerted_piv: "1A2B3C4D5E6F"
    4. Officer acknowledges alert (tap PIV card)
    5. System updates officer's assignment (pursuit authorized)
    6. If officer locates vehicle:
       - Officer taps "Suspect Located" (PIV confirmation)
       - GPS location logged
       - Dash camera flagged (auto-save footage)
       - Backup units auto-dispatched
```

### 5. PASSN + PIV Integration (Drone Network)

**Capability**: PIV-authenticated drone authorization and flight logging

```yaml
Integration Architecture:
  Drone Flight Authorization Flow:
    1. Operator taps PIV card to drone controller
    2. Controller validates PIV certificate
    3. System checks:
       - Operator has drone pilot license (TC database)
       - Operator authorized for this drone class
       - Flight zone approved (geofencing check)
       - Weather conditions acceptable
    4. System logs flight plan:
       flight_plan:
         - flight_id: DRONE-2025-001234
           operator_piv: "1A2B3C4D5E6F"
           operator_name: "John Doe"
           drone_serial: "DJI-M300-12345"
           takeoff_location: [43.6532, -79.3832]  # GPS
           planned_route: [waypoint_array]
           purpose: "Perimeter patrol, Site 042"
           authorization_timestamp: 2025-12-15T14:00:00Z
    5. Drone unlocked (motors enabled)
    6. Flight begins (all telemetry logged)
    7. Video feed tagged with operator PIV serial
  
  Drone Hardware Integration:
    Drone Model: DJI Matrice 300 RTK (or equivalent)
    Modifications:
      - Add NFC reader to controller (PIV authentication)
      - Integrate with Provincial PIV validation
      - Embed PIV serial in video metadata
      - Geofencing enforced (restricted zones)
    
    Controller:
      - DJI RC Plus (ruggedized)
      - PIV Reader: Bluetooth NFC module
      - Network: 4G LTE (real-time telemetry)
      - Storage: Local cache (uploads to PASSN)

Cross-Agency Drone Sharing:
  Scenario: Agency A needs specialized drone from Agency B
  
  Authorization:
    1. Operator from Agency A logs into PASSN portal
    2. Operator requests Agency B's thermal imaging drone
    3. System checks:
       - Operator PIV certificate valid
       - Operator has thermal drone certification
       - Agency B approves cross-agency use (auto-rule)
    4. System generates temporary authorization:
       temp_auth:
         - drone_id: "THERMAL-AgencyB-003"
           authorized_operator_piv: "1A2B3C4D5E6F"
           authorization_expires: 2025-12-15T18:00:00Z
           restrictions:
             - max_altitude: 400_feet
             - geofence: [defined_polygon]
             - max_flight_time: 2_hours
    5. Operator taps PIV to Agency B drone (authorization valid)
    6. Drone unlocked for this operator (time-limited)
    7. All footage shared with both agencies
```

### 6. PISN + PIV Integration (Intelligent Services Network)

**Capability**: PIV-authenticated visitor registration and building services

```yaml
Integration Architecture:
  Visitor Registration Flow:
    1. Visitor arrives at building reception
    2. Security guard logs into PISN portal
    3. Guard taps their PIV card (authentication)
    4. Guard enters visitor details:
       visitor:
         - name: "Jane Visitor"
           company: "ABC Corp"
           purpose: "Meeting with Bob Manager"
           host_name: "Bob Manager"
           expected_duration: 2_hours
           registered_by_piv: "1A2B3C4D5E6F"
    5. System generates temporary visitor credential:
       - Type: QR code + NFC badge
       - Valid: 2 hours
       - Access: Lobby + Meeting Room 5
       - Escort required: No
    6. System notifies host (email + SMS)
    7. Visitor receives badge (printed + digital)
    8. Visitor taps badge to door reader (OS-PACS integration)
    9. Access logged with visitor ID + guard PIV who issued
  
  Cross-Organization Visitor Credentials:
    Universal Visitor Registry:
      - Visitor registers once (background check)
      - Credential valid province-wide
      - Organizations opt-in to accept
      - Trust based on issuing organization's PIV
    
    Example:
      1. Contractor registers at Company A (background check)
      2. Company A guard issues universal visitor credential
      3. Contractor can now visit Company B, C, D (pre-authorized)
      4. Each visit logged (who, where, when)
      5. Any security incident → all organizations notified

Building Services (AI Concierge):
  PIV-Authenticated Service Requests:
    1. Employee wants to book conference room
    2. Employee taps PIV card to kiosk (or uses mobile app)
    3. System validates PIV certificate
    4. System shows available rooms (based on employee's organization)
    5. Employee books room (2PM-4PM, Meeting Room 3)
    6. System:
       - Reserves room in calendar
       - Updates door access (room unlocked during booking)
       - Notifies AV system (auto-configure projector)
       - Logs booking with employee PIV serial
```

### 7. PXRSN + PIV Integration (AR Glasses Network)

**Capability**: PIV-authenticated AR glasses pairing and situational awareness

```yaml
Integration Architecture:
  AR Glasses Pairing Flow:
    1. Officer powers on AR glasses (RealWear Navigator 520)
    2. Glasses prompt: "Tap PIV card to pair"
    3. Officer taps PIV card to miniature NFC reader (wrist-worn)
    4. Reader extracts PIV certificate
    5. Reader pairs with glasses via Bluetooth
    6. System configures glasses for officer:
       profile:
         - officer_piv: "1A2B3C4D5E6F"
           officer_name: "John Doe"
           role: "Security Guard"
           organization: "ABC Security Inc"
           authorized_apps:
             - navigation (real-time maps)
             - facial_recognition (suspect database)
             - vehicle_lookup (license plate query)
             - building_layout (indoor maps)
             - translation (real-time language)
    7. Glasses display HUD with officer info
    8. All AR interactions logged with PIV serial
  
  AR Hardware Integration:
    AR Glasses: RealWear Navigator 520
    Modifications:
      - Integrate with Provincial PIV validation
      - Embed PIV serial in all captured media
      - Real-time OCSP validation (certificate status)
    
    Wrist-Worn PIV Reader:
      - Model: Custom miniature NFC reader
      - Form Factor: Wristband (like smartwatch)
      - Battery: 24 hours continuous
      - Connectivity: Bluetooth 5.0 LE to glasses
      - Function: PIV authentication + quick-tap commands

Real-Time Facial Recognition (PIV-Authorized):
  Workflow:
    1. Officer wearing AR glasses
    2. Officer encounters suspicious person
    3. Officer voice command: "Identify person"
    4. Glasses capture photo (privacy overlay shown)
    5. Photo sent to PXRSN facial recognition service
    6. Service validates:
       - Officer PIV certificate (authorization check)
       - Officer's role allows facial recognition (RBAC)
       - Reason code provided (officer must state)
    7. Service searches databases:
       - Wanted persons (active warrants)
       - Missing persons
       - Known associates (gang members)
    8. Results displayed in AR HUD:
       result:
         - name: "Suspect Name" (if match found)
           confidence: 98.5%
           warrant_status: "Active warrant - Robbery"
           last_seen: "Main St, 2 days ago"
           approached_by_piv: "1A2B3C4D5E6F"
           query_timestamp: 2025-12-15T14:23:45Z
    9. Officer can take action (arrest, question, etc.)
    10. All queries logged (audit trail for civil rights)
```

### 8. PSRFIP + PIV Integration (Military Reserve Program)

**Capability**: Dual-credential PIV card (civilian + military) for reserve mobilization

```yaml
Integration Architecture:
  Dual-Credential PIV Card:
    Civilian Certificate:
      - Issuer: Provincial PIV Authority
      - Subject DN: CN=John Doe, OU=ABC Security Inc, O=Ontario
      - Usage: Building access, video network, body cameras
      - Validity: 3 years
    
    Military Certificate:
      - Issuer: Department of National Defence CA
      - Subject DN: CN=Pte John Doe, OU=Primary Reserve, O=Canadian Forces
      - Military ID: CF-RES-789012
      - Rank: Private
      - Unit: 32 Canadian Brigade Group
      - Usage: Base access, military training, mobilization
      - Validity: 5 years (renewable)
    
    Card Data Model:
      - Slot 1: Civilian PIV Auth Certificate
      - Slot 2: Military PIV Auth Certificate
      - Slot 3: Digital Signature Certificate (dual-use)
      - Slot 4: Encryption Certificate (dual-use)
      - PIN 1: Civilian operations (4-digit)
      - PIN 2: Military operations (6-digit, higher security)

Mobilization Workflow:
  Emergency Mobilization:
    1. National emergency declared (government order)
    2. DND sends mobilization order to all reserve units
    3. Dual-enrolled guards receive SMS + email:
       "Report to [Armory] by [Deadline]. Bring PIV card."
    4. Guard arrives at armory
    5. Guard taps PIV card to military access control
    6. System reads military certificate (Slot 2)
    7. System validates:
       - Certificate valid (not revoked, not expired)
       - Rank and unit correct
       - Medical fitness current
       - Training certifications up-to-date
    8. System logs attendance:
       mobilization_log:
         - event_id: MOBEX-2025-001
           member_piv: "1A2B3C4D5E6F"
           military_id: "CF-RES-789012"
           rank: "Private"
           unit: "32 CBG"
           arrival_time: 2025-12-15T06:23:12Z
           status: "Ready for deployment"
    9. System grants access to:
       - Weapons storage (issue rifle, ammo)
       - Equipment storage (issue uniform, gear)
       - Vehicle motor pool (assign transport)
    10. Guard transitions to military role (active duty)
  
  Dual-Use Equipment Access:
    Body Cameras (PBCEN):
      - Civilian mode: Evidence recording (police powers)
      - Military mode: Combat action recorder (ROE compliance)
      - Switch: PIN 2 activates military mode
    
    Vehicles (PSVN-Fleet):
      - Civilian mode: Patrol vehicle
      - Military mode: Troop transport / convoy
      - Switch: Military certificate enables military functions
    
    Drones (PASSN):
      - Civilian mode: Security surveillance
      - Military mode: Tactical ISR (Intelligence/Surveillance/Recon)
      - Switch: Geofencing rules change (military zones OK)
```

---

## PIV Lifecycle Management

### Enrollment & Issuance

```yaml
Enrollment Process:
  Step 1: Identity Verification (In-Person at RA Station)
    Required Documents:
      - Government-issued photo ID (driver's license, passport)
      - Proof of employment (security company letter)
      - Criminal background check (CPIC query, negative result)
      - Proof of address (utility bill, lease agreement)
    
    Verification Steps:
      1. RA officer validates photo ID (UV light, hologram check)
      2. RA officer queries CPIC database (criminal history)
      3. RA officer contacts employer (verify employment)
      4. RA officer captures biometrics:
         - Photo (2000x2500 pixels, JPEG2000)
         - Fingerprints (2 fingers, 500 DPI, WSQ format)
         - (Optional) Iris scan (for high-security roles)
      5. RA officer generates enrollment token (valid 24 hours)
  
  Step 2: Background Check (Automated + Manual Review)
    Automated Checks:
      - CPIC criminal history (Royal Canadian Mounted Police)
      - Credit check (Equifax, for financial roles)
      - Sex offender registry (high-risk positions)
      - Terrorist watchlist (CSIS, for critical infrastructure)
    
    Manual Review:
      - Employment history verification (past 5 years)
      - Reference checks (2 professional references)
      - Education verification (for specialized roles)
      - Foreign travel history (for national security positions)
    
    Approval Criteria:
      - No violent crimes (5 years minimum)
      - No fraud/theft (3 years minimum)
      - No drug trafficking (lifetime ban)
      - No terrorism affiliation (lifetime ban)
      - Credit score >600 (for financial access)
  
  Step 3: PIV Card Personalization (Automated at RA Station)
    Card Production:
      1. RA system generates key pairs (on-card):
         - PIV Authentication (RSA-2048)
         - Digital Signature (RSA-2048)
         - Key Management (RSA-2048)
         - Card Authentication (ECC P-256)
      2. RA system requests certificates from Issuing CA
      3. Issuing CA signs certificates, returns to RA
      4. RA writes certificates to card slots
      5. RA writes biometric data (fingerprints, photo)
      6. RA writes CHUID (Card Holder Unique Identifier)
      7. RA prints visual layout (photo, name, ID, expiration)
      8. RA applies holographic overlay (anti-counterfeiting)
    
    Card Activation:
      1. User sets PIN (4-8 digits, complexity rules)
      2. User confirms receipt (signature on tablet)
      3. User tests card at reader (validation)
      4. Card status set to ACTIVE in database
    
    Time to Issue: 15-30 minutes per card

Issuance SLA:
  - Walk-in enrollment: Card issued same day
  - Background check required: Card issued within 5 business days
  - Expedited (emergency): Card issued within 4 hours (fee applies)
```

### Renewal

```yaml
Renewal Process:
  Notification:
    - 90 days before expiration: Email reminder
    - 60 days before expiration: Email + SMS reminder
    - 30 days before expiration: Email + SMS + postal mail
    - 7 days before expiration: Daily email + SMS
  
  Renewal Methods:
    Option 1: Online Renewal (No Identity Change)
      Eligibility:
        - No legal name change
        - No appearance change (same photo acceptable)
        - No criminal charges since last issue
      
      Process:
        1. User logs into PIV portal (existing PIV card)
        2. User reviews current information (confirm accuracy)
        3. User pays renewal fee ($50)
        4. System performs background check (automated)
        5. If approved:
           - New certificates generated (same card)
           - Expiration date extended (+3 years)
           - User receives confirmation email
        6. Old card remains valid (no re-issue needed)
      
      Time: 5 minutes (instant approval if background check passes)
    
    Option 2: In-Person Renewal (Identity Change)
      Eligibility:
        - Name change (marriage, legal name change)
        - Significant appearance change (new photo required)
        - Card lost/stolen (re-issue with revocation)
      
      Process:
        1. User books appointment at RA station
        2. User brings required documents (see enrollment)
        3. RA officer updates information
        4. New biometrics captured (photo, fingerprints)
        5. New card issued (old card revoked)
      
      Time: 30 minutes (same-day issuance)

Grace Period:
  - Cards remain valid for 30 days past expiration
  - Access limited to essential functions (emergency only)
  - Renewal fee increases after expiration (+$25 late fee)
```

### Revocation

```yaml
Revocation Triggers:
  Immediate Revocation (Effective Instantly):
    - Card reported lost or stolen
    - Employee terminated for cause
    - Criminal arrest (violent crime, theft, fraud)
    - Security clearance revoked
    - Card compromised (private key exposed)
  
  Pending Revocation (Investigation Period):
    - Employee under investigation (fraud, misconduct)
    - Pending criminal charges (non-violent)
    - Employer requests temporary suspension
    - Medical leave (long-term disability)

Revocation Process:
  Step 1: Trigger Event
    - Automated: CPIC arrest notification
    - Manual: Employer submits revocation request
    - Self-reported: User reports card lost
  
  Step 2: Certificate Revocation
    1. Issuing CA adds certificate to CRL (Certificate Revocation List)
    2. CRL published (updated hourly, https://crl.provincial-piv.on.ca)
    3. OCSP responder updated (real-time, <1 second)
    4. Card status set to REVOKED in database
  
  Step 3: Access Removal
    - All systems check OCSP before granting access
    - Access denied within 1 minute of revocation
    - Systems with offline grace period (24 hours):
      └─ Access denied at next CRL update (hourly)
  
  Step 4: Physical Card Recovery (If Possible)
    - Employer collects card from terminated employee
    - Card returned to RA station (destruction)
    - If card not recoverable:
      └─ Card remains revoked (unusable)
      └─ Replacement fee applies if re-issued

Revocation Audit:
  Every revocation logged:
    - Who requested revocation (PIV serial or system ID)
    - Reason for revocation (lost, terminated, arrest, etc.)
    - Timestamp (when revocation took effect)
    - Confirmation (OCSP updated, CRL published)
```

### Recovery (Lost/Stolen Cards)

```yaml
Lost/Stolen Reporting:
  Reporting Methods:
    - Online: PIV portal (https://piv.provincial.on.ca/report-lost)
    - Phone: 24/7 hotline (1-800-PIV-LOST)
    - In-person: RA station (walk-in)
  
  Immediate Actions:
    1. User reports card lost/stolen
    2. System prompts for verification:
       - Full name
       - Date of birth
       - Last 4 digits of ID number
       - Security question answer
    3. If verified:
       - Certificate revoked immediately (OCSP + CRL)
       - Access denied within 1 minute
       - User receives confirmation (email + SMS)
       - Police report generated (if stolen)
  
  Replacement Process:
    1. User books appointment at RA station
    2. User brings photo ID (verification)
    3. RA officer validates identity (same as enrollment)
    4. RA officer confirms revocation (old cert unusable)
    5. New card issued (new serial number, new certificates)
    6. User pays replacement fee ($75)
    7. Old card flagged (cannot be reactivated)
  
  Time to Replace: Same day (30-minute appointment)
```

---

## Security & Compliance

### Cryptographic Standards

```yaml
Algorithms (FIPS 201-3 Compliant):
  Asymmetric:
    - RSA:
      - Key sizes: 2048-bit (standard), 3072-bit (high security), 4096-bit (max)
      - Padding: RSA-PSS (signatures), RSA-OAEP (encryption)
      - Usage: PIV Authentication, Digital Signature, Key Management
    
    - ECC:
      - Curves: P-256 (standard), P-384 (high security)
      - Usage: Card Authentication, ECDH key agreement
  
  Symmetric:
    - AES:
      - Key sizes: 128-bit (standard), 192-bit, 256-bit (max)
      - Modes: GCM (authenticated encryption), CBC (legacy)
      - Usage: Data encryption, secure messaging
    
    - 3DES:
      - Key size: 168-bit (legacy, deprecated 2024)
      - Usage: Backwards compatibility only
  
  Hash Functions:
    - SHA-2 family:
      - SHA-256 (standard, 256-bit output)
      - SHA-384 (high security, 384-bit output)
      - SHA-512 (maximum security, 512-bit output)
      - Usage: Digital signatures, HMAC, certificate fingerprints
    
    - SHA-3 family (optional, future):
      - SHA3-256, SHA3-384, SHA3-512
      - Usage: Next-generation applications

Certificate Profiles (X.509 v3):
  PIV Authentication Certificate:
    - Key Usage: Digital Signature
    - Extended Key Usage: Client Authentication (TLS)
    - Subject Alternative Name: UUID (FASC-N)
    - Validity: 3 years
  
  Digital Signature Certificate:
    - Key Usage: Digital Signature, Non-Repudiation
    - Extended Key Usage: Email Protection, Code Signing
    - Validity: 3 years
  
  Key Management Certificate:
    - Key Usage: Key Encipherment
    - Extended Key Usage: Email Protection
    - Validity: 3 years
  
  Card Authentication Certificate:
    - Key Usage: Digital Signature
    - Extended Key Usage: Client Authentication (contactless)
    - Validity: 3 years

Key Generation & Storage:
  On-Card Key Generation:
    - All private keys generated on PIV card (never exposed)
    - Keys cannot be exported (FIPS 140-2 Level 3)
    - Tamper detection (chip self-destructs if attacked)
  
  Certificate Signing:
    - Public key sent to Issuing CA (in CSR format)
    - CA signs certificate, returns to card
    - Private key remains on card (never leaves)
```

### Audit Logging

```yaml
Audit Requirements:
  All PIV Operations Logged:
    - Authentication attempts (success + failure)
    - Certificate issuance
    - Certificate renewal
    - Certificate revocation
    - Access grants (door, video, vehicle, etc.)
    - Access denials
    - Administrative actions (user account changes)
  
  Log Format (JSON):
    {
      "timestamp": "2025-12-15T14:23:45.123Z",
      "event_type": "piv_authentication",
      "result": "success",
      "user": {
        "piv_serial": "1A2B3C4D5E6F",
        "subject_dn": "CN=John Doe,OU=ABC Security Inc,O=Ontario",
        "role": "security_guard"
      },
      "resource": {
        "type": "door",
        "id": "SITE042-DOOR012",
        "location": "123 Main St, Building A, Floor 2"
      },
      "source_ip": "192.168.1.100",
      "reader_id": "READER-12345",
      "session_id": "sess_abc123xyz",
      "metadata": {
        "shift_id": "SHIFT-2025-12-15-DAY",
        "supervisor": "Jane Supervisor (PIV: 2E3F4A5B...)"
      }
    }
  
  Log Storage:
    - Primary: Elasticsearch cluster (30 days hot storage)
    - Archive: S3-compatible object storage (7 years cold storage)
    - Replication: 3 geographic zones (HA)
    - Encryption: AES-256-GCM (at rest), TLS 1.3 (in transit)
  
  Log Access:
    - Security Operations Center (SOC): Read-only, full access
    - Auditors: Read-only, specific time ranges
    - Law Enforcement: Read-only, warrant required
    - Administrators: No delete permissions (append-only)

SIEM Integration:
  Platform: Splunk Enterprise Security (or equivalent)
  Data Sources:
    - PIV CA (certificate lifecycle events)
    - OS-PACS (door access logs)
    - PSVN (video access logs)
    - PBCEN (body camera access logs)
    - PSVN-Fleet (vehicle assignment logs)
    - PASSN (drone authorization logs)
    - PISN (visitor registration logs)
    - PXRSN (AR glasses usage logs)
  
  Correlation Rules:
    - Impossible travel (access at 2 locations >100km apart in <1 hour)
    - Privilege escalation (role change without approval)
    - After-hours access (outside authorized schedule)
    - Excessive failures (10+ denials in 1 hour)
    - Concurrent sessions (same PIV used at 2 locations simultaneously)
    - Revoked credential use (attempt to use revoked certificate)
  
  Alerting:
    - Critical: Immediate (email + SMS + pager)
    - High: 15-minute delay (email + SMS)
    - Medium: 1-hour delay (email)
    - Low: Daily digest (email)
```

### Privacy Protection

```yaml
Data Minimization:
  Principle: Collect only necessary data, retain only required duration
  
  PIV Card Data (On-Card):
    - Photo: Required (visual identification)
    - Fingerprints: Required (biometric authentication)
    - Iris scan: Optional (high-security roles only)
    - Name: Required (legal name only)
    - ID number: Required (unique identifier)
    - Employment: Required (organization name only, no salary)
    - Address: Not stored on card (only in backend database)
    - SSN/SIN: Not stored (not required for PIV)
  
  Backend Database (Provincial PIV Authority):
    - Photo: 3-year retention (until card expiration)
    - Fingerprints: 3-year retention (encrypted at rest)
    - Background check: 5-year retention (audit trail)
    - Access logs: 7-year retention (legal compliance)
    - After retention: Automatic purge (cannot be recovered)

Access Control:
  Who Can Access PIV Data:
    - RA Officers: During enrollment/renewal only
    - SOC Analysts: Access logs only (no biometrics)
    - Auditors: Aggregate statistics only (no PII)
    - Law Enforcement: Warrant required (specific individual)
    - User (self): Full access to own data (via portal)
  
  Access Logging:
    - Every database query logged (who, what, when, why)
    - Annual audit of access logs (detect anomalies)
    - Unauthorized access = immediate investigation + notification

Consent & Transparency:
  User Rights:
    - Right to access: View all PIV data (via portal)
    - Right to correction: Request data correction (errors)
    - Right to deletion: Request account closure (with exceptions)
    - Right to portability: Export data (JSON format)
    - Right to notification: Notified of breaches (72 hours)
  
  Privacy Policy:
    - Published: https://piv.provincial.on.ca/privacy
    - Language: Plain language (no legalese)
    - Consent: Explicit opt-in (enrollment time)
    - Changes: 30-day notice before policy changes
```

---

## Deployment Roadmap

### Phase 1: Pilot Program (6 Months)

```yaml
Scope:
  - 500 security guards (5% of provincial workforce)
  - 10 security companies (participating organizations)
  - 3 municipalities (geographic diversity)
  - 2,000 doors (OS-PACS integration)
  - 100 cameras (PSVN integration)
  - 50 vehicles (PSVN-Fleet integration)

Infrastructure:
  PIV CA:
    - 1 Root CA (offline HSM)
    - 2 Issuing CAs (HA cluster)
    - 2 OCSP responders
    - 3 RA stations (enrollment locations)
  
  Card Production:
    - 1,000 PIV cards (500 active, 500 spare)
    - 10 card printers (RA stations)
  
  Reader Deployment:
    - 2,000 door readers (existing OS-PACS readers)
    - 100 mobile readers (vehicles, body cameras)
    - 3 RA workstations (enrollment)

Timeline:
  Month 1-2: Infrastructure Build
    - Deploy PIV CA (Root + Issuing)
    - Setup RA stations (3 locations)
    - Integrate with OS-PACS (Leosac config)
    - Train RA officers (identity verification)
  
  Month 3-4: User Enrollment
    - Enroll 500 guards (100 per week)
    - Issue PIV cards (same-day issuance)
    - Deploy door readers (2,000 readers)
    - Configure access policies (RBAC)
  
  Month 5-6: Integration Testing
    - Test OS-PACS (door access)
    - Test PSVN (video access)
    - Test PBCEN (body camera activation)
    - Test PSVN-Fleet (vehicle assignment)
    - Collect user feedback (surveys, interviews)
    - Measure performance (success rate, latency)

Success Metrics:
  - Enrollment time: <30 minutes per guard
  - Door access latency: <1 second (PIV tap to unlock)
  - Authentication success rate: >99.5%
  - User satisfaction: >4.0/5.0
  - Zero security incidents (unauthorized access)
  - Zero lost/stolen cards (proper handling procedures)
```

### Phase 2: Province-Wide Rollout (18 Months)

```yaml
Scope:
  - 10,000 security guards (100% provincial workforce)
  - 200 security companies
  - 20 municipalities
  - 50,000 doors
  - 10,000 cameras
  - 2,000 vehicles
  - 500 drones
  - 1,000 AR glasses

Infrastructure Scale-Up:
  PIV CA:
    - 1 Root CA (unchanged, offline HSM)
    - 6 Issuing CAs (HA cluster, 3 geographic zones)
    - 10 OCSP responders (load balanced)
    - 20 RA stations (major cities + mobile units)
  
  Card Production:
    - 25,000 PIV cards (10K active, 15K spare + renewals)
    - 50 card printers (RA stations + mobile)
  
  Reader Deployment:
    - 50,000 door readers
    - 10,000 mobile readers
    - 20 RA workstations

Timeline:
  Month 1-6: Infrastructure Expansion
    - Deploy additional Issuing CAs (geographic redundancy)
    - Setup additional RA stations (20 locations)
    - Integrate all provincial systems (7 pillars)
    - Train 100 RA officers
  
  Month 7-12: Mass Enrollment
    - Enroll 10,000 guards (200 per week)
    - Deploy 50,000 door readers
    - Integrate 200 security companies
    - Train 2,000 system administrators
  
  Month 13-18: Full Integration
    - All 7 pillars operational (PSVN, PBCEN, Fleet, etc.)
    - Cross-agency cooperation enabled
    - Data sharing agreements signed
    - Compliance audits passed

Success Metrics:
  - 100% of security guards enrolled
  - 100% of participating buildings integrated
  - >99.9% system uptime (SLA)
  - <1 second authentication latency (province-wide)
  - Zero major security breaches
  - >4.5/5.0 user satisfaction
```

### Phase 3: Advanced Features (12 Months)

```yaml
Scope:
  - Biometric secondary factor (fingerprint + PIV)
  - Mobile PIV (smartphone-based credentials)
  - Blockchain audit trail (immutable logs)
  - AI-powered anomaly detection
  - Cross-province federation (multi-province trust)

Features:
  Biometric Enhancement:
    - Fingerprint readers at high-security doors
    - Dual-factor: PIV card + fingerprint match
    - Fallback: PIN code (if biometric fails)
  
  Mobile PIV:
    - Virtual PIV card (smartphone app)
    - NFC emulation (tap phone to reader)
    - Biometric unlock (Face ID, Touch ID)
    - Revocation: Remote wipe (lost phone)
  
  Blockchain Audit:
    - Immutable access logs (cannot be altered)
    - Distributed ledger (3 geographic nodes)
    - Smart contract: Automatic compliance checks
  
  AI Anomaly Detection:
    - Behavioral analysis (normal vs abnormal access patterns)
    - Risk scoring (flagged users get extra scrutiny)
    - Predictive alerts (potential security incidents)

Timeline:
  Month 1-4: Biometric Rollout
    - Deploy fingerprint readers (high-security areas)
    - Enroll biometric templates (opt-in)
  
  Month 5-8: Mobile PIV
    - Develop smartphone app (iOS + Android)
    - Pilot test (1,000 users)
    - Full rollout (10,000 users)
  
  Month 9-12: Advanced Analytics
    - Deploy blockchain (audit trail)
    - Train AI models (anomaly detection)
    - Integrate with SIEM (correlation)
```

---

## Cost Analysis

### Capital Expenditures (CapEx)

```yaml
PIV Infrastructure (One-Time):
  Certificate Authority:
    - Root CA HSM: $150,000 (Thales Luna SA 7)
    - Issuing CA servers: $300,000 (6 servers, HA cluster)
    - OCSP responders: $100,000 (10 servers)
    - Load balancers: $50,000 (F5 BIG-IP)
    - Network equipment: $100,000 (switches, firewalls)
    - Software licenses: $200,000 (PKI software, SIEM)
    - Total CA Infrastructure: $900,000
  
  Registration Authority:
    - RA workstations: $100,000 (20 stations × $5,000)
    - PIV card readers: $20,000 (100 readers × $200)
    - Fingerprint scanners: $40,000 (20 scanners × $2,000)
    - Card printers: $250,000 (50 printers × $5,000)
    - Cameras (badge photos): $10,000 (20 cameras × $500)
    - Total RA Infrastructure: $420,000
  
  PIV Cards:
    - Initial stock: $625,000 (25,000 cards × $25 each)
    - Spare inventory: $250,000 (10,000 cards)
    - Total Cards: $875,000
  
  Reader Deployment:
    - Door readers: $10,000,000 (50,000 readers × $200)
    - Mobile readers: $2,000,000 (10,000 readers × $200)
    - Vehicle-integrated: $600,000 (2,000 vehicles × $300)
    - Specialized readers: $500,000 (drones, AR glasses, body cams)
    - Total Readers: $13,100,000
  
  Total CapEx: $15,295,000 (~$15.3M)

Per-User CapEx: $1,530 (for 10,000 users)
```

### Operating Expenditures (OpEx)

```yaml
Annual Operating Costs:
  Personnel:
    - RA officers: $2,000,000 (20 FTE × $100K salary)
    - PKI administrators: $600,000 (6 FTE × $100K)
    - SOC analysts: $1,200,000 (12 FTE × $100K)
    - Help desk: $800,000 (10 FTE × $80K)
    - Total Personnel: $4,600,000/year
  
  Infrastructure:
    - Data center (colocation): $500,000/year
    - Cloud services (OCSP, CRL): $200,000/year
    - Network bandwidth: $100,000/year
    - Software licenses (renewals): $300,000/year
    - Total Infrastructure: $1,100,000/year
  
  Consumables:
    - PIV cards (replacements): $500,000/year (20,000 cards × $25)
    - Card printer supplies: $100,000/year
    - Reader maintenance: $200,000/year
    - Total Consumables: $800,000/year
  
  Services:
    - Background checks: $500,000/year (10,000 checks × $50)
    - Compliance audits: $200,000/year
    - Penetration testing: $100,000/year
    - Total Services: $800,000/year
  
  Total OpEx: $7,300,000/year

Per-User OpEx: $730/year (for 10,000 users)
```

### Return on Investment (ROI)

```yaml
Cost Savings (Compared to Fragmented Systems):
  Eliminated Costs:
    - Per-system credentials: $5,000,000/year
      (10,000 users × 7 systems × $71/credential/year)
    - Password resets: $1,000,000/year
      (10,000 users × 10 resets/year × $10/reset)
    - Unauthorized access incidents: $2,000,000/year
      (reduced 90%, from $20M to $2M)
    - Manual identity verification: $500,000/year
      (security guard time saved)
    - Duplicate infrastructure: $3,000,000/year
      (per-system auth servers eliminated)
  
  Total Savings: $11,500,000/year

Net Benefit:
  Year 1:
    - Savings: $11,500,000
    - OpEx: $7,300,000
    - CapEx: $15,300,000 (amortized over 7 years = $2,186,000/year)
    - Net: $11,500,000 - $7,300,000 - $2,186,000 = $2,014,000 profit
  
  Year 2-7:
    - Savings: $11,500,000/year
    - OpEx: $7,300,000/year
    - Net: $4,200,000/year profit

7-Year ROI:
  - Total Investment: $15,300,000 (CapEx) + ($7,300,000 × 7) = $66,400,000
  - Total Savings: $11,500,000 × 7 = $80,500,000
  - Net Benefit: $80,500,000 - $66,400,000 = $14,100,000
  - ROI: ($14,100,000 / $66,400,000) × 100 = 21.2%
  - Payback Period: 3.1 years
```

---

## Appendix: Technical Specifications

### PIV Card Applet (Java Card)

```java
// Simplified PIV Card Applet (FIPS 201-3 Compliant)
package gov.provincial.piv;

import javacard.framework.*;
import javacard.security.*;
import javacardx.crypto.*;

public class PIVApplet extends Applet {
    
    // PIV AID: A0 00 00 03 08 00 00 10 00 01 00
    private static final byte[] PIV_AID = {
        (byte)0xA0, 0x00, 0x00, 0x03, 0x08,
        0x00, 0x00, 0x10, 0x00, 0x01, 0x00
    };
    
    // PIN management
    private OwnerPIN userPIN;
    private static final byte PIN_TRY_LIMIT = 3;
    private static final byte MAX_PIN_SIZE = 8;
    
    // Key pairs (PIV Authentication, Digital Signature, Key Management)
    private RSAPrivateKey privKeyAuth;
    private RSAPublicKey pubKeyAuth;
    private RSAPrivateKey privKeySign;
    private RSAPublicKey pubKeySign;
    private RSAPrivateKey privKeyKM;
    private RSAPublicKey pubKeyKM;
    
    // Card Authentication (ECC)
    private ECPrivateKey privKeyCardAuth;
    private ECPublicKey pubKeyCardAuth;
    
    // Certificates
    private byte[] certAuth;  // PIV Authentication Certificate
    private byte[] certSign;  // Digital Signature Certificate
    private byte[] certKM;    // Key Management Certificate
    private byte[] certCardAuth;  // Card Authentication Certificate
    
    // Biometric data
    private byte[] fingerprints;  // Encrypted fingerprint templates
    private byte[] facialImage;   // JPEG2000 photo
    
    // CHUID (Card Holder Unique Identifier)
    private byte[] chuid;
    
    private PIVApplet() {
        // Initialize PIN (default: 123456)
        userPIN = new OwnerPIN(PIN_TRY_LIMIT, MAX_PIN_SIZE);
        byte[] defaultPIN = {0x31, 0x32, 0x33, 0x34, 0x35, 0x36};
        userPIN.update(defaultPIN, (short)0, (byte)6);
        
        // Generate key pairs (2048-bit RSA)
        KeyPair kpAuth = new KeyPair(KeyPair.ALG_RSA, KeyBuilder.LENGTH_RSA_2048);
        kpAuth.genKeyPair();
        privKeyAuth = (RSAPrivateKey)kpAuth.getPrivate();
        pubKeyAuth = (RSAPublicKey)kpAuth.getPublic();
        
        // ... (additional key pairs for Sign, KM, CardAuth)
        
        register();
    }
    
    public static void install(byte[] bArray, short bOffset, byte bLength) {
        new PIVApplet();
    }
    
    public void process(APDU apdu) {
        byte[] buffer = apdu.getBuffer();
        
        // Check SELECT command
        if (selectingApplet()) {
            return;
        }
        
        // Process PIV commands
        switch (buffer[ISO7816.OFFSET_INS]) {
            case (byte)0x20:  // VERIFY PIN
                verifyPIN(apdu);
                break;
            case (byte)0x87:  // GENERAL AUTHENTICATE
                generalAuthenticate(apdu);
                break;
            case (byte)0xCB:  // GET DATA
                getData(apdu);
                break;
            case (byte)0xDB:  // PUT DATA
                putData(apdu);
                break;
            default:
                ISOException.throwIt(ISO7816.SW_INS_NOT_SUPPORTED);
        }
    }
    
    private void verifyPIN(APDU apdu) {
        byte[] buffer = apdu.getBuffer();
        byte numBytes = (byte)apdu.setIncomingAndReceive();
        
        if (userPIN.check(buffer, ISO7816.OFFSET_CDATA, numBytes)) {
            // PIN correct
            return;
        } else {
            // PIN incorrect
            ISOException.throwIt((short)(0x63C0 | userPIN.getTriesRemaining()));
        }
    }
    
    private void generalAuthenticate(APDU apdu) {
        // Implement RSA signature/decryption for PIV Authentication
        // This is called when reader authenticates user
        
        if (!userPIN.isValidated()) {
            ISOException.throwIt(ISO7816.SW_SECURITY_STATUS_NOT_SATISFIED);
        }
        
        byte[] buffer = apdu.getBuffer();
        // ... (RSA signature generation using privKeyAuth)
    }
    
    private void getData(APDU apdu) {
        // Return certificates, biometric data, CHUID, etc.
        byte[] buffer = apdu.getBuffer();
        short tag = Util.getShort(buffer, ISO7816.OFFSET_P1);
        
        switch (tag) {
            case (short)0x5FC1:  // PIV Authentication Certificate
                Util.arrayCopyNonAtomic(certAuth, (short)0, buffer, (short)0, (short)certAuth.length);
                apdu.setOutgoingAndSend((short)0, (short)certAuth.length);
                break;
            // ... (other data objects)
        }
    }
    
    private void putData(APDU apdu) {
        // Write certificates, biometric data (during personalization)
        // Only allowed during card initialization
    }
}
```

### OS-PACS Integration (Leosac Configuration)

```yaml
# /etc/leosac/leosac.conf
# Leosac configuration for PIV card support

kernel:
  plugin_directories:
    - /usr/lib/leosac/plugins
  
  modules:
    - name: NETWORK
      file: libnetwork.so
      level: 42
      config:
        port: 4242
        interfaces:
          - eth0
    
    - name: RPLETH
      file: librpleth.so
      level: 50
      config:
        port: /dev/ttyUSB0
        baudrate: 115200
        readers:
          - name: MAIN_ENTRANCE
            address: 01
            type: HID_Omnikey_5427
    
    - name: PIV_AUTH
      file: libpiv.so
      level: 60
      config:
        # Provincial PIV CA certificate
        ca_certificate: /etc/leosac/certs/provincial_ca.pem
        
        # OCSP responder for real-time validation
        ocsp_responder: https://ocsp.provincial-piv.on.ca
        ocsp_timeout: 5000  # 5 seconds
        
        # CRL for offline validation
        crl_url: https://crl.provincial-piv.on.ca/provincial.crl
        crl_refresh: 3600  # 1 hour
        
        # Cache validated certificates (performance)
        cache_size: 10000
        cache_ttl: 86400  # 24 hours
        
        # Offline grace period (if OCSP unreachable)
        offline_grace_period: 86400  # 24 hours
        
        # Certificate validation options
        check_revocation: true
        require_ocsp: true  # Fail if OCSP unreachable
        allow_crl_fallback: true
    
    - name: AUTH_DATABASE
      file: libauth-db.so
      level: 70
      config:
        database: /var/lib/leosac/auth.db
        
        # Map PIV certificates to users
        users:
          - certificate_serial: "1A2B3C4D5E6F7890"
            user_id: john_doe
            name: "John Doe"
            role: security_guard
            organization: "ABC Security Inc"
            groups:
              - security_guards
              - building_a_access
          
          - certificate_serial: "9F8E7D6C5B4A3210"
            user_id: jane_smith
            name: "Jane Smith"
            role: security_supervisor
            organization: "ABC Security Inc"
            groups:
              - security_supervisors
              - all_buildings_access
    
    - name: AUTH_FILE
      file: libauth-file.so
      level: 80
      config:
        auth_file: /etc/leosac/access_policies.xml
        
        # Access policies (RBAC)
        policies:
          - name: security_guard_standard
            groups:
              - security_guards
            doors:
              - MAIN_ENTRANCE
              - PATROL_ROUTE_DOORS
              - BREAK_ROOM
            schedules:
              - weekdays: 06:00-22:00
              - weekends: 08:00-20:00
          
          - name: security_supervisor
            groups:
              - security_supervisors
            doors:
              - ALL  # All doors
            schedules:
              - always  # No time restrictions
            require_pin: true  # Two-factor

# Authentication flow:
# 1. User taps PIV card to reader
# 2. Reader extracts PIV Authentication Certificate
# 3. Leosac validates certificate:
#    a. Check signature (Provincial CA)
#    b. Query OCSP (is cert revoked?)
#    c. Check expiration date
# 4. Leosac maps cert serial to user account
# 5. Leosac evaluates access policy (role, door, time)
# 6. Grant or deny access
# 7. Log event (certificate serial, door, timestamp, result)
```

---

**END OF PROVINCIAL PIV INFRASTRUCTURE INTEGRATION DOCUMENT**

This comprehensive document provides complete PIV infrastructure specifications, hardware requirements, integration details for all 7 provincial security pillars, deployment roadmap, cost analysis, and technical implementations.
