---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: c4823538-6684-4f5f-a926-342a36f74643
original_filename: IHOSE_DevOps_Infrastructure_Implementation_Guide.md
created_at: 2025-11-10T23:32:29.307655+00:00
content_hash: 91ea5dc5e832
---

# Iron Horse Security - IHOSE DevOps & Infrastructure Implementation Guide

**Version 1.0 - Production Deployment Specifications**

*Extends: IHOSE Complete Technical Specification v3.0*

---

## Table of Contents

1. [Configuration Blueprints](#1-configuration-blueprints)
   - Helm Charts
   - Docker Compose Stacks
   - Ansible Playbooks
   - Terraform Modules
2. [Data Flow & API Contracts](#2-data-flow--api-contracts)
   - OpenAPI 3.1 Specifications
   - GraphQL Federation Schemas
   - Event Stream Definitions
3. [DevSecOps Pipeline](#3-devsecops-pipeline)
   - GitLab CI/CD Configuration
   - Security Scanning Integration
   - Deployment Automation

---

# 1. Configuration Blueprints

## 1.1 Helm Charts

### Core Services Helm Chart Structure

```
ironhorse-platform/
â”œâ”€â”€ Chart.yaml
â”œâ”€â”€ values.yaml
â”œâ”€â”€ values-production.yaml
â”œâ”€â”€ values-staging.yaml
â”œâ”€â”€ templates/
â”‚   â”œâ”€â”€ _helpers.tpl
â”‚   â”œâ”€â”€ keycloak/
â”‚   â”‚   â”œâ”€â”€ deployment.yaml
â”‚   â”‚   â”œâ”€â”€ service.yaml
â”‚   â”‚   â”œâ”€â”€ ingress.yaml
â”‚   â”‚   â”œâ”€â”€ configmap.yaml
â”‚   â”‚   â””â”€â”€ secrets.yaml
â”‚   â”œâ”€â”€ erpnext/
â”‚   â”œâ”€â”€ nextcloud/
â”‚   â”œâ”€â”€ mailu/
â”‚   â”œâ”€â”€ matrix/
â”‚   â”œâ”€â”€ wazuh/
â”‚   â””â”€â”€ kafka/
â””â”€â”€ charts/
    â””â”€â”€ [sub-charts]
```

### Keycloak Helm Chart Example

**Chart.yaml**
```yaml
apiVersion: v2
name: keycloak
description: Keycloak SSO/IAM for Iron Horse Security
type: application
version: 1.0.0
appVersion: "24.0.3"
dependencies:
  - name: postgresql
    version: 12.x.x
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
```

**values.yaml**
```yaml
# Keycloak Configuration
keycloak:
  replicas: 3
  image:
    repository: quay.io/keycloak/keycloak
    tag: "24.0.3"
    pullPolicy: IfNotPresent

  resources:
    requests:
      memory: "1Gi"
      cpu: "500m"
    limits:
      memory: "2Gi"
      cpu: "1000m"

  env:
    # Database configuration
    - name: KC_DB
      value: "postgres"
    - name: KC_DB_URL_HOST
      value: "postgres-keycloak"
    - name: KC_DB_URL_DATABASE
      value: "keycloak"
    - name: KC_DB_USERNAME
      valueFrom:
        secretKeyRef:
          name: keycloak-db-credentials
          key: username
    - name: KC_DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: keycloak-db-credentials
          key: password
    
    # Hostname configuration
    - name: KC_HOSTNAME
      value: "auth.ironhorsesecurity.com"
    - name: KC_HOSTNAME_STRICT
      value: "true"
    - name: KC_PROXY
      value: "edge"
    
    # TLS configuration
    - name: KC_HTTPS_CERTIFICATE_FILE
      value: "/opt/keycloak/certs/tls.crt"
    - name: KC_HTTPS_CERTIFICATE_KEY_FILE
      value: "/opt/keycloak/certs/tls.key"
    
    # Clustering
    - name: KC_CACHE
      value: "ispn"
    - name: KC_CACHE_STACK
      value: "kubernetes"
    - name: JGROUPS_DISCOVERY_PROTOCOL
      value: "kubernetes.KUBE_PING"
    - name: JGROUPS_DISCOVERY_PROPERTIES
      value: "namespace=ironhorse-platform"
    
    # Performance tuning
    - name: KC_TRANSACTION_XA_ENABLED
      value: "false"
    - name: KC_HEALTH_ENABLED
      value: "true"
    - name: KC_METRICS_ENABLED
      value: "true"

  volumeMounts:
    - name: tls-certs
      mountPath: /opt/keycloak/certs
      readOnly: true
    - name: realm-config
      mountPath: /opt/keycloak/data/import
      readOnly: true

  volumes:
    - name: tls-certs
      secret:
        secretName: keycloak-tls
    - name: realm-config
      configMap:
        name: keycloak-realm-config

  service:
    type: ClusterIP
    port: 8443
    targetPort: 8443

  ingress:
    enabled: true
    className: nginx
    annotations:
      cert-manager.io/cluster-issuer: "letsencrypt-prod"
      nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
      nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
      nginx.ingress.kubernetes.io/ssl-protocols: "TLSv1.3"
    hosts:
      - host: auth.ironhorsesecurity.com
        paths:
          - path: /
            pathType: Prefix
    tls:
      - secretName: keycloak-tls
        hosts:
          - auth.ironhorsesecurity.com

  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 10
    targetCPUUtilizationPercentage: 75
    targetMemoryUtilizationPercentage: 80

  podSecurityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000
    seccompProfile:
      type: RuntimeDefault

  securityContext:
    allowPrivilegeEscalation: false
    capabilities:
      drop:
        - ALL
    readOnlyRootFilesystem: true

# PostgreSQL configuration
postgresql:
  enabled: true
  auth:
    username: keycloak
    database: keycloak
    existingSecret: keycloak-db-credentials
  primary:
    persistence:
      enabled: true
      size: 20Gi
      storageClass: "ceph-rbd-ssd"
    resources:
      requests:
        memory: "512Mi"
        cpu: "250m"
      limits:
        memory: "1Gi"
        cpu: "500m"
    podSecurityContext:
      fsGroup: 1001
```

**templates/keycloak/deployment.yaml**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "keycloak.fullname" . }}
  namespace: {{ .Release.Namespace }}
  labels:
    {{- include "keycloak.labels" . | nindent 4 }}
    app.kubernetes.io/component: identity-provider
spec:
  replicas: {{ .Values.keycloak.replicas }}
  selector:
    matchLabels:
      {{- include "keycloak.selectorLabels" . | nindent 6 }}
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/keycloak/configmap.yaml") . | sha256sum }}
        prometheus.io/scrape: "true"
        prometheus.io/port: "8443"
        prometheus.io/path: "/metrics"
      labels:
        {{- include "keycloak.selectorLabels" . | nindent 8 }}
    spec:
      {{- with .Values.keycloak.podSecurityContext }}
      securityContext:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "keycloak.serviceAccountName" . }}
      initContainers:
        - name: wait-for-postgres
          image: busybox:1.36
          command:
            - sh
            - -c
            - |
              until nc -z postgres-keycloak 5432; do
                echo "Waiting for PostgreSQL..."
                sleep 2
              done
      containers:
        - name: keycloak
          {{- with .Values.keycloak.securityContext }}
          securityContext:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          image: "{{ .Values.keycloak.image.repository }}:{{ .Values.keycloak.image.tag }}"
          imagePullPolicy: {{ .Values.keycloak.image.pullPolicy }}
          args:
            - start
            - --optimized
            - --import-realm
          ports:
            - name: https
              containerPort: 8443
              protocol: TCP
            - name: management
              containerPort: 9000
              protocol: TCP
          env:
            {{- toYaml .Values.keycloak.env | nindent 12 }}
          volumeMounts:
            {{- toYaml .Values.keycloak.volumeMounts | nindent 12 }}
          livenessProbe:
            httpGet:
              path: /health/live
              port: 9000
              scheme: HTTP
            initialDelaySeconds: 60
            periodSeconds: 30
            timeoutSeconds: 10
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 9000
              scheme: HTTP
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
          resources:
            {{- toYaml .Values.keycloak.resources | nindent 12 }}
      volumes:
        {{- toYaml .Values.keycloak.volumes | nindent 8 }}
      {{- with .Values.keycloak.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.keycloak.affinity }}
      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchExpressions:
                    - key: app.kubernetes.io/name
                      operator: In
                      values:
                        - keycloak
                topologyKey: kubernetes.io/hostname
      {{- end }}
