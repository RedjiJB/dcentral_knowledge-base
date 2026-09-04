---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: 6116d031-6182-48cb-9b55-75176e47c89b
original_filename: OpenPIV_Technical_Architecture.md
created_at: 2026-03-04T20:36:57.610093+00:00
content_hash: bf34d5020639topic: openfips-personalization-login
---

# OpenPIV Technical Architecture
## System Component Reference & Data Flow

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      OpenPIV Ecosystem                           │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐         ┌──────────────────┐
│   Smart Cards    │◄────────│  Enrollment      │
│  (OpenFIPS201)   │         │  System (Web)    │
└────────┬─────────┘         └────────┬─────────┘
         │                            │
         │ APDU Commands              │ REST API
         │                            │
         ▼                            ▼
┌─────────────────────────────────────────────┐
│        PKI Infrastructure (Dogtag)          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Root CA  │  │Issue CA  │  │  OCSP    │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────┬───────────────────────┘
                      │
         ┌────────────┼────────────┐
         │            │            │
         ▼            ▼            ▼
┌─────────────┐  ┌─────────┐  ┌──────────────┐
│   Doors     │  │ Desktops│  │ Web Services │
│  (Leosac)   │  │(OpenSC) │  │ (Browser)    │
└─────────────┘  └─────────┘  └──────────────┘
```

---

## Component Breakdown

### Layer 1: Smart Card (Hardware + Applet)

**Physical Card:**
- Java Card 3.0.4+ with cryptographic co-processor
- Contact interface (ISO 7816-3)
- Contactless interface (ISO 14443 - optional)
- 80KB+ persistent EEPROM

**OpenFIPS201 Applet:**
- PIV Application Identifier (AID): A0 00 00 03 08 00 00 10 00 01 00
- Implements NIST SP 800-73-4 interface
- Supports 4 asymmetric key pairs (9A, 9C, 9D, 9E)
- Stores X.509 certificates
- PIN/PUK management

**Data Objects on Card:**
```
┌─────────────────────────────────────┐
│ PIV Card Data Structure             │
├─────────────────────────────────────┤
│ 5FC102 - Card Capability Container  │
│ 5FC105 - CHUID (Cardholder UID)     │
│ 5FC107 - Security Object            │
│ 5FC10A - Facial Image               │
│ 5FC10B - Fingerprints (2)           │
├─────────────────────────────────────┤
│ Certificate Slots:                  │
│   9A - PIV Authentication           │
│   9C - Digital Signature            │
│   9D - Key Management               │
│   9E - Card Authentication          │
└─────────────────────────────────────┘
```

**Key Generation Methods:**
1. **On-card generation** (preferred for security)
   - Private key never leaves card
   - Public key extracted for CSR
2. **External generation + import**
   - For backup/escrow scenarios
   - Requires secure key injection

---

### Layer 2: PKI Infrastructure (Dogtag Certificate System)

**Architecture:**

```
┌────────────────────────────────────────────┐
│         Dogtag PKI Hierarchy               │
├────────────────────────────────────────────┤
│                                            │
│  ┌──────────────────────────────────┐     │
│  │        Root CA (Offline)          │     │
│  │  - Stored in HSM or air-gapped    │     │
│  │  - 10 year validity               │     │
│  │  - Self-signed                    │     │
│  └─────────────┬────────────────────┘     │
│                │                           │
│                ▼                           │
│  ┌──────────────────────────────────┐     │
│  │     Issuing CA (Online)          │     │
│  │  - Issues end-entity certs        │     │
│  │  - 3-5 year validity              │     │
│  │  - Signed by Root CA              │     │
│  └─────────────┬────────────────────┘     │
│                │                           │
│                ├──► PIV Auth Certs         │
│                ├──► Card Auth Certs        │
│                ├──► Digital Sig Certs      │
│                └──► Key Mgmt Certs         │
│                                            │
│  ┌──────────────────────────────────┐     │
│  │      OCSP Responder              │     │
│  │  - Real-time cert validation      │     │
│  │  - Responds to revocation checks  │     │
│  └──────────────────────────────────┘     │
│                                            │
│  ┌──────────────────────────────────┐     │
│  │      CRL Distribution             │     │
│  │  - Publishes Certificate          │     │
│  │    Revocation Lists               │     │
│  │  - HTTP/LDAP distribution         │     │
│  └──────────────────────────────────┘     │
└────────────────────────────────────────────┘
```

**Certificate Profiles:**

```yaml
PIV Authentication Certificate (9A):
  Subject DN: CN=John Doe PIV Auth,O=Organization
  Key Usage: Digital Signature, Key Encipherment
  Extended Key Usage: Client Authentication (1.3.6.1.5.5.7.3.2)
  Validity: 3 years
  Key Size: ECC P-256 or RSA 2048

