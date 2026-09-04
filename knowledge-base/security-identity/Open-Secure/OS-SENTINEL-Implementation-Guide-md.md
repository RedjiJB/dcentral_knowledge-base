---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: d6004578-38ec-43db-9e4b-bae1d5de93ad
original_filename: OS-SENTINEL_Implementation_Guide.md
created_at: 2026-03-04T20:34:07.864699+00:00
content_hash: c4164341ff39topic: timeout-lighting-login
---

# OS-SENTINEL Implementation Guide
## Video Surveillance & AI Analytics System Deployment

**Document Type**: Implementation Guide  
**Version**: 1.0  
**Date**: December 2024  
**Classification**: Technical Documentation  
**Audience**: Security Integrators, IT Teams, Video System Installers

---

## Executive Summary

**Deployment Timeline**: 2-4 weeks (10-100 cameras)  
**Team Required**: 3-4 technicians (Electrician + Low Voltage + IT)  
**Cost Range**: $15,000-$100,000 (complete system)  
**Scalability**: 10 to 1,000+ cameras per site

### Phase Overview

| Phase | Duration | Team | Deliverable |
|-------|----------|------|-------------|
| Site Survey | 2-3 days | PM + Electrician | CAD drawings, cable plan |
| Infrastructure | 5-7 days | Electrician + LV Tech | PoE switches, cabling complete |
| Camera Install | 5-10 days | 2-3 LV Techs | All cameras mounted |
| NVR Setup | 2-3 days | IT Specialist | Recording operational |
| AI Analytics | 2-3 days | IT Specialist | Detection models deployed |
| Testing | 2-3 days | Full team | System validated |
| Training | 1 day | Trainer + Users | Staff trained |
| Go-Live | 1 day | Full team | System operational |

---

## Pre-Deployment Planning

### Site Survey & Assessment

**Coverage Analysis Checklist:**
```
CRITICAL AREAS (High Priority)
☐ Perimeter/property line
☐ All entry/exit points (doors, gates)
☐ Parking lots/garages
☐ Loading docks/receiving areas
☐ Cash handling areas (if applicable)
☐ Server rooms/IT areas
☐ Restricted areas

MEDIUM PRIORITY AREAS
☐ Hallways and corridors
☐ Stairwells and elevators
☐ Common areas/lobbies
☐ Outdoor walkways
☐ Storage areas

OPTIONAL AREAS
☐ Office spaces
☐ Break rooms
☐ Restrooms (exterior only)
☐ Roof access points

CAMERA REQUIREMENTS PER LOCATION
☐ Field of view needed (wide, medium, narrow)
☐ Resolution requirements (identify vs detect)
☐ Lighting conditions (day, night, low-light)
☐ Environmental factors (weather, temperature)
☐ Vandal resistance needed?
☐ PTZ functionality required?
☐ Audio recording needed?
```

**Infrastructure Assessment:**
```
POWER
☐ PoE switch locations identified
☐ PoE budget calculated (cameras × 30W)
☐ UPS capacity verified
☐ Circuit breaker capacity checked

NETWORK
☐ Bandwidth calculated (cameras × bitrate)
☐ Network drops available or needed
☐ VLAN segmentation planned
☐ Internet connectivity (for remote viewing)

MOUNTING
☐ Mounting surfaces identified (concrete, drywall, metal)
☐ Conduit pathways planned
☐ Above-ceiling access verified
☐ Outdoor weather protection planned

STORAGE
☐ Recording retention requirement (days)
☐ Storage capacity calculated
☐ RAID configuration planned
☐ Backup procedures defined
```

### Camera Selection Guide

**By Use Case:**
```
GENERAL SURVEILLANCE (Lobby, Hallways)
├── Type: Fixed dome or turret
├── Resolution: 2MP (1080p)
├── Lens: 2.8mm or 3.6mm (wide angle)
├── Features: WDR, IR 30m
├── Cost: $80-150
└── Example: Hikvision DS-2CD2123G2-I

PERIMETER/PARKING (Wide area coverage)
├── Type: Bullet or turret
├── Resolution: 4MP (2K)
├── Lens: 2.8mm-12mm varifocal
├── Features: IR 60m, weatherproof IP67
├── Cost: $120-200
└── Example: Dahua IPC-HFW3441T-ZS

LICENSE PLATE RECOGNITION (LPR)
├── Type: Specialized LPR camera
├── Resolution: 2MP minimum
├── Lens: 5mm-50mm (narrow)
├── Features: High shutter speed, IR illuminator
├── Cost: $180-400
└── Example: Hikvision DS-2CD4A26FWD-IZH/P

PTZ (Active monitoring, large areas)
├── Type: Pan-Tilt-Zoom dome
├── Resolution: 4MP-8MP
├── Lens: 25x-32x optical zoom
├── Features: Auto-tracking, presets, IR 150m
├── Cost: $600-1,200
└── Example: Dahua SD59432XA-HNR

FACIAL RECOGNITION (Entrances)
├── Type: Fixed box or turret
├── Resolution: 4MP minimum
├── Lens: 6mm-8mm (facial capture)
├── Features: Face detection, WDR
├── Cost: $200-400
└── Example: Hikvision DS-2CD2743G2-IZS
```

