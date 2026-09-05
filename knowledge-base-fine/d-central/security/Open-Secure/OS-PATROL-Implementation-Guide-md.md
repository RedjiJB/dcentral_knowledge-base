---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: e383559c-20be-46a1-bfbb-474240c77ad3
original_filename: OS-PATROL_Implementation_Guide.md
created_at: 2026-03-04T20:33:40.303754+00:00
content_hash: 341301480efc
---

# OS-PATROL Implementation Guide
## Fleet Management & Mobile Patrol System Deployment

**Document Type**: Implementation Guide  
**Version**: 1.0  
**Date**: December 2024  
**Classification**: Technical Documentation  
**Audience**: Fleet Managers, Mobile Technicians, IT Teams

---

## Executive Summary

**Deployment Timeline**: 1-2 days per vehicle  
**Team Required**: 2 technicians (automotive + IT)  
**Cost per Vehicle**: $800-$1,500 (hardware + installation)  
**Server Setup**: 1 day (centralized fleet server)

### Phase Overview

| Phase | Duration | Team | Deliverable |
|-------|----------|------|-------------|
| Server Setup | 1 day | IT Specialist | Traccar server operational |
| Vehicle Install | 4-6 hours | 2 Technicians | Hardware installed per vehicle |
| Software Config | 2 hours | IT Specialist | Vehicle registered & tracking |
| Testing | 1 hour | Full team | GPS verified, LPR tested |
| Training | 2 hours | Dispatcher + Drivers | System operational |

---

## Pre-Deployment Planning

### Fleet Assessment Checklist

```
VEHICLE INVENTORY
☐ Count total vehicles requiring tracking
☐ Identify vehicle types (sedan, SUV, truck, motorcycle)
☐ Note 12V power availability (cigarette lighter vs hardwire)
☐ Check existing equipment (dashcams, radios)
☐ Document VIN numbers for each vehicle
☐ Identify mounting locations (dashboard, windshield)

HARDWARE REQUIREMENTS PER VEHICLE
☐ GPS tracker (Raspberry Pi 4 or dedicated tracker)
☐ 4G/LTE modem with SIM card
☐ GPS antenna (external or internal)
☐ Dashcam (front-facing, 1080p minimum)
☐ LPR camera (2MP minimum, IR capable)
☐ Power supply (12V to 5V converter, 3A)
☐ SD card (64GB minimum for local storage)
☐ Mounting hardware (brackets, adhesive, screws)

INFRASTRUCTURE
☐ Server location identified (cloud or on-premises)
☐ Cellular data plan (unlimited recommended)
☐ Static IP or VPN for server access
☐ Backup procedures planned
```

### Bill of Materials Calculator

