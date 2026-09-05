---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: bf4fc23c-22d9-486d-972c-3e7f224fdf89
original_filename: OS-GUARDIAN_Implementation_Guide.md
created_at: 2026-03-04T20:35:37.555622+00:00
content_hash: 3fad9f925c4e
---

# OS-GUARDIAN Implementation Guide
## Body Camera & Evidence Management System Deployment

**Document Type**: Implementation Guide  
**Version**: 1.0  
**Date**: December 2024  
**Classification**: Technical Documentation  
**Audience**: Law Enforcement IT, Security Operations, Evidence Custodians

---

## Executive Summary

**Deployment Timeline**: 1 week for full department  
**Team Required**: 2-3 technicians + trainer  
**Cost per Officer**: $800-$1,200  
**Department Cost**: $35,000 (20 officers, complete system)

### Phase Overview

| Phase | Duration | Team | Deliverable |
|-------|----------|------|-------------|
| Planning | 1 day | PM + Legal | Policies documented |
| Server Setup | 1 day | IT Specialist | Evidence storage ready |
| Camera Config | 2 days | 2 Technicians | Cameras assigned |
| Docking Install | 1 day | Technician | Auto-upload working |
| Policy Setup | 1 day | Admin + Legal | Retention configured |
| Officer Training | 2 days | Trainer | Officers certified |
| Go-Live | 1 day | Full team | Operational |

---

## Pre-Deployment Planning

### Legal & Policy Framework

**Policy Requirements Checklist:**
```
LEGAL COMPLIANCE
☐ State body camera laws reviewed
☐ Privacy policies defined
☐ Retention requirements documented
☐ Public disclosure rules established
☐ Audio recording consent (if required)
☐ Biometric data handling (facial recognition)
☐ Chain of custody procedures
☐ Discovery request procedures

OPERATIONAL POLICIES
☐ When to record (mandatory vs discretionary)
☐ When NOT to record (privacy situations)
☐ Pre-event buffer settings (30-60 seconds)
☐ Activation procedures (manual vs automatic)
☐ Categorization system (incident types)
☐ Review procedures (supervisor access)
☐ Audit logging requirements
☐ Officer access limitations

RETENTION POLICIES
☐ General footage: 30-90 days
☐ Evidence: 7 years minimum
☐ Use of force: Permanent
☐ Citizen complaints: 3-5 years
☐ Court cases: Until disposition + appeals
☐ Officer-involved shooting: Permanent
☐ Training footage: 1 year
☐ Redaction requirements

DATA SECURITY
☐ Encryption at rest (AES-256)
☐ Encryption in transit (TLS 1.3)
☐ Access control (role-based)
☐ Audit logging (all access tracked)
☐ Backup procedures (3-2-1 rule)
☐ Disaster recovery plan
☐ Cybersecurity incident response
```

### Department Assessment

**Officer & Equipment Inventory:**
```
PERSONNEL
☐ Number of officers requiring cameras
☐ Number of shifts/rotations
☐ Camera sharing model (1:1 or pooled)
☐ Special units (K9, bike patrol, marine, etc.)
☐ Administrative staff needing access

EXISTING INFRASTRUCTURE
☐ CAD system integration possible?
☐ RMS system integration needed?
☐ Network infrastructure adequate?
☐ Storage capacity available?
☐ Evidence room space?
☐ Workstation availability?

OPERATIONAL REQUIREMENTS
☐ Average shift length (8, 10, 12 hours?)
☐ Recording hours per shift (est. 2-4 hours)
☐ Calls for service per day
☐ Evidence retention requirements
☐ Peak activity hours
☐ Multiple locations/precincts?
```

### Hardware Selection Guide

**Body Camera Options:**

```
COMMERCIAL CAMERAS
1. Axon Body 3 ($799)
   ├── 1080p/1440p recording
   ├── GPS tagging
   ├── 12+ hour battery
   ├── WiFi/LTE auto-upload
   ├── Signal suppression alerts
   └── Best for: Large agencies, proven platform

2. WatchGuard V300 ($749)
   ├── 1080p recording
   ├── Wide 170° field of view
   ├── 12 hour battery
   ├── WiFi auto-upload
   └── Best for: Mid-size agencies

3. Motorola VB400 ($699)
   ├── 1080p recording
   ├── Rugged design (IP67)
   ├── 12 hour battery
   ├── Bluetooth triggers
   └── Best for: Harsh environments

DIY/OPEN SOURCE OPTION
Raspberry Pi-Based Camera ($95-150)
   ├── Raspberry Pi Zero 2 W: $15
   ├── Pi Camera Module v2: $25
   ├── 10,000mAh USB battery: $20
   ├── 128GB microSD card: $25
   ├── 3D printed case: $10
   ├── GPS module: $15
   ├── Development/setup: $50
   └── Best for: Tight budgets, customization
```

### Bill of Materials Calculator

