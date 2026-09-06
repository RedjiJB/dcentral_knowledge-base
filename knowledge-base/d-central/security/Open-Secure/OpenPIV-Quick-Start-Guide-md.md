---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: 84786f05-33ec-4fce-9f2a-5599844c47eb
original_filename: OpenPIV_Quick_Start_Guide.md
created_at: 2026-03-04T20:36:57.350024+00:00
content_hash: 3f912a73b822
topic: opensecure-openpiv-subsystem
topic: "openpiv-pacs-integration-suite"
consolidated_into: [docs/DC-OPENPIV-PACS-INTEGRATION-RECONCILED-001.md, docs/DC-OPENSECURE-OPENPIV-SUBSYSTEM-RECONCILED-001.md]
---

# OpenPIV Quick Start Guide
## Get Your First PIV Card Working in One Day

**Target:** Working PIV card authenticating to a Linux system  
**Time Required:** 4-8 hours  
**Prerequisites:** Ubuntu 24.04 system, $100 budget for hardware

---

## Shopping List (Order Today)

### Essential Hardware (~$70)

1. **Smart Card Reader** (~$35)
   - **Option A:** ACR38U-I1 USB Reader
     - Link: Amazon, eBay, SmartCardFocus
   - **Option B:** Identiv SCR3500
   
2. **Java Cards** (~$30 for 5 cards)
   - **Recommended:** NXP JCOP3 J3H145
     - Specs: 144KB memory, Java Card 3.0.4
     - Suppliers:
       - SmartCardFocus.com
       - CardLogix.com
       - eBay (search "JCOP3 J3H145")
   - **Alternative:** Infineon SLE78
   
3. **Optional:** Fingerprint scanner ($200-400)
   - Skip for initial testing
   - Use for production deployment

---

## Day 1 Timeline

### Hour 1: Environment Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install core dependencies
sudo apt install -y \
    git curl wget \
    openjdk-11-jdk ant \
    pcscd pcsc-tools \
    opensc-pkcs11 \
    python3 python3-pip python3-venv \
    postgresql postgresql-contrib \
    docker.io docker-compose

# Add user to smartcard group
sudo usermod -a -G scard $USER

# Start PC/SC daemon
sudo systemctl enable pcscd
sudo systemctl start pcscd

# Verify reader detection (plug in reader first)
pcsc_scan
# Should show: "Reader 0: ACR38U..."
# Press Ctrl+C to exit
```

---

### Hour 2: Java Card Setup

**Download GlobalPlatformPro:**

```bash
cd ~/Downloads
wget https://github.com/martinpaljak/GlobalPlatformPro/releases/download/v20.01.23/gp.jar
chmod +x gp.jar

# Create tools directory
mkdir -p ~/openpiv-tools
mv gp.jar ~/openpiv-tools/
cd ~/openpiv-tools
```

**Test Card Detection:**

```bash
# Insert a blank Java Card into reader
java -jar gp.jar -l
# Expected output: Lists detected cards

java -jar gp.jar -i
# Expected output: Card info including ATR
```

**Build OpenFIPS201:**

```bash
cd ~/openpiv-tools
git clone https://github.com/makinako/OpenFIPS201
cd OpenFIPS201

# Build the applet
ant dist

# Verify CAP file exists
ls -lh OpenFIPS201.cap
# Should show ~30-50KB file
```

**Load Applet to Card:**

```bash
# CRITICAL: Make sure card is inserted
java -jar ../gp.jar --install OpenFIPS201.cap

# Verify installation
java -jar ../gp.jar -l
# Should show OpenFIPS201 in applet list
```

**Troubleshooting:**
- **Error: "No readers found"** → Check reader connection, restart pcscd
- **Error: "Authentication failed"** → Card may be locked, try new card
- **Error: "Not enough memory"** → Wrong card type, need JCOP3 144KB

---

### Hour 3: PKI Setup (Dogtag)

**Install Dogtag:**

```bash
# Add Dogtag repository
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:dogtag-pki/dogtag-pki
sudo apt update

# Install Dogtag
sudo apt install -y dogtag-pki

# Verify installation
pkispawn --help
```

**Quick CA Configuration:**

```bash
# Create config file
cat > ~/openpiv-tools/ca-config.cfg << 'EOF'
[DEFAULT]
pki_instance_name=pki-tomcat
pki_https_port=8443
pki_http_port=8080

[CA]
pki_admin_email=admin@example.com
pki_admin_name=Administrator
pki_admin_uid=admin
pki_admin_password=Secret.123
pki_client_pkcs12_password=Secret.123
pki_ds_password=Secret.123
pki_security_domain_password=Secret.123

