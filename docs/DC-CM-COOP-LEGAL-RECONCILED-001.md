# DC-CM-COOP-LEGAL-RECONCILED-001 — CivicMesh Cooperative Legal Structures, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `civicmesh-cooperative-legal-structures` (2 docs).

## Current understanding

Two parallel Ontario Cooperative Corporations Act bylaws specifications, structurally identical in
purpose (convert a class of platform participants from commercial counterparties into cooperative
stakeholders) but for different member classes: security response providers (LEGAL-GUARD-COOP-001) and
MSSP operators (LEGAL-MSSP-COOP-001).

**Guard Cooperative (incorporated):** membership requires an Ontario security licence, Track 4
certification, E&O insurance, and active dispatch integration, for a $2,500/yr fee. Revenue flows per
dispatch (platform retains a share, dispatches a share to the responding provider, and cooperative
patronage returns a further share to all members pro-rata by dispatch volume — exact percentages left
as `[X]/[Y]/[Z]` placeholders, not yet finalized). D-Central Guard Inc. holds a permanent founding-member
vote and is explicitly framed as a transitional first-responder, expected to become "one competitive
provider among many" as the cooperative grows [LEGAL-GUARD-COOP-001 §1-2].

**MSSP Cooperative (incorporated):** membership requires Gold-tier MSSP certification, for a $5,000/yr
fee, one-member-one-vote governance via an elected Platform Standards Committee, and patronage as a
pro-rata share of net platform fee revenue by nodes under management. D-Central Group Inc. holds the
same kind of permanent, non-dilutive founding-member vote as in the Guard cooperative, and additionally
retains unilateral (non-votable) authority over security architecture, privacy architecture, open-source
licence terms, and DID/VC schema changes — a broader founder-reserved-powers list than the Guard
cooperative states [LEGAL-MSSP-COOP-001 §1, §3].

**Common pattern across both (incorporated):** a $2,500-5,000/yr membership fee, patronage returns tied
to a volume metric specific to that member class (dispatches vs. nodes-under-management), a permanent
non-dilutive D-Central founding-member vote, and framing the cooperative as raising switching costs by
giving competitors a shared economic stake in the platform's growth rather than treating them purely as
commercial partners.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Guard Cooperative membership/eligibility/fee/dispatch revenue model | LEGAL-GUARD-COOP-001 §1 | incorporated |
| D-Central Guard's founding-member role and stated transition plan | LEGAL-GUARD-COOP-001 §2 | incorporated |
| MSSP Cooperative membership/governance/patronage model | LEGAL-MSSP-COOP-001 §1-2 | incorporated |
| D-Central's founding-member vote and reserved unilateral-authority list | LEGAL-MSSP-COOP-001 §3 | incorporated |

## Unresolved tensions

None identified in this pass — the two cooperatives are parallel structures for different member
classes rather than overlapping claims about the same thing, so there is nothing to reconcile between
them. Note (not a cross-doc conflict, but worth flagging): LEGAL-GUARD-COOP-001's patronage-split
percentages are left as unfilled `[X]/[Y]/[Z]` placeholders in the source document itself — this is an
incompleteness in the source, not a disagreement between sources.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/business-legal/CivicMesh/LEGAL-GUARD-COOP-001-CivicMesh-Guard-Cooperative-v1-docx.md`
- `knowledge-base/d-central/business-legal/CivicMesh/LEGAL-MSSP-COOP-001-CivicMesh-MSSP-Cooperative-v1-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/business-legal/CivicMesh/LEGAL-GUARD-COOP-001-CivicMesh-Guard-Cooperative-v1-docx.md,
  knowledge-base/d-central/business-legal/CivicMesh/LEGAL-MSSP-COOP-001-CivicMesh-MSSP-Cooperative-v1-docx.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

Neither source doc is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