```

**templates/keycloak/configmap.yaml**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: keycloak-realm-config
  namespace: {{ .Release.Namespace }}
data:
  ironhorse-realm.json: |
    {
      "realm": "ironhorse",
      "enabled": true,
      "displayName": "Iron Horse Security",
      "sslRequired": "external",
      "registrationAllowed": false,
      "resetPasswordAllowed": true,
      "editUsernameAllowed": false,
      "bruteForceProtected": true,
      "permanentLockout": false,
      "maxFailureWaitSeconds": 900,
      "minimumQuickLoginWaitSeconds": 60,
      "waitIncrementSeconds": 60,
      "quickLoginCheckMilliSeconds": 1000,
      "maxDeltaTimeSeconds": 43200,
      "failureFactor": 5,
      "defaultSignatureAlgorithm": "RS256",
      "revokeRefreshToken": true,
      "refreshTokenMaxReuse": 0,
      "accessTokenLifespan": 900,
      "accessTokenLifespanForImplicitFlow": 900,
      "ssoSessionIdleTimeout": 1800,
      "ssoSessionMaxLifespan": 36000,
      "offlineSessionIdleTimeout": 2592000,
      "offlineSessionMaxLifespanEnabled": false,
      "clientSessionIdleTimeout": 0,
      "clientSessionMaxLifespan": 0,
      "clients": [
        {
          "clientId": "erpnext",
          "name": "ERPNext ERP System",
          "enabled": true,
          "protocol": "openid-connect",
          "publicClient": false,
          "bearerOnly": false,
          "standardFlowEnabled": true,
          "implicitFlowEnabled": false,
          "directAccessGrantsEnabled": true,
          "serviceAccountsEnabled": true,
          "authorizationServicesEnabled": true,
          "redirectUris": [
            "https://erp.ironhorsesecurity.com/*"
          ],
          "webOrigins": [
            "https://erp.ironhorsesecurity.com"
          ],
          "attributes": {
            "access.token.lifespan": "900",
            "pkce.code.challenge.method": "S256"
          }
        },
        {
          "clientId": "nextcloud",
          "name": "Nextcloud File Storage",
          "enabled": true,
          "protocol": "openid-connect",
          "publicClient": false,
          "redirectUris": [
            "https://files.ironhorsesecurity.com/*"
          ],
          "webOrigins": [
            "https://files.ironhorsesecurity.com"
          ]
        },
        {
          "clientId": "grafana",
          "name": "Grafana Analytics",
          "enabled": true,
          "protocol": "openid-connect",
          "publicClient": false,
          "redirectUris": [
            "https://metrics.ironhorsesecurity.com/*"
          ]
        }
      ],
      "roles": {
        "realm": [
          {
            "name": "security_guard",
            "description": "Field security personnel"
          },
          {
            "name": "site_supervisor",
            "description": "Site management role"
          },
          {
            "name": "operations_manager",
            "description": "Operations management"
          },
          {
            "name": "hr_officer",
            "description": "Human resources"
          },
          {
            "name": "system_admin",
            "description": "System administrator"
          },
          {
            "name": "executive",
            "description": "Executive leadership"
          }
        ]
      },
      "groups": [
        {
          "name": "Field Operations",
          "path": "/Field Operations",
          "realmRoles": ["security_guard"]
        },
        {
          "name": "Management",
          "path": "/Management",
          "realmRoles": ["operations_manager", "hr_officer"]
        },
        {
          "name": "IT",
          "path": "/IT",
          "realmRoles": ["system_admin"]
        }
      ],
      "requiredActions": [
        {
          "alias": "CONFIGURE_TOTP",
          "name": "Configure OTP",
          "providerId": "CONFIGURE_TOTP",
          "enabled": true,
          "defaultAction": true,
          "priority": 10
        },
        {
          "alias": "UPDATE_PASSWORD",
          "name": "Update Password",
          "providerId": "UPDATE_PASSWORD",
          "enabled": true,
          "defaultAction": true,
          "priority": 20
        }
      ],
      "authenticationFlows": [
        {
          "alias": "browser-with-mfa",
          "description": "Browser flow with mandatory MFA",
          "providerId": "basic-flow",
          "topLevel": true,
          "builtIn": false,
          "authenticationExecutions": [
            {
              "authenticator": "auth-cookie",
              "requirement": "ALTERNATIVE",
              "priority": 10
            },
            {
              "authenticator": "identity-provider-redirector",
              "requirement": "ALTERNATIVE",
              "priority": 20
            },
            {
              "authenticatorFlow": true,
              "requirement": "ALTERNATIVE",
              "priority": 30,
              "flowAlias": "Forms"
            }
          ]
        }
      ],
      "browserFlow": "browser-with-mfa",
      "smtpServer": {
        "from": "noreply@ironhorsesecurity.com",
        "fromDisplayName": "Iron Horse Security",
        "host": "mail.ironhorsesecurity.com",
        "port": "587",
        "ssl": "true",
        "starttls": "true",
        "auth": "true",
        "user": "${env.SMTP_USER}",
        "password": "${env.SMTP_PASSWORD}"
      }
    }
```

### ERPNext Helm Chart

