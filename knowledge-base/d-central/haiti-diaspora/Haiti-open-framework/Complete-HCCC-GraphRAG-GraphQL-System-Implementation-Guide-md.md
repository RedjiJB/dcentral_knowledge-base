---
source_project: Haiti open framework
source_project_uuid: 019895b3-de37-7121-94fc-2bab9f1f436d
doc_uuid: 47ef7365-cc4f-4f89-b06a-663c3231b891
original_filename: Complete HCCC GraphRAG & GraphQL System Implementation Guide.md
created_at: 2025-08-16T18:58:05.203187+00:00
content_hash: 74e63dcc229b
topic: haiti-graphrag-graphql-system
---

# Complete HCCC GraphRAG & GraphQL System Implementation Guide
## From Zero to Production: Building the Haitian Cooperative Coordination Center

### Version: 1.0
### Date: 2025-01-16
### Implementation Type: Step-by-Step Production Guide

---

## Table of Contents

1. [Prerequisites & System Requirements](#1-prerequisites--system-requirements)
2. [Development Environment Setup](#2-development-environment-setup)
3. [Project Directory Structure](#3-project-directory-structure)
4. [Core Infrastructure Setup](#4-core-infrastructure-setup)
5. [Database Layer Implementation](#5-database-layer-implementation)
6. [GraphQL Federation Gateway](#6-graphql-federation-gateway)
7. [GraphRAG Intelligence Engine](#7-graphrag-intelligence-engine)
8. [Microservices Implementation](#8-microservices-implementation)
9. [Federated Social Media Integration](#9-federated-social-media-integration)
10. [Edge Computing & Mesh Network](#10-edge-computing--mesh-network)
11. [Community Data Sovereignty Layer](#11-community-data-sovereignty-layer)
12. [Testing & Quality Assurance](#12-testing--quality-assurance)
13. [Deployment & Infrastructure](#13-deployment--infrastructure)
14. [Post-Deployment Configuration](#14-post-deployment-configuration)
15. [Operations & Maintenance](#15-operations--maintenance)

---

## 1. Prerequisites & System Requirements

### 1.1 Hardware Requirements

#### **Development Machine**
```
Minimum:
- CPU: 8 cores (Intel i7/AMD Ryzen 7)
- RAM: 32GB
- Storage: 1TB SSD
- GPU: 8GB VRAM (RTX 3070/4060 or better for local AI development)

Recommended:
- CPU: 12+ cores (Intel i9/AMD Ryzen 9)
- RAM: 64GB
- Storage: 2TB NVMe SSD
- GPU: 16GB+ VRAM (RTX 4080/4090 or A4000)
```

#### **Production Infrastructure**
```
Cloud Resources (per environment):
- Kubernetes Cluster: 6-20 nodes (4 vCPU, 16GB RAM each)
- GPU Nodes: 2-4 nodes with Tesla V100/A100
- Storage: 5TB+ distributed storage
- Network: 10Gbps+ bandwidth
- Backup: 10TB+ object storage

Edge Infrastructure:
- Raspberry Pi 4B (8GB) × 50+ units
- Solar panels: 400W per edge node
- Battery: 24V 200Ah LiFePO4 per node
- LoRaWAN Gateway × 10+
```

### 1.2 Software Prerequisites

#### **Development Tools**
```bash
# Install these on your development machine

# Core Development
- Node.js 20.x LTS
- Python 3.11+
- Docker Desktop
- Git
- VS Code or similar IDE

# Container & Orchestration
- Docker 24.x
- Docker Compose 2.x
- kubectl
- Helm 3.x
- Kind or Minikube (for local K8s)

# Database Tools
- Neo4j Desktop
- PostgreSQL 15+
- Redis 7.x

# Build Tools
- Make
- Yarn or npm
- Poetry (Python)
- Terraform
```

#### **Development Environment Setup Script**
```bash
#!/bin/bash
# setup-dev-environment.sh

set -e

echo "🚀 Setting up HCCC Development Environment..."

# Install Node.js via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 20
nvm use 20

# Install Python dependencies
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-pip python3.11-venv

# Install Poetry for Python dependency management
curl -sSL https://install.python-poetry.org | python3 -

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Install Helm
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Install Terraform
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install terraform

# Install Kind for local Kubernetes
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

echo "✅ Development environment setup complete!"
echo "👉 Please log out and back in to apply Docker group changes"
```

---

## 2. Development Environment Setup

### 2.1 Local Development Cluster

#### **Create Local Kubernetes Cluster**
```bash
# kind-cluster-config.yaml
cat > kind-cluster-config.yaml << EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
name: hccc-dev
nodes:
- role: control-plane
  kubeadmConfigPatches:
  - |
    kind: InitConfiguration
    nodeRegistration:
      kubeletExtraArgs:
        node-labels: "ingress-ready=true"
  extraPortMappings:
  - containerPort: 80
    hostPort: 80
    protocol: TCP
  - containerPort: 443
    hostPort: 443
    protocol: TCP
- role: worker
  extraMounts:
  - hostPath: ./data
    containerPath: /data
- role: worker
  extraMounts:
  - hostPath: ./data
    containerPath: /data
EOF

# Create the cluster
kind create cluster --config kind-cluster-config.yaml

# Verify cluster
kubectl cluster-info --context kind-hccc-dev
```

#### **Install Core Infrastructure in Local Cluster**
```bash
# install-local-infrastructure.sh
#!/bin/bash

echo "🔧 Installing core infrastructure..."

# Install NGINX Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml

# Wait for ingress controller
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=90s

# Install Prometheus & Grafana
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.service.type=NodePort \
  --set grafana.service.type=NodePort

# Install Redis
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install redis bitnami/redis \
  --namespace hccc-system \
  --create-namespace \
  --set auth.enabled=false \
  --set master.persistence.enabled=false

# Install PostgreSQL
helm install postgresql bitnami/postgresql \
  --namespace hccc-system \
  --set auth.database=hccc \
  --set auth.username=hccc \
  --set auth.password=dev-password \
  --set primary.persistence.enabled=false

echo "✅ Local infrastructure installed!"
```

### 2.2 Development Configuration

#### **Environment Configuration**
```bash
# .env.development
NODE_ENV=development
DEBUG=true

# Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=dev-password

POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=hccc
POSTGRES_USER=hccc
POSTGRES_PASSWORD=dev-password

REDIS_HOST=localhost
REDIS_PORT=6379

# GraphQL Configuration
GRAPHQL_PORT=4000
GRAPHQL_INTROSPECTION=true
GRAPHQL_PLAYGROUND=true

# GraphRAG Configuration
GRAPHRAG_PORT=8000
GRAPHRAG_MODEL_PATH=./models
GRAPHRAG_ENABLE_GPU=false  # Set to true if you have GPU

# Community Configuration
DEFAULT_COMMUNITY_ID=dev-community-001
CULTURAL_VALIDATION_ENABLED=true
COMMUNITY_DATA_SOVEREIGNTY=true

# Development Features
MOCK_EXTERNAL_SERVICES=true
ENABLE_SEED_DATA=true
LOG_LEVEL=debug
```

---

## 3. Project Directory Structure

### 3.1 Complete Project Structure
```
hccc-system/
├── README.md
├── docker-compose.yml
├── docker-compose.override.yml
├── .env.example
├── .gitignore
├── Makefile
├── package.json
├── 
├── apps/                              # Application services
│   ├── graphql-gateway/              # Apollo Federation Gateway
│   │   ├── src/
│   │   │   ├── index.ts
│   │   │   ├── schema/
│   │   │   ├── resolvers/
│   │   │   ├── middleware/
│   │   │   ├── auth/
│   │   │   └── utils/
│   │   ├── package.json
│   │   ├── Dockerfile
│   │   └── tsconfig.json
│   │
│   ├── graphrag-engine/              # GraphRAG Intelligence Engine
│   │   ├── src/
│   │   │   ├── main.py
│   │   │   ├── graphrag/
│   │   │   ├── models/
│   │   │   ├── processors/
│   │   │   ├── cultural/
│   │   │   └── trust/
│   │   ├── requirements.txt
│   │   ├── pyproject.toml
│   │   ├── Dockerfile
│   │   └── poetry.lock
│   │
│   ├── personnel-service/            # Personnel Management API
│   ├── mesh-service/                 # Mesh Network Coordination
│   ├── sop-service/                  # Standard Operating Procedures
│   ├── security-service/             # Security Systems API
│   ├── health-service/               # Healthcare Information System
│   ├── education-service/            # Educational Technology Network
│   ├── agrimesh-service/             # Agriculture & Supply Chain
│   └── social-service/               # Federated Social Media
│
├── infrastructure/                   # Infrastructure as Code
│   ├── terraform/
│   │   ├── environments/
│   │   │   ├── development/
│   │   │   ├── staging/
│   │   │   └── production/
│   │   ├── modules/
│   │   │   ├── k8s-cluster/
│   │   │   ├── neo4j/
│   │   │   ├── redis-cluster/
│   │   │   └── monitoring/
│   │   └── main.tf
│   │
│   ├── kubernetes/                   # K8s manifests
│   │   ├── base/
│   │   ├── overlays/
│   │   │   ├── development/
│   │   │   ├── staging/
│   │   │   └── production/
│   │   └── helm-charts/
│   │
│   └── ansible/                      # Edge node provisioning
│       ├── inventories/
│       ├── playbooks/
│       └── roles/
│
├── packages/                         # Shared libraries
│   ├── shared-types/                 # TypeScript type definitions
│   ├── graphql-schemas/              # GraphQL schema definitions
│   ├── cultural-validation/          # Cultural validation utilities
│   ├── trust-scoring/                # Trust scoring algorithms
│   ├── community-governance/         # Governance utilities
│   └── monitoring/                   # Monitoring utilities
│
├── tools/                           # Development and build tools
│   ├── scripts/
│   │   ├── setup-dev.sh
│   │   ├── build-all.sh
│   │   ├── deploy.sh
│   │   └── seed-data.sh
│   ├── docker/
│   │   ├── base-images/
│   │   └── development/
│   └── codegen/
│       ├── generate-schemas.js
│       └── generate-types.js
│
├── docs/                            # Documentation
│   ├── api/
│   ├── deployment/
│   ├── development/
│   └── user-guides/
│
├── tests/                           # Test suites
│   ├── integration/
│   ├── e2e/
│   ├── performance/
│   └── cultural-validation/
│
├── data/                            # Development data
│   ├── seeds/
│   ├── migrations/
│   └── fixtures/
│
└── edge/                            # Edge computing components
    ├── raspberry-pi/
    ├── sensors/
    ├── mesh-networking/
    └── solar-management/
```

### 3.2 Initialize Project Structure
```bash
#!/bin/bash
# create-project-structure.sh

echo "📁 Creating HCCC project structure..."

# Create main project directory
mkdir -p hccc-system
cd hccc-system

# Create all directories
mkdir -p {apps,infrastructure,packages,tools,docs,tests,data,edge}

# Apps directories
mkdir -p apps/{graphql-gateway,graphrag-engine,personnel-service,mesh-service,sop-service,security-service,health-service,education-service,agrimesh-service,social-service}

# Infrastructure directories
mkdir -p infrastructure/{terraform/{environments/{development,staging,production},modules/{k8s-cluster,neo4j,redis-cluster,monitoring}},kubernetes/{base,overlays/{development,staging,production},helm-charts},ansible/{inventories,playbooks,roles}}

# Package directories
mkdir -p packages/{shared-types,graphql-schemas,cultural-validation,trust-scoring,community-governance,monitoring}

# Tools directories
mkdir -p tools/{scripts,docker/{base-images,development},codegen}

# Documentation directories
mkdir -p docs/{api,deployment,development,user-guides}

# Test directories
mkdir -p tests/{integration,e2e,performance,cultural-validation}

# Data directories
mkdir -p data/{seeds,migrations,fixtures}

# Edge computing directories
mkdir -p edge/{raspberry-pi,sensors,mesh-networking,solar-management}

# Initialize Git repository
git init
echo "node_modules/
*.log
.env
.env.local
dist/
build/
coverage/
.DS_Store
*.pyc
__pycache__/
.pytest_cache/
.mypy_cache/
terraform.tfstate*
.terraform/
helm-charts/*/charts/
*.tgz" > .gitignore

echo "✅ Project structure created!"
```

---

## 4. Core Infrastructure Setup

### 4.1 Docker Compose for Development

#### **Main Docker Compose Configuration**
```yaml
# docker-compose.yml
version: '3.8'

services:
  # Neo4j Graph Database
  neo4j:
    image: neo4j:5.13-community
    container_name: hccc-neo4j
    environment:
      - NEO4J_AUTH=neo4j/dev-password
      - NEO4J_PLUGINS=["apoc", "graph-data-science"]
      - NEO4J_dbms_security_procedures_unrestricted=apoc.*,gds.*
      - NEO4J_dbms_security_procedures_allowlist=apoc.*,gds.*
    ports:
      - "7474:7474"
      - "7687:7687"
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
      - neo4j_conf:/conf
      - neo4j_plugins:/plugins
    networks:
      - hccc-network

  # PostgreSQL for structured data
  postgres:
    image: postgres:15-alpine
    container_name: hccc-postgres
    environment:
      - POSTGRES_DB=hccc
      - POSTGRES_USER=hccc
      - POSTGRES_PASSWORD=dev-password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./data/migrations:/docker-entrypoint-initdb.d
    networks:
      - hccc-network

  # Redis for caching and pub/sub
  redis:
    image: redis:7-alpine
    container_name: hccc-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - hccc-network

  # IPFS for distributed storage
  ipfs:
    image: ipfs/go-ipfs:latest
    container_name: hccc-ipfs
    environment:
      - IPFS_PROFILE=server
    ports:
      - "4001:4001"      # P2P swarm
      - "5001:5001"      # API
      - "8080:8080"      # Gateway
    volumes:
      - ipfs_data:/data/ipfs
      - ipfs_staging:/export
    networks:
      - hccc-network

  # Prometheus for monitoring
  prometheus:
    image: prom/prometheus:latest
    container_name: hccc-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./infrastructure/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
      - '--web.enable-lifecycle'
    networks:
      - hccc-network

  # Grafana for visualization
  grafana:
    image: grafana/grafana:latest
    container_name: hccc-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=dev-password
    volumes:
      - grafana_data:/var/lib/grafana
      - ./infrastructure/monitoring/grafana:/etc/grafana/provisioning
    networks:
      - hccc-network

  # Jaeger for distributed tracing
  jaeger:
    image: jaegertracing/all-in-one:latest
    container_name: hccc-jaeger
    ports:
      - "16686:16686"    # Jaeger UI
      - "14268:14268"    # Jaeger HTTP collector
    environment:
      - COLLECTOR_OTLP_ENABLED=true
    networks:
      - hccc-network

volumes:
  neo4j_data:
  neo4j_logs:
  neo4j_conf:
  neo4j_plugins:
  postgres_data:
  redis_data:
  ipfs_data:
  ipfs_staging:
  prometheus_data:
  grafana_data:

networks:
  hccc-network:
    driver: bridge
```

#### **Development Override**
```yaml
# docker-compose.override.yml
version: '3.8'

services:
  # GraphQL Gateway
  graphql-gateway:
    build:
      context: ./apps/graphql-gateway
      dockerfile: Dockerfile.dev
    container_name: hccc-graphql-gateway
    environment:
      - NODE_ENV=development
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=dev-password
      - POSTGRES_HOST=postgres
      - POSTGRES_PORT=5432
      - POSTGRES_DB=hccc
      - POSTGRES_USER=hccc
      - POSTGRES_PASSWORD=dev-password
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    ports:
      - "4000:4000"
    volumes:
      - ./apps/graphql-gateway:/app
      - /app/node_modules
    depends_on:
      - neo4j
      - postgres
      - redis
    networks:
      - hccc-network
    command: npm run dev

  # GraphRAG Engine
  graphrag-engine:
    build:
      context: ./apps/graphrag-engine
      dockerfile: Dockerfile.dev
    container_name: hccc-graphrag-engine
    environment:
      - PYTHONPATH=/app
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=dev-password
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - CUDA_VISIBLE_DEVICES=0
    ports:
      - "8000:8000"
    volumes:
      - ./apps/graphrag-engine:/app
      - ./data/models:/app/models
    depends_on:
      - neo4j
      - redis
    networks:
      - hccc-network
    command: python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4.2 Start Development Environment
```bash
#!/bin/bash
# start-dev-environment.sh

echo "🚀 Starting HCCC development environment..."

# Create data directories
mkdir -p data/{models,seeds,migrations}

# Start core infrastructure
docker-compose up -d neo4j postgres redis ipfs prometheus grafana jaeger

echo "⏳ Waiting for databases to be ready..."
sleep 30

# Check if Neo4j is ready
echo "🔍 Checking Neo4j connection..."
until docker exec hccc-neo4j cypher-shell -u neo4j -p dev-password "RETURN 1"; do
  echo "Waiting for Neo4j..."
  sleep 5
done

# Check if PostgreSQL is ready
echo "🔍 Checking PostgreSQL connection..."
until docker exec hccc-postgres pg_isready -U hccc; do
  echo "Waiting for PostgreSQL..."
  sleep 5
done

echo "✅ Core infrastructure is ready!"
echo "📊 Grafana: http://localhost:3000 (admin/dev-password)"
echo "🔍 Prometheus: http://localhost:9090"
echo "🕵️ Jaeger: http://localhost:16686"
echo "🗃️ Neo4j Browser: http://localhost:7474"
echo "📁 IPFS Gateway: http://localhost:8080"
```

---

## 5. Database Layer Implementation

### 5.1 Neo4j Knowledge Graph Setup

#### **Initialize Neo4j with Constraints and Indexes**
```cypher
-- initialize-neo4j.cypher
-- Run this in Neo4j Browser or via cypher-shell

// Create constraints for unique identifiers
CREATE CONSTRAINT community_id IF NOT EXISTS FOR (c:Community) REQUIRE c.id IS UNIQUE;
CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT organization_id IF NOT EXISTS FOR (o:Organization) REQUIRE o.id IS UNIQUE;
CREATE CONSTRAINT event_id IF NOT EXISTS FOR (e:Event) REQUIRE e.id IS UNIQUE;
CREATE CONSTRAINT resource_id IF NOT EXISTS FOR (r:Resource) REQUIRE r.id IS UNIQUE;
CREATE CONSTRAINT location_id IF NOT EXISTS FOR (l:Location) REQUIRE l.id IS UNIQUE;
CREATE CONSTRAINT cooperative_id IF NOT EXISTS FOR (coop:Cooperative) REQUIRE coop.id IS UNIQUE;
CREATE CONSTRAINT product_id IF NOT EXISTS FOR (prod:Product) REQUIRE prod.id IS UNIQUE;

// Create indexes for frequently queried properties
CREATE INDEX person_name IF NOT EXISTS FOR (p:Person) ON (p.name);
CREATE INDEX person_skills IF NOT EXISTS FOR (p:Person) ON (p.skills);
CREATE INDEX event_timestamp IF NOT EXISTS FOR (e:Event) ON (e.timestamp);
CREATE INDEX event_type IF NOT EXISTS FOR (e:Event) ON (e.type);
CREATE INDEX location_name IF NOT EXISTS FOR (l:Location) ON (l.name);
CREATE INDEX cooperative_sector IF NOT EXISTS FOR (coop:Cooperative) ON (coop.sector);

// Create spatial indexes for geographic queries
CREATE INDEX location_spatial IF NOT EXISTS FOR (l:Location) ON (l.point);
CREATE INDEX event_location_spatial IF NOT EXISTS FOR (e:Event) ON (e.location);

// Create full-text search indexes
CREATE FULLTEXT INDEX entity_search IF NOT EXISTS
FOR (n:Person|Organization|Location|Event|Resource|Cooperative|Product)
ON EACH [n.name, n.description, n.tags];

// Create trust and reliability indexes
CREATE INDEX trust_score IF NOT EXISTS FOR (n) ON (n.trustScore);
CREATE INDEX reliability_score IF NOT EXISTS FOR (n) ON (n.reliabilityScore);
CREATE INDEX community_validation IF NOT EXISTS FOR (n) ON (n.communityValidated);

// Initialize sample community for development
MERGE (community:Community {
  id: 'dev-community-001',
  name: 'Development Community',
  region: 'Central Plateau',
  language: 'kreyol',
  established: date('2025-01-01'),
  governanceType: 'democratic_consensus'
});

// Create sample cooperative network
MERGE (agri_coop:Cooperative {
  id: 'agri-coop-001',
  name: 'Central Plateau Agricultural Cooperative',
  sector: 'agriculture',
  memberCount: 150,
  established: date('2023-06-15'),
  location: point({latitude: 18.5437, longitude: -72.3371})
});

MERGE (health_coop:Cooperative {
  id: 'health-coop-001', 
  name: 'Community Health Cooperative',
  sector: 'health',
  memberCount: 45,
  established: date('2023-08-20'),
  location: point({latitude: 18.5500, longitude: -72.3300})
});

// Link cooperatives to community
MERGE (community)-[:CONTAINS]->(agri_coop);
MERGE (community)-[:CONTAINS]->(health_coop);

// Create sample locations
MERGE (central_plateau:Location {
  id: 'location-central-plateau',
  name: 'Central Plateau',
  type: 'region',
  point: point({latitude: 18.5437, longitude: -72.3371}),
  population: 750000
});

MERGE (hinche:Location {
  id: 'location-hinche',
  name: 'Hinche',
  type: 'city',
  point: point({latitude: 19.1497, longitude: -72.0175}),
  population: 50000
});

// Link locations
MERGE (central_plateau)-[:CONTAINS]->(hinche);
MERGE (community)-[:LOCATED_IN]->(central_plateau);

// Create sample resources
MERGE (solar_panels:Resource {
  id: 'resource-solar-panels-001',
  name: 'Solar Panel Array',
  type: 'energy_infrastructure',
  capacity: '400W',
  status: 'operational',
  location: point({latitude: 18.5437, longitude: -72.3371}),
  cooperative: 'agri-coop-001'
});

MERGE (health_clinic:Resource {
  id: 'resource-health-clinic-001',
  name: 'Community Health Clinic',
  type: 'health_facility',
  capacity: '100 patients/day',
  status: 'operational',
  location: point({latitude: 18.5500, longitude: -72.3300}),
  cooperative: 'health-coop-001'
});

// Link resources
MERGE (agri_coop)-[:OWNS]->(solar_panels);
MERGE (health_coop)-[:OPERATES]->(health_clinic);
MERGE (solar_panels)-[:LOCATED_AT]->(central_plateau);
MERGE (health_clinic)-[:LOCATED_AT]->(central_plateau);
```

#### **Initialize Neo4j Script**
```bash
#!/bin/bash
# initialize-neo4j.sh

echo "🗃️ Initializing Neo4j Knowledge Graph..."

# Wait for Neo4j to be ready
until docker exec hccc-neo4j cypher-shell -u neo4j -p dev-password "RETURN 1" > /dev/null 2>&1; do
  echo "Waiting for Neo4j..."
  sleep 5
done

# Run initialization script
docker exec -i hccc-neo4j cypher-shell -u neo4j -p dev-password < data/seeds/initialize-neo4j.cypher

echo "✅ Neo4j Knowledge Graph initialized!"
```

### 5.2 PostgreSQL Schema Setup

#### **Database Migrations**
```sql
-- data/migrations/001_initial_schema.sql

-- Enable PostGIS for geographic data
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Communities table
CREATE TABLE communities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    region VARCHAR(255),
    language VARCHAR(50) DEFAULT 'kreyol',
    governance_type VARCHAR(100),
    established DATE,
    location GEOGRAPHY(POINT, 4326),
    cultural_values JSONB,
    contact_info JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Cooperatives table
CREATE TABLE cooperatives (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    community_id UUID REFERENCES communities(id),
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(100),
    member_count INTEGER,
    established DATE,
    location GEOGRAPHY(POINT, 4326),
    governance_structure JSONB,
    financial_info JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Personnel registry
CREATE TABLE personnel (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    community_id UUID REFERENCES communities(id),
    cooperative_id UUID REFERENCES cooperatives(id),
    name VARCHAR(255) NOT NULL,
    skills TEXT[],
    certifications JSONB,
    availability_status VARCHAR(50),
    contact_info JSONB,
    trust_score DECIMAL(3,2),
    community_validation BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Events and incidents
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    community_id UUID REFERENCES communities(id),
    type VARCHAR(100) NOT NULL,
    severity VARCHAR(50),
    status VARCHAR(50),
    title VARCHAR(255),
    description TEXT,
    location GEOGRAPHY(POINT, 4326),
    affected_area GEOGRAPHY(POLYGON, 4326),
    started_at TIMESTAMP WITH TIME ZONE,
    resolved_at TIMESTAMP WITH TIME ZONE,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Resources inventory
CREATE TABLE resources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    community_id UUID REFERENCES communities(id),
    cooperative_id UUID REFERENCES cooperatives(id),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100),
    category VARCHAR(100),
    quantity DECIMAL,
    unit VARCHAR(50),
    status VARCHAR(50),
    location GEOGRAPHY(POINT, 4326),
    specifications JSONB,
    maintenance_schedule JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Governance proposals
CREATE TABLE governance_proposals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    community_id UUID REFERENCES communities(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    proposal_type VARCHAR(100),
    status VARCHAR(50),
    voting_threshold DECIMAL(3,2),
    voting_period_start TIMESTAMP WITH TIME ZONE,
    voting_period_end TIMESTAMP WITH TIME ZONE,
    cultural_considerations JSONB,
    impact_assessment JSONB,
    submitted_by UUID REFERENCES personnel(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Votes on proposals
CREATE TABLE proposal_votes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    proposal_id UUID REFERENCES governance_proposals(id),
    voter_id UUID REFERENCES personnel(id),
    vote VARCHAR(20) CHECK (vote IN ('approve', 'reject', 'abstain')),
    reasoning TEXT,
    vote_weight DECIMAL(3,2) DEFAULT 1.0,
    is_anonymous BOOLEAN DEFAULT false,
    voted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Cultural validation records
CREATE TABLE cultural_validations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    entity_type VARCHAR(100),
    entity_id UUID,
    validation_type VARCHAR(100),
    approved BOOLEAN,
    elder_consulted BOOLEAN DEFAULT false,
    cultural_concerns TEXT[],
    recommendations TEXT[],
    validated_by UUID REFERENCES personnel(id),
    validated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Trust and reliability tracking
CREATE TABLE trust_assessments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    assessed_entity_type VARCHAR(100),
    assessed_entity_id UUID,
    assessor_id UUID REFERENCES personnel(id),
    trust_score DECIMAL(3,2),
    reliability_score DECIMAL(3,2),
    assessment_criteria JSONB,
    notes TEXT,
    assessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Audit trail
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    community_id UUID REFERENCES communities(id),
    action VARCHAR(255),
    resource_type VARCHAR(100),
    resource_id UUID,
    old_values JSONB,
    new_values JSONB,
    success BOOLEAN,
    error_message TEXT,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_communities_region ON communities(region);
CREATE INDEX idx_cooperatives_community ON cooperatives(community_id);
CREATE INDEX idx_cooperatives_sector ON cooperatives(sector);
CREATE INDEX idx_personnel_community ON personnel(community_id);
CREATE INDEX idx_personnel_skills ON personnel USING GIN(skills);
CREATE INDEX idx_events_community ON events(community_id);
CREATE INDEX idx_events_type ON events(type);
CREATE INDEX idx_events_status ON events(status);
CREATE INDEX idx_events_started_at ON events(started_at);
CREATE INDEX idx_resources_community ON resources(community_id);
CREATE INDEX idx_resources_type ON resources(type);
CREATE INDEX idx_proposals_community ON governance_proposals(community_id);
CREATE INDEX idx_proposals_status ON governance_proposals(status);
CREATE INDEX idx_votes_proposal ON proposal_votes(proposal_id);
CREATE INDEX idx_audit_log_user ON audit_log(user_id);
CREATE INDEX idx_audit_log_community ON audit_log(community_id);
CREATE INDEX idx_audit_log_created_at ON audit_log(created_at);

-- Create spatial indexes
CREATE INDEX idx_communities_location ON communities USING GIST(location);
CREATE INDEX idx_cooperatives_location ON cooperatives USING GIST(location);
CREATE INDEX idx_events_location ON events USING GIST(location);
CREATE INDEX idx_events_affected_area ON events USING GIST(affected_area);
CREATE INDEX idx_resources_location ON resources USING GIST(location);
```

#### **Seed Development Data**
```sql
-- data/seeds/002_development_data.sql

-- Insert development community
INSERT INTO communities (id, name, region, language, governance_type, established, location, cultural_values) VALUES 
(
    'dev-community-001'::uuid,
    'Development Community',
    'Central Plateau',
    'kreyol',
    'democratic_consensus',
    '2025-01-01',
    ST_GeogFromText('POINT(-72.3371 18.5437)'),
    '{"community_consensus": 0.9, "elder_respect": 0.95, "environmental_stewardship": 0.85}'::jsonb
);

-- Insert cooperatives
INSERT INTO cooperatives (id, community_id, name, sector, member_count, established, location, governance_structure) VALUES
(
    'agri-coop-001'::uuid,
    'dev-community-001'::uuid,
    'Central Plateau Agricultural Cooperative',
    'agriculture',
    150,
    '2023-06-15',
    ST_GeogFromText('POINT(-72.3371 18.5437)'),
    '{"decision_making": "consensus", "leadership": "rotating", "meetings": "weekly"}'::jsonb
),
(
    'health-coop-001'::uuid,
    'dev-community-001'::uuid,
    'Community Health Cooperative',
    'health',
    45,
    '2023-08-20',
    ST_GeogFromText('POINT(-72.3300 18.5500)'),
    '{"decision_making": "majority_vote", "leadership": "elected", "meetings": "bi_weekly"}'::jsonb
);

-- Insert sample personnel
INSERT INTO personnel (id, community_id, cooperative_id, name, skills, availability_status, trust_score, community_validation) VALUES
(
    uuid_generate_v4(),
    'dev-community-001'::uuid,
    'agri-coop-001'::uuid,
    'Marie Joseph',
    ARRAY['agriculture', 'soil_management', 'crop_rotation', 'community_organizing'],
    'available',
    0.92,
    true
),
(
    uuid_generate_v4(),
    'dev-community-001'::uuid,
    'health-coop-001'::uuid,
    'Pierre Antoine',
    ARRAY['community_health', 'first_aid', 'health_education', 'herbal_medicine'],
    'available',
    0.88,
    true
),
(
    uuid_generate_v4(),
    'dev-community-001'::uuid,
    'agri-coop-001'::uuid,
    'Claudette Michel',
    ARRAY['sustainable_agriculture', 'seed_saving', 'food_processing', 'market_coordination'],
    'available',
    0.91,
    true
);

-- Insert sample resources
INSERT INTO resources (id, community_id, cooperative_id, name, type, category, quantity, unit, status, location, specifications) VALUES
(
    uuid_generate_v4(),
    'dev-community-001'::uuid,
    'agri-coop-001'::uuid,
    'Solar Panel Array',
    'energy_infrastructure',
    'renewable_energy',
    400,
    'watts',
    'operational',
    ST_GeogFromText('POINT(-72.3371 18.5437)'),
    '{"efficiency": "20%", "installation_date": "2023-09-15", "warranty": "25 years"}'::jsonb
),
(
    uuid_generate_v4(),
    'dev-community-001'::uuid,
    'health-coop-001'::uuid,
    'Community Health Clinic',
    'health_facility',
    'primary_care',
    100,
    'patients_per_day',
    'operational',
    ST_GeogFromText('POINT(-72.3300 18.5500)'),
    '{"rooms": 5, "equipment": ["basic_medical", "examination", "pharmacy"], "staffing": "2 nurses, 1 doctor"}'::jsonb
);
```

---

## 6. GraphQL Federation Gateway

### 6.1 Gateway Implementation

#### **Package Configuration**
```json
// apps/graphql-gateway/package.json
{
  "name": "@hccc/graphql-gateway",
  "version": "1.0.0",
  "description": "HCCC Apollo Federation Gateway",
  "main": "dist/index.js",
  "scripts": {
    "dev": "nodemon --exec ts-node src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "jest",
    "test:watch": "jest --watch",
    "lint": "eslint src/**/*.ts",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "@apollo/gateway": "^2.5.1",
    "@apollo/server": "^4.9.5",
    "@apollo/subgraph": "^2.5.1",
    "apollo-server-express": "^3.12.1",
    "express": "^4.18.2",
    "graphql": "^16.8.1",
    "redis": "^4.6.10",
    "pg": "^8.11.3",
    "neo4j-driver": "^5.14.0",
    "jsonwebtoken": "^9.0.2",
    "bcryptjs": "^2.4.3",
    "helmet": "^7.1.0",
    "cors": "^2.8.5",
    "compression": "^1.7.4",
    "rate-limiter-flexible": "^4.0.1",
    "prom-client": "^15.0.0",
    "@opentelemetry/api": "^1.7.0",
    "@opentelemetry/sdk-node": "^0.45.0",
    "@opentelemetry/instrumentation-graphql": "^0.35.0",
    "winston": "^3.11.0",
    "dotenv": "^16.3.1"
  },
  "devDependencies": {
    "@types/node": "^20.8.7",
    "@types/express": "^4.17.20",
    "@types/cors": "^2.8.15",
    "@types/compression": "^1.7.4",
    "@types/jsonwebtoken": "^9.0.4",
    "@types/bcryptjs": "^2.4.5",
    "typescript": "^5.2.2",
    "ts-node": "^10.9.1",
    "nodemon": "^3.0.1",
    "jest": "^29.7.0",
    "@types/jest": "^29.5.7",
    "eslint": "^8.52.0",
    "@typescript-eslint/parser": "^6.9.1",
    "@typescript-eslint/eslint-plugin": "^6.9.1"
  }
}
```

#### **TypeScript Configuration**
```json
// apps/graphql-gateway/tsconfig.json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "lib": ["ES2020"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "removeComments": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "noImplicitThis": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "moduleResolution": "node",
    "baseUrl": "./",
    "paths": {
      "@/*": ["src/*"]
    },
    "allowSyntheticDefaultImports": true,
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true
  },
  "include": [
    "src/**/*"
  ],
  "exclude": [
    "node_modules",
    "dist"
  ]
}
```

#### **Main Gateway Server**
```typescript
// apps/graphql-gateway/src/index.ts

import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import { ApolloGateway, IntrospectAndCompose } from '@apollo/gateway';
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import { createServer } from 'http';
import { WebSocketServer } from 'ws';
import { useServer } from 'graphql-ws/lib/use/ws';
import { buildSchema } from 'graphql';
import { config } from '@/config';
import { logger } from '@/utils/logger';
import { createContext } from '@/context';
import { authMiddleware } from '@/middleware/auth';
import { rateLimitMiddleware } from '@/middleware/rateLimit';
import { metricsMiddleware } from '@/middleware/metrics';
import { errorHandler } from '@/middleware/errorHandler';
import { setupTracing } from '@/utils/tracing';

// Initialize distributed tracing
setupTracing();

async function startServer() {
  try {
    logger.info('🚀 Starting HCCC GraphQL Gateway...');

    // Create Express app
    const app = express();
    const httpServer = createServer(app);

    // Security middleware
    app.use(helmet({
      contentSecurityPolicy: {
        directives: {
          defaultSrc: ["'self'"],
          scriptSrc: ["'self'", "'unsafe-inline'"],
          styleSrc: ["'self'", "'unsafe-inline'"],
          imgSrc: ["'self'", "data:", "https:"],
        },
      },
      crossOriginEmbedderPolicy: false,
    }));

    app.use(compression());
    app.use(cors({
      origin: config.cors.origins,
      credentials: true,
    }));

    // Rate limiting
    app.use(rateLimitMiddleware);

    // Metrics middleware
    app.use(metricsMiddleware);

    // Create Apollo Gateway
    const gateway = new ApolloGateway({
      supergraphSdl: new IntrospectAndCompose({
        subgraphs: [
          { 
            name: 'personnel', 
            url: `${config.services.personnel.url}/graphql` 
          },
          { 
            name: 'mesh', 
            url: `${config.services.mesh.url}/graphql` 
          },
          { 
            name: 'sop', 
            url: `${config.services.sop.url}/graphql` 
          },
          { 
            name: 'security', 
            url: `${config.services.security.url}/graphql` 
          },
          { 
            name: 'health', 
            url: `${config.services.health.url}/graphql` 
          },
          { 
            name: 'education', 
            url: `${config.services.education.url}/graphql` 
          },
          { 
            name: 'agrimesh', 
            url: `${config.services.agrimesh.url}/graphql` 
          },
          { 
            name: 'social', 
            url: `${config.services.social.url}/graphql` 
          },
        ],
        pollIntervalInMs: config.gateway.pollInterval,
      }),
      debug: config.isDevelopment,
    });

    // Create Apollo Server
    const server = new ApolloServer({
      gateway,
      introspection: config.graphql.introspection,
      includeStacktraceInErrorResponses: config.isDevelopment,
      formatError: (err) => {
        logger.error('GraphQL Error:', err);
        return err;
      },
      plugins: [
        // Apollo Studio plugin for production
        ...(config.apollo.studio.enabled ? [
          require('@apollo/server-plugin-usage-reporting')({
            apiKey: config.apollo.studio.apiKey,
          })
        ] : []),
        
        // Custom metrics plugin
        {
          requestDidStart() {
            return {
              didResolveOperation(requestContext) {
                const operationName = requestContext.request.operationName;
                const operation = requestContext.document?.definitions[0];
                const operationType = operation?.kind === 'OperationDefinition' 
                  ? operation.operation 
                  : 'unknown';
                
                logger.info('GraphQL Operation', {
                  operationName,
                  operationType,
                  communityId: requestContext.contextValue?.user?.communityId,
                });
              },
            };
          },
        },
      ],
    });

    await server.start();

    // GraphQL endpoint with authentication
    app.use(
      '/graphql',
      authMiddleware,
      expressMiddleware(server, {
        context: createContext,
      })
    );

    // Health check endpoint
    app.get('/health', (req, res) => {
      res.json({ 
        status: 'healthy', 
        timestamp: new Date().toISOString(),
        version: process.env.npm_package_version 
      });
    });

    // Readiness check
    app.get('/ready', async (req, res) => {
      try {
        // Check gateway health
        const gatewayHealth = gateway.executor ? 'healthy' : 'unhealthy';
        
        res.json({
          status: gatewayHealth,
          services: {
            gateway: gatewayHealth,
          },
          timestamp: new Date().toISOString(),
        });
      } catch (error) {
        res.status(503).json({
          status: 'unhealthy',
          error: error.message,
          timestamp: new Date().toISOString(),
        });
      }
    });

    // Metrics endpoint
    app.get('/metrics', async (req, res) => {
      const register = require('prom-client').register;
      res.set('Content-Type', register.contentType);
      res.end(await register.metrics());
    });

    // Error handling middleware
    app.use(errorHandler);

    // WebSocket server for subscriptions
    const wsServer = new WebSocketServer({
      server: httpServer,
      path: '/graphql',
    });

    // Set up subscription handling
    const serverCleanup = useServer(
      {
        schema: buildSchema(`
          type Query { _: String }
          type Subscription {
            crisisUpdates(region: String!): String
            coordinationMessages(hcccId: String!): String
          }
        `),
        context: createContext,
        onConnect: async (ctx) => {
          logger.info('WebSocket connection established');
          return ctx;
        },
        onDisconnect: (ctx, code, reason) => {
          logger.info('WebSocket connection closed', { code, reason });
        },
      },
      wsServer
    );

    // Start HTTP server
    const port = config.server.port;
    httpServer.listen(port, () => {
      logger.info(`🚀 GraphQL Gateway ready at http://localhost:${port}/graphql`);
      logger.info(`🔌 WebSocket subscriptions ready at ws://localhost:${port}/graphql`);
      logger.info(`❤️ Health check available at http://localhost:${port}/health`);
      logger.info(`📊 Metrics available at http://localhost:${port}/metrics`);
    });

    // Graceful shutdown
    process.on('SIGTERM', async () => {
      logger.info('SIGTERM received, shutting down gracefully...');
      
      serverCleanup.dispose();
      await server.stop();
      httpServer.close(() => {
        logger.info('HTTP server closed');
        process.exit(0);
      });
    });

  } catch (error) {
    logger.error('Failed to start server:', error);
    process.exit(1);
  }
}

// Handle unhandled promise rejections
process.on('unhandledRejection', (reason, promise) => {
  logger.error('Unhandled Rejection at:', promise, 'reason:', reason);
  process.exit(1);
});

// Handle uncaught exceptions
process.on('uncaughtException', (error) => {
  logger.error('Uncaught Exception:', error);
  process.exit(1);
});

// Start the server
startServer();
```

#### **Configuration Management**
```typescript
// apps/graphql-gateway/src/config/index.ts

import dotenv from 'dotenv';
import { logger } from '@/utils/logger';

// Load environment variables
dotenv.config();

interface Config {
  env: string;
  isDevelopment: boolean;
  isProduction: boolean;
  
  server: {
    port: number;
    host: string;
  };
  
  graphql: {
    introspection: boolean;
    playground: boolean;
  };
  
  gateway: {
    pollInterval: number;
  };
  
  cors: {
    origins: string[];
  };
  
  auth: {
    jwtSecret: string;
    jwtExpiration: string;
  };
  
  databases: {
    neo4j: {
      uri: string;
      user: string;
      password: string;
    };
    postgres: {
      host: string;
      port: number;
      database: string;
      user: string;
      password: string;
    };
    redis: {
      host: string;
      port: number;
      password?: string;
    };
  };
  
  services: {
    personnel: { url: string };
    mesh: { url: string };
    sop: { url: string };
    security: { url: string };
    health: { url: string };
    education: { url: string };
    agrimesh: { url: string };
    social: { url: string };
    graphrag: { url: string };
  };
  
  apollo: {
    studio: {
      enabled: boolean;
      apiKey?: string;
    };
  };
  
  monitoring: {
    jaeger: {
      endpoint: string;
    };
  };
  
  rateLimit: {
    windowMs: number;
    maxRequests: number;
  };
}

function getEnvVar(name: string, defaultValue?: string): string {
  const value = process.env[name];
  if (!value && !defaultValue) {
    throw new Error(`Environment variable ${name} is required`);
  }
  return value || defaultValue!;
}

function getEnvNumber(name: string, defaultValue: number): number {
  const value = process.env[name];
  return value ? parseInt(value, 10) : defaultValue;
}

function getEnvBoolean(name: string, defaultValue: boolean): boolean {
  const value = process.env[name];
  return value ? value.toLowerCase() === 'true' : defaultValue;
}

export const config: Config = {
  env: getEnvVar('NODE_ENV', 'development'),
  isDevelopment: getEnvVar('NODE_ENV', 'development') === 'development',
  isProduction: getEnvVar('NODE_ENV', 'development') === 'production',
  
  server: {
    port: getEnvNumber('GRAPHQL_PORT', 4000),
    host: getEnvVar('GRAPHQL_HOST', '0.0.0.0'),
  },
  
  graphql: {
    introspection: getEnvBoolean('GRAPHQL_INTROSPECTION', true),
    playground: getEnvBoolean('GRAPHQL_PLAYGROUND', true),
  },
  
  gateway: {
    pollInterval: getEnvNumber('GATEWAY_POLL_INTERVAL', 30000),
  },
  
  cors: {
    origins: getEnvVar('CORS_ORIGINS', 'http://localhost:3000,http://localhost:3001')
      .split(',')
      .map(origin => origin.trim()),
  },
  
  auth: {
    jwtSecret: getEnvVar('JWT_SECRET', 'dev-secret-key'),
    jwtExpiration: getEnvVar('JWT_EXPIRATION', '24h'),
  },
  
  databases: {
    neo4j: {
      uri: getEnvVar('NEO4J_URI', 'bolt://localhost:7687'),
      user: getEnvVar('NEO4J_USER', 'neo4j'),
      password: getEnvVar('NEO4J_PASSWORD', 'dev-password'),
    },
    postgres: {
      host: getEnvVar('POSTGRES_HOST', 'localhost'),
      port: getEnvNumber('POSTGRES_PORT', 5432),
      database: getEnvVar('POSTGRES_DB', 'hccc'),
      user: getEnvVar('POSTGRES_USER', 'hccc'),
      password: getEnvVar('POSTGRES_PASSWORD', 'dev-password'),
    },
    redis: {
      host: getEnvVar('REDIS_HOST', 'localhost'),
      port: getEnvNumber('REDIS_PORT', 6379),
      password: process.env.REDIS_PASSWORD,
    },
  },
  
  services: {
    personnel: { 
      url: getEnvVar('PERSONNEL_SERVICE_URL', 'http://localhost:4001') 
    },
    mesh: { 
      url: getEnvVar('MESH_SERVICE_URL', 'http://localhost:4002') 
    },
    sop: { 
      url: getEnvVar('SOP_SERVICE_URL', 'http://localhost:4003') 
    },
    security: { 
      url: getEnvVar('SECURITY_SERVICE_URL', 'http://localhost:4004') 
    },
    health: { 
      url: getEnvVar('HEALTH_SERVICE_URL', 'http://localhost:4005') 
    },
    education: { 
      url: getEnvVar('EDUCATION_SERVICE_URL', 'http://localhost:4006') 
    },
    agrimesh: { 
      url: getEnvVar('AGRIMESH_SERVICE_URL', 'http://localhost:4007') 
    },
    social: { 
      url: getEnvVar('SOCIAL_SERVICE_URL', 'http://localhost:4008') 
    },
    graphrag: { 
      url: getEnvVar('GRAPHRAG_SERVICE_URL', 'http://localhost:8000') 
    },
  },
  
  apollo: {
    studio: {
      enabled: getEnvBoolean('APOLLO_STUDIO_ENABLED', false),
      apiKey: process.env.APOLLO_KEY,
    },
  },
  
  monitoring: {
    jaeger: {
      endpoint: getEnvVar('JAEGER_ENDPOINT', 'http://localhost:14268/api/traces'),
    },
  },
  
  rateLimit: {
    windowMs: getEnvNumber('RATE_LIMIT_WINDOW_MS', 60000), // 1 minute
    maxRequests: getEnvNumber('RATE_LIMIT_MAX_REQUESTS', 100),
  },
};

// Log configuration on startup (excluding sensitive data)
logger.info('Configuration loaded', {
  env: config.env,
  server: config.server,
  graphql: config.graphql,
  services: Object.keys(config.services),
});
```

### 6.2 Authentication & Authorization

#### **JWT Authentication Middleware**
```typescript
// apps/graphql-gateway/src/middleware/auth.ts

import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import { config } from '@/config';
import { logger } from '@/utils/logger';
import { getUserFromDatabase } from '@/services/userService';

export interface AuthenticatedUser {
  id: string;
  communityId: string;
  cooperativeId?: string;
  permissions: string[];
  trustScore: number;
  communityValidated: boolean;
}

export interface AuthenticatedRequest extends Request {
  user?: AuthenticatedUser;
}

export const authMiddleware = async (
  req: AuthenticatedRequest,
  res: Response,
  next: NextFunction
): Promise<void> => {
  try {
    // Skip authentication for health checks and introspection in development
    if (req.path === '/health' || 
        req.path === '/ready' || 
        req.path === '/metrics' ||
        (config.isDevelopment && req.body?.query?.includes('__schema'))) {
      return next();
    }

    const authHeader = req.headers.authorization;
    
    if (!authHeader?.startsWith('Bearer ')) {
      res.status(401).json({ 
        error: 'Authorization header missing or invalid',
        code: 'UNAUTHORIZED'
      });
      return;
    }

    const token = authHeader.substring(7);
    
    try {
      const decoded = jwt.verify(token, config.auth.jwtSecret) as any;
      
      // Get full user details from database
      const user = await getUserFromDatabase(decoded.userId);
      
      if (!user) {
        res.status(401).json({ 
          error: 'User not found',
          code: 'USER_NOT_FOUND'
        });
        return;
      }

      // Check if user is still active and validated
      if (!user.isActive || !user.communityValidated) {
        res.status(403).json({ 
          error: 'User account is not active or not community validated',
          code: 'ACCOUNT_INACTIVE'
        });
        return;
      }

      req.user = {
        id: user.id,
        communityId: user.communityId,
        cooperativeId: user.cooperativeId,
        permissions: user.permissions,
        trustScore: user.trustScore,
        communityValidated: user.communityValidated,
      };

      logger.debug('User authenticated', {
        userId: user.id,
        communityId: user.communityId,
        permissions: user.permissions.length,
      });

      next();
      
    } catch (jwtError) {
      logger.warn('JWT verification failed', {
        error: jwtError.message,
        token: token.substring(0, 10) + '...',
      });
      
      res.status(401).json({ 
        error: 'Invalid token',
        code: 'INVALID_TOKEN'
      });
      return;
    }
    
  } catch (error) {
    logger.error('Authentication middleware error:', error);
    res.status(500).json({ 
      error: 'Authentication service error',
      code: 'AUTH_SERVICE_ERROR'
    });
  }
};

// Permission checking utility
export const hasPermission = (
  user: AuthenticatedUser, 
  requiredPermission: string
): boolean => {
  return user.permissions.includes(requiredPermission) || 
         user.permissions.includes('admin:all');
};

// Community access checking
export const hasCommunityAccess = (
  user: AuthenticatedUser, 
  communityId: string
): boolean => {
  return user.communityId === communityId || 
         user.permissions.includes('access:all_communities');
};

// Trust score validation
export const meetsTrustThreshold = (
  user: AuthenticatedUser, 
  requiredTrustScore: number
): boolean => {
  return user.trustScore >= requiredTrustScore;
};
```

#### **GraphQL Context Creation**
```typescript
// apps/graphql-gateway/src/context/index.ts

import { Request } from 'express';
import { Neo4jService } from '@/services/neo4jService';
import { PostgresService } from '@/services/postgresService';
import { RedisService } from '@/services/redisService';
import { GraphRAGService } from '@/services/graphragService';
import { CommunityDataService } from '@/services/communityDataService';
import { CulturalValidationService } from '@/services/culturalValidationService';
import { AuditService } from '@/services/auditService';
import { AuthenticatedUser } from '@/middleware/auth';
import { logger } from '@/utils/logger';

export interface GraphQLContext {
  user?: AuthenticatedUser;
  
  // Data sources
  neo4j: Neo4jService;
  postgres: PostgresService;
  redis: RedisService;
  
  // AI and intelligence services
  graphRAG: GraphRAGService;
  
  // Community services
  communityData: CommunityDataService;
  culturalValidation: CulturalValidationService;
  
  // Audit and logging
  audit: AuditService;
  
  // Request context
  request: Request;
  requestId: string;
}

// Initialize services (singleton instances)
const neo4jService = new Neo4jService();
const postgresService = new PostgresService();
const redisService = new RedisService();
const graphRAGService = new GraphRAGService();
const communityDataService = new CommunityDataService();
const culturalValidationService = new CulturalValidationService();
const auditService = new AuditService();

export const createContext = async ({ req }: { req: Request }): Promise<GraphQLContext> => {
  const requestId = req.headers['x-request-id'] as string || 
                   Math.random().toString(36).substring(2, 15);

  const context: GraphQLContext = {
    user: (req as any).user,
    
    // Data sources
    neo4j: neo4jService,
    postgres: postgresService,
    redis: redisService,
    
    // AI services
    graphRAG: graphRAGService,
    
    // Community services
    communityData: communityDataService,
    culturalValidation: culturalValidationService,
    
    // Audit
    audit: auditService,
    
    // Request context
    request: req,
    requestId,
  };

  // Log request context creation
  logger.debug('GraphQL context created', {
    requestId,
    userId: context.user?.id,
    communityId: context.user?.communityId,
    operationName: req.body?.operationName,
  });

  return context;
};
```

### 6.3 Dockerfile for Gateway

#### **Development Dockerfile**
```dockerfile
# apps/graphql-gateway/Dockerfile.dev
FROM node:20-alpine

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache python3 make g++

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY src/ ./src/

# Expose port
EXPOSE 4000

# Development command (will be overridden by docker-compose)
CMD ["npm", "run", "dev"]
```

#### **Production Dockerfile**
```dockerfile
# apps/graphql-gateway/Dockerfile
FROM node:20-alpine AS builder

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache python3 make g++

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY src/ ./src/

# Build application
RUN npm run build

# Production stage
FROM node:20-alpine AS production

WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Copy built application
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Change ownership
RUN chown -R nodejs:nodejs /app

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 4000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD node -e "require('http').get('http://localhost:4000/health', (res) => { process.exit(res.statusCode === 200 ? 0 : 1) })"

# Start application
CMD ["node", "dist/index.js"]
```

---

## 7. GraphRAG Intelligence Engine

### 7.1 Python Project Setup

#### **Poetry Configuration**
```toml
# apps/graphrag-engine/pyproject.toml
[tool.poetry]
name = "hccc-graphrag-engine"
version = "1.0.0"
description = "HCCC GraphRAG Intelligence Engine"
authors = ["HCCC Development Team <dev@hccc.ht>"]
readme = "README.md"
packages = [{include = "graphrag", from = "src"}]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.104.1"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
neo4j = "^5.14.1"
redis = "^5.0.1"
numpy = "^1.25.2"
pandas = "^2.1.3"
torch = "^2.1.1"
transformers = "^4.35.2"
sentence-transformers = "^2.2.2"
spacy = "^3.7.2"
networkx = "^3.2.1"
scikit-learn = "^1.3.2"
langchain = "^0.0.330"
openai = "^1.3.5"
anthropic = "^0.5.0"
pydantic = "^2.5.0"
pydantic-settings = "^2.1.0"
httpx = "^0.25.2"
aiofiles = "^23.2.1"
prometheus-client = "^0.19.0"
structlog = "^23.2.0"
python-multipart = "^0.0.6"
python-jose = {extras = ["cryptography"], version = "^3.3.0"}
asyncpg = "^0.29.0"
asyncio-redis = "^0.16.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.3"
pytest-asyncio = "^0.21.1"
pytest-cov = "^4.1.0"
black = "^23.11.0"
isort = "^5.12.0"
flake8 = "^6.1.0"
mypy = "^1.7.1"
pre-commit = "^3.5.0"

[tool.poetry.group.gpu]
optional = true

[tool.poetry.group.gpu.dependencies]
torch = {version = "^2.1.1", source = "pytorch-gpu"}
torchvision = {version = "^0.16.1", source = "pytorch-gpu"}
torchaudio = {version = "^2.1.1", source = "pytorch-gpu"}

[[tool.poetry.source]]
name = "pytorch-gpu"
url = "https://download.pytorch.org/whl/cu118"
priority = "explicit"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

#### **Main FastAPI Application**
```python
# apps/graphrag-engine/src/main.py

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_client import make_asgi_app, Counter, Histogram, Gauge
import uvicorn

from graphrag.config import settings
from graphrag.core.knowledge_graph import KnowledgeGraphManager
from graphrag.core.reasoning_engine import ReasoningEngine
from graphrag.core.entity_extraction import EntityExtractionPipeline
from graphrag.core.trust_scoring import TrustScoringEngine
from graphrag.services.cultural_validation import CulturalValidationService
from graphrag.services.federated_learning import FederatedLearningCoordinator
from graphrag.api.routes import graphrag_router, health_router, metrics_router
from graphrag.middleware.auth import AuthMiddleware
from graphrag.middleware.logging import LoggingMiddleware
from graphrag.middleware.tracing import TracingMiddleware
from graphrag.utils.startup import initialize_models, check_dependencies

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    'graphrag_requests_total', 
    'Total GraphRAG requests', 
    ['operation_type', 'community_id', 'success']
)

REQUEST_DURATION = Histogram(
    'graphrag_processing_duration_seconds',
    'GraphRAG processing duration',
    ['operation_type', 'complexity_level']
)

ACTIVE_REQUESTS = Gauge(
    'graphrag_active_requests',
    'Currently active GraphRAG requests'
)

MODEL_MEMORY_USAGE = Gauge(
    'graphrag_model_memory_bytes',
    'Memory usage of loaded models'
)

# Global services (initialized at startup)
knowledge_graph: KnowledgeGraphManager = None
reasoning_engine: ReasoningEngine = None
entity_extraction: EntityExtractionPipeline = None
trust_scoring: TrustScoringEngine = None
cultural_validation: CulturalValidationService = None
federated_learning: FederatedLearningCoordinator = None

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application lifespan manager for startup and shutdown."""
    
    logger.info("🚀 Starting HCCC GraphRAG Engine...")
    
    try:
        # Check system dependencies
        await check_dependencies()
        
        # Initialize core services
        global knowledge_graph, reasoning_engine, entity_extraction
        global trust_scoring, cultural_validation, federated_learning
        
        logger.info("Initializing knowledge graph manager...")
        knowledge_graph = KnowledgeGraphManager(
            uri=settings.neo4j.uri,
            user=settings.neo4j.user,
            password=settings.neo4j.password
        )
        await knowledge_graph.initialize()
        
        logger.info("Loading AI models...")
        models = await initialize_models(
            model_path=settings.models.path,
            enable_gpu=settings.models.enable_gpu
        )
        
        logger.info("Initializing entity extraction pipeline...")
        entity_extraction = EntityExtractionPipeline(
            models=models,
            knowledge_graph=knowledge_graph
        )
        
        logger.info("Initializing reasoning engine...")
        reasoning_engine = ReasoningEngine(
            knowledge_graph=knowledge_graph,
            models=models
        )
        
        logger.info("Initializing trust scoring engine...")
        trust_scoring = TrustScoringEngine(
            knowledge_graph=knowledge_graph
        )
        
        logger.info("Initializing cultural validation service...")
        cultural_validation = CulturalValidationService(
            knowledge_graph=knowledge_graph
        )
        
        if settings.federated_learning.enabled:
            logger.info("Initializing federated learning coordinator...")
            federated_learning = FederatedLearningCoordinator(
                community_id=settings.community.default_id,
                coordination_endpoint=settings.federated_learning.coordination_endpoint
            )
            await federated_learning.initialize()
        
        logger.info("✅ GraphRAG Engine initialization complete!")
        
        yield
        
    except Exception as e:
        logger.error(f"Failed to initialize GraphRAG Engine: {e}")
        raise
    
    finally:
        logger.info("🛑 Shutting down GraphRAG Engine...")
        
        # Cleanup resources
        if knowledge_graph:
            await knowledge_graph.close()
        
        if federated_learning:
            await federated_learning.shutdown()
        
        logger.info("✅ GraphRAG Engine shutdown complete")

# Create FastAPI application
app = FastAPI(
    title="HCCC GraphRAG Intelligence Engine",
    description="Graph-based Retrieval Augmented Generation for Community Coordination",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs" if settings.api.enable_docs else None,
    redoc_url="/redoc" if settings.api.enable_docs else None,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.api.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(TracingMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuthMiddleware)

# Include routers
app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(graphrag_router, prefix="/graphrag", tags=["graphrag"])
app.include_router(metrics_router, prefix="/metrics", tags=["metrics"])

# Mount Prometheus metrics
metrics_app = make_asgi_app()
app.mount("/prometheus", metrics_app)

# Dependency injection for services
async def get_knowledge_graph() -> KnowledgeGraphManager:
    if knowledge_graph is None:
        raise HTTPException(
            status_code=503, 
            detail="Knowledge graph not initialized"
        )
    return knowledge_graph

async def get_reasoning_engine() -> ReasoningEngine:
    if reasoning_engine is None:
        raise HTTPException(
            status_code=503, 
            detail="Reasoning engine not initialized"
        )
    return reasoning_engine

async def get_entity_extraction() -> EntityExtractionPipeline:
    if entity_extraction is None:
        raise HTTPException(
            status_code=503, 
            detail="Entity extraction not initialized"
        )
    return entity_extraction

async def get_trust_scoring() -> TrustScoringEngine:
    if trust_scoring is None:
        raise HTTPException(
            status_code=503, 
            detail="Trust scoring not initialized"
        )
    return trust_scoring

async def get_cultural_validation() -> CulturalValidationService:
    if cultural_validation is None:
        raise HTTPException(
            status_code=503, 
            detail="Cultural validation not initialized"
        )
    return cultural_validation

async def get_federated_learning() -> FederatedLearningCoordinator:
    if federated_learning is None:
        raise HTTPException(
            status_code=503, 
            detail="Federated learning not initialized"
        )
    return federated_learning

# Make services available globally for dependency injection
app.dependency_overrides = {
    KnowledgeGraphManager: get_knowledge_graph,
    ReasoningEngine: get_reasoning_engine,
    EntityExtractionPipeline: get_entity_extraction,
    TrustScoringEngine: get_trust_scoring,
    CulturalValidationService: get_cultural_validation,
    FederatedLearningCoordinator: get_federated_learning,
}

@app.get("/")
async def root():
    """Root endpoint with basic service information."""
    return {
        "service": "HCCC GraphRAG Intelligence Engine",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "graphrag": "/graphrag",
            "metrics": "/prometheus"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.api.host,
        port=settings.api.port,
        log_level=settings.api.log_level.lower(),
        reload=settings.api.reload,
        workers=1 if settings.api.reload else settings.api.workers,
    )
```

#### **Configuration Management**
```python
# apps/graphrag-engine/src/graphrag/config.py

import os
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

class Neo4jConfig(BaseModel):
    uri: str = Field(default="bolt://localhost:7687")
    user: str = Field(default="neo4j")
    password: str = Field(default="dev-password")
    max_connection_lifetime: int = Field(default=3600)
    max_connection_pool_size: int = Field(default=50)

class RedisConfig(BaseModel):
    host: str = Field(default="localhost")
    port: int = Field(default=6379)
    password: Optional[str] = Field(default=None)
    db: int = Field(default=0)
    max_connections: int = Field(default=20)

class PostgresConfig(BaseModel):
    host: str = Field(default="localhost")
    port: int = Field(default=5432)
    database: str = Field(default="hccc")
    user: str = Field(default="hccc")
    password: str = Field(default="dev-password")
    pool_size: int = Field(default=20)
    max_overflow: int = Field(default=0)

class ModelsConfig(BaseModel):
    path: str = Field(default="./models")
    enable_gpu: bool = Field(default=False)
    gpu_memory_fraction: float = Field(default=0.8)
    
    # Language models
    text_embedding_model: str = Field(default="sentence-transformers/all-MiniLM-L6-v2")
    text_generation_model: str = Field(default="microsoft/DialoGPT-medium")
    
    # NLP models
    spacy_model: str = Field(default="en_core_web_sm")
    kreyol_model: Optional[str] = Field(default=None)
    
    # Graph models
    node_classification_model: Optional[str] = Field(default=None)
    link_prediction_model: Optional[str] = Field(default=None)

class CommunityConfig(BaseModel):
    default_id: str = Field(default="dev-community-001")
    data_sovereignty_enabled: bool = Field(default=True)
    cultural_validation_enabled: bool = Field(default=True)
    trust_threshold: float = Field(default=0.7)

class FederatedLearningConfig(BaseModel):
    enabled: bool = Field(default=False)
    coordination_endpoint: Optional[str] = Field(default=None)
    min_participants: int = Field(default=3)
    privacy_budget_epsilon: float = Field(default=1.0)
    privacy_budget_delta: float = Field(default=1e-5)

class APIConfig(BaseModel):
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8000)
    workers: int = Field(default=1)
    reload: bool = Field(default=False)
    log_level: str = Field(default="INFO")
    enable_docs: bool = Field(default=True)
    cors_origins: List[str] = Field(default=["*"])
    max_request_size: int = Field(default=10 * 1024 * 1024)  # 10MB

class MonitoringConfig(BaseModel):
    enable_prometheus: bool = Field(default=True)
    enable_jaeger: bool = Field(default=True)
    jaeger_endpoint: str = Field(default="http://localhost:14268/api/traces")
    log_requests: bool = Field(default=True)

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Environment
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    
    # Database configurations
    neo4j: Neo4jConfig = Field(default_factory=Neo4jConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
    
    # AI/ML configurations
    models: ModelsConfig = Field(default_factory=ModelsConfig)
    
    # Community configurations
    community: CommunityConfig = Field(default_factory=CommunityConfig)
    
    # Federated learning
    federated_learning: FederatedLearningConfig = Field(default_factory=FederatedLearningConfig)
    
    # API configurations
    api: APIConfig = Field(default_factory=APIConfig)
    
    # Monitoring
    monitoring: MonitoringConfig = Field(default_factory=MonitoringConfig)
    
    # Security
    jwt_secret: str = Field(default="dev-secret-key")
    
    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
        case_sensitive = False

# Create global settings instance
settings = Settings()

# Validate critical settings
if settings.environment == "production":
    assert settings.neo4j.password != "dev-password", "Change Neo4j password for production"
    assert settings.jwt_secret != "dev-secret-key", "Change JWT secret for production"
    assert not settings.debug, "Disable debug mode for production"
```

### 7.2 Core GraphRAG Components

#### **Knowledge Graph Manager**
```python
# apps/graphrag-engine/src/graphrag/core/knowledge_graph.py

import asyncio
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import structlog
from neo4j import AsyncGraphDatabase, AsyncDriver, AsyncSession
from neo4j.exceptions import ServiceUnavailable, TransientError

from graphrag.models.entities import KnowledgeGraphEntity, KnowledgeGraphRelationship
from graphrag.models.queries import GraphQuery, QueryResult
from graphrag.config import Neo4jConfig

logger = structlog.get_logger(__name__)

class KnowledgeGraphManager:
    """Manages the Neo4j knowledge graph with async operations."""
    
    def __init__(self, uri: str, user: str, password: str):
        self.uri = uri
        self.user = user
        self.password = password
        self.driver: Optional[AsyncDriver] = None
        self._initialized = False

    async def initialize(self) -> None:
        """Initialize the connection to Neo4j."""
        try:
            self.driver = AsyncGraphDatabase.driver(
                self.uri,
                auth=(self.user, self.password),
                max_connection_lifetime=3600,
                max_connection_pool_size=50,
                connection_acquisition_timeout=60,
                connection_timeout=60,
                max_retry_time=30,
            )
            
            # Verify connectivity
            await self.driver.verify_connectivity()
            
            # Initialize schema
            await self._initialize_schema()
            
            self._initialized = True
            logger.info("Knowledge graph manager initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize knowledge graph: {e}")
            raise

    async def close(self) -> None:
        """Close the connection to Neo4j."""
        if self.driver:
            await self.driver.close()
            logger.info("Knowledge graph connection closed")

    async def _initialize_schema(self) -> None:
        """Initialize the knowledge graph schema."""
        schema_queries = [
            # Constraints
            "CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE",
            "CREATE CONSTRAINT community_id IF NOT EXISTS FOR (c:Community) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT person_id IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT organization_id IF NOT EXISTS FOR (o:Organization) REQUIRE o.id IS UNIQUE",
            "CREATE CONSTRAINT event_id IF NOT EXISTS FOR (ev:Event) REQUIRE ev.id IS UNIQUE",
            
            # Indexes
            "CREATE INDEX entity_type IF NOT EXISTS FOR (e:Entity) ON (e.type)",
            "CREATE INDEX entity_trust_score IF NOT EXISTS FOR (e:Entity) ON (e.trustScore)",
            "CREATE INDEX entity_timestamp IF NOT EXISTS FOR (e:Entity) ON (e.timestamp)",
            "CREATE INDEX relationship_type IF NOT EXISTS FOR ()-[r]-() ON (r.type)",
            "CREATE INDEX relationship_confidence IF NOT EXISTS FOR ()-[r]-() ON (r.confidence)",
            
            # Full-text search
            "CREATE FULLTEXT INDEX entity_search IF NOT EXISTS FOR (e:Entity) ON EACH [e.name, e.description, e.content]",
        ]
        
        async with self.driver.session() as session:
            for query in schema_queries:
                try:
                    await session.run(query)
                except Exception as e:
                    logger.warning(f"Schema query failed (may already exist): {query[:50]}... Error: {e}")

    async def add_entity(self, entity: KnowledgeGraphEntity) -> str:
        """Add an entity to the knowledge graph."""
        if not self._initialized:
            raise RuntimeError("Knowledge graph not initialized")
        
        query = """
        MERGE (e:Entity {id: $id})
        SET e += $properties
        SET e.lastUpdated = datetime()
        RETURN e.id as id
        """
        
        parameters = {
            "id": entity.id,
            "properties": {
                "type": entity.type,
                "name": entity.properties.get("name", ""),
                "description": entity.properties.get("description", ""),
                "trustScore": entity.trust_score,
                "reliabilityScore": entity.reliability_score,
                "communityValidated": entity.community_validated,
                "sourceIds": entity.source_ids,
                **entity.properties
            }
        }
        
        async with self.driver.session() as session:
            result = await session.run(query, parameters)
            record = await result.single()
            
            logger.debug(f"Added entity: {entity.id}")
            return record["id"]

    async def add_relationship(self, relationship: KnowledgeGraphRelationship) -> str:
        """Add a relationship between entities."""
        if not self._initialized:
            raise RuntimeError("Knowledge graph not initialized")
        
        query = """
        MATCH (source:Entity {id: $source_id})
        MATCH (target:Entity {id: $target_id})
        MERGE (source)-[r:RELATES {type: $rel_type}]->(target)
        SET r += $properties
        SET r.lastUpdated = datetime()
        RETURN r.type as relationship_type
        """
        
        parameters = {
            "source_id": relationship.source_entity,
            "target_id": relationship.target_entity,
            "rel_type": relationship.relationship_type,
            "properties": {
                "confidence": relationship.confidence,
                "evidence": relationship.evidence,
                "causalStrength": relationship.causal_strength,
                **relationship.properties
            }
        }
        
        async with self.driver.session() as session:
            result = await session.run(query, parameters)
            record = await result.single()
            
            logger.debug(f"Added relationship: {relationship.source_entity} -> {relationship.target_entity}")
            return record["relationship_type"]

    async def execute_cypher(self, query: str, parameters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Execute a raw Cypher query."""
        if not self._initialized:
            raise RuntimeError("Knowledge graph not initialized")
        
        async with self.driver.session() as session:
            try:
                result = await session.run(query, parameters or {})
                records = await result.data()
                return records
            except (ServiceUnavailable, TransientError) as e:
                logger.error(f"Neo4j connection error: {e}")
                raise
            except Exception as e:
                logger.error(f"Cypher query failed: {query[:100]}... Error: {e}")
                raise

    async def find_causal_paths(
        self, 
        start_entity: str, 
        target_entities: List[str],
        max_hops: int = 5,
        min_confidence: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Find causal paths between entities."""
        
        query = """
        MATCH path = (start:Entity {id: $start_id})-[r:RELATES*1..$max_hops]->(target:Entity)
        WHERE target.id IN $target_ids
        AND ALL(rel in relationships(path) WHERE rel.confidence >= $min_confidence)
        WITH path, 
             nodes(path) as path_nodes,
             relationships(path) as path_rels,
             reduce(conf = 1.0, rel in relationships(path) | conf * rel.confidence) as path_confidence,
             reduce(strength = 1.0, rel in relationships(path) | 
                CASE WHEN rel.causalStrength IS NOT NULL 
                THEN strength * rel.causalStrength 
                ELSE strength * 0.5 END) as causal_strength
        WHERE path_confidence >= $min_confidence
        RETURN {
            path: path,
            nodes: [node in path_nodes | {id: node.id, type: node.type, name: node.name}],
            relationships: [rel in path_rels | {type: rel.type, confidence: rel.confidence}],
            pathConfidence: path_confidence,
            causalStrength: causal_strength
        } as result
        ORDER BY causal_strength DESC, path_confidence DESC
        LIMIT 20
        """
        
        parameters = {
            "start_id": start_entity,
            "target_ids": target_entities,
            "max_hops": max_hops,
            "min_confidence": min_confidence
        }
        
        results = await self.execute_cypher(query, parameters)
        return [record["result"] for record in results]

    async def get_entity_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Get an entity by its ID."""
        query = """
        MATCH (e:Entity {id: $entity_id})
        RETURN {
            id: e.id,
            type: e.type,
            name: e.name,
            description: e.description,
            trustScore: e.trustScore,
            reliabilityScore: e.reliabilityScore,
            communityValidated: e.communityValidated,
            properties: properties(e)
        } as entity
        """
        
        results = await self.execute_cypher(query, {"entity_id": entity_id})
        return results[0]["entity"] if results else None

    async def search_entities(
        self, 
        search_term: str, 
        entity_types: Optional[List[str]] = None,
        community_id: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search entities using full-text search."""
        
        # Build the query dynamically based on filters
        where_clauses = []
        if entity_types:
            where_clauses.append("e.type IN $entity_types")
        if community_id:
            where_clauses.append("e.communityId = $community_id")
        
        where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
        
        query = f"""
        CALL db.index.fulltext.queryNodes('entity_search', $search_term) YIELD node as e, score
        {where_clause}
        RETURN {{
            id: e.id,
            type: e.type,
            name: e.name,
            description: e.description,
            trustScore: e.trustScore,
            searchScore: score
        }} as entity
        ORDER BY score DESC
        LIMIT $limit
        """
        
        parameters = {
            "search_term": search_term,
            "limit": limit
        }
        
        if entity_types:
            parameters["entity_types"] = entity_types
        if community_id:
            parameters["community_id"] = community_id
        
        results = await self.execute_cypher(query, parameters)
        return [record["entity"] for record in results]

    async def get_community_entities(self, community_id: str) -> Dict[str, Any]:
        """Get all entities related to a specific community."""
        query = """
        MATCH (c:Community {id: $community_id})
        OPTIONAL MATCH (c)-[:CONTAINS|OWNS|OPERATES*1..2]-(e:Entity)
        WITH c, collect(DISTINCT e) as entities
        RETURN {
            community: {
                id: c.id,
                name: c.name,
                region: c.region,
                governanceType: c.governanceType
            },
            entities: [entity in entities | {
                id: entity.id,
                type: entity.type,
                name: entity.name,
                trustScore: entity.trustScore
            }],
            entityCount: size(entities)
        } as result
        """
        
        results = await self.execute_cypher(query, {"community_id": community_id})
        return results[0]["result"] if results else None

    async def get_graph_statistics(self) -> Dict[str, Any]:
        """Get basic statistics about the knowledge graph."""
        query = """
        MATCH (e:Entity)
        WITH count(e) as totalEntities
        MATCH ()-[r:RELATES]->()
        WITH totalEntities, count(r) as totalRelationships
        MATCH (e:Entity)
        WITH totalEntities, totalRelationships, 
             avg(e.trustScore) as avgTrustScore,
             count(CASE WHEN e.communityValidated = true THEN 1 END) as validatedEntities
        RETURN {
            totalEntities: totalEntities,
            totalRelationships: totalRelationships,
            averageTrustScore: avgTrustScore,
            validatedEntities: validatedEntities,
            validationRate: toFloat(validatedEntities) / totalEntities
        } as stats
        """
        
        results = await self.execute_cypher(query)
        return results[0]["stats"] if results else {}
```

#### **Entity Extraction Pipeline**
```python
# apps/graphrag-engine/src/graphrag/core/entity_extraction.py

import asyncio
from typing import List, Dict, Any, Optional, Tuple
import spacy
from spacy import displacy
import torch
from transformers import pipeline, AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer
import structlog

from graphrag.models.entities import KnowledgeGraphEntity, KnowledgeGraphRelationship
from graphrag.models.extraction import (
    ExtractionResult, 
    MultiModalData, 
    TextDocument, 
    ImageData, 
    VideoData, 
    SensorData
)
from graphrag.core.knowledge_graph import KnowledgeGraphManager
from graphrag.services.cultural_validation import CulturalValidationService
from graphrag.utils.text_processing import detect_language, clean_text

logger = structlog.get_logger(__name__)

class EntityExtractionPipeline:
    """Multi-modal entity extraction pipeline with cultural awareness."""
    
    def __init__(self, models: Dict[str, Any], knowledge_graph: KnowledgeGraphManager):
        self.knowledge_graph = knowledge_graph
        self.models = models
        
        # Language models
        self.nlp_en = spacy.load("en_core_web_sm")
        self.nlp_kreyol = self._load_kreyol_model() if models.get("kreyol_model") else None
        
        # Embedding model for similarity
        self.embedding_model = SentenceTransformer(models.get("embedding_model", "all-MiniLM-L6-v2"))
        
        # Relation extraction model
        self.relation_extractor = self._initialize_relation_extractor()
        
        # Cultural validation
        self.cultural_validator: Optional[CulturalValidationService] = None
        
        logger.info("Entity extraction pipeline initialized")

    def set_cultural_validator(self, validator: CulturalValidationService):
        """Set the cultural validation service."""
        self.cultural_validator = validator

    def _load_kreyol_model(self) -> Optional[spacy.Language]:
        """Load Kreyòl language model if available."""
        try:
            # This would load a custom Kreyòl model if available
            # For now, we'll use the English model with custom rules
            nlp = spacy.blank("ht")  # Haitian Creole language code
            
            # Add custom components for Kreyòl processing
            # This is a placeholder - in production, you'd train a proper model
            return nlp
        except Exception as e:
            logger.warning(f"Could not load Kreyòl model: {e}")
            return None

    def _initialize_relation_extractor(self):
        """Initialize relation extraction model."""
        try:
            # Use a pre-trained model for relation extraction
            return pipeline(
                "text-classification",
                model="microsoft/DialoGPT-medium",
                return_all_scores=True
            )
        except Exception as e:
            logger.warning(f"Could not initialize relation extractor: {e}")
            return None

    async def extract_from_multi_modal_data(
        self, 
        data: MultiModalData,
        community_context: Optional[Dict[str, Any]] = None
    ) -> ExtractionResult:
        """Extract entities and relationships from multi-modal data."""
        
        logger.info(f"Starting multi-modal extraction for {len(data.text_content)} text documents")
        
        all_entities = []
        all_relationships = []
        
        # Extract from text content
        if data.text_content:
            text_results = await self._extract_from_text(data.text_content, community_context)
            all_entities.extend(text_results.entities)
            all_relationships.extend(text_results.relationships)
        
        # Extract from images
        if data.images:
            image_results = await self._extract_from_images(data.images, community_context)
            all_entities.extend(image_results.entities)
            all_relationships.extend(image_results.relationships)
        
        # Extract from sensor data
        if data.sensor_readings:
            sensor_results = await self._extract_from_sensors(data.sensor_readings, community_context)
            all_entities.extend(sensor_results.entities)
            all_relationships.extend(sensor_results.relationships)
        
        # Extract from video data
        if data.videos:
            video_results = await self._extract_from_videos(data.videos, community_context)
            all_entities.extend(video_results.entities)
            all_relationships.extend(video_results.relationships)
        
        # Resolve cross-modal entities
        resolved_entities = await self._resolve_cross_modal_entities(all_entities)
        
        # Apply cultural validation if available
        if self.cultural_validator and community_context:
            validated_entities = []
            for entity in resolved_entities:
                validation_result = await self.cultural_validator.validate_entity(
                    entity, community_context
                )
                if validation_result.approved:
                    entity.community_validated = True
                    validated_entities.append(entity)
                else:
                    logger.warning(f"Entity {entity.id} failed cultural validation: {validation_result.concerns}")
            
            resolved_entities = validated_entities
        
        return ExtractionResult(
            entities=resolved_entities,
            relationships=all_relationships,
            metadata={
                "extraction_timestamp": datetime.now().isoformat(),
                "community_context": community_context,
                "total_sources": len(data.text_content) + len(data.images) + len(data.sensor_readings) + len(data.videos),
                "cultural_validation_applied": self.cultural_validator is not None
            }
        )

    async def _extract_from_text(
        self, 
        text_documents: List[TextDocument],
        community_context: Optional[Dict[str, Any]] = None
    ) -> ExtractionResult:
        """Extract entities and relationships from text documents."""
        
        entities = []
        relationships = []
        
        for doc in text_documents:
            try:
                # Detect language
                language = detect_language(doc.content)
                
                # Choose appropriate NLP model
                if language == "kreyol" and self.nlp_kreyol:
                    nlp = self.nlp_kreyol
                else:
                    nlp = self.nlp_en
                
                # Clean and process text
                cleaned_text = clean_text(doc.content)
                processed_doc = nlp(cleaned_text)
                
                # Extract named entities
                for ent in processed_doc.ents:
                    entity = KnowledgeGraphEntity(
                        id=self._generate_entity_id(ent.text, ent.label_),
                        type=self._map_spacy_label_to_type(ent.label_),
                        properties={
                            "name": ent.text,
                            "text": ent.text,
                            "start_char": ent.start_char,
                            "end_char": ent.end_char,
                            "confidence": getattr(ent, "_.confidence", 0.8),
                            "language": language,
                            "source_document": doc.source_id,
                            "context": doc.content[max(0, ent.start_char-50):ent.end_char+50]
                        },
                        trust_score=0.0,  # Will be calculated by trust scoring engine
                        reliability_score=0.0,
                        last_updated=datetime.now(),
                        source_ids=[doc.source_id],
                        community_validated=False
                    )
                    entities.append(entity)
                
                # Extract relationships using dependency parsing
                doc_relationships = await self._extract_relationships_from_doc(processed_doc, doc.source_id)
                relationships.extend(doc_relationships)
                
            except Exception as e:
                logger.error(f"Failed to process text document {doc.source_id}: {e}")
                continue
        
        return ExtractionResult(
            entities=entities,
            relationships=relationships,
            metadata={"extractor": "text", "documents_processed": len(text_documents)}
        )

    async def _extract_from_images(
        self, 
        images: List[ImageData],
        community_context: Optional[Dict[str, Any]] = None
    ) -> ExtractionResult:
        """Extract entities from images using computer vision."""
        
        entities = []
        relationships = []
        
        # Placeholder for image processing
        # In a full implementation, you would use:
        # - Object detection models (YOLO, R-CNN)
        # - OCR for text in images (Tesseract, PaddleOCR)
        # - Scene classification
        # - Facial recognition (with privacy considerations)
        
        for image in images:
            try:
                # Extract metadata entities
                metadata_entity = KnowledgeGraphEntity(
                    id=f"image_{image.image_id}",
                    type="image_document",
                    properties={
                        "image_id": image.image_id,
                        "timestamp": image.timestamp.isoformat() if image.timestamp else None,
                        "location": image.location,
                        "camera_info": image.metadata.get("camera_info", {}),
                        "file_size": image.metadata.get("file_size"),
                        "resolution": image.metadata.get("resolution")
                    },
                    trust_score=0.8,  # Images generally have higher trust
                    reliability_score=0.8,
                    last_updated=datetime.now(),
                    source_ids=[image.image_id],
                    community_validated=False
                )
                entities.append(metadata_entity)
                
                # TODO: Implement actual computer vision processing
                # - Object detection
                # - OCR text extraction
                # - Location/landmark recognition
                # - Activity recognition
                
            except Exception as e:
                logger.error(f"Failed to process image {image.image_id}: {e}")
                continue
        
        return ExtractionResult(
            entities=entities,
            relationships=relationships,
            metadata={"extractor": "image", "images_processed": len(images)}
        )

    async def _extract_from_sensors(
        self, 
        sensor_data: List[SensorData],
        community_context: Optional[Dict[str, Any]] = None
    ) -> ExtractionResult:
        """Extract entities from IoT sensor data."""
        
        entities = []
        relationships = []
        
        for sensor in sensor_data:
            try:
                # Create sensor entity
                sensor_entity = KnowledgeGraphEntity(
                    id=f"sensor_{sensor.sensor_id}",
                    type="iot_sensor",
                    properties={
                        "sensor_id": sensor.sensor_id,
                        "sensor_type": sensor.sensor_type,
                        "location": sensor.location,
                        "current_value": sensor.value,
                        "unit": sensor.unit,
                        "timestamp": sensor.timestamp.isoformat(),
                        "quality": sensor.quality
                    },
                    trust_score=0.9,  # IoT sensors are generally reliable
                    reliability_score=0.85,
                    last_updated=datetime.now(),
                    source_ids=[sensor.sensor_id],
                    community_validated=True  # Sensors are community-owned
                )
                entities.append(sensor_entity)
                
                # Create reading entity if significant
                if self._is_significant_reading(sensor):
                    reading_entity = KnowledgeGraphEntity(
                        id=f"reading_{sensor.sensor_id}_{int(sensor.timestamp.timestamp())}",
                        type="sensor_reading",
                        properties={
                            "sensor_id": sensor.sensor_id,
                            "value": sensor.value,
                            "unit": sensor.unit,
                            "timestamp": sensor.timestamp.isoformat(),
                            "significance_level": self._calculate_significance(sensor),
                            "alert_level": self._determine_alert_level(sensor)
                        },
                        trust_score=0.95,
                        reliability_score=0.9,
                        last_updated=datetime.now(),
                        source_ids=[sensor.sensor_id],
                        community_validated=True
                    )
                    entities.append(reading_entity)
                    
                    # Create relationship between sensor and reading
                    relationship = KnowledgeGraphRelationship(
                        id=f"sensor_reading_{sensor.sensor_id}_{int(sensor.timestamp.timestamp())}",
                        source_entity=sensor_entity.id,
                        target_entity=reading_entity.id,
                        relationship_type="PRODUCES",
                        properties={
                            "timestamp": sensor.timestamp.isoformat()
                        },
                        confidence=0.95,
                        evidence=[f"Direct sensor measurement from {sensor.sensor_id}"]
                    )
                    relationships.append(relationship)
                
            except Exception as e:
                logger.error(f"Failed to process sensor data {sensor.sensor_id}: {e}")
                continue
        
        return ExtractionResult(
            entities=entities,
            relationships=relationships,
            metadata={"extractor": "sensor", "sensors_processed": len(sensor_data)}
        )

    async def _extract_from_videos(
        self, 
        videos: List[VideoData],
        community_context: Optional[Dict[str, Any]] = None
    ) -> ExtractionResult:
        """Extract entities from video data."""
        
        entities = []
        relationships = []
        
        # Placeholder for video processing
        # In a full implementation, you would use:
        # - Video activity recognition
        # - Object tracking
        # - Speech-to-text for audio
        # - Scene segmentation
        # - Motion analysis
        
        for video in videos:
            try:
                # Extract basic video metadata entity
                video_entity = KnowledgeGraphEntity(
                    id=f"video_{video.video_id}",
                    type="video_document",
                    properties={
                        "video_id": video.video_id,
                        "duration": video.duration,
                        "timestamp": video.timestamp.isoformat() if video.timestamp else None,
                        "location": video.location,
                        "camera_info": video.metadata.get("camera_info", {}),
                        "file_size": video.metadata.get("file_size"),
                        "resolution": video.metadata.get("resolution"),
                        "frame_rate": video.metadata.get("frame_rate")
                    },
                    trust_score=0.8,
                    reliability_score=0.8,
                    last_updated=datetime.now(),
                    source_ids=[video.video_id],
                    community_validated=False
                )
                entities.append(video_entity)
                
                # TODO: Implement actual video processing
                # - Extract keyframes for image analysis
                # - Audio extraction and speech recognition
                # - Activity recognition
                # - Object tracking and identification
                
            except Exception as e:
                logger.error(f"Failed to process video {video.video_id}: {e}")
                continue
        
        return ExtractionResult(
            entities=entities,
            relationships=relationships,
            metadata={"extractor": "video", "videos_processed": len(videos)}
        )

    async def _extract_relationships_from_doc(
        self, 
        doc: spacy.tokens.Doc, 
        source_id: str
    ) -> List[KnowledgeGraphRelationship]:
        """Extract relationships from spaCy document using dependency parsing."""
        
        relationships = []
        
        # Use dependency parsing to find relationships
        for token in doc:
            if token.dep_ in ["nsubj", "dobj", "pobj"] and token.head.pos_ == "VERB":
                # Found a subject-verb-object relationship
                subject = token.text
                verb = token.head.text
                
                # Find object
                obj = None
                for child in token.head.children:
                    if child.dep_ in ["dobj", "pobj"]:
                        obj = child.text
                        break
                
                if obj:
                    relationship = KnowledgeGraphRelationship(
                        id=f"rel_{hash(f'{subject}_{verb}_{obj}_{source_id}')}",
                        source_entity=self._generate_entity_id(subject, "ENTITY"),
                        target_entity=self._generate_entity_id(obj, "ENTITY"),
                        relationship_type=verb.upper(),
                        properties={
                            "verb": verb,
                            "sentence": token.sent.text,
                            "source_document": source_id
                        },
                        confidence=0.7,  # Medium confidence for dependency parsing
                        evidence=[f"Dependency parsing from: {token.sent.text}"]
                    )
                    relationships.append(relationship)
        
        return relationships

    async def _resolve_cross_modal_entities(
        self, 
        entities: List[KnowledgeGraphEntity]
    ) -> List[KnowledgeGraphEntity]:
        """Resolve duplicate entities across different modalities."""
        
        if not entities:
            return entities
        
        # Group entities by type for similarity comparison
        entity_groups = {}
        for entity in entities:
            entity_type = entity.type
            if entity_type not in entity_groups:
                entity_groups[entity_type] = []
            entity_groups[entity_type].append(entity)
        
        resolved_entities = []
        
        for entity_type, group_entities in entity_groups.items():
            if len(group_entities) <= 1:
                resolved_entities.extend(group_entities)
                continue
            
            # Calculate embeddings for entity names/descriptions
            texts = []
            for entity in group_entities:
                text = entity.properties.get("name", "") + " " + entity.properties.get("description", "")
                texts.append(text.strip())
            
            try:
                embeddings = self.embedding_model.encode(texts)
                
                # Find similar entities using cosine similarity
                used_indices = set()
                
                for i, entity in enumerate(group_entities):
                    if i in used_indices:
                        continue
                    
                    similar_indices = [i]
                    
                    for j, other_entity in enumerate(group_entities[i+1:], i+1):
                        if j in used_indices:
                            continue
                        
                        # Calculate cosine similarity
                        similarity = torch.cosine_similarity(
                            torch.tensor(embeddings[i]).unsqueeze(0),
                            torch.tensor(embeddings[j]).unsqueeze(0)
                        ).item()
                        
                        if similarity > 0.85:  # High similarity threshold
                            similar_indices.append(j)
                    
                    # Merge similar entities
                    if len(similar_indices) > 1:
                        merged_entity = self._merge_entities([group_entities[idx] for idx in similar_indices])
                        resolved_entities.append(merged_entity)
                        used_indices.update(similar_indices)
                    else:
                        resolved_entities.append(entity)
                        used_indices.add(i)
                
            except Exception as e:
                logger.error(f"Failed to resolve cross-modal entities: {e}")
                # Fallback: return all entities without merging
                resolved_entities.extend(group_entities)
        
        return resolved_entities

    def _merge_entities(self, entities: List[KnowledgeGraphEntity]) -> KnowledgeGraphEntity:
        """Merge multiple similar entities into one."""
        
        # Use the entity with highest trust score as base
        base_entity = max(entities, key=lambda e: e.trust_score)
        
        # Merge properties
        merged_properties = base_entity.properties.copy()
        all_source_ids = set(base_entity.source_ids)
        
        for entity in entities:
            if entity.id != base_entity.id:
                # Merge properties (prefer higher trust score)
                for key, value in entity.properties.items():
                    if key not in merged_properties or entity.trust_score > base_entity.trust_score:
                        merged_properties[key] = value
                
                all_source_ids.update(entity.source_ids)
        
        # Create merged entity
        merged_entity = KnowledgeGraphEntity(
            id=base_entity.id,
            type=base_entity.type,
            properties=merged_properties,
            trust_score=max(e.trust_score for e in entities),
            reliability_score=sum(e.reliability_score for e in entities) / len(entities),
            last_updated=datetime.now(),
            source_ids=list(all_source_ids),
            community_validated=any(e.community_validated for e in entities)
        )
        
        return merged_entity

    def _generate_entity_id(self, text: str, entity_type: str) -> str:
        """Generate a consistent entity ID."""
        import hashlib
        content = f"{text.lower()}_{entity_type.lower()}"
        return f"entity_{hashlib.md5(content.encode()).hexdigest()[:12]}"

    def _map_spacy_label_to_type(self, spacy_label: str) -> str:
        """Map spaCy entity labels to our entity types."""
        mapping = {
            "PERSON": "person",
            "ORG": "organization", 
            "GPE": "location",
            "LOC": "location",
            "EVENT": "event",
            "PRODUCT": "product",
            "WORK_OF_ART": "cultural_artifact",
            "LAW": "governance_document",
            "LANGUAGE": "language",
            "DATE": "temporal",
            "TIME": "temporal",
            "PERCENT": "metric",
            "MONEY": "economic",
            "QUANTITY": "resource",
            "ORDINAL": "metric",
            "CARDINAL": "metric"
        }
        return mapping.get(spacy_label, "entity")

    def _is_significant_reading(self, sensor: SensorData) -> bool:
        """Determine if a sensor reading is significant enough to create an entity."""
        # Implement logic based on sensor type and value thresholds
        if sensor.sensor_type == "temperature" and abs(sensor.value) > 35:  # Hot temperature
            return True
        elif sensor.sensor_type == "humidity" and sensor.value > 80:  # High humidity
            return True
        elif sensor.sensor_type == "flood_level" and sensor.value > 0.5:  # Flood warning
            return True
        elif sensor.sensor_type == "air_quality" and sensor.value > 150:  # Poor air quality
            return True
        
        return False

    def _calculate_significance(self, sensor: SensorData) -> float:
        """Calculate the significance level of a sensor reading."""
        # Implement domain-specific significance calculation
        # This is a placeholder implementation
        if sensor.sensor_type == "flood_level":
            return min(sensor.value / 2.0, 1.0)  # Normalize to 0-1
        elif sensor.sensor_type == "temperature":
            return min(abs(sensor.value - 25) / 20.0, 1.0)  # Distance from comfortable temp
        else:
            return 0.5  # Default medium significance

    def _determine_alert_level(self, sensor: SensorData) -> str:
        """Determine alert level for sensor reading."""
        significance = self._calculate_significance(sensor)
        
        if significance > 0.8:
            return "critical"
        elif significance > 0.6:
            return "high"
        elif significance > 0.4:
            return "medium"
        else:
            return "low"
```

### 7.3 Reasoning Engine

#### **Multi-Hop Reasoning Implementation**
```python
# apps/graphrag-engine/src/graphrag/core/reasoning_engine.py

import asyncio
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from dataclasses import dataclass
import structlog

from graphrag.core.knowledge_graph import KnowledgeGraphManager
from graphrag.models.reasoning import (
    CausalAnalysisRequest,
    CausalAnalysisResult,
    CausalChain,
    InterventionPoint,
    PredictiveAnalysisRequest,
    PredictiveAnalysisResult,
    ConfidenceInterval
)
from graphrag.services.cultural_validation import CulturalValidationService

logger = structlog.get_logger(__name__)

@dataclass
class ReasoningContext:
    """Context for reasoning operations."""
    community_id: str
    cultural_context: Dict[str, Any]
    trust_threshold: float = 0.7
    max_reasoning_depth: int = 5
    enable_cultural_validation: bool = True

class ReasoningEngine:
    """Advanced reasoning engine for causal analysis and prediction."""
    
    def __init__(self, knowledge_graph: KnowledgeGraphManager, models: Dict[str, Any]):
        self.knowledge_graph = knowledge_graph
        self.models = models
        self.cultural_validator: Optional[CulturalValidationService] = None
        
        # Reasoning parameters
        self.default_confidence_threshold = 0.6
        self.max_causal_chain_length = 10
        self.intervention_effectiveness_threshold = 0.5
        
        logger.info("Reasoning engine initialized")

    def set_cultural_validator(self, validator: CulturalValidationService):
        """Set cultural validation service."""
        self.cultural_validator = validator

    async def analyze_causal_chains(
        self, 
        request: CausalAnalysisRequest,
        context: ReasoningContext
    ) -> CausalAnalysisResult:
        """Analyze causal relationships between events and outcomes."""
        
        logger.info(f"Starting causal analysis: {request.start_event} -> {request.target_outcomes}")
        
        # Validate cultural appropriateness if enabled
        if context.enable_cultural_validation and self.cultural_validator:
            await self._validate_analysis_culturally_appropriate(request, context)
        
        # Find causal paths in knowledge graph
        causal_paths = await self.knowledge_graph.find_causal_paths(
            start_entity=request.start_event,
            target_entities=request.target_outcomes,
            max_hops=context.max_reasoning_depth,
            min_confidence=context.trust_threshold
        )
        
        if not causal_paths:
            return CausalAnalysisResult(
                causal_chains=[],
                intervention_recommendations=[],
                confidence_assessment=ConfidenceInterval(average=0.0, lower=0.0, upper=0.0),
                cultural_considerations=[],
                uncertainty_analysis={"message": "No causal paths found"}
            )
        
        # Convert to causal chains with analysis
        causal_chains = []
        for path_data in causal_paths:
            chain = await self._analyze_causal_path(path_data, context)
            if chain:
                causal_chains.append(chain)
        
        # Sort by causal strength
        causal_chains.sort(key=lambda c: c.causal_strength, reverse=True)
        
        # Generate intervention recommendations
        intervention_recommendations = await self._generate_intervention_recommendations(
            causal_chains, context
        )
        
        # Calculate overall confidence
        confidence_assessment = self._calculate_confidence_assessment(causal_chains)
        
        # Extract cultural considerations
        cultural_considerations = await self._extract_cultural_considerations(
            causal_chains, context
        )
        
        # Perform uncertainty analysis
        uncertainty_analysis = self._analyze_uncertainty(causal_chains, context)
        
        return CausalAnalysisResult(
            causal_chains=causal_chains,
            intervention_recommendations=intervention_recommendations,
            confidence_assessment=confidence_assessment,
            cultural_considerations=cultural_considerations,
            uncertainty_analysis=uncertainty_analysis
        )

    async def _analyze_causal_path(
        self, 
        path_data: Dict[str, Any], 
        context: ReasoningContext
    ) -> Optional[CausalChain]:
        """Analyze a single causal path and convert to CausalChain."""
        
        try:
            # Extract path information
            nodes = path_data["nodes"]
            relationships = path_data["relationships"]
            path_confidence = path_data["pathConfidence"]
            causal_strength = path_data["causalStrength"]
            
            # Identify intervention points
            intervention_points = await self._identify_intervention_points(
                nodes, relationships, context
            )
            
            # Calculate intervention effectiveness for each point
            for point in intervention_points:
                point.effectiveness = await self._calculate_intervention_effectiveness(
                    point, nodes, relationships, context
                )
                point.feasibility = await self._assess_intervention_feasibility(
                    point, context
                )
                point.community_acceptance = await self._assess_community_acceptance(
                    point, context
                )
            
            # Sort intervention points by effectiveness
            intervention_points.sort(key=lambda p: p.effectiveness, reverse=True)
            
            return CausalChain(
                path_id=f"chain_{hash(str(nodes))}",
                nodes=nodes,
                relationships=relationships,
                confidence=path_confidence,
                causal_strength=causal_strength,
                intervention_points=intervention_points[:5],  # Top 5 intervention points
                evidence_quality=self._assess_evidence_quality(relationships),
                temporal_consistency=self._check_temporal_consistency(nodes)
            )
            
        except Exception as e:
            logger.error(f"Failed to analyze causal path: {e}")
            return None

    async def _identify_intervention_points(
        self, 
        nodes: List[Dict[str, Any]], 
        relationships: List[Dict[str, Any]],
        context: ReasoningContext
    ) -> List[InterventionPoint]:
        """Identify potential intervention points in a causal chain."""
        
        intervention_points = []
        
        # Skip the last node (target outcome) when looking for intervention points
        for i, node in enumerate(nodes[:-1]):
            
            # Calculate the potential impact of intervening at this node
            downstream_impact = len(nodes) - i - 1  # Number of downstream nodes
            
            # Check if intervention at this node is actionable
            if await self._is_actionable_entity(node, context):
                
                intervention_point = InterventionPoint(
                    node=node,
                    position_in_chain=i,
                    effectiveness=0.0,  # Will be calculated separately
                    cost_estimate=await self._estimate_intervention_cost(node, context),
                    feasibility=0.0,    # Will be calculated separately
                    community_acceptance=0.0,  # Will be calculated separately
                    potential_impact=downstream_impact / len(nodes),
                    intervention_strategies=await self._suggest_intervention_strategies(node, context)
                )
                
                intervention_points.append(intervention_point)
        
        return intervention_points

    async def _calculate_intervention_effectiveness(
        self, 
        intervention_point: InterventionPoint,
        nodes: List[Dict[str, Any]],
        relationships: List[Dict[str, Any]],
        context: ReasoningContext
    ) -> float:
        """Calculate the effectiveness of an intervention at a specific point."""
        
        try:
            # Factors affecting intervention effectiveness:
            # 1. Position in chain (earlier = more effective)
            position_factor = 1.0 - (intervention_point.position_in_chain / len(nodes))
            
            # 2. Causal strength of downstream relationships
            downstream_strength = 1.0
            for i in range(intervention_point.position_in_chain, len(relationships)):
                rel_confidence = relationships[i].get("confidence", 0.5)
                downstream_strength *= rel_confidence
            
            # 3. Node controllability (how easy to influence)
            controllability = await self._assess_node_controllability(
                intervention_point.node, context
            )
            
            # 4. Historical success rate of similar interventions
            historical_success = await self._get_historical_intervention_success(
                intervention_point.node["type"], context
            )
            
            # Combine factors
            effectiveness = (
                position_factor * 0.3 +
                downstream_strength * 0.3 +
                controllability * 0.2 +
                historical_success * 0.2
            )
            
            return min(max(effectiveness, 0.0), 1.0)
            
        except Exception as e:
            logger.error(f"Failed to calculate intervention effectiveness: {e}")
            return 0.5  # Default medium effectiveness

    async def _assess_intervention_feasibility(
        self, 
        intervention_point: InterventionPoint,
        context: ReasoningContext
    ) -> float:
        """Assess the feasibility of implementing an intervention."""
        
        try:
            # Query knowledge graph for resources and capabilities
            query = """
            MATCH (community:Community {id: $community_id})
            MATCH (community)-[:HAS_CAPABILITY|OWNS|CONTROLS*1..2]-(resource)
            WHERE resource.type IN $relevant_types
            RETURN count(resource) as available_resources
            """
            
            relevant_types = self._get_relevant_resource_types(intervention_point.node)
            
            results = await self.knowledge_graph.execute_cypher(query, {
                "community_id": context.community_id,
                "relevant_types": relevant_types
            })
            
            available_resources = results[0]["available_resources"] if results else 0
            
            # Calculate feasibility based on available resources
            max_resources = len(relevant_types) * 2  # Assumption: 2 resources per type for high feasibility
            resource_feasibility = min(available_resources / max_resources, 1.0) if max_resources > 0 else 0.5
            
            # Consider cost factor
            cost_factor = max(1.0 - (intervention_point.cost_estimate / 10000), 0.0)  # Assume $10k as high cost threshold
            
            # Consider complexity
            complexity_factor = 1.0 - self._assess_intervention_complexity(intervention_point.node)
            
            feasibility = (resource_feasibility * 0.4 + cost_factor * 0.3 + complexity_factor * 0.3)
            
            return min(max(feasibility, 0.0), 1.0)
            
        except Exception as e:
            logger.error(f"Failed to assess intervention feasibility: {e}")
            return 0.5

    async def _assess_community_acceptance(
        self, 
        intervention_point: InterventionPoint,
        context: ReasoningContext
    ) -> float:
        """Assess likely community acceptance of an intervention."""
        
        try:
            # Check cultural alignment
            cultural_alignment = 1.0
            if self.cultural_validator:
                cultural_check = await self.cultural_validator.validate_intervention(
                    intervention_point, context.cultural_context
                )
                cultural_alignment = 1.0 if cultural_check.approved else 0.3
            
            # Check historical community preferences
            historical_acceptance = await self._get_historical_community_acceptance(
                intervention_point.node["type"], context
            )
            
            # Check if intervention aligns with community values
            values_alignment = self._assess_values_alignment(
                intervention_point, context.cultural_context
            )
            
            # Check transparency and participation potential
            participation_potential = self._assess_participation_potential(intervention_point)
            
            acceptance = (
                cultural_alignment * 0.3 +
                historical_acceptance * 0.25 +
                values_alignment * 0.25 +
                participation_potential * 0.2
            )
            
            return min(max(acceptance, 0.0), 1.0)
            
        except Exception as e:
            logger.error(f"Failed to assess community acceptance: {e}")
            return 0.5

    async def _generate_intervention_recommendations(
        self, 
        causal_chains: List[CausalChain],
        context: ReasoningContext
    ) -> List[Dict[str, Any]]:
        """Generate intervention recommendations based on causal analysis."""
        
        recommendations = []
        
        # Collect all intervention points across chains
        all_intervention_points = []
        for chain in causal_chains:
            for point in chain.intervention_points:
                # Add chain context to intervention point
                point_with_context = {
                    **point.__dict__,
                    "chain_id": chain.path_id,
                    "chain_confidence": chain.confidence,
                    "chain_causal_strength": chain.causal_strength
                }
                all_intervention_points.append(point_with_context)
        
        # Sort by overall effectiveness (considering chain strength)
        all_intervention_points.sort(
            key=lambda p: p["effectiveness"] * p["chain_causal_strength"] * p["community_acceptance"],
            reverse=True
        )
        
        # Generate top recommendations
        for i, point in enumerate(all_intervention_points[:10]):  # Top 10
            recommendation = {
                "rank": i + 1,
                "intervention_type": point["node"]["type"],
                "target_entity": point["node"]["name"],
                "description": await self._generate_intervention_description(point, context),
                "effectiveness_score": point["effectiveness"],
                "feasibility_score": point["feasibility"],
                "community_acceptance_score": point["community_acceptance"],
                "estimated_cost": point["cost_estimate"],
                "implementation_strategies": point["intervention_strategies"],
                "expected_impact": self._calculate_expected_impact(point),
                "risk_factors": await self._identify_risk_factors(point, context),
                "success_indicators": await self._define_success_indicators(point, context),
                "timeline_estimate": self._estimate_implementation_timeline(point),
                "required_resources": await self._identify_required_resources(point, context),
                "stakeholders": await self._identify_key_stakeholders(point, context)
            }
            recommendations.append(recommendation)
        
        return recommendations

    def _calculate_confidence_assessment(self, causal_chains: List[CausalChain]) -> ConfidenceInterval:
        """Calculate overall confidence assessment for the analysis."""
        
        if not causal_chains:
            return ConfidenceInterval(average=0.0, lower=0.0, upper=0.0)
        
        confidences = [chain.confidence for chain in causal_chains]
        causal_strengths = [chain.causal_strength for chain in causal_chains]
        
        # Weight confidence by causal strength
        weighted_confidences = []
        total_weight = sum(causal_strengths)
        
        for conf, strength in zip(confidences, causal_strengths):
            weight = strength / total_weight if total_weight > 0 else 1.0 / len(confidences)
            weighted_confidences.append(conf * weight)
        
        average_confidence = sum(weighted_confidences)
        std_confidence = np.std(confidences) if len(confidences) > 1 else 0.0
        
        # Calculate confidence interval (assuming normal distribution)
        lower_bound = max(average_confidence - 1.96 * std_confidence, 0.0)
        upper_bound = min(average_confidence + 1.96 * std_confidence, 1.0)
        
        return ConfidenceInterval(
            average=average_confidence,
            lower=lower_bound,
            upper=upper_bound
        )

    # Helper methods (implementations would be detailed based on specific domain requirements)
    
    async def _validate_analysis_culturally_appropriate(
        self, request: CausalAnalysisRequest, context: ReasoningContext
    ):
        """Validate that the requested analysis is culturally appropriate."""
        if self.cultural_validator:
            validation = await self.cultural_validator.validate_analysis_request(request, context)
            if not validation.approved:
                raise ValueError(f"Analysis not culturally appropriate: {validation.concerns}")

    async def _is_actionable_entity(self, node: Dict[str, Any], context: ReasoningContext) -> bool:
        """Check if an entity represents something that can be acted upon."""
        actionable_types = {
            "resource", "infrastructure", "policy", "process", 
            "organization", "cooperative", "governance_mechanism"
        }
        return node.get("type", "").lower() in actionable_types

    async def _estimate_intervention_cost(self, node: Dict[str, Any], context: ReasoningContext) -> float:
        """Estimate the cost of intervening at a specific node."""
        # Placeholder implementation - would be domain-specific
        cost_by_type = {
            "infrastructure": 5000,
            "policy": 1000,
            "process": 2000,
            "organization": 3000,
            "resource": 1500
        }
        return cost_by_type.get(node.get("type", ""), 2500)

    def _assess_evidence_quality(self, relationships: List[Dict[str, Any]]) -> float:
        """Assess the quality of evidence supporting the causal chain."""
        if not relationships:
            return 0.0
        
        confidences = [rel.get("confidence", 0.5) for rel in relationships]
        return sum(confidences) / len(confidences)

    def _check_temporal_consistency(self, nodes: List[Dict[str, Any]]) -> bool:
        """Check if the causal chain is temporally consistent."""
        # Placeholder - would check timestamps and logical sequence
        return True

    async def _suggest_intervention_strategies(
        self, node: Dict[str, Any], context: ReasoningContext
    ) -> List[str]:
        """Suggest specific intervention strategies for a node."""
        # Placeholder implementation
        strategies_by_type = {
            "infrastructure": ["upgrade", "maintain", "relocate"],
            "policy": ["revise", "enforce", "educate"],
            "process": ["optimize", "automate", "standardize"],
            "organization": ["restructure", "train", "support"],
            "resource": ["allocate", "conserve", "substitute"]
        }
        return strategies_by_type.get(node.get("type", ""), ["assess", "plan", "implement"])

    # Additional helper methods would be implemented based on specific requirements...
```

### 7.4 Dockerfile for GraphRAG Engine

#### **Development Dockerfile**
```dockerfile
# apps/graphrag-engine/Dockerfile.dev
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Configure Poetry
RUN poetry config virtualenvs.create false

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install Python dependencies
RUN poetry install --with dev

# Install spaCy models
RUN python -m spacy download en_core_web_sm

# Copy source code
COPY src/ ./src/

# Expose port
EXPOSE 8000

# Development command
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

#### **Production Dockerfile**
```dockerfile
# apps/graphrag-engine/Dockerfile
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Configure Poetry for production
RUN poetry config virtualenvs.create false

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies (production only)
RUN poetry install --only=main

# Production stage
FROM python:3.11-slim AS production

WORKDIR /app

# Create non-root user
RUN groupadd -r graphrag && useradd -r -g graphrag graphrag

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Install spaCy models
RUN python -m spacy download en_core_web_sm

# Copy source code
COPY src/ ./src/

# Create directories for models and data
RUN mkdir -p models data logs && \
    chown -R graphrag:graphrag /app

# Switch to non-root user
USER graphrag

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start application
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

---

## 8. Microservices Implementation

### 8.1 Personnel Service

#### **Personnel Service Structure**
```typescript
// apps/personnel-service/src/index.ts

import { ApolloServer } from '@apollo/server';
import { startStandaloneServer } from '@apollo/server/standalone';
import { buildSubgraphSchema } from '@apollo/subgraph';
import { gql } from 'graphql-tag';
import { PersonnelService } from './services/PersonnelService';
import { AuthService } from './services/AuthService';
import { config } from './config';

// GraphQL schema for Personnel subgraph
const typeDefs = gql`
  extend schema @link(url: "https://specs.apollo.dev/federation/v2.3", import: ["@key", "@shareable", "@external", "@requires"])

  type Person @key(fields: "id") {
    id: ID!
    name: String!
    skills: [String!]!
    certifications: [Certification!]!
    availabilityStatus: AvailabilityStatus!
    communityId: ID!
    cooperativeId: ID
    trustScore: Float!
    communityValidated: Boolean!
    contactInfo: ContactInfo
    deploymentHistory: [Deployment!]!
    
    # Cross-service references
    community: Community @external
    cooperative: Cooperative @external
  }

  type Certification {
    id: ID!
    name: String!
    issuedBy: String!
    issuedDate: Date!
    expiryDate: Date
    verificationStatus: VerificationStatus!
    blockchainRecord: String
  }

  type ContactInfo {
    email: String
    phone: String
    address: Address
    emergencyContact: EmergencyContact
  }

  type Address {
    street: String
    city: String
    region: String
    country: String!
    coordinates: Coordinates
  }

  type Coordinates {
    latitude: Float!
    longitude: Float!
  }

  type EmergencyContact {
    name: String!
    relationship: String!
    phone: String!
  }

  type Deployment {
    id: ID!
    personId: ID!
    operation: String!
    role: String!
    startDate: Date!
    endDate: Date
    location: String!
    performance: PerformanceRating
    feedback: String
  }

  type PerformanceRating {
    technical: Float!
    leadership: Float!
    cooperation: Float!
    culturalSensitivity: Float!
    overall: Float!
  }

  type SkillAssessment {
    skill: String!
    level: SkillLevel!
    assessedBy: String!
    assessmentDate: Date!
    validUntil: Date
  }

  enum AvailabilityStatus {
    AVAILABLE
    DEPLOYED
    UNAVAILABLE
    EMERGENCY_ONLY
  }

  enum VerificationStatus {
    VERIFIED
    PENDING
    EXPIRED
    REVOKED
  }

  enum SkillLevel {
    BEGINNER
    INTERMEDIATE
    ADVANCED
    EXPERT
    MASTER
  }

  type Query {
    # Personnel queries
    person(id: ID!): Person
    personnel(filter: PersonnelFilter): [Person!]!
    availablePersonnel(skills: [String!], location: String): [Person!]!
    skillsInventory(communityId: ID!): SkillsInventory!
    deploymentCapacity(region: String!): DeploymentCapacity!
    
    # Cross-sector coordination
    personnelForCrisis(crisisType: String!, severity: String!, location: String!): [Person!]!
  }

  type Mutation {
    # Personnel management
    createPerson(input: CreatePersonInput!): Person!
    updatePerson(id: ID!, input: UpdatePersonInput!): Person!
    updateAvailability(id: ID!, status: AvailabilityStatus!): Person!
    
    # Skills and certifications
    addSkill(personId: ID!, skill: String!, level: SkillLevel!): Person!
    addCertification(personId: ID!, certification: CertificationInput!): Person!
    validateCertification(certificationId: ID!): Certification!
    
    # Deployment management
    deployPerson(input: DeploymentInput!): Deployment!
    completeDeploy(deploymentId: ID!, performance: PerformanceRatingInput!): Deployment!
    
    # Community validation
    validatePersonCommunity(personId: ID!, validatorId: ID!): Person!
  }

  type Subscription {
    # Real-time updates
    personnelAvailabilityChanged(communityId: ID!): Person!
    emergencyDeploymentRequest(region: String!): DeploymentRequest!
    skillsGapAlert(communityId: ID!): SkillsGapAlert!
  }

  # Input types
  input PersonnelFilter {
    communityId: ID
    cooperativeId: ID
    skills: [String!]
    availabilityStatus: AvailabilityStatus
    trustScoreMin: Float
    location: String
  }

  input CreatePersonInput {
    name: String!
    communityId: ID!
    cooperativeId: ID
    skills: [String!]!
    contactInfo: ContactInfoInput!
    emergencyContact: EmergencyContactInput!
  }

  input UpdatePersonInput {
    name: String
    skills: [String!]
    contactInfo: ContactInfoInput
    availabilityStatus: AvailabilityStatus
  }

  input CertificationInput {
    name: String!
    issuedBy: String!
    issuedDate: Date!
    expiryDate: Date
  }

  input DeploymentInput {
    personId: ID!
    operation: String!
    role: String!
    location: String!
    expectedDuration: Int
  }

  input PerformanceRatingInput {
    technical: Float!
    leadership: Float!
    cooperation: Float!
    culturalSensitivity: Float!
  }

  input ContactInfoInput {
    email: String
    phone: String
    address: AddressInput
  }

  input AddressInput {
    street: String
    city: String
    region: String
    country: String!
    coordinates: CoordinatesInput
  }

  input CoordinatesInput {
    latitude: Float!
    longitude: Float!
  }

  input EmergencyContactInput {
    name: String!
    relationship: String!
    phone: String!
  }

  # Support types
  type SkillsInventory {
    communityId: ID!
    totalPersonnel: Int!
    availablePersonnel: Int!
    skillsBreakdown: [SkillCount!]!
    criticalGaps: [String!]!
  }

  type SkillCount {
    skill: String!
    count: Int!
    averageLevel: Float!
  }

  type DeploymentCapacity {
    region: String!
    totalCapacity: Int!
    currentDeployments: Int!
    availableCapacity: Int!
    specializedCapabilities: [String!]!
  }

  type DeploymentRequest {
    id: ID!
    operation: String!
    urgency: String!
    requiredSkills: [String!]!
    location: String!
    requestedBy: String!
  }

  type SkillsGapAlert {
    communityId: ID!
    criticalSkills: [String!]!
    recommendedTraining: [String!]!
    urgencyLevel: String!
  }

  # External types (defined in other services)
  type Community @key(fields: "id") @external {
    id: ID! @external
  }

  type Cooperative @key(fields: "id") @external {
    id: ID! @external
  }

  scalar Date
`;

// Resolvers
const resolvers = {
  Query: {
    person: async (_, { id }, { dataSources }) => {
      return await dataSources.personnelService.getPersonById(id);
    },
    
    personnel: async (_, { filter }, { dataSources }) => {
      return await dataSources.personnelService.getPersonnel(filter);
    },
    
    availablePersonnel: async (_, { skills, location }, { dataSources }) => {
      return await dataSources.personnelService.getAvailablePersonnel(skills, location);
    },
    
    skillsInventory: async (_, { communityId }, { dataSources }) => {
      return await dataSources.personnelService.getSkillsInventory(communityId);
    },
    
    deploymentCapacity: async (_, { region }, { dataSources }) => {
      return await dataSources.personnelService.getDeploymentCapacity(region);
    },
    
    personnelForCrisis: async (_, { crisisType, severity, location }, { dataSources }) => {
      return await dataSources.personnelService.getPersonnelForCrisis(crisisType, severity, location);
    },
  },

  Mutation: {
    createPerson: async (_, { input }, { dataSources, user }) => {
      // Check authorization
      if (!user.hasPermission('create:personnel')) {
        throw new ForbiddenError('Insufficient permissions');
      }
      
      return await dataSources.personnelService.createPerson(input, user);
    },
    
    updatePerson: async (_, { id, input }, { dataSources, user }) => {
      return await dataSources.personnelService.updatePerson(id, input, user);
    },
    
    updateAvailability: async (_, { id, status }, { dataSources, user }) => {
      return await dataSources.personnelService.updateAvailability(id, status, user);
    },
    
    deployPerson: async (_, { input }, { dataSources, user }) => {
      return await dataSources.personnelService.deployPerson(input, user);
    },
    
    validatePersonCommunity: async (_, { personId, validatorId }, { dataSources, user }) => {
      return await dataSources.personnelService.validatePersonCommunity(personId, validatorId, user);
    },
  },

  Subscription: {
    personnelAvailabilityChanged: {
      subscribe: async (_, { communityId }, { dataSources }) => {
        return dataSources.personnelService.subscribeToAvailabilityChanges(communityId);
      },
    },
    
    emergencyDeploymentRequest: {
      subscribe: async (_, { region }, { dataSources }) => {
        return dataSources.personnelService.subscribeToEmergencyRequests(region);
      },
    },
  },

  Person: {
    __resolveReference: async (person, { dataSources }) => {
      return await dataSources.personnelService.getPersonById(person.id);
    },
    
    deploymentHistory: async (person, _, { dataSources }) => {
      return await dataSources.personnelService.getDeploymentHistory(person.id);
    },
  },
};

// Create Apollo Server
async function createServer() {
  const schema = buildSubgraphSchema([{ typeDefs, resolvers }]);
  
  const server = new ApolloServer({
    schema,
    introspection: config.isDevelopment,
  });

  const { url } = await startStandaloneServer(server, {
    listen: { port: config.port },
    context: async ({ req }) => {
      // Authentication and context creation
      const token = req.headers.authorization?.replace('Bearer ', '');
      const user = token ? await AuthService.validateToken(token) : null;
      
      return {
        user,
        dataSources: {
          personnelService: new PersonnelService(),
        },
      };
    },
  });

  console.log(`🚀 Personnel Service ready at ${url}`);
}

createServer().catch(error => {
  console.error('Failed to start Personnel Service:', error);
  process.exit(1);
});
```

#### **Personnel Service Implementation**
```typescript
// apps/personnel-service/src/services/PersonnelService.ts

import { Pool } from 'pg';
import { Redis } from 'ioredis';
import { PersonnelRepository } from '../repositories/PersonnelRepository';
import { SkillsAnalyzer } from '../utils/SkillsAnalyzer';
import { CommunityValidator } from '../utils/CommunityValidator';
import { logger } from '../utils/logger';
import { config } from '../config';

export class PersonnelService {
  private personnelRepo: PersonnelRepository;
  private skillsAnalyzer: SkillsAnalyzer;
  private communityValidator: CommunityValidator;
  private redis: Redis;

  constructor() {
    const pgPool = new Pool({
      host: config.postgres.host,
      port: config.postgres.port,
      database: config.postgres.database,
      user: config.postgres.user,
      password: config.postgres.password,
      max: 20,
    });

    this.redis = new Redis({
      host: config.redis.host,
      port: config.redis.port,
      password: config.redis.password,
    });

    this.personnelRepo = new PersonnelRepository(pgPool);
    this.skillsAnalyzer = new SkillsAnalyzer();
    this.communityValidator = new CommunityValidator();
  }

  async getPersonById(id: string): Promise<Person | null> {
    try {
      // Try cache first
      const cached = await this.redis.get(`person:${id}`);
      if (cached) {
        return JSON.parse(cached);
      }

      // Fetch from database
      const person = await this.personnelRepo.findById(id);
      if (person) {
        // Cache for 5 minutes
        await this.redis.setex(`person:${id}`, 300, JSON.stringify(person));
      }

      return person;
    } catch (error) {
      logger.error('Failed to get person by ID', { id, error });
      throw error;
    }
  }

  async getPersonnel(filter: PersonnelFilter): Promise<Person[]> {
    try {
      const cacheKey = `personnel:${JSON.stringify(filter)}`;
      const cached = await this.redis.get(cacheKey);
      
      if (cached) {
        return JSON.parse(cached);
      }

      const personnel = await this.personnelRepo.findByFilter(filter);
      
      // Cache for 2 minutes (shorter cache for lists)
      await this.redis.setex(cacheKey, 120, JSON.stringify(personnel));
      
      return personnel;
    } catch (error) {
      logger.error('Failed to get personnel', { filter, error });
      throw error;
    }
  }

  async getAvailablePersonnel(skills: string[], location: string): Promise<Person[]> {
    try {
      const filter: PersonnelFilter = {
        skills,
        availabilityStatus: 'AVAILABLE',
        location,
      };

      const availablePersonnel = await this.personnelRepo.findByFilter(filter);
      
      // Sort by skill match and trust score
      return availablePersonnel.sort((a, b) => {
        const aSkillMatch = this.skillsAnalyzer.calculateSkillMatch(a.skills, skills);
        const bSkillMatch = this.skillsAnalyzer.calculateSkillMatch(b.skills, skills);
        
        if (aSkillMatch !== bSkillMatch) {
          return bSkillMatch - aSkillMatch; // Higher skill match first
        }
        
        return b.trustScore - a.trustScore; // Higher trust score first
      });
    } catch (error) {
      logger.error('Failed to get available personnel', { skills, location, error });
      throw error;
    }
  }

  async getSkillsInventory(communityId: string): Promise<SkillsInventory> {
    try {
      const personnel = await this.personnelRepo.findByFilter({ communityId });
      
      const totalPersonnel = personnel.length;
      const availablePersonnel = personnel.filter(p => p.availabilityStatus === 'AVAILABLE').length;
      
      // Analyze skills breakdown
      const skillsMap = new Map<string, { count: number; totalLevel: number }>();
      
      personnel.forEach(person => {
        person.skills.forEach(skill => {
          if (!skillsMap.has(skill)) {
            skillsMap.set(skill, { count: 0, totalLevel: 0 });
          }
          const skillData = skillsMap.get(skill)!;
          skillData.count++;
          skillData.totalLevel += this.skillsAnalyzer.getSkillLevel(person, skill);
        });
      });
      
      const skillsBreakdown = Array.from(skillsMap.entries()).map(([skill, data]) => ({
        skill,
        count: data.count,
        averageLevel: data.totalLevel / data.count,
      }));
      
      // Identify critical gaps
      const criticalGaps = await this.skillsAnalyzer.identifyCriticalGaps(communityId, skillsBreakdown);
      
      return {
        communityId,
        totalPersonnel,
        availablePersonnel,
        skillsBreakdown,
        criticalGaps,
      };
    } catch (error) {
      logger.error('Failed to get skills inventory', { communityId, error });
      throw error;
    }
  }

  async createPerson(input: CreatePersonInput, user: AuthenticatedUser): Promise<Person> {
    try {
      // Validate community access
      if (!user.hasAccessToCommunity(input.communityId)) {
        throw new ForbiddenError('No access to specified community');
      }

      // Create person in database
      const personData = {
        ...input,
        trustScore: 0.5, // Initial trust score
        communityValidated: false,
        createdBy: user.id,
        createdAt: new Date(),
      };

      const person = await this.personnelRepo.create(personData);
      
      // Invalidate relevant caches
      await this.invalidatePersonnelCaches(input.communityId);
      
      // Log activity
      logger.info('Person created', { 
        personId: person.id, 
        communityId: input.communityId,
        createdBy: user.id 
      });
      
      // Publish event for real-time updates
      await this.publishPersonnelEvent('PERSON_CREATED', person);
      
      return person;
    } catch (error) {
      logger.error('Failed to create person', { input, error });
      throw error;
    }
  }

  async deployPerson(input: DeploymentInput, user: AuthenticatedUser): Promise<Deployment> {
    try {
      // Validate person exists and is available
      const person = await this.getPersonById(input.personId);
      if (!person) {
        throw new NotFoundError('Person not found');
      }
      
      if (person.availabilityStatus !== 'AVAILABLE') {
        throw new ValidationError('Person is not available for deployment');
      }
      
      // Create deployment record
      const deployment = await this.personnelRepo.createDeployment({
        ...input,
        startDate: new Date(),
        deployedBy: user.id,
      });
      
      // Update person availability
      await this.updateAvailability(input.personId, 'DEPLOYED', user);
      
      // Log deployment
      logger.info('Person deployed', {
        personId: input.personId,
        deploymentId: deployment.id,
        operation: input.operation,
        deployedBy: user.id,
      });
      
      return deployment;
    } catch (error) {
      logger.error('Failed to deploy person', { input, error });
      throw error;
    }
  }

  async validatePersonCommunity(
    personId: string, 
    validatorId: string, 
    user: AuthenticatedUser
  ): Promise<Person> {
    try {
      // Check if user has validation permissions
      if (!user.hasPermission('validate:community_members')) {
        throw new ForbiddenError('Insufficient permissions for community validation');
      }
      
      const person = await this.getPersonById(personId);
      if (!person) {
        throw new NotFoundError('Person not found');
      }
      
      // Perform community validation
      const validationResult = await this.communityValidator.validateMember(
        person, validatorId, user.communityId
      );
      
      if (validationResult.approved) {
        // Update person record
        const updatedPerson = await this.personnelRepo.update(personId, {
          communityValidated: true,
          trustScore: Math.min(person.trustScore + 0.2, 1.0), // Increase trust score
          validatedAt: new Date(),
          validatedBy: validatorId,
        });
        
        // Invalidate cache
        await this.redis.del(`person:${personId}`);
        
        logger.info('Person community validated', {
          personId,
          validatorId,
          communityId: user.communityId,
        });
        
        return updatedPerson;
      } else {
        throw new ValidationError(`Community validation failed: ${validationResult.reason}`);
      }
    } catch (error) {
      logger.error('Failed to validate person community', { personId, validatorId, error });
      throw error;
    }
  }

  private async invalidatePersonnelCaches(communityId: string): Promise<void> {
    const patterns = [
      `personnel:*${communityId}*`,
      `skills_inventory:${communityId}`,
      `deployment_capacity:*`,
    ];
    
    for (const pattern of patterns) {
      const keys = await this.redis.keys(pattern);
      if (keys.length > 0) {
        await this.redis.del(...keys);
      }
    }
  }

  private async publishPersonnelEvent(eventType: string, data: any): Promise<void> {
    try {
      await this.redis.publish('personnel_events', JSON.stringify({
        type: eventType,
        data,
        timestamp: new Date().toISOString(),
      }));
    } catch (error) {
      logger.error('Failed to publish personnel event', { eventType, error });
    }
  }
}
```

### 8.2 Quick Setup Script for All Services

#### **Build All Services Script**
```bash
#!/bin/bash
# tools/scripts/build-all-services.sh

set -e

echo "🔨 Building all HCCC microservices..."

# List of all services
services=(
  "graphql-gateway"
  "graphrag-engine"
  "personnel-service"
  "mesh-service"
  "sop-service"
  "security-service"
  "health-service"
  "education-service"
  "agrimesh-service"
  "social-service"
)

# Build each service
for service in "${services[@]}"; do
  echo "📦 Building $service..."
  
  if [ -d "apps/$service" ]; then
    cd "apps/$service"
    
    # Install dependencies and build
    if [ -f "package.json" ]; then
      echo "  Installing Node.js dependencies..."
      npm ci
      echo "  Building TypeScript..."
      npm run build
    elif [ -f "pyproject.toml" ]; then
      echo "  Installing Python dependencies..."
      poetry install
      echo "  Running Python tests..."
      poetry run pytest --quiet
    fi
    
    # Build Docker image
    echo "  Building Docker image..."
    docker build -t "hccc/$service:latest" .
    
    cd "../.."
    echo "  ✅ $service built successfully"
  else
    echo "  ⚠️  $service directory not found, skipping..."
  fi
done

echo "🎉 All services built successfully!"

# Tag images for development
echo "🏷️  Tagging images for development..."
for service in "${services[@]}"; do
  docker tag "hccc/$service:latest" "hccc/$service:dev"
done

echo "📊 Image summary:"
docker images | grep hccc
```

#### **Start All Services Script**
```bash
#!/bin/bash
# tools/scripts/start-all-services.sh

set -e

echo "🚀 Starting all HCCC services..."

# Start infrastructure first
echo "🏗️  Starting infrastructure services..."
docker-compose up -d neo4j postgres redis ipfs prometheus grafana jaeger

# Wait for infrastructure to be ready
echo "⏳ Waiting for infrastructure to be ready..."
sleep 30

# Check infrastructure health
echo "🔍 Checking infrastructure health..."
until docker exec hccc-neo4j cypher-shell -u neo4j -p dev-password "RETURN 1" > /dev/null 2>&1; do
  echo "  Waiting for Neo4j..."
  sleep 5
done

until docker exec hccc-postgres pg_isready -U hccc > /dev/null 2>&1; do
  echo "  Waiting for PostgreSQL..."
  sleep 5
done

until docker exec hccc-redis redis-cli ping > /dev/null 2>&1; do
  echo "  Waiting for Redis..."
  sleep 5
done

echo "✅ Infrastructure ready!"

# Start GraphRAG engine
echo "🧠 Starting GraphRAG engine..."
docker-compose up -d graphrag-engine

# Wait for GraphRAG to be ready
echo "⏳ Waiting for GraphRAG engine..."
until curl -f http://localhost:8000/health > /dev/null 2>&1; do
  echo "  Waiting for GraphRAG..."
  sleep 10
done

# Start all microservices
echo "⚙️  Starting microservices..."
docker-compose up -d \
  personnel-service \
  mesh-service \
  sop-service \
  security-service \
  health-service \
  education-service \
  agrimesh-service \
  social-service

# Wait for services to be ready
echo "⏳ Waiting for microservices..."
sleep 20

# Start GraphQL gateway last
echo "🌐 Starting GraphQL gateway..."
docker-compose up -d graphql-gateway

# Wait for gateway
echo "⏳ Waiting for GraphQL gateway..."
until curl -f http://localhost:4000/health > /dev/null 2>&1; do
  echo "  Waiting for gateway..."
  sleep 5
done

echo "🎉 All services started successfully!"

# Show service status
echo "📊 Service Status:"
echo "  GraphQL Gateway: http://localhost:4000/graphql"
echo "  GraphRAG Engine: http://localhost:8000"
echo "  Neo4j Browser: http://localhost:7474"
echo "  Grafana: http://localhost:3000"
echo "  Prometheus: http://localhost:9090"
echo "  Jaeger: http://localhost:16686"

# Show logs for any failed services
echo "🔍 Checking for any failed services..."
failed_services=$(docker-compose ps --filter "status=exited" --format "table {{.Service}}")
if [ -n "$failed_services" ]; then
  echo "⚠️  Failed services detected:"
  echo "$failed_services"
  echo "💡 Run 'docker-compose logs <service-name>' to check logs"
else
  echo "✅ All services running successfully!"
fi
```

---

## 9. Federated Social Media Integration

### 9.1 ActivityPub Implementation

#### **Social Service with ActivityPub**
```typescript
// apps/social-service/src/activitypub/ActivityPubService.ts

import { Request, Response } from 'express';
import crypto from 'crypto';
import { ActivityPubActor, ActivityPubActivity, ActivityPubObject } from '../types/activitypub';
import { CommunityService } from '../services/CommunityService';
import { ContentModerationService } from '../services/ContentModerationService';
import { logger } from '../utils/logger';

export class ActivityPubService {
  private communityService: CommunityService;
  private moderationService: ContentModerationService;
  private federation: Map<string, FederatedPlatform> = new Map();

  constructor() {
    this.communityService = new CommunityService();
    this.moderationService = new ContentModerationService();
    this.initializeFederatedPlatforms();
  }

  private initializeFederatedPlatforms() {
    // Initialize connections to federated platforms
    this.federation.set('mastodon', new MastodonConnector());
    this.federation.set('peertube', new PeerTubeConnector());
    this.federation.set('pixelfed', new PixelfedConnector());
    this.federation.set('lemmy', new LemmyConnector());
    this.federation.set('writefreely', new WriteFreelyConnector());
    this.federation.set('funkwhale', new FunkwhaleConnector());
    this.federation.set('mobilizon', new MobilizonConnector());
    this.federation.set('bookstack', new BookStackConnector());
    this.federation.set('nextcloud', new NextcloudConnector());
    this.federation.set('bookwyrm', new BookWyrmConnector());
    this.federation.set('owncast', new OwncastConnector());
  }

  // ActivityPub Actor endpoint
  async getActor(req: Request, res: Response): Promise<void> {
    try {
      const { communityId } = req.params;
      
      const community = await this.communityService.getCommunityById(communityId);
      if (!community) {
        res.status(404).json({ error: 'Community not found' });
        return;
      }

      const actor: ActivityPubActor = {
        '@context': [
          'https://www.w3.org/ns/activitystreams',
          'https://w3id.org/security/v1',
          {
            'hccc': 'https://hccc.ht/ns#',
            'cooperative': 'hccc:cooperative',
            'governanceType': 'hccc:governanceType',
            'culturalContext': 'hccc:culturalContext'
          }
        ],
        type: 'Organization',
        id: `${req.protocol}://${req.get('host')}/actors/${communityId}`,
        name: community.name,
        preferredUsername: community.slug,
        summary: community.description,
        inbox: `${req.protocol}://${req.get('host')}/actors/${communityId}/inbox`,
        outbox: `${req.protocol}://${req.get('host')}/actors/${communityId}/outbox`,
        followers: `${req.protocol}://${req.get('host')}/actors/${communityId}/followers`,
        following: `${req.protocol}://${req.get('host')}/actors/${communityId}/following`,
        
        // Cryptographic keys for verification
        publicKey: {
          id: `${req.protocol}://${req.get('host')}/actors/${communityId}#main-key`,
          owner: `${req.protocol}://${req.get('host')}/actors/${communityId}`,
          publicKeyPem: community.publicKey
        },
        
        // HCCC-specific extensions
        cooperative: {
          type: 'Cooperative',
          memberCount: community.memberCount,
          governanceType: community.governanceType,
          economicSectors: community.economicSectors,
          location: {
            type: 'Place',
            name: community.location.name,
            latitude: community.location.latitude,
            longitude: community.location.longitude
          }
        },
        
        culturalContext: {
          language: community.language,
          culturalValues: community.culturalValues,
          traditionalPractices: community.traditionalPractices
        }
      };

      res.setHeader('Content-Type', 'application/activity+json');
      res.json(actor);
      
    } catch (error) {
      logger.error('Failed to get ActivityPub actor', { communityId: req.params.communityId, error });
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  // ActivityPub Inbox endpoint
  async handleInbox(req: Request, res: Response): Promise<void> {
    try {
      const { communityId } = req.params;
      const activity: ActivityPubActivity = req.body;

      // Verify HTTP signature
      const isValidSignature = await this.verifyHttpSignature(req);
      if (!isValidSignature) {
        res.status(401).json({ error: 'Invalid signature' });
        return;
      }

      // Process the activity
      await this.processIncomingActivity(activity, communityId);
      
      res.status(202).json({ message: 'Activity accepted' });
      
    } catch (error) {
      logger.error('Failed to handle inbox activity', { 
        communityId: req.params.communityId, 
        activity: req.body,
        error 
      });
      res.status(500).json({ error: 'Failed to process activity' });
    }
  }

  // ActivityPub Outbox endpoint
  async getOutbox(req: Request, res: Response): Promise<void> {
    try {
      const { communityId } = req.params;
      const page = parseInt(req.query.page as string) || 1;
      const limit = 20;

      const activities = await this.communityService.getCommunityActivities(
        communityId, page, limit
      );

      const outbox = {
        '@context': 'https://www.w3.org/ns/activitystreams',
        type: 'OrderedCollection',
        id: `${req.protocol}://${req.get('host')}/actors/${communityId}/outbox`,
        totalItems: activities.totalCount,
        orderedItems: activities.items.map(this.formatActivityForFederation),
        first: `${req.protocol}://${req.get('host')}/actors/${communityId}/outbox?page=1`,
        last: `${req.protocol}://${req.get('host')}/actors/${communityId}/outbox?page=${Math.ceil(activities.totalCount / limit)}`
      };

      res.setHeader('Content-Type', 'application/activity+json');
      res.json(outbox);
      
    } catch (error) {
      logger.error('Failed to get outbox', { communityId: req.params.communityId, error });
      res.status(500).json({ error: 'Internal server error' });
    }
  }

  // Process incoming ActivityPub activities
  private async processIncomingActivity(
    activity: ActivityPubActivity, 
    communityId: string
  ): Promise<void> {
    
    logger.info('Processing incoming activity', { 
      type: activity.type, 
      actorId: activity.actor,
      communityId 
    });

    // Apply community moderation
    const moderationResult = await this.moderationService.moderateIncomingActivity(
      activity, communityId
    );

    if (!moderationResult.approved) {
      logger.warn('Activity rejected by moderation', { 
        activityId: activity.id,
        reasons: moderationResult.reasons 
      });
      return;
    }

    // Process based on activity type
    switch (activity.type) {
      case 'Follow':
        await this.handleFollowActivity(activity, communityId);
        break;
        
      case 'Create':
        await this.handleCreateActivity(activity, communityId);
        break;
        
      case 'Update':
        await this.handleUpdateActivity(activity, communityId);
        break;
        
      case 'Delete':
        await this.handleDeleteActivity(activity, communityId);
        break;
        
      case 'Like':
        await this.handleLikeActivity(activity, communityId);
        break;
        
      case 'Announce': // Share/Boost
        await this.handleAnnounceActivity(activity, communityId);
        break;
        
      default:
        logger.warn('Unknown activity type', { type: activity.type, activityId: activity.id });
    }
  }

  private async handleCreateActivity(
    activity: ActivityPubActivity, 
    communityId: string
  ): Promise<void> {
    
    const object = activity.object as ActivityPubObject;
    
    // Check if this is supply chain related content
    if (this.isSupplyChainContent(object)) {
      await this.processSupplyChainUpdate(object, communityId);
    }
    
    // Check if this is crisis-related content
    if (this.isCrisisContent(object)) {
      await this.processCrisisUpdate(object, communityId);
    }
    
    // Store the activity for community timeline
    await this.communityService.storeIncomingActivity(activity, communityId);
    
    // Notify relevant community members
    await this.notifyCommunityMembers(activity, communityId);
  }

  // Publish supply chain updates across platforms
  async publishSupplyChainUpdate(update: SupplyChainUpdate): Promise<void> {
    const activity: ActivityPubActivity = {
      '@context': 'https://www.w3.org/ns/activitystreams',
      type: 'Create',
      id: `${update.cooperative.actorId}/activities/${update.id}`,
      actor: update.cooperative.actorId,
      published: new Date().toISOString(),
      object: {
        type: 'Note',
        id: `${update.cooperative.actorId}/notes/${update.id}`,
        content: this.formatSupplyChainContent(update),
        tag: [
          { type: 'Hashtag', name: '#SupplyChain' },
          { type: 'Hashtag', name: `#${update.product.category}` },
          { type: 'Hashtag', name: '#HaitianCooperative' },
          { type: 'Hashtag', name: '#CommunityControlled' }
        ],
        attachment: update.media?.map(media => ({
          type: 'Image',
          url: media.url,
          name: media.description,
          mediaType: media.mimeType
        })) || [],
        
        // HCCC-specific supply chain data
        'hccc:supplyChain': {
          productId: update.product.id,
          stage: update.stage,
          location: update.location,
          qualityMetrics: update.qualityMetrics,
          culturalSignificance: update.culturalSignificance,
          cooperativeInfo: {
            name: update.cooperative.name,
            memberCount: update.cooperative.memberCount,
            sector: update.cooperative.sector
          }
        }
      }
    };

    // Distribute to all federated platforms
    const publishTasks = Array.from(this.federation.values()).map(
      platform => platform.publishActivity(activity).catch(error => {
        logger.error(`Failed to publish to ${platform.name}`, { error, activityId: activity.id });
      })
    );

    await Promise.allSettled(publishTasks);
    
    logger.info('Supply chain update published', { 
      updateId: update.id, 
      platforms: this.federation.size,
      productId: update.product.id 
    });
  }

  // Coordinate crisis response across platforms
  async coordinateCrisisResponse(crisis: CrisisEvent): Promise<void> {
    
    // Mastodon: Immediate alerts and status updates
    if (this.federation.has('mastodon')) {
      await this.federation.get('mastodon')!.publishCrisisAlert({
        urgency: crisis.urgency,
        location: crisis.location,
        type: crisis.type,
        instructions: crisis.immediateInstructions,
        hashtags: ['#CrisisResponse', '#Haiti', `#${crisis.type}`]
      });
    }

    // PeerTube: Video briefings and instructions
    if (crisis.videoBriefing && this.federation.has('peertube')) {
      await this.federation.get('peertube')!.publishVideo({
        title: `Crisis Response: ${crisis.type}`,
        description: crisis.description,
        videoFile: crisis.videoBriefing.file,
        tags: ['crisis', 'emergency', crisis.type.toLowerCase()],
        category: 'News & Events',
        privacy: 'Public'
      });
    }

    // Mobilizon: Emergency coordination meetings
    if (crisis.coordinationMeeting && this.federation.has('mobilizon')) {
      await this.federation.get('mobilizon')!.createEvent({
        name: `Emergency Coordination: ${crisis.type}`,
        description: crisis.coordinationMeeting.description,
        startTime: crisis.coordinationMeeting.startTime,
        location: crisis.coordinationMeeting.location,
        onlineAddress: crisis.coordinationMeeting.bigBlueButtonUrl,
        tags: ['emergency', 'coordination', crisis.type.toLowerCase()]
      });
    }

    // Lemmy: Community discussion and coordination
    if (this.federation.has('lemmy')) {
      await this.federation.get('lemmy')!.createPost({
        community: 'emergency-response',
        title: `Crisis Response Discussion: ${crisis.type}`,
        body: crisis.discussionPrompt,
        nsfw: false,
        language_id: 1, // English
        url: crisis.informationUrl
      });
    }

    // Nextcloud: Document sharing for response teams
    if (crisis.responseDocuments && this.federation.has('nextcloud')) {
      await this.federation.get('nextcloud')!.shareDocuments({
        documents: crisis.responseDocuments,
        shareWith: crisis.responseTeams,
        permissions: ['read', 'comment'],
        expiration: crisis.responseDe