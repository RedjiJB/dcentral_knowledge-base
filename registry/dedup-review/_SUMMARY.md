# Stage 4 Dedup Pass — Summary

**Review queue resolved** — see [_RESOLUTION.md](_RESOLUTION.md). Every explicit-language and
similarity candidate below was read and given an actual verdict: 9 false positives dismissed,
11 confirmed SUPERSEDES relocations applied, 1 confirmed UNRESOLVED (genuinely no basis to prefer
one doc over the other).


Totals: 28 exact-duplicate docs relocated to `_superseded/`, 9 explicit-supersession candidates flagged, 13 similarity candidates flagged for review.

Step 1 was applied automatically (mechanical, per DC-DEDUP-STD-001 §3 step 1). Steps 2-5 are reports only — no verdict is applied without human/agent confirmation, per the standard's authority boundary (this script classifies nothing on its own judgment;
it only surfaces evidence for a later confirmation pass).

- **academic-training**: 5 docs, 0 exact dupes relocated, 1 explicit candidates, 0 similarity candidates → [registry/dedup-review/academic-training.md](registry/dedup-review/academic-training.md)
- **ai-ml-research**: 63 docs, 0 exact dupes relocated, 0 explicit candidates, 0 similarity candidates → [registry/dedup-review/ai-ml-research.md](registry/dedup-review/ai-ml-research.md)
- **dcentral-ecosystem**: 62 docs, 8 exact dupes relocated, 8 explicit candidates, 2 similarity candidates → [registry/dedup-review/dcentral-ecosystem.md](registry/dedup-review/dcentral-ecosystem.md)
- **haiti-initiative**: 19 docs, 1 exact dupes relocated, 0 explicit candidates, 5 similarity candidates → [registry/dedup-review/haiti-initiative.md](registry/dedup-review/haiti-initiative.md)
- **infrastructure-mesh**: 120 docs, 5 exact dupes relocated, 0 explicit candidates, 0 similarity candidates → [registry/dedup-review/infrastructure-mesh.md](registry/dedup-review/infrastructure-mesh.md)
- **other-experimental**: 1 docs, 0 exact dupes relocated, 0 explicit candidates, 0 similarity candidates → [registry/dedup-review/other-experimental.md](registry/dedup-review/other-experimental.md)
- **security-identity**: 91 docs, 8 exact dupes relocated, 0 explicit candidates, 0 similarity candidates → [registry/dedup-review/security-identity.md](registry/dedup-review/security-identity.md)
- **verticals-products**: 67 docs, 6 exact dupes relocated, 0 explicit candidates, 6 similarity candidates → [registry/dedup-review/verticals-products.md](registry/dedup-review/verticals-products.md)
