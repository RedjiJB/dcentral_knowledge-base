#!/usr/bin/env python3
"""
One-off diagnostic (not part of the regular pipeline): search every conversation
for any mention of DC-STATUS-001 -- both inside create_file tool-use blocks
(would mean it was drafted as an artifact, the same way DC-LKB-*/DC-SIM-* were
found) and in plain message text (would mean it's discussed/assumed but never
actually written as a file).

Usage: python3 scripts/search_dc_status_001.py
"""

import json
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent
CONV_PATH = REPO_ROOT / "raw-export" / "conversations" / "conversations.json"

TARGET = "DC-STATUS-001"


def main():
    if not CONV_PATH.exists():
        sys.exit(f"Missing {CONV_PATH}")

    convs = json.loads(CONV_PATH.read_text(encoding="utf-8"))

    file_hits = []   # TARGET found inside a create_file block (path or content)
    text_hits = []   # TARGET found in plain message text
    seen_convs = set()

    for conv in convs:
        conv_uuid = conv.get("uuid", "")
        conv_title = conv.get("name", "") or "(untitled)"
        created_at = conv.get("created_at", "")

        for msg in conv.get("chat_messages", []):
            content = msg.get("content", [])
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict):
                    continue

                if block.get("type") == "tool_use" and block.get("name") == "create_file":
                    inp = block.get("input", {})
                    path = inp.get("path", "") or ""
                    text = inp.get("file_text", "") or ""
                    is_own_file = TARGET in path.rsplit("/", 1)[-1]
                    if TARGET in path or TARGET in text:
                        idx = text.find(TARGET)
                        snippet = text[max(0, idx - 100):idx + 200] if idx >= 0 else ""
                        file_hits.append({
                            "conv_uuid": conv_uuid, "conv_title": conv_title,
                            "created_at": created_at, "path": path, "snippet": snippet,
                            "is_own_file": is_own_file,
                        })
                        seen_convs.add(conv_uuid)

                elif block.get("type") == "text":
                    text = block.get("text", "") or ""
                    if TARGET in text:
                        idx = text.find(TARGET)
                        snippet = text[max(0, idx - 150):idx + 250]
                        text_hits.append({
                            "conv_uuid": conv_uuid, "conv_title": conv_title,
                            "created_at": created_at, "snippet": snippet,
                        })
                        seen_convs.add(conv_uuid)

    print(f"Scanned {len(convs)} conversations.")
    print(f"Conversations mentioning {TARGET}: {len(seen_convs)}")
    print()
    own_file_hits = [h for h in file_hits if h["is_own_file"]]
    print(f"=== create_file blocks whose OWN path is DC-STATUS-001: {len(own_file_hits)} ===")
    for h in own_file_hits:
        print(f"- conv '{h['conv_title']}' ({h['conv_uuid']}, {h['created_at'][:10]}), path={h['path']!r}")
        print(f"  snippet: ...{h['snippet']!r}...")
    print()
    print(f"=== create_file blocks that merely CITE DC-STATUS-001 in their own content: {len(file_hits) - len(own_file_hits)} ===")
    for h in file_hits:
        if h["is_own_file"]:
            continue
        print(f"- conv '{h['conv_title']}' ({h['conv_uuid']}, {h['created_at'][:10]}), path={h['path']!r}")
        print(f"  snippet: ...{h['snippet']!r}...")
    print()
    print(f"=== plain-text mentions (discussed but not necessarily a file): {len(text_hits)} ===")
    for h in text_hits[:20]:
        print(f"- conv '{h['conv_title']}' ({h['conv_uuid']}, {h['created_at'][:10]})")
        print(f"  snippet: ...{h['snippet']!r}...")
    if len(text_hits) > 20:
        print(f"  ... and {len(text_hits) - 20} more text hits")


if __name__ == "__main__":
    main()
