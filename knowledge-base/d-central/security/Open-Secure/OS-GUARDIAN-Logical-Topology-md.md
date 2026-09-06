---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: 457d8a37-559f-41fa-8fe1-80c9d6ecf18e
original_filename: OS-GUARDIAN_Logical_Topology.md
created_at: 2026-03-04T20:35:37.848975+00:00
content_hash: d2e42c1a450c
topic: "opensecure-topology-documentation-suite"
consolidated_into: docs/DC-OPENSECURE-TOPOLOGY-DOCUMENTATION-SUITE-RECONCILED-001.md
---

# OS-GUARDIAN Logical Topology
## Evidence Management System Architecture & Chain of Custody

**Document Type**: Logical Architecture Specification  
**Version**: 1.0  
**Date**: December 2024  
**Classification**: Technical Documentation  
**Audience**: Solution Architects, Evidence Custodians, Legal Teams

---

## Executive Summary

### Architectural Philosophy

OS-GUARDIAN implements a **forensically sound, legally defensible evidence management architecture** built on principles of:

- **Cryptographic Integrity**: Every piece of evidence has verifiable chain of custody
- **Immutability**: Evidence cannot be altered once captured
- **Auditability**: Every access logged with who, when, why, what
- **Compliance**: Meets CJIS Security Policy, FBI CJIS Audit, Brady disclosure
- **Performance**: Real-time indexing and search across petabytes

---

## Logical Architecture Overview

### Five-Layer Evidence Architecture

```
┌────────────────────────────────────────────────────────────────┐
│            LAYER 5: USER INTERFACES                            │
├────────────────────────────────────────────────────────────────┤
│ • Officer Portal (evidence.department.gov/officer)             │
│ • Investigator Portal (evidence.department.gov/investigator)   │
│ • Public Portal (evidence.department.gov/public - FOIA)        │
│ • Court Integration (electronic filing)                        │
│ • Mobile App (iOS/Android)                                     │
└────────────────────────┬───────────────────────────────────────┘
                         │ HTTPS / REST API
┌────────────────────────▼───────────────────────────────────────┐
│            LAYER 4: APPLICATION SERVICES                       │
├────────────────────────────────────────────────────────────────┤
│ ┌──────────────────┐  ┌──────────────────┐                    │
│ │ Evidence         │  │ Chain of         │                    │
│ │ Ingestion        │  │ Custody          │                    │
│ │ Service          │  │ Service          │                    │
│ └──────────────────┘  └──────────────────┘                    │
│                                                                 │
│ ┌──────────────────┐  ┌──────────────────┐                    │
│ │ Video Analytics  │  │ Redaction        │                    │
│ │ (AI Processing)  │  │ Engine           │                    │
│ └──────────────────┘  └──────────────────┘                    │
│                                                                 │
│ ┌──────────────────┐  ┌──────────────────┐                    │
│ │ Search/Discovery │  │ Access Control   │                    │
│ │ Engine           │  │ & Audit          │                    │
│ └──────────────────┘  └──────────────────┘                    │
└────────────────────────┬───────────────────────────────────────┘
                         │ Event Bus (Kafka)
┌────────────────────────▼───────────────────────────────────────┐
│            LAYER 3: DATA SERVICES                              │
├────────────────────────────────────────────────────────────────┤
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│ │ PostgreSQL   │  │ Elasticsearch│  │ MongoDB      │         │
│ │ (Metadata)   │  │ (Full-Text)  │  │ (Analytics)  │         │
│ └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                 │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│ │ Redis        │  │ TimescaleDB  │  │ Neo4j        │         │
│ │ (Cache)      │  │ (Metrics)    │  │ (Graph)      │         │
│ └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────────────┬───────────────────────────────────────┘
                         │
┌────────────────────────▼───────────────────────────────────────┐
│            LAYER 2: STORAGE SERVICES                           │
├────────────────────────────────────────────────────────────────┤
│ ┌──────────────────────────────────────────────────────────┐  │
│ │ Evidence Blob Storage (MinIO)                            │  │
│ │ • Original files (videos, images, audio, documents)      │  │
│ │ • Encrypted at rest (AES-256)                            │  │
│ │ • Content-addressable (hash-based IDs)                   │  │
│ │ • Tiered storage (hot/warm/cold)                         │  │
│ └──────────────────────────────────────────────────────────┘  │
│                                                                 │
│ ┌──────────────────────────────────────────────────────────┐  │
│ │ Blockchain Ledger (Hyperledger Fabric)                   │  │
│ │ • Immutable chain of custody records                     │  │
│ │ • Cryptographic proof of integrity                       │  │
│ │ • Tamper-evident audit trail                             │  │
│ └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬───────────────────────────────────────┘
                         │
┌────────────────────────▼───────────────────────────────────────┐
│            LAYER 1: EDGE DEVICES                               │
├────────────────────────────────────────────────────────────────┤
│ • Body Cameras (capture & local storage)                       │
│ • In-Car Cameras (dashcams, backseat)                          │
│ • Interview Room Recording Systems                             │
│ • Evidence Collection Tablets (crime scene)                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Entity Model

### Evidence Management Schema

```
┌──────────────┐
│   OFFICER    │
├──────────────┤
│ id           │ PK
│ badge_number │ UNIQUE
│ name         │
│ department   │
│ rank         │
│ assignment   │
└──────┬───────┘
       │ 1:N
       │