### Bill of Materials Calculator

```python
def calculate_sentinel_bom(num_cameras, system_type='standard'):
    """Calculate complete system cost"""
    
    # Camera costs by type
    camera_costs = {
        'basic': 120,      # 2MP fixed
        'standard': 150,   # 4MP varifocal
        'premium': 250,    # 4K or specialty
        'ptz': 800         # PTZ dome
    }
    
    # Infrastructure per 24 cameras
    infrastructure_per_24 = {
        'poe_switch': 400,
        'cabinet': 200,
        'ups': 250,
        'cables': 50
    }
    
    # Cabling per camera (average 150 feet)
    cable_per_camera = {
        'cat6_cable': 30,
        'conduit': 20,
        'labor': 50
    }
    
    # Server/NVR costs
    server_costs = {
        'small': {  # 1-24 cameras
            'description': 'Workstation + HDD',
            'hardware': 1500,
            'storage_4TB': 400
        },
        'medium': {  # 25-100 cameras
            'description': 'Entry server + RAID',
            'hardware': 3000,
            'storage_24TB': 2000,
            'gpu_analytics': 600
        },
        'large': {  # 100+ cameras
            'description': 'Enterprise server + GPU',
            'hardware': 5000,
            'storage_96TB': 8000,
            'gpu_rtx3090': 1500
        }
    }
    
    # Calculate camera costs
    if system_type == 'basic':
        camera_unit_cost = camera_costs['basic']
    elif system_type == 'premium':
        camera_unit_cost = camera_costs['premium']
    else:
        camera_unit_cost = camera_costs['standard']
    
    total_camera_cost = num_cameras * camera_unit_cost
    
    # Calculate infrastructure (switches, etc)
    num_switches = (num_cameras // 24) + 1
    infrastructure_cost = sum(infrastructure_per_24.values()) * num_switches
    
    # Calculate cabling
    cabling_cost = sum(cable_per_camera.values()) * num_cameras
    
    # Select server tier
    if num_cameras <= 24:
        server = server_costs['small']
        server_total = server['hardware'] + server['storage_4TB']
    elif num_cameras <= 100:
        server = server_costs['medium']
        server_total = server['hardware'] + server['storage_24TB'] + server['gpu_analytics']
    else:
        server = server_costs['large']
        server_total = server['hardware'] + server['storage_96TB'] + server['gpu_rtx3090']
    
    # Total system cost
    total = total_camera_cost + infrastructure_cost + cabling_cost + server_total
    
    return {
        'num_cameras': num_cameras,
        'camera_cost': total_camera_cost,
        'infrastructure': infrastructure_cost,
        'cabling': cabling_cost,
        'server_nvr': server_total,
        'subtotal': total,
        'installation_labor': int(total * 0.3),  # 30% labor
        'total_project': int(total * 1.3),
        'cost_per_camera': int(total * 1.3 / num_cameras)
    }

# Example calculations:
print("10 cameras (basic):")
print(calculate_sentinel_bom(10, 'basic'))
# Total: ~$9,500

print("\n24 cameras (standard):")
print(calculate_sentinel_bom(24, 'standard'))
# Total: ~$18,000

print("\n50 cameras (standard):")
print(calculate_sentinel_bom(50, 'standard'))
# Total: ~$35,000

print("\n100 cameras (premium):")
print(calculate_sentinel_bom(100, 'premium'))
# Total: ~$85,000
```

---

## Phase 1: Infrastructure Deployment

### Week 1: Network Infrastructure

**1.1 Install PoE Switches**

```bash
# Switch selection criteria
# - Port count: Plan for 20-25% growth
# - PoE budget: 30W per camera (802.3at)
# - Uplink: 10Gb for >24 cameras
# - Management: Managed switch required (VLAN, QoS)

# Recommended switches:
# - 24-port: TP-Link TL-SG3428MP ($400)
# - 48-port: Ubiquiti USW-Pro-48-PoE ($800)
# - Enterprise: Cisco CBS350-48P ($1,200)

# Installation procedure:
1. Mount switch in network cabinet/rack
2. Connect power (consider dual PSU for critical systems)
3. Connect UPS backup
4. Configure management IP
5. Create VLAN for cameras (VLAN 30)
6. Enable DHCP or assign static IPs
7. Configure QoS for video traffic
8. Document port mapping

# Switch configuration (example)
# Access via web UI or CLI

# VLAN configuration
interface range GigabitEthernet1/0/1-24
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
 spanning-tree bpduguard enable
 power inline auto

# QoS for video traffic
mls qos
class-map match-all VIDEO
 match dscp 34
policy-map VIDEO-POLICY
 class VIDEO
  priority percent 50
interface GigabitEthernet1/0/1-24
 service-policy output VIDEO-POLICY
```

**1.2 Cable Installation**

