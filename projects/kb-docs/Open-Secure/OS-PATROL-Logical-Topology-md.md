---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: 52053d40-a9b5-4cd1-844e-c74a48a8a947
original_filename: OS-PATROL_Logical_Topology.md
created_at: 2026-03-04T20:33:40.759833+00:00
content_hash: a64caf68f8de
---

# OS-PATROL Logical Topology
## Fleet Management System Architecture & Data Flow Patterns

**Document Type**: Logical Architecture Specification  
**Version**: 1.0  
**Date**: December 2024  
**Classification**: Technical Documentation  
**Audience**: Solution Architects, Fleet Managers, System Designers

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Logical Architecture Overview](#logical-architecture-overview)
3. [Component Relationships](#component-relationships)
4. [Data Flow Patterns](#data-flow-patterns)
5. [GPS Tracking Architecture](#gps-tracking-architecture)
6. [License Plate Recognition Pipeline](#license-plate-recognition-pipeline)
7. [Video Management](#video-management)
8. [Dispatch & CAD Integration](#dispatch--cad-integration)
9. [API Architecture](#api-architecture)
10. [State Management](#state-management)

---

## Executive Summary

### Architectural Philosophy

OS-PATROL implements a **distributed edge-cloud architecture** where intelligence lives both in vehicles (edge) and the fleet operations center (cloud). This hybrid approach enables:

- **Real-time tracking** with 5-second position updates
- **Offline operation** for up to 7 days without connectivity
- **Intelligent data prioritization** (critical events upload immediately, bulk data via WiFi)
- **Scalable processing** (edge AI for LPR, cloud for analytics)

### Key Logical Concepts

| Concept | Definition | Implementation |
|---------|------------|----------------|
| **Vehicle Unit** | Autonomous mobile edge node | Raspberry Pi 4 / Jetson Nano with sensors |
| **GPS Track** | Time-series position data | PostGIS + TimescaleDB |
| **LPR Event** | License plate detection | OpenALPR + hot-list matching |
| **Video Clip** | Incident-tagged footage | H.264 segments in MinIO |
| **Dispatch Event** | Call for service | CAD system integration |
| **Geofence** | Virtual boundary | PostGIS polygon queries |

---

## Logical Architecture Overview

### Five-Layer Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                    LAYER 5: PRESENTATION                            │
│                                                                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐  │
│  │  Web       │  │  Mobile    │  │  Dispatch  │  │  Analytics │  │
│  │  Dashboard │  │  App       │  │  Console   │  │  Portal    │  │
│  │  (React)   │  │ (Flutter)  │  │  (CAD)     │  │ (Grafana)  │  │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘  │
└────────────────────────────┬───────────────────────────────────────┘
                             │ HTTPS / WebSocket
┌────────────────────────────▼───────────────────────────────────────┐
│                    LAYER 4: APPLICATION SERVICES                    │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │               Traccar Fleet Server                            │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │ │
│  │  │  GPS     │  │  Route   │  │ Geofence │  │  Alert   │    │ │
│  │  │ Tracking │  │ Planning │  │  Engine  │  │  Engine  │    │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │               LibreDispatch CAD System                        │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │ │
│  │  │  Unit    │  │ Incident │  │  Status  │  │  Radio   │    │ │
│  │  │ Location │  │  Assign  │  │  Board   │  │  Link    │    │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │           LPR Processing Service                              │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │ │
│  │  │Hot-List  │  │  Image   │  │ Database │                   │ │
│  │  │  Match   │  │ Enhance  │  │  Search  │                   │ │
│  │  └──────────┘  └──────────┘  └──────────┘                   │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬───────────────────────────────────────┘
                             │ Internal APIs
┌────────────────────────────▼───────────────────────────────────────┐
│                    LAYER 3: DATA SERVICES                           │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │PostgreSQL│  │ MinIO    │  │  Redis   │  │  NATS    │         │
│  │+ PostGIS │  │ Video    │  │  Cache   │  │ Message  │         │
│  │+ Time-   │  │ Storage  │  │          │  │   Bus    │         │
│  │  scale   │  │          │  │          │  │          │         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
└────────────────────────────┬───────────────────────────────────────┘
                             │ 4G LTE / VPN
┌────────────────────────────▼───────────────────────────────────────┐
│                    LAYER 2: EDGE INTELLIGENCE                       │
│                    (On-Vehicle Processing)                          │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  Raspberry Pi 4 / Jetson Nano Edge Controller                │ │
│  │                                                                │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │ │
│  │  │ Traccar  │  │ OpenALPR │  │MotionEye │  │ OBD-II   │    │ │
│  │  │  Client  │  │  (LPR)   │  │(Dashcam) │  │ Monitor  │    │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │ │
│  │                                                                │ │
│  │  ┌──────────────────────────────────────────────────────┐    │ │
│  │  │  Local Data Buffer (128GB SD)                        │    │ │
│  │  │  • GPS: 30 days                                      │    │ │
│  │  │  • LPR: 7 days                                       │    │ │
│  │  │  • Video: 72 hours                                   │    │ │
│  │  └──────────────────────────────────────────────────────┘    │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬───────────────────────────────────────┘
                             │ USB / Serial / GPIO
┌────────────────────────────▼───────────────────────────────────────┐
│                    LAYER 1: SENSOR LAYER                            │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │   GPS    │  │   LPR    │  │ Dashcam  │  │  OBD-II  │         │
│  │ Receiver │  │  Camera  │  │  (×4-6)  │  │  Port    │         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Component Relationships

### Entity-Relationship Model

```
┌──────────┐
│ VEHICLE  │
├──────────┤
│ id       │
│ unit_num │◄─────┐
│ vin      │      │ 1:N
│ status   │      │
└────┬─────┘      │
     │            │
     │ 1:N        │
     │            │
┌────▼──────┐     │
│GPS_TRACK  │     │
├───────────┤     │
│ vehicle_id│─────┘
│ timestamp │
│ location  │ (PostGIS Point)
│ speed     │
│ heading   │
└────┬──────┘
     │
     │ 1:N
     │
┌────▼────────┐
│  LPR_EVENT  │
├─────────────┤
│ vehicle_id  │
│ timestamp   │
│ plate_number│
│ confidence  │
│ image_url   │
│ hot_list_hit│ (Boolean)
└────┬────────┘
     │
     │ 1:N
     │
┌────▼──────────┐
│  VIDEO_CLIP   │
├───────────────┤
│ vehicle_id    │
│ camera_id     │
│ timestamp     │
│ duration      │
│ event_type    │ (incident, routine, manual)
│ file_url      │
└───────────────┘

┌────────────┐
│  DISPATCH  │
│   EVENT    │
├────────────┤
│ incident_id│
│ location   │ (PostGIS Point)
│ type       │
│ priority   │
└────┬───────┘
     │
     │ 1:N
     │
┌────▼──────────┐
│UNIT_ASSIGNMENT│
├───────────────┤
│ vehicle_id    │
│ incident_id   │
│ assigned_at   │
│ status        │ (dispatched, enroute, onscene)
└───────────────┘
```

---

## Data Flow Patterns

### GPS Tracking Flow (Real-Time)

```
┌─────────────────────────────────────────────────────────────────┐
│                  GPS TRACKING DATA FLOW                          │
└─────────────────────────────────────────────────────────────────┘

Step 1: GPS Signal Acquisition
┌──────────┐
│ GPS      │  Receives signals from 4+ satellites
│ Receiver │  Calculates: lat, lon, altitude, speed, heading
└────┬─────┘  Accuracy: ±3-10m depending on conditions
     │
     │ NMEA sentences (38400 baud serial)
     │ $GPGGA: Position fix
     │ $GPRMC: Recommended minimum
     │ $GPGSV: Satellites in view
     ▼
Step 2: Local Processing
┌──────────┐
│  gpsd    │  Daemon parses NMEA → structured data
│ Daemon   │  Validates position (sanity checks)
└────┬─────┘  Enriches with: timestamp, quality metrics
     │
     │ JSON via local socket
     │ {
     │   "lat": 40.7128,
     │   "lon": -74.0060,
     │   "speed_mph": 35.5,
     │   "heading": 270,
     │   "satellites": 12,
     │   "hdop": 0.9
     │ }
     ▼
Step 3: Client Batching
┌──────────┐
│ Traccar  │  Buffers positions locally
│  Client  │  Batch size: 30 seconds OR 50 points
└────┬─────┘  Adds: vehicle_id, odometer, fuel_level (OBD)
     │
     │ HTTPS POST (every 30s)
     │ POST /api/positions
     │ [
     │   {timestamp, vehicle_id, lat, lon, ...},
     │   {timestamp, vehicle_id, lat, lon, ...},
     │   ...
     │ ]
     ▼
Step 4: Cloud Ingestion
┌──────────┐
│ Traccar  │  REST API receives batch
│  Server  │  Validates data
└────┬─────┘  Deduplicates (if retry)
     │
     │ Async write to database
     │
     ▼
┌──────────────────┐
│PostgreSQL        │  INSERT INTO positions ...
│ + TimescaleDB    │  Hypertable optimized for time-series
│ + PostGIS        │  Spatial indexing for location queries
└────┬─────────────┘
     │
     │ Triggers update
     │
     ▼
┌──────────┐
│ WebSocket│  Push to connected clients
│  Server  │  Topic: "vehicle.{id}.position"
└────┬─────┘  Payload: Latest position
     │
     ├──────────────┬──────────────┬──────────────┐
     ▼              ▼              ▼              ▼
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│Dashboard│  │Mobile   │  │Dispatch │  │Analytics│
│(Web UI) │  │App      │  │Console  │  │Engine   │
└─────────┘  └─────────┘  └─────────┘  └─────────┘

Total Latency: 5-15 seconds (GPS → Dashboard)
- GPS fix: 1s
- Client batch: 0-30s (depends on buffer)
- Network transmission: 1-5s
- Server processing: 0.5s
- WebSocket push: 0.5s
```

### LPR Event Flow (Hot-List Matching)

```
Step 1: Image Capture
LPR Camera (4MP @ 60fps) → Continuous capture
     │
     │ USB 3.0 video stream
     ▼
Step 2: Edge Processing
Jetson Nano / RPi 4
  ┌─────────────────────┐
  │ OpenALPR Engine     │
  │ • Plate detection   │ YOLOv5 object detection
  │ • OCR recognition   │ Tesseract + custom training
  │ • Confidence scoring│ 0.0-1.0 (reject if <0.7)
  └──────┬──────────────┘
         │
         │ Detected: "ABC1234" (confidence: 0.92)
         │ Image crop saved: /tmp/lpr/ABC1234_timestamp.jpg
         ▼
Step 3: Local Hot-List Check
  ┌─────────────────────┐
  │ Local SQLite DB     │
  │ Hot-list: 10,000    │
  │ plates (synced)     │
  └──────┬──────────────┘
         │
         │ Query: SELECT * FROM hot_list WHERE plate = 'ABC1234'
         │
    ┌────┴────┐
    │         │
  MATCH     NO MATCH
    │         │
    ▼         ▼
[CRITICAL] [NORMAL]
    │         │
    ├─────────┴──────┐
    │                │
Step 4: Event Upload
    │ Immediate      │ Batch upload (every 5 min)
    │ (4G LTE)       │ (or WiFi)
    ▼                ▼
POST /api/lpr/events
{
  "vehicle_id": 12,
  "timestamp": "2024-12-08T14:23:45Z",
  "plate": "ABC1234",
  "confidence": 0.92,
  "location": {"lat": 40.7128, "lon": -74.0060},
  "image_url": "s3://bucket/lpr/ABC1234.jpg",
  "hot_list_match": true,
  "hot_list_reason": "Stolen vehicle - Case #2024-5678"
}

Step 5: Cloud Processing
Traccar Server
  │
  │ INSERT INTO lpr_events
  │
  ▼
IF hot_list_match == true:
  ┌─────────────────────┐
  │ Alert Engine        │
  │ • SMS to officer    │
  │ • Dashboard popup   │
  │ • Email to command  │
  │ • Log for audit     │
  └─────────────────────┘

Total Latency (Hot-List Hit):
- Detection: 0.1s
- OCR: 0.5s
- Local query: 0.01s
- Upload: 2-5s (4G LTE)
- Alert: 1s
= 3.6-6.6 seconds total

Officer notified within 7 seconds of plate scan!
```

---

## GPS Tracking Architecture

### Spatial Data Model (PostGIS)

```sql
-- Positions table (TimescaleDB hypertable)
CREATE TABLE positions (
    time TIMESTAMPTZ NOT NULL,
    vehicle_id INT NOT NULL,
    location GEOGRAPHY(Point, 4326),  -- PostGIS
    speed DOUBLE PRECISION,           -- mph
    heading INT,                      -- 0-359 degrees
    altitude DOUBLE PRECISION,        -- meters
    satellites INT,
    hdop DOUBLE PRECISION,            -- Horizontal dilution of precision
    odometer BIGINT,                  -- meters
    fuel_level INT,                   -- 0-100%
    engine_status VARCHAR(20)         -- running, idle, off
);

-- Convert to hypertable (time-series optimization)
SELECT create_hypertable('positions', 'time');

-- Spatial index for location queries
CREATE INDEX idx_positions_location ON positions USING GIST(location);

-- Composite index for vehicle time-series queries
CREATE INDEX idx_positions_vehicle_time ON positions(vehicle_id, time DESC);

-- Query: Get vehicle's last 100 positions
SELECT 
    time,
    ST_X(location::geometry) as longitude,
    ST_Y(location::geometry) as latitude,
    speed,
    heading
FROM positions
WHERE vehicle_id = 12
ORDER BY time DESC
LIMIT 100;

-- Query: Find all vehicles within 1 mile of a point
SELECT 
    vehicle_id,
    ST_Distance(
        location,
        ST_MakePoint(-74.0060, 40.7128)::geography
    ) / 1609.34 as distance_miles
FROM positions
WHERE time > NOW() - INTERVAL '5 minutes'
  AND ST_DWithin(
      location,
      ST_MakePoint(-74.0060, 40.7128)::geography,
      1609.34  -- 1 mile in meters
  )
ORDER BY distance_miles;
```

### Geofence Engine

```python
class GeofenceEngine:
    def __init__(self):
        self.geofences = self.load_geofences()
        
    def load_geofences(self):
        """Load all active geofences from database"""
        # Geofence types:
        # - CIRCLE: center point + radius
        # - POLYGON: arbitrary shape
        # - ROUTE: polyline with buffer
        
        return [
            {
                'id': 1,
                'name': 'Downtown District',
                'type': 'POLYGON',
                'coordinates': [...],
                'alert_on_enter': True,
                'alert_on_exit': False
            },
            {
                'id': 2,
                'name': 'School Zone',
                'type': 'CIRCLE',
                'center': (-74.0060, 40.7128),
                'radius_meters': 300,
                'speed_limit': 25,
                'alert_on_speed': True
            }
        ]
    
    def check_position(self, vehicle_id, position):
        """Check if position violates any geofences"""
        
        for geofence in self.geofences:
            inside = self.is_inside(position, geofence)
            
            # Check previous state
            was_inside = self.get_previous_state(vehicle_id, geofence['id'])
            
            # Detect state change
            if inside and not was_inside:
                # Just entered geofence
                if geofence.get('alert_on_enter'):
                    self.trigger_alert(vehicle_id, geofence, 'ENTER')
                
            elif not inside and was_inside:
                # Just exited geofence
                if geofence.get('alert_on_exit'):
                    self.trigger_alert(vehicle_id, geofence, 'EXIT')
            
            # Check speed if inside speed-limited zone
            if inside and geofence.get('speed_limit'):
                if position['speed'] > geofence['speed_limit']:
                    self.trigger_alert(vehicle_id, geofence, 'SPEEDING')
            
            # Update state
            self.update_state(vehicle_id, geofence['id'], inside)
    
    def is_inside(self, position, geofence):
        """Check if position is inside geofence"""
        if geofence['type'] == 'CIRCLE':
            distance = haversine(position, geofence['center'])
            return distance <= geofence['radius_meters']
        
        elif geofence['type'] == 'POLYGON':
            # Use PostGIS for complex polygon checks
            return self.postgis_contains(geofence['id'], position)
```

---

## License Plate Recognition Pipeline

### OpenALPR Processing Architecture

```
Image Input (4MP @ 60fps)
        │
        ▼
┌────────────────────────┐
│ Frame Selection        │  Only process every 3rd frame (20fps effective)
│                        │  Skip if: vehicle stationary, poor lighting
└───────┬────────────────┘
        │
        ▼
┌────────────────────────┐
│ Plate Detection        │  YOLOv5 object detection
│                        │  Finds license plate bounding boxes
│                        │  Confidence threshold: 0.6
└───────┬────────────────┘
        │
        ▼
┌────────────────────────┐
│ Image Preprocessing    │  • Grayscale conversion
│                        │  • Histogram equalization
│                        │  • Contrast enhancement
│                        │  • Rotation correction
└───────┬────────────────┘
        │
        ▼
┌────────────────────────┐
│ OCR (Tesseract)        │  Character recognition
│                        │  Trained on license plate fonts
│                        │  Output: "ABC1234"
└───────┬────────────────┘
        │
        ▼
┌────────────────────────┐
│ Validation & Scoring   │  • Format check (state-specific)
│                        │  • Character confidence (per letter)
│                        │  • Overall confidence: 0.0-1.0
└───────┬────────────────┘
        │
        ▼
    Confidence >= 0.7?
        │
   ┌────┴────┐
   │         │
  YES       NO
   │         │
   │         └──► Discard (don't log low-confidence reads)
   │
   ▼
┌────────────────────────┐
│ Hot-List Matching      │  Query local SQLite (10,000 plates)
│                        │  O(1) lookup via hash index
└───────┬────────────────┘
        │
    ┌───┴────┐
    │        │
  MATCH    NO MATCH
    │        │
    ├────────┴──────┐
    │               │
CRITICAL EVENT    NORMAL EVENT
    │               │
Upload immediately  Buffer for batch
(4G LTE)           (upload every 5 min or WiFi)
    │               │
    └───────┬───────┘
            │
            ▼
    Store in MinIO
    (image + metadata)
```

### Hot-List Management

```python
class HotListManager:
    def __init__(self):
        self.db = sqlite3.connect('/data/hot_list.db')
        self.create_tables()
        
    def create_tables(self):
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS hot_list (
                plate VARCHAR(20) PRIMARY KEY,
                state VARCHAR(2),
                reason VARCHAR(255),
                agency VARCHAR(100),
                case_number VARCHAR(50),
                severity VARCHAR(20),  -- CRITICAL, HIGH, MEDIUM
                added_date TIMESTAMP,
                expires TIMESTAMP
            )
        ''')
        
        # Hash index for O(1) lookups
        self.db.execute('''
            CREATE INDEX IF NOT EXISTS idx_plate ON hot_list(plate)
        ''')
    
    def sync_from_cloud(self):
        """Download latest hot-list from cloud server"""
        response = requests.get('https://fleet.company.com/api/hot-list')
        plates = response.json()
        
        # Atomic update
        self.db.execute('BEGIN TRANSACTION')
        self.db.execute('DELETE FROM hot_list')
        
        for plate in plates:
            self.db.execute('''
                INSERT INTO hot_list VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                plate['plate'],
                plate['state'],
                plate['reason'],
                plate['agency'],
                plate['case_number'],
                plate['severity'],
                plate['added_date'],
                plate['expires']
            ))
        
        self.db.execute('COMMIT')
        
        print(f"Hot-list synced: {len(plates)} plates")
    
    def check_plate(self, plate):
        """Check if plate is on hot-list"""
        cursor = self.db.execute('''
            SELECT * FROM hot_list WHERE plate = ?
        ''', (plate,))
        
        result = cursor.fetchone()
        
        if result:
            return {
                'match': True,
                'plate': result[0],
                'reason': result[2],
                'agency': result[3],
                'case_number': result[4],
                'severity': result[5]
            }
        else:
            return {'match': False}
```

---

## API Architecture

### REST API Endpoints

```
BASE URL: https://fleet.company.com/api/v1

GPS TRACKING
├── GET    /vehicles                    List all vehicles
├── GET    /vehicles/{id}               Get vehicle details
├── GET    /vehicles/{id}/position      Current position
├── GET    /vehicles/{id}/track         Historical track
│          ?start_time=...&end_time=...
├── POST   /positions                   Upload position batch (from vehicle)
└── GET    /positions/near              Find vehicles near point
           ?lat=...&lon=...&radius=...

LICENSE PLATE RECOGNITION
├── GET    /lpr/events                  List LPR events
├── GET    /lpr/events/{id}             Get event details
├── POST   /lpr/events                  Upload LPR event (from vehicle)
├── GET    /lpr/hot-list                Get hot-list
├── POST   /lpr/hot-list                Add plate to hot-list
└── DELETE /lpr/hot-list/{plate}        Remove from hot-list

VIDEO MANAGEMENT
├── GET    /videos                      List video clips
├── GET    /videos/{id}                 Get video metadata
├── GET    /videos/{id}/download        Download video file
├── POST   /videos/upload               Upload video clip (from vehicle)
└── DELETE /videos/{id}                 Delete video

DISPATCH (CAD INTEGRATION)
├── GET    /dispatch/incidents          List active incidents
├── GET    /dispatch/incidents/{id}     Get incident details
├── POST   /dispatch/assign             Assign vehicle to incident
├── PATCH  /dispatch/status             Update unit status
│          {vehicle_id, status: "ENROUTE" | "ONSCENE" | "AVAILABLE"}
└── POST   /dispatch/location           Update unit location for CAD

GEOFENCES
├── GET    /geofences                   List geofences
├── POST   /geofences                   Create geofence
├── PUT    /geofences/{id}              Update geofence
├── DELETE /geofences/{id}              Delete geofence
└── GET    /geofences/check             Check if point inside geofence

REPORTS
├── GET    /reports/vehicle-activity    Vehicle activity report
│          ?vehicle_id=...&date=...
├── GET    /reports/lpr-summary         LPR scan summary
├── GET    /reports/speeding            Speeding violations
└── GET    /reports/utilization         Fleet utilization metrics
```

---

## State Management

### Vehicle State Machine

```
┌────────────────────────────────────────────────────────────────┐
│                  VEHICLE STATE DIAGRAM                          │
└────────────────────────────────────────────────────────────────┘

    ┌───────────┐
    │  OFFLINE  │ ◄── Initial state / no connectivity
    └─────┬─────┘
          │
          │ Vehicle powered on, GPS acquired
          ▼
    ┌───────────┐
    │  ONLINE   │ ◄── Connected to fleet server
    └─────┬─────┘
          │
          │ Dispatch assignment received
          ▼
    ┌───────────┐
    │DISPATCHED │ ◄── Assigned to incident
    └─────┬─────┘
          │
          │ Officer accepts, starts driving
          ▼
    ┌───────────┐
    │  ENROUTE  │ ◄── Traveling to incident
    └─────┬─────┘
          │
          │ Arrives at incident location
          ▼
    ┌───────────┐
    │  ONSCENE  │ ◄── Handling incident
    └─────┬─────┘
          │
          │ Incident resolved
          ▼
    ┌───────────┐
    │ AVAILABLE │ ◄── Ready for next assignment
    └─────┬─────┘
          │
          │ Shift ends, vehicle returns to base
          ▼
    ┌───────────┐
    │   IDLE    │ ◄── Parked, engine off
    └───────────┘

Special States:
┌─────────────┐  Triggered by panic button
│   PANIC     │  or officer-down sensor
└─────────────┘

┌─────────────┐  Triggered by pursuit initiation
│  PURSUIT    │  (speed >80 mph + emergency lights)
└─────────────┘

┌─────────────┐  Triggered by maintenance flag
│ MAINTENANCE │  (vehicle in shop, unavailable)
└─────────────┘
```

---

## Dispatch & CAD Integration

### Incident Assignment Flow

```
┌──────────────────────────────────────────────────────────────┐
│           DISPATCH WORKFLOW                                   │
└──────────────────────────────────────────────────────────────┘

Step 1: Incident Created
┌─────────────┐
│ 911 Call    │ → Dispatcher creates incident
│ or Report   │    {
└─────────────┘      type: "Traffic Stop",
                     location: {lat, lon},
                     priority: "HIGH"
                   }

Step 2: Find Nearest Available Units
┌─────────────────────────────┐
│ Fleet Server                │
│ • Query all vehicles with   │
│   status = "AVAILABLE"      │
│ • Calculate distance to     │
│   incident (PostGIS query)  │
│ • Sort by distance          │
│ • Return top 3 candidates   │
└──────────┬──────────────────┘
           │
           │ Nearest: Vehicle #12 (0.8 miles, ETA 2 min)
           ▼
Step 3: Dispatch Assignment
┌─────────────────────────────┐
│ LibreDispatch CAD           │
│ • Assign Vehicle #12        │
│ • Send notification         │
│ • Update status board       │
└──────────┬──────────────────┘
           │
           │ NATS message: "dispatch.assign"
           │ Payload: {vehicle_id: 12, incident_id: 5678, ...}
           ▼
Step 4: Vehicle Notification
┌─────────────────────────────┐
│ Vehicle #12 (Jetson Nano)   │
│ • Subscribes to NATS        │
│ • Receives assignment       │
│ • Displays on tablet:       │
│   "ASSIGNED: Traffic Stop"  │
│   "123 Main St"             │
│   "ETA: 2 minutes"          │
│ • Alert sound + vibration   │
└──────────┬──────────────────┘
           │
           │ Officer presses "ACCEPT"
           ▼
Step 5: Status Update
┌─────────────────────────────┐
│ Vehicle sends status:       │
│ POST /api/dispatch/status   │
│ {                           │
│   vehicle_id: 12,           │
│   incident_id: 5678,        │
│   status: "ENROUTE"         │
│ }                           │
└──────────┬──────────────────┘
           │
           ▼
Step 6: GPS Tracking
Vehicle sends position every 5s
CAD map shows vehicle approaching incident
ETA updates dynamically

Step 7: Arrival
Vehicle arrives at incident location (within 100m)
System auto-detects: status → "ONSCENE"
Dispatch notified, timer starts

Step 8: Resolution
Officer completes task, presses "CLEAR"
Status → "AVAILABLE"
Vehicle ready for next assignment
```

---

## Video Management

### Video Lifecycle

```
Capture → Process → Store → Retrieve → Purge

1. CAPTURE (On-Vehicle)
   ├── Continuous recording (all cameras)
   ├── H.264 encoding, 5 Mbps
   ├── 1-minute segments
   └── Ring buffer: 72 hours

2. PROCESS (Event Detection)
   ├── Motion detection (skip static scenes)
   ├── Trigger events:
   │   • Hard braking (>0.5g deceleration)
   │   • Speeding (>speed limit + 10 mph)
   │   • Hot-list LPR hit
   │   • Panic button press
   │   • Officer manual tag
   └── Tag segments as "INCIDENT"

3. STORE (Upload to Cloud)
   ├── INCIDENT clips: Upload immediately (4G)
   ├── Normal footage: Upload via WiFi (bulk)
   ├── Destination: MinIO object storage
   └── Retention: 90 days (configurable)

4. RETRIEVE (On-Demand)
   ├── Web UI: Search by vehicle, date, event
   ├── API: Generate pre-signed URL
   ├── Download: Direct from MinIO
   └── Streaming: HLS/DASH for in-browser playback

5. PURGE (Automated)
   ├── After retention period (90 days default)
   ├── Or manual: Investigation closed
   └── Secure deletion (3-pass overwrite)
```

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Related Documents**:
- [OS-PATROL Network Topology](./OS-PATROL_Network_Topology.md)
- [OS-PATROL Technical Architecture](./OS-PATROL_Technical_Architecture.md)
