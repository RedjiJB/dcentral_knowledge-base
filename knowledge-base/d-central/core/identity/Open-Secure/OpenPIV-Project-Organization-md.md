---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: 78f28244-f1a2-4e0c-b609-eb8f26c79d4e
original_filename: OpenPIV_Project_Organization.md
created_at: 2026-03-04T20:36:57.066434+00:00
content_hash: bb875f310945
topic: opensecure-openpiv-subsystem
consolidated_into: docs/DC-OPENSECURE-OPENPIV-SUBSYSTEM-RECONCILED-001.md
---

# OpenPIV - Open Source Personal Identity Verification Ecosystem

**Project Vision:** Build a fully open-source identity verification and access control ecosystem that meets FIPS 201 standards using transparent, auditable components.

---

## Executive Summary

OpenPIV creates a complete alternative to proprietary PIV/CIV systems by implementing federal standards (NIST SP 800-73, FIPS 201) using exclusively open-source components. The system provides:

- **Smart card issuance** using OpenFIPS201 on programmable Java Cards
- **Enterprise PKI** with Dogtag Certificate System
- **Physical access control** via Leosac/LibOSDP
- **Logical access** through OpenSC middleware
- **Complete sovereignty** - no vendor lock-in or proprietary dependencies

**Target Use Cases:**
- Private organizations requiring strong authentication
- Educational institutions for student/staff credentials
- Cybersecurity labs and training environments
- Organizations wanting PIV-like security without federal dependencies

---

## Project Structure

### Core Repositories

```
OpenPIV-Ecosystem/
├── openpiv-cards/              # Smart card implementation
├── openpiv-pki/                # Certificate authority and PKI
├── openpiv-enrollment/         # Identity proofing and card issuance
├── openpiv-middleware/         # Client authentication stack
├── openpiv-access-control/     # Physical access management
├── openpiv-integration/        # System integration guides
└── openpiv-docs/               # Comprehensive documentation
```

---

## Component Architecture

### 1. Smart Card Layer (openpiv-cards)

**Primary Component:** OpenFIPS201  
**Function:** PIV applet for Java Cards implementing NIST SP 800-73-4

**Deliverables:**
- Pre-compiled OpenFIPS201 CAP files
- Card initialization scripts
- Hardware compatibility matrix
- Testing suite for card validation

**Key Files:**
```
openpiv-cards/
├── applets/
│   ├── OpenFIPS201.cap           # Compiled applet
│   ├── build-instructions.md
│   └── source/                   # OpenFIPS201 source
├── scripts/
│   ├── load-applet.sh            # GlobalPlatformPro wrapper
│   ├── initialize-card.sh
│   └── verify-card.sh
├── hardware/
│   ├── compatible-cards.md       # Tested Java Card models
│   └── reader-requirements.md
└── docs/
    ├── card-lifecycle.md
    └── troubleshooting.md
```

**Technical Requirements:**
- Java Card 3.0.4+ with cryptographic extensions
- Support for ECC P-256 or RSA 2048
- Minimum 80KB persistent memory
- GlobalPlatform 2.1.1 compliant

---

### 2. PKI Infrastructure (openpiv-pki)

**Primary Component:** Dogtag Certificate System  
**Function:** Enterprise Certificate Authority for PIV certificates

**Deliverables:**
- Dogtag deployment automation (Ansible/Docker)
- PIV certificate profiles (4 types)
- CA hierarchy design templates
- OCSP responder configuration

**Key Files:**
```
openpiv-pki/
├── deployment/
│   ├── docker-compose.yml        # Containerized CA
│   ├── ansible/                  # Production deployment
│   └── vagrant/                  # Development environment
├── profiles/
│   ├── piv-auth.cfg              # PIV Authentication
│   ├── card-auth.cfg             # Card Authentication
│   ├── digital-signature.cfg
│   └── key-management.cfg
├── scripts/
│   ├── initialize-ca.sh
│   ├── issue-certificate.py
│   └── revoke-certificate.py
├── policies/
│   ├── certificate-policy.md
│   └── cps-template.md           # Certificate Practice Statement
└── docs/
    ├── architecture.md
    ├── security-hardening.md
    └── backup-recovery.md
```