┌──────▼───────┐
│ BODY_CAMERA  │
├──────────────┤
│ id           │ PK
│ officer_id   │ FK
│ serial_num   │ UNIQUE
│ model        │
│ firmware_ver │
│ assigned_date│
└──────┬───────┘
       │ 1:N
       │
┌──────▼────────────┐
│  RECORDING        │
├───────────────────┤
│ id                │ PK
│ camera_id         │ FK
│ officer_id        │ FK
│ start_time        │
│ end_time          │
│ duration_seconds  │
│ file_size_bytes   │
│ file_hash_sha256  │ UNIQUE (content-addressable)
│ storage_location  │ (MinIO bucket + key)
│ encrypted         │ BOOLEAN
│ encryption_key_id │
│ gps_start         │ (lat, lon)
│ gps_end           │ (lat, lon)
│ tags              │ JSONB {incident, traffic_stop, etc.}
│ retention_until   │ (auto-delete date)
└──────┬────────────┘
       │ 1:N
       │
┌──────▼───────────┐
│  CASE            │
├──────────────────┤
│ id               │ PK
│ case_number      │ UNIQUE
│ incident_date    │
│ incident_type    │ (assault, theft, homicide, etc.)
│ status           │ (open, closed, court)
│ assigned_to      │ FK → INVESTIGATOR
│ prosecutor       │
│ court_case_num   │
└──────┬───────────┘
       │ N:M
       │
┌──────▼───────────┐
│ CASE_EVIDENCE    │ (Join table)
├──────────────────┤
│ case_id          │ FK
│ recording_id     │ FK
│ exhibit_number   │ (A-1, B-2, etc.)
│ added_by         │ FK → OFFICER
│ added_date       │
│ notes            │
└──────────────────┘

┌──────────────────┐
│ CHAIN_OF_CUSTODY │
├──────────────────┤
│ id               │ PK
│ recording_id     │ FK
│ timestamp        │
│ action           │ (captured, uploaded, viewed, copied, shared)
│ actor_id         │ FK → USER
│ actor_role       │ (officer, investigator, prosecutor, judge)
│ reason           │ (case investigation, court preparation)
│ ip_address       │
│ device_info      │
│ hash_before      │ SHA-256 (verify integrity)
│ hash_after       │ SHA-256
│ blockchain_tx    │ (Hyperledger transaction ID)
└──────────────────┘

