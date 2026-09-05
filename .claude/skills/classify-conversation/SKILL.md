---
name: classify-conversation
description: Classify the next unclassified D-Central conversation into the fixed taxonomy, extract cross-links, write an abstract, and append the result to conversations/_classified.jsonl. Use when running the Stage 2 classification pass over the conversation export.
---

# Classify Conversation (Stage 2 classifier agent)

## 1. Role

You are classifying D-Central conversations, one at a time internally, into a fixed category
taxonomy, extracting which document IDs each links to, and writing a short abstract. This is Stage 2
of the knowledge-base pipeline described in `PLAN.md` and the `standards/DC-*-STD-001.md` docs — the
per-conversation classification pass that `scripts/classify_docs.py` (Stage 3, project-level) stood
in for by hand.

**Batch size: process up to 40 conversations per invocation**, looping through steps 1-7 of §4
internally, then stop and report a summary (§8) — don't process only one and wait to be told
"keep going" every single time; that doesn't scale to 743 conversations. Still stop before 40 if
`get_next_conversation.py` reports nothing left.

**This ceiling has moved three times, and it's back down for a serious reason.** It started at 20,
dropped to 10 after a real failure (a 20-item batch degraded to an identical copy-pasted abstract for
17 conversations straight, including a 269KB white paper misfiled as "no D-Central content"), went
back up to 40 once the mechanical backstop held across several clean batches — then a batch at 40
degraded again, WORSE than before: after getting a validation rejection for a boilerplate phrase, it
started pasting the first ~150 characters of raw conversation text with a new generic suffix
("Portfolio/technical work.") specifically to slip past the exact-phrase filter. 40 of 41 records in
that batch did this, including several major D-Central documents ("D Central Core Build Plan and
Deliverables," "Building an Investor Pitch Deck for a Mesh Network") misfiled with junk abstracts.
That is not a speed shortcut, that is circumventing a validation check that exists specifically to
catch bad output — a materially worse failure than the first one, which is why the ceiling dropped
back to 10 rather than to 20. Both validators now also reject first-person assistant-reply-style
openers ("I'll help you...", "I see you have...") as a second, independent detection signal — but
treat any validation rejection as "go re-read the conversation," never as "find different wording."

**Raised back to 40 when running directly in a supervised session (not a separately-invoked,
unsupervised batch)** — the failure above happened specifically because a batch ran unattended across
many tool calls with no one reading the output until it finished. When the person running this skill
is present in the same conversation and reviewing output as it goes, the batch ceiling is less about
"how much can go wrong before anyone notices" and more just a throughput number. Still: if you get a
validation rejection during a supervised run, stop and actually re-read — being watched doesn't change
what the correct response to a rejection is.

Done = up to 40 JSON lines appended to `conversations/_classified.jsonl` via the safe append path in
§4 step 6 — never construct a shell command with the record's JSON inlined into it (see the
guardrail in §7 on why).

## 2. Scoped context — what to read, what NOT to read

- **Run `python3 scripts/get_next_conversation.py` first.** It writes the next unclassified
  conversation's title/summary/excerpt/doc-IDs to `conversations/_scratch/current.json` — a few KB.
- **Read only `conversations/_scratch/current.json`.** Never read `raw-export/conversations/conversations.json`
  directly — it's 320MB, and reading it defeats the entire scoped-context premise this pipeline runs
  on. If `get_next_conversation.py` exits 1 ("nothing left to classify"), stop — the pass is done.
- **Running more than one classification session at the same time**: pass `--session <name>` to
  `get_next_conversation.py` (e.g. `--session a` in one session, `--session b` in the other). Each
  session then gets its own scratch file (`current_<name>.json` instead of the shared `current.json`)
  and the script claims whichever uuid it hands out (in `conversations/_scratch/_claims.json`, TTL
  20 min) so the other session's next call skips it instead of also picking it. Without distinct
  `--session` values, two concurrent runs will repeatedly grab the same conversation and clobber each
  other's scratch file — pass matching `<path-to-record.json>` names to `append_classification.py`
  too (e.g. `pending_a.json` / `pending_b.json`) so the two sessions' in-progress records don't
  overwrite each other either.
