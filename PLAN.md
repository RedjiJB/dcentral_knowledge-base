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
| 5. Topic synthesis | [DC-TOPIC-SYNTH-STD-001](standards/DC-TOPIC-SYNTH-STD-001.md) | **Done, including the subject-check pass.** `scripts/topic_synthesis.py` (first-pass lexical clustering, non-transitive star clustering to avoid chaining — see git history for the connected-components bug this replaced) → `scripts/resolve_topic_review.py` (real subject-check verdicts against §4's calibration test on all 59 first-pass clusters). Result: **55 confirmed topics**, 231 docs clustered, 124 correctly left ungrouped. Applied: 2 genuine splits (clusters that merged unrelated subjects sharing only generic vocabulary), 2 merges (clusters split only by superficial audience/doc-type difference), 4 doc demotions (a single mismatched doc inside an otherwise-coherent cluster). **Correction made mid-pass on user feedback:** an initial subject-check wrongly split 4 clusters apart on the assumption that "different Claude Project = different subject" — e.g. separating CivicMesh's community docs from Local-Fediverse's academic-platform docs, or Drone-Zoe's Haiti docs from VDI-Solutions' Haiti docs. That assumption is backwards for this corpus: D-Central deliberately reuses the same concepts (community/participation platforms, federation, credentialing, Haiti integration) across many verticals on purpose, so cross-project overlap is often the real topic, not noise. Those 4 splits were reverted into concept-based merged topics (`digital-community-participation-platforms`, `federation-sovereignty-cooperative-platforms`, `security-ecosystem-sector-platforms`, `haiti-integration-platforms`). Full reasoning: `TOPIC-RESOLUTION.md`. |
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

## Cross-pollination check

Following the Local-Fediverse correction, checked whether the categories treated as separate
"verticals" (`ai-ml-research`, `verticals-products`, `security-identity`) actually share D-Central's
core concepts (DAO governance, DID/VC credentialing, cooperative economics, federation) closely
enough to warrant folding back into the core rather than staying siloed. Findings:
`CROSS-POLLINATION-FINDINGS.md`. Short version: strong overlap in `verticals-products` (64% of docs
hit core vocabulary — Bounty's "DION Platform" docs are explicitly a D-Central Intelligence Operator
Network subsystem, not an unrelated product) and `ai-ml-research` (52% — Federated-Learning-
Platform's sovereignty docs and IHOSE's federation docs describe the same federation/DAO pattern
applied per-sector). `academic-training` correctly has zero overlap and stays separate. This is a
findings report, not an applied merge — concrete candidates are scoped for the Stage 6 Consolidator
pass to reconcile against D-Central's own core docs in `docs/`.

## DION/core reconciliation: confirmed

Read both sides directly (not just flagged). Confirmed real architecture duplication, not just
similar vocabulary: the Bounty/DION docs build a complete parallel identity/credential/governance/
token stack (`did:dcentral:operator:`, custom `DIONRegistry`/`OperatorCredentialingSystem` smart
contracts, `INTEL_TOKEN`/`REP_TOKEN` economics, own `DIONGovernance` voting contract) instead of
reusing `dc-identity`/`dc-governance`/`dc-attestation`, despite `docs/DC-AGENT-CREDENTIAL-001.md`
explicitly stating "not a new identity system." Full comparison table and reasoning in
`CROSS-POLLINATION-FINDINGS.md`. The two Bounty docs are now tagged with a `reconciliation_note`
front-matter field pointing at the authoritative core docs. DION's operational content (training
curriculum, hardware tiers, emergency-services integrations) is NOT duplicated and should be kept —
only the identity/credential/governance/token layer needs replacing. This is now a scoped Stage 6
Consolidator task, not just a finding.

## Stage 6 (Consolidator): first consolidated document produced

