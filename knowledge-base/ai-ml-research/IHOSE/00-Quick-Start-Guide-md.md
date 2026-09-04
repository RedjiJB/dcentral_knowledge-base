---
source_project: IHOSE
source_project_uuid: 019a6ba2-1cf8-703d-b379-bb50cd7fad34
doc_uuid: 0184a391-b416-4fd5-9c40-81e57e42f883
original_filename: 00-Quick-Start-Guide.md
created_at: 2025-12-02T00:47:54.552334+00:00
content_hash: 4e09e21e0155cross_category_duplicate_at: "security-identity/Open-Vision/00-Quick-Start-Guide-md.md"topic: yml-compose-frigate
---

# OpenVision Platform
## Quick Start Guide

**Get started in 30 minutes or less**

---

## What is OpenVision Platform?

OpenVision is a **fully open-source, enterprise-grade video surveillance and IoT integration platform** that provides:

✅ **Zero licensing costs** - 100% open source  
✅ **Unlimited customization** - Plugin architecture  
✅ **30-50% cost savings** - vs. commercial solutions  
✅ **No vendor lock-in** - Complete control  
✅ **Edge-first AI** - Process locally, reduce cloud costs  

---

## Who Should Use This Guide?

- **Developers** - Test the platform locally
- **IT Admins** - Quick deployment for evaluation
- **Decision Makers** - Hands-on proof of concept
- **Anyone** - Curious about the platform capabilities

---

## Prerequisites

Before starting, ensure you have:

- **Hardware:** Computer with 8GB RAM, 50GB disk space
- **Software:** Docker and Docker Compose installed
- **Network:** Internet connection
- **Camera (Optional):** IP camera with RTSP stream OR use test stream

### Install Docker (If Not Already Installed)

**Ubuntu/Debian:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
# Log out and back in
```

**macOS:**
```bash
# Download Docker Desktop from docker.com
# Install and start Docker Desktop
```

**Windows:**
```bash
# Download Docker Desktop from docker.com
# Install and start Docker Desktop
```

**Verify Installation:**
```bash
docker --version
docker-compose --version
```

---

## Quick Deployment (Docker Compose)

### Step 1: Get the Code

```bash
# Create project directory
mkdir -p ~/openvision-platform
cd ~/openvision-platform

# Download docker-compose file
curl -O https://raw.githubusercontent.com/openvision/platform/main/docker-compose.yml

# Download example configuration
curl -O https://raw.githubusercontent.com/openvision/platform/main/configs/env.example
mv env.example .env
```

### Step 2: Configure Environment

```bash
# Edit configuration
nano .env

# Minimal required changes:
# - Set strong passwords (auto-generated recommended)
# - Adjust camera settings if you have real cameras
```

**Quick Password Generation:**
```bash
# Generate secure passwords
export POSTGRES_PASSWORD=$(openssl rand -base64 32)
export REDIS_PASSWORD=$(openssl rand -base64 32)
export JWT_SECRET=$(openssl rand -base64 64)

# Update .env file
sed -i "s/POSTGRES_PASSWORD=.*/POSTGRES_PASSWORD=$POSTGRES_PASSWORD/" .env
sed -i "s/REDIS_PASSWORD=.*/REDIS_PASSWORD=$REDIS_PASSWORD/" .env
sed -i "s/JWT_SECRET=.*/JWT_SECRET=$JWT_SECRET/" .env
```

### Step 3: Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Wait for services to initialize (1-2 minutes)
```

### Step 4: Access Web Interfaces

Open your browser and navigate to:

| Service | URL | Default Credentials |
|---------|-----|---------------------|
| **Frigate (VMS)** | http://localhost:5000 | No authentication (demo) |
| **Grafana** | http://localhost:3000 | admin / (see .env) |
| **Node-RED** | http://localhost:1880 | No authentication (demo) |
| **MinIO Console** | http://localhost:9001 | minioadmin / (see .env) |

---

## Configure Your First Camera

