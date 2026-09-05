#!/usr/bin/env python3
"""
Materializes newly-classified docs from knowledge-base/_kb_doc_classified.jsonl
into knowledge-base/ at their fine-grained category path.

Successor to rebuild_knowledge_base_fine.py (retired along with
knowledge-base-fine/ once scripts/reconcile_knowledge_base.py merged it into
knowledge-base/ directly). This script is the ongoing "place newly classified
docs" step for ANY doc source -- projects/kb-docs/ (the original 428) or
conversations/artifacts/ (the Stage 2 gap-fill, 44 conversation-artifact docs)
-- since classify-kb-doc / get_next_kb_doc.py now reads from both.

Only ADDS docs that are classified but not yet present in knowledge-base/ at
their expected path; never touches docs already placed (those may carry
Stage 4/5 metadata from scripts/reconcile_knowledge_base.py that this script
has no opinion on and must not clobber).

Usage: python3 scripts/materialize_kb_docs.py
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DOCS_DIR = REPO_ROOT / "projects" / "kb-docs"
ARTIFACTS_DIR = REPO_ROOT / "conversations" / "artifacts"
KB_DIR = REPO_ROOT / "knowledge-base"
CLASSIFIED_PATH = KB_DIR / "_kb_doc_classified.jsonl"


def slugify(name):
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", name).strip("-")


def find_source(doc_uuid, source_project, original_filename):
    if source_project == "conversation-artifacts":
        path = ARTIFACTS_DIR / original_filename
        return path if path.exists() else None
    for path in KB_DOCS_DIR.glob("*/*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not m:
            continue
        for line in m.group(1).splitlines():
            if line.strip().startswith("doc_uuid:") and line.split(":", 1)[1].strip() == doc_uuid:
                return path
    return None


def main():
    if not CLASSIFIED_PATH.exists():
        print(f"No {CLASSIFIED_PATH} yet.")
        return 1

    records = [json.loads(l) for l in CLASSIFIED_PATH.read_text(encoding="utf-8").splitlines() if l.strip()]

    # Index existing tree by doc_uuid so we don't re-place (and don't clobber
    # any Stage 4/5 metadata already attached to a placed doc).
    existing_uuids = set()
    for path in KB_DIR.rglob("*.md"):
        if path.name.startswith("_"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"^doc_uuid: (\S+)", text, re.MULTILINE)
        if m:
            existing_uuids.add(m.group(1))

    placed, missing = 0, []
    # Cache project-doc lookups (find_source rescans the whole tree per call
    # otherwise, which is wasteful for many missing project docs at once).
    project_uuid_to_path = {}
    for path in KB_DOCS_DIR.glob("*/*.md"):
        text = path.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not m:
            continue
        for line in m.group(1).splitlines():
            if line.strip().startswith("doc_uuid:"):
                project_uuid_to_path[line.split(":", 1)[1].strip()] = path
                break

    for rec in records:
        uuid = rec["doc_uuid"]
        if uuid in existing_uuids:
            continue
        if rec["source_project"] == "conversation-artifacts":
            src = ARTIFACTS_DIR / rec["original_filename"]
        else:
            src = project_uuid_to_path.get(uuid)
        if not src or not src.exists():
            missing.append(uuid)
            continue

        project_slug = slugify(rec["source_project"])
        dest = KB_DIR / rec["primary_category"] / project_slug / src.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(src.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
        placed += 1

    print(f"Placed {placed} newly-classified docs into knowledge-base/.")
    if missing:
        print(f"WARNING: {len(missing)} classified doc_uuids have no matching source file: {missing}")
    unclassified = len(records) - len(existing_uuids) - placed
    return 0


if __name__ == "__main__":
    sys.exit(main())