```
CABLE TYPES
├── Cat6 or Cat6a (recommended for PoE+)
├── Outdoor-rated for exterior runs
├── Shielded (STP) for high-EMI environments
└── Plenum-rated for above-ceiling runs

INSTALLATION STANDARDS
├── Maximum run length: 300 feet (90m)
├── Bend radius: 4× cable diameter minimum
├── Pull tension: <25 lbs for Cat6
├── Separation from power: 12" minimum
└── Testing: All 8 wires must test pass

CABLE ROUTES
1. Interior runs:
   ├── Above drop ceiling (most common)
   ├── Through walls (fish tape)
   ├── Surface mount with raceway
   └── Under raised floor

2. Exterior runs:
   ├── Underground conduit (PVC Schedule 40)
   ├── Aerial cable (messenger wire support)
   ├── Building exterior (EMT conduit)
   └── Weatherproof junction boxes

TERMINATION
├── Camera end: RJ45 connector or pigtail
├── Switch end: Punch down to patch panel
├── Label both ends clearly
├── Test with cable tester
└── Document in spreadsheet (CAM-ID, Cable-ID, Port)
```

**1.3 Power & UPS**

```bash
# Calculate power requirements
cameras=50
power_per_camera=30  # Watts (PoE+)
total_power=$((cameras * power_per_camera))  # 1,500W

# Add switches and NVR
switch_power=200  # Per 24-port switch
nvr_power=500
num_switches=$((cameras / 24 + 1))

total_system_power=$((total_power + (switch_power * num_switches) + nvr_power))
echo "Total system power: ${total_system_power}W"

# UPS sizing (runtime target: 2 hours)
# VA = Watts / Power Factor (0.8)
ups_va=$((total_system_power * 2 / 0.8))  # For 2-hour runtime
echo "UPS capacity needed: ${ups_va}VA"

# Recommended UPS models:
# - Small (1-24 cameras): APC Smart-UPS 1500VA
# - Medium (25-100 cameras): APC Smart-UPS 3000VA
# - Large (100+ cameras): APC Smart-UPS 5000VA or generator backup
```

---

## Phase 2: Camera Installation

### Week 2-3: Physical Installation

**2.1 Camera Mounting Procedure**

```
MOUNTING HEIGHTS
├── Perimeter: 10-15 feet (out of reach)
├── Parking lots: 15-25 feet (pole mount)
├── Interior hallways: 8-10 feet
├── Entrances (facial): 7-8 feet (face level)
└── PTZ: 20-40 feet (overview)

MOUNTING TYPES
1. Wall Mount
   ├── Drill pilot holes (concrete: 3/8" masonry bit)
   ├── Insert anchors (Tapcon or toggle bolts)
   ├── Attach bracket with lag bolts
   ├── Mount camera to bracket
   └── Adjust angle and tighten

2. Pole Mount
   ├── Use stainless steel band clamps
   ├── Weatherproof junction box on pole
   ├── Route cable through pole if possible
   └── Ground strap for lightning protection

3. Ceiling Mount
   ├── Locate ceiling joist or use backing plate
   ├── Drill through ceiling tile
   ├── Mount bracket to joist/plate
   └── Drop camera through tile opening

4. Soffit/Overhang Mount
   ├── Ideal for weather protection
   ├── Use junction box for cable entry
   └── Seal all penetrations

WEATHERPROOFING (Outdoor)
├── Use weatherproof junction boxes (NEMA 4X)
├── Seal all cable entries with silicone
├── Use drip loops on cables
├── Use sunshields for south/west facing cameras
└── Install lightning arrestors on exposed poles
```

**2.2 Camera Positioning & Aiming**

```
FIELD OF VIEW GUIDELINES
├── Identify: Can recognize faces (50-100 pixels/face)
├── Recognize: Can identify known person (200+ pixels/face)
├── Detect: Can see that person is there (25 pixels/face)
└── Monitor: General awareness (any resolution)

LENS SELECTION
├── 2.8mm: 103° horizontal (wide, up to 20ft)
├── 3.6mm: 87° horizontal (medium, up to 30ft)
├── 6mm: 54° horizontal (narrow, up to 50ft)
├── 12mm: 28° horizontal (telephoto, 100ft+)
└── Varifocal: Adjustable (e.g., 2.7-13.5mm)

CAMERA ANGLES
├── Entrance doors: 5-10° downward angle
├── Hallways: 15-20° downward (reduce glare)
├── Parking lots: 25-30° downward (vehicle plates)
├── Perimeter: 0-5° (straight ahead for distance)
└── Avoid: Pointing at lights, windows, or sky

AIMING PROCEDURE
1. Power camera via PoE
2. Use mobile app or laptop to view live feed
3. Adjust camera angle (pan/tilt adjustments)
4. Focus lens (if varifocal)
5. Walk through field of view
6. Verify coverage at day and night
7. Tighten all adjustment screws
8. Apply thread-lock to prevent loosening
```

**2.3 Camera Configuration**

