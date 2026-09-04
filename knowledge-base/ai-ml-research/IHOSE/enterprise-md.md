---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: ebe8d611-867a-46d4-8c46-761904bf6849
original_filename: enterprise.md
created_at: 2025-12-02T00:47:54.611595+00:00
content_hash: f073231f17bd
---

# Enterprise Deployment Guide

## Overview

This guide covers deploying OpenVision Platform at enterprise scale:
- **500+ cameras** across **20+ sites**
- **Central Kubernetes cluster** for management
- **Edge K3s nodes** at each site
- **Distributed storage** with Ceph
- **High availability** and **disaster recovery**

## Architecture Summary

```
Central Cloud (AWS/Azure/On-Prem)
├─ K8s Cluster (5 nodes minimum)
│  ├─ Control Plane (3 nodes)
│  └─ Worker Nodes (2+ nodes, auto-scaling)
├─ Ceph Storage Cluster (6+ nodes)
├─ PostgreSQL HA (3 nodes, streaming replication)
└─ Load Balancers (2+ nodes)

Edge Sites (20 locations)
├─ Site 1: 2x K3s nodes (25 cameras)
├─ Site 2: 2x K3s nodes (25 cameras)
└─ ... (repeat for each site)

Networking
├─ VPN Mesh (WireGuard or Tailscale)
├─ Private network between sites
└─ Public API endpoint (with WAF)
```

## Hardware Requirements

### Central Cloud

**Kubernetes Control Plane** (3 nodes):
- CPU: 8 cores per node
- RAM: 32GB per node
- Storage: 500GB SSD per node
- Network: 10 Gbps
- **Recommendation**: Bare metal or VM (avoid shared CPU)

**Kubernetes Worker Nodes** (start with 5, auto-scale):
- CPU: 16 cores per node
- RAM: 64GB per node
- Storage: 1TB NVMe SSD per node
- GPU: Optional (NVIDIA T4 for ML training)
- Network: 10 Gbps

**Ceph Storage Cluster** (6 nodes minimum):
- CPU: 8 cores per node
- RAM: 64GB per node
- Storage: 12x 18TB HDDs per node (216TB raw per node)
- NVMe: 2x 1TB for metadata/cache
- Network: 25 Gbps (dual NICs, separate storage network)

**PostgreSQL HA Cluster** (3 nodes):
- CPU: 16 cores per node
- RAM: 128GB per node
- Storage: 4TB NVMe SSD per node
- Network: 10 Gbps

**Total Central Cloud**:
- Servers: 17 nodes minimum
- Storage: ~1.2 PB raw (~800TB usable with 3x replication)
- Estimated cost: $150,000-200,000 hardware

### Edge Sites (per site, 25 cameras)

**Edge Nodes** (2 per site for HA):
- **Option A (Budget)**: Orange Pi 5 Plus + Hailo-8
  - Cost: ~$220 per node
  - Handles: 10-15 cameras with AI analytics
  
- **Option B (Performance)**: NVIDIA Jetson Orin Nano
  - Cost: ~$500 per node
  - Handles: 15-25 cameras with heavy AI

- **Option C (High-end)**: NVIDIA Jetson Orin NX
  - Cost: ~$800 per node
  - Handles: 20-30 cameras with complex AI

**Per-Site Storage**:
- 2x 4TB NVMe SSD (RAID 1 or distributed)
- Holds 7-14 days local retention
- Cost: ~$600

**Per-Site Network**:
- PoE Network Switch (24-48 ports)
- Cost: $300-500
- Router with VPN capability
- Cost: $100-200

**Cameras** (25 per site):
- OpenIPC cameras: $35-50 each = $875-1,250
- OR quality commercial: $80-200 each = $2,000-5,000

**Total Per Site**:
- Budget: ~$3,000-4,000
- Standard: ~$5,000-7,000
- High-end: ~$8,000-10,000

**20 Sites Total**: $60,000-200,000 depending on options

## Pre-Deployment Checklist

### Network Requirements
- [ ] VPN connectivity between all sites and central cloud
- [ ] Dedicated camera VLAN at each site
- [ ] 100 Mbps minimum internet at each edge site
- [ ] 10 Gbps between central cloud nodes
- [ ] DNS resolution configured
- [ ] NTP servers configured
- [ ] Firewall rules documented

### Access Requirements
- [ ] SSH access to all servers
- [ ] Root/sudo access
- [ ] Certificate authority for TLS certificates
- [ ] Cloud provider API keys (if using cloud)
- [ ] DNS management access

