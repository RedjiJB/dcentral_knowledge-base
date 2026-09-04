---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: 11c2e85c-b7f8-4c7a-98e3-c15ab996f217
original_filename: Provincial_Security_Guard_Universal_Credential_System.md
created_at: 2026-03-04T20:38:02.898157+00:00
content_hash: 87c24300f835topic: federation-guard-pin
---

# Provincial Security Guard Universal Credential System
## Open Standards-Based Professional Identity & Access Management

**Project Name**: SecureGuard Provincial Identity System (SGPIS)  
**Version**: 1.0  
**Date**: December 2025  
**Classification**: Public Sector Identity Infrastructure  
**Scope**: Province-wide security guard certification and credentialing

---

## Executive Summary

### Vision Statement

Create a **universal, interoperable identity credential system** for all certified security guards in the province, enabling seamless physical and logical access across thousands of sites while maintaining professional standards, improving public safety, and eliminating credential fraud.

### The Problem Being Solved

**Current State Issues:**

1. **Fragmented Credentials** - Each security company issues their own badges
2. **No Standardization** - Inconsistent verification of guard certification
3. **Credential Fraud** - Easy to fake paper licenses or cheap photo IDs
4. **Access Management Chaos** - Guards working multiple sites need multiple credentials
5. **No Interoperability** - Guards can't seamlessly transition between companies
6. **Limited Accountability** - Difficult to track guard access history
7. **Inefficient Onboarding** - Days/weeks to provision credentials for each new site

**Impact:**
- Public safety risk from uncertified or fraudulent guards
- Operational inefficiency for security companies
- Poor professional image for the industry
- Regulatory compliance challenges

### The Solution: Universal PIV Credential

**One Card. One Standard. Province-Wide.**

```
┌─────────────────────────────────────────────────────────────────┐
│         Provincial Ministry of Public Safety                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │    Security Guard Registry & Credentialing Authority      │   │
│  │  • Issues FIPS 201 PIV cards to all certified guards     │   │
│  │  • Maintains PKI infrastructure                          │   │
│  │  • Operates provincial trust anchor                      │   │
│  │  • Enforces certification standards                      │   │
│  └────────────────┬─────────────────────────────────────────┘   │
└───────────────────┼─────────────────────────────────────────────┘
                    │
                    │ Federation API (OpenID Connect)
                    │ Certificate Trust Chain
                    │
     ┌──────────────┼──────────────┬──────────────────┐
     │              │              │                  │
     ▼              ▼              ▼                  ▼
┌─────────┐  ┌─────────┐  ┌─────────┐        ┌─────────┐
│Security │  │Security │  │In-House │  ....  │Client   │
│Company A│  │Company B│  │Security │        │Site     │
│         │  │         │  │(Corp)   │        │Access   │
└────┬────┘  └────┬────┘  └────┬────┘        └────┬────┘
     │            │            │                  │
     │ Grant/Revoke Site Access                   │
     │ Assign Roles & Permissions                 │
     │                                            │
     └────────────────────────────────────────────┘
              Access Control Decisions
              (Federated, Real-time)
```

**Key Benefits:**

| Stakeholder | Benefit |
|-------------|---------|
| **Ministry** | Reduced fraud, improved compliance, real-time oversight |
| **Security Companies** | Lower costs, faster onboarding, better ops |
| **Guards** | Professional credential, seamless multi-site work |
| **Client Sites** | Verified guards, granular access control, audit trails |
| **Public** | Enhanced safety, accountability, professionalization |

**Cost Savings:**
- **Ministry**: 70% reduction in credential fraud investigations
- **Security Companies**: 80% faster onboarding (days → hours)
- **Guards**: No need for multiple company-specific badges
- **Province-wide ROI**: $15M annually (10,000 active guards)

---

## System Architecture

### Three-Tier Federation Model

#### Tier 1: Provincial Trust Anchor (Ministry)

**Role**: Root of trust, credential issuance authority

```
┌───────────────────────────────────────────────────────────────┐
│  Ministry of Public Safety - Provincial Trust Anchor         │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Root PKI (Dogtag Certificate Authority)              │  │
│  │  • Root CA (offline, HSM-protected)                   │  │
│  │  • Issuing CA (issues guard credentials)              │  │
│  │  • OCSP Responder (revocation checking)               │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Security Guard Registry (PostgreSQL)                 │  │
│  │  • Guard certifications & qualifications              │  │
│  │  • Training records                                   │  │
│  │  • Disciplinary actions                               │  │
│  │  • Employment history                                 │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Credential Issuance System (OpenPIV)                 │  │
│  │  • PIV card personalization                           │  │
│  │  • Biometric enrollment (fingerprint + photo)         │  │
│  │  • Background check integration                       │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Federation Gateway (OAuth 2.0 + OpenID Connect)      │  │
│  │  • Company registration API                           │  │
│  │  • Guard status verification API                      │  │
│  │  • Real-time revocation broadcasts                    │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

**Ministry APIs (Open Standards):**

```yaml
# OpenAPI 3.0 Specification
openapi: 3.0.0
info:
  title: Provincial Security Guard Credential API
  version: 1.0.0
  description: |
    Federation API for security companies to verify guard credentials
    and manage site access permissions.

servers:
  - url: https://api.securityguard.gov.on.ca/v1
    description: Production API

paths:
  /guards/{guard_id}/verify:
    get:
      summary: Verify guard certification status
      parameters:
        - name: guard_id
          in: path
          required: true
          schema:
            type: string
          description: Guard's provincial license number
      responses:
        '200':
          description: Guard verification result
          content:
            application/json:
              schema:
                type: object
                properties:
                  guard_id:
                    type: string
                    example: "SG-ON-123456"
                  full_name:
                    type: string
                    example: "John Smith"
                  certification_level:
                    type: string
                    enum: [basic, advanced, supervisor, trainer]
                  status:
                    type: string
                    enum: [active, suspended, revoked, expired]
                  issue_date:
                    type: string
                    format: date
                  expiration_date:
                    type: string
                    format: date
                  qualifications:
                    type: array
                    items:
                      type: string
                    example: ["First Aid", "WHMIS", "Use of Force"]
                  certificate_serial:
                    type: string
                    description: PIV certificate serial number
                  photo_url:
                    type: string
                    format: uri
                    description: Secure URL to guard's photo (time-limited)

  /guards/{guard_id}/employment:
    post:
      summary: Register guard employment with company
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                company_id:
                  type: string
                position:
                  type: string
                start_date:
                  type: string
                  format: date
                sites:
                  type: array
                  items:
                    type: string
                  description: Initial site access requests
      responses:
        '201':
          description: Employment registered

  /guards/{guard_id}/revoke:
    post:
      summary: Revoke guard certification (Ministry only)
      security:
        - ministry_auth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                reason:
                  type: string
                  enum: [misconduct, criminal_charge, failed_renewal, other]
                effective_date:
                  type: string
                  format: date-time
                notes:
                  type: string
      responses:
        '200':
          description: Credential revoked, all companies notified

  /certificates/validate:
    post:
      summary: Validate PIV certificate (for site access systems)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                certificate_pem:
                  type: string
                  description: X.509 certificate in PEM format
      responses:
        '200':
          description: Certificate validation result
          content:
            application/json:
              schema:
                type: object
                properties:
                  valid:
                    type: boolean
                  status:
                    type: string
                    enum: [good, revoked, expired]
                  guard_id:
                    type: string
                  certification_status:
                    type: string