```python
def calculate_vehicle_bom(vehicle_type='standard'):
    """Calculate hardware cost per vehicle"""
    
    configurations = {
        'basic': {
            'description': 'GPS tracking only',
            'gps_tracker': 150,      # Dedicated GPS tracker
            'sim_card': 25,          # Monthly data plan
            'power_supply': 20,
            'mounting': 15,
            'total': 210
        },
        'standard': {
            'description': 'GPS + Dashcam',
            'raspberry_pi': 75,
            'gps_module': 30,
            'dashcam': 120,
            'sim_card': 25,
            'power_supply': 25,
            'sd_card': 20,
            'mounting': 25,
            'total': 320
        },
        'advanced': {
            'description': 'GPS + Dashcam + LPR',
            'raspberry_pi': 75,
            'gps_module': 30,
            'dashcam': 120,
            'lpr_camera': 180,
            'jetson_nano': 150,      # For LPR processing
            'sim_card': 35,          # Higher data usage
            'power_supply': 40,
            'sd_card': 30,
            'mounting': 40,
            'total': 700
        },
        'premium': {
            'description': 'Full suite + interior camera',
            'raspberry_pi': 75,
            'gps_module': 30,
            'dashcam_dual': 200,     # Front + rear
            'lpr_camera': 180,
            'interior_camera': 80,
            'jetson_nano': 150,
            'sim_card': 50,
            'power_supply': 50,
            'sd_card': 40,
            'mounting': 60,
            'obd2_adapter': 35,      # Vehicle diagnostics
            'total': 950
        }
    }
    
    config = configurations[vehicle_type]
    
    # Add recurring costs
    config['monthly_data'] = config['sim_card']
    config['annual_data'] = config['sim_card'] * 12
    
    return config

# Examples:
print("Basic (GPS only):", calculate_vehicle_bom('basic'))
# Total: $210 + $25/month

print("Standard (GPS + Dashcam):", calculate_vehicle_bom('standard'))
# Total: $320 + $25/month

print("Advanced (GPS + Dashcam + LPR):", calculate_vehicle_bom('advanced'))
# Total: $700 + $35/month

# Fleet calculation
def calculate_fleet_cost(num_vehicles, config_type='standard'):
    vehicle_cost = calculate_vehicle_bom(config_type)
    
    # Server costs (one-time + recurring)
    server_cost = {
        'cloud': 150,  # Monthly AWS/Azure
        'on_prem': 2000  # One-time hardware
    }
    
    total_hardware = vehicle_cost['total'] * num_vehicles
    monthly_data = vehicle_cost['monthly_data'] * num_vehicles
    
    return {
        'fleet_size': num_vehicles,
        'hardware_per_vehicle': vehicle_cost['total'],
        'total_hardware': total_hardware,
        'monthly_data': monthly_data,
        'annual_data': monthly_data * 12,
        'server_monthly': server_cost['cloud'],
        'total_first_year': total_hardware + (monthly_data * 12) + (server_cost['cloud'] * 12)
    }

# 10-vehicle fleet
fleet_10 = calculate_fleet_cost(10, 'standard')
print(f"10 vehicles: ${fleet_10['total_first_year']:,} first year")
# Output: ~$7,000 first year

# 50-vehicle fleet
fleet_50 = calculate_fleet_cost(50, 'advanced')
print(f"50 vehicles: ${fleet_50['total_first_year']:,} first year")
# Output: ~$56,000 first year
```

---

## Phase 1: Server Setup

### Day 1: Deploy Traccar Server

**1.1 Install Traccar (Docker)**

```bash
# Ubuntu 22.04 Server
sudo apt update
sudo apt install -y docker.io docker-compose

# Create directory structure
mkdir -p ~/traccar
cd ~/traccar

# Create docker-compose.yml
cat > docker-compose.yml <<EOF
version: '3.8'

services:
  traccar:
    image: traccar/traccar:latest
    container_name: traccar
    hostname: traccar
    ports:
      - "8082:8082"      # Web interface
      - "5055:5055"      # GPS tracker port (OsmAnd)
      - "5000-5150:5000-5150"  # Various tracker protocols
    volumes:
      - ./data:/opt/traccar/data
      - ./logs:/opt/traccar/logs
      - ./config:/opt/traccar/conf
    restart: unless-stopped
    environment:
      - TZ=America/New_York

  postgres:
    image: postgres:15
    container_name: traccar-db
    environment:
      POSTGRES_DB: traccar
      POSTGRES_USER: traccar
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres-data:
EOF

# Generate database password
export DB_PASSWORD=$(openssl rand -base64 32)
echo "DB_PASSWORD=$DB_PASSWORD" > .env

# Start services
docker-compose up -d

# Wait for Traccar to start (2-3 minutes)
docker-compose logs -f traccar
# Look for: "Starting server..."

# Access web interface
# http://server-ip:8082
# Default login: admin / admin (CHANGE IMMEDIATELY)
```

**1.2 Configure Traccar**

```bash
# Connect to Traccar container
docker exec -it traccar bash

# Edit configuration
cat > /opt/traccar/conf/traccar.xml <<EOF
<?xml version='1.0' encoding='UTF-8'?>
<config>
    <entry key='web.port'>8082</entry>
    <entry key='database.driver'>org.postgresql.Driver</entry>
    <entry key='database.url'>jdbc:postgresql://postgres:5432/traccar</entry>
    <entry key='database.user'>traccar</entry>
    <entry key='database.password'>${DB_PASSWORD}</entry>
    
    <!-- GPS accuracy filtering -->
    <entry key='coordinates.filter'>true</entry>
    <entry key='coordinates.minError'>50</entry>
    
    <!-- Data retention -->
    <entry key='database.history.days'>90</entry>
    
    <!-- Geofencing -->
    <entry key='geofence.polylineEncoder'>true</entry>
    
    <!-- Notifications -->
    <entry key='mail.smtp.host'>smtp.gmail.com</entry>
    <entry key='mail.smtp.port'>587</entry>
    <entry key='mail.smtp.starttls.enable'>true</entry>
    <entry key='mail.smtp.from'>patrol@company.com</entry>
    <entry key='mail.smtp.auth'>true</entry>
    <entry key='mail.smtp.username'>patrol@company.com</entry>
    <entry key='mail.smtp.password'>your_app_password</entry>
</config>
EOF

# Restart to apply config
exit
docker-compose restart traccar
```

