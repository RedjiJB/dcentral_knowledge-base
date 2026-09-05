# DC-CM-OFFICER-PORTAL-RECONCILED-001 — CivicMesh Officer Portal & Municipal Training, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `civicmesh-officer-portal-municipal-training` (3 docs).

## Current understanding

Three tightly-linked documents: DC-CM-APP-008 is the officer portal product spec; OPS-TM-002 is its
operating SOP; TRAIN-006 is the certification curriculum that trains officers on both. All three are
fully consistent on every shared numeric threshold and badge/reason-code definition.

**Officer Portal product spec (incorporated):** legal admissibility is the stated primary design
constraint — every officer action is immutably logged, and citation issuance is architecturally blocked
without an officer DID signature [§Purpose and Legal Design Constraint]. Three evidence queues by AI
confidence: Fast-Track (≥0.90 confidence AND ≥0.95 ALPR, minimum 3-second timer-locked video playback,
one-tap confirm), Standard Review (0.70-0.89 confidence, full clip + manual violation-type confirmation
+ plate-read confirmation required), and Manual Review (NOC-flagged, mandatory notes + supervisor
countersignature) [§Evidence Queue Design]. A three-state credential-chain badge (GREEN/AMBER/RED) with
a public independent-verification URL [§Credential Verification Display]. A five-step citation workflow
from DID signature through MTO lookup, citation generation, delivery, and revenue attribution
[§Citation Workflow].

**Officer Review Portal SOP (incorporated):** target review times per queue — Fast-Track <4 hours,
Standard <24 hours, Manual <48 hours — with OC Transpo pilot volume expectations (5-20/shift Fast-Track,
2-8/shift Standard, <1/week Manual) [§Daily Review Workflow]. The same three-badge system is restated
with explicit officer instructions: officers must NOT confirm a citation from a RED badge (dismiss with
reason code CREDENTIAL_FAILURE, alert NOC immediately) [§Credential Chain Verification]. Eight named
dismissal reason codes, each tied to a specific AI-model-retraining feedback effect (e.g.,
NOT_A_VIOLATION is a direct negative training signal; CLIP_UNCLEAR triggers a hardware-inspection flag)
[§Dismissal Reason Codes]. A detailed contested-citation legal-package generation procedure, including
cryptographic sealing and named D-Central Forensics expert-witness response times (10 business days
written, 30 days in-person) [§Contested Citation Preparation]. Officer DID credential lifecycle
management: annual expiry with 90/60/30-day reminders, a defined lost-key recovery process (revoke
within 24hr, reissue within 5 business days), and an explicit non-retroactivity rule — an officer's
past reviewed packages remain valid after their credential is revoked on departure [§Officer DID
Credential Management].

**Municipal Partner Certification Curriculum (incorporated):** a 6-hour, $599 course with six modules
mapping directly onto the portal spec and SOP (Evidence Overview, Portal Operation, Dismissal
Discipline, Citation Workflow, Contested Citation Preparation, HTA Compliance/Legal Framework — the last
explicitly built on REG-TM-001's findings, consolidated separately under `trafficmesh-ontario-
regulatory-compliance`) [§1]. Ongoing certification obligations: annual refresher + exam, annual
background recheck, quarterly supervisor review of an officer's dismissal-rate pattern (flagging both
unusually high AND unusually low rates for retraining), and a separate certification module required
per newly-activated violation type [§2].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Legal admissibility design constraint and DID-signature enforcement | DC-CM-APP-008 §Purpose and Legal Design Constraint | incorporated |
| Three-queue evidence design with confidence thresholds | DC-CM-APP-008 §Evidence Queue Design | incorporated (thresholds match SOP exactly) |
| Credential verification badge system | DC-CM-APP-008 §Credential Verification Display | incorporated (restated identically in SOP) |
| Five-step citation workflow | DC-CM-APP-008 §Citation Workflow | incorporated |
| Daily review workflow and target review times by queue | OPS-TM-002 §Daily Review Workflow | incorporated |
| Credential badge officer-action rules (esp. RED = do not confirm) | OPS-TM-002 §Credential Chain Verification | incorporated |
| Eight dismissal reason codes and model-feedback effects | OPS-TM-002 §Dismissal Reason Codes | incorporated |
| Contested-citation legal package generation procedure | OPS-TM-002 §Contested Citation Preparation | incorporated |
| Officer DID credential lifecycle (expiry, loss, departure non-retroactivity) | OPS-TM-002 §Officer DID Credential Management | incorporated |
| 6-module, 6-hour, $599 certification curriculum | TRAIN-006 §1 | incorporated (modules map directly onto portal spec + SOP content) |
| Ongoing certification obligations (annual renewal, background recheck, quarterly dismissal-rate review) | TRAIN-006 §2 | incorporated |

## Unresolved tensions

None identified in this pass — every shared threshold (confidence bands, badge colors, review-time
targets) matches exactly across all three documents, and the curriculum's modules map directly onto the
portal spec's and SOP's actual content rather than introducing independent claims.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/core/identity/CivicMesh/TRAIN-006-Track5-Municipal-Partner-Curriculum-v1-docx.md`
- `knowledge-base/d-central/mesh-services/sensors-mobility/CivicMesh/DC-CM-APP-008-CivicMesh-Officer-Portal-v1-docx.md`
- `knowledge-base/d-central/mesh-services/sensors-mobility/CivicMesh/OPS-TM-002-Officer-Review-Portal-SOP-v1-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/core/identity/CivicMesh/TRAIN-006-Track5-Municipal-Partner-Curriculum-v1-docx.md,
  knowledge-base/d-central/mesh-services/sensors-mobility/CivicMesh/DC-CM-APP-008-CivicMesh-Officer-Portal-v1-docx.md,
  knowledge-base/d-central/mesh-services/sensors-mobility/CivicMesh/OPS-TM-002-Officer-Review-Portal-SOP-v1-docx.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
