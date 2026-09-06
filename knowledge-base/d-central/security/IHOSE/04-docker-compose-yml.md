---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: 0e52c46f-4e06-4b1c-8b40-798a1bc6d04b
original_filename: 04-docker-compose.yml
created_at: 2025-12-02T00:47:55.330226+00:00
content_hash: 175760e08949
topic: ihose-deployment-infrastructure
topic: "ihose-openvision-documentation-package"
consolidated_into: [docs/DC-IHOSE-DEPLOYMENT-INFRA-RECONCILED-001.md, docs/DC-IHOSE-OPENVISION-DOCUMENTATION-PACKAGE-RECONCILED-001.md]
---

version: '3.8'

# OpenVision Platform - Docker Compose Deployment
# Suitable for: Development, Small Business (5-20 cameras), Testing
# Requirements: Docker 20.10+, Docker Compose 2.0+, 16GB RAM minimum

services:
  # ==================== Video Management ====================
  
  mediamtx:
    image: bluenviron/mediamtx:latest
    container_name: openvision-mediamtx
    ports:
      - "8554:8554"     # RTSP
      - "8888:8888"     # WebRTC
      - "8889:8889"     # HLS
    volumes:
      - ./config/mediamtx.yml:/mediamtx.yml
    restart: unless-stopped
    networks:
      - openvision

  shinobi:
    image: shinobi/shinobi:latest
    container_name: openvision-shinobi
    ports:
      - "8080:8080"     # Web UI
    environment:
      - PLUGIN_KEYS={}
      - CRON_KEY=changeme
      - DB_HOST=postgres
      - DB_USER=shinobi
      - DB_PASSWORD=shinobi_secure_pass
      - DB_DATABASE=shinobi
    volumes:
      - shinobi-videos:/home/Shinobi/videos
      - shinobi-data:/var/lib/shinobi
    depends_on:
      - postgres
    restart: unless-stopped
    networks:
      - openvision

  # ==================== AI & Analytics ====================
  
  yolo-detector:
    image: ultralytics/ultralytics:latest
    container_name: openvision-yolo
    runtime: nvidia  # Remove if no GPU
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
    volumes:
      - ./modules/yolo:/app
      - yolo-models:/models
    command: python -m app.detector
    restart: unless-stopped
    networks:
      - openvision
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  compreface:
    image: exadel/compreface-core:latest
    container_name: openvision-compreface
    ports:
      - "8000:8000"
    environment:
      - POSTGRES_USER=compreface
      - POSTGRES_PASSWORD=compreface_pass
      - POSTGRES_DB=compreface
      - POSTGRES_URL=jdbc:postgresql://postgres:5432/compreface
    depends_on:
      - postgres
    restart: unless-stopped
    networks:
      - openvision

  mlflow:
    image: ghcr.io/mlflow/mlflow:latest
    container_name: openvision-mlflow
    ports:
      - "5000:5000"
    environment:
      - BACKEND_STORE_URI=postgresql://mlflow:mlflow_pass@postgres:5432/mlflow
      - DEFAULT_ARTIFACT_ROOT=/mlruns
    volumes:
      - mlflow-artifacts:/mlruns
    command: >
      mlflow server
      --backend-store-uri postgresql://mlflow:mlflow_pass@postgres:5432/mlflow
      --default-artifact-root /mlruns
      --host 0.0.0.0
    depends_on:
      - postgres
    restart: unless-stopped
    networks:
      - openvision

  # ==================== Message Brokers ====================
  
  nats:
    image: nats:latest
    container_name: openvision-nats
    command: --jetstream --http_port 8222
    ports:
      - "4222:4222"     # Client connections
      - "8222:8222"     # HTTP management
    volumes:
      - nats-data:/data
    restart: unless-stopped
    networks:
      - openvision

  mosquitto:
    image: eclipse-mosquitto:latest
    container_name: openvision-mosquitto
    ports:
      - "1883:1883"     # MQTT
      - "9001:9001"     # WebSocket
    volumes:
      - ./config/mosquitto.conf:/mosquitto/config/mosquitto.conf
      - mosquitto-data:/mosquitto/data
      - mosquitto-logs:/mosquitto/log
    restart: unless-stopped
    networks:
      - openvision

  # ==================== Storage Layer ====================
  
  postgres:
    image: timescale/timescaledb:latest-pg15
    container_name: openvision-postgres
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_PASSWORD=openvision_secure_password
      - POSTGRES_USER=openvision
      - POSTGRES_DB=openvision
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init-scripts:/docker-entrypoint-initdb.d
    restart: unless-stopped
    networks:
      - openvision

  redis:
    image: redis:7-alpine
    container_name: openvision-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    command: redis-server --appendonly yes
    restart: unless-stopped
    networks:
      - openvision

  minio:
    image: minio/minio:latest
    container_name: openvision-minio
    ports:
      - "9000:9000"     # API
      - "9001:9001"     # Console
    environment:
      - MINIO_ROOT_USER=openvision
      - MINIO_ROOT_PASSWORD=openvision_minio_secure_pass
    volumes:
      - minio-data:/data
    command: server /data --console-address ":9001"
    restart: unless-stopped
    networks:
      - openvision
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3

  # ==================== IoT Integration ====================
  
  nodered:
    image: nodered/node-red:latest
    container_name: openvision-nodered
    ports:
      - "1880:1880"
    environment:
      - TZ=UTC
    volumes:
      - nodered-data:/data
    restart: unless-stopped
    networks:
      - openvision

  # ==================== API Gateway ====================
  
  apisix:
    image: apache/apisix:latest
    container_name: openvision-apisix
    ports:
      - "9080:9080"     # HTTP
      - "9443:9443"     # HTTPS
      - "9091:9091"     # Admin API
    environment:
      - APISIX_STAND_ALONE=true
    volumes:
      - ./config/apisix.yaml:/usr/local/apisix/conf/apisix.yaml
      - apisix-logs:/usr/local/apisix/logs
    restart: unless-stopped
    networks:
      - openvision

  # ==================== Observability ====================
  
  prometheus:
    image: prom/prometheus:latest
    container_name: openvision-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    restart: unless-stopped
    networks:
      - openvision

  grafana:
    image: grafana/grafana:latest
    container_name: openvision-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=openvision_grafana_pass
      - GF_INSTALL_PLUGINS=grafana-clock-panel
    volumes:
      - grafana-data:/var/lib/grafana
      - ./config/grafana-datasources.yml:/etc/grafana/provisioning/datasources/datasources.yml
    depends_on:
      - prometheus
    restart: unless-stopped
    networks:
      - openvision

  loki:
    image: grafana/loki:latest
    container_name: openvision-loki
    ports:
      - "3100:3100"
    volumes:
      - loki-data:/loki
      - ./config/loki-config.yml:/etc/loki/config.yml
    command: -config.file=/etc/loki/config.yml
    restart: unless-stopped
    networks:
      - openvision

  # ==================== Authentication ====================
  
  keycloak:
    image: quay.io/keycloak/keycloak:latest
    container_name: openvision-keycloak
    ports:
      - "8180:8080"
    environment:
      - KEYCLOAK_ADMIN=admin
      - KEYCLOAK_ADMIN_PASSWORD=openvision_keycloak_admin
      - KC_DB=postgres
      - KC_DB_URL=jdbc:postgresql://postgres:5432/keycloak
      - KC_DB_USERNAME=keycloak
      - KC_DB_PASSWORD=keycloak_pass
    command: start-dev
    depends_on:
      - postgres
    restart: unless-stopped
    networks:
      - openvision

