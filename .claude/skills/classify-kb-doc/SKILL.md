---
name: classify-kb-doc
description: Classify the next unclassified KB document into the fixed D-Central taxonomy, one document at a time, and append the result to knowledge-base/_kb_doc_classified.jsonl. Use when running the Stage 3 (fine-grained, per-document) classification pass over projects/kb-docs/.
---

# Classify KB Doc (Stage 3 classifier agent, per-document)

## 1. Role

You are classifying D-Central knowledge-base documents (the 428 files under
`projects/kb-docs/<project>/`), one at a time, into the same fixed category taxonomy used by
the Stage 2 conversation classifier (`.claude/skills/classify-conversation/SKILL.md`). This
replaces `scripts/classify_docs.py`'s coarse 33-entry project→category lookup table (every doc
in a project got the same category) with a real per-document read: "what is this document
genuinely about," not "which project was it uploaded to."

**Batch size: process up to 20 documents per invocation**, looping through steps 1-6 of §4
internally, then stop and report a summary (§7). Starting at 20 rather than 40 — the
conversation classifier's history (`PLAN.md`) shows batch size should earn its way up through
clean runs, not start high. Stop early if `get_next_kb_doc.py` reports nothing left.

Done = up to 20 JSON lines appended to `knowledge-base/_kb_doc_classified.jsonl` via the safe
append path in §4 step 5 — never construct a shell command with the record's JSON inlined into
it, for the exact same reason documented in the conversation-classifier skill (quoting breaks
unpredictably on real content).

## 2. Scoped context — what to read, what NOT to read

- **Run `python3 scripts/get_next_kb_doc.py --count 20` first** (batch mode — hands out up to 20
  unclassified docs in one call, writing `{"progress": "...", "docs": [...]}` to
  `conversations/_scratch/current_kb_doc.json`). Plain `get_next_kb_doc.py` with no `--count` still
  works and writes the single-object shape for backward compatibility, but batch mode is what
  makes a 20-document invocation a handful of tool calls instead of 20 separate round-trips.
- **Read only that scratch file.** Never read all 428 files under `projects/kb-docs/` at once,
  and never read the full original document if the excerpt already makes the subject clear —
  the excerpt is capped at 4000 chars specifically to keep this scoped. If a document's subject
  is genuinely ambiguous from the excerpt alone (e.g. it starts with boilerplate/front-matter-like
  content), Read the actual file at `relative_path` from the scratch record to see more.
- **Read the taxonomy in §3 below.** Do not read the other Skill's worked examples or
  `knowledge-base/`'s existing coarse tree — you don't need either.
- You do NOT need `knowledge-base/_kb_doc_classified.jsonl`'s prior entries to do this task.

## 3. Fixed taxonomy — identical to the Stage 2 conversation classifier, pick from this list only

```
d-central/core/identity              (dc-identity, DID/VC, credentials)
d-central/core/governance            (dc-governance, DAO-agent-loop, expert-DAO)
d-central/core/economics             (dc-credit, Lakou Protocol, financial modeling)
d-central/core/attestation-storage   (dc-attestation, mesh-storage archive tier)
d-central/core/observability         (agent observability, monitoring)
d-central/mesh-services/connectivity (mesh-connectivity, cellular, CBRS/MulteFire, 802.1X)
d-central/mesh-services/compute      (distributed/edge compute)
d-central/mesh-services/storage      (mesh-storage, IPFS/Filecoin/Arweave)
d-central/mesh-services/energy       (power tiers, solar, energy systems)
d-central/mesh-services/sensors-mobility (TrafficMesh, DIMO-style vehicle networks)
d-central/mesh-services/ai           (mesh-ai, federated learning, inference)
d-central/mesh-services/bandwidth    (bandwidth/QoS mechanisms)
d-central/mesh-services/geo          (SkyLedger, geo/mapping, Hivemapper-style)
d-central/verticals/commerce         (MeshShop, MeshEats, MeshBank, Lakou Marketplace)
d-central/verticals/social-comm      (MeshSocial, MeshDM, MeshWire, MeshWiki, fediverse)
d-central/verticals/health           (MeshHealth, SHI health tier)
d-central/verticals/mobility         (MeshRide, MeshCar, delivery)
d-central/verticals/home-trades      (MeshBuild, home/trades verticals)
d-central/verticals/manufacturing    (textile, manufacturing verticals)
d-central/hardware/shi-node          (DC-SHI-SPEC, node BOM/hardware)
d-central/hardware/campus            (campus/district topology, transit)
d-central/hardware/sensing-planes    (multi-plane sensing, swarm/biomimicry)
d-central/hardware/wearables-display (wearables, display tech)
d-central/business-legal             (licensing, venture, governance, legal docs)
d-central/haiti-diaspora             (Haiti pilot, diaspora-specific work)
d-central/meta/status-tracking       (DC-STATUS-001-style gap/status tracking)
d-central/meta/simulation            (DC-SIM series, GNS3 lab work)
d-central/meta/platform-scaffolding  (whole-platform README/setup/repo scaffolding touching every
                                      module at once -- agent, mesh, blockchain, identity, AI, DAO --
                                      rather than one specific vertical)
d-central/security                   (OpenSecure suite, OS-PACS/GUARDIAN/PATROL/SENTINEL/CONCIERGE)
d-central/academic-personal          (coursework, career, personal/non-D-Central content)
d-central/other                      (genuinely doesn't fit above -- last resort, use sparingly)
```