┌──────────────────┐
│ ACCESS_LOG       │ (Audit trail)
├──────────────────┤
│ id               │ PK
│ recording_id     │ FK
│ user_id          │ FK
│ timestamp        │
│ action           │ (search, view, download, share)
│ duration_seconds │ (how long viewed)
│ success          │ BOOLEAN
│ denial_reason    │ (if access denied)
│ audit_flags      │ JSONB (unusual access patterns)
└──────────────────┘

┌──────────────────┐
│ VIDEO_ANALYTICS  │
├──────────────────┤
│ id               │ PK
│ recording_id     │ FK
│ analysis_type    │ (face_detection, object_detection, transcription)
│ results          │ JSONB
│ confidence       │ 0.0 - 1.0
│ processed_at     │
│ processing_time  │ (seconds)
└──────────────────┘
```

---

## Evidence Ingestion Flow

### Camera Dock Upload Process

```
┌────────────────────────────────────────────────────────────────┐
│           EVIDENCE INGESTION PIPELINE                           │
└────────────────────────────────────────────────────────────────┘

Step 1: Camera Docking
Officer docks camera at end of shift
        │
        │ USB 3.0 connection
        │ Camera detected by Evidence Management Software
        ▼
Step 2: Authentication & Verification
┌─────────────────────────────────────┐
│ Verify:                             │
│ • Officer badge (NFC scan)          │
│ • Camera serial number              │
│ • Firmware version (no tampering)   │
│ • Last sync timestamp               │
│ • Battery level (>20% for transfer) │
└──────────────┬──────────────────────┘
               │
               │ IF any check fails → Alert supervisor
               ▼
Step 3: File Discovery
┌─────────────────────────────────────┐
│ Scan camera storage:                │
│ /DCIM/                              │
│   ├── 2024-12-08_14-00-00.mp4      │
│   ├── 2024-12-08_15-30-15.mp4      │
│   └── 2024-12-08_16-45-22.mp4      │
│                                     │
│ New files: 3 recordings             │
│ Total size: 10.5 GB                 │
└──────────────┬──────────────────────┘
               │
               ▼
Step 4: Hash Calculation (Integrity)
For each file:
┌─────────────────────────────────────┐
│ Calculate SHA-256 hash:             │
│ hash = sha256(file_contents)       │
│                                     │
│ Compare with camera's embedded hash:│
│ IF hash_calculated == hash_embedded:│
│   → File is intact (no corruption)  │
│ ELSE:                               │
│   → Flag as corrupted, alert        │
│   → Quarantine file for manual      │
│     review                          │
└──────────────┬──────────────────────┘
               │
               ▼
Step 5: Metadata Extraction
┌─────────────────────────────────────┐
│ Parse video metadata:               │
│ • Start time: 2024-12-08T14:00:00Z  │
│ • End time: 2024-12-08T15:30:00Z    │
│ • Duration: 90 minutes              │
│ • Resolution: 1920×1080 @ 30 fps    │
│ • GPS start: (40.7128, -74.0060)    │
│ • GPS end: (40.7580, -73.9855)      │
│ • Officer ID: Badge #123            │
│ • Camera SN: BC-001234              │
│ • Tags: [traffic_stop, DUI_arrest]  │
└──────────────┬──────────────────────┘
               │
               ▼
Step 6: Database Entry
INSERT INTO recordings (
  camera_id,
  officer_id,
  start_time,
  end_time,
  duration_seconds,
  file_size_bytes,
  file_hash_sha256,
  storage_location,  -- NULL initially
  encrypted,
  gps_start,
  gps_end,
  tags
) VALUES (...)
RETURNING id;  -- Get recording_id

recording_id = 12345
               │
               ▼
Step 7: Encryption
┌─────────────────────────────────────┐
│ Generate unique encryption key:     │
│ data_key = random(32 bytes)         │
│                                     │
│ Encrypt file:                       │
│ encrypted_file = AES-256-GCM(       │
│   plaintext=file_contents,          │
│   key=data_key,                     │
│   iv=random(16 bytes)               │
│ )                                   │
│                                     │
│ Encrypt data key (envelope):        │
│ encrypted_key = RSA_OAEP(           │
│   data_key,                         │
│   public_key=HSM_master_key         │
│ )                                   │
│                                     │
│ Store: encrypted_file + encrypted_key│
└──────────────┬──────────────────────┘
               │
               ▼