**Certificate Types Issued:**
1. **PIV Authentication** - Network/system login
2. **Card Authentication** - Contactless authentication
3. **Digital Signature** - Document signing
4. **Key Management** - Email encryption

---

### 3. Enrollment & Issuance (openpiv-enrollment)

**Primary Components:** Custom Python stack + workflow engine  
**Function:** Identity proofing, biometric capture, card personalization

**Deliverables:**
- Web-based enrollment portal
- Biometric capture integration
- Card programming workflow
- Identity vetting framework

**Key Files:**
```
openpiv-enrollment/
├── webapp/
│   ├── backend/                  # Flask/FastAPI application
│   ├── frontend/                 # React enrollment interface
│   └── database/                 # PostgreSQL schemas
├── biometrics/
│   ├── fingerprint-capture.py
│   ├── photo-capture.py
│   └── quality-checks.py
├── card-programming/
│   ├── personalization.py        # Write certs to card
│   ├── chuid-generator.py        # Generate CHUID
│   └── pin-setup.py
├── identity-proofing/
│   ├── verification-levels.md    # IAL-1, IAL-2, IAL-3
│   ├── document-validation.py
│   └── workflow-engine.py
└── docs/
    ├── enrollment-process.md
    ├── operator-manual.md
    └── audit-logging.md
```

**Identity Assurance Levels:**
- **IAL-1:** Self-asserted (basic registration)
- **IAL-2:** Remote verification with documents
- **IAL-3:** In-person proofing (federal equivalent)

---

### 4. Client Middleware (openpiv-middleware)

**Primary Component:** OpenSC  
**Function:** Operating system integration for PIV card recognition

**Deliverables:**
- OpenSC configuration templates
- OS-specific integration guides
- PAM modules for Linux authentication
- GINA/Credential Provider for Windows

**Key Files:**
```
openpiv-middleware/
├── opensc-config/
│   ├── opensc.conf               # Custom PIV settings
│   └── profiles/
├── integration/
│   ├── linux/
│   │   ├── pam-config.sh
│   │   └── polkit-rules/
│   ├── windows/
│   │   ├── minidriver-install.ps1
│   │   └── registry-settings.reg
│   └── macos/
│       └── tokend-config.sh
├── ssh/
│   ├── ssh-piv-setup.sh
│   └── agent-forwarding.md
├── browser/
│   ├── firefox-client-cert.md
│   └── chrome-setup.md
└── docs/
    ├── deployment-guide.md
    └── troubleshooting.md
```

**Capabilities Enabled:**
- Smart card login (Windows/Linux/macOS)
- SSH authentication via PIV
- Web browser client certificates
- Email signing (S/MIME)
- VPN authentication

---

### 5. Physical Access Control (openpiv-access-control)

**Primary Components:** Leosac + LibOSDP  
**Function:** Door controllers and access decision engine

**Deliverables:**
- Leosac server deployment
- OSDP reader configurations
- Access control policies
- Integration with card authentication

**Key Files:**
```
openpiv-access-control/
├── leosac/
│   ├── docker-compose.yml
│   ├── kernel.xml                # Main configuration
│   └── modules/
│       ├── piv-auth.xml          # PIV certificate validation
│       └── wiegand-config.xml
├── hardware/
│   ├── compatible-readers.md
│   ├── controller-specs.md
│   └── wiring-diagrams/
├── policies/
│   ├── access-rules.md
│   ├── role-based-access.yml
│   └── time-restrictions.yml
├── integration/
│   ├── dogtag-certificate-check.py
│   └── real-time-revocation.py
└── docs/
    ├── deployment.md
    ├── osdp-protocol.md
    └── security-best-practices.md
```

**Access Control Features:**
- Certificate-based authentication
- Real-time revocation checking (OCSP)
- Role-based access control
- Time-of-day restrictions
- Audit logging and reporting

---