**values.yaml (ERPNext)**
```yaml
erpnext:
  image:
    repository: frappe/erpnext
    tag: "v15.0.0"
    pullPolicy: IfNotPresent

  replicas: 3

  resources:
    requests:
      memory: "2Gi"
      cpu: "1000m"
    limits:
      memory: "4Gi"
      cpu: "2000m"

  # Database configuration
  database:
    host: "mariadb-erpnext"
    port: 3306
    rootPassword:
      existingSecret: erpnext-db-root
      key: password
    user: erpnext
    password:
      existingSecret: erpnext-db-user
      key: password

  # Redis configuration
  redis:
    host: "redis-erpnext"
    port: 6379
    cache:
      enabled: true
    queue:
      enabled: true
    socketio:
      enabled: true

  # Site configuration
  sites:
    - name: erp.ironhorsesecurity.com
      adminPassword:
        existingSecret: erpnext-admin
        key: password
      dbName: erpnext_production
      install_apps:
        - erpnext
        - hrms
        - iron_horse_integrations  # Custom app

  # S3/MinIO for file storage
  storage:
    type: "s3"
    endpoint: "https://minio.ironhorsesecurity.com"
    bucket: "erpnext-files"
    accessKey:
      existingSecret: minio-credentials
      key: access-key
    secretKey:
      existingSecret: minio-credentials
      key: secret-key

  # Integration configurations
  integrations:
    keycloak:
      enabled: true
      server: "https://auth.ironhorsesecurity.com"
      realm: "ironhorse"
      clientId: "erpnext"
      clientSecret:
        existingSecret: keycloak-client-erpnext
        key: secret

    kafka:
      enabled: true
      brokers:
        - kafka-0.kafka-headless.ironhorse-platform.svc.cluster.local:9092
        - kafka-1.kafka-headless.ironhorse-platform.svc.cluster.local:9092
        - kafka-2.kafka-headless.ironhorse-platform.svc.cluster.local:9092
      topics:
        - training.completion
        - hr.attendance
        - payroll.processed
        - incident.created

    prometheus:
      enabled: true
      port: 9090
      path: /metrics

  # Worker configuration for background jobs
  workers:
    default:
      replicas: 2
      resources:
        requests:
          memory: "512Mi"
          cpu: "250m"
        limits:
          memory: "1Gi"
          cpu: "500m"
    
    short:
      replicas: 2
      resources:
        requests:
          memory: "256Mi"
          cpu: "125m"
        limits:
          memory: "512Mi"
          cpu: "250m"
    
    long:
      replicas: 1
      resources:
        requests:
          memory: "1Gi"
          cpu: "500m"
        limits:
          memory: "2Gi"
          cpu: "1000m"

  # Nginx configuration
  nginx:
    enabled: true
    replicas: 2
    resources:
      requests:
        memory: "128Mi"
        cpu: "100m"
      limits:
        memory: "256Mi"
        cpu: "200m"

  # Socket.IO for real-time updates
  socketio:
    enabled: true
    replicas: 2
    resources:
      requests:
        memory: "256Mi"
        cpu: "125m"
      limits:
        memory: "512Mi"
        cpu: "250m"

  service:
    type: ClusterIP
    port: 8000

  ingress:
    enabled: true
    className: nginx
    annotations:
      cert-manager.io/cluster-issuer: "letsencrypt-prod"
      nginx.ingress.kubernetes.io/proxy-body-size: "100m"
      nginx.ingress.kubernetes.io/proxy-read-timeout: "600"
      nginx.ingress.kubernetes.io/proxy-send-timeout: "600"
    hosts:
      - host: erp.ironhorsesecurity.com
        paths:
          - path: /
            pathType: Prefix
    tls:
      - secretName: erpnext-tls
        hosts:
          - erp.ironhorsesecurity.com

# MariaDB configuration
mariadb:
  enabled: true
  auth:
    rootPassword: ""  # Set via existingSecret
    username: erpnext
    password: ""  # Set via existingSecret
    database: erpnext_production
    existingSecret: erpnext-db-credentials
  primary:
    persistence:
      enabled: true
      size: 100Gi
      storageClass: "ceph-rbd-ssd"
    configuration: |-
      [mysqld]
      character-set-server=utf8mb4
      collation-server=utf8mb4_unicode_ci
      max_allowed_packet=512M
      innodb_buffer_pool_size=2G
      innodb_log_file_size=256M
      innodb_flush_method=O_DIRECT
      innodb_file_per_table=1
      query_cache_size=0
      query_cache_type=0
    resources:
      requests:
        memory: "4Gi"
        cpu: "1000m"
      limits:
        memory: "8Gi"
        cpu: "2000m"

# Redis configuration
redis:
  enabled: true
  architecture: standalone
  master:
    persistence:
      enabled: true
      size: 10Gi
    resources:
      requests:
        memory: "512Mi"
        cpu: "250m"
      limits:
        memory: "1Gi"
        cpu: "500m"
```

## 1.2 Docker Compose Stacks

### Edge Site Deployment Stack