Step 8: Upload to Object Storage (MinIO)
PUT /evidence/2024/12/08/recording-12345.mp4.enc
  Headers:
    X-Amz-Server-Side-Encryption: AES256
    X-Evidence-Hash: <SHA-256>
    X-Officer-ID: 123
    X-Recording-ID: 12345
        │
        │ S3 API
        ▼
MinIO Storage:
  Bucket: evidence-2024
  Key: 12/08/recording-12345.mp4.enc
  Size: 10.5 GB
  Encrypted: Yes
  Replicas: 3 (erasure coding EC 6+4)
               │
               │ Upload complete
               ▼
Step 9: Update Database
UPDATE recordings
SET storage_location = 's3://evidence-2024/12/08/recording-12345.mp4.enc',
    uploaded_at = NOW()
WHERE id = 12345;
               │
               ▼
Step 10: Chain of Custody Entry
INSERT INTO chain_of_custody (
  recording_id,
  timestamp,
  action,
  actor_id,
  actor_role,
  reason,
  hash_before,
  hash_after
) VALUES (
  12345,
  NOW(),
  'captured_and_uploaded',
  123,  -- Officer ID
  'officer',
  'End of shift routine upload',
  'abc123...',  -- Original hash
  'abc123...'   -- Same (no alteration)
);
               │
               ▼
Step 11: Blockchain Ledger Entry
┌─────────────────────────────────────┐
│ Hyperledger Fabric Transaction:    │
│ {                                   │
│   "recording_id": 12345,            │
│   "timestamp": "2024-12-08T...",    │
│   "hash": "abc123...",              │
│   "officer_id": 123,                │
│   "action": "upload",               │
│   "previous_block": "def456..."     │
│ }                                   │
│                                     │
│ Block added to ledger (immutable)   │
│ Transaction ID: tx-789              │
└──────────────┬──────────────────────┘
               │
               ▼
Step 12: AI Processing Queue
Publish to Kafka:
  Topic: "evidence.video.uploaded"
  Payload: {
    recording_id: 12345,
    storage_location: "s3://...",
    priority: "normal"
  }
        │
        │ Async processing
        ▼
Background Jobs:
├── Transcoding (generate 720p, 480p versions)
├── Thumbnail extraction (every 10 seconds)
├── Audio transcription (speech-to-text)
├── Face detection (blur for privacy)
└── Object detection (weapons, vehicles)
               │
               │ Processing complete (5-30 minutes)
               ▼
Step 13: Indexing (Elasticsearch)
Index document:
{
  "recording_id": 12345,
  "officer_id": 123,
  "officer_name": "John Smith",
  "start_time": "2024-12-08T14:00:00Z",
  "duration": 5400,  // seconds
  "location": {
    "lat": 40.7128,
    "lon": -74.0060
  },
  "tags": ["traffic_stop", "dui_arrest"],
  "transcription": "Officer: License and registration please...",
  "objects_detected": ["vehicle", "person", "license_plate"],
  "faces_count": 2
}
               │
               ▼
Step 14: Officer Notification
SMS to Officer 123:
"Your shift footage (3 recordings, 10.5 GB) has been uploaded.
 Recording IDs: 12345, 12346, 12347"
               │
               ▼