networks:
  openvision:
    driver: bridge

volumes:
  # Video Management
  shinobi-videos:
  shinobi-data:
  
  # AI/ML
  yolo-models:
  mlflow-artifacts:
  
  # Message Brokers
  nats-data:
  mosquitto-data:
  mosquitto-logs:
  
  # Storage
  postgres-data:
  redis-data:
  minio-data:
  
  # IoT
  nodered-data:
  
  # Observability
  prometheus-data:
  grafana-data:
  loki-data:
  apisix-logs:

# ====================  Usage Instructions ====================
#
# 1. Prerequisites:
#    - Docker 20.10+ and Docker Compose 2.0+
#    - For GPU support: NVIDIA Docker runtime
#    - Minimum 16GB RAM, 100GB disk space
#
# 2. Setup:
#    - Create config directory: mkdir -p config
#    - Copy configuration templates from docs/config-templates/
#    - Update passwords in this file (search for "changeme" and "_pass")
#
# 3. Start services:
#    docker-compose up -d
#
# 4. Verify deployment:
#    docker-compose ps
#    docker-compose logs -f
#
# 5. Access web interfaces:
#    - Shinobi VMS: http://localhost:8080
#    - Grafana: http://localhost:3000 (admin/openvision_grafana_pass)
#    - Node-RED: http://localhost:1880
#    - MinIO Console: http://localhost:9001
#    - Keycloak: http://localhost:8180
#
# 6. Add cameras:
#    - Log into Shinobi, add camera with RTSP URL
#    - MediaMTX will automatically proxy streams
#
# 7. Enable analytics:
#    - Deploy custom modules via openvision-cli
#    - Or use pre-built modules from module registry
#
# 8. Scaling for production:
#    - For >20 cameras, migrate to Kubernetes deployment
#    - See 05-kubernetes-manifests/ directory
#
# ====================  Security Hardening ====================
#
# Before production deployment:
# 1. Change ALL default passwords
# 2. Enable TLS/SSL for all services
# 3. Configure firewall rules (only expose necessary ports)
# 4. Set up backup strategy for volumes
# 5. Enable audit logging
# 6. Configure Keycloak with LDAP/AD integration
# 7. Implement network segmentation (separate camera VLAN)
#