**docker-compose.edge.yml** (For Raspberry Pi edge clusters)
```yaml
version: '3.8'

services:
  # K3s is installed as system service, this stack runs on top

  # Local ZoneMinder CCTV management
  zoneminder:
    image: dlandon/zoneminder:latest
    container_name: zoneminder
    restart: unless-stopped
    shm_size: '2gb'
    ports:
      - "8080:80"
      - "9000:9000"
    environment:
      - TZ=America/Toronto
      - PUID=99
      - PGID=100
      - INSTALL_HOOK=1
      - INSTALL_FACE=1
      - INSTALL_TINY_YOLO=1
      - INSTALL_YOLO=0
      - MULTI_PORT_START=0
      - MULTI_PORT_END=0
    volumes:
      - /opt/ironhorse/zoneminder/config:/config
      - /opt/ironhorse/zoneminder/data:/var/cache/zoneminder
      - /mnt/cctv-storage:/var/cache/zoneminder/events
      - /etc/localtime:/etc/localtime:ro
    devices:
      - /dev/dri:/dev/dri  # Hardware acceleration
    networks:
      - edge-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # MariaDB for ZoneMinder
  zoneminder-db:
    image: mariadb:11.0
    container_name: zoneminder-db
    restart: unless-stopped
    environment:
      - MYSQL_ROOT_PASSWORD_FILE=/run/secrets/zm_db_root_password
      - MYSQL_DATABASE=zm
      - MYSQL_USER=zmuser
      - MYSQL_PASSWORD_FILE=/run/secrets/zm_db_password
      - TZ=America/Toronto
    volumes:
      - /opt/ironhorse/zoneminder/db:/var/lib/mysql
    secrets:
      - zm_db_root_password
      - zm_db_password
    networks:
      - edge-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # OpenHAB for access control
  openhab:
    image: openhab/openhab:4.0.3
    container_name: openhab
    restart: unless-stopped
    network_mode: host
    environment:
      - OPENHAB_HTTP_PORT=8081
      - OPENHAB_HTTPS_PORT=8443
      - EXTRA_JAVA_OPTS=-Duser.timezone=America/Toronto
      - CRYPTO_POLICY=unlimited
    volumes:
      - /opt/ironhorse/openhab/conf:/openhab/conf
      - /opt/ironhorse/openhab/userdata:/openhab/userdata
      - /opt/ironhorse/openhab/addons:/openhab/addons
      - /etc/localtime:/etc/localtime:ro
    devices:
      - /dev/ttyUSB0:/dev/ttyUSB0  # Z-Wave/Zigbee controller
      - /dev/ttyACM0:/dev/ttyACM0  # ESP32 serial
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Node-RED for IoT data flows
  nodered:
    image: nodered/node-red:latest
    container_name: nodered
    restart: unless-stopped
    ports:
      - "1880:1880"
    environment:
      - TZ=America/Toronto
      - NODE_RED_ENABLE_SAFE_MODE=false
      - NODE_RED_ENABLE_PROJECTS=true
    volumes:
      - /opt/ironhorse/nodered:/data
      - /etc/localtime:/etc/localtime:ro
    networks:
      - edge-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # MQTT Broker for IoT devices
  mosquitto:
    image: eclipse-mosquitto:2.0
    container_name: mosquitto
    restart: unless-stopped
    ports:
      - "1883:1883"
      - "8883:8883"
      - "9001:9001"
    environment:
      - TZ=America/Toronto
    volumes:
      - /opt/ironhorse/mosquitto/config:/mosquitto/config
      - /opt/ironhorse/mosquitto/data:/mosquitto/data
      - /opt/ironhorse/mosquitto/log:/mosquitto/log
      - /opt/ironhorse/certs/mosquitto:/mosquitto/certs:ro
    networks:
      - edge-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Local Matrix Synapse (edge instance for offline operation)
  matrix-synapse:
    image: matrixdotorg/synapse:latest
    container_name: matrix-synapse
    restart: unless-stopped
    ports:
      - "8008:8008"
      - "8448:8448"
    environment:
      - SYNAPSE_SERVER_NAME=edge.ironhorsesecurity.local
      - SYNAPSE_REPORT_STATS=no
      - TZ=America/Toronto
    volumes:
      - /opt/ironhorse/matrix/data:/data
      - /opt/ironhorse/certs/matrix:/certs:ro
    networks:
      - edge-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # PostgreSQL for Matrix
  matrix-db:
    image: postgres:15-alpine
    container_name: matrix-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=synapse
      - POSTGRES_PASSWORD_FILE=/run/secrets/matrix_db_password
      - POSTGRES_DB=synapse
      - POSTGRES_INITDB_ARGS=--encoding=UTF-8 --lc-collate=C --lc-ctype=C
    volumes:
      - /opt/ironhorse/matrix/db:/var/lib/postgresql/data
    secrets:
      - matrix_db_password
    networks:
      - edge-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # ERPNext Operations Module (read-only mirror)
  erpnext-edge:
    image: frappe/erpnext:v15.0.0
    container_name: erpnext-edge
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      - FRAPPE_SITE_NAME=edge.ironhorsesecurity.local
      - DB_HOST=erpnext-edge-db
      - DB_PORT=3306
      - REDIS_CACHE=redis-erpnext:6379
      - REDIS_QUEUE=redis-erpnext:6379
      - REDIS_SOCKETIO=redis-erpnext:6379
      - SOCKETIO_PORT=9000
    volumes:
      - /opt/ironhorse/erpnext/sites:/home/frappe/frappe-bench/sites
      - /opt/ironhorse/erpnext/logs:/home/frappe/frappe-bench/logs
    depends_on:
      - erpnext-edge-db
      - redis-erpnext
    networks:
      - edge-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # MariaDB for ERPNext edge
  erpnext-edge-db:
    image: mariadb:11.0
    container_name: erpnext-edge-db
    restart: unless-stopped
    environment:
      - MYSQL_ROOT_PASSWORD_FILE=/run/secrets/erpnext_db_root_password
      - MYSQL_DATABASE=erpnext_edge
      - MYSQL_USER=erpnext
      - MYSQL_PASSWORD_FILE=/run/secrets/erpnext_db_password
    volumes:
      - /opt/ironhorse/erpnext/db:/var/lib/mysql
    secrets:
      - erpnext_db_root_password
      - erpnext_db_password
    networks:
      - edge-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Redis for ERPNext
  redis-erpnext:
    image: redis:7-alpine
    container_name: redis-erpnext
    restart: unless-stopped
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - /opt/ironhorse/redis:/data
    networks:
      - edge-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Grafana for local monitoring
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: unless-stopped
    ports:
      - "3000:3000"
    environment:
      - GF_SERVER_ROOT_URL=http://edge.ironhorsesecurity.local:3000
      - GF_SECURITY_ADMIN_PASSWORD__FILE=/run/secrets/grafana_admin_password
      - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-simple-json-datasource
      - GF_AUTH_GENERIC_OAUTH_ENABLED=true
      - GF_AUTH_GENERIC_OAUTH_NAME=Keycloak
      - GF_AUTH_GENERIC_OAUTH_CLIENT_ID=grafana
      - GF_AUTH_GENERIC_OAUTH_CLIENT_SECRET__FILE=/run/secrets/grafana_oauth_secret
      - GF_AUTH_GENERIC_OAUTH_SCOPES=openid email profile
      - GF_AUTH_GENERIC_OAUTH_AUTH_URL=https://auth.ironhorsesecurity.com/realms/ironhorse/protocol/openid-connect/auth
      - GF_AUTH_GENERIC_OAUTH_TOKEN_URL=https://auth.ironhorsesecurity.com/realms/ironhorse/protocol/openid-connect/token
      - GF_AUTH_GENERIC_OAUTH_API_URL=https://auth.ironhorsesecurity.com/realms/ironhorse/protocol/openid-connect/userinfo
    volumes:
      - /opt/ironhorse/grafana/data:/var/lib/grafana
      - /opt/ironhorse/grafana/provisioning:/etc/grafana/provisioning
    secrets:
      - grafana_admin_password
      - grafana_oauth_secret
    networks:
      - edge-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Prometheus for metrics collection
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    ports:
      - "9090:9090"
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
    volumes:
      - /opt/ironhorse/prometheus/config:/etc/prometheus
      - /opt/ironhorse/prometheus/data:/prometheus
    networks:
      - edge-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Wazuh Agent for security monitoring
  wazuh-agent:
    image: wazuh/wazuh-agent:4.7.0
    container_name: wazuh-agent
    restart: unless-stopped
    environment:
      - WAZUH_MANAGER=wazuh.ironhorsesecurity.com
      - WAZUH_AGENT_NAME=edge-${SITE_ID}
      - WAZUH_AGENT_GROUP=edge-sites
    volumes:
      - /opt/ironhorse/wazuh:/var/ossec/data
      - /var/log:/host/var/log:ro
      - /var/run/docker.sock:/var/run/docker.sock:ro
    networks:
      - edge-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # WireGuard VPN to HQ
  wireguard:
    image: linuxserver/wireguard:latest
    container_name: wireguard
    restart: unless-stopped
    cap_add:
      - NET_ADMIN
      - SYS_MODULE
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/Toronto
    volumes:
      - /opt/ironhorse/wireguard/config:/config
      - /lib/modules:/lib/modules
    ports:
      - "51820:51820/udp"
    sysctls:
      - net.ipv4.conf.all.src_valid_mark=1
    networks:
      - edge-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  # Restic backup to HQ MinIO
  restic-backup:
    image: mazzolino/restic:latest
    container_name: restic-backup
    restart: unless-stopped
    environment:
      - RESTIC_REPOSITORY=s3:https://minio.ironhorsesecurity.com/backups-edge-${SITE_ID}
      - RESTIC_PASSWORD_FILE=/run/secrets/restic_password
      - AWS_ACCESS_KEY_ID_FILE=/run/secrets/minio_access_key
      - AWS_SECRET_ACCESS_KEY_FILE=/run/secrets/minio_secret_key
      - BACKUP_CRON=0 2 * * *
      - RESTIC_FORGET_ARGS=--keep-daily 7 --keep-weekly 4 --keep-monthly 12
      - RESTIC_JOB_ARGS=--verbose
      - RESTIC_BACKUP_SOURCES=/data
    volumes:
      - /opt/ironhorse:/data:ro
    secrets:
      - restic_password
      - minio_access_key
      - minio_secret_key
    networks:
      - edge-network
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  edge-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16

secrets:
  zm_db_root_password:
    file: /opt/ironhorse/secrets/zm_db_root_password
  zm_db_password:
    file: /opt/ironhorse/secrets/zm_db_password
  matrix_db_password:
    file: /opt/ironhorse/secrets/matrix_db_password
  erpnext_db_root_password:
    file: /opt/ironhorse/secrets/erpnext_db_root_password
  erpnext_db_password:
    file: /opt/ironhorse/secrets/erpnext_db_password
  grafana_admin_password:
    file: /opt/ironhorse/secrets/grafana_admin_password
  grafana_oauth_secret:
    file: /opt/ironhorse/secrets/grafana_oauth_secret
  restic_password:
    file: /opt/ironhorse/secrets/restic_password
  minio_access_key:
    file: /opt/ironhorse/secrets/minio_access_key
  minio_secret_key:
    file: /opt/ironhorse/secrets/minio_secret_key
```

### Mailu Email Stack

