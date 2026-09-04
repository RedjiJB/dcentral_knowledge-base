#!/usr/bin/env python3
"""
Stage 2: agent-based per-conversation classification.

This is the actual "organize with an agent" step that classify_docs.py (Stage 3
in this repo's numbering, but the same job as the design's "Stage 2") never
did -- that script used a hand-written 33-entry project->category lookup table,
which only worked because there were few enough Projects to map by hand. This
script does the real thing: reads EACH of the 743 conversations individually
and asks a cheap model (Haiku) to place it in the fixed taxonomy skeleton,
extract cross-links, and write a short abstract.

Run this yourself with an ANTHROPIC_API_KEY set -- it makes ~743 API calls
(cheap on Haiku, but real cost and real time, so it's not run automatically
as part of the rest of this pipeline):

    pip install anthropic
    export ANTHROPIC_API_KEY=sk-...
    python3 scripts/classify_conversations_agent.py

Resumable: writes one JSON line per conversation to
conversations/_classified.jsonl as it goes, and skips any uuid already in
that file on a re-run -- safe to Ctrl-C and restart.

Scoped-context discipline (per 04-context-engineering-standards.md, applied
here rather than to mesh-ai agents): each call gets ONE conversation's
title/summary/excerpt/extracted-doc-IDs plus the fixed taxonomy skeleton --
never the other 742 conversations, never the full corpus. The taxonomy is
fixed (not agent-invented) specifically so conversation N and conversation
N+1 don't create two slightly-different category names for the same thing --
exactly the failure mode DC-TOPIC-SYNTH-STD-001 SS8 warns about for automated
topic naming.
"""

import json
import os
import re
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONV_PATH = REPO_ROOT / "raw-export" / "conversations" / "conversations.json"
OUT_PATH = REPO_ROOT / "conversations" / "_classified.jsonl"
MODEL = "claude-haiku-4-5-20251001"
EXCERPT_CHARS = 3000  # scoped context, not a full-conversation dump

# Fixed taxonomy skeleton -- the agent PICKS from this, it does not invent
# new top-level branches. Keeps classification consistent across all 743
# calls instead of drifting category names conversation-to-conversation.
TAXONOMY = """
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
d-central/security                   (OpenSecure suite, OS-PACS/GUARDIAN/PATROL/SENTINEL/CONCIERGE, identity/credentialing security)
d-central/academic-personal          (coursework, career, personal/non-D-Central content)
d-central/other                      (genuinely doesn't fit above -- use sparingly, last resort)
""".strip()

SYSTEM_PROMPT = f"""You are a document classifier for the D-Central knowledge base. You will be given
ONE conversation's title, summary/excerpt, and any document IDs already found in it. Your job:

1. Pick exactly ONE primary_category from the fixed taxonomy below -- the single best-fit path.
   Do not invent a new category path. If genuinely nothing fits, use "d-central/other".
2. List 0-3 secondary_tags -- other categories from the same taxonomy this conversation also
   touches, if any. Leave empty if it's cleanly single-topic.
3. List links_to -- any doc IDs (DC-*, OS-*) mentioned that this conversation appears to extend,
   revise, or reference. Use exactly the doc IDs given to you; do not invent new ones.
4. Write a 2-3 sentence abstract of what this conversation actually covers.

Fixed taxonomy (pick primary_category and secondary_tags only from these paths):
{TAXONOMY}

Output ONLY a JSON object, no other text, matching this exact schema:
{{"primary_category": "<one path from the taxonomy>", "secondary_tags": ["<path>", ...], "links_to": ["<doc id>", ...], "abstract": "<2-3 sentences>"}}
"""

DOC_ID_PATTERNS = [
    re.compile(r"\bDC-[A-Z0-9]+-\d{3}\b"),
    re.compile(r"\bOS-[A-Z0-9]+-\d{3}\b"),
]


def extract_doc_ids(text):
    found = set()
    for pat in DOC_ID_PATTERNS:
        found.update(pat.findall(text))
    return sorted(found)


def flatten_text(conv, limit=EXCERPT_CHARS):
    parts = []
    total = 0
    for m in conv.get("chat_messages", []):
        content = m.get("content", [])
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    t = block.get("text", "")
                    if t:
                        parts.append(t)
                        total += len(t)
        if total >= limit:
            break
    return "\n".join(parts)[:limit]


def load_done(out_path):
    done = set()
    if out_path.exists():
        with open(out_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    done.add(json.loads(line)["uuid"])
                except Exception:
                    pass
    return done


def main():
    try:
        import anthropic
    except ImportError:
        sys.exit("Missing dependency. Run: pip install anthropic")

    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("Set ANTHROPIC_API_KEY before running this script.")

    if not CONV_PATH.exists():
        sys.exit(f"Missing {CONV_PATH} -- unzip conversations-000.zip into raw-export/conversations/ first")

    OUT_PATH.parent.mkdir(exist_ok=True)
    client = anthropic.Anthropic()

    print("Loading conversations.json...")
    with open(CONV_PATH, "r", encoding="utf-8") as f:
        convs = json.load(f)
    print(f"Loaded {len(convs)} conversations.")

    done = load_done(OUT_PATH)
    print(f"{len(done)} already classified, resuming.")

    with open(OUT_PATH, "a", encoding="utf-8") as out:
        for i, conv in enumerate(convs, 1):
            uuid = conv.get("uuid")
            if uuid in done:
                continue

            title = conv.get("name") or "(untitled)"
            summary = conv.get("summary") or ""
            excerpt = flatten_text(conv)
            doc_ids = extract_doc_ids(summary + " " + excerpt + " " + title)

            user_content = (
                f"Title: {title}\n"
                f"Summary: {summary or '(none provided)'}\n"
                f"Extracted doc IDs found in this conversation: {doc_ids or '(none)'}\n"
                f"Excerpt (first {EXCERPT_CHARS} chars of conversation text):\n{excerpt}"
            )

            try:
                response = client.messages.create(
                    model=MODEL,
                    max_tokens=500,
                    system=SYSTEM_PROMPT,
                    messages=[{"role": "user", "content": user_content}],
                )
                raw = response.content[0].text.strip()
                # strip markdown code fences if the model adds them anyway
                raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw)
                parsed = json.loads(raw)
            except Exception as e:
                print(f"  [{i}/{len(convs)}] FAILED {uuid} ({title[:50]}): {e}")
                continue

            record = {
                "uuid": uuid,
                "title": title,
                "created_at": conv.get("created_at", ""),
                "extracted_doc_ids": doc_ids,
                **parsed,
            }
            out.write(json.dumps(record, ensure_ascii=False) + "\n")
            out.flush()

            if i % 25 == 0:
                print(f"  [{i}/{len(convs)}] classified: {title[:60]!r} -> {parsed.get('primary_category')}")

            time.sleep(0.1)  # light rate-limit courtesy, adjust to your tier

    print(f"Done. Results in {OUT_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