### Software Prerequisites
- [ ] Ubuntu 22.04 LTS on all nodes
- [ ] Docker installed on all nodes
- [ ] kubectl installed on management workstation
- [ ] Helm 3.x installed
- [ ] Ansible installed (for automation)

## Installation Steps

### Phase 1: Central Cloud Setup

#### Step 1.1: Provision Servers

**Using Terraform** (recommended):
```bash
cd deployment/terraform/enterprise/

# Configure variables
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars

# Set:
# region = "us-east-1"
# k8s_control_plane_count = 3
# k8s_worker_count = 5
# ceph_node_count = 6
# postgres_node_count = 3

# Provision infrastructure
terraform init
terraform plan
terraform apply
```

**Manual Provisioning**:
- Provision 17 servers with Ubuntu 22.04 LTS
- Configure networking (private IPs, subnets)
- Set up SSH key-based authentication
- Install basic tools (curl, wget, git)

#### Step 1.2: Install Kubernetes Cluster

**Using kubeadm**:
```bash
# On control plane node 1
sudo kubeadm init --control-plane-endpoint "k8s-api.yourdomain.com:6443" \
  --upload-certs \
  --pod-network-cidr=10.244.0.0/16

# Save the join command output!

# Install CNI (Calico recommended for network policies)
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml

# On control plane nodes 2 and 3
sudo kubeadm join k8s-api.yourdomain.com:6443 \
  --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash> \
  --control-plane --certificate-key <cert-key>

# On worker nodes 1-5
sudo kubeadm join k8s-api.yourdomain.com:6443 \
  --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash>

# Verify cluster
kubectl get nodes
# All nodes should show Ready
```

**Using RKE2** (alternative, simpler):
```bash
# Install on first server
curl -sfL https://get.rke2.io | sh -
systemctl enable rke2-server.service
systemctl start rke2-server.service

# Get token
cat /var/lib/rancher/rke2/server/node-token

# Join other servers
curl -sfL https://get.rke2.io | INSTALL_RKE2_TYPE="server" sh -
systemctl enable rke2-server.service

# Configure /etc/rancher/rke2/config.yaml
server: https://first-server:9345
token: <token-from-first-server>

systemctl start rke2-server.service
```

#### Step 1.3: Install Ceph Storage Cluster

**Using Rook**:
```bash
# Add Rook Helm repo
helm repo add rook-release https://charts.rook.io/release
helm repo update

# Install Rook Operator
kubectl create namespace rook-ceph
helm install --namespace rook-ceph rook-ceph rook-release/rook-ceph

# Wait for operator
kubectl -n rook-ceph get pod -w

# Configure Ceph cluster
kubectl apply -f - <<EOF
apiVersion: ceph.rook.io/v1
kind: CephCluster
metadata:
  name: rook-ceph
  namespace: rook-ceph
spec:
  cephVersion:
    image: quay.io/ceph/ceph:v17.2.6
  dataDirHostPath: /var/lib/rook
  mon:
    count: 3
  storage:
    useAllNodes: true
    useAllDevices: true
  dashboard:
    enabled: true
EOF

# Wait for Ceph cluster ready
kubectl -n rook-ceph get cephcluster -w

# Create storage class
kubectl apply -f deployment/kubernetes/storage/ceph-storageclass.yml
```

**Configure object storage (S3-compatible)**:
```bash
kubectl apply -f - <<EOF
apiVersion: ceph.rook.io/v1
kind: CephObjectStore
metadata:
  name: openvision-store
  namespace: rook-ceph
spec:
  metadataPool:
    replicated:
      size: 3
  dataPool:
    replicated:
      size: 3
  gateway:
    instances: 2
EOF
```

#### Step 1.4: Install PostgreSQL HA

**Using CloudNativePG operator**:
```bash
# Install operator
kubectl apply -f \
  https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/main/releases/cnpg-1.20.0.yaml

# Create PostgreSQL cluster
kubectl apply -f - <<EOF
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: openvision-postgres
  namespace: openvision
spec:
  instances: 3
  storage:
    size: 2Ti
    storageClass: ceph-block
  postgresql:
    parameters:
      max_connections: "1000"
      shared_buffers: "16GB"
      work_mem: "64MB"
  bootstrap:
    initdb:
      database: openvision
      owner: openvision
  monitoring:
    enabled: true
EOF

# Install TimescaleDB extension
kubectl exec -it openvision-postgres-1 -- psql -U postgres -d openvision \
  -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"
```

