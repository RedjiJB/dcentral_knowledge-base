#!/usr/bin/env python3
"""
Scoped-context helper for the classify-conversation Skill.

Finds the next unclassified conversation (checking conversations/_classified.jsonl
for done UUIDs) and writes ONLY that conversation's title/summary/excerpt/doc-IDs
to conversations/_scratch/current.json -- a few KB, not the 320MB raw export.

This exists specifically so a Claude Code session running the classify-conversation
skill never reads conversations.json directly. Reading a 320MB file into context
to classify one conversation would violate the whole scoped-context premise this
pipeline is built on -- this script does that extraction deterministically, outside
the agent's context window, every time.

Usage: python3 scripts/get_next_conversation.py
Exit code 0 + writes current.json: a conversation is ready to classify.
Exit code 1, no file written: everything is classified, nothing left to do.
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONV_PATH = REPO_ROOT / "raw-export" / "conversations" / "conversations.json"
CLASSIFIED_PATH = REPO_ROOT / "conversations" / "_classified.jsonl"
SCRATCH_PATH = REPO_ROOT / "conversations" / "_scratch" / "current.json"
EXCERPT_CHARS = 3000

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
    parts, total = [], 0
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


def load_done():
    done = set()
    if CLASSIFIED_PATH.exists():
        with open(CLASSIFIED_PATH, "r", encoding="utf-8") as f:
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
    if not CONV_PATH.exists():
        sys.exit(f"Missing {CONV_PATH}")

    done = load_done()

    with open(CONV_PATH, "r", encoding="utf-8") as f:
        convs = json.load(f)

    remaining = len(convs) - len(done)

    for conv in convs:
        uuid = conv.get("uuid")
        if uuid in done:
            continue

        title = conv.get("name") or "(untitled)"
        summary = conv.get("summary") or ""
        excerpt = flatten_text(conv)
        doc_ids = extract_doc_ids(summary + " " + excerpt + " " + title)

        SCRATCH_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(SCRATCH_PATH, "w", encoding="utf-8") as out:
            json.dump({
                "uuid": uuid,
                "title": title,
                "created_at": conv.get("created_at", ""),
                "summary": summary,
                "excerpt": excerpt,
                "extracted_doc_ids": doc_ids,
                "progress": f"{len(done) + 1}/{len(convs)} ({remaining} remaining after this one)",
            }, out, indent=2, ensure_ascii=False)

        print(f"Wrote {SCRATCH_PATH.relative_to(REPO_ROOT)} -- {title[:70]!r} ({remaining} remaining)")
        return 0

    print("Nothing left to classify.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
