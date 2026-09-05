# DC-IHOSE-HARDWARE-BOM-RECONCILED-001 — OpenVision (IHOSE) Hardware Bill of Materials, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `ihose-hardware-bom` (4 docs).

## Current understanding

Four hardware/procurement documents for the OpenVision Platform, at increasing levels of BOM detail:
a philosophy-and-tiers overview (02-Hardware-Specifications.docx), a full line-item enterprise/SMB/
household BOM aimed at procurement/finance (05-Hardware-Specifications.md), and two near-identical
detailed enterprise BOMs (HARDWARE_BOM.md and bom-enterprise.md) that agree with each other closely but
diverge from 05-Hardware-Specifications.md on the same configuration's totals.

**02-Hardware-Specifications.docx (incorporated):** frames an "open vs. pragmatic proprietary"
philosophy — RISC-V/Orange Pi/OpenIPC/OpenWrt where open hardware is viable, NVIDIA Jetson and
enterprise HDDs where performance or reliability justifies proprietary components [Hardware
Philosophy]. Gives its own three-tier BOM at coarser granularity than the other three docs: Small
(5-20 cameras, two configs at $940 and $2,690), Medium (50-100 cameras, $2,950/site + $3,650 central =
$15,450 for 4 sites/80 cameras), and Large Enterprise (500-1000 cameras/25 sites, a single $332,000
total) [Small/Medium/Large Deployment]. This large-enterprise figure uses a different site count (25,
not 20) and coarser line items than the other three docs' enterprise BOMs, so it is not directly
comparable to their $213K-$772K range.

**05-Hardware-Specifications.md (incorporated):** a full line-item BOM for Enterprise (500 cameras/20
sites), SMB (10-50 cameras), and Household (1-5 cameras) tiers, aimed at procurement/finance readers.
Enterprise Central Cloud totals **$131,910** (control plane + worker + Ceph storage + PostgreSQL HA +
networking, with a $57,300 networking subtotal including UPS and SFP+/DAC cabling). Three edge
configurations (Budget/Standard/Premium) combine with this central total for grand totals of
**$226,410 / $294,110 / $772,910** [Enterprise Deployment BOM]. Gives its own SMB ($11,930) and
Household ($559) BOMs, a vendor matrix, lead times, and a 3-year TCO/cost-comparison section stating
OpenVision Standard at $819,110 vs. Genetec at $1,015,000 (19% savings) [Cost Comparison].