**1.3 Create Geofences**

```bash
# Via Traccar API
API_TOKEN="your_admin_token"

# Create company headquarters geofence
curl -X POST http://localhost:8082/api/geofences \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{
    "name": "Company HQ",
    "description": "Main office location",
    "area": "CIRCLE (37.7749 -122.4194, 100)",
    "attributes": {
      "color": "#0000FF",
      "speedLimit": 15
    }
  }'

# Create service area geofence
curl -X POST http://localhost:8082/api/geofences \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{
    "name": "Service Area",
    "description": "Primary coverage zone",
    "area": "POLYGON ((37.8 -122.5, 37.8 -122.3, 37.7 -122.3, 37.7 -122.5, 37.8 -122.5))",
    "attributes": {}
  }'
```

---

## Phase 2: Vehicle Hardware Installation

### Day 2: Install Hardware (Per Vehicle)

**2.1 GPS Tracker Installation (Raspberry Pi)**

```bash
# Raspberry Pi 4 setup for GPS tracking

# 1. Flash Raspberry Pi OS Lite to SD card
# 2. Enable SSH and configure WiFi
# 3. Boot Pi and SSH in

# Update system
sudo apt update && sudo apt upgrade -y

# Install GPS daemon
sudo apt install -y gpsd gpsd-clients python3-gps

# Configure GPSD for USB GPS module
sudo nano /etc/default/gpsd
# Set: DEVICES="/dev/ttyUSB0"
# Set: GPSD_OPTIONS="-n"

# Test GPS
cgps -s
# Should show satellite data

# Install tracking client
sudo apt install -y git python3-pip
git clone https://github.com/traccar/traccar-client-android.git
cd traccar-client-android/client

# Create tracking script
cat > /home/pi/tracker.py <<'EOF'
#!/usr/bin/env python3
import gps
import requests
import time

TRACCAR_URL = "http://server-ip:5055"
DEVICE_ID = "VEHICLE_001"

session = gps.gps(mode=gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

while True:
    try:
        report = session.next()
        if report['class'] == 'TPV':
            if hasattr(report, 'lat') and hasattr(report, 'lon'):
                # Send to Traccar
                params = {
                    'id': DEVICE_ID,
                    'lat': report.lat,
                    'lon': report.lon,
                    'timestamp': int(time.time()),
                    'speed': getattr(report, 'speed', 0),
                    'bearing': getattr(report, 'track', 0),
                    'altitude': getattr(report, 'alt', 0),
                    'accuracy': getattr(report, 'epx', 0)
                }
                
                requests.get(TRACCAR_URL, params=params, timeout=10)
                print(f"Sent: {report.lat}, {report.lon}")
        
        time.sleep(5)  # Send every 5 seconds
        
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
EOF

chmod +x /home/pi/tracker.py

# Create systemd service
sudo nano /etc/systemd/system/tracker.service
# [Service content with ExecStart=/home/pi/tracker.py]

sudo systemctl enable tracker
sudo systemctl start tracker
```

**2.2 Dashcam Installation**

```
Mounting Location:
├── Behind rearview mirror (optimal)
├── Center of windshield, below mirror
├── Height: Driver's eye level
└── Angle: 5-10° downward

Wiring:
1. Route cable along headliner
2. Down A-pillar (use plastic pry tools)
3. Under dashboard to power source
4. Connect to 12V accessory (switched, not always-on)
5. Use inline fuse (3A)

Configuration:
- Resolution: 1080p @ 30fps
- Loop recording: 3-minute segments
- G-sensor: Medium sensitivity
- Parking mode: Motion detection
- GPS: Enabled
- Time/date stamp: Enabled
```

**2.3 LPR Camera Installation (Advanced)**