pki_ca_signing_nickname=CA Signing Certificate
pki_organization=OpenPIV Demo
EOF

# Deploy CA (takes 2-3 minutes)
sudo pkispawn -f ~/openpiv-tools/ca-config.cfg -s CA

# Check CA status
sudo systemctl status pki-tomcatd@pki-tomcat.service

# Access web interface
# URL: https://localhost:8443/ca
# Login: admin / Secret.123
```

**Create PIV Certificate Profile:**

```bash
# Create profile for PIV Authentication certificate
sudo tee /etc/pki/pki-tomcat/ca/profiles/ca/pivAuth.cfg > /dev/null << 'EOF'
profileId=pivAuth
desc=PIV Authentication Certificate
visible=true
enable=true
auth.instance_id=

input.list=i1,i2
input.i1.class_id=certReqInputImpl
input.i2.class_id=submitterInfoInputImpl

output.list=o1
output.o1.class_id=certOutputImpl

policyset.list=serverCertSet
policyset.serverCertSet.list=1,2,3,4,5,6,7,8

policyset.serverCertSet.1.constraint.class_id=subjectNameConstraintImpl
policyset.serverCertSet.1.constraint.name=Subject Name Constraint
policyset.serverCertSet.1.constraint.params.pattern=CN=.*PIV Auth.*

policyset.serverCertSet.2.constraint.class_id=validityConstraintImpl
policyset.serverCertSet.2.constraint.name=Validity Constraint
policyset.serverCertSet.2.default.class_id=validityDefaultImpl
policyset.serverCertSet.2.default.params.range=1095
policyset.serverCertSet.2.default.params.startTime=0

policyset.serverCertSet.3.constraint.class_id=keyConstraintImpl
policyset.serverCertSet.3.constraint.name=Key Constraint
policyset.serverCertSet.3.constraint.params.keyType=RSA
policyset.serverCertSet.3.constraint.params.keyParameters=2048

policyset.serverCertSet.4.default.class_id=authorityKeyIdentifierExtDefaultImpl
policyset.serverCertSet.4.default.name=Authority Key Identifier Extension Default

policyset.serverCertSet.5.default.class_id=keyUsageExtDefaultImpl
policyset.serverCertSet.5.default.name=Key Usage Extension Default
policyset.serverCertSet.5.default.params.keyUsageDigitalSignature=true
policyset.serverCertSet.5.default.params.keyUsageKeyEncipherment=true
policyset.serverCertSet.5.default.params.keyUsageCritical=true

policyset.serverCertSet.6.default.class_id=extendedKeyUsageExtDefaultImpl
policyset.serverCertSet.6.default.name=Extended Key Usage Extension Default
policyset.serverCertSet.6.default.params.exKeyUsageOIDs=1.3.6.1.5.5.7.3.2

policyset.serverCertSet.7.default.class_id=subjectKeyIdentifierExtDefaultImpl
policyset.serverCertSet.7.default.name=Subject Key Identifier Extension Default

policyset.serverCertSet.8.default.class_id=signingAlgDefaultImpl
policyset.serverCertSet.8.default.name=Signing Alg
policyset.serverCertSet.8.default.params.signingAlg=-
EOF

# Restart CA to load profile
sudo systemctl restart pki-tomcatd@pki-tomcat.service
```

---

### Hour 4: Card Personalization Script

**Create Python Script:**

```bash
mkdir -p ~/openpiv-tools/scripts
cd ~/openpiv-tools/scripts

# Install dependencies
pip3 install PyKCS11 cryptography requests

# Create personalization script
cat > personalize_card.py << 'EOF'
#!/usr/bin/env python3
"""
OpenPIV Card Personalization Script
Generates keys, creates CSR, gets certificate from CA, imports to card
"""

import subprocess
import sys
import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
import requests
from datetime import datetime

def run_command(cmd, description):
    """Execute shell command and handle errors"""
    print(f"\n[*] {description}")
    print(f"    Command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[!] Error: {result.stderr}")
        sys.exit(1)
    print(f"[✓] Success")
    return result.stdout

def generate_key_on_card(slot):
    """Generate RSA key pair on PIV card"""
    print(f"\n=== Generating key in slot {slot} ===")
    cmd = ["piv-tool", "--generate-key", slot, "--key-type", "RSA2048"]
    output = run_command(cmd, f"Generating RSA-2048 key in slot {slot}")
    
    # Extract public key
    pubkey_file = f"/tmp/pubkey_{slot}.pem"
    cmd = ["piv-tool", "--read-certificate", slot]
    run_command(cmd, f"Reading public key from slot {slot}")
    
    return pubkey_file

