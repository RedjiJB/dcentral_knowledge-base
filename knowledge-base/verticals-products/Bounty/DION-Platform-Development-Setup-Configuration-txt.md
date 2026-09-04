---
source_project: Bounty
source_project_uuid: 0198b52e-0516-768e-b6d4-182ebfca6ef0
doc_uuid: 52986876-02ae-4e41-92fb-e64f9a568ba0
original_filename: DION Platform - Development Setup & Configuration.txt
created_at: 2025-08-23T16:08:52.703020+00:00
content_hash: 0bca8453c7c5topic: url-kubernetes-yaml
topic: dion-platform-technical-architecture
---

# DION Platform - Development Setup & Configuration Files

# =============================================================================
# 1. DOCKER COMPOSE FOR LOCAL DEVELOPMENT
# =============================================================================

# docker-compose.yml
version: '3.8'

services:
  # Databases
  postgres:
    image: postgis/postgis:15-3.3
    environment:
      POSTGRES_DB: dion_platform
      POSTGRES_USER: dion_user
      POSTGRES_PASSWORD: dion_password
      POSTGRES_MULTIPLE_EXTENSIONS: postgis,uuid-ossp,pg_trgm,btree_gin
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/db-init:/docker-entrypoint-initdb.d
    networks:
      - dion-network

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    networks:
      - dion-network

  neo4j:
    image: neo4j:5-community
    environment:
      NEO4J_AUTH: neo4j/dion_password
      NEO4J_PLUGINS: '["graph-data-science"]'
      NEO4J_dbms_security_procedures_unrestricted: gds.*
      NEO4J_dbms_memory_heap_initial__size: 512m
      NEO4J_dbms_memory_heap_max__size: 2g
    ports:
      - "7474:7474"
      - "7687:7687"
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
    networks:
      - dion-network

  elasticsearch:
    image: elasticsearch:8.8.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx1g"
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - dion-network

  clickhouse:
    image: clickhouse/clickhouse-server:latest
    ports:
      - "8123:8123"
      - "9000:9000"
    volumes:
      - clickhouse_data:/var/lib/clickhouse
      - ./config/clickhouse:/etc/clickhouse-server/config.d
    networks:
      - dion-network

  # Message Queue
  nats:
    image: nats:2.9-alpine
    ports:
      - "4222:4222"
      - "6222:6222"
      - "8222:8222"
    command: ["--cluster_name", "dion", "--jetstream", "--store_dir", "/data"]
    volumes:
      - nats_data:/data
    networks:
      - dion-network

  # Object Storage
  minio:
    image: minio/minio:latest
    ports:
      - "9001:9000"
      - "9002:9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadmin123
      MINIO_BROWSER_REDIRECT_URL: http://localhost:9002
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data
    networks:
      - dion-network

  # Monitoring
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - dion-network

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
    environment:
      GF_SECURITY_ADMIN_PASSWORD: admin
      GF_INSTALL_PLUGINS: grafana-worldmap-panel,grafana-piechart-panel
    volumes:
      - grafana_data:/var/lib/grafana
      - ./config/grafana/dashboards:/var/lib/grafana/dashboards
      - ./config/grafana/provisioning:/etc/grafana/provisioning
    networks:
      - dion-network

  # API Gateway
  kong:
    image: kong:3.3-alpine
    environment:
      KONG_DATABASE: "off"
      KONG_DECLARATIVE_CONFIG: /kong/declarative/kong.yml
      KONG_PROXY_ACCESS_LOG: /dev/stdout
      KONG_ADMIN_ACCESS_LOG: /dev/stdout
      KONG_PROXY_ERROR_LOG: /dev/stderr
      KONG_ADMIN_ERROR_LOG: /dev/stderr
      KONG_ADMIN_LISTEN: "0.0.0.0:8001"
    ports:
      - "8000:8000"
      - "8001:8001"
    volumes:
      - ./config/kong:/kong/declarative
    networks:
      - dion-network

volumes:
  postgres_data:
  redis_data:
  neo4j_data:
  neo4j_logs:
  elasticsearch_data:
  clickhouse_data:
  nats_data:
  minio_data:
  prometheus_data:
  grafana_data:

