# DC-CM-TM-GRANT-FUNDING-RECONCILED-001 — CivicMesh/TrafficMesh IRAP & SR&ED Funding Documentation, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `civicmesh-trafficmesh-grant-funding-applications` (3 docs).

## Current understanding

Three funding/tax-documentation instruments: IRAP-TM-001 is the TrafficMesh-specific IRAP grant
application (explicitly a companion to a separate CivicMesh-platform IRAP-CM-001, not among these three
docs); SRED-CM-001 is the CivicMesh-platform SR&ED evidence ledger and daily documentation system;
SRED-TM-001 is its TrafficMesh-specific companion ledger. All three explicitly cross-reference each
other and are internally consistent.

**IRAP-TM-001 (incorporated):** four TrafficMesh-specific technical uncertainties justifying IRAP
funding — Tier 2 seasonal node operation at -30°C on snowplows/sweepers, continuous digital-twin update
fusion from 200+ moving nodes, evidence-package legal-admissibility design against an HTA standard that
doesn't yet exist, and a 5-minute universal-vehicle contractor install kit [§1]. A 6-phase, 17-month
milestone plan from officer-portal-with-simulated-evidence (Month 3) through live digital-twin
pothole-validation against 311 records (Month 17) [§2]. Five named public-safety dual-use
justifications (municipal enforcement, ALPR/police integration, Amber Alert search-network conversion,
hit-and-run investigation support, emergency situational awareness) [§3]. The IRAP/SR&ED interaction
rule: IRAP funds 80% of eligible salary, SR&ED then refunds a portion of the *remaining* 20% (both
programs combined cover ~88% of eligible R&D salary cost) [§4].

**SRED-CM-001 (incorporated):** establishes the CivicMesh SR&ED documentation system as a "Day 1
non-negotiable" — GitHub org, Linear workspace with SR&ED tags, and a Technical Decision Log must exist
before any code is written, because undocumented R&D days are unrecoverable evidence [Executive
Summary]. The three-part CRA eligibility test (technological advancement / uncertainty / systematic
investigation) is applied to CivicMesh's specific work [§1]. An eligible/ineligible activity table
(edge AI, ALPR optimization, federation protocol, DID/VC design = eligible; officer-portal UI, business
development, routine API integration = not eligible) [§2]. Detailed documentation-habit specifications:
commit-message standards contrasting bad ("Fix null pointer") vs. good ("Resolve null pointer... third
approach tried — previous two caused unacceptable latency") examples, Linear SR&ED-eligibility tagging
fields, a Technical Decision Log template, and daily time-tracking requirements — explicitly noting CRA
does not accept retroactive time reconstruction [§3]. A worked financial summary table showing $180,000
total eligible-category spend reducing to $54,000 net SR&ED-eligible after the 80% IRAP offset, yielding
a $35,100 combined federal+Ontario refund [§4]. A 6-step annual claim-filing process from year-end
documentation export through CRA refund (typically 60-120 days after filing) [§5].

**SRED-TM-001 (incorporated):** the same documentation discipline applied to seven TrafficMesh-specific
R&D activities (YOLOv8 violation-detection training, cold-weather ALPR optimization, OBD-II telemetry
speed-fusion, digital-twin update algorithm, IP67 -40°C enclosure design, evidence chain-of-custody
cryptographic pipeline, and the 5-minute universal contractor-kit design), each with its own required
documentation type and eligible-expenditure category [§1]. TrafficMesh-specific commit-message examples
extend SRED-CM-001's general standard with hardware/model-training context (e.g., a YOLOv8 training-run
commit citing exact mAP scores and the specific failure mode driving the next iteration) [§2]. A
hardware-materials eligibility table distinguishes R&D-prototype hardware (Jetson Orin dev kits, camera
modules, secure-element boards — eligible as consumed materials) from production deployment hardware
(not eligible, must be depreciated as capital) [§3].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| TrafficMesh technical uncertainties and IRAP milestone plan | IRAP-TM-001 §1-2 | incorporated |
| Public-safety dual-use justification | IRAP-TM-001 §3 | incorporated |
| IRAP/SR&ED combined-funding interaction rule | IRAP-TM-001 §4 | incorporated |
| CivicMesh SR&ED "Day 1" documentation system and CRA eligibility test | SRED-CM-001 Executive Summary, §1 | incorporated |
| CivicMesh eligible/ineligible activity determinations | SRED-CM-001 §2 | incorporated |
| Documentation habits (commit standards, Linear tagging, Technical Decision Log, time tracking) | SRED-CM-001 §3 | incorporated |
| CivicMesh financial summary template and annual claim process | SRED-CM-001 §4-5 | incorporated |
| TrafficMesh 7-activity SR&ED register | SRED-TM-001 §1 | incorporated |
| TrafficMesh-specific commit message standards | SRED-TM-001 §2 | incorporated (extends SRED-CM-001's general standard) |
| Hardware R&D materials eligibility table | SRED-TM-001 §3 | incorporated |

## Unresolved tensions

None identified in this pass — all three documents are explicitly designed as companion pieces (IRAP-
TM-001 to a separate CivicMesh IRAP application; SRED-TM-001 to SRED-CM-001), and the IRAP/SR&ED
interaction rule stated in IRAP-TM-001 is consistent with the financial modeling in SRED-CM-001's
worked example.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/business-legal/CivicMesh/IRAP-TM-001-NRC-IRAP-Application-TrafficMesh-v1-docx.md`
- `knowledge-base/d-central/business-legal/CivicMesh/SRED-CM-001-SR-ED-Project-Ledger-CivicMesh-v1-docx.md`
- `knowledge-base/d-central/business-legal/CivicMesh/SRED-TM-001-SR-ED-Project-Ledger-TrafficMesh-v1-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/business-legal/CivicMesh/IRAP-TM-001-NRC-IRAP-Application-TrafficMesh-v1-docx.md,
  knowledge-base/d-central/business-legal/CivicMesh/SRED-CM-001-SR-ED-Project-Ledger-CivicMesh-v1-docx.md,
  knowledge-base/d-central/business-legal/CivicMesh/SRED-TM-001-SR-ED-Project-Ledger-TrafficMesh-v1-docx.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
