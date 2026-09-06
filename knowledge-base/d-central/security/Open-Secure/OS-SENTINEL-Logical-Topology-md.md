---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: a24f60e2-01fd-4b3e-82c2-dd2c47910023
original_filename: OS-SENTINEL_Logical_Topology.md
created_at: 2026-03-04T20:34:08.249743+00:00
content_hash: fc173e5b2151
topic: "opensecure-topology-documentation-suite"
consolidated_into: docs/DC-OPENSECURE-TOPOLOGY-DOCUMENTATION-SUITE-RECONCILED-001.md
---

# OS-SENTINEL Logical Topology
## AI-Powered Surveillance System Architecture & Video Analytics Pipeline

**Document Type**: Logical Architecture Specification  
**Version**: 1.0  
**Date**: December 2024  
**Classification**: Technical Documentation  
**Audience**: Solution Architects, Security Directors, System Designers

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Logical Architecture Overview](#logical-architecture-overview)
3. [Video Processing Pipeline](#video-processing-pipeline)
4. [AI Analytics Architecture](#ai-analytics-architecture)
5. [Object Detection & Tracking](#object-detection--tracking)
6. [Natural Language Query System](#natural-language-query-system)
7. [Event Management](#event-management)
8. [Data Flow Patterns](#data-flow-patterns)
9. [API Architecture](#api-architecture)
10. [Scalability & Performance](#scalability--performance)

---

## Executive Summary

### Architectural Philosophy

OS-SENTINEL implements a **multi-tier AI-powered video analytics architecture** that processes video streams in real-time while maintaining searchable historical archives. The system prioritizes:

- **Edge-Cloud Hybrid Processing**: Motion detection at camera, AI in data center
- **Real-Time Analytics**: Object detection, facial recognition, behavior analysis
- **Natural Language Interface**: Search video using plain English queries
- **Scalable Architecture**: Support 10 to 10,000+ cameras from single deployment
- **Privacy-Compliant**: Configurable retention, anonymization, audit trails

### Key Logical Concepts

| Concept | Definition | Implementation |
|---------|------------|----------------|
| **Video Stream** | Live camera feed | RTSP/ONVIF protocol |
| **Recording** | Archived video segment | H.264/H.265 in MinIO |
| **Detection Event** | AI-identified object/behavior | PostgreSQL + TimescaleDB |
| **Analytics Job** | Batch video analysis | Celery task queue |
| **NLQ (Natural Language Query)** | Text-based video search | LLM + vector embeddings |
| **Alert Rule** | Automated notification trigger | Rule engine |

---

## Logical Architecture Overview

### Five-Layer Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                    LAYER 5: PRESENTATION                            │
│                                                                     │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐  │
│  │  Web UI    │  │  Mobile    │  │  Video     │  │  Command   │  │
│  │  (React)   │  │  App       │  │  Wall      │  │  Center    │  │
│  │            │  │ (Flutter)  │  │  Display   │  │  Console   │  │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘  │
└────────────────────────────┬───────────────────────────────────────┘
                             │ HTTPS / WebSocket / HLS
┌────────────────────────────▼───────────────────────────────────────┐
│                    LAYER 4: APPLICATION SERVICES                    │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │               Shinobi Video Management                        │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │ │
│  │  │  Stream  │  │Recording │  │Playback  │  │  Live    │    │ │
│  │  │  Mgmt    │  │  Engine  │  │  API     │  │  Stream  │    │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │               AI Analytics Engine                             │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │ │
│  │  │ Object   │  │  Face    │  │ Behavior │  │  Scene   │    │ │
│  │  │Detection │  │Recognition│  │ Analysis │  │ Classify │    │ │
│  │  │(YOLOv8)  │  │(DeepFace)│  │  (CNN)   │  │  (ResNet)│    │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │           Natural Language Query (NLQ) Engine                 │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                   │ │
│  │  │   LLM    │  │  Vector  │  │  Query   │                   │ │
│  │  │  Parser  │  │Embeddings│  │ Executor │                   │ │
│  │  │ (GPT-4)  │  │(CLIP)    │  │          │                   │ │
│  │  └──────────┘  └──────────┘  └──────────┘                   │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬───────────────────────────────────────┘
                             │ Internal APIs
┌────────────────────────────▼───────────────────────────────────────┐
│                    LAYER 3: DATA SERVICES                           │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │PostgreSQL│  │ MinIO    │  │  Redis   │  │RabbitMQ  │         │
│  │+ pgvector│  │ Video    │  │  Cache   │  │ Message  │         │
│  │+ Time-   │  │ Storage  │  │          │  │  Queue   │         │
│  │  scale   │  │          │  │          │  │          │         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
└────────────────────────────┬───────────────────────────────────────┘
                             │ RTSP / ONVIF
┌────────────────────────────▼───────────────────────────────────────┐
│                    LAYER 2: RECORDING & ANALYTICS                   │
│                    (Video Processing Servers)                       │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  GPU-Accelerated Inference Servers (NVIDIA)                  │ │
│  │                                                                │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │ │
│  │  │  CUDA    │  │  CUDA    │  │  CUDA    │  │  CUDA    │    │ │
│  │  │ Worker 1 │  │ Worker 2 │  │ Worker 3 │  │ Worker 4 │    │ │
│  │  │(20 cams) │  │(20 cams) │  │(20 cams) │  │(20 cams) │    │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │ │
│  │                                                                │ │
│  │  Each worker: YOLOv8, DeepFace, ResNet models loaded          │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────────┬───────────────────────────────────────┘
                             │ Network / PoE
┌────────────────────────────▼───────────────────────────────────────┐
│                    LAYER 1: CAMERA LAYER                            │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │IP Camera │  │IP Camera │  │IP Camera │  │IP Camera │         │
│  │4MP 30fps │  │4MP 30fps │  │8MP 15fps │  │PTZ 4K    │         │
│  │(Indoor)  │  │(Outdoor) │  │(Parking) │  │(Perimeter│         │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Video Processing Pipeline

### Real-Time Stream Processing Flow

```
┌────────────────────────────────────────────────────────────────┐
│              VIDEO PROCESSING PIPELINE                          │
└────────────────────────────────────────────────────────────────┘

Step 1: Camera Capture
IP Camera (H.264, 4MP @ 30fps)
    │ Bitrate: 4 Mbps
    │ Resolution: 2560×1440
    │
    │ RTSP stream: rtsp://10.0.20.10:554/stream1
    │
    ▼
Step 2: Stream Ingestion
Shinobi Video Server
├── FFmpeg receives RTSP
├── Transcode if needed (H.265 for storage)
├── Generate multi-bitrate streams (HLS)
│   ├── High: 4 Mbps (original)
│   ├── Medium: 2 Mbps (1080p)
│   └── Low: 500 Kbps (480p)
└── Push frames to analytics queue

    │ Frame queue: RabbitMQ
    │ Every 3rd frame → analytics (10 fps)
    ▼
Step 3: AI Analytics (GPU Worker)
CUDA Worker Server (NVIDIA RTX 4090)
├── Load frame from queue
├── Run inference:
│   ├── YOLOv8: Object detection (15ms)
│   ├── DeepFace: Face detection (20ms)
│   ├── ResNet: Scene classification (10ms)
│   └── Custom: Behavior analysis (25ms)
├── Total: ~70ms per frame
└── Process 14 frames/second

    │ Detected objects:
    │ {
    │   "timestamp": "2024-12-08T14:23:45.123Z",
    │   "camera_id": 10,
    │   "detections": [
    │     {"class": "person", "confidence": 0.95, "bbox": [...]},
    │     {"class": "vehicle", "confidence": 0.89, "bbox": [...]}
    │   ],
    │   "faces": [
    │     {"bbox": [...], "embedding": [...], "match": "unknown"}
    │   ]
    │ }
    │
    ▼
Step 4: Event Generation
Detection Events Stored:
PostgreSQL + TimescaleDB
├── INSERT INTO detections
├── INSERT INTO tracking (object trajectories)
├── UPDATE statistics (counts, heatmaps)
└── Trigger alerts if rules match

    │
    ├──► Alert Engine
    │    IF person in restricted zone:
    │      Send notification
    │
    └──► Dashboard Update
         WebSocket push to connected clients

Step 5: Recording Storage
Video segments stored continuously:
MinIO Object Storage
├── Path: /videos/{camera_id}/{date}/{hour}/{minute}.mp4
├── Segment size: 1 minute chunks
├── Retention: 30-90 days (configurable)
└── Indexed by: timestamp, camera, events

Total Latency: Camera → Alert in <2 seconds
```

---

## AI Analytics Architecture

### Multi-Model Inference Pipeline

```
┌────────────────────────────────────────────────────────────────┐
│              AI MODEL ARCHITECTURE                              │
└────────────────────────────────────────────────────────────────┘

Input Frame (1920×1080 RGB)
        │
        ▼
┌────────────────────────┐
│ Model 1: YOLOv8        │  Object Detection
│ ---------------------- │
│ Input: 640×640         │  Resize + normalize
│ Output: Bounding boxes │  80 COCO classes
│ Inference: 15ms        │  (person, car, dog, etc.)
│ GPU Memory: 2GB        │
└───────┬────────────────┘
        │ Detected: 2 persons, 1 vehicle
        ▼
┌────────────────────────┐
│ Model 2: DeepFace      │  Face Detection & Recognition
│ ---------------------- │
│ Input: Person crops    │  From YOLO bounding boxes
│ Output: Face embeddings│  512-dim vectors
│ Inference: 20ms/face   │
│ GPU Memory: 1GB        │
└───────┬────────────────┘
        │ Detected: 1 face, embedding: [0.23, -0.15, ...]
        │ Compare to: Known faces database (1,000 entries)
        │ Match: "John Doe" (similarity: 0.87)
        ▼
┌────────────────────────┐
│ Model 3: ResNet-50     │  Scene Classification
│ ---------------------- │
│ Input: Full frame      │
│ Output: Scene type     │  Indoor/outdoor, day/night
│ Inference: 10ms        │  Empty/crowded, etc.
│ GPU Memory: 500MB      │
└───────┬────────────────┘
        │ Scene: "outdoor parking lot, daytime, moderate activity"
        ▼
┌────────────────────────┐
│ Model 4: Custom CNN    │  Behavior Analysis
│ ---------------------- │
│ Input: Temporal frames │  Last 30 frames (1 second)
│ Output: Behaviors      │  Walking, running, loitering
│ Inference: 25ms        │  Fighting, falling, etc.
│ GPU Memory: 1.5GB      │
└───────┬────────────────┘
        │ Behavior: "Person loitering (60 seconds)"
        ▼
Final Analytics Result:
{
  "timestamp": "2024-12-08T14:23:45Z",
  "camera_id": 10,
  "scene": {
    "type": "outdoor_parking",
    "lighting": "daytime",
    "activity_level": "moderate"
  },
  "objects": [
    {
      "id": "obj_001",
      "class": "person",
      "confidence": 0.95,
      "bbox": [100, 200, 50, 150],
      "tracking_id": "track_12345"
    }
  ],
  "faces": [
    {
      "person_id": "obj_001",
      "match": "John Doe",
      "confidence": 0.87
    }
  ],
  "behaviors": [
    {
      "person_id": "obj_001",
      "type": "loitering",
      "duration": 60
    }
  ],
  "alerts": [
    {
      "type": "unauthorized_person",
      "severity": "medium",
      "message": "Unknown person loitering in parking lot"
    }
  ]
}

GPU Resource Allocation (Per Worker):
├── Total VRAM: 24GB (RTX 4090)
├── YOLOv8: 2GB
├── DeepFace: 1GB
├── ResNet: 500MB
├── Custom CNN: 1.5GB
├── Frame buffers: 1GB
└── Available: 18GB (for 4× concurrent streams)

Each worker processes: 20 cameras @ 10 fps = 200 frames/sec
```

---

## Object Detection & Tracking

### Multi-Object Tracking (MOT)

```python
class ObjectTracker:
    def __init__(self):
        self.active_tracks = {}  # tracking_id → track_data
        self.next_track_id = 1
        
    def update(self, frame_detections, timestamp):
        """Update tracks with new frame detections"""
        
        # Step 1: Match new detections to existing tracks
        matches = self.match_detections_to_tracks(frame_detections)
        
        # Step 2: Update matched tracks
        for detection, track_id in matches:
            self.update_track(track_id, detection, timestamp)
        
        # Step 3: Create new tracks for unmatched detections
        unmatched = self.get_unmatched_detections(frame_detections, matches)
        for detection in unmatched:
            self.create_new_track(detection, timestamp)
        
        # Step 4: Remove stale tracks (no update in 2 seconds)
        self.remove_stale_tracks(timestamp)
        
        return self.active_tracks
    
    def match_detections_to_tracks(self, detections):
        """Match using IoU (Intersection over Union) + appearance"""
        matches = []
        
        for detection in detections:
            best_match = None
            best_score = 0.0
            
            for track_id, track in self.active_tracks.items():
                # Calculate IoU (position similarity)
                iou = self.calculate_iou(detection.bbox, track.predicted_bbox)
                
                # Calculate appearance similarity (feature vector)
                appearance = cosine_similarity(
                    detection.features,
                    track.features
                )
                
                # Combined score (weighted)
                score = 0.7 * iou + 0.3 * appearance
                
                if score > 0.5 and score > best_score:
                    best_match = track_id
                    best_score = score
            
            if best_match:
                matches.append((detection, best_match))
        
        return matches
    
    def create_new_track(self, detection, timestamp):
        """Create new track for unmatched detection"""
        track_id = f"track_{self.next_track_id}"
        self.next_track_id += 1
        
        self.active_tracks[track_id] = {
            'id': track_id,
            'class': detection.class_name,
            'first_seen': timestamp,
            'last_seen': timestamp,
            'positions': [detection.bbox],
            'features': detection.features,
            'trajectory': [detection.center],
            'velocity': (0, 0),
            'predicted_bbox': detection.bbox
        }
        
        # Store in database
        self.db.execute('''
            INSERT INTO object_tracks (id, camera_id, class, first_seen)
            VALUES (?, ?, ?, ?)
        ''', (track_id, detection.camera_id, detection.class_name, timestamp))
    
    def calculate_trajectory(self, track):
        """Analyze object movement pattern"""
        positions = track['trajectory']
        
        if len(positions) < 10:
            return None  # Not enough data
        
        # Calculate velocity
        dx = positions[-1][0] - positions[-10][0]
        dy = positions[-1][1] - positions[-10][1]
        velocity = (dx / 10, dy / 10)  # pixels per frame
        
        # Detect patterns
        if self.is_loitering(positions):
            return {'type': 'loitering', 'duration': len(positions) / 10}
        
        if self.is_running(velocity):
            return {'type': 'running', 'speed': math.sqrt(dx**2 + dy**2)}
        
        return {'type': 'walking', 'velocity': velocity}

# Usage:
tracker = ObjectTracker()

for frame in video_stream:
    detections = yolo_detect(frame)
    tracks = tracker.update(detections, frame.timestamp)
    
    # Check for alerts
    for track_id, track in tracks.items():
        trajectory = tracker.calculate_trajectory(track)
        
        if trajectory and trajectory['type'] == 'loitering':
            if trajectory['duration'] > 60:  # 60 seconds
                send_alert(f"Loitering detected: {track_id}")
```

---

## Natural Language Query System

### LLM-Powered Video Search Architecture

```
┌────────────────────────────────────────────────────────────────┐
│           NATURAL LANGUAGE QUERY (NLQ) SYSTEM                   │
└────────────────────────────────────────────────────────────────┘

User Query: "Show me when someone entered the parking lot this morning"

Step 1: Query Understanding (LLM)
GPT-4 parses natural language:
    │
    │ Prompt: "Convert this to structured query:
    │          'Show me when someone entered the parking lot this morning'"
    │
    ▼
LLM Output (JSON):
{
  "entities": {
    "object": "person",
    "location": "parking lot",
    "action": "entered",
    "time": "this morning"
  },
  "temporal_range": {
    "start": "2024-12-08T06:00:00Z",
    "end": "2024-12-08T12:00:00Z"
  },
  "spatial_filter": {
    "zone": "parking_lot_entrance",
    "camera_ids": [5, 6]
  }
}

Step 2: Vector Similarity Search (CLIP Embeddings)
Query embedding: "person entering parking lot"
    │
    │ CLIP model generates 512-dim vector
    │ Vector: [0.23, -0.15, 0.87, ...]
    │
    ▼
Search vector database (pgvector):
SELECT 
    event_id,
    timestamp,
    camera_id,
    1 - (embedding <=> query_vector) as similarity
FROM detection_events
WHERE timestamp BETWEEN '2024-12-08 06:00' AND '2024-12-08 12:00'
  AND camera_id IN (5, 6)
  AND class = 'person'
ORDER BY similarity DESC
LIMIT 100;

Step 3: Temporal Reasoning
Filter events by action: "entered"
    │
    │ Analyze trajectories:
    │ • Find tracks that crossed entrance line
    │ • Direction: outside → inside
    │ • Ignore: inside → outside (exit, not entrance)
    │
    ▼
Matched Events:
├── Event 1: 06:23:15 - Person entered (track_12345)
├── Event 2: 07:45:22 - Person entered (track_12389)
├── Event 3: 09:12:08 - Person entered (track_12401)
└── Event 4: 11:03:55 - Person entered (track_12456)

Step 4: Result Generation
For each event, fetch:
├── Video clip (30 seconds: 15s before + 15s after)
├── Thumbnail (snapshot at event time)
├── Metadata (camera, location, track info)
└── Related events (same track in other cameras)

Step 5: Response to User
Web UI displays:
┌──────────────────────────────────────────────┐
│  Found 4 matches for your query:             │
│                                              │
│  ┌────────┐  06:23 AM - Parking Entrance   │
│  │[IMAGE]│  Person entered through main gate │
│  └────────┘  Camera: Entrance-05             │
│              [Watch Video]                   │
│                                              │
│  ┌────────┐  07:45 AM - Parking Entrance   │
│  │[IMAGE]│  Person entered through side gate │
│  └────────┘  Camera: Side-06                 │
│              [Watch Video]                   │
│  ...                                         │
└──────────────────────────────────────────────┘
```

### NLQ Query Examples

```
Query: "Show me all blue cars that entered today"
→ Object: vehicle
→ Color: blue
→ Time: today (00:00 - 23:59)
→ Action: entered (trajectory analysis)

Query: "Find when the package was delivered to the front desk"
→ Object: package
→ Location: front desk
→ Action: delivered (object appeared + person interaction)
→ Time: unspecified (search last 7 days)

Query: "Was there anyone in the server room last night?"
→ Object: person
→ Location: server room
→ Time: last night (18:00 - 06:00)
→ Action: presence (any detection)

Query: "Show me people running in the hallway this week"
→ Object: person
→ Behavior: running (velocity > threshold)
→ Location: hallway
→ Time: this week

Query: "Who accessed the restricted area without authorization?"
→ Object: person
→ Location: restricted area
→ Authorization: check against access control logs
→ Time: unspecified
```

---

## Event Management

### Alert Rule Engine

```python
class AlertRuleEngine:
    def __init__(self):
        self.rules = self.load_rules()
        
    def load_rules(self):
        """Load alert rules from database"""
        return [
            {
                'id': 1,
                'name': 'Unauthorized Access',
                'conditions': {
                    'object_class': 'person',
                    'zone': 'restricted_area',
                    'authorized': False
                },
                'actions': [
                    {'type': 'email', 'to': 'security@company.com'},
                    {'type': 'sms', 'to': '+1234567890'},
                    {'type': 'popup', 'client': 'security_console'}
                ],
                'cooldown': 300  # Don't alert again for 5 minutes
            },
            {
                'id': 2,
                'name': 'Loitering Detection',
                'conditions': {
                    'behavior': 'loitering',
                    'duration': 60,  # seconds
                    'zone': 'entrance'
                },
                'actions': [
                    {'type': 'email', 'to': 'security@company.com'}
                ]
            },
            {
                'id': 3,
                'name': 'After-Hours Activity',
                'conditions': {
                    'object_class': 'person',
                    'time_range': ('22:00', '06:00'),
                    'zones': ['office_floor_2', 'office_floor_3']
                },
                'actions': [
                    {'type': 'sms', 'to': '+1234567890'},
                    {'type': 'record_clip', 'duration': 60}
                ]
            }
        ]
    
    def evaluate(self, detection_event):
        """Check if event matches any alert rules"""
        
        for rule in self.rules:
            if self.matches_conditions(detection_event, rule['conditions']):
                # Check cooldown
                if self.is_in_cooldown(rule['id'], detection_event.camera_id):
                    continue
                
                # Trigger alert
                self.trigger_alert(rule, detection_event)
                
                # Set cooldown
                self.set_cooldown(rule['id'], detection_event.camera_id, rule['cooldown'])
    
    def matches_conditions(self, event, conditions):
        """Check if event matches rule conditions"""
        
        # Check object class
        if 'object_class' in conditions:
            if event.object_class != conditions['object_class']:
                return False
        
        # Check zone
        if 'zone' in conditions:
            if not self.is_in_zone(event.location, conditions['zone']):
                return False
        
        # Check time range
        if 'time_range' in conditions:
            if not self.is_in_time_range(event.timestamp, conditions['time_range']):
                return False
        
        # Check behavior
        if 'behavior' in conditions:
            if event.behavior != conditions['behavior']:
                return False
        
        return True
    
    def trigger_alert(self, rule, event):
        """Execute alert actions"""
        
        alert_message = f"Alert: {rule['name']} - {event.description}"
        
        for action in rule['actions']:
            if action['type'] == 'email':
                send_email(action['to'], alert_message, event.video_clip_url)
            
            elif action['type'] == 'sms':
                send_sms(action['to'], alert_message)
            
            elif action['type'] == 'popup':
                websocket_send(action['client'], {
                    'type': 'alert',
                    'message': alert_message,
                    'event': event.to_dict()
                })
            
            elif action['type'] == 'record_clip':
                record_video_clip(
                    event.camera_id,
                    duration=action['duration'],
                    tag='alert'
                )
```

---

## API Architecture

### REST API Endpoints

```
BASE URL: https://surveillance.company.com/api/v1

CAMERAS
├── GET    /cameras                     List all cameras
├── GET    /cameras/{id}                Get camera details
├── GET    /cameras/{id}/live           Live stream URL (HLS)
├── GET    /cameras/{id}/snapshot       Latest snapshot
├── POST   /cameras                     Add camera
└── PATCH  /cameras/{id}                Update camera settings

RECORDINGS
├── GET    /recordings                  List recordings
│          ?camera_id=...&start=...&end=...
├── GET    /recordings/{id}             Get recording metadata
├── GET    /recordings/{id}/download    Download video file
├── GET    /recordings/{id}/thumbnail   Get thumbnail
└── DELETE /recordings/{id}             Delete recording

DETECTIONS / EVENTS
├── GET    /events                      List detection events
│          ?camera_id=...&class=...&start=...&end=...
├── GET    /events/{id}                 Get event details
├── GET    /events/search               Search events
│          ?query=...                   (supports filters)
└── GET    /events/heatmap              Generate heatmap data

NATURAL LANGUAGE QUERY
├── POST   /nlq/query                   Submit NLQ query
│          {"query": "show me when..."}
├── GET    /nlq/results/{query_id}      Get query results
└── GET    /nlq/history                 User's query history

ANALYTICS
├── GET    /analytics/summary           Daily summary stats
│          ?date=...
├── GET    /analytics/trajectory        Object trajectory data
│          ?track_id=...
├── GET    /analytics/occupancy         Zone occupancy over time
└── GET    /analytics/demographics      People counting stats

ALERTS
├── GET    /alerts/rules                List alert rules
├── POST   /alerts/rules                Create alert rule
├── PUT    /alerts/rules/{id}           Update rule
├── DELETE /alerts/rules/{id}           Delete rule
└── GET    /alerts/history              Alert history

FACE RECOGNITION
├── POST   /faces/enroll                Enroll new face
│          (multipart: name, photos)
├── GET    /faces/gallery               List enrolled faces
├── DELETE /faces/{id}                  Remove face
└── GET    /faces/matches               Recent face matches
```

---

## Data Flow Patterns

### Historical Video Playback

```
User Request: "Play video from Camera 5, Dec 8 2PM-3PM"
    │
    ▼
Step 1: Query recordings database
SELECT file_path, duration, timestamp
FROM recordings
WHERE camera_id = 5
  AND timestamp >= '2024-12-08 14:00:00'
  AND timestamp < '2024-12-08 15:00:00'
ORDER BY timestamp;

Results:
├── /videos/5/2024-12-08/14/00.mp4 (1 minute)
├── /videos/5/2024-12-08/14/01.mp4 (1 minute)
├── ...
└── /videos/5/2024-12-08/14/59.mp4 (1 minute)
(60 segments total)

Step 2: Generate playlist (HLS)
Create m3u8 playlist:
#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:60
#EXTINF:60.0,
https://cdn.company.com/videos/5/2024-12-08/14/00.mp4
#EXTINF:60.0,
https://cdn.company.com/videos/5/2024-12-08/14/01.mp4
...
#EXT-X-ENDLIST

Step 3: Stream to client
├── Client: video.js player
├── Protocol: HLS over HTTPS
├── Buffering: 10 seconds
└── Playback: Smooth 30fps

User can:
├── Seek to any timestamp
├── Adjust playback speed (0.5×, 1×, 2×)
├── Enable motion-only playback (skip idle periods)
└── Overlay detections (bounding boxes from database)
```

---

## Scalability & Performance

### Horizontal Scaling Strategy

```
┌────────────────────────────────────────────────────────────┐
│            SCALABILITY ARCHITECTURE                         │
└────────────────────────────────────────────────────────────┘

Component: GPU Workers (AI Inference)
├── Scaling: Add GPU servers as camera count grows
├── Ratio: 1 GPU worker per 20 cameras (@ 10fps analytics)
├── Load balancing: Camera-to-worker assignment via RabbitMQ
└── Capacity: 100 cameras = 5 GPU workers

Component: Recording Servers
├── Scaling: Add servers based on storage write throughput
├── Ratio: 1 server per 50 cameras (@ 4 Mbps each = 200 Mbps)
├── Distribution: Cameras assigned to servers (sticky assignment)
└── Capacity: 100 cameras = 2 recording servers

Component: Database (PostgreSQL + TimescaleDB)
├── Vertical scaling: Up to 10,000 events/sec on single server
├── Read replicas: Add replicas for analytics queries
├── Partitioning: By time (daily partitions, auto-drop old data)
└── Capacity: 1 primary + 2 replicas handles 500 cameras

Component: Object Storage (MinIO)
├── Scaling: Erasure-coded cluster, add nodes as needed
├── Ratio: 1 TB per camera per month @ 30-day retention
├── Example: 100 cameras × 1 TB = 100 TB usable
│            EC 4+2 = 150 TB raw
└── Capacity: 8-node cluster = 320 TB usable

Total Infrastructure (100 Cameras):
├── GPU Workers: 5× (NVIDIA RTX 4090 servers)
├── Recording Servers: 2× (high disk throughput)
├── PostgreSQL: 1 primary + 2 replicas
├── MinIO: 8-node cluster (40TB each)
├── Load Balancer: 1× (HAProxy)
└── Total Cost: ~$150K (hardware) + $5K/mo (ops)
```

### Performance Metrics

| Metric | Target | Typical | Notes |
|--------|--------|---------|-------|
| Detection latency | <2s | 1.2s | Frame → Alert |
| Video playback start | <1s | 0.5s | Click → First frame |
| NLQ query response | <5s | 3s | Query → Results |
| Live stream delay | <5s | 2s | Camera → Browser |
| API response (simple) | <100ms | 50ms | GET /cameras |
| API response (search) | <500ms | 300ms | GET /events/search |

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Related Documents**:
- [OS-SENTINEL Network Topology](./OS-SENTINEL_Network_Topology.md)
- [OS-SENTINEL Technical Architecture](./OS-SENTINEL_Technical_Architecture.md)

**Completion Status**: This completes the 10-document OpenSecure Topology Suite.


<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Topics:**
- [[knowledge-base/_topics/opensecure-topology-documentation-suite|opensecure-topology-documentation-suite]]

**Consolidated into:**
- [[docs/DC-OPENSECURE-TOPOLOGY-DOCUMENTATION-SUITE-RECONCILED-001]]

<!-- AUTO-GENERATED RELATED END -->