networks:
  dion-network:
    driver: bridge

---

# =============================================================================
# 2. PACKAGE.JSON FOR MONOREPO ROOT
# =============================================================================

# package.json
{
  "name": "dion-platform",
  "version": "1.0.0",
  "description": "D Central Intelligence & Operator Network Platform",
  "private": true,
  "workspaces": [
    "apps/*",
    "services/*",
    "libs/*"
  ],
  "scripts": {
    "dev": "nx run-many --target=serve --all --parallel",
    "dev:web": "nx serve web-dashboard",
    "dev:admin": "nx serve admin-portal",
    "dev:api": "nx run-many --target=serve --projects=intelligence-service,operator-service,emergency-service --parallel",
    "build": "nx run-many --target=build --all",
    "test": "nx run-many --target=test --all --parallel",
    "test:e2e": "nx run-many --target=e2e --all",
    "lint": "nx run-many --target=lint --all --parallel",
    "format": "prettier --write .",
    "docker:up": "docker-compose up -d",
    "docker:down": "docker-compose down",
    "db:migrate": "nx run intelligence-service:migrate",
    "db:seed": "nx run intelligence-service:seed",
    "setup": "./scripts/setup-development.sh",
    "clean": "nx reset"
  },
  "devDependencies": {
    "@nx/workspace": "^17.0.0",
    "@nx/react": "^17.0.0",
    "@nx/node": "^17.0.0",
    "@nx/web": "^17.0.0",
    "@nx/jest": "^17.0.0",
    "@nx/eslint": "^17.0.0",
    "@nx/cypress": "^17.0.0",
    "@typescript-eslint/eslint-plugin": "^6.0.0",
    "@typescript-eslint/parser": "^6.0.0",
    "eslint": "^8.0.0",
    "eslint-config-prettier": "^9.0.0",
    "prettier": "^3.0.0",
    "typescript": "^5.0.0"
  },
  "nx": {
    "includedScripts": []
  }
}

---

# =============================================================================
# 3. NX WORKSPACE CONFIGURATION
# =============================================================================

# nx.json
{
  "$schema": "./node_modules/nx/schemas/nx-schema.json",
  "namedInputs": {
    "default": [
      "{projectRoot}/**/*",
      "sharedGlobals"
    ],
    "production": [
      "default",
      "!{projectRoot}/**/?(*.)+(spec|test).[jt]s?(x)?(.snap)",
      "!{projectRoot}/tsconfig.spec.json",
      "!{projectRoot}/.eslintrc.json",
      "!{projectRoot}/jest.config.[jt]s"
    ],
    "sharedGlobals": []
  },
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["production", "^production"],
      "cache": true
    },
    "test": {
      "inputs": ["default", "^production", "{workspaceRoot}/jest.preset.js"],
      "cache": true
    },
    "e2e": {
      "inputs": ["default", "^production"],
      "cache": true
    },
    "lint": {
      "inputs": ["default", "{workspaceRoot}/.eslintrc.json"],
      "cache": true
    }
  },
  "generators": {
    "@nx/react": {
      "application": {
        "style": "css",
        "linter": "eslint",
        "bundler": "vite"
      },
      "component": {
        "style": "css"
      },
      "library": {
        "style": "css",
        "linter": "eslint"
      }
    },
    "@nx/node": {
      "application": {
        "linter": "eslint"
      },
      "library": {
        "linter": "eslint"
      }
    }
  },
  "defaultProject": "web-dashboard"
}

---

# =============================================================================
# 4. TYPESCRIPT CONFIGURATION
# =============================================================================

# tsconfig.base.json
{
  "compileOnSave": false,
  "compilerOptions": {
    "rootDir": ".",
    "sourceMap": true,
    "declaration": false,
    "moduleResolution": "node",
    "emitDecoratorMetadata": true,
    "experimentalDecorators": true,
    "importHelpers": true,
    "target": "es2015",
    "module": "esnext",
    "lib": ["es2020", "dom"],
    "skipLibCheck": true,
    "skipDefaultLibCheck": true,
    "baseUrl": ".",
    "strict": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "paths": {
      "@dion/shared-types": ["libs/shared-types/src/index.ts"],
      "@dion/ui-components": ["libs/ui-components/src/index.ts"],
      "@dion/api-client": ["libs/api-client/src/index.ts"],
      "@dion/utils": ["libs/utils/src/index.ts"],
      "@dion/blockchain-sdk": ["libs/blockchain-sdk/src/index.ts"]
    }
  },
  "exclude": ["node_modules", "tmp"]
}