```

#### Tier 2: Security Companies & In-House Security

**Role**: Employers who grant/revoke site access

```
┌───────────────────────────────────────────────────────────────┐
│  Security Company Portal (Web Application)                   │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Guard Management                                      │  │
│  │  • View all guards with valid provincial credentials  │  │
│  │  • Hire/terminate guards (reflected in ministry)      │  │
│  │  • Assign guards to client sites                      │  │
│  │  • Define role-based permissions per site             │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Site Access Control                                   │  │
│  │  • Grant temporary/permanent access                    │  │
│  │  • Set access schedules (shifts, days off)            │  │
│  │  • Emergency revocation (instant)                      │  │
│  │  • Audit logs (who accessed what, when)               │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Integration with OS-PACS                              │  │
│  │  • Push access policies to door controllers           │  │
│  │  • Real-time access event notifications               │  │
│  │  • Compliance reporting                                │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

**Company Database Schema:**

```sql
-- Company's local database (federated with ministry)

CREATE TABLE guards (
    id SERIAL PRIMARY KEY,
    provincial_guard_id VARCHAR(20) UNIQUE NOT NULL, -- e.g., SG-ON-123456
    certificate_serial BIGINT UNIQUE NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    hire_date DATE NOT NULL,
    termination_date DATE,
    employment_status VARCHAR(20) DEFAULT 'active',
    position VARCHAR(50), -- e.g., security guard, supervisor, site manager
    
    -- Cached from ministry (synced hourly)
    certification_level VARCHAR(20),
    certification_expiration DATE,
    qualifications JSONB,
    
    last_sync TIMESTAMP DEFAULT NOW(),
    
    FOREIGN KEY (provincial_guard_id) REFERENCES ministry.guards(guard_id)
);

CREATE TABLE sites (
    id SERIAL PRIMARY KEY,
    site_name VARCHAR(200) NOT NULL,
    client_name VARCHAR(200) NOT NULL,
    address TEXT,
    site_code VARCHAR(50) UNIQUE,
    security_level VARCHAR(20), -- low, medium, high, critical
    
    -- OS-PACS integration
    ospacs_site_id INTEGER
);

CREATE TABLE guard_site_access (
    id SERIAL PRIMARY KEY,
    guard_id INTEGER REFERENCES guards(id),
    site_id INTEGER REFERENCES sites(id),
    
    -- Access control
    access_level VARCHAR(20), -- visitor, guard, supervisor, manager
    access_start_date DATE NOT NULL,
    access_end_date DATE,
    
    -- Schedules
    schedule JSONB, -- {"monday": {"start": "08:00", "end": "16:00"}, ...}
    
    -- Permissions (logical access)
    permissions JSONB, -- {"can_access_computer": true, "can_view_cameras": true, ...}
    
    -- Metadata
    granted_by INTEGER REFERENCES users(id),
    granted_at TIMESTAMP DEFAULT NOW(),
    revoked_by INTEGER,
    revoked_at TIMESTAMP,
    revocation_reason TEXT,
    
    status VARCHAR(20) DEFAULT 'active',
    
    UNIQUE(guard_id, site_id)
);

-- Sync table for ministry federation
CREATE TABLE ministry_sync_log (
    id SERIAL PRIMARY KEY,
    sync_type VARCHAR(50), -- guard_status, certification_update, revocation
    guard_id VARCHAR(20),
    sync_timestamp TIMESTAMP DEFAULT NOW(),
    sync_status VARCHAR(20), -- success, failed
    details JSONB
);
```

#### Tier 3: Client Sites (Physical & Logical Access)

**Role**: Enforce access decisions at doors and systems

```
┌───────────────────────────────────────────────────────────────┐
│  Client Site Access Control (OS-PACS + IT Systems)           │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Physical Access (OS-PACS)                             │  │
│  │  • Leosac controllers at doors                         │  │
│  │  • Smart card readers (PIV-compatible)                 │  │
│  │  • Real-time policy sync from security company        │  │
│  │  • Certificate validation against ministry PKI        │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Logical Access (Computers, VMS, etc.)                 │  │
│  │  • Video management system (guard login with PIV)     │  │
│  │  • Computer workstations (smart card login)           │  │
│  │  • Access control admin panel (role-based)            │  │
│  │  • Time & attendance system                            │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                               │
└───────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Complete Lifecycle

### 1. Guard Certification & Credential Issuance

```
┌────────────────────────────────────────────────────────────────┐
│  STEP 1: Initial Certification                                │
└────────────────────────────────────────────────────────────────┘

Security Guard Training → Ministry Exam → Background Check
    ↓                          ↓                ↓
  Pass                       Pass            Clear
    ↓                          ↓                ↓
    └──────────────────────────┴────────────────┘
                               ↓
                    ┌──────────────────────┐
                    │  Certification       │
                    │  Granted             │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │  Schedule            │
                    │  Credential          │
                    │  Issuance            │
                    └──────────┬───────────┘
                               ↓

┌────────────────────────────────────────────────────────────────┐
│  STEP 2: PIV Card Issuance (Ministry Office)                  │
└────────────────────────────────────────────────────────────────┘

Guard visits ministry enrollment center
    ↓
Identity Verification (government-issued ID)
    ↓
Biometric Capture (fingerprints + photo)
    ↓