**HARDWARE_BOM.md and bom-enterprise.md (incorporated together, near-identical):** these two documents
give matching, more granular enterprise BOMs. Central Cloud totals **$118,830** (the same node
categories as 05-Hardware-Specifications.md, but a $41,000 networking subtotal rather than $57,300 —
fewer/less-itemized cabling and UPS line items). Combined with the same three edge configurations,
grand totals are **$213,330 / $294,430 / $733,830** for Budget/Standard/Premium. Both give an identical
3-year TCO analysis: hardware $339,430 (with year-over-year replacement costs), personnel $480,000,
optional support $90,000, for an on-premise 3-year TCO of **$819,430** vs. a stated Genetec/Milestone
comparison of $890,000 — a **$70,570 (8%)** savings [Cost Breakdown, 3-Year TCO Analysis]. HARDWARE_BOM.md
additionally covers SMB (on-premise $6,800 vs. cloud 3-year $14,780) and Household ($180-$800 across
three tiers) BOMs, plus a vendor directory and lead-time table matching 05-Hardware-Specifications.md's
structure closely.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Open-vs-proprietary hardware philosophy | 02-Hardware-Specifications.docx, Hardware Philosophy | incorporated |
| Small/Medium/Large coarse-grained BOM (different site count for Large tier) | 02-Hardware-Specifications.docx | incorporated (not directly comparable to the other 3 docs' enterprise figures — see tension below) |
| RISC-V/ARM/AI-accelerator/OpenIPC open-hardware component recommendations | 02-Hardware-Specifications.docx, Open Hardware Recommendations | incorporated (consistent with the same recommendations repeated in the other 3 docs) |
| Enterprise BOM detail, Central Cloud $131,910 total, 3 edge configs | 05-Hardware-Specifications.md, Enterprise Deployment BOM | incorporated — see tension below |
| SMB and Household BOMs (05-doc) | 05-Hardware-Specifications.md | incorporated |
| TCO vs. Genetec ($819,110 vs $1,015,000, 19% savings) | 05-Hardware-Specifications.md, Cost Comparison | incorporated — see tension below |
| Enterprise BOM detail, Central Cloud $118,830 total, 3 edge configs | HARDWARE_BOM.md, bom-enterprise.md | incorporated — see tension below |
| SMB and Household BOMs (HARDWARE_BOM.md) | HARDWARE_BOM.md | incorporated |
| TCO vs. Genetec/Milestone ($819,430 vs $890,000, $70,570 savings) | HARDWARE_BOM.md, bom-enterprise.md, 3-Year TCO Analysis | incorporated — see tension below |
| Vendor directories and lead-time tables | 05-Hardware-Specifications.md, HARDWARE_BOM.md | incorporated (consistent between the two) |

## Unresolved tensions

**Two documents claiming to detail the identical Enterprise Standard configuration (500 cameras, 20
sites) give different Central Cloud subtotals and different grand totals, with no cross-reference
reconciling them.** 05-Hardware-Specifications.md computes Central Cloud at $131,910 (Standard grand
total $294,110), while HARDWARE_BOM.md and bom-enterprise.md (which agree with each other) compute
Central Cloud at $118,830 (Standard grand total $294,430). The line-item categories are nearly
identical (same node counts, same CPU/RAM/storage specs per category), but 05-Hardware-Specifications.md's
networking subtotal ($57,300, including a 10KVA UPS pair and itemized SFP+/DAC cabling) is larger than
the other two documents' networking subtotal ($41,000, without the UPS or as much cabling detail).
Attempted reconciliation: none of the three documents states that one figure supersedes another or
that the difference is an intentional UPS-inclusive vs. UPS-exclusive framing — this reads as three
independently-maintained versions of the same BOM that drifted rather than a stated methodology
difference. The 3-year TCO comparisons compound this: 05-Hardware-Specifications.md states $819,110
vs. Genetec's $1,015,000 (19% savings), while HARDWARE_BOM.md/bom-enterprise.md state a very close but
not identical $819,430 vs. a different commercial baseline of $890,000 (8% savings) — a third TCO
framing ($774,430 vs $1,120,000, 31%) appears in the sibling
[DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001](DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001.md), which flags
the same unreconciled-figures pattern independently. Left unresolved rather than picking one figure as
authoritative.

**02-Hardware-Specifications.docx's Large Enterprise tier is not directly comparable to the other three
documents' Enterprise tier**, since it assumes 25 sites (not 20) and a materially different hardware mix
(4x NVIDIA A100 GPU nodes, a flat $332,000 total with far less line-item granularity). This isn't
treated as a contradiction — it reads as an earlier, coarser-grained pass superseded in practice by the
other three documents' much more detailed BOMs — but no document states this supersession explicitly.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/hardware/sensing-planes/IHOSE/02-Hardware-Specifications-docx.md`
- `knowledge-base/d-central/hardware/sensing-planes/IHOSE/05-Hardware-Specifications-md.md`
- `knowledge-base/d-central/hardware/sensing-planes/IHOSE/HARDWARE-BOM-md.md`
- `knowledge-base/d-central/hardware/sensing-planes/IHOSE/bom-enterprise-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/hardware/sensing-planes/IHOSE/02-Hardware-Specifications-docx.md,
  knowledge-base/d-central/hardware/sensing-planes/IHOSE/05-Hardware-Specifications-md.md,
  knowledge-base/d-central/hardware/sensing-planes/IHOSE/HARDWARE-BOM-md.md,
  knowledge-base/d-central/hardware/sensing-planes/IHOSE/bom-enterprise-md.md,
]
reconciled_against: [DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001.md (independently flags a third, unreconciled TCO figure)]
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