```bash
# Initial camera setup via web interface
# Default IP: Usually 192.168.1.64 or DHCP

# Change default password immediately!
curl -u admin:admin http://camera-ip/cgi-bin/configManager.cgi \
  -d "action=setConfig&Modify.Password=NewSecurePass123!"

# Set static IP address
curl -u admin:NewSecurePass123 http://camera-ip/cgi-bin/configManager.cgi \
  -d "action=setConfig&Network.IPAddress=10.0.30.50&Network.SubnetMask=255.255.255.0&Network.DefaultGateway=10.0.30.1"

# Configure video encoding
curl -u admin:NewSecurePass123 http://camera-ip/cgi-bin/configManager.cgi \
  -d "action=setConfig&Encode.MainFormat=H.265&Encode.Resolution=1920x1080&Encode.FPS=30&Encode.Bitrate=4096"

# Enable ONVIF (for NVR compatibility)
curl -u admin:NewSecurePass123 http://camera-ip/cgi-bin/configManager.cgi \
  -d "action=setConfig&ONVIF.Enable=true"

# Set timezone and NTP
curl -u admin:NewSecurePass123 http://camera-ip/cgi-bin/configManager.cgi \
  -d "action=setConfig&Locales.TimeZone=America/New_York&NTP.Enable=true&NTP.Server=pool.ntp.org"

# Enable motion detection
curl -u admin:NewSecurePass123 http://camera-ip/cgi-bin/configManager.cgi \
  -d "action=setConfig&MotionDetect.Enable=true&MotionDetect.Level=3"

# Configure night vision (IR)
curl -u admin:NewSecurePass123 http://camera-ip/cgi-bin/configManager.cgi \
  -d "action=setConfig&Lighting.Mode=Auto&Lighting.IRCutFilter=Auto"
```

---

## Phase 3: NVR/VMS Deployment

### Week 3: Recording Server Setup

**3.1 Server Hardware Setup**

```bash
# Hardware specifications for 50-camera system
CPU: Intel Xeon E-2288G (8 cores) or AMD Ryzen 9 5950X
RAM: 64GB DDR4 ECC (for AI analytics)
Storage:
  ├── OS: 500GB NVMe SSD (RAID 1)
  ├── Recording: 48TB HDD (RAID 6)
  │   ├── 8× 8TB 7200RPM SATA drives
  │   └── Hardware RAID controller (LSI/Broadcom)
  └── Retention: 30 days @ 4Mbps avg = 38TB needed
GPU: NVIDIA RTX 3090 (for AI object detection)
Network: Dual 10GbE NIC (one for cameras, one for clients)
PSU: 850W 80+ Gold (redundant recommended)
Chassis: 4U rackmount server

# Ubuntu 22.04 LTS installation
# 1. Download Ubuntu Server ISO
# 2. Create bootable USB
# 3. Install with LVM partitioning:
#    - /boot: 1GB
#    - /: 100GB (OS + apps)
#    - /var/lib/docker: 100GB (containers)
#    - /mnt/recordings: Remaining (video storage)

# Post-install configuration
sudo apt update && sudo apt upgrade -y
sudo apt install -y ubuntu-drivers-common
sudo ubuntu-drivers autoinstall  # NVIDIA drivers

# Install Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# Install NVIDIA Container Toolkit (for GPU in Docker)
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo systemctl restart docker

# Verify GPU access in Docker
docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
```

**3.2 Deploy Shinobi NVR**

```bash
# Shinobi - Open Source NVR
# https://shinobi.video

# Create directory structure
mkdir -p ~/shinobi/{config,videos,streams,plugins}
cd ~/shinobi

# Create docker-compose.yml
cat > docker-compose.yml <<EOF
version: '3.8'

services:
  shinobi:
    image: shinobisystems/shinobi:latest
    container_name: shinobi
    hostname: shinobi
    ports:
      - "8080:8080"   # Web UI
      - "8443:8443"   # HTTPS
    volumes:
      - ./config:/config
      - ./videos:/opt/shinobi/videos
      - ./streams:/dev/shm/streams  # Temporary stream files
      - ./plugins:/opt/shinobi/plugins
    environment:
      - ADMIN_USER=admin@company.com
      - ADMIN_PASSWORD=ChangeMe123!
      - PLUGIN_KEYS={}
      - TIMEZONE=America/New_York
      - DB_HOST=mariadb
      - DB_USER=shinobi
      - DB_PASSWORD=shinobipass
      - DB_DATABASE=ccio
    depends_on:
      - mariadb
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  mariadb:
    image: mariadb:10.11
    container_name: shinobi-db
    environment:
      - MYSQL_ROOT_PASSWORD=rootpass
      - MYSQL_DATABASE=ccio
      - MYSQL_USER=shinobi
      - MYSQL_PASSWORD=shinobipass
    volumes:
      - mariadb-data:/var/lib/mysql
    restart: unless-stopped

volumes:
  mariadb-data:
    driver: local
EOF

# Start Shinobi
docker-compose up -d

# Wait for startup (2-3 minutes)
docker-compose logs -f shinobi

# Access web interface
# http://server-ip:8080
# Login: admin@company.com / ChangeMe123! (CHANGE IMMEDIATELY)
```

**3.3 Add Cameras to Shinobi**