### 6. System Integration (openpiv-integration)

**Function:** End-to-end deployment guides and testing

**Key Files:**
```
openpiv-integration/
├── deployment-scenarios/
│   ├── small-office.md           # 10-50 users
│   ├── enterprise.md             # 500+ users
│   └── education.md              # University campus
├── testing/
│   ├── integration-tests.py
│   ├── load-testing/
│   └── compliance-validation.py
├── monitoring/
│   ├── prometheus-exporters/
│   ├── grafana-dashboards/
│   └── alerting-rules.yml
└── migration/
    ├── from-proprietary-piv.md
    └── data-import-tools/
```

---

### 7. Documentation Hub (openpiv-docs)

**Function:** Central knowledge base for entire ecosystem

**Key Files:**
```
openpiv-docs/
├── getting-started/
│   ├── 01-introduction.md
│   ├── 02-quick-start.md
│   └── 03-architecture-overview.md
├── standards/
│   ├── fips-201-compliance.md
│   ├── nist-sp-800-73.md
│   └── gap-analysis.md           # What we can't do vs. federal
├── security/
│   ├── threat-model.md
│   ├── security-hardening.md
│   └── incident-response.md
├── operations/
│   ├── day-to-day-operations.md
│   ├── backup-restore.md
│   └── disaster-recovery.md
└── development/
    ├── contributing.md
    ├── coding-standards.md
    └── testing-guidelines.md
```

---

## Development Phases

### Phase 1: Core Infrastructure (Months 1-3)
**Goal:** Establish foundational components

**Milestones:**
- [ ] OpenFIPS201 successfully loaded on test Java Cards
- [ ] Dogtag CA issuing test certificates
- [ ] OpenSC recognizing cards on Linux workstation
- [ ] Basic enrollment workflow (CLI-based)

**Deliverables:**
- Working PKI infrastructure
- Card programming pipeline
- Certificate issuance automation
- Basic documentation

---

### Phase 2: Enrollment System (Months 4-6)
**Goal:** Build user-friendly enrollment capabilities

**Milestones:**
- [ ] Web-based enrollment portal deployed
- [ ] Biometric capture integrated (fingerprints + photo)
- [ ] Automated card personalization
- [ ] Identity proofing workflows implemented

**Deliverables:**
- React enrollment application
- Database schema for user records
- Card programming automation
- Operator training materials

---

### Phase 3: Access Control (Months 7-9)
**Goal:** Physical access control integration

**Milestones:**
- [ ] Leosac server operational
- [ ] OSDP readers communicating
- [ ] Certificate validation at doors
- [ ] Access policies enforced

**Deliverables:**
- Physical access control system
- Hardware compatibility testing
- Integration with PKI
- Access control policies

---

### Phase 4: Logical Access (Months 10-12)
**Goal:** Complete authentication ecosystem

**Milestones:**
- [ ] Windows login via PIV
- [ ] Linux PAM integration
- [ ] SSH authentication working
- [ ] Browser client certificates

**Deliverables:**
- Multi-OS middleware configurations
- SSH/VPN integration guides
- Email signing setup
- User training documentation

---

### Phase 5: Hardening & Compliance (Months 13-15)
**Goal:** Security hardening and standards validation

**Milestones:**
- [ ] Security audit completed
- [ ] Penetration testing performed
- [ ] FIPS 201 gap analysis documented
- [ ] Compliance documentation

**Deliverables:**
- Security audit report
- Hardening guides
- Compliance documentation
- Best practices guide

---

## Technical Stack Summary

| Layer | Component | License | Purpose |
|-------|-----------|---------|---------|
| **Smart Card** | OpenFIPS201 | Apache 2.0 | PIV applet |
| **Card Loading** | GlobalPlatformPro | LGPL 3.0 | Applet deployment |
| **PKI** | Dogtag | GPL 2.0 | Certificate Authority |
| **Middleware** | OpenSC | LGPL 2.1 | Card driver |
| **Access Control** | Leosac | AGPL 3.0 | Door controller |
| **OSDP Protocol** | LibOSDP | Apache 2.0 | Reader communication |
| **Database** | PostgreSQL | PostgreSQL | Data persistence |
| **Web Framework** | FastAPI | MIT | Enrollment backend |
| **Frontend** | React | MIT | Enrollment UI |

