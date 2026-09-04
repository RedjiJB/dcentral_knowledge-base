#!/usr/bin/env python3
"""
DC-REG-001 builder — processes a Claude.ai data export and uses Claude
Haiku 4.5 to recursively extract a document registry (doc IDs, scope,
status) from every conversation in your history.

Cost note: Haiku 4.5 is $1/$5 per million input/output tokens (as of
Aug 2026 — verify at anthropic.com/pricing before a big run). For a
few hundred conversations this should run a few dollars, not much
more. Use --batch for a 50% discount if you don't need results live
(the Batch API runs asynchronously; not wired up here, but worth
adding if you're processing thousands of chats).

Setup:
    pip install anthropic
    export ANTHROPIC_API_KEY=your_key_here

Usage:
    1. Export your data: claude.ai -> Settings -> Privacy -> Export data
    2. Unzip the download, find the conversations JSON file
    3. python build_registry.py path/to/conversations.json
"""

import json
import sys
import time
import csv
from pathlib import Path
import anthropic

MODEL = "claude-haiku-4-5-20251001"
LOG_EVERY = 10
MAX_CHARS = 180_000  # truncate very long chats: head + tail, not middle

EXTRACTION_PROMPT = """You are scanning ONE conversation from a much larger \
archive to build a document registry. Read the conversation below and \
extract any formal documents, specifications, or named artifacts that \
were created, referenced, or discussed with an identifiable name or ID \
(e.g. "DC-XXX-001" style IDs, or clearly named specs/systems even \
without a formal ID).

Return ONLY a JSON array (no markdown, no preamble, no code fences). \
Each element:
{{
  "doc_id": "DC-XXX-001, or null if there is no formal ID",
  "title": "short title",
  "scope": "one sentence describing what it covers",
  "status": "one of: complete / draft / referenced-only / executed / unclear",
  "category": "best-guess category, e.g. network, identity, finance, security, coursework, personal"
}}

If the conversation contains no identifiable documents or named \
artifacts, return an empty array: []

Conversation:
---
{conversation_text}
---

JSON array only:"""


def load_conversations(path):
    """Load conversations from a Claude data export JSON file.
    Export schema can vary by version -- this handles the common shapes
    and fails loudly with guidance if it doesn't recognize the file."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "conversations" in data:
        return data["conversations"]

    raise ValueError(
        "Unrecognized export schema. Open the JSON in a text editor, "
        "check the top-level structure, and adjust load_conversations() "
        "to match -- the export format has changed between versions."
    )


def flatten_messages(conv):
    """Turn a conversation's message list into plain text."""
    msgs = conv.get("chat_messages") or conv.get("messages") or []
    lines = []
    for m in msgs:
        sender = m.get("sender") or m.get("role") or "unknown"
        text = m.get("text")
        if text is None:
            content = m.get("content", [])
            if isinstance(content, list):
                text = " ".join(
                    b.get("text", "") for b in content if isinstance(b, dict)
                )
            else:
                text = str(content)
        lines.append(f"{sender}: {text}")
    return "\n".join(lines)


def extract_from_conversation(client, conv_text, title):
    if len(conv_text) > MAX_CHARS:
        half = MAX_CHARS // 2
        conv_text = conv_text[:half] + "\n\n[...truncated...]\n\n" + conv_text[-half:]

    prompt = EXTRACTION_PROMPT.format(conversation_text=conv_text)

    resp = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = resp.content[0].text.strip()

    if raw.startswith("```"):
        raw = raw.strip("`")
        if "\n" in raw:
            raw = raw.split("\n", 1)[-1]
        if raw.lower().startswith("json"):
            raw = raw[4:]

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        print(f"  [!] Could not parse response for '{title}' -- skipping. "
              f"Raw (first 200 chars): {raw[:200]}")
        return []


def main():
    if len(sys.argv) != 2:
        print("Usage: python build_registry.py path/to/conversations.json")
        sys.exit(1)

    export_path = Path(sys.argv[1])
    conversations = load_conversations(export_path)
    print(f"Loaded {len(conversations)} conversations from export.")

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

    all_entries = []
    for i, conv in enumerate(conversations, 1):
        title = conv.get("name") or conv.get("title") or f"conversation_{i}"
        text = flatten_messages(conv)
        if not text.strip():
            continue

        entries = extract_from_conversation(client, text, title)
        for e in entries:
            e["source_conversation"] = title
            e["source_updated_at"] = conv.get("updated_at", "")
        all_entries.extend(entries)

        if i % LOG_EVERY == 0:
            print(f"  ...{i}/{len(conversations)} conversations processed, "
                  f"{len(all_entries)} entries found so far")

        time.sleep(0.3)  # light pacing -- raise if you hit rate limits

    out_csv = export_path.parent / "dc_registry_raw.csv"
    fieldnames = ["doc_id", "title", "scope", "status", "category",
                  "source_conversation", "source_updated_at"]
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for e in all_entries:
            writer.writerow({k: e.get(k, "") for k in fieldnames})

    print(f"\nDone. {len(all_entries)} entries written to {out_csv}")
    print("Next: dedupe by doc_id (the same doc often surfaces in multiple "
          "chats), then fold the survivors into DC-REG-001's tables.")


if __name__ == "__main__":
    main()