```
Mounting Location:
├── Hood or grille (forward-facing)
├── Driver side mirror (side-facing)
├── Roof rack (both directions)
└── Height: 3-4 feet from ground

Specifications:
- Resolution: 2MP minimum (1920×1080)
- Frame rate: 30fps
- IR illumination: 850nm (night reading)
- Lens: 6-12mm varifocal
- Viewing angle: Capture 2-3 lanes

Wiring:
1. PoE injector if using PoE camera
2. Or: 12V power + Ethernet
3. Route cable to Jetson Nano (if AI processing)
4. Or: Stream to cloud for processing

Camera Angle:
- 30-45° from perpendicular to traffic
- Capture plates at 5-60 mph
- Adjust focus for 10-40 feet distance
```

**2.4 Power Installation**

```
Option A: Cigarette Lighter (Temporary)
- Quick install (5 minutes)
- Easy removal
- May not work when vehicle off
- Suitable for: Basic tracking

Option B: Hardwire to Fuse Box (Permanent)
- Professional install (30 minutes)
- Always-on or ignition-switched
- Cleaner appearance
- Suitable for: All configurations

Hardwire Procedure:
1. Locate fuse box (usually driver side, below dashboard)
2. Identify switched 12V circuit (radio, accessories)
3. Use add-a-fuse adapter
4. Connect red wire to fuse tap
5. Connect black wire to chassis ground
6. Route cables neatly, secure with zip ties
7. Test: Key on = power, key off = no power (if switched)

Voltage Regulator:
- Input: 12V DC (vehicle)
- Output: 5V DC 3A (Raspberry Pi)
- Use buck converter with voltage protection
- Add inline fuse (5A on 12V side)
```

---

## Phase 3: Software Configuration

### Day 2-3: Configure Tracking

**3.1 Register Vehicles in Traccar**

```python
# Bulk vehicle registration script
import requests

TRACCAR_URL = "http://server-ip:8082/api"
API_TOKEN = "admin_token"

vehicles = [
    {
        'name': 'Unit 1 - Ford Explorer',
        'uniqueId': 'VEHICLE_001',
        'category': 'suv',
        'phone': '+15551234567',
        'model': 'Ford Explorer',
        'contact': 'Officer Smith',
        'vin': '1FMCU0G92MUA12345'
    },
    {
        'name': 'Unit 2 - Chevy Tahoe',
        'uniqueId': 'VEHICLE_002',
        'category': 'suv',
        'phone': '+15551234568',
        'model': 'Chevrolet Tahoe',
        'contact': 'Officer Jones',
        'vin': '1GNSCCKC1KR123456'
    }
]

for vehicle in vehicles:
    response = requests.post(
        f"{TRACCAR_URL}/devices",
        headers={
            'Authorization': f'Bearer {API_TOKEN}',
            'Content-Type': 'application/json'
        },
        json=vehicle
    )
    
    if response.status_code == 200:
        print(f"✅ Registered: {vehicle['name']}")
    else:
        print(f"❌ Failed: {vehicle['name']} - {response.text}")
```

**3.2 Configure Notifications**

```bash
# Email notification for geofence exit
curl -X POST http://localhost:8082/api/notifications \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{
    "type": "geofenceExit",
    "always": true,
    "notificators": "mail",
    "attributes": {
      "message": "Vehicle {deviceName} has left {geofenceName}"
    }
  }'

# SMS notification for speeding
curl -X POST http://localhost:8082/api/notifications \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{
    "type": "deviceOverspeed",
    "always": true,
    "notificators": "sms",
    "attributes": {
      "speedLimit": 75,
      "message": "ALERT: {deviceName} speeding at {speed} mph"
    }
  }'
```

**3.3 Setup LPR Processing (Advanced)**

