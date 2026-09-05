# DC-OPENSECURE-OPENPIV-SUBSYSTEM-RECONCILED-001 — OpenSecure OpenPIV Subsystem, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `opensecure-openpiv-subsystem` (5 docs).

## Current understanding

This topic's membership overlaps the already-consolidated `openpiv-pacs-integration-suite` topic on
three of its five docs (Implementation Roadmap, OS-PACS Integration Guide, Quick Start Guide) — see
[DC-OPENPIV-PACS-INTEGRATION-RECONCILED-001](DC-OPENPIV-PACS-INTEGRATION-RECONCILED-001.md) for their
full claim inventory. This consolidation details the two documents this topic adds: a project-
organization overview and a component-level technical architecture reference, both consistent with the
sibling consolidation's content and with each other.

**Recap from the prior consolidation (incorporated by reference):** the Implementation Roadmap's
60-week phased build plan, the Deployment Checklist's hardware BOM and cost figures (with its own
unreconciled tension against the Integration Guide's separate cost figures, already documented in the
sibling), and the Quick Start Guide's one-day single-card path — all fully detailed there.

**OpenPIV Project Organization (incorporated):** a project-vision/repo-organization overview structuring
the ecosystem into 7 repositories (cards, PKI, enrollment, middleware, access-control, integration,
docs), each with its primary open-source component (OpenFIPS201, Dogtag, a custom enrollment stack,
OpenSC, Leosac+LibOSDP) and a full proposed file-tree layout [Project Structure, Component Architecture].
A technology-license table (Apache 2.0 for OpenFIPS201/LibOSDP, LGPL for GlobalPlatformPro/OpenSC, GPL
for Dogtag, AGPL for Leosac) [Technical Stack Summary]. A standards-compliance section explicitly listing
what OpenPIV **can** achieve (technical compliance with FIPS 201-3/SP 800-73-4/800-76-2/800-78-4,
interoperable card format) versus what it **cannot** (official NIST validation, federal PKI cross-
certification, GSA Approved Product List listing, actual federal facility access) — summarized as
"95%+ of PIV functionality for private sector use" [Standards Compliance]. Three deployment models with
their own cost figures — Small Office (10-50 users, $3,000-5,000, 2-3 weeks), Enterprise (500+ users,
$25,000-50,000, 2-3 months), Education/Training Lab ($1,000-2,000, 1-2 days) [Deployment Models] — which
describe identity/PKI-only scope (not door count) and are not directly comparable to the sibling
consolidation's 50-door/500-user PACS-integration cost figures. A 5-phase, 15-month development roadmap,
risk-management tables, and a community-governance section (Apache 2.0, 2-approver code review, >80%
test coverage requirement).

