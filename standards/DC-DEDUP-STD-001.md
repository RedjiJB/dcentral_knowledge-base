# DC-DEDUP-STD-001: Standard for the Stage 2.5 Dedup/Status Agent

## 0. Purpose and boundary

This agent is the sole authority for assigning artifact status (`canonical`, `superseded`, `merged`) and for the physical `_superseded/` relocation. It never synthesizes new content — that's the Consolidator's job ([[DC-CONSOLIDATOR-STD-001]]) — and it never invents a canonical answer where none of the sources agree; it only classifies relationships between existing artifacts and writes the graph edges that record those relationships.

## 1. Trigger conditions

Runs against pairs/clusters of artifacts that share a topic node or doc-ID prefix, specifically:

- Any two artifacts newly linked to the same topic node since the last dedup pass
- Any artifact revision (new version of an existing doc-ID)
- On-demand, when a human or the classification pass (Stage 3) flags suspected overlap

A pair is not re-evaluated if a prior dedup decision already exists for that exact pair and neither artifact has changed since.

## 2. The four possible verdicts (exhaustive — every evaluated pair lands in exactly one)

1. **SUPERSEDES** — B's content is factually/architecturally replaced by A; B is no longer a valid standalone reference for current work.
2. **MERGED_FROM** — A synthesizes and preserves content from B and C; B and C remain individually inspectable for dropped detail but are not independently canonical.
3. **DISTINCT** — A and B cover genuinely different scope despite surface similarity; both stay canonical, no edge beyond `DISCUSSES` to the shared topic.
4. **UNRESOLVED** — genuine factual conflict between A and B with no basis to prefer one; both stay canonical, flagged for human review. This is the escape hatch that keeps the agent from forcing a verdict it can't support — never silently defaults to SUPERSEDES just because one doc is newer.

## 3. Decision procedure (in order — later steps only run if earlier ones don't resolve it)

1. **Identity check**: same content hash → not a dedup case, just a duplicate file; dedupe mechanically, log, skip remaining steps.
2. **Explicit supersession check**: does either artifact contain explicit language correcting/replacing the other? If yes → SUPERSEDES, cite the explicit language as evidence. Strongest, least-inferential signal — check first.
3. **Content overlap classification**: extract claims from both (same granularity discipline as [[DC-CONSOLIDATOR-STD-001]] §3) and compare:
   - B's claims are a subset of A's, none contradicted/dropped without replacement → SUPERSEDES.
   - A's claims are drawn from both B and C with none contradicted, just combined → MERGED_FROM.
   - Claim sets barely overlap beyond shared vocabulary → DISTINCT.
   - Claim sets overlap AND at least one pair is genuinely incompatible → go to step 4.
4. **Reconciliation attempt** (only reached on apparent conflict): check whether the conflict is actually a scope/layer difference. If reconciled, verdict is DISTINCT with a `DISCUSSES` note explaining the layering.
5. **Recency-with-engagement check** (only reached on true unresolved conflict): does the later artifact show evidence it engaged with the earlier claim specifically? If yes → SUPERSEDES, citing the engagement. If it simply never mentions the earlier claim → silence, not correction → UNRESOLVED.

## 4. What "no basis to prefer one" actually means (calibration)

UNRESOLVED requires that steps 2-5 were all attempted and none produced a verdict. Disqualifying shortcuts:
- "A is longer/more detailed" is not a basis.
- "A is more recent" alone is not a basis — recency requires engagement (step 5).
- "A came from a more important conversation" is not a basis.

## 5. Physical relocation rules

- **SUPERSEDES**: superseded artifact moves to `_superseded/` in its current folder, `_superseded/_INDEX.md` gets an entry with the reason and a pointer to the replacement.
- **MERGED_FROM**: sources do NOT move — merge preserves standalone inspectability of dropped detail.
- **DISTINCT / UNRESOLVED**: no relocation. UNRESOLVED gets a `status: disputed` flag so it surfaces in a human review queue rather than sitting as two canonical docs that quietly disagree forever.

## 6. Graph writes (per verdict)

```
SUPERSEDES → (A)-[:SUPERSEDES {reason, evidence_type: explicit|superset|recency-engaged}]->(B)
             (B)-[:STATUS]->(Superseded)
MERGED_FROM → (A)-[:MERGED_FROM]->(B), (A)-[:MERGED_FROM]->(C)
DISTINCT    → (A)-[:DISCUSSES]->(topic), (B)-[:DISCUSSES]->(topic)
UNRESOLVED  → (A)-[:CONFLICTS_WITH {claim_pair, checked_reconciliation: true}]->(B)
              both retain (:STATUS)->(Canonical)
```

## 7. Multi-generational chains

When A supersedes B, and later D supersedes A, the agent does not re-evaluate B — the existing edge stands untouched, and D is only evaluated against A (unless D directly engages with B's original claims, which is rare).

## 8. Failure modes to explicitly guard against

- **False superset**: treating "A mentions everything B does, plus more" as SUPERSEDES when A actually drops a caveat B had.
- **Merge misclassified as supersession**: relocating merged-from sources to `_superseded/` destroys the "check the old one for dropped content" operation. When ambiguous between SUPERSEDES and MERGED_FROM, default to MERGED_FROM (reversible) pending human confirmation.
- **UNRESOLVED starvation**: unresolved conflicts must surface in the topic's provenance table (per [[DC-CONSOLIDATOR-STD-001]]), not just sit in the graph.
- **Cross-authority creep**: this agent must never write a `CONSOLIDATES` edge or generate synthesized prose.

Pipeline note: Stage 2.5 always runs before the Consolidator pass — see [[DC-PIPELINE-STD-001]].
