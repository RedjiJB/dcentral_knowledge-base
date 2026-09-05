# DC-IHOSE-BUSINESS-SUMMARIES-RECONCILED-001 — OpenVision (IHOSE) Business Summaries, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `ihose-business-summaries` (5 docs).

## Current understanding

Five business-summary documents for the OpenVision Platform: a 21-slide presentation deck (already
fully detailed in the sibling [DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001](DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001.md)),
two documentation-package overview/index documents, and two independently-drafted executive summaries.
All five restate the same core business case at different levels of detail, and — consistent with the
pattern already flagged in two sibling consolidations — none of the TCO/savings figures these
independent drafts state agree with each other.

**Business Presentation Deck (incorporated by reference):** this document's full content (21 slides,
appendices, presentation tips) is already detailed in the sibling
[DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001](DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001.md), which also
documents its internal 70%-headline-vs-31%-table inconsistency. Not re-derived here.

**Delivery Summary (incorporated):** a meta-document inventorying the full 181-page, 6-document
OpenVision documentation package (README, Executive Summary, Business Presentation, Technical
Architecture, Deployment Guide, Hardware BOM) with per-document page counts, audiences, and content
summaries [Document Inventory]. Restates the Business Presentation's $774,430 vs. $1,120,000 (31%,
$345,570) TCO figures as the package's "Financial Highlights," alongside a $12,400 (54%) SMB savings
figure [Financial Highlights]. A documentation-statistics table (181 pages, ~90,000 words, 15+ diagrams,
50+ code examples, 80+ tables) and quality/completeness checklists close the document.

**Project Summary (incorporated):** a technical-framework overview describing the same platform's file
structure, deployment configurations, module SDK, hardware BOM, and installation automation in prose
form [What Has Been Created]. Its own cost-comparison figure is **$70,000+ savings** over three years
versus Genetec/Milestone [Cost Analysis] — a third, smaller savings figure than either the Business
Presentation's $345,570 or the figures the two executive summaries below state, and one that matches
the sibling IHOSE Quickstart consolidation's own $70,570 figure rather than the Business Presentation's.
Gives its own 5-phase, 6-12-month implementation roadmap (proof of concept → MVP → edge deployment →
production hardening → enterprise features) and a distinct four-model business-model list matching the
other summaries' models in substance.

**01-Executive-Summary.md (incorporated):** an independently-drafted executive summary stating the
OpenVision 3-year TCO at **$820,000** against a $890,000 Genetec figure — implying roughly a
**$70,000/8%** savings, consistent with the Project Summary's figure and the sibling Quickstart
consolidation's $70,570 figure, but not with the Business Presentation's $345,570/31% or the Delivery
Summary's restatement of it. Gives its own investment ask ($850K over 2 years across 3 phases), its own
revenue projections (Year 3: $16.95M, materially higher than the Business Presentation's $5.2M Year-3
figure), and its own go/no-go decision-criteria framework recommending "PROCEED."

**EXECUTIVE-SUMMARY.md (incorporated):** a second, separately-authored executive summary (different
`doc_uuid` and file path from the one above, despite the near-identical title) that instead uses the
Business Presentation's own figures verbatim — $774,430 vs. $1,120,000, 31%/$345,570 savings — while
its own headline claims **"70% cost savings"** and **"50-70%"** in its Decision Matrix, repeating the
same internal 31%-table-vs-70%-headline inconsistency already flagged in the Business Presentation
sibling consolidation. Its revenue projections ($724K/$2.19M/$5.2M across Years 1-3) match the Business
Presentation exactly, unlike the other executive summary's much higher $16.95M Year-3 figure.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Full 21-slide deck content | Business Presentation Deck | incorporated by reference — fully detailed in sibling [DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001](DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001.md) |
| Documentation package inventory (6 docs, 181 pages) | Delivery Summary, Document Inventory | incorporated |
| Restated $774,430/$1,120,000/31% TCO figures | Delivery Summary, Financial Highlights | incorporated — see tension below |
| Technical framework overview, file structure, module SDK | Project Summary, What Has Been Created | incorporated |
| $70,000+ savings figure and 5-phase roadmap | Project Summary, Cost Analysis / Implementation Roadmap | incorporated — see tension below (matches sibling Quickstart consolidation's $70,570, not the Business Presentation's $345,570) |
| $820K vs $890K TCO, $850K investment ask, $16.95M Year-3 revenue | 01-Executive-Summary.md | incorporated — see tension below |
| $774,430/$1,120,000/31% TCO restated, "70%" headline claim, $5.2M Year-3 revenue | EXECUTIVE-SUMMARY.md | incorporated — repeats the Business Presentation's own internal 31%-vs-70% inconsistency |

