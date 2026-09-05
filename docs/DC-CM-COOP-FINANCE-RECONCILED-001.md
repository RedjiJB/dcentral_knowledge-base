# DC-CM-COOP-FINANCE-RECONCILED-001 — CivicMesh Cooperative Finance & Regulatory Compliance, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `civicmesh-cooperative-finance-regulatory` (2 docs).

## Current understanding

REG-COOP-001 covers the regulatory compliance obligations of D-Central's Ontario cooperatives (CCSC and
others); FIN-COOP-001 covers the specific patronage-distribution formula and payout mechanics for CCSC.
Both explicitly cross-reference each other.

**Regulatory compliance (incorporated):** Ontario Cooperative Corporations Act obligations — AGM within
6 months of fiscal year end, audited/reviewed financial statements, a DID-keyed member register, a
Canadian-resident director majority, and dissolution surplus distributed to members rather than retained
[REG-COOP-001 §1]. CRA treats patronage dividends as deductible to the cooperative and taxable income to
members, with T4A slips required above $500/year [REG-COOP-001 §2]. DECU's path to become a licensed
Ontario credit union requires 150 founding members, $250,000 in member shares, FSRA approval, and a
realistic 12-24 month timeline, treated as a Year 3-5 initiative — until then D-Credit is managed as a
cooperative accounting instrument by CivicMesh Inc. directly, deliberately structured to avoid securities
classification [REG-COOP-001 §3].

**Patronage distribution mechanics (incorporated):** a per-revenue-source formula (e.g., 80% of
TrafficMesh citation revenue to contributing node owners, 20% retained by CCSC; 100% pass-through for
government stipends and insurance rebates) [FIN-COOP-001 §1]; four payout options (CAD direct deposit,
D-Credit at par, platform-fee credit, transit credit) each with a monthly distribution schedule
[FIN-COOP-001 §2-3]; and a 5% D-Credit velocity bonus for spending patronage within the ecosystem, framed
as the cooperative's core economic flywheel [FIN-COOP-001 §4].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Ontario CCA compliance obligations (AGM, member register, director residency, dissolution) | REG-COOP-001 §1 | incorporated |
| CRA patronage/T4A tax treatment | REG-COOP-001 §2 | incorporated |
| DECU regulatory path and interim D-Credit structure | REG-COOP-001 §3 | incorporated |
| Per-revenue-source patronage distribution formula | FIN-COOP-001 §1 | incorporated |
| Payout options and distribution schedule | FIN-COOP-001 §2-3 | incorporated |
| D-Credit velocity bonus (5%) | FIN-COOP-001 §4 | incorporated |

## Unresolved tensions

**D-Credit tax treatment on receipt is stated two different ways by the two sources.** REG-COOP-001 §3
states D-Credit "should be structured to be received as D-Credit and not taxable until converted to CAD."
FIN-COOP-001 §2's payout-options table states the opposite: "D-Credit received as patronage should be
taxable on receipt at par value." Attempted reconciliation: both documents separately flag that "CRA has
not issued specific guidance on cooperative digital currencies" and that a legal opinion is required
before public launch — so this isn't two confident, contradictory legal conclusions so much as two
different provisional guesses at an actually-unresolved question upstream. Left as an open tension rather
than picked between, since neither source has the authority to resolve it and picking one would
misrepresent the state of legal certainty to a reader relying on this document.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/business-legal/CivicMesh/REG-COOP-001-Cooperative-Regulatory-Compliance-Matrix-v1-docx.md`
- `knowledge-base/d-central/core/economics/CivicMesh/FIN-COOP-001-Cooperative-Patronage-Distribution-Model-v1-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/business-legal/CivicMesh/REG-COOP-001-Cooperative-Regulatory-Compliance-Matrix-v1-docx.md,
  knowledge-base/d-central/core/economics/CivicMesh/FIN-COOP-001-Cooperative-Patronage-Distribution-Model-v1-docx.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

Neither source doc is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