- **Read the taxonomy in §3 below.** Do not read other categories' `_topics.md` or the full
  `knowledge-base/` tree — you don't need it, and loading it just for one classification call is the
  same "context dump" failure mode this whole pipeline exists to avoid.
- You do NOT need `conversations/_classified.jsonl`'s prior entries to do this task — the fixed
  taxonomy below is what keeps classifications consistent, not looking at what you did last time.

## 3. Fixed taxonomy — pick from this list, do not invent new paths

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

This list is fixed on purpose — per DC-TOPIC-SYNTH-STD-001 §8's "keyword-clustering instead of
subject-clustering" failure mode, letting each call invent its own category name produces drift
(conversation 40 calls something "networking," conversation 41 calls the same thing
"connectivity-layer"). Picking from one fixed list keeps 743 independent calls comparable.

**`platform-scaffolding` vs `other`**: use `platform-scaffolding` for README/setup/repo-structure
conversations that explicitly span the whole platform (agent + mesh + blockchain + identity + AI +
DAO all mentioned together, e.g. as a directory tree or module list) — this was added after the
first real batches showed this is a recurring, specific pattern, not a one-off. Reserve `other` for
things that genuinely don't fit any bucket at all, including this one.

## 4. Numbered steps (repeat 1-7 up to 40 times per invocation, then do step 8 once)

1. Run `python3 scripts/get_next_conversation.py`. If it exits 1 (nothing left), stop the loop early
   and go straight to step 8 — don't treat this as an error.
2. Read `conversations/_scratch/current.json`.
3. Pick exactly one `primary_category` from §3 — the single best-fit path.
4. Pick 0-3 `secondary_tags` from §3 — other categories this conversation also genuinely touches.
   Leave empty if it's cleanly single-topic; don't pad this list.
5. Build `links_to` from the `extracted_doc_ids` field already in the scratch file — these are the
   doc IDs this conversation appears to extend, revise, or reference. Don't invent doc IDs not
   already in that list. Write a 2-3 sentence `abstract` — specific enough that someone deciding
   whether to open the conversation can tell from the abstract alone, not a generic restatement of
   the title. If two conversations look similar (same underlying issue, different day), still give
   each abstract the specific detail that actually differs — don't copy-paste one abstract onto both.
6. **Write the record safely, then append it — never inline the JSON into a shell command.**
   - Use the Write tool to save the record (matching the schema in §5, using the `uuid`/`title`/
     `created_at` already in the scratch file) to `conversations/_scratch/pending.json`.
   - Run `python3 scripts/append_classification.py conversations/_scratch/pending.json` to validate
     and append it to `conversations/_classified.jsonl`.
   - This two-step path exists because inlining a record's JSON directly into a shell command (e.g.
     PowerShell `Add-Content -Value '...'`) breaks unpredictably on abstracts containing quotes,
     backslashes, or literal sequences like `\n\nHuman:` — real failures already hit this. The Write
     tool has no shell-quoting problem; let it carry the content instead.
   - If `append_classification.py` exits non-zero, read its error, fix the record in
     `pending.json`, and re-run it — don't just skip the conversation.
7. Go back to step 1 for the next conversation, up to 40 total this invocation.
8. **Report a summary, not per-item narration**: how many were classified this invocation, and a
   one-line list of title → primary_category for each one processed. **For the "how many remain" and
   "total classified so far" numbers, use ONLY the `progress` field from the most recent
   `conversations/_scratch/current.json` you read (e.g. `"42/743 (701 remaining after this one)"`) —
   never estimate, guess, or calculate a cumulative total yourself.** This already went wrong twice:
   one invocation reported "73/743 total classified" when the real number was 17, another reported
   "93/743" when the real number was 26 — in both cases the actual remaining-count was roughly right
   (it came from the reliable `progress` field) but the "total classified" figure was a separate,
   wrong, self-generated number. If you're not looking at the `progress` field for a number you're
   about to report, don't report that number. Then stop — the person running this decides whether to
   invoke the skill again.

## 5. Output schema

Append exactly this shape as one JSON line (no pretty-printing, one line per record):