```javascript
// Via Shinobi Web UI or API

// Add camera via API
const addCamera = async (cameraConfig) => {
  const response = await fetch('http://server-ip:8080/api/monitor/add', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer YOUR_API_KEY'
    },
    body: JSON.stringify({
      name: cameraConfig.name,
      type: 'h264',
      host: cameraConfig.ip,
      port: 554,
      path: '/cam/realmonitor?channel=1&subtype=0',  // RTSP path
      protocol: 'rtsp',
      username: 'admin',
      password: 'camera_password',
      mode: 'record',
      details: {
        detector: 'motion',
        detector_trigger: 1,
        detector_record: 1,
        detector_send_frames: 1
      }
    })
  });
  
  return response.json();
};

// Bulk add cameras
const cameras = [
  {name: 'Front Entrance', ip: '10.0.30.10'},
  {name: 'Parking Lot A', ip: '10.0.30.11'},
  {name: 'Rear Exit', ip: '10.0.30.12'},
  // ... 47 more cameras
];

for (const camera of cameras) {
  await addCamera(camera);
  console.log(`Added: ${camera.name}`);
}
```

**3.4 Configure Recording Settings**

```sql
-- Connect to MariaDB
docker exec -it shinobi-db mysql -u shinobi -pshinobipass ccio

-- Update recording settings for all monitors
UPDATE Monitors SET 
  details = JSON_SET(details,
    '$.recording_mode', 'continuous',        -- or 'motion'
    '$.video_codec', 'h265',                 -- H.265 for efficiency
    '$.video_resolution', '1920x1080',
    '$.video_fps', '30',
    '$.video_bitrate', '4096',               -- 4 Mbps
    '$.segment_duration', '300'              -- 5-minute segments
  );

-- Set retention policy (30 days)
UPDATE Monitors SET
  details = JSON_SET(details,
    '$.retention_days', '30',
    '$.auto_delete_enabled', true
  );

-- Enable motion detection
UPDATE Monitors SET
  details = JSON_SET(details,
    '$.motion_detection_enabled', true,
    '$.motion_sensitivity', '3',             -- 1-5 scale
    '$.motion_zones', JSON_ARRAY()           -- Full frame
  );
```

---

## Phase 4: AI Analytics Deployment

### Week 4: Computer Vision Setup

**4.1 Deploy YOLOv8 Object Detection**

```python
# Install dependencies
pip install ultralytics opencv-python numpy requests

# Create analytics service
cat > /opt/sentinel/analytics.py <<'EOF'
#!/usr/bin/env python3
"""
OS-SENTINEL AI Analytics Service
Real-time object detection using YOLOv8
"""

from ultralytics import YOLO
import cv2
import numpy as np
from datetime import datetime
import requests
import json
import threading
import queue

class SentinelAnalytics:
    def __init__(self, model_path='yolov8n.pt'):
        """Initialize YOLO model and detection settings"""
        self.model = YOLO(model_path)
        
        # Detection classes (COCO dataset)
        self.classes = {
            0: 'person',
            1: 'bicycle',
            2: 'car',
            3: 'motorcycle',
            5: 'bus',
            7: 'truck',
            15: 'cat',
            16: 'dog',
            24: 'backpack',
            26: 'handbag',
            28: 'suitcase'
        }
        
        # Detection zones per camera
        self.zones = {}
        
        # Event queue
        self.event_queue = queue.Queue()
        
    def add_detection_zone(self, camera_id, zone_name, polygon):
        """Add detection zone for a camera"""
        if camera_id not in self.zones:
            self.zones[camera_id] = []
        
        self.zones[camera_id].append({
            'name': zone_name,
            'polygon': np.array(polygon, dtype=np.int32)
        })
    
    def point_in_polygon(self, point, polygon):
        """Check if point is inside polygon"""
        return cv2.pointPolygonTest(polygon, point, False) >= 0
    
    def process_stream(self, camera_id, rtsp_url, fps=5):
        """Process camera stream for detections"""
        
        cap = cv2.VideoCapture(rtsp_url)
        frame_skip = int(cap.get(cv2.CAP_PROP_FPS) / fps)
        frame_count = 0
        
        print(f"Processing {camera_id}: {rtsp_url}")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print(f"Failed to read frame from {camera_id}")
                break
            
            frame_count += 1
            
            # Skip frames to reduce processing
            if frame_count % frame_skip != 0:
                continue
            
            # Run detection
            results = self.model(frame, classes=list(self.classes.keys()))
            
            # Process detections
            detections = []
            for detection in results[0].boxes:
                class_id = int(detection.cls[0])
                confidence = float(detection.conf[0])
                bbox = detection.xyxy[0].tolist()
                
                if confidence < 0.6:  # Confidence threshold
                    continue
                
                # Calculate center point
                center_x = int((bbox[0] + bbox[2]) / 2)
                center_y = int((bbox[1] + bbox[3]) / 2)
                center = (center_x, center_y)
                
                # Check if in detection zone
                in_zone = False
                zone_name = None
                
                if camera_id in self.zones:
                    for zone in self.zones[camera_id]:
                        if self.point_in_polygon(center, zone['polygon']):
                            in_zone = True
                            zone_name = zone['name']
                            break
                else:
                    in_zone = True  # No zones = full frame
                
                if in_zone:
                    detection_event = {
                        'camera_id': camera_id,
                        'timestamp': datetime.now().isoformat(),
                        'class': self.classes[class_id],
                        'confidence': confidence,
                        'bbox': bbox,
                        'center': center,
                        'zone': zone_name
                    }
                    
                    detections.append(detection_event)
            
            # Send detections to event handler
            if detections:
                self.event_queue.put({
                    'camera_id': camera_id,
                    'timestamp': datetime.now().isoformat(),
                    'detections': detections
                })
    
    def event_processor(self):
        """Process detection events"""
        while True:
            event = self.event_queue.get()
            
            # Send to OS-SENTINEL API
            try:
                response = requests.post(
                    'http://localhost:8080/api/v1/detections',
                    json=event,
                    timeout=5
                )
                
                if response.status_code == 200:
                    print(f"Event logged: {event['camera_id']} - {len(event['detections'])} detections")
                else:
                    print(f"Failed to log event: {response.status_code}")
                    
            except Exception as e:
                print(f"Error sending event: {e}")
    
    def run(self, cameras):
        """Start processing all cameras"""
        
        # Start event processor thread
        processor_thread = threading.Thread(target=self.event_processor)
        processor_thread.daemon = True
        processor_thread.start()
        
        # Start camera processing threads
        threads = []
        for camera in cameras:
            thread = threading.Thread(
                target=self.process_stream,
                args=(camera['id'], camera['rtsp_url'], 5)
            )
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        # Keep running
        for thread in threads:
            thread.join()

# Configuration
if __name__ == '__main__':
    analytics = SentinelAnalytics(model_path='yolov8n.pt')
    
    # Define detection zones (example)
    analytics.add_detection_zone(
        'CAM-001',
        'Restricted Area',
        [(100, 100), (500, 100), (500, 400), (100, 400)]  # Rectangle
    )
    
    # Camera list
    cameras = [
        {'id': 'CAM-001', 'rtsp_url': 'rtsp://admin:pass@10.0.30.10:554/cam/realmonitor'},
        {'id': 'CAM-002', 'rtsp_url': 'rtsp://admin:pass@10.0.30.11:554/cam/realmonitor'},
        # ... add all cameras
    ]
    
    # Start processing
    analytics.run(cameras)
EOF

chmod +x /opt/sentinel/analytics.py
```

