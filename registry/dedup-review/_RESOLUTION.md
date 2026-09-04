# Stage 4 Review Queue — Resolution

Every item from `_SUMMARY.md`'s review queue was read and given an actual verdict (not re-run through the heuristic). Results:

## Explicit-language candidates (9 total)

All 9 Step-2 explicit-language candidates flagged by dedup_pass.py were confirmed FALSE POSITIVES after reading the actual matched sentences. The heuristic matched generic single-word titles ("Framework", "{Game Suite}") rather than real cross-document references. Root causes found:
  - Product-description prose using "replaces/supersedes/deprecated" as ordinary English (e.g. "DAO governance replaces corporate control", "Replaces boring memorization").
  - Self-referential `supersedes:` front-matter metadata already present in three D-Central-V1 docs, pointing at "scattered technical documentation across multiple directories" (i.e. superseding unindexed past conversational scatter, not another doc in this corpus) -- not something Stage 4 needs to act on since there is no corresponding artifact here to relocate.
No relocations applied for any of the 9.

## SUPERSEDES verdicts applied (11)

| Canonical (kept) | Superseded (moved to _superseded/) | Reason |
|---|---|---|
| knowledge-base/dcentral-ecosystem/D-Central-v2/D-Central-Edge-Distribution-Computation-Deep-Dive-md-4aa82ecd.md | knowledge-base/dcentral-ecosystem/D-Central-v2/D-Central-Edge-Distribution-Computation-Deep-Dive-md.md | Same title re-uploaded same project 4.5h later, 2.5x content (78648 vs 31970 chars) -- confirmed expansion, not coincidental overlap. |
| knowledge-base/dcentral-ecosystem/D-Central-v2/D-Central-Complete-Fractal-DAO-Governance-Architecture-md-7edde1e7.md | knowledge-base/dcentral-ecosystem/D-Central-v2/D-Central-Complete-Fractal-DAO-Governance-Architecture-md.md | Same title re-uploaded same project 24min later, 2.5x content (77116 vs 30721 chars). |
| knowledge-base/haiti-initiative/Haiti-open-framework/Complete-Enhanced-Open-Source-Cooperative-Resilience-Framework-for-Haiti-md-fa474e23.md | knowledge-base/haiti-initiative/Haiti-open-framework/Complete-Enhanced-Open-Source-Cooperative-Resilience-Framework-for-Haiti-md-d47533bb.md | 4-generation revision chain (see complete-framework-tex.md -> base .md -> d47533bb -> fa474e23), each later upload larger. fa474e23 is final/largest (314367 chars). |
| knowledge-base/haiti-initiative/Haiti-open-framework/Complete-Enhanced-Open-Source-Cooperative-Resilience-Framework-for-Haiti-md-d47533bb.md | knowledge-base/haiti-initiative/Haiti-open-framework/Complete-Enhanced-Open-Source-Cooperative-Resilience-Framework-for-Haiti-md.md | Middle generation of the same revision chain -- see fa474e23 entry. |
| knowledge-base/haiti-initiative/Haiti-open-framework/Complete-Enhanced-Open-Source-Cooperative-Resilience-Framework-for-Haiti-md.md | knowledge-base/haiti-initiative/Haiti-open-framework/complete-framework-tex.md | Earliest generation: a LaTeX source (confirmed via \documentclass header and matching pdftitle) of the same document, uploaded ~2.5h before the .md version begins the chain. |
| knowledge-base/haiti-initiative/Haiti-open-framework/haiti-security-proposal-md.md | knowledge-base/haiti-initiative/Haiti-open-framework/hait-security-proposal-eng-tex.md | Same memo (same recipient, subject, author) -- .tex LaTeX source vs .md prose version uploaded 30s later; treated as the .md prose version being the refined/final upload. |
| knowledge-base/verticals-products/Drone-Zoe/drone-selection-guide2-md-f756780a.md | knowledge-base/verticals-products/Drone-Zoe/drone-selection-guide2-md.md | Same title re-uploaded 6 weeks later, slightly larger (45039 vs 44929 chars). |
| knowledge-base/verticals-products/Drone-Zoe/haiti-drone-cooperative-framework-md-ec202f4d.md | knowledge-base/verticals-products/Drone-Zoe/haiti-drone-cooperative-framework-md.md | Same title re-uploaded 6 weeks later, slightly larger (37524 vs 37340 chars). |
| knowledge-base/verticals-products/Drone-Zoe/haiti-drone-expanded-strategy-md-eb50bcaa.md | knowledge-base/verticals-products/Drone-Zoe/haiti-drone-expanded-strategy-md.md | Same title re-uploaded 6 weeks later, near-identical size (34808 vs 34807 chars, 1.00 Jaccard) -- effectively a mechanical duplicate the content-hash check couldn't catch due to a trivial byte difference. |
| knowledge-base/verticals-products/Drone-Zoe/updated-drone-guide-md-1780e328.md | knowledge-base/verticals-products/Drone-Zoe/updated-drone-guide-md.md | Same title re-uploaded 6 weeks later, near-identical size (22234 vs 22228 chars). |
| knowledge-base/verticals-products/Drone-Zoe/Comprehensive-Democratized-Development-Framework-for-Haiti-md-735f60aa.md | knowledge-base/verticals-products/Drone-Zoe/Comprehensive-Democratized-Development-Framework-for-Haiti-md.md | Same title re-uploaded 13 seconds later, nearly double content (61987 vs 33712 chars) -- confirmed expansion within the same upload session. |

## UNRESOLVED verdicts confirmed (1)

| Doc A | Doc B | Why unresolved |
|---|---|---|
| knowledge-base/verticals-products/VDI-Solutions/D-Central-Ecosystem-Haiti-Integration-Framework-md-53dbf869.md | knowledge-base/verticals-products/VDI-Solutions/D-Central-Ecosystem-Haiti-Integration-Framework-md.md | Identical title and opening TOC, but the LATER upload (53dbf869, 19:36) is less than half the size of the EARLIER one (19:35, 130812 chars) -- contradicts the recency-implies-superset pattern every other pair in this batch fit. No explicit correction language, no engagement evidence either direction. Per DC-DEDUP-STD-001 SS4, this is a genuine 'no basis to prefer one' case, not a failure to resolve. |
