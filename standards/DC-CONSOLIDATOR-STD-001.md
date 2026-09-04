# DC-CONSOLIDATOR-STD-001: Standard for the Consolidator Agent Role

## 0. Purpose and boundary

The Consolidator produces one standalone synthesized document per topic node, representing current best understanding across every source that discusses that topic. It never edits, deletes, or re-labels a source document, and it never assigns `superseded` status — that authority belongs exclusively to the Stage 2.5 dedup/status agent ([[DC-DEDUP-STD-001]]). This separation is load-bearing: synthesizing a better answer and declaring an old answer dead are different authorities, and collapsing them into one agent recreates the self-approval problem the governance architecture rules out elsewhere.

## 1. Trigger conditions (when a topic gets consolidated)

A topic node is eligible for consolidation only when all hold:

- It has ≥2 `discussed_in` or `resolved_by` links (a single-source topic has nothing to consolidate — skip it, don't manufacture a synthesis of one)
- At least one linked source has been added or revised since the topic's last consolidation timestamp (or it has never been consolidated) — this is what makes re-runs cheap: unchanged topics are skipped entirely, not re-synthesized on every pass
- The topic is not itself flagged `resolved-terminal` (a topic may be marked closed by explicit human decision — see §7 — and shouldn't get silently reopened by a new tangential mention)

## 2. Exhaustiveness requirement — the granular part

The Consolidator must account for every linked source, not a representative sample. Concretely:

- Build a claim inventory before drafting anything: walk every linked conversation and artifact, extract every discrete factual/architectural claim relevant to the topic as a separate line item with its source reference. This is a mechanical extraction step, done before any synthesis judgment is applied — judging "what's true" before "what was actually said" is how sources quietly get dropped.
- Every claim in the inventory must end up in exactly one of three buckets in the final document: **incorporated** (folded into the consolidated narrative), **superseded-within-this-topic** (an earlier claim a later source explicitly corrected — cited as history, not silently omitted), or **unresolved conflict** (§4). A claim that lands in none of these three is a process failure, not an acceptable simplification.
- No minimum-source-count shortcut: a topic with 11 contributing conversations gets the same per-claim accounting as a topic with 2. If the corpus is large, the document can organize by sub-cluster to stay readable, but the inventory itself stays exhaustive.

## 3. Granularity requirement — what counts as one claim

A claim is the smallest independently-verifiable statement — not a whole document's summary, not a whole paragraph. Calibration examples:

- Too coarse: "DC-TAXONOMY-008 covers cellular architecture" (that's a description, not a claim)
- Correct: "CBRS's SAS requires fixed GPS coordinates and cuts transmission on location drift" — one falsifiable, sourceable statement
- Too fine: splitting "CBRS requires fixed GPS" and "GPS drift breaks the SAS heartbeat" into two claims when the source stated them as one causal point — don't atomize past the level the source actually asserted it at

## 4. Conflict handling — never silently resolved

When two sources make claims that are genuinely incompatible (not just differently scoped), the Consolidator:

1. States both claims verbatim-referenced (not paraphrased into a compromise position neither source actually stated)
2. Attempts a reconciliation check first — is this actually a scope/layer difference rather than a true conflict? If reconciliation succeeds, document the reconciled structure and cite both sources as compatible, with the "layers" framing made explicit.
3. If no reconciliation is found, the conflict goes into an explicit Unresolved Tensions section — never picked between silently, never averaged into a hedge that both sources would reject.

## 5. Provenance — every claim traceable

Every incorporated claim carries an inline source reference (conversation ID or artifact ID + rough location). Cite at the claim-cluster level, not the sentence level — group 3-5 related claims from the same source under one reference marker, but never let an entire section go uncited.

## 6. Structure of the output document

Fixed template, every consolidation:

```markdown
# [Topic Name] — Consolidated (v[N], generated [date])

## Current understanding
[Synthesized narrative, organized by sub-topic, cited per §5]

## Provenance
| Claim cluster | Sources | Status |
|---|---|---|
| ... | conv-id, artifact-id | incorporated / superseded-within-topic |

## Unresolved tensions
[Explicit conflicts per §4, or "None identified in this pass"]

## Sources consulted (exhaustive list)
[Every conversation/artifact linked to this topic, even ones that
contributed nothing beyond confirming what others said]

## Consolidation metadata
consolidates: [artifact/conversation ids]
supersedes_prior_consolidation: [prior consolidated-doc id, if any]
generated_by: consolidator-agent
```

## 7. Versioning and re-runs

Each consolidation produces a new version, never an in-place edit of the prior document — the prior version moves to that topic's own `_superseded/` (consolidated docs can supersede earlier consolidated docs, same mechanism as any other artifact).

A human can mark a topic `resolved-terminal` (§1) to stop automatic re-consolidation. This is a manual override, never inferred by the agent itself.

## 8. Failure modes to explicitly guard against

- **Majority-vote fallacy**: if 4 sources say X and 1 says Y, the Consolidator does not treat X as "more true" by count — it evaluates whether Y is outdated, a genuine minority-correct insight, or a real unresolved conflict.
- **Recency bias without verification**: a later source isn't automatically right just because it's later — the Consolidator checks whether it actually engaged with the earlier claim versus simply not mentioning it (silence isn't correction).
- **Scope creep**: the Consolidator only pulls from sources actually linked to this topic node — it does not go researching adjacent topics to "fill gaps." Gaps get flagged in the output, not fabricated.
