---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: 2027d371-2448-486b-b93f-15b9c3623c4f
original_filename: 05-kubernetes-manifests.yml
created_at: 2025-12-02T00:47:53.944256+00:00
content_hash: a70faedca0ef
topic: ihose-deployment-infrastructure
---

# OpenVision Platform - Kubernetes Deployment Manifests
# Suitable for: Enterprise deployments (50+ cameras), Multi-site, High Availability
# Requirements: Kubernetes 1.25+, kubectl, Helm 3.0+

---
apiVersion: v1
kind: Namespace
metadata:
  name: openvision
  labels:
    name: openvision
    environment: production

---
# Storage Classes
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: openvision-fast
  namespace: openvision
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
# For video hot storage (NVMe)

---
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: openvision-standard
  namespace: openvision
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
# For warm storage (HDD RAID)

---
# ConfigMaps
apiVersion: v1
kind: ConfigMap
metadata:
  name: openvision-config
  namespace: openvision
data:
  ENVIRONMENT: "production"
  LOG_LEVEL: "INFO"
  TIMEZONE: "UTC"
  RETENTION_DAYS: "90"
  MAX_CAMERAS_PER_NODE: "50"

---
# Secrets (Base64 encoded - replace with actual values)
apiVersion: v1
kind: Secret
metadata:
  name: openvision-secrets
  namespace: openvision
type: Opaque
data:
  POSTGRES_PASSWORD: b3BlbnZpc2lvbl9zZWN1cmU=  # Change this!
  REDIS_PASSWORD: cmVkaXNfc2VjdXJl  # Change this!
  MINIO_ROOT_PASSWORD: bWluaW9fc2VjdXJl  # Change this!
  KEYCLOAK_ADMIN_PASSWORD: a2V5Y2xvYWtfc2VjdXJl  # Change this!

---
# PostgreSQL with TimescaleDB
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgres
  namespace: openvision
spec:
  serviceName: postgres
  replicas: 3  # Primary + 2 replicas
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: timescale/timescaledb:latest-pg15
        ports:
        - containerPort: 5432
          name: postgres
        env:
        - name: POSTGRES_USER
          value: "openvision"
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: openvision-secrets
              key: POSTGRES_PASSWORD
        - name: PGDATA
          value: /var/lib/postgresql/data/pgdata
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
        resources:
          requests:
            memory: "8Gi"
            cpu: "2000m"
          limits:
            memory: "16Gi"
            cpu: "4000m"
  volumeClaimTemplates:
  - metadata:
      name: postgres-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: openvision-standard
      resources:
        requests:
          storage: 500Gi

---
apiVersion: v1
kind: Service
metadata:
  name: postgres
  namespace: openvision
spec:
  clusterIP: None
  selector:
    app: postgres
  ports:
  - port: 5432
    targetPort: 5432

---
# Redis Cluster
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis
  namespace: openvision
spec:
  serviceName: redis
  replicas: 6  # 3 master + 3 replica
  selector:
    matchLabels:
      app: redis
  template:
    metadata:
      labels:
        app: redis
    spec:
      containers:
      - name: redis
        image: redis:7-alpine
        ports:
        - containerPort: 6379
          name: client
        - containerPort: 16379
          name: gossip
        command:
        - redis-server
        - /conf/redis.conf
        - --requirepass
        - $(REDIS_PASSWORD)
        env:
        - name: REDIS_PASSWORD
          valueFrom:
            secretKeyRef:
              name: openvision-secrets
              key: REDIS_PASSWORD
        volumeMounts:
        - name: redis-storage
          mountPath: /data
        - name: redis-config
          mountPath: /conf
        resources:
          requests:
            memory: "4Gi"
            cpu: "1000m"
          limits:
            memory: "8Gi"
            cpu: "2000m"
      volumes:
      - name: redis-config
        configMap:
          name: redis-config
  volumeClaimTemplates:
  - metadata:
      name: redis-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 50Gi

---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: openvision
spec:
  clusterIP: None
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
    name: client
  - port: 16379
    targetPort: 16379
    name: gossip

---
# NATS JetStream
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: nats
  namespace: openvision