---

## Standards Compliance

### NIST Standards Implemented

**FIPS 201-3:** Personal Identity Verification  
- Credential format and structure
- Biometric data requirements
- Visual card specifications

**SP 800-73-4:** PIV Interfaces  
- Card command interface (APDUs)
- Data object specifications
- Cryptographic mechanisms

**SP 800-76-2:** Biometric Specifications  
- Fingerprint image quality
- Facial image requirements

**SP 800-78-4:** Cryptographic Algorithms  
- Approved algorithms (ECC P-256, RSA 2048)
- Key generation requirements

### Gaps vs. Federal PIV

**What We CAN Achieve:**
- Technical compliance with NIST specifications
- Interoperable card format
- Cryptographically secure authentication
- Complete open-source transparency

**What We CANNOT Achieve:**
- Official FIPS 201 approval (requires NIST validation)
- Federal PKI cross-certification
- Appearance on GSA Approved Product List (APL)
- Use for actual federal facility access

**Practical Reality:**  
OpenPIV provides 95%+ of PIV functionality for private sector use while maintaining complete control over the ecosystem.

---

## Hardware Requirements

### Essential Hardware

**For Card Issuance Station:**
- Smart card reader/writer (ISO 7816 compliant)
  - Recommended: ACR38U, Identiv SCR3500
  - ~$30-50 each
- Fingerprint scanner (FBI-certified for production)
  - Recommended: Digital Persona U.are.U 4500
  - ~$200-400
- Webcam or camera (for facial photos)
  - Minimum: 1080p resolution
  - ~$50-100

**Java Cards:**
- NXP JCOP3 J3H145 or J3R180
- Infineon SLE78 series
- Cost: $2-8 per card (bulk pricing)

**Physical Access Readers:**
- OSDP-compliant contactless readers
  - HID Signo series
  - Identiv uTrust readers
  - ~$150-300 per reader

**Access Controllers:**
- Raspberry Pi 4 (4GB+ RAM) or industrial PC
  - For running Leosac
  - ~$75-150

---

## Security Considerations

### Cryptographic Key Management

**Root CA Private Key:**
- **Storage:** HSM (Hardware Security Module) or air-gapped system
- **Access:** Ceremony-based with multi-person control
- **Backup:** Encrypted, geographically distributed

**Issuing CA Keys:**
- **Storage:** HSM for production, encrypted files for development
- **Rotation:** Every 2-3 years
- **Monitoring:** All signing operations logged

### Enrollment Station Hardening

- Dedicated, isolated network segment
- Full disk encryption
- Biometric data encrypted at rest
- Audit logging of all operations
- Physical security (locked room, camera coverage)

### Card PIN Management

- User-selected 6-8 digit PIN
- Minimum 3 failed attempts before lockout
- PUK (PIN Unblock Key) for recovery
- Never transmitted or stored in plaintext

---

## Deployment Models

### Model 1: Small Office (10-50 users)

**Infrastructure:**
- Single Ubuntu server (Dogtag CA + Leosac)
- One enrollment workstation
- 2-5 door readers

**Estimated Cost:** $3,000-5,000  
**Setup Time:** 2-3 weeks  
**Maintenance:** Minimal (quarterly cert renewals)

---

### Model 2: Enterprise (500+ users)

**Infrastructure:**
- Clustered PKI (3+ Dogtag instances)
- Multiple enrollment stations
- 50+ door readers across facilities
- Dedicated monitoring/logging infrastructure

**Estimated Cost:** $25,000-50,000  
**Setup Time:** 2-3 months  
**Maintenance:** Dedicated team

---

### Model 3: Education/Training Lab

**Infrastructure:**
- Containerized deployment (Docker Compose)
- Rapid provisioning/teardown
- Simulated scenarios for cybersecurity training