PIV Card Personalization:
    1. Insert blank Java Card
    2. Load OpenFIPS201 applet
    3. Generate 4 key pairs on card
    4. Create CSRs for each key
    5. Dogtag CA signs certificates:
       • PIV Authentication (9A) - Computer/VPN login
       • Card Authentication (9E) - Door access
       • Digital Signature (9C) - Incident reports
       • Key Management (9D) - Encrypted communications
    6. Import certificates to card
    7. Set PIN (6-8 digits, guard-selected)
    8. Print card:
       • Guard photo
       • Name
       • Provincial Guard ID (e.g., SG-ON-123456)
       • Expiration date
       • Ministry seal/logo
    ↓
Guard receives card + PIN
    ↓
Card registered in provincial database
```

**Card Appearance:**

```
┌─────────────────────────────────────────────────────┐
│  ONTARIO MINISTRY OF PUBLIC SAFETY                  │
│  Security Guard Credential                          │
│                                                      │
│  ┌─────────────┐                                    │
│  │             │  Name: SMITH, JOHN                 │
│  │   PHOTO     │  Guard ID: SG-ON-123456            │
│  │             │  Level: ADVANCED GUARD             │
│  │             │  Issued: 2025-01-15                │
│  └─────────────┘  Expires: 2027-01-15               │
│                                                      │
│  ════════════════════════════════════════════════   │
│  Valid for physical and logical access              │
│  Province of Ontario seal ⚜                         │
└─────────────────────────────────────────────────────┘
```

### 2. Guard Employment & Site Assignment

```
┌────────────────────────────────────────────────────────────────┐
│  STEP 3: Guard Hired by Security Company                      │
└────────────────────────────────────────────────────────────────┘

Guard applies for job at Security Company A
    ↓
Company verifies provincial credential:
    • Scans guard's PIV card
    • Calls ministry API: GET /guards/{guard_id}/verify
    • Confirms certification is active & valid
    ↓
Company hires guard
    ↓
Company registers employment via API:
    POST /guards/SG-ON-123456/employment
    {
        "company_id": "SEC-CORP-001",
        "position": "security_guard",
        "start_date": "2025-02-01"
    }
    ↓
Ministry records employment (audit trail)

┌────────────────────────────────────────────────────────────────┐
│  STEP 4: Assign Guard to Client Site                          │
└────────────────────────────────────────────────────────────────┘

Company Portal → Site Access Management
    ↓
Select Guard: JOHN SMITH (SG-ON-123456)
Select Site: Acme Corporation HQ
Set Parameters:
    • Access Level: Security Guard
    • Schedule: Monday-Friday, 08:00-16:00
    • Start Date: 2025-02-05
    • End Date: (leave blank for permanent)
    • Permissions:
        ☑ Physical access (main entrance, loading dock)
        ☑ Computer login (guard station only)
        ☑ View security cameras
        ☐ Access server room
        ☐ Admin rights
    ↓
Company submits access request
    ↓
System validates:
    • Guard has active provincial certification ✓
    • Guard is currently employed by company ✓
    • Site exists in system ✓
    ↓
Access Policy Created:

{
    "guard_id": "SG-ON-123456",
    "certificate_serial": "0x1A2B3C4D",
    "site_id": "ACME-HQ-001",
    "access_level": "guard",
    "schedule": {
        "monday": {"start": "08:00", "end": "16:00"},
        "tuesday": {"start": "08:00", "end": "16:00"},
        "wednesday": {"start": "08:00", "end": "16:00"},
        "thursday": {"start": "08:00", "end": "16:00"},
        "friday": {"start": "08:00", "end": "16:00"}
    },
    "doors": [1, 2, 5, 12],  // Door IDs: main entrance, etc.
    "logical_access": {
        "workstation_login": true,
        "vms_access": true,
        "admin_panel": false
    },
    "effective_immediately": true
}
    ↓
Policy pushed to:
    1. OS-PACS controllers at site (within 60 seconds)
    2. Site's Active Directory (for computer login)
    3. Video Management System
    4. Audit log
    ↓
Guard notified: "Access granted to Acme Corporation HQ"
```

### 3. Daily Access Operations

**Physical Access at Door:**

```
┌────────────────────────────────────────────────────────────────┐
│  STEP 5: Guard Arrives at Site                                │
└────────────────────────────────────────────────────────────────┘

Guard taps PIV card on reader (NFC)
    ↓
Reader extracts Card Auth certificate (9E)
    ↓
Leosac Controller validates:

    1. Certificate Cryptographic Validation
       ├─► Verify signature chain (signed by ministry CA)
       ├─► Check expiration date
       └─► Query OCSP (ministry server)
           └─► Status: GOOD ✓
    
    2. Guard Certification Status
       ├─► Extract Guard ID from certificate
       ├─► Query company database (local cache)
       └─► Status: ACTIVE ✓
    
    3. Site Access Authorization
       ├─► Check guard_site_access table
       ├─► Guard has access to this door ✓
       ├─► Current time within schedule ✓
       └─► No temporary suspension ✓
    
    All checks pass (150ms total)
    ↓
Door unlocks, LED green, beep
    ↓
Access log created:
    • Timestamp: 2025-02-05 08:03:42
    • Guard: JOHN SMITH (SG-ON-123456)
    • Door: Main Entrance (Door ID 1)
    • Site: Acme Corporation HQ
    • Decision: GRANTED
    • Certificate Serial: 0x1A2B3C4D
    • Response Time: 152ms
```

**Logical Access (Computer Login):**

```
Guard arrives at guard station computer
    ↓
Inserts PIV card into reader
    ↓
Windows prompts for PIN
    ↓
Guard enters PIN
    ↓
OpenSC validates PIN on card
    ↓
Windows authenticates using PIV Auth certificate (9A)
    ↓
Active Directory maps certificate to guard's account
    ↓
Login successful
    ↓
Profile loaded with guard-level permissions:
    • Can access VMS software
    • Can log incidents
    • Cannot access HR systems
    • Cannot modify site config
```

### 4. Multi-Site Scenario (Guard Works for Multiple Companies)

```
┌────────────────────────────────────────────────────────────────┐
│  Real-World Example: Guard works 3 jobs                       │
└────────────────────────────────────────────────────────────────┘

Guard: JANE DOE (SG-ON-789012)

Monday-Wednesday: Security Company A → Client Site 1 (Office Building)
Thursday-Friday: Security Company B → Client Site 2 (Warehouse)
Weekends: In-House Security → Client Site 3 (Hospital)

┌──────────────────────────────────────────────────────────────┐
│  ONE CARD - ALL ACCESS                                       │
└──────────────────────────────────────────────────────────────┘