**4.2 Create Systemd Service**

```bash
# Create systemd service for analytics
sudo cat > /etc/systemd/system/sentinel-analytics.service <<EOF
[Unit]
Description=OS-SENTINEL AI Analytics Service
After=network.target docker.service

[Service]
Type=simple
User=sentinel
WorkingDirectory=/opt/sentinel
ExecStart=/usr/bin/python3 /opt/sentinel/analytics.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable sentinel-analytics
sudo systemctl start sentinel-analytics

# Check status
sudo systemctl status sentinel-analytics
```

**4.3 Advanced Analytics Rules**

```python
# Loitering detection
class LoiteringDetector:
    def __init__(self, threshold_seconds=45):
        self.threshold = threshold_seconds
        self.tracked_objects = {}  # object_id: first_seen_time
    
    def check_loitering(self, camera_id, detections):
        """Detect if person has been in area too long"""
        current_time = datetime.now()
        
        for detection in detections:
            if detection['class'] != 'person':
                continue
            
            object_id = f"{camera_id}_{detection['center']}"
            
            if object_id not in self.tracked_objects:
                self.tracked_objects[object_id] = current_time
            else:
                duration = (current_time - self.tracked_objects[object_id]).seconds
                
                if duration > self.threshold:
                    # Loitering detected!
                    return {
                        'alert': 'loitering',
                        'camera_id': camera_id,
                        'duration': duration,
                        'location': detection['center']
                    }
        
        return None

# Perimeter breach detection
class PerimeterDetector:
    def __init__(self, perimeter_line):
        self.line = perimeter_line  # [(x1,y1), (x2,y2)]
        self.previous_positions = {}
    
    def check_breach(self, camera_id, detections):
        """Detect if object crossed perimeter line"""
        breaches = []
        
        for detection in detections:
            object_id = f"{camera_id}_{detection['class']}"
            current_pos = detection['center']
            
            if object_id in self.previous_positions:
                prev_pos = self.previous_positions[object_id]
                
                # Check if line segment crosses perimeter
                if self.line_intersection(prev_pos, current_pos, self.line[0], self.line[1]):
                    breaches.append({
                        'alert': 'perimeter_breach',
                        'camera_id': camera_id,
                        'object': detection['class'],
                        'confidence': detection['confidence']
                    })
            
            self.previous_positions[object_id] = current_pos
        
        return breaches
    
    def line_intersection(self, p1, p2, p3, p4):
        """Check if line segment p1-p2 intersects p3-p4"""
        def ccw(A, B, C):
            return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
        
        return ccw(p1,p3,p4) != ccw(p2,p3,p4) and ccw(p1,p2,p3) != ccw(p1,p2,p4)

# Crowd density detection
class CrowdDetector:
    def __init__(self, threshold_count=10):
        self.threshold = threshold_count
    
    def check_density(self, camera_id, detections):
        """Detect if too many people in area"""
        person_count = sum(1 for d in detections if d['class'] == 'person')
        
        if person_count >= self.threshold:
            return {
                'alert': 'crowd_detected',
                'camera_id': camera_id,
                'person_count': person_count,
                'threshold': self.threshold
            }
        
        return None
```

---

## Phase 5: Testing & Validation

### Week 4: System Testing