COMPLETE: Evidence securely stored and indexed
```

---

## Chain of Custody Management

### Custody Tracking

```python
class ChainOfCustodyManager:
    """
    Manages the legal chain of custody for all evidence
    """
    
    def record_custody_event(self, recording_id, user_id, action, reason):
        """
        Log every interaction with evidence
        """
        
        # Get current file hash (verify integrity)
        current_hash = self.calculate_hash(recording_id)
        
        # Get previous hash from last custody event
        previous_event = db.query(
            "SELECT hash_after FROM chain_of_custody "
            "WHERE recording_id = %s ORDER BY timestamp DESC LIMIT 1",
            (recording_id,)
        )
        
        previous_hash = previous_event['hash_after'] if previous_event else None
        
        # Verify integrity
        if previous_hash and previous_hash != current_hash:
            raise IntegrityViolationError(
                f"Hash mismatch! Evidence {recording_id} may be tampered."
            )
        
        # Log event to database
        custody_id = db.execute(
            "INSERT INTO chain_of_custody "
            "(recording_id, timestamp, action, actor_id, reason, "
            " hash_before, hash_after, blockchain_tx) "
            "VALUES (%s, NOW(), %s, %s, %s, %s, %s, %s) "
            "RETURNING id",
            (recording_id, action, user_id, reason, 
             previous_hash, current_hash, None)
        )
        
        # Write to blockchain (immutable ledger)
        blockchain_tx = self.write_to_blockchain({
            'recording_id': recording_id,
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'actor': user_id,
            'hash': current_hash,
            'custody_id': custody_id
        })
        
        # Update with blockchain TX ID
        db.execute(
            "UPDATE chain_of_custody SET blockchain_tx = %s WHERE id = %s",
            (blockchain_tx, custody_id)
        )
        
        # Publish event
        self.event_bus.publish('custody.recorded', {
            'recording_id': recording_id,
            'action': action,
            'actor': user_id
        })
        
        return custody_id
    
    def verify_chain(self, recording_id):
        """
        Verify complete chain of custody for a recording
        """
        
        events = db.query(
            "SELECT * FROM chain_of_custody "
            "WHERE recording_id = %s ORDER BY timestamp ASC",
            (recording_id,)
        )
        
        violations = []
        
        for i, event in enumerate(events):
            # Check hash continuity
            if i > 0:
                if events[i-1]['hash_after'] != event['hash_before']:
                    violations.append({
                        'event_id': event['id'],
                        'issue': 'Hash discontinuity',
                        'severity': 'CRITICAL'
                    })
            
            # Verify blockchain entry
            blockchain_valid = self.verify_blockchain_tx(
                event['blockchain_tx']
            )
            if not blockchain_valid:
                violations.append({
                    'event_id': event['id'],
                    'issue': 'Blockchain verification failed',
                    'severity': 'CRITICAL'
                })
        
        return {
            'valid': len(violations) == 0,
            'violations': violations,
            'event_count': len(events)
        }
    
    def generate_custody_report(self, recording_id):
        """
        Generate legal chain of custody report (for court)
        """
        
        recording = db.query(
            "SELECT * FROM recordings WHERE id = %s", (recording_id,)
        )
        
        events = db.query(
            "SELECT c.*, u.name as actor_name, u.badge_number "
            "FROM chain_of_custody c "
            "JOIN users u ON c.actor_id = u.id "
            "WHERE c.recording_id = %s ORDER BY c.timestamp",
            (recording_id,)
        )
        
        return {
            'recording': {
                'id': recording['id'],
                'officer': recording['officer_id'],
                'date': recording['start_time'],
                'duration': recording['duration_seconds'],
                'hash': recording['file_hash_sha256']
            },
            'custody_events': [
                {
                    'timestamp': e['timestamp'],
                    'action': e['action'],
                    'actor': f"{e['actor_name']} (Badge #{e['badge_number']})",
                    'reason': e['reason'],
                    'hash': e['hash_after'],
                    'blockchain_tx': e['blockchain_tx']
                }
                for e in events
            ],
            'integrity_verified': self.verify_chain(recording_id)['valid'],
            'generated_at': datetime.now().isoformat(),
            'generated_by': 'OS-GUARDIAN Evidence Management System'
        }
```

---

## Video Analytics Pipeline

### AI Processing Workflow

```
Video Uploaded → Kafka Queue
        │
        ▼
