---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: 77a3e43d-3a6d-4618-bfdc-c5762adfa6ce
original_filename: core-stack.yml
created_at: 2025-12-02T00:47:54.281538+00:00
content_hash: ba11b9a30327
topic: "ihose-openvision-documentation-package"
---

# Docker Compose - SMB Deployment
# Single-server deployment for 10-50 cameras

version: '3.8'

services:
  # Video Management System
  frigate:
    image: ghcr.io/blakeblackshear/frigate:stable
    container_name: frigate
    restart: unless-stopped
    privileged: true
    shm_size: "512mb"
    ports:
      - "5000:5000"  # Web UI
      - "1935:1935"  # RTMP
      - "8554:8554"  # RTSP
    volumes:
      - ./configs/frigate.yml:/config/config.yml
      - frigate_media:/media/frigate
      - /etc/localtime:/etc/localtime:ro
    environment:
      - FRIGATE_RTSP_PASSWORD=${FRIGATE_RTSP_PASSWORD:-changeme}
    networks:
      - openvision
    depends_on:
      - mqtt
      - postgres
    labels:
      - "com.openvision.service=vms"

  # RTSP Streaming Server
  mediamtx:
    image: bluenviron/mediamtx:latest
    container_name: mediamtx
    restart: unless-stopped
    ports:
      - "8555:8554"  # RTSP
      - "8889:8888"  # WebRTC
      - "8890:8890"  # HTTP API
    volumes:
      - ./configs/mediamtx.yml:/mediamtx.yml
    networks:
      - openvision
    labels:
      - "com.openvision.service=streaming"

  # Object Detection Analytics
  yolo-analytics:
    image: openvision/yolo-analytics:latest
    container_name: yolo-analytics
    restart: unless-stopped
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    volumes:
      - ./configs/yolo-config.yml:/app/config.yml
      - yolo_models:/models
    environment:
      - MODEL_PATH=/models/yolov8n.pt
      - CONFIDENCE_THRESHOLD=0.7
      - NATS_URL=nats://nats:4222
    networks:
      - openvision
    depends_on:
      - nats
    labels:
      - "com.openvision.service=analytics"

  # Face Recognition (optional)
  compreface:
    image: exadel/compreface-core:latest
    container_name: compreface
    restart: unless-stopped
    ports:
      - "8001:8000"
    environment:
      - POSTGRES_URL=jdbc:postgresql://postgres:5432/compreface
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - compreface_data:/app/data
    networks:
      - openvision
    depends_on:
      - postgres
    labels:
      - "com.openvision.service=face-recognition"

  # PostgreSQL + TimescaleDB
  postgres:
    image: timescale/timescaledb:latest-pg15
    container_name: postgres
    restart: unless-stopped
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=${POSTGRES_USER:-openvision}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=openvision
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init-db.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - openvision
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-openvision}"]
      interval: 10s
      timeout: 5s
      retries: 5
    labels:
      - "com.openvision.service=database"

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - redis_data:/data
    networks:
      - openvision
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    labels:
      - "com.openvision.service=cache"

  # MinIO Object Storage
  minio:
    image: minio/minio:latest
    container_name: minio
    restart: unless-stopped
    ports:
      - "9000:9000"
      - "9001:9001"  # Console
    environment:
      - MINIO_ROOT_USER=${MINIO_ROOT_USER:-minioadmin}
      - MINIO_ROOT_PASSWORD=${MINIO_ROOT_PASSWORD}
    command: server /data --console-address ":9001"
    volumes:
      - minio_data:/data
    networks:
      - openvision
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 20s
      retries: 3
    labels:
      - "com.openvision.service=object-storage"

  # NATS Message Broker
  nats:
    image: nats:latest
    container_name: nats
    restart: unless-stopped
    ports:
      - "4222:4222"  # Client
      - "8222:8222"  # Monitoring
    command: "--js --sd /data"
    volumes:
      - nats_data:/data
    networks:
      - openvision
    labels:
      - "com.openvision.service=messaging"

  # Mosquitto MQTT Broker
  mqtt:
    image: eclipse-mosquitto:latest
    container_name: mosquitto
    restart: unless-stopped
    ports:
      - "1883:1883"  # MQTT
      - "9883:9883"  # WebSocket
    volumes:
      - ./configs/mosquitto.conf:/mosquitto/config/mosquitto.conf
      - ./configs/mosquitto-passwd:/mosquitto/config/passwd
      - mosquitto_data:/mosquitto/data
      - mosquitto_log:/mosquitto/log
    networks:
      - openvision
    labels:
      - "com.openvision.service=mqtt"

  # Node-RED Workflow Automation
  nodered:
    image: nodered/node-red:latest
    container_name: nodered
    restart: unless-stopped
    ports:
      - "1880:1880"
    environment:
      - TZ=America/Toronto
    volumes:
      - nodered_data:/data
    networks:
      - openvision
    labels:
      - "com.openvision.service=workflow"

  # Eclipse Ditto (Digital Twin)
  ditto:
    image: eclipse/ditto:latest
    container_name: ditto
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - MONGO_DB_URI=mongodb://mongodb:27017/ditto
    networks:
      - openvision
    depends_on:
      - mongodb
    labels:
      - "com.openvision.service=digital-twin"

  # MongoDB (for Ditto)
  mongodb:
    image: mongo:6
    container_name: mongodb
    restart: unless-stopped
    volumes:
      - mongodb_data:/data/db
    networks:
      - openvision
    labels:
      - "com.openvision.service=database"

  # Keycloak Identity Management
  keycloak:
    image: quay.io/keycloak/keycloak:latest
    container_name: keycloak
    restart: unless-stopped
    ports:
      - "8180:8080"
    environment:
      - KEYCLOAK_ADMIN=${KEYCLOAK_ADMIN:-admin}
      - KEYCLOAK_ADMIN_PASSWORD=${KEYCLOAK_ADMIN_PASSWORD}
      - KC_DB=postgres
      - KC_DB_URL=jdbc:postgresql://postgres:5432/keycloak
      - KC_DB_USERNAME=${POSTGRES_USER}
      - KC_DB_PASSWORD=${POSTGRES_PASSWORD}
      - KC_HOSTNAME=localhost
      - KC_HTTP_ENABLED=true
    command: start-dev
    networks:
      - openvision
    depends_on:
      - postgres
    labels:
      - "com.openvision.service=identity"

  # API Gateway (Apache APISIX)
  apisix:
    image: apache/apisix:latest
    container_name: apisix
    restart: unless-stopped
    ports:
      - "9080:9080"  # HTTP
      - "9443:9443"  # HTTPS
      - "9180:9180"  # Admin API
    volumes:
      - ./configs/apisix.yaml:/usr/local/apisix/conf/config.yaml
    networks:
      - openvision
    depends_on:
      - etcd
    labels:
      - "com.openvision.service=api-gateway"

  # etcd (for APISIX)
  etcd:
    image: bitnami/etcd:latest
    container_name: etcd
    restart: unless-stopped
    environment:
      - ALLOW_NONE_AUTHENTICATION=yes
      - ETCD_ADVERTISE_CLIENT_URLS=http://etcd:2379
    volumes:
      - etcd_data:/bitnami/etcd
    networks:
      - openvision
    labels:
      - "com.openvision.service=config-store"

  # Grafana Monitoring
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=${GRAFANA_ADMIN_USER:-admin}
      - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD}
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource
    volumes:
      - grafana_data:/var/lib/grafana
      - ./configs/grafana/provisioning:/etc/grafana/provisioning
    networks:
      - openvision
    depends_on:
      - prometheus
    labels:
      - "com.openvision.service=monitoring"

  # Prometheus Metrics
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=90d'
    volumes:
      - ./configs/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    networks:
      - openvision
    labels:
      - "com.openvision.service=monitoring"

  # Loki Log Aggregation
  loki:
    image: grafana/loki:latest
    container_name: loki
    restart: unless-stopped
    ports:
      - "3100:3100"
    command: -config.file=/etc/loki/local-config.yaml
    volumes:
      - loki_data:/loki
    networks:
      - openvision
    labels:
      - "com.openvision.service=logging"

  # Promtail Log Collector
  promtail:
    image: grafana/promtail:latest
    container_name: promtail
    restart: unless-stopped
    volumes:
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
      - ./configs/promtail.yml:/etc/promtail/config.yml
    command: -config.file=/etc/promtail/config.yml
    networks:
      - openvision
    depends_on:
      - loki
    labels:
      - "com.openvision.service=logging"

  # Web UI (React)
  web-ui:
    image: openvision/web-ui:latest
    container_name: web-ui
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    environment:
      - API_URL=http://apisix:9080
      - KEYCLOAK_URL=http://keycloak:8080
    volumes:
      - ./configs/nginx.conf:/etc/nginx/nginx.conf:ro
    networks:
      - openvision
    depends_on:
      - apisix
      - keycloak
    labels:
      - "com.openvision.service=frontend"

networks:
  openvision:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

volumes:
  frigate_media:
    driver: local
  yolo_models:
    driver: local
  compreface_data:
    driver: local
  postgres_data:
    driver: local
  redis_data:
    driver: local
  minio_data:
    driver: local
  nats_data:
    driver: local
  mosquitto_data:
    driver: local
  mosquitto_log:
    driver: local
  nodered_data:
    driver: local
  mongodb_data:
    driver: local
  etcd_data:
    driver: local
  grafana_data:
    driver: local
  prometheus_data:
    driver: local
  loki_data:
    driver: local