#### Step 1.5: Install Core Platform Services

**Create namespace and secrets**:
```bash
# Create namespace
kubectl create namespace openvision

# Create image pull secret (if using private registry)
kubectl create secret docker-registry regcred \
  --docker-server=registry.yourdomain.com \
  --docker-username=<username> \
  --docker-password=<password> \
  --namespace=openvision

# Create PostgreSQL credentials
kubectl create secret generic postgres-credentials \
  --from-literal=username=openvision \
  --from-literal=password=$(openssl rand -base64 32) \
  --namespace=openvision

# Create MinIO/S3 credentials
kubectl create secret generic s3-credentials \
  --from-literal=access-key=$(openssl rand -base64 16) \
  --from-literal=secret-key=$(openssl rand -base64 32) \
  --namespace=openvision

# Create JWT signing key
kubectl create secret generic jwt-signing-key \
  --from-literal=key=$(openssl rand -base64 64) \
  --namespace=openvision
```

**Deploy core services**:
```bash
# Deploy NATS
helm repo add nats https://nats-io.github.io/k8s/helm/charts/
helm install nats nats/nats \
  --namespace openvision \
  --set cluster.enabled=true \
  --set cluster.replicas=3 \
  --set natsbox.enabled=true

# Deploy Redis cluster
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install redis bitnami/redis-cluster \
  --namespace openvision \
  --set cluster.nodes=6 \
  --set cluster.replicas=1

# Deploy Mosquitto (MQTT)
kubectl apply -f deployment/kubernetes/core/mosquitto.yml

# Deploy Eclipse Ditto (Digital Twin)
kubectl apply -f deployment/kubernetes/core/ditto.yml

# Deploy Keycloak
helm install keycloak bitnami/keycloak \
  --namespace openvision \
  --set auth.adminUser=admin \
  --set auth.adminPassword=$(openssl rand -base64 16) \
  --set postgresql.enabled=false \
  --set externalDatabase.host=openvision-postgres-rw \
  --set externalDatabase.database=keycloak

# Deploy API Gateway (APISIX)
helm repo add apisix https://charts.apiseven.com
helm install apisix apisix/apisix \
  --namespace openvision \
  --set gateway.type=LoadBalancer \
  --set ingress-controller.enabled=true

# Deploy Grafana + Prometheus stack
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace openvision \
  --set grafana.enabled=true \
  --set prometheus.prometheusSpec.retention=90d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=500Gi
```

**Deploy OpenVision application services**:
```bash
# Deploy from manifests
kubectl apply -f deployment/kubernetes/core/vms-service.yml
kubectl apply -f deployment/kubernetes/core/analytics-service.yml
kubectl apply -f deployment/kubernetes/core/integration-service.yml
kubectl apply -f deployment/kubernetes/core/storage-service.yml
kubectl apply -f deployment/kubernetes/core/event-service.yml
kubectl apply -f deployment/kubernetes/core/workflow-service.yml
kubectl apply -f deployment/kubernetes/core/web-ui.yml

# Verify all pods running
kubectl get pods -n openvision
```

#### Step 1.6: Configure Ingress and TLS

```bash
# Install cert-manager for TLS certificates
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create ClusterIssuer for Let's Encrypt
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: admin@yourdomain.com
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

# Create Ingress
kubectl apply -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: openvision-ingress
  namespace: openvision
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
spec:
  tls:
  - hosts:
    - api.openvision.yourdomain.com
    - app.openvision.yourdomain.com
    secretName: openvision-tls
  rules:
  - host: api.openvision.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-gateway
            port:
              number: 80
  - host: app.openvision.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web-ui
            port:
              number: 80
EOF
```

### Phase 2: Edge Site Deployment

#### Step 2.1: Prepare Edge Nodes

**For each edge site** (automate with Ansible):

```bash
# SSH into edge node
ssh ubuntu@edge-site1-node1.yourdomain.com

# Install K3s
curl -sfL https://get.k3s.io | sh -s - \
  --disable traefik \
  --write-kubeconfig-mode 644

# Install k3s on second node (HA)
curl -sfL https://get.k3s.io | K3S_URL=https://first-node:6443 \
  K3S_TOKEN=<token-from-first-node> sh -

# Verify
sudo k3s kubectl get nodes
```

