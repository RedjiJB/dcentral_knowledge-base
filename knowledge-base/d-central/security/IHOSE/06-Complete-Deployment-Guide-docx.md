---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: 280dc084-52ee-47fc-b8ec-f7158c4ff0ff
original_filename: 06-Complete-Deployment-Guide.docx
created_at: 2025-12-02T00:47:54.508711+00:00
content_hash: a0e851e6325e
topic: ihose-deployment-infrastructure
topic: "ihose-openvision-documentation-package"
---

OpenVision Platform

**Complete Deployment Guide**

From Development to Enterprise Production

Version 1.0

Deployment Scenarios

OpenVision Platform supports multiple deployment models optimized for
different scales and use cases. This guide covers setup, configuration,
and operations for each scenario.

  -----------------------------------------------------------------------
  **Scenario**      **Scale**         **Technology**    **Best For**
  ----------------- ----------------- ----------------- -----------------
  **Development**   1-5 cameras       Docker Compose    Testing, demos

  **Small           5-25 cameras      Docker Compose    Retail, office
  Business**                                            

  **Edge**          10-50/site        K3s + EdgeX       Multi-site

  **Enterprise**    100+ cameras      Kubernetes        Campus, data
                                                        center

  **SaaS**          Multi-tenant      Kubernetes        Service provider
  -----------------------------------------------------------------------

Quick Start: Docker Compose

Docker Compose deployment is ideal for development, testing, and small
business deployments up to 25 cameras. Single-node setup with all
services containerized.

Prerequisites

-   Linux server (Ubuntu 22.04 LTS recommended)

-   16GB RAM minimum, 32GB recommended

-   500GB disk space (1TB+ for production)

-   Docker Engine 20.10+ and Docker Compose 2.0+

-   Optional: NVIDIA GPU with Docker runtime for AI acceleration

Installation Steps

**Step 1: Install Docker**

curl -fsSL https://get.docker.com -o get-docker.sh sudo sh get-docker.sh
sudo usermod -aG docker \$USER newgrp docker

**Step 2: Clone Repository**

git clone https://github.com/openvision/platform.git cd platform cp
.env.example .env

**Step 3: Configure Environment**

Edit .env file and set secure passwords:

POSTGRES_PASSWORD=secure_random_password_here
REDIS_PASSWORD=another_secure_password
MINIO_ROOT_PASSWORD=minio_secure_password
KEYCLOAK_ADMIN_PASSWORD=keycloak_admin_password

**Step 4: Start Services**

docker-compose up -d docker-compose ps \# Verify all services are
running docker-compose logs -f \# Watch logs

**Step 5: Initial Configuration**

Access web interfaces:

-   Shinobi VMS: http://your-server:8080

-   Grafana: http://your-server:3000 (admin/configured_password)

-   Node-RED: http://your-server:1880

-   MinIO Console: http://your-server:9001

**Step 6: Add Cameras**

In Shinobi:

1.  Log in with default credentials (see documentation)

2.  Click Add Camera

3.  Enter RTSP URL: rtsp://username:password@camera-ip:554/stream

4.  Configure recording schedule and motion detection

5.  Save and start monitoring

Edge Deployment with K3s

Edge deployments enable distributed architecture with local processing
at each site. Ideal for retail chains, branch offices, or facilities
requiring local autonomy with centralized management.

Edge Node Setup

**Hardware per Edge Node:**

-   Orange Pi 5 Plus or Rock 5B (ARM)

-   OR Intel NUC (x86) for better performance

-   NVIDIA Jetson Orin Nano for AI workloads

-   2TB NVMe SSD for local storage

-   Handles 15-30 cameras with local analytics

**Install K3s (Lightweight Kubernetes):**

curl -sfL https://get.k3s.io \| sh - sudo k3s kubectl get nodes \# Node
should show as Ready

**Deploy EdgeX Foundry:**

helm repo add edgexfoundry https://edgexfoundry.github.io/edgex-helm
helm install edgex edgexfoundry/edgex \--namespace edgex
\--create-namespace

**Deploy OpenVision Edge Stack:**

