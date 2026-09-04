# DC-PIPELINE-STD-001: Standard for Pipeline Orchestration

## 0. Purpose and boundary

This standard governs how the four processing stages ([[DC-DEDUP-STD-001]], [[DC-TOPIC-SYNTH-STD-001]], [[DC-CONSOLIDATOR-STD-001]], plus extraction/classification) run together as one system: ordering, re-run triggers, partial failure handling, and enforcement of each stage's authority boundary at the orchestration level.

## 1. The eight-stage pipeline (canonical order)

```
1. Extract conversations
2. Extract artifacts (content-hashed, doc-ID tagged)
3. Classify conversations → folder tree
4. Stage 2.5: Dedup/status pass        [DC-DEDUP-STD-001]
5. Topic synthesis pass                 [DC-TOPIC-SYNTH-STD-001]
6. Consolidator pass                    [DC-CONSOLIDATOR-STD-001]
7. Materialize filesystem (_INDEX.md, _superseded/)
8. Build/update graph (Neo4j/Obsidian)
```

Steps 1-3 run once per new conversation (ingestion-triggered). Steps 4-8 form the standing loop — they re-run periodically against the accumulated corpus, not just once at migration time.

## 2. Hard dependency ordering

- **3 → 4**: Dedup needs artifacts placed in the folder tree to know which pairs/clusters share a topic scope worth comparing.
- **4 → 5**: Topic synthesis needs canonical/superseded status already resolved — clustering a superseded duplicate alongside its replacement would corrupt topic membership.
- **5 → 6**: The Consolidator's unit of work is the topic node — it cannot run against a folder or raw source list.
- **6 → 7**: Filesystem materialization reflects decisions made in 4-6; must never run ahead of them.
- **7 → 8**: filesystem and graph should be written in the same pass/transaction where possible so they never observably diverge mid-run.

No stage may run on a corpus slice that a required upstream stage hasn't yet processed.

## 3. Re-run triggers

- **New conversation ingested** → triggers 1-3 immediately, then queues target folder(s) for a 4-6 re-run.
- **New artifact revision** → queues linked topics for stage 4 re-evaluation, then 5-6 if it survives as canonical.
- **Human-flagged split/merge** → queues affected topic(s) immediately, bypassing the skip.
- **Periodic backstop sweep** → safety net only; if it finds unqueued work, that's a bug signal, not normal operation.

## 4. Idempotency and the skip contract

- Track a `last_run` timestamp per stage per unit (per-folder for 4-5, per-topic for 6).
- A stage only runs on a unit if it has a change timestamp newer than the stage's `last_run` for it, or has never run.
- This keeps the standing loop cheap at scale.

## 5. Partial failure and recovery

- A single artifact pair failing dedup classification does not block other pairs — log as `UNRESOLVED` and continue.
- A single topic failing consolidation (retrieval error, not judgment failure) retries in the next run without blocking siblings.
- Stage failures propagate a **hold**, not a **skip**: if stage 4 fails on a folder, stage 5 must not proceed on that folder using stale/partial data.
- Human-review flags (UNRESOLVED, split/merge proposals, disputed topics) accumulate in a review queue surfaced via the periodic sweep — never auto-resolved by re-running the same stage with the same inputs.

## 6. Authority enforcement at the orchestration layer

- Stage 4 write permissions: `STATUS`, `SUPERSEDES`, `MERGED_FROM`, `CONFLICTS_WITH` edges, `_superseded/` moves. Nothing else.
- Stage 5 write permissions: topic nodes, `DISCUSSES`, `SPLIT_INTO`/`MERGED_INTO` edges, `_INDEX.md` topic listings. Nothing else.
- Stage 6 write permissions: new consolidated artifacts, `CONSOLIDATES` edges, provenance tables. No `STATUS`/`SUPERSEDES`/dedup-owned edges.
- Scoped write permissions per stage are the actual enforcement mechanism for the authority boundaries each stage standard declares, not an optimization detail.

## 7. Observability requirement

Every run of every stage logs: what unit it ran on, what verdict/output it produced, and which upstream `last_run` timestamps it consumed.

## 8. Failure modes to explicitly guard against

- **Stage-skipping under time pressure**: running the Consolidator against a folder that hasn't had a dedup pass yet — the most damaging shortcut, since consolidated docs would draw from superseded content as if canonical.
- **Full-corpus reprocessing creep**: abandoning the incremental skip contract (§4), turning a cheap standing loop into a full rebuild every time.
- **Silent downstream proceeding on upstream failure**: a `try/except: continue` around a stage-4 failure that lets stage 5 run anyway on stale data.
- **Write-permission drift**: a stage's process quietly gaining write access to another stage's owned fields "for convenience," eroding the authority boundaries in §6.