spec:
  serviceName: nats
  replicas: 3
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
        ports:
        - containerPort: 4222
          name: client
        - containerPort: 6222
          name: cluster
        - containerPort: 8222
          name: monitor
        command:
        - nats-server
        - --config
        - /etc/nats-config/nats.conf
        volumeMounts:
        - name: nats-storage
          mountPath: /data
        - name: nats-config
          mountPath: /etc/nats-config
        resources:
          requests:
            memory: "4Gi"
            cpu: "1000m"
          limits:
            memory: "8Gi"
            cpu: "2000m"
      volumes:
      - name: nats-config
        configMap:
          name: nats-config
  volumeClaimTemplates:
  - metadata:
      name: nats-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 100Gi

---
apiVersion: v1
kind: Service
metadata:
  name: nats
  namespace: openvision
spec:
  selector:
    app: nats
  ports:
  - port: 4222
    targetPort: 4222
    name: client
  - port: 6222
    targetPort: 6222
    name: cluster
  - port: 8222
    targetPort: 8222
    name: monitor

---
# MinIO Distributed Object Storage
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: minio
  namespace: openvision
spec:
  serviceName: minio
  replicas: 4  # Minimum for distributed mode
  selector:
    matchLabels:
      app: minio
  template:
    metadata:
      labels:
        app: minio
    spec:
      containers:
      - name: minio
        image: minio/minio:latest
        args:
        - server
        - http://minio-{0...3}.minio.openvision.svc.cluster.local/data
        - --console-address
        - ":9001"
        env:
        - name: MINIO_ROOT_USER
          value: "openvision"
        - name: MINIO_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
              name: openvision-secrets
              key: MINIO_ROOT_PASSWORD
        ports:
        - containerPort: 9000
          name: api
        - containerPort: 9001
          name: console
        volumeMounts:
        - name: minio-storage
          mountPath: /data
        resources:
          requests:
            memory: "8Gi"
            cpu: "2000m"
          limits:
            memory: "16Gi"
            cpu: "4000m"
  volumeClaimTemplates:
  - metadata:
      name: minio-storage
    spec:
      accessModes: [ "ReadWriteOnce" ]
      storageClassName: openvision-standard
      resources:
        requests:
          storage: 5Ti  # 5TB per node = 20TB total

---
apiVersion: v1
kind: Service
metadata:
  name: minio
  namespace: openvision
spec:
  clusterIP: None
  selector:
    app: minio
  ports:
  - port: 9000
    targetPort: 9000
    name: api
  - port: 9001
    targetPort: 9001
    name: console

---
# MediaMTX Stream Server
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mediamtx
  namespace: openvision
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mediamtx
  template:
    metadata:
      labels:
        app: mediamtx
    spec:
      containers:
      - name: mediamtx
        image: bluenviron/mediamtx:latest
        ports:
        - containerPort: 8554
          name: rtsp
        - containerPort: 8888
          name: webrtc
        - containerPort: 8889
          name: hls
        volumeMounts:
        - name: mediamtx-config
          mountPath: /mediamtx.yml
          subPath: mediamtx.yml
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
      volumes:
      - name: mediamtx-config
        configMap:
          name: mediamtx-config

---
apiVersion: v1
kind: Service
metadata:
  name: mediamtx
  namespace: openvision
spec:
  type: LoadBalancer
  selector:
    app: mediamtx
  ports:
  - port: 8554
    targetPort: 8554
    name: rtsp
  - port: 8888
    targetPort: 8888
    name: webrtc
  - port: 8889
    targetPort: 8889
    name: hls

---
# Shinobi VMS
apiVersion: apps/v1
kind: Deployment
metadata:
  name: shinobi
  namespace: openvision
spec:
  replicas: 2
  selector:
    matchLabels:
      app: shinobi
  template:
    metadata:
      labels:
        app: shinobi
    spec:
      containers:
      - name: shinobi
        image: shinobi/shinobi:latest
        ports:
        - containerPort: 8080
          name: http
        env:
        - name: DB_HOST
          value: "postgres"
        - name: DB_USER
          value: "shinobi"
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: openvision-secrets
              key: POSTGRES_PASSWORD
        - name: DB_DATABASE
          value: "shinobi"
        volumeMounts:
        - name: shinobi-videos
          mountPath: /home/Shinobi/videos
        resources:
          requests:
            memory: "4Gi"
            cpu: "2000m"
          limits:
            memory: "8Gi"
            cpu: "4000m"
      volumes:
      - name: shinobi-videos
        persistentVolumeClaim:
          claimName: shinobi-videos-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: shinobi
  namespace: openvision