Company A Portal:
    Guard: JANE DOE
    Site: Office Building
    Schedule: Mon-Wed, 07:00-15:00
    Access: Main doors, employee lounge
    Status: ACTIVE

Company B Portal:
    Guard: JANE DOE
    Site: Warehouse
    Schedule: Thu-Fri, 16:00-00:00
    Access: Warehouse floor, loading dock
    Status: ACTIVE

Hospital HR Portal:
    Guard: JANE DOE
    Site: Hospital Campus
    Schedule: Sat-Sun, 08:00-20:00
    Access: ER entrance, parking garage, cafeteria
    Status: ACTIVE

┌──────────────────────────────────────────────────────────────┐
│  Card Behavior                                               │
└──────────────────────────────────────────────────────────────┘

Monday 08:00 at Office Building → GRANTED (Company A schedule)
Monday 08:00 at Warehouse → DENIED (outside Company B schedule)
Thursday 17:00 at Warehouse → GRANTED (Company B schedule)
Thursday 17:00 at Office Building → DENIED (outside Company A schedule)
Saturday 10:00 at Hospital → GRANTED (Hospital schedule)

All from ONE provincial credential!
```

### 5. Revocation Scenarios

**Scenario A: Guard Terminated from Company**

```
Security Company A terminates guard JOHN SMITH
    ↓
Company Portal → Revoke Access
    ↓
Select: JOHN SMITH
Reason: Termination
Effective: Immediately
    ↓
System actions:
    1. Update guard_site_access.status = 'revoked'
    2. Push policy update to all site controllers (<60 sec)
    3. Notify ministry of employment termination
    4. Generate termination report
    ↓
Guard's card still works for:
    • Other employers (if any)
    • Provincial services
    
Guard's card STOPS working for:
    • All Company A sites (immediate)
```

**Scenario B: Ministry Revokes Certification**

```
Ministry discovers guard misconduct
    ↓
Investigation completed → Certification revoked
    ↓
Ministry Portal → Revoke Certification
    Guard: SG-ON-123456
    Reason: Misconduct
    Effective: Immediately
    ↓
Automated actions:
    1. Revoke all PIV certificates via OCSP
    2. Broadcast revocation to all federated companies
    3. API webhook to all registered companies:
       
       POST https://company-a.com/api/ministry/revocation
       {
           "guard_id": "SG-ON-123456",
           "reason": "certification_revoked",
           "effective_date": "2025-03-15T14:30:00Z"
       }
    
    4. Companies auto-revoke ALL site access
    5. Door controllers update cache (next OCSP check)
    ↓
Within 5 minutes:
    • Card rejected at ALL sites province-wide
    • Computer login disabled
    • All access logs flagged
    ↓
Guard notified:
    "Your provincial security guard certification has been revoked.
     Your credential is no longer valid. Contact ministry for details."
```

---

## Technical Implementation

### Ministry PKI Infrastructure

**Certificate Hierarchy:**

```
┌─────────────────────────────────────────────────────────┐
│  Ontario Security Guard Root CA                         │
│  Validity: 20 years                                     │
│  Storage: HSM (Hardware Security Module)                │
│  Location: Ministry data center (offline)               │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  Ontario Security Guard Issuing CA                      │
│  Validity: 5 years                                      │
│  Storage: Online HSM                                    │
│  Purpose: Issues guard PIV certificates                 │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ├──────────────────────┬──────────────┬──────────────┐
                   ▼                      ▼              ▼              ▼
        ┌──────────────────┐  ┌──────────────┐  ┌──────────┐  ┌──────────┐
        │ PIV Auth Cert    │  │ Card Auth    │  │ Digital  │  │ Key Mgmt │
        │ (Guard Login)    │  │ (Door Access)│  │ Signature│  │ (Encrypt)│
        │ Validity: 3 yrs  │  │ Validity: 3  │  │ 3 years  │  │ 3 years  │
        └──────────────────┘  └──────────────┘  └──────────┘  └──────────┘
```

**Certificate Profile (Card Auth - Physical Access):**

```
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 1234567890 (0x499602d2)
        Signature Algorithm: ecdsa-with-SHA256
        Issuer: C=CA, ST=Ontario, O=Ministry of Public Safety, OU=Security Guard Division, CN=Ontario SG Issuing CA
        Validity
            Not Before: Feb  1 00:00:00 2025 GMT
            Not After : Feb  1 23:59:59 2028 GMT
        Subject: C=CA, ST=Ontario, O=Ministry of Public Safety, OU=Security Guards, CN=SG-ON-123456 SMITH JOHN Card Auth
        Subject Public Key Info:
            Public Key Algorithm: id-ecPublicKey
                Public-Key: (256 bit)
                Curve: P-256
        X509v3 extensions:
            X509v3 Key Usage: critical
                Digital Signature
            X509v3 Extended Key Usage:
                1.3.6.1.4.1.311.20.2.2 (Smart Card Logon)
                1.3.6.1.5.5.7.3.2 (TLS Client Auth)
            X509v3 Subject Alternative Name:
                UUID: 12345678-90ab-cdef-1234-567890abcdef
                otherName: FASC-N (Federal Agency Smart Credential Number)
            X509v3 Authority Information Access:
                OCSP - URI:http://ocsp.securityguard.gov.on.ca
                CA Issuers - URI:http://pki.securityguard.gov.on.ca/issuing-ca.crt
            X509v3 CRL Distribution Points:
                Full Name:
                  URI:http://pki.securityguard.gov.on.ca/crl.pem
    Signature Algorithm: ecdsa-with-SHA256
```

### Federation Protocol

**OpenID Connect + OAuth 2.0 for Company Integration:**

```yaml
# OIDC Discovery Document
# https://api.securityguard.gov.on.ca/.well-known/openid-configuration

{
  "issuer": "https://api.securityguard.gov.on.ca",
  "authorization_endpoint": "https://api.securityguard.gov.on.ca/oauth/authorize",
  "token_endpoint": "https://api.securityguard.gov.on.ca/oauth/token",
  "userinfo_endpoint": "https://api.securityguard.gov.on.ca/oauth/userinfo",
  "jwks_uri": "https://api.securityguard.gov.on.ca/oauth/jwks",
  "scopes_supported": [
    "openid",
    "profile",
    "guard.verify",
    "guard.employment",
    "guard.access"
  ],
  "response_types_supported": [
    "code",
    "token",
    "id_token"
  ],
  "grant_types_supported": [
    "authorization_code",
    "client_credentials"
  ],
  "token_endpoint_auth_methods_supported": [
    "client_secret_post",
    "private_key_jwt"
  ]
}
```

**Company Registration Process:**

```bash
# Step 1: Company registers with ministry
POST https://api.securityguard.gov.on.ca/v1/companies/register