**OpenPIV Technical Architecture (incorporated):** a component-level system reference — the PIV card's
data-object layout (CHUID, facial image, fingerprint objects, and the four key slots 9A/9C/9D/9E) and
two key-generation methods (on-card generation preferred; external generation+import for backup/escrow
only) [Layer 1]. The Dogtag PKI hierarchy (offline 10-year Root CA, online 3-5-year Issuing CA, OCSP
responder, CRL distribution) with full certificate-profile YAML for all four PIV certificate types,
matching the certificate-type list in the sibling consolidation's Integration Guide detail exactly
[Layer 2]. A complete enrollment-system database schema (users/credentials/certificates/biometrics/
audit_log tables) and REST API endpoint list [Layer 3]. OpenSC's internal layering (application →
PKCS#11 module → PIV card driver → PC/SC → reader → card) with actual config-file content for
`opensc.conf`, Linux PAM, and SSH [Layer 4]. Leosac's module architecture (OSDP/GPIO/Wiegand modules)
with actual `kernel.xml` and YAML access-policy examples [Layer 5]. Three worked data-flow diagrams
(enrollment, physical-access authentication, logical desktop-login authentication) and a 4-zone network-
segmentation design (DMZ → internal management → PKI security zone → physical access control zone) with
a port-requirements table. Performance specs (200-300 cards/day issuance capacity, <2s authentication,
<500ms OCSP) and security specs (ECC P-256/RSA 2048 card keys, RSA 4096/ECC P-384 Root CA keys, 7-year
minimum audit-log retention).

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| 60-week phased build plan | Implementation Roadmap (full detail) | incorporated — fully detailed in the sibling consolidation [DC-OPENPIV-PACS-INTEGRATION-RECONCILED-001](DC-OPENPIV-PACS-INTEGRATION-RECONCILED-001.md) |
| Deployment checklist hardware BOM and cost figures | OS-PACS Integration Guide (full detail) | incorporated — fully detailed in the sibling consolidation, including its own unreconciled cost tension |
| One-day single-card quick start | Quick Start Guide (full detail) | incorporated — fully detailed in the sibling consolidation |
| 7-repo project structure and per-component technology choices | Project Organization, Project Structure / Component Architecture | incorporated |
| License table | Project Organization, Technical Stack Summary | incorporated (consistent with the components named in the Technical Architecture document) |
| FIPS 201 compliance boundary (can/cannot achieve) | Project Organization, Standards Compliance | incorporated |
| Three deployment models and their cost figures | Project Organization, Deployment Models | incorporated — not directly comparable to the sibling's PACS-integration cost figures (different scope: identity/PKI-only vs. door-integrated) |
| 5-phase, 15-month roadmap and risk tables | Project Organization, Development Phases / Risk Management | incorporated |
| PIV card data-object layout and key-generation methods | Technical Architecture, Layer 1 | incorporated |
| Dogtag PKI hierarchy and certificate profiles | Technical Architecture, Layer 2 | incorporated (certificate types match the sibling Integration Guide's list exactly) |
| Enrollment database schema and API endpoints | Technical Architecture, Layer 3 | incorporated |
| OpenSC layering and config files | Technical Architecture, Layer 4 | incorporated |
| Leosac module architecture and access policy | Technical Architecture, Layer 5 | incorporated |
| Data-flow diagrams and network segmentation | Technical Architecture, Data Flow Diagrams / Network Architecture | incorporated |
| Performance and security specifications | Technical Architecture, Performance Specifications / Security Specifications | incorporated |

## Unresolved tensions

None identified between the two new documents and the sibling consolidation's content — the Technical
Architecture document's certificate types, component choices, and PIV data model are fully consistent
with the Project Organization document's stack summary and with the sibling consolidation's own
Integration Guide detail. The Project Organization document's deployment-model cost figures are noted as
non-comparable to (not conflicting with) the sibling's PACS-integration cost figures, since they measure
a different deployment scope (identity/PKI infrastructure sized by user count, not door-integrated
physical access control sized by door count).

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/core/identity/Open-Secure/OpenPIV-Project-Organization-md.md`
- `knowledge-base/d-central/core/identity/Open-Secure/OpenPIV-Technical-Architecture-md.md`
- `knowledge-base/d-central/security/Open-Secure/OpenPIV-Implementation-Roadmap-md.md`
- `knowledge-base/d-central/security/Open-Secure/OpenPIV-OS-PACS-Integration-Guide-md.md`
- `knowledge-base/d-central/security/Open-Secure/OpenPIV-Quick-Start-Guide-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/core/identity/Open-Secure/OpenPIV-Project-Organization-md.md,
  knowledge-base/d-central/core/identity/Open-Secure/OpenPIV-Technical-Architecture-md.md,
  knowledge-base/d-central/security/Open-Secure/OpenPIV-Implementation-Roadmap-md.md,
  knowledge-base/d-central/security/Open-Secure/OpenPIV-OS-PACS-Integration-Guide-md.md,
  knowledge-base/d-central/security/Open-Secure/OpenPIV-Quick-Start-Guide-md.md,
]
reconciled_against: [DC-OPENPIV-PACS-INTEGRATION-RECONCILED-001.md (sibling consolidation covering the Implementation Roadmap, Integration Guide, and Quick Start Guide in full detail)]
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