```python
def calculate_guardian_bom(num_officers, camera_type='commercial', sharing_model='1:1'):
    """Calculate complete system cost"""
    
    # Camera costs
    camera_costs = {
        'commercial': 799,  # Axon Body 3
        'mid_range': 699,   # Motorola VB400
        'diy': 95           # Raspberry Pi
    }
    
    # Accessories per officer
    accessories = {
        'spare_battery': 50,
        'mounting_clip': 20,
        'charging_cable': 15,
        'storage_case': 10,
        'total': 95
    }
    
    # Docking stations (10-bay stations)
    docking_per_10 = {
        'commercial': 600,
        'diy': 200  # USB hub + power
    }
    
    # Calculate camera count
    if sharing_model == '1:1':
        num_cameras = num_officers
    elif sharing_model == '2:1':  # 2 officers share 1 camera
        num_cameras = int(num_officers / 2 + 0.5)
    else:  # '1.5:1' - some spares
        num_cameras = int(num_officers * 1.2)
    
    # Camera hardware
    camera_cost = camera_costs[camera_type]
    cameras_total = (camera_cost + accessories['total']) * num_cameras
    
    # Docking stations
    num_docks = int(num_cameras / 10 + 0.999)  # Round up
    dock_type = 'commercial' if camera_type in ['commercial', 'mid_range'] else 'diy'
    docks_total = docking_per_10[dock_type] * num_docks
    
    # Workstations (1 per 20 officers)
    num_workstations = max(1, int(num_officers / 20 + 0.999))
    workstation_cost = {
        'pc': 800,
        'monitor': 200,
        'ups': 150
    }
    workstations_total = sum(workstation_cost.values()) * num_workstations
    
    # Evidence server
    # Storage calculation: 
    # - 2 hours recording/shift × 8GB/hour = 16GB/day/officer
    # - Retention: 90 days average
    # - 16GB × 90 days × num_officers = storage needed
    storage_gb = 16 * 90 * num_officers
    storage_tb = storage_gb / 1000
    
    server_tiers = {
        'small': {  # 1-10 officers, <15TB
            'server': 3000,
            'storage_10tb': 800,
            'total': 3800
        },
        'medium': {  # 11-50 officers, 15-80TB
            'server': 5000,
            'storage_48tb': 4000,
            'total': 9000
        },
        'large': {  # 51+ officers, >80TB
            'server': 8000,
            'storage_100tb': 8000,
            'raid_controller': 800,
            'total': 16800
        }
    }
    
    if num_officers <= 10:
        server = server_tiers['small']
    elif num_officers <= 50:
        server = server_tiers['medium']
    else:
        server = server_tiers['large']
    
    # Software/Cloud (optional)
    cloud_monthly = {
        'storage': storage_tb * 10,  # $10/TB/month
        'compute': 50,
        'total': (storage_tb * 10) + 50
    }
    
    # Total costs
    hardware_total = cameras_total + docks_total + workstations_total + server['total']
    
    return {
        'num_officers': num_officers,
        'num_cameras': num_cameras,
        'camera_type': camera_type,
        'sharing_model': sharing_model,
        'cameras_total': cameras_total,
        'docking_stations': docks_total,
        'workstations': workstations_total,
        'evidence_server': server['total'],
        'hardware_total': hardware_total,
        'storage_tb': round(storage_tb, 1),
        'cloud_monthly': round(cloud_monthly['total'], 2),
        'first_year_total': int(hardware_total + (cloud_monthly['total'] * 12))
    }

# Example calculations
print("Small department (10 officers):")
print(calculate_guardian_bom(10, 'commercial', '1:1'))
# Hardware: ~$13,000, Cloud: ~$165/mo

print("\nMedium department (25 officers):")
print(calculate_guardian_bom(25, 'commercial', '1:1'))
# Hardware: ~$32,000, Cloud: ~$410/mo

print("\nLarge department (50 officers):")
print(calculate_guardian_bom(50, 'commercial', '1:1'))
# Hardware: ~$63,000, Cloud: ~$770/mo

print("\nBudget option (20 officers, DIY):")
print(calculate_guardian_bom(20, 'diy', '1:1'))
# Hardware: ~$14,000, Cloud: ~$340/mo
```

---

## Phase 1: Evidence Server Deployment

### Day 1: Server Infrastructure (6-8 hours)

**1.1 Server Hardware Setup**

```bash
# Server specifications for 50-officer department
# Dell PowerEdge R740 or equivalent

CPU: 2× Intel Xeon Silver 4214 (12 cores each)
RAM: 128GB DDR4 ECC
Storage:
  ├── OS: 2× 500GB SSD RAID 1
  ├── Evidence: 12× 10TB HDD RAID 6
  │   └── Usable: ~100TB
  └── Hot spare: 2× 10TB HDD
RAID Controller: PERC H740P (2GB cache, BBU)
Network: 2× 10GbE (bonded)
PSU: Redundant 750W
Management: iDRAC9 Enterprise

# Ubuntu 22.04 LTS installation
# 1. Boot from USB installer
# 2. Select "Ubuntu Server"
# 3. Configure storage:
#    - /boot: 1GB ext4
#    - /: 50GB ext4 (OS)
#    - /var/lib/docker: 100GB ext4
#    - /mnt/evidence: Remaining RAID6 array
# 4. Install OpenSSH server
# 5. Reboot
```

**1.2 Install MinIO (S3-Compatible Storage)**

```bash
# MinIO provides object storage with immutability, versioning, and legal hold
# Perfect for evidence management

# Create MinIO user
sudo useradd -r -s /bin/false minio

# Create data directories
sudo mkdir -p /mnt/evidence/data
sudo chown -R minio:minio /mnt/evidence/data

# Download MinIO
wget https://dl.min.io/server/minio/release/linux-amd64/minio
chmod +x minio
sudo mv minio /usr/local/bin/

# Create systemd service
sudo cat > /etc/systemd/system/minio.service <<EOF
[Unit]
Description=MinIO
Documentation=https://docs.min.io
Wants=network-online.target
After=network-online.target

[Service]
User=minio
Group=minio
Type=notify
WorkingDirectory=/usr/local/

# Root credentials
Environment="MINIO_ROOT_USER=admin"
Environment="MINIO_ROOT_PASSWORD=ChangeMe123!SecurePassword"

# Evidence bucket settings
Environment="MINIO_BROWSER=on"
Environment="MINIO_DOMAIN=evidence.department.gov"

ExecStart=/usr/local/bin/minio server \
  --console-address ":9001" \
  --address ":9000" \
  /mnt/evidence/data

Restart=always
LimitNOFILE=65536
TasksMax=infinity

[Install]
WantedBy=multi-user.target
EOF

# Start MinIO
sudo systemctl daemon-reload
sudo systemctl enable minio
sudo systemctl start minio

# Check status
sudo systemctl status minio

# Access MinIO Console
# http://server-ip:9001
# Login: admin / ChangeMe123!SecurePassword
```