**Using Ansible** (recommended for 20 sites):
```bash
# Configure inventory
nano deployment/ansible/inventory/hosts.yml

# Set:
all:
  children:
    edge_sites:
      children:
        site_1:
          hosts:
            edge-site1-node1:
              ansible_host: 10.1.1.10
            edge-site1-node2:
              ansible_host: 10.1.1.11
        site_2:
          hosts:
            edge-site2-node1:
              ansible_host: 10.2.1.10
            edge-site2-node2:
              ansible_host: 10.2.1.11
        # ... repeat for all 20 sites

# Run playbook
ansible-playbook -i deployment/ansible/inventory/hosts.yml \
  deployment/ansible/playbooks/edge-setup.yml
```

#### Step 2.2: Deploy Edge Services

**Per edge site**:
```bash
# Create namespace
kubectl create namespace openvision-edge

# Deploy Frigate (VMS)
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frigate
  namespace: openvision-edge
spec:
  replicas: 1
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
        image: ghcr.io/blakeblackshear/frigate:stable
        ports:
        - containerPort: 5000
        - containerPort: 1935  # RTMP
        volumeMounts:
        - name: config
          mountPath: /config
        - name: media
          mountPath: /media
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
      volumes:
      - name: config
        configMap:
          name: frigate-config
      - name: media
        persistentVolumeClaim:
          claimName: frigate-media-pvc
EOF

# Deploy MediaMTX (RTSP server)
kubectl apply -f deployment/kubernetes/edge/mediamtx.yml

# Deploy YOLO analytics
kubectl apply -f deployment/kubernetes/edge/yolo-analytics.yml

# Deploy EdgeX Foundry (IoT)
kubectl apply -f deployment/kubernetes/edge/edgex.yml

# Deploy NATS leaf node (connects to central)
kubectl apply -f - <<EOF
apiVersion: v1
kind: ConfigMap
metadata:
  name: nats-config
  namespace: openvision-edge
data:
  nats.conf: |
    port: 4222
    leafnodes {
      remotes = [
        {
          url: "nats-leaf://nats.openvision.svc.cluster.local:7422"
        }
      ]
    }
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nats
  namespace: openvision-edge
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nats
  template:
    metadata:
      labels:
        app: nats
    spec:
      containers:
      - name: nats
        image: nats:latest
        args: ["-c", "/config/nats.conf"]
        volumeMounts:
        - name: config
          mountPath: /config
      volumes:
      - name: config
        configMap:
          name: nats-config
EOF
```

#### Step 2.3: Configure Cameras

**Create camera configuration**:
```yaml
# configs/cameras-site1.yml
cameras:
  front_entrance:
    ffmpeg:
      inputs:
        - path: rtsp://192.168.1.100:554/stream1
          roles:
            - detect
            - record
    detect:
      enabled: true
      width: 1920
      height: 1080
      fps: 5
    record:
      enabled: true
      retain:
        days: 14
        mode: motion
    objects:
      track:
        - person
        - car
      filters:
        person:
          min_area: 5000
          threshold: 0.7
  
  parking_lot_1:
    ffmpeg:
      inputs:
        - path: rtsp://192.168.1.101:554/stream1
          roles:
            - detect
            - record
    detect:
      enabled: true
      width: 2560
      height: 1440
      fps: 5
    record:
      enabled: true
      retain:
        days: 7
        mode: all  # 24/7 recording
    objects:
      track:
        - car
        - person
  
  # ... add all 25 cameras
```

**Apply configuration**:
```bash
kubectl create configmap frigate-config \
  --from-file=configs/cameras-site1.yml \
  --namespace=openvision-edge

# Restart Frigate to apply
kubectl rollout restart deployment/frigate -n openvision-edge
```

### Phase 3: Integration and Testing

#### Step 3.1: Connect Edge to Cloud

**Verify NATS connectivity**:
```bash
# From edge node
kubectl exec -it deploy/nats -n openvision-edge -- nats pub test.message "Hello from edge"

# From central cloud
kubectl exec -it nats-0 -n openvision -- nats sub "test.message"
# Should receive message
```

**Configure data sync**:
```bash
# Deploy sync service on edge
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloud-sync
  namespace: openvision-edge
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cloud-sync
  template:
    metadata:
      labels:
        app: cloud-sync
    spec:
      containers:
      - name: sync
        image: openvision/cloud-sync:latest
        env:
        - name: CLOUD_API
          value: "https://api.openvision.yourdomain.com"
        - name: SITE_ID
          value: "site_1"
        - name: SYNC_INTERVAL
          value: "60"  # seconds
EOF
```