**docker-compose.mailu.yml**
```yaml
version: '3.8'

services:
  # Redis for session storage
  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - /opt/mailu/redis:/data
    depends_on:
      - resolver
    dns:
      - 192.168.203.254

  # Frontend proxy
  front:
    image: ${DOCKER_ORG:-ghcr.io/mailu}/${DOCKER_PREFIX:-}nginx:${MAILU_VERSION:-2.0}
    restart: always
    env_file: mailu.env
    logging:
      driver: journald
      options:
        tag: mailu-front
    ports:
      - "80:80"
      - "443:443"
      - "25:25"
      - "465:465"
      - "587:587"
      - "110:110"
      - "995:995"
      - "143:143"
      - "993:993"
    networks:
      - default
      - webmail
    volumes:
      - /opt/mailu/certs:/certs
      - /opt/mailu/overrides/nginx:/overrides:ro
    depends_on:
      - resolver
    dns:
      - 192.168.203.254

  # DNS resolver
  resolver:
    image: ${DOCKER_ORG:-ghcr.io/mailu}/${DOCKER_PREFIX:-}unbound:${MAILU_VERSION:-2.0}
    env_file: mailu.env
    restart: always
    networks:
      default:
        ipv4_address: 192.168.203.254

  # Admin interface
  admin:
    image: ${DOCKER_ORG:-ghcr.io/mailu}/${DOCKER_PREFIX:-}admin:${MAILU_VERSION:-2.0}
    restart: always
    env_file: mailu.env
    logging:
      driver: journald
      options:
        tag: mailu-admin
    volumes:
      - /opt/mailu/data:/data
      - /opt/mailu/dkim:/dkim
    depends_on:
      - redis
      - resolver
    dns:
      - 192.168.203.254

  # Postfix SMTP server
  smtp:
    image: ${DOCKER_ORG:-ghcr.io/mailu}/${DOCKER_PREFIX:-}postfix:${MAILU_VERSION:-2.0}
    restart: always
    env_file: mailu.env
    logging:
      driver: journald
      options:
        tag: mailu-smtp
    volumes:
      - /opt/mailu/mailqueue:/queue
      - /opt/mailu/overrides/postfix:/overrides:ro
    depends_on:
      - front
      - resolver
    dns:
      - 192.168.203.254

  # Dovecot IMAP server
  imap:
    image: ${DOCKER_ORG:-ghcr.io/mailu}/${DOCKER_PREFIX:-}dovecot:${MAILU_VERSION:-2.0}
    restart: always
    env_file: mailu.env
    logging:
      driver: journald
      options:
        tag: mailu-imap
    volumes:
      - /opt/mailu/mail:/mail
      - /opt/mailu/overrides/dovecot:/overrides:ro
    depends_on:
      - front
      - resolver
    dns:
      - 192.168.203.254

  # Rspamd spam filter
  antispam:
    image: ${DOCKER_ORG:-ghcr.io/mailu}/${DOCKER_PREFIX:-}rspamd:${MAILU_VERSION:-2.0}
    restart: always
    env_file: mailu.env
    logging:
      driver: journald
      options:
        tag: mailu-antispam
    volumes:
      - /opt/mailu/filter:/var/lib/rspamd
      - /opt/mailu/overrides/rspamd:/overrides:ro
    depends_on:
      - front
      - resolver
      - antivirus
    dns:
      - 192.168.203.254

  # ClamAV antivirus
  antivirus:
    image: ${DOCKER_ORG:-ghcr.io/mailu}/${DOCKER_PREFIX:-}clamav:${MAILU_VERSION:-2.0}
    restart: always
    env_file: mailu.env
    logging:
      driver: journald
      options:
        tag: mailu-antivirus
    volumes:
      - /opt/mailu/filter:/data
    depends_on:
      - resolver
    dns:
      - 192.168.203.254

  # Webmail (Roundcube)
  webmail:
    image: ${DOCKER_ORG:-ghcr.io/mailu}/${DOCKER_PREFIX:-}webmail:${MAILU_VERSION:-2.0}
    restart: always
    env_file: mailu.env
    logging:
      driver: journald
      options:
        tag: mailu-webmail
    volumes:
      - /opt/mailu/webmail:/data
      - /opt/mailu/overrides/roundcube:/overrides:ro
    networks:
      - webmail
    depends_on:
      - front

  # Fetchmail for external account polling
  fetchmail:
    image: ${DOCKER_ORG:-ghcr.io/mailu}/${DOCKER_PREFIX:-}fetchmail:${MAILU_VERSION:-2.0}
    restart: always
    env_file: mailu.env
    logging:
      driver: journald
      options:
        tag: mailu-fetchmail
    volumes:
      - /opt/mailu/data/fetchmail:/data
    depends_on:
      - admin
      - smtp
      - imap
      - resolver
    dns:
      - 192.168.203.254

networks:
  default:
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 192.168.203.0/24
  webmail:
    driver: bridge
```

## 1.3 Ansible Playbooks

### Master Playbook Structure

```
ansible/
â”œâ”€â”€ inventory/
â”‚   â”œâ”€â”€ production/
â”‚   â”‚   â”œâ”€â”€ hosts.yml
â”‚   â”‚   â””â”€â”€ group_vars/
â”‚   â”œâ”€â”€ staging/
â”‚   â””â”€â”€ edge_sites/
â”œâ”€â”€ roles/
â”‚   â”œâ”€â”€ common/
â”‚   â”œâ”€â”€ kubernetes/
â”‚   â”œâ”€â”€ keycloak/
â”‚   â”œâ”€â”€ erpnext/
â”‚   â”œâ”€â”€ edge_deployment/
â”‚   â””â”€â”€ security_hardening/
â”œâ”€â”€ playbooks/
â”‚   â”œâ”€â”€ site.yml
â”‚   â”œâ”€â”€ deploy_infrastructure.yml
â”‚   â”œâ”€â”€ deploy_applications.yml
â”‚   â””â”€â”€ security_audit.yml
â””â”€â”€ ansible.cfg
```

### Infrastructure Deployment Playbook

**playbooks/deploy_infrastructure.yml**
```yaml
---
- name: Deploy Iron Horse Infrastructure
  hosts: all
  become: yes
  gather_facts: yes

  vars_files:
    - vars/vault.yml  # Encrypted secrets

  pre_tasks:
    - name: Update apt cache
      apt:
        update_cache: yes
        cache_valid_time: 3600
      when: ansible_os_family == "Debian"

    - name: Install common packages
      package:
        name:
          - vim
          - htop
          - curl
          - wget
          - git
          - python3-pip
          - ufw
          - fail2ban
        state: present

  roles:
    - role: common
      tags: [common]
    
    - role: security_hardening
      tags: [security]
    
    - role: wireguard
      tags: [networking, vpn]
    
    - role: docker
      when: "'edge_sites' in group_names"
      tags: [docker]
    
    - role: kubernetes
      when: "'k8s_cluster' in group_names"
      tags: [kubernetes]

  post_tasks:
    - name: Ensure all services are started
      service:
        name: "{{ item }}"
        state: started
        enabled: yes
      loop:
        - wazuh-agent
        - prometheus-node-exporter
        - wireguard
      ignore_errors: yes

- name: Deploy Kubernetes Control Plane
  hosts: k8s_masters
  become: yes
  roles:
    - role: kubernetes/master
      tags: [k8s-master]

- name: Deploy Kubernetes Workers
  hosts: k8s_workers
  become: yes
  roles:
    - role: kubernetes/worker
      tags: [k8s-worker]

- name: Deploy Storage Cluster
  hosts: ceph_nodes
  become: yes
  roles:
    - role: ceph
      tags: [storage, ceph]

- name: Configure Load Balancers
  hosts: load_balancers
  become: yes
  roles:
    - role: haproxy
      tags: [lb, haproxy]

- name: Deploy Monitoring Stack
  hosts: monitoring
  become: yes
  roles:
    - role: prometheus
      tags: [monitoring, prometheus]
    
    - role: grafana
      tags: [monitoring, grafana]
    
    - role: alertmanager
      tags: [monitoring, alerting]
```

### Keycloak Deployment Role