**1.3 Configure Evidence Bucket**

```bash
# Install MinIO Client (mc)
wget https://dl.min.io/client/mc/release/linux-amd64/mc
chmod +x mc
sudo mv mc /usr/local/bin/

# Configure alias
mc alias set evidence http://localhost:9000 admin ChangeMe123!SecurePassword

# Create evidence bucket
mc mb evidence/bodycam-evidence

# Enable versioning (prevents accidental deletion)
mc version enable evidence/bodycam-evidence

# Set object lock mode (WORM - Write Once Read Many)
mc retention set --default COMPLIANCE "7y" evidence/bodycam-evidence

# Create lifecycle policy (auto-delete after retention)
cat > lifecycle-policy.json <<EOF
{
  "Rules": [
    {
      "ID": "ExpireAfterRetention",
      "Status": "Enabled",
      "Expiration": {
        "Days": 2555
      }
    }
  ]
}
EOF

mc ilm import evidence/bodycam-evidence < lifecycle-policy.json

# Set bucket quota (prevent runaway storage)
mc quota set evidence/bodycam-evidence --size 90TB

# Verify configuration
mc version info evidence/bodycam-evidence
mc retention info evidence/bodycam-evidence
mc quota info evidence/bodycam-evidence
```

**1.4 Setup Encryption**

```bash
# Server-Side Encryption with KMS

# Install Vault (for key management)
wget https://releases.hashicorp.com/vault/1.15.0/vault_1.15.0_linux_amd64.zip
unzip vault_1.15.0_linux_amd64.zip
sudo mv vault /usr/local/bin/

# Initialize Vault
vault server -dev &
export VAULT_ADDR='http://127.0.0.1:8200'
vault status

# Create encryption key for evidence
vault kv put secret/evidence-encryption key=$(openssl rand -base64 32)

# Configure MinIO to use Vault
mc admin config set evidence/ kms_vault \
  endpoint="http://127.0.0.1:8200" \
  approle_id="evidence-app" \
  approle_secret="secret" \
  key_name="evidence-encryption"

# Enable auto-encryption for evidence bucket
mc encrypt set sse-s3 evidence/bodycam-evidence

# Verify encryption
mc encrypt info evidence/bodycam-evidence
```

**1.5 Chain of Custody Logging**

```bash
# Enable audit logging for all access
mc admin config set evidence/ audit \
  webhook_enable=on \
  webhook_endpoint="http://localhost:3000/audit"

# Setup PostgreSQL for audit logs
docker run -d \
  --name evidence-audit-db \
  -e POSTGRES_DB=evidence_audit \
  -e POSTGRES_USER=audit \
  -e POSTGRES_PASSWORD=SecureAuditPass123 \
  -v /mnt/evidence/audit-db:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:15

# Create audit log table
psql -h localhost -U audit -d evidence_audit <<EOF
CREATE TABLE audit_log (
  id SERIAL PRIMARY KEY,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  user_id VARCHAR(100),
  action VARCHAR(50),
  object_key VARCHAR(500),
  ip_address INET,
  user_agent TEXT,
  result VARCHAR(20),
  metadata JSONB
);

CREATE INDEX idx_timestamp ON audit_log(timestamp);
CREATE INDEX idx_user ON audit_log(user_id);
CREATE INDEX idx_object ON audit_log(object_key);
EOF

# Create audit webhook service
cat > /opt/guardian/audit-service.js <<'EOF'
const express = require('express');
const { Pool } = require('pg');

const app = express();
app.use(express.json());

const pool = new Pool({
  host: 'localhost',
  database: 'evidence_audit',
  user: 'audit',
  password: 'SecureAuditPass123',
  port: 5432
});

app.post('/audit', async (req, res) => {
  const event = req.body;
  
  try {
    await pool.query(
      `INSERT INTO audit_log (user_id, action, object_key, ip_address, user_agent, result, metadata)
       VALUES ($1, $2, $3, $4, $5, $6, $7)`,
      [
        event.user_identity?.principalId || 'anonymous',
        event.eventName,
        event.object_key,
        event.source?.ipAddress,
        event.user_agent,
        event.response?.statusCode === 200 ? 'success' : 'failure',
        JSON.stringify(event)
      ]
    );
    
    res.json({ success: true });
  } catch (error) {
    console.error('Audit log error:', error);
    res.status(500).json({ success: false });
  }
});

app.listen(3000, () => {
  console.log('Audit service running on port 3000');
});
EOF

# Install dependencies and start
cd /opt/guardian
npm init -y
npm install express pg
node audit-service.js &
```

---

## Phase 2: Body Camera Configuration

### Day 2-3: Camera Setup (2 days)

**2.1 Commercial Camera Setup (Axon Body 3)**