#### Step 3.2: Configure Monitoring

**Deploy monitoring on edge**:
```bash
# Install Prometheus agent mode
helm install prometheus-agent prometheus-community/prometheus \
  --namespace openvision-edge \
  --set server.remoteWrite[0].url=https://prometheus.openvision.yourdomain.com/api/v1/write

# Install node-exporter
kubectl apply -f deployment/kubernetes/edge/node-exporter.yml

# Install cAdvisor for container metrics
kubectl apply -f deployment/kubernetes/edge/cadvisor.yml
```

**Configure alerts**:
```yaml
# configs/alerts-site1.yml
groups:
- name: cameras
  interval: 30s
  rules:
  - alert: CameraOffline
    expr: up{job="frigate-cameras"} == 0
    for: 5m
    annotations:
      summary: "Camera {{ $labels.camera_name }} offline"
    
  - alert: HighCPUUsage
    expr: rate(node_cpu_seconds_total{mode="idle"}[5m]) < 0.2
    for: 10m
    annotations:
      summary: "High CPU usage on {{ $labels.instance }}"
  
  - alert: LowDiskSpace
    expr: node_filesystem_avail_bytes{mountpoint="/media"} / node_filesystem_size_bytes{mountpoint="/media"} < 0.1
    for: 5m
    annotations:
      summary: "Low disk space on {{ $labels.instance }}"
```

#### Step 3.3: Security Hardening

**Network policies**:
```yaml
# deployment/kubernetes/security/network-policy.yml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: openvision
spec:
  podSelector: {}
  policyTypes:
  - Ingress
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-api-gateway
  namespace: openvision
spec:
  podSelector:
    matchLabels:
      app: api-gateway
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector: {}
    ports:
    - protocol: TCP
      port: 80
```

**Pod security policies**:
```yaml
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: restricted
spec:
  privileged: false
  allowPrivilegeEscalation: false
  requiredDropCapabilities:
    - ALL
  volumes:
    - 'configMap'
    - 'emptyDir'
    - 'projected'
    - 'secret'
    - 'downwardAPI'
    - 'persistentVolumeClaim'
  hostNetwork: false
  hostIPC: false
  hostPID: false
  runAsUser:
    rule: 'MustRunAsNonRoot'
  seLinux:
    rule: 'RunAsAny'
  fsGroup:
    rule: 'RunAsAny'
  readOnlyRootFilesystem: true
```

**Enable Falco (runtime security)**:
```bash
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm install falco falcosecurity/falco \
  --namespace falco --create-namespace \
  --set falcosidekick.enabled=true
```

### Phase 4: Production Cutover

#### Step 4.1: Data Migration

If migrating from existing system:
```bash
# Export existing recordings
./scripts/export-recordings.sh \
  --source old-nvr.yourdomain.com \
  --destination s3://openvision-archive/ \
  --date-range 2024-01-01:2024-11-19

# Import to new system
./scripts/import-recordings.sh \
  --source s3://openvision-archive/ \
  --site site_1
```

#### Step 4.2: Performance Testing

**Load test API**:
```bash
# Using k6
k6 run - <<EOF
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '5m', target: 100 },  // Ramp up
    { duration: '10m', target: 100 }, // Stay at 100 users
    { duration: '5m', target: 0 },    // Ramp down
  ],
};

export default function () {
  let res = http.get('https://api.openvision.yourdomain.com/api/v1/cameras');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });
  sleep(1);
}
EOF
```

**Test analytics throughput**:
```bash
# Simulate camera load
./scripts/analytics-load-test.sh \
  --cameras 500 \
  --duration 3600 \
  --fps 5
```

#### Step 4.3: User Training

- Schedule training sessions for security operators
- Provide documentation and video tutorials
- Set up test environment for practice
- Conduct mock incident response drills

#### Step 4.4: Go-Live Checklist

- [ ] All cameras online and recording
- [ ] Analytics modules producing results
- [ ] Alerts configured and tested
- [ ] Monitoring dashboards created
- [ ] Backup/restore tested
- [ ] Disaster recovery plan documented
- [ ] Security team trained
- [ ] Support escalation paths defined
- [ ] Performance baselines established
- [ ] Documentation complete

### Maintenance Operations

#### Backup and Restore

