#!/usr/bin/env python3
"""
Stage 7 item #2 -- forward pointer from each topic-member doc to its Stage 6
consolidated output. Purely mechanical: reads registry/materialized-manifest.json
(built by build_manifest.py, which must be run first) and inserts/updates a
`consolidated_into:` front-matter field on every doc with >=1 topic. A doc
cross-listed in two topics gets a JSON-array-style value with both.

No judgment calls -- this only ever writes what the manifest already says.

Usage: python3 scripts/add_consolidated_into.py
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DIR = REPO_ROOT / "knowledge-base"
MANIFEST_PATH = REPO_ROOT / "registry" / "materialized-manifest.json"

FRONTMATTER_RE = re.compile(r"^(---\n)(.*?\n)(---\n)", re.DOTALL)
EXISTING_FIELD_RE = re.compile(r"^consolidated_into:.*$\n?", re.MULTILINE)


def format_value(consolidated_docs):
    if len(consolidated_docs) == 1:
        return consolidated_docs[0]
    return "[" + ", ".join(consolidated_docs) + "]"


def main():
    if not MANIFEST_PATH.exists():
        sys.exit("FAIL: registry/materialized-manifest.json not found -- run scripts/build_manifest.py first")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    docs = manifest["docs"]

    updated, skipped_no_topic, skipped_unresolved_topic, already_current = 0, 0, 0, 0

    for rel_path, record in docs.items():
        consolidated_docs = record.get("consolidated_docs", [])
        topics = record.get("topics", [])

        if not topics:
            skipped_no_topic += 1
            continue
        if not consolidated_docs:
            # Topic exists but hasn't been consolidated yet -- shouldn't happen post
            # Stage-6-complete, but don't silently invent a pointer if it does.
            skipped_unresolved_topic += 1
            continue

        path = KB_DIR / rel_path
        text = path.read_text(encoding="utf-8", errors="replace")
        m = FRONTMATTER_RE.match(text)
        if not m:
            print(f"WARN: no front matter block, skipping: {rel_path}")
            continue

        new_value = format_value(sorted(set(consolidated_docs)))
        new_field_line = f"consolidated_into: {new_value}\n"

        body = m.group(2)
        if EXISTING_FIELD_RE.search(body):
            existing = EXISTING_FIELD_RE.search(body).group(0).strip()
            if existing == f"consolidated_into: {new_value}":
                already_current += 1
                continue
            body = EXISTING_FIELD_RE.sub(new_field_line, body)
        else:
            body = body + new_field_line

        new_text = m.group(1) + body + m.group(3) + text[m.end():]
        path.write_text(new_text, encoding="utf-8")
        updated += 1

    print(f"Updated {updated} docs with a consolidated_into field.")
    print(f"  {already_current} already current, {skipped_no_topic} not in any topic, {skipped_unresolved_topic} in an unconsolidated topic")


if __name__ == "__main__":
    main()