**5.1 Camera Functionality Tests**

```bash
#!/bin/bash
# Camera test script

echo "OS-SENTINEL Camera Testing"
echo "==========================="

# Test RTSP stream from each camera
test_camera() {
    camera_ip=$1
    camera_name=$2
    
    echo "Testing: $camera_name ($camera_ip)"
    
    # Test RTSP connection
    timeout 5 ffmpeg -i "rtsp://admin:password@$camera_ip:554/cam/realmonitor" \
      -frames:v 1 -f null - &> /dev/null
    
    if [ $? -eq 0 ]; then
        echo "  ✅ RTSP stream: OK"
    else
        echo "  ❌ RTSP stream: FAILED"
        return 1
    fi
    
    # Test snapshot
    curl -s -u admin:password "http://$camera_ip/cgi-bin/snapshot.cgi" \
      -o "/tmp/test_$camera_ip.jpg"
    
    if [ -f "/tmp/test_$camera_ip.jpg" ]; then
        echo "  ✅ Snapshot: OK"
    else
        echo "  ❌ Snapshot: FAILED"
    fi
    
    # Test motion detection
    # (Would require triggering motion and checking events)
    
    echo ""
}

# Test all cameras
test_camera "10.0.30.10" "Front Entrance"
test_camera "10.0.30.11" "Parking Lot A"
test_camera "10.0.30.12" "Rear Exit"
# ... test all cameras

echo "Camera testing complete!"
```

**5.2 Recording Validation**

```python
# Verify recordings are being saved
import os
import time
from datetime import datetime, timedelta

def verify_recordings(recording_path='/opt/shinobi/videos'):
    """Check that recordings exist for each camera"""
    
    cameras = os.listdir(recording_path)
    
    for camera in cameras:
        camera_path = os.path.join(recording_path, camera)
        
        # Get files from last hour
        one_hour_ago = time.time() - 3600
        recent_files = [
            f for f in os.listdir(camera_path)
            if os.path.getmtime(os.path.join(camera_path, f)) > one_hour_ago
        ]
        
        if len(recent_files) > 0:
            total_size = sum(
                os.path.getsize(os.path.join(camera_path, f))
                for f in recent_files
            )
            print(f"✅ {camera}: {len(recent_files)} files, {total_size/1024/1024:.1f} MB")
        else:
            print(f"❌ {camera}: No recordings in last hour!")

verify_recordings()
```

**5.3 AI Detection Test**

```python
# Test AI detection accuracy
def test_detection_accuracy():
    """Walk through camera views and verify detections"""
    
    test_scenarios = [
        {
            'camera': 'CAM-001',
            'action': 'person_walk_through',
            'expected': 'person detected'
        },
        {
            'camera': 'CAM-002',
            'action': 'vehicle_enter_parking',
            'expected': 'car detected'
        },
        {
            'camera': 'CAM-003',
            'action': 'loiter_45_seconds',
            'expected': 'loitering alert'
        }
    ]
    
    for scenario in test_scenarios:
        print(f"\nTest: {scenario['action']} on {scenario['camera']}")
        print(f"Expected: {scenario['expected']}")
        input("Perform action, then press Enter...")
        
        # Check if detection occurred
        time.sleep(5)
        
        # Query detections from last minute
        detections = requests.get(
            f"http://localhost:8080/api/v1/detections?camera={scenario['camera']}&since=60"
        ).json()
        
        if len(detections) > 0:
            print(f"✅ Detection occurred: {detections[0]['class']}")
        else:
            print(f"❌ No detection!")

test_detection_accuracy()
```

**5.4 Load Testing**

```bash
# Simulate 50 cameras streaming simultaneously
# Monitor system resources

# Install stress testing tools
sudo apt install -y stress-ng htop iotop

# Monitor during test
htop  # CPU/RAM
iotop  # Disk I/O
nvidia-smi -l 1  # GPU utilization

# Expected performance:
# - CPU: 50-70% average
# - RAM: <80% usage
# - GPU: 40-60% for analytics
# - Disk write: 200-500 MB/s
# - Network: 200-1000 Mbps
```

---

## Phase 6: Go-Live

### Week 4: Production Cutover

**6.1 Pre-Go-Live Checklist**

```
TECHNICAL VALIDATION
☐ All cameras online and recording
☐ All recordings viewable in Shinobi
☐ Motion detection triggering correctly
☐ AI analytics generating events
☐ Storage capacity adequate (30+ days)
☐ Network performance acceptable (<50ms latency)
☐ UPS tested (simulated power loss)
☐ Backup procedures verified

CAMERA COVERAGE
☐ All critical areas covered
☐ No significant blind spots
☐ Camera angles optimized
☐ Day and night visibility verified
☐ Weather resistance tested (outdoor cameras)

USER ACCESS
☐ User accounts created
☐ Role-based permissions configured
☐ Mobile app access tested
☐ Remote viewing tested
☐ Export functionality tested

DOCUMENTATION
☐ Camera map/diagram completed
☐ IP address list documented
☐ Login credentials secured
☐ Support procedures documented
☐ Escalation path defined

TRAINING
☐ Security staff trained
☐ Management trained
☐ IT staff trained
☐ Emergency procedures reviewed
```