Consumer: Video Analytics Service (Python + TensorFlow)
        │
        ▼
┌─────────────────────────────────────────────────────────────┐
│                   ANALYTICS PIPELINE                         │
└─────────────────────────────────────────────────────────────┘

Stage 1: Video Decoding
├── Extract frames: 1 fps (1 frame per second)
├── Format: JPEG, 1280×720
└── Output: 5,400 frames (90-minute video)
        │
        ▼
Stage 2: Face Detection (YOLO v5)
For each frame:
  ├── Detect faces (bounding boxes)
  ├── Extract face embeddings (512-dim vectors)
  └── Output: face_locations, face_embeddings
        │
        ▼
Stage 3: Object Detection (YOLO v8)
For each frame:
  ├── Detect objects: person, vehicle, weapon, etc.
  ├── Confidence threshold: 0.7
  └── Output: object_type, bounding_box, confidence
        │
        ▼
Stage 4: License Plate Recognition (OpenALPR)
For frames with vehicles:
  ├── Detect license plates
  ├── OCR text recognition
  └── Output: plate_number, state, confidence
        │
        ▼
Stage 5: Audio Transcription (Whisper AI)
├── Extract audio track
├── Transcribe to text (speech-to-text)
├── Speaker diarization (who said what)
└── Output: transcript with timestamps
        │
        ▼
Stage 6: Scene Classification
├── Classify scene type: traffic_stop, foot_pursuit, interview
├── Detect events: gunshot, crash, breaking glass
└── Output: scene_type, events_detected
        │
        ▼
Stage 7: Results Storage
INSERT INTO video_analytics (
  recording_id,
  analysis_type,
  results,
  confidence,
  processed_at
) VALUES (
  12345,
  'comprehensive',
  {
    "faces": [
      {"timestamp": 0, "count": 2, "locations": [...]},
      {"timestamp": 10, "count": 1, "locations": [...]}
    ],
    "objects": {
      "person": 15,
      "vehicle": 3,
      "weapon": 0
    },
    "plates": ["ABC1234"],
    "transcript": "Officer: License please. Driver: ...",
    "scene_type": "traffic_stop",
    "duration": 5400
  },
  0.89,
  NOW()
);
        │
        ▼
Stage 8: Elasticsearch Indexing
Update document:
{
  "recording_id": 12345,
  "transcription": "full text of audio...",
  "objects_detected": ["person", "vehicle"],
  "plates_detected": ["ABC1234"],
  "faces_count_avg": 1.5,
  "scene_type": "traffic_stop"
}
        │
        ▼
COMPLETE: Video fully analyzed and searchable

Latency:
- Small video (5 min): 2-3 minutes
- Medium video (30 min): 10-15 minutes
- Large video (2 hours): 30-45 minutes
```

---

## Access Control & Redaction

### Privacy-Preserving Disclosure

```python
class EvidenceRedactionEngine:
    """
    Automated redaction for public disclosure (FOIA)
    """
    
    def redact_video(self, recording_id, redaction_level='public'):
        """
        Create redacted version of video for public release
        
        Redaction levels:
        - 'public': Heavy redaction (faces, audio, PII)
        - 'defense': Medium redaction (protect witnesses)
        - 'prosecution': Light redaction (minimal)
        - 'internal': No redaction (full access)
        """
        
        recording = self.get_recording(recording_id)
        analytics = self.get_analytics(recording_id)
        
        if redaction_level == 'public':
            return self.heavy_redaction(recording, analytics)
        elif redaction_level == 'defense':
            return self.medium_redaction(recording, analytics)
        elif redaction_level == 'prosecution':
            return self.light_redaction(recording, analytics)
        else:
            return recording  # No redaction
    
    def heavy_redaction(self, recording, analytics):
        """
        Public disclosure redaction
        """
        
        video_path = self.download_from_storage(recording['storage_location'])
        
        # Redaction rules
        redactions = []
        
        # 1. Blur all faces
        for face in analytics['faces']:
            redactions.append({
                'type': 'blur',
                'start_time': face['timestamp'],
                'duration': 1,  # 1 second
                'region': face['bounding_box']
            })
        
        # 2. Blur license plates
        for plate in analytics['plates']:
            redactions.append({
                'type': 'blur',
                'start_time': plate['timestamp'],
                'duration': 2,
                'region': plate['bounding_box']
            })
        
        # 3. Mute audio (except officer)
        redactions.append({
            'type': 'audio_filter',
            'action': 'mute_non_officer_speech'
        })
        
        # 4. Overlay watermark
        redactions.append({
            'type': 'watermark',
            'text': 'REDACTED - PUBLIC DISCLOSURE',
            'position': 'top_center'
        })
        
        # Apply redactions using FFmpeg
        redacted_video = self.apply_redactions(video_path, redactions)
        
        # Upload redacted version
        redacted_key = f"redacted/{recording['id']}_public.mp4"
        self.upload_to_storage(redacted_video, redacted_key)
        
        # Log redaction
        db.execute(
            "INSERT INTO redactions "
            "(recording_id, redaction_level, redacted_location, created_at) "
            "VALUES (%s, %s, %s, NOW())",
            (recording['id'], 'public', redacted_key)
        )
        
        return redacted_key