Card Authentication Certificate (9E):
  Subject DN: CN=John Doe PIV Card,O=Organization
  Key Usage: Digital Signature
  Extended Key Usage: Smart Card Logon (1.3.6.1.4.1.311.20.2.2)
  Validity: 3 years
  Purpose: Contactless authentication, no PIN required

Digital Signature Certificate (9C):
  Subject DN: CN=John Doe PIV Sig,O=Organization
  Key Usage: Digital Signature, Non-Repudiation
  Extended Key Usage: Email Protection (1.3.6.1.5.5.7.3.4)
  Validity: 3 years
  Purpose: Document signing, email S/MIME

Key Management Certificate (9D):
  Subject DN: CN=John Doe PIV Enc,O=Organization
  Key Usage: Key Encipherment
  Extended Key Usage: Email Protection
  Validity: 3 years
  Purpose: Email encryption, key establishment
```

**Certificate Issuance Workflow:**

```
User Enrollment → Generate Keys on Card → Create CSR → 
Submit to Dogtag → CA Signs Certificate → Import to Card
```

**Dogtag Directory Structure:**
```
/var/lib/pki/pki-tomcat/
├── ca/                    # CA instance
│   ├── conf/              # Configuration
│   │   └── CS.cfg         # Main config
│   ├── profiles/          # Certificate profiles
│   │   ├── caUserCert.cfg
│   │   └── custom_piv_*.cfg
│   └── emails/            # Notification templates
├── alias/                 # NSS database (keys/certs)
└── logs/                  # Audit and error logs
```

---

### Layer 3: Enrollment System

**Technology Stack:**
- **Backend:** FastAPI (Python 3.11+)
- **Database:** PostgreSQL 15
- **Frontend:** React 18 + TypeScript
- **Auth:** JWT with role-based access control

**Database Schema:**

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    employee_id VARCHAR(50) UNIQUE,
    department VARCHAR(100),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Credentials table
CREATE TABLE credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    card_serial VARCHAR(50) UNIQUE NOT NULL,
    chuid VARCHAR(200) NOT NULL,
    issued_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP NOT NULL,
    status VARCHAR(20) DEFAULT 'active',
    pin_set BOOLEAN DEFAULT FALSE
);

-- Certificates table
CREATE TABLE certificates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    credential_id UUID REFERENCES credentials(id),
    key_slot VARCHAR(2) NOT NULL, -- 9A, 9C, 9D, 9E
    subject_dn TEXT NOT NULL,
    serial_number VARCHAR(100) UNIQUE NOT NULL,
    issued_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    revoked_at TIMESTAMP,
    revocation_reason VARCHAR(50),
    certificate_pem TEXT NOT NULL
);

-- Biometrics table (encrypted)
CREATE TABLE biometrics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    biometric_type VARCHAR(20) NOT NULL, -- fingerprint, facial
    template_data BYTEA NOT NULL, -- Encrypted
    quality_score INTEGER,
    captured_at TIMESTAMP DEFAULT NOW(),
    encryption_key_id VARCHAR(100) NOT NULL
);

-- Audit log table
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    user_id UUID REFERENCES users(id),
    operator_id UUID,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    details JSONB
);
```

**API Endpoints:**

```
POST   /api/v1/enrollment/initiate
  → Start enrollment, create user record

POST   /api/v1/enrollment/biometrics
  → Upload fingerprints and facial photo

POST   /api/v1/enrollment/verify-identity
  → Submit identity documents for verification

POST   /api/v1/enrollment/issue-card
  → Trigger card personalization

GET    /api/v1/users/{user_id}
  → Retrieve user details

GET    /api/v1/credentials/{credential_id}
  → Get credential info and certificate status

POST   /api/v1/certificates/revoke
  → Revoke a certificate

GET    /api/v1/certificates/{cert_id}/status
  → Check certificate validity

POST   /api/v1/admin/reset-pin
  → Administrative PIN reset

GET    /api/v1/audit-log
  → Query audit events
```

