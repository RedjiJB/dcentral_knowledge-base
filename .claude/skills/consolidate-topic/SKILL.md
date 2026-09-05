# Consolidate Topic (Stage 6 Consolidator agent, per-topic)

## 1. Role

You are the Consolidator per [DC-CONSOLIDATOR-STD-001](../../../standards/DC-CONSOLIDATOR-STD-001.md),
producing one standalone synthesized document per confirmed Stage 5 topic (from
`knowledge-base/_topics.md`), working through topics one batch at a time until none remain.

**Batch size: process up to 10 topics per invocation**, unless total source reading exceeds roughly
8,000-10,000 lines first — small 2-3 doc topics go fast; a topic with a 10+ doc or a 20,000-line
source should usually be the only one you do that invocation, even if the count of 10 isn't reached.
Judge by the doc_count and scratch-file size `get_next_topic.py` reports, not a rigid line count.
Stop early if `get_next_topic.py` reports nothing left.

Done = one `docs/DC-<SLUG>-RECONCILED-NNN.md` file per topic, each passing
`mark_topic_consolidated.py`'s mechanical check (§4 below) before moving to the next topic.

## 2. Scoped context — what to read, what NOT to read

- **Run `python3 scripts/get_next_topic.py` first.** It writes the next un-consolidated topic's full
  member-doc text to `conversations/_scratch/current_topic.md` and metadata (topic name, doc count,
  member paths, progress) to `conversations/_scratch/current_topic.json`. Topics are handed out
  smallest-doc-count-first.
- **Read `current_topic.json` for the topic name and progress**, then **read `current_topic.md`** —
  it already contains every member doc's full text concatenated with `SOURCE: <path>` separators, so
  you don't need to re-read the individual files.
- For a topic whose combined source text is very large (a 15,000+ line scratch file), it's fine to
  read it in chunks (multiple Read calls with `offset`/`limit`) rather than one call — the
  exhaustiveness requirement (§3 below) is about accounting for every doc's claims, not about reading
  the whole file in one gulp.
- You do NOT need `knowledge-base/_kb_doc_classified.jsonl`, `_dedup` registries, or any other topic's
  scratch file to do this task.

## 3. Numbered steps (repeat 1-6 per topic, up to the batch limit in §1)

1. Run `python3 scripts/get_next_topic.py`. If it exits 1 (nothing left), stop the loop early and go
   to step 7.
2. Read `conversations/_scratch/current_topic.json` for the topic name, doc count, and member paths.
3. Read `conversations/_scratch/current_topic.md` (the concatenated source text).
4. **Build a claim inventory before drafting anything** (DC-CONSOLIDATOR-STD-001 §2-3): walk every
   source, extract each discrete factual/architectural claim at the granularity the source actually
   asserted it at — not a whole-document summary, not an atomized sub-clause. Every claim must land
   in exactly one of: incorporated, superseded-within-this-topic, or unresolved conflict.
   - Before treating two sources as conflicting, **attempt reconciliation first** (§4 of the
     standard): is this actually a scope/version difference one source states explicitly (like "this
     extends the 20ft design to 40ft"), rather than a true contradiction? Only genuine, unreconciled
     contradictions go in Unresolved Tensions — and state both claims verbatim-referenced there, never
     picked between or averaged into a hedge.
   - Watch for the standard's named failure modes (§8): majority-vote fallacy, recency-bias-without-
     verification, scope creep (don't go pull in claims from docs outside this topic to "fill gaps").
5. Write the consolidated doc to `docs/DC-<SLUG>-RECONCILED-NNN.md` (pick `<SLUG>` as a short,
   readable stand-in for the topic — doesn't need to match the topic slug verbatim, e.g.
   `civicmesh-competitive-analysis` → `DC-CM-COMPETITIVE-RECONCILED-001`), using the fixed template
   from DC-CONSOLIDATOR-STD-001 §6 (`# [Topic Name] — Consolidated`, `## Current understanding`,
   `## Provenance`, `## Unresolved tensions`, `## Sources consulted (exhaustive list)`,
   `## Consolidation metadata`). Every member doc path must appear somewhere in the document (the
   Sources Consulted list, at minimum) — this is checked mechanically in step 6.
   Include the standard's closing note that the Consolidator never marks source docs `superseded` or
   moves them — that's DC-DEDUP-STD-001's authority, not this one's.
6. Run `python3 scripts/mark_topic_consolidated.py "<topic-name>" docs/DC-<SLUG>-RECONCILED-NNN.md`
   to validate structure/exhaustiveness and record the topic as done. If it exits non-zero, read the
   error (missing section heading, or a member path never mentioned in the doc) and fix the
   consolidated doc, then re-run — don't skip the topic or fake coverage by pasting a raw file list.
7. **Report a summary, not per-topic narration**: how many topics were consolidated this invocation,
   a one-line list of topic → output-doc-path, and total remaining. Use ONLY the `progress` /
   `remaining_after_this` fields from the most recently read scratch JSON for counts — never estimate
   a cumulative total yourself. Then stop.

## 4. Mechanical validation (what `mark_topic_consolidated.py` checks)

- All 5 required section headings are present (`## Current understanding`, `## Provenance`,
  `## Unresolved tensions`, `## Sources consulted`, `## Consolidation metadata`).
- Every member doc's repo-relative path (from `_topics.md`) appears somewhere in the consolidated
  doc's text — the mechanical proxy for "every linked source accounted for" (§2 of the standard). It
  cannot check claim-level exhaustiveness or conflict-handling quality — that's still your judgment
  call, not something a script can verify.
- Registers the topic in `registry/consolidated-topics.json` so `get_next_topic.py` won't hand it out
  again.

## 5. Guardrails

- **Never invent a topic** not already in `knowledge-base/_topics.md` — if you notice a topic looks
  mis-scoped (conflates two unrelated subjects, the way `federation-sovereignty-cooperative-platforms`
  did during this pipeline's first Stage 6 pass), stop and flag it rather than consolidating it as-is
  or silently splitting it yourself mid-batch — a topic split changes `_topics.md` and the doc
  registry and should be its own deliberate step, not a side effect of one Consolidator invocation.
- **Never mark a source doc `superseded` or move it** — that authority belongs to DC-DEDUP-STD-001,
  not this skill (DC-CONSOLIDATOR-STD-001 §0). If you notice what looks like a genuine duplicate
  or supersession relationship between two sources while consolidating, note it as an unresolved
  observation in the doc rather than acting on it.
- **Never re-consolidate an already-done topic** — `get_next_topic.py` filters these out via
  `registry/consolidated-topics.json`.
- **Don't pad the claim inventory to look thorough, and don't compress it to go faster.** A 2-doc
  topic with genuinely little to say should produce a short document; a 15-doc topic needs
  proportionate coverage. Length should track actual source complexity, not a target word count.
