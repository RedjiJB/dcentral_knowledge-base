# DC-TOPIC-SYNTH-STD-001: Standard for the Topic Synthesis Pass

## 0. Purpose and boundary

This pass generates topic nodes — the graph objects the Consolidator ([[DC-CONSOLIDATOR-STD-001]]) later consumes and that `_INDEX.md` files display. It clusters artifacts/conversations by actual subject matter and creates or updates the topic layer of the graph. It does not write prose synthesis and does not assign canonical/superseded status ([[DC-DEDUP-STD-001]]) — it only decides what the topics are and which sources belong to which topic.

## 1. Why this pass exists as a distinct step

Folder placement (Stage 1 classification) tells you where a conversation lives, not what discrete topics that folder actually contains. Without this pass, the Consolidator has no unit of work smaller than "everything in a folder," producing bloated, unfocused consolidated docs. Topic nodes are that missing unit.

## 2. Trigger conditions

- A folder receives a new conversation/artifact since its last topic-synthesis run
- A folder has never had topic nodes generated
- Human-flagged: a topic node is manually split, merged, or renamed

Skip a folder entirely if nothing has changed since its last run.

## 3. Procedure

1. **Abstract extraction**: 2-4 sentence abstract per source, what it actually discusses. Reuse existing abstracts if the source hasn't changed.
2. **Clustering**: group abstracts by actual subject overlap, not keyword match.
3. **Topic boundary decision** (§4).
4. **Topic node creation/update**: `name`, `folder_scope`, `first_seen`, `member_count`, `status` (`active` / `resolved-terminal`).
5. **Edge writes**: `(source)-[:DISCUSSES]->(topic)` for every cluster member.
6. **Cross-folder check** (§5) before finalizing.

## 4. Topic granularity — what counts as one topic

- **Too coarse**: "Cellular architecture" covering federation design, hardware selection, and regulatory taxonomy all at once — recreates folder-level bloat one level down.
- **Too fine**: splitting inseparable sub-claims into separate topics — creates node sprawl and near-duplicate Consolidator output.
- **Correct test**: a topic is right-sized when you can write one honest 2-4 sentence abstract without using "and" to join two unrelated ideas, and at least two independent sources would plausibly both link to it.
- **Precedent check**: match sibling topic nodes' granularity within the same folder rather than introducing an inconsistent grain size.

## 5. Cross-folder topics

- Before creating a new topic node, search existing topic nodes graph-wide for subject overlap.
- If found, link the new source to the existing topic node; add `folder_scope` as a list if it now spans multiple folders.
- The topic should appear in every folder's `_INDEX.md` it has members in, annotated as cross-folder.
- If uncertain whether it's the same topic or coincidental overlap, err toward DISTINCT (two separate nodes) — false-merging is harder to detect later because evidence is scattered.

## 6. Topic lifecycle and re-derivation

- Membership is append-only under normal operation.
- **Split**: `(topic-A-original)-[:SPLIT_INTO]->(topic-A1)`, `...->(topic-A2)`, original marked `status: split`, never deleted.
- **Merge**: `(topic-A)-[:MERGED_INTO]->(topic-C)`, `(topic-B)-[:MERGED_INTO]->(topic-C)`.
- Splits and merges are flagged for human confirmation before finalizing.

## 7. Output artifacts

- Topic nodes in the graph.
- `_INDEX.md` regeneration at the folder level, cross-folder topics annotated.
- No prose document is produced — that's deferred to the Consolidator.

## 8. Failure modes to explicitly guard against

- **Keyword-clustering instead of subject-clustering** — same distinction Stage 2.5 draws for content overlap ([[DC-DEDUP-STD-001]] §3).
- **Silent re-partitioning**: regenerating a folder's entire topic set from scratch instead of incrementally updating — breaks append-only guarantee and spuriously triggers Consolidator re-runs.
- **Folder-boundary tunnel vision**: missing legitimate cross-folder topics, creating fragmented duplicates.
- **Overfitting to the newest source**: letting a recent conversation redefine an existing topic's boundary incidentally — scope changes only via the explicit split/merge procedure (§6).

Pipeline position: runs after Stage 2.5 and before the Consolidator — see [[DC-PIPELINE-STD-001]].