```python
# OpenALPR integration for license plate recognition
import requests
from openalpr import Alpr

class LPRProcessor:
    def __init__(self, camera_stream_url):
        self.alpr = Alpr("us", "/etc/openalpr/openalpr.conf", 
                         "/usr/share/openalpr/runtime_data")
        self.camera_url = camera_stream_url
        self.hot_list = self.load_hot_list()
    
    def load_hot_list(self):
        """Load hot list from database"""
        # In production, query from database
        return [
            {'plate': 'ABC1234', 'state': 'CA', 'reason': 'stolen'},
            {'plate': 'XYZ9876', 'state': 'NY', 'reason': 'warrant'}
        ]
    
    def process_frame(self, frame):
        """Process single frame for plates"""
        results = self.alpr.recognize_ndarray(frame)
        
        plates_found = []
        for plate in results['results']:
            plate_number = plate['plate']
            confidence = plate['confidence']
            
            if confidence > 85:  # High confidence threshold
                plates_found.append({
                    'plate': plate_number,
                    'confidence': confidence,
                    'timestamp': time.time()
                })
                
                # Check against hot list
                if self.check_hot_list(plate_number):
                    self.alert_dispatch(plate_number, plate)
        
        return plates_found
    
    def check_hot_list(self, plate_number):
        """Check if plate is on hot list"""
        for hot_plate in self.hot_list:
            if hot_plate['plate'] == plate_number:
                return True
        return False
    
    def alert_dispatch(self, plate, details):
        """Send alert for hot list match"""
        alert = {
            'type': 'hot_list_match',
            'plate': plate,
            'confidence': details['confidence'],
            'location': self.get_current_location(),
            'timestamp': time.time(),
            'vehicle_id': 'VEHICLE_001'
        }
        
        # Send to dispatch system
        requests.post('http://dispatch.company.com/api/alerts', json=alert)
        
        # Log to OS-PATROL API
        requests.post('http://patrol-api.company.com/v1/lpr/hits', json=alert)

# Usage
lpr = LPRProcessor('rtsp://camera-ip:554/stream')

# Process video stream
import cv2
cap = cv2.VideoCapture(lpr.camera_url)

while True:
    ret, frame = cap.read()
    if ret:
        plates = lpr.process_frame(frame)
        for plate in plates:
            print(f"Detected: {plate['plate']} ({plate['confidence']}%)")
    
    time.sleep(1)  # Process 1 frame per second
```

---

## Phase 4: Testing & Validation

### Day 3: System Testing

**4.1 GPS Accuracy Test**

```bash
#!/bin/bash
# GPS accuracy test script

echo "GPS Accuracy Test"
echo "================="

VEHICLE_ID="VEHICLE_001"
API_URL="http://server-ip:8082/api"
TOKEN="admin_token"

# Test 1: Position reporting
echo "Test 1: Position Reporting"
response=$(curl -s "$API_URL/positions?deviceId=$VEHICLE_ID" \
  -H "Authorization: Bearer $TOKEN")

latitude=$(echo $response | jq '.[0].latitude')
longitude=$(echo $response | jq '.[0].longitude')
accuracy=$(echo $response | jq '.[0].accuracy')

echo "  Latitude: $latitude"
echo "  Longitude: $longitude"
echo "  Accuracy: $accuracy meters"

if (( $(echo "$accuracy < 50" | bc -l) )); then
    echo "  ✅ PASS: Accuracy good (<50m)"
else
    echo "  ❌ FAIL: Accuracy poor (>50m)"
fi

# Test 2: Update frequency
echo ""
echo "Test 2: Update Frequency"
sleep 10
response2=$(curl -s "$API_URL/positions?deviceId=$VEHICLE_ID" \
  -H "Authorization: Bearer $TOKEN")

timestamp1=$(echo $response | jq '.[0].deviceTime')
timestamp2=$(echo $response2 | jq '.[0].deviceTime')

if [ "$timestamp1" != "$timestamp2" ]; then
    echo "  ✅ PASS: Position updates working"
else
    echo "  ❌ FAIL: Position not updating"
fi

# Test 3: Speed accuracy (requires vehicle movement)
echo ""
echo "Test 3: Speed Accuracy"
speed=$(echo $response2 | jq '.[0].speed')
echo "  Current speed: $speed mph"
echo "  (Drive vehicle and verify speed matches speedometer)"

echo ""
echo "Testing complete!"
```

**4.2 Geofence Test**

