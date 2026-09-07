# DC-MESHPLATE-PRIVACY-COMPLIANCE-RECONCILED-001 — MeshPlate Federation & CivicMesh Privacy Compliance, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `meshplate-federation-privacy-compliance` (4 docs).

## Current understanding

Four documents covering CivicMesh's license-plate federation protocol and its privacy/regulatory
foundations, from three different angles: the technical federation protocol itself, the public-facing
privacy commitment, the formal PIPEDA compliance framework, and a surveillance-law analysis for the
sibling CommunityShield residential product. All four are technically and legally consistent.

**MeshPlate Federation Protocol (incorporated):** distinguishes automatic federation (confirmed bylaw-
violation evidence packages only — never the resident trusted-vehicle registry or raw visitor logs)
from investigation-specific cross-community query, which requires a warrant for historical queries,
hashes the submitted plate against each community's salt, returns only matching event metadata (never
exposing the community's plate database), and purges plaintext-derived data within 30 days of case
closure [§1-2]. A "no-data-broker covenant" bars sale or access by commercial brokers, insurance
aggregators (outside direct insurer relationships), immigration enforcement, or political campaigns —
enforced both technically (no bulk-export API; query API restricted to municipal law enforcement with
active federation agreements, community managers for their own data, CCSC members for their own
vehicle) and legally (written into the AGPL v3 Community Edition license, making non-compliant
deployment a license breach) [§3].

**CivicMesh Privacy Promise (incorporated):** the public plain-language commitment (published at
civicmesh.ca/privacy) restating the same technical facts as the other three documents in consumer
terms — on-device face blurring before transmission, hash-before-store ALPR (SHA-256, plate held in
device memory only during capture), no continuous recording (non-violation frames discarded on-
device), and a "we will never" list matching the Federation Protocol's no-data-broker covenant exactly
(no advertiser sharing, no immigration-authority sharing without a court order, no movement-profile
building) [Privacy Promise, §1]. A verifiability table marks each control as independently verifiable
via published open-source firmware code or the public evidence-package schema (DC-CM-ARCH-001) [§1]. A
rights-exercise table (see/correct/delete data, view access history, file a complaint) with a uniform
30-day fulfillment commitment matching REG-CM-001's individual-access-rights timelines exactly [§2].

**CivicMesh PIPEDA Compliance Framework (incorporated):** confirms PIPEDA applies (commercial personal-
information collection, no purely-personal-use or law-enforcement exemption for CivicMesh as operator),
notes Quebec Law 25/BC PIPA/Alberta PIPA take precedence where stricter [§1]. A PIA template assigning
responsible parties per element (data inventory, data-flow diagram, risk assessment, consent mechanism,
third-party disclosures, retention/deletion, breach response) [§2]. All ten PIPEDA principles mapped to
specific technical controls — notably Principle 4 (Limiting Collection) citing the identical on-device
minimization/hash-before-store/no-continuous-recording controls the Privacy Promise document describes
publicly, and Principle 3 (Consent) describing GraphQL-API-layer technical consent enforcement [§3]. A
detailed breach-notification procedure (72-hour OPC notification if real risk of significant harm,
48-hour community notification via NOC Console, 2-year minimum breach-record retention) [§4].