**Estimated Cost:** $1,000-2,000  
**Setup Time:** 1-2 days  
**Use Case:** Hands-on PIV/PKI training

---

## Success Metrics

### Technical Metrics
- Card issuance time: <15 minutes per user
- Authentication latency: <2 seconds
- Certificate validation: <1 second
- System uptime: >99.5%

### Security Metrics
- Zero private key compromises
- 100% audit trail coverage
- Certificate revocation propagation: <1 hour
- Failed authentication alerts: Real-time

### Operational Metrics
- User satisfaction: >85% positive feedback
- Support tickets: <5% of user base monthly
- Documentation completeness: >90% coverage
- Training completion: 100% of operators

---

## Risk Management

### Technical Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Java Card compatibility | High | Maintain tested hardware matrix |
| CA key compromise | Critical | HSM storage, access controls |
| Certificate expiry | Medium | Automated monitoring, alerts |
| Reader firmware bugs | Low | Vendor testing, fallback protocols |

### Operational Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Staff turnover | Medium | Cross-training, documentation |
| Hardware failure | Medium | Redundancy, spare inventory |
| Budget constraints | High | Phased deployment, open-source |
| Compliance gaps | Low | Regular gap analysis |

---

## Community & Governance

### Open Source Strategy

**License:** Apache 2.0 (permissive, enterprise-friendly)  
**Repository:** GitHub with public issue tracking  
**Communication:** Discord/Slack for real-time, mailing list for formal

### Contribution Guidelines

- Code review required (2 approvers minimum)
- Security issues reported privately
- Comprehensive test coverage (>80%)
- Documentation required for new features

### Roadmap Transparency

- Quarterly planning published publicly
- Feature requests tracked in GitHub
- Community voting on priorities

---

## Future Enhancements

### Year 2 Goals
- Mobile credential support (digital wallet)
- Blockchain-based certificate transparency logs
- AI-driven anomaly detection
- Multi-tenant SaaS offering

### Year 3+ Vision
- FIDO2 integration
- Quantum-resistant cryptography
- Decentralized identity (DID) support
- Global interoperability framework

---

## Getting Started

### For Evaluators (1 Hour Quick Start)

```bash
# Clone repositories
git clone https://github.com/OpenPIV/openpiv-ecosystem
cd openpiv-ecosystem

# Launch demo environment (Docker)
docker-compose -f quick-start.yml up -d

# Access enrollment portal
open http://localhost:8080

# Follow guided demo workflow
```

### For Production Deployment (Full Guide)

See: `openpiv-docs/deployment/production-deployment.md`

---

## Support & Resources

**Documentation:** https://docs.openpiv.org  
**Community Forum:** https://community.openpiv.org  
**Security Issues:** security@openpiv.org  
**Commercial Support:** List of certified integrators

---

## License & Legal

**Primary License:** Apache 2.0  
**Component Licenses:** See individual repositories  
**Trademark:** "OpenPIV" is a registered trademark

**Disclaimer:** OpenPIV provides technical compliance with FIPS 201 standards but is not officially validated by NIST or approved for federal government use. Organizations should conduct their own security assessments before production deployment.

---

## Appendices

### Appendix A: Glossary
- **PIV:** Personal Identity Verification
- **FIPS 201:** Federal standard for PIV credentials
- **CHUID:** Cardholder Unique Identifier
- **APDU:** Application Protocol Data Unit
- **OSDP:** Open Supervised Device Protocol
- **HSM:** Hardware Security Module
- **IAL:** Identity Assurance Level

### Appendix B: References
- NIST Special Publications (800-73, 800-76, 800-78)
- FIPS 201-3 Standard
- OpenFIPS201 GitHub Repository
- Dogtag Certificate System Documentation
- OpenSC Wiki

### Appendix C: Vendor Contact List
- Java Card Suppliers
- Reader Manufacturers
- HSM Providers
- Training Organizations

---

**Document Version:** 1.0  
**Last Updated:** December 2025  
**Author:** Toussaint Louis  
**Organization:** OpenPIV Project