---

### Layer 4: Client Middleware (OpenSC)

**OpenSC Components:**

```
┌────────────────────────────────────────┐
│          OpenSC Architecture           │
├────────────────────────────────────────┤
│                                        │
│  Application Layer                     │
│  └─► pkcs11-tool, opensc-tool, ssh    │
│         │                              │
│         ▼                              │
│  ┌──────────────────────────────┐     │
│  │   PKCS#11 Module             │     │
│  │   - opensc-pkcs11.so         │     │
│  │   - Standard crypto API      │     │
│  └──────────────┬───────────────┘     │
│                 │                      │
│                 ▼                      │
│  ┌──────────────────────────────┐     │
│  │   PIV Card Driver            │     │
│  │   - Understands SP 800-73    │     │
│  │   - Reads data objects       │     │
│  └──────────────┬───────────────┘     │
│                 │                      │
│                 ▼                      │
│  ┌──────────────────────────────┐     │
│  │   PC/SC Interface            │     │
│  │   - pcscd daemon             │     │
│  │   - Reader communication     │     │
│  └──────────────┬───────────────┘     │
│                 │                      │
│                 ▼                      │
│         Smart Card Reader             │
│                 │                      │
│                 ▼                      │
│            PIV Card                    │
└────────────────────────────────────────┘
```

**OpenSC Configuration (`/etc/opensc/opensc.conf`):**

```conf
app default {
    debug = 0;
    debug_file = "/tmp/opensc-debug.log";
    
    # Enable PIV driver
    card_drivers = piv;
    
    # Reader preferences
    reader_driver {
        pcsc {
            # Maximum reader instances
            max_readers = 4;
        }
    }
    
    # PIV-specific settings
    card piv {
        # PIN cache duration (seconds)
        pin_cache = true;
        pin_cache_timeout = 300;
        
        # Retire compromised keys
        retire_on_delete = true;
    }
}
```

**Linux PAM Integration:**

```bash
# /etc/pam.d/common-auth
auth    [success=2 default=ignore]  pam_pkcs11.so
auth    requisite                   pam_deny.so
auth    required                    pam_permit.so
```

**SSH Configuration:**

```bash
# ~/.ssh/config
Host *
    PKCS11Provider /usr/lib/x86_64-linux-gnu/opensc-pkcs11.so
    
# Or use ssh-agent
ssh-add -s /usr/lib/x86_64-linux-gnu/opensc-pkcs11.so
```

---

### Layer 5: Physical Access Control (Leosac)

**Leosac Architecture:**

```
┌─────────────────────────────────────────┐
│       Leosac Access Control             │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────────────────────────┐   │
│  │   Web Interface (REST API)      │   │
│  └──────────────┬──────────────────┘   │
│                 │                       │
│                 ▼                       │
│  ┌─────────────────────────────────┐   │
│  │   Core Access Decision Engine   │   │
│  │   - Policy evaluation            │   │
│  │   - Certificate validation       │   │
│  │   - Role checking                │   │
│  └──────────────┬──────────────────┘   │
│                 │                       │
│     ┌───────────┼───────────┐          │
│     ▼           ▼           ▼          │
│  ┌─────┐   ┌─────┐     ┌─────┐        │
│  │OSDP │   │GPIO │     │Wieg │        │
│  │Mod. │   │Mod. │     │Mod. │        │
│  └──┬──┘   └──┬──┘     └──┬──┘        │
│     │         │            │           │
└─────┼─────────┼────────────┼───────────┘
      │         │            │
      ▼         ▼            ▼
   Readers    Relays    Legacy Readers
```

**Configuration (`kernel.xml`):**