kubectl apply -f k8s/edge/openvision-edge.yml kubectl get pods -n
openvision \# All pods should be Running

Central Management Server

Deploy Kubernetes cluster at central location for:

-   Long-term video archival

-   Centralized monitoring and alerts

-   Cross-site analytics and reporting

-   Edge node management and updates

-   User access and authentication

**Connect Edge to Central:**

\# On edge node kubectl apply -f k8s/edge/central-sync.yml \# Configure
VPN (Tailscale recommended) curl -fsSL https://tailscale.com/install.sh
\| sh sudo tailscale up \# Register edge node with central curl -X POST
https://central.openvision.local/api/v1/edge/register \\ -H
\"Authorization: Bearer \$EDGE_TOKEN\" \\ -d \'{\"node_id\":
\"store-01\", \"location\": \"New York\"}\'

Enterprise Kubernetes Deployment

Production-grade Kubernetes deployment for large-scale enterprise
operations with high availability, disaster recovery, and multi-region
support.

Infrastructure Requirements

**Kubernetes Cluster:**

-   3 master nodes (control plane)

-   10+ worker nodes (compute)

-   4 GPU nodes (NVIDIA A100/H100 for AI)

-   10 storage nodes (Ceph distributed storage)

-   10GbE/40GbE networking backbone

**Setup Kubernetes Cluster:**

Option 1: Managed Kubernetes (Recommended)

-   AWS EKS, Google GKE, or Azure AKS

-   Simplified operations, automatic updates

-   Built-in high availability

Option 2: Self-Managed Kubernetes

\# Using kubeadm on Ubuntu 22.04 sudo apt-get update sudo apt-get
install -y kubeadm kubelet kubectl \# Initialize master node sudo
kubeadm init \--pod-network-cidr=10.244.0.0/16 \# Install CNI (Calico)
kubectl apply -f https://docs.projectcalico.org/manifests/calico.yaml \#
Join worker nodes sudo kubeadm join \<master-ip\>:6443 \--token
\<token\> \--discovery-token-ca-cert-hash \<hash\>

Deploy OpenVision Platform

**Step 1: Install Prerequisites**

\# NVIDIA GPU Operator kubectl apply -f
https://raw.githubusercontent.com/NVIDIA/gpu-operator/master/deployments/gpu-operator.yaml
\# Cert Manager kubectl apply -f
https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml
\# Prometheus Operator helm repo add prometheus-community
https://prometheus-community.github.io/helm-charts helm install
prometheus prometheus-community/kube-prometheus-stack

**Step 2: Deploy Storage Layer**

\# Rook-Ceph for distributed storage kubectl apply -f
k8s/storage/rook-operator.yml kubectl apply -f
k8s/storage/rook-cluster.yml kubectl apply -f
k8s/storage/rook-filesystem.yml

**Step 3: Configure Secrets**

\# Create namespace kubectl create namespace openvision \# Generate
strong passwords POSTGRES_PASS=\$(openssl rand -base64 32)
REDIS_PASS=\$(openssl rand -base64 32) MINIO_PASS=\$(openssl rand
-base64 32) \# Create secrets kubectl create secret generic
openvision-secrets -n openvision \\
\--from-literal=POSTGRES_PASSWORD=\$POSTGRES_PASS \\
\--from-literal=REDIS_PASSWORD=\$REDIS_PASS \\
\--from-literal=MINIO_ROOT_PASSWORD=\$MINIO_PASS

**Step 4: Deploy Core Services**

kubectl apply -f k8s/openvision-base.yml kubectl apply -f
k8s/openvision-analytics.yml kubectl apply -f
k8s/openvision-observability.yml

**Step 5: Verify Deployment**

kubectl get pods -n openvision kubectl get svc -n openvision kubectl top
nodes kubectl top pods -n openvision

**Step 6: Configure Ingress**

kubectl apply -f k8s/ingress.yml \# Configure DNS:
openvision.yourdomain.com -\> LoadBalancer IP

SaaS Multi-Tenant Deployment

Multi-tenant SaaS deployment enables serving multiple organizations from
a single platform instance with complete data isolation and per-tenant
customization.

Tenant Isolation Architecture

