#!/usr/bin/env python3
"""
Stage 2 gap-fill: extracts DC-*-NNN/OS-*-NNN-pattern documents that were
created as inline conversation artifacts (via the create_file tool) rather
than uploaded to a Project's knowledge base.

Why this exists: Stage 2 as originally built (extract_project_docs.py) only
pulls docs from projects/*/docs[] -- it has no visibility into a document
that a conversation created for itself via create_file and never uploaded
anywhere. The DC-LKB-001/002/003 docs (Lakou Protocol) were found this way
by hand, for one conversation; this script does that scan systematically
across all 743 conversations instead.

Detection rule: a create_file tool-use block whose path's basename starts
with a DC-*-NNN or OS-*-NNN pattern (case-sensitive, matching the same
pattern get_next_conversation.py already uses for doc-ID *mentions*) is
treated as a genuine standalone document -- as opposed to a build/registry
script that merely *mentions* a doc ID inside its own logic (those don't
match this stricter "the filename itself is the doc ID" rule).

Usage: python3 scripts/extract_conversation_artifacts.py
Writes one file per artifact to conversations/artifacts/<basename>, each
with front matter (source_conversation_uuid, conversation_title, created_at,
extraction_method), skipping any doc_id already present in docs/ (e.g.
DC-LKB-001/002/003, pulled by hand in an earlier session). Also writes
conversations/_artifacts_index.md summarizing what was found.
"""

import json
import re
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent
CONV_PATH = REPO_ROOT / "raw-export" / "conversations" / "conversations.json"
OUT_DIR = REPO_ROOT / "conversations" / "artifacts"
DOCS_DIR = REPO_ROOT / "docs"
INDEX_PATH = REPO_ROOT / "conversations" / "_artifacts_index.md"

NAME_RE = re.compile(r"^((?:DC|OS)-[A-Z0-9]+-\d{3})")


def already_extracted_doc_ids():
    """doc_id (e.g. DC-LKB-001) -> True for anything already pulled into docs/."""
    ids = set()
    if DOCS_DIR.exists():
        for path in DOCS_DIR.glob("*.md"):
            m = NAME_RE.match(path.stem)
            if m:
                ids.add(m.group(1))
    return ids


def main():
    if not CONV_PATH.exists():
        sys.exit(f"Missing {CONV_PATH}")

    convs = json.loads(CONV_PATH.read_text(encoding="utf-8"))
    skip_ids = already_extracted_doc_ids()

    found = []
    for conv in convs:
        for msg in conv.get("chat_messages", []):
            content = msg.get("content", [])
            if not isinstance(content, list):
                continue
            for block in content:
                if not (isinstance(block, dict) and block.get("type") == "tool_use"
                        and block.get("name") == "create_file"):
                    continue
                inp = block.get("input", {})
                path = inp.get("path", "") or ""
                basename = path.rsplit("/", 1)[-1]
                m = NAME_RE.match(basename)
                if not m:
                    continue
                found.append({
                    "doc_id": m.group(1),
                    "basename": basename,
                    "file_text": inp.get("file_text", "") or "",
                    "description": inp.get("description", "") or "",
                    "conv_uuid": conv.get("uuid", ""),
                    "conv_title": conv.get("name", "") or "(untitled)",
                    "created_at": conv.get("created_at", ""),
                })

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    written, skipped_already, skipped_empty = [], [], []
    for item in found:
        if item["doc_id"] in skip_ids:
            skipped_already.append(item)
            continue
        if not item["file_text"].strip():
            skipped_empty.append(item)
            continue

        dest = OUT_DIR / item["basename"]
        front = (
            "---\n"
            f"source_conversation_uuid: {item['conv_uuid']}\n"
            f"conversation_title: {item['conv_title']!r}\n"
            f"created_at: {item['created_at']}\n"
            f"doc_id: {item['doc_id']}\n"
            f"description: {item['description']!r}\n"
            "extraction_method: conversation-artifact (create_file tool-use block, "
            "never uploaded to a Project KB)\n"
            "---\n\n"
        )
        dest.write_text(front + item["file_text"], encoding="utf-8")
        written.append(item)

    index_lines = [
        "# Conversation-Artifact Extraction (Stage 2 gap-fill)",
        "",
        f"Scanned all {len(convs)} conversations' `create_file` tool-use blocks for "
        "DC-*-NNN/OS-*-NNN-pattern document filenames -- artifacts created inline in "
        "a conversation and never uploaded to any Project's knowledge base, so Stage "
        "2's original project-KB extraction (`extract_project_docs.py`) had no way to "
        "find them.",
        "",
        f"**{len(written)} new documents extracted** to `conversations/artifacts/`. "
        f"{len(skipped_already)} already present in `docs/` (skipped, not re-extracted). "
        f"{len(skipped_empty)} matched the naming pattern but had empty content (skipped).",
        "",
        "| Doc ID | Filename | Conversation | Created |",
        "|---|---|---|---|",
    ]
    for item in sorted(written, key=lambda x: x["doc_id"]):
        index_lines.append(
            f"| {item['doc_id']} | `{item['basename']}` | {item['conv_title']} | {item['created_at'][:10]} |"
        )
    if skipped_already:
        index_lines += ["", "## Already extracted (skipped)", ""]
        for item in skipped_already:
            index_lines.append(f"- {item['doc_id']} (`{item['basename']}`) -- already in `docs/`")
    if skipped_empty:
        index_lines += ["", "## Matched pattern but empty content (skipped)", ""]
        for item in skipped_empty:
            index_lines.append(f"- {item['doc_id']} (`{item['basename']}`) in conversation {item['conv_uuid']}")

    INDEX_PATH.write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    print(f"Scanned {len(convs)} conversations, found {len(found)} doc-ID-named create_file artifacts.")
    print(f"Extracted {len(written)} new docs to {OUT_DIR.relative_to(REPO_ROOT)}/")
    print(f"Skipped {len(skipped_already)} already in docs/, {len(skipped_empty)} empty.")
    print(f"Index: {INDEX_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
