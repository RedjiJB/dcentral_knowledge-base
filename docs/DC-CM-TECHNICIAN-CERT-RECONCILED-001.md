# DC-CM-TECHNICIAN-CERT-RECONCILED-001 — CivicMesh Technician Certification & Training, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `civicmesh-technician-certification-training` (2 docs).

## Current understanding

DC-CM-CERT-001 defines the three-level (L1/L2/L3) technician certification programme structure
(scope, prerequisites, assessment format, background-check tier, renewal cycle); TRAIN-002 is the
actual curriculum content that fulfills it. The two are consistent on every checkable detail.

**Certification programme structure (incorporated):** L1 (Basic, entry-level, Tier 3 kit install) →
L2 (Advanced, requires L1 + 3 months field experience, Tier 1/2 install + edge-compute config) → L3
(Expert, requires L2 + 1 year experience + MSSP supervisor endorsement, tamper investigation + expert
witness support), each with an escalating background-check tier (basic CPIC → enhanced reliability →
enhanced security screening with credit check) and its own renewal cadence (L1 annual refresher, L2
biennial practical reassessment, L3 annual continuing education + oral assessment), with a 30-day
grace period before revocation [DC-CM-CERT-001 §1-3].

**Curriculum content (incorporated):** L1 is a 4-hour, $299 course (platform overview, hardware
fundamentals, installation procedures, privacy basics, a timed 10-minute practical) whose five embedded
quiz sections total exactly 30 questions — matching DC-CM-CERT-001's stated "30-question online exam"
for L1 precisely. L2 is 8 hours/$499 (Tier 1/2 hardware, edge-compute configuration, calibration,
fault diagnosis, a timed 60-minute full-fleet-vehicle practical). L3 is 16 hours/$799 (advanced
hardware/secure-boot, tamper investigation, advanced diagnostics, expert-witness preparation, MSSP NOC
integration, a comprehensive 4-hour practical) [TRAIN-002 §1-3].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| L1/L2/L3 level definitions, prerequisites, assessment format | DC-CM-CERT-001 §1 | incorporated |
| Background-check requirements by level | DC-CM-CERT-001 §2 | incorporated |
| Annual/biennial renewal requirements and grace period | DC-CM-CERT-001 §3 | incorporated |
| L1 curriculum (5 modules, 30 embedded-quiz questions total, practical) | TRAIN-002 §1 | incorporated (question count matches DC-CM-CERT-001's stated 30-question L1 exam exactly) |
| L2 curriculum (6 modules incl. edge-compute and fault diagnosis, practical) | TRAIN-002 §2 | incorporated |
| L3 curriculum (6 modules incl. tamper investigation and expert-witness prep, practical) | TRAIN-002 §3 | incorporated |

## Unresolved tensions

None identified in this pass — the one cross-checkable numeric detail (L1's 30-question exam) matches
exactly between the programme-definition document and the curriculum content, and no other claim in
either document contradicts the other.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/core/identity/CivicMesh/DC-CM-CERT-001-Technician-Certification-Programme-v1-docx.md`
- `knowledge-base/d-central/core/identity/CivicMesh/TRAIN-002-Track1-Node-Technician-Curriculum-v1-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/core/identity/CivicMesh/DC-CM-CERT-001-Technician-Certification-Programme-v1-docx.md,
  knowledge-base/d-central/core/identity/CivicMesh/TRAIN-002-Track1-Node-Technician-Curriculum-v1-docx.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

Neither source doc is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

*No cross-references detected to/from other docs/*.md files.*

<!-- AUTO-GENERATED RELATED END -->