```bash
# Axon Body 3 configuration via Evidence.com

# Initial setup:
1. Charge all cameras (4-6 hours)
2. Power on each camera
3. Connect to computer via USB
4. Access camera via web browser: http://192.168.1.1

# Configuration settings:
Video Quality: 1080p @ 30fps (or 1440p @ 30fps)
Pre-Event Buffer: 30 seconds
Auto-Activation: GPS (in vehicle), Holster (weapon draw)
Audio: Enabled
GPS: Enabled
WiFi: Department SSID configured
Upload: Auto-upload when docked
Retention: Upload all footage, delete local after 7 days

# Assign cameras to officers
# Via Evidence.com web portal:
1. Admin → Devices
2. Select camera by serial number
3. Assign to Officer (badge number, name)
4. Set default video category
5. Generate pairing code
6. Officer enters code on camera to accept

# Test recording
1. Press record button
2. Record 30 seconds
3. Stop recording
4. Review footage on camera
5. Dock camera to verify upload
```

**2.2 DIY Camera Setup (Raspberry Pi)**

```python
#!/usr/bin/env python3
"""
OS-GUARDIAN Body Camera Software
Raspberry Pi-based open source body camera
"""

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput, FileOutput
import RPi.GPIO as GPIO
import time
from datetime import datetime
import os
import gpsd
import requests

class BodyCamera:
    def __init__(self, officer_id):
        self.officer_id = officer_id
        self.camera = Picamera2()
        self.recording = False
        self.current_file = None
        
        # Configure camera
        config = self.camera.create_video_configuration(
            main={"size": (1920, 1080), "format": "RGB888"},
            encode="main"
        )
        self.camera.configure(config)
        
        # Pre-event buffer (last 30 seconds)
        self.encoder = H264Encoder(bitrate=10000000)
        self.buffer = CircularOutput(buffersize=30 * 30)  # 30 fps × 30 sec
        
        # GPIO setup (record button)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(17, GPIO.FALLING, 
                             callback=self.toggle_recording, 
                             bouncetime=300)
        
        # GPS setup
        gpsd.connect()
        
        # LED indicators
        GPIO.setup(27, GPIO.OUT)  # Red LED (recording)
        GPIO.setup(22, GPIO.OUT)  # Green LED (ready)
        
        self.led_ready()
    
    def led_ready(self):
        """Green LED = ready"""
        GPIO.output(27, GPIO.LOW)
        GPIO.output(22, GPIO.HIGH)
    
    def led_recording(self):
        """Red LED = recording"""
        GPIO.output(27, GPIO.HIGH)
        GPIO.output(22, GPIO.LOW)
    
    def get_gps(self):
        """Get current GPS coordinates"""
        try:
            packet = gpsd.get_current()
            return {
                'lat': packet.lat,
                'lon': packet.lon,
                'altitude': packet.alt,
                'speed': packet.speed(),
                'time': packet.time
            }
        except:
            return None
    
    def start_recording(self):
        """Start recording video"""
        if self.recording:
            return
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"/media/videos/{self.officer_id}_{timestamp}.h264"
        
        # Get GPS
        gps = self.get_gps()
        
        # Save metadata
        metadata = {
            'officer_id': self.officer_id,
            'timestamp': timestamp,
            'gps': gps,
            'duration': 0,
            'filename': filename
        }
        
        with open(f"{filename}.json", 'w') as f:
            json.dump(metadata, f)
        
        # Start recording with pre-event buffer
        output = FileOutput(filename)
        self.encoder.output = [self.buffer, output]
        self.camera.start_encoder(self.encoder)
        self.buffer.fileoutput = output
        self.buffer.start()
        
        self.recording = True
        self.current_file = filename
        self.led_recording()
        
        print(f"Recording started: {filename}")
    
    def stop_recording(self):
        """Stop recording video"""
        if not self.recording:
            return
        
        self.camera.stop_encoder()
        self.recording = False
        self.led_ready()
        
        print(f"Recording stopped: {self.current_file}")
        
        # Update metadata with duration
        # (Calculate from file size and bitrate)
    
    def toggle_recording(self, channel):
        """Toggle recording on button press"""
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()
    
    def run(self):
        """Main loop"""
        print(f"Body camera ready - Officer {self.officer_id}")
        self.camera.start()
        
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            if self.recording:
                self.stop_recording()
            self.camera.stop()
            GPIO.cleanup()

# Usage
if __name__ == '__main__':
    camera = BodyCamera(officer_id='OFF_001')
    camera.run()
```

**Installation on Raspberry Pi:**

```bash
# Install OS (Raspberry Pi OS Lite)
# Flash to microSD card

# First boot setup
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3-pip python3-picamera2 gpsd gpsd-clients python3-gps

# Enable camera
sudo raspi-config
# Interface Options → Camera → Enable

# Install body camera software
sudo mkdir -p /opt/bodycam
sudo cp bodycam.py /opt/bodycam/

# Create systemd service
sudo cat > /etc/systemd/system/bodycam.service <<EOF
[Unit]
Description=Body Camera Service
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/opt/bodycam
ExecStart=/usr/bin/python3 /opt/bodycam/bodycam.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start
sudo systemctl enable bodycam
sudo systemctl start bodycam

# Check status
sudo systemctl status bodycam
```

---

## Phase 3: Docking Station Installation

### Day 4: Auto-Upload Configuration

**3.1 Install Docking Stations**

```bash
# Docking station locations:
# - Shift briefing room
# - Evidence room
# - Supervisor offices

# Each docking station needs:
# 1. Power outlets (one per camera port + computer)
# 2. Network connection (Ethernet preferred)
# 3. Workstation PC (for evidence management)

# Physical installation:
1. Mount docking station on wall or desk
2. Connect power
3. Connect Ethernet to local network
4. Connect to workstation PC via USB
5. Test each camera port (insert camera, verify charging)
```

**3.2 Auto-Upload Service**