---

# =============================================================================
# 5. GITHUB ACTIONS CI/CD
# =============================================================================

# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgis/postgis:15-3.3
        env:
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
          
      redis:
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run linting
        run: nx run-many --target=lint --all --parallel

      - name: Run unit tests
        run: nx run-many --target=test --all --parallel
        env:
          DATABASE_URL: postgresql://postgres:test_password@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379

      - name: Run build
        run: nx run-many --target=build --all --parallel

      - name: Run E2E tests
        run: nx run-many --target=e2e --all --parallel
        env:
          DATABASE_URL: postgresql://postgres:test_password@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379

  security:
    runs-on: ubuntu-latest
    needs: test
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  build-and-push:
    runs-on: ubuntu-latest
    needs: [test, security]
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/develop'
    
    strategy:
      matrix:
        service: [
          'intelligence-service',
          'operator-service', 
          'emergency-service',
          'user-service',
          'notification-service',
          'blockchain-service'
        ]
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-${{ matrix.service }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=sha

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          file: services/${{ matrix.service }}/Dockerfile
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.ref == 'refs/heads/develop'
    environment: staging
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: 'latest'

      - name: Configure kubectl
        run: |
          echo "${{ secrets.KUBECONFIG_STAGING }}" | base64 -d > $HOME/.kube/config

      - name: Deploy to staging
        run: |
          kubectl set image deployment/intelligence-service intelligence-service=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-intelligence-service:${{ github.sha }} -n dion-staging
          kubectl set image deployment/operator-service operator-service=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-operator-service:${{ github.sha }} -n dion-staging
          kubectl rollout status deployment/intelligence-service -n dion-staging
          kubectl rollout status deployment/operator-service -n dion-staging

  deploy-production:
    runs-on: ubuntu-latest
    needs: build-and-push
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup kubectl
        uses: azure/setup-kubectl@v3
        with:
          version: 'latest'

      - name: Configure kubectl
        run: |
          echo "${{ secrets.KUBECONFIG_PRODUCTION }}" | base64 -d > $HOME/.kube/config

      - name: Deploy to production
        run: |
          kubectl set image deployment/intelligence-service intelligence-service=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-intelligence-service:${{ github.sha }} -n dion-production
          kubectl set image deployment/operator-service operator-service=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}-operator-service:${{ github.sha }} -n dion-production
          kubectl rollout status deployment/intelligence-service -n dion-production
          kubectl rollout status deployment/operator-service -n dion-production

---

# =============================================================================
# 6. KUBERNETES CONFIGURATIONS
# =============================================================================

# infrastructure/kubernetes/base/namespaces/dion-system.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: dion-system
  labels:
    name: dion-system

---

# infrastructure/kubernetes/base/services/intelligence-service/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: intelligence-service
  namespace: dion-system
  labels:
    app: intelligence-service
    version: v1
spec:
  replicas: 3
  selector:
    matchLabels:
      app: intelligence-service
      version: v1
  template:
    metadata:
      labels:
        app: intelligence-service
        version: v1
    spec:
      containers:
      - name: intelligence-service
        image: ghcr.io/dion-platform/intelligence-service:latest
        ports:
        - containerPort: 3000
          name: http
        env:
        - name: NODE_ENV
          value: "production"
        - name: PORT
          value: "3000"
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-secret
              key: DATABASE_URL
        - name: REDIS_URL
          valueFrom:
            secretKeyRef:
              name: redis-secret
              key: REDIS_URL
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 3000
          initialDelaySeconds: 5
          periodSeconds: 5

---

# infrastructure/kubernetes/base/services/intelligence-service/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: intelligence-service
  namespace: dion-system
  labels:
    app: intelligence-service
spec:
  selector:
    app: intelligence-service
  ports:
  - port: 80
    targetPort: 3000
    protocol: TCP
    name: http