## Unresolved tensions

**This topic's five documents contain at least four distinct, mutually unreconciled TCO/savings figures
for the identical 500-camera, 3-year OpenVision-vs-Genetec comparison**, extending the pattern already
flagged in the sibling [DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001](DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001.md)
and [DC-IHOSE-HARDWARE-BOM-RECONCILED-001](DC-IHOSE-HARDWARE-BOM-RECONCILED-001.md) consolidations: (1)
$774,430 vs. $1,120,000 (31%, $345,570) — the Business Presentation's and EXECUTIVE-SUMMARY.md's figure;
(2) $820,000 vs. $890,000 (~8%, ~$70,000) — 01-Executive-Summary.md's figure, matching the separately-
flagged $819,430/$819,110/$70,570 cluster from the Hardware BOM and Quickstart consolidations; (3) a
generic "$70,000+ savings" in the Project Summary, consistent with cluster (2); and (4) the recurring
"70%" headline claim (in both the Business Presentation and EXECUTIVE-SUMMARY.md) which doesn't match
either cluster's own percentage (31% or 8%). None of the five documents cross-references or reconciles
these figures. Left unresolved rather than picking one as authoritative, consistent with the prior
consolidations' treatment of the same underlying pattern.

**The two "Executive Summary" documents are independently-authored duplicates with materially different
financial projections** (Year 3 revenue $16.95M vs. $5.2M; investment ask $850K vs. an implicit $790K
Year-1 cost figure) despite near-identical titles, structure, and section headings. Neither states that
it supersedes or updates the other. This is a stronger candidate for a formal Stage 4 dedup decision
(which of the two, if either, is the "current" executive summary) than for Consolidator-level
reconciliation, since the two documents' narratives don't merely differ in numbers — they propose
different investment asks and different growth trajectories for what is framed as the same business
plan.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/business-legal/IHOSE/BUSINESS-PRESENTATION-md.md`
- `knowledge-base/d-central/meta/status-tracking/IHOSE/DELIVERY-SUMMARY-md.md`
- `knowledge-base/d-central/meta/status-tracking/IHOSE/PROJECT-SUMMARY-md.md`
- `knowledge-base/d-central/security/IHOSE/01-Executive-Summary-md.md`
- `knowledge-base/d-central/security/IHOSE/EXECUTIVE-SUMMARY-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/business-legal/IHOSE/BUSINESS-PRESENTATION-md.md,
  knowledge-base/d-central/meta/status-tracking/IHOSE/DELIVERY-SUMMARY-md.md,
  knowledge-base/d-central/meta/status-tracking/IHOSE/PROJECT-SUMMARY-md.md,
  knowledge-base/d-central/security/IHOSE/01-Executive-Summary-md.md,
  knowledge-base/d-central/security/IHOSE/EXECUTIVE-SUMMARY-md.md,
]
reconciled_against: [DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001.md (sibling covering the Business Presentation Deck in full, and its own 70%-vs-31% tension), DC-IHOSE-HARDWARE-BOM-RECONCILED-001.md (independently flags the same $70K/$819K TCO cluster)]
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