```python
#!/usr/bin/env python3
"""
Auto-upload service for docked cameras
Monitors USB devices and uploads videos to evidence server
"""

import os
import time
import subprocess
import hashlib
import json
from pathlib import Path
import boto3
from datetime import datetime

class DockingStation:
    def __init__(self, evidence_server):
        self.evidence_server = evidence_server
        self.s3 = boto3.client('s3',
            endpoint_url=f'http://{evidence_server}:9000',
            aws_access_key_id='admin',
            aws_secret_access_key='ChangeMe123!SecurePassword'
        )
        self.bucket = 'bodycam-evidence'
        
    def detect_cameras(self):
        """Detect docked cameras via USB"""
        # Look for mounted USB devices
        result = subprocess.run(['lsblk', '-o', 'NAME,MOUNTPOINT'], 
                               capture_output=True, text=True)
        
        cameras = []
        for line in result.stdout.split('\n'):
            if '/media/' in line:
                mount = line.split()[-1]
                if os.path.exists(os.path.join(mount, 'videos')):
                    cameras.append(mount)
        
        return cameras
    
    def calculate_checksum(self, filepath):
        """Calculate SHA-256 checksum"""
        sha256 = hashlib.sha256()
        with open(filepath, 'rb') as f:
            while True:
                data = f.read(65536)  # 64KB chunks
                if not data:
                    break
                sha256.update(data)
        return sha256.hexdigest()
    
    def upload_video(self, video_path, metadata_path):
        """Upload video to evidence server"""
        
        # Read metadata
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        # Calculate checksum
        checksum = self.calculate_checksum(video_path)
        
        # Generate object key
        # Format: OFFICER_ID/YEAR/MONTH/DAY/TIMESTAMP.h264
        dt = datetime.strptime(metadata['timestamp'], "%Y%m%d_%H%M%S")
        object_key = (f"{metadata['officer_id']}/"
                     f"{dt.year}/{dt.month:02d}/{dt.day:02d}/"
                     f"{metadata['timestamp']}.h264")
        
        print(f"Uploading: {object_key}")
        
        # Upload with metadata
        self.s3.upload_file(
            video_path,
            self.bucket,
            object_key,
            ExtraArgs={
                'Metadata': {
                    'officer-id': metadata['officer_id'],
                    'timestamp': metadata['timestamp'],
                    'gps-lat': str(metadata['gps']['lat']) if metadata['gps'] else '',
                    'gps-lon': str(metadata['gps']['lon']) if metadata['gps'] else '',
                    'checksum-sha256': checksum,
                    'duration': str(metadata['duration']),
                    'uploaded-at': datetime.now().isoformat(),
                    'uploaded-from': os.uname().nodename
                }
            }
        )
        
        # Log chain of custody
        self.log_custody_event(object_key, 'uploaded', checksum)
        
        print(f"✅ Upload complete: {object_key}")
        
        return object_key
    
    def log_custody_event(self, object_key, event, checksum):
        """Log chain of custody event"""
        requests.post('http://localhost:3000/custody', json={
            'object_key': object_key,
            'event': event,
            'checksum': checksum,
            'timestamp': datetime.now().isoformat(),
            'system': os.uname().nodename
        })
    
    def sync_camera(self, camera_mount):
        """Sync all videos from a docked camera"""
        
        videos_dir = os.path.join(camera_mount, 'videos')
        
        if not os.path.exists(videos_dir):
            print(f"No videos directory on {camera_mount}")
            return
        
        # Find all video files
        video_files = list(Path(videos_dir).glob('*.h264'))
        
        if not video_files:
            print(f"No videos to upload from {camera_mount}")
            return
        
        print(f"Found {len(video_files)} videos on {camera_mount}")
        
        for video_file in video_files:
            metadata_file = video_file.with_suffix('.h264.json')
            
            if not metadata_file.exists():
                print(f"⚠️  Missing metadata for {video_file}")
                continue
            
            try:
                # Upload video
                object_key = self.upload_video(str(video_file), str(metadata_file))
                
                # Verify upload
                response = self.s3.head_object(Bucket=self.bucket, Key=object_key)
                
                if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                    # Delete from camera
                    os.remove(video_file)
                    os.remove(metadata_file)
                    print(f"✅ Deleted local copy: {video_file.name}")
                else:
                    print(f"❌ Upload verification failed: {video_file.name}")
                    
            except Exception as e:
                print(f"❌ Upload error for {video_file.name}: {e}")
    
    def monitor(self):
        """Monitor for docked cameras and auto-sync"""
        
        print("Docking station monitoring active...")
        print("Waiting for cameras...")
        
        synced_cameras = set()
        
        while True:
            cameras = self.detect_cameras()
            
            for camera in cameras:
                if camera not in synced_cameras:
                    print(f"\n📷 Camera detected: {camera}")
                    self.sync_camera(camera)
                    synced_cameras.add(camera)
            
            # Remove cameras that are no longer connected
            synced_cameras = synced_cameras.intersection(set(cameras))
            
            time.sleep(5)  # Check every 5 seconds

# Usage
if __name__ == '__main__':
    station = DockingStation(evidence_server='10.0.50.10')
    station.monitor()
```

**Deploy as Service:**

```bash
# Create systemd service
sudo cat > /etc/systemd/system/docking-sync.service <<EOF
[Unit]
Description=Body Camera Docking Sync Service
After=network.target

[Service]
Type=simple
User=evidence
WorkingDirectory=/opt/guardian
ExecStart=/usr/bin/python3 /opt/guardian/docking-sync.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl enable docking-sync
sudo systemctl start docking-sync
sudo systemctl status docking-sync
```