**roles/keycloak/tasks/main.yml**
```yaml
---
- name: Create Keycloak namespace
  kubernetes.core.k8s:
    state: present
    definition:
      apiVersion: v1
      kind: Namespace
      metadata:
        name: ironhorse-iam
        labels:
          name: ironhorse-iam
          managed-by: ansible

- name: Create PostgreSQL secret for Keycloak
  kubernetes.core.k8s:
    state: present
    definition:
      apiVersion: v1
      kind: Secret
      metadata:
        name: keycloak-db-credentials
        namespace: ironhorse-iam
      type: Opaque
      stringData:
        username: "{{ keycloak_db_username }}"
        password: "{{ keycloak_db_password }}"

- name: Create Keycloak admin secret
  kubernetes.core.k8s:
    state: present
    definition:
      apiVersion: v1
      kind: Secret
      metadata:
        name: keycloak-admin-credentials
        namespace: ironhorse-iam
      type: Opaque
      stringData:
        username: "{{ keycloak_admin_username }}"
        password: "{{ keycloak_admin_password }}"

- name: Deploy Keycloak using Helm
  kubernetes.core.helm:
    name: keycloak
    chart_ref: bitnami/keycloak
    release_namespace: ironhorse-iam
    create_namespace: false
    values: "{{ lookup('template', 'keycloak-values.yaml.j2') | from_yaml }}"
    wait: true
    wait_timeout: 10m

- name: Wait for Keycloak to be ready
  kubernetes.core.k8s_info:
    kind: Deployment
    namespace: ironhorse-iam
    name: keycloak
    wait: yes
    wait_condition:
      type: Available
      status: "True"
    wait_timeout: 600

- name: Get Keycloak service endpoint
  kubernetes.core.k8s_info:
    kind: Service
    namespace: ironhorse-iam
    name: keycloak
  register: keycloak_service

- name: Display Keycloak endpoint
  debug:
    msg: "Keycloak is accessible at: https://auth.ironhorsesecurity.com"

- name: Import Iron Horse realm configuration
  uri:
    url: "https://auth.ironhorsesecurity.com/admin/realms"
    method: POST
    headers:
      Authorization: "Bearer {{ keycloak_admin_token }}"
      Content-Type: "application/json"
    body: "{{ lookup('file', 'files/ironhorse-realm.json') }}"
    body_format: json
    status_code: 201
  register: realm_import
  failed_when: 
    - realm_import.status != 201
    - realm_import.status != 409  # Already exists

- name: Configure Keycloak client for ERPNext
  uri:
    url: "https://auth.ironhorsesecurity.com/admin/realms/ironhorse/clients"
    method: POST
    headers:
      Authorization: "Bearer {{ keycloak_admin_token }}"
      Content-Type: "application/json"
    body:
      clientId: "erpnext"
      name: "ERPNext ERP System"
      enabled: true
      protocol: "openid-connect"
      publicClient: false
      redirectUris:
        - "https://erp.ironhorsesecurity.com/*"
      webOrigins:
        - "https://erp.ironhorsesecurity.com"
      attributes:
        "access.token.lifespan": "900"
        "pkce.code.challenge.method": "S256"
    body_format: json
    status_code: [201, 409]

- name: Create default user groups
  kubernetes.core.k8s:
    state: present
    definition:
      apiVersion: batch/v1
      kind: Job
      metadata:
        name: keycloak-setup-groups
        namespace: ironhorse-iam
      spec:
        template:
          spec:
            containers:
              - name: setup
                image: curlimages/curl:latest
                command:
                  - /bin/sh
                  - -c
                  - |
                    # Script to create groups via Keycloak API
                    TOKEN=$(curl -X POST \
                      https://auth.ironhorsesecurity.com/realms/master/protocol/openid-connect/token \
                      -d "client_id=admin-cli" \
                      -d "username=$KC_ADMIN" \
                      -d "password=$KC_ADMIN_PASSWORD" \
                      -d "grant_type=password" | jq -r '.access_token')
                    
                    for group in "Field Operations" "Management" "IT"; do
                      curl -X POST \
                        https://auth.ironhorsesecurity.com/admin/realms/ironhorse/groups \
                        -H "Authorization: Bearer $TOKEN" \
                        -H "Content-Type: application/json" \
                        -d "{\"name\": \"$group\"}"
                    done
                env:
                  - name: KC_ADMIN
                    valueFrom:
                      secretKeyRef:
                        name: keycloak-admin-credentials
                        key: username
                  - name: KC_ADMIN_PASSWORD
                    valueFrom:
                      secretKeyRef:
                        name: keycloak-admin-credentials
                        key: password
            restartPolicy: OnFailure
```

### Edge Site Deployment Playbook

