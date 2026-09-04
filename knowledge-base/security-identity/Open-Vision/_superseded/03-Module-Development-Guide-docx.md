---
source_project: Open Vision
source_project_uuid: 019adc89-3095-77fb-a6f8-3f599d84699a
doc_uuid: 9b4e3c90-29fd-43e4-a462-8156129492f3
original_filename: 03-Module-Development-Guide.docx
created_at: 2025-12-02T00:49:43.295361+00:00
content_hash: 8f4d5286535fstatus: duplicate
duplicate_of: "ai-ml-research/IHOSE/03-Module-Development-Guide-docx.md"
duplicate_reason: "exact content_hash match, different category (same doc uploaded to multiple Claude Projects)"
---

OpenVision Platform

**Custom Module Development Guide**

Building Analytics Extensions & Integrations

Version 1.0

Introduction

OpenVision Platform\'s module framework enables organizations to extend
the system with custom analytics, processing logic, and integrations
without modifying the core codebase. Modules are containerized
applications that conform to standardized interfaces for receiving video
streams and emitting structured results.

This guide covers the complete module lifecycle: development, testing,
containerization, deployment, and monitoring. Whether building simple
object detection enhancements or complex multi-stage analytics
pipelines, the module framework provides the infrastructure and tooling
needed for production deployment.

Module Types

  -----------------------------------------------------------------------
  **Module Type**   **Purpose**                **Examples**
  ----------------- -------------------------- --------------------------
  **Frame           Processes individual       License plate recognition,
  Processor**       frames, returns per-frame  PPE detection, quality
                    results                    inspection

  **Stream          Maintains state across     Loitering detection, queue
  Analyzer**        frames, detects patterns   analysis, crowd counting
                    over time                  

  **Event           Triggers alerts based on   Perimeter breach,
  Generator**       analytics results and      unauthorized access,
                    business rules             equipment fault

  **Integration     Connects analytics results SIEM integration, POS
  Module**          to external systems        correlation, access
                                               control link
  -----------------------------------------------------------------------

Module Interface Specification

Input Methods

Modules receive video data through one of the following standard
interfaces. The platform automatically handles protocol conversion and
buffering.

**1. HTTP REST API**

Simple request-response pattern. Platform POSTs video frames as JPEG/PNG
with metadata.

POST /analyze Content-Type: multipart/form-data image: \[binary JPEG
data\] metadata: {camera_id, timestamp, frame_number}

**2. gRPC Streaming**

High-performance bidirectional streaming. Ideal for real-time analytics
with low latency.

service VideoAnalytics { rpc ProcessStream(stream Frame) returns (stream
Result); }

**3. RTSP Direct Access**

Module pulls video streams directly via RTSP URL. Full control over
frame extraction and buffering.

Environment: RTSP_URL=rtsp://mediamtx:8554/camera123

**4. Message Queue**

Asynchronous processing via NATS or Kafka. Decouples module from video
pipeline.

Topic: video.frames.camera-01 Payload: {frame_base64, metadata}

Output Format

All modules must return results as structured JSON conforming to this
schema:

{ \"module_id\": \"license-plate-detector\", \"version\": \"1.2.3\",
\"timestamp\": \"2025-11-19T14:30:00Z\", \"camera_id\":
\"cam-parking-01\", \"frame_number\": 12345, \"processing_time_ms\": 45,
\"detections\": \[ { \"class\": \"license-plate\", \"confidence\": 0.95,
\"bbox\": {\"x\": 100, \"y\": 200, \"width\": 150, \"height\": 50},
\"attributes\": {\"plate_number\": \"ABC123\", \"state\": \"CA\"} } \],
\"events\": \[ { \"type\": \"vehicle-detected\", \"severity\": \"info\",
\"description\": \"Vehicle with plate ABC123 entered zone\" } \],
\"metadata\": {\"gpu_utilization\": 0.75, \"queue_depth\": 3} }

Development Workflow

Step 1: Setup Development Environment

**Prerequisites:**

-   Docker and Docker Compose

-   Python 3.9+ or C++17 compiler

-   OpenCV, NumPy, Requests (for Python modules)

-   OpenVision SDK (provided as starter template)

-   Access to module registry (obtain credentials from platform admin)

**Clone SDK Template:**

git clone https://github.com/openvision/module-sdk-python.git cd
module-sdk-python pip install -r requirements.txt

Step 2: Implement Module Logic

**Python Example: Custom Object Detector**

from openvision.module import VideoModule import cv2 import numpy as np
class CustomDetector(VideoModule): def \_\_init\_\_(self, config):
super().\_\_init\_\_(config) self.model =
self.load_model(config\[\'model_path\'\]) def process_frame(self, frame,
metadata): \# Your analytics logic here detections =
self.model.detect(frame) return { \'detections\': \[ { \'class\':
det.class_name, \'confidence\': float(det.score), \'bbox\':
det.bbox.to_dict() } for det in detections \], \'processing_time_ms\':
metadata\[\'processing_time\'\] } if \_\_name\_\_ == \'\_\_main\_\_\':
module = CustomDetector(config_from_env()) module.start()

Step 3: Test Locally

Use the provided test harness to validate module behavior with recorded
video clips:

python -m openvision.test \\ \--module custom_detector.py \\ \--video
test_clips/parking_lot.mp4 \\ \--config config.yaml

**Test outputs:**

-   Annotated video showing detections

-   Performance metrics (FPS, latency, memory usage)

-   JSON output log for validation

-   Error logs and debugging info

Step 4: Containerization

**Create Dockerfile:**

FROM openvision/module-base-python:3.9-cuda11.8 WORKDIR /app COPY
requirements.txt . RUN pip install \--no-cache-dir -r requirements.txt
COPY src/ ./src/ COPY models/ ./models/ ENV MODULE_NAME=custom-detector
ENV LOG_LEVEL=INFO CMD \[\"python\", \"-m\", \"src.custom_detector\"\]

**Build and tag image:**

docker build -t registry.openvision.local/custom-detector:1.0.0 . docker
push registry.openvision.local/custom-detector:1.0.0

**Resource requirements in module.yaml:**

resources: requests: memory: \"2Gi\" cpu: \"1000m\" nvidia.com/gpu:
\"1\" limits: memory: \"4Gi\" cpu: \"2000m\" nvidia.com/gpu: \"1\"

Deployment

Module Registration

Register module with the platform\'s module registry:

openvision-cli module register \\ \--name custom-detector \\ \--version
1.0.0 \\ \--image registry.openvision.local/custom-detector:1.0.0 \\
\--config module.yaml

**Module Configuration (module.yaml):**

apiVersion: v1 kind: Module metadata: name: custom-detector version:
1.0.0 description: \"Custom object detection for specific use case\"
spec: input: type: grpc-stream cameras: - camera-01 - camera-02 zones: -
parking-lot-zone output: events: - topic: analytics/custom-detections -
webhook: https://client-system/api/events replicas: 2 autoscaling:
enabled: true minReplicas: 1 maxReplicas: 5 targetCPU: 70

Deployment to Kubernetes

Platform automatically generates Kubernetes manifests from module.yaml:

openvision-cli module deploy custom-detector \--environment production

**Verify deployment:**

kubectl get pods -l module=custom-detector kubectl logs -f
custom-detector-7d9f8c-xyz12

**Check module status via API:**

curl https://api.openvision.local/v1/modules/custom-detector/status

Advanced Topics

GPU Acceleration

**CUDA Integration:**

import torch class GPUModule(VideoModule): def \_\_init\_\_(self,
config): super().\_\_init\_\_(config) self.device =
torch.device(\'cuda\' if torch.cuda.is_available() else \'cpu\')
self.model = load_model().to(self.device)

**TensorRT Optimization:**

\# Convert PyTorch model to TensorRT for 3-5x speedup import
torch_tensorrt trt_model = torch_tensorrt.compile( model,
inputs=\[torch_tensorrt.Input((1, 3, 640, 640))\],
enabled_precisions={torch.half} )

State Management

For modules that track state across frames (people tracking, queue
analysis), use Redis for shared state:

import redis class StatefulModule(VideoModule): def \_\_init\_\_(self,
config): super().\_\_init\_\_(config) self.redis =
redis.Redis(host=\'redis\', port=6379, db=0) def process_frame(self,
frame, metadata): \# Retrieve previous state state_key =
f\"tracker:{metadata\[\'camera_id\'\]}\" prev_state =
self.redis.get(state_key) \# Update state new_state =
self.update_tracking(frame, prev_state) \# Save state with TTL
self.redis.setex(state_key, 300, new_state)

Multi-Stage Pipelines

Chain multiple modules together for complex workflows:

pipeline: - module: motion-detector output: motion-events-topic -
module: person-detector input: motion-events-topic condition:
\"event.type == \'motion_detected\'\" output: person-events-topic -
module: face-recognizer input: person-events-topic condition:
\"detection.class == \'person\'\" output: face-recognition-results

Monitoring & Operations

Performance Metrics

Platform automatically collects key metrics from all modules:

-   Processing latency (p50, p95, p99)

-   Throughput (frames per second)

-   Resource utilization (CPU, GPU, memory)

-   Error rate and failure types

-   Queue depth and backpressure

**Custom Metrics:**

from openvision.metrics import Counter, Histogram detection_counter =
Counter(\'detections_total\', \'Total detections\', \[\'class\'\])
confidence_histogram = Histogram(\'detection_confidence\', \'Detection
confidence\') def process_frame(self, frame, metadata): detections =
self.detect(frame) for det in detections:
detection_counter.labels(class=det.class_name).inc()
confidence_histogram.observe(det.confidence)

Logging Best Practices

1.  **Use structured logging (JSON format)**

2.  **Include correlation IDs for request tracing**

3.  **Log at appropriate levels (DEBUG, INFO, WARN, ERROR)**

4.  **Never log sensitive information (PII, credentials)**

import logging import json logger = logging.getLogger(\_\_name\_\_)
logger.info(json.dumps({ \'event\': \'frame_processed\', \'camera_id\':
metadata\[\'camera_id\'\], \'frame_number\':
metadata\[\'frame_number\'\], \'detections\': len(results),
\'processing_time_ms\': elapsed_time }))

Debugging

**Enable debug mode:**

kubectl set env deployment/custom-detector LOG_LEVEL=DEBUG kubectl logs
-f deployment/custom-detector \--tail=100

**Capture failed frames for analysis:**

if detection_failed: debug_path = f\"/debug/failures/{timestamp}.jpg\"
cv2.imwrite(debug_path, frame) logger.error(f\"Detection failed, frame
saved to {debug_path}\")

Best Practices

Performance Optimization

-   **Batch processing:** Process multiple frames in single inference
    call

-   **Frame skipping:** Process every Nth frame for computationally
    expensive analytics

-   **ROI processing:** Only analyze relevant regions of frame

-   **Model quantization:** Use INT8 or FP16 precision for faster
    inference

-   **Async I/O:** Use async operations for network calls and database
    queries

Security

-   Input validation: Validate all external inputs (frame size, metadata
    formats)

-   Secrets management: Use environment variables, never hardcode
    credentials

-   Least privilege: Run containers as non-root user

-   Dependency scanning: Regularly scan for vulnerable dependencies

-   Network policies: Restrict module network access to required
    services only

Reliability

-   Graceful degradation: Return partial results if some processing
    fails

-   Health checks: Implement liveness and readiness probes

-   Timeouts: Set appropriate timeouts for all external calls

-   Circuit breakers: Prevent cascading failures to downstream services

-   Retry logic: Implement exponential backoff for transient failures

Conclusion

The OpenVision module framework provides a production-grade
infrastructure for deploying custom analytics at scale. By following the
patterns and practices outlined in this guide, developers can create
robust, performant modules that integrate seamlessly with the platform
while maintaining operational excellence.

For questions and support, visit the OpenVision developer community at
https://community.openvision.io or file issues at
https://github.com/openvision/modules