-   **Namespace per tenant:** Kubernetes namespace provides resource
    isolation

-   **Database schema per tenant:** PostgreSQL schema isolation for data
    security

-   **Storage buckets per tenant:** Separate MinIO buckets with
    encryption keys

-   **Network policies:** Prevent cross-tenant traffic

-   **Resource quotas:** CPU/memory/storage limits per subscription tier

Tenant Provisioning Workflow

**Automated tenant creation:**

\# Create new tenant via API curl -X POST
https://api.openvision.cloud/v1/tenants \\ -H \"Authorization: Bearer
\$ADMIN_TOKEN\" \\ -d \'{ \"tenant_id\": \"acme-corp\", \"name\": \"Acme
Corporation\", \"subscription_tier\": \"professional\", \"max_cameras\":
50, \"retention_days\": 90, \"admin_email\": \"admin@acmecorp.com\" }\'

Automation creates:

6.  Kubernetes namespace: openvision-acme-corp

7.  PostgreSQL schema: acme_corp

8.  MinIO bucket: acme-corp-videos

9.  Keycloak realm: acme-corp

10. Resource quotas based on tier

11. Initial admin user credentials

Subscription Tiers

  ------------------------------------------------------------------------
  **Tier**           **Cameras**       **Resources**     **Price/Month**
  ------------------ ----------------- ----------------- -----------------
  **Home**           1-4               2GB RAM, 100GB    \$29
                                       storage           

  **Professional**   5-25              8GB RAM, 500GB    \$199
                                       storage           

  **Enterprise**     25+               Custom            Custom
  ------------------------------------------------------------------------

**Configure resource quotas:**

apiVersion: v1 kind: ResourceQuota metadata: name: tenant-quota
namespace: openvision-acme-corp spec: hard: requests.cpu: \"8\"
requests.memory: 16Gi persistentvolumeclaims: \"10\" pods: \"50\"
services.loadbalancers: \"1\"

Operations & Maintenance

Monitoring & Alerting

**Key Metrics to Monitor:**

-   System health: CPU, memory, disk, network utilization

-   Camera status: Online/offline, frame rate, bitrate quality

-   Storage: Disk usage, retention compliance, backup status

-   Analytics: Processing latency, queue depth, error rates

-   API: Request rate, response time, error rate

**Configure Alerts:**

\# Prometheus AlertManager rules apiVersion: v1 kind: ConfigMap
metadata: name: prometheus-alerts data: alerts.yml: \| groups: - name:
openvision rules: - alert: CameraOffline expr: camera_online == 0 for:
5m annotations: description: Camera {{\$labels.camera_id}} offline -
alert: HighCPU expr: cpu_usage \> 90 for: 10m annotations: description:
High CPU on {{\$labels.node}}

Backup & Disaster Recovery

**Backup Strategy:**

12. **Configuration backups:** Daily backup of all Kubernetes manifests
    and configs

13. **Database backups:** Automated PostgreSQL backups every 6 hours

14. **Video archives:** Critical footage replicated to secondary site

15. **ML models:** Model registry with version history

**Disaster Recovery Test:**

Quarterly DR drills to validate recovery procedures:

16. Simulate primary site failure

17. Failover to secondary site

18. Verify all services operational

19. Test data recovery from backups

20. Document recovery time and issues

Scaling Operations

**Horizontal Scaling:**

\# Scale analytics pods kubectl scale deployment yolo-detector -n
openvision \--replicas=20 \# Add worker nodes to cluster kubeadm token
create \--print-join-command \# Run join command on new nodes \# Expand
storage cluster kubectl apply -f k8s/storage/add-osd-nodes.yml

**Vertical Scaling:**

\# Increase pod resources kubectl set resources deployment postgres -n
openvision \\ \--limits=cpu=8,memory=32Gi \\
\--requests=cpu=4,memory=16Gi

Conclusion

OpenVision Platform provides flexible deployment options scaling from
development environments to multi-region enterprise deployments. The
modular architecture ensures consistent operations across deployment
models while optimizing resource utilization for each use case.

For additional support, visit the community forum at
https://community.openvision.io or consult the full documentation at
https://docs.openvision.io