spec:
  type: ClusterIP
  selector:
    app: shinobi
  ports:
  - port: 8080
    targetPort: 8080

---
# YOLO Object Detection
apiVersion: apps/v1
kind: Deployment
metadata:
  name: yolo-detector
  namespace: openvision
spec:
  replicas: 4
  selector:
    matchLabels:
      app: yolo-detector
  template:
    metadata:
      labels:
        app: yolo-detector
    spec:
      nodeSelector:
        nvidia.com/gpu: "true"
      containers:
      - name: yolo
        image: ultralytics/ultralytics:latest
        command: ["python", "-m", "openvision.modules.yolo"]
        env:
        - name: MODEL_PATH
          value: "/models/yolov8n.pt"
        - name: CONFIDENCE_THRESHOLD
          value: "0.5"
        - name: NATS_URL
          value: "nats://nats:4222"
        volumeMounts:
        - name: models
          mountPath: /models
        resources:
          requests:
            memory: "4Gi"
            cpu: "2000m"
            nvidia.com/gpu: 1
          limits:
            memory: "8Gi"
            cpu: "4000m"
            nvidia.com/gpu: 1
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: ml-models-pvc

---
# Grafana
apiVersion: apps/v1
kind: Deployment
metadata:
  name: grafana
  namespace: openvision
spec:
  replicas: 2
  selector:
    matchLabels:
      app: grafana
  template:
    metadata:
      labels:
        app: grafana
    spec:
      containers:
      - name: grafana
        image: grafana/grafana:latest
        ports:
        - containerPort: 3000
          name: http
        env:
        - name: GF_SECURITY_ADMIN_PASSWORD
          valueFrom:
            secretKeyRef:
              name: openvision-secrets
              key: POSTGRES_PASSWORD
        volumeMounts:
        - name: grafana-storage
          mountPath: /var/lib/grafana
        resources:
          requests:
            memory: "2Gi"
            cpu: "500m"
          limits:
            memory: "4Gi"
            cpu: "1000m"
      volumes:
      - name: grafana-storage
        persistentVolumeClaim:
          claimName: grafana-pvc

---
apiVersion: v1
kind: Service
metadata:
  name: grafana
  namespace: openvision
spec:
  type: LoadBalancer
  selector:
    app: grafana
  ports:
  - port: 3000
    targetPort: 3000

---
# HorizontalPodAutoscaler for YOLO
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: yolo-detector-hpa
  namespace: openvision
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: yolo-detector
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80

---
# NetworkPolicy - Restrict traffic between components
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-all
  namespace: openvision
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  - Egress

---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-database-access
  namespace: openvision
spec:
  podSelector:
    matchLabels:
      app: postgres
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          role: application
    ports:
    - protocol: TCP
      port: 5432

# ====================  Deployment Instructions ====================
#
# 1. Prerequisites:
#    kubectl apply -f https://raw.githubusercontent.com/NVIDIA/k8s-device-plugin/v0.13.0/nvidia-device-plugin.yml
#    helm repo add jetstack https://charts.jetstack.io
#    helm install cert-manager jetstack/cert-manager --namespace cert-manager --create-namespace
#
# 2. Deploy namespace and base resources:
#    kubectl apply -f 05-kubernetes-base.yml
#
# 3. Update secrets:
#    kubectl create secret generic openvision-secrets -n openvision \
#      --from-literal=POSTGRES_PASSWORD=<your-secure-password> \
#      --from-literal=REDIS_PASSWORD=<your-secure-password> \
#      --from-literal=MINIO_ROOT_PASSWORD=<your-secure-password> \
#      --from-literal=KEYCLOAK_ADMIN_PASSWORD=<your-secure-password> \
#      --dry-run=client -o yaml | kubectl apply -f -
#
# 4. Deploy all components:
#    kubectl apply -f 05-kubernetes-base.yml
#    kubectl apply -f 06-kubernetes-analytics.yml
#    kubectl apply -f 07-kubernetes-observability.yml
#
# 5. Verify deployment:
#    kubectl get pods -n openvision
#    kubectl get svc -n openvision
#
# 6. Access services:
#    kubectl port-forward -n openvision svc/grafana 3000:3000
#    Open http://localhost:3000
#
# 7. Scale for production:
#    kubectl scale deployment yolo-detector -n openvision --replicas=10
#
# 8. Monitor:
#    kubectl top pods -n openvision
#    kubectl logs -f -n openvision deployment/yolo-detector
#
