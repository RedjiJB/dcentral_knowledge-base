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
| 4. Dedup/status pass | [DC-DEDUP-STD-001](standards/DC-DEDUP-STD-001.md) | **Step 1 done (mechanical); steps 2-5 surfaced as review reports, not auto-applied.** `scripts/dedup_pass.py` runs per category (the current topic-scope proxy, per pipeline ordering §2): 28 exact-content duplicates relocated to `<category>/_superseded/` automatically (§3 step 1 — same content hash, not a judgment call). 9 explicit-supersession language hits and 13 content-similarity candidates (5-word-shingle Jaccard ≥0.35) written to `registry/dedup-review/<category>.md` as **UNRESOLVED by default** — the script does not classify SUPERSEDES/MERGED_FROM on its own, since that needs claim-level reading comprehension it can't do; see `registry/dedup-review/_SUMMARY.md`. **Known limitation:** this only catches duplicates *within* a category — of the 61 exact-hash duplicates found globally in Stage 2, only 28 were relocated here because the other 33 are duplicates *across* categories (the same doc uploaded to projects that got classified into different categories), which a per-category pass structurally can't see. A cross-category identity-check pass is a candidate follow-up. |
| 5. Topic synthesis | [DC-TOPIC-SYNTH-STD-001](standards/DC-TOPIC-SYNTH-STD-001.md) | Not started. |
| 6. Consolidator | [DC-CONSOLIDATOR-STD-001](standards/DC-CONSOLIDATOR-STD-001.md) | Not started. |
| 7. Materialize filesystem | — | Not started. |
| 8. Build graph | — | Not started. |

## Known gaps in the extraction itself

- **Project-to-conversation mapping is missing from the export** (Anthropic limitation, not ours) — the 743 conversations aren't tagged with which of the 33 projects they belong to. Stage 3 classification will have to infer folder placement from conversation content/title rather than reading it off a field.
- **136 unique doc IDs found** in conversation text — this number should be reconciled against `registry/DC-REG-001-Master-Registry-v0.2.md`'s claimed 135 and against the actual 428 KB docs (a KB doc doesn't necessarily get its doc-ID mentioned inside conversation text, so these two counts measuring different things is expected, not a discrepancy to force-match).
- **61 of 428 KB docs are exact content duplicates** of another doc already extracted (same sha256 hash) — see `projects/_kb_docs_index.md`. These are likely the same document uploaded to more than one project's knowledge base, not genuine content variants.

## Next concrete step

Two options, not mutually exclusive:

1. **Cross-category identity-check pass** — catch the remaining 33 exact-hash duplicates that a
   per-category Stage 4 run structurally can't see (same content, different category).
2. **Resolve the review queue** — `registry/dedup-review/_SUMMARY.md` lists 9 explicit-supersession
   candidates and 13 similarity candidates across categories. Each needs an actual reading pass
   (human or an agent doing DC-DEDUP-STD-001 §3 steps 2-5 properly, with real claim extraction) to
   turn into a real verdict — the script deliberately stopped short of guessing these.

After that, Stage 5 (DC-TOPIC-SYNTH-STD-001): cluster each category's surviving docs into actual
topic nodes finer than "whole category" — e.g. Infrastructure/Mesh's 120 docs are not one topic.
