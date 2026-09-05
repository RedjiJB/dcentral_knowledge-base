# DC-CM-AUDIT-TRANSPARENCY-RECONCILED-001 — CivicMesh Governance Audit & Transparency, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `civicmesh-governance-audit-transparency` (2 docs).

## Current understanding

DC-CM-GOV-002 specifies the annual independent-audit process; DC-CM-GOV-003 specifies the mandatory
report that publishes the audit's results and other governance metrics. The two are explicitly
cross-referenced and consistent on timing (both anchor to "30 days before the CCSC AGM").

**Audit process (incorporated):** an annual audit, run within 6 months of fiscal year end, scoped to
six areas (data-flow architecture conformance, federation-event authorization, retention compliance,
consent-record validity, AI model false-positive/dismissal rates, and privacy-complaint resolution),
conducted by an independent auditor the CCSC board selects from a pre-approved list — D-Central is
explicitly excluded from auditor selection and cannot be the sole approved auditor
[DC-CM-GOV-002 §1]. Individual members can request their own personal audit record (fulfilled within
30 days); 20%+ of members can petition for an extraordinary audit at any time, which D-Central must
support within 10 business days [DC-CM-GOV-002 §2].

**Transparency report (incorporated):** a mandatory 8-section annual report — network overview,
incident volume, revenue distribution, law-enforcement access requests (broken out by legal-authority
type), privacy performance, AI performance, cooperative governance activity, and corrective actions
from prior audit findings — published both as a member-facing PDF and a machine-readable JSON, with an
explicit anti-redaction rule: every field must be populated even if the value is zero, since omission
is treated as equivalent to concealment [DC-CM-GOV-003 §1-2].

**How the two fit together:** the audit (DC-CM-GOV-002) is the verification process; the transparency
report (DC-CM-GOV-003) is the standing publication that makes the audit's findings and the platform's
ongoing metrics visible to members and the public on a fixed cadence — DC-CM-GOV-003's "Corrective
Actions" section is explicitly sourced from the prior year's audit report.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Annual audit scope, auditor-selection independence, access rights | DC-CM-GOV-002 §1 | incorporated |
| Individual and collective (20%-petition) audit rights | DC-CM-GOV-002 §2 | incorporated |
| Mandatory 8-section transparency report structure | DC-CM-GOV-003 §1 | incorporated |
| Publication format, timing, and anti-redaction policy | DC-CM-GOV-003 §2 | incorporated |

## Unresolved tensions

None identified in this pass — the two documents describe complementary halves of one governance
cycle (audit → report) with consistent timing and no contradicting claims.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/core/governance/CivicMesh/DC-CM-GOV-002-Community-Audit-Framework-v1-docx.md`
- `knowledge-base/d-central/core/governance/CivicMesh/DC-CM-GOV-003-Transparency-Reporting-Standard-v1-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/core/governance/CivicMesh/DC-CM-GOV-002-Community-Audit-Framework-v1-docx.md,
  knowledge-base/d-central/core/governance/CivicMesh/DC-CM-GOV-003-Transparency-Reporting-Standard-v1-docx.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

Neither source doc is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