def create_csr(slot, subject_cn):
    """Create Certificate Signing Request"""
    print(f"\n=== Creating CSR for {subject_cn} ===")
    
    # Generate CSR using piv-tool
    csr_file = f"/tmp/csr_{slot}.pem"
    cmd = [
        "piv-tool",
        "--generate-csr",
        slot,
        "--subject", f"CN={subject_cn},O=OpenPIV Demo",
        "--output", csr_file
    ]
    run_command(cmd, "Creating CSR")
    
    return csr_file

def submit_to_ca(csr_file, profile="pivAuth"):
    """Submit CSR to Dogtag CA and get signed certificate"""
    print(f"\n=== Submitting CSR to CA (profile: {profile}) ===")
    
    # Read CSR
    with open(csr_file, 'r') as f:
        csr_pem = f.read()
    
    # Submit to Dogtag (simplified - use pki command)
    cert_file = csr_file.replace('.pem', '_cert.pem')
    
    # Use pki CLI tool
    cmd = [
        "pki",
        "-d", "/etc/pki/pki-tomcat/alias",
        "-c", "Secret.123",
        "-n", "CA Signing Certificate",
        "ca-cert-request-submit",
        "--profile", profile,
        "--request-type", "pkcs10",
        "--csr-file", csr_file,
        "--subject", f"CN=Test User PIV Auth,O=OpenPIV Demo"
    ]
    
    output = run_command(cmd, "Submitting CSR to CA")
    
    # Extract request ID
    request_id = None
    for line in output.split('\n'):
        if 'Request ID:' in line:
            request_id = line.split(':')[1].strip()
            break
    
    if not request_id:
        print("[!] Failed to extract request ID")
        sys.exit(1)
    
    print(f"[*] Request ID: {request_id}")
    
    # Approve request (auto-approve in demo)
    cmd = [
        "pki",
        "-d", "/etc/pki/pki-tomcat/alias",
        "-c", "Secret.123",
        "-n", "CA Signing Certificate",
        "ca-cert-request-approve",
        request_id
    ]
    run_command(cmd, "Approving certificate request")
    
    # Download certificate
    cmd = [
        "pki",
        "-d", "/etc/pki/pki-tomcat/alias",
        "-c", "Secret.123",
        "ca-cert-export",
        f"--output-file", cert_file,
        f"0x{request_id}"
    ]
    run_command(cmd, "Downloading signed certificate")
    
    return cert_file

def import_certificate_to_card(cert_file, slot):
    """Import signed certificate to PIV card"""
    print(f"\n=== Importing certificate to slot {slot} ===")
    
    cmd = [
        "piv-tool",
        "--import-certificate",
        cert_file,
        "--key-slot", slot
    ]
    run_command(cmd, f"Importing certificate to slot {slot}")

def set_pin():
    """Set user PIN on card"""
    print("\n=== Setting User PIN ===")
    print("[*] Default PIN: 123456")
    print("[*] New PIN: 654321")
    
    cmd = ["piv-tool", "--change-pin"]
    # Note: This is interactive, handle accordingly
    print("[!] Manual step: Run 'piv-tool --change-pin' and set PIN")

