---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: cbc19923-ae3a-46d9-96a8-92f566982a67
original_filename: OpenPIV_Implementation_Roadmap.md
created_at: 2026-03-04T20:36:55.731188+00:00
content_hash: 315c9263543f
topic: opensecure-openpiv-subsystem
topic: "openpiv-pacs-integration-suite"
---

# OpenPIV Implementation Roadmap
## Detailed Task Breakdown & Sprint Planning

---

## Phase 1: Foundation (Weeks 1-12)

### Sprint 1.1: Development Environment Setup (Week 1-2)

#### Tasks

**1.1.1 Lab Infrastructure Setup**
- [ ] Provision Ubuntu 24.04 server (physical or VM)
  - Minimum: 4 cores, 8GB RAM, 100GB storage
  - Network: Static IP, firewall configured
- [ ] Install base dependencies
  ```bash
  sudo apt update && sudo apt upgrade -y
  sudo apt install -y git python3-pip python3-venv openjdk-11-jdk \
    postgresql postgresql-contrib docker.io docker-compose \
    pcscd pcsc-tools opensc-pkcs11
  ```
- [ ] Configure Docker for non-root user
- [ ] Set up GitHub organization/repositories

**1.1.2 Hardware Acquisition**
- [ ] Order Java Cards (5-10 for testing)
  - Recommended: NXP JCOP3 J3H145
  - Supplier: SmartCardFocus, CardLogix, or eBay
- [ ] Order smart card reader/writer
  - Option 1: ACR38U (~$30)
  - Option 2: Identiv SCR3500 (~$45)
- [ ] Test reader connectivity
  ```bash
  pcsc_scan  # Should detect reader
  ```

**1.1.3 Documentation Framework**
- [ ] Initialize openpiv-docs repository
- [ ] Set up MkDocs or Docusaurus
- [ ] Create documentation outline
- [ ] Establish Git workflow (branching strategy)

**Deliverable:** Working development environment with reader detecting cards

---

### Sprint 1.2: PKI Infrastructure (Weeks 3-5)

#### Tasks

**1.2.1 Dogtag Installation**
- [ ] Review Dogtag documentation
  - https://www.dogtagpki.org/wiki/PKI_Main_Page
- [ ] Install Dogtag PKI
  ```bash
  sudo apt install dogtag-pki
  pkispawn -f ca.cfg  # Use pre-configured CA profile
  ```
- [ ] Configure initial CA
  - Set organization name
  - Generate root certificate
  - Configure OCSP responder
- [ ] Document CA initialization process

**1.2.2 Certificate Profiles**
- [ ] Create PIV Authentication profile
  - Key Usage: Digital Signature, Key Encipherment
  - Extended Key Usage: Client Authentication
- [ ] Create Card Authentication profile
  - Key Usage: Digital Signature
  - Extended Key Usage: Smart Card Logon
- [ ] Create Digital Signature profile
  - Key Usage: Digital Signature, Non-Repudiation
- [ ] Create Key Management profile
  - Key Usage: Key Encipherment
  - Extended Key Usage: Email Protection
- [ ] Test manual certificate issuance

**1.2.3 PKI Automation Scripts**
- [ ] Write Python script: `issue_piv_certs.py`
  - Generate key pair on card
  - Submit CSR to Dogtag
  - Retrieve signed certificates
  - Import certs to card
- [ ] Write script: `revoke_certificate.py`
  - Check certificate status
  - Add to CRL
  - Update OCSP
- [ ] Write script: `renew_certificate.py`
- [ ] Create integration tests

**Deliverable:** Functional PKI issuing test certificates

---

### Sprint 1.3: Smart Card Programming (Weeks 6-8)

#### Tasks

**1.3.1 OpenFIPS201 Setup**
- [ ] Clone OpenFIPS201 repository
  ```bash
  git clone https://github.com/makinako/OpenFIPS201
  cd OpenFIPS201
  ```