**playbooks/deploy_edge_site.yml**
```yaml
---
- name: Deploy Iron Horse Edge Site
  hosts: "{{ target_site | default('all_edge_sites') }}"
  become: yes
  gather_facts: yes

  vars:
    site_id: "{{ site_id | mandatory }}"
    site_name: "{{ site_name | mandatory }}"
    hq_wireguard_endpoint: "vpn.ironhorsesecurity.com:51820"
    hq_wireguard_public_key: "{{ vault_hq_wireguard_pubkey }}"

  pre_tasks:
    - name: Validate site configuration
      assert:
        that:
          - site_id is defined
          - site_name is defined
          - ansible_architecture == "aarch64" or ansible_architecture == "x86_64"
        fail_msg: "Missing required site configuration variables"

    - name: Create Iron Horse directory structure
      file:
        path: "{{ item }}"
        state: directory
        mode: '0755'
      loop:
        - /opt/ironhorse
        - /opt/ironhorse/secrets
        - /opt/ironhorse/certs
        - /opt/ironhorse/zoneminder/config
        - /opt/ironhorse/zoneminder/data
        - /opt/ironhorse/openhab/conf
        - /opt/ironhorse/openhab/userdata
        - /opt/ironhorse/nodered
        - /opt/ironhorse/mosquitto/config
        - /opt/ironhorse/matrix/data
        - /opt/ironhorse/erpnext/sites
        - /opt/ironhorse/grafana/data
        - /opt/ironhorse/prometheus/config
        - /opt/ironhorse/wazuh
        - /opt/ironhorse/wireguard/config
        - /mnt/cctv-storage

  tasks:
    - name: Install Docker
      include_role:
        name: docker
      tags: [docker]

    - name: Install Docker Compose
      get_url:
        url: "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-linux-{{ 'aarch64' if ansible_architecture == 'aarch64' else 'x86_64' }}"
        dest: /usr/local/bin/docker-compose
        mode: '0755'

    - name: Configure WireGuard VPN to HQ
      include_role:
        name: wireguard
      vars:
        wg_interface: wg0
        wg_address: "10.10.{{ site_id }}.1/24"
        wg_peers:
          - name: "hq"
            public_key: "{{ hq_wireguard_public_key }}"
            endpoint: "{{ hq_wireguard_endpoint }}"
            allowed_ips: "10.10.0.0/16,172.16.0.0/12"
            persistent_keepalive: 25

    - name: Generate site-specific secrets
      include_role:
        name: generate_secrets
      vars:
        secret_files:
          - name: zm_db_root_password
            length: 32
          - name: zm_db_password
            length: 32
          - name: matrix_db_password
            length: 32
          - name: erpnext_db_root_password
            length: 32
          - name: erpnext_db_password
            length: 32
          - name: grafana_admin_password
            length: 16
          - name: restic_password
            length: 32

    - name: Copy MinIO credentials from HQ
      copy:
        content: "{{ item.content }}"
        dest: "/opt/ironhorse/secrets/{{ item.name }}"
        mode: '0600'
      loop:
        - name: minio_access_key
          content: "{{ vault_minio_access_key }}"
        - name: minio_secret_key
          content: "{{ vault_minio_secret_key }}"
      no_log: true

    - name: Deploy edge services
      template:
        src: docker-compose.edge.yml.j2
        dest: /opt/ironhorse/docker-compose.yml
        mode: '0644'

    - name: Create .env file for Docker Compose
      template:
        src: edge.env.j2
        dest: /opt/ironhorse/.env
        mode: '0600'

    - name: Start edge services
      community.docker.docker_compose:
        project_src: /opt/ironhorse
        state: present
        pull: yes
      register: docker_output

    - name: Configure ZoneMinder
      include_role:
        name: zoneminder
      vars:
        zm_admin_password: "{{ lookup('password', '/opt/ironhorse/secrets/zm_admin_password length=16') }}"

    - name: Configure OpenHAB access control
      include_role:
        name: openhab
      vars:
        openhab_admin_password: "{{ lookup('password', '/opt/ironhorse/secrets/openhab_admin_password length=16') }}"

    - name: Import Node-RED flows
      copy:
        src: files/nodered-flows.json
        dest: /opt/ironhorse/nodered/flows.json
        mode: '0644'

    - name: Configure Mosquitto MQTT broker
      template:
        src: mosquitto.conf.j2
        dest: /opt/ironhorse/mosquitto/config/mosquitto.conf
        mode: '0644'
      notify: restart mosquitto

    - name: Configure Grafana dashboards
      include_role:
        name: grafana
      vars:
        grafana_admin_password: "{{ lookup('file', '/opt/ironhorse/secrets/grafana_admin_password') }}"
        grafana_dashboards:
          - site_overview
          - patrol_tracking
          - cctv_analytics
          - system_health

    - name: Configure Prometheus monitoring
      template:
        src: prometheus.yml.j2
        dest: /opt/ironhorse/prometheus/config/prometheus.yml
        mode: '0644'
      notify: restart prometheus

    - name: Deploy Wazuh agent
      include_role:
        name: wazuh_agent
      vars:
        wazuh_manager: "wazuh.ironhorsesecurity.com"
        wazuh_agent_name: "edge-{{ site_id }}"
        wazuh_agent_groups: "edge-sites"

    - name: Initialize Restic backup repository
      shell: |
        export RESTIC_REPOSITORY=s3:https://minio.ironhorsesecurity.com/backups-edge-{{ site_id }}
        export RESTIC_PASSWORD=$(cat /opt/ironhorse/secrets/restic_password)
        export AWS_ACCESS_KEY_ID=$(cat /opt/ironhorse/secrets/minio_access_key)
        export AWS_SECRET_ACCESS_KEY=$(cat /opt/ironhorse/secrets/minio_secret_key)
        restic init || true
      args:
        creates: /opt/ironhorse/.restic_initialized

    - name: Register site with HQ ERPNext
      uri:
        url: "https://erp.ironhorsesecurity.com/api/resource/Site"
        method: POST
        headers:
          Authorization: "token {{ erpnext_api_key }}:{{ erpnext_api_secret }}"
          Content-Type: "application/json"
        body:
          site_id: "{{ site_id }}"
          site_name: "{{ site_name }}"
          site_type: "Edge"
          ip_address: "{{ ansible_default_ipv4.address }}"
          wireguard_address: "10.10.{{ site_id }}.1"
          status: "Active"
          deployed_date: "{{ ansible_date_time.iso8601 }}"
        body_format: json
        status_code: [200, 409]

  post_tasks:
    - name: Verify all services are running
      community.docker.docker_container_info:
        name: "{{ item }}"
      loop:
        - zoneminder
        - openhab
        - nodered
        - mosquitto
        - matrix-synapse
        - erpnext-edge
        - grafana
        - prometheus
        - wazuh-agent
        - wireguard
      register: service_status
      failed_when: service_status.container.State.Running != true

    - name: Display site deployment summary
      debug:
        msg:
          - "=== Edge Site Deployment Complete ==="
          - "Site ID: {{ site_id }}"
          - "Site Name: {{ site_name }}"
          - "WireGuard IP: 10.10.{{ site_id }}.1"
          - "Local Access:"
          - "  - ZoneMinder: http://{{ ansible_default_ipv4.address }}:8080"
          - "  - OpenHAB: http://{{ ansible_default_ipv4.address }}:8081"
          - "  - Node-RED: http://{{ ansible_default_ipv4.address }}:1880"
          - "  - Grafana: http://{{ ansible_default_ipv4.address }}:3000"
          - "  - ERPNext: http://{{ ansible_default_ipv4.address }}:8000"
          - "Backup: Restic to MinIO backups-edge-{{ site_id }}"
          - "Monitoring: Wazuh agent connected to HQ"

  handlers:
    - name: restart mosquitto
      community.docker.docker_compose:
        project_src: /opt/ironhorse
        services:
          - mosquitto
        restarted: yes

    - name: restart prometheus
      community.docker.docker_compose:
        project_src: /opt/ironhorse
        services:
          - prometheus
        restarted: yes
```

## 1.4 Terraform Modules

### Infrastructure as Code Structure

```
terraform/
â”œâ”€â”€ modules/
â”‚   â”œâ”€â”€ kubernetes-cluster/
â”‚   â”œâ”€â”€ ceph-storage/
â”‚   â”œâ”€â”€ networking/
â”‚   â”œâ”€â”€ security/
â”‚   â””â”€â”€ monitoring/
â”œâ”€â”€ environments/
â”‚   â”œâ”€â”€ production/
â”‚   â”œâ”€â”€ staging/
â”‚   â””â”€â”€ edge/
â””â”€â”€ main.tf
```

### Kubernetes Cluster Module

