#!/usr/bin/env python3
"""
Stage 7b -- manifest for docs/*.md, the hand-authored architecture-spec layer
that Stage 7's build_manifest.py never scanned (it only walks knowledge-base/
d-central/, since docs/ files carry no Stage 3-6 frontmatter/topic-membership
schema -- they're Consolidator OUTPUTS, not classified member docs).

docs/*.md files reference each other via plain prose markdown links
(`[label](OTHER-DOC.md)` or `[label](OTHER-DOC.md#anchor)`), not YAML
frontmatter and not [[wikilinks]]. This script is the read-only extraction
step: it finds every such link between docs/*.md files and records it as a
directed reference, so build_docs_graph.py (the write step) can turn that
into Obsidian [[wikilink]] Related blocks and Neo4j nodes/edges the same way
Stage 8 already does for knowledge-base/.

Output: registry/docs-manifest.json
  {
    "generated_at": "...",
    "counts": {"total_docs": N, "total_references": N},
    "docs": {
      "<filename>.md": {
        "title": "<first H1 heading text>",
        "references": ["<other filename>.md", ...],   # outgoing, deduped, sorted
        "referenced_by": ["<other filename>.md", ...]  # incoming, computed
      }, ...
    }
  }

Usage: python3 scripts/build_docs_manifest.py
"""

import json
import re
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
OUT_PATH = REPO_ROOT / "registry" / "docs-manifest.json"

TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
# Matches [label](TARGET.md) or [label](TARGET.md#anchor) or [label](./TARGET.md) --
# deliberately excludes links into ../knowledge-base/... (those are a different,
# already-covered graph) and excludes bare http(s) links.
LINK_RE = re.compile(r"\[[^\]]*\]\(\.?/?([A-Za-z0-9_.-]+\.md)(?:#[^)]*)?\)")


def main():
    docs = {}
    for path in sorted(DOCS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        title_m = TITLE_RE.search(text)
        title = title_m.group(1) if title_m else path.stem

        refs = set()
        for m in LINK_RE.finditer(text):
            target = m.group(1)
            if target != path.name and (DOCS_DIR / target).exists():
                refs.add(target)

        docs[path.name] = {
            "title": title,
            "references": sorted(refs),
            "referenced_by": [],  # filled in below
        }

    # Compute reverse edges
    for name, rec in docs.items():
        for target in rec["references"]:
            if target in docs:
                docs[target]["referenced_by"].append(name)
    for rec in docs.values():
        rec["referenced_by"] = sorted(set(rec["referenced_by"]))

    total_refs = sum(len(rec["references"]) for rec in docs.values())
    orphans = [name for name, rec in docs.items() if not rec["references"] and not rec["referenced_by"]]

    manifest = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "counts": {
            "total_docs": len(docs),
            "total_references": total_refs,
            "orphaned_docs": len(orphans),
        },
        "docs": docs,
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    print(f"Wrote {OUT_PATH.relative_to(REPO_ROOT)}")
    print(f"  {len(docs)} docs/*.md files scanned")
    print(f"  {total_refs} directed cross-references found")
    if orphans:
        print(f"  {len(orphans)} docs with zero references in or out (not necessarily wrong -- may be a leaf spec):")
        for o in orphans:
            print(f"    - {o}")


if __name__ == "__main__":
    main()