```python
# Simulate geofence entry/exit
import time
import requests

def test_geofence(vehicle_id, geofence_id):
    """Test geofence notifications"""
    
    print(f"Testing geofence for {vehicle_id}")
    
    # 1. Drive vehicle into geofence
    print("Step 1: Drive vehicle into geofence...")
    input("Press Enter when vehicle is INSIDE geofence")
    
    # Check if geofence entry was detected
    time.sleep(5)
    events = requests.get(
        f"http://server-ip:8082/api/events?deviceId={vehicle_id}&type=geofenceEnter",
        headers={'Authorization': 'Bearer admin_token'}
    ).json()
    
    if len(events) > 0:
        print("✅ Geofence entry detected")
    else:
        print("❌ Geofence entry NOT detected")
    
    # 2. Drive vehicle out of geofence
    print("Step 2: Drive vehicle OUT of geofence...")
    input("Press Enter when vehicle is OUTSIDE geofence")
    
    time.sleep(5)
    events = requests.get(
        f"http://server-ip:8082/api/events?deviceId={vehicle_id}&type=geofenceExit",
        headers={'Authorization': 'Bearer admin_token'}
    ).json()
    
    if len(events) > 0:
        print("✅ Geofence exit detected")
    else:
        print("❌ Geofence exit NOT detected")

test_geofence('VEHICLE_001', 'GEOFENCE_HQ')
```

**4.3 LPR Test (If Installed)**

```python
# Test license plate recognition
def test_lpr():
    """Test LPR camera and processing"""
    
    print("LPR Test")
    print("========")
    
    # 1. Camera connectivity
    import cv2
    cap = cv2.VideoCapture('rtsp://camera-ip:554/stream')
    
    if cap.isOpened():
        print("✅ Camera connected")
    else:
        print("❌ Camera connection failed")
        return
    
    # 2. Frame capture
    ret, frame = cap.read()
    if ret:
        print(f"✅ Frame captured ({frame.shape[1]}x{frame.shape[0]})")
    else:
        print("❌ Frame capture failed")
        return
    
    # 3. Plate detection
    from openalpr import Alpr
    alpr = Alpr("us", "/etc/openalpr/openalpr.conf", 
                "/usr/share/openalpr/runtime_data")
    
    results = alpr.recognize_ndarray(frame)
    
    if len(results['results']) > 0:
        for plate in results['results']:
            print(f"✅ Detected plate: {plate['plate']} ({plate['confidence']}%)")
    else:
        print("⚠️  No plates detected (drive past vehicles with visible plates)")
    
    cap.release()

test_lpr()
```

---

## Phase 5: Go-Live

### Day 3: Production Deployment

**5.1 Pre-Go-Live Checklist**

```
TECHNICAL READINESS
☐ All vehicles reporting GPS positions
☐ Position updates every 5-10 seconds
☐ GPS accuracy < 50 meters
☐ Geofences configured and tested
☐ Notifications enabled (email/SMS)
☐ Dashboard accessible to dispatchers
☐ Mobile app installed on driver devices
☐ Backup procedures tested
☐ Monitoring configured

VEHICLE READINESS
☐ All hardware installed securely
☐ Cables routed and secured
☐ Power connections tested
☐ Cameras aligned and focused
☐ LPR tested (if applicable)
☐ Vehicle-specific settings configured

OPERATIONAL READINESS
☐ Dispatchers trained on system
☐ Drivers trained on mobile app
☐ Standard operating procedures documented
☐ Emergency procedures defined
☐ On-call support established
☐ Hot list populated (if using LPR)
```

**5.2 Go-Live Procedure**

```bash
#!/bin/bash
# Go-live script

echo "OS-PATROL Go-Live Procedure"
echo "==========================="

# Step 1: Final system check
echo "Step 1: System Health Check"
./scripts/health-check.sh

# Step 2: Activate all vehicles
echo "Step 2: Activate Vehicles"
python3 - <<EOF
import requests

vehicles = requests.get(
    'http://server-ip:8082/api/devices',
    headers={'Authorization': 'Bearer admin_token'}
).json()

for vehicle in vehicles:
    # Enable tracking
    requests.put(
        f"http://server-ip:8082/api/devices/{vehicle['id']}",
        headers={'Authorization': 'Bearer admin_token'},
        json={'disabled': False}
    )
    print(f"✅ Activated: {vehicle['name']}")
EOF

# Step 3: Enable notifications
echo "Step 3: Enable Notifications"
# Notifications already configured in Phase 3

# Step 4: Grant dispatcher access
echo "Step 4: Grant Access"
echo "  Dispatchers can now access: http://server-ip:8082"

# Step 5: Monitor first hour
echo "Step 5: Monitor System"
echo "  Watch for:"
echo "    - All vehicles reporting"
echo "    - No GPS errors"
echo "    - Notifications working"

echo ""
echo "✅ GO-LIVE COMPLETE!"
echo ""
echo "Dashboard: http://server-ip:8082"
echo "Username: dispatcher / Password: [set during setup]"
```

