---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: 388efd7d-e1d1-4ed6-ae81-01107bafbee9
original_filename: development.md
created_at: 2025-12-02T00:47:54.475170+00:00
content_hash: 32792e91c3bc
---

# Module Development Guide

## Overview

The OpenVision Platform uses a plugin-based architecture that allows you to create custom analytics, integrations, and processing modules without modifying core code. Modules run as isolated containers and communicate via standardized APIs.

## Module Types

### 1. Analytics Modules
Process video frames to detect objects, recognize patterns, or extract insights.

**Examples**: 
- Custom object detection
- PPE (Personal Protective Equipment) detection
- Crowd counting
- Vehicle classification
- Safety compliance monitoring

### 2. Integration Modules
Connect with external systems and devices.

**Examples**:
- Access control integration
- Building automation systems
- Custom IoT protocols
- Third-party APIs
- Legacy system adapters

### 3. Processing Modules
Transform or enhance video/data before storage or analysis.

**Examples**:
- Video enhancement (denoising, stabilization)
- Privacy filters (face blurring)
- Format conversion
- Compression optimization

### 4. Notification Modules
Handle alerts and notifications to external systems.

**Examples**:
- SMS gateways
- Custom webhook handlers
- PagerDuty integration
- Slack/Teams notifications

## Module Architecture

```
┌─────────────────────────────────────────┐
│         Your Custom Module              │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │    Module Implementation          │  │
│  │    (Your Code)                    │  │
│  └───────────────────────────────────┘  │
│              ▲                          │
│              │                          │
│  ┌───────────▼───────────────────────┐  │
│  │    OpenVision SDK                 │  │
│  │  • Frame receiver                 │  │
│  │  • Result publisher               │  │
│  │  • Config management              │  │
│  │  • Health checks                  │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
              ▲         │
              │         │
       ┌──────┴─────┐   └────────┐
       │  Video     │   │ NATS   │
       │  Stream    │   │ Events │
       └────────────┘   └────────┘
```

## Module SDK

### Installation

```bash
# Python SDK
pip install openvision-sdk

# Node.js SDK
npm install @openvision/sdk

# Go SDK
go get github.com/openvision/sdk-go
```

### Python SDK

#### Basic Analytics Module

```python
from openvision.sdk import AnalyticsModule, Detection, BoundingBox
import cv2
import numpy as np

class CustomDetector(AnalyticsModule):
    """
    Custom object detection module example
    """
    
    def __init__(self):
        super().__init__(
            module_id="custom-detector",
            module_name="Custom Object Detector",
            version="1.0.0"
        )
        self.model = None
        
    def initialize(self, config: dict) -> bool:
        """
        Initialize module with configuration
        
        Args:
            config: Module configuration dictionary
            
        Returns:
            True if initialization successful
        """
        self.logger.info("Initializing Custom Detector")
        
        # Load your model
        model_path = config.get('model_path', '/models/custom.pt')
        self.confidence_threshold = config.get('confidence_threshold', 0.7)
        
        try:
            # Load model (example with YOLO, adapt to your needs)
            from ultralytics import YOLO
            self.model = YOLO(model_path)
            self.logger.info(f"Model loaded from {model_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to load model: {e}")
            return False
    
    def process_frame(self, frame: np.ndarray, metadata: dict) -> list:
        """
        Process a single video frame
        
        Args:
            frame: OpenCV image (numpy array, BGR format)
            metadata: Frame metadata (camera_id, timestamp, etc.)
            
        Returns:
            List of Detection objects
        """
        if self.model is None:
            return []
        
        # Run inference
        results = self.model(frame, verbose=False)
        
        detections = []
        for result in results:
            boxes = result.boxes
            
            for box in boxes:
                confidence = float(box.conf[0])
                
                if confidence < self.confidence_threshold:
                    continue
                
                # Extract bounding box
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                class_id = int(box.cls[0])
                class_name = result.names[class_id]
                
                # Create detection object
                detection = Detection(
                    class_name=class_name,
                    confidence=confidence,
                    bbox=BoundingBox(
                        x1=int(x1),
                        y1=int(y1),
                        x2=int(x2),
                        y2=int(y2)
                    ),
                    metadata={
                        'camera_id': metadata.get('camera_id'),
                        'timestamp': metadata.get('timestamp')
                    }
                )
                
                detections.append(detection)
        
        return detections
    
    def process_stream(self, stream_url: str, camera_id: str):
        """
        Process continuous video stream
        
        Args:
            stream_url: RTSP or HTTP stream URL
            camera_id: Unique camera identifier
        """
        cap = cv2.VideoCapture(stream_url)
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    self.logger.warning(f"Failed to read frame from {camera_id}")
                    break
                
                # Process every nth frame (reduce CPU load)
                if frame_count % self.config.get('frame_skip', 5) == 0:
                    metadata = {
                        'camera_id': camera_id,
                        'timestamp': self.get_timestamp(),
                        'frame_number': frame_count
                    }
                    
                    # Process frame
                    detections = self.process_frame(frame, metadata)
                    
                    # Publish results
                    if detections:
                        self.publish_detections(detections)
                
                frame_count += 1
                
        finally:
            cap.release()
    
    def cleanup(self):
        """Cleanup resources"""
        self.logger.info("Cleaning up Custom Detector")
        if self.model:
            del self.model

# Entry point
if __name__ == "__main__":
    module = CustomDetector()
    module.run()
```

