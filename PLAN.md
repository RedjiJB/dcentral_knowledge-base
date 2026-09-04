# Extraction Plan — Current Status Against DC-PIPELINE-STD-001

Tracks where the real Claude export (743 conversations, 33 projects, 1 memory file)
stands against the eight-stage pipeline defined in [standards/DC-PIPELINE-STD-001.md](standards/DC-PIPELINE-STD-001.md).

## Source export

Downloaded 2026-08-24 (manifest UUID `c777fb30-7a97-4144-93ac-15d06242fa6b`), four categories:

| Category | File | Contents |
|---|---|---|
| conversations | `conversations-000.zip` | 743 conversations, single JSON array, no project links (Anthropic export limitation) |
| projects | `projects-000.zip` | 33 projects — name, instructions, KB docs (428 KB docs total) |
| memories | `memories-000.zip` | 1 memory file |
| light_metadata | `light_metadata-000.zip` | login history, account info |

Two duplicate zip downloads (`conversations-000(1).zip`, `projects-000(1).zip`) were confirmed byte-identical
(md5) and discarded — not re-extracted.

Raw unzipped JSON lives in `raw-export/` (git-ignored — see `.gitignore` — it's the extraction *input*,
not versioned KB content; regenerate by re-unzipping the export and re-running the script below).

## Stage-by-stage status