`docs/DC-DION-RECONCILED-001.md` — the DION reconciliation, written per DC-CONSOLIDATOR-STD-001's
fixed template (current understanding, provenance table, unresolved tensions, sources consulted,
consolidation metadata). Incorporates DION's genuine operational content (hardware tiers, multi-INT
collection, operator training/career progression, application-layer use cases, API surface) while
marking the identity/credential/governance/token layer superseded-within-topic by the existing
`dc-identity`/`dc-governance`/`dc-attestation` mechanisms. One real unresolved tension recorded
rather than guessed at: DION's `INTEL_TOKEN` payment need has no confirmed equivalent in the
reconciled core docs — `DC-LKB-*` (Lakou Protocol banking) is the likely place to check, but those
docs aren't yet in this repo. The two DION source docs' `reconciliation_note` front matter now points
to this consolidated doc; per the Consolidator's authority boundary, neither source was marked
superseded or moved (that's Stage 4's job, not Stage 6's).

## DC-LKB-001/002/003 pulled in, DION payment tension resolved

The Lakou Protocol docs weren't project KB docs — they were artifacts created inline in a conversation
("Decentralized family banking framework with modular services," conversation uuid
`76d91c3d-0b67-437f-a5dc-e5841bc93104`), living inside `create_file` tool-use blocks in
`conversations.json`, not in any project's `docs[]` array. Stage 2's extraction only covers project
KB docs, so this required a manual, targeted extraction — a real gap in the automated pipeline worth
noting: **an unknown number of other DC-*-NNN docs likely exist the same way**, created as
conversation artifacts rather than uploaded to a Project, and Stage 2 as currently built has no way
to find them systematically (it would need to scan every conversation's tool-use blocks for
`create_file` calls, not just grep message text for doc-ID mentions the way `dc_registry_extracted_v2.csv`
does).

Extracted `docs/DC-LKB-001.md` (23KB, concept doc), `DC-LKB-002.md` (61KB, technical spec),
`DC-LKB-003.md` (51KB, v2 universal banking OS) with front matter noting the extraction method.

These directly resolved `DC-DION-RECONCILED-001`'s one open tension: `dc-credit` (D-Central's
existing payments/settlement microservice, `DC-TAXONOMY-002` §1.2) already handles payroll
disbursement and milestone-released payments, and DC-LKB-003 shows the actual pattern — a
vault-native stablecoin (e.g. `HGUSD`) for payment settlement, with governance tokens kept strictly
non-transferable and separate from payment currency. Updated `DC-DION-RECONCILED-001` to v2:
`INTEL_TOKEN` is now superseded-within-topic like the rest of DION's token/governance layer, zero
unresolved tensions remain in that document.

## Stage 2 classifier agent: two implementations, neither run yet

**Option A — standalone script** (`scripts/classify_conversations_agent.py`): calls the Anthropic
API directly (Haiku), ~743 calls, needs `ANTHROPIC_API_KEY` + `pip install anthropic`. Run it
yourself: `python3 scripts/classify_conversations_agent.py`.

**Option B — Claude Code session** (built second, the one actually meant to be used): a proper
`classify-conversation` Skill at `.claude/skills/classify-conversation/SKILL.md`, following the
6-component context-engineering discipline (role, scoped context, numbered steps, examples, output
schema, guardrails) instead of a hardcoded API prompt. Supporting infrastructure:

- `scripts/get_next_conversation.py` — scoped-context helper. Extracts ONE unclassified
  conversation's title/summary/excerpt/doc-IDs to `conversations/_scratch/current.json` (a few KB)
  so the skill never has to read the 320MB `conversations.json` directly.
- `scripts/validate_classification.py` — mechanical guardrail, wired as a `PostToolUse` hook in
  `.claude/settings.json`. Rejects invented taxonomy categories, missing fields, and duplicate UUIDs
  after every write — enforcement, not just an instruction the model might follow.
- `CLAUDE.md` (repo root) — auto-loaded orientation pointing any fresh session at the skill and the
  scoping rule, so this doesn't need re-explaining every session.
- Deliberately NOT using persistent "memory" for the taxonomy — memory is for cross-session facts
  about the user, not task configuration; the fixed taxonomy lives in the Skill file (versioned,
  reviewable) instead.

Both are unrun. Fixed taxonomy is identical in both (`d-central/core/*`, `mesh-services/*`,
`verticals/*`, `hardware/*`, `business-legal`, `haiti-diaspora`, `meta/*`, `security`,
`academic-personal`, `other`) — one call classifies one conversation; invoke the skill 743 times (or
wrap it in a loop) to run the full pass.

## Next concrete step

Three threads, not mutually exclusive:

1. **Run the Stage 2 classifier** (above) — once run, its output should be reconciled against the
   existing `knowledge-base/` category tree (built from Project-level classification, coarser) rather
   than replacing it outright.
2. **Systematic conversation-artifact extraction** — scan all 743 conversations' `create_file`
   tool-use blocks for `DC-*-NNN`-pattern filenames, not just project KB docs (the DC-LKB pull did
   this by hand for one conversation; likely more exist).
3. More Stage 6 Consolidator passes: `federation-sovereignty-cooperative-platforms` (11 docs),
   `digital-community-participation-platforms` (16 docs), `chopshop-project-documentation` (17 docs),
   `haiti-integration-platforms` (12 docs).