#### Configuration File

```yaml
# config.yml
module:
  id: custom-detector
  name: Custom Object Detector
  version: 1.0.0

settings:
  model_path: /models/custom_yolo.pt
  confidence_threshold: 0.7
  frame_skip: 5  # Process every 5th frame
  
  classes:
    - forklift
    - worker
    - safety_vest
    - hard_hat

cameras:
  - camera_id: warehouse_01
    stream_url: rtsp://192.168.1.100/stream1
  - camera_id: warehouse_02
    stream_url: rtsp://192.168.1.101/stream1

nats:
  url: nats://nats:4222
  subject: analytics.detections.custom

redis:
  host: redis
  port: 6379
  db: 0

logging:
  level: INFO
  format: json
```

### Integration Module Example

```python
from openvision.sdk import IntegrationModule
import requests

class AccessControlIntegration(IntegrationModule):
    """
    Integration with access control system
    Correlates badge swipes with camera detections
    """
    
    def initialize(self, config: dict) -> bool:
        self.api_url = config['access_control_api']
        self.api_key = config['api_key']
        return True
    
    def handle_detection(self, detection: dict):
        """
        Called when person is detected
        Check if authorized
        """
        camera_id = detection['camera_id']
        
        # Find nearby door
        door = self.get_nearby_door(camera_id)
        
        if door:
            # Check recent badge swipes
            recent_swipes = self.get_recent_swipes(door['id'], seconds=10)
            
            if not recent_swipes:
                # Person detected but no badge swipe
                self.create_alert(
                    alert_type="tailgating",
                    camera_id=camera_id,
                    door_id=door['id'],
                    detection=detection
                )
    
    def get_recent_swipes(self, door_id: str, seconds: int) -> list:
        """Query access control system"""
        response = requests.get(
            f"{self.api_url}/doors/{door_id}/swipes",
            headers={'Authorization': f'Bearer {self.api_key}'},
            params={'since': self.get_timestamp(seconds_ago=seconds)}
        )
        return response.json()
    
    def create_alert(self, alert_type: str, **kwargs):
        """Publish alert event"""
        self.publish_event(
            subject="alerts.security.tailgating",
            data={
                'type': alert_type,
                'timestamp': self.get_timestamp(),
                **kwargs
            }
        )

if __name__ == "__main__":
    module = AccessControlIntegration()
    module.run()
```

## Module Deployment

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libopencv-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy module code
COPY . .

# Non-root user for security
RUN useradd -m -u 1000 module && chown -R module:module /app
USER module

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8080/health')"