- [ ] Build applet
  ```bash
  # Install ant if needed
  sudo apt install ant
  ant dist
  ```
- [ ] Verify CAP file creation

**1.3.2 Card Loading**
- [ ] Install GlobalPlatformPro
  ```bash
  wget https://github.com/martinpaljak/GlobalPlatformPro/releases/download/v20.01.23/gp.jar
  ```
- [ ] Test card detection
  ```bash
  java -jar gp.jar -l  # List cards
  java -jar gp.jar -i  # Card info
  ```
- [ ] Load OpenFIPS201 applet
  ```bash
  java -jar gp.jar --install OpenFIPS201.cap
  ```
- [ ] Verify applet installation
- [ ] Document any errors/workarounds

**1.3.3 Card Initialization**
- [ ] Install piv-tool (part of OpenSC)
- [ ] Initialize PIV application
  ```bash
  piv-tool --admin A:9B:03  # Set admin key
  piv-tool --generate-key 9A  # Generate auth key
  ```
- [ ] Write initialization script
- [ ] Test key generation on card
- [ ] Generate CSR from card

**1.3.4 Full Card Personalization**
- [ ] Write end-to-end script: `personalize_card.py`
  1. Load applet
  2. Set admin keys
  3. Generate 4 key pairs on card
  4. Submit CSRs to Dogtag
  5. Import signed certificates
  6. Set cardholder PIN
  7. Write CHUID data object
  8. Write FASC-N (if applicable)
- [ ] Test complete workflow
- [ ] Document timing (should be <10 minutes)

**Deliverable:** Script that takes blank Java Card → fully personalized PIV card

---

### Sprint 1.4: Client Middleware (Weeks 9-10)

#### Tasks

**1.4.1 OpenSC Configuration**
- [ ] Verify OpenSC installation
  ```bash
  opensc-tool --list-readers
  pkcs11-tool --list-slots
  ```
- [ ] Create custom opensc.conf
  - Enable PIV driver
  - Set card reader preferences
  - Configure debug logging
- [ ] Test card recognition
  ```bash
  pkcs11-tool --list-objects  # Should show certificates
  ```

**1.4.2 Linux Authentication**
- [ ] Install PAM module
  ```bash
  sudo apt install libpam-pkcs11
  ```
- [ ] Configure PAM
  - Edit /etc/pam.d/common-auth
  - Add pkcs11 authentication
- [ ] Map certificates to users
  - Create user certificate mapping
  - Test with test account
- [ ] Test login flow
  - Insert card
  - Enter PIN
  - Verify login success

**1.4.3 SSH Authentication**
- [ ] Configure SSH for PIV
  - Enable public key authentication
  - Extract public key from certificate
- [ ] Add to authorized_keys
- [ ] Test SSH login with card
  ```bash
  ssh -I /usr/lib/x86_64-linux-gnu/opensc-pkcs11.so user@host
  ```
- [ ] Document setup process

**Deliverable:** Linux workstation authenticating via PIV card

---

### Sprint 1.5: Testing & Documentation (Weeks 11-12)

#### Tasks

**1.5.1 Integration Testing**
- [ ] Create test suite
  - Test: Card loading
  - Test: Certificate issuance
  - Test: Card authentication
  - Test: Certificate revocation
- [ ] Document test results
- [ ] Create troubleshooting guide

**1.5.2 Initial Documentation**
- [ ] Write "Getting Started" guide
- [ ] Document hardware requirements
- [ ] Create setup tutorials with screenshots
- [ ] Write operator manual for card issuance
- [ ] Document security considerations

**1.5.3 Demo Environment**
- [ ] Create Docker Compose file
  - Dogtag CA container
  - PostgreSQL database
  - Test web interface
- [ ] Write quick-start script
- [ ] Test on clean Ubuntu VM

**Deliverable:** Complete Phase 1 documentation and demo environment

---

## Phase 2: Enrollment System (Weeks 13-24)

### Sprint 2.1: Database Design (Weeks 13-14)

#### Tasks