```

---

## API Architecture

### REST API Endpoints

```
BASE URL: https://evidence.department.gov/api/v1

RECORDINGS
├── GET    /recordings                      List recordings (filtered)
│          ?officer_id=123&date=2024-12-08&tags=traffic_stop
├── GET    /recordings/{id}                 Get recording metadata
├── GET    /recordings/{id}/stream          Stream video (authenticated)
├── GET    /recordings/{id}/download        Download original
├── POST   /recordings/{id}/redact          Generate redacted version
└── GET    /recordings/{id}/custody         Chain of custody report

SEARCH
├── POST   /search/videos                   Full-text search
│          Body: {
│            "query": "traffic stop on Main St",
│            "date_range": {"start": "...", "end": "..."},
│            "officer_ids": [123, 456],
│            "tags": ["dui"]
│          }
├── GET    /search/by-plate/{plate}         Find by license plate
├── GET    /search/by-location              Geospatial search
│          ?lat=40.7128&lon=-74.0060&radius=1000
└── POST   /search/by-face                  Face recognition search
           Body: {face_image: "base64..."}

CASES
├── GET    /cases                           List cases
├── GET    /cases/{id}                      Get case details
├── POST   /cases                           Create case
├── PUT    /cases/{id}                      Update case
├── POST   /cases/{id}/evidence             Add recording to case
└── GET    /cases/{id}/evidence             List case evidence

ACCESS CONTROL
├── POST   /access/request                  Request evidence access
├── GET    /access/requests/{id}            Get request status
├── POST   /access/approve                  Approve access (supervisor)
└── GET    /access/audit/{recording_id}     Access audit log

ANALYTICS
├── GET    /analytics/{recording_id}        Get analytics results
├── POST   /analytics/reprocess             Re-run analytics
└── GET    /analytics/search                Search by analytics
           ?objects=weapon&confidence>0.9

REPORTS
├── GET    /reports/officer-activity        Officer recording summary
├── GET    /reports/storage-usage           Storage capacity report
├── GET    /reports/compliance              Compliance audit report
└── GET    /reports/public-disclosure       FOIA request tracking
```

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Related Documents**:
- [OS-GUARDIAN Network Topology](./OS-GUARDIAN_Network_Topology.md)
- [OS-GUARDIAN Technical Architecture](./OS-GUARDIAN_Technical_Architecture.md)


<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Topics:**
- [[knowledge-base/_topics/opensecure-topology-documentation-suite|opensecure-topology-documentation-suite]]

**Consolidated into:**
- [[docs/DC-OPENSECURE-TOPOLOGY-DOCUMENTATION-SUITE-RECONCILED-001]]

<!-- AUTO-GENERATED RELATED END -->