```xml
<kernel>
    <plugin_directories>
        <plugindir>/usr/lib/leosac</plugindir>
    </plugin_directories>
    
    <modules>
        <!-- OSDP Module for secure readers -->
        <module>
            <name>OSDP</name>
            <file>libosdp.so</file>
            <config>
                <serial_port>/dev/ttyUSB0</serial_port>
                <baud_rate>9600</baud_rate>
                <readers>
                    <reader>
                        <id>main_entrance</id>
                        <address>0</address>
                        <secure_channel>true</secure_channel>
                    </reader>
                </readers>
            </config>
        </module>
        
        <!-- PIV Authentication Module -->
        <module>
            <name>PIVAuth</name>
            <file>libpivauth.so</file>
            <config>
                <ca_cert>/etc/leosac/ca.crt</ca_cert>
                <ocsp_url>http://pki.example.org:9080/ca/ocsp</ocsp_url>
                <crl_url>http://pki.example.org/ca.crl</crl_url>
            </config>
        </module>
        
        <!-- Database Module -->
        <module>
            <name>Database</name>
            <file>libdatabase.so</file>
            <config>
                <db_type>postgresql</db_type>
                <host>localhost</host>
                <port>5432</port>
                <db_name>leosac</db_name>
                <username>leosac</username>
                <password>changeme</password>
            </config>
        </module>
    </modules>
</kernel>
```

**Access Policy Example:**

```yaml
access_policies:
  - name: "Business Hours Access"
    doors:
      - main_entrance
      - office_floor_2
    conditions:
      roles:
        - employee
        - contractor
      schedule:
        days: [Monday, Tuesday, Wednesday, Thursday, Friday]
        hours: "07:00-19:00"
      certificate_requirements:
        valid: true
        not_revoked: true
        chain_validated: true
  
  - name: "Admin Full Access"
    doors: all
    conditions:
      roles:
        - admin
        - security
      schedule:
        always: true
```

---

## Data Flow Diagrams

### Enrollment Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │
     │ 1. Submits identity documents
     │
     ▼
┌──────────────┐
│  Enrollment  │
│   Portal     │
└──────┬───────┘
       │
       │ 2. Validates identity (IAL-2/3)
       │ 3. Captures biometrics
       │
       ▼
┌──────────────┐         ┌──────────────┐
│  Database    │◄────────│   Operator   │
│              │         │  Approves    │
└──────┬───────┘         └──────────────┘
       │
       │ 4. Approved → Trigger card programming
       │
       ▼
┌──────────────────────────────────────┐
│  Card Personalization Workstation    │
│  ┌────────────────────────────────┐  │
│  │ 1. Load OpenFIPS201 applet     │  │
│  │ 2. Generate 4 key pairs        │  │
│  │ 3. Create CSRs                 │  │
│  │ 4. Submit to Dogtag            │  │
│  │ 5. Import signed certificates  │  │
│  │ 6. Write CHUID                 │  │
│  │ 7. Set PIN                     │  │
│  └────────────────────────────────┘  │
└───────────────┬──────────────────────┘
                │
                ▼
        ┌───────────────┐
        │  PIV Card     │
        │  (Complete)   │
        └───────────────┘
```

---

### Authentication Flow (Physical Access)

```
┌──────────┐
│   User   │
└────┬─────┘
     │
     │ 1. Taps card on reader
     │
     ▼
┌─────────────┐
│OSDP Reader  │
└──────┬──────┘
       │
       │ 2. Reads Card Auth certificate (9E)
       │
       ▼
┌─────────────────┐
│  Leosac Server  │
└────────┬────────┘
         │
         ├──► 3a. Validate cert chain
         │         against CA
         │
         ├──► 3b. Check revocation
         │         (OCSP query to Dogtag)
         │
         ├──► 3c. Evaluate access policy
         │         (role, time, door)
         │
         ▼
    Decision: Grant/Deny
         │
         ├──► Grant → Send unlock command
         │             via OSDP
         │
         └──► Deny  → Log event, beep error
                      
┌─────────────────┐
│  Door Strike   │ ◄─── Unlock signal
└─────────────────┘
```

---

### Logical Access Flow (Desktop Login)

```
┌──────────┐
│   User   │
└────┬─────┘
     │
     │ 1. Inserts card, enters PIN
     │
     ▼
┌──────────────┐
│  PC/SC &     │
│  OpenSC      │
└──────┬───────┘
       │
       │ 2. Reads PIV Auth cert (9A)
       │
       ▼
┌──────────────────┐
│  Operating       │
│  System (PAM)    │
└────────┬─────────┘
         │
         ├──► 3a. Verify PIN on card
         │
         ├──► 3b. Challenge-response
         │         with private key (9A)
         │
         ├──► 3c. Validate certificate
         │         chain against CA
         │
         ▼
    Map cert → user account
         │
         └──► Grant login session
