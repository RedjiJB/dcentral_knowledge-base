# DC-SECURITY-ECOSYSTEM-SECTOR-PLATFORMS-RECONCILED-001 — Security Ecosystem Sector Platforms, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `security-ecosystem-sector-platforms` (8 docs).

## Current understanding

Four of this topic's eight member documents — the Comprehensive OS-CONCIERGE, OS-GUARDIAN, OS-PATROL, and
OS-SENTINEL Sectors documents — are the same source files already fully consolidated in
[DC-OPENSECURE-SECTOR-USE-CASE-RECONCILED-001](DC-OPENSECURE-SECTOR-USE-CASE-RECONCILED-001.md) under
topic `opensecure-sector-use-case-analyses` (which also included the OS-DRONE sectors document, not a
member of this topic). Per the sibling-consolidation pattern, their per-sector content, ROI ranges, and
quick-switch module framework are not re-detailed here — see that document. This document covers the
four new members: a monetization playbook for the OS-PACS access-control platform, a consumer/network/
cloud business model for the "Iron Horse Security" brand, an adjacent productivity-suite offering from
the same brand, and a worked museum client use case.

**OS-PACS v2 (incorporated):** a business-model guide for security integrator firms monetizing the
open-source OS-PACS access-control platform, structured around three revenue pillars — one-time
installation/modernization projects, recurring managed services, and sector-specific vertical
applications — enabled by OS-PACS's elimination of per-door licensing fees and vendor lock-in
[Introduction]. Part 1 details five project types (new installation, controller "panel replacement"
takeovers, reader swaps, legacy system takeovers, and expansion projects), each with a worked revenue
model contrasting one-time project margin against a "project → recurring ladder." Part 2 details managed-
services offerings — tiered (Basic/Professional/Enterprise) managed-service packages, credential-
operations-as-a-service, RBAC/policy design sold as three recurring revenue streams, "Compliance as a
Service" audit/exception-reporting packages, mobile-credential/MFA premium upsells, monthly health-check
and backup services, and an SLA-backed "Access Control NOC" remote-administration tier — each with a
financial comparison table contrasting traditional installation-only economics against the OS-PACS
recurring model (a worked 100-door hotel property example shows the flip from front-loaded installation
margin to compounding "operational annuity" revenue). Part 3 covers integration upsells (video
verification, extended visitor/contractor/vendor access-ecosystem management, multi-site "security
drift" governance, and managed credential operations as a distinct MSS line), each with its own worked
real-world facility example (a 200-door manufacturing facility, a 15-location retail chain). Part 4
covers steady-state hardware/credential lifecycle management as predictable recurring revenue, and Part
5 is a sector-by-sector applications survey.

**Iron Horse Security - Distributed Ecosystem Architecture (incorporated):** a three-layer business
architecture for the "Iron Horse Security" consumer brand — a Hardware Layer of retail-ready, open-
source, standalone security products (vision systems, access control, sensors/detectors, vehicle/fleet,
smart-home hub, professional/commercial tiers, and bundles), an optional Network Layer enabling
community monitoring and a peer-to-peer service marketplace ("Uber for Security Services"), and a Cloud
Layer distributed-compute/storage marketplace using spare device capacity ("Airbnb meets AWS") [Executive
Summary, Parts 1-4]. Four consent-based government/public-sector integration types (law enforcement
access, community programs, municipal infrastructure, cross-agency data sharing, research/analysis)
explicitly built on an opt-in, privacy-first principle [Part 5]. A revenue-streams summary projecting
$24M-$85M total Year-3 revenue, unit economics, financial projections, and a funding strategy [Part 6],
followed by a 4-phase (Pre-Launch through Scale, Years 4-5) implementation roadmap and a risk-mitigation
section [Parts 7-8].

**Iron Horse Workspace Suite (incorporated):** an open-source Microsoft 365/Google Workspace alternative
offered as an adjacent revenue line to the same Iron Horse Security brand, explicitly framed in its own
"Strategic Value" section as combining with the security product line into "total digital infrastructure"
[Executive Summary]. A nine-component productivity suite (identity/access management as an Active
Directory replacement, office productivity apps, email/calendar, cloud storage, team collaboration,
project/task management, document management, intranet/knowledge management, and business intelligence)
[Part 1], and an explicit "Integration with Iron Horse Security Ecosystem" section detailing single-sign-
on via Keycloak/OAuth2/SAML/LDAP across both product lines and four worked cross-system automation
examples (incident response linking a camera alert to a project-management task and client notification;
badge-swipe-driven presence/payroll integration; visitor-management workflow spanning pre-registration
through access-log compliance; and ALPR-triggered parking-violation billing) [Part 2]. Deployment models
and pricing, a government/enterprise value proposition emphasizing Canadian data sovereignty and
auditability versus Microsoft 365, a technical-architecture and hardware-requirements section, and a
revenue-model/financial-projections/go-to-market section [Parts 3-6].

**Iron Horse Security - Client Use Case: Canada Agriculture and Food Museum (incorporated):** a fully
worked, single-client deployment case study applying the Iron Horse Security platform (referred to here
as "Intelligent Security & Building Operations Platform") to a real Ottawa museum (15,000 sq ft indoor,
~50 acres outdoor, 100+ live animals, 250 parking spaces, 150,000+ annual visitors) [Executive Summary,
Client Profile]. Twelve sections covering site/network infrastructure assessment, camera deployment and
AI video analytics, an animal-welfare-specific monitoring suite (individual animal tracking, barn
environmental monitoring, health/activity monitoring, feed management, veterinary-care integration,
birth/breeding management) not present in any of this topic's other documents, visitor analytics and
experience management, event/vendor coordination, automated parking integrated with the City of Ottawa's
own parking system, an inter-museum collaboration network (including a "collaborative blacklist" for
banned individuals shared reciprocally between museums), IoT/building-automation integration (HVAC,
lighting, access control), employee-management/scheduling systems, a cloud-services/analytics/ML
platform, and closing implementation-timeline/budget and ROI-analysis sections.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| 10 OS-CONCIERGE sectors, case studies, module framework | Comprehensive OS-CONCIERGE Sectors | referenced — fully detailed in [DC-OPENSECURE-SECTOR-USE-CASE-RECONCILED-001](DC-OPENSECURE-SECTOR-USE-CASE-RECONCILED-001.md) |
| 10 OS-GUARDIAN sectors, case studies, module framework | Comprehensive OS-GUARDIAN Sectors | referenced — fully detailed in the sibling document above |
| 20 OS-PATROL sectors, case studies, module framework | Comprehensive OS-PATROL Sectors | referenced — fully detailed in the sibling document above |
| 10 OS-SENTINEL sectors, case studies, module framework | Comprehensive OS-SENTINEL Sectors | referenced — fully detailed in the sibling document above |
| OS-PACS installation/modernization project revenue models | OS-PACS v2, Part 1 | incorporated |
| OS-PACS managed-services tiers, RBAC/CaaS/NOC recurring-revenue offerings | OS-PACS v2, Part 2 | incorporated |
| OS-PACS integration upsells and hardware/credential steady-state revenue | OS-PACS v2, Parts 3-5 | incorporated |
| Iron Horse three-layer hardware/network/cloud architecture, consumer product lineup | Iron Horse Distributed Ecosystem, Executive Summary, Parts 1-4 | incorporated |
| Government integration, revenue projections, implementation roadmap, risk mitigation | Iron Horse Distributed Ecosystem, Parts 5-8 | incorporated |
| Iron Horse Workspace Suite productivity-component catalogue | Iron Horse Workspace Suite, Part 1 | incorporated |
| SSO/data/workflow integration with the Iron Horse Security ecosystem | Iron Horse Workspace Suite, Part 2 | incorporated |
| Workspace Suite deployment models, government value proposition, financial projections | Iron Horse Workspace Suite, Parts 3-6 | incorporated |
| Museum site/network/camera/AI-analytics deployment | Museum Agriculture Use Case, §1-2 | incorporated |
| Animal-welfare monitoring, visitor analytics, event/vendor coordination, parking | Museum Agriculture Use Case, §3-6 | incorporated |
| Inter-museum collaboration network, IoT/building automation, employee management, cloud analytics, budget/ROI | Museum Agriculture Use Case, §7-12 | incorporated |

## Unresolved tensions

None identified. The four new documents operate at clearly distinct, non-overlapping layers of the same
brand ecosystem — a monetization playbook for one product (OS-PACS), a broader consumer/network/cloud
business architecture for the umbrella brand, an adjacent productivity-suite product line explicitly
cross-referencing that same brand's security ecosystem, and one concrete client deployment applying it —
and no numeric or architectural claim in any one of them contradicts another. Note for a mis-scoped-topic
check performed during this pass: the Iron Horse Workspace Suite document (a Microsoft-365 alternative
with no inherent connection to physical security) was flagged as a likely lexical mis-merge in an earlier
Stage 6 pass on a different topic (`ihose-federation-ecosystem-partnership-framework`, corrected during
consolidation of [DC-IHOSE-FEDERATION-ECOSYSTEM-RECONCILED-001](DC-IHOSE-FEDERATION-ECOSYSTEM-RECONCILED-001.md)).
Its inclusion here, in a differently-scoped topic, was independently verified as legitimate: the document
itself contains an explicit "PART 2: Integration with Iron Horse Security Ecosystem" section and its own
"Strategic Value" framing as a deliberate revenue-line extension of the same Iron Horse Security brand
that also authored the Distributed Ecosystem Architecture document in this topic — unlike the narrower
federation-partnership topic it was wrongly attached to previously, this broader "sector platforms" topic
is a legitimate home for it.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/business-legal/Open-Secure/OS-PACS-v2-md.md`
- `knowledge-base/d-central/meta/platform-scaffolding/Security-Ecosystem/iron-horse-distributed-ecosystem-md.md`
- `knowledge-base/d-central/meta/platform-scaffolding/Security-Ecosystem/iron-horse-workspace-suite-md.md`
- `knowledge-base/d-central/security/Open-Secure/Comprehensive-OS-CONCIERGE-Sectors-md.md`
- `knowledge-base/d-central/security/Open-Secure/Comprehensive-OS-GUARDIAN-Sectors-md.md`
- `knowledge-base/d-central/security/Open-Secure/Comprehensive-OS-PATROL-Sectors-md.md`
- `knowledge-base/d-central/security/Open-Secure/Comprehensive-OS-SENTINEL-Sectors-md.md`
- `knowledge-base/d-central/security/Security-Ecosystem/museum-agriculture-use-case-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/business-legal/Open-Secure/OS-PACS-v2-md.md,
  knowledge-base/d-central/meta/platform-scaffolding/Security-Ecosystem/iron-horse-distributed-ecosystem-md.md,
  knowledge-base/d-central/meta/platform-scaffolding/Security-Ecosystem/iron-horse-workspace-suite-md.md,
  knowledge-base/d-central/security/Open-Secure/Comprehensive-OS-CONCIERGE-Sectors-md.md,
  knowledge-base/d-central/security/Open-Secure/Comprehensive-OS-GUARDIAN-Sectors-md.md,
  knowledge-base/d-central/security/Open-Secure/Comprehensive-OS-PATROL-Sectors-md.md,
  knowledge-base/d-central/security/Open-Secure/Comprehensive-OS-SENTINEL-Sectors-md.md,
  knowledge-base/d-central/security/Security-Ecosystem/museum-agriculture-use-case-md.md,
]
reconciled_against: [
  docs/DC-OPENSECURE-SECTOR-USE-CASE-RECONCILED-001.md,
]
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

**References:**
- [[DC-IHOSE-FEDERATION-ECOSYSTEM-RECONCILED-001|DC-IHOSE-FEDERATION-ECOSYSTEM-RECONCILED-001 — Iron Horse Security (IHOSE) Federation & Ecosystem Partnership Framework, Consolidated (v1, generated 2026-09-05)]]
- [[DC-OPENSECURE-SECTOR-USE-CASE-RECONCILED-001|DC-OPENSECURE-SECTOR-USE-CASE-RECONCILED-001 — OpenSecure Sector Use-Case Analyses, Consolidated (v1, generated 2026-09-05)]]

<!-- AUTO-GENERATED RELATED END -->