{
  "company_name": "Acme Security Services Inc.",
  "business_number": "123456789RC0001",
  "license_number": "SEC-LIC-5678",
  "contact_email": "admin@acmesecurity.com",
  "api_callback_url": "https://api.acmesecurity.com/ministry/webhook"
}

# Response:
{
  "company_id": "SEC-CORP-001",
  "client_id": "acme_security_prod_client",
  "client_secret": "sk_live_abc123...",
  "api_key": "pk_live_xyz789...",
  "status": "approved"
}

# Step 2: Company tests API access
GET https://api.securityguard.gov.on.ca/v1/guards/SG-ON-123456/verify
Authorization: Bearer {access_token}

# Step 3: Company integrates webhook for real-time updates
# Ministry calls company webhook on events:
POST https://api.acmesecurity.com/ministry/webhook

{
  "event_type": "guard.certification.revoked",
  "guard_id": "SG-ON-123456",
  "timestamp": "2025-03-15T14:30:00Z",
  "reason": "misconduct",
  "action_required": "revoke_all_access"
}
```

### OS-PACS Integration

**Enhanced Leosac Configuration for Provincial System:**

```xml
<!-- /etc/leosac/kernel.xml -->
<kernel>
    <plugin_directories>
        <plugindir>/usr/lib/leosac</plugindir>
    </plugin_directories>
    
    <modules>
        <!-- Provincial PIV Authentication Module -->
        <module>
            <n>ProvincialPIVAuth</n>
            <file>libprovincial_piv.so</file>
            <config>
                <!-- Ministry PKI -->
                <root_ca>/etc/leosac/ontario-sg-root-ca.crt</root_ca>
                <issuing_ca>/etc/leosac/ontario-sg-issuing-ca.crt</issuing_ca>
                
                <!-- OCSP Configuration -->
                <ocsp_url>http://ocsp.securityguard.gov.on.ca</ocsp_url>
                <ocsp_timeout>2000</ocsp_timeout>
                <ocsp_cache_ttl>3600</ocsp_cache_ttl>
                
                <!-- Company Database -->
                <database_url>postgresql://leosac:pass@localhost/company_db</database_url>
                
                <!-- Ministry API (for real-time verification) -->
                <ministry_api_url>https://api.securityguard.gov.on.ca/v1</ministry_api_url>
                <api_key>${MINISTRY_API_KEY}</api_key>
                
                <!-- Policy Sync -->
                <policy_sync_interval>300</policy_sync_interval> <!-- 5 minutes -->
                
                <!-- Failover Strategy -->
                <offline_mode>fail_open_with_cache</offline_mode>
                <cache_expiry_grace_period>86400</cache_expiry_grace_period> <!-- 24 hours -->
            </config>
        </module>
        
        <!-- Database Module -->
        <module>
            <n>Database</n>
            <file>libdatabase.so</file>
            <config>
                <db_type>postgresql</db_type>
                <host>localhost</host>
                <port>5432</port>
                <db_name>company_db</db_name>
                <username>leosac</username>
                <password>${DB_PASSWORD}</password>
            </config>
        </module>
        
        <!-- OSDP Reader Module -->
        <module>
            <n>OSDP</n>
            <file>libosdp.so</file>
            <config>
                <port>/dev/ttyUSB0</port>
                <baud_rate>9600</baud_rate>
                <readers>
                    <reader>
                        <id>main_entrance</id>
                        <address>0</address>
                        <secure_channel>true</secure_channel>
                        <mode>piv_certificate</mode>
                    </reader>
                </readers>
            </config>
        </module>
    </modules>
</kernel>
```

**Access Decision Algorithm:**

```python
# Provincial PIV Access Decision Engine

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import requests
import psycopg2
from cryptography import x509
from cryptography.hazmat.backends import default_backend

@dataclass
class AccessDecision:
    granted: bool
    reason: str
    guard_id: Optional[str]
    guard_name: Optional[str]
    certification_level: Optional[str]
    response_time_ms: int