---

# =============================================================================
# 7. DEVELOPMENT SETUP SCRIPT
# =============================================================================

# scripts/setup-development.sh
#!/bin/bash
set -e

echo "🚀 Setting up DION Platform development environment..."

# Check prerequisites
echo "📋 Checking prerequisites..."
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed. Aborting." >&2; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required but not installed. Aborting." >&2; exit 1; }
command -v docker-compose >/dev/null 2>&1 || { echo "❌ Docker Compose is required but not installed. Aborting." >&2; exit 1; }

echo "✅ Prerequisites check passed"

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Start infrastructure services
echo "🐳 Starting infrastructure services..."
docker-compose up -d postgres redis neo4j elasticsearch clickhouse nats minio

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Check service health
echo "🔍 Checking service health..."
./scripts/check-services.sh

# Run database migrations
echo "🗃️ Running database migrations..."
npm run db:migrate

# Seed development data
echo "🌱 Seeding development data..."
npm run db:seed

# Generate SSL certificates for development
echo "🔐 Generating development SSL certificates..."
./scripts/generate-dev-certs.sh

# Start monitoring services
echo "📊 Starting monitoring services..."
docker-compose up -d prometheus grafana

echo "🎉 Development environment setup complete!"
echo ""
echo "📍 Access URLs:"
echo "  🌐 Web Dashboard: http://localhost:3000"
echo "  👥 Admin Portal: http://localhost:3001"
echo "  🔧 API Gateway: http://localhost:8000"
echo "  📊 Grafana: http://localhost:3001 (admin/admin)"
echo "  🔍 Neo4j Browser: http://localhost:7474"
echo "  📈 Prometheus: http://localhost:9090"
echo ""
echo "🚀 Start development servers with: npm run dev"

---

# =============================================================================
# 8. ENVIRONMENT VARIABLES TEMPLATE
# =============================================================================

# .env.example
# DION Platform Environment Variables

# =============================================================================
# DATABASE CONFIGURATION
# =============================================================================
DATABASE_URL=postgresql://dion_user:dion_password@localhost:5432/dion_platform
REDIS_URL=redis://localhost:6379
NEO4J_URL=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=dion_password
ELASTICSEARCH_URL=http://localhost:9200
CLICKHOUSE_URL=http://localhost:8123

# =============================================================================
# API CONFIGURATION
# =============================================================================
API_PORT=4000
API_HOST=localhost
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production
ENCRYPTION_KEY=your-32-byte-encryption-key-change-this

# =============================================================================
# BLOCKCHAIN CONFIGURATION
# =============================================================================
BLOCKCHAIN_NETWORK=sepolia
BLOCKCHAIN_RPC_URL=https://sepolia.infura.io/v3/your-project-id
PRIVATE_KEY=your-deployer-private-key
SMART_CONTRACT_ADDRESS=0x...

# =============================================================================
# EXTERNAL INTEGRATIONS
# =============================================================================
FEMA_API_KEY=your-fema-api-key
EMERGENCY_WEBHOOK_URL=https://your-emergency-webhook-endpoint.com
NEWS_API_KEY=your-news-api-key

# =============================================================================
# MONITORING & OBSERVABILITY
# =============================================================================
PROMETHEUS_URL=http://localhost:9090
GRAFANA_URL=http://localhost:3001
JAEGER_URL=http://localhost:14268

# =============================================================================
# SECURITY & AUTHENTICATION
# =============================================================================
DID_RESOLVER_URL=https://resolver.identity.foundation
CORS_ORIGIN=http://localhost:3000,http://localhost:3001
SESSION_SECRET=your-session-secret-change-this
RATE_LIMIT_WINDOW_MS=900000
RATE_LIMIT_MAX=100

# =============================================================================
# STORAGE & CONTENT
# =============================================================================
MINIO_ENDPOINT=localhost:9001
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123
IPFS_GATEWAY=http://localhost:5001

# =============================================================================
# DEVELOPMENT/PRODUCTION FLAGS
# =============================================================================
NODE_ENV=development
LOG_LEVEL=debug
ENABLE_SWAGGER=true
ENABLE_METRICS=true
ENABLE_TRACING=true