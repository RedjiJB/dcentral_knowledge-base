#!/usr/bin/env python3
"""
Stage 7 item #3 -- one materialized manifest tying Stage 3/4/5/6 decisions
together per document, so downstream consumers (rebuild_index.py,
add_consolidated_into.py, and eventually Stage 8's graph build) read one
source of truth instead of re-deriving it independently.

Inputs (read-only):
  - knowledge-base/_kb_doc_classified.jsonl  (Stage 3: category, project, doc_uuid)
  - knowledge-base/_topics.md                (Stage 5: topic -> member doc paths)
  - registry/consolidated-topics.json        (Stage 6: topic -> consolidated doc)
  - each doc's own front matter               (Stage 4: dedup/supersession status)

Output: registry/materialized-manifest.json
  {
    "generated_at": "...",
    "counts": {...},
    "docs": {
      "<path relative to knowledge-base/, posix>": {
        "category": "...", "project": "...", "doc_uuid": "...",
        "dedup_status": "canonical" | "superseded" | "disputed",
        "duplicate_of" / "superseded_by": "..." (if applicable),
        "topic": "..." | null,
        "consolidated_doc": "docs/DC-...-RECONCILED-NNN.md" | null
      }, ...
    }
  }

Usage: python3 scripts/build_manifest.py
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DIR = REPO_ROOT / "knowledge-base"
KB_ROOT = KB_DIR / "d-central"
CLASSIFIED_PATH = KB_DIR / "_kb_doc_classified.jsonl"
TOPICS_MD = KB_DIR / "_topics.md"
CONSOLIDATED_JSON = REPO_ROOT / "registry" / "consolidated-topics.json"
OUT_PATH = REPO_ROOT / "registry" / "materialized-manifest.json"

FRONTMATTER_RE = re.compile(r"^---\n(.*?\n)---\n", re.DOTALL)
FIELD_RE = re.compile(r'^(\w+):\s*"?(.*?)"?\s*$')
TOPIC_HEADING_RE = re.compile(r"^##\s+(.+?)\s+\((\d+)\s+docs?\)\s*$")
TOPIC_LINK_RE = re.compile(r"^-\s*\[.*?\]\(\./(.+?)\)\s*$")


def parse_frontmatter(path: Path) -> dict:
    """Best-effort key: value parse. Duplicate keys (e.g. two `topic:` lines,
    the first raw, the second the resolved slug) keep the LAST occurrence,
    since that matches this corpus's convention of quoting the resolved value."""
    text = path.read_text(encoding="utf-8", errors="replace")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fields = {}
    for line in m.group(1).splitlines():
        fm = FIELD_RE.match(line)
        if fm:
            fields[fm.group(1)] = fm.group(2)
    return fields


def load_classified() -> dict:
    """doc_uuid -> {relative_path, primary_category, source_project} from Stage 3 output."""
    by_path = {}
    if not CLASSIFIED_PATH.exists():
        return by_path
    for line in CLASSIFIED_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        rel = rec.get("relative_path", "")
        by_path[rel] = rec
    return by_path


def load_topics_md() -> dict:
    """doc path (relative to knowledge-base/, posix) -> list of topic names.
    A doc can legitimately appear under more than one topic heading (e.g. a
    document belonging to both a broad and a narrower overlapping cluster) --
    this must be a list, not a single value, or 65 of this corpus's 367
    topic-membership links silently vanish."""
    doc_to_topics = {}
    if not TOPICS_MD.exists():
        return doc_to_topics
    current_topic = None
    for line in TOPICS_MD.read_text(encoding="utf-8").splitlines():
        h = TOPIC_HEADING_RE.match(line)
        if h:
            current_topic = h.group(1)
            continue
        l = TOPIC_LINK_RE.match(line)
        if l and current_topic:
            doc_to_topics.setdefault(l.group(1), []).append(current_topic)
    return doc_to_topics


def category_from_path(rel_to_kb_root: Path) -> str:
    """rel_to_kb_root is relative to knowledge-base/d-central/. Category is
    everything between d-central/ and the project directory (second-to-last
    path segment before the filename, or third-to-last if under _superseded/)."""
    parts = list(rel_to_kb_root.parts[:-1])  # drop filename
    if parts and parts[-1] == "_superseded":
        parts = parts[:-1]
    if not parts:
        return ""
    return "/".join(parts[:-1])  # drop the project-directory segment


def main():
    classified_by_path = load_classified()
    doc_to_topics = load_topics_md()
    consolidated = json.loads(CONSOLIDATED_JSON.read_text(encoding="utf-8")) if CONSOLIDATED_JSON.exists() else {}

    docs = {}
    counts = {"canonical": 0, "superseded": 0, "disputed": 0, "topic_memberships": 0, "docs_in_at_least_one_topic": 0, "ungrouped": 0}

    for path in sorted(KB_ROOT.rglob("*.md")):
        rel_to_kb = path.relative_to(KB_DIR).as_posix()          # e.g. "d-central/.../file.md"
        rel_to_kb_root = path.relative_to(KB_ROOT)                 # e.g. ".../file.md" under d-central/

        fm = parse_frontmatter(path)
        is_superseded = "_superseded" in path.parts

        if is_superseded:
            dedup_status = "superseded"
        elif fm.get("status") == "disputed":
            dedup_status = "disputed"
        else:
            dedup_status = "canonical"
        counts[dedup_status] = counts.get(dedup_status, 0) + 1

        topics = doc_to_topics.get(rel_to_kb, [])
        consolidated_docs = [consolidated[t]["consolidated_doc"] for t in topics if t in consolidated]
        if topics:
            counts["docs_in_at_least_one_topic"] += 1
            counts["topic_memberships"] += len(topics)
        elif dedup_status == "canonical":
            counts["ungrouped"] += 1

        # Stage 3 record keyed by the *classified* relative path, which is
        # projects/kb-docs/... not knowledge-base/... -- match on doc_uuid instead.
        doc_uuid = fm.get("doc_uuid", "")

        record = {
            "category": category_from_path(rel_to_kb_root),
            "project": fm.get("source_project", ""),
            "doc_uuid": doc_uuid,
            "dedup_status": dedup_status,
            "topics": topics,
            "consolidated_docs": consolidated_docs,
        }
        for key in ("duplicate_of", "superseded_by", "conflicts_with", "supersession_reason", "duplicate_reason", "unresolved_reason"):
            if key in fm:
                record[key] = fm[key]

        docs[rel_to_kb] = record

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "counts": {
            **counts,
            "total_docs": len(docs),
            "topics": len(consolidated),
        },
        "docs": docs,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    print(f"Wrote {OUT_PATH.relative_to(REPO_ROOT)}")
    print(f"  {len(docs)} docs total")
    print(f"  {counts['canonical']} canonical, {counts['superseded']} superseded, {counts['disputed']} disputed")
    print(
        f"  {counts['docs_in_at_least_one_topic']} docs in >=1 of {len(consolidated)} topics "
        f"({counts['topic_memberships']} total memberships, {counts['topic_memberships'] - counts['docs_in_at_least_one_topic']} cross-listed twice), "
        f"{counts['ungrouped']} canonical docs left ungrouped"
    )


if __name__ == "__main__":
    main()
