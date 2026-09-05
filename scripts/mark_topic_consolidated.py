#!/usr/bin/env python3
"""
Validates a just-written Consolidator output doc against DC-CONSOLIDATOR-
STD-001's required structure (mechanical backstop, same spirit as
validate_kb_doc_classification.py for Stage 3), then records the topic as
done in registry/consolidated-topics.json so scripts/get_next_topic.py skips
it on future runs.

Usage: python3 scripts/mark_topic_consolidated.py <topic-name> <docs/DC-...-RECONCILED-NNN.md>
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY = REPO_ROOT / "registry" / "consolidated-topics.json"
TOPICS_MD = REPO_ROOT / "knowledge-base" / "_topics.md"

REQUIRED_HEADINGS = [
    "## Current understanding",
    "## Provenance",
    "## Unresolved tensions",
    "## Sources consulted",
    "## Consolidation metadata",
]


def get_topic_members(topic_name):
    text = TOPICS_MD.read_text(encoding="utf-8")
    m = re.search(r"^## " + re.escape(topic_name) + r" \((\d+) docs?\)\s*$", text, re.MULTILINE)
    if not m:
        return None
    n = int(m.group(1))
    next_h = re.search(r"^## ", text[m.end():], re.MULTILINE)
    end = m.end() + (next_h.start() if next_h else len(text) - m.end())
    section = text[m.end():end]
    rels = [l.split("](")[0][3:] for l in section.splitlines() if l.startswith("- [")]
    return n, rels


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 scripts/mark_topic_consolidated.py <topic-name> <path-to-consolidated-doc>")

    topic_name, doc_path_arg = sys.argv[1], sys.argv[2]
    doc_path = Path(doc_path_arg)
    if not doc_path.is_absolute():
        doc_path = REPO_ROOT / doc_path
    if not doc_path.exists():
        sys.exit(f"FAIL: consolidated doc not found: {doc_path}")

    text = doc_path.read_text(encoding="utf-8", errors="replace")

    missing_headings = [h for h in REQUIRED_HEADINGS if h not in text]
    if missing_headings:
        sys.exit(f"FAIL: consolidated doc missing required section(s): {missing_headings}")

    result = get_topic_members(topic_name)
    if result is None:
        sys.exit(f"FAIL: topic not found in _topics.md: {topic_name}")
    n, rels = result

    missing_sources = [r for r in rels if r not in text]
    if missing_sources:
        sys.exit(
            f"FAIL: {len(missing_sources)} of {n} topic member path(s) not referenced anywhere in "
            f"the consolidated doc (exhaustiveness requirement, DC-CONSOLIDATOR-STD-001 §2): "
            f"{missing_sources}"
        )

    registry = json.loads(REGISTRY.read_text(encoding="utf-8")) if REGISTRY.exists() else {}
    if topic_name in registry:
        sys.exit(f"FAIL: topic already marked consolidated: {topic_name}")

    registry[topic_name] = {
        "consolidated_doc": str(doc_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "doc_count": n,
    }
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(registry, indent=2, sort_keys=True), encoding="utf-8")
    print(f"OK: marked '{topic_name}' consolidated ({n} docs) -> {doc_path.relative_to(REPO_ROOT)}")
    print(f"Total consolidated so far: {len(registry)}")


if __name__ == "__main__":
    main()