def main():
    print("""
    ╔═══════════════════════════════════════╗
    ║  OpenPIV Card Personalization Tool   ║
    ║  Version 1.0 - Demo Edition          ║
    ╚═══════════════════════════════════════╝
    """)
    
    # Check for card
    print("[*] Checking for card...")
    result = subprocess.run(["piv-tool", "--info"], capture_output=True)
    if result.returncode != 0:
        print("[!] No PIV card detected. Insert card and try again.")
        sys.exit(1)
    
    print("[✓] PIV card detected")
    
    # User information
    user_name = input("\n[?] Enter user's full name (e.g., John Doe): ").strip()
    if not user_name:
        user_name = "Test User"
    
    # Generate key and certificate for PIV Authentication (slot 9A)
    slot = "9A"
    subject_cn = f"{user_name} PIV Auth"
    
    print(f"\n[*] Starting personalization for: {subject_cn}")
    print(f"[*] Timestamp: {datetime.now()}")
    
    # Workflow
    pubkey_file = generate_key_on_card(slot)
    csr_file = create_csr(slot, subject_cn)
    cert_file = submit_to_ca(csr_file, profile="pivAuth")
    import_certificate_to_card(cert_file, slot)
    
    print("\n" + "="*50)
    print("[✓] Card personalization complete!")
    print("="*50)
    print(f"Certificate imported to slot {slot}")
    print("\nNext steps:")
    print("1. Set PIN: piv-tool --change-pin")
    print("2. Test authentication: pkcs11-tool --list-objects")
    print("3. Configure PAM for login")
    print("\nCard is ready to use!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
EOF

chmod +x personalize_card.py
```

**Run Personalization:**

```bash
# Make sure card is inserted!
python3 personalize_card.py

# Follow prompts
# Enter name: Test User
# Script will:
# 1. Generate RSA key on card
# 2. Create CSR
# 3. Submit to CA
# 4. Import signed certificate
```

---

### Hour 5: Linux Authentication Setup

**Install PAM Module:**

```bash
sudo apt install -y libpam-pkcs11

# Configure PAM
sudo tee /etc/pam_pkcs11/pam_pkcs11.conf > /dev/null << 'EOF'
pam_pkcs11 {
    nullok = false;
    debug = true;
    
    use_pkcs11_module = opensc;
    
    pkcs11_module opensc {
        module = /usr/lib/x86_64-linux-gnu/opensc-pkcs11.so;
        description = "OpenSC PKCS#11 Module";
        slot_num = 0;
    }
    
    cert_policy = ca,signature;
    
    mapper default {
        debug = true;
        module = /usr/lib/x86_64-linux-gnu/pam_pkcs11/subject_mapper.so;
        ignorecase = true;
        mapfile = /etc/pam_pkcs11/subject_mapping;
    }
}
EOF

# Create user mapping
sudo mkdir -p /etc/pam_pkcs11
sudo tee /etc/pam_pkcs11/subject_mapping << 'EOF'
# Map certificate CN to Linux username
# Format: CN=... -> username

CN=Test User PIV Auth,O=OpenPIV Demo -> testuser
EOF

# Create test user
sudo useradd -m -s /bin/bash testuser
sudo passwd testuser
# Set a password (you'll use card + PIN instead later)
```

**Configure PAM:**

```bash
# Backup original PAM config
sudo cp /etc/pam.d/common-auth /etc/pam.d/common-auth.backup

# Add smart card authentication
sudo tee -a /etc/pam.d/common-auth > /dev/null << 'EOF'

# Smart card authentication
auth    [success=1 default=ignore]  pam_pkcs11.so
EOF

# Test configuration
sudo pam-auth-update
# Select "Unix authentication" and "Smart card authentication"
```

---

### Hour 6: Testing

**Test Card Recognition:**

```bash
# Insert card and check detection
pkcs11-tool --module /usr/lib/x86_64-linux-gnu/opensc-pkcs11.so --list-slots

# Should show slot with card

# List objects on card
pkcs11-tool --module /usr/lib/x86_64-linux-gnu/opensc-pkcs11.so --list-objects --login --pin 654321

# Should show:
# - Private key
# - Certificate
# - Public key
```

**Test Certificate Validation:**

```bash
# Extract certificate from card
pkcs11-tool --module /usr/lib/x86_64-linux-gnu/opensc-pkcs11.so \
    --read-object --type cert --id 01 --pin 654321 \
    --output-file /tmp/card_cert.der

# Convert to PEM
openssl x509 -inform DER -in /tmp/card_cert.der -out /tmp/card_cert.pem

# Verify certificate
openssl x509 -in /tmp/card_cert.pem -text -noout

# Should show:
# - Subject: CN=Test User PIV Auth,O=OpenPIV Demo
# - Issuer: Your CA
# - Validity dates
# - Key Usage: Digital Signature, Key Encipherment
```

**Test Authentication (Console):**

```bash
# Switch to another TTY (Ctrl+Alt+F2)
# Login prompt should appear

# Login with:
# Username: testuser
# [Insert card]
# PIN: 654321

# Should successfully log in using card!
```

**Test SSH Authentication:**

```bash
# Enable SSH key from card
ssh-add -s /usr/lib/x86_64-linux-gnu/opensc-pkcs11.so
# Enter PIN: 654321

# List loaded keys
ssh-add -L

# Test SSH to localhost
ssh testuser@localhost
# Should authenticate with card (no password!)
```

---

## Troubleshooting

### Card Not Detected

```bash
# Check reader
lsusb | grep -i reader

# Restart pcscd
sudo systemctl restart pcscd

# Check logs
journalctl -u pcscd -f
```

### PIN Errors

```bash
# Check PIN retry counter
piv-tool --pin-status

# Reset PIN (if locked)
piv-tool --admin A:9B:03 --reset-pin
```

### Certificate Issues

```bash
# Check CA status
sudo systemctl status pki-tomcatd@pki-tomcat.service

# Check CA logs
sudo tail -f /var/log/pki/pki-tomcat/ca/system

# Manually verify certificate
openssl verify -CAfile /etc/pki/pki-tomcat/ca_signing.crt /tmp/card_cert.pem
```

---

## What You've Built

At this point, you have:

✅ Working PIV cards with OpenFIPS201 applet  
✅ Local Certificate Authority (Dogtag)  
✅ Automated card personalization  
✅ Linux authentication via smart card  
✅ SSH authentication with PIV  
✅ Foundation for full OpenPIV ecosystem  

---

## Next Steps

### Immediate Improvements

1. **Create More Certificate Types**
   - Card Authentication (9E)
   - Digital Signature (9C)
   - Key Management (9D)

2. **Build Web Enrollment Portal**
   - See Phase 2 in Implementation Roadmap
   - FastAPI + React

3. **Add Biometrics**
   - Order fingerprint scanner
   - Integrate with enrollment

### Week 2 Goals

1. **Physical Access Control**
   - Order OSDP reader
   - Install Leosac
   - Connect door strike

2. **Windows Support**
   - Install OpenSC Minidriver
   - Test Windows login

3. **Production Hardening**
   - Move Root CA to HSM
   - Enable OCSP
   - Set up monitoring

---

## Cost Breakdown

| Item | Cost | Status |
|------|------|--------|
| Smart Card Reader | $35 | Required |
| Java Cards (5x) | $30 | Required |
| **Total Day 1** | **$65** | **Minimum** |
| Fingerprint Scanner | $250 | Optional (Phase 2) |
| OSDP Reader | $200 | Optional (Phase 3) |
| Door Strike | $100 | Optional (Phase 3) |
| HSM (YubiHSM) | $650 | Optional (Production) |

---

## Resources

**Documentation:**
- OpenFIPS201: https://github.com/makinako/OpenFIPS201
- Dogtag PKI: https://www.dogtagpki.org
- OpenSC: https://github.com/OpenSC/OpenSC/wiki

**Community:**
- OpenPIV Discord: (Coming soon)
- Smart Card Developers: https://ludovicrousseau.blogspot.com

**Standards:**
- NIST SP 800-73: PIV Interface Spec
- FIPS 201: PIV Standard

---

## Daily Practice Checklist

**Daily Testing (5 minutes):**
- [ ] Insert card → Should be detected
- [ ] pkcs11-tool --list-objects → Should list certificate
- [ ] SSH with card → Should authenticate
- [ ] Check CA status → Should be running

**Weekly Maintenance:**
- [ ] Review audit logs
- [ ] Test backup/restore
- [ ] Update documentation
- [ ] Plan next feature

---

## Emergency Contacts

**Card Locked?**
```bash
# Check status
piv-tool --pin-status

# Unblock with PUK
piv-tool --unblock-pin
```

**CA Down?**
```bash
# Check service
sudo systemctl status pki-tomcatd@pki-tomcat

# View logs
sudo journalctl -u pki-tomcatd@pki-tomcat -f

# Restart if needed
sudo systemctl restart pki-tomcatd@pki-tomcat
```

**Card Corrupted?**
```bash
# Re-initialize card
java -jar ~/openpiv-tools/gp.jar --delete-all
java -jar ~/openpiv-tools/gp.jar --install ~/openpiv-tools/OpenFIPS201/OpenFIPS201.cap

# Re-run personalization
python3 ~/openpiv-tools/scripts/personalize_card.py
```

---

**Good luck with your OpenPIV journey!**

For questions or contributions, see the main project documentation.

---

**Document Version:** 1.0  
**Last Updated:** December 2025  
**Author:** Toussaint Louis


<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Topics:**
- [[knowledge-base/_topics/openpiv-pacs-integration-suite|openpiv-pacs-integration-suite]]
- [[knowledge-base/_topics/opensecure-openpiv-subsystem|opensecure-openpiv-subsystem]]

**Consolidated into:**
- [[docs/DC-OPENPIV-PACS-INTEGRATION-RECONCILED-001]]
- [[docs/DC-OPENSECURE-OPENPIV-SUBSYSTEM-RECONCILED-001]]

<!-- AUTO-GENERATED RELATED END -->