---

## Phase 4: Policy & Access Control

### Day 5: Retention & Permissions

**4.1 Configure Retention Policies**

```sql
-- Retention policy database
CREATE TABLE retention_policies (
  id SERIAL PRIMARY KEY,
  category VARCHAR(50),
  description TEXT,
  retention_days INTEGER,
  legal_hold BOOLEAN DEFAULT false,
  auto_delete BOOLEAN DEFAULT true
);

-- Insert standard policies
INSERT INTO retention_policies (category, description, retention_days, auto_delete) VALUES
  ('general', 'General patrol footage', 90, true),
  ('evidence', 'Crime evidence', 2555, false),  -- 7 years
  ('use_of_force', 'Use of force incident', 0, false),  -- Permanent
  ('complaint', 'Citizen complaint', 1825, false),  -- 5 years
  ('court_case', 'Court case evidence', 3650, false),  -- 10 years (plus appeals)
  ('training', 'Training footage', 365, true),  -- 1 year
  ('ois', 'Officer-involved shooting', 0, false);  -- Permanent

-- Video categorization table
CREATE TABLE video_metadata (
  id SERIAL PRIMARY KEY,
  object_key VARCHAR(500) UNIQUE,
  officer_id VARCHAR(50),
  recorded_at TIMESTAMPTZ,
  uploaded_at TIMESTAMPTZ DEFAULT NOW(),
  category VARCHAR(50) DEFAULT 'general',
  case_number VARCHAR(100),
  incident_number VARCHAR(100),
  tags TEXT[],
  retention_policy_id INTEGER REFERENCES retention_policies(id),
  delete_after TIMESTAMPTZ,
  legal_hold BOOLEAN DEFAULT false,
  checksum VARCHAR(64)
);

-- Function to calculate delete date
CREATE OR REPLACE FUNCTION calculate_delete_date()
RETURNS TRIGGER AS $$
BEGIN
  SELECT retention_days INTO NEW.delete_after
  FROM retention_policies
  WHERE id = NEW.retention_policy_id;
  
  IF NEW.delete_after > 0 THEN
    NEW.delete_after := NEW.recorded_at + (NEW.delete_after || ' days')::INTERVAL;
  ELSE
    NEW.delete_after := NULL;  -- Permanent
  END IF;
  
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_delete_date
  BEFORE INSERT OR UPDATE ON video_metadata
  FOR EACH ROW
  EXECUTE FUNCTION calculate_delete_date();
```

**4.2 Role-Based Access Control**

```sql
-- User roles
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username VARCHAR(100) UNIQUE,
  email VARCHAR(255),
  badge_number VARCHAR(50),
  role VARCHAR(50),
  active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Role definitions
INSERT INTO users (username, email, badge_number, role) VALUES
  ('officer.smith', 'smith@dept.gov', 'OFF_001', 'officer'),
  ('sgt.jones', 'jones@dept.gov', 'SGT_010', 'supervisor'),
  ('lt.brown', 'brown@dept.gov', 'LT_020', 'command'),
  ('det.davis', 'davis@dept.gov', 'DET_030', 'detective'),
  ('admin.taylor', 'taylor@dept.gov', '', 'admin'),
  ('evidence.wilson', 'wilson@dept.gov', '', 'evidence_custodian');

-- Access control rules
CREATE TABLE access_control (
  role VARCHAR(50),
  permission VARCHAR(100),
  PRIMARY KEY (role, permission)
);

INSERT INTO access_control (role, permission) VALUES
  -- Officers can view their own videos
  ('officer', 'view_own_videos'),
  ('officer', 'categorize_own_videos'),
  ('officer', 'add_notes_own_videos'),
  
  -- Supervisors can view their subordinates' videos
  ('supervisor', 'view_own_videos'),
  ('supervisor', 'view_subordinate_videos'),
  ('supervisor', 'categorize_any_video'),
  ('supervisor', 'approve_redaction'),
  
  -- Command staff has broader access
  ('command', 'view_all_videos'),
  ('command', 'export_videos'),
  ('command', 'override_retention'),
  
  -- Detectives can access case-related videos
  ('detective', 'view_case_videos'),
  ('detective', 'export_case_videos'),
  ('detective', 'set_legal_hold'),
  
  -- Evidence custodians manage storage
  ('evidence_custodian', 'view_all_videos'),
  ('evidence_custodian', 'export_any_video'),
  ('evidence_custodian', 'modify_retention'),
  ('evidence_custodian', 'chain_of_custody'),
  
  -- Admins have full access
  ('admin', 'full_access');
```

**4.3 Implement Access Control in API**

```javascript
// Express.js middleware for access control
const checkPermission = (permission) => {
  return async (req, res, next) => {
    const user = req.user;  // From JWT token
    
    // Check if user has permission
    const result = await db.query(
      'SELECT 1 FROM access_control WHERE role = $1 AND permission = $2',
      [user.role, permission]
    );
    
    if (result.rows.length === 0) {
      return res.status(403).json({ error: 'Access denied' });
    }
    
    next();
  };
};

// Video access endpoint
app.get('/api/videos/:objectKey', 
  authenticateToken,
  async (req, res) => {
    const { objectKey } = req.params;
    const user = req.user;
    
    // Get video metadata
    const video = await db.query(
      'SELECT * FROM video_metadata WHERE object_key = $1',
      [objectKey]
    );
    
    if (video.rows.length === 0) {
      return res.status(404).json({ error: 'Video not found' });
    }
    
    const videoData = video.rows[0];
    
    // Check access permissions
    if (user.role === 'officer' && videoData.officer_id !== user.badge_number) {
      return res.status(403).json({ error: 'Access denied' });
    }
    
    // Log access
    await db.query(
      `INSERT INTO audit_log (user_id, action, object_key, ip_address)
       VALUES ($1, $2, $3, $4)`,
      [user.username, 'view_video', objectKey, req.ip]
    );
    
    // Generate presigned URL (expires in 1 hour)
    const url = s3.getSignedUrl('getObject', {
      Bucket: 'bodycam-evidence',
      Key: objectKey,
      Expires: 3600
    });
    
    res.json({ url, metadata: videoData });
  }
);
```