# Entry point
CMD ["python", "module.py"]
```

### requirements.txt

```
openvision-sdk==1.0.0
ultralytics==8.0.200
opencv-python-headless==4.8.1.78
numpy==1.24.3
pydantic==2.4.2
```

### Build and Deploy

```bash
# Build Docker image
docker build -t custom-detector:1.0.0 .

# Test locally
docker run --rm \
  -e NATS_URL=nats://localhost:4222 \
  -e REDIS_HOST=localhost \
  -v $(pwd)/config.yml:/app/config.yml \
  -v $(pwd)/models:/models \
  custom-detector:1.0.0

# Push to registry
docker tag custom-detector:1.0.0 registry.yourdomain.com/custom-detector:1.0.0
docker push registry.yourdomain.com/custom-detector:1.0.0

# Deploy to Kubernetes
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: custom-detector
  namespace: openvision-modules
spec:
  replicas: 2
  selector:
    matchLabels:
      app: custom-detector
  template:
    metadata:
      labels:
        app: custom-detector
    spec:
      containers:
      - name: detector
        image: registry.yourdomain.com/custom-detector:1.0.0
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        env:
        - name: NATS_URL
          value: "nats://nats:4222"
        - name: REDIS_HOST
          value: "redis"
        volumeMounts:
        - name: config
          mountPath: /app/config.yml
          subPath: config.yml
        - name: models
          mountPath: /models
      volumes:
      - name: config
        configMap:
          name: custom-detector-config
      - name: models
        persistentVolumeClaim:
          claimName: ml-models-pvc
EOF
```

## Module API Reference

### Base Module Class

```python
class BaseModule:
    """Base class for all modules"""
    
    def __init__(self, module_id: str, module_name: str, version: str):
        """
        Initialize module
        
        Args:
            module_id: Unique module identifier
            module_name: Human-readable name
            version: Semantic version
        """
        pass
    
    def initialize(self, config: dict) -> bool:
        """
        Initialize module with configuration
        Must be implemented by subclass
        
        Returns:
            True if successful, False otherwise
        """
        raise NotImplementedError
    
    def run(self):
        """
        Main entry point
        Starts the module and handles lifecycle
        """
        pass
    
    def cleanup(self):
        """
        Cleanup resources before shutdown
        Optional override
        """
        pass
    
    # Utility methods
    def get_timestamp(self) -> str:
        """Get current ISO timestamp"""
        pass
    
    def publish_event(self, subject: str, data: dict):
        """Publish event to NATS"""
        pass
    
    def subscribe(self, subject: str, callback):
        """Subscribe to NATS subject"""
        pass
    
    def get_redis_client(self):
        """Get Redis client"""
        pass
    
    def get_postgres_conn(self):
        """Get PostgreSQL connection"""
        pass
```

### Analytics Module Helpers

```python
class Detection:
    """Detection result object"""
    def __init__(self, 
                 class_name: str,
                 confidence: float,
                 bbox: BoundingBox,
                 metadata: dict = None):
        self.class_name = class_name
        self.confidence = confidence
        self.bbox = bbox
        self.metadata = metadata or {}

