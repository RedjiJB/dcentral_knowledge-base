#!/usr/bin/env python3
"""Concatenate every member doc of one _topics.md topic into a single scratch
file, so the Consolidator pass can read a topic in one shot instead of N
separate file reads. Usage:
    python3 scripts/gather_topic_docs.py <topic-name> <output-scratch.md>
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_MD = REPO_ROOT / "knowledge-base" / "_topics.md"


def main():
    topic = sys.argv[1]
    out_path = Path(sys.argv[2]).resolve()
    text = TOPICS_MD.read_text(encoding="utf-8")
    m = re.search(r"^## " + re.escape(topic) + r" \(\d+ docs?\)\s*$", text, re.MULTILINE)
    if not m:
        sys.exit(f"Topic not found: {topic}")
    next_h = re.search(r"^## ", text[m.end():], re.MULTILINE)
    section = text[m.end(): m.end() + (next_h.start() if next_h else len(text) - m.end())]
    rels = [l.split("](")[0][3:] for l in section.splitlines() if l.startswith("- [")]

    with open(out_path, "w", encoding="utf-8") as out:
        for rel in rels:
            full_rel = "knowledge-base/" + rel
            p = REPO_ROOT / full_rel
            out.write(f"\n\n{'='*100}\nSOURCE: {full_rel}\n{'='*100}\n\n")
            if p.exists():
                out.write(p.read_text(encoding="utf-8", errors="replace"))
            else:
                out.write("MISSING FILE\n")
    print(f"{len(rels)} docs gathered -> {out_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
