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
| 2. Extract artifacts | — | **Partial.** Doc-ID mentions extracted into `registry/dc_registry_extracted_v2.csv` (136 unique IDs, full corpus — supersedes the stale 135-ID v1 CSV that only covered pattern-matching against a smaller pass). Project KB docs (428 of them, the actual artifact *content*, not just ID mentions) indexed by count only in `projects/_extracted_index.md` — not yet pulled out as individual files. |
| 3. Classify → folder tree | — | **Not started.** No `mesh-services/`-style topic folder tree exists yet; conversations/projects are only in flat indexes. |
| 4. Dedup/status pass | [DC-DEDUP-STD-001](standards/DC-DEDUP-STD-001.md) | **Not started** (needs Stage 3 first, per pipeline ordering §2). One manual example done by hand: the two identical Haiti-ISP chat exports were an "identity check" (§3 step 1) case — same content, kept one copy in `conversations/examples/`. |
| 5. Topic synthesis | [DC-TOPIC-SYNTH-STD-001](standards/DC-TOPIC-SYNTH-STD-001.md) | Not started. |
| 6. Consolidator | [DC-CONSOLIDATOR-STD-001](standards/DC-CONSOLIDATOR-STD-001.md) | Not started. |
| 7. Materialize filesystem | — | Not started. |
| 8. Build graph | — | Not started. |

## Known gaps in the extraction itself

- **Project-to-conversation mapping is missing from the export** (Anthropic limitation, not ours) — the 743 conversations aren't tagged with which of the 33 projects they belong to. Stage 3 classification will have to infer folder placement from conversation content/title rather than reading it off a field.
- **428 project KB docs are not yet extracted as individual files** — `projects/_extracted_index.md` only has per-project counts. Pulling each `doc` out of each project JSON (`raw-export/projects/projects/*.json` → `docs[]` → `title`/`content`) is the next concrete task under Stage 2, and is what actually populates the artifact layer the rest of the pipeline operates on.
- **136 unique doc IDs found** in conversation text — this number should be reconciled against `registry/DC-REG-001-Master-Registry-v0.2.md`'s claimed 135 and against the actual 428 KB docs (a KB doc doesn't necessarily get its doc-ID mentioned inside conversation text, so these two counts measuring different things is expected, not a discrepancy to force-match).

## Next concrete step

Write `scripts/extract_project_docs.py`: walk `raw-export/projects/projects/*.json`, write each `docs[]` entry
to `projects/kb-docs/<project-name>/<doc-title>.md` (or content-hash filename if titles collide). That's the
actual Stage 2 artifact extraction the pipeline standards assume exists before Stage 3 classification can run.
