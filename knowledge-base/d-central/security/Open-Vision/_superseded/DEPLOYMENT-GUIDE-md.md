---
source_project: Open Vision
source_project_uuid: 019adc89-3095-77fb-a6f8-3f599d84699a
doc_uuid: 7909414e-5d33-406f-952f-c8c2f9faa044
original_filename: DEPLOYMENT_GUIDE.md
created_at: 2025-12-02T00:49:42.058177+00:00
content_hash: 14499fa4188d
status: duplicate
duplicate_of: "knowledge-base/d-central/security/IHOSE/DEPLOYMENT-GUIDE-md.md"
duplicate_reason: exact content_hash match, different category (same doc uploaded to multiple Claude Projects)
---

# OpenVision Platform - Complete Deployment Guide

**Document Type**: Deployment Guide  
**Version**: 1.0  
**Audience**: IT Managers, System Administrators, DevOps Engineers

---

## Table of Contents

1. [Deployment Overview](#deployment-overview)
2. [Household Deployment (1-5 Cameras)](#household-deployment)
3. [Small Business Deployment (10-50 Cameras)](#small-business-deployment)
4. [Enterprise Deployment (500+ Cameras)](#enterprise-deployment)
5. [SaaS Multi-Tenant Deployment](#saas-multi-tenant-deployment)
6. [Troubleshooting](#troubleshooting)
7. [Maintenance Operations](#maintenance-operations)

---

## Deployment Overview

### Choosing Your Deployment

| Scale | Cameras | Investment | Timeline | Complexity |
|-------|---------|------------|----------|------------|
| **Household** | 1-5 | $300-500 | 2-4 hours | Low |
| **SMB** | 10-50 | $5K-15K | 1-2 days | Medium |
| **Enterprise** | 500+ | $200K-700K | 2-4 weeks | High |
| **SaaS** | Unlimited | $100K-300K | 4-8 weeks | High |

### Prerequisites - All Deployments

**Technical Skills**:
- Basic Linux command line
- Docker basics
- Networking fundamentals
- RTSP camera configuration

**Tools Required**:
- Linux distribution (Ubuntu 22.04 LTS recommended)
- Docker & Docker Compose
- SSH access to servers
- Text editor (nano, vim, or VS Code)

**Network Requirements**:
- Static IP addresses for servers
- DHCP reservations for cameras
- Separate VLAN for cameras (recommended)
- Internet access for updates

---

## Household Deployment

### Overview
**Perfect for**: Home security, vacation properties, small offices  
**Cameras**: 1-5  
**Cost**: $300-500  
**Timeline**: 2-4 hours  
**Hardware**: Raspberry Pi 4 or equivalent

### Hardware Shopping List

| Item | Specification | Quantity | Cost |
|------|---------------|----------|------|
| **Compute** | Raspberry Pi 4 (8GB) | 1 | $75 |
| **AI Accelerator** | Google Coral USB TPU | 1 | $60 |
| **Storage** | 500GB External SSD | 1 | $60 |
| **Power** | Official Pi Power Supply | 1 | $10 |
| **Case** | Aluminum case with fan | 1 | $15 |
| **Cameras** | 1080p IP Camera (ONVIF) | 3 | $120 |
| **Network** | Cat6 cables, PoE injectors | - | $60 |
| **Total** | | | **$400** |

Alternative: Use existing hardware (old PC, cloud VM)

### Step-by-Step Installation

#### 1. Prepare Raspberry Pi

```bash
# Flash Ubuntu Server 22.04 LTS to microSD card
# Use Raspberry Pi Imager: https://www.raspberrypi.com/software/

# Boot Pi and SSH in
ssh ubuntu@raspberrypi.local
# Default password: ubuntu (will be prompted to change)

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo apt install docker-compose -y

# Reboot
sudo reboot
```

#### 2. Mount External SSD

```bash
# Find the drive
lsblk

# Format as ext4 (assuming /dev/sda1)
sudo mkfs.ext4 /dev/sda1

# Create mount point
sudo mkdir -p /mnt/storage

# Add to /etc/fstab for auto-mount
echo "/dev/sda1 /mnt/storage ext4 defaults 0 2" | sudo tee -a /etc/fstab

# Mount
sudo mount -a

# Set permissions
sudo chown -R ubuntu:ubuntu /mnt/storage
```

#### 3. Download and Configure OpenVision

```bash
# Clone repository
cd ~
git clone https://github.com/openvision-platform/openvision.git
cd openvision

# Copy environment template
cp configs/env.household.example configs/.env

# Edit configuration
nano configs/.env

# Set these variables:
POSTGRES_PASSWORD=<generate-strong-password>
REDIS_PASSWORD=<generate-strong-password>
FRIGATE_RTSP_PASSWORD=<generate-strong-password>
```

#### 4. Configure Cameras

```bash
# Edit camera configuration
nano configs/frigate.yml

# Add your cameras:
cameras:
  front_door:
    ffmpeg:
      inputs:
        - path: rtsp://username:password@192.168.1.100:554/stream1
          roles: [detect, record]
    detect:
      enabled: true
      width: 1920
      height: 1080
      fps: 5
    record:
      enabled: true
      retain:
        days: 7
        mode: motion
    objects:
      track:
        - person
        - car
```

#### 5. Start Services

```bash
# Start OpenVision
docker-compose -f deployment/docker/household-stack.yml up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f frigate
```

#### 6. Access Web Interface

Open browser to: `http://raspberrypi.local:5000`

**Default Credentials**:
- Username: admin
- Password: (check configs/.env for FRIGATE_RTSP_PASSWORD)

### Mobile Access Setup

#### Option A: Tailscale VPN (Recommended)

```bash
# Install Tailscale on Pi
curl -fsSL https://tailscale.com/install.sh | sh

# Authenticate
sudo tailscale up

# Access from anywhere using Pi's Tailscale IP
# Install Tailscale app on phone
```

#### Option B: Port Forwarding

```
⚠️ Security Warning: Only do this if you understand the risks

1. Set static IP for Pi in router
2. Forward port 5000 to Pi's IP
3. Set strong password
4. Enable HTTPS (Let's Encrypt)
```

### Household Deployment - Complete!

✅ You should now have:
- Live camera feeds
- Motion detection recording
- 7 days retention
- Mobile access via VPN

---

## Small Business Deployment

### Overview
**Perfect for**: Retail stores, small offices, warehouses  
**Cameras**: 10-50  
**Cost**: $5,000-15,000  
**Timeline**: 1-2 days  
**Hardware**: Single server or cloud instance

### Hardware Options

#### Option A: On-Premise Server

| Item | Specification | Cost |
|------|---------------|------|
| **Server** | Dell PowerEdge T340 or equivalent | $2,500 |
| | - Intel Xeon E-2234 (4-core) | |
| | - 32GB RAM | |
| | - 2x 4TB HDD (RAID 1) | |
| | - 500GB SSD (boot) | |
| **Network** | 24-port PoE switch (Ubiquiti) | $500 |
| **Cameras** | 20x 4MP IP cameras | $2,000 |
| **Cabling** | Cat6 cables, labor | $1,500 |
| **UPS** | 1500VA UPS | $300 |
| **Total** | | **$6,800** |

#### Option B: Cloud Deployment

| Item | Specification | Monthly Cost |
|------|---------------|--------------|
| **Compute** | 4 vCPU, 16GB RAM | $80 |
| **Storage** | 2TB SSD | $200 |
| **Bandwidth** | 5TB egress | $50 |
| **Backup** | 500GB | $25 |
| **Total** | | **$355/month** |

**Note**: Cloud TCO over 3 years = $12,780 vs. $6,800 on-premise + $100/month power = $10,400

**Recommendation**: On-premise for 3+ year use, cloud for flexibility

### Step-by-Step Installation (On-Premise)

#### 1. Server Setup

```bash
# Install Ubuntu Server 22.04 LTS
# During installation:
# - Use entire disk for LVM
# - Install OpenSSH server
# - Create admin user

# After installation, SSH in
ssh admin@<server-ip>

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker admin

# Install Docker Compose
sudo apt install docker-compose -y

# Install additional tools
sudo apt install -y git curl wget htop
```

#### 2. Configure Storage

```bash
# Format data drives (assuming /dev/sdb, /dev/sdc)
sudo pvcreate /dev/sdb /dev/sdc
sudo vgcreate vg-data /dev/sdb /dev/sdc
sudo lvcreate -L 7TB -n lv-recordings vg-data
sudo mkfs.ext4 /dev/vg-data/lv-recordings

# Mount
sudo mkdir -p /mnt/recordings
echo "/dev/vg-data/lv-recordings /mnt/recordings ext4 defaults 0 2" | sudo tee -a /etc/fstab
sudo mount -a
```

#### 3. Deploy OpenVision Platform

```bash
# Clone repository
cd /opt
sudo git clone https://github.com/openvision-platform/openvision.git
sudo chown -R admin:admin openvision
cd openvision

# Generate configuration
./scripts/generate-config.sh --scale smb

# Edit configuration
nano configs/.env

# Critical settings:
POSTGRES_PASSWORD=<generated>
REDIS_PASSWORD=<generated>
S3_SECRET_KEY=<generated>
DOMAIN=cctv.yourcompany.com
RETENTION_CONTINUOUS_DAYS=30
RETENTION_EVENTS_DAYS=90
```

#### 4. Configure Cameras

```bash
# Edit camera configuration
nano configs/frigate.yml

# Template for 20 cameras:
cameras:
  # Front entrance
  cam_front_01:
    ffmpeg:
      inputs:
        - path: rtsp://admin:password@192.168.10.101:554/stream1
          roles: [detect, record]
    detect:
      enabled: true
      width: 2560
      height: 1440
      fps: 5
    record:
      enabled: true
      retain:
        days: 30
        mode: motion
    objects:
      track: [person, car, truck]
  
  # Repeat for cam_front_02 through cam_storage_20
  # Tip: Use a script to generate this configuration
```

#### 5. Start Services

```bash
# Start all services
docker-compose -f deployment/docker/core-stack.yml up -d

# Check status (all should show "healthy" or "running")
docker-compose ps

# View startup logs
docker-compose logs -f

# Wait for services to initialize (~2 minutes)
```

#### 6. Initial Configuration

```bash
# Access web interface
# http://<server-ip> or https://cctv.yourcompany.com

# Log in with default credentials
# Username: admin
# Password: (from configs/.env - KEYCLOAK_ADMIN_PASSWORD)

# Configure:
# 1. Change admin password
# 2. Create user accounts
# 3. Set up detection zones
# 4. Configure alerts
# 5. Test recording and playback
```

#### 7. Network Configuration

```bash
# Set up reverse proxy with SSL (optional but recommended)
sudo apt install nginx certbot python3-certbot-nginx

# Create Nginx config
sudo nano /etc/nginx/sites-available/openvision

# Content:
server {
    listen 80;
    server_name cctv.yourcompany.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}

# Enable site
sudo ln -s /etc/nginx/sites-available/openvision /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Get SSL certificate
sudo certbot --nginx -d cctv.yourcompany.com
```

### Monitoring Setup

```bash
# Access Grafana
# http://<server-ip>:3000

# Login:
# Username: admin
# Password: (from configs/.env - GRAFANA_ADMIN_PASSWORD)

# Import dashboards:
# 1. OpenVision Overview
# 2. Camera Health
# 3. Storage Usage
# 4. Analytics Performance
```

### Small Business Deployment - Complete!

✅ You should now have:
- 20-50 cameras recording
- 30-90 day retention
- AI analytics running
- Web and mobile access
- Monitoring dashboards
- Automated backups

---

## Enterprise Deployment

### Overview
**Perfect for**: Campuses, airports, large facilities  
**Cameras**: 500+  
**Sites**: 20+  
**Cost**: $200,000-700,000  
**Timeline**: 2-4 weeks  
**Architecture**: Central Kubernetes cluster + edge nodes

### High-Level Architecture

```
Central Cloud (Kubernetes)
├─ Management plane
├─ Long-term storage (Ceph)
├─ Cross-site analytics
└─ User management

20x Edge Sites
├─ K3s cluster (2 nodes per site)
├─ Local recording (14 days)
├─ Real-time analytics
└─ 25 cameras per site
```

### Phase 1: Planning (Week 1)

#### Hardware Procurement

See detailed BOM: `/hardware/ENTERPRISE_BOM.md`

**Central Cloud** (~$120,000):
- 3x Control plane nodes
- 5x Worker nodes
- 6x Ceph storage nodes
- 3x PostgreSQL nodes
- Networking equipment

**Edge Sites** (~$6,000/site × 20 = $120,000):
- 2x Edge compute nodes (Jetson or Orange Pi)
- 1x 24-port PoE switch
- 1x Router
- 25x IP cameras
- Cabling and installation

**Total Hardware**: ~$240,000

#### Network Planning

**Requirements**:
- 100 Mbps+ internet per site
- VPN mesh between sites
- Dedicated camera VLAN
- Management VLAN
- DNS infrastructure

**IP Addressing Scheme**:
```
Central Cloud: 10.0.0.0/16
Site 1: 10.1.0.0/16
  - Cameras: 10.1.10.0/24
  - Edge nodes: 10.1.20.0/24
  - Management: 10.1.30.0/24
Site 2: 10.2.0.0/16
  ...
Site 20: 10.20.0.0/16
```

#### Team Preparation

**Required Roles**:
- Project Manager
- Kubernetes Administrator
- Network Engineer
- Security Engineer
- Application Administrator
- Field Technicians (for camera installation)

### Phase 2: Central Cloud Setup (Week 1-2)

#### 1. Kubernetes Cluster Installation

**Control Plane Setup** (3 nodes):

```bash
# On first control plane node
sudo kubeadm init \
  --control-plane-endpoint "k8s-api.company.com:6443" \
  --upload-certs \
  --pod-network-cidr=10.244.0.0/16

# Save the join commands output!

# Install CNI (Calico)
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

# On second and third control plane nodes
sudo kubeadm join k8s-api.company.com:6443 \
  --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash> \
  --control-plane \
  --certificate-key <cert-key>

# Verify
kubectl get nodes
# All should show STATUS: Ready
```

**Worker Nodes** (5 nodes):

```bash
# On each worker node
sudo kubeadm join k8s-api.company.com:6443 \
  --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash>

# Verify from control plane
kubectl get nodes
# Should show 8 nodes total (3 control, 5 workers)
```

#### 2. Ceph Storage Cluster

**Using Rook Operator**:

```bash
# Add Rook Helm repo
helm repo add rook-release https://charts.rook.io/release
helm repo update

# Install Rook Operator
kubectl create namespace rook-ceph
helm install --namespace rook-ceph rook-ceph rook-release/rook-ceph

# Wait for operator
kubectl -n rook-ceph get pod -w

# Deploy Ceph cluster
kubectl apply -f deployment/kubernetes/storage/ceph-cluster.yml

# Wait for Ceph ready (~10 minutes)
kubectl -n rook-ceph get cephcluster

# Create storage classes
kubectl apply -f deployment/kubernetes/storage/ceph-storageclass.yml

# Verify
kubectl get sc
```

**Create Object Storage**:

```bash
# Deploy object store
kubectl apply -f deployment/kubernetes/storage/ceph-objectstore.yml

# Get S3 credentials
kubectl -n rook-ceph get secret rook-ceph-object-user-openvision-store -o jsonpath='{.data.AccessKey}' | base64 --decode
kubectl -n rook-ceph get secret rook-ceph-object-user-openvision-store -o jsonpath='{.data.SecretKey}' | base64 --decode

# Save these credentials!
```

#### 3. PostgreSQL HA

**Using CloudNativePG**:

```bash
# Install operator
kubectl apply -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/main/releases/cnpg-1.20.0.yaml

# Deploy PostgreSQL cluster
kubectl apply -f deployment/kubernetes/data/postgres-cluster.yml

# Wait for ready
kubectl get cluster -n openvision

# Install TimescaleDB extension
kubectl exec -it openvision-postgres-1 -n openvision -- \
  psql -U postgres -d openvision \
  -c "CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;"
```

#### 4. Deploy Core Services

```bash
# Create namespace
kubectl create namespace openvision

# Create secrets
./scripts/create-k8s-secrets.sh

# Deploy infrastructure services
kubectl apply -f deployment/kubernetes/core/nats.yml
kubectl apply -f deployment/kubernetes/core/redis.yml
kubectl apply -f deployment/kubernetes/core/mosquitto.yml

# Deploy application services
kubectl apply -f deployment/kubernetes/core/vms-service.yml
kubectl apply -f deployment/kubernetes/core/analytics-service.yml
kubectl apply -f deployment/kubernetes/core/storage-service.yml
kubectl apply -f deployment/kubernetes/core/event-service.yml
kubectl apply -f deployment/kubernetes/core/api-gateway.yml

# Deploy auth and UI
kubectl apply -f deployment/kubernetes/core/keycloak.yml
kubectl apply -f deployment/kubernetes/core/web-ui.yml

# Verify all pods running
kubectl get pods -n openvision -w
```

#### 5. Configure Ingress

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create cluster issuer
kubectl apply -f deployment/kubernetes/network/letsencrypt-issuer.yml

# Create ingress
kubectl apply -f deployment/kubernetes/network/ingress.yml

# Wait for certificate
kubectl get certificate -n openvision -w
```

### Phase 3: Edge Site Deployment (Week 2-3)

**For Each Site** (can be parallelized with field teams):

#### 1. Prepare Edge Nodes

```bash
# SSH into edge node 1
ssh admin@site1-edge1.company.com

# Install K3s (first node)
curl -sfL https://get.k3s.io | sh -s - \
  --write-kubeconfig-mode 644 \
  --disable traefik

# Get token
sudo cat /var/lib/rancher/k3s/server/node-token

# On edge node 2 (HA)
curl -sfL https://get.k3s.io | K3S_URL=https://site1-edge1:6443 \
  K3S_TOKEN=<token> sh -

# Verify
kubectl get nodes
```

#### 2. Deploy Edge Services

```bash
# Create namespace
kubectl create namespace openvision-edge

# Deploy Frigate
kubectl apply -f deployment/kubernetes/edge/frigate.yml

# Deploy MediaMTX
kubectl apply -f deployment/kubernetes/edge/mediamtx.yml

# Deploy analytics
kubectl apply -f deployment/kubernetes/edge/yolo-analytics.yml

# Deploy NATS (leaf node to central)
kubectl apply -f deployment/kubernetes/edge/nats-leaf.yml

# Deploy EdgeX Foundry (IoT)
kubectl apply -f deployment/kubernetes/edge/edgex.yml
```

#### 3. Configure Site Cameras

```bash
# Generate camera config (25 cameras per site)
./scripts/generate-camera-config.sh \
  --site site1 \
  --camera-count 25 \
  --start-ip 10.1.10.101

# Apply configuration
kubectl create configmap frigate-config \
  --from-file=configs/cameras-site1.yml \
  --namespace=openvision-edge

# Restart Frigate
kubectl rollout restart deployment/frigate -n openvision-edge
```

#### 4. Verify Site Operation

```bash
# Check all pods running
kubectl get pods -n openvision-edge

# Check camera connectivity
kubectl logs deployment/frigate -n openvision-edge | grep "camera"

# Test recording
# Access Frigate UI: http://site1-edge1.company.local:5000

# Verify cloud connection
kubectl logs deployment/cloud-sync -n openvision-edge
```

### Phase 4: Integration & Testing (Week 3-4)

#### 1. Verify Central Management

```bash
# Access central management UI
# https://openvision.company.com

# Verify:
# ✓ All 20 sites visible
# ✓ All 500 cameras online
# ✓ Recording status green
# ✓ Analytics running
# ✓ Storage usage tracking
```

#### 2. Configure Monitoring

```bash
# Deploy Prometheus stack
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace openvision \
  --values deployment/kubernetes/monitoring/values.yml

# Import dashboards
kubectl apply -f deployment/kubernetes/monitoring/dashboards/
```

#### 3. Set Up Alerting

```bash
# Configure alert rules
kubectl apply -f deployment/kubernetes/monitoring/alerts/

# Configure alert channels (Slack, email, PagerDuty)
kubectl apply -f deployment/kubernetes/monitoring/alertmanager-config.yml
```

#### 4. Load Testing

```bash
# Test API performance
k6 run tests/load/api-load-test.js

# Test video streaming
./scripts/test-streaming-performance.sh --cameras 500

# Test analytics throughput
./scripts/test-analytics-load.sh --streams 500
```

#### 5. Disaster Recovery Test

```bash
# Simulate node failure
kubectl drain <node-name> --ignore-daemonsets

# Verify auto-recovery
# - Pods rescheduled to other nodes
# - No camera downtime
# - Recordings continue

# Simulate site network failure
# - Edge site continues local operation
# - Central management shows "degraded"
# - Site recovers when network restored

# Uncordon node
kubectl uncordon <node-name>
```

### Phase 5: Production Cutover (Week 4)

#### 1. User Training

```
- Security operators (4 hours)
- IT administrators (8 hours)
- Management overview (2 hours)
```

#### 2. Documentation Handover

```
- System architecture
- Runbooks for common tasks
- Troubleshooting guides
- Emergency contacts
- Escalation procedures
```

#### 3. Go-Live Checklist

```
✓ All cameras recording
✓ Analytics producing results
✓ Alerts configured and tested
✓ Monitoring dashboards active
✓ Backup/restore tested
✓ DR plan documented
✓ Team trained
✓ Support contracts in place
✓ Performance baselines established
```

### Enterprise Deployment - Complete!

✅ You should now have:
- 500+ cameras across 20 sites
- Central management and monitoring
- 90-day retention
- Real-time AI analytics
- High availability
- Disaster recovery
- 24/7 monitoring and alerting

---

## SaaS Multi-Tenant Deployment

### Overview
**Perfect for**: Security companies, MSPs, property management  
**Scale**: Unlimited customers  
**Cost**: $100K-300K initial platform  
**Revenue**: $10-50/camera/month  
**Architecture**: Multi-region Kubernetes with tenant isolation

### Multi-Tenancy Design

**Tenant Isolation**:
```
Namespace per Tenant:
├─ openvision-tenant-001
│  ├─ VMS pods
│  ├─ Analytics pods
│  ├─ Storage quota (1TB)
│  └─ Network policies
├─ openvision-tenant-002
└─ ...

Shared Services:
├─ openvision-shared
   ├─ Keycloak (multi-tenant)
   ├─ API Gateway
   ├─ Billing service
   └─ Monitoring
```

### Implementation Steps

#### 1. Platform Setup

```bash
# Install Kubernetes cluster (managed service recommended)
# AWS EKS, Google GKE, or Azure AKS

# Install tenant operator
kubectl apply -f deployment/kubernetes/saas/tenant-operator.yml

# Configure default resource quotas
kubectl apply -f deployment/kubernetes/saas/resource-quotas.yml
```

#### 2. Tenant Provisioning

```bash
# Create new tenant
./scripts/create-tenant.sh \
  --name "Acme Corp" \
  --plan business \
  --max-cameras 50 \
  --storage-gb 1000

# This creates:
# - Namespace: openvision-tenant-<id>
# - Resource quotas
# - Network policies
# - Storage class
# - Keycloak realm
# - Database schema
```

#### 3. Billing Integration

```bash
# Configure Stripe
kubectl create secret generic stripe-credentials \
  --from-literal=secret-key=<stripe-secret> \
  --namespace=openvision-billing

# Deploy billing service
kubectl apply -f deployment/kubernetes/saas/billing-service.yml
```

#### 4. Self-Service Portal

```bash
# Deploy customer portal
kubectl apply -f deployment/kubernetes/saas/customer-portal.yml

# Features:
# - Sign up / onboarding
# - Camera management
# - Billing / invoices
# - Usage dashboard
# - Support tickets
```

### SaaS Deployment - Complete!

✅ Platform ready for customers

---

## Troubleshooting

### Common Issues

#### Camera Won't Connect

```bash
# Test RTSP stream
ffmpeg -i rtsp://camera-ip/stream1 -frames:v 1 test.jpg

# Check network connectivity
ping camera-ip
telnet camera-ip 554

# Verify credentials
# Check Frigate logs
docker-compose logs frigate | grep camera-name
```

#### High CPU Usage

```bash
# Check resource usage
docker stats
# or
kubectl top pods -n openvision

# Reduce analytics load
# Edit configs/frigate.yml
# Increase frame_skip from 5 to 10
# Reduce detection FPS

# Scale up resources
docker-compose up -d --scale analytics-service=3
```

#### Storage Full

```bash
# Check storage usage
df -h /mnt/recordings

# Manual cleanup (be careful!)
./scripts/cleanup-old-recordings.sh --older-than 60

# Adjust retention policy
# Edit configs/.env
RETENTION_CONTINUOUS_DAYS=7
RETENTION_EVENTS_DAYS=30

# Restart services
docker-compose restart storage-service
```

#### Service Won't Start

```bash
# Check logs
docker-compose logs <service-name>

# Common fixes:
# 1. Port conflict
sudo netstat -tulpn | grep <port>

# 2. Permission issue
sudo chown -R <user>:<group> /path/to/data

# 3. Resource exhaustion
free -h
df -h

# 4. Config error
docker-compose config
```

---

## Maintenance Operations

### Daily Tasks

```bash
# Check system health
./scripts/health-check.sh

# Review alerts (if any)
docker-compose logs --since 24h | grep -i error

# Verify backups completed
ls -lah /backups/
```

### Weekly Tasks

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Review storage usage
./scripts/storage-report.sh

# Test backup restore
./scripts/test-restore.sh

# Review access logs
./scripts/audit-report.sh --last-week
```

### Monthly Tasks

```bash
# Update Docker images
docker-compose pull
docker-compose up -d

# Review and optimize database
docker-compose exec postgres psql -U openvision -c "VACUUM ANALYZE;"

# Review retention policies
./scripts/retention-analysis.sh

# Security audit
./scripts/security-scan.sh
```

### Backup Procedures

```bash
# Manual backup
./scripts/backup-now.sh

# Automated daily backup (cron)
0 2 * * * /opt/openvision/scripts/backup-automated.sh

# Verify backups
./scripts/verify-backup.sh --backup-id <id>

# Restore from backup
./scripts/restore-from-backup.sh \
  --backup-id <id> \
  --restore-date 2024-11-19
```

---

## Next Steps After Deployment

1. **Optimize**: Monitor performance, adjust resources
2. **Customize**: Add custom analytics modules
3. **Integrate**: Connect with other systems
4. **Train**: Ensure all users comfortable with system
5. **Document**: Keep deployment docs updated

---

**Need Help?**
- Documentation: https://docs.openvision.io
- Community: https://community.openvision.io
- Commercial Support: support@openvision.io

**Document Version**: 1.0  
**Last Updated**: November 2024


<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Duplicate of:** [[knowledge-base/d-central/security/IHOSE/DEPLOYMENT-GUIDE-md]]

<!-- AUTO-GENERATED RELATED END -->
