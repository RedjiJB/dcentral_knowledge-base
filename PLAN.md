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
| 4. Dedup/status pass | [DC-DEDUP-STD-001](standards/DC-DEDUP-STD-001.md) | **Not started** as an automated pass, but **61 exact-content duplicates were already surfaced for free** by the Stage 2 extraction's content-hash check — see `projects/_kb_docs_index.md`'s "Exact duplicate of" column. These are ready-made §3-step-1 identity-check cases: same content hash, mechanical dedup, no judgment call needed. One earlier manual example also done by hand: the two identical Haiti-ISP chat exports (kept one copy in `conversations/examples/`). |
| 5. Topic synthesis | [DC-TOPIC-SYNTH-STD-001](standards/DC-TOPIC-SYNTH-STD-001.md) | Not started. |
| 6. Consolidator | [DC-CONSOLIDATOR-STD-001](standards/DC-CONSOLIDATOR-STD-001.md) | Not started. |
| 7. Materialize filesystem | — | Not started. |
| 8. Build graph | — | Not started. |

## Known gaps in the extraction itself

- **Project-to-conversation mapping is missing from the export** (Anthropic limitation, not ours) — the 743 conversations aren't tagged with which of the 33 projects they belong to. Stage 3 classification will have to infer folder placement from conversation content/title rather than reading it off a field.
- **136 unique doc IDs found** in conversation text — this number should be reconciled against `registry/DC-REG-001-Master-Registry-v0.2.md`'s claimed 135 and against the actual 428 KB docs (a KB doc doesn't necessarily get its doc-ID mentioned inside conversation text, so these two counts measuring different things is expected, not a discrepancy to force-match).
- **61 of 428 KB docs are exact content duplicates** of another doc already extracted (same sha256 hash) — see `projects/_kb_docs_index.md`. These are likely the same document uploaded to more than one project's knowledge base, not genuine content variants.

## Next concrete step

Stage 4: run an actual DC-DEDUP-STD-001 pass. The 61 exact-content duplicates already flagged in
`projects/_kb_docs_index.md` are the easy identity-check cases (§3 step 1) — mechanical, no judgment
call. The harder cases (SUPERSEDES/MERGED_FROM/DISTINCT/UNRESOLVED, per §3 steps 2-5) need each
category folder's docs compared pairwise for content overlap, which needs either a semantic-similarity
pass or manual review per category, starting with the largest ones (Infrastructure/Mesh at 120 docs,
Security/Identity at 91).
