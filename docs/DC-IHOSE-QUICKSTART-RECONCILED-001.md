# DC-IHOSE-QUICKSTART-RECONCILED-001 — OpenVision Platform Quick Start & Installation, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `ihose-quickstart-install` (3 docs).

## Current understanding

Three tightly-related onboarding documents for the OpenVision Platform: QUICK-START.md is a top-level
"reference guide" summarizing the whole documentation package and business case; 00-Quick-Start-Guide.md
is the actual hands-on 30-minute Docker Compose walkthrough; install.sh is the automated version of the
same walkthrough as an executable script. All three are consistent on every shared technical detail
(URLs, ports, service names, deployment tiers).

**QUICK-START.md reference overview (incorporated):** summarizes an 8-document package (README,
PROJECT_SUMMARY, architecture overview, enterprise deployment guide, module development guide, Docker
Compose config, hardware BOM, env config, install script), each with file size and content summary
[§Documentation Overview]. Three deployment tiers with cost/time figures: Household (Pi 4 + Coral TPU,
~$300, 30 min), SMB (single server/cluster, $1,000-5,000, 2-4 hours), Enterprise (K8s cluster, $213K-
734K, 2-4 weeks) [§Deployment Options]. A cost comparison against commercial VMS (Genetec/Milestone):
OpenVision 3-year TCO $819,430 (standard enterprise tier: $294,430 hardware) vs. commercial $890,000+,
netting $70,570+ savings — the two figures are internally consistent (890,000 − 819,430 = 70,570)
[§Cost Comparison]. A learning path, deployment checklist, and success-metrics targets (99%+ uptime,
<2s analytics latency, 18-24 month ROI) close the document [§Learning Path through §Success Metrics].

**00-Quick-Start-Guide.md hands-on walkthrough (incorporated):** prerequisites (8GB RAM, 50GB disk,
Docker), Docker installation per-OS, then a 4-step deployment (get code → configure .env with generated
passwords → `docker-compose up -d` → access web interfaces at localhost:5000/3000/1880/9001)
[§Prerequisites, §Quick Deployment]. Camera configuration via Frigate YAML (test-stream option or real
RTSP camera), YOLO analytics configuration, Node-RED-based email alerting, Grafana dashboards, and MQTT/
REST API testing commands [§Configure Your First Camera through §Test Integrations]. A troubleshooting
section covering camera-connection failures, high CPU usage, database errors, and storage exhaustion
[§Troubleshooting].

**install.sh automation (incorporated):** a bash script automating the same walkthrough — checks for
Docker/docker-compose/git prerequisites, interactively selects deployment type (Household/SMB/
Enterprise, the same three tiers as QUICK-START.md), auto-generates strong passwords for Postgres/
Redis/MinIO/JWT/Keycloak/Grafana via `openssl rand`, creates required data directories, downloads the
YOLOv8n model, generates default Frigate/Mosquitto configs, pulls Docker images, starts services, checks
health, and displays access URLs/credentials at the end [main() function flow]. Enterprise selection
explicitly exits early with a pointer to the separate enterprise deployment guide rather than attempting
automated Kubernetes setup — consistent with QUICK-START.md's framing of Enterprise as a 2-4-week manual
deployment, not a quick-start path.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| 8-document package overview and deployment-tier table | QUICK-START.md §Documentation Overview, §Deployment Options | incorporated |
| Cost comparison vs. commercial VMS | QUICK-START.md §Cost Comparison | incorporated (internally consistent figures) |
| Learning path, deployment checklist, success metrics | QUICK-START.md §Learning Path through §Success Metrics | incorporated |
| Prerequisites and 4-step Docker Compose deployment | 00-Quick-Start-Guide §Prerequisites, §Quick Deployment | incorporated |
| Camera configuration, AI analytics, alerts, dashboards, API testing | 00-Quick-Start-Guide §Configure Your First Camera through §Test Integrations | incorporated |
| Troubleshooting guide | 00-Quick-Start-Guide §Troubleshooting | incorporated |
| Automated installation flow (prerequisite check → deployment-type selection → config generation → service start → health check) | install.sh, main() function | incorporated |
| Enterprise-tier early-exit behavior (points to separate guide, doesn't attempt automated K8s) | install.sh, select_deployment_type() | incorporated (consistent with QUICK-START.md's framing of Enterprise as non-quick-start) |

## Unresolved tensions

None identified in this pass — all three documents describe the same platform, tiers, and deployment
mechanics consistently, and the one arithmetic claim checkable across documents (the $70,570 3-year TCO
savings figure) is internally consistent with its own component numbers.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/meta/status-tracking/IHOSE/QUICK-START-md.md`
- `knowledge-base/d-central/security/IHOSE/00-Quick-Start-Guide-md.md`
- `knowledge-base/d-central/security/IHOSE/install-sh.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/meta/status-tracking/IHOSE/QUICK-START-md.md,
  knowledge-base/d-central/security/IHOSE/00-Quick-Start-Guide-md.md,
  knowledge-base/d-central/security/IHOSE/install-sh.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
