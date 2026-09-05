# DC-CS-HOA-DEPLOYMENT-RECONCILED-001 — CommunityShield HOA/Condo Deployment Package, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `communityshield-hoa-deployment-package` (4 docs).

## Current understanding

Four complementary documents covering CommunityShield's residential-property deployment product: two
operational deployment playbooks for different property types (HOA/condo vs. apartment/rental), the
master legal participation agreement template underlying both, and a public-consultation toolkit for
managing community pushback. All four are consistent on fee splits, consent timelines, and data
governance.

**HOA/condo deployment (DEPLOY-CS-001, incorporated):** a standard hardware/service package (2 outdoor
cameras, community NAS, PoE switch, install) delivered on a 30-day timeline from agreement signature to
first weekly report, with mandatory resident notice (7-point disclosure list, minimum 14 days for
non-residential / 30 days for residential properties, board/strata approval required) [§1-3]. Fine
revenue is off by default; activating it requires the community to confirm bylaw authority and
configure violation types, with proceeds split 60% community / 25% node-owner members (via CCSC) / 15%
CommunityShield platform fee, and mandatory manual review of the first 10 enforcement incidents before
Fast-Track automation is enabled [§4].

**Apartment/rental deployment (DEPLOY-CS-002, incorporated):** distinguishes what a landlord may deploy
unilaterally (exterior/lobby/parking cameras with posted notice) from what requires tenant consent
(hallway cameras positioned to avoid revealing tenant presence patterns) from what's prohibited entirely
(cameras inside units — Residential Tenancies Act s.29) [§1]. A tenant-opt-in rent-credit programme lets
tenants connect their own doorbell cameras for an estimated $20-60/month rent credit funded by CCSC
patronage, explicitly structured as voluntary since the RTA prohibits landlords from mandating
surveillance equipment as a tenancy condition [§2]. A parallel 8-week deployment timeline mirrors
DEPLOY-CS-001's structure with a longer 30-day tenant-notification period built in [§3].

**Master participation agreement (LEGAL-CM-012, incorporated):** the template contract both deployment
playbooks operate under — a 2-year renewable term, resident-consent certification gating node
activation (matching the same 14/30-day notice periods as DEPLOY-CS-001) [§1-2], a fee schedule (TBD
dollar amounts for monthly platform fee, per-node fee, installation fee, annual audit fee) [§3], a
revenue-distribution table breaking fine revenue down by violation type — parking violations 60/25/15
(community/node-owners/CommunityShield), HOA rule violations 70/20/10, trespassing/access 65/20/15,
government citations per separate agreements [§4] — an insurance premium-reduction facilitation process
with no guaranteed outcome [§5], data governance (community + individual node-owner co-ownership of
evidence, 24-hour law-enforcement-access notification, 90-day default retention) [§6], and exit terms
(60-day notice, data returned in CSV+MP4 or deleted, CCSC membership continuity preserved) [§7].

**Public consultation toolkit (MKT-CCSC-003, incorporated):** a preparation checklist and meeting-agenda
template explicitly designed to prevent "DeFlock-style backlash" by front-loading transparency (camera
map, privacy notice, empty law-enforcement-request log at launch) before residents can raise objections
[§1-2]. A prepared-answers table for five anticipated hard questions (footage-request authority, breach
scenarios, opt-out/non-consent, Big Tech data access, cancellation terms) [§3], each answer consistent
with LEGAL-CM-012's actual contractual terms (community-owned NAS storage, 48-hour breach/request
notification, 60-day no-cost cancellation with full data return).

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Standard HOA hardware/service package and 30-day timeline | DEPLOY-CS-001 §1-2 | incorporated |
| HOA resident consent requirements (7-point disclosure, 14/30-day notice, board approval) | DEPLOY-CS-001 §3 | incorporated (consistent with LEGAL-CM-012 §2's notice periods) |
| HOA fine-revenue activation and 60/25/15 split | DEPLOY-CS-001 §4 | incorporated (matches LEGAL-CM-012 §4's parking-violation row exactly) |
| Landlord permitted/prohibited camera placements under RTA | DEPLOY-CS-002 §1 | incorporated |
| Tenant opt-in rent-credit programme (voluntary, RTA-compliant) | DEPLOY-CS-002 §2 | incorporated |
| Apartment 8-week deployment timeline | DEPLOY-CS-002 §3 | incorporated (consistent structure with DEPLOY-CS-001, longer tenant-notice window) |
| Master agreement scope, term, consent-certification gate | LEGAL-CM-012 §1-2 | incorporated |
| Fee schedule (platform/per-node/install/audit) | LEGAL-CM-012 §3 | incorporated (dollar amounts left as template placeholders, per-community) |
| Fine-revenue distribution by violation type | LEGAL-CM-012 §4 | incorporated |
| Insurance facilitation, data governance, exit terms | LEGAL-CM-012 §5-7 | incorporated |
| Consultation preparation checklist and meeting agenda | MKT-CCSC-003 §1-2 | incorporated |
| Prepared answers to anticipated hard questions | MKT-CCSC-003 §3 | incorporated (answers consistent with LEGAL-CM-012's actual contractual terms) |

## Unresolved tensions

None identified in this pass — all four documents describe the same product (deployment playbooks,
master contract, consultation toolkit) consistently, and every cross-checkable figure (fee splits,
notice periods, data-governance terms) matches across documents.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/business-legal/CivicMesh/DEPLOY-CS-001-CommunityShield-HOA-Condo-Deployment-v1-docx.md`
- `knowledge-base/d-central/business-legal/CivicMesh/DEPLOY-CS-002-CommunityShield-Apartment-Complex-Deployment-v1-docx.md`
- `knowledge-base/d-central/business-legal/CivicMesh/LEGAL-CM-012-HOA-Condo-Participation-Agreement-v1-docx.md`
- `knowledge-base/d-central/business-legal/CivicMesh/MKT-CCSC-003-Public-Consultation-Toolkit-v1-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/business-legal/CivicMesh/DEPLOY-CS-001-CommunityShield-HOA-Condo-Deployment-v1-docx.md,
  knowledge-base/d-central/business-legal/CivicMesh/DEPLOY-CS-002-CommunityShield-Apartment-Complex-Deployment-v1-docx.md,
  knowledge-base/d-central/business-legal/CivicMesh/LEGAL-CM-012-HOA-Condo-Participation-Agreement-v1-docx.md,
  knowledge-base/d-central/business-legal/CivicMesh/MKT-CCSC-003-Public-Consultation-Toolkit-v1-docx.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
