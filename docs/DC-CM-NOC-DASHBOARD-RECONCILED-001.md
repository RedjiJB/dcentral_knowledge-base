# DC-CM-NOC-DASHBOARD-RECONCILED-001 — CivicMesh NOC & Manager Dashboard Specifications, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `civicmesh-noc-manager-dashboard-specifications` (3 docs).

## Current understanding

Three tightly-related dashboard specs: DC-CM-APP-009 specifies the community-manager-facing dashboard;
DC-CM-APP-003 specifies the MSSP NOC-operator-facing console; DC-CM-NOC-001 is the unifying functional-
requirements document that explicitly covers both views as two credential-scoped filters over the same
underlying data model. All three are fully consistent on every shared numeric threshold.

**Community Manager Dashboard (incorporated):** built for non-technical HOA/condo/campus managers, with
all platform complexity hidden — the design goal is "nothing more complex than [node status, today's
activity, revenue, data-access log] on the main screen" [§Purpose]. Six primary sections: Community
Overview, Incident Queue (one-tap confirm/dismiss with DID-logged decisions), Member Management,
Law Enforcement Access Log (full detail, no redactions), one-click Transparency Report generation, and
Privacy Complaints tracking [§Primary Sections]. A mandatory Public Node Map (CCSC bylaws/municipal
transparency requirement, not optional) publishes node locations rounded to the nearest 10m at a
no-login public URL [§Public Node Map].

**MSSP NOC Console (incorporated):** built for professional NOC operators managing many communities
at once, targeting "everything on one screen, drill into any issue within 3 clicks" [§Purpose]. Five
primary dashboards with specific alert thresholds: Fleet Health (node offline >15min or tamper = P1),
Evidence Pipeline (lag >5min = P2, any chain-of-custody failure = immediate P1), Federation Requests
(>4hr in queue = P2), SLA Compliance (breach projected within 1hr = P1), and Credential Monitor (30 days
to expiry = P3) [§Primary Dashboards]. Four named external integrations: PagerDuty, Slack, Linear/JIRA,
Datadog/Grafana [§Integrations].

**Unifying NOC/Community Dashboard Specification (incorporated):** explicitly frames both dashboards as
credential-scoped views over one shared data model [§Executive Summary]. Restates the MSSP NOC view's
8 features with identical alert thresholds to DC-CM-APP-003 (15min offline, 5min pipeline lag, 4hr
federation queue, 30-day credential expiry) [§1] — an exact match, not an independent re-derivation.
Restates the Community Manager view's 7 features with matching access-control notes to DC-CM-APP-009
[§2]. Adds data-architecture detail not present in either individual spec: per-community isolated
PostgreSQL schemas with explicit cross-tenant permission checks at query level, Kafka→Server-Sent-Events
push-based (not polling) real-time updates, immutable append-only audit logging that NOC operators
cannot edit, and DID-attributed access logging auditable by the MSSP certification auditor [§3].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Community Manager Dashboard sections and design philosophy | DC-CM-APP-009 §Purpose, §Primary Sections | incorporated |
| Public Node Map requirement | DC-CM-APP-009 §Public Node Map | incorporated |
| MSSP NOC Console dashboards and alert thresholds | DC-CM-APP-003 §Purpose, §Primary Dashboards | incorporated (thresholds match DC-CM-NOC-001 exactly) |
| NOC Console external integrations | DC-CM-APP-003 §Integrations | incorporated |
| Unified data-model framing (both views, shared data, credential-scoped) | DC-CM-NOC-001 §Executive Summary | incorporated |
| MSSP NOC view functional requirements (restated, thresholds match) | DC-CM-NOC-001 §1 | incorporated |
| Community Manager view functional requirements (restated, matches) | DC-CM-NOC-001 §2 | incorporated |
| Data architecture (multi-tenant isolation, real-time push, immutable audit log) | DC-CM-NOC-001 §3 | incorporated (new detail not in either individual spec) |

## Unresolved tensions

None identified in this pass — every alert threshold and functional-requirement detail that appears in
more than one document matches exactly, consistent with DC-CM-NOC-001's role as the deliberate unifying
specification for the other two.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/core/governance/CivicMesh/DC-CM-APP-009-CivicMesh-Manager-Dashboard-v1-docx.md`
- `knowledge-base/d-central/core/observability/CivicMesh/DC-CM-APP-003-CivicMesh-NOC-Console-v1-docx.md`
- `knowledge-base/d-central/core/observability/CivicMesh/DC-CM-NOC-001-NOC-Dashboard-Specification-v1-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/core/governance/CivicMesh/DC-CM-APP-009-CivicMesh-Manager-Dashboard-v1-docx.md,
  knowledge-base/d-central/core/observability/CivicMesh/DC-CM-APP-003-CivicMesh-NOC-Console-v1-docx.md,
  knowledge-base/d-central/core/observability/CivicMesh/DC-CM-NOC-001-NOC-Dashboard-Specification-v1-docx.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