Reusing this exact list (rather than letting per-document classification drift into new
category names) is what makes the 428 document-level calls comparable to each other and to the
743 conversation-level calls already done.

## 4. Numbered steps (repeat 1-5 up to 20 times per invocation, then do step 6 once)

1. Run `python3 scripts/get_next_kb_doc.py`. If it exits 1 (nothing left), stop the loop early
   and go to step 6.
2. Read `conversations/_scratch/current_kb_doc.json`.
3. Pick exactly one `primary_category` from §3 based on what the document's content is actually
   about — not the source project's overall theme, and not the coarse category
   `projects/_kb_docs_index.md` or `classify_docs.py` would have assigned. Pick 0-3
   `secondary_tags` for other categories the document genuinely also touches; leave empty for a
   clean single-topic document.
4. Write a 2-3 sentence `abstract` specific enough that someone deciding whether to open the
   document can tell from the abstract alone what's in it — not a restatement of the filename.
5. **Write the record(s) safely, then append.**
   - In batch mode: classify every doc in the `docs` array, then use the Write tool to save a JSON
     ARRAY of records (schema in §5, one object per doc, using each doc's own `doc_uuid`/
     `source_project`/`original_filename`/`relative_path`) to
     `conversations/_scratch/pending_kb_doc.json`.
   - Run `python3 scripts/append_kb_doc_classification.py conversations/_scratch/pending_kb_doc.json`
     to validate and append — it accepts either a single object or an array, and appends each
     record in order, stopping at (and reporting) the first one that fails validation.
   - If it exits non-zero, the error names which record (index + doc_uuid) failed — fix just that
     record and re-run with the remaining unclassified records still in the array (already-appended
     ones ahead of it are safe; re-running with them included is harmless since they're already in
     `_kb_doc_classified.jsonl` and the append script would just reject them as duplicates — better
     to trim them out of the retry file to keep the error signal clean).
6. **Report a summary, not per-item narration**: how many were classified this invocation, and a
   one-line list of filename → primary_category. For "how many remain" and "total classified,"
   use ONLY the `progress` field from the most recently read scratch file — never estimate or
   calculate a cumulative total yourself (the conversation classifier got this wrong twice by
   guessing instead of reading that field; see `PLAN.md`). Then stop.

## 5. Output schema

```json
{"doc_uuid": "...", "source_project": "...", "original_filename": "...", "relative_path": "projects/kb-docs/.../file.md", "primary_category": "d-central/mesh-services/connectivity", "secondary_tags": ["d-central/hardware/shi-node"], "abstract": "..."}
```

## 6. Worked example

**Document**: `Algonquin-Courses/MAT8002-Week-1-Preparation-Guide-Decimal-Number-System-md.md` —
front matter shows `source_project: Algonquin Courses`; content is a course prep guide for a
decimal-number-systems electronics/computer-math class (professor contact info, required text,
calculator policy).

```json
{"doc_uuid": "71d6685c-4c5e-457c-b83a-0f6667298756", "source_project": "Algonquin Courses", "original_filename": "MAT8002 Week 1 Preparation Guide - Decimal Number System.md", "relative_path": "projects/kb-docs/Algonquin-Courses/MAT8002-Week-1-Preparation-Guide-Decimal-Number-System-md.md", "primary_category": "d-central/academic-personal", "secondary_tags": [], "abstract": "Week 1 course-prep guide for an Algonquin College electronics/computer-math course covering the decimal number system -- professor contact info, required textbook edition, and calculator policy. No D-Central content."}
```

Why `academic-personal` and not something forced from D-Central's taxonomy: this is genuinely
coursework with zero conceptual overlap with the architecture, same test the conversation
classifier's worked examples apply (`.claude/skills/classify-conversation/SKILL.md` §6) — don't
stretch a classification just because the source project also happens to contain D-Central work
elsewhere. Classify what THIS document is about, not what its project is generally for.

## 7. Guardrails

- **Never invent a taxonomy path** not in §3. Use `d-central/other` if genuinely nothing fits.
- **A document's category is independent of its project's usual theme.** A project can hold both
  core D-Central architecture docs and unrelated coursework/scratch files — classify each
  document by its own content, not by inheriting the project's dominant category (that
  project-level inheritance is exactly the coarse behavior this skill exists to replace).
- **Never write a generic, templated, or reused abstract to go faster**, and never paste raw
  document text with a generic suffix to dodge the validator. Both failure modes already happened
  in the conversation classifier (see `PLAN.md` and `.claude/skills/classify-conversation/SKILL.md`
  §7) and the same mechanical bans apply here (`append_kb_doc_classification.py` /
  `validate_kb_doc_classification.py` reject known boilerplate phrases, first-person
  assistant-reply openers, and duplicate abstracts). A validation rejection means re-read the
  document, never reword to slip past the check.
- **Never re-classify an already-done doc_uuid** — `get_next_kb_doc.py` filters these out.
- **After a full pass, run `python3 scripts/rebuild_knowledge_base_fine.py`** to materialize the
  classified records into `knowledge-base-fine/<category>/<project>/<file>` — this only needs to
  run once at the end (or after any batch, to check progress), not per document.
