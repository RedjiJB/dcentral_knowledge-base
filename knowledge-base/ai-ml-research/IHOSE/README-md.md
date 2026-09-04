---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: c99be3d9-c143-45d0-a003-55f4e52664d3
original_filename: README.md
created_at: 2025-12-02T00:47:53.883120+00:00
content_hash: 7d314f7879b3cross_category_duplicate_at: "security-identity/Open-Vision/README-md.md"
---

# OpenVision Platform: Enterprise CCTV & IoT Integration Ecosystem

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Status: Alpha](https://img.shields.io/badge/Status-Alpha-orange.svg)]()

## Overview

OpenVision is a fully open-source, enterprise-grade video surveillance and IoT integration platform designed for maximum customization, scalability, and interoperability. Built on modern microservices architecture with edge-to-cloud capabilities.

### Key Features

- **Fully Open Source**: 100% AGPL/Apache 2.0 licensed components
- **Hardware Agnostic**: Runs on x86, ARM, and RISC-V architectures
- **Edge-Native**: Distributed architecture with intelligent edge processing
- **AI-First**: Built-in object detection, face recognition, custom ML model support
- **IoT Integration**: MQTT, ONVIF, Modbus, BACnet, OPC UA support
- **Customizable**: Plugin architecture for client-specific modules
- **Multi-Tenant**: SaaS-ready with complete tenant isolation
- **Digital Twin**: Real-time 3D visualization and simulation
- **Open Hardware**: Recommended open hardware bill of materials

### Architecture Highlights

```
┌─────────────────────────────────────────────────────────────────┐
│                        Cloud/Central Layer                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │Kubernetes│  │PostgreSQL│  │  MinIO   │  │  Grafana │       │
│  │  Cluster │  │ +TimescaleDB  │ Object   │  │ Dashboard│       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ NATS JetStream / MQTT
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Edge Layer (K3s)                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Frigate  │  │MediaMTX  │  │  YOLO    │  │EdgeX     │       │
│  │   VMS    │  │Streaming │  │Analytics │  │Foundry   │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
└─────────────────────────────────────────────────────────────────┘
                              ▲
                              │ RTSP/ONVIF
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Camera Layer                             │
│    [IP Cam 1]  [IP Cam 2]  ... [IP Cam N]  [IoT Sensors]      │
└─────────────────────────────────────────────────────────────────┘
```

## Deployment Options

### 1. Enterprise Edge Deployment
- **Scale**: 500+ cameras across multiple sites
- **Hardware**: Jetson Orin NX edge nodes + central Kubernetes cluster
- **Features**: Full AI analytics, digital twin, multi-site management
- **Docs**: [docs/deployment/enterprise.md](docs/deployment/enterprise.md)

### 2. SMB Cloud Deployment
- **Scale**: 10-50 cameras, single site
- **Hardware**: Orange Pi 5 or cloud VMs
- **Features**: Core VMS, basic analytics, cloud backup
- **Docs**: [docs/deployment/smb.md](docs/deployment/smb.md)

### 3. Household SaaS
- **Scale**: 1-5 cameras
- **Hardware**: Raspberry Pi or cloud-hosted
- **Features**: Live viewing, motion detection, mobile app
- **Docs**: [docs/deployment/household.md](docs/deployment/household.md)

## Quick Start

### Prerequisites
- Docker & Docker Compose OR Kubernetes cluster
- Minimum 4GB RAM, 50GB storage
- Ubuntu 22.04 LTS or compatible Linux distribution

### Basic Installation (Docker Compose)

```bash
# Clone repository
git clone https://github.com/yourusername/openvision-platform.git
cd openvision-platform

# Copy environment configuration
cp configs/env.example configs/.env
nano configs/.env  # Configure your settings

# Launch core services
docker-compose -f deployment/docker/core-stack.yml up -d

# Access web interface
open http://localhost:8080
# Default credentials: admin / changeme
```

### Production Kubernetes Deployment

```bash
# Install prerequisites
./scripts/install-k3s.sh  # For edge nodes
# OR use existing K8s cluster

# Deploy platform
kubectl apply -f deployment/kubernetes/namespace.yml
kubectl apply -f deployment/kubernetes/storage/
kubectl apply -f deployment/kubernetes/core/
kubectl apply -f deployment/kubernetes/analytics/

# Check status
kubectl get pods -n openvision
```

## Project Structure

```
openvision-platform/
├── README.md                          # This file
├── LICENSE                            # Apache 2.0 License
├── docs/                              # Complete documentation
│   ├── architecture/                  # System architecture
│   ├── deployment/                    # Deployment guides
│   ├── modules/                       # Module development
│   ├── api/                           # API documentation
│   └── hardware/                      # Hardware recommendations
├── deployment/                        # Deployment configurations
│   ├── docker/                        # Docker Compose files
│   ├── kubernetes/                    # Kubernetes manifests
│   └── terraform/                     # Infrastructure as Code
├── modules/                           # Custom modules
│   ├── analytics/                     # AI/ML modules
│   ├── integration/                   # IoT integrations
│   └── templates/                     # Module templates
├── configs/                           # Configuration files
│   ├── env.example                    # Environment template
│   ├── cameras.yml                    # Camera configuration
│   └── analytics.yml                  # Analytics pipeline
├── scripts/                           # Utility scripts
│   ├── install-k3s.sh                 # K3s installation
│   ├── setup-edge-node.sh             # Edge node setup
│   └── backup.sh                      # Backup automation
├── hardware/                          # Hardware specifications
│   ├── bom-enterprise.md              # Enterprise BOM
│   ├── bom-smb.md                     # SMB BOM
│   └── bom-household.md               # Household BOM
└── examples/                          # Example configurations
    ├── retail-store/                  # Retail deployment
    ├── warehouse/                     # Warehouse deployment
    └── residential/                   # Home deployment
```

## Core Components

### Video Management System (VMS)
- **Frigate**: Primary VMS with AI integration
- **MediaMTX**: RTSP/WebRTC streaming server
- **FFmpeg**: Video processing and transcoding

### AI/Analytics
- **YOLOv8**: Real-time object detection
- **CompreFace**: Face recognition service
- **OpenCV**: Computer vision operations
- **TensorFlow Serving**: Custom model deployment

### Storage
- **PostgreSQL + TimescaleDB**: Metadata and time-series data
- **MinIO**: S3-compatible video archive storage
- **Redis**: Caching and real-time state
- **Ceph**: Distributed storage (optional, large scale)

### Messaging & Integration
- **NATS JetStream**: Internal event bus
- **Eclipse Mosquitto**: MQTT broker for IoT
- **Node-RED**: Visual workflow automation
- **Apache APISIX**: API gateway

### Edge Computing
- **K3s**: Lightweight Kubernetes for edge
- **EdgeX Foundry**: IoT edge framework
- **KubeEdge**: Cloud-edge coordination

### Observability
- **Grafana**: Dashboards and visualization
- **Prometheus**: Metrics collection
- **Loki**: Log aggregation
- **Jaeger**: Distributed tracing

### Security
- **Keycloak**: Identity and access management
- **Falco**: Runtime security monitoring
- **OPA**: Policy enforcement

### Digital Twin
- **Eclipse Ditto**: Digital twin framework
- **PostGIS**: Spatial database queries

## Documentation

### Getting Started
- [Installation Guide](docs/installation.md)
- [Configuration Guide](docs/configuration.md)
- [First Camera Setup](docs/quickstart-camera.md)

### Architecture
- [System Architecture](docs/architecture/overview.md)
- [Edge Architecture](docs/architecture/edge.md)
- [Cloud Architecture](docs/architecture/cloud.md)
- [Multi-Tenant Design](docs/architecture/multi-tenant.md)
- [Security Model](docs/architecture/security.md)

### Deployment
- [Enterprise Deployment](docs/deployment/enterprise.md)
- [SMB Deployment](docs/deployment/smb.md)
- [Household SaaS](docs/deployment/household.md)
- [Hardware Selection Guide](docs/deployment/hardware-guide.md)

### Development
- [Module Development Guide](docs/modules/development.md)
- [Custom Analytics Module](docs/modules/analytics.md)
- [IoT Integration Module](docs/modules/iot-integration.md)
- [API Reference](docs/api/reference.md)

### Hardware
- [Open Hardware Recommendations](docs/hardware/open-hardware.md)
- [Enterprise BOM](hardware/bom-enterprise.md)
- [Performance Benchmarks](docs/hardware/benchmarks.md)

## Module Ecosystem

### Built-in Modules
- **Person Detection**: Real-time person tracking
- **Vehicle Detection**: License plate recognition
- **Face Recognition**: Identity verification
- **Motion Zones**: Configurable detection zones
- **Perimeter Breach**: Boundary violation detection
- **Occupancy Counting**: Real-time people counting

### Example Custom Modules
- **Forklift Safety**: Industrial vehicle monitoring
- **PPE Detection**: Safety equipment compliance
- **Shelf Monitoring**: Retail stock tracking
- **Traffic Analysis**: Vehicle flow analytics
- **Crowd Density**: Public safety monitoring

### Development
Create your own modules using our [Module SDK](docs/modules/sdk.md):

```python
from openvision.sdk import AnalyticsModule

class CustomDetector(AnalyticsModule):
    def process_frame(self, frame, metadata):
        # Your detection logic
        detections = self.model.predict(frame)
        return self.format_results(detections)
```

Deploy as containerized microservice:
```bash
./scripts/deploy-module.sh custom-detector:v1.0
```

## Hardware Recommendations

### Edge Node Options

#### Budget (Household/SMB)
- **Raspberry Pi 5** (8GB): $80
- **Orange Pi 5 Plus** (16GB): $150
- **Google Coral TPU**: $60
- **Total**: ~$240 per edge node

#### Performance (Enterprise)
- **NVIDIA Jetson Orin Nano**: $500
- **Rock 5B** (16GB): $180
- **Hailo-8 AI Accelerator**: $70
- **Total**: ~$750 per edge node

#### High-End (Data Center Edge)
- **NVIDIA Jetson AGX Orin**: $2,000
- **2x 2TB NVMe SSD**: $300
- **10GbE NIC**: $200
- **Total**: ~$2,500 per edge node

### Central Server Options

#### SMB
- **System76 Thelio** or custom build
- AMD Ryzen 9, 64GB RAM
- 4x 4TB HDD (ZFS RAID 10)
- **Cost**: ~$2,000

#### Enterprise
- **2x System76 Thelio Major** or server-grade hardware
- AMD Threadripper or EPYC, 128GB RAM each
- 12x 18TB HDD per server
- **Cost**: ~$12,000 (2 servers)

### Camera Options

#### Open Hardware
- **OpenIPC-compatible cameras**: $30-50 each
- **ESP32-CAM modules**: $15 each (IoT sensors)

#### Quality Commercial
- **Hikvision/Dahua**: $80-200 each
- **Axis Communications**: $200-500 each (high-end)

Full hardware documentation: [docs/hardware/](docs/hardware/)

## Scaling Examples

### Household (1-5 cameras)
- **Hardware**: Raspberry Pi 4 + Coral TPU
- **Storage**: 500GB for 30 days retention
- **Cost**: ~$300 hardware + $10/month cloud (optional)

### Small Business (10-20 cameras)
- **Hardware**: Orange Pi 5 or cloud instance
- **Storage**: 4TB for 30 days retention
- **Cost**: ~$1,000 hardware + $50/month cloud

### Medium Enterprise (100 cameras, single site)
- **Hardware**: 1x Jetson Orin NX edge node, 1x server
- **Storage**: 40TB for 90 days retention
- **Cost**: ~$15,000 hardware

### Large Enterprise (500 cameras, 20 sites)
- **Hardware**: 20x edge nodes + central K8s cluster
- **Storage**: 200TB distributed
- **Cost**: ~$150,000 hardware

## SaaS Model

### Multi-Tenant Architecture
- Complete tenant isolation (namespace per customer)
- Shared infrastructure, isolated data
- Per-tenant resource quotas
- White-label UI capabilities

### Pricing Tiers

**Home Tier** ($9.99/month)
- Up to 5 cameras
- 7 days cloud storage
- Mobile app access
- Basic motion detection

**Business Tier** ($49.99/month)
- Up to 20 cameras
- 30 days cloud storage
- AI analytics (person/vehicle detection)
- Multi-user access
- API access

**Enterprise Tier** (Custom pricing)
- Unlimited cameras
- Custom retention
- Advanced AI modules
- Dedicated support
- On-premise option
- Custom integrations

### Deployment
SaaS version runs on Kubernetes with:
- Multi-region for low latency
- Auto-scaling based on camera count
- Automated backups
- 99.9% uptime SLA

See: [docs/deployment/saas.md](docs/deployment/saas.md)

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Areas Needing Contribution
- Additional IoT protocol support
- Mobile app improvements
- Hardware testing and benchmarks
- Documentation translations
- Custom analytics modules
- UI/UX enhancements

## Roadmap

### Current Version: 0.1.0-alpha

### Q1 2026
- [ ] Stable 1.0 release
- [ ] Mobile apps (iOS/Android)
- [ ] RISC-V hardware support
- [ ] Enhanced digital twin visualization

### Q2 2026
- [ ] Federated learning capabilities
- [ ] Blockchain audit trail
- [ ] Advanced multi-tenant features
- [ ] Marketplace for modules

### Q3 2026
- [ ] Edge AI model training
- [ ] 5G network optimization
- [ ] Enhanced privacy features (on-device processing)

## Community & Support

- **Documentation**: [docs.openvision.io](https://docs.openvision.io)
- **Forum**: [community.openvision.io](https://community.openvision.io)
- **Discord**: [discord.gg/openvision](https://discord.gg/openvision)
- **Issue Tracker**: [GitHub Issues](https://github.com/yourusername/openvision-platform/issues)
- **Commercial Support**: support@openvision.io

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

Core components may use compatible licenses (MIT, BSD, AGPL-3.0) - see individual component documentation.

## Acknowledgments

Built on the shoulders of giants:
- Frigate NVR team
- EdgeX Foundry community
- Eclipse Ditto project
- YOLO/Ultralytics team
- And hundreds of open-source contributors

## Security

Found a security vulnerability? Please email security@openvision.io instead of using the issue tracker.

See [SECURITY.md](SECURITY.md) for our security policy.

---

**Made with ❤️ by the open-source community**

⭐ Star us on GitHub if this project helps you!