### Option 1: Use Test Stream (No Camera Required)

Edit camera configuration:

```bash
nano configs/frigate.yml
```

Add test camera:

```yaml
cameras:
  test_camera:
    enabled: true
    ffmpeg:
      inputs:
        - path: rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mp4
          roles:
            - detect
            - record
    detect:
      enabled: true
      width: 1280
      height: 720
    record:
      enabled: true
      retain:
        days: 7
        mode: all
```

### Option 2: Add Real IP Camera

Find your camera's RTSP URL (check camera documentation), then:

```yaml
cameras:
  front_door:
    enabled: true
    ffmpeg:
      inputs:
        - path: rtsp://username:password@192.168.1.100:554/stream1
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
        days: 30
        mode: motion
    objects:
      track:
        - person
        - car
        - dog
```

**Restart Frigate:**
```bash
docker-compose restart frigate
```

---

## Enable AI Analytics

### Object Detection (YOLO)

YOLO is enabled by default. To customize:

```bash
nano configs/analytics.yml
```

```yaml
analytics:
  yolo:
    enabled: true
    model: yolov8n.pt  # or yolov8s.pt for better accuracy
    confidence: 0.7
    classes:
      - person
      - car
      - truck
      - bicycle
```

**Restart analytics service:**
```bash
docker-compose restart yolo-analytics
```

### View Detections

1. Open Frigate: http://localhost:5000
2. Click on camera
3. View live stream with bounding boxes
4. Check Events tab for recorded detections

---

## Set Up Alerts

### Configure Email Alerts (Optional)

```bash
nano .env
```

Update SMTP settings:
```bash
SMTP_ENABLED=true
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=alerts@openvision.local
```

### Create Alert Rule in Node-RED

1. Open Node-RED: http://localhost:1880
2. Drag "mqtt in" node to canvas
3. Configure:
   - Server: mosquitto:1883
   - Topic: frigate/events
4. Add "switch" node to filter person detections
5. Add "email" node for notifications
6. Deploy flow

---

## View Dashboards

### Grafana Dashboards

1. Open Grafana: http://localhost:3000
2. Login: admin / (password from .env)
3. Navigate to Dashboards
4. View pre-configured dashboards:
   - System Overview
   - Camera Health
   - Analytics Performance
   - Storage Utilization

### Create Custom Dashboard

1. Click "+" → Dashboard
2. Add Panel
3. Select Data Source: Prometheus
4. Create queries for metrics:
   - `frigate_camera_fps`
   - `frigate_detection_fps`
   - `up{job="frigate"}`

---

## Test Integrations

### MQTT Integration

**Subscribe to events:**
```bash
# Install mosquitto client
sudo apt install mosquitto-clients

# Subscribe to all events
mosquitto_sub -h localhost -p 1883 -t "frigate/#" -v

# Subscribe to detections only
mosquitto_sub -h localhost -p 1883 -t "frigate/+/person" -v
```

**Publish test event:**
```bash
mosquitto_pub -h localhost -p 1883 -t "test/message" -m "Hello OpenVision"
```

### REST API

**List cameras:**
```bash
curl http://localhost:5000/api/config
```

**Get events:**
```bash
curl http://localhost:5000/api/events
```

**Capture snapshot:**
```bash
curl -X POST http://localhost:5000/api/front_door/snapshot
```

---

## Common Tasks

### Check Service Status

```bash
# View all containers
docker-compose ps

# Check specific service logs
docker-compose logs frigate
docker-compose logs postgres
docker-compose logs yolo-analytics

# Follow logs in real-time
docker-compose logs -f frigate
```

### Restart Services

```bash
# Restart single service
docker-compose restart frigate

# Restart all services
docker-compose restart

# Stop all services
docker-compose down

# Start all services
docker-compose up -d
```

### Access Container Shell

```bash
# Access Frigate container
docker-compose exec frigate bash

# Access PostgreSQL
docker-compose exec postgres psql -U openvision

# Access Redis
docker-compose exec redis redis-cli
```