```

---

## Network Architecture

### Recommended Network Segmentation

```
┌───────────────────────────────────────────────────┐
│              DMZ / Public Zone                    │
│  ┌────────────────────────────────────┐           │
│  │  Web Enrollment Portal             │           │
│  │  (HTTPS only, certificate pinning) │           │
│  └────────────────┬───────────────────┘           │
└───────────────────┼───────────────────────────────┘
                    │ Firewall
                    │ (Port 443 only)
                    ▼
┌───────────────────────────────────────────────────┐
│           Internal Management Zone                │
│  ┌────────────────────────────────────┐           │
│  │  Enrollment Backend (FastAPI)      │           │
│  └────────────────┬───────────────────┘           │
│                   │                               │
│  ┌────────────────┴───────────────────┐           │
│  │  PostgreSQL Database               │           │
│  │  (Encrypted at rest)               │           │
│  └────────────────────────────────────┘           │
└───────────────────┼───────────────────────────────┘
                    │ Firewall
                    │ (PKI protocol only)
                    ▼
┌───────────────────────────────────────────────────┐
│              PKI Security Zone                    │
│  ┌────────────────────────────────────┐           │
│  │  Dogtag CA (Issuing)               │           │
│  │  Port 8443 (HTTPS)                 │           │
│  └────────────────────────────────────┘           │
│                                                   │
│  ┌────────────────────────────────────┐           │
│  │  Root CA (Air-gapped/HSM)          │           │
│  │  Network Isolated                  │           │
│  └────────────────────────────────────┘           │
│                                                   │
│  ┌────────────────────────────────────┐           │
│  │  OCSP Responder                    │           │
│  │  Port 9080 (HTTP read-only)        │           │
│  └────────────────────────────────────┘           │
└───────────────────┼───────────────────────────────┘
                    │ Firewall
                    │ (OSDP/HTTPS only)
                    ▼
┌───────────────────────────────────────────────────┐
│         Physical Access Control Zone              │
│  ┌────────────────────────────────────┐           │
│  │  Leosac Servers                    │           │
│  │  (Clustered for HA)                │           │
│  └────────────────┬───────────────────┘           │
│                   │                               │
│                   │ OSDP Protocol                 │
│                   │                               │
│  ┌────────────────┴───────────────────┐           │
│  │  Door Controllers (OSDP)           │           │
│  │  └─► Readers, Strikes, Sensors     │           │
│  └────────────────────────────────────┘           │
└───────────────────────────────────────────────────┘
```

**Port Requirements:**

| Service | Port | Protocol | Purpose |
|---------|------|----------|---------|
| Enrollment Web | 443 | HTTPS | User-facing portal |
| Dogtag CA | 8443 | HTTPS | Certificate operations |
| OCSP | 9080 | HTTP | Revocation checking |
| PostgreSQL | 5432 | TCP | Database access |
| Leosac API | 8080 | HTTPS | Access control mgmt |
| OSDP | N/A | RS-485 | Reader communication |

---

## Performance Specifications

### Expected Throughput

**Certificate Issuance:**
- 4 certificates per card: ~30 seconds
- Concurrent enrollments: 5-10 simultaneous
- Daily capacity: 200-300 cards

**Authentication:**
- Card read + cert validation: <2 seconds
- OCSP response time: <500ms
- Concurrent door auth: 50+ per second

**Database:**
- User records: 100,000+
- Certificates: 400,000+
- Audit events: 1M+ per month
- Query response: <100ms (indexed)

---

## Security Specifications

### Cryptographic Requirements

**Card Keys:**
- Algorithm: ECC P-256 (preferred) or RSA 2048
- On-card generation mandatory for production
- Private keys never exported

**CA Keys:**
- Root CA: RSA 4096 or ECC P-384
- Issuing CA: RSA 3072 or ECC P-256
- OCSP Signing: RSA 2048 or ECC P-256

**Certificate Validity:**
- Root CA: 10 years
- Issuing CA: 5 years
- End-entity: 3 years
- OCSP: 7 days

### Audit Requirements

**Logged Events:**
- All certificate issuances
- All revocations
- All authentication attempts
- All policy changes
- All administrative actions

**Log Retention:**
- Minimum: 7 years
- Encrypted storage
- Tamper-evident (append-only)
- Regular integrity checks

---

**Document Version:** 1.0  
**Last Updated:** December 2025  
**Author:** Toussaint Louis