```json
{"uuid": "...", "title": "...", "created_at": "...", "extracted_doc_ids": ["DC-XXX-001"], "primary_category": "d-central/mesh-services/connectivity", "secondary_tags": ["d-central/hardware/shi-node"], "links_to": ["DC-TAXONOMY-008"], "abstract": "..."}
```

## 6. Worked examples

These are the first three real conversations classified by this skill (uuids 1-3 of 743), kept as
worked examples because they demonstrate a real edge case, not a manufactured one: two of the three
are near-duplicate conversations about the same underlying problem, and each still needs a distinct,
specific abstract rather than a copy-pasted one.

**Example 1** — title: "Creating Custom iPhone Shortcuts", excerpt is a personal request for iPhone
Shortcuts automations (morning routine, sunrise routine).

```json
{"uuid": "cb4f9448-d4db-44fe-8c6b-a5aceff7d0db", "title": "Creating Custom iPhone Shortcuts", "created_at": "2025-03-10T03:03:28.457417Z", "extracted_doc_ids": [], "primary_category": "d-central/academic-personal", "secondary_tags": [], "links_to": [], "abstract": "Personal request for iPhone Shortcuts automations (morning routine, sunrise routine). No D-Central content."}
```

**Example 2** — title: "Troubleshooting SSH Connection Timeout to Azure VM", excerpt is a personal/work
Azure VM SSH connection timeout, diagnosing NSG rules, firewall, and dynamic IP.

```json
{"uuid": "d78e87d5-b525-4e2e-a478-27f032d9f37d", "title": "Troubleshooting SSH Connection Timeout to Azure VM", "created_at": "2025-03-11T08:49:59.782833Z", "extracted_doc_ids": [], "primary_category": "d-central/academic-personal", "secondary_tags": [], "links_to": [], "abstract": "Troubleshooting an SSH connection timeout to a personal/work Azure VM (network security group, firewall, dynamic IP checks). No D-Central content."}
```

**Example 3** — title: "Troubleshooting SSH Access to Azure VM", a DIFFERENT conversation than Example
2, one day later, same VM, but a different failure mode (permission-denied / wrong username, not a
timeout) and further into it, a "what can I do with this VM" follow-up.

```json
{"uuid": "648dab5c-c6ae-43d7-91c5-c9788276ea80", "title": "Troubleshooting SSH Access to Azure VM", "created_at": "2025-03-12T09:24:11.031957Z", "extracted_doc_ids": [], "primary_category": "d-central/academic-personal", "secondary_tags": [], "links_to": [], "abstract": "Fixing SSH key-permission and username errors to access a personal Azure VM, then a general orientation on what to do with the VM once connected. No D-Central content."}
```

Why all three get `academic-personal`: none contain D-Central content — this mirrors the real corpus
finding that some conversations genuinely have zero conceptual overlap with the architecture (see
`CROSS-POLLINATION-FINDINGS.md`'s `academic-training` category, which found the same thing). Don't
force a stretch classification just because a conversation involves technical work — "technical" and
"D-Central-related" are not the same test.

Why examples 2 and 3 get DIFFERENT abstracts despite being about the same VM one day apart: example 2
is a connection *timeout* (network/firewall-layer problem), example 3 is a permission *denial* with a
different root cause (wrong username) that gets fixed mid-conversation, plus new content afterward (a
"what can I do with this VM" orientation). A lazy classification would copy-paste one abstract across
both since they look similar at a glance — the actual content differs enough that they need distinct
abstracts. If you find yourself writing near-identical abstracts for two different UUIDs, that's a
signal to re-read the excerpt rather than assume they're duplicates (a real duplicate would have the
same UUID, and `get_next_conversation.py` already filters those out).

**A hypothetical example, for contrast** — showing what a real D-Central-content conversation looks
like, since the three real ones above happened to all be personal/unrelated: a conversation titled
"D-Central ISP implementation in Haiti" discussing MeshISP network architecture and DID-based
universal WiFi access would get:

```json
{"primary_category": "d-central/mesh-services/connectivity", "secondary_tags": ["d-central/haiti-diaspora", "d-central/core/identity"], "links_to": ["DC-MESHISP-ARCH-001"], "abstract": "Designs the full MeshISP network architecture for a Haiti pilot, correcting an early assumption to make WiFi access identity-bound (device-DID to person-DID to subscription VC) rather than tied to the household router, so a person's service follows them across any CPE in the mesh."}
```

