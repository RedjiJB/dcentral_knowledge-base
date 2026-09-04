---
source_project: D Central v2
source_project_uuid: 0199df04-2107-76ac-8919-203857b7a6c9
doc_uuid: 9c0addb8-21cd-42ff-88f5-8f51e1323cca
original_filename: dcentral-operations-runbook.md
created_at: 2025-10-13T19:26:30.911989+00:00
content_hash: 5764258c7a39
---

# D-Central IoT Operations Runbook

**Document Version:** 1.0  
**Last Updated:** October 2025  
**Audience:** Site Operators, SREs, Network Engineers

---

## Table of Contents

1. [System Overview](#system-overview)
2. [Daily Operations](#daily-operations)
3. [Monitoring & Alerting](#monitoring--alerting)
4. [Common Issues & Troubleshooting](#common-issues--troubleshooting)
5. [Incident Response](#incident-response)
6. [Maintenance Procedures](#maintenance-procedures)
7. [Emergency Procedures](#emergency-procedures)
8. [Change Management](#change-management)
9. [Backup & Recovery](#backup--recovery)
10. [Security Operations](#security-operations)

---

## 1. System Overview

### Architecture Layers

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚          Digital Twin Registry & UI                 â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚          FCN Functions (WASM Runtime)               â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚          ICN / MQTT Messaging Layer                 â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚          Protocol Gateways                          â”‚
â”‚     (BACnet, Modbus, Zigbee, ONVIF, OCPP)          â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚          IoT Devices (350+ types)                   â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Key Components

| Component | Location | Purpose | HA Config |
|-----------|----------|---------|-----------|
| MQTT Broker | `mqtt.dcentral.local:8883` | Message routing | 3-node cluster |
| Twin Registry | `registry.dcentral.local` | Device metadata | PostgreSQL HA |
| FCN Orchestrator | `fcn.dcentral.local` | Function execution | K3s autoscaling |
| Protocol Gateways | Edge nodes | Legacy protocol bridge | Per-protocol HA |
| Monitoring Stack | `monitor.dcentral.local` | Observability | Prometheus + Grafana |
| Identity Service | `id.dcentral.local` | DID/VC management | Vault + HSM |

### Access Points

- **Admin Portal:** https://admin.dcentral.local
- **Grafana:** https://grafana.dcentral.local
- **Prometheus:** https://prometheus.dcentral.local:9090
- **MQTT Broker:** mqtts://mqtt.dcentral.local:8883
- **SSH Jump Host:** ssh://jump.dcentral.local:22

---

## 2. Daily Operations

### Morning Checklist (Start of Day)

```bash
#!/bin/bash
# daily-morning-check.sh

echo "D-Central Daily Health Check - $(date)"
echo "=========================================="

# 1. Check MQTT broker cluster
echo "1. MQTT Broker Status"
kubectl get pods -n mqtt-system
mosquitto_sub -h mqtt.dcentral.local -p 8883 -t '$SYS/broker/uptime' --cafile ca.crt --cert client.crt --key client.key

# 2. Check gateway connectivity
echo "2. Gateway Status"
for gw in bacnet-gw modbus-gw zigbee-gw onvif-gw ocpp-gw; do
    echo -n "  $gw: "
    systemctl is-active $gw
done

# 3. Check device counts
echo "3. Device Counts"
psql -h registry.dcentral.local -U admin -d twin_registry -c \
    "SELECT state, COUNT(*) FROM devices GROUP BY state;"

# 4. Check overnight alerts
echo "4. Overnight Alerts (Critical/Warning)"
curl -s http://prometheus.dcentral.local:9090/api/v1/alerts | \
    jq '.data.alerts[] | select(.state=="firing") | {name: .labels.alertname, severity: .labels.severity}'

# 5. Check backup status
echo "5. Last Backup Status"
ls -lh /var/backups/dcentral/ | tail -5

echo "=========================================="
echo "Daily check complete"
```

**Run:** `./daily-morning-check.sh | tee /var/log/dcentral/daily-check-$(date +%Y%m%d).log`

### Evening Checklist (End of Day)

- Review alert history for trends
- Check disk space on edge nodes: `df -h`
- Verify scheduled backups completed
- Review security audit logs for anomalies
- Check device enrollment queue: `SELECT COUNT(*) FROM enrollment_queue WHERE status='pending';`

---

## 3. Monitoring & Alerting

### Key Metrics & SLOs

| Service | SLO | Alert Threshold | Dashboard |
|---------|-----|-----------------|-----------|
| MQTT Broker | 99.9% uptime | <99.5% | mqtt-overview |
| Message Latency | p99 < 100ms | p99 > 200ms | mqtt-performance |
| Device Online | >95% | <90% | device-health |
| FCN Execution | p95 < 50ms | p95 > 100ms | fcn-performance |
| Gateway Uptime | 99.5% | <99% | gateway-overview |
| Disk Usage | <80% | >85% | infrastructure |

### Alert Severity Levels

**P0 - Critical (Page Immediately)**
- MQTT cluster down (all nodes)
- Security breach detected
- Fire/safety alarm cascade
- Data center power failure

**P1 - High (Page During Business Hours)**
- MQTT node failure (1 of 3)
- Gateway offline >10 minutes
- Certificate expiring in <7 days
- Disk usage >90%

**P2 - Medium (Email/Slack)**
- Device offline >1 hour
- Elevated error rates
- Certificate expiring in <30 days
- Firmware update failed

**P3 - Low (Dashboard Only)**
- Device offline <1 hour
- Minor config drift
- Info-level security events

### Accessing Metrics

```bash
# Query Prometheus
curl -G 'http://prometheus.dcentral.local:9090/api/v1/query' \
    --data-urlencode 'query=mqtt_broker_uptime'

# MQTT broker statistics
mosquitto_sub -h mqtt.dcentral.local -p 8883 \
    -t '$SYS/#' -v \
    --cafile ca.crt --cert client.crt --key client.key

# Check specific device
psql -h registry.dcentral.local -U admin -d twin_registry \
    -c "SELECT * FROM devices WHERE device_id='therm-2f-east';"

# View recent telemetry
influx -host tsdb.dcentral.local -database telemetry \
    -execute "SELECT * FROM env_temp WHERE time > now() - 1h"
```

### Grafana Dashboards

Essential dashboards to monitor:

1. **Executive Overview** - High-level health
2. **MQTT Performance** - Broker metrics, topic stats
3. **Device Health** - Online/offline, battery levels
4. **Gateway Status** - Protocol-specific metrics
5. **Energy Dashboard** - Power consumption, grid status
6. **Security Audit** - Failed auth, policy violations
7. **Capacity Planning** - Growth trends, forecasts

---

## 4. Common Issues & Troubleshooting

### Issue: Device Not Publishing Telemetry

**Symptoms:**
- No data in last 10+ minutes
- Device shows "online" but no telemetry

**Diagnosis:**
```bash
# 1. Check device status in registry
psql -h registry.dcentral.local -U admin -d twin_registry \
    -c "SELECT device_id, last_seen, state FROM devices WHERE device_id='DEVICE_ID';"

# 2. Check MQTT subscriptions
mosquitto_sub -h mqtt.dcentral.local -p 8883 \
    -t 'dcentral/DEVICE_ID/#' -v \
    --cafile ca.crt --cert client.crt --key client.key

# 3. Check gateway logs
journalctl -u bacnet-gw -f --since "10 minutes ago"

# 4. Verify network connectivity
ping DEVICE_IP
nmap -p 47808 DEVICE_IP  # BACnet port
```

**Resolution Steps:**
1. If gateway shows errors: restart gateway (`systemctl restart bacnet-gw`)
2. If device unreachable: check network (VLAN, switch port, IP)
3. If device reachable but not responding: power cycle device
4. If auth errors: check certificate expiry, regenerate if needed
5. Re-enroll device if persistent issues

**Prevention:**
- Enable heartbeat monitoring
- Set up dead-letter queue for failed messages
- Configure automatic retries with exponential backoff

---

### Issue: MQTT Broker High Latency

**Symptoms:**
- Message publish latency >500ms
- Growing queue depth
- Clients disconnecting

**Diagnosis:**
```bash
# Check broker resource usage
kubectl top pods -n mqtt-system

# Check queue depths
mosquitto_sub -h mqtt.dcentral.local -p 8883 \
    -t '$SYS/broker/messages/stored' -C 1

# Check client connections
mosquitto_sub -h mqtt.dcentral.local -p 8883 \
    -t '$SYS/broker/clients/connected' -C 1

# Check network I/O
iftop -i eth0
```

**Resolution Steps:**
1. Check for message storms (one device flooding)
2. Increase broker resources: `kubectl scale deployment mqtt-broker --replicas=5`
3. Enable QoS throttling on offending devices
4. Check for retained message buildup
5. Restart broker if necessary (rolling restart for HA)

**Prevention:**
- Configure rate limits per device
- Monitor topic cardinality
- Set message TTL and retention policies
- Use QoS 0 for non-critical telemetry

---

### Issue: Gateway Offline

**Symptoms:**
- All devices on protocol show offline
- Gateway not responding to ping
- No logs from gateway

**Diagnosis:**
```bash
# Check service status
ssh gateway.dcentral.local
systemctl status bacnet-gw

# Check gateway process
ps aux | grep bacnet-gw

# Check resource usage
htop

# Check network interfaces
ip addr show
ip route show
```

**Resolution Steps:**
1. Restart gateway service: `systemctl restart bacnet-gw`
2. If crashed: check logs for segfault/OOM: `journalctl -xe`
3. If network issue: restart network: `systemctl restart networking`
4. If persistent: reboot gateway host
5. If hardware issue: fail over to standby gateway

**Prevention:**
- Deploy HA gateway pairs
- Configure systemd auto-restart: `Restart=always`
- Set up resource limits: `MemoryLimit=2G`
- Enable watchdog timer

---

### Issue: Certificate Expired

**Symptoms:**
- Device auth failures
- TLS handshake errors
- "Certificate has expired" in logs

**Diagnosis:**
```bash
# Check certificate expiry
openssl x509 -in /etc/dcentral/certs/device-cert.pem -noout -dates

# List expiring soon
psql -h registry.dcentral.local -U admin -d twin_registry \
    -c "SELECT device_id, cert_expiry FROM devices WHERE cert_expiry < NOW() + INTERVAL '30 days';"
```

**Resolution Steps:**
1. Generate new certificate:
   ```bash
   ./scripts/renew-device-cert.sh DEVICE_ID
   ```
2. Deploy certificate to device:
   ```bash
   ./scripts/deploy-cert.sh DEVICE_ID
   ```
3. Update registry:
   ```bash
   psql -h registry.dcentral.local -U admin -d twin_registry \
       -c "UPDATE devices SET cert_expiry='NEW_EXPIRY', cert_fingerprint='NEW_FINGERPRINT' WHERE device_id='DEVICE_ID';"
   ```
4. Restart device or trigger cert reload

**Prevention:**
- Enable automatic cert rotation (180-day cycle)
- Set alerts for certs expiring <30 days
- Use short-lived certs (1 year max) for security

---

### Issue: Disk Space Critical

**Symptoms:**
- Alert: Disk usage >90%
- Service failures
- Database errors

**Diagnosis:**
```bash
# Check disk usage
df -h

# Find large files/directories
du -sh /* | sort -hr | head -10

# Check log sizes
du -sh /var/log/dcentral/*

# Check time-series database
du -sh /var/lib/influxdb/data/*
```

**Resolution Steps:**
1. **Immediate:** Clean old logs
   ```bash
   find /var/log/dcentral -name "*.log" -mtime +30 -delete
   journalctl --vacuum-time=7d
   ```

2. **Short-term:** Compress old data
   ```bash
   influx -execute "DELETE FROM env_temp WHERE time < now() - 90d"
   ```

3. **Long-term:** 
   - Adjust retention policies
   - Add storage capacity
   - Archive to cold storage

**Prevention:**
- Configure log rotation: `/etc/logrotate.d/dcentral`
- Set time-series retention: `hot=7d, warm=30d, cold=1y`
- Enable automated archival to S3/MinIO
- Monitor growth trends: set alerts at 80%

---

## 5. Incident Response

### Incident Response Process

```
1. DETECT
   â†“
2. ASSESS (Severity: P0/P1/P2/P3)
   â†“
3. NOTIFY (Page/Email/Slack)
   â†“
4. INVESTIGATE (Root cause)
   â†“
5. MITIGATE (Stop bleeding)
   â†“
6. RESOLVE (Fix root cause)
   â†“
7. DOCUMENT (Post-mortem)
```

### P0 - Critical Incident Response

**Trigger:** MQTT cluster down, security breach, safety critical failure

**Response Team:**
- On-Call Engineer (Primary)
- SRE Manager (Escalation)
- Security Officer (if security incident)
- Facility Manager (if safety incident)

**Response Steps:**

1. **Acknowledge** (Within 5 minutes)
   - Acknowledge alert in PagerDuty
   - Open incident channel: `#incident-YYYYMMDD-NNN`
   - Post status: "Incident declared, investigating"

2. **Assess Impact** (Within 10 minutes)
   - How many devices affected?
   - Any safety/security implications?
   - Customer impact?

3. **Communicate** (Within 15 minutes)
   - Post to status page
   - Notify stakeholders
   - Update every 30 minutes minimum

4. **Mitigate**
   - Fail over to backup systems
   - Engage emergency procedures if needed
   - Document all actions

5. **Resolve**
   - Fix root cause
   - Verify all systems restored
   - Monitor for 1 hour post-resolution

6. **Post-Mortem** (Within 48 hours)
   - Write incident report
   - Identify action items
   - Update runbooks

### Security Incident Response

**If Security Breach Suspected:**

1. **Isolate:** Disconnect affected systems from network
2. **Preserve:** Capture logs, memory dumps before shutdown
3. **Notify:** Security team + legal + management
4. **Investigate:** Forensic analysis
5. **Remediate:** Patch, rotate credentials, rebuild
6. **Report:** Document findings, file reports as required

**Common Security Events:**

| Event | Action |
|-------|--------|
| Failed auth spike | Check for brute force, enable rate limiting |
| Unauthorized device | Quarantine device, revoke certificate |
| Policy violation | Review logs, identify user/device, disable access |
| Malware detected | Isolate device, scan network, update signatures |
| Certificate compromise | Revoke cert, blacklist, rotate all certs |

---

## 6. Maintenance Procedures

### Scheduled Maintenance Windows

**Weekly:**
- Sunday 02:00-04:00 UTC - Firmware updates (rolling)
- Sunday 04:00-05:00 UTC - Certificate rotations

**Monthly:**
- First Sunday 00:00-06:00 UTC - Full system maintenance

**Quarterly:**
- Platform upgrades (K3s, PostgreSQL, etc.)

### Device Firmware Updates

```bash
#!/bin/bash
# firmware-update.sh - Rolling firmware update

DEVICE_TYPE="hvac.smart-thermostat"
FIRMWARE_VERSION="4.8.8"
CANARY_GROUP_SIZE=5
RING_DELAY_MINUTES=60

echo "Starting firmware rollout: $DEVICE_TYPE â†’ $FIRMWARE_VERSION"

# Stage 1: Canary deployment
echo "Stage 1: Canary ($CANARY_GROUP_SIZE devices)"
CANARY_DEVICES=$(psql -t -h registry.dcentral.local -U admin -d twin_registry \
    -c "SELECT device_id FROM devices WHERE type='$DEVICE_TYPE' ORDER BY RANDOM() LIMIT $CANARY_GROUP_SIZE;")

for device in $CANARY_DEVICES; do
    echo "Updating $device..."
    mosquitto_pub -h mqtt.dcentral.local -p 8883 \
        -t "dcentral/$device/config" \
        -m "{\"firmware_update\": {\"version\": \"$FIRMWARE_VERSION\", \"url\": \"https://firmware.dcentral.local/$FIRMWARE_VERSION.bin\"}}"
    
    # Wait for update confirmation
    sleep 60
done

# Monitor canary group for 1 hour
echo "Monitoring canary group for $RING_DELAY_MINUTES minutes..."
sleep $(($RING_DELAY_MINUTES * 60))

# Check canary health
CANARY_HEALTHY=$(psql -t -h registry.dcentral.local -U admin -d twin_registry \
    -c "SELECT COUNT(*) FROM devices WHERE device_id IN ('$CANARY_DEVICES') AND firmware_version='$FIRMWARE_VERSION' AND state='active';")

if [ "$CANARY_HEALTHY" -lt "$CANARY_GROUP_SIZE" ]; then
    echo "ABORT: Canary failures detected"
    exit 1
fi

# Stage 2: Ring 1 (10%)
echo "Stage 2: Ring 1 (10% of devices)"
# ... similar logic for 10% of devices

# Stage 3: Ring 2 (50%)
echo "Stage 3: Ring 2 (50% of devices)"
# ...

# Stage 4: Remaining devices
echo "Stage 4: All remaining devices"
# ...

echo "Firmware rollout complete"
```

### Gateway Maintenance

**Before Maintenance:**
```bash
# 1. Notify monitoring
curl -X POST http://prometheus.dcentral.local:9093/api/v1/silences \
    -d '{"matchers":[{"name":"instance","value":"bacnet-gw"}], "startsAt":"...","endsAt":"..."}'

# 2. Drain connections
systemctl stop bacnet-gw

# 3. Verify devices migrated to backup gateway
mosquitto_sub -h mqtt.dcentral.local -p 8883 -t 'dcentral/+/state' -C 10
```

**During Maintenance:**
```bash
# Update gateway software
apt update && apt upgrade -y
pip3 install --upgrade dcentral-gateway

# Update configuration
vi /etc/dcentral/bacnet-gw.conf

# Test configuration
dcentral-gw --config /etc/dcentral/bacnet-gw.conf --test
```

**After Maintenance:**
```bash
# Restart gateway
systemctl start bacnet-gw

# Verify health
systemctl status bacnet-gw
journalctl -u bacnet-gw --since "1 minute ago"

# Clear monitoring silence
curl -X DELETE http://prometheus.dcentral.local:9093/api/v1/silence/SILENCE_ID
```

### Database Maintenance

**Weekly Vacuum:**
```sql
-- Run during low-traffic window
VACUUM ANALYZE devices;
VACUUM ANALYZE telemetry_events;
```

**Monthly Reindexing:**
```sql
REINDEX DATABASE twin_registry;
```

**Backup Verification:**
```bash
# Restore last night's backup to test instance
pg_restore -h test-db.dcentral.local -U admin -d twin_registry_test \
    /var/backups/dcentral/twin_registry-20241013.dump

# Verify row counts match
psql -h test-db.dcentral.local -U admin -d twin_registry_test \
    -c "SELECT COUNT(*) FROM devices;"
```

---

## 7. Emergency Procedures

### Fire Alarm Cascade

**Automatic Actions (via FCN /fn/safety/fire-cascade):**
1. Sound alarm bells
2. Activate emergency lighting
3. Unlock all access-controlled doors
4. Shut down HVAC (prevent smoke spread)
5. Recall elevators to ground floor
6. Send alert to monitoring company
7. Notify building management

**Manual Actions:**
1. Verify alarm is not false positive
2. Call fire department if confirmed
3. Initiate evacuation if necessary
4. Disable HVAC system if not auto-disabled
5. Meet fire department at designated location
6. Provide building access and floor plans

**Post-Incident:**
1. Reset fire alarm system
2. Verify all sensors operational
3. Review logs for root cause
4. Test emergency systems
5. Document incident

### Power Failure

**Automatic Actions:**
1. UPS kicks in (critical systems: 30-60 min runtime)
2. Non-critical loads shed automatically
3. Battery backup for safety systems
4. Generate emergency power status report

**Manual Actions (if UPS runtime exceeded):**
1. Start backup generator (if available)
2. Gracefully shut down non-critical systems
3. Maintain monitoring and safety systems only
4. Notify facilities management
5. Monitor UPS status

**Power Restoration:**
1. Verify clean power (no surges)
2. Restart systems in order:
   - Network infrastructure
   - MQTT broker cluster
   - Protocol gateways
   - Monitoring systems
   - IoT devices (auto-reconnect)
3. Verify all services operational
4. Check for any devices that didn't auto-recover

### Network Partition

**Symptoms:**
- Devices in one zone unable to reach MQTT broker
- Gateway shows offline but responds to local ping
- Monitoring shows "split brain"

**Response:**
1. Identify partition boundary (which switch/router?)
2. Check for redundant paths (mesh backup)
3. Enable offline resilience mode (devices cache locally)
4. Route critical traffic via alternate path
5. Engage network team to resolve

**Offline Resilience Features:**
- Devices cache telemetry locally (7 days)
- Control continues with last-known-good config
- Sync resumes automatically on reconnection

### Data Center Cooling Failure

**Automatic Actions (via /fn/datacenter/temp-alert):**
1. Alert raised when temp >28Â°C
2. Increase CRAC/CRAH airflow
3. Shed non-critical compute workloads
4. Enable hot-aisle containment bypass

**Manual Actions:**
1. Check CRAC units (filters, refrigerant)
2. Open data center doors if emergency
3. Deploy portable AC units
4. Consider emergency shutdown if temp >40Â°C
5. Notify data center management

---

## 8. Change Management

### Change Request Process

**Required Information:**
- **Change ID:** CHG-YYYYMMDD-NNN
- **Type:** Standard/Emergency/Normal
- **Risk:** Low/Medium/High
- **Systems Affected:** List all
- **Downtime Required:** Yes/No (duration)
- **Rollback Plan:** Detailed steps
- **Approvers:** Required sign-offs

**Change Types:**

| Type | Approval | Notice | Examples |
|------|----------|--------|----------|
| Standard | Pre-approved | None | Firmware updates, cert rotation |
| Normal | CAB meeting | 48 hours | Gateway upgrades, config changes |
| Emergency | Post-approval | ASAP | Security patches, outage fixes |

### Change Workflow

```
1. Request â†’ 2. Review â†’ 3. Approve â†’ 4. Schedule â†’ 5. Implement â†’ 6. Verify â†’ 7. Close
```

### GitOps Configuration Changes

All configuration managed via Git:

```bash
# Clone config repo
git clone https://gitlab.dcentral.local/ops/dcentral-config.git
cd dcentral-config

# Create feature branch
git checkout -b update-hvac-setpoints

# Make changes
vi configs/hvac/setpoints.yaml

# Commit
git add configs/hvac/setpoints.yaml
git commit -m "Adjust HVAC setpoints for winter"

# Push and create merge request
git push origin update-hvac-setpoints
# Open MR in GitLab, request review

# After approval, merge triggers ArgoCD/FluxCD deployment
```

**Automated Deployment:**
- Changes to `main` branch auto-deploy to production
- Rollback: `git revert COMMIT_SHA && git push`
- All changes are audited and reversible

---

## 9. Backup & Recovery

### Backup Schedule

| Component | Frequency | Retention | Location |
|-----------|-----------|-----------|----------|
| PostgreSQL (Twin Registry) | Hourly (incremental) | 30 days | S3 + tape |
| PostgreSQL (Full) | Daily | 90 days | S3 + tape |
| InfluxDB (Time-series) | Daily | 30 days | S3 |
| MQTT Retained Messages | Daily | 7 days | Local NAS |
| Configuration Files | On change (GitOps) | Forever | Git |
| Certificate Private Keys | On generation | Forever | Vault + HSM |
| System Images | Weekly | 30 days | S3 |

### Backup Procedures

**PostgreSQL Backup:**
```bash
#!/bin/bash
# /opt/dcentral/backups/backup-postgres.sh

DATE=$(date +%Y%m%d-%H%M)
BACKUP_DIR="/var/backups/dcentral"
S3_BUCKET="s3://dcentral-backups/postgres"

# Full backup
pg_dump -h registry.dcentral.local -U admin -Fc twin_registry > \
    $BACKUP_DIR/twin_registry-$DATE.dump

# Compress
gzip $BACKUP_DIR/twin_registry-$DATE.dump

# Upload to S3
aws s3 cp $BACKUP_DIR/twin_registry-$DATE.dump.gz $S3_BUCKET/

# Verify
aws s3 ls $S3_BUCKET/ | grep $DATE

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -name "twin_registry-*.dump.gz" -mtime +30 -delete

echo "Backup complete: twin_registry-$DATE.dump.gz"
```

**InfluxDB Backup:**
```bash
influxd backup -portable -database telemetry /var/backups/dcentral/influx-$(date +%Y%m%d)
```

### Recovery Procedures

**PostgreSQL Recovery:**
```bash
# Restore from backup
pg_restore -h registry.dcentral.local -U admin -d twin_registry -c \
    /var/backups/dcentral/twin_registry-20241013-0200.dump

# Verify
psql -h registry.dcentral.local -U admin -d twin_registry \
    -c "SELECT COUNT(*) FROM devices;"
```

**Point-in-Time Recovery:**
```bash
# Restore base backup
pg_restore ...

# Apply WAL logs up to specific time
# (PostgreSQL WAL archiving must be enabled)
```

**Disaster Recovery:**

If entire site lost:

1. **Activate DR site** (alternate data center)
2. **Restore latest backups** to DR site
3. **Update DNS** to point to DR site
4. **Verify systems operational**
5. **Re-enroll devices** (if certificates lost)
6. **Notify users** of DR activation

**RTO (Recovery Time Objective):** 4 hours  
**RPO (Recovery Point Objective):** 1 hour (last incremental backup)

---

## 10. Security Operations

### Security Monitoring

**Daily Security Checks:**
```bash
# Failed authentication attempts
psql -h registry.dcentral.local -U admin -d audit_log \
    -c "SELECT COUNT(*), device_id FROM auth_failures WHERE timestamp > NOW() - INTERVAL '24 hours' GROUP BY device_id ORDER BY COUNT(*) DESC LIMIT 10;"

# Certificate validation failures
grep "certificate verification failed" /var/log/dcentral/*.log

# OPA policy denials
curl http://opa.dcentral.local:8181/v1/data/dcentral/violations

# Unusual network traffic
tcpdump -i any -c 1000 -w /tmp/capture.pcap port 8883
```

**Weekly Security Tasks:**
- Review audit logs for anomalies
- Check for CVEs affecting deployed software
- Verify backup encryption
- Test security alert escalation
- Review OPA policy effectiveness

### Security Incident Handling

**If Compromised Device Detected:**

1. **Quarantine Device**
   ```bash
   # Disable in OPA
   curl -X PUT http://opa.dcentral.local:8181/v1/data/dcentral/blacklist/DEVICE_ID \
       -d '{"blacklisted": true, "reason": "Compromised", "timestamp": "..."}'
   
   # Block network
   iptables -A INPUT -s DEVICE_IP -j DROP
   iptables -A OUTPUT -d DEVICE_IP -j DROP
   ```

2. **Revoke Credentials**
   ```bash
   # Revoke certificate
   ./scripts/revoke-cert.sh DEVICE_ID
   
   # Update CRL
   ./scripts/publish-crl.sh
   ```

3. **Investigate**
   - Review device logs
   - Check what data was accessed
   - Identify attack vector

4. **Remediate**
   - Reimage device if possible
   - Apply security patches
   - Update firewall rules
   - Rotate credentials

5. **Re-enroll** (if device can be trusted again)
   ```bash
   ./scripts/enroll-device.sh DEVICE_ID
   ```

### Credential Rotation

**Certificate Rotation (Automated):**
```bash
# Rotate certificates expiring in <30 days
./scripts/auto-cert-rotation.sh

# Verify rotation
psql -h registry.dcentral.local -U admin -d twin_registry \
    -c "SELECT device_id, cert_expiry FROM devices WHERE cert_expiry < NOW() + INTERVAL '30 days';"
```

**MQTT Credentials Rotation:**
```bash
# Rotate broker admin password
mosquitto_passwd -c /etc/mosquitto/passwd admin
systemctl restart mosquitto

# Update in secrets manager
vault kv put secret/mqtt/admin password="NEW_PASSWORD"
```

---

## Appendix A: Contact Information

| Role | Name | Phone | Email | Pager |
|------|------|-------|-------|-------|
| On-Call Engineer | Rotation | +1-XXX-XXX-XXXX | oncall@dcentral.local | PagerDuty |
| SRE Manager | Alice Smith | +1-XXX-XXX-XXXX | alice@dcentral.local | - |
| Security Officer | Bob Johnson | +1-XXX-XXX-XXXX | bob@dcentral.local | PagerDuty |
| Network Engineer | Carol Williams | +1-XXX-XXX-XXXX | carol@dcentral.local | - |
| Facility Manager | Dave Brown | +1-XXX-XXX-XXXX | dave@dcentral.local | SMS |

---

## Appendix B: Useful Commands

```bash
# Quick device status
device-status() {
    psql -h registry.dcentral.local -U admin -d twin_registry \
        -c "SELECT device_id, state, last_seen FROM devices WHERE device_id='$1';"
}

# Tail device telemetry
device-tail() {
    mosquitto_sub -h mqtt.dcentral.local -p 8883 \
        -t "dcentral/$1/#" -v \
        --cafile /etc/dcentral/ca.crt \
        --cert /etc/dcentral/client.crt \
        --key /etc/dcentral/client.key
}

# Send device command
device-cmd() {
    local device_id=$1
    local command=$2
    mosquitto_pub -h mqtt.dcentral.local -p 8883 \
        -t "dcentral/$device_id/ctrl" \
        -m "$command" \
        --cafile /etc/dcentral/ca.crt \
        --cert /etc/dcentral/client.crt \
        --key /etc/dcentral/client.key
}

# Check gateway health
gateway-health() {
    for gw in bacnet modbus zigbee onvif ocpp; do
        echo -n "$gw-gw: "
        systemctl is-active ${gw}-gw
    done
}
```

---

## Appendix C: Escalation Matrix

| Issue Type | L1 Support | L2 Support | L3 Support | Vendor |
|------------|------------|------------|------------|--------|
| Device offline | Ops Team | Network Team | - | - |
| Gateway failure | Ops Team | SRE Team | - | - |
| MQTT cluster issue | SRE Team | Platform Team | Vendor | EMQX |
| Network partition | Network Team | Network Architect | - | ISP |
| Security incident | Security Team | CISO | Legal | - |
| Database issue | DBA | SRE Team | Vendor | PostgreSQL |

---

**Document End**

*For questions or updates to this runbook, contact: ops@dcentral.local*
