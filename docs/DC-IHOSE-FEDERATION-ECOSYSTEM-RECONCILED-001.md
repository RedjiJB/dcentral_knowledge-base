# DC-IHOSE-FEDERATION-ECOSYSTEM-RECONCILED-001 — Iron Horse Security (IHOSE) Federation & Ecosystem Partnership Framework, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic
`ihose-federation-ecosystem-partnership-framework` (4 docs — corrected from the 5 docs originally
clustered; see note below).

## Topic correction made during this pass

This topic's `_topics.md` entry originally listed a fifth document,
`IronHorse-md.md` (original filename `IronHorse.md`). On reading it, that document is **"Iron Horse
Workspace Suite" — an open-source Microsoft 365 / productivity-suite alternative** — an entirely
different product from "Iron Horse Security" (IHOSE), the enterprise security-guard/video-surveillance
modernization platform the other four documents describe. The two share only the "Iron Horse" brand
name, which is exactly the lexical-clustering failure mode DC-TOPIC-SYNTH-STD-001 warns against. Per
this repo's guardrail against silently splitting or consolidating a mis-scoped topic, the mis-tagged
document's `topic:` front-matter line was removed and `knowledge-base/_topics.md`'s entry for this
topic was corrected from 5 to 4 docs before this consolidation proceeded. `IronHorse-md.md` is not
consolidated here and is not currently a member of any confirmed Stage 5 topic — it should get its own
topic-synthesis pass in a future session, since it appears to be the sole D-Central document about that
distinct product.

## Current understanding

