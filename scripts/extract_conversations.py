#!/usr/bin/env python3
"""
Stage 1/2 extractor for the real Claude export format: a single
conversations.json array (743 conversations) plus per-file project JSONs.

Produces, under registry/ and conversations/:
  - registry/dc_registry_extracted_v2.csv   (doc-ID mentions across all conversations)
  - conversations/_extracted_index.md        (one row per conversation: uuid, name, dates, doc-ids mentioned)
  - projects/_extracted_index.md             (one row per project: uuid, name, kb doc count)

This replaces build_registry_local.py (DC-REG-001 script era), which assumed
one-JSON-file-per-conversation and does not match this export's shape.
"""

import json
import re
import csv
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW = REPO_ROOT / "raw-export"

DOC_PATTERNS = [
    re.compile(r'\bDC-[A-Z0-9]+-\d{3}\b'),
    re.compile(r'\bOS-[A-Z0-9]+-\d{3}\b'),
    re.compile(r'\bCST\d{4}\b'),
    re.compile(r'\bMAT\d{4}\b'),
    re.compile(r'\bGEN\d{4}\b'),
    re.compile(r'\bAC-[A-Z0-9]+-\d{3}\b'),
]


def extract_doc_ids(text):
    found = set()
    for pat in DOC_PATTERNS:
        found.update(pat.findall(text))
    return found


def flatten_conversation_text(conv):
    parts = []
    for m in conv.get("chat_messages", []):
        content = m.get("content", [])
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text = block.get("text", "")
                    if text:
                        parts.append(text)
        elif isinstance(content, str):
            parts.append(content)
    return "\n".join(parts)


def infer_status(snippet):
    lower = snippet.lower()
    if any(w in lower for w in ["superseded", "replaced by", "deprecated"]):
        return "superseded"
    if any(w in lower for w in ["complete", "done", "finished", "built", "executed", "finalized"]):
        return "complete"
    if any(w in lower for w in ["draft", "wip", "in progress", "unclear"]):
        return "draft"
    return "referenced"


def context_around(text, doc_id, window=200):
    idx = text.upper().find(doc_id.upper())
    if idx == -1:
        return ""
    start = max(0, idx - window)
    end = min(len(text), idx + len(doc_id) + window)
    return text[start:end].replace("\n", " ").strip()


def main():
    conv_path = RAW / "conversations" / "conversations.json"
    if not conv_path.exists():
        raise SystemExit(f"Missing {conv_path} — unzip conversations-000.zip into raw-export/conversations/ first")

    print("Loading conversations.json (this is ~320MB, may take a moment)...")
    with open(conv_path, "r", encoding="utf-8") as f:
        conversations = json.load(f)
    print(f"Loaded {len(conversations)} conversations.")

    doc_registry = defaultdict(lambda: {"sources": set(), "contexts": [], "statuses": []})
    conv_rows = []

    for i, conv in enumerate(conversations, 1):
        if i % 100 == 0:
            print(f"  {i}/{len(conversations)} processed...")
        uuid = conv.get("uuid", "")
        name = conv.get("name") or "(untitled)"
        created = conv.get("created_at", "")
        updated = conv.get("updated_at", "")
        text = flatten_conversation_text(conv)
        ids_here = extract_doc_ids(text) | extract_doc_ids(name)

        for doc_id in ids_here:
            ctx = context_around(text, doc_id) or context_around(name, doc_id)
            doc_registry[doc_id]["sources"].add(uuid)
            doc_registry[doc_id]["contexts"].append(ctx[:200])
            doc_registry[doc_id]["statuses"].append(infer_status(ctx))

        conv_rows.append({
            "uuid": uuid,
            "name": name,
            "created_at": created,
            "updated_at": updated,
            "doc_ids": ", ".join(sorted(ids_here)) if ids_here else "",
        })

    # Registry CSV
    registry_out = REPO_ROOT / "registry" / "dc_registry_extracted_v2.csv"
    with open(registry_out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "doc_id", "mention_count", "inferred_status", "source_conversation_uuids", "sample_context"
        ])
        writer.writeheader()
        for doc_id in sorted(doc_registry.keys()):
            data = doc_registry[doc_id]
            most_common = max(set(data["statuses"]), key=data["statuses"].count) if data["statuses"] else "unclear"
            writer.writerow({
                "doc_id": doc_id,
                "mention_count": len(data["sources"]),
                "inferred_status": most_common,
                "source_conversation_uuids": "; ".join(sorted(data["sources"])),
                "sample_context": data["contexts"][0] if data["contexts"] else "",
            })
    print(f"Wrote {registry_out} ({len(doc_registry)} unique doc IDs found)")

    # Conversation index
    conv_out = REPO_ROOT / "conversations" / "_extracted_index.md"
    conv_out.parent.mkdir(exist_ok=True)
    with open(conv_out, "w", encoding="utf-8") as f:
        f.write(f"# Conversation Index (Stage 1 extraction)\n\n")
        f.write(f"Extracted from conversations-000.zip — {len(conv_rows)} conversations.\n\n")
        f.write("| UUID | Name | Created | Updated | Doc IDs mentioned |\n")
        f.write("|---|---|---|---|---|\n")
        for row in sorted(conv_rows, key=lambda r: r["updated_at"], reverse=True):
            f.write(f"| {row['uuid']} | {row['name'][:80]} | {row['created_at'][:10]} | {row['updated_at'][:10]} | {row['doc_ids']} |\n")
    print(f"Wrote {conv_out}")

    # Project index
    projects_dir = RAW / "projects" / "projects"
    project_rows = []
    if projects_dir.exists():
        for pf in sorted(projects_dir.glob("*.json")):
            with open(pf, "r", encoding="utf-8") as f:
                proj = json.load(f)
            project_rows.append({
                "uuid": proj.get("uuid", pf.stem),
                "name": proj.get("name", "(untitled)"),
                "doc_count": len(proj.get("docs", [])),
                "updated_at": proj.get("updated_at", ""),
            })
        proj_out = REPO_ROOT / "projects" / "_extracted_index.md"
        proj_out.parent.mkdir(exist_ok=True)
        with open(proj_out, "w", encoding="utf-8") as f:
            f.write("# Project Index (Stage 1 extraction)\n\n")
            f.write(f"Extracted from projects-000.zip — {len(project_rows)} projects.\n\n")
            f.write("| UUID | Name | KB doc count | Updated |\n")
            f.write("|---|---|---|---|\n")
            for row in sorted(project_rows, key=lambda r: r["doc_count"], reverse=True):
                f.write(f"| {row['uuid']} | {row['name']} | {row['doc_count']} | {row['updated_at'][:10]} |\n")
        print(f"Wrote {proj_out}")

    print("\nDone. Next: Stage 3 classification (route conversations/projects into the folder tree).")


if __name__ == "__main__":
    main()
