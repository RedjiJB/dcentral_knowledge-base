#!/usr/bin/env python3
"""
Scoped-context helper for Stage 6 Consolidator batch runs (mirrors
get_next_kb_doc.py's pattern for Stage 3): hands out the next not-yet-
consolidated topic from knowledge-base/_topics.md, smallest doc-count first
so batches make even progress before the large (10+ doc) topics are all
that's left.

Writes the full concatenated text of every member doc to
conversations/_scratch/current_topic.md, and metadata (topic name, doc
count, member paths, progress) to conversations/_scratch/current_topic.json.

A topic already in registry/consolidated-topics.json is skipped. Exits 1
when nothing is left.

Usage: python3 scripts/get_next_topic.py
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_MD = REPO_ROOT / "knowledge-base" / "_topics.md"
REGISTRY = REPO_ROOT / "registry" / "consolidated-topics.json"
SCRATCH_MD = REPO_ROOT / "conversations" / "_scratch" / "current_topic.md"
SCRATCH_JSON = REPO_ROOT / "conversations" / "_scratch" / "current_topic.json"


def load_registry():
    if REGISTRY.exists():
        return json.loads(REGISTRY.read_text(encoding="utf-8"))
    return {}


def parse_topics(text):
    topics = []
    for m in re.finditer(r"^## (.+?) \((\d+) docs?\)\s*$", text, re.MULTILINE):
        name = m.group(1)
        n = int(m.group(2))
        next_h = re.search(r"^## ", text[m.end():], re.MULTILINE)
        end = m.end() + (next_h.start() if next_h else len(text) - m.end())
        section = text[m.end():end]
        rels = [l.split("](")[0][3:] for l in section.splitlines() if l.startswith("- [")]
        topics.append((name, n, rels))
    return topics


def main():
    text = TOPICS_MD.read_text(encoding="utf-8")
    all_topics = parse_topics(text)
    registry = load_registry()

    remaining = [t for t in all_topics if t[0] not in registry]
    if not remaining:
        print("No topics left to consolidate.")
        sys.exit(1)

    remaining.sort(key=lambda t: t[1])  # smallest doc-count first
    name, n, rels = remaining[0]

    SCRATCH_MD.parent.mkdir(parents=True, exist_ok=True)
    with open(SCRATCH_MD, "w", encoding="utf-8") as out:
        out.write(f"# Topic: {name} ({n} docs)\n")
        for rel in rels:
            full_rel = "knowledge-base/" + rel
            p = REPO_ROOT / full_rel
            out.write(f"\n\n{'='*100}\nSOURCE: {full_rel}\n{'='*100}\n\n")
            if p.exists():
                out.write(p.read_text(encoding="utf-8", errors="replace"))
            else:
                out.write("MISSING FILE\n")

    done = len(registry)
    total = len(all_topics)
    meta = {
        "topic": name,
        "doc_count": n,
        "members": ["knowledge-base/" + r for r in rels],
        "progress": f"{done}/{total} topics consolidated so far, this will be #{done + 1}",
        "remaining_after_this": len(remaining) - 1,
    }
    SCRATCH_JSON.write_text(json.dumps(meta, indent=2), encoding="utf-8")

    print(f"Next topic: {name} ({n} docs)")
    print(f"Progress: {meta['progress']}")
    print(f"Remaining after this one: {meta['remaining_after_this']}")


if __name__ == "__main__":
    main()