Four documents specifying IHOSE (Iron Horse Security's open-source enterprise modernization framework)
at different scopes: a documentation-improvement recommendations memo, the federation/partner-ecosystem
extension (v1.0), the complete v3.0 technical specification, and a docx-converted export that
substantially duplicates part of the v3.0 specification's later sections.

**IHOSE Federation & Ecosystem Framework v1.0 (incorporated):** the core document for this topic —
explicitly framed as extending "IHOSE Complete Technical Specification v3.0" — transforms IHOSE from a
single-company solution into an open platform ecosystem across four stakeholder types (partner security
companies, open-source community, hardware manufacturers, academic institutions), each given an explicit
value-received/contribution pair [§1]. A **Federated Partner Program** (§2): a Partner SDK (REST/GraphQL
APIs, standardized guard/site/incident/patrol data schemas, Keycloak-based multi-tenant auth, governance
templates, Python/JS/Go/Java client libraries, sandbox testing tools) with a full repo layout and a
worked Python client implementation (`IronHorseClient`, OAuth2 client-credentials flow against
per-partner Keycloak realms, automatic token refresh, retry-with-backoff) [§2.1-2.3]; a Multi-Tenant
Keycloak Federation Manager and a Partner Onboarding Automation service provisioning a new partner's
realm, VPN endpoint, and monitoring stack (Grafana/Prometheus subdomains) automatically [§2.4-2.5]. A
**Community Open-Source Foundation** (§3): the Iron Horse Open Technology Foundation (IHOTF) governance
body, a defined repository structure, a contributor agreement, and a governance model. A **Hardware
Certification Program** (§4): the "Iron Horse Certified Hardware" initiative, technical standards for
certified cameras/sensors/access-control devices, a certification process, and reference designs. An
**Academic & Research Integration** section (§5): a university partnership framework, joint R&D programs,
a certification-to-academic-credit mapping, and a student co-op program. An implementation roadmap
closes the document (§6).

**IHOSE Complete Technical Specification (Combined), v3.0 (incorporated):** the full underlying platform
specification this topic's Federation Framework extends — a 13-section enterprise architecture covering
a 7-layer architectural philosophy (infrastructure/networking → security/identity → platform services →
layers 4-7 summarized) [§1]; core business-systems transformation replacing the Microsoft/Google
productivity stack (a full Microsoft-ecosystem replacement matrix, Mailu-based email/messaging
infrastructure, and 10 further core-system replacements summarized) [§2]; field operations (guard
technology/IoT), on-site edge computing and security systems, open-hardware supply chain, a client-
facing portal/marketplace ecosystem, AI/analytics, enterprise integration/data fabric, and governance/
security/compliance (§3-9, each summarized at chapter level in the combined document); a detailed
Training, Onboarding & Personnel Development framework (Moodle/Open edX LMS integrated with Keycloak via
OAuth2/LTI 1.3 and Kafka completion events, a full onboarding workflow, continuous-learning/career-
development tracks, specialized training programs, performance analytics, open training content/hardware
labs, and a "Training-as-a-Service" commercialization model) [§10]; sector-specific operations (a
deployment-architecture pattern plus a fully worked Healthcare-sector implementation, with 9 further
sectors summarized) [§11]; a scalability/global-platform-strategy section (product portfolio strategy,
implementation roadmap, strategic outcomes) [§12]; and a conclusion [§13].

**IHOSE Improvement & Enhancement Recommendations (incorporated):** a documentation-strategy memo
(already independently detailed for its business-strategy content in the sibling
[DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001](DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001.md) consolidation)
recommending 13 categories of improvement to the overall IHOSE/OpenVision documentation package: visual
communication, financial modeling rigor (three-scenario analysis, sensitivity analysis, Monte Carlo
simulation, NPV/IRR), competitive intelligence depth, proof points/validation, implementation tools/
calculators, risk quantification, industry-specific deep dives, sales enablement materials, technical
documentation enhancements, additional recommended documents (including, notably, a "Partner Ecosystem
Guide" — directly anticipating the Federation & Ecosystem Framework document this topic centers on),
presentation formats, metrics/KPIs, and change-management content [§1-13]. This document's relevance to
*this* topic specifically is narrow — its one direct connection is recommending the partner-ecosystem
documentation that the Federation Framework document later delivers; its remaining content is business-
strategy-general and is the sibling consolidation's primary subject.

**Iron Horse IHOSE Complete Technical Specification (docx export) (incorporated, overlapping):** a
docx-converted export whose visible sections (10.1 through 12.3 — Training/Onboarding through Sector
Operations and Scalability) match the Complete Technical Specification (Combined) document's own
section 10-12 content almost exactly in structure and heading numbering. This reads as a partial
duplicate extraction of the same v3.0 specification (likely a different upload/export pass of the same
underlying document) rather than a document contributing genuinely new claims beyond what §10-12 of the
Combined specification already state. No content in this document contradicts the Combined document's
version of the same sections.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Federation ecosystem architecture and 4-stakeholder value proposition | Federation & Ecosystem Framework §1 | incorporated |
| Partner SDK, Keycloak multi-tenant federation, partner onboarding automation | Federation & Ecosystem Framework §2 | incorporated |
| Community Open-Source Foundation (IHOTF), repo structure, governance | Federation & Ecosystem Framework §3 | incorporated |
| Hardware Certification Program | Federation & Ecosystem Framework §4 | incorporated |
| Academic & Research Integration | Federation & Ecosystem Framework §5 | incorporated |
| Federation implementation roadmap | Federation & Ecosystem Framework §6 | incorporated |
| 7-layer enterprise architecture | Complete Technical Specification (Combined) §1 | incorporated |
| Core business-systems replacement (Microsoft/Google stack) | Complete Technical Specification (Combined) §2 | incorporated |
| Field ops, on-site infra, supply chain, client ecosystem, AI/analytics, integration, governance | Complete Technical Specification (Combined) §3-9 | incorporated (chapter-level, per the source's own summary depth) |
| Training/onboarding/personnel development framework | Complete Technical Specification (Combined) §10 | incorporated — same content also appears in the docx export, see below |
| Sector operations (deployment pattern + Healthcare worked example) | Complete Technical Specification (Combined) §11 | incorporated — same content also appears in the docx export |
| Scalability and global platform strategy | Complete Technical Specification (Combined) §12 | incorporated — same content also appears in the docx export |
| Conclusion | Complete Technical Specification (Combined) §13 | incorporated |
| Documentation-improvement recommendations (13 categories) | Improvement & Enhancement Recommendations | incorporated — business-strategy content fully detailed in sibling [DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001](DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001.md); its "Partner Ecosystem Guide" recommendation is the one direct link to this topic |
| Training/sector-ops/scalability sections (docx export) | Iron Horse IHOSE Complete Technical Specification (docx) §10.1-12.3 | incorporated (duplicate of Combined document's own §10-12; no new or conflicting claims found) |

## Unresolved tensions

None identified among the four correctly-scoped documents — the Federation Framework explicitly extends
the Complete Technical Specification, the docx export duplicates rather than contradicts a subset of
that same specification, and the Improvement Recommendations memo's one point of direct relevance
(recommending a partner-ecosystem guide) is consistent with what the Federation Framework document
actually delivers.

**Observation (not a conflict, flagged for a future Stage 4 dedup pass):** the docx export's §10.1-12.3
appear to be a duplicate extraction of the Combined specification's own §10-12, differing mainly in
document-conversion artifacts (docx-style plain-text section numbers vs. Markdown headings). A dedup
pass may find these two documents' overlapping sections are near-identical enough to warrant a formal
supersession or merge decision — that determination belongs to DC-DEDUP-STD-001, not this consolidation.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/business-legal/IHOSE/IMPROVEMENT-RECOMMENDATIONS-md.md`
- `knowledge-base/d-central/core/governance/IHOSE/IHOSE-Federation-Ecosystem-Framework-md.md`
- `knowledge-base/d-central/meta/platform-scaffolding/IHOSE/IHOSE-Complete-Technical-Specification-Combined-md.md`
- `knowledge-base/d-central/meta/platform-scaffolding/IHOSE/Iron-Horse-IHOSE-Complete-Technical-Specification-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/business-legal/IHOSE/IMPROVEMENT-RECOMMENDATIONS-md.md,
  knowledge-base/d-central/core/governance/IHOSE/IHOSE-Federation-Ecosystem-Framework-md.md,
  knowledge-base/d-central/meta/platform-scaffolding/IHOSE/IHOSE-Complete-Technical-Specification-Combined-md.md,
  knowledge-base/d-central/meta/platform-scaffolding/IHOSE/Iron-Horse-IHOSE-Complete-Technical-Specification-docx.md,
]
reconciled_against: [DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001.md (sibling consolidation covering IMPROVEMENT-RECOMMENDATIONS' business-strategy content in full)]
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator. The topic-membership correction (removing the mis-tagged `IronHorse-md.md`) was made per this repo's Stage 5 mis-scoped-topic guardrail, documented above rather than performed silently.
