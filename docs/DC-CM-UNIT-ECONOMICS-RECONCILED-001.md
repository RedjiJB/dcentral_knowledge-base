# DC-CM-UNIT-ECONOMICS-RECONCILED-001 — CivicMesh Financial Unit Economics, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `civicmesh-financial-unit-economics` (2 docs).

## Current understanding

FIN-CM-002 models per-node, per-community, and per-municipal-contract economics across the whole
CivicMesh value chain; FIN-CM-005 zooms into one link of that chain — the MSSP operator's own P&L —
in more detail, and is explicitly cross-referenced from FIN-CM-002.

**Per-node cost/revenue baseline (incorporated):** node hardware+install runs $950-3,000 one-time
(amortized $26-83/month over a 3-year life), monthly operating cost $26-53/node, and monthly MSSP
revenue $18-88/node, giving an MSSP break-even of 6-18 months per node and an NPV of $400-2,200/node
over 3 years at a 15% discount rate [FIN-CM-002 §1].

**Per-community economics (incorporated):** three reference sizes (20-node small HOA, 60-node medium
condo, 150-node large campus), each with hardware cost, monthly platform fee, monthly citation-revenue
community share (60%), and an estimated 4-12 month hardware payback period across all three sizes
[FIN-CM-002 §2].

**Municipal contract economics (incorporated):** a three-phase revenue split (65% municipal / 20%
MSSP / 15% CCSC-community) scaling from a 30-vehicle OC Transpo pilot ($216K-720K/yr gross citation
revenue) through a 200-vehicle Phase 2A to an 800+-node full Ottawa deployment ($5.76M-19.2M/yr gross)
[FIN-CM-002 §3].

**Platform-wide break-even thresholds (incorporated):** D-Central Shield (the founding MSSP) reaches
break-even at an estimated 150-200 nodes under management, explicitly noting the 30-node OC Transpo
pilot alone does not reach it; CivicMesh Inc. (the platform layer) reaches break-even at roughly 3
active MSSP operators + 1 insurance subscriber + 500 active nodes; CCSC's patronage operations become
self-sustaining above a $15,000/month citation-revenue-share threshold [FIN-CM-002 §4].

**MSSP partner P&L detail (incorporated):** a five-stream revenue breakdown (citation share, NOC fees,
installation fees, cooperative patronage, training-certification pass-through) with per-stream margin
ranges, and an illustrative scale table across 50/200/500/1,000-node MSSP portfolios showing
profitability turning positive between the 50- and 200-node tiers [FIN-CM-005 §1-2]. A worked patronage
example (a 200-of-1,000-node MSSP receiving 20% of a $50,000/yr cooperative pool = $10,000/yr in
addition to direct revenue) illustrates FIN-CM-002's cooperative-patronage-sustainability claim at the
individual-MSSP level rather than the CCSC-aggregate level [FIN-CM-005 §3].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Per-node hardware/operating cost and revenue baseline | FIN-CM-002 §1 | incorporated |
| Per-community (HOA/condo/campus) economics | FIN-CM-002 §2 | incorporated |
| Municipal contract phased economics (OC Transpo → full Ottawa) | FIN-CM-002 §3 | incorporated |
| D-Central Shield / CivicMesh Inc. / CCSC break-even thresholds | FIN-CM-002 §4 | incorporated — see tension below on the MSSP break-even figure |
| MSSP five-stream revenue model with margin ranges | FIN-CM-005 §1 | incorporated |
| MSSP scale illustration (50/200/500/1,000 nodes) | FIN-CM-005 §2 | incorporated — states a ~100-node break-even, see tension below |
| Individual-MSSP cooperative patronage worked example | FIN-CM-005 §3 | incorporated |

## Unresolved tensions

**MSSP break-even node count is stated two different ways.** FIN-CM-002 §4 states D-Central Shield
(the founding MSSP) breaks even at an estimated **150-200 nodes** under management. FIN-CM-005 §2's
illustrative scale table states a generic MSSP break-even at **~100 nodes**. Attempted reconciliation:
FIN-CM-002's figure is stated for a specific company (D-Central Shield) while FIN-CM-005's is an
"illustrative example" not tied to a named operator, so these could be a specific-case-vs-generic-model
difference rather than a true contradiction — but neither document states that relationship explicitly,
and the numbers aren't close enough (100 vs. 150-200) to assume they're describing the same curve with
rounding. Left as an open discrepancy rather than resolved either way.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/core/economics/CivicMesh/FIN-CM-002-CivicMesh-Unit-Economics-Model-v1-docx.md`
- `knowledge-base/d-central/core/economics/CivicMesh/FIN-CM-005-MSSP-Cooperative-Revenue-Model-v1-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/core/economics/CivicMesh/FIN-CM-002-CivicMesh-Unit-Economics-Model-v1-docx.md,
  knowledge-base/d-central/core/economics/CivicMesh/FIN-CM-005-MSSP-Cooperative-Revenue-Model-v1-docx.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

Neither source doc is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