**CommunityShield Surveillance Regulatory Analysis (incorporated):** extends the same PIPEDA foundation
to the residential/HOA/apartment CommunityShield product — a municipal-bylaw survey (Ottawa/Toronto/
Vancouver, none requiring camera registration for private property, BC PIPA applying additionally in
Vancouver) [§1], condo-corporation camera authority under the Ontario Condominium Act (board authority
over common elements, s.97 owner-notification requirement, specific hallway-camera placement guidance
to avoid unit-entrance monitoring) [§2], and a Residential Tenancies Act permitted/prohibited matrix for
landlord-installed cameras (exterior/common areas permitted with notice, in-unit prohibited, cameras
cannot be a lease condition) [§3]. The hallway-camera and RTA guidance here is identical in substance to
the equivalent guidance already detailed in the sibling
[DC-CS-HOA-DEPLOYMENT-RECONCILED-001](DC-CS-HOA-DEPLOYMENT-RECONCILED-001.md) consolidation (which
covers DEPLOY-CS-002's restatement of this same REG-CS-001 analysis).

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Automatic vs. investigation-specific federation, warrant/hash/purge requirements | DC-MP-FED-001, §1-2 | incorporated |
| No-data-broker covenant and its technical/legal (AGPL) enforcement | DC-MP-FED-001, §3 | incorporated |
| Public privacy promise (collection scope, rights, access log) | MKT-CCSC-004, Privacy Promise / §2 | incorporated (consistent with REG-CM-001's technical controls and rights timelines) |
| Technical privacy controls and independent-verifiability claims | MKT-CCSC-004, §1 | incorporated |
| PIPEDA applicability and provincial supplements | REG-CM-001, §1 | incorporated |
| PIA template and responsible parties | REG-CM-001, §2 | incorporated |
| Ten PIPEDA principles mapped to technical controls | REG-CM-001, §3 | incorporated (Principle 4's on-device minimization controls match the Privacy Promise document's public claims exactly) |
| Breach notification procedure | REG-CM-001, §4 | incorporated |
| Municipal camera bylaw survey (Ottawa/Toronto/Vancouver) | REG-CS-001, §1 | incorporated |
| Condo corporation camera authority and hallway-camera guidance | REG-CS-001, §2 | incorporated (same substance as the sibling DC-CS-HOA-DEPLOYMENT consolidation's coverage of DEPLOY-CS-002) |
| RTA landlord permitted/prohibited camera matrix | REG-CS-001, §3 | incorporated |

## Unresolved tensions

None identified in this pass — the technical controls described in the public Privacy Promise, the
formal PIPEDA framework's principle-by-principle mapping, and the Federation Protocol's own technical
enforcement mechanisms are consistent and mutually reinforcing (hash-before-store, on-device face
blurring, no continuous recording, and the no-data-broker covenant recur identically across all
relevant documents), and the CommunityShield surveillance analysis extends the same legal foundation
without contradicting any figure or claim in the other three.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/security/CivicMesh/DC-MP-FED-001-MeshPlate-Federation-Protocol-v1-docx.md`
- `knowledge-base/d-central/security/CivicMesh/MKT-CCSC-004-CivicMesh-Privacy-Promise-v1-docx.md`
- `knowledge-base/d-central/security/CivicMesh/REG-CM-001-CivicMesh-PIPEDA-Compliance-Framework-v1-docx.md`
- `knowledge-base/d-central/security/CivicMesh/REG-CS-001-CommunityShield-Surveillance-Regulatory-Analysis-v1-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/security/CivicMesh/DC-MP-FED-001-MeshPlate-Federation-Protocol-v1-docx.md,
  knowledge-base/d-central/security/CivicMesh/MKT-CCSC-004-CivicMesh-Privacy-Promise-v1-docx.md,
  knowledge-base/d-central/security/CivicMesh/REG-CM-001-CivicMesh-PIPEDA-Compliance-Framework-v1-docx.md,
  knowledge-base/d-central/security/CivicMesh/REG-CS-001-CommunityShield-Surveillance-Regulatory-Analysis-v1-docx.md,
]
reconciled_against: [DC-CS-HOA-DEPLOYMENT-RECONCILED-001.md (sibling consolidation covering the same REG-CS-001 hallway-camera/RTA guidance as restated in DEPLOY-CS-002)]
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

**References:**
- [[DC-CS-HOA-DEPLOYMENT-RECONCILED-001|DC-CS-HOA-DEPLOYMENT-RECONCILED-001 — CommunityShield HOA/Condo Deployment Package, Consolidated (v1, generated 2026-09-05)]]

**Referenced by:**
- [[DC-CIVICMESH-FEDERATION-NOC-MUNICIPAL-RECONCILED-001|DC-CIVICMESH-FEDERATION-NOC-MUNICIPAL-RECONCILED-001 — CivicMesh Federation, NOC & Municipal Deployment, Consolidated (v1, generated 2026-09-05)]]

<!-- AUTO-GENERATED RELATED END -->
