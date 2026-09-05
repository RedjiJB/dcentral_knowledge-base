# DC-IHOSE-OPENVISION-DOCUMENTATION-PACKAGE-RECONCILED-001 — IHOSE OpenVision Documentation Package, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `ihose-openvision-documentation-package` (20 docs). **This is the final topic of the Stage 6 Consolidator pass — 80/80 topics complete upon this document's registration.**

## Current understanding

Six of this topic's twenty member documents — `01-OpenVision-Architecture-docx.md`, `03-Technical-
Architecture-md.md`, `DEPLOYMENT-GUIDE-md.md`, `TECHNICAL-ARCHITECTURE-md.md`, `enterprise-md.md`, and
`overview-md.md` — are the exact same source files already fully consolidated in
[DC-IHOSE-ARCHITECTURE-DEPLOYMENT-RECONCILED-001](DC-IHOSE-ARCHITECTURE-DEPLOYMENT-RECONCILED-001.md)
under topic `ihose-architecture-deployment`. Per the sibling-consolidation pattern, their content is
referenced rather than re-detailed here — see that document, including its finding of an API-gateway/
event-bus tooling divergence and its four-way duplication observation among the OpenVision architecture
documents. This document details the fourteen new members, which extend that same duplication pattern
substantially further: this topic's documents include a **second, independent Executive Summary
duplicate pair** and a **second, independent Module Development Guide duplicate pair**, on top of what
the sibling document already found.

**00-Quick-Start-Guide and install-sh (both incorporated, complementary pair):** a 30-minute quick-start
narrative (zero licensing costs, plugin architecture, 30-50% cost savings versus commercial CCTV, edge-
first AI) paired with its executable counterpart — a bash installation script automating OpenVision setup.

**01-Executive-Summary and EXECUTIVE-SUMMARY (both incorporated — a confirmed duplicate pair, see
Unresolved Tensions):** both present OpenVision as eliminating vendor lock-in and reducing TCO by 30-50%
against the same named incumbent vendors (Genetec, Milestone, Axis/Verkada), sizing the global video-
surveillance market at $50B+ annually.

**03-Module-Development-Guide and development-md (both incorporated — a confirmed duplicate pair, see
Unresolved Tensions):** both describe the same plugin-based module framework — custom analytics/
processing/integration modules run as isolated, containerized applications communicating via standardized
interfaces without modifying the core codebase.

**04-Enterprise-Deployment, 06-Complete-Deployment-Guide, 04-docker-compose-yml, 05-kubernetes-manifests-
yml, and core-stack-yml (all incorporated — a five-document deployment cluster with two internal
technology divergences, see Unresolved Tensions):** 04-Enterprise-Deployment is a DevOps/SRE-targeted
guide for a 500-camera/20-site high-availability deployment (central cloud setup, edge-site deployment,
network configuration, security hardening). 06-Complete-Deployment-Guide restates deployment scenarios
"from development to enterprise production" spanning the same scale range. 05-kubernetes-manifests-yml is
the Kubernetes deployment counterpart to the sibling document's enterprise-tier Rook-Ceph/PostgreSQL-
operator stack. Two small-deployment docker-compose files exist for the same 5-50-camera SMB/development
tier: 04-docker-compose-yml specifies MediaMTX as the video-management system, while core-stack-yml
specifies Frigate — the same VMS-choice divergence pattern already flagged in the sibling document's tech-
stack findings, here appearing again between two documents nominally targeting the identical small-
deployment use case.

**07-Use-Cases-Integration (incorporated):** a business-audience document ("Business Leaders, Operations
Managers, Innovation Teams") framing transformative use cases for repositioning CCTV infrastructure "from
cost center to strategic asset."

**IHOSE-DataFlow-API-DevSecOps-Specification (incorporated, genuinely distinct):** the one document in
this topic explicitly scoped as an extension of a *different* IHOSE document ("Extends: IHOSE Complete
Technical Specification v3.0" — a document not itself a member of this topic), covering OpenAPI 3.1 data-
flow/API contracts and a CI/CD DevSecOps automation pipeline — content not duplicated anywhere else in
this topic.

**README (incorporated):** the project's top-level README, describing OpenVision's Apache 2.0/AGPL dual-
licensing, an "Alpha" status badge, and a microservices/edge-to-cloud architecture overview consistent
with the sibling document's architecture description.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| OpenVision executive architecture overview and key differentiators | 01-OpenVision-Architecture | referenced — fully detailed in [DC-IHOSE-ARCHITECTURE-DEPLOYMENT-RECONCILED-001](DC-IHOSE-ARCHITECTURE-DEPLOYMENT-RECONCILED-001.md) |
| OpenVision technology-stack table (APISIX gateway, NATS/Kafka messaging) | 03-Technical-Architecture | referenced — fully detailed in the sibling document above |
| Household/Small-Business/Enterprise/SaaS deployment runbooks | DEPLOYMENT-GUIDE | referenced — fully detailed in the sibling document above |
| OpenVision complete technical architecture | TECHNICAL-ARCHITECTURE | referenced — fully detailed in the sibling document above |
| Enterprise-tier infrastructure provisioning, service stack, cost analysis | enterprise-md | referenced — fully detailed in the sibling document above |
| OpenVision architecture principles, layered architecture | overview-md | referenced — fully detailed in the sibling document above |
| 30-minute quick-start narrative | 00-Quick-Start-Guide | incorporated |
| Executable installation script | install-sh | incorporated |
| Executive summary (first copy) | 01-Executive-Summary | incorporated (duplicate pair, see Unresolved Tensions) |
| Executive summary (second copy) | EXECUTIVE-SUMMARY | incorporated (duplicate pair, see Unresolved Tensions) |
| Module-development plugin framework (first copy) | 03-Module-Development-Guide | incorporated (duplicate pair, see Unresolved Tensions) |
| Module-development plugin framework (second copy) | development-md | incorporated (duplicate pair, see Unresolved Tensions) |
| Enterprise deployment guide, 500-camera/20-site HA scenario | 04-Enterprise-Deployment | incorporated |
| Complete deployment guide, dev-to-production scenarios | 06-Complete-Deployment-Guide | incorporated |
| Kubernetes deployment manifests | 05-kubernetes-manifests-yml | incorporated |
| SMB docker-compose (MediaMTX VMS choice) | 04-docker-compose-yml | incorporated (VMS-choice divergence, see Unresolved Tensions) |
| SMB docker-compose (Frigate VMS choice) | core-stack-yml | incorporated (VMS-choice divergence, see Unresolved Tensions) |
| Business-audience transformative use cases | 07-Use-Cases-Integration | incorporated |
| OpenAPI data-flow contracts and DevSecOps CI/CD pipeline | IHOSE-DataFlow-API-DevSecOps-Specification | incorporated |
| Top-level project README, licensing, architecture overview | README | incorporated |

## Unresolved tensions

**This topic extends the OpenVision documentation-duplication pattern already identified in
[DC-IHOSE-ARCHITECTURE-DEPLOYMENT-RECONCILED-001](DC-IHOSE-ARCHITECTURE-DEPLOYMENT-RECONCILED-001.md) with
two further confirmed duplicate pairs, reported here as Stage 4 dedup-review candidates rather than
resolved by this pass** (per DC-CONSOLIDATOR-STD-001 §0):

1. **01-Executive-Summary-md.md and EXECUTIVE-SUMMARY-md.md** open with near-identical framing — the
   same $50B+ market-size figure, the same three named incumbent vendors (Genetec, Milestone, Verkada/
   Axis), and the same 30-50% TCO-reduction claim — under near-identical titles ("OpenVision Platform
   Executive Summary" vs "OpenVision Platform - Executive Summary").
2. **03-Module-Development-Guide-docx.md and development-md.md** describe the identical plugin-based
   module framework (isolated containerized modules, standardized interfaces, no core-code modification
   required) under near-identical titles ("Custom Module Development Guide" vs "Module Development
   Guide").

**A third, narrower divergence:** the two small-deployment docker-compose files targeting the same 5-50-
camera use case (`04-docker-compose-yml.md` and `core-stack-yml.md`) specify different video-management
systems as their primary VMS — MediaMTX in one, Frigate in the other — neither cross-referencing the
other. This is the same category of unreconciled tooling-specificity divergence the sibling document
already flagged for the API-gateway/event-bus choice, now appearing a second time at the small-deployment
tier specifically.

**Combined with the sibling document's own findings, this brings the total confirmed or likely duplicate/
divergence clusters across the two IHOSE OpenVision-related Consolidator topics to: one API-gateway/event-
bus tooling divergence, one VMS-choice divergence, a four-way architecture-document duplication cluster,
and now two further confirmed duplicate pairs (Executive Summary, Module Development Guide) — a pattern
consistent enough across this many independent document pairs that it likely reflects a systematic
authoring process (repeated AI-assisted document generation from similar prompts) rather than isolated
incidents, worth flagging to whoever maintains the IHOSE/OpenVision documentation set as a candidate for
a full audit rather than piecemeal dedup.**

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/security/IHOSE/00-Quick-Start-Guide-md.md`
- `knowledge-base/d-central/security/IHOSE/01-Executive-Summary-md.md`
- `knowledge-base/d-central/security/IHOSE/01-OpenVision-Architecture-docx.md`
- `knowledge-base/d-central/security/IHOSE/03-Module-Development-Guide-docx.md`
- `knowledge-base/d-central/security/IHOSE/03-Technical-Architecture-md.md`
- `knowledge-base/d-central/security/IHOSE/04-Enterprise-Deployment-md.md`
- `knowledge-base/d-central/security/IHOSE/04-docker-compose-yml.md`
- `knowledge-base/d-central/security/IHOSE/05-kubernetes-manifests-yml.md`
- `knowledge-base/d-central/security/IHOSE/06-Complete-Deployment-Guide-docx.md`
- `knowledge-base/d-central/security/IHOSE/07-Use-Cases-Integration-md.md`
- `knowledge-base/d-central/security/IHOSE/DEPLOYMENT-GUIDE-md.md`
- `knowledge-base/d-central/security/IHOSE/EXECUTIVE-SUMMARY-md.md`
- `knowledge-base/d-central/security/IHOSE/IHOSE-DataFlow-API-DevSecOps-Specification-md.md`
- `knowledge-base/d-central/security/IHOSE/README-md.md`
- `knowledge-base/d-central/security/IHOSE/TECHNICAL-ARCHITECTURE-md.md`
- `knowledge-base/d-central/security/IHOSE/core-stack-yml.md`
- `knowledge-base/d-central/security/IHOSE/development-md.md`
- `knowledge-base/d-central/security/IHOSE/enterprise-md.md`
- `knowledge-base/d-central/security/IHOSE/install-sh.md`
- `knowledge-base/d-central/security/IHOSE/overview-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/security/IHOSE/00-Quick-Start-Guide-md.md,
  knowledge-base/d-central/security/IHOSE/01-Executive-Summary-md.md,
  knowledge-base/d-central/security/IHOSE/01-OpenVision-Architecture-docx.md,
  knowledge-base/d-central/security/IHOSE/03-Module-Development-Guide-docx.md,
  knowledge-base/d-central/security/IHOSE/03-Technical-Architecture-md.md,
  knowledge-base/d-central/security/IHOSE/04-Enterprise-Deployment-md.md,
  knowledge-base/d-central/security/IHOSE/04-docker-compose-yml.md,
  knowledge-base/d-central/security/IHOSE/05-kubernetes-manifests-yml.md,
  knowledge-base/d-central/security/IHOSE/06-Complete-Deployment-Guide-docx.md,
  knowledge-base/d-central/security/IHOSE/07-Use-Cases-Integration-md.md,
  knowledge-base/d-central/security/IHOSE/DEPLOYMENT-GUIDE-md.md,
  knowledge-base/d-central/security/IHOSE/EXECUTIVE-SUMMARY-md.md,
  knowledge-base/d-central/security/IHOSE/IHOSE-DataFlow-API-DevSecOps-Specification-md.md,
  knowledge-base/d-central/security/IHOSE/README-md.md,
  knowledge-base/d-central/security/IHOSE/TECHNICAL-ARCHITECTURE-md.md,
  knowledge-base/d-central/security/IHOSE/core-stack-yml.md,
  knowledge-base/d-central/security/IHOSE/development-md.md,
  knowledge-base/d-central/security/IHOSE/enterprise-md.md,
  knowledge-base/d-central/security/IHOSE/install-sh.md,
  knowledge-base/d-central/security/IHOSE/overview-md.md,
]
reconciled_against: [
  docs/DC-IHOSE-ARCHITECTURE-DEPLOYMENT-RECONCILED-001.md,
]
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved by this pass — status assignment, including all
duplicate/divergence findings above, belongs to DC-DEDUP-STD-001, not the Consolidator.