class BoundingBox:
    """Bounding box coordinates"""
    def __init__(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
    
    def area(self) -> int:
        """Calculate box area"""
        return (self.x2 - self.x1) * (self.y2 - self.y1)
    
    def iou(self, other: 'BoundingBox') -> float:
        """Calculate Intersection over Union"""
        # Implementation
        pass
```

## Testing Modules

### Unit Tests

```python
# test_custom_detector.py
import pytest
import numpy as np
from custom_detector import CustomDetector

@pytest.fixture
def module():
    detector = CustomDetector()
    detector.initialize({
        'model_path': 'tests/fixtures/test_model.pt',
        'confidence_threshold': 0.7
    })
    return detector

def test_initialization(module):
    assert module.model is not None
    assert module.confidence_threshold == 0.7

def test_process_frame(module):
    # Load test image
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    # Process
    detections = module.process_frame(frame, {
        'camera_id': 'test_cam',
        'timestamp': '2024-11-19T10:00:00Z'
    })
    
    # Verify
    assert isinstance(detections, list)

def test_confidence_filtering(module):
    # Test that low-confidence detections are filtered
    pass
```

### Integration Tests

```python
# test_integration.py
import docker
import time

def test_module_deployment():
    """Test module can be deployed and responds to health checks"""
    client = docker.from_env()
    
    # Start dependencies
    nats = client.containers.run('nats:latest', detach=True)
    redis = client.containers.run('redis:alpine', detach=True)
    
    time.sleep(5)  # Wait for services
    
    try:
        # Start module
        module = client.containers.run(
            'custom-detector:test',
            environment={
                'NATS_URL': f'nats://{nats.id}:4222',
                'REDIS_HOST': redis.id
            },
            detach=True
        )
        
        time.sleep(10)  # Wait for initialization
        
        # Check health
        health = module.exec_run('curl http://localhost:8080/health')
        assert health.exit_code == 0
        
    finally:
        # Cleanup
        module.stop()
        nats.stop()
        redis.stop()
```

## Best Practices

### 1. Resource Management

```python
class EfficientModule(AnalyticsModule):
    def process_frame(self, frame, metadata):
        # Process every Nth frame to reduce load
        if metadata['frame_number'] % self.frame_skip != 0:
            return []
        
        # Use smaller image for detection
        resized = cv2.resize(frame, (640, 480))
        
        # Release memory after processing
        del resized
        
        return detections
```

### 2. Error Handling

```python
def process_frame(self, frame, metadata):
    try:
        detections = self.model(frame)
        return detections
    except Exception as e:
        self.logger.error(f"Processing error: {e}", exc_info=True)
        self.metrics.increment('errors.processing')
        return []
```

### 3. Configuration Validation

```python
from pydantic import BaseModel, Field

class ModuleConfig(BaseModel):
    model_path: str = Field(..., description="Path to model file")
    confidence_threshold: float = Field(0.7, ge=0.0, le=1.0)
    frame_skip: int = Field(5, ge=1, le=30)

def initialize(self, config: dict) -> bool:
    try:
        validated_config = ModuleConfig(**config)
        self.config = validated_config
        return True
    except ValidationError as e:
        self.logger.error(f"Invalid configuration: {e}")
        return False
```

### 4. Metrics and Monitoring

```python
from prometheus_client import Counter, Histogram

class MonitoredModule(AnalyticsModule):
    def __init__(self):
        super().__init__()
        
        # Define metrics
        self.frames_processed = Counter(
            'frames_processed_total',
            'Total frames processed'
        )
        
        self.processing_time = Histogram(
            'frame_processing_seconds',
            'Time to process frame'
        )
        
        self.detections_count = Counter(
            'detections_total',
            'Total detections',
            ['class_name']
        )
    
    def process_frame(self, frame, metadata):
        with self.processing_time.time():
            detections = super().process_frame(frame, metadata)
        
        self.frames_processed.inc()
        
        for det in detections:
            self.detections_count.labels(
                class_name=det.class_name
            ).inc()
        
        return detections
```

## Module Marketplace

### Publishing Modules

1. **Package your module**:
```bash
./scripts/package-module.sh custom-detector
```

2. **Create module manifest**:
```yaml
# module.yaml
name: custom-detector
version: 1.0.0
author: Your Company
description: Custom object detection for forklifts
license: Apache-2.0
repository: https://github.com/yourcompany/custom-detector

requirements:
  cpu: 1000m
  memory: 2Gi
  gpu: optional

configuration:
  - name: confidence_threshold
    type: float
    default: 0.7
    description: Minimum confidence for detections
  
  - name: model_path
    type: string
    required: true
    description: Path to model file

inputs:
  - type: video_stream
    formats: [rtsp, http]

outputs:
  - type: detections
    schema: openvision.detection.v1
```

3. **Submit to marketplace**:
```bash
openvision-cli module publish custom-detector
```

## Support

- SDK Documentation: https://docs.openvision.io/sdk
- Module Examples: https://github.com/openvision/modules
- Community Forum: https://community.openvision.io
- Discord: #module-development channel

---

**Next**: [API Reference](../api/reference.md) | [Integration Guide](integration.md)