---

## Post-Deployment

### Week 1: Monitoring & Optimization

**Key Metrics:**
```
Daily:
- Vehicle uptime (% time reporting)
- GPS accuracy (average error in meters)
- Speeding incidents
- Geofence violations
- Battery health (if monitoring)

Weekly:
- Miles driven per vehicle
- Idle time per vehicle
- Fuel efficiency trends (if OBD-II connected)
- Driver behavior scores
- Hot list hits (if LPR enabled)
```

**Monitoring Dashboard:**
```python
# Create daily fleet report
from datetime import datetime, timedelta

def generate_fleet_report():
    """Generate daily fleet activity report"""
    
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    report = {
        'date': str(today),
        'vehicles': []
    }
    
    # For each vehicle
    vehicles = traccar.get_devices()
    
    for vehicle in vehicles:
        # Get trips
        trips = traccar.get_trips(
            vehicle['id'],
            start=yesterday,
            end=today
        )
        
        # Calculate stats
        total_distance = sum(trip['distance'] for trip in trips)
        total_duration = sum(trip['duration'] for trip in trips)
        max_speed = max((trip['maxSpeed'] for trip in trips), default=0)
        
        vehicle_stats = {
            'name': vehicle['name'],
            'trips': len(trips),
            'distance_miles': total_distance / 1609.34,  # Convert meters to miles
            'drive_time_hours': total_duration / 3600,
            'max_speed_mph': max_speed,
            'avg_speed_mph': (total_distance / total_duration * 2.23694) if total_duration > 0 else 0
        }
        
        report['vehicles'].append(vehicle_stats)
    
    # Generate PDF or email report
    return report

# Run daily via cron
report = generate_fleet_report()
email_report(report, recipients=['fleet@company.com'])
```

---

## Troubleshooting Guide

### Issue 1: GPS Not Reporting

```
Symptoms: Vehicle shows "offline" or stale position
Diagnosis:
1. Check cellular signal: ping GPS device
2. Check power: Measure voltage at device (should be 5V)
3. Check GPS antenna: Verify connected, check LED
4. Check GPS fix: Run 'cgps -s' on device

Resolution:
- Weak cell signal → Move antenna, upgrade to external antenna
- No power → Check fuse, wiring, converter
- No GPS fix → Check antenna placement (sky view), wait for satellites
- Device offline → Restart device, check network config
```

### Issue 2: Poor GPS Accuracy

```
Symptoms: Position "jumps" or > 100m error
Diagnosis:
1. Check satellite count: Should have 6+ satellites
2. Check HDOP: Should be < 2.0 (lower is better)
3. Check antenna placement: Obstructed by metal?

Resolution:
- Move antenna to windshield (best sky view)
- Use external antenna on roof
- Enable GPS filtering in Traccar (coordinates.filter=true)
- Wait for GPS to acquire more satellites
```

### Issue 3: LPR Not Reading Plates

```
Symptoms: No plates detected or low confidence
Diagnosis:
1. Check camera angle: 30-45° from perpendicular
2. Check focus: Plates should be sharp at 10-40 feet
3. Check lighting: IR illumination working at night?
4. Check speed: Plates readable at target speed?

Resolution:
- Adjust camera angle (test while parked)
- Refocus lens for plate distance
- Verify IR LEDs working (use phone camera to see IR glow)
- Slow down vehicle speed for initial testing
- Increase shutter speed to reduce motion blur
```

### Issue 4: High Data Usage

```
Symptoms: Cellular data limit exceeded
Diagnosis:
1. Check reporting frequency (every 5 sec = ~50MB/day)
2. Check video streaming (dashcam/LPR streams?)
3. Check for loops (device continuously reconnecting?)

Resolution:
- Increase reporting interval: 5 sec → 30 sec
- Disable continuous video streaming, use motion-triggered
- Implement data usage monitoring and alerts
- Use WiFi sync when vehicle at base
```

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Typical Deployment**: 1-2 days per vehicle  
**Fleet Rollout**: 1 week for 10 vehicles
