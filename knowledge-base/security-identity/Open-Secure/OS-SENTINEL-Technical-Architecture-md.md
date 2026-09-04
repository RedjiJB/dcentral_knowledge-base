---
source_project: Open Secure
source_project_uuid: 019cba7f-8d2d-72ed-bbc7-a730cc31b95e
doc_uuid: ec910805-50ad-4acd-8243-463bd976e7d3
original_filename: OS-SENTINEL_Technical_Architecture.md
created_at: 2026-03-04T20:34:08.954514+00:00
content_hash: aafaaacda0b4topic: lag-kubernetes-interval
---

# OS-SENTINEL - Complete Technical Architecture
## AI-Powered Video Surveillance & Analytics Platform

**Document Type**: Technical Architecture
**Version**: 1.0
**Date**: December 2024
**Classification**: Technical Documentation
**Audience**: Technical Leaders, Security Architects, AI/ML Engineers, System Engineers

---

## Table of Contents

1. [Executive Technical Summary](#executive-technical-summary)
2. [System Architecture Overview](#system-architecture-overview)
3. [Core Technology Deep-Dive](#core-technology-deep-dive)
4. [Component Architecture](#component-architecture)
5. [AI/ML Architecture](#aiml-architecture)
6. [Data Architecture](#data-architecture)
7. [Video Processing Pipeline](#video-processing-pipeline)
8. [Security Architecture](#security-architecture)
9. [Network Architecture](#network-architecture)
10. [Scalability & Performance](#scalability--performance)
11. [High Availability & Redundancy](#high-availability--redundancy)
12. [Integration Architecture](#integration--architecture)
13. [Deployment Models](#deployment-models)
14. [Monitoring & Operations](#monitoring--operations)
15. [Compliance Frameworks](#compliance-frameworks)
16. [Disaster Recovery](#disaster-recovery)
17. [Cost Modeling at Scale](#cost-modeling-at-scale)

---

## Executive Technical Summary

### Platform Overview

OS-SENTINEL is an enterprise-grade, AI-powered video surveillance platform built on Frigate NVR core technology, designed for organizations requiring real-time intelligent video analytics with complete control over their video infrastructure and AI models without proprietary vendor lock-in.

**Core Design Principles:**

- **Edge-First AI Processing**: Real-time inference at camera edge (sub-100ms latency)
- **GPU/TPU Acceleration**: Native support for NVIDIA CUDA, Google Coral TPU, Intel OpenVINO
- **Privacy-Preserving**: On-premise AI (no cloud transmission of video)
- **Protocol Agnostic**: RTSP, ONVIF, HTTP, WebRTC streaming
- **Hardware Neutral**: Runs on x86, ARM (Raspberry Pi to enterprise servers)
- **Model Flexible**: YOLOv8, TensorFlow, PyTorch, ONNX, custom models
- **Database-Centric**: PostgreSQL + TimescaleDB for events, MinIO for video storage
- **API-First**: REST/WebSocket/MQTT APIs for all operations
- **Compliance-Ready**: HIPAA, GDPR, CCPA, SOC2, CJIS compatible

### Scale Characteristics

| Deployment Scale | Cameras | Processing | Storage | Architecture |
|------------------|---------|------------|---------|--------------|
| **Small** | 1-10 | Single GPU/Coral TPU | 1-2TB NVMe SSD | Single server |
| **Medium** | 10-100 | Multi-GPU cluster | 10-50TB NAS | Distributed processing |
| **Enterprise** | 100-1,000 | GPU farm + edge TPUs | 100TB-1PB SAN | Hub-and-spoke |
| **Campus** | 1,000-10,000+ | Regional GPU clusters | Multi-PB object storage | Hierarchical federation |

### Technology Stack

**Core Platform:**
- Frigate NVR 0.13+ (Python, real-time video processing)
- FFmpeg 6.0+ (video encoding/decoding/transcoding)
- PostgreSQL 15+ with TimescaleDB (time-series event storage)
- MinIO (S3-compatible video object storage)
- MQTT (Eclipse Mosquitto, event streaming)
- Docker + Kubernetes (containerized deployment)

**AI/ML Framework:**
- YOLOv8 (Ultralytics, primary object detection)
- TensorFlow Lite (mobile/edge deployment)
- PyTorch (custom model training)
- ONNX Runtime (model portability)
- OpenVINO (Intel CPU optimization)
- TensorRT (NVIDIA GPU optimization)

**Acceleration Hardware:**
- Google Coral TPU (13 TOPS, USB/PCIe/M.2)
- NVIDIA GPUs (RTX 4090: 82 TFLOPS, A100: 312 TFLOPS)
- Intel Neural Compute Stick 2 (1 TOPS)
- Raspberry Pi AI HAT (26 TOPS)

**Supported Cameras:**
- ONVIF-compliant IP cameras (1,000+ models)
- RTSP H.264/H.265 streams
- USB cameras (UVC protocol)
- ESP32-CAM (DIY cameras)
- Raspberry Pi Camera Modules

**Integration Protocols:**
- REST API (JSON over HTTPS)
- MQTT (pub/sub events)
- WebSocket (real-time streams)
- WebRTC (low-latency browser streaming)
- gRPC (high-performance service-to-service)

---

## System Architecture Overview

### Layered Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Presentation Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Web UI     │  │  Mobile App  │  │   Grafana    │             │
│  │  (React +    │  │  (Flutter)   │  │  Analytics   │             │
│  │   WebRTC)    │  │              │  │  Dashboards  │             │
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
│  │  • Rate Limiting & Throttling                                │  │
│  │  • WebRTC Signaling Proxy                                    │  │
│  │  • Static Asset Serving                                      │  │
│  │  • TLS Termination                                           │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                          Internal APIs
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Application Services Layer                        │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │  Frigate  │  │  AI/ML    │  │ MediaMTX  │  │   User    │       │
│  │   NVR     │  │ Analytics │  │ Streaming │  │   Auth    │       │
│  │  Service  │  │  Service  │  │  Server   │  │ (Keycloak)│       │
│  │           │  │           │  │           │  │           │       │
│  │ • Camera  │  │ • YOLOv8  │  │ • WebRTC  │  │ • SSO     │       │
│  │   Mgmt    │  │ • Face    │  │ • RTSP    │  │ • RBAC    │       │
│  │ • Record  │  │   Recog   │  │ • HLS     │  │ • MFA     │       │
│  │ • Detect  │  │ • LPR     │  │ • Transcode│  │ • Audit   │       │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘       │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐       │
│  │  Storage  │  │   Event   │  │  Workflow │  │  Alert    │       │
│  │  Manager  │  │  Engine   │  │  Service  │  │  Service  │       │
│  │           │  │           │  │           │  │           │       │
│  │ • Tiering │  │ • CEP     │  │ • Node-RED│  │ • Email   │       │
│  │ • Cleanup │  │ • Filters │  │ • Triggers│  │ • SMS     │       │
│  │ • Backup  │  │ • Alerts  │  │ • Actions │  │ • Push    │       │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘       │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                        Message Bus (MQTT)
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Message Broker Layer                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Eclipse Mosquitto (MQTT Broker)                             │  │
│  │  • frigate/events/* - Detection events                       │  │
│  │  • frigate/stats/* - System statistics                       │  │
│  │  • frigate/alerts/* - Alert notifications                    │  │
│  │  • frigate/cameras/+/status - Camera status                  │  │
│  │  • sentinel/analytics/* - AI inference results               │  │
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
│  │ • Events  │  │ • Video   │  │ • Frames  │  │ • FPS     │       │
│  │ • Objects │  │   Clips   │  │ • Sessions│  │ • Latency │       │
│  │ • Metadata│  │ • Snapshots│  │ • Live    │  │ • GPU%    │       │
│  │ • Faces   │  │ • Exports │  │   State   │  │ • Detections│      │
│  │ • Plates  │  │ • S3 API  │  │ • Pub/Sub │  │ • Errors  │       │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘       │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                          RTSP/ONVIF/HTTP
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        Edge Processing Layer                         │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │            Edge Server (per site/building)                    │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐         │  │
│  │  │ Frigate │  │MediaMTX │  │  YOLO   │  │  TPU    │         │  │
│  │  │  Edge   │  │  Proxy  │  │ Detector│  │ Accel   │         │  │
│  │  │         │  │         │  │         │  │         │         │  │
│  │  │ • Local │  │ • RTSP  │  │ • Edge  │  │ • Coral │         │  │
│  │  │   Record│  │   Proxy │  │   AI    │  │   TPU   │         │  │
│  │  │ • Motion│  │ • WebRTC│  │ • 30 FPS│  │ • 13    │         │  │
│  │  │   Detect│  │ • Cache │  │ • Low   │  │   TOPS  │         │  │
│  │  │ • Upload│  │ • Buffer│  │   Latency│  │         │         │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘         │  │
│  │                                                                │  │
│  │  Local Storage: 1-4TB NVMe SSD (7-14 days hot retention)      │  │
│  │  Network: Isolated camera VLAN, 1Gbps uplink to core          │  │
│  └──────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                ▲
                          RTSP/ONVIF
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       Camera Layer                                   │
│                                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ IP Camera│  │ PTZ Cam  │  │ LPR Cam  │  │ USB Cam  │           │
│  │ RTSP/ONVIF│  │ (Pan/Tilt│  │ (License │  │ (Local)  │           │
│  │ H.265    │  │  Zoom)   │  │  Plate)  │  │          │           │
│  │ 1080p-4K │  │          │  │          │  │          │           │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
│                                                                     │
│  Protocols: RTSP, ONVIF, HTTP, MJPEG                               │
│  Network: PoE (802.3af/at), isolated VLAN (192.168.100.0/24)      │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Architectural Decisions

| Decision | Rationale | Trade-off |
|----------|-----------|-----------|
| **Frigate NVR Core** | Modern Python codebase, MQTT-native, active development, AI-first design | Smaller ecosystem vs Zoneminder/MotionEye |
| **Edge AI Processing** | <100ms inference, privacy (no cloud), reduced bandwidth | Higher edge hardware cost vs cloud SaaS |
| **PostgreSQL + TimescaleDB** | Time-series optimized, excellent querying, ACID compliance | Not horizontally scalable like Cassandra |
| **MinIO for Video** | S3-compatible, Kubernetes-native, tiering support | More complex than simple NAS |
| **MQTT Event Bus** | Lightweight, publish-subscribe, IoT-standard | Less enterprise features vs Kafka |
| **YOLOv8 Detection** | State-of-art accuracy, fast, easy to customize | Larger model size vs MobileNet |
| **WebRTC Streaming** | Sub-second latency, browser-native, NAT traversal | More complex setup vs RTSP |
| **GPU Acceleration** | 10-50x faster than CPU, enables real-time 4K | Higher hardware cost, power consumption |

---

## Core Technology Deep-Dive

### Frigate NVR Architecture

Frigate is the core video management and AI processing engine. Written in Python with C/C++ performance-critical components.

**Component Structure:**

```
┌────────────────────────────────────────────┐
│           Frigate Process (Python)          │
│                                             │
│  ┌────────────────────────────────────┐    │
│  │  Camera Manager                    │    │
│  │  • ONVIF Discovery                 │    │
│  │  • RTSP Connection Pool            │    │
│  │  • Stream Health Monitoring        │    │
│  │  • Auto-Reconnect                  │    │
│  └────────────────────────────────────┘    │
│                     ▼                       │
│  ┌────────────────────────────────────┐    │
│  │  FFmpeg Wrapper (go2rtc)           │    │
│  │  • RTSP → Raw Frames               │    │
│  │  • H.264/H.265 Decoding            │    │
│  │  • Frame Rate Control              │    │
│  │  • Resolution Scaling              │    │
│  └────────────────────────────────────┘    │
│                     ▼                       │
│  ┌────────────────────────────────────┐    │
│  │  Detector Process (subprocess)     │    │
│  │  ┌──────────────────────────────┐  │    │
│  │  │ Model: YOLOv8n.tflite        │  │    │
│  │  │ Accelerator: Coral TPU       │  │    │
│  │  │ Input: 320x320 RGB           │  │    │
│  │  │ Output: Bounding boxes       │  │    │
│  │  │ Throughput: 30 FPS           │  │    │
│  │  └──────────────────────────────┘  │    │
│  └────────────────────────────────────┘    │
│                     ▼                       │
│  ┌────────────────────────────────────┐    │
│  │  Object Tracker                    │    │
│  │  • DeepSORT Algorithm              │    │
│  │  • Track ID Assignment             │    │
│  │  • Kalman Filter Prediction        │    │
│  │  • Zone Crossing Detection         │    │
│  └────────────────────────────────────┘    │
│                     ▼                       │
│  ┌────────────────────────────────────┐    │
│  │  Event Manager                     │    │
│  │  • Event Lifecycle                 │    │
│  │  • Clip Generation                 │    │
│  │  • Snapshot Capture                │    │
│  │  • MQTT Publishing                 │    │
│  └────────────────────────────────────┘    │
│                     ▼                       │
│  ┌────────────────────────────────────┐    │
│  │  Storage Manager                   │    │
│  │  • MinIO S3 Upload                 │    │
│  │  • Local Cache (tmpfs)             │    │
│  │  • Retention Enforcement           │    │
│  │  • Tiering Logic                   │    │
│  └────────────────────────────────────┘    │
│                     ▼                       │
│  ┌────────────────────────────────────┐    │
│  │  API Server (Flask)                │    │
│  │  • REST Endpoints                  │    │
│  │  • WebSocket Feeds                 │    │
│  │  • Authentication                  │    │
│  │  • Rate Limiting                   │    │
│  └────────────────────────────────────┘    │
└────────────────────────────────────────────┘
```

### Frigate Configuration Deep-Dive

**File**: `config/config.yml`

```yaml
# MQTT Configuration
mqtt:
  enabled: true
  host: mosquitto
  port: 1883
  topic_prefix: frigate
  user: frigate_user
  password: secure_password
  client_id: frigate_main

# Database Configuration
database:
  path: postgresql://frigate:password@postgres:5432/frigate_db

# Detectors (AI Accelerators)
detectors:
  # Primary: Google Coral TPU
  coral:
    type: edgetpu
    device: usb
    num_threads: 2

  # Fallback: CPU (OpenVINO optimized)
  cpu_openvino:
    type: openvino
    device: CPU
    num_threads: 4

  # GPU: NVIDIA TensorRT
  # gpu_tensorrt:
  #   type: tensorrt
  #   device: 0  # GPU index

# AI Models
model:
  path: /config/models/yolov8n_320x320.tflite
  input_tensor: nhwc
  input_pixel_format: rgb
  width: 320
  height: 320
  labelmap_path: /config/models/coco_labelmap.txt

# Global object detection settings
objects:
  track:
    - person
    - car
    - truck
    - bicycle
    - motorcycle
    - dog
    - cat
  filters:
    person:
      min_area: 2500          # 50x50 pixels at 1080p
      max_area: 100000        # Ignore if too large (likely false positive)
      min_score: 0.70         # 70% confidence minimum
      threshold: 0.75         # 75% IOU for tracking
    car:
      min_area: 10000
      max_area: 300000
      min_score: 0.65
      threshold: 0.70

# Recording settings (global defaults)
record:
  enabled: true
  retain:
    days: 7                   # Hot storage: 7 days
    mode: motion              # Only record when motion detected
  events:
    retain:
      default: 30             # Event clips: 30 days
      mode: active_objects
    pre_capture: 10           # 10 seconds before event
    post_capture: 30          # 30 seconds after event
  export:
    timelapse_args: "-vf setpts=0.04*PTS -r 30"

# Snapshot settings
snapshots:
  enabled: true
  clean_copy: true            # No bounding boxes (for privacy)
  timestamp: false
  bounding_box: true
  crop: false
  retain:
    default: 14               # 14 days retention
    objects:
      person: 30              # 30 days for person snapshots

# Live streaming
live:
  stream_name: "{camera_name}_live"
  height: 720                 # Reduce resolution for bandwidth
  quality: 8                  # VP9 quality (1-31, lower = better)

# Camera definitions
cameras:
  # ========================================
  # Camera 1: Front Entrance (High Traffic)
  # ========================================
  front_entrance:
    enabled: true

    # FFmpeg stream configuration
    ffmpeg:
      inputs:
        # Main stream (high resolution for recording)
        - path: rtsp://admin:password@192.168.100.101/stream1
          roles:
            - record
            - detect

        # Sub-stream (lower resolution for detection - less bandwidth)
        # - path: rtsp://admin:password@192.168.100.101/stream2
        #   roles:
        #     - detect

      # Output arguments (quality settings)
      output_args:
        record: -f segment -segment_time 10 -segment_format mp4 -reset_timestamps 1 -strftime 1 -c:v copy -c:a aac

    # Detection settings (override global)
    detect:
      enabled: true
      width: 1920
      height: 1080
      fps: 5                  # 5 FPS sufficient for detection (reduce GPU load)
      stationary:
        interval: 50          # Check for stationary objects every 50 frames
        threshold: 100        # 100 frames = 20 seconds at 5 FPS

    # Camera-specific object filters
    objects:
      track:
        - person
        - car
        - truck
        - bicycle
      filters:
        person:
          min_area: 5000      # Larger threshold for front entrance
          max_area: 100000
          min_score: 0.75     # Higher confidence (busy area, reduce false positives)
          threshold: 0.80
          mask:               # Ignore areas (privacy zones, static objects)
            - 0,0,0,200,200,200,200,0  # Top-left corner (coordinates)

    # Motion detection (pre-filter for AI)
    motion:
      mask:
        - 0,0,1920,100        # Ignore top 100 pixels (timestamp overlay)
      threshold: 30           # Sensitivity (1-255, lower = more sensitive)
      contour_area: 10        # Minimum contour area
      delta_alpha: 0.2        # Smoothing factor
      frame_alpha: 0.01       # Background learning rate
      frame_height: 100       # Resize for motion detection (faster)

    # Zone definitions (virtual tripwires)
    zones:
      entrance_zone:
        coordinates: 400,1080,1520,1080,1520,200,400,200  # Rectangle
        objects:
          - person
        filters:
          person:
            min_area: 5000
            threshold: 0.8

      parking_lot:
        coordinates: 0,800,400,800,400,1080,0,1080
        objects:
          - car
          - truck
        filters:
          car:
            min_area: 20000

    # Recording overrides
    record:
      enabled: true
      retain:
        days: 14              # Front entrance: keep 14 days
        mode: motion
      events:
        retain:
          default: 60         # Event clips: 60 days (important entrance)

    # Snapshots
    snapshots:
      enabled: true
      timestamp: true
      bounding_box: true
      crop: true              # Crop to object for alerts
      retain:
        default: 30
        objects:
          person: 90          # Front entrance person snapshots: 90 days

    # ONVIF PTZ (if camera supports)
    onvif:
      host: 192.168.100.101
      port: 80
      user: admin
      password: password
      autotracking:
        enabled: false        # Disable auto-tracking (static view)

    # Timestamps
    timestamp_style:
      position: "tl"          # Top-left
      format: "%Y-%m-%d %H:%M:%S"
      color:
        red: 255
        green: 255
        blue: 255
      thickness: 2
      effect: shadow

  # ========================================
  # Camera 2: Parking Lot (LPR Focus)
  # ========================================
  parking_lpr:
    enabled: true

    ffmpeg:
      inputs:
        - path: rtsp://admin:password@192.168.100.102/stream1
          roles:
            - record
            - detect

    detect:
      enabled: true
      width: 1920
      height: 1080
      fps: 10                 # Higher FPS for moving vehicles

    objects:
      track:
        - car
        - truck
        - motorcycle
        - license_plate       # Custom trained model
      filters:
        car:
          min_area: 15000
          max_area: 500000
          min_score: 0.70
        license_plate:
          min_area: 500       # Small objects
          max_area: 5000
          min_score: 0.80     # High confidence for LPR

    zones:
      entrance_gate:
        coordinates: 600,400,1320,400,1320,800,600,800
        objects:
          - car
          - license_plate

    record:
      enabled: true
      retain:
        days: 30              # Parking violations require longer retention
        mode: all             # Continuous recording for LPR

  # ========================================
  # Camera 3: Warehouse (PPE Detection)
  # ========================================
  warehouse_floor:
    enabled: true

    ffmpeg:
      inputs:
        - path: rtsp://admin:password@192.168.100.103/stream1
          roles:
            - record
            - detect

    detect:
      enabled: true
      width: 1920
      height: 1080
      fps: 5

    objects:
      track:
        - person
        - forklift
        - hard_hat            # Custom PPE model
        - safety_vest
      filters:
        person:
          min_area: 3000
          min_score: 0.75
        hard_hat:
          min_area: 200       # Small object (on head)
          max_area: 2000
          min_score: 0.70

    zones:
      production_area:
        coordinates: 200,200,1720,200,1720,880,200,880
        objects:
          - person
        filters:
          person:
            min_area: 3000
            threshold: 0.80

    record:
      enabled: true
      retain:
        days: 90              # OSHA compliance: 90 days

  # ========================================
  # Camera 4: Retail Aisle (Shoplifting Detection)
  # ========================================
  retail_aisle_3:
    enabled: true

    ffmpeg:
      inputs:
        - path: rtsp://admin:password@192.168.100.104/stream1
          roles:
            - record
            - detect

    detect:
      enabled: true
      width: 1920
      height: 1080
      fps: 5

    objects:
      track:
        - person
        - shopping_cart
        - backpack
      filters:
        person:
          min_area: 4000
          min_score: 0.75
        backpack:
          min_area: 1000
          min_score: 0.70

    zones:
      electronics_section:
        coordinates: 400,300,1520,300,1520,780,400,780
        objects:
          - person

    record:
      enabled: true
      retain:
        days: 30              # Loss prevention retention
        mode: motion

# Go2RTC Configuration (WebRTC streaming)
go2rtc:
  streams:
    front_entrance_live:
      - rtsp://admin:password@192.168.100.101/stream2  # Sub-stream for live view
      - "ffmpeg:front_entrance#audio=opus"

    parking_lpr_live:
      - rtsp://admin:password@192.168.100.102/stream2

    warehouse_floor_live:
      - rtsp://admin:password@192.168.100.103/stream2

    retail_aisle_3_live:
      - rtsp://admin:password@192.168.100.104/stream2

  # WebRTC configuration
  webrtc:
    candidates:
      - 192.168.1.100:8555    # Internal IP
      - stun:8555              # STUN for NAT traversal

# Birdseye (multi-camera view)
birdseye:
  enabled: true
  mode: continuous            # Always show all cameras
  width: 1920
  height: 1080
  quality: 8
  restream: true

# UI Configuration
ui:
  live_mode: webrtc           # Use WebRTC for live view (low latency)
  timezone: America/Toronto
  use_experimental: false

# Logger
logger:
  default: info
  logs:
    frigate.mqtt: info
    frigate.record: info
    frigate.detect: debug     # Verbose detection logging
    frigate.event: info
```

### AI Inference Pipeline

**Detection Flow (30 FPS target on Coral TPU):**

```python
# Simplified pseudo-code of Frigate's detection pipeline

import cv2
import numpy as np
from pycoral.adapters import detect
from pycoral.utils.edgetpu import make_interpreter

class FrigateDetector:
    def __init__(self, model_path, device):
        # Load TensorFlow Lite model to Coral TPU
        self.interpreter = make_interpreter(model_path, device=device)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # Model expects 320x320 RGB input
        self.input_shape = (320, 320)

    def preprocess_frame(self, frame):
        """
        Convert camera frame to model input format
        Input: 1920x1080 BGR (from FFmpeg)
        Output: 320x320 RGB (for YOLO)
        """
        # Resize to 320x320 (GPU-accelerated if available)
        resized = cv2.resize(frame, self.input_shape, interpolation=cv2.INTER_LINEAR)

        # Convert BGR → RGB
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

        # Normalize to [0, 1] (if model requires)
        normalized = rgb.astype(np.float32) / 255.0

        # Add batch dimension: (320, 320, 3) → (1, 320, 320, 3)
        input_tensor = np.expand_dims(normalized, axis=0)

        return input_tensor

    def detect_objects(self, frame):
        """
        Run AI inference on single frame
        Returns: List of detections [(class, confidence, bbox), ...]
        """
        # Preprocess
        input_tensor = self.preprocess_frame(frame)

        # Set input tensor
        self.interpreter.set_tensor(self.input_details[0]['index'], input_tensor)

        # Run inference (this is the GPU/TPU-accelerated step)
        start_time = time.time()
        self.interpreter.invoke()
        inference_time = (time.time() - start_time) * 1000  # ms

        # Get output tensors
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])      # Bounding boxes
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])    # Class IDs
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])     # Confidence
        num_detections = int(self.interpreter.get_tensor(self.output_details[3]['index'])[0])

        detections = []
        for i in range(num_detections):
            score = scores[0][i]
            if score < 0.5:  # Confidence threshold
                continue

            class_id = int(classes[0][i])
            class_name = self.get_class_name(class_id)

            # Bounding box (normalized coordinates)
            ymin, xmin, ymax, xmax = boxes[0][i]

            # Convert to pixel coordinates (original frame size)
            h, w = frame.shape[:2]
            bbox = {
                'xmin': int(xmin * w),
                'ymin': int(ymin * h),
                'xmax': int(xmax * w),
                'ymax': int(ymax * h)
            }

            detections.append({
                'class': class_name,
                'confidence': float(score),
                'bbox': bbox,
                'inference_time_ms': inference_time
            })

        return detections

    def get_class_name(self, class_id):
        """Map class ID to human-readable label"""
        coco_labels = {
            0: 'person',
            2: 'car',
            3: 'motorcycle',
            5: 'bus',
            7: 'truck',
            # ... (80 total COCO classes)
        }
        return coco_labels.get(class_id, 'unknown')

# ========================================
# Object Tracking (DeepSORT Algorithm)
# ========================================

class ObjectTracker:
    def __init__(self):
        self.tracks = {}        # Track ID → Track object
        self.next_id = 1
        self.max_age = 30       # Remove tracks after 30 frames of no match

    def update(self, detections, frame_id):
        """
        Update tracks with new detections
        Returns: List of active tracks with IDs
        """
        # Match detections to existing tracks (Hungarian algorithm)
        matched, unmatched_detections, unmatched_tracks = self.match_detections(detections)

        # Update matched tracks
        for track_id, detection in matched:
            self.tracks[track_id].update(detection, frame_id)

        # Create new tracks for unmatched detections
        for detection in unmatched_detections:
            track_id = self.next_id
            self.next_id += 1
            self.tracks[track_id] = Track(track_id, detection, frame_id)

        # Remove stale tracks (no match for max_age frames)
        for track_id in list(self.tracks.keys()):
            if frame_id - self.tracks[track_id].last_seen > self.max_age:
                del self.tracks[track_id]

        # Return active tracks
        return [track.to_dict() for track in self.tracks.values()]

    def match_detections(self, detections):
        """Use IOU (Intersection over Union) to match detections to tracks"""
        # Simplified: use bounding box overlap to match
        # Full implementation uses Kalman filter prediction + IOU
        matched = []
        unmatched_detections = detections.copy()
        unmatched_tracks = list(self.tracks.keys())

        for detection in detections:
            best_match = None
            best_iou = 0.3  # Minimum IOU threshold

            for track_id in unmatched_tracks:
                iou = self.calculate_iou(detection['bbox'], self.tracks[track_id].bbox)
                if iou > best_iou:
                    best_iou = iou
                    best_match = track_id

            if best_match:
                matched.append((best_match, detection))
                unmatched_detections.remove(detection)
                unmatched_tracks.remove(best_match)

        return matched, unmatched_detections, unmatched_tracks

    def calculate_iou(self, bbox1, bbox2):
        """Calculate Intersection over Union"""
        # Intersection area
        x_left = max(bbox1['xmin'], bbox2['xmin'])
        y_top = max(bbox1['ymin'], bbox2['ymin'])
        x_right = min(bbox1['xmax'], bbox2['xmax'])
        y_bottom = min(bbox1['ymax'], bbox2['ymax'])

        if x_right < x_left or y_bottom < y_top:
            return 0.0

        intersection_area = (x_right - x_left) * (y_bottom - y_top)

        # Union area
        bbox1_area = (bbox1['xmax'] - bbox1['xmin']) * (bbox1['ymax'] - bbox1['ymin'])
        bbox2_area = (bbox2['xmax'] - bbox2['xmin']) * (bbox2['ymax'] - bbox2['ymin'])
        union_area = bbox1_area + bbox2_area - intersection_area

        return intersection_area / union_area if union_area > 0 else 0.0

# ========================================
# Event Manager
# ========================================

class EventManager:
    def __init__(self, mqtt_client, db_connection):
        self.mqtt = mqtt_client
        self.db = db_connection
        self.active_events = {}

    def process_tracks(self, tracks, camera_name, timestamp):
        """
        Convert tracks into events (start/update/end)
        """
        for track in tracks:
            track_id = track['id']
            event_id = f"{camera_name}_{track_id}"

            if event_id not in self.active_events:
                # New event: object entered frame
                self.start_event(event_id, track, camera_name, timestamp)
            else:
                # Update existing event
                self.update_event(event_id, track, timestamp)

        # Check for ended events (tracks no longer active)
        for event_id in list(self.active_events.keys()):
            if event_id not in [f"{camera_name}_{t['id']}" for t in tracks]:
                self.end_event(event_id, timestamp)

    def start_event(self, event_id, track, camera_name, timestamp):
        """Create new event in database and publish MQTT"""
        event = {
            'id': event_id,
            'camera': camera_name,
            'label': track['class'],
            'start_time': timestamp,
            'end_time': None,
            'top_score': track['confidence'],
            'false_positive': False,
            'zones': [],
            'thumbnail': None,
            'has_clip': False,
            'has_snapshot': False
        }

        self.active_events[event_id] = event

        # Insert into database
        self.db.execute("""
            INSERT INTO events (id, camera, label, start_time, top_score)
            VALUES (%s, %s, %s, %s, %s)
        """, (event['id'], event['camera'], event['label'], event['start_time'], event['top_score']))

        # Publish MQTT event
        self.mqtt.publish(f"frigate/events/{camera_name}/new", json.dumps(event))

    def update_event(self, event_id, track, timestamp):
        """Update event with latest track data"""
        event = self.active_events[event_id]

        # Update top score if current confidence is higher
        if track['confidence'] > event['top_score']:
            event['top_score'] = track['confidence']
            self.db.execute("UPDATE events SET top_score = %s WHERE id = %s",
                            (event['top_score'], event_id))

    def end_event(self, event_id, timestamp):
        """Finalize event: generate clip, snapshot, publish end"""
        event = self.active_events[event_id]
        event['end_time'] = timestamp

        # Update database
        self.db.execute("UPDATE events SET end_time = %s WHERE id = %s",
                        (event['end_time'], event_id))

        # Generate video clip (30s before + 10s after)
        self.generate_clip(event)

        # Generate snapshot (best frame)
        self.generate_snapshot(event)

        # Publish MQTT end event
        self.mqtt.publish(f"frigate/events/{event['camera']}/end", json.dumps(event))

        # Remove from active events
        del self.active_events[event_id]
```

### Performance Metrics

**Inference Performance (YOLOv8n, 320x320 input):**

| Hardware | FPS (single camera) | Cameras (30 FPS total) | Latency | Power |
|----------|---------------------|------------------------|---------|-------|
| **Coral TPU (USB)** | 100 FPS | 3-4 cameras | <10ms | 2.5W |
| **Coral TPU (PCIe Dual)** | 200 FPS | 6-8 cameras | <10ms | 5W |
| **NVIDIA RTX 4090** | 600 FPS | 20 cameras | <5ms | 450W |
| **NVIDIA Jetson Orin Nano** | 60 FPS | 2 cameras | <15ms | 15W |
| **Intel i7-12700 (CPU)** | 15 FPS | 0.5 cameras | <70ms | 65W |
| **Raspberry Pi 4 (CPU)** | 2 FPS | 0.06 cameras | <500ms | 7W |

**Recording Performance (H.265, 1080p):**

| Stream Config | Bitrate | Storage/Day | CPU Load | Bandwidth |
|---------------|---------|-------------|----------|-----------|
| **Continuous** | 4 Mbps | 43 GB | 5% (decode only) | 4 Mbps |
| **Motion-based** | 4 Mbps (avg 0.5) | 5 GB | 5% | 0.5 Mbps avg |
| **Event-only** | 4 Mbps (clips) | 1 GB | <1% | <0.1 Mbps |

---

## Component Architecture

### 1. Camera Manager Service

**Purpose**: ONVIF discovery, RTSP stream management, health monitoring

**Technology Stack**:
- python-onvif-zeep (ONVIF protocol)
- FFmpeg (stream decoding)
- go2rtc (modern RTSP proxy)

**Responsibilities**:
```
• Camera Discovery
  - ONVIF WS-Discovery (UDP broadcast)
  - Manual RTSP URL configuration
  - Automatic camera capabilities detection
  - Credential management

• Stream Management
  - RTSP connection pooling
  - Auto-reconnect on failure (exponential backoff)
  - Stream health monitoring (FPS, dropouts)
  - Bandwidth adaptation

• PTZ Control
  - Pan/Tilt/Zoom commands via ONVIF
  - Preset position management
  - Auto-tracking integration
  - Manual override interface
```

**ONVIF Discovery Script**:

```python
from onvif import ONVIFCamera
import socket
import struct

def discover_cameras(timeout=5):
    """
    Discover ONVIF cameras on local network using WS-Discovery
    """
    discovered = []

    # WS-Discovery multicast address
    MCAST_GRP = '239.255.255.250'
    MCAST_PORT = 3702

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(timeout)

    # Bind to multicast group
    sock.bind(('', MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # Send WS-Discovery probe
    probe_message = '''<?xml version="1.0" encoding="UTF-8"?>
    <e:Envelope xmlns:e="http://www.w3.org/2003/05/soap-envelope"
                xmlns:w="http://schemas.xmlsoap.org/ws/2004/08/addressing"
                xmlns:d="http://schemas.xmlsoap.org/ws/2005/04/discovery"
                xmlns:dn="http://www.onvif.org/ver10/network/wsdl">
        <e:Header>
            <w:MessageID>uuid:12345678-1234-1234-1234-123456789012</w:MessageID>
            <w:To>urn:schemas-xmlsoap-org:ws:2005:04:discovery</w:To>
            <w:Action>http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</w:Action>
        </e:Header>
        <e:Body>
            <d:Probe>
                <d:Types>dn:NetworkVideoTransmitter</d:Types>
            </d:Probe>
        </e:Body>
    </e:Envelope>'''

    sock.sendto(probe_message.encode(), (MCAST_GRP, MCAST_PORT))

    # Receive responses
    try:
        while True:
            data, addr = sock.recvfrom(65535)
            # Parse XML response to extract camera details
            # (simplified - full implementation parses XAddrs, scopes, etc.)
            if b'NetworkVideoTransmitter' in data:
                discovered.append({
                    'ip': addr[0],
                    'response': data.decode('utf-8', errors='ignore')
                })
    except socket.timeout:
        pass

    sock.close()
    return discovered

def connect_camera(ip, port, user, password):
    """
    Connect to ONVIF camera and retrieve capabilities
    """
    camera = ONVIFCamera(ip, port, user, password, '/etc/onvif/wsdl/')

    # Get device information
    device_info = camera.devicemgmt.GetDeviceInformation()

    # Get capabilities
    capabilities = camera.devicemgmt.GetCapabilities()

    # Get stream URIs
    media_service = camera.create_media_service()
    profiles = media_service.GetProfiles()

    stream_uris = []
    for profile in profiles:
        stream_uri = media_service.GetStreamUri({
            'StreamSetup': {
                'Stream': 'RTP-Unicast',
                'Transport': {'Protocol': 'RTSP'}
            },
            'ProfileToken': profile.token
        })
        stream_uris.append({
            'profile': profile.Name,
            'resolution': f"{profile.VideoEncoderConfiguration.Resolution.Width}x{profile.VideoEncoderConfiguration.Resolution.Height}",
            'uri': stream_uri.Uri
        })

    return {
        'device_info': {
            'manufacturer': device_info.Manufacturer,
            'model': device_info.Model,
            'firmware': device_info.FirmwareVersion,
            'serial': device_info.SerialNumber
        },
        'capabilities': {
            'ptz': capabilities.PTZ is not None,
            'analytics': capabilities.Analytics is not None,
            'events': capabilities.Events is not None
        },
        'streams': stream_uris
    }

# Usage
if __name__ == '__main__':
    print("Discovering cameras...")
    cameras = discover_cameras(timeout=10)

    for cam in cameras:
        print(f"\nFound camera at {cam['ip']}")

        # Attempt connection (try default credentials)
        try:
            details = connect_camera(cam['ip'], 80, 'admin', 'admin')
            print(f"  Manufacturer: {details['device_info']['manufacturer']}")
            print(f"  Model: {details['device_info']['model']}")
            print(f"  Streams: {len(details['streams'])}")
            for stream in details['streams']:
                print(f"    - {stream['profile']}: {stream['resolution']} - {stream['uri']}")
        except Exception as e:
            print(f"  Connection failed: {e}")
```

### 2. AI Analytics Service

**Purpose**: Advanced AI beyond basic object detection

**Technology Stack**:
- CompreFace (facial recognition)
- OpenALPR (license plate reading)
- DeepFace (face attributes)
- Custom PyTorch models

**Architecture**:

```
┌────────────────────────────────────────────┐
│      AI Analytics Coordinator               │
│                                             │
│  ┌────────────────────────────────────┐    │
│  │  Event Subscriber (MQTT)           │    │
│  │  • frigate/events/+/new            │    │
│  │  • frigate/events/+/update         │    │
│  └────────────────┬───────────────────┘    │
│                   ▼                         │
│  ┌────────────────────────────────────┐    │
│  │  Job Dispatcher                    │    │
│  │  • Route to appropriate analyzer   │    │
│  │  • Load balancing                  │    │
│  │  • Priority queue                  │    │
│  └────────────────┬───────────────────┘    │
│                   ▼                         │
│  ┌─────────────┬──────────────┬─────────┐  │
│  │             │              │         │  │
│  ▼             ▼              ▼         ▼  │
│ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐│
│ │ Face   │ │  LPR   │ │Behavior│ │Custom  ││
│ │ Recog  │ │Service │ │Analysis│ │Model   ││
│ │        │ │        │ │        │ │        ││
│ │Compre- │ │OpenALPR│ │Action  │ │Industry││
│ │ Face   │ │        │ │Recog   │ │Specific││
│ └────────┘ └────────┘ └────────┘ └────────┘│
│     │          │          │          │      │
│     └──────────┴──────────┴──────────┘      │
│                   ▼                          │
│  ┌────────────────────────────────────┐     │
│  │  Result Aggregator                 │     │
│  │  • Confidence scoring              │     │
│  │  • Multi-model fusion              │     │
│  │  • Metadata enrichment             │     │
│  └────────────────┬───────────────────┘     │
│                   ▼                          │
│  ┌────────────────────────────────────┐     │
│  │  Database Writer (PostgreSQL)      │     │
│  │  • analytics_results table         │     │
│  │  • face_recognitions              │     │
│  │  • license_plates                  │     │
│  └────────────────────────────────────┘     │
└─────────────────────────────────────────────┘
```

**Facial Recognition Integration** (CompreFace):

```python
import requests
import cv2
import base64
from typing import List, Dict

class FaceRecognitionService:
    def __init__(self, compreface_url, api_key):
        self.base_url = compreface_url
        self.api_key = api_key
        self.recognition_url = f"{self.base_url}/api/v1/recognition"

    def add_face(self, person_name: str, image_path: str) -> Dict:
        """
        Add a face to the recognition database
        """
        with open(image_path, 'rb') as image_file:
            files = {'file': image_file}
            headers = {'x-api-key': self.api_key}
            params = {'subject': person_name}

            response = requests.post(
                f"{self.recognition_url}/faces",
                headers=headers,
                params=params,
                files=files
            )

            return response.json()

    def recognize_face(self, image: np.ndarray, confidence_threshold: float = 0.85) -> List[Dict]:
        """
        Recognize faces in an image
        Returns: List of recognized faces with identities
        """
        # Encode image to JPEG
        _, buffer = cv2.imencode('.jpg', image)
        image_bytes = buffer.tobytes()

        # Send to CompreFace
        files = {'file': ('image.jpg', image_bytes, 'image/jpeg')}
        headers = {'x-api-key': self.api_key}
        params = {
            'limit': 1,  # Return top match
            'det_prob_threshold': 0.8,  # Detection confidence
            'prediction_count': 1
        }

        response = requests.post(
            f"{self.recognition_url}/recognize",
            headers=headers,
            params=params,
            files=files
        )

        result = response.json()

        # Parse results
        recognized_faces = []
        for face in result.get('result', []):
            if not face.get('subjects'):
                # Unknown face
                recognized_faces.append({
                    'identity': 'Unknown',
                    'confidence': 0.0,
                    'bbox': face['box'],
                    'age': face.get('age'),
                    'gender': face.get('gender'),
                    'mask': face.get('mask')
                })
            else:
                # Known face
                subject = face['subjects'][0]
                if subject['similarity'] >= confidence_threshold:
                    recognized_faces.append({
                        'identity': subject['subject'],
                        'confidence': subject['similarity'],
                        'bbox': face['box'],
                        'age': face.get('age'),
                        'gender': face.get('gender'),
                        'mask': face.get('mask')
                    })

        return recognized_faces

    def detect_faces(self, image: np.ndarray) -> List[Dict]:
        """
        Detect faces without recognition (for privacy mode)
        """
        _, buffer = cv2.imencode('.jpg', image)
        image_bytes = buffer.tobytes()

        files = {'file': ('image.jpg', image_bytes, 'image/jpeg')}
        headers = {'x-api-key': self.api_key}

        response = requests.post(
            f"{self.base_url}/api/v1/detection/detect",
            headers=headers,
            files=files
        )

        result = response.json()

        faces = []
        for face in result.get('result', []):
            faces.append({
                'bbox': face['box'],
                'confidence': face['probability'],
                'landmarks': face.get('landmarks')
            })

        return faces

# ========================================
# License Plate Recognition (OpenALPR)
# ========================================

import subprocess
import json

class LicensePlateRecognition:
    def __init__(self, alpr_binary='/usr/bin/alpr', region='us'):
        self.alpr_binary = alpr_binary
        self.region = region

    def recognize_plate(self, image_path: str, top_n: int = 3) -> List[Dict]:
        """
        Recognize license plates in image
        Returns: List of plate readings with confidence
        """
        # Run OpenALPR command-line
        cmd = [
            self.alpr_binary,
            '-c', self.region,  # Country/region (us, eu, etc.)
            '-n', str(top_n),   # Top N results
            '-j',               # JSON output
            image_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return []

        # Parse JSON output
        alpr_result = json.loads(result.stdout)

        plates = []
        for plate_result in alpr_result.get('results', []):
            # Top candidate
            candidate = plate_result['candidates'][0]

            plates.append({
                'plate': candidate['plate'],
                'confidence': candidate['confidence'],
                'region': plate_result.get('region'),
                'bbox': {
                    'x': plate_result['coordinates'][0]['x'],
                    'y': plate_result['coordinates'][0]['y'],
                    'width': plate_result['coordinates'][1]['x'] - plate_result['coordinates'][0]['x'],
                    'height': plate_result['coordinates'][2]['y'] - plate_result['coordinates'][0]['y']
                },
                'processing_time_ms': plate_result['processing_time_ms']
            })

        return plates

    def check_hot_list(self, plate: str, hot_list_db) -> Dict:
        """
        Check if plate is on hot-list (stolen vehicles, wanted persons, etc.)
        """
        # Query database (PostgreSQL example)
        query = """
            SELECT plate, reason, severity, last_updated
            FROM hot_list
            WHERE plate = %s AND active = true
        """

        result = hot_list_db.execute(query, (plate,))
        match = result.fetchone()

        if match:
            return {
                'match': True,
                'plate': match['plate'],
                'reason': match['reason'],
                'severity': match['severity'],  # e.g., 'critical', 'warning'
                'action': 'alert_security'
            }
        else:
            return {'match': False}

# ========================================
# Analytics Event Processor
# ========================================

class AnalyticsProcessor:
    def __init__(self, mqtt_client, db_connection):
        self.mqtt = mqtt_client
        self.db = db_connection

        # Initialize AI services
        self.face_service = FaceRecognitionService(
            compreface_url='http://compreface:8000',
            api_key='your-api-key'
        )

        self.lpr_service = LicensePlateRecognition(region='us')

        # Subscribe to Frigate events
        self.mqtt.subscribe('frigate/events/+/new')
        self.mqtt.on_message = self.handle_event

    def handle_event(self, client, userdata, message):
        """
        Process new Frigate event with additional AI analytics
        """
        event = json.loads(message.payload)

        camera = event['camera']
        label = event['label']
        snapshot_path = event.get('snapshot_path')

        # Route to appropriate analyzer
        if label == 'person' and snapshot_path:
            # Run facial recognition
            image = cv2.imread(snapshot_path)
            faces = self.face_service.recognize_face(image, confidence_threshold=0.85)

            if faces:
                # Store face recognition results
                for face in faces:
                    self.db.execute("""
                        INSERT INTO face_recognitions
                        (event_id, identity, confidence, bbox, age, gender, timestamp)
                        VALUES (%s, %s, %s, %s, %s, %s, NOW())
                    """, (
                        event['id'],
                        face['identity'],
                        face['confidence'],
                        json.dumps(face['bbox']),
                        face.get('age'),
                        face.get('gender')
                    ))

                    # Publish MQTT alert if recognized
                    if face['identity'] != 'Unknown':
                        alert = {
                            'event_id': event['id'],
                            'camera': camera,
                            'person': face['identity'],
                            'confidence': face['confidence'],
                            'timestamp': event['start_time']
                        }
                        self.mqtt.publish(f"sentinel/alerts/{camera}/person_recognized",
                                          json.dumps(alert))

        elif label in ['car', 'truck', 'motorcycle'] and snapshot_path:
            # Run license plate recognition
            plates = self.lpr_service.recognize_plate(snapshot_path)

            for plate_data in plates:
                # Check hot-list
                hot_list_match = self.lpr_service.check_hot_list(
                    plate_data['plate'],
                    self.db
                )

                # Store LPR result
                self.db.execute("""
                    INSERT INTO license_plates
                    (event_id, plate, confidence, region, bbox, hot_list_match, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW())
                """, (
                    event['id'],
                    plate_data['plate'],
                    plate_data['confidence'],
                    plate_data['region'],
                    json.dumps(plate_data['bbox']),
                    hot_list_match['match']
                ))

                # Publish alert if hot-list match
                if hot_list_match['match']:
                    alert = {
                        'event_id': event['id'],
                        'camera': camera,
                        'plate': plate_data['plate'],
                        'reason': hot_list_match['reason'],
                        'severity': hot_list_match['severity'],
                        'timestamp': event['start_time']
                    }
                    self.mqtt.publish(f"sentinel/alerts/{camera}/hot_list_match",
                                      json.dumps(alert))
```

### 3. Storage Manager Service

**Purpose**: Video tiering, retention, backup

**Technology Stack**:
- MinIO (S3-compatible object storage)
- PostgreSQL (metadata)
- Rclone (cloud backup)

**Storage Tiers**:

```
Tier 1 (Hot - NVMe SSD):
  - Age: 0-7 days
  - Quality: Original (H.265)
  - Access: Instant (<100ms)
  - Cost: $0.15/GB/month
  - Use: Live playback, recent events

Tier 2 (Warm - HDD):
  - Age: 7-30 days
  - Quality: Original or slightly compressed
  - Access: Fast (<500ms)
  - Cost: $0.03/GB/month
  - Use: Investigations, compliance

Tier 3 (Cold - Object Storage):
  - Age: 30-365 days
  - Quality: Compressed (reduced bitrate)
  - Access: Moderate (2-5 seconds)
  - Cost: $0.01/GB/month
  - Use: Long-term retention, legal

Tier 4 (Archive - Glacier/Tape):
  - Age: 365+ days
  - Quality: Event clips only (not continuous)
  - Access: Slow (minutes to hours)
  - Cost: $0.004/GB/month
  - Use: Compliance, historical
```

**Tiering Automation** (Python cron job):

```python
import os
import datetime
from minio import Minio
from minio.commonconfig import GOVERNANCE
import psycopg2

class StorageTieringService:
    def __init__(self, minio_client, postgres_conn):
        self.minio = minio_client
        self.db = postgres_conn

        # Storage buckets by tier
        self.buckets = {
            'hot': 'frigate-hot',
            'warm': 'frigate-warm',
            'cold': 'frigate-cold',
            'archive': 'frigate-archive'
        }

    def tier_hot_to_warm(self):
        """
        Move videos from hot (SSD) to warm (HDD) storage after 7 days
        """
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=7)

        # Query videos older than 7 days in hot tier
        query = """
            SELECT id, object_key, camera, start_time, end_time, size_bytes
            FROM recordings
            WHERE tier = 'hot' AND start_time < %s
        """

        cursor = self.db.cursor()
        cursor.execute(query, (cutoff_date,))

        for row in cursor.fetchall():
            video_id, object_key, camera, start_time, end_time, size_bytes = row

            try:
                # Copy from hot bucket to warm bucket
                self.minio.copy_object(
                    bucket_name=self.buckets['warm'],
                    object_name=object_key,
                    source=f"{self.buckets['hot']}/{object_key}"
                )

                # Delete from hot bucket
                self.minio.remove_object(
                    bucket_name=self.buckets['hot'],
                    object_name=object_key
                )

                # Update database
                cursor.execute("""
                    UPDATE recordings
                    SET tier = 'warm', tier_changed_at = NOW()
                    WHERE id = %s
                """, (video_id,))

                self.db.commit()

                print(f"Tiered {object_key} from hot to warm")

            except Exception as e:
                print(f"Error tiering {object_key}: {e}")
                self.db.rollback()

    def tier_warm_to_cold(self):
        """
        Move videos from warm (HDD) to cold (object storage) after 30 days
        Optional: transcode to lower bitrate to save space
        """
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=30)

        query = """
            SELECT id, object_key, camera, start_time, size_bytes
            FROM recordings
            WHERE tier = 'warm' AND start_time < %s
        """

        cursor = self.db.cursor()
        cursor.execute(query, (cutoff_date,))

        for row in cursor.fetchall():
            video_id, object_key, camera, start_time, size_bytes = row

            try:
                # Download from warm tier
                temp_path = f"/tmp/{object_key}"
                self.minio.fget_object(
                    bucket_name=self.buckets['warm'],
                    object_name=object_key,
                    file_path=temp_path
                )

                # Transcode to lower bitrate (optional)
                compressed_path = f"/tmp/{object_key}.compressed.mp4"
                self.transcode_video(temp_path, compressed_path, target_bitrate='1M')

                # Upload to cold tier
                self.minio.fput_object(
                    bucket_name=self.buckets['cold'],
                    object_name=object_key,
                    file_path=compressed_path
                )

                # Get new file size
                stat = os.stat(compressed_path)
                new_size = stat.st_size

                # Delete from warm tier
                self.minio.remove_object(
                    bucket_name=self.buckets['warm'],
                    object_name=object_key
                )

                # Update database
                cursor.execute("""
                    UPDATE recordings
                    SET tier = 'cold', tier_changed_at = NOW(), size_bytes = %s
                    WHERE id = %s
                """, (new_size, video_id))

                self.db.commit()

                # Clean up temp files
                os.remove(temp_path)
                os.remove(compressed_path)

                savings = ((size_bytes - new_size) / size_bytes) * 100
                print(f"Tiered {object_key} to cold, saved {savings:.1f}%")

            except Exception as e:
                print(f"Error tiering {object_key}: {e}")
                self.db.rollback()

    def tier_cold_to_archive(self):
        """
        Move event clips only to archive tier after 1 year
        Delete continuous recordings (keep events only for compliance)
        """
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=365)

        query = """
            SELECT id, object_key, camera, start_time, has_event
            FROM recordings
            WHERE tier = 'cold' AND start_time < %s
        """

        cursor = self.db.cursor()
        cursor.execute(query, (cutoff_date,))

        for row in cursor.fetchall():
            video_id, object_key, camera, start_time, has_event = row

            if has_event:
                # Archive event clips (important for compliance)
                try:
                    self.minio.copy_object(
                        bucket_name=self.buckets['archive'],
                        object_name=object_key,
                        source=f"{self.buckets['cold']}/{object_key}"
                    )

                    self.minio.remove_object(
                        bucket_name=self.buckets['cold'],
                        object_name=object_key
                    )

                    cursor.execute("""
                        UPDATE recordings
                        SET tier = 'archive', tier_changed_at = NOW()
                        WHERE id = %s
                    """, (video_id,))

                    self.db.commit()
                    print(f"Archived event clip: {object_key}")

                except Exception as e:
                    print(f"Error archiving {object_key}: {e}")
                    self.db.rollback()
            else:
                # Delete continuous recordings (no events, past retention)
                try:
                    self.minio.remove_object(
                        bucket_name=self.buckets['cold'],
                        object_name=object_key
                    )

                    cursor.execute("""
                        DELETE FROM recordings WHERE id = %s
                    """, (video_id,))

                    self.db.commit()
                    print(f"Deleted old continuous recording: {object_key}")

                except Exception as e:
                    print(f"Error deleting {object_key}: {e}")
                    self.db.rollback()

    def transcode_video(self, input_path, output_path, target_bitrate='1M'):
        """
        Transcode video to lower bitrate using FFmpeg
        """
        import subprocess

        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-c:v', 'libx265',      # H.265 codec
            '-preset', 'medium',     # Encoding speed
            '-b:v', target_bitrate,  # Target bitrate
            '-c:a', 'aac',           # Audio codec
            '-b:a', '128k',          # Audio bitrate
            '-y',                    # Overwrite output
            output_path
        ]

        subprocess.run(cmd, check=True, capture_output=True)

    def run_tiering_cycle(self):
        """
        Run all tiering operations (called by cron job)
        """
        print(f"Starting tiering cycle: {datetime.datetime.now()}")

        print("Phase 1: Hot → Warm")
        self.tier_hot_to_warm()

        print("Phase 2: Warm → Cold")
        self.tier_warm_to_cold()

        print("Phase 3: Cold → Archive")
        self.tier_cold_to_archive()

        print("Tiering cycle complete")

# ========================================
# Usage (cron job runs hourly)
# ========================================

if __name__ == '__main__':
    # Initialize MinIO client
    minio_client = Minio(
        endpoint='minio:9000',
        access_key='minioadmin',
        secret_key='minioadmin',
        secure=False
    )

    # Initialize PostgreSQL connection
    postgres_conn = psycopg2.connect(
        host='postgres',
        database='frigate_db',
        user='frigate',
        password='password'
    )

    # Run tiering
    tiering_service = StorageTieringService(minio_client, postgres_conn)
    tiering_service.run_tiering_cycle()
```

---

## AI/ML Architecture

### Model Training Pipeline

**Custom Model Training Workflow** (for industry-specific use cases):

```
1. Data Collection
   ├─> Existing footage (Frigate recordings)
   ├─> Public datasets (COCO, Open Images, custom)
   └─> Synthetic data generation (for rare events)

2. Annotation
   ├─> CVAT (Computer Vision Annotation Tool)
   ├─> Roboflow (cloud-based labeling)
   └─> Label Studio (self-hosted)

3. Data Preparation
   ├─> Train/validation/test split (70%/20%/10%)
   ├─> Augmentation (rotation, brightness, blur)
   ├─> Format conversion (COCO → YOLOv8)
   └─> Class balancing

4. Model Training
   ├─> Base model: YOLOv8n (pretrained on COCO)
   ├─> Transfer learning (freeze backbone, train head)
   ├─> Hyperparameter tuning (learning rate, batch size)
   └─> Early stopping (monitor validation loss)

5. Model Optimization
   ├─> Quantization (FP32 → INT8 for TPU)
   ├─> Pruning (remove low-importance weights)
   ├─> Export to TFLite / ONNX
   └─> Benchmark on target hardware

6. Deployment
   ├─> Upload to model repository (MinIO)
   ├─> Update Frigate config (model path)
   ├─> A/B testing (compare with baseline)
   └─> Gradual rollout
```

**Training Script** (PyTorch + YOLOv8):

```python
from ultralytics import YOLO
import torch

def train_custom_model(dataset_path, output_dir, epochs=100):
    """
    Train custom YOLOv8 model on labeled dataset
    """
    # Load pretrained YOLOv8 nano model
    model = YOLO('yolov8n.pt')

    # Configure training
    results = model.train(
        data=f'{dataset_path}/data.yaml',  # Dataset config
        epochs=epochs,
        imgsz=640,                          # Input image size
        batch=16,                           # Batch size (adjust for GPU memory)
        device=0,                           # GPU index (0 = first GPU)
        workers=8,                          # Data loader threads
        project=output_dir,
        name='custom_model',
        exist_ok=True,

        # Hyperparameters
        optimizer='AdamW',
        lr0=0.001,                          # Initial learning rate
        lrf=0.01,                           # Final learning rate (lr0 * lrf)
        momentum=0.937,
        weight_decay=0.0005,
        warmup_epochs=3.0,
        warmup_momentum=0.8,

        # Augmentation
        hsv_h=0.015,                        # Hue augmentation
        hsv_s=0.7,                          # Saturation
        hsv_v=0.4,                          # Value (brightness)
        degrees=0.0,                        # Rotation degrees
        translate=0.1,                      # Translation
        scale=0.5,                          # Scaling
        shear=0.0,                          # Shear
        perspective=0.0,                    # Perspective
        flipud=0.0,                         # Flip up-down
        fliplr=0.5,                         # Flip left-right
        mosaic=1.0,                         # Mosaic augmentation
        mixup=0.0,                          # MixUp augmentation

        # Early stopping
        patience=50,                        # Epochs to wait for improvement

        # Validation
        val=True,
        plots=True,                         # Generate plots
        save=True,
        save_period=10,                     # Save checkpoint every N epochs

        # Logging
        verbose=True
    )

    # Evaluate on test set
    metrics = model.val()

    print(f"Training complete!")
    print(f"  mAP50: {metrics.box.map50:.3f}")
    print(f"  mAP50-95: {metrics.box.map:.3f}")
    print(f"  Precision: {metrics.box.mp:.3f}")
    print(f"  Recall: {metrics.box.mr:.3f}")

    # Export to TFLite for Coral TPU
    model.export(format='edgetpu', imgsz=320)

    return results

# ========================================
# Example: Train PPE Detection Model
# ========================================

if __name__ == '__main__':
    # Dataset structure:
    # ppe_dataset/
    #   ├─ data.yaml
    #   ├─ train/
    #   │   ├─ images/
    #   │   └─ labels/
    #   ├─ val/
    #   └─ test/

    train_custom_model(
        dataset_path='/data/ppe_dataset',
        output_dir='/models/ppe_detection',
        epochs=100
    )
```

**Dataset Configuration** (`data.yaml`):

```yaml
# PPE Detection Dataset

path: /data/ppe_dataset
train: train/images
val: val/images
test: test/images

names:
  0: person
  1: hard_hat
  2: safety_vest
  3: safety_glasses
  4: gloves
  5: face_mask
  6: no_hard_hat
  7: no_safety_vest

nc: 8  # Number of classes
```

---

## Data Architecture

### PostgreSQL Schema Design

**Core Tables:**

```sql
-- Events table (time-series optimized with TimescaleDB)
CREATE TABLE events (
    id VARCHAR(50) PRIMARY KEY,
    camera VARCHAR(50) NOT NULL,
    label VARCHAR(50) NOT NULL,
    sub_label VARCHAR(50),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    top_score REAL NOT NULL,
    false_positive BOOLEAN DEFAULT FALSE,
    zones TEXT[],
    thumbnail VARCHAR(255),
    has_clip BOOLEAN DEFAULT FALSE,
    has_snapshot BOOLEAN DEFAULT FALSE,
    region_id VARCHAR(50),
    data JSONB
);

-- Convert to hypertable (TimescaleDB)
SELECT create_hypertable('events', 'start_time');

-- Create indexes
CREATE INDEX idx_events_camera_time ON events (camera, start_time DESC);
CREATE INDEX idx_events_label ON events (label);
CREATE INDEX idx_events_zones ON events USING GIN (zones);

-- Tracked objects (detections within events)
CREATE TABLE tracked_objects (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(50) REFERENCES events(id) ON DELETE CASCADE,
    timestamp TIMESTAMP NOT NULL,
    position JSONB NOT NULL,  -- {x, y, width, height}
    score REAL NOT NULL,
    attributes JSONB  -- Additional metadata
);

CREATE INDEX idx_tracked_objects_event ON tracked_objects (event_id);
CREATE INDEX idx_tracked_objects_time ON tracked_objects (timestamp DESC);

-- Face recognitions
CREATE TABLE face_recognitions (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(50) REFERENCES events(id),
    identity VARCHAR(100) NOT NULL,
    confidence REAL NOT NULL,
    bbox JSONB NOT NULL,
    age INT,
    gender VARCHAR(10),
    timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_face_identity ON face_recognitions (identity, timestamp DESC);
CREATE INDEX idx_face_event ON face_recognitions (event_id);

-- License plates
CREATE TABLE license_plates (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(50) REFERENCES events(id),
    plate VARCHAR(20) NOT NULL,
    confidence REAL NOT NULL,
    region VARCHAR(10),
    bbox JSONB NOT NULL,
    hot_list_match BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_lpr_plate ON license_plates (plate, timestamp DESC);
CREATE INDEX idx_lpr_hot_list ON license_plates (hot_list_match, timestamp DESC) WHERE hot_list_match = TRUE;

-- Hot list (stolen vehicles, wanted persons, banned visitors)
CREATE TABLE hot_list (
    id SERIAL PRIMARY KEY,
    list_type VARCHAR(20) NOT NULL,  -- 'vehicle', 'person', 'other'
    identifier VARCHAR(100) NOT NULL,  -- Plate number, name, etc.
    reason TEXT NOT NULL,
    severity VARCHAR(20) NOT NULL,  -- 'critical', 'warning', 'info'
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMP,
    metadata JSONB
);

CREATE INDEX idx_hot_list_identifier ON hot_list (identifier, active) WHERE active = TRUE;

-- Recordings metadata
CREATE TABLE recordings (
    id SERIAL PRIMARY KEY,
    camera VARCHAR(50) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    duration_seconds INT NOT NULL,
    object_key VARCHAR(255) NOT NULL,  -- MinIO object path
    size_bytes BIGINT NOT NULL,
    tier VARCHAR(20) NOT NULL DEFAULT 'hot',  -- hot, warm, cold, archive
    tier_changed_at TIMESTAMP,
    has_event BOOLEAN DEFAULT FALSE,
    segment_size INT DEFAULT 10  -- seconds per segment
);

CREATE INDEX idx_recordings_camera_time ON recordings (camera, start_time DESC);
CREATE INDEX idx_recordings_tier ON recordings (tier, start_time);

-- Cameras configuration
CREATE TABLE cameras (
    name VARCHAR(50) PRIMARY KEY,
    enabled BOOLEAN DEFAULT TRUE,
    rtsp_url TEXT NOT NULL,
    resolution_width INT NOT NULL,
    resolution_height INT NOT NULL,
    fps INT NOT NULL,
    detect_enabled BOOLEAN DEFAULT TRUE,
    record_enabled BOOLEAN DEFAULT TRUE,
    zones JSONB,
    objects_to_track TEXT[],
    motion_mask JSONB,
    onvif_host VARCHAR(255),
    onvif_port INT,
    ptz_capable BOOLEAN DEFAULT FALSE,
    config JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- System statistics (TimescaleDB)
CREATE TABLE system_stats (
    timestamp TIMESTAMP NOT NULL,
    camera VARCHAR(50) NOT NULL,
    fps REAL,
    detection_fps REAL,
    process_fps REAL,
    skipped_fps REAL,
    cpu_percent REAL,
    gpu_percent REAL,
    memory_percent REAL,
    temperature_celsius REAL
);

SELECT create_hypertable('system_stats', 'timestamp');
CREATE INDEX idx_system_stats_camera ON system_stats (camera, timestamp DESC);

-- Alerts configuration
CREATE TABLE alert_rules (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    camera_filter TEXT[],  -- Apply to these cameras (empty = all)
    label_filter TEXT[],   -- Trigger on these object types
    zone_filter TEXT[],    -- Trigger in these zones
    time_filter JSONB,     -- {start_hour, end_hour, days_of_week}
    confidence_threshold REAL DEFAULT 0.8,
    cooldown_seconds INT DEFAULT 60,  -- Don't repeat alert for X seconds
    actions JSONB NOT NULL,  -- {email: [...], sms: [...], webhook: ...}
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Alert history
CREATE TABLE alert_history (
    id SERIAL PRIMARY KEY,
    rule_id INT REFERENCES alert_rules(id),
    event_id VARCHAR(50) REFERENCES events(id),
    camera VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    actions_taken JSONB,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_alert_history_time ON alert_history (timestamp DESC);
CREATE INDEX idx_alert_history_rule ON alert_history (rule_id, timestamp DESC);

-- Retention policies (TimescaleDB)
SELECT add_retention_policy('events', INTERVAL '90 days');
SELECT add_retention_policy('system_stats', INTERVAL '30 days');
SELECT add_retention_policy('tracked_objects', INTERVAL '90 days');
```

### Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    Camera → Frigate                          │
│  RTSP Stream (H.265, 4 Mbps) ──────────────────────────────┐│
│                                                              ││
│  Frame Extraction (5 FPS for detection) ─────────────────┐  ││
│                                                           │  ││
│  AI Inference (Coral TPU) ──────────────────────────────┐│  ││
│                                                          ││  ││
│  Object Tracking (DeepSORT) ────────────────────────────┼┘  ││
│                                                          │   ││
│  Event Detection ────────────────────────────────────────┘   ││
│                                                              ││
└──────────────────────────────────────────────────────────────┘│
                                 │                              │
                    ┌────────────┼────────────┐                 │
                    │            │            │                 │
                    ▼            ▼            ▼                 │
          ┌──────────────┐ ┌──────────┐ ┌──────────┐          │
          │ PostgreSQL   │ │  MinIO   │ │   MQTT   │          │
          │              │ │          │ │          │          │
          │ • Event      │ │ • Video  │ │ • Real-  │          │
          │   metadata   │ │   clips  │ │   time   │          │
          │ • Detections │ │ • Snap-  │ │   events │          │
          │ • Face data  │ │   shots  │ │ • Alerts │          │
          │ • LPR data   │ │          │ │          │          │
          └──────────────┘ └──────────┘ └──────────┘          │
                                 │                              │
                                 ▼                              │
                    ┌─────────────────────────┐                │
                    │  Analytics Services     │                │
                    │  • Face Recognition     │                │
                    │  • LPR Processing       │                │
                    │  • Behavior Analysis    │                │
                    └─────────────────────────┘                │
                                 │                              │
                                 ▼                              │
                    ┌─────────────────────────┐                │
                    │  Storage Tiering Cron   │                │
                    │  Hot → Warm → Cold →    │                │
                    │  Archive (lifecycle)    │                │
                    └─────────────────────────┘                │
                                                                │
                    ┌─────────────────────────┐                │
                    │  Alerting Service       │◄───────────────┘
                    │  • Email (SMTP)         │
                    │  • SMS (Twilio)         │
                    │  • Push (FCM)           │
                    │  • Webhook (HTTP POST)  │
                    └─────────────────────────┘
```

---

## Video Processing Pipeline

### FFmpeg Processing Chain

**Frigate's video processing uses FFmpeg for decoding and go2rtc for streaming:**

```
┌────────────────────────────────────────────────────┐
│         IP Camera (RTSP Stream)                     │
│  rtsp://camera_ip/stream1                          │
│  Codec: H.265, Resolution: 1920x1080, FPS: 15     │
└────────────────────┬───────────────────────────────┘
                     │
                     ▼
┌────────────────────────────────────────────────────┐
│         go2rtc (RTSP Proxy & Transcoder)           │
│  • Maintains persistent RTSP connection            │
│  • Buffers video for rewind/replay                │
│  • Provides multiple output formats:              │
│    - RTSP (for Frigate)                           │
│    - WebRTC (for browsers, low latency)           │
│    - HLS (for mobile apps)                        │
│    - RTMP (for streaming services)                │
└────────────────────┬───────────────────────────────┘
                     │
       ┌─────────────┴─────────────┐
       │                           │
       ▼                           ▼
┌─────────────────┐     ┌─────────────────────┐
│ Detection Path  │     │  Recording Path     │
│ (Low FPS)       │     │  (Full FPS)         │
└─────────────────┘     └─────────────────────┘
       │                           │
       ▼                           ▼
┌─────────────────┐     ┌─────────────────────┐
│ FFmpeg Decode   │     │ FFmpeg Passthrough  │
│ • Decode H.265  │     │ • Copy codec (no    │
│ • Scale to      │     │   re-encode)        │
│   320x320       │     │ • Segment into      │
│ • Convert to    │     │   10-second chunks  │
│   RGB           │     │ • Write to MinIO    │
│ • Output: 5 FPS │     │ • Continuous or     │
│                 │     │   motion-based      │
└────────┬────────┘     └──────────┬──────────┘
         │                         │
         ▼                         │
┌─────────────────┐                │
│ AI Detector     │                │
│ (Coral TPU)     │                │
│ • YOLO Inference│                │
│ • 30ms latency  │                │
│ • Bounding boxes│                │
└────────┬────────┘                │
         │                         │
         ▼                         │
┌─────────────────┐                │
│ Object Tracker  │                │
│ (DeepSORT)      │                │
│ • Track IDs     │                │
│ • Motion vectors│                │
└────────┬────────┘                │
         │                         │
         ▼                         │
┌─────────────────┐                │
│ Event Manager   │◄───────────────┘
│ • Detect start/ │  (Links events
│   end of events │   to recordings)
│ • Generate clips│
│ • Save snapshots│
└─────────────────┘
```

**FFmpeg Command Examples** (used internally by Frigate):

```bash
# Detection stream (low FPS, scaled down)
ffmpeg -hide_banner -loglevel warning \
  -hwaccel auto \
  -rtsp_transport tcp \
  -i rtsp://admin:password@192.168.100.101/stream1 \
  -f rawvideo \
  -pix_fmt rgb24 \
  -s 320x320 \
  -r 5 \
  pipe:

# Recording stream (passthrough, no re-encode)
ffmpeg -hide_banner -loglevel warning \
  -hwaccel auto \
  -rtsp_transport tcp \
  -i rtsp://admin:password@192.168.100.101/stream1 \
  -c:v copy \
  -c:a aac \
  -f segment \
  -segment_time 10 \
  -segment_format mp4 \
  -reset_timestamps 1 \
  -strftime 1 \
  /media/frigate/recordings/%Y-%m-%d/%H/%Y%m%d_%H%M%S.mp4

# Clip generation (extract event with pre/post buffer)
ffmpeg -hide_banner -loglevel warning \
  -ss 00:00:00 \
  -i /media/frigate/recordings/2024-12-08/14/20241208_143000.mp4 \
  -t 00:00:40 \
  -c:v copy \
  -c:a copy \
  /media/frigate/clips/front_entrance-20241208_143015.mp4
```

---

## Security Architecture

### Defense-in-Depth Strategy

**Layer 1: Network Segmentation**

```
┌────────────────────────────────────────────────────────────┐
│              Internet (Untrusted)                           │
└───────────────────────┬────────────────────────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │  Firewall / NGF  │
              │  • WAN → DMZ only│
              │  • Block all else│
              └─────────┬────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────┐
│                DMZ (Semi-Trusted)                          │
│  ┌──────────────┐  ┌──────────────┐                      │
│  │ Reverse Proxy│  │  VPN Gateway │                      │
│  │  (NGINX)     │  │  (WireGuard) │                      │
│  └──────┬───────┘  └──────┬───────┘                      │
└─────────┼──────────────────┼──────────────────────────────┘
          │                  │
          │      ┌───────────┴────────────┐
          │      │                        │
          ▼      ▼                        ▼
┌──────────────────────┐      ┌────────────────────────┐
│  Management VLAN     │      │  Camera VLAN (Isolated)│
│  (10.0.1.0/24)       │      │  (192.168.100.0/24)    │
│                      │      │                        │
│  • Frigate Server    │      │  • IP Cameras only     │
│  • PostgreSQL        │      │  • No internet access  │
│  • MinIO             │      │  • One-way to Mgmt     │
│  • User Workstations │      │                        │
└──────────────────────┘      └────────────────────────┘
```

**Firewall Rules** (iptables):

```bash
#!/bin/bash
# OS-SENTINEL Firewall Configuration

# Flush existing rules
iptables -F
iptables -X
iptables -t nat -F

# Default policies: DENY all
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

# Management VLAN (10.0.1.0/24)
# ========================================

# Allow SSH from internal only
iptables -A INPUT -p tcp -s 10.0.1.0/24 --dport 22 -j ACCEPT

# Allow HTTPS for Frigate web UI (from internal only)
iptables -A INPUT -p tcp -s 10.0.1.0/24 --dport 5000 -j ACCEPT

# Allow PostgreSQL (from Frigate only)
iptables -A INPUT -p tcp -s 10.0.1.10 --dport 5432 -j ACCEPT

# Allow MinIO API (from Frigate only)
iptables -A INPUT -p tcp -s 10.0.1.10 --dport 9000 -j ACCEPT

# Allow MQTT (from internal services)
iptables -A INPUT -p tcp -s 10.0.1.0/24 --dport 1883 -j ACCEPT

# Camera VLAN (192.168.100.0/24)
# ========================================

# Allow RTSP from cameras (one-way: cameras → Frigate)
iptables -A FORWARD -s 192.168.100.0/24 -d 10.0.1.10 -p tcp --dport 554 -j ACCEPT
iptables -A FORWARD -s 192.168.100.0/24 -d 10.0.1.10 -p tcp --dport 8554 -j ACCEPT

# Allow ONVIF from Frigate to cameras (discovery, PTZ control)
iptables -A FORWARD -s 10.0.1.10 -d 192.168.100.0/24 -p tcp --dport 80 -j ACCEPT
iptables -A FORWARD -s 10.0.1.10 -d 192.168.100.0/24 -p tcp --dport 8000 -j ACCEPT

# DENY cameras from accessing internet (prevent botnet, data exfiltration)
iptables -A FORWARD -s 192.168.100.0/24 -d 0.0.0.0/0 -j DROP

# DENY cameras from accessing management VLAN (except Frigate)
iptables -A FORWARD -s 192.168.100.0/24 -d 10.0.1.0/24 -j DROP

# DMZ Rules (Reverse Proxy)
# ========================================

# Allow HTTPS from internet to reverse proxy
iptables -A FORWARD -d <DMZ_IP> -p tcp --dport 443 -j ACCEPT

# Reverse proxy can forward to Frigate (with restrictions)
iptables -A FORWARD -s <DMZ_IP> -d 10.0.1.10 -p tcp --dport 5000 -j ACCEPT

# Rate Limiting (DDoS protection)
# ========================================

# Limit SSH connections (max 3 per minute per IP)
iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --set
iptables -A INPUT -p tcp --dport 22 -m state --state NEW -m recent --update --seconds 60 --hitcount 4 -j DROP

# Limit HTTPS connections (max 100 per minute per IP)
iptables -A INPUT -p tcp --dport 443 -m state --state NEW -m recent --set
iptables -A INPUT -p tcp --dport 443 -m state --state NEW -m recent --update --seconds 60 --hitcount 100 -j DROP

# Logging (dropped packets)
iptables -A INPUT -m limit --limit 5/min -j LOG --log-prefix "iptables-INPUT-DROP: "
iptables -A FORWARD -m limit --limit 5/min -j LOG --log-prefix "iptables-FORWARD-DROP: "

# Save rules
iptables-save > /etc/iptables/rules.v4
```

**Layer 2: Application Security**

**Frigate Authentication** (JWT):

```yaml
# config/config.yml

auth:
  enabled: true
  secret_key: "your-very-long-random-secret-key-here-min-32-chars"
  access_token_expire_minutes: 60
  refresh_token_expire_days: 30

  # User database (or integrate with Keycloak/LDAP)
  users:
    admin:
      password: "$2b$12$hashed_password_here"
      roles:
        - admin
    operator:
      password: "$2b$12$another_hashed_password"
      roles:
        - viewer
        - operator

  # Role-based access control
  roles:
    admin:
      cameras: "*"
      clips: "*"
      events: "*"
      config: true
      delete: true

    operator:
      cameras: "*"
      clips: ["read"]
      events: ["read", "update"]
      config: false
      delete: false

    viewer:
      cameras: ["front_entrance", "lobby"]
      clips: ["read"]
      events: ["read"]
      config: false
      delete: false
```

**HTTPS/TLS Configuration** (NGINX reverse proxy):

```nginx
# /etc/nginx/sites-available/sentinel

server {
    listen 443 ssl http2;
    server_name sentinel.example.com;

    # TLS Configuration
    ssl_certificate /etc/letsencrypt/live/sentinel.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/sentinel.example.com/privkey.pem;

    # Modern TLS only (TLS 1.3 preferred, TLS 1.2 minimum)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;

    # HSTS (force HTTPS for 1 year)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; connect-src 'self' wss://sentinel.example.com; media-src 'self' blob:;" always;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
    limit_req zone=api_limit burst=20 nodelay;

    # Proxy to Frigate
    location / {
        proxy_pass http://10.0.1.10:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support (for live streams)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Block sensitive endpoints from external access
    location ~ ^/(api/config|api/restart) {
        # Only allow from internal IPs
        allow 10.0.1.0/24;
        deny all;

        proxy_pass http://10.0.1.10:5000;
    }

    # Access logs
    access_log /var/log/nginx/sentinel_access.log;
    error_log /var/log/nginx/sentinel_error.log;
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name sentinel.example.com;
    return 301 https://$server_name$request_uri;
}
```

**Layer 3: Data Encryption**

**Database Encryption** (PostgreSQL):

```bash
# Enable SSL for PostgreSQL connections

# /var/lib/postgresql/data/postgresql.conf
ssl = on
ssl_cert_file = '/etc/ssl/certs/server.crt'
ssl_key_file = '/etc/ssl/private/server.key'
ssl_ca_file = '/etc/ssl/certs/ca.crt'

# Require SSL for all connections
# /var/lib/postgresql/data/pg_hba.conf
hostssl all all 0.0.0.0/0 scram-sha-256
```

**MinIO Encryption** (S3 bucket encryption):

```bash
# Enable encryption at rest for MinIO buckets

mc admin config set myminio/ \
  encryption master-key="my-32-byte-long-secret-key-here!"

# Enable encryption for specific bucket
mc encrypt set sse-s3 myminio/frigate-hot
mc encrypt set sse-s3 myminio/frigate-warm
mc encrypt set sse-s3 myminio/frigate-cold
```

---

## Network Architecture

### Deployment Network Topology

**Small Deployment (1-10 cameras):**

```
Internet
   │
   ▼
[Router/Firewall]
   │
   ├──[WiFi/Switch]────[User Devices]
   │
   ├──[PoE Switch]─────[IP Cameras x 10]
   │                    (192.168.100.101-110)
   │
   └──[Server]─────────[Frigate + PostgreSQL + MinIO]
       (10.0.1.10)      Intel NUC / Jetson Orin
                        + Coral TPU
                        Storage: 2TB NVMe SSD
```

**Medium Deployment (10-100 cameras):**

```
Internet
   │
   ▼
[Enterprise Firewall]
   │
   ├──[Core Switch 10Gbps]
   │      │
   │      ├──[Management VLAN 10.0.1.0/24]
   │      │     │
   │      │     ├──[Frigate Servers x 3] (load balanced)
   │      │     ├──[PostgreSQL HA Cluster]
   │      │     ├──[MinIO Cluster (4 nodes)]
   │      │     └──[Workstations]
   │      │
   │      ├──[Camera VLAN 192.168.100.0/24]
   │      │     │
   │      │     ├──[PoE Switch 1]──[Cameras 1-24]
   │      │     ├──[PoE Switch 2]──[Cameras 25-48]
   │      │     ├──[PoE Switch 3]──[Cameras 49-72]
   │      │     └──[PoE Switch 4]──[Cameras 73-100]
   │      │
   │      └──[Storage VLAN 10.0.2.0/24]
   │            └──[NAS / SAN]──[Long-term storage]
   │
   └──[DMZ]
       └──[Reverse Proxy]──[External HTTPS access]
```

**Enterprise Deployment (100-1,000+ cameras):**

```
                        [Internet]
                            │
                            ▼
                    [Edge Firewall]
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
    [Site A: Building 1] [Site B] [Site C: Campus]
         (50 cameras)    (30 cams)  (200 cameras)
            │               │               │
            │               │               │
    ┌───────┴─────┐  ┌──────┴──────┐  ┌────┴─────┐
    │             │  │             │  │          │
    ▼             ▼  ▼             ▼  ▼          ▼
[Edge Server] [Cams] [Edge Server] [Cams] [Regional] [Cams]
Frigate Lite        Frigate Lite          Cluster
Coral TPU           Coral TPU             (3 servers)
Local 7-day         Local 7-day           Local 14-day
    │                   │                      │
    └───────────────────┴──────────────────────┘
                        │
                    [MPLS/VPN]
                        │
                        ▼
            ┌───────────────────────┐
            │  Central Data Center  │
            │                       │
            │ [Frigate Aggregator]  │
            │ [PostgreSQL Cluster]  │
            │ [MinIO Object Store]  │
            │   (Multi-PB)          │
            │ [AI Training Pipeline]│
            │ [Analytics Dashboard] │
            └───────────────────────┘
```

### Bandwidth Calculations

**Per-Camera Bandwidth:**

| Resolution | FPS | Codec | Bitrate | Daily | Monthly |
|------------|-----|-------|---------|-------|---------|
| 1080p | 15 | H.265 | 2 Mbps | 21 GB | 630 GB |
| 1080p | 30 | H.265 | 4 Mbps | 43 GB | 1.3 TB |
| 4K | 15 | H.265 | 8 Mbps | 86 GB | 2.6 TB |
| 4K | 30 | H.265 | 16 Mbps | 173 GB | 5.2 TB |

**100-Camera Deployment** (1080p @ 15 FPS, H.265):
- Total bandwidth: 200 Mbps (peak continuous)
- Daily storage: 2.1 TB
- Monthly storage: 63 TB (30-day retention)
- Recommended uplink: 1 Gbps (20% headroom)

---

## Scalability & Performance

### Horizontal Scaling Architecture

**Load Distribution Strategies:**

**1. Camera Sharding** (by camera count):

```yaml
# Frigate Instance 1: Cameras 1-50
cameras:
  camera_001: ...
  camera_002: ...
  # ... up to camera_050

# Frigate Instance 2: Cameras 51-100
cameras:
  camera_051: ...
  camera_052: ...
  # ... up to camera_100
```

**2. Role-Based Scaling** (by function):

```
┌─────────────────────────────────────────────────┐
│  Detection Cluster (GPU-heavy)                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │Frigate 1 │  │Frigate 2 │  │Frigate 3 │      │
│  │4x RTX    │  │4x RTX    │  │4x RTX    │      │
│  │4090      │  │4090      │  │4090      │      │
│  │          │  │          │  │          │      │
│  │Cameras:  │  │Cameras:  │  │Cameras:  │      │
│  │1-30      │  │31-60     │  │61-90     │      │
│  └──────────┘  └──────────┘  └──────────┘      │
└─────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│  Recording Cluster (Storage-heavy)               │
│  ┌──────────┐  ┌──────────┐                     │
│  │Recorder 1│  │Recorder 2│                     │
│  │20TB RAID │  │20TB RAID │                     │
│  │          │  │          │                     │
│  │All       │  │All       │                     │
│  │cameras   │  │cameras   │                     │
│  │(hot      │  │(redundant│                     │
│  │storage)  │  │backup)   │                     │
│  └──────────┘  └──────────┘                     │
└─────────────────────────────────────────────────┘
```

**Performance Benchmarks:**

| Hardware | Cameras (1080p) | Cameras (4K) | Total FPS | Cost |
|----------|-----------------|--------------|-----------|------|
| **Raspberry Pi 4 + Coral TPU** | 4 | 1 | 20 | $140 |
| **Intel NUC i7 + Coral TPU** | 10 | 3 | 50 | $700 |
| **Jetson Orin Nano** | 8 | 2 | 40 | $500 |
| **Jetson Orin AGX** | 20 | 6 | 100 | $2,000 |
| **Xeon + RTX 4090** | 60 | 20 | 300 | $6,000 |
| **Dual Xeon + 4x RTX 4090** | 250 | 80 | 1,200 | $20,000 |

### Caching Strategy

**Redis Caching Layer:**

```python
import redis
import json

class CacheManager:
    def __init__(self, redis_host='localhost', redis_port=6379):
        self.redis = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

        # Cache TTLs
        self.ttls = {
            'camera_status': 10,      # 10 seconds
            'live_detections': 5,     # 5 seconds
            'event_list': 60,         # 1 minute
            'camera_config': 300,     # 5 minutes
            'hot_list': 600           # 10 minutes
        }

    def cache_camera_status(self, camera_name, status):
        """Cache camera online/offline status"""
        key = f"camera:status:{camera_name}"
        self.redis.setex(key, self.ttls['camera_status'], json.dumps(status))

    def get_camera_status(self, camera_name):
        """Get cached camera status"""
        key = f"camera:status:{camera_name}"
        data = self.redis.get(key)
        return json.loads(data) if data else None

    def cache_detections(self, camera_name, detections):
        """Cache latest detections for quick dashboard updates"""
        key = f"detections:live:{camera_name}"
        self.redis.setex(key, self.ttls['live_detections'], json.dumps(detections))

    def cache_hot_list(self, hot_list_data):
        """Cache hot-list for fast LPR matching"""
        key = "hot_list:all"
        self.redis.setex(key, self.ttls['hot_list'], json.dumps(hot_list_data))

    def invalidate_cache(self, pattern):
        """Invalidate cache by pattern (e.g., "camera:*")"""
        for key in self.redis.scan_iter(match=pattern):
            self.redis.delete(key)
```

---

## High Availability & Redundancy

### HA Architecture

**3-Node Frigate Cluster with Load Balancer:**

```
                    [Load Balancer - HAProxy]
                    (VIP: 10.0.1.100)
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
    [Frigate Node 1] [Frigate Node 2] [Frigate Node 3]
    10.0.1.101       10.0.1.102       10.0.1.103
    Active           Active           Active
    Cameras 1-30     Cameras 31-60    Cameras 61-90
            │               │               │
            └───────────────┼───────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │  PostgreSQL Primary/Replica   │
            │  (Streaming Replication)      │
            │  Primary: 10.0.1.201          │
            │  Replica: 10.0.1.202          │
            └───────────────────────────────┘
                            │
                            ▼
            ┌───────────────────────────────┐
            │  MinIO Distributed Cluster    │
            │  4 nodes (erasure coded 4:2) │
            │  10.0.1.211-214               │
            └───────────────────────────────┘
```

**HAProxy Configuration:**

```
# /etc/haproxy/haproxy.cfg

global
    log /dev/log local0
    log /dev/log local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5000
    timeout client  50000
    timeout server  50000

# Frigate Web UI (round-robin)
frontend frigate_frontend
    bind *:5000
    default_backend frigate_backend

backend frigate_backend
    balance roundrobin
    option httpchk GET /api/version
    http-check expect status 200

    server frigate1 10.0.1.101:5000 check inter 5000 rise 2 fall 3
    server frigate2 10.0.1.102:5000 check inter 5000 rise 2 fall 3
    server frigate3 10.0.1.103:5000 check inter 5000 rise 2 fall 3

# Stats interface
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 30s
    stats auth admin:password
```

**PostgreSQL Streaming Replication:**

```bash
# Primary server (10.0.1.201)
# /var/lib/postgresql/data/postgresql.conf

wal_level = replica
max_wal_senders = 3
wal_keep_size = 1GB
hot_standby = on

# /var/lib/postgresql/data/pg_hba.conf
host replication replicator 10.0.1.202/32 scram-sha-256

# Replica server (10.0.1.202)
# Create replication slot on primary first:
# psql> SELECT * FROM pg_create_physical_replication_slot('replica_1');

# Stop replica, clone from primary
pg_basebackup -h 10.0.1.201 -D /var/lib/postgresql/data -U replicator -P -v -R -X stream -C -S replica_1

# Start replica (will automatically replicate)
systemctl start postgresql
```

**Automatic Failover** (Patroni for PostgreSQL):

```yaml
# /etc/patroni/patroni.yml

scope: frigate_cluster
name: node1

restapi:
  listen: 10.0.1.201:8008
  connect_address: 10.0.1.201:8008

etcd:
  hosts: 10.0.1.220:2379,10.0.1.221:2379,10.0.1.222:2379

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
        shared_buffers: 4GB
        effective_cache_size: 12GB

postgresql:
  listen: 10.0.1.201:5432
  connect_address: 10.0.1.201:5432
  data_dir: /var/lib/postgresql/data
  authentication:
    replication:
      username: replicator
      password: repl_password
    superuser:
      username: postgres
      password: postgres_password
```

---

## Integration Architecture

### REST API Reference

**Core Endpoints:**

```
# Authentication
POST   /api/auth/login              # Get JWT token
POST   /api/auth/refresh            # Refresh token
POST   /api/auth/logout             # Invalidate token

# Cameras
GET    /api/cameras                 # List all cameras
GET    /api/cameras/{name}          # Get camera details
POST   /api/cameras/{name}/snapshot # Capture snapshot
POST   /api/cameras/{name}/ptz      # PTZ control
GET    /api/cameras/{name}/recordings # Get recordings list

# Events
GET    /api/events                  # List events (paginated)
GET    /api/events/{id}             # Get event details
PUT    /api/events/{id}             # Update event (mark false positive)
DELETE /api/events/{id}             # Delete event
GET    /api/events/{id}/snapshot    # Get event snapshot
GET    /api/events/{id}/clip        # Download event video clip
GET    /api/events/{id}/thumbnail   # Get event thumbnail

# Live Streaming
GET    /api/cameras/{name}/latest.jpg # Latest frame (MJPEG)
GET    /api/cameras/{name}/webrtc     # WebRTC offer/answer
GET    /live/webrtc/cameras/{name}    # WebRTC live stream

# Statistics
GET    /api/stats                   # System-wide stats
GET    /api/cameras/{name}/stats    # Per-camera stats

# Configuration
GET    /api/config                  # Get Frigate config (admin only)
POST   /api/config                  # Update config (admin only)
POST   /api/restart                 # Restart Frigate (admin only)

# Alerts
GET    /api/alerts                  # List alert rules
POST   /api/alerts                  # Create alert rule
PUT    /api/alerts/{id}             # Update alert rule
DELETE /api/alerts/{id}             # Delete alert rule
```

**Example API Usage** (Python):

```python
import requests
import json

class SentinelAPI:
    def __init__(self, base_url, username, password):
        self.base_url = base_url
        self.token = None
        self.login(username, password)

    def login(self, username, password):
        """Authenticate and get JWT token"""
        response = requests.post(
            f"{self.base_url}/api/auth/login",
            json={"username": username, "password": password}
        )
        self.token = response.json()['access_token']

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}"}

    def list_events(self, camera=None, label=None, limit=50):
        """List recent events"""
        params = {'limit': limit}
        if camera:
            params['camera'] = camera
        if label:
            params['label'] = label

        response = requests.get(
            f"{self.base_url}/api/events",
            headers=self._headers(),
            params=params
        )
        return response.json()

    def get_event_clip(self, event_id, output_path):
        """Download event video clip"""
        response = requests.get(
            f"{self.base_url}/api/events/{event_id}/clip",
            headers=self._headers(),
            stream=True
        )

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

    def create_alert_rule(self, name, camera_filter, label_filter, actions):
        """Create new alert rule"""
        rule = {
            "name": name,
            "enabled": True,
            "camera_filter": camera_filter,
            "label_filter": label_filter,
            "confidence_threshold": 0.85,
            "cooldown_seconds": 300,
            "actions": actions
        }

        response = requests.post(
            f"{self.base_url}/api/alerts",
            headers=self._headers(),
            json=rule
        )
        return response.json()

    def get_camera_snapshot(self, camera_name, output_path):
        """Capture current snapshot"""
        response = requests.post(
            f"{self.base_url}/api/cameras/{camera_name}/snapshot",
            headers=self._headers()
        )

        with open(output_path, 'wb') as f:
            f.write(response.content)

# Usage
api = SentinelAPI("https://sentinel.example.com", "admin", "password")

# Get recent person detections
events = api.list_events(label="person", limit=10)
for event in events:
    print(f"{event['camera']}: Person detected at {event['start_time']} ({event['top_score']:.2f})")

# Create alert for hot-list vehicles in parking lot
api.create_alert_rule(
    name="Hot-List Vehicle Alert",
    camera_filter=["parking_lpr"],
    label_filter=["car", "truck"],
    actions={
        "email": ["security@example.com"],
        "sms": ["+15551234567"],
        "webhook": "https://api.example.com/alerts/hot-list"
    }
)
```

### MQTT Topics

**Published by Frigate:**

```
frigate/events/{camera_name}/new       # New event started
frigate/events/{camera_name}/update    # Event updated (higher confidence)
frigate/events/{camera_name}/end       # Event ended

frigate/stats                          # System statistics (every 60s)
frigate/stats/{camera_name}            # Per-camera stats (every 60s)

frigate/cameras/{camera_name}/status   # Camera online/offline
frigate/cameras/{camera_name}/motion   # Motion detected (binary)

frigate/alerts/{camera_name}/{rule_name} # Alert triggered

sentinel/analytics/{camera_name}/face   # Face recognized
sentinel/analytics/{camera_name}/lpr    # License plate read
sentinel/analytics/{camera_name}/custom # Custom AI result
```

**Subscribed by Frigate:**

```
frigate/cameras/{camera_name}/snapshot/request  # Request snapshot
frigate/cameras/{camera_name}/ptz/command       # PTZ control
frigate/restart                                 # Restart Frigate
```

**Example MQTT Client** (Node-RED flow):

```json
[
  {
    "id": "mqtt_in",
    "type": "mqtt in",
    "topic": "frigate/events/+/new",
    "broker": "mosquitto_broker",
    "qos": "1",
    "outputs": 1,
    "name": "Frigate Events"
  },
  {
    "id": "filter_person",
    "type": "switch",
    "name": "Filter Person",
    "property": "payload.label",
    "rules": [
      {
        "t": "eq",
        "v": "person",
        "vt": "str"
      }
    ]
  },
  {
    "id": "check_hot_list",
    "type": "function",
    "name": "Check Hot-List",
    "func": "// Check if face is on watch list\nconst identity = msg.payload.face_recognition?.identity;\nif (identity && context.global.watchList.includes(identity)) {\n    msg.alert = true;\n    msg.severity = 'critical';\n} else {\n    msg.alert = false;\n}\nreturn msg;"
  },
  {
    "id": "send_alert",
    "type": "email",
    "name": "Email Security",
    "to": "security@example.com",
    "subject": "Security Alert: Watch List Match"
  }
]
```

---

## Deployment Models

### Docker Compose (All-in-One)

**File**: `docker-compose.yml`

```yaml
version: '3.8'

services:
  frigate:
    container_name: frigate
    image: ghcr.io/blakeblackshear/frigate:0.13.0
    restart: unless-stopped
    privileged: true
    shm_size: '256mb'

    devices:
      - /dev/bus/usb:/dev/bus/usb  # Coral TPU
      - /dev/dri:/dev/dri          # Intel QuickSync

    volumes:
      - ./config:/config
      - ./storage:/media/frigate
      - type: tmpfs
        target: /tmp/cache
        tmpfs:
          size: 1000000000

    ports:
      - "5000:5000"   # Web UI
      - "8554:8554"   # RTSP
      - "8555:8555/tcp"
      - "8555:8555/udp"

    environment:
      FRIGATE_RTSP_PASSWORD: "password"
      TZ: "America/Toronto"

    depends_on:
      - postgres
      - mosquitto
      - go2rtc

  postgres:
    container_name: postgres
    image: timescale/timescaledb:latest-pg15
    restart: unless-stopped

    volumes:
      - ./postgres_data:/var/lib/postgresql/data

    environment:
      POSTGRES_USER: frigate
      POSTGRES_PASSWORD: password
      POSTGRES_DB: frigate

    ports:
      - "5432:5432"

  mosquitto:
    container_name: mosquitto
    image: eclipse-mosquitto:latest
    restart: unless-stopped

    volumes:
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/data:/mosquitto/data
      - ./mosquitto/log:/mosquitto/log

    ports:
      - "1883:1883"

  go2rtc:
    container_name: go2rtc
    image: alexxit/go2rtc:latest
    restart: unless-stopped

    volumes:
      - ./go2rtc.yaml:/config/go2rtc.yaml

    ports:
      - "1984:1984"  # Web UI
      - "8555:8555"  # WebRTC

  minio:
    container_name: minio
    image: minio/minio:latest
    restart: unless-stopped

    command: server /data --console-address ":9001"

    volumes:
      - ./minio_data:/data

    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin

    ports:
      - "9000:9000"
      - "9001:9001"

  grafana:
    container_name: grafana
    image: grafana/grafana:latest
    restart: unless-stopped

    volumes:
      - ./grafana_data:/var/lib/grafana

    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin

    ports:
      - "3000:3000"

    depends_on:
      - postgres

  redis:
    container_name: redis
    image: redis:alpine
    restart: unless-stopped

    ports:
      - "6379:6379"

networks:
  default:
    name: sentinel_network
```

### Kubernetes Deployment

**Frigate StatefulSet:**

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: frigate
  namespace: sentinel
spec:
  serviceName: "frigate"
  replicas: 3
  selector:
    matchLabels:
      app: frigate
  template:
    metadata:
      labels:
        app: frigate
    spec:
      containers:
      - name: frigate
        image: ghcr.io/blakeblackshear/frigate:0.13.0
        ports:
        - containerPort: 5000
          name: http
        - containerPort: 8554
          name: rtsp

        env:
        - name: FRIGATE_RTSP_PASSWORD
          valueFrom:
            secretKeyRef:
              name: frigate-secrets
              key: rtsp-password

        volumeMounts:
        - name: config
          mountPath: /config
        - name: storage
          mountPath: /media/frigate
        - name: cache
          mountPath: /tmp/cache

        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
            nvidia.com/gpu: 1  # Request GPU

        securityContext:
          privileged: true  # Required for Coral TPU

      volumes:
      - name: config
        configMap:
          name: frigate-config
      - name: cache
        emptyDir:
          sizeLimit: 1Gi

  volumeClaimTemplates:
  - metadata:
      name: storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: "fast-ssd"
      resources:
        requests:
          storage: 1Ti
```

---

## Monitoring & Operations

### Prometheus Metrics

**Exported Metrics:**

```
# Cameras
frigate_camera_fps{camera="front_entrance"}
frigate_camera_detection_fps{camera="front_entrance"}
frigate_camera_process_fps{camera="front_entrance"}
frigate_camera_skipped_fps{camera="front_entrance"}

# Detections
frigate_detections_total{camera="front_entrance", label="person"}
frigate_detection_confidence_avg{camera="front_entrance", label="person"}

# System
frigate_cpu_percent
frigate_gpu_percent
frigate_memory_percent
frigate_detector_inference_ms{detector="coral"}

# Storage
frigate_storage_used_bytes{tier="hot"}
frigate_storage_available_bytes{tier="hot"}

# Events
frigate_events_total{camera="front_entrance", label="person"}
frigate_events_active{camera="front_entrance"}
```

### Grafana Dashboard

**Dashboard JSON** (sample panels):

```json
{
  "dashboard": {
    "title": "OS-SENTINEL Monitoring",
    "panels": [
      {
        "id": 1,
        "title": "Camera FPS",
        "type": "graph",
        "targets": [
          {
            "expr": "frigate_camera_fps",
            "legendFormat": "{{camera}}"
          }
        ],
        "yaxes": [
          {
            "label": "FPS",
            "min": 0,
            "max": 30
          }
        ]
      },
      {
        "id": 2,
        "title": "Detection Count (Last Hour)",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(increase(frigate_detections_total[1h]))",
            "legendFormat": "Total Detections"
          }
        ]
      },
      {
        "id": 3,
        "title": "GPU Utilization",
        "type": "gauge",
        "targets": [
          {
            "expr": "frigate_gpu_percent",
            "legendFormat": "GPU %"
          }
        ],
        "thresholds": {
          "steps": [
            {"value": 0, "color": "green"},
            {"value": 70, "color": "yellow"},
            {"value": 90, "color": "red"}
          ]
        }
      },
      {
        "id": 4,
        "title": "Storage Usage by Tier",
        "type": "piechart",
        "targets": [
          {
            "expr": "frigate_storage_used_bytes",
            "legendFormat": "{{tier}}"
          }
        ]
      }
    ]
  }
}
```

---

## Compliance Frameworks

### GDPR Compliance (Privacy)

**Requirements:**

1. **Data Minimization**: Only collect necessary video
2. **Purpose Limitation**: Use only for stated security purposes
3. **Storage Limitation**: Retention policies (delete after 30-90 days)
4. **Privacy by Design**: Face blurring, zone masking
5. **Right to Access**: Provide footage upon request
6. **Right to Erasure**: Delete footage upon request
7. **Data Breach Notification**: Alert within 72 hours

**Implementation:**

```yaml
# GDPR-compliant Frigate configuration

cameras:
  front_entrance:
    # Privacy zones (blur sensitive areas)
    motion:
      mask:
        - 100,100,300,300  # Neighbor's property (blur)

    # Face detection only (no recognition)
    objects:
      track:
        - person
      filters:
        person:
          # Detect but don't store faces
          mask: []  # No face masking (allow detection)

    # Retention policy (GDPR: delete after 30 days)
    record:
      retain:
        days: 30  # Maximum retention
        mode: motion

    # Snapshot retention (even shorter)
    snapshots:
      retain:
        default: 14  # 14 days

# Disable facial recognition (unless legally justified)
# analytics:
#   face_recognition:
#     enabled: false

# Audit logging (track who accessed what)
audit:
  enabled: true
  retention_days: 90
```

**GDPR Compliance Checklist:**

- [ ] Privacy impact assessment completed
- [ ] Data protection officer assigned
- [ ] Privacy policy published
- [ ] Signage posted (cameras in operation)
- [ ] Retention policies configured
- [ ] Face blurring enabled (if no legal basis)
- [ ] Access controls implemented
- [ ] Audit logging enabled
- [ ] Incident response plan documented
- [ ] Data subject request process defined

### HIPAA Compliance (Healthcare)

**Requirements:**

1. **Encryption**: Data at rest and in transit
2. **Access Controls**: Role-based access
3. **Audit Logs**: Track all access to PHI
4. **Business Associate Agreement**: With vendors
5. **Risk Assessment**: Annual security assessment
6. **Training**: Staff training on privacy

**Implementation:**

```yaml
# HIPAA-compliant configuration

# Encryption at rest (MinIO)
minio:
  encryption:
    enabled: true
    key_rotation: 90days

# Encryption in transit (TLS)
network:
  tls_required: true
  min_tls_version: "1.2"

# Access controls
auth:
  enabled: true
  mfa_required: true  # Multi-factor authentication
  password_policy:
    min_length: 12
    complexity: true
    expiry_days: 90

# Audit logging
audit:
  enabled: true
  log_level: verbose
  retention_days: 2555  # 7 years (HIPAA requirement)
  events:
    - login
    - logout
    - video_access
    - config_change
    - export

# Automatic logout
session:
  timeout_minutes: 15  # HIPAA recommends 15 minutes
  concurrent_sessions: 1  # One session per user
```

---

## Disaster Recovery

### Backup Strategy

**3-2-1 Rule:**
- 3 copies of data
- 2 different media types
- 1 off-site copy

**Backup Schedule:**

| Data Type | Frequency | Retention | Method |
|-----------|-----------|-----------|--------|
| **PostgreSQL** | Hourly | 7 days | pg_dump |
| **Config files** | Daily | 30 days | rsync |
| **Hot storage (7 days)** | Daily | 30 days | Rclone to cloud |
| **Event clips** | Weekly | 1 year | Glacier |
| **Full system** | Weekly | 4 weeks | Disk image |

**Automated Backup Script:**

```bash
#!/bin/bash
# /usr/local/bin/sentinel-backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/sentinel"
S3_BUCKET="s3://sentinel-backups"

# 1. PostgreSQL backup
echo "Backing up PostgreSQL..."
pg_dump -h postgres -U frigate -d frigate | gzip > "$BACKUP_DIR/db_$DATE.sql.gz"

# 2. Config files
echo "Backing up configuration..."
tar -czf "$BACKUP_DIR/config_$DATE.tar.gz" /etc/frigate

# 3. Event clips (last 7 days, upload to S3)
echo "Syncing event clips to S3..."
rclone sync /media/frigate/clips/ $S3_BUCKET/clips/ \
  --max-age 7d \
  --transfers 4 \
  --checkers 8

# 4. MinIO metadata
echo "Backing up MinIO metadata..."
mc admin config export myminio > "$BACKUP_DIR/minio_config_$DATE.json"

# 5. Cleanup old backups (keep 30 days local)
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup complete: $DATE"
```

**Restore Procedure:**

```bash
#!/bin/bash
# Disaster recovery restore

# 1. Restore PostgreSQL
gunzip < backup/db_20241208.sql.gz | psql -h postgres -U frigate -d frigate

# 2. Restore configuration
tar -xzf backup/config_20241208.tar.gz -C /

# 3. Restore video clips from S3
rclone sync s3://sentinel-backups/clips/ /media/frigate/clips/ \
  --progress

# 4. Restart services
docker-compose restart

echo "Restore complete"
```

---

## Cost Modeling at Scale

### Total Cost of Ownership (TCO)

**100-Camera Deployment (3 years):**

| Category | Year 1 | Year 2 | Year 3 | Total |
|----------|--------|--------|--------|-------|
| **Hardware** | | | | |
| Cameras (100x $200) | $20,000 | $0 | $0 | $20,000 |
| Servers (3x $6,000) | $18,000 | $0 | $6,000 | $24,000 |
| Storage (100TB) | $15,000 | $5,000 | $5,000 | $25,000 |
| Network (switches, cabling) | $10,000 | $0 | $0 | $10,000 |
| **Software** | | | | |
| OS-SENTINEL (open source) | $0 | $0 | $0 | $0 |
| **Labor** | | | | |
| Installation | $20,000 | $0 | $0 | $20,000 |
| Training | $5,000 | $0 | $0 | $5,000 |
| Maintenance (20 hrs/mo) | $24,000 | $24,000 | $24,000 | $72,000 |
| **Operational** | | | | |
| Electricity (~10 kW) | $10,512 | $10,512 | $10,512 | $31,536 |
| Internet (1 Gbps) | $12,000 | $12,000 | $12,000 | $36,000 |
| **Total** | $134,512 | $51,512 | $57,512 | **$243,536** |
| **Per Camera** | $1,345 | $515 | $575 | **$2,435** |

**Comparison to Proprietary (Genetec, Verkada):**

| Solution | Cameras | 3-Year TCO | Per Camera |
|----------|---------|------------|------------|
| **OS-SENTINEL** | 100 | $243,536 | $2,435 |
| **Genetec Synergy** | 100 | $480,000 | $4,800 |
| **Verkada** | 100 | $720,000 | $7,200 |

**ROI Calculation:**

```
Savings vs. Genetec: $480,000 - $243,536 = $236,464 (49% less)
Savings vs. Verkada: $720,000 - $243,536 = $476,464 (66% less)

Break-even: Immediate (no licensing fees)
Payback period: N/A (lower upfront cost)
```

---

## Conclusion

OS-SENTINEL provides enterprise-grade AI-powered video surveillance with complete ownership, privacy, and cost control. The open-source foundation enables customization for any industry while avoiding vendor lock-in and recurring licensing fees.

**Key Advantages:**

✓ **Cost**: 50-70% less than proprietary alternatives
✓ **Privacy**: On-premise AI (no cloud transmission)
✓ **Flexibility**: Custom models, integrations, workflows
✓ **Scalability**: 1 to 10,000+ cameras
✓ **Ownership**: No licensing fees, perpetual use
✓ **Community**: Active open-source development

**Next Steps:**

1. Review deployment models for your scale
2. Pilot with 5-10 cameras
3. Train custom AI models for your industry
4. Integrate with existing systems (access control, alarms)
5. Scale to full production

---

**Document Version**: 1.0
**Last Updated**: December 2024
**Maintained By**: OS-SENTINEL Architecture Team
**Next Review**: Q2 2025

For technical support or architecture consulting: architecture@opensecure.io
