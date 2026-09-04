#!/usr/bin/env python3
"""
Stage 2 artifact extractor: pulls the 428 real knowledge-base documents out
of the 33 project JSONs and writes each one to disk as a standalone .md file.

This is the actual artifact layer the rest of the pipeline (DC-DEDUP-STD-001,
DC-TOPIC-SYNTH-STD-001, DC-CONSOLIDATOR-STD-001) operates on. Stage 1
(extract_conversations.py) only found doc-ID *mentions* in conversation text;
this extracts the KB doc *content* itself.

Output: projects/kb-docs/<project-slug>/<doc-slug>.md
  - front matter: source project uuid/name, doc uuid, filename, created_at,
    and a content hash (sha256, first 12 hex chars) for Stage-2.5 identity
    checks (DC-DEDUP-STD-001 §3 step 1) without re-reading full content.
  - filename collisions within a project (same title, different uuid) get
    a short hash suffix rather than overwriting.

Also writes projects/_kb_docs_index.md: one row per extracted doc, so
Stage 3 classification has a flat list to route from.
"""

import json
import re
import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PROJECTS_DIR = REPO_ROOT / "raw-export" / "projects" / "projects"
OUT_DIR = REPO_ROOT / "projects" / "kb-docs"


def slugify(name, maxlen=80):
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-")
    return (slug or "untitled")[:maxlen]


def content_hash(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def main():
    if not PROJECTS_DIR.exists():
        raise SystemExit(f"Missing {PROJECTS_DIR} — unzip projects-000.zip into raw-export/projects/ first")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    index_rows = []
    total_docs = 0
    seen_hashes = {}  # content_hash -> first (project, filename) seen, to flag exact duplicates

    for pf in sorted(PROJECTS_DIR.glob("*.json")):
        with open(pf, "r", encoding="utf-8") as f:
            project = json.load(f)

        proj_name = project.get("name") or pf.stem
        proj_uuid = project.get("uuid", pf.stem)
        proj_slug = slugify(proj_name)
        proj_dir = OUT_DIR / proj_slug
        docs = project.get("docs", [])
        if not docs:
            continue
        proj_dir.mkdir(parents=True, exist_ok=True)

        used_names = set()
        for doc in docs:
            doc_uuid = doc.get("uuid", "")
            filename = doc.get("filename") or "untitled"
            content = doc.get("content", "") or ""
            created_at = doc.get("created_at", "")
            chash = content_hash(content)

            base_slug = slugify(filename)
            out_name = f"{base_slug}.md"
            if out_name in used_names:
                out_name = f"{base_slug}-{doc_uuid[:8]}.md"
            used_names.add(out_name)

            out_path = proj_dir / out_name
            with open(out_path, "w", encoding="utf-8") as out:
                out.write("---\n")
                out.write(f"source_project: {proj_name}\n")
                out.write(f"source_project_uuid: {proj_uuid}\n")
                out.write(f"doc_uuid: {doc_uuid}\n")
                out.write(f"original_filename: {filename}\n")
                out.write(f"created_at: {created_at}\n")
                out.write(f"content_hash: {chash}\n")
                out.write("---\n\n")
                out.write(content)

            total_docs += 1
            dup_of = seen_hashes.get(chash)
            if dup_of is None:
                seen_hashes[chash] = (proj_name, filename)
            index_rows.append({
                "project": proj_name,
                "filename": filename,
                "path": str(out_path.relative_to(REPO_ROOT)).replace("\\", "/"),
                "content_hash": chash,
                "created_at": created_at,
                "exact_duplicate_of": f"{dup_of[0]} / {dup_of[1]}" if dup_of else "",
            })

    index_out = REPO_ROOT / "projects" / "_kb_docs_index.md"
    dup_count = sum(1 for r in index_rows if r["exact_duplicate_of"])
    with open(index_out, "w", encoding="utf-8") as f:
        f.write("# Project KB Docs Index (Stage 2 extraction)\n\n")
        f.write(f"Extracted {total_docs} knowledge-base documents from 33 projects.\n")
        f.write(f"{dup_count} are exact content duplicates of an earlier-processed doc "
                f"(same content_hash) — candidates for immediate DC-DEDUP-STD-001 §3 step 1 identity-check dedup.\n\n")
        f.write("| Project | Filename | Path | Content hash | Created | Exact duplicate of |\n")
        f.write("|---|---|---|---|---|---|\n")
        for row in sorted(index_rows, key=lambda r: (r["project"], r["filename"])):
            f.write(f"| {row['project']} | {row['filename'][:60]} | {row['path']} | "
                    f"{row['content_hash']} | {row['created_at'][:10]} | {row['exact_duplicate_of']} |\n")

    print(f"Extracted {total_docs} KB docs across {len(list(OUT_DIR.iterdir()))} project folders.")
    print(f"{dup_count} exact content duplicates flagged.")
    print(f"Wrote {index_out}")


if __name__ == "__main__":
    main()
