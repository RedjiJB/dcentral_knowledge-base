---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: c8e7d188-0e8f-4e67-b185-1548997a2e46
original_filename: 04-Enterprise-Deployment.md
created_at: 2025-12-02T00:47:55.903097+00:00
content_hash: 2ef2b76fd7f9
topic: ihose-deployment-infrastructure
topic: "ihose-openvision-documentation-package"
---

# OpenVision Platform
## Enterprise Deployment Guide

**Version:** 1.0  
**Audience:** DevOps, SRE, System Administrators  
**Deployment:** 500 Cameras, 20 Sites, High Availability

---

## Table of Contents
1. [Deployment Overview](#deployment-overview)
2. [Prerequisites](#prerequisites)
3. [Central Cloud Setup](#central-cloud-setup)
4. [Edge Site Deployment](#edge-site-deployment)
5. [Network Configuration](#network-configuration)
6. [Security Hardening](#security-hardening)
7. [Monitoring & Operations](#monitoring--operations)
8. [Disaster Recovery](#disaster-recovery)

---

## Deployment Overview

### Target Architecture

**Central Cloud:**
- Kubernetes cluster (5+ nodes)
- Ceph storage cluster (6 nodes, 1.2 PB raw)
- PostgreSQL HA (3 nodes)
- Management services

**Edge Sites (20 locations):**
- 2x K3s nodes per site (HA)
- Local storage (14-day retention)
- 25 cameras per site
- Edge analytics

**Total Scale:**
- 500 cameras
- 20 edge sites
- 40 edge compute nodes
- 17 central servers
- ~1 PB usable storage

### Deployment Timeline

| Phase | Duration | Description |
|-------|----------|-------------|
| **Phase 1:** Infrastructure | Week 1-2 | Provision hardware, network |
| **Phase 2:** Central Cloud | Week 3-4 | Deploy K8s, Ceph, PostgreSQL |
| **Phase 3:** Core Services | Week 5-6 | Deploy platform services |
| **Phase 4:** Edge Sites | Week 7-10 | Deploy edge nodes, cameras |
| **Phase 5:** Testing | Week 11-12 | Integration, load, security testing |
| **Phase 6:** Production | Week 13-14 | Go-live, documentation, training |

**Total:** 14 weeks (3.5 months)

---

## Prerequisites

### Hardware Requirements

**Central Cloud (Minimum):**
- 3x Control plane nodes (8 cores, 32GB RAM, 500GB SSD each)
- 5x Worker nodes (16 cores, 64GB RAM, 1TB NVMe each)
- 6x Storage nodes (8 cores, 64GB RAM, 12x 18TB HDD + 2x 1TB NVMe each)
- 3x PostgreSQL nodes (12 cores, 128GB RAM, 4TB NVMe each)
- 2x Load balancer appliances
- 2x 48-port 10GbE switches
- 2x 24-port 25GbE switches (Ceph network)

**Per Edge Site:**
- 2x Compute nodes (Jetson Orin Nano or Orange Pi 5 Plus)
- 1x NAS (4x 8TB HDDs)
- 1x PoE switch (48-port)
- 1x Router with VPN
- 25x IP cameras

### Network Requirements

**Central Cloud:**
- 10 Gbps internal network
- 25 Gbps storage network (Ceph)
- 1 Gbps internet connection
- Static IP addresses
- DNS management

**Edge Sites:**
- 100 Mbps internet minimum
- Gigabit internal network
- VPN to central cloud
- Static IP or DDNS

### Software Prerequisites

**Management Workstation:**
- Ubuntu 22.04 LTS or macOS
- kubectl 1.28+
- Helm 3.x
- Ansible 2.14+
- Terraform 1.5+ (optional)
- SSH key-based authentication

**All Nodes:**
- Ubuntu 22.04 LTS (minimal install)
- SSH enabled
- Root/sudo access
- NTP configured
- Firewall disabled (will configure later)

---

## Central Cloud Setup

### Step 1: Provision Infrastructure

#### Option A: Using Terraform

```bash
cd deployment/terraform/enterprise/

# Configure variables
cp terraform.tfvars.example terraform.tfvars
nano terraform.tfvars

# Set:
# cloud_provider = "aws"  # or "azure", "gcp", "baremetal"
# region = "us-east-1"
# k8s_nodes = 8
# ceph_nodes = 6
# postgres_nodes = 3

# Provision
terraform init
terraform plan
terraform apply
```

#### Option B: Manual Provisioning

Install Ubuntu 22.04 LTS on all servers, then:

```bash
# On all nodes
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git vim htop

# Disable swap (required for Kubernetes)
sudo swapoff -a
sudo sed -i '/ swap / s/^/#/' /etc/fstab

# Configure hostname
sudo hostnamectl set-hostname k8s-control-1
# Repeat for each node with appropriate name

# Add hosts file entries
sudo nano /etc/hosts
# Add all cluster nodes:
# 10.0.1.10 k8s-control-1
# 10.0.1.11 k8s-control-2
# 10.0.1.12 k8s-control-3
# ...
```

### Step 2: Install Kubernetes Cluster

#### Using kubeadm (Production)

**On first control plane node:**

```bash
# Install containerd
sudo apt install -y containerd

# Configure containerd
sudo mkdir -p /etc/containerd
containerd config default | sudo tee /etc/containerd/config.toml
sudo sed -i 's/SystemdCgroup = false/SystemdCgroup = true/' /etc/containerd/config.toml
sudo systemctl restart containerd

# Install kubeadm, kubelet, kubectl
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list

sudo apt update
sudo apt install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

# Initialize cluster
sudo kubeadm init \
  --control-plane-endpoint "k8s-api.openvision.local:6443" \
  --upload-certs \
  --pod-network-cidr=10.244.0.0/16 \
  --service-cidr=10.96.0.0/16

# Save join commands from output!

# Configure kubectl for root user
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# Install Calico CNI
kubectl apply -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.0/manifests/calico.yaml

# Verify
kubectl get nodes
kubectl get pods -n kube-system
```

**On additional control plane nodes:**

```bash
# Use the control plane join command from above
sudo kubeadm join k8s-api.openvision.local:6443 \
  --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash> \
  --control-plane --certificate-key <cert-key>
```

**On worker nodes:**

```bash
# Use the worker join command from above
sudo kubeadm join k8s-api.openvision.local:6443 \
  --token <token> \
  --discovery-token-ca-cert-hash sha256:<hash>
```

#### Using RKE2 (Simpler Alternative)

**On first server:**

```bash
curl -sfL https://get.rke2.io | sh -
sudo systemctl enable rke2-server.service
sudo systemctl start rke2-server.service

# Get token
cat /var/lib/rancher/rke2/server/node-token

# Configure kubectl
mkdir -p ~/.kube
sudo cp /etc/rancher/rke2/rke2.yaml ~/.kube/config
sudo chown $(id -u):$(id -g) ~/.kube/config
export KUBECONFIG=~/.kube/config
```

**On additional servers:**

```bash
curl -sfL https://get.rke2.io | INSTALL_RKE2_TYPE="server" sh -
sudo mkdir -p /etc/rancher/rke2
sudo cat > /etc/rancher/rke2/config.yaml <<EOF
server: https://first-server:9345
token: <token-from-first-server>
EOF

sudo systemctl enable rke2-server.service
sudo systemctl start rke2-server.service
```

### Step 3: Deploy Ceph Storage

**Using Rook Operator:**

```bash
# Add Rook Helm repo
helm repo add rook-release https://charts.rook.io/release
helm repo update

# Install Rook operator
kubectl create namespace rook-ceph
helm install --namespace rook-ceph rook-ceph rook-release/rook-ceph

# Wait for operator
kubectl -n rook-ceph get pod -w

# Deploy Ceph cluster
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
    allowMultiplePerNode: false
  mgr:
    count: 2
  dashboard:
    enabled: true
    ssl: true
  storage:
    useAllNodes: true
    useAllDevices: true
    config:
      osdsPerDevice: "1"
  healthCheck:
    daemonHealth:
      mon:
        interval: 45s
EOF

# Wait for cluster ready (10-15 minutes)
kubectl -n rook-ceph get cephcluster -w

# Create block storage class
kubectl apply -f - <<EOF
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: ceph-block
provisioner: rook-ceph.rbd.csi.ceph.com
parameters:
  clusterID: rook-ceph
  pool: replicapool
  imageFormat: "2"
  imageFeatures: layering
  csi.storage.k8s.io/provisioner-secret-name: rook-csi-rbd-provisioner
  csi.storage.k8s.io/provisioner-secret-namespace: rook-ceph
  csi.storage.k8s.io/controller-expand-secret-name: rook-csi-rbd-provisioner
  csi.storage.k8s.io/controller-expand-secret-namespace: rook-ceph
  csi.storage.k8s.io/node-stage-secret-name: rook-csi-rbd-node
  csi.storage.k8s.io/node-stage-secret-namespace: rook-ceph
  csi.storage.k8s.io/fstype: ext4
allowVolumeExpansion: true
reclaimPolicy: Delete
EOF

# Verify Ceph status
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph status
```

**Create Object Storage (S3):**

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
  preservePoolsOnDelete: true
  gateway:
    instances: 2
    port: 80
    resources:
      limits:
        cpu: "2000m"
        memory: "2Gi"
      requests:
        cpu: "1000m"
        memory: "1Gi"
EOF

# Create S3 user
kubectl apply -f - <<EOF
apiVersion: ceph.rook.io/v1
kind: CephObjectStoreUser
metadata:
  name: openvision-user
  namespace: rook-ceph
spec:
  store: openvision-store
  displayName: "OpenVision S3 User"
EOF

# Get access credentials
kubectl -n rook-ceph get secret rook-ceph-object-user-openvision-store-openvision-user -o jsonpath='{.data.AccessKey}' | base64 -d
kubectl -n rook-ceph get secret rook-ceph-object-user-openvision-store-openvision-user -o jsonpath='{.data.SecretKey}' | base64 -d
```

### Step 4: Deploy PostgreSQL HA Cluster

**Using CloudNativePG:**

```bash
# Install operator
kubectl apply -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/main/releases/cnpg-1.22.0.yaml

# Create namespace
kubectl create namespace openvision

# Deploy cluster
kubectl apply -f - <<EOF
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: openvision-postgres
  namespace: openvision
spec:
  instances: 3
  primaryUpdateStrategy: unsupervised
  
  storage:
    size: 2Ti
    storageClass: ceph-block
  
  postgresql:
    parameters:
      max_connections: "1000"
      shared_buffers: "16GB"
      effective_cache_size: "48GB"
      maintenance_work_mem: "2GB"
      checkpoint_completion_target: "0.9"
      wal_buffers: "16MB"
      default_statistics_target: "100"
      random_page_cost: "1.1"
      effective_io_concurrency: "200"
      work_mem: "64MB"
      min_wal_size: "1GB"
      max_wal_size: "4GB"
  
  bootstrap:
    initdb:
      database: openvision
      owner: openvision
      secret:
        name: postgres-credentials
  
  monitoring:
    enablePodMonitor: true
  
  backup:
    barmanObjectStore:
      destinationPath: s3://openvision-backups/postgres/
      s3Credentials:
        accessKeyId:
          name: s3-credentials
          key: access-key
        secretAccessKey:
          name: s3-credentials
          key: secret-key
    retentionPolicy: "30d"
EOF

# Wait for cluster ready
kubectl -n openvision get cluster openvision-postgres -w

# Install extensions
kubectl -n openvision exec -it openvision-postgres-1 -- psql -U postgres -d openvision -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"
kubectl -n openvision exec -it openvision-postgres-1 -- psql -U postgres -d openvision -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```

### Step 5: Deploy Platform Services

**Create secrets:**

```bash
# Generate secure passwords
export POSTGRES_PASSWORD=$(openssl rand -base64 32)
export REDIS_PASSWORD=$(openssl rand -base64 32)
export S3_SECRET_KEY=$(openssl rand -base64 32)
export JWT_SECRET=$(openssl rand -base64 64)
export KEYCLOAK_PASSWORD=$(openssl rand -base64 24)

# Create secret manifests
kubectl create secret generic postgres-credentials \
  --from-literal=username=openvision \
  --from-literal=password=$POSTGRES_PASSWORD \
  --namespace=openvision \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic s3-credentials \
  --from-literal=access-key=ACCESS_KEY_FROM_CEPH \
  --from-literal=secret-key=SECRET_KEY_FROM_CEPH \
  --namespace=openvision \
  --dry-run=client -o yaml | kubectl apply -f -

kubectl create secret generic jwt-signing-key \
  --from-literal=key=$JWT_SECRET \
  --namespace=openvision \
  --dry-run=client -o yaml | kubectl apply -f -
```

**Deploy core services with Helm:**

```bash
# Add Helm repos
helm repo add nats https://nats-io.github.io/k8s/helm/charts/
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add apisix https://charts.apiseven.com
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

# Deploy NATS
helm install nats nats/nats \
  --namespace openvision \
  --set cluster.enabled=true \
  --set cluster.replicas=3 \
  --set natsbox.enabled=true \
  --set jetstream.enabled=true \
  --set jetstream.fileStore.size=50Gi

# Deploy Redis Cluster
helm install redis bitnami/redis-cluster \
  --namespace openvision \
  --set cluster.nodes=6 \
  --set cluster.replicas=1 \
  --set password=$REDIS_PASSWORD

# Deploy Keycloak
helm install keycloak bitnami/keycloak \
  --namespace openvision \
  --set auth.adminUser=admin \
  --set auth.adminPassword=$KEYCLOAK_PASSWORD \
  --set postgresql.enabled=false \
  --set externalDatabase.host=openvision-postgres-rw \
  --set externalDatabase.database=keycloak \
  --set externalDatabase.user=openvision \
  --set externalDatabase.password=$POSTGRES_PASSWORD \
  --set replicaCount=2

# Deploy APISIX
helm install apisix apisix/apisix \
  --namespace openvision \
  --set gateway.type=LoadBalancer \
  --set ingress-controller.enabled=true \
  --set etcd.replicaCount=3

# Deploy Monitoring Stack
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace openvision \
  --set grafana.enabled=true \
  --set grafana.adminPassword=$GRAFANA_PASSWORD \
  --set prometheus.prometheusSpec.retention=90d \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.resources.requests.storage=500Gi \
  --set prometheus.prometheusSpec.storageSpec.volumeClaimTemplate.spec.storageClassName=ceph-block
```

**Deploy OpenVision applications:**

```bash
# Clone repository
git clone https://github.com/openvision/platform.git
cd platform

# Deploy manifests
kubectl apply -f deployment/kubernetes/core/
kubectl apply -f deployment/kubernetes/analytics/
kubectl apply -f deployment/kubernetes/integration/

# Verify
kubectl get pods -n openvision
kubectl get svc -n openvision
```

---

## Edge Site Deployment

### Step 1: Prepare Edge Nodes

**Using Ansible (Recommended for 20 sites):**

```bash
# Configure inventory
cat > inventory.yml <<EOF
all:
  children:
    edge_sites:
      children:
        site_01:
          hosts:
            edge-s01-n1:
              ansible_host: 10.1.1.10
            edge-s01-n2:
              ansible_host: 10.1.1.11
        site_02:
          hosts:
            edge-s02-n1:
              ansible_host: 10.2.1.10
            edge-s02-n2:
              ansible_host: 10.2.1.11
        # ... repeat for all 20 sites
EOF

# Run playbook
ansible-playbook -i inventory.yml playbooks/edge-setup.yml
```

**Manual Setup (Single Site):**

```bash
# SSH into edge node
ssh ubuntu@edge-site1-node1

# Install K3s
curl -sfL https://get.k3s.io | sh -s - \
  --disable traefik \
  --write-kubeconfig-mode 644 \
  --node-label site=site_01

# Get token for second node
sudo cat /var/lib/rancher/k3s/server/node-token

# On second node
curl -sfL https://get.k3s.io | K3S_URL=https://first-node:6443 \
  K3S_TOKEN=<token> sh -
```

### Step 2: Deploy Edge Services

```bash
# Create namespace
kubectl create namespace openvision-edge

# Deploy Frigate
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: frigate
  namespace: openvision-edge
spec:
  serviceName: frigate
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
        - containerPort: 1935
        - containerPort: 8554
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
  volumeClaimTemplates:
  - metadata:
      name: media
    spec:
      accessModes: ["ReadWriteOnce"]
      resources:
        requests:
          storage: 2Ti
EOF

# Deploy edge analytics
kubectl apply -f deployment/kubernetes/edge/

# Connect to central cloud (NATS leaf node)
kubectl apply -f deployment/kubernetes/edge/nats-leaf.yml
```

### Step 3: Configure Cameras

```bash
# Create camera configuration
kubectl create configmap frigate-config \
  --from-file=config.yml=configs/frigate-site1.yml \
  --namespace=openvision-edge

# Restart Frigate
kubectl rollout restart statefulset/frigate -n openvision-edge
```

---

## Network Configuration

### VPN Setup (WireGuard)

**Central Server:**

```bash
# Install WireGuard
sudo apt install -y wireguard

# Generate keys
wg genkey | tee privatekey | wg pubkey > publickey

# Configure
sudo nano /etc/wireguard/wg0.conf
# [Interface]
# Address = 10.100.0.1/24
# ListenPort = 51820
# PrivateKey = <server-private-key>
#
# [Peer]
# PublicKey = <site1-public-key>
# AllowedIPs = 10.100.1.0/24

# Start
sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0
```

**Edge Sites:**

```bash
# On each edge site
sudo apt install -y wireguard
wg genkey | tee privatekey | wg pubkey > publickey

sudo nano /etc/wireguard/wg0.conf
# [Interface]
# Address = 10.100.1.1/24
# PrivateKey = <site-private-key>
#
# [Peer]
# PublicKey = <server-public-key>
# Endpoint = vpn.openvision.com:51820
# AllowedIPs = 10.100.0.0/16
# PersistentKeepalive = 25

sudo wg-quick up wg0
sudo systemctl enable wg-quick@wg0
```

### Firewall Rules

```bash
# Allow Kubernetes API
sudo ufw allow 6443/tcp

# Allow node communication
sudo ufw allow 10250/tcp

# Allow VPN
sudo ufw allow 51820/udp

# Enable firewall
sudo ufw enable
```

---

## Security Hardening

### Enable Pod Security

```bash
kubectl apply -f - <<EOF
apiVersion: v1
kind: Namespace
metadata:
  name: openvision
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
EOF
```

### Deploy Falco

```bash
helm repo add falcosecurity https://falcosecurity.github.io/charts
helm install falco falcosecurity/falco \
  --namespace falco --create-namespace \
  --set falcosidekick.enabled=true \
  --set falcosidekick.webui.enabled=true
```

### Network Policies

```bash
kubectl apply -f deployment/kubernetes/security/network-policies.yml
```

---

## Monitoring & Operations

### Access Dashboards

```bash
# Get Grafana password
kubectl -n openvision get secret monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 -d

# Port forward
kubectl port-forward -n openvision svc/monitoring-grafana 3000:80

# Access: http://localhost:3000
# Username: admin
# Password: <from above>
```

### Health Checks

```bash
# Check all pods
kubectl get pods -n openvision

# Check Ceph status
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- ceph status

# Check PostgreSQL
kubectl -n openvision get cluster

# Check NATS
kubectl -n openvision exec -it nats-0 -- nats server info
```

---

## Disaster Recovery

### Backup Procedures

**PostgreSQL:**
```bash
# Automated with CloudNativePG
kubectl -n openvision exec -it openvision-postgres-1 -- \
  pg_basebackup -h localhost -U postgres -D /backup
```

**Ceph:**
```bash
# Snapshot-based
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- \
  rbd snap create replicapool/volume@snapshot1
```

### Recovery Procedures

See separate DR runbook for detailed procedures.

---

## Next Steps

1. ✅ **Validate Deployment** - Run integration tests
2. ✅ **Load Testing** - Simulate 500 cameras
3. ✅ **Security Audit** - Penetration testing
4. ✅ **Documentation** - Runbooks, procedures
5. ✅ **Training** - Operations team training
6. ✅ **Go-Live** - Production cutover

---

**Deployment Status:** Complete
**Support:** support@openvision.io
**Documentation:** https://docs.openvision.io