class ProvincialAccessController:
    def __init__(self, config):
        self.config = config
        self.db = psycopg2.connect(config['database_url'])
        self.ministry_api = config['ministry_api_url']
        self.api_key = config['api_key']
    
    def process_access_request(self, certificate_pem: str, door_id: int) -> AccessDecision:
        """
        Complete access decision workflow for provincial security guard system
        """
        start_time = datetime.now()
        
        # Step 1: Parse certificate
        cert = x509.load_pem_x509_certificate(
            certificate_pem.encode(),
            default_backend()
        )
        
        # Step 2: Validate certificate cryptography
        if not self.validate_certificate_chain(cert):
            return AccessDecision(
                granted=False,
                reason="Invalid certificate chain",
                guard_id=None,
                guard_name=None,
                certification_level=None,
                response_time_ms=self.elapsed_ms(start_time)
            )
        
        # Step 3: Check certificate expiration
        if datetime.utcnow() > cert.not_valid_after:
            return AccessDecision(
                granted=False,
                reason="Certificate expired",
                guard_id=None,
                guard_name=None,
                certification_level=None,
                response_time_ms=self.elapsed_ms(start_time)
            )
        
        # Step 4: Extract Guard ID from certificate
        guard_id = self.extract_guard_id(cert)
        if not guard_id:
            return AccessDecision(
                granted=False,
                reason="Invalid certificate format - no Guard ID",
                guard_id=None,
                guard_name=None,
                certification_level=None,
                response_time_ms=self.elapsed_ms(start_time)
            )
        
        # Step 5: Check OCSP (revocation status)
        if not self.check_ocsp(cert):
            return AccessDecision(
                granted=False,
                reason="Certificate revoked",
                guard_id=guard_id,
                guard_name=None,
                certification_level=None,
                response_time_ms=self.elapsed_ms(start_time)
            )
        
        # Step 6: Verify guard certification status (local cache first)
        guard_info = self.get_guard_info(guard_id)
        if not guard_info:
            # Not in cache, query ministry API
            guard_info = self.query_ministry_api(guard_id)
            if guard_info:
                self.cache_guard_info(guard_info)
        
        if not guard_info or guard_info['status'] != 'active':
            return AccessDecision(
                granted=False,
                reason=f"Guard certification status: {guard_info.get('status', 'unknown')}",
                guard_id=guard_id,
                guard_name=guard_info.get('full_name') if guard_info else None,
                certification_level=guard_info.get('certification_level') if guard_info else None,
                response_time_ms=self.elapsed_ms(start_time)
            )
        
        # Step 7: Check site access authorization
        access_auth = self.check_site_authorization(guard_id, door_id)
        if not access_auth['authorized']:
            return AccessDecision(
                granted=False,
                reason=access_auth['reason'],
                guard_id=guard_id,
                guard_name=guard_info['full_name'],
                certification_level=guard_info['certification_level'],
                response_time_ms=self.elapsed_ms(start_time)
            )
        
        # Step 8: Check schedule (time-based access)
        if not self.check_schedule(guard_id, door_id):
            return AccessDecision(
                granted=False,
                reason="Outside authorized schedule",
                guard_id=guard_id,
                guard_name=guard_info['full_name'],
                certification_level=guard_info['certification_level'],
                response_time_ms=self.elapsed_ms(start_time)
            )
        
        # All checks passed - GRANT ACCESS
        return AccessDecision(
            granted=True,
            reason="Access authorized",
            guard_id=guard_id,
            guard_name=guard_info['full_name'],
            certification_level=guard_info['certification_level'],
            response_time_ms=self.elapsed_ms(start_time)
        )
    
    def validate_certificate_chain(self, cert):
        """Verify certificate is signed by ministry CA"""
        # Implementation using OpenSSL
        # Verify against root_ca and issuing_ca
        return True  # Simplified
    
    def check_ocsp(self, cert):
        """Query ministry OCSP responder"""
        serial = cert.serial_number
        
        # Check local cache first
        cached = self.get_ocsp_cache(serial)
        if cached and cached['valid_until'] > datetime.now():
            return cached['status'] == 'good'
        
        # Query OCSP server
        try:
            response = requests.get(
                f"{self.config['ocsp_url']}?serial={serial}",
                timeout=2
            )
            status = response.json()['status']
            
            # Update cache
            self.update_ocsp_cache(serial, status, ttl=3600)
            
            return status == 'good'
        except:
            # OCSP unreachable - use cached value or fail open
            return cached['status'] == 'good' if cached else True
    
    def extract_guard_id(self, cert):
        """Extract provincial guard ID from certificate subject"""
        # Parse CN field: "SG-ON-123456 SMITH JOHN Card Auth"
        cn = cert.subject.get_attributes_for_oid(
            x509.oid.NameOID.COMMON_NAME
        )[0].value
        
        parts = cn.split()
        if parts and parts[0].startswith('SG-ON-'):
            return parts[0]
        return None
    
    def get_guard_info(self, guard_id):
        """Get guard info from local database cache"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT provincial_guard_id, full_name, certification_level,
                   certification_expiration, employment_status
            FROM guards
            WHERE provincial_guard_id = %s
              AND last_sync > NOW() - INTERVAL '1 hour'
        """, (guard_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        return {
            'guard_id': row[0],
            'full_name': row[1],
            'certification_level': row[2],
            'expiration': row[3],
            'status': 'active' if row[4] == 'active' else 'inactive'
        }
    
    def query_ministry_api(self, guard_id):
        """Query ministry API for guard status (fallback)"""
        try:
            response = requests.get(
                f"{self.ministry_api}/guards/{guard_id}/verify",
                headers={'Authorization': f'Bearer {self.api_key}'},
                timeout=2
            )
            return response.json()
        except:
            return None
    
    def check_site_authorization(self, guard_id, door_id):
        """Check if guard has access to this door"""
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT gsa.id, gsa.access_level, gsa.status
            FROM guard_site_access gsa
            JOIN guards g ON gsa.guard_id = g.id
            JOIN sites s ON gsa.site_id = s.id
            JOIN site_doors sd ON s.id = sd.site_id
            WHERE g.provincial_guard_id = %s
              AND sd.door_id = %s
              AND gsa.status = 'active'
              AND (gsa.access_start_date IS NULL OR gsa.access_start_date <= CURRENT_DATE)
              AND (gsa.access_end_date IS NULL OR gsa.access_end_date >= CURRENT_DATE)
        """, (guard_id, door_id))
        
        row = cursor.fetchone()
        if not row:
            return {'authorized': False, 'reason': 'No access grant for this door'}
        
        return {'authorized': True, 'access_level': row[1]}
    
    def check_schedule(self, guard_id, door_id):
        """Check if current time is within guard's authorized schedule"""
        # Get current day and time
        now = datetime.now()
        day_of_week = now.strftime('%A').lower()
        current_time = now.time()
        
        cursor = self.db.cursor()
        cursor.execute("""
            SELECT gsa.schedule
            FROM guard_site_access gsa
            JOIN guards g ON gsa.guard_id = g.id
            WHERE g.provincial_guard_id = %s
              AND gsa.status = 'active'
        """, (guard_id,))
        
        row = cursor.fetchone()
        if not row or not row[0]:
            return True  # No schedule restriction
        
        schedule = row[0]  # JSONB
        day_schedule = schedule.get(day_of_week)
        
        if not day_schedule:
            return False  # Not authorized today
        
        start_time = datetime.strptime(day_schedule['start'], '%H:%M').time()
        end_time = datetime.strptime(day_schedule['end'], '%H:%M').time()
        
        return start_time <= current_time <= end_time
    
    def elapsed_ms(self, start_time):
        """Calculate elapsed milliseconds"""
        return int((datetime.now() - start_time).total_seconds() * 1000)
```

---

## Company Portal Interface

### Web Application (React + FastAPI)

**Dashboard:**

```
┌─────────────────────────────────────────────────────────────────┐
│  Acme Security Services - Guard Management Portal               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────┐  ┌──────────────────────┐            │
│  │  Active Guards       │  │  Active Sites         │            │
│  │  ════════════        │  │  ════════════         │            │
│  │      127             │  │       24              │            │
│  └──────────────────────┘  └──────────────────────┘            │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Recent Access Events                                     │  │
│  ├────────┬──────────────┬──────────────┬──────────┬────────┤  │
│  │ Time   │ Guard        │ Site         │ Door     │ Result │  │
│  ├────────┼──────────────┼──────────────┼──────────┼────────┤  │
│  │ 08:03  │ SMITH, JOHN  │ Acme Corp HQ │ Main Ent │ ✓ GRANT│  │
│  │ 08:15  │ DOE, JANE    │ Warehouse #2 │ Loading  │ ✓ GRANT│  │
│  │ 08:22  │ JONES, BOB   │ Acme Corp HQ │ Server   │ ✗ DENY │  │
│  │ 08:35  │ BROWN, ALICE │ Office Plaza │ Lobby    │ ✓ GRANT│  │
│  └────────┴──────────────┴──────────────┴──────────┴────────┘  │
│                                                                  │
│  [+ Add Guard]  [Manage Sites]  [Access Reports]  [Settings]   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Guard Management Screen:**

```
┌─────────────────────────────────────────────────────────────────┐
│  Guard: SMITH, JOHN (SG-ON-123456)                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Provincial Certification Status                          │ │
│  │  ═══════════════════════════════                          │ │
│  │  Status: ● ACTIVE                                         │ │
│  │  Level: Advanced Guard                                    │ │
│  │  Issued: 2025-01-15                                       │ │
│  │  Expires: 2027-01-15                                      │ │
│  │  Qualifications: First Aid, Use of Force, WHMIS          │ │
│  │  [View Provincial Record] [Verify Now]                   │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Employment Details                                        │ │
│  │  ══════════════════                                        │ │
│  │  Position: Security Guard                                 │ │
│  │  Hire Date: 2025-02-01                                    │ │
│  │  Status: Active                                           │ │
│  │  Employee ID: EMP-4532                                    │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  Site Access Assignments                                  │ │
│  │  ════════════════════                                     │ │
│  │  ┌──────────────────┬──────────┬────────────────────────┐ │ │
│  │  │ Site             │ Level    │ Schedule                │ │ │
│  │  ├──────────────────┼──────────┼────────────────────────┤ │ │
│  │  │ Acme Corp HQ     │ Guard    │ Mon-Fri 08:00-16:00    │ │ │
│  │  │ Office Plaza     │ Patrol   │ Sat-Sun 10:00-18:00    │ │ │
│  │  └──────────────────┴──────────┴────────────────────────┘ │ │
│  │  [+ Assign New Site]                                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  [Edit] [Terminate] [View Access Log]                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Site Access Assignment Wizard:**

```
┌─────────────────────────────────────────────────────────────────┐
│  Assign Guard to Site                                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 1: Select Guard                                           │
│  ═══════════════════                                            │
│  Guard: SMITH, JOHN (SG-ON-123456)                             │
│  Certification: ✓ Active (Verified 2 mins ago)                 │
│                                                                  │
│  Step 2: Select Site                                            │
│  ═══════════════════                                            │
│  ▼ Select Site...                                              │
│  ├─ Acme Corporation HQ                                        │
│  ├─ Warehouse District #2                                      │
│  ├─ Office Plaza Downtown                                      │
│  └─ Manufacturing Facility East                                │
│                                                                  │
│  Step 3: Configure Access                                       │
│  ═══════════════════════                                        │
│  Access Level: ▼ Security Guard                               │
│               (Options: Visitor, Guard, Supervisor, Manager)   │
│                                                                  │
│  Physical Access (Doors):                                      │
│  ☑ Main Entrance (Door 1)                                      │
│  ☑ Employee Entrance (Door 2)                                  │
│  ☐ Executive Floor (Door 15)                                   │
│  ☑ Parking Garage (Door 20)                                    │
│                                                                  │
│  Logical Access (Systems):                                     │
│  ☑ Computer Login (Guard Station)                             │
│  ☑ Video Management System (View Only)                        │
│  ☐ Access Control Admin Panel                                 │
│  ☐ Time & Attendance Admin                                    │
│                                                                  │
│  Step 4: Set Schedule                                           │
│  ═══════════════════                                            │
│  ☑ Monday    08:00 - 16:00                                     │
│  ☑ Tuesday   08:00 - 16:00                                     │
│  ☑ Wednesday 08:00 - 16:00                                     │
│  ☑ Thursday  08:00 - 16:00                                     │
│  ☑ Friday    08:00 - 16:00                                     │
│  ☐ Saturday  ______ - ______                                   │
│  ☐ Sunday    ______ - ______                                   │
│                                                                  │
│  Access Period:                                                │
│  Start Date: [2025-02-05]                                      │
│  End Date:   [  Permanent  ] or [____-__-__]                   │
│                                                                  │
│  [Cancel] [Save & Deploy] ←── Pushes to controllers in 60 sec  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Governance & Operations

### Ministry Responsibilities

**Certification Management:**
- Conduct or approve security guard training programs
- Administer certification exams
- Perform background checks
- Issue PIV credentials
- Maintain guard registry
- Handle disciplinary actions
- Process renewals

**PKI Operations:**
- Operate Root and Issuing CAs
- OCSP responder (24/7 uptime)
- Certificate lifecycle management
- Key escrow (optional, for recovery)
- Audit logging

**Federation Management:**
- Company registration and vetting
- API key issuance
- Rate limiting and abuse prevention
- Dispute resolution
- Standards enforcement

### Security Company Responsibilities

**Employment Management:**
- Register guards with ministry
- Assign guards to sites
- Maintain employment records
- Terminate access when needed
- Report incidents

**Access Control:**
- Define site access policies
- Configure schedules and permissions
- Monitor access events
- Generate compliance reports

**System Integration:**
- Deploy OS-PACS infrastructure
- Maintain door controllers
- Sync with ministry APIs
- Respond to webhook notifications

### Guard Responsibilities

**Credential Protection:**
- Safeguard PIV card (treat like driver's license)
- Never share PIN
- Report lost/stolen card immediately
- Keep contact info current with ministry

**Professional Conduct:**
- Maintain active certification
- Complete required training
- Follow site-specific procedures
- Accurate time and attendance

---

## Cost Model

### Ministry Setup Costs (One-Time)

| Component | Cost | Notes |
|-----------|------|-------|
| PKI Infrastructure | $100,000 | HSM, servers, Dogtag setup |
| Enrollment Centers (5 locations) | $250,000 | Biometric equipment, workstations |
| Software Development | $500,000 | APIs, portal, integration |
| Java Cards (initial 15,000) | $75,000 | $5 each |
| Training & Change Management | $100,000 | Ministry staff, documentation |
| **Total Setup** | **$1,025,000** | |

### Ministry Annual Operating Costs

| Component | Cost | Notes |
|-----------|------|-------|
| PKI Operations | $50,000 | Hosting, maintenance, support |
| Card Issuance (5,000/year new + renewal) | $25,000 | Cards, labor |
| Staff (3 FTE) | $250,000 | Admin, support, enforcement |
| Infrastructure | $30,000 | Servers, bandwidth, monitoring |
| **Total Annual** | **$355,000** | |

**Funded by**: Guard certification fees ($50/year × 10,000 guards = $500,000/year)

### Security Company Costs (Per Company, 100 Guards)

**Initial Setup:**

| Component | Cost | Notes |
|-----------|------|-------|
| OS-PACS Infrastructure (20 sites, 80 doors) | $35,000 | Controllers, readers, locks |
| Company Portal License | $0 | Open source |
| Integration Services | $10,000 | Professional services (one-time) |
| **Total Setup** | **$45,000** | vs $80,000 proprietary |

**Annual Operating:**

| Component | Cost | Notes |
|-----------|------|-------|
| System Maintenance | $5,000 | Updates, support |
| API Fees | $0 | Ministry provides free |
| Hardware Replacement | $2,000 | 5% annual |
| **Total Annual** | **$7,000** | vs $15,000 proprietary |

**ROI**: 44% savings on initial costs, 53% savings on annual costs

---

## Security & Privacy

### Data Protection

**Personal Information Handling:**

```yaml
Data Classification:
  Public:
    - Guard ID (SG-ON-123456)
    - Certification level
    - Active/inactive status
  
  Protected B (Ministry & Employer Only):
    - Full name
    - Photo
    - Fingerprint templates (encrypted)
    - Training records
    - Disciplinary history
  
  Restricted (Ministry Only):
    - Background check results
    - Criminal record checks
    - Home address
    - SIN (if collected)

Access Controls:
  - Role-based access (RBAC)
  - Audit all queries
  - Data minimization (companies see only what they need)
  - Encryption at rest and in transit
  - Annual privacy impact assessments

Retention:
  - Active guard records: Indefinite
  - Terminated guards: 7 years post-termination
  - Access logs: 2 years
  - Audit trails: 7 years
```

### Threat Model & Mitigations

| Threat | Impact | Mitigation |
|--------|--------|------------|
| Card cloning | High | Cryptographic certificates (can't clone private keys) |
| Credential fraud | High | Biometric enrollment, PKI validation |
| Insider threat (company) | Medium | Ministry oversight, audit trails |
| Certificate revocation delay | Medium | OCSP (real-time), push notifications |
| Ministry system compromise | Critical | HSM for Root CA, offline storage |
| Privacy breach | High | Encryption, access controls, audits |
| Denial of service | Medium | Offline mode, cached credentials |

---

## Compliance & Standards

### Alignment with Standards

| Standard | Application | Compliance Level |
|----------|-------------|------------------|
| **FIPS 201** | PIV credential format | Full compliance |
| **NIST SP 800-73** | PIV interface specifications | Full compliance |
| **ISO 27001** | Information security management | Aligned |
| **OpenID Connect** | Federation protocol | Certified |
| **OAuth 2.0** | Authorization framework | RFC compliant |
| **GDPR/PIPEDA** | Privacy regulations | Compliant (Canada) |

### Open Source Licenses

| Component | License | Allows Commercial Use |
|-----------|---------|----------------------|
| OpenPIV | Apache 2.0 | Yes |
| OS-PACS (Leosac) | AGPL 3.0 | Yes (with source disclosure) |
| Dogtag PKI | GPL 2.0 | Yes |
| OpenSC | LGPL 2.1 | Yes |
| Company Portal | Apache 2.0 | Yes |
| Federation APIs | Apache 2.0 | Yes |

---

## Implementation Roadmap

### Phase 1: Pilot Program (6 months)

**Scope**: 500 guards, 5 companies, 20 sites

**Milestones:**
- Month 1-2: Ministry PKI setup, enrollment center deployment
- Month 3: Issue 100 pilot cards, onboard 2 companies
- Month 4-5: Deploy OS-PACS at 10 sites, test federation
- Month 6: Evaluate, refine, prepare for full rollout

**Budget**: $200,000

### Phase 2: Provincial Rollout (12 months)

**Scope**: 10,000 guards, 200 companies, 500 sites

**Milestones:**
- Month 7-9: Open 5 enrollment centers province-wide
- Month 10-15: Mass card issuance (2,000/month)
- Month 16-18: Company onboarding (40/month)
- Month 18: Full operational capability

**Budget**: $1,200,000

### Phase 3: Continuous Improvement (Ongoing)

- Mobile credential support (2026)
- Biometric verification at doors (2026)
- AI anomaly detection (2027)
- Integration with police databases (2027)
- Expand to other regulated professions (paramedics, tow truck operators)

---

## Success Metrics

### Key Performance Indicators (KPIs)

**Security:**
- Credential fraud incidents: <1 per year (vs 50+ current)
- Unauthorized access events: <0.1% of attempts
- Revocation propagation time: <5 minutes (vs 48 hours current)

**Efficiency:**
- Guard onboarding time: <24 hours (vs 5-7 days current)
- Multi-site guard deployment: Same day (vs 2 weeks current)
- Access policy changes: <1 hour (vs 1 week current)

**Adoption:**
- Year 1: 50% of active guards credentialed
- Year 2: 90% of active guards credentialed
- Year 3: 100% compliance (mandatory)

**Cost:**
- Total 5-year TCO: $10M (vs $25M proprietary)
- ROI: 60% savings
- Break-even: 18 months

---

## Conclusion

The Provincial Security Guard Universal Credential System represents a **transformational approach** to professional identity management in the security industry:

✅ **One Card, One Standard** - Universal PIV credential works everywhere  
✅ **Enhanced Security** - Cryptographic authentication prevents fraud  
✅ **Instant Revocation** - Real-time certificate validation across province  
✅ **Professional Standards** - Ministry oversight ensures quality  
✅ **Operational Efficiency** - Seamless multi-site, multi-company operations  
✅ **Complete Interoperability** - Open standards enable competition  
✅ **Cost Effective** - 60% savings vs proprietary systems  
✅ **Privacy Protected** - Data minimization, encryption, oversight  
✅ **100% Open Source** - Transparent, auditable, community-driven  

**This system can serve as a model for other regulated professions across Canada and globally.**

---

**Document Version**: 1.0  
**Date**: December 2025  
**Author**: Toussaint Louis  
**Status**: Concept Proposal  
**Next Steps**: Present to Ministry of Public Safety for feasibility assessment

**For More Information:**
- OpenPIV Project: https://openpiv.org
- OS-PACS Documentation: https://os-pacs.org
- Technical Questions: tech@securityguard.gov.on.ca
- Policy Questions: policy@securityguard.gov.on.ca
