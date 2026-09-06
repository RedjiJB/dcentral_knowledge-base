---
source_project: CivicMesh
source_project_uuid: 019e82f3-7ab2-715c-87c1-3e1074a12ab6
doc_uuid: ca1dacac-3b95-4552-8286-6dcb60680f06
original_filename: DC-CM-APP-003_CivicMesh_NOC_Console_v1.docx
created_at: 2026-06-01T11:32:22.325278+00:00
content_hash: 15bbba6195dc
topic: "civicmesh-noc-manager-dashboard-specifications"
consolidated_into: docs/DC-CM-NOC-DASHBOARD-RECONCILED-001.md
---

**D-Central Group  |  Confidential**	Section 2 — Legal & Corporate Structure

**DC-CM-APP-003**

**D-CENTRAL GROUP**

**CivicMesh Inc.**

CivicMesh NOC Console — Product Specification

| **Document ID** | DC-CM-APP-003 |
| --- | --- |
| **Version** | 1.0 |
| **Status** | Draft |
| **Date** | May 2026 |
| **Author** | Toussaint Redji Jean Baptiste |
| **Classification** | Confidential — Technical |
| **Primary Audience** | MSSP NOC operators |
| **Platform** | Web — desktop-first, responsive |
| **Related Documents** | DC-CM-APP-001 │ DC-CM-ARCH-001 |

# **1. Purpose**

Professional operations tool for MSSP NOC teams. Designed for high information density, operability under pressure, and integration with standard NOC tooling. A NOC operator managing 50 community deployments should be able to see everything they need on one screen and drill into any issue within 3 clicks.

# **2. Primary Dashboards**

| **Dashboard** | **Key Metrics** | **Alert Triggers** |
| --- | --- | --- |
| Fleet Health | Active/degraded/offline/tamper-flagged node counts by community. Geographic node map with colour-coded health. Last ping time, firmware version, uptime by node. | Node offline >15 min, tamper event (immediate P1) |
| Evidence Pipeline | Packages/hour, processing latency percentiles (p50/p95/p99), upload failure rate, storage utilisation, chain of custody integrity failures | Pipeline lag >5 min (P2), any COC failure (P1 immediate) |
| Federation Requests | Pending law enforcement requests with time-in-queue, legal authority type, data scope. MSSP legal review workflow. | Any request >4 hours in queue (P2) |
| SLA Compliance | Uptime % vs 99.9% target, P1/P2/P3 incident response times vs SLA, open ticket count by severity | SLA breach projected within 1 hour (P1) |
| Credential Monitor | All credentials in managed communities expiring within 90/60/30 days — technician, MSSP staff, node activation | 30 days to any credential expiry (P3) |

# **3. Integrations**

| **System** | **Integration Type** | **Purpose** |
| --- | --- | --- |
| PagerDuty | Outbound webhook | On-call alerting for P1/P2 incidents |
| Slack | Outbound webhook | Team notifications, daily digest |
| Linear / JIRA | REST API | Auto-create tickets from incidents with full context |
| Datadog / Grafana | Metrics ingestion | Infrastructure metrics alongside evidence pipeline metrics |

# **Document Control**

| **Ver** | **Date** | **Author** | **Description** |
| --- | --- | --- | --- |
| 1.0 | May 2026 | Toussaint Redji Jean Baptiste | Initial release |

| Classification Notice — This document is CONFIDENTIAL and intended for internal use, legal counsel, and authorized personnel only. Distribution requires written authorization from Toussaint Redji Jean Baptiste. |
| --- |

	Toussaint Redji Jean Baptiste  |  D-Central Ecosystem  |  May 2026	Page  of

<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Topics:**
- [[knowledge-base/_topics/civicmesh-noc-manager-dashboard-specifications|civicmesh-noc-manager-dashboard-specifications]]

**Consolidated into:**
- [[docs/DC-CM-NOC-DASHBOARD-RECONCILED-001]]

<!-- AUTO-GENERATED RELATED END -->