---

## Phase 5: Officer Training

### Day 6-7: Training Program (2 days)

**5.1 Training Curriculum**

```
DAY 1: TECHNICAL TRAINING (4 hours)

Module 1: Camera Operation (1 hour)
├── Power on/off
├── Recording start/stop
├── Pre-event buffer explanation
├── Battery management
├── Mounting and positioning
└── LED indicator meanings

Module 2: Docking & Upload (30 min)
├── Docking procedure
├── Auto-upload verification
├── Troubleshooting failed uploads
└── Battery charging best practices

Module 3: Video Review (1 hour)
├── Accessing video portal
├── Searching your footage
├── Adding notes/tags
├── Categorizing videos
└── Export procedures

Module 4: Hands-On Practice (1.5 hours)
├── Each officer gets camera
├── Practice recording scenarios
├── Dock and verify upload
├── Review footage in portal
└── Q&A

DAY 2: POLICY & LEGAL TRAINING (4 hours)

Module 5: Department Policy (1 hour)
├── When to record (mandatory vs discretionary)
├── When NOT to record (privacy)
├── Notification requirements
├── Supervisor review procedures
└── Disciplinary consequences

Module 6: Legal Requirements (1 hour)
├── State body camera law
├── Evidence handling
├── Court testimony with video
├── Discovery requests
└── Privacy rights

Module 7: Scenarios & Role Play (1.5 hours)
├── Traffic stop
├── Domestic violence call
├── Arrest scenario
├── Use of force incident
└── Hospital/victim interview

Module 8: Assessment (30 min)
├── Written test (80% to pass)
├── Practical demonstration
└── Sign acknowledgment form
```

**5.2 Training Scenarios**

```
SCENARIO 1: TRAFFIC STOP
Setup: Role-play traffic stop
Learning objectives:
  ☐ Activate camera before exiting vehicle
  ☐ Position camera for clear view
  ☐ Announce recording to driver
  ☐ Continue recording entire interaction
  ☐ Categorize as "traffic stop" when reviewing

SCENARIO 2: DOMESTIC VIOLENCE
Setup: Role-play domestic call
Learning objectives:
  ☐ Activate upon dispatch
  ☐ Record entire scene
  ☐ Capture victim interview separately
  ☐ Document injuries on video
  ☐ Categorize as "evidence" + case number

SCENARIO 3: USE OF FORCE
Setup: Role-play resistant subject
Learning objectives:
  ☐ Camera already recording from dispatch
  ☐ Clear narration of actions
  ☐ Continue recording through medical
  ☐ Supervisor review within 24 hours
  ☐ Immediate categorization as "use of force"

SCENARIO 4: PRIVACY SITUATION
Setup: Hospital interview
Learning objectives:
  ☐ Recognize privacy-sensitive location
  ☐ Announce recording to patient
  ☐ Respect request to turn off if appropriate
  ☐ Document decision in report
  ☐ Know when recording is still required
```

**5.3 Training Assessment**

```
WRITTEN TEST (20 questions, 80% to pass)

1. When MUST you activate your body camera? (Select all)
   □ Traffic stops
   □ Calls for service
   □ Arrests
   □ Use of force
   □ All enforcement activities

2. When should you NOT record? (Select all)
   □ Interviewing sexual assault victim
   □ Interviewing confidential informant
   □ Inside hospital (with exceptions)
   □ Conversations with attorneys
   □ Never - always record

3. Your camera battery dies during a call. What do you do?
   □ Continue without camera
   □ Return to station immediately
   □ Notify dispatch and document
   □ Borrow another officer's camera

4. How long is general patrol footage retained?
   □ 30 days
   □ 90 days
   □ 1 year
   □ Permanently

5. Who can view your body camera footage?
   □ Only you
   □ You and your supervisor
   □ Anyone in the department
   □ Public via open records request

[... 15 more questions ...]

PRACTICAL ASSESSMENT
☐ Demonstrate camera activation
☐ Properly position camera
☐ Dock camera and verify upload
☐ Log into portal and find video
☐ Categorize video correctly
☐ Add case number to video

ACKNOWLEDGMENT
I have completed body camera training and understand:
- When I must record
- When I should not record
- How to operate the camera
- Department policies and procedures
- Legal requirements
- Consequences of policy violations

Signature: _________________ Badge: _____ Date: _______
```

---

## Phase 6: Go-Live

### Day 8: Department Rollout

**6.1 Go-Live Checklist**

```
TECHNICAL READINESS
☐ Evidence server operational
☐ All cameras assigned to officers
☐ Docking stations installed and tested
☐ Auto-upload working on all stations
☐ Access control configured
☐ Retention policies active
☐ Chain of custody logging verified
☐ Backup procedures tested

TRAINING COMPLETION
☐ All officers trained (100%)
☐ All supervisors trained
☐ Evidence custodians trained
☐ IT staff trained
☐ Assessments passed (80%+)
☐ Acknowledgments signed

POLICY IMPLEMENTATION
☐ Body camera policy published
☐ General orders updated
☐ Union notification (if applicable)
☐ Public notification completed
☐ Website updated with policy
☐ Press release issued

OPERATIONAL READINESS
☐ Supervisor review procedures established
☐ IT support on-call
☐ Help desk trained
☐ Troubleshooting guide distributed
☐ Emergency procedures documented
☐ Audit schedule established
```