**6.2 Go-Live Script**

```bash
#!/bin/bash
# OS-SENTINEL Go-Live

echo "OS-SENTINEL System Go-Live"
echo "==========================="

# Step 1: Final system health check
echo "Step 1: System Health Check"
./scripts/health-check.sh
echo ""

# Step 2: Verify all cameras online
echo "Step 2: Camera Status"
camera_count=$(docker exec shinobi-db mysql -u shinobi -pshinobipass ccio \
  -se "SELECT COUNT(*) FROM Monitors WHERE mode='record'")
echo "  Cameras recording: $camera_count"

# Step 3: Enable AI analytics
echo "Step 3: Enable AI Analytics"
sudo systemctl start sentinel-analytics
sleep 5
sudo systemctl status sentinel-analytics --no-pager

# Step 4: Enable notifications
echo "Step 4: Enable Notifications"
# Configure via Shinobi UI or API

# Step 5: Grant user access
echo "Step 5: User Access"
echo "  Users can now access: http://server-ip:8080"

# Step 6: Final smoke test
echo "Step 6: Smoke Test"
./scripts/smoke-test.sh

echo ""
echo "✅ GO-LIVE COMPLETE!"
echo ""
echo "System Information:"
echo "  - NVR URL: http://$(hostname -I | awk '{print $1}'):8080"
echo "  - Cameras: $camera_count"
echo "  - Analytics: Enabled"
echo "  - Storage: $(df -h /opt/shinobi/videos | tail -1 | awk '{print $4}') available"
echo ""
echo "Next Steps:"
echo "  1. Monitor first 24 hours closely"
echo "  2. Adjust motion sensitivity if needed"
echo "  3. Fine-tune AI detection zones"
echo "  4. Collect user feedback"
```

---

## Post-Deployment

### Maintenance & Optimization

**Weekly Tasks:**
```
☐ Review storage usage (delete old recordings if needed)
☐ Check camera online status
☐ Verify backup completion
☐ Review AI detection logs (false positives/negatives)
☐ Check system logs for errors
```

**Monthly Tasks:**
```
☐ Review user access (add/remove as needed)
☐ Update camera firmware
☐ Test UPS battery backup
☐ Clean camera lenses (outdoor cameras)
☐ Review and adjust detection zones
☐ Performance optimization
```

**Quarterly Tasks:**
```
☐ Full system backup
☐ Disaster recovery test
☐ Security audit
☐ Camera realignment (check for shifts)
☐ Storage capacity planning
```

---

## Troubleshooting Guide

### Common Issues

**Issue 1: Camera Offline**
```
Symptoms: Camera shows offline in NVR
Diagnosis:
1. Ping camera IP address
2. Check PoE switch (port status, power budget)
3. Check physical connections (cable, connector)
4. Verify camera has power (LED indicator)

Resolution:
- No ping → Check cable, switch port, camera power
- Ping OK but offline → Check credentials, RTSP path
- Intermittent → Check cable quality, EMI interference
```

**Issue 2: Poor Video Quality**
```
Symptoms: Blurry, pixelated, or laggy video
Diagnosis:
1. Check camera bitrate setting (should be 4-8 Mbps for 1080p)
2. Check network bandwidth utilization
3. Check camera focus (varifocal cameras)
4. Check lighting conditions

Resolution:
- Increase bitrate in camera settings
- Reduce FPS if bandwidth limited (30fps → 15fps)
- Refocus lens (outdoor cameras: check for condensation)
- Add external lighting for low-light areas
```

**Issue 3: Motion Detection Not Triggering**
```
Symptoms: No motion events recorded
Diagnosis:
1. Check motion sensitivity setting (too low?)
2. Check motion detection zones (configured?)
3. Check lighting (drastic changes can cause issues)
4. Test with obvious motion (walk directly at camera)

Resolution:
- Increase sensitivity (but watch for false positives)
- Redraw detection zones (avoid trees, flags, etc.)
- Adjust to scene (parking lot ≠ hallway)
- Disable motion detection in very low light, use analytics instead
```

**Issue 4: Storage Filling Up Fast**
```
Symptoms: Disk space running out before retention period
Diagnosis:
1. Check bitrate (is it too high?)
2. Check retention settings (too long?)
3. Check for continuous vs motion recording
4. Check number of cameras vs storage capacity

Resolution:
- Reduce bitrate: 8Mbps → 4Mbps
- Reduce retention: 30 days → 14 days
- Switch to motion-only recording (instead of continuous)
- Add more storage or reduce camera count
```

**Issue 5: AI Detections Inaccurate**
```
Symptoms: Too many false positives or missed detections
Diagnosis:
1. Check detection confidence threshold (default 0.6)
2. Check detection zones (too large?)
3. Check camera angle (objects too small/far?)
4. Check lighting (very dark causes false detections)

Resolution:
- Adjust confidence: 0.6 → 0.75 (reduce false positives)
- Redraw detection zones (smaller, more specific)
- Reposition camera (closer for better resolution)
- Add lighting or switch to higher resolution camera
```

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Typical Deployment**: 2-4 weeks (50 cameras)  
**System Scalability**: 10 to 1,000+ cameras per NVR
