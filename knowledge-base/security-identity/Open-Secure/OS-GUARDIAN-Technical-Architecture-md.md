---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: a6340737-4013-4e35-a00b-9613eae61220
original_filename: OS-GUARDIAN_Technical_Architecture.md
created_at: 2026-03-04T20:30:19.372173+00:00
content_hash: 19c920013b67topic: lag-kubernetes-interval
topic: opensecure-guardian-sentinel-architecture
---

# OS-GUARDIAN - Complete Technical Architecture
## Body-Worn Camera & Evidence Management Platform

**Document Type**: Technical Architecture
**Version**: 1.0
**Date**: December 2024
**Classification**: Technical Documentation
**Audience**: Technical Leaders, Evidence Management Specialists, System Architects, DevOps Engineers

---

## Table of Contents

1. [Executive Technical Summary](#executive-technical-summary)
2. [System Architecture Overview](#system-architecture-overview)
3. [Core Technology Deep-Dive](#core-technology-deep-dive)
4. [Component Architecture](#component-architecture)
5. [Body Camera Hardware Architecture](#body-camera-hardware-architecture)
6. [Data Architecture](#data-architecture)
7. [Video Ingestion Pipeline](#video-ingestion-pipeline)
8. [Blockchain Chain-of-Custody](#blockchain-chain-of-custody)
9. [Security Architecture](#security-architecture)
10. [Network Architecture](#network-architecture)
11. [Scalability & Performance](#scalability--performance)
12. [High Availability & Redundancy](#high-availability--redundancy)
13. [Integration Architecture](#integration-architecture)
14. [Deployment Models](#deployment-models)
15. [Monitoring & Operations](#monitoring--operations)
16. [Compliance Frameworks](#compliance-frameworks)
17. [Disaster Recovery](#disaster-recovery)
18. [Cost Modeling at Scale](#cost-modeling-at-scale)

---

## Executive Technical Summary

### Platform Overview

OS-GUARDIAN is an enterprise-grade, open-source body-worn camera and evidence management platform designed for organizations requiring legally admissible video evidence with cryptographic chain-of-custody verification, complete data sovereignty, and no vendor lock-in.

**Core Design Principles:**

- **Edge Recording**: Raspberry Pi-based cameras with local storage (no network dependency)
- **Blockchain Chain-of-Custody**: Immutable audit trail with cryptographic signatures
- **Evidence Integrity**: SHA256 hashing, tamper detection, legal admissibility
- **Zero Vendor Lock-In**: Open standards (H.264, PostgreSQL, S3, REST APIs)
- **Privacy-First**: On-premise storage, configurable retention, redaction tools
- **Hardware Flexibility**: Runs on Raspberry Pi Zero 2 W to Pi 4 (scalable performance)
- **Database-Centric**: PostgreSQL + TimescaleDB for events, MinIO for video storage
- **API-First**: REST/MQTT APIs for all operations
- **Compliance-Ready**: CJIS, HIPAA, FOIA, legal admissibility standards

### Scale Characteristics

| Deployment Scale | Cameras | Storage | Architecture | Use Case |
|------------------|---------|---------|--------------|----------|
| **Small** | 1-20 | 1-4TB SSD | Single server | Small security team, retail stores |
| **Medium** | 20-100 | 10-50TB NAS | Multi-server cluster | Police dept, hospital security |
| **Enterprise** | 100-1,000 | 100TB-1PB SAN | Distributed hub-spoke | City police, university campus |
| **Multi-Site** | 1,000-10,000+ | Multi-PB object storage | Regional federation | State police, national retail chain |

### Technology Stack

**Body Camera Platform:**
- Raspberry Pi Zero 2 W / Pi 4 (ARM Cortex-A53/A72)
- Raspberry Pi Camera Module v2/v3 (1080p @ 30 FPS, 4K optional)
- PiCamera Python library (video capture)
- FFmpeg (H.264 encoding, compression)
- GPS module (USB, u-blox NEO-6M)
- WiFi/Bluetooth (networking, auto-sync)

**Evidence Server:**
- Ubuntu Server 22.04 LTS / Debian 12
- Docker + Docker Compose (containerization)
- PostgreSQL 15+ with TimescaleDB (metadata, COC records)
- MinIO (S3-compatible video object storage)
- MQTT (Eclipse Mosquitto, event streaming)
- FastAPI (Python REST API server)
- React (web UI)

**Blockchain:**
- Hyperledger Fabric 2.5+ (permissioned blockchain)
- Ethereum (alternative, public ledger)
- IPFS (InterPlanetary File System, decentralized storage)
- OpenTimestamps (Bitcoin blockchain timestamping)

**Video Processing:**
- FFmpeg 6.0+ (transcoding, analysis)
- MediaMTX (RTSP/WebRTC live streaming)
- OpenCV (video analysis, redaction, face blur)

**Integration Protocols:**
- REST API (JSON over HTTPS)
- MQTT (pub/sub events)
- WebSocket (real-time streams)
- S3 API (MinIO, AWS S3, Azure Blob)
- gRPC (high-performance service-to-service)

---

## System Architecture Overview

### Layered Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Presentation Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Web UI     │  │  Mobile App  │  │   Admin      │             │
│  │  (React +    │  │  (Flutter)   │  │   Console    │             │
│  │   WebRTC)    │  │              │  │  (Grafana)   │             │
│  │              │  │              │  │              │             │
│  │ • Evidence   │  │ • Camera     │  │ • Analytics  │             │
│  │   Library    │  │   Control    │  │ • Reports    │             │
│  │ • Playback   │  │ • Live View  │  │ • Audit Logs │             │
│  │ • Export     │  │ • Alerts     │  │ • Compliance │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                        HTTPS/WSS/WebRTC (TLS 1.3)
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      API Gateway Layer                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                   NGINX / Traefik                             │  │
│  │  • JWT/OAuth2 Authentication                                 │  │
│  │  • Rate Limiting (100 req/min per user)                      │  │
│  │  • Audit Logging (all API requests)                          │  │
│  │  • TLS Termination (TLS 1.3)                                 │  │
│  │  • IP Whitelisting (optional)                                │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                          Internal APIs
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Application Services Layer                        │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │ Evidence  │  │Blockchain │  │ MediaMTX  │  │   User    │       │
│  │Ingestion  │  │Chain-of-  │  │ Streaming │  │   Auth    │       │
│  │ Service   │  │ Custody   │  │  Server   │  │ (Keycloak)│       │
│  │           │  │  Service  │  │           │  │           │       │
│  │ • Upload  │  │ • SHA256  │  │ • WebRTC  │  │ • SSO     │       │
│  │ • Hash    │  │ • Signing │  │ • RTSP    │  │ • RBAC    │       │
│  │ • Verify  │  │ • Ledger  │  │ • HLS     │  │ • MFA     │       │
│  │ • Index   │  │ • Audit   │  │ • Live    │  │ • Audit   │       │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘       │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │  Storage  │  │   Event   │  │  Redaction│  │  Alert    │       │
│  │  Manager  │  │  Engine   │  │  Service  │  │  Service  │       │
│  │           │  │           │  │           │  │           │       │
│  │ • Tiering │  │ • Triggers│  │ • Face    │  │ • Email   │       │
│  │ • Cleanup │  │ • Metadata│  │   Blur    │  │ • SMS     │       │
│  │ • Backup  │  │ • Search  │  │ • Audio   │  │ • Push    │       │
│  │ • Export  │  │ • Alerts  │  │   Mute    │  │ • Webhooks│       │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘       │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                        Message Bus (MQTT)
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Message Broker Layer                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Eclipse Mosquitto (MQTT Broker)                             │  │
│  │  • guardian/cameras/+/status - Camera status (online/offline)│  │
│  │  • guardian/evidence/new - New evidence uploaded             │  │
│  │  • guardian/alerts/+ - Critical events (tamper, low battery) │  │
│  │  • guardian/sync/+ - Sync progress (upload status)           │  │
│  │  • guardian/blockchain/new_block - Blockchain updates        │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                           Database/Storage APIs
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Data Layer                                   │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │PostgreSQL │  │   MinIO   │  │   Redis   │  │Prometheus │       │
│  │    +      │  │  Object   │  │   Cache   │  │  Metrics  │       │
│  │TimescaleDB│  │  Storage  │  │  & Queue  │  │  Storage  │       │
│  │           │  │           │  │           │  │           │       │
│  │ • Officers│  │ • Video   │  │ • Sessions│  │ • Uploads │       │
│  │ • Cameras │  │   Files   │  │ • Transcode│ │ • Storage │       │
│  │ • Evidence│  │   (H.264) │  │   Queue   │  │ • Errors  │       │
│  │ • COC     │  │ • SHA256  │  │ • Live    │  │ • Battery │       │
│  │   Ledger  │  │   Hashes  │  │   Streams │  │ • Sync    │       │
│  │ • Audit   │  │ • S3 API  │  │ • Pub/Sub │  │   Status  │       │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘       │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                          WiFi/Bluetooth/USB
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Charging Dock & Sync Layer                        │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │            Charging Dock (USB-C PD Hub)                       │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐         │  │
│  │  │  Slot 1 │  │  Slot 2 │  │  Slot 3 │  │  Slot 4 │         │  │
│  │  │ ┌─────┐ │  │ ┌─────┐ │  │ ┌─────┐ │  │ ┌─────┐ │         │  │
│  │  │ │CAM01│ │  │ │CAM02│ │  │ │CAM03│ │  │ │CAM04│ │         │  │
│  │  │ │85%  │ │  │ │100% │ │  │ │72%  │ │  │ │Empty│ │         │  │
│  │  │ │Sync │ │  │ │Ready│ │  │ │Charge│ │  │ │     │ │         │  │
│  │  │ └─────┘ │  │ └─────┘ │  │ └─────┘ │  │ └─────┘ │         │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘         │  │
│  │                                                                │  │
│  │  Auto-Sync:                                                    │  │
│  │  1. Camera docked → Power negotiation (USB-C PD)              │  │
│  │  2. WiFi connects to base station → DHCP                      │  │
│  │  3. Upload queue processed → Videos + metadata                │  │
│  │  4. SHA256 hash verified → Blockchain record created          │  │
│  │  5. Local files optionally deleted → Free space               │  │
│  │  6. Battery charged → 100% in 2-4 hours                       │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                          WiFi Recording & Storage
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Body Camera Layer                              │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │   Raspberry Pi Body Camera (per unit)                        │  │
│  │                                                               │  │
│  │  Hardware:                                                    │  │
│  │  • Raspberry Pi Zero 2 W / Pi 4 (ARM CPU)                   │  │
│  │  • Pi Camera Module (1080p @ 30 FPS, 4K optional)           │  │
│  │  • 64-256GB microSD (local storage)                         │  │
│  │  • 10,000-20,000mAh battery (8-16hr runtime)                │  │
│  │  • GPS module (USB, location tagging)                        │  │
│  │  • WiFi/Bluetooth (802.11ac, BT 5.0)                        │  │
│  │  • Enclosure (3D printed or ruggedized IP65)                │  │
│  │                                                               │  │
│  │  Software:                                                    │  │
│  │  • Raspberry Pi OS Lite (headless, no GUI)                  │  │
│  │  • Python 3.11 (recording script)                           │  │
│  │  • PiCamera library (video capture)                         │  │
│  │  • FFmpeg (H.264 encoding)                                  │  │
│  │  • systemd service (auto-start recording)                   │  │
│  │  • gpsd (GPS daemon)                                        │  │
│  │  • rsync (upload to server)                                 │  │
│  │                                                               │  │
│  │  Recording Workflow:                                          │  │
│  │  1. Boot → Start recording automatically (30s boot time)    │  │
│  │  2. Record 5-minute segments → H.264 @ 4 Mbps               │  │
│  │  3. Save to microSD → /media/recordings/CAM01_20241207...   │  │
│  │  4. Tag GPS coordinates → Metadata JSON file                │  │
│  │  5. When WiFi available → Upload to evidence server         │  │
│  │  6. Verify upload → Delete local copy (optional)            │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  Storage: 64-256GB microSD (8-24 hours @ 1080p)                   │
│  Battery: 8-16 hours continuous recording                         │
│  Network: WiFi auto-connect to known SSIDs, fallback to hotspot  │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Architectural Decisions

| Decision | Rationale | Trade-off |
|----------|-----------|-----------|
| **Raspberry Pi Platform** | Low cost ($15-75), open hardware, huge ecosystem, ARM efficiency | Lower performance vs x86, limited I/O |
| **Local Edge Recording** | No network dependency, privacy, bandwidth efficiency | Requires manual sync/docking |
| **Blockchain COC** | Cryptographic proof, legal admissibility, tamper-evident | Complexity, storage overhead |
| **PostgreSQL + TimescaleDB** | Time-series optimized, ACID compliance, excellent querying | Not horizontally scalable like Cassandra |
| **MinIO for Video** | S3-compatible, self-hosted, tiering, versioning | More complex than simple NFS |
| **H.264 Encoding** | Universal compatibility, hardware acceleration, good compression | Not as efficient as H.265 (patent issues) |
| **WiFi Sync** | No cables, auto-upload when in range | Slower than wired, security concerns |
| **microSD Storage** | Cheap, swappable, standard | Write endurance limits (use high-endurance) |

---

## Core Technology Deep-Dive

### Body Camera Recording Architecture

**File**: `/usr/local/bin/bodycam-recorder.py` (installed on each camera)

```python
#!/usr/bin/env python3
"""
OS-GUARDIAN Body Camera Recorder
Continuously records video to microSD, uploads to evidence server when WiFi available
"""

import os
import time
import json
import hashlib
import logging
import subprocess
from datetime import datetime
from pathlib import Path
from threading import Thread
import requests
import picamera
import gpsd

# Configuration
CAMERA_ID = os.getenv('CAMERA_ID', 'CAM001')
OFFICER_ID = os.getenv('OFFICER_ID', 'OFFICER001')
EVIDENCE_SERVER = os.getenv('EVIDENCE_SERVER', 'http://192.168.1.100:8000')
STORAGE_PATH = Path('/media/recordings')
SEGMENT_DURATION = 300  # 5 minutes per segment
RESOLUTION = (1920, 1080)  # 1080p
FPS = 30
BITRATE = 4000000  # 4 Mbps

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('/var/log/bodycam.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GPSTracker:
    """GPS location tracking"""
    def __init__(self):
        try:
            gpsd.connect()
            self.enabled = True
            logger.info("GPS connected")
        except Exception as e:
            logger.warning(f"GPS unavailable: {e}")
            self.enabled = False

    def get_location(self):
        """Get current GPS coordinates"""
        if not self.enabled:
            return None
        try:
            packet = gpsd.get_current()
            return {
                'latitude': packet.lat,
                'longitude': packet.lon,
                'altitude': packet.alt,
                'speed': packet.hspeed,
                'timestamp': packet.time,
                'accuracy': packet.error['y']  # Horizontal accuracy
            }
        except Exception as e:
            logger.error(f"GPS read error: {e}")
            return None

class VideoUploader:
    """Background thread to upload completed segments"""
    def __init__(self):
        self.upload_queue = []
        self.running = True
        self.thread = Thread(target=self._upload_worker, daemon=True)
        self.thread.start()

    def add_to_queue(self, filepath, metadata):
        """Add video segment to upload queue"""
        self.upload_queue.append((filepath, metadata))
        logger.info(f"Queued for upload: {filepath.name} ({len(self.upload_queue)} in queue)")

    def _upload_worker(self):
        """Background worker thread"""
        while self.running:
            if not self.upload_queue:
                time.sleep(5)
                continue

            filepath, metadata = self.upload_queue[0]

            try:
                # Check if server reachable
                response = requests.get(f"{EVIDENCE_SERVER}/api/health", timeout=5)
                if response.status_code != 200:
                    logger.warning("Evidence server not reachable, will retry")
                    time.sleep(30)
                    continue

                # Calculate SHA256 hash
                sha256 = hashlib.sha256()
                with open(filepath, 'rb') as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        sha256.update(chunk)
                file_hash = sha256.hexdigest()
                metadata['sha256'] = file_hash

                # Upload video file
                with open(filepath, 'rb') as f:
                    files = {'file': (filepath.name, f, 'video/h264')}
                    data = {'metadata': json.dumps(metadata)}
                    response = requests.post(
                        f"{EVIDENCE_SERVER}/api/evidence/upload",
                        files=files,
                        data=data,
                        timeout=600  # 10 minutes for large files
                    )

                if response.status_code == 200:
                    logger.info(f"✓ Uploaded: {filepath.name} (hash: {file_hash[:16]}...)")

                    # Optionally delete local file to save space
                    # filepath.unlink()

                    # Remove from queue
                    self.upload_queue.pop(0)
                else:
                    logger.error(f"Upload failed: {response.status_code} - {response.text}")
                    time.sleep(60)  # Wait 1 minute before retry

            except Exception as e:
                logger.error(f"Upload error: {e}")
                time.sleep(60)  # Wait 1 minute before retry

    def stop(self):
        """Stop uploader thread"""
        self.running = False
        self.thread.join()

class BodyCamRecorder:
    """Main body camera recorder"""
    def __init__(self):
        self.camera = None
        self.gps = GPSTracker()
        self.uploader = VideoUploader()
        self.segment_count = 0
        STORAGE_PATH.mkdir(parents=True, exist_ok=True)

    def record_segment(self):
        """Record one 5-minute video segment"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{CAMERA_ID}_{OFFICER_ID}_{timestamp}.h264'
        filepath = STORAGE_PATH / filename

        logger.info(f"Recording segment {self.segment_count}: {filename}")

        # Capture GPS location at start
        gps_start = self.gps.get_location()

        # Record video
        self.camera.start_recording(str(filepath), bitrate=BITRATE)

        # Wait for segment duration (check battery every 30s)
        for i in range(SEGMENT_DURATION // 30):
            self.camera.wait_recording(30)
            battery_pct = self._get_battery_percentage()
            if battery_pct < 10:
                logger.warning(f"Low battery: {battery_pct}%")

        self.camera.stop_recording()

        # Capture GPS location at end
        gps_end = self.gps.get_location()

        # Get video file stats
        file_size = filepath.stat().st_size
        duration = SEGMENT_DURATION

        # Create metadata
        metadata = {
            'camera_id': CAMERA_ID,
            'officer_id': OFFICER_ID,
            'start_time': timestamp,
            'duration': duration,
            'file_size': file_size,
            'resolution': f"{RESOLUTION[0]}x{RESOLUTION[1]}",
            'fps': FPS,
            'bitrate': BITRATE,
            'gps_start': gps_start,
            'gps_end': gps_end,
            'segment_number': self.segment_count
        }

        # Save metadata JSON
        metadata_path = STORAGE_PATH / f"{filepath.stem}.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

        logger.info(f"✓ Recorded {duration}s, {file_size / 1024 / 1024:.1f} MB")

        # Add to upload queue
        self.uploader.add_to_queue(filepath, metadata)

        self.segment_count += 1

    def _get_battery_percentage(self):
        """Read battery percentage from power management"""
        try:
            # Read from UPS HAT or battery gauge (I2C)
            # Simplified: Read from sysfs (if available)
            with open('/sys/class/power_supply/battery/capacity', 'r') as f:
                return int(f.read().strip())
        except:
            return 100  # Assume full if unavailable

    def run(self):
        """Main recording loop"""
        logger.info("="*60)
        logger.info("OS-GUARDIAN Body Camera Recorder")
        logger.info(f"Camera ID: {CAMERA_ID}")
        logger.info(f"Officer ID: {OFFICER_ID}")
        logger.info(f"Resolution: {RESOLUTION[0]}x{RESOLUTION[1]} @ {FPS} FPS")
        logger.info(f"Bitrate: {BITRATE / 1000000} Mbps")
        logger.info(f"Segment Duration: {SEGMENT_DURATION} seconds")
        logger.info(f"Storage: {STORAGE_PATH}")
        logger.info(f"Evidence Server: {EVIDENCE_SERVER}")
        logger.info("="*60)

        try:
            with picamera.PiCamera() as camera:
                self.camera = camera
                camera.resolution = RESOLUTION
                camera.framerate = FPS
                camera.rotation = 0  # Adjust based on mounting

                # Warm up
                time.sleep(2)

                logger.info("Starting continuous recording...")

                while True:
                    self.record_segment()

        except KeyboardInterrupt:
            logger.info("Stopping recording (user interrupt)")
        except Exception as e:
            logger.error(f"Recording error: {e}")
        finally:
            self.uploader.stop()
            logger.info("Recorder stopped")

if __name__ == '__main__':
    recorder = BodyCamRecorder()
    recorder.run()
```

### Evidence Ingestion Service

**File**: `ingestion-service/ingest.py` (runs on evidence server)

```python
#!/usr/bin/env python3
"""
OS-GUARDIAN Evidence Ingestion Service
Receives uploaded videos from body cameras, verifies integrity, stores with blockchain COC
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
import psycopg2
from minio import Minio
from minio.error import S3Error
import paho.mqtt.client as mqtt

# Configuration
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'guardian')
DB_USER = os.getenv('DB_USER', 'guardian')
DB_PASS = os.getenv('DB_PASS', 'password')

MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin')
MINIO_BUCKET = 'evidence-vault'

MQTT_BROKER = os.getenv('MQTT_BROKER', 'localhost')
MQTT_PORT = int(os.getenv('MQTT_PORT', 1883))

app = FastAPI(title="OS-GUARDIAN Evidence Ingestion")

# Database connection
def get_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# MinIO client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # Use True for HTTPS
)

# Ensure bucket exists
if not minio_client.bucket_exists(MINIO_BUCKET):
    minio_client.make_bucket(MINIO_BUCKET)

# MQTT client
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

@app.post("/api/evidence/upload")
async def upload_evidence(
    file: UploadFile = File(...),
    metadata: str = Form(...)
):
    """
    Upload evidence video from body camera

    Steps:
    1. Receive video file + metadata
    2. Verify SHA256 hash
    3. Store in MinIO (S3-compatible)
    4. Insert metadata into PostgreSQL
    5. Create blockchain chain-of-custody record
    6. Publish MQTT event
    """
    try:
        # Parse metadata
        meta = json.loads(metadata)

        # Read file content
        file_content = await file.read()
        file_size = len(file_content)

        # Verify SHA256 hash
        calculated_hash = hashlib.sha256(file_content).hexdigest()
        provided_hash = meta.get('sha256')

        if calculated_hash != provided_hash:
            raise HTTPException(
                status_code=400,
                detail=f"Hash mismatch! Calculated: {calculated_hash}, Provided: {provided_hash}"
            )

        # Generate evidence ID
        evidence_id = f"EV-{datetime.now().strftime('%Y%m%d%H%M%S')}-{meta['camera_id']}"

        # Upload to MinIO
        object_name = f"{meta['camera_id']}/{datetime.now().strftime('%Y/%m/%d')}/{file.filename}"

        from io import BytesIO
        minio_client.put_object(
            MINIO_BUCKET,
            object_name,
            BytesIO(file_content),
            file_size,
            content_type='video/h264'
        )

        # Insert into database
        db = get_db()
        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO evidence (
                evidence_id, camera_id, officer_id, filename, object_name,
                file_size, sha256_hash, duration, resolution, fps, bitrate,
                gps_start_lat, gps_start_lon, gps_end_lat, gps_end_lon,
                recorded_at, uploaded_at, status
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            ) RETURNING id
        """, (
            evidence_id,
            meta['camera_id'],
            meta['officer_id'],
            file.filename,
            object_name,
            file_size,
            calculated_hash,
            meta['duration'],
            meta['resolution'],
            meta['fps'],
            meta['bitrate'],
            meta['gps_start']['latitude'] if meta.get('gps_start') else None,
            meta['gps_start']['longitude'] if meta.get('gps_start') else None,
            meta['gps_end']['latitude'] if meta.get('gps_end') else None,
            meta['gps_end']['longitude'] if meta.get('gps_end') else None,
            meta['start_time'],
            datetime.now(),
            'uploaded'
        ))

        evidence_db_id = cursor.fetchone()[0]

        # Create blockchain chain-of-custody record
        cursor.execute("""
            INSERT INTO chain_of_custody (
                evidence_id, action, user_id, timestamp, sha256_hash, details
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            evidence_db_id,
            'UPLOADED',
            meta['officer_id'],
            datetime.now(),
            calculated_hash,
            json.dumps({'camera_id': meta['camera_id'], 'segment': meta.get('segment_number')})
        ))

        db.commit()
        cursor.close()
        db.close()

        # Publish MQTT event
        mqtt_client.publish(
            f"guardian/evidence/new",
            json.dumps({
                'evidence_id': evidence_id,
                'camera_id': meta['camera_id'],
                'officer_id': meta['officer_id'],
                'timestamp': datetime.now().isoformat()
            })
        )

        return JSONResponse({
            'status': 'success',
            'evidence_id': evidence_id,
            'sha256': calculated_hash,
            'size': file_size,
            'message': 'Evidence uploaded and verified'
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok", "service": "OS-GUARDIAN Evidence Ingestion"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## Component Architecture

### Body Camera Components

```
┌────────────────────────────────────────────────────────┐
│         Raspberry Pi Body Camera Architecture          │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Raspberry Pi Zero 2 W / Pi 4                    │ │
│  │  ┌────────────────────────────────────────────┐  │ │
│  │  │ ARM CPU (Cortex-A53 @ 1GHz / A72 @ 1.8GHz)│  │ │
│  │  │ 512MB / 2GB / 4GB / 8GB RAM                │  │ │
│  │  │ WiFi 802.11ac, Bluetooth 5.0               │  │ │
│  │  │ GPIO (40-pin header)                        │  │ │
│  │  │ CSI Camera Interface                        │  │ │
│  │  │ USB 2.0 / USB 3.0 ports                    │  │ │
│  │  └────────────────────────────────────────────┘  │ │
│  └──────────────────────────────────────────────────┘ │
│                        ▲                              │
│          ┌─────────────┼─────────────┐                │
│          │             │             │                │
│  ┌───────▼──────┐ ┌───▼─────┐ ┌────▼──────┐         │
│  │Pi Camera v2/v3│GPS Module│ │Power Bank │         │
│  │8MP, 1080p@30│ │u-blox    │ │10-20Ah    │         │
│  │12MP, 4K@30   │ │NEO-6M    │ │USB-C PD   │         │
│  │160° FOV      │ │USB       │ │18-30W     │         │
│  └──────────────┘ └──────────┘ └───────────┘         │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  microSD Card (64-256GB, High-Endurance)        │ │
│  │  • Raspberry Pi OS Lite (headless)              │ │
│  │  • Python recording script (systemd service)    │ │
│  │  • Local video storage (8-24 hours capacity)    │ │
│  │  • Auto-sync to server when WiFi available      │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Enclosure (3D Printed or Ruggedized)           │ │
│  │  • Chest clip or shoulder mount                 │ │
│  │  • IP65 water/dust resistance (professional)    │ │
│  │  • LED indicator (recording status)             │ │
│  │  • Power button, manual record button           │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

### Evidence Server Components

```
┌────────────────────────────────────────────────────────┐
│         Evidence Server Architecture                   │
│         (Raspberry Pi 4 8GB or x86 Server)            │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  Docker Containers                               │ │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐ │ │
│  │  │PostgreSQL  │  │   MinIO    │  │ Ingestion  │ │ │
│  │  │  +         │  │   Object   │  │  Service   │ │ │
│  │  │TimescaleDB │  │  Storage   │  │  (FastAPI) │ │ │
│  │  │            │  │            │  │            │ │ │
│  │  │• Metadata  │  │• Video     │  │• Upload    │ │ │
│  │  │• Officers  │  │  Files     │  │• Hash      │ │ │
│  │  │• Cameras   │  │• S3 API    │  │• Verify    │ │ │
│  │  │• COC Log   │  │• Tiering   │  │• Index     │ │ │
│  │  └────────────┘  └────────────┘  └────────────┘ │ │
│  │                                                  │ │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐ │ │
│  │  │Blockchain  │  │ MediaMTX   │  │  Web UI    │ │ │
│  │  │Chain-of-   │  │  RTSP/     │  │  (React)   │ │ │
│  │  │ Custody    │  │  WebRTC    │  │            │ │ │
│  │  │            │  │            │  │• Playback  │ │ │
│  │  │• Ledger    │  │• Live      │  │• Search    │ │ │
│  │  │• Signing   │  │  Streams   │  │• Export    │ │ │
│  │  │• Audit     │  │• Transcode │  │• Reports   │ │ │
│  │  └────────────┘  └────────────┘  └────────────┘ │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │  External Storage (1-4TB SSD, NAS, or SAN)      │ │
│  │  • MinIO data volume (video vault)              │ │
│  │  • PostgreSQL data volume (database)            │ │
│  │  • Backup destination (rsync, rclone)           │ │
│  └──────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────┘
```

---

## Body Camera Hardware Architecture

### Recommended Configurations

#### Budget Configuration ($75 per camera)
```yaml
CPU: Raspberry Pi Zero 2 W ($15)
Camera: Pi Camera Module v2, 8MP 1080p @ 30 FPS ($25)
Storage: 64GB microSD High-Endurance A1 ($12)
Battery: 10,000mAh USB power bank, 18W ($20)
Enclosure: 3D printed chest clip mount ($3 filament cost)
Total: ~$75
Runtime: 8-10 hours continuous recording
Storage Capacity: ~8 hours @ 1080p 30 FPS 4 Mbps
```

#### Professional Configuration ($200 per camera)
```yaml
CPU: Raspberry Pi 4 Model B, 2GB RAM ($45)
Camera: Pi HQ Camera 12MP + 6mm wide lens, 4K @ 30 FPS ($85 total)
Storage: 128GB microSD High-Endurance A2 ($20)
Battery: 20,000mAh USB-C PD power bank, 30W dual output ($35)
GPS: USB GPS module, u-blox NEO-6M ($15)
Enclosure: Ruggedized IP65-rated housing, shock-resistant ($50)
Accessories: IR LED night vision module ($12), chest clip + helmet mount ($8)
Total: ~$200
Runtime: 12-16 hours continuous recording
Storage Capacity: ~12 hours @ 4K 30 FPS or 24 hours @ 1080p
Night Vision: 10-meter IR range
GPS: Real-time location tagging
```

#### Enterprise Configuration ($350 per camera)
```yaml
CPU: Raspberry Pi 4 Model B, 4GB RAM ($55)
Camera: Pi HQ Camera 12MP + 6mm wide lens + IR filter ($100)
Storage: 256GB microSD High-Endurance A2 ($40)
Battery: 30,000mAh USB-C PD power bank, 65W, swappable ($60)
GPS: High-precision GPS module with external antenna ($35)
Cellular: 4G LTE USB modem for real-time upload ($40)
Enclosure: Military-spec ruggedized IP67 housing ($80)
Accessories: Dual IR/white LED illumination ($20), multi-mount kit ($15)
Audio: External USB microphone with noise cancellation ($25)
Total: ~$350
Runtime: 20-24 hours continuous recording (swappable batteries)
Storage Capacity: ~24 hours @ 4K 30 FPS or 48 hours @ 1080p
Network: Real-time upload via 4G LTE (fallback to WiFi)
Environmental: -20°C to +60°C operating range, IP67 waterproof
```

### Hardware Specifications Comparison

| Component | Budget | Professional | Enterprise |
|-----------|--------|--------------|------------|
| **CPU** | Pi Zero 2 W (1GHz quad) | Pi 4 (1.8GHz quad, 2GB RAM) | Pi 4 (1.8GHz quad, 4GB RAM) |
| **Video Resolution** | 1080p @ 30 FPS | 4K @ 30 FPS | 4K @ 30 FPS |
| **Storage** | 64GB (~8hr) | 128GB (~12hr) | 256GB (~24hr) |
| **Battery Life** | 8-10 hours | 12-16 hours | 20-24 hours |
| **GPS** | ✗ No | ✓ Yes | ✓ High-precision |
| **Night Vision** | ✗ No | ✓ 10m IR | ✓ Dual IR/white LED |
| **Cellular Upload** | ✗ No | ✗ No | ✓ 4G LTE |
| **Waterproof Rating** | IP40 (basic) | IP65 (dust/water resist) | IP67 (submersible) |
| **Weight** | 180g | 220g | 280g |
| **Cost** | $75 | $200 | $350 |

---

## Data Architecture

### PostgreSQL Schema

**Database**: `guardian`

```sql
-- Officers table
CREATE TABLE officers (
    id SERIAL PRIMARY KEY,
    officer_id VARCHAR(50) UNIQUE NOT NULL,
    badge_number VARCHAR(50),
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    department VARCHAR(200),
    rank VARCHAR(100),
    email VARCHAR(255),
    phone VARCHAR(20),
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Body cameras table
CREATE TABLE cameras (
    id SERIAL PRIMARY KEY,
    camera_id VARCHAR(50) UNIQUE NOT NULL,
    hardware_type VARCHAR(100),  -- 'Pi Zero 2 W', 'Pi 4 2GB', etc.
    serial_number VARCHAR(100),
    firmware_version VARCHAR(50),
    assigned_officer_id INTEGER REFERENCES officers(id),
    status VARCHAR(50) DEFAULT 'offline',  -- 'online', 'offline', 'recording', 'charging', 'maintenance'
    last_seen TIMESTAMP,
    battery_percentage INTEGER,
    storage_used_gb NUMERIC(10,2),
    storage_total_gb NUMERIC(10,2),
    gps_enabled BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Evidence table (time-series optimized)
CREATE TABLE evidence (
    id SERIAL PRIMARY KEY,
    evidence_id VARCHAR(100) UNIQUE NOT NULL,
    camera_id VARCHAR(50) REFERENCES cameras(camera_id),
    officer_id VARCHAR(50) REFERENCES officers(officer_id),
    filename VARCHAR(255) NOT NULL,
    object_name VARCHAR(500) NOT NULL,  -- MinIO object path
    file_size BIGINT NOT NULL,
    sha256_hash VARCHAR(64) NOT NULL,
    duration INTEGER,  -- seconds
    resolution VARCHAR(20),  -- '1920x1080'
    fps INTEGER,
    bitrate INTEGER,
    gps_start_lat NUMERIC(10, 7),
    gps_start_lon NUMERIC(11, 7),
    gps_end_lat NUMERIC(10, 7),
    gps_end_lon NUMERIC(11, 7),
    recorded_at TIMESTAMP NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'uploaded',  -- 'uploaded', 'verified', 'redacted', 'exported', 'archived', 'deleted'
    retention_until DATE,
    tags TEXT[],  -- Array of tags: ['incident', 'arrest', 'patrol']
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Convert evidence table to hypertable (TimescaleDB)
SELECT create_hypertable('evidence', 'recorded_at', chunk_time_interval => INTERVAL '1 day');

-- Chain of Custody (blockchain ledger)
CREATE TABLE chain_of_custody (
    id SERIAL PRIMARY KEY,
    evidence_id INTEGER REFERENCES evidence(id) ON DELETE CASCADE,
    action VARCHAR(100) NOT NULL,  -- 'UPLOADED', 'VIEWED', 'DOWNLOADED', 'EXPORTED', 'REDACTED', 'DELETED'
    user_id VARCHAR(100) NOT NULL,  -- officer_id or username
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    sha256_hash VARCHAR(64),  -- Hash of evidence file at time of action
    blockchain_tx_hash VARCHAR(66),  -- Ethereum/Fabric transaction hash
    details JSONB,  -- Additional metadata
    signature VARCHAR(500)  -- Cryptographic signature
);

-- Incidents table (link multiple evidence files to one incident)
CREATE TABLE incidents (
    id SERIAL PRIMARY KEY,
    incident_id VARCHAR(100) UNIQUE NOT NULL,
    incident_type VARCHAR(100),  -- 'arrest', 'use_of_force', 'traffic_stop', 'complaint', etc.
    incident_date TIMESTAMP NOT NULL,
    location VARCHAR(500),
    location_lat NUMERIC(10, 7),
    location_lon NUMERIC(11, 7),
    summary TEXT,
    officers_involved INTEGER[],  -- Array of officer IDs
    status VARCHAR(50) DEFAULT 'open',  -- 'open', 'closed', 'under_review'
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Evidence-Incident mapping (many-to-many)
CREATE TABLE incident_evidence (
    incident_id INTEGER REFERENCES incidents(id) ON DELETE CASCADE,
    evidence_id INTEGER REFERENCES evidence(id) ON DELETE CASCADE,
    PRIMARY KEY (incident_id, evidence_id)
);

-- Redaction requests
CREATE TABLE redactions (
    id SERIAL PRIMARY KEY,
    evidence_id INTEGER REFERENCES evidence(id) ON DELETE CASCADE,
    requested_by VARCHAR(100) NOT NULL,
    reason VARCHAR(500),
    redaction_type VARCHAR(100),  -- 'face_blur', 'audio_mute', 'area_pixelate'
    redaction_frames TEXT,  -- JSON array of frame ranges
    status VARCHAR(50) DEFAULT 'pending',  -- 'pending', 'approved', 'rejected', 'completed'
    redacted_file_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Audit log (all system access)
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    action VARCHAR(200) NOT NULL,
    resource_type VARCHAR(100),  -- 'evidence', 'officer', 'camera', 'incident'
    resource_id VARCHAR(100),
    ip_address INET,
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details JSONB
);

-- Indexes
CREATE INDEX idx_evidence_camera_id ON evidence(camera_id);
CREATE INDEX idx_evidence_officer_id ON evidence(officer_id);
CREATE INDEX idx_evidence_recorded_at ON evidence(recorded_at);
CREATE INDEX idx_evidence_sha256 ON evidence(sha256_hash);
CREATE INDEX idx_coc_evidence_id ON chain_of_custody(evidence_id);
CREATE INDEX idx_coc_timestamp ON chain_of_custody(timestamp);
CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX idx_audit_log_timestamp ON audit_log(timestamp);

-- Full-text search on evidence notes and incident summaries
CREATE INDEX idx_evidence_notes_fulltext ON evidence USING gin(to_tsvector('english', notes));
CREATE INDEX idx_incident_summary_fulltext ON incidents USING gin(to_tsvector('english', summary));
```

### Sample Queries

**Find all evidence from Officer #5824 in the past 7 days:**
```sql
SELECT
    e.evidence_id,
    e.filename,
    e.recorded_at,
    e.duration,
    e.file_size / 1024 / 1024 AS size_mb,
    o.first_name || ' ' || o.last_name AS officer_name
FROM evidence e
JOIN officers o ON e.officer_id = o.officer_id
WHERE e.officer_id = 'OFFICER_5824'
    AND e.recorded_at >= NOW() - INTERVAL '7 days'
ORDER BY e.recorded_at DESC;
```

**Get chain-of-custody trail for specific evidence:**
```sql
SELECT
    coc.id,
    coc.action,
    coc.user_id,
    coc.timestamp,
    coc.ip_address,
    coc.details
FROM chain_of_custody coc
WHERE coc.evidence_id = (SELECT id FROM evidence WHERE evidence_id = 'EV-20241207143215-CAM001')
ORDER BY coc.timestamp ASC;
```

**Find all evidence within 500 meters of specific GPS coordinates:**
```sql
SELECT
    e.evidence_id,
    e.filename,
    e.recorded_at,
    ST_Distance(
        ST_MakePoint(e.gps_start_lon, e.gps_start_lat)::geography,
        ST_MakePoint(-75.6972, 45.4215)::geography
    ) AS distance_meters
FROM evidence e
WHERE e.gps_start_lat IS NOT NULL
    AND ST_DWithin(
        ST_MakePoint(e.gps_start_lon, e.gps_start_lat)::geography,
        ST_MakePoint(-75.6972, 45.4215)::geography,
        500  -- 500 meters
    )
ORDER BY distance_meters ASC;
```

**Storage utilization report by camera:**
```sql
SELECT
    c.camera_id,
    COUNT(e.id) AS video_count,
    SUM(e.file_size) / 1024 / 1024 / 1024 AS total_gb,
    SUM(e.duration) / 3600 AS total_hours,
    MIN(e.recorded_at) AS oldest_recording,
    MAX(e.recorded_at) AS newest_recording
FROM cameras c
LEFT JOIN evidence e ON c.camera_id = e.camera_id
GROUP BY c.camera_id
ORDER BY total_gb DESC;
```

---

## Video Ingestion Pipeline

### Upload Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  Body Camera (on duty, recording)                           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 1. Record 5-minute segments                           │  │
│  │    File: CAM001_OFFICER01_20241207_143215.h264       │  │
│  │    Metadata: GPS, duration, resolution, FPS           │  │
│  │ 2. Calculate SHA256 hash                              │  │
│  │    Hash: 8f7b2c3e9a1d4f6b...                         │  │
│  │ 3. Save to local microSD                              │  │
│  │    Path: /media/recordings/                           │  │
│  │ 4. Add to upload queue                                │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                    WiFi available?
                            │
                        ┌───▼───┐
                        │  Yes  │
                        └───┬───┘
                            │
┌───────────────────────────▼─────────────────────────────────┐
│  Upload Process (background thread)                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 1. Connect to evidence server                         │  │
│  │    POST /api/evidence/upload                          │  │
│  │ 2. Send video file + metadata JSON                    │  │
│  │ 3. Wait for server acknowledgment                     │  │
│  │ 4. Verify upload success                              │  │
│  │ 5. Optionally delete local copy (free space)          │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Evidence Server - Ingestion Service                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 1. Receive file upload                                │  │
│  │    FastAPI endpoint: /api/evidence/upload             │  │
│  │ 2. Verify SHA256 hash                                 │  │
│  │    Calculated: 8f7b2c3e...                           │  │
│  │    Provided: 8f7b2c3e...                             │  │
│  │    ✓ Match → Continue                                 │  │
│  │    ✗ Mismatch → Reject (integrity failure)            │  │
│  │ 3. Store video in MinIO (S3)                          │  │
│  │    Bucket: evidence-vault                             │  │
│  │    Object: CAM001/2024/12/07/CAM001_...h264          │  │
│  │ 4. Insert metadata into PostgreSQL                    │  │
│  │    Table: evidence                                    │  │
│  │    Columns: evidence_id, camera_id, officer_id,      │  │
│  │             sha256_hash, file_size, duration, etc.    │  │
│  │ 5. Create blockchain chain-of-custody record          │  │
│  │    Action: UPLOADED                                   │  │
│  │    User: OFFICER_01                                   │  │
│  │    Timestamp: 2024-12-07 14:32:18                    │  │
│  │    Signature: [cryptographic signature]               │  │
│  │ 6. Publish MQTT event                                 │  │
│  │    Topic: guardian/evidence/new                       │  │
│  │    Payload: {evidence_id, camera_id, timestamp}      │  │
│  │ 7. Send acknowledgment to camera                      │  │
│  │    Response: {"status": "success", "evidence_id":... │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Post-Ingestion Processing (async)                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 1. Generate video thumbnail                           │  │
│  │    FFmpeg: Extract frame at 5 seconds                 │  │
│  │ 2. Extract metadata (duration, codec, bitrate)        │  │
│  │    FFprobe: Read video properties                     │  │
│  │ 3. Transcode for streaming (optional)                 │  │
│  │    FFmpeg: Generate HLS playlist or WebRTC-compatible│  │
│  │ 4. Analyze video (optional AI features)               │  │
│  │    Object detection, face detection, license plates   │  │
│  │ 5. Update evidence record with processed data         │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### FFmpeg Video Processing

**Generate thumbnail:**
```bash
ffmpeg -i evidence.h264 -ss 00:00:05 -frames:v 1 thumbnail.jpg
```

**Transcode to MP4 (browser-compatible):**
```bash
ffmpeg -i evidence.h264 -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 128k evidence.mp4
```

**Extract metadata:**
```bash
ffprobe -v quiet -print_format json -show_format -show_streams evidence.h264
```

**Generate HLS streaming playlist:**
```bash
ffmpeg -i evidence.h264 \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  -hls_time 10 -hls_list_size 0 \
  -f hls evidence.m3u8
```

---

## Blockchain Chain-of-Custody

### Conceptual Architecture

**Problem**: Evidence tampering, deleted files, modified videos

**Solution**: Cryptographic proof that evidence has not been altered since capture

**How it Works**:

1. **Capture**: Body camera records video, calculates SHA256 hash
2. **Upload**: Video uploaded to server, hash verified
3. **Blockchain Record**: Hash + metadata written to immutable ledger
4. **Every Access**: View, download, export → New blockchain record
5. **Verification**: At any time, recalculate hash, compare to blockchain
   - ✓ Match → Evidence is authentic
   - ✗ Mismatch → Evidence has been tampered

### Implementation Options

#### Option 1: Private Hyperledger Fabric Blockchain

**Pros**: Permissioned, fast, enterprise-grade, GDPR-compliant
**Cons**: Complex setup, requires dedicated infrastructure

```yaml
# Hyperledger Fabric Network
Organizations:
  - Department (e.g., Police Dept)
    - Peer nodes: Store ledger, validate transactions
    - Orderer nodes: Sequence transactions into blocks
    - Certificate Authority: Issue digital certificates

Channels:
  - evidence-channel: All chain-of-custody transactions

Chaincode (Smart Contract):
  - recordEvidence(evidenceID, sha256, officerID, timestamp, signature)
  - getEvidenceHistory(evidenceID) → Returns all COC records
  - verifyEvidenceIntegrity(evidenceID, currentSHA256) → Returns true/false
```

**Python Integration:**
```python
from hfc.fabric import Client

# Connect to Hyperledger Fabric
client = Client(net_profile="network.json")
user = client.get_user('org1', 'officer01')

# Invoke chaincode to record evidence
response = client.chaincode_invoke(
    requestor=user,
    channel_name='evidence-channel',
    peers=['peer0.org1'],
    cc_name='evidence_coc',
    cc_version='1.0',
    fcn='recordEvidence',
    args=[evidence_id, sha256_hash, officer_id, timestamp, signature],
    cc_pattern=None
)

print(f"Blockchain TX Hash: {response.tx_id}")
```

#### Option 2: Public Ethereum Blockchain

**Pros**: Truly immutable, public verification, well-understood
**Cons**: Gas fees, slower, privacy concerns (metadata is public)

```python
from web3 import Web3

# Connect to Ethereum (Mainnet or private network)
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

# Smart contract (Solidity)
contract_abi = [...]  # Contract ABI
contract_address = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb'
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Call smart contract function to record evidence
tx_hash = contract.functions.recordEvidence(
    evidence_id,
    sha256_hash,
    officer_id,
    int(time.time())
).transact({'from': w3.eth.accounts[0]})

# Wait for transaction confirmation
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Blockchain TX Hash: {receipt.transactionHash.hex()}")
```

**Smart Contract (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EvidenceChainOfCustody {
    struct Evidence {
        string evidenceID;
        bytes32 sha256Hash;
        string officerID;
        uint256 timestamp;
        string action;
    }

    mapping(string => Evidence[]) public evidenceHistory;

    event EvidenceRecorded(
        string indexed evidenceID,
        bytes32 sha256Hash,
        string officerID,
        uint256 timestamp,
        string action
    );

    function recordEvidence(
        string memory _evidenceID,
        bytes32 _sha256Hash,
        string memory _officerID,
        string memory _action
    ) public {
        Evidence memory newRecord = Evidence({
            evidenceID: _evidenceID,
            sha256Hash: _sha256Hash,
            officerID: _officerID,
            timestamp: block.timestamp,
            action: _action
        });

        evidenceHistory[_evidenceID].push(newRecord);

        emit EvidenceRecorded(
            _evidenceID,
            _sha256Hash,
            _officerID,
            block.timestamp,
            _action
        );
    }

    function getEvidenceHistory(string memory _evidenceID)
        public
        view
        returns (Evidence[] memory)
    {
        return evidenceHistory[_evidenceID];
    }

    function verifyEvidence(string memory _evidenceID, bytes32 _currentHash)
        public
        view
        returns (bool)
    {
        Evidence[] memory history = evidenceHistory[_evidenceID];
        require(history.length > 0, "Evidence not found");

        // Get original hash (first record)
        bytes32 originalHash = history[0].sha256Hash;

        return (originalHash == _currentHash);
    }
}
```

#### Option 3: OpenTimestamps (Bitcoin Blockchain)

**Pros**: Leverages Bitcoin security, cheap, simple
**Cons**: Timestamping only (not full COC), delayed confirmations

```python
import opentimestamps

# Calculate SHA256 of evidence file
sha256_hash = hashlib.sha256(open('evidence.h264', 'rb').read()).digest()

# Submit to OpenTimestamps calendar servers
timestamp = opentimestamps.stamp(sha256_hash)

# Save timestamp proof
with open('evidence.ots', 'wb') as f:
    f.write(timestamp.serialize())

# Later: Verify timestamp
with open('evidence.ots', 'rb') as f:
    timestamp_proof = opentimestamps.deserialize(f.read())

result = opentimestamps.verify(timestamp_proof, sha256_hash)
if result:
    print(f"✓ Evidence timestamp verified: {result.timestamp}")
else:
    print("✗ Timestamp verification failed")
```

### Chain-of-Custody Report (Legal Export)

**Generated for court proceedings:**

```
════════════════════════════════════════════════════════════════
                CHAIN-OF-CUSTODY CERTIFICATE
════════════════════════════════════════════════════════════════

Evidence ID: EV-20241207143215-CAM001
File Name: CAM001_OFFICER01_20241207_143215.h264
File Size: 1,247,893,504 bytes (1.16 GB)
SHA256 Hash: 8f7b2c3e9a1d4f6b2e5c8a3f1d9b4e6c7a2f8d5b1c4e9a6f3d7b2e8c5a1f4d6b

════════════════════════════════════════════════════════════════
                  CHAIN-OF-CUSTODY TIMELINE
════════════════════════════════════════════════════════════════

1. RECORDED
   Timestamp: 2024-12-07 14:32:15 UTC
   Officer: John Smith (Badge #5824)
   Camera: CAM001 (Raspberry Pi 4, Serial #RPi4-00123456)
   Location: 45.4215° N, 75.6972° W (GPS)
   Duration: 300 seconds (5:00)
   SHA256: 8f7b2c3e9a1d4f6b2e5c8a3f1d9b4e6c7a2f8d5b1c4e9a6f3d7b2e8c5a1f4d6b
   Blockchain TX: 0x742d35cc6634c0532925a3b844bc9e7595f0beb...

2. UPLOADED
   Timestamp: 2024-12-07 14:45:32 UTC
   User: Officer John Smith (OFFICER_5824)
   IP Address: 192.168.1.105
   Evidence Server: guardian-prod-01
   Storage: MinIO bucket 'evidence-vault'
   SHA256 Verified: ✓ Match
   Blockchain TX: 0x8a3f1d9b4e6c7a2f8d5b1c4e9a6f3d7b2e8c5a1f...

3. VIEWED
   Timestamp: 2024-12-07 15:20:14 UTC
   User: Supervisor Michael Chen (SUPERVISOR_02)
   IP Address: 192.168.1.112
   Browser: Chrome 120.0 (Windows 10)
   Duration Viewed: 120 seconds (2:00)
   Blockchain TX: 0x1c4e9a6f3d7b2e8c5a1f4d6b8f7b2c3e9a1d4f6b...

4. EXPORTED
   Timestamp: 2024-12-08 09:15:47 UTC
   User: Legal Department (LEGAL_01)
   IP Address: 192.168.1.150
   Export Format: MP4 (H.264, AAC audio)
   Export Size: 1,198,234,112 bytes
   Export SHA256: 2e8c5a1f4d6b8f7b2c3e9a1d4f6b1c4e9a6f3d7b...
   Reason: Court Exhibit #42, Case #2024-CR-12345
   Blockchain TX: 0x3d7b2e8c5a1f4d6b8f7b2c3e9a1d4f6b1c4e9a6f...

════════════════════════════════════════════════════════════════
                  CRYPTOGRAPHIC VERIFICATION
════════════════════════════════════════════════════════════════

Original SHA256 Hash (at recording):
8f7b2c3e9a1d4f6b2e5c8a3f1d9b4e6c7a2f8d5b1c4e9a6f3d7b2e8c5a1f4d6b

Current SHA256 Hash (at export):
8f7b2c3e9a1d4f6b2e5c8a3f1d9b4e6c7a2f8d5b1c4e9a6f3d7b2e8c5a1f4d6b

Verification: ✓ MATCH - Evidence has NOT been tampered with

Blockchain Verification:
Network: Ethereum Mainnet
Smart Contract: 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb
Block Number: 18,234,567
Block Timestamp: 2024-12-07 14:45:35 UTC
Confirmations: 1,247 blocks

════════════════════════════════════════════════════════════════

This certificate was generated by OS-GUARDIAN Evidence Management
System v1.0 on 2024-12-08 09:16:00 UTC.

Digital Signature:
-----BEGIN PGP SIGNATURE-----
iQIzBAABCAAdFiEE...
[GPG signature of this certificate]
-----END PGP SIGNATURE-----

════════════════════════════════════════════════════════════════
```

---

## Security Architecture

### Threat Model

| Threat | Mitigation |
|--------|------------|
| **Evidence Tampering** | SHA256 hashing + blockchain COC, immutable storage |
| **Unauthorized Access** | JWT authentication, RBAC, MFA, IP whitelisting |
| **Man-in-the-Middle** | TLS 1.3 encryption, certificate pinning |
| **Data Breach** | Encryption at rest (AES-256), encrypted backups |
| **Insider Threat** | Audit logging (all access logged), least privilege RBAC |
| **Physical Theft** | Full-disk encryption on cameras/servers, remote wipe |
| **Network Eavesdropping** | WPA3 WiFi encryption, VPN tunnels |
| **Denial of Service** | Rate limiting, CDN/reverse proxy, DDoS protection |

### Authentication & Authorization

**Keycloak (Identity Provider):**
```yaml
# Keycloak configuration
Realm: OS-GUARDIAN
Clients:
  - web-ui (React frontend)
  - api-server (FastAPI backend)
  - mobile-app (Flutter app)

Roles:
  - officer: View own evidence, upload videos
  - supervisor: View all evidence in department
  - investigator: Search, export, redact evidence
  - admin: Full system access, user management
  - legal: Export evidence, generate COC certificates

Authentication Methods:
  - Username/password (bcrypt hashed)
  - Multi-factor authentication (TOTP, SMS)
  - LDAP/Active Directory integration
  - SAML 2.0 / OAuth2 / OpenID Connect

Authorization:
  - Role-based access control (RBAC)
  - Attribute-based access control (ABAC)
  - Per-evidence permissions (officer can only view own videos)
```

**JWT Token Structure:**
```json
{
  "sub": "officer_5824",
  "name": "John Smith",
  "email": "john.smith@dept.gov",
  "roles": ["officer", "patrol"],
  "department": "north_precinct",
  "badge_number": "5824",
  "exp": 1702321234,
  "iat": 1702234834
}
```

### Encryption

**At Rest:**
- Body cameras: LUKS full-disk encryption on microSD (optional, performance impact)
- Evidence server: LUKS full-disk encryption on all drives
- MinIO: Server-side encryption (SSE-S3)
- PostgreSQL: Transparent Data Encryption (TDE) via pg_crypto

**In Transit:**
- TLS 1.3 for all HTTPS/WSS connections
- WPA3 encryption for WiFi (cameras to access points)
- VPN tunnels for multi-site deployments

### Network Segmentation

```
┌────────────────────────────────────────────────────────┐
│                    Public Internet                     │
│                      (untrusted)                       │
└────────────────────┬───────────────────────────────────┘
                     │
               ┌─────▼─────┐
               │ Firewall  │ (only ports 443, 22 open)
               └─────┬─────┘
                     │
┌────────────────────▼───────────────────────────────────┐
│                   DMZ (Public Zone)                    │
│  ┌──────────────┐  ┌──────────────┐                   │
│  │   NGINX      │  │   Keycloak   │                   │
│  │  (Reverse    │  │     (SSO)    │                   │
│  │   Proxy)     │  │              │                   │
│  └──────────────┘  └──────────────┘                   │
└────────────────────┬───────────────────────────────────┘
                     │
               ┌─────▼─────┐
               │ Firewall  │ (internal only)
               └─────┬─────┘
                     │
┌────────────────────▼───────────────────────────────────┐
│                Internal Network (Private Zone)         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Evidence    │  │  PostgreSQL  │  │    MinIO     │ │
│  │  Server      │  │   Database   │  │   Storage    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│  ┌──────────────┐  ┌──────────────┐                   │
│  │  Blockchain  │  │    MQTT      │                   │
│  │   Service    │  │    Broker    │                   │
│  └──────────────┘  └──────────────┘                   │
└────────────────────┬───────────────────────────────────┘
                     │
               ┌─────▼─────┐
               │WiFi Access│ (separate VLAN)
               │   Points  │
               └─────┬─────┘
                     │
┌────────────────────▼───────────────────────────────────┐
│                Camera Network (Isolated VLAN)          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │ Camera 1 │  │ Camera 2 │  │ Camera 3 │  ...       │
│  └──────────┘  └──────────┘  └──────────┘            │
│                                                        │
│  VLAN: 192.168.100.0/24 (no internet access)          │
└────────────────────────────────────────────────────────┘
```

---

## Network Architecture

### Camera WiFi Auto-Connect

**File**: `/etc/wpa_supplicant/wpa_supplicant.conf` (on each camera)

```conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=US

# Priority 1: Evidence Server (fastest upload)
network={
    ssid="Guardian-Evidence-5GHz"
    psk="secure_password_here"
    priority=10
    scan_ssid=1
}

# Priority 2: Station WiFi (backup)
network={
    ssid="Police-Station-Guest"
    psk="another_password"
    priority=5
}

# Priority 3: Mobile Hotspot (patrol car)
network={
    ssid="Patrol-Unit-42-Hotspot"
    psk="hotspot_password"
    priority=3
}

# Priority 4: Any open network (last resort, insecure)
# network={
#     key_mgmt=NONE
#     priority=1
# }
```

### Upload Bandwidth Requirements

**Scenario**: 50 cameras, each recording 8 hours/day

```
Per Camera:
  Resolution: 1080p @ 30 FPS
  Bitrate: 4 Mbps
  Recording: 8 hours/day
  File Size: 4 Mbps × 8 hours = 32 Mb/hr × 8 = 14.4 GB/day

Total (50 cameras):
  Daily Upload: 50 × 14.4 GB = 720 GB/day
  Peak Upload (all cameras docking simultaneously):
    50 cameras × 4 Mbps = 200 Mbps

  Realistic Upload (staggered over 2 hours):
    720 GB / 2 hours = 360 GB/hr = 100 MB/s = 800 Mbps

Required Network:
  Internet uplink: 1 Gbps (if cloud backup enabled)
  Local LAN: 1 Gbps (sufficient for staggered uploads)
  WiFi: 802.11ac (WiFi 5), 5 GHz, 80 MHz channels = 866 Mbps per camera
```

---

## Scalability & Performance

### Single Server Capacity

**Hardware**: Raspberry Pi 4 (8GB RAM) or x86 server

| Metric | Capacity |
|--------|----------|
| **Cameras Supported** | 1-50 cameras |
| **Concurrent Uploads** | 10 cameras |
| **Storage** | 1-4TB (30-120 days retention @ 50 cameras) |
| **Live Streams** | 5 concurrent WebRTC streams |
| **Database** | 1M evidence records (PostgreSQL) |
| **Throughput** | 100 Mbps upload bandwidth |

### Multi-Server Cluster (100-1,000 cameras)

```
┌────────────────────────────────────────────────────────┐
│                  Load Balancer (HAProxy)               │
│                   (HTTPS/WebSocket)                    │
└────────────────────┬───────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────▼────┐  ┌───▼─────┐  ┌──▼──────┐
   │Evidence │  │Evidence │  │Evidence │
   │Server 1 │  │Server 2 │  │Server 3 │
   │         │  │         │  │         │
   │Cameras  │  │Cameras  │  │Cameras  │
   │1-33     │  │34-66    │  │67-100   │
   └────┬────┘  └───┬─────┘  └──┬──────┘
        │           │           │
        └───────────┼───────────┘
                    │
         ┌──────────▼──────────┐
         │  PostgreSQL Cluster │
         │  (Primary + 2 Standby)│
         └──────────┬──────────┘
                    │
         ┌──────────▼──────────┐
         │   MinIO Cluster     │
         │   (Distributed Mode)│
         │   8 nodes, 100TB    │
         └─────────────────────┘
```

### Performance Benchmarks

**Upload Performance** (Raspberry Pi 4, WiFi 5):
- Single camera: 15 Mbps sustained upload
- 10 cameras (staggered): 100 Mbps aggregate
- Database insert rate: 500 records/second
- MinIO write throughput: 200 MB/s (4-node cluster)

**Query Performance** (PostgreSQL + TimescaleDB):
- Simple metadata query: <10ms
- Complex join (evidence + COC): 50-100ms
- Full-text search: 100-200ms
- Geospatial query (GPS radius): 150ms
- Time-series aggregation: 200-500ms

---

## High Availability & Redundancy

### Database HA (PostgreSQL with Patroni)

```yaml
# Patroni configuration for PostgreSQL HA
scope: guardian-cluster
name: postgres-01

restapi:
  listen: 0.0.0.0:8008
  connect_address: 192.168.1.101:8008

etcd:
  hosts: 192.168.1.201:2379,192.168.1.202:2379,192.168.1.203:2379

bootstrap:
  dcs:
    ttl: 30
    loop_wait: 10
    retry_timeout: 10
    maximum_lag_on_failover: 1048576
    postgresql:
      use_pg_rewind: true
      parameters:
        max_connections: 200
        shared_buffers: 2GB
        effective_cache_size: 6GB
        maintenance_work_mem: 512MB
        checkpoint_completion_target: 0.9
        wal_buffers: 16MB
        default_statistics_target: 100
        random_page_cost: 1.1
        effective_io_concurrency: 200
        work_mem: 10MB
        min_wal_size: 1GB
        max_wal_size: 4GB

postgresql:
  listen: 0.0.0.0:5432
  connect_address: 192.168.1.101:5432
  data_dir: /var/lib/postgresql/15/main
  pgpass: /tmp/pgpass0
  authentication:
    replication:
      username: replicator
      password: secure_password
    superuser:
      username: postgres
      password: admin_password
  parameters:
    unix_socket_directories: '/var/run/postgresql'
```

**Cluster Architecture:**
```
┌────────────────────────────────────────────────────────┐
│                    etcd Cluster (DCS)                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐            │
│  │  etcd-1  │  │  etcd-2  │  │  etcd-3  │            │
│  └──────────┘  └──────────┘  └──────────┘            │
│         (Distributed consensus / leader election)      │
└────────────────────┬───────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
   ┌────▼────┐  ┌───▼─────┐  ┌──▼──────┐
   │Postgres │  │Postgres │  │Postgres │
   │Primary  │  │Standby 1│  │Standby 2│
   │(Master) │  │(Replica)│  │(Replica)│
   │         │  │         │  │         │
   │Read/    │  │Read-Only│  │Read-Only│
   │Write    │  │         │  │         │
   └────┬────┘  └───┬─────┘  └──┬──────┘
        │           │           │
        │  Streaming Replication│
        └───────────┴───────────┘

Automatic Failover:
1. Primary fails → etcd detects (health checks)
2. Patroni elects new primary (standby-1 promoted)
3. DNS/VIP updated → traffic routes to new primary
4. Total downtime: <30 seconds
```

### MinIO HA (Distributed Mode)

```bash
# 8-node MinIO cluster (4 servers, 2 drives each)
docker run -d \
  -p 9000:9000 -p 9001:9001 \
  -v /mnt/disk1:/data1 \
  -v /mnt/disk2:/data2 \
  minio/minio server \
    http://minio-{1...4}/data{1...2} \
    --console-address ":9001"

# Features:
# - Erasure coding (N/2 data, N/2 parity = tolerate N/2 node failures)
# - Automatic healing (detect and repair corrupted objects)
# - Bitrot protection (checksums)
# - Versioning (keep all versions of evidence files)
```

### Backup Strategy

**3-2-1 Backup Rule:**
- **3** copies of data
- **2** different storage types
- **1** offsite backup

**Implementation:**
1. **Primary**: MinIO cluster (production storage)
2. **Secondary**: Daily backup to NAS (on-premise)
   ```bash
   # Cron job: Daily at 2 AM
   rclone sync minio:evidence-vault /mnt/nas-backup/evidence --progress
   ```
3. **Tertiary**: Weekly backup to cloud (AWS S3, Azure Blob)
   ```bash
   # Cron job: Weekly on Sunday at 3 AM
   rclone sync minio:evidence-vault s3:guardian-offsite-backup --progress
   ```

**Retention Policy:**
- Evidence files: 90 days (hot) → 1 year (warm) → 7 years (cold/archive)
- Database: Full backup daily, incremental hourly, retain 30 days
- Logs: 90 days

---

## Integration Architecture

### REST API Endpoints

**Base URL**: `https://guardian.example.com/api/v1`

#### Evidence Endpoints

```
GET    /evidence                   # List all evidence (paginated, filtered)
GET    /evidence/{evidence_id}     # Get specific evidence metadata
POST   /evidence/upload            # Upload new evidence from camera
GET    /evidence/{evidence_id}/download  # Download video file
POST   /evidence/{evidence_id}/view      # Log view access (COC record)
POST   /evidence/{evidence_id}/export    # Export evidence + COC certificate
DELETE /evidence/{evidence_id}     # Mark evidence for deletion (soft delete)

GET    /evidence/{evidence_id}/coc        # Get chain-of-custody history
GET    /evidence/{evidence_id}/thumbnail  # Get video thumbnail image
GET    /evidence/{evidence_id}/stream     # Get streaming URL (WebRTC/HLS)
```

**Example Request:**
```bash
curl -X GET https://guardian.example.com/api/v1/evidence \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..." \
  -G \
  --data-urlencode "officer_id=OFFICER_5824" \
  --data-urlencode "start_date=2024-12-01" \
  --data-urlencode "end_date=2024-12-07" \
  --data-urlencode "page=1" \
  --data-urlencode "per_page=20"
```

**Example Response:**
```json
{
  "total": 42,
  "page": 1,
  "per_page": 20,
  "evidence": [
    {
      "evidence_id": "EV-20241207143215-CAM001",
      "camera_id": "CAM001",
      "officer_id": "OFFICER_5824",
      "officer_name": "John Smith",
      "filename": "CAM001_OFFICER01_20241207_143215.h264",
      "file_size": 1247893504,
      "sha256_hash": "8f7b2c3e9a1d4f6b2e5c8a3f1d9b4e6c...",
      "duration": 300,
      "resolution": "1920x1080",
      "fps": 30,
      "recorded_at": "2024-12-07T14:32:15Z",
      "uploaded_at": "2024-12-07T14:45:32Z",
      "gps_start": {"lat": 45.4215, "lon": -75.6972},
      "gps_end": {"lat": 45.4218, "lon": -75.6975},
      "status": "verified",
      "thumbnail_url": "/api/v1/evidence/EV-20241207143215-CAM001/thumbnail"
    },
    ...
  ]
}
```

#### Camera Endpoints

```
GET    /cameras                    # List all cameras
GET    /cameras/{camera_id}        # Get camera details
POST   /cameras                    # Register new camera
PUT    /cameras/{camera_id}        # Update camera settings
DELETE /cameras/{camera_id}        # Decommission camera

GET    /cameras/{camera_id}/status # Get real-time status (battery, storage, GPS)
POST   /cameras/{camera_id}/command  # Send command (start recording, reboot)
```

#### Officer Endpoints

```
GET    /officers                   # List all officers
GET    /officers/{officer_id}      # Get officer details
POST   /officers                   # Create new officer
PUT    /officers/{officer_id}      # Update officer info
DELETE /officers/{officer_id}      # Deactivate officer

GET    /officers/{officer_id}/evidence  # Get all evidence for officer
```

### MQTT Topics

**Message Bus for Real-Time Events:**

```
guardian/cameras/{camera_id}/status
  Payload: {"status": "online", "battery": 85, "recording": true, "gps": {"lat": 45.4215, "lon": -75.6972}}
  Published: Every 60 seconds by each camera

guardian/evidence/new
  Payload: {"evidence_id": "EV-...", "camera_id": "CAM001", "officer_id": "OFFICER_5824", "timestamp": "2024-12-07T14:45:32Z"}
  Published: When new evidence uploaded

guardian/alerts/low_battery
  Payload: {"camera_id": "CAM001", "battery": 15, "timestamp": "2024-12-07T18:30:00Z"}
  Published: When battery <20%

guardian/alerts/storage_full
  Payload: {"camera_id": "CAM002", "storage_used_pct": 95, "timestamp": "2024-12-07T19:00:00Z"}
  Published: When storage >90% full

guardian/blockchain/new_block
  Payload: {"block_number": 1247, "transactions": 15, "timestamp": "2024-12-07T14:45:35Z"}
  Published: When new blockchain block created
```

**Subscriber Example (Python):**
```python
import paho.mqtt.client as mqtt
import json

def on_message(client, userdata, message):
    topic = message.topic
    payload = json.loads(message.payload.decode())

    if topic.startswith('guardian/alerts/'):
        print(f"🚨 ALERT: {topic}")
        print(f"   Details: {payload}")

        # Send email/SMS notification
        send_alert(payload)

client = mqtt.Client()
client.on_message = on_message
client.connect('mqtt.guardian.local', 1883)

# Subscribe to all alert topics
client.subscribe('guardian/alerts/#')

client.loop_forever()
```

### Integration with OS-PACS, OS-SENTINEL, OS-PATROL

**Unified Event Correlation:**

```
Scenario: Security officer badge swipe triggers body camera recording

1. Officer swipes badge at restricted door (OS-PACS)
   → MQTT: ospacs/access/granted
   → Payload: {officer_id: "OFFICER_5824", door: "Server Room", timestamp: "14:32:15"}

2. OS-GUARDIAN subscribes to ospacs/access/granted
   → Receives event
   → Checks: Is officer_id wearing body camera?
   → Sends command to CAM001: "Start 30-second pre-buffer recording"

3. CAM001 starts recording
   → Publishes: guardian/cameras/CAM001/status {"recording": true}

4. OS-SENTINEL (fixed cameras) receives same ospacs/access/granted event
   → Activates camera at Server Room door
   → Records 10 seconds pre-buffer + 60 seconds post-event

5. Both body camera + fixed camera footage linked to incident
   → Incident ID: INC-20241207-001
   → Evidence: [body_cam_video.h264, fixed_cam_video.mp4]
   → Timeline: Synchronized timestamps, GPS correlation
```

**Cross-Platform Evidence Package:**
```json
{
  "incident_id": "INC-20241207-001",
  "incident_type": "restricted_area_access",
  "timestamp": "2024-12-07T14:32:15Z",
  "location": {
    "address": "123 Main St, Server Room",
    "gps": {"lat": 45.4215, "lon": -75.6972}
  },
  "evidence": [
    {
      "source": "OS-GUARDIAN",
      "evidence_id": "EV-20241207143215-CAM001",
      "type": "body_camera_video",
      "officer_id": "OFFICER_5824",
      "duration": 90,
      "sha256": "8f7b2c3e9a1d...",
      "blockchain_tx": "0x742d35cc..."
    },
    {
      "source": "OS-SENTINEL",
      "evidence_id": "SEN-20241207143210-FIXED12",
      "type": "fixed_camera_video",
      "camera_location": "Server Room Door",
      "duration": 70,
      "sha256": "2e8c5a1f4d6b...",
      "blockchain_tx": "0x8a3f1d9b..."
    },
    {
      "source": "OS-PACS",
      "evidence_id": "PACS-20241207143215-ACCESS",
      "type": "access_log",
      "door_id": "DOOR_SERVERROOM",
      "access_result": "GRANTED",
      "credential_used": "Badge #5824"
    }
  ],
  "timeline": [
    {"time": "14:32:15", "event": "Badge swipe (OS-PACS)", "actor": "Officer Smith"},
    {"time": "14:32:16", "event": "Door unlocked (OS-PACS)", "actor": "System"},
    {"time": "14:32:17", "event": "Body camera activated (OS-GUARDIAN)", "actor": "System"},
    {"time": "14:32:18", "event": "Fixed camera recording started (OS-SENTINEL)", "actor": "System"},
    {"time": "14:32:30", "event": "Officer entered room", "actor": "Officer Smith"},
    {"time": "14:34:00", "event": "Officer exited room", "actor": "Officer Smith"},
    {"time": "14:34:05", "event": "Door auto-locked (OS-PACS)", "actor": "System"}
  ]
}
```

---

## Deployment Models

### 1. Single-Site Deployment (Small Police Dept, Security Team)

**Scale**: 1-50 cameras, single location

**Hardware**:
- 1× Evidence server (Raspberry Pi 4 8GB or x86 mini-PC)
- 1× 4TB external SSD (evidence storage)
- 1× WiFi access point (802.11ac)
- 1× Charging dock (10-port USB hub)

**Software**:
```bash
# docker-compose.yml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: guardian
      POSTGRES_USER: guardian
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_USER}
      MINIO_ROOT_PASSWORD: ${MINIO_PASSWORD}
    volumes:
      - ./minio-data:/data
    ports:
      - "9000:9000"
      - "9001:9001"

  ingestion:
    build: ./ingestion-service
    environment:
      DB_HOST: postgres
      MINIO_ENDPOINT: minio:9000
    ports:
      - "8000:8000"

  web-ui:
    build: ./web-ui
    ports:
      - "80:80"
      - "443:443"
```

**Total Cost**: ~$1,500 (server + storage + network equipment)

### 2. Multi-Site Deployment (City Police Dept, Retail Chain)

**Scale**: 100-500 cameras, 5-10 locations

**Architecture**: Hub-and-spoke
- Central evidence server (high-capacity)
- Edge servers at each site (local caching)
- VPN tunnels between sites

**Central Server**:
- 3× PostgreSQL nodes (Patroni HA cluster)
- 8× MinIO nodes (distributed mode, 100TB)
- Load balancer (HAProxy)

**Per-Site Edge Server**:
- 1× Raspberry Pi 4 (local ingestion, caching)
- 1× 4TB SSD (7-day local retention)
- Upload to central server overnight (off-peak hours)

**Total Cost**: ~$50,000 (central cluster) + ~$1,500/site × 10 sites = $65,000

### 3. Enterprise Deployment (State Police, University Campus)

**Scale**: 1,000-10,000 cameras, 50+ locations

**Architecture**: Regional hubs
- 5× Regional evidence servers (20 sites each)
- Central aggregation server (search, analytics, compliance)
- Kubernetes orchestration (auto-scaling, HA)
- CDN for video distribution

**Technology Stack**:
- Kubernetes (EKS, GKE, or on-premise)
- Ceph or GlusterFS (distributed storage)
- Elasticsearch (fast search across billions of records)
- Kafka (high-throughput event streaming)

**Total Cost**: ~$500,000-1M (infrastructure) + ~$100/camera/year (maintenance)

---

## Monitoring & Operations

### Prometheus Metrics

**Exported by Evidence Server:**

```yaml
# Evidence upload metrics
guardian_evidence_uploads_total{camera_id="CAM001", status="success"} 1247
guardian_evidence_uploads_total{camera_id="CAM002", status="failed"} 3
guardian_evidence_upload_duration_seconds{camera_id="CAM001", quantile="0.5"} 12.3
guardian_evidence_upload_duration_seconds{camera_id="CAM001", quantile="0.99"} 45.7

# Storage metrics
guardian_storage_used_bytes{bucket="evidence-vault"} 3248912384000  # 3.2TB
guardian_storage_total_bytes{bucket="evidence-vault"} 4000000000000  # 4TB
guardian_storage_utilization_percent{bucket="evidence-vault"} 81.2

# Database metrics
guardian_database_connections_active 42
guardian_database_connections_idle 8
guardian_database_query_duration_seconds{query_type="insert", quantile="0.5"} 0.012
guardian_database_query_duration_seconds{query_type="search", quantile="0.99"} 0.385

# Camera metrics
guardian_cameras_total 50
guardian_cameras_online 48
guardian_cameras_offline 2
guardian_camera_battery_percent{camera_id="CAM001"} 85
guardian_camera_storage_used_percent{camera_id="CAM001"} 67

# Blockchain metrics
guardian_blockchain_blocks_total 1247
guardian_blockchain_transactions_total 18423
guardian_blockchain_verification_duration_seconds{quantile="0.99"} 0.234
```

**Grafana Dashboard:**

```json
{
  "dashboard": {
    "title": "OS-GUARDIAN Operations Dashboard",
    "panels": [
      {
        "title": "Evidence Upload Rate",
        "targets": [
          {
            "expr": "rate(guardian_evidence_uploads_total[5m])",
            "legendFormat": "{{camera_id}} - {{status}}"
          }
        ]
      },
      {
        "title": "Storage Utilization",
        "targets": [
          {
            "expr": "guardian_storage_utilization_percent",
            "legendFormat": "{{bucket}}"
          }
        ]
      },
      {
        "title": "Camera Status Map",
        "type": "geomap",
        "targets": [
          {
            "expr": "guardian_camera_battery_percent",
            "format": "table"
          }
        ]
      }
    ]
  }
}
```

### Alerting Rules

**Prometheus Alertmanager:**

```yaml
groups:
  - name: guardian_alerts
    interval: 60s
    rules:
      # Low battery alert
      - alert: CameraLowBattery
        expr: guardian_camera_battery_percent < 20
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Camera {{$labels.camera_id}} has low battery ({{$value}}%)"
          description: "Please charge or replace battery for camera {{$labels.camera_id}}"

      # Storage almost full
      - alert: StorageAlmostFull
        expr: guardian_storage_utilization_percent > 90
        for: 10m
        labels:
          severity: critical
        annotations:
          summary: "Evidence storage is {{$value}}% full"
          description: "Storage {{$labels.bucket}} is running out of space. Add more drives or purge old evidence."

      # Camera offline
      - alert: CameraOffline
        expr: guardian_cameras_offline > 0
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "{{$value}} camera(s) are offline"
          description: "Check camera connectivity and battery status"

      # Upload failures
      - alert: EvidenceUploadFailures
        expr: rate(guardian_evidence_uploads_total{status="failed"}[10m]) > 0.1
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High rate of evidence upload failures"
          description: "{{$value}} uploads/min are failing. Check network and server health."

      # Database slow queries
      - alert: DatabaseSlowQueries
        expr: guardian_database_query_duration_seconds{quantile="0.99"} > 1.0
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Database queries are slow (p99: {{$value}}s)"
          description: "Review database indexes and query performance"

      # Blockchain verification failures
      - alert: BlockchainVerificationFailure
        expr: rate(guardian_blockchain_verification_errors_total[10m]) > 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Blockchain verification errors detected"
          description: "Evidence integrity may be compromised. Investigate immediately."
```

---

## Compliance Frameworks

### CJIS (Criminal Justice Information Services)

**Requirements**:
- Advanced authentication (MFA)
- Audit logging (all access)
- Encryption (at rest and in transit)
- Incident response plan
- Security training for personnel

**OS-GUARDIAN Implementation**:
- ✓ Keycloak with MFA (TOTP, SMS)
- ✓ Comprehensive audit log (all evidence access)
- ✓ TLS 1.3 + AES-256 encryption
- ✓ Blockchain COC (tamper-evident)
- ✓ Role-based access control (RBAC)

**Compliance Checklist**:
```
[ ] Personnel background checks completed
[ ] Security awareness training (annual)
[ ] Multi-factor authentication enabled for all users
[ ] Password policy enforced (12+ chars, complexity, 90-day rotation)
[ ] Audit logs reviewed monthly
[ ] Incident response plan documented and tested
[ ] Data retention policy defined (7 years for evidence)
[ ] Encryption keys rotated annually
[ ] Disaster recovery plan tested quarterly
[ ] Third-party audit completed (annual)
```

### HIPAA (Healthcare)

**Relevant for**: Hospital security, healthcare body cameras

**Requirements**:
- Patient privacy (de-identify PHI)
- Access controls (minimum necessary)
- Audit trails (who accessed what)
- Breach notification (<60 days)
- Business Associate Agreements (BAAs)

**OS-GUARDIAN Implementation**:
- ✓ Face blur / redaction tools (auto-detect faces, pixelate)
- ✓ RBAC (nurses can't view other departments' footage)
- ✓ Chain-of-custody log (every view logged)
- ✓ Automated breach detection (unauthorized access = alert)

**Face Redaction (OpenCV):**
```python
import cv2

# Load video
video = cv2.VideoCapture('evidence.mp4')

# Load Haar Cascade face detector
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

while True:
    ret, frame = video.read()
    if not ret:
        break

    # Detect faces
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Blur each face
    for (x, y, w, h) in faces:
        face_roi = frame[y:y+h, x:x+w]
        blurred_face = cv2.GaussianBlur(face_roi, (99, 99), 30)
        frame[y:y+h, x:x+w] = blurred_face

    # Write redacted frame to output video
    output.write(frame)

video.release()
output.release()
```

### GDPR (EU Data Protection)

**Requirements**:
- Data minimization (collect only necessary)
- Right to be forgotten (delete on request)
- Data portability (export in standard format)
- Consent management
- Data breach notification (<72 hours)

**OS-GUARDIAN Implementation**:
- ✓ Configurable retention (auto-delete after X days)
- ✓ Soft delete + purge mechanism (irreversible deletion)
- ✓ Export API (download all evidence in standard format)
- ✓ Consent logging (record when individuals appear in videos)
- ✓ Breach detection (alert on unauthorized access)

---

## Disaster Recovery

### Backup & Restore Procedures

**Full System Backup:**
```bash
#!/bin/bash
# backup-guardian.sh - Full system backup

BACKUP_DIR="/mnt/nas-backup/guardian-backup-$(date +%Y%m%d)"
mkdir -p $BACKUP_DIR

# 1. Database dump
docker-compose exec -T postgres pg_dump -U guardian guardian > $BACKUP_DIR/database.sql

# 2. MinIO data (incremental)
rclone sync minio:evidence-vault $BACKUP_DIR/evidence --progress

# 3. Configuration files
tar -czf $BACKUP_DIR/config.tar.gz \
  docker-compose.yml \
  ingestion-service/ \
  web-ui/ \
  nginx.conf

# 4. Blockchain ledger
tar -czf $BACKUP_DIR/blockchain.tar.gz blockchain-data/

# 5. Generate backup manifest
cat > $BACKUP_DIR/MANIFEST.txt <<EOF
Backup Date: $(date)
Database Size: $(du -sh $BACKUP_DIR/database.sql | cut -f1)
Evidence Size: $(du -sh $BACKUP_DIR/evidence | cut -f1)
Total Size: $(du -sh $BACKUP_DIR | cut -f1)

Files:
$(ls -lh $BACKUP_DIR)
EOF

echo "✓ Backup completed: $BACKUP_DIR"
```

**Restore Procedure:**
```bash
#!/bin/bash
# restore-guardian.sh - Restore from backup

BACKUP_DIR=$1

if [ -z "$BACKUP_DIR" ]; then
  echo "Usage: ./restore-guardian.sh /path/to/backup"
  exit 1
fi

# 1. Stop services
docker-compose down

# 2. Restore database
cat $BACKUP_DIR/database.sql | docker-compose exec -T postgres psql -U guardian guardian

# 3. Restore evidence files
rclone sync $BACKUP_DIR/evidence minio:evidence-vault

# 4. Restore configuration
tar -xzf $BACKUP_DIR/config.tar.gz

# 5. Restore blockchain ledger
tar -xzf $BACKUP_DIR/blockchain.tar.gz

# 6. Restart services
docker-compose up -d

echo "✓ Restore completed from: $BACKUP_DIR"
```

### RTO & RPO Targets

| Deployment Scale | RTO (Recovery Time Objective) | RPO (Recovery Point Objective) |
|------------------|-------------------------------|--------------------------------|
| **Single-Site** | 4 hours | 24 hours (daily backups) |
| **Multi-Site** | 1 hour | 1 hour (continuous replication) |
| **Enterprise** | 15 minutes | 0 minutes (real-time HA cluster) |

### Disaster Scenarios

**Scenario 1: Server Hardware Failure**
- Detection: Prometheus alerts "server down"
- Action: Failover to standby server (automatic with Patroni)
- Impact: 30 seconds downtime
- Recovery: Replace failed server, re-join cluster

**Scenario 2: Ransomware Attack**
- Detection: File integrity monitoring (FIM) alerts
- Action: Isolate affected systems, restore from offline backups
- Impact: 4-12 hours downtime
- Recovery: Rebuild from clean backups, patch vulnerabilities

**Scenario 3: Natural Disaster (Fire, Flood)**
- Detection: Site offline, no heartbeat
- Action: Activate offsite backup datacenter
- Impact: 2-4 hours (DNS updates, traffic reroute)
- Recovery: Provision new hardware, restore from cloud backups

---

## Cost Modeling at Scale

### 100-Camera Deployment (Medium Police Dept)

**Hardware Costs** (one-time):
| Item | Quantity | Unit Price | Total |
|------|----------|------------|-------|
| **Body Cameras (Professional)** | 100 | $200 | $20,000 |
| **Charging Docks** | 5 | $200 | $1,000 |
| **Evidence Server (x86)** | 3 | $2,000 | $6,000 |
| **Storage (50TB NAS)** | 1 | $5,000 | $5,000 |
| **Network Equipment** | 1 set | $2,000 | $2,000 |
| **Installation & Training** | - | - | $5,000 |
| **Total Hardware** | | | **$39,000** |

**Software Costs** (annual):
| Item | Cost |
|------|------|
| **OS-GUARDIAN Software** | $0 (open-source) |
| **Support Contract (optional)** | $5,000/year |
| **Cloud Backup (AWS S3)** | $1,200/year (5TB) |
| **Total Annual Software** | **$6,200/year** |

**5-Year TCO**:
- Year 0: $39,000 (hardware) + $6,200 (software) = $45,200
- Years 1-4: $6,200/year × 4 = $24,800
- **Total 5-Year Cost**: $70,000

**Cost per Camera (5-year)**:
- $70,000 / 100 cameras = **$700/camera** over 5 years
- **$140/camera/year**

### Comparison to Proprietary Solutions

**Axon Body 3** (100 cameras, 5 years):
| Item | Cost |
|------|------|
| Camera Hardware | 100 × $800 = $80,000 |
| Evidence.com Subscription | 100 × $99/month × 60 months = $594,000 |
| **Total 5-Year Cost** | **$674,000** |
| **Cost per Camera** | **$6,740/camera** over 5 years |

**Motorola VB400** (100 cameras, 5 years):
| Item | Cost |
|------|------|
| Camera Hardware | 100 × $1,200 = $120,000 |
| VideoManager Subscription | 100 × $89/month × 60 months = $534,000 |
| **Total 5-Year Cost** | **$654,000** |
| **Cost per Camera** | **$6,540/camera** over 5 years |

**Cost Savings: OS-GUARDIAN vs Proprietary**:
- Axon: $674,000 - $70,000 = **$604,000 saved (90% savings)**
- Motorola: $654,000 - $70,000 = **$584,000 saved (89% savings)**

---

## Conclusion

OS-GUARDIAN provides an enterprise-grade, legally admissible body camera and evidence management solution at a fraction of the cost of proprietary systems. By leveraging open-source technologies, commodity hardware (Raspberry Pi), and blockchain chain-of-custody, organizations can deploy scalable, secure, and compliant evidence management from 1 to 10,000+ cameras.

**Key Benefits**:
- ✓ **90% cost savings** vs Axon/Motorola
- ✓ **Zero vendor lock-in**: Own your data, hardware, software
- ✓ **Legally admissible**: Blockchain COC, cryptographic signatures
- ✓ **Privacy-first**: On-premise deployment, no cloud requirement
- ✓ **Scalable**: Single server to multi-site clusters
- ✓ **Compliance-ready**: CJIS, HIPAA, GDPR, FOIA
- ✓ **Integration-ready**: REST/MQTT APIs, works with OS-PACS, OS-SENTINEL, OS-PATROL

**Next Steps**:
1. Build demo kit (2-4 cameras, evidence server)
2. Pilot deployment (10-20 cameras, single site)
3. Evaluate results (evidence quality, cost savings, user feedback)
4. Scale to full deployment (100+ cameras, multi-site)

---

**Technical Support**:
- Documentation: docs.opensecure.io/os-guardian
- Community Forum: forum.opensecure.io
- Email: support@opensecure.io
- GitHub: github.com/opensecure/os-guardian

**Commercial Support & Services**:
- Deployment assistance: $5,000-50,000 (based on scale)
- Custom development: $150/hour
- Training & certification: $2,000 per cohort
- Annual support contract: $5,000-50,000 (based on camera count)

Contact: enterprise@opensecure.io
