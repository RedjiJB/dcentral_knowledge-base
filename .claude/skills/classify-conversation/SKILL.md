---
name: classify-conversation
description: Classify the next unclassified D-Central conversation into the fixed taxonomy, extract cross-links, write an abstract, and append the result to conversations/_classified.jsonl. Use when running the Stage 2 classification pass over the conversation export.
---

# Classify Conversation (Stage 2 classifier agent)

## 1. Role

You are classifying ONE D-Central conversation at a time into a fixed category taxonomy, extracting
which document IDs it links to, and writing a short abstract. This is Stage 2 of the knowledge-base
pipeline described in `PLAN.md` and the `standards/DC-*-STD-001.md` docs — the per-conversation
classification pass that `scripts/classify_docs.py` (Stage 3, project-level) stood in for by hand.

Done = one JSON line appended to `conversations/_classified.jsonl`, matching the schema in §5.

## 2. Scoped context — what to read, what NOT to read

- **Run `python3 scripts/get_next_conversation.py` first.** It writes the next unclassified
  conversation's title/summary/excerpt/doc-IDs to `conversations/_scratch/current.json` — a few KB.
- **Read only `conversations/_scratch/current.json`.** Never read `raw-export/conversations/conversations.json`
  directly — it's 320MB, and reading it defeats the entire scoped-context premise this pipeline runs
  on. If `get_next_conversation.py` exits 1 ("nothing left to classify"), stop — the pass is done.
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
d-central/security                   (OpenSecure suite, OS-PACS/GUARDIAN/PATROL/SENTINEL/CONCIERGE)
d-central/academic-personal          (coursework, career, personal/non-D-Central content)
d-central/other                      (genuinely doesn't fit above -- last resort, use sparingly)
```

This list is fixed on purpose — per DC-TOPIC-SYNTH-STD-001 §8's "keyword-clustering instead of
subject-clustering" failure mode, letting each call invent its own category name produces drift
(conversation 40 calls something "networking," conversation 41 calls the same thing
"connectivity-layer"). Picking from one fixed list keeps 743 independent calls comparable.

## 4. Numbered steps

1. Run `python3 scripts/get_next_conversation.py`. If it exits 1, stop — nothing left to do.
2. Read `conversations/_scratch/current.json`.
3. Pick exactly one `primary_category` from §3 — the single best-fit path.
4. Pick 0-3 `secondary_tags` from §3 — other categories this conversation also genuinely touches.
   Leave empty if it's cleanly single-topic; don't pad this list.
5. Build `links_to` from the `extracted_doc_ids` field already in the scratch file — these are the
   doc IDs this conversation appears to extend, revise, or reference. Don't invent doc IDs not
   already in that list.
6. Write a 2-3 sentence `abstract` of what the conversation actually covers — specific enough that
   someone deciding whether to open it can tell from the abstract alone, not a generic restatement
   of the title.
7. Append one line to `conversations/_classified.jsonl` matching the schema in §5 exactly (use the
   `uuid`, `title`, `created_at` already in the scratch file — don't retype them from memory).
8. Report the result in one line (title -> primary_category) and stop. Do not automatically loop to
   the next conversation — the person running this decides whether to invoke the skill again (or set
   up a loop around it). One invocation classifies one conversation.

## 5. Output schema

Append exactly this shape as one JSON line (no pretty-printing, one line per record):

```json
{"uuid": "...", "title": "...", "created_at": "...", "extracted_doc_ids": ["DC-XXX-001"], "primary_category": "d-central/mesh-services/connectivity", "secondary_tags": ["d-central/hardware/shi-node"], "links_to": ["DC-TAXONOMY-008"], "abstract": "..."}
```

## 6. Worked examples

**Example 1** — title: "D-Central ISP implementation in Haiti", excerpt discusses MeshISP network
architecture, cellular/router identity binding, DID-based universal WiFi access.

```json
{"uuid": "fc99aa3d-...", "title": "D-Central ISP implementation in Haiti", "created_at": "2025-08-23T05:28:35Z", "extracted_doc_ids": ["DC-MESHISP-ARCH-001"], "primary_category": "d-central/mesh-services/connectivity", "secondary_tags": ["d-central/haiti-diaspora", "d-central/core/identity"], "links_to": ["DC-MESHISP-ARCH-001"], "abstract": "Designs the full MeshISP network architecture for a Haiti pilot, correcting an early assumption to make WiFi access identity-bound (device-DID to person-DID to subscription VC) rather than tied to the household router, so a person's service follows them across any CPE in the mesh."}
```

Why this classification: the conversation's core subject is mesh connectivity/access design, not
Haiti policy generally — `haiti-diaspora` is a secondary tag (the deployment target), not primary,
because the technical content (identity-bound WiFi access) is the actual thing being designed.

**Example 2** — title: "CompTIA A+ Week 3 assignment help", excerpt is coursework Q&A, no D-Central
content.

```json
{"uuid": "...", "title": "CompTIA A+ Week 3 assignment help", "created_at": "...", "extracted_doc_ids": [], "primary_category": "d-central/academic-personal", "secondary_tags": [], "links_to": [], "abstract": "Coursework help for a CompTIA A+ certification assignment covering hardware troubleshooting basics. No D-Central content."}
```

Why this classification: genuinely unrelated coursework gets `academic-personal`, not forced into a
D-Central category — this mirrors the real corpus finding that `academic-training` correctly has
zero conceptual overlap with the rest of the architecture (see `CROSS-POLLINATION-FINDINGS.md`).

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
- **One conversation per invocation.** Don't try to batch multiple conversations into one skill run —
  that's what breaks the scoped-context guarantee this whole design depends on.