### View Storage Usage

```bash
# Check volume sizes
docker system df -v

# Clean up unused volumes
docker volume prune
```

---

## Troubleshooting

### Camera Won't Connect

**Check RTSP URL:**
```bash
# Test with ffplay (if installed)
ffplay rtsp://username:password@camera-ip/stream1

# Test with ffmpeg
ffmpeg -i rtsp://username:password@camera-ip/stream1 -frames:v 1 test.jpg
```

**Check Frigate logs:**
```bash
docker-compose logs frigate | grep ERROR
```

**Common issues:**
- Wrong username/password
- Wrong RTSP path (check camera manual)
- Network/firewall blocking connection
- Camera only supports one connection at a time

### High CPU Usage

**Check resource usage:**
```bash
docker stats
```

**Optimize settings:**
```yaml
# In frigate.yml, reduce detection FPS
detect:
  fps: 5  # Lower = less CPU (was 20)

# Process fewer frames
motion:
  frame_height: 720  # Lower resolution
```

### Database Connection Error

**Check PostgreSQL status:**
```bash
docker-compose ps postgres
docker-compose logs postgres
```

**Restart database:**
```bash
docker-compose restart postgres
```

### Out of Storage Space

**Check disk usage:**
```bash
df -h

# Check Docker volumes
docker system df -v
```

**Clean up old recordings:**
```bash
# Frigate auto-deletes based on retention policy
# To manually clean up:
docker-compose exec frigate bash
cd /media/frigate/recordings
# Delete old folders
```

---

## Next Steps

### Explore Advanced Features

1. **Add More Cameras** - Scale to 10, 20, 100+ cameras
2. **Custom Analytics** - Develop custom ML modules
3. **IoT Integration** - Connect sensors, access control
4. **Digital Twin** - 3D visualization of camera coverage
5. **Mobile App** - iOS/Android remote access

### Learn More

- **Full Documentation:** https://docs.openvision.io
- **Architecture Guide:** See `technical/03-Technical-Architecture.md`
- **Deployment Guide:** See `deployment/04-Enterprise-Deployment.md`
- **Module Development:** See `development/07-Module-Development.md`

### Get Support

- **Community Forum:** https://community.openvision.io
- **Discord:** https://discord.gg/openvision
- **GitHub Issues:** https://github.com/openvision/platform/issues
- **Commercial Support:** support@openvision.io

---

## Clean Up (When Done Testing)

```bash
# Stop all services
docker-compose down

# Remove volumes (deletes all data)
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Complete cleanup
docker system prune -a --volumes
```

---

## Quick Reference

### Important URLs

| Service | URL |
|---------|-----|
| Frigate VMS | http://localhost:5000 |
| Grafana | http://localhost:3000 |
| Node-RED | http://localhost:1880 |
| MinIO Console | http://localhost:9001 |
| Prometheus | http://localhost:9090 |

### Important Directories

| Path | Purpose |
|------|---------|
| `configs/` | Configuration files |
| `data/` | Persistent data volumes |
| `logs/` | Application logs |
| `models/` | ML models |

### Important Commands

```bash
# Start platform
docker-compose up -d

# Stop platform
docker-compose down

# View logs
docker-compose logs -f

# Restart service
docker-compose restart frigate

# Check status
docker-compose ps

# Update images
docker-compose pull
docker-compose up -d
```

---

## You're Ready!

You now have:
✓ OpenVision Platform running locally  
✓ Test camera streaming and recording  
✓ AI analytics detecting objects  
✓ Monitoring dashboards operational  
✓ Integration framework ready  

**Time to explore!** Try adding more cameras, creating custom workflows in Node-RED, or developing your first custom analytics module.

---

**Questions?** Check the full documentation or reach out to the community!

**Want to deploy at scale?** See the Enterprise Deployment Guide.

**Ready to contribute?** Visit https://github.com/openvision/platform