**PostgreSQL backup**:
```bash
# Automated daily backup
kubectl apply -f - <<EOF
apiVersion: batch/v1
kind: CronJob
metadata:
  name: postgres-backup
  namespace: openvision
spec:
  schedule: "0 2 * * *"  # 2 AM daily
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:15
            command:
            - /bin/bash
            - -c
            - |
              PGPASSWORD=\$POSTGRES_PASSWORD pg_dump \
                -h openvision-postgres-rw \
                -U openvision \
                -d openvision \
                | gzip > /backup/postgres-\$(date +%Y%m%d).sql.gz
              
              # Upload to S3
              aws s3 cp /backup/postgres-\$(date +%Y%m%d).sql.gz \
                s3://openvision-backups/postgres/
            volumeMounts:
            - name: backup
              mountPath: /backup
          volumes:
          - name: backup
            emptyDir: {}
          restartPolicy: OnFailure
EOF
```

**Video archive backup**:
```bash
# Ceph snapshots (automated)
kubectl apply -f - <<EOF
apiVersion: ceph.rook.io/v1
kind: CephBlockPoolSnapshot
metadata:
  name: daily-snapshot
  namespace: rook-ceph
spec:
  blockPoolName: openvision-pool
  schedule: "0 3 * * *"
  retention: 30
EOF
```

#### Scaling Operations

**Scale worker nodes**:
```bash
# Horizontal pod autoscaling
kubectl apply -f - <<EOF
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: analytics-hpa
  namespace: openvision
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: analytics-service
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
EOF

# Cluster autoscaling (cloud providers)
# Configure cluster autoscaler based on your cloud provider
```

#### Upgrade Procedures

**Rolling update**:
```bash
# Update application
kubectl set image deployment/vms-service \
  vms-service=openvision/vms-service:v2.0.0 \
  --namespace=openvision

# Monitor rollout
kubectl rollout status deployment/vms-service -n openvision

# Rollback if needed
kubectl rollout undo deployment/vms-service -n openvision
```

## Cost Analysis

### Hardware Costs (20 sites, 500 cameras)

**Central Cloud**: $180,000
- K8s cluster: $50,000
- Ceph storage: $100,000
- PostgreSQL cluster: $30,000

**Edge Sites** (20 × $6,000): $120,000
- Edge nodes: $1,000/site
- Storage: $600/site
- Cameras: $3,000/site
- Networking: $500/site

**Total Hardware**: ~$300,000

### Operational Costs (annual)

**Cloud Hosting** (if not on-prem):
- K8s managed service: $24,000/year
- Bandwidth: $12,000/year
- Storage: $6,000/year

**Maintenance**:
- Support staff: $120,000/year (2 engineers)
- Replacements/upgrades: $30,000/year

**Total Annual**: ~$190,000

### ROI Calculation

Compared to commercial solutions (Genetec, Milestone):
- Commercial licensing: $200-400 per camera = $100,000-200,000 initial
- Annual maintenance: 20% = $20,000-40,000/year
- Vendor lock-in, limited customization

**OpenVision Platform**:
- Initial: $300,000 (includes hardware)
- Annual: $50,000 (operational, excludes staff)
- Full customization, no licensing
- **Payback period**: 18-24 months

## Troubleshooting

### Common Issues

**Issue**: Camera won't connect
```bash
# Test RTSP stream
ffmpeg -i rtsp://camera-ip/stream1 -frames:v 1 test.jpg

# Check network connectivity
ping camera-ip
telnet camera-ip 554

# Verify Frigate logs
kubectl logs -n openvision-edge deployment/frigate
```

**Issue**: High CPU usage
```bash
# Check resource usage
kubectl top pods -n openvision

# Check analytics queue depth
kubectl exec -it deploy/analytics-service -n openvision -- \
  curl localhost:8080/metrics | grep queue_depth

# Scale up if needed
kubectl scale deployment/analytics-service --replicas=5 -n openvision
```

**Issue**: Storage full
```bash
# Check Ceph utilization
kubectl exec -it -n rook-ceph deploy/rook-ceph-tools -- ceph df

# Check retention policies
kubectl exec -it deploy/storage-service -n openvision -- \
  ./scripts/check-retention.sh

# Manually trigger cleanup
kubectl exec -it deploy/storage-service -n openvision -- \
  ./scripts/cleanup-old-recordings.sh --older-than 90
```

## Support

For enterprise support:
- Email: enterprise-support@openvision.io
- Phone: +1-555-0123 (24/7)
- Slack: openvision-enterprise.slack.com

---

**Next**: [Multi-Tenant SaaS Deployment](saas.md)
