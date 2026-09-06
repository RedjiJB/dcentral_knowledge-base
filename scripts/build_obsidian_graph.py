#!/usr/bin/env python3
"""
Stage 8, Track A -- Obsidian-compatible graph layer. No external dependency:
this only writes [[wikilink]]-style cross-references into existing markdown,
plus one small hub-note folder, so any Obsidian vault pointed at this repo
root renders a graph view of the same relationships already captured in
registry/materialized-manifest.json.

Link targets use the FULL vault-relative path (not bare filename) with a
display alias -- 35 filename stems collide across projects (e.g. three
unrelated README-md.md files), and Obsidian's bare-[[filename]] resolution
is ambiguous/unreliable when that happens. A full-path wikilink is always
unique regardless of collisions.

Idempotent: re-running replaces the block between the AUTO-GENERATED markers
rather than appending a new one each time.

Usage: python3 scripts/build_obsidian_graph.py
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DIR = REPO_ROOT / "knowledge-base"
TOPICS_HUB_DIR = KB_DIR / "_topics"
MANIFEST_PATH = REPO_ROOT / "registry" / "materialized-manifest.json"

START_MARKER = "<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->"
END_MARKER = "<!-- AUTO-GENERATED RELATED END -->"
BLOCK_RE = re.compile(re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER) + r"\n?", re.DOTALL)


def slugify_topic(name: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", name.lower()).strip("-")


def wikilink(rel_path: str, display: str | None = None) -> str:
    target = rel_path[:-3] if rel_path.endswith(".md") else rel_path  # Obsidian omits the extension
    return f"[[{target}|{display}]]" if display else f"[[{target}]]"


def strip_bracket_note(raw: str) -> str:
    return raw.split(" [")[0].strip()


def build_related_block(rel_path: str, record: dict, docs: dict) -> str:
    lines = [START_MARKER, "", "## Related (auto-generated)", ""]

    topics = record.get("topics", [])
    if topics:
        lines.append("**Topics:**")
        for t in topics:
            lines.append(f"- {wikilink(f'knowledge-base/_topics/{slugify_topic(t)}.md', t)}")
        lines.append("")

    consolidated = record.get("consolidated_docs", [])
    if consolidated:
        lines.append("**Consolidated into:**")
        for c in consolidated:
            lines.append(f"- {wikilink(c)}")
        lines.append("")

    for field, label in (("duplicate_of", "Duplicate of"), ("superseded_by", "Superseded by")):
        if field in record:
            target = strip_bracket_note(record[field])
            # docs dict keys are relative to knowledge-base/ (no prefix); the raw front-matter
            # value usually carries the "knowledge-base/" prefix, so strip it for the lookup
            # but keep the vault-root-relative form (with prefix) for the wikilink itself.
            lookup_key = target[len("knowledge-base/"):] if target.startswith("knowledge-base/") else target
            target_rel = target if target.startswith("knowledge-base/") else f"knowledge-base/{target}"
            if lookup_key in docs:
                lines.append(f"**{label}:** {wikilink(target_rel)}")
            else:
                lines.append(f"**{label}:** {target} (unresolved path, see registry/materialized-manifest.json)")
            lines.append("")

    lines.append(END_MARKER)
    return "\n".join(lines) + "\n"


def upsert_block(path: Path, block: str):
    text = path.read_text(encoding="utf-8", errors="replace")
    if BLOCK_RE.search(text):
        new_text = BLOCK_RE.sub(block, text)
    else:
        sep = "" if text.endswith("\n\n") else ("\n\n" if text.endswith("\n") else "\n\n")
        new_text = text + sep + block
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def build_topic_hub_notes(manifest: dict):
    consolidated_json = json.loads((REPO_ROOT / "registry" / "consolidated-topics.json").read_text(encoding="utf-8"))
    topic_members = {}
    for rel_path, record in manifest["docs"].items():
        for t in record.get("topics", []):
            topic_members.setdefault(t, []).append(rel_path)

    TOPICS_HUB_DIR.mkdir(parents=True, exist_ok=True)
    written = 0
    for topic, members in sorted(topic_members.items()):
        slug = slugify_topic(topic)
        hub_path = TOPICS_HUB_DIR / f"{slug}.md"
        info = consolidated_json.get(topic, {})
        lines = [f"# Topic: {topic}", ""]
        if info.get("consolidated_doc"):
            lines += [f"**Consolidated doc:** {wikilink(info['consolidated_doc'])}", ""]
        lines += [f"**Members ({len(members)}):**", ""]
        for m in sorted(members):
            lines.append(f"- {wikilink(f'knowledge-base/{m}')}")
        hub_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        written += 1
    return written


def main():
    if not MANIFEST_PATH.exists():
        sys.exit("FAIL: registry/materialized-manifest.json not found -- run scripts/build_manifest.py first")

    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    docs = manifest["docs"]

    updated = 0
    for rel_path, record in docs.items():
        if not record.get("topics") and "duplicate_of" not in record and "superseded_by" not in record:
            continue  # nothing to link
        block = build_related_block(rel_path, record, docs)
        if upsert_block(KB_DIR / rel_path, block):
            updated += 1

    hub_count = build_topic_hub_notes(manifest)

    print(f"Updated {updated} docs with a Related block.")
    print(f"Wrote {hub_count} topic hub notes to {TOPICS_HUB_DIR.relative_to(REPO_ROOT)}/")


if __name__ == "__main__":
    main()