| Stage | Standard | Status |
|---|---|---|
| 1. Extract conversations | — | **Done.** `scripts/extract_conversations.py` → `conversations/_extracted_index.md` (743 rows: uuid, name, dates, doc-IDs mentioned) |
| 2. Extract artifacts | — | **Done.** `scripts/extract_project_docs.py` → all 428 project KB docs pulled out of `raw-export/projects/projects/*.json` as individual files under `projects/kb-docs/<project>/<doc>.md`, each with front matter (source project, doc uuid, created_at, sha256 content hash). Indexed in `projects/_kb_docs_index.md`. Doc-ID *mentions* in conversation text (separate from KB doc *content*) remain in `registry/dc_registry_extracted_v2.csv` (136 unique IDs). |
| 3. Classify → folder tree | — | **Done at category level.** `scripts/classify_docs.py` routes all 428 docs from `projects/kb-docs/<project>/` (mirrors Claude's own Project structure) into `knowledge-base/<category>/<project>/` (mirrors subject matter instead), using an explicit project→category mapping. 8 categories: D-Central Ecosystem (62), Security/Identity (91), Infrastructure/Mesh (120), Haiti Initiative (19), AI/ML/Research (63), Verticals/Products (67), Academic/Training (5), Other/Experimental (1). This is coarse, project-level classification — the finer per-topic clustering within each category (e.g. `mesh-services/connectivity/` style) is Stage 5's job, not this one. `projects/kb-docs/` is left untouched as the Stage-2 ground truth; `knowledge-base/` is a regeneratable derived view (rerun the script rather than hand-editing it). |
| 4. Dedup/status pass | [DC-DEDUP-STD-001](standards/DC-DEDUP-STD-001.md) | **Done, including the review queue and cross-category duplicates.** `scripts/dedup_pass.py` (mechanical step 1 within category + candidate surfacing) → `scripts/resolve_dedup_review.py` (actual verdicts on flagged pairs) → `scripts/dedup_cross_category.py` (catches duplicates spanning category boundaries). Totals: 28 + 33 = 61/61 exact-content duplicates relocated (100% of Stage 2's original count, none unaccounted for), plus 11 confirmed SUPERSEDES and 1 confirmed UNRESOLVED from the review queue, 9 false positives dismissed. 72 docs total now under `_superseded/`. See `registry/dedup-review/_RESOLUTION.md` and `_CROSS_CATEGORY.md`. |
| 5. Topic synthesis | [DC-TOPIC-SYNTH-STD-001](standards/DC-TOPIC-SYNTH-STD-001.md) | Not started. |
| 6. Consolidator | [DC-CONSOLIDATOR-STD-001](standards/DC-CONSOLIDATOR-STD-001.md) | Not started. |
| 7. Materialize filesystem | — | Not started. |
| 8. Build graph | — | Not started. |

## Known gaps in the extraction itself

- **Project-to-conversation mapping is missing from the export** (Anthropic limitation, not ours) — the 743 conversations aren't tagged with which of the 33 projects they belong to. Stage 3 classification will have to infer folder placement from conversation content/title rather than reading it off a field.
- **136 unique doc IDs found** in conversation text — this number should be reconciled against `registry/DC-REG-001-Master-Registry-v0.2.md`'s claimed 135 and against the actual 428 KB docs (a KB doc doesn't necessarily get its doc-ID mentioned inside conversation text, so these two counts measuring different things is expected, not a discrepancy to force-match).
- **61 of 428 KB docs are exact content duplicates** of another doc already extracted (same sha256 hash) — see `projects/_kb_docs_index.md`. These are likely the same document uploaded to more than one project's knowledge base, not genuine content variants.

## Review queue: resolved

All 22 items flagged in the Stage 4 review queue were read and given an actual verdict —
`scripts/resolve_dedup_review.py`, results in `registry/dedup-review/_RESOLUTION.md`:

- **9 explicit-language candidates → all false positives.** The heuristic matched a generic
  single-word title ("Framework", "{Game Suite}") rather than a real cross-document reference.
  Confirmed by reading the actual sentences: ordinary product-description prose ("DAO governance
  replaces corporate control") or self-referential `supersedes:` metadata already in three docs
  pointing at unindexed past conversational scatter, not another artifact in this corpus.
- **11 similarity candidates → confirmed SUPERSEDES**, each verified by reading both docs (not just
  trusting recency): same title re-uploaded to the same project's KB later with substantially more
  content. Includes a 4-generation revision chain in Haiti Initiative (a `.tex` source → 3 successive
  `.md` re-uploads, each larger). Older docs relocated to `<category>/_superseded/<project>/` with
  `superseded_by`/`supersession_reason` front matter added to both sides of each pair.
- **1 similarity candidate → confirmed UNRESOLVED** (not a script default this time, an actual
  judgment call): a VDI-Solutions pair with identical title/TOC where the *later* upload is under
  half the size of the earlier one — contradicts the recency-implies-superset pattern every other
  pair fit, no explicit correction language either direction. Tagged `status: disputed` on both,
  left in place. This is DC-DEDUP-STD-001 §4's "no basis to prefer one" working as intended, not
  a gap.

## Cross-category duplicates: caught

`scripts/dedup_cross_category.py` closes the gap: scans the whole `knowledge-base/` tree by
content_hash regardless of category, relocates every duplicate to its own category's `_superseded/`.
Found and resolved all 33 remaining duplicates from Stage 2's original count of 61 (28 were caught
within-category by `dedup_pass.py`, these 33 needed the cross-category pass) — full accounting closed,
0 unaccounted-for exact duplicates left. Report: `registry/dedup-review/_CROSS_CATEGORY.md`.

**Notable finding:** 32 of the 33 are one thing — **Open-Vision's entire 32-document knowledge base
was an exact duplicate of IHOSE's**, filename-for-filename, byte-for-byte. Not overlapping content,
not a revision — the whole project was a clone. Canonical kept in IHOSE (earlier `created_at`); all
32 Open-Vision copies relocated. The 33rd is unrelated: one trades-cooperative doc shared between
Federated-System-Integration and Local-Fediverse. Worth deciding by hand whether Open-Vision as a
project concept still needs its own home in the classification scheme, given its KB content turned
out to be entirely borrowed from IHOSE.

## Next concrete step

Stage 5 (DC-TOPIC-SYNTH-STD-001): cluster each category's surviving docs into actual topic nodes
finer than "whole category" — e.g. Infrastructure/Mesh's 120 docs are not one topic.