`haiti-diaspora` is a secondary tag here, not primary — the deployment target isn't the core subject,
the identity-bound access design is.

## 7. Guardrails

- **Never invent a taxonomy path** not listed in §3. If genuinely nothing fits, use `d-central/other`
  — that's a valid, honest answer, not a failure.
- **Never read `conversations.json` directly.** If you find yourself about to Read/Grep that file,
  stop — that means `get_next_conversation.py` wasn't run, or something is wrong with the scratch
  file. Fix that instead of working around the scoping.
- **Never re-classify an already-done UUID.** `get_next_conversation.py` already filters these out —
  if you're ever handed a UUID and asked to classify it a second time, that's a signal something
  upstream is wrong, not a reason to silently overwrite the old record.
- **Don't pad `secondary_tags` or `links_to`** to look thorough — an empty list is the correct output
  for a single-topic conversation with no doc-ID mentions. Padding these produces exactly the kind of
  false cross-links `DC-TOPIC-SYNTH-STD-001` warns against.
- **Never inline a classification record's JSON into a shell command.** Always write it to
  `conversations/_scratch/pending.json` with the Write tool first, then append via
  `scripts/append_classification.py`. A shell one-liner with the record's content embedded in it
  (e.g. `Add-Content -Value '{...}'`) breaks unpredictably on real content — quotes, backslashes, or
  a literal `\n\nHuman:` sequence in an abstract have already caused real failures this way.
- **40 conversations per invocation is a ceiling, not a target.** Stop early (fewer than 40) the
  moment `get_next_conversation.py` reports nothing left — don't pad the batch or wait for a full 10
  before reporting. The scoped-context guarantee (one conversation's data in view at a time) still
  holds within a batch — you're repeating the same one-at-a-time read/classify/write cycle, just
  without stopping to ask permission between each one.
- **Never write a generic, templated, or reused abstract to go faster.** This already happened once:
  a batch run wrote the identical placeholder "Technical work on development and troubleshooting. No
  D-Central content identified." for 17 conversations in a row instead of reading each one, silently
  misclassifying a 269KB white paper on D-Central's full architecture as having "no D-Central
  content." Both `append_classification.py` and the `PostToolUse` hook now mechanically reject known
  boilerplate phrases and any abstract that's identical to another record's — but don't rely on that
  backstop; it exists to catch a mistake, not to license making one. If a batch is taking a long time,
  that's expected — reading each conversation properly takes real effort per item. Slowing down and
  reporting fewer than the batch ceiling done is always correct; silently switching to a shortcut is
  never correct.
- **If `append_classification.py` rejects a record, the correct response is to re-read the
  conversation, not to reword the abstract just enough to slip past the check.** This happened: after
  getting rejected for the boilerplate phrase above, a later run started pasting the first ~150
  characters of the raw conversation excerpt and appending a new generic suffix ("Portfolio/technical
  work.") instead of writing an actual summary — 40 of 41 records in that batch did this, including
  several that were obviously major D-Central documents ("D Central Core Build Plan and
  Deliverables," "Building an Investor Pitch Deck for a Mesh Network") misfiled with junk abstracts.
  A validation rejection is telling you the abstract wasn't real — the fix is to go read the excerpt
  in `conversations/_scratch/current.json` and describe what it's actually about, never to find
  wording that technically avoids the specific banned phrase while still not being a real summary.
  Both validators now also reject abstracts that open with first-person assistant-reply phrasing
  ("I'll help you...", "I see you have...", "Here's a comprehensive...") as a second, independent
  signal for this same failure — but again, the check existing is not permission to find a new way
  around it.
- **A long title alone is a strong signal, not proof.** Titles like "D Central: Building a
  Decentralized Ecosystem" or "Verifying D-Central-MVP Project Structure" are very likely real
  D-Central content — if you find yourself about to classify something with an obviously D-Central
  title as `academic-personal` or `other`, that's a moment to actually read the excerpt more
  carefully before deciding, not a coincidence to wave through.
