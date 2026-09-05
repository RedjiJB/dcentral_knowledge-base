#!/usr/bin/env python3
"""
Stage 3 (fine-grained) tree builder.

Regenerates knowledge-base-fine/<primary_category>/<project-slug>/<doc>.md from
knowledge-base/_kb_doc_classified.jsonl -- the per-document classification produced
by the classify-kb-doc skill. This supersedes classify_docs.py's coarse
project-level tree (knowledge-base/) with a real per-document classification into
the same fixed taxonomy used for Stage 2 conversations (see SKILL.md / PLAN.md).

Docs are COPIED from projects/kb-docs/ (Stage-2 ground truth), never moved.
Only docs present in _kb_doc_classified.jsonl are placed -- unclassified docs are
reported at the end, not silently dropped or defaulted.

The old knowledge-base/ tree (coarse, project-level) is left untouched -- this is
a new, separate output (knowledge-base-fine/) until the reconciliation is judged
complete and knowledge-base/ is deliberately replaced.

Usage: python3 scripts/rebuild_knowledge_base_fine.py
"""

import json
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DOCS_DIR = REPO_ROOT / "projects" / "kb-docs"
CLASSIFIED_PATH = REPO_ROOT / "knowledge-base" / "_kb_doc_classified.jsonl"
OUT_DIR = REPO_ROOT / "knowledge-base-fine"


def slugify(name):
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", name).strip("-")


def main():
    if not CLASSIFIED_PATH.exists():
        print(f"No {CLASSIFIED_PATH} yet -- run the classify-kb-doc skill first.")
        return 1

    records = []
    for line in CLASSIFIED_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))

    all_docs = {}
    for path in sorted(KB_DOCS_DIR.glob("*/*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not m:
            continue
        front = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                front[k.strip()] = v.strip()
        doc_uuid = front.get("doc_uuid")
        if doc_uuid:
            all_docs[doc_uuid] = path

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    placed, missing_source = 0, []
    category_counts = {}
    for rec in records:
        src = all_docs.get(rec["doc_uuid"])
        if not src:
            missing_source.append(rec["doc_uuid"])
            continue
        category = rec["primary_category"]
        project_slug = slugify(rec["source_project"])
        dest_dir = OUT_DIR / category / project_slug
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / src.name
        shutil.copy2(src, dest)
        placed += 1
        category_counts[category] = category_counts.get(category, 0) + 1

    classified_uuids = {r["doc_uuid"] for r in records}
    unclassified = [u for u in all_docs if u not in classified_uuids]

    print(f"Placed {placed} docs into {OUT_DIR.relative_to(REPO_ROOT)}/")
    for cat, count in sorted(category_counts.items()):
        print(f"  {cat}: {count}")
    if missing_source:
        print(f"WARNING: {len(missing_source)} classified doc_uuids have no matching source file: {missing_source}")
    print(f"{len(unclassified)}/{len(all_docs)} docs not yet classified (run classify-kb-doc skill).")
    return 0


if __name__ == "__main__":
    exit(main())