**2.1.1 Schema Design**
- [ ] Design database schema
  ```sql
  -- Users table
  -- Credentials table
  -- Biometrics table
  -- Audit log table
  -- Certificates table
  ```
- [ ] Set up PostgreSQL
- [ ] Create migrations (using Alembic)
- [ ] Add indexes for performance
- [ ] Implement audit logging

**2.1.2 Data Security**
- [ ] Implement encryption at rest
  - Biometric data encrypted
  - PII fields encrypted
- [ ] Set up database backups
- [ ] Configure access controls
- [ ] Test backup/restore

---

### Sprint 2.2: Backend API (Weeks 15-18)

#### Tasks

**2.2.1 FastAPI Setup**
- [ ] Initialize FastAPI project
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  pip install fastapi uvicorn sqlalchemy pydantic
  ```
- [ ] Create project structure
  ```
  backend/
  ├── app/
  │   ├── api/
  │   ├── models/
  │   ├── schemas/
  │   ├── services/
  │   └── main.py
  ```
- [ ] Set up database connection
- [ ] Implement authentication

**2.2.2 Core API Endpoints**
- [ ] POST /api/enrollment/initiate
  - Validate identity documents
  - Create user record
  - Return enrollment ID
- [ ] POST /api/enrollment/biometrics
  - Upload fingerprint data
  - Upload facial photo
  - Quality checks
- [ ] POST /api/enrollment/issue-card
  - Trigger card personalization
  - Return card serial number
- [ ] GET /api/credentials/{user_id}
  - Retrieve user credentials
  - Return certificate status
- [ ] POST /api/certificates/revoke
  - Revoke certificate
  - Update CRL

**2.2.3 Card Programming Integration**
- [ ] Integrate card personalization script
- [ ] Handle async card programming
- [ ] Implement error handling
- [ ] Add progress tracking

**2.2.4 Security Hardening**
- [ ] Implement JWT authentication
- [ ] Add role-based access control
- [ ] Rate limiting
- [ ] Input validation
- [ ] SQL injection prevention

---

### Sprint 2.3: Frontend Development (Weeks 19-21)

#### Tasks

**2.3.1 React Setup**
- [ ] Initialize React app
  ```bash
  npx create-react-app enrollment-portal
  cd enrollment-portal
  npm install axios react-router-dom
  ```
- [ ] Set up routing
- [ ] Create component structure
- [ ] Implement authentication flow

**2.3.2 Enrollment Workflow UI**
- [ ] Create enrollment wizard
  - Step 1: Identity verification
  - Step 2: Biometric capture
  - Step 3: Card issuance
  - Step 4: Confirmation
- [ ] Implement form validation
- [ ] Add progress indicators
- [ ] Create success/error handling

**2.3.3 Biometric Capture Interface**
- [ ] Webcam integration for photos
  - Use react-webcam library
  - Quality preview
  - Retake option
- [ ] Fingerprint scanner integration
  - Use Web USB API or native bridge
  - Template quality check
  - Multiple finger capture
- [ ] Signature capture (optional)

**2.3.4 Admin Dashboard**
- [ ] Create user management interface
- [ ] Certificate status viewer
- [ ] Revocation interface
- [ ] Audit log viewer
- [ ] System health monitoring

---

### Sprint 2.4: Biometric Processing (Weeks 22-23)

#### Tasks

**2.4.1 Fingerprint Processing**
- [ ] Research fingerprint libraries
  - Option 1: PyFingerprint
  - Option 2: NBIS (NIST Biometric Image Software)
- [ ] Implement quality checks
  - NFIQ score calculation
  - Resolution validation
- [ ] Template extraction
- [ ] Format conversion (ANSI 378, ISO 19794-2)

**2.4.2 Facial Image Processing**
- [ ] Face detection (OpenCV)
- [ ] Quality assessment
  - Lighting check
  - Face positioning
  - Resolution validation
- [ ] Crop and format
- [ ] JPEG2000 encoding (PIV requirement)

**2.4.3 Data Storage**
- [ ] Encrypt biometric templates
- [ ] Implement secure deletion
- [ ] Retention policy enforcement
- [ ] Privacy compliance documentation

---

### Sprint 2.5: Identity Proofing (Week 24)

#### Tasks

**2.5.1 Identity Verification Workflow**
- [ ] Define IAL levels
  - IAL-1: Self-asserted
  - IAL-2: Remote with documents
  - IAL-3: In-person proofing
- [ ] Document validation
  - Driver's license parsing
  - Passport validation
  - Government ID checks
- [ ] Anti-fraud measures
  - Duplicate detection
  - Liveness detection (for photos)

**2.5.2 Approval Workflow**
- [ ] Multi-stage approval process
- [ ] Notification system
- [ ] Rejection handling
- [ ] Re-enrollment process

**Deliverable:** Functional enrollment system (web-based)

---

## Phase 3: Physical Access Control (Weeks 25-36)

### Sprint 3.1: Leosac Deployment (Weeks 25-27)

#### Tasks

**3.1.1 Leosac Installation**
- [ ] Clone Leosac repository
  ```bash
  git clone https://github.com/leosac/leosac
  cd leosac
  ```
- [ ] Build from source or use Docker
  ```bash
  docker pull leosac/leosac
  ```
- [ ] Configure kernel.xml
  - Database connection
  - Module loading
  - Network settings
- [ ] Start Leosac server
- [ ] Access web interface

**3.1.2 Module Configuration**
- [ ] Enable PIV authentication module
- [ ] Configure OSDP module
- [ ] Set up database persistence
- [ ] Enable audit logging
- [ ] Configure event notification

**3.1.3 Certificate Validation**
- [ ] Integrate with Dogtag OCSP
- [ ] Implement certificate chain validation
- [ ] Add CRL checking
- [ ] Test revocation detection
- [ ] Performance optimization

---

### Sprint 3.2: Hardware Integration (Weeks 28-30)

#### Tasks

**3.2.1 Reader Procurement & Testing**
- [ ] Order OSDP readers
  - Option 1: HID Signo 40 (~$200)
  - Option 2: Identiv uTrust (~$150)
- [ ] Test reader communication
- [ ] Configure reader settings
  - Beep settings
  - LED behavior
  - Read distance

**3.2.2 Wiring & Installation**
- [ ] Plan wiring runs
- [ ] Install readers at test door
- [ ] Connect to Raspberry Pi/controller
- [ ] Configure OSDP addresses
- [ ] Test card reading

**3.2.3 Door Control Integration**
- [ ] Install door strike/maglock
- [ ] Wire relay board
- [ ] Configure unlock duration
- [ ] Test door operation
- [ ] Add emergency override

---

### Sprint 3.3: Access Policies (Weeks 31-32)

#### Tasks

**3.3.1 Policy Engine**
- [ ] Design policy schema
  ```yaml
  doors:
    - id: main_entrance
      policies:
        - role: employee
          schedule: business_hours
        - role: admin
          schedule: always
  ```
- [ ] Implement policy evaluation
- [ ] Add time-based restrictions
- [ ] Implement role-based access

**3.3.2 User Provisioning**
- [ ] Link user accounts to certificates
- [ ] Assign roles and permissions
- [ ] Manage door groups
- [ ] Implement temporary access
- [ ] Guest access workflow

---

### Sprint 3.4: Monitoring & Logging (Weeks 33-34)

#### Tasks

**3.4.1 Event Logging**
- [ ] Configure comprehensive logging
  - Access grants
  - Access denials
  - System events
- [ ] Implement log rotation
- [ ] Set up centralized logging
- [ ] Create audit reports

**3.4.2 Real-time Monitoring**
- [ ] Install Prometheus exporters
- [ ] Create Grafana dashboards
  - Door status
  - Access events
  - System health
- [ ] Configure alerting
  - Failed access attempts
  - System failures
  - Certificate expirations

---

### Sprint 3.5: Testing & Documentation (Weeks 35-36)

#### Tasks

**3.5.1 Integration Testing**
- [ ] Test normal access flow
- [ ] Test denied access (expired cert)
- [ ] Test revoked certificate
- [ ] Test time restrictions
- [ ] Test emergency scenarios
- [ ] Load testing (multiple readers)

**3.5.2 Documentation**
- [ ] Hardware installation guide
- [ ] Configuration manual
- [ ] Troubleshooting guide
- [ ] Security best practices

**Deliverable:** Operational physical access control system

---

## Phase 4: Windows/macOS Integration (Weeks 37-48)

### Sprint 4.1: Windows Support (Weeks 37-40)

#### Tasks

**4.1.1 Minidriver Installation**
- [ ] Install OpenSC Minidriver
- [ ] Configure Windows to recognize cards
- [ ] Test credential provider
- [ ] Document installation steps

**4.1.2 Group Policy Integration**
- [ ] Configure domain for smart card auth
- [ ] Map certificates to AD users
- [ ] Set up certificate trust
- [ ] Test domain login

**4.1.3 Application Integration**
- [ ] Outlook S/MIME
- [ ] VPN (Cisco AnyConnect, etc.)
- [ ] Web browsers
- [ ] Custom applications

---

### Sprint 4.2: macOS Support (Weeks 41-43)

#### Tasks

**4.2.1 macOS Configuration**
- [ ] Install OpenSC on macOS
- [ ] Configure Keychain Access
- [ ] Test card recognition
- [ ] Enable smart card login

**4.2.2 Application Integration**
- [ ] Safari client certificates
- [ ] Mail.app S/MIME
- [ ] SSH authentication
- [ ] FileVault integration

---

### Sprint 4.3: Cross-Platform Testing (Week 44)

#### Tasks

- [ ] Test card on all platforms
- [ ] Verify certificate portability
- [ ] Document platform-specific issues
- [ ] Create user guides for each OS

---

### Sprint 4.4: User Training Materials (Weeks 45-46)

#### Tasks

**4.4.1 User Documentation**
- [ ] Create quick start guide
- [ ] Write PIN management guide
- [ ] Document common issues
- [ ] Create FAQ

**4.4.2 Training Videos**
- [ ] Record enrollment process
- [ ] Demonstrate card usage
- [ ] Show troubleshooting steps
- [ ] Publish to docs site

---

### Sprint 4.5: Help Desk Resources (Weeks 47-48)

#### Tasks

**4.5.1 Support Tools**
- [ ] Create diagnostic script
- [ ] Build card status checker
- [ ] Implement remote assistance tools
- [ ] Create troubleshooting flowchart

**4.5.2 Help Desk Training**
- [ ] Write operator manual
- [ ] Create escalation procedures
- [ ] Document common solutions
- [ ] Conduct training session

**Deliverable:** Multi-platform support with comprehensive documentation

---

## Phase 5: Hardening & Production (Weeks 49-60)

### Sprint 5.1: Security Audit (Weeks 49-51)

#### Tasks

**5.1.1 Vulnerability Assessment**
- [ ] Run automated scanners
  - OWASP ZAP for web interface
  - Nmap for network services
  - Lynis for Linux hardening
- [ ] Review code for security issues
- [ ] Check for outdated dependencies
- [ ] Scan for exposed secrets

**5.1.2 Penetration Testing**
- [ ] Test card cloning resistance
- [ ] Attempt privilege escalation
- [ ] Test certificate validation bypass
- [ ] Social engineering scenarios
- [ ] Document all findings

**5.1.3 Remediation**
- [ ] Fix critical vulnerabilities
- [ ] Patch high-priority issues
- [ ] Re-test after fixes
- [ ] Update security documentation

---

### Sprint 5.2: Compliance Documentation (Weeks 52-54)

#### Tasks

**5.2.1 FIPS 201 Gap Analysis**
- [ ] Document compliant features
- [ ] Identify gaps vs. federal standard
- [ ] Create compliance matrix
- [ ] Write limitations disclosure

**5.2.2 Security Policies**
- [ ] Write Certificate Practice Statement (CPS)
- [ ] Create Certification Policy (CP)
- [ ] Document key management procedures
- [ ] Incident response plan

**5.2.3 Audit Trails**
- [ ] Verify complete audit coverage
- [ ] Test log integrity
- [ ] Document retention policies
- [ ] Create audit reports

---

### Sprint 5.3: High Availability (Weeks 55-57)

#### Tasks

**5.3.1 CA Redundancy**
- [ ] Set up secondary CA server
- [ ] Configure database replication
- [ ] Test failover procedures
- [ ] Document recovery steps

**5.3.2 Backup & Recovery**
- [ ] Implement automated backups
  - Database dumps
  - Certificate archives
  - Configuration files
- [ ] Test restoration procedures
- [ ] Document RTO/RPO
- [ ] Offsite backup storage

**5.3.3 Monitoring & Alerting**
- [ ] Configure health checks
- [ ] Set up uptime monitoring
- [ ] Create alert escalation
- [ ] Test notification system

---

### Sprint 5.4: Performance Optimization (Weeks 58-59)

#### Tasks

**5.4.1 Load Testing**
- [ ] Simulate 100 concurrent enrollments
- [ ] Test 1000+ certificate validations/min
- [ ] Benchmark database queries
- [ ] Identify bottlenecks

**5.4.2 Optimization**
- [ ] Database query optimization
- [ ] Caching strategy (Redis)
- [ ] Connection pooling
- [ ] Certificate revocation caching

**5.4.3 Scalability Planning**
- [ ] Document scaling strategies
- [ ] Plan for 10x growth
- [ ] Test horizontal scaling
- [ ] Create capacity planning guide

---

### Sprint 5.5: Production Deployment (Week 60)

#### Tasks

**5.5.1 Production Checklist**
- [ ] Security hardening complete
- [ ] Backups operational
- [ ] Monitoring configured
- [ ] Documentation finalized
- [ ] Training completed
- [ ] Support processes established

**5.5.2 Go-Live**
- [ ] Final pre-deployment testing
- [ ] Deploy to production
- [ ] Pilot group enrollment (10-20 users)
- [ ] Monitor for issues
- [ ] Gradual rollout to all users

**5.5.3 Post-Deployment**
- [ ] Collect user feedback
- [ ] Address immediate issues
- [ ] Performance monitoring
- [ ] Plan next iteration

**Deliverable:** Production-ready OpenPIV system

---

## Ongoing Maintenance & Iteration

### Monthly Tasks
- [ ] Certificate renewals
- [ ] Security updates
- [ ] Backup verification
- [ ] User access reviews
- [ ] Performance monitoring

### Quarterly Tasks
- [ ] Security audits
- [ ] Disaster recovery testing
- [ ] User training refreshers
- [ ] Hardware inventory
- [ ] Software updates

### Annual Tasks
- [ ] Comprehensive security assessment
- [ ] Compliance review
- [ ] Business continuity planning
- [ ] Technology refresh planning

---

## Success Criteria Checklist

### Technical Success
- [ ] Cards authenticate successfully on all platforms
- [ ] Certificate issuance < 15 minutes
- [ ] Authentication latency < 2 seconds
- [ ] Zero security incidents in pilot
- [ ] 99.5% system uptime

### Operational Success
- [ ] User satisfaction > 85%
- [ ] Support tickets < 5% monthly
- [ ] All operators trained
- [ ] Documentation 100% complete
- [ ] Audit compliance verified

### Business Success
- [ ] Project delivered on time
- [ ] Within budget
- [ ] Meets security requirements
- [ ] Positive stakeholder feedback
- [ ] Roadmap for future enhancements

---

**Document Version:** 1.0  
**Last Updated:** December 2025  
**Author:** Toussaint Louis