**modules/kubernetes-cluster/main.tf**
```hcl
# Iron Horse Kubernetes Cluster Module
# Supports AWS EKS, Azure AKS, and on-premises bare-metal

variable "environment" {
  description = "Environment name (production, staging, edge)"
  type        = string
}

variable "cluster_name" {
  description = "Kubernetes cluster name"
  type        = string
}

variable "provider_type" {
  description = "Infrastructure provider (aws, azure, bare-metal)"
  type        = string
  validation {
    condition     = contains(["aws", "azure", "bare-metal"], var.provider_type)
    error_message = "Provider must be aws, azure, or bare-metal."
  }
}

variable "node_count" {
  description = "Number of worker nodes"
  type        = number
  default     = 3
}

variable "node_instance_type" {
  description = "Instance type for worker nodes"
  type        = string
  default     = "t3.xlarge"  # AWS default
}

variable "kubernetes_version" {
  description = "Kubernetes version"
  type        = string
  default     = "1.28"
}

variable "enable_monitoring" {
  description = "Enable Prometheus/Grafana monitoring stack"
  type        = bool
  default     = true
}

variable "enable_backup" {
  description = "Enable Velero backup integration"
  type        = bool
  default     = true
}

variable "vpc_cidr" {
  description = "VPC CIDR block"
  type        = string
  default     = "10.0.0.0/16"
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}

# AWS EKS Implementation
module "eks_cluster" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"
  count   = var.provider_type == "aws" ? 1 : 0

  cluster_name    = var.cluster_name
  cluster_version = var.kubernetes_version

  cluster_endpoint_public_access  = true
  cluster_endpoint_private_access = true

  cluster_addons = {
    coredns = {
      most_recent = true
    }
    kube-proxy = {
      most_recent = true
    }
    vpc-cni = {
      most_recent = true
    }
    aws-ebs-csi-driver = {
      most_recent = true
    }
  }

  vpc_id     = module.vpc[0].vpc_id
  subnet_ids = module.vpc[0].private_subnets

  # Managed node groups
  eks_managed_node_groups = {
    general = {
      name         = "${var.cluster_name}-general"
      min_size     = 3
      max_size     = 10
      desired_size = var.node_count

      instance_types = [var.node_instance_type]
      capacity_type  = "ON_DEMAND"

      labels = {
        role        = "general"
        environment = var.environment
      }

      taints = []

      tags = merge(
        var.tags,
        {
          NodeGroup = "general"
        }
      )
    }

    monitoring = {
      name         = "${var.cluster_name}-monitoring"
      min_size     = 2
      max_size     = 5
      desired_size = 2

      instance_types = ["t3.large"]
      capacity_type  = "SPOT"

      labels = {
        role        = "monitoring"
        environment = var.environment
      }

      taints = [
        {
          key    = "monitoring"
          value  = "true"
          effect = "NoSchedule"
        }
      ]

      tags = merge(
        var.tags,
        {
          NodeGroup = "monitoring"
        }
      )
    }
  }

  # OIDC provider for service accounts
  enable_irsa = true

  # Cluster security group rules
  cluster_security_group_additional_rules = {
    ingress_nodes_ephemeral_ports_tcp = {
      description                = "Nodes on ephemeral ports"
      protocol                   = "tcp"
      from_port                  = 1025
      to_port                    = 65535
      type                       = "ingress"
      source_node_security_group = true
    }
  }

  # Node security group rules
  node_security_group_additional_rules = {
    ingress_self_all = {
      description = "Node to node all traffic"
      protocol    = "-1"
      from_port   = 0
      to_port     = 0
      type        = "ingress"
      self        = true
    }
    
    ingress_cluster_all = {
      description                   = "Cluster to node all traffic"
      protocol                      = "-1"
      from_port                     = 0
      to_port                       = 0
      type                          = "ingress"
      source_cluster_security_group = true
    }
    
    egress_all = {
      description      = "Node all egress"
      protocol         = "-1"
      from_port        = 0
      to_port          = 0
      type             = "egress"
      cidr_blocks      = ["0.0.0.0/0"]
      ipv6_cidr_blocks = ["::/0"]
    }
  }

  tags = merge(
    var.tags,
    {
      Terraform   = "true"
      Environment = var.environment
      Platform    = "ironhorse"
    }
  )
}

# VPC Module for AWS
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"
  count   = var.provider_type == "aws" ? 1 : 0

  name = "${var.cluster_name}-vpc"
  cidr = var.vpc_cidr

  azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
  private_subnets = [
    cidrsubnet(var.vpc_cidr, 4, 0),
    cidrsubnet(var.vpc_cidr, 4, 1),
    cidrsubnet(var.vpc_cidr, 4, 2)
  ]
  public_subnets = [
    cidrsubnet(var.vpc_cidr, 8, 0),
    cidrsubnet(var.vpc_cidr, 8, 1),
    cidrsubnet(var.vpc_cidr, 8, 2)
  ]

  enable_nat_gateway   = true
  single_nat_gateway   = false
  enable_dns_hostnames = true
  enable_dns_support   = true

  enable_flow_log                      = true
  create_flow_log_cloudwatch_iam_role  = true
  create_flow_log_cloudwatch_log_group = true

  public_subnet_tags = {
    "kubernetes.io/role/elb" = 1
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb" = 1
  }

  tags = var.tags
}

# Azure AKS Implementation
resource "azurerm_kubernetes_cluster" "main" {
  count               = var.provider_type == "azure" ? 1 : 0
  name                = var.cluster_name
  location            = var.azure_location
  resource_group_name = azurerm_resource_group.main[0].name
  dns_prefix          = var.cluster_name
  kubernetes_version  = var.kubernetes_version

  default_node_pool {
    name                = "general"
    node_count          = var.node_count
    vm_size             = var.node_instance_type
    type                = "VirtualMachineScaleSets"
    availability_zones  = ["1", "2", "3"]
    enable_auto_scaling = true
    min_count           = 3
    max_count           = 10

    node_labels = {
      role        = "general"
      environment = var.environment
    }
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin     = "azure"
    network_policy     = "azure"
    load_balancer_sku  = "standard"
    service_cidr       = "10.1.0.0/16"
    dns_service_ip     = "10.1.0.10"
  }

  oms_agent {
    log_analytics_workspace_id = azurerm_log_analytics_workspace.main[0].id
  }

  tags = var.tags
}

# Bare-metal cluster configuration
resource "null_resource" "bare_metal_cluster" {
  count = var.provider_type == "bare-metal" ? 1 : 0

  provisioner "local-exec" {
    command = <<-EOT
      ansible-playbook \
        -i ${var.inventory_file} \
        playbooks/deploy_kubernetes_cluster.yml \
        -e cluster_name=${var.cluster_name} \
        -e kubernetes_version=${var.kubernetes_version} \
        -e node_count=${var.node_count}
    EOT
  }
}

# Install Cert-Manager
resource "helm_release" "cert_manager" {
  name             = "cert-manager"
  repository       = "https://charts.jetstack.io"
  chart            = "cert-manager"
  namespace        = "cert-manager"
  create_namespace = true
  version          = "v1.13.0"

  set {
    name  = "installCRDs"
    value = "true"
  }

  set {
    name  = "global.leaderElection.namespace"
    value = "cert-manager"
  }
}

# Install NGINX Ingress Controller
resource "helm_release" "nginx_ingress" {
  name             = "ingress-nginx"
  repository       = "https://kubernetes.github.io/ingress-nginx"
  chart            = "ingress-nginx"
  namespace        = "ingress-nginx"
  create_namespace = true
  version          = "4.8.0"

  values = [
    templatefile("${path.module}/templates/nginx-ingress-values.yaml", {
      replica_count = 3
      enable_metrics = var.enable_monitoring
    })
  ]
}

# Install Prometheus/Grafana stack
resource "helm_release" "kube_prometheus_stack" {
  count            = var.enable_monitoring ? 1 : 0
  name             = "kube-prometheus-stack"
  repository       = "https://prometheus-community.github.io/helm-charts"
  chart            = "kube-prometheus-stack"
  namespace        = "monitoring"
  create_namespace = true
  version          = "51.0.0"

  values = [
    templatefile("${path.module}/templates/prometheus-stack-values.yaml", {
      grafana_admin_password = random_password.grafana_admin[0].result
      retention_days         = 30
      storage_size          = "100Gi"
    })
  ]
}

# Install Velero for backups
resource "helm_release" "velero" {
  count            = var.enable_backup ? 1 : 0
  name             = "velero"
  repository       = "https://vmware-tanzu.github.io/helm-charts"
  chart            = "velero"
  namespace        = "velero"
  create_namespace = true
  version          = "5.1.0"

  values = [
    templatefile("${path.module}/templates/velero-values.yaml", {
      provider              = var.provider_type
      backup_location       = var.backup_location
      s3_url               = var.backup_s3_url
      s3_bucket            = var.backup_s3_bucket
      aws_access_key_id    = var.backup_aws_access_key
      aws_secret_access_key = var.backup_aws_secret_key
    })
  ]
}

# Random password for Grafana
resource "random_password" "grafana_admin" {
  count   = var.enable_monitoring ? 1 : 0
  length  = 16
  special = true
}

# Outputs
output "cluster_endpoint" {
  description = "Kubernetes cluster endpoint"
  value = var.provider_type == "aws" ? module.eks_cluster[0].cluster_endpoint : (
    var.provider_type == "azure" ? azurerm_kubernetes_cluster.main[0].kube_config[0].host : 
    "Configured via Ansible"
  )
}

output "cluster_ca_certificate" {
  description = "Cluster CA certificate"
  sensitive   = true
  value = var.provider_type == "aws" ? module.eks_cluster[0].cluster_certificate_authority_data : (
    var.provider_type == "azure" ? azurerm_kubernetes_cluster.main[0].kube_config[0].cluster_ca_certificate : 
    "Configured via Ansible"
  )
}

output "kubeconfig_command" {
  description = "Command to configure kubectl"
  value = var.provider_type == "aws" ? "aws eks update-kubeconfig --region us-east-1 --name ${var.cluster_name}" : (
    var.provider_type == "azure" ? "az aks get-credentials --resource-group ${azurerm_resource_group.main[0].name} --name ${var.cluster_name}" :
    "Copy kubeconfig from /etc/kubernetes/admin.conf on master node"
  )
}

output "grafana_password" {
  description = "Grafana admin password"
  sensitive   = true
  value       = var.enable_monitoring ? random_password.grafana_admin[0].result : null
}
```

This is getting quite long. Let me continue with the remaining sections in the next part. Would you like me to continue with:

1. **Data Flow & API Contracts** (OpenAPI, GraphQL, Kafka schemas)
2. **DevSecOps Pipeline** (GitLab CI/CD, security scanning)

Or would you prefer I create these as separate documents?