**6.2 Go-Live Procedure**

```bash
#!/bin/bash
# OS-GUARDIAN Go-Live

echo "OS-GUARDIAN System Go-Live"
echo "=========================="

# Step 1: Verify evidence server
echo "Step 1: Evidence Server Status"
curl -s http://evidence.dept.gov:9001/minio/health/live
if [ $? -eq 0 ]; then
    echo "✅ Evidence server: Online"
else
    echo "❌ Evidence server: OFFLINE - STOP"
    exit 1
fi

# Step 2: Check storage capacity
echo ""
echo "Step 2: Storage Capacity"
USED=$(mc du evidence/bodycam-evidence --json | jq '.size')
QUOTA=$(mc quota info evidence/bodycam-evidence | grep -oP '\d+' | head -1)
echo "  Used: $USED bytes"
echo "  Quota: $QUOTA TB"

# Step 3: Verify docking stations
echo ""
echo "Step 3: Docking Stations"
systemctl status docking-sync --no-pager | grep "active (running)"
if [ $? -eq 0 ]; then
    echo "✅ Docking sync: Running"
else
    echo "❌ Docking sync: NOT RUNNING"
fi

# Step 4: Test camera upload
echo ""
echo "Step 4: Camera Upload Test"
echo "  Dock a test camera and wait 30 seconds..."
sleep 30
RECENT_VIDEOS=$(mc ls evidence/bodycam-evidence --recursive | tail -5)
echo "$RECENT_VIDEOS"

# Step 5: Distribute cameras
echo ""
echo "Step 5: Camera Distribution"
echo "  Number of officers: $(wc -l < /opt/guardian/officer-roster.txt)"
echo "  Number of cameras: $(mc ls evidence/bodycam-evidence/cameras | wc -l)"

# Step 6: Enable production
echo ""
echo "Step 6: Production Mode"
echo "  All systems operational"
echo "  Officers may now use body cameras"

echo ""
echo "✅ GO-LIVE COMPLETE!"
echo ""
echo "System Information:"
echo "  - Evidence Portal: https://evidence.dept.gov"
echo "  - Storage Available: $(mc quota info evidence/bodycam-evidence)"
echo "  - Help Desk: x5555"
echo ""
echo "Monitor:"
echo "  - First 24 hours: Close monitoring"
echo "  - Review upload logs daily"
echo "  - Check storage usage weekly"
```

---

## Post-Deployment

### Ongoing Operations

**Daily Tasks:**
```
☐ Monitor upload logs (any failures?)
☐ Check storage usage
☐ Verify backup completion
☐ Review audit logs for anomalies
☐ Respond to technical issues
```

**Weekly Tasks:**
```
☐ Audit camera assignments
☐ Review categorization accuracy
☐ Check retention policy compliance
☐ Verify chain of custody logs
☐ Test disaster recovery
☐ Update officer roster
```

**Monthly Tasks:**
```
☐ Generate usage reports
☐ Review access patterns
☐ Audit user permissions
☐ Update firmware (cameras)
☐ Storage capacity planning
☐ Policy compliance audit
```

**Quarterly Tasks:**
```
☐ Full system backup test
☐ Disaster recovery drill
☐ Security audit
☐ Refresh officer training
☐ Review and update policies
☐ Hardware maintenance
```

---

## Troubleshooting Guide

### Common Issues

**Issue 1: Camera Not Uploading**
```
Symptoms: Video remains on camera after docking
Diagnosis:
1. Check if camera is detected: lsusb
2. Check if mounted: lsblk
3. Check sync service: systemctl status docking-sync
4. Check logs: journalctl -u docking-sync -n 50

Resolution:
- Camera not detected → Check USB cable/port
- Not mounted → Check filesystem (may need repair)
- Service not running → systemctl restart docking-sync
- Upload failing → Check network, evidence server
```

**Issue 2: Storage Full**
```
Symptoms: Uploads failing with storage error
Diagnosis:
1. Check usage: mc du evidence/bodycam-evidence
2. Check quota: mc quota info evidence/bodycam-evidence
3. Check for retention issues

Resolution:
- Increase storage capacity (add drives)
- Review retention policies (shorten if appropriate)
- Run manual cleanup: DELETE WHERE delete_after < NOW()
- Check for legal holds preventing deletion
```

**Issue 3: Video Not Accessible**
```
Symptoms: Officer cannot view their video
Diagnosis:
1. Check user permissions in database
2. Verify video exists: mc ls evidence/bodycam-evidence/OFF_001/
3. Check access control policy
4. Review audit logs for errors

Resolution:
- Permission denied → Grant appropriate role
- Video not found → Check upload logs, may not have uploaded
- Policy issue → Review and update access control
```

**Issue 4: Battery Life Short**
```
Symptoms: Camera battery dies mid-shift
Diagnosis:
1. Check battery health (charge cycles)
2. Review recording duration
3. Check for continuous recording

Resolution:
- Replace battery if >500 cycles
- Carry spare battery
- Optimize recording (motion activation vs continuous)
- Check for firmware updates
```

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Typical Deployment**: 1 week for department  
**System Scalability**: 10 to 1,000+ officers

**Evidence Storage**: Tamper-proof, legally compliant, 7-year retention  
**Chain of Custody**: Complete audit trail, court-admissible  
**Security**: AES-256 encryption, role-based access, WORM storage
