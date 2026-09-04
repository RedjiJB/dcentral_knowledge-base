#!/usr/bin/env python3
"""
DC-REG-001 builder — processes a Claude.ai data export (unzipped folder structure)
and uses Claude Haiku 4.5 to extract document registry entries from every conversation.

This version handles the folder structure where each conversation is a separate JSON file,
with improved message parsing for the actual export format.

Cost note: Haiku 4.5 is $1/$5 per million input/output tokens (as of Aug 2026).
For a few hundred conversations this should run a few dollars. For 700+ chats,
consider using the Batch API for a 50% discount (fire-and-forget, results in 24h).

Setup:
    pip install anthropic
    export ANTHROPIC_API_KEY=your_key_here

Usage:
    1. Export your data: claude.ai -> Settings -> Privacy -> Export data
    2. Unzip the download
    3. python build_registry_from_export.py /path/to/unzipped/folder

Example:
    python build_registry_from_export.py ~/Downloads/claude-export-2026-08-23
"""

import json
import sys
import time
import csv
from pathlib import Path
import anthropic

MODEL = "claude-haiku-4-5-20251001"
LOG_EVERY = 10
MAX_CHARS = 200_000  # increased for longer conversations

EXTRACTION_PROMPT = """You are scanning ONE conversation from a large archive to build a \
document registry. Read the conversation below and extract any formal documents, \
specifications, or named artifacts that were created, referenced, or discussed \
with an identifiable name or ID (e.g. "DC-XXX-001", "OS-YYY-ZZZ", "DC-TPL-XXX", \
or clearly named systems/specs even without formal IDs).

For each document found, return ONLY a JSON array (no markdown, no preamble, \
no code fences). Each element should have:
{{
  "doc_id": "formal ID like DC-XXX-001, or null if no formal ID found",
  "title": "extracted or inferred title from context",
  "scope": "one sentence describing what it covers or its purpose",
  "status": "one of: complete / draft / referenced-only / executed / unclear",
  "category": "best-fit category: network / identity / finance / security / infrastructure / coursework / personal / coordination / vertical / other"
}}

If a document appears under different names or IDs in the conversation, include all variants 
as separate entries (dedup will happen later).

If the conversation contains no identifiable documents or named artifacts, return: []

IMPORTANT: Be conservative — only include entries you're confident about. False positives 
are worse than false negatives (gaps in the registry are better than noise).

Conversation text:
---
{conversation_text}
---

Return JSON array only (no markdown, no preamble):"""


def flatten_messages(conv):
    """
    Extract text from conversation message structure.
    Handles the actual export format: messages have content arrays with type blocks.
    """
    msgs = conv.get("chat_messages") or conv.get("messages") or []
    lines = []
    
    for m in msgs:
        sender = m.get("sender") or m.get("role") or "unknown"
        
        # Try top-level text field first
        text = m.get("text")
        if text is None or not text.strip():
            # Fall back to content array
            content = m.get("content", [])
            if isinstance(content, list):
                text_parts = []
                for block in content:
                    if isinstance(block, dict):
                        # Extract from type-specific fields
                        if block.get("type") == "text":
                            block_text = block.get("text", "")
                            if block_text:
                                text_parts.append(block_text)
                        elif block.get("type") == "thinking":
                            # Skip thinking blocks (internal reasoning)
                            pass
                        elif "text" in block:
                            # Fallback for blocks with text but no type
                            text_parts.append(block.get("text", ""))
                text = " ".join(text_parts) if text_parts else ""
            else:
                text = str(content) if content else ""
        
        if text and text.strip():
            lines.append(f"{sender}: {text}")
    
    return "\n".join(lines)


def extract_from_conversation(client, conv_text, title, max_retries=2):
    """
    Send conversation to Haiku for document extraction with retry logic.
    """
    if len(conv_text) > MAX_CHARS:
        half = MAX_CHARS // 2
        conv_text = conv_text[:half] + "\n\n[...middle truncated for length...]\n\n" + conv_text[-half:]

    prompt = EXTRACTION_PROMPT.format(conversation_text=conv_text)

    for attempt in range(max_retries):
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=2500,
                messages=[{"role": "user", "content": prompt}],
            )
            raw = resp.content[0].text.strip()

            # Clean up markdown code fences if present
            if raw.startswith("```"):
                raw = raw.strip("`").strip()
                if raw.lower().startswith("json"):
                    raw = raw[4:].strip()

            parsed = json.loads(raw)
            if isinstance(parsed, list):
                return parsed
            else:
                print(f"  [!] Response was not an array for '{title}' — skipping")
                return []
                
        except json.JSONDecodeError as e:
            if attempt < max_retries - 1:
                print(f"  [retry] JSON parse failed for '{title}' (attempt {attempt + 1}/{max_retries})")
                time.sleep(1)
            else:
                print(f"  [!] Could not parse response for '{title}' — skipping. "
                      f"Raw (first 300 chars): {raw[:300]}")
                return []
        except anthropic.APIError as e:
            if attempt < max_retries - 1:
                print(f"  [retry] API error for '{title}' (attempt {attempt + 1}/{max_retries}): {e}")
                time.sleep(2)
            else:
                print(f"  [!] API error for '{title}': {e}")
                return []


def find_conversation_files(export_dir):
    """
    Find all conversation JSON files in the export directory.
    Export structure: folder per conversation, with one .json file inside.
    """
    export_dir = Path(export_dir)
    json_files = sorted(export_dir.glob("**/*.json"))
    
    # Filter to conversation files (those with chat_messages or messages)
    conv_files = []
    for f in json_files:
        try:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            if isinstance(data, dict) and ("chat_messages" in data or "messages" in data):
                conv_files.append(f)
        except (json.JSONDecodeError, IOError):
            pass
    
    return conv_files


def main():
    if len(sys.argv) != 2:
        print("Usage: python build_registry_from_export.py /path/to/unzipped/export/folder")
        print("\nExample:")
        print("  python build_registry_from_export.py ~/Downloads/claude-export-2026-08-23")
        sys.exit(1)

    export_dir = sys.argv[1]
    conv_files = find_conversation_files(export_dir)
    
    if not conv_files:
        print(f"ERROR: No conversation files found in {export_dir}")
        print("Make sure you've unzipped the export and are pointing to the root folder.")
        sys.exit(1)
    
    print(f"Found {len(conv_files)} conversation JSON files in {export_dir}\n")

    try:
        client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
    except anthropic.APIError as e:
        print(f"ERROR: Could not initialize Anthropic client: {e}")
        print("Make sure ANTHROPIC_API_KEY is set in your environment.")
        sys.exit(1)

    all_entries = []
    skipped = 0
    
    for i, conv_file in enumerate(conv_files, 1):
        try:
            with open(conv_file, "r", encoding="utf-8") as f:
                conv = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"  [!] Could not read {conv_file.name}: {e}")
            skipped += 1
            continue

        title = conv.get("name") or conv.get("title") or conv_file.stem
        text = flatten_messages(conv)
        
        if not text.strip():
            skipped += 1
            continue

        print(f"[{i:3d}/{len(conv_files)}] Processing: {title[:60]}...", end=" ", flush=True)
        entries = extract_from_conversation(client, text, title)
        
        for e in entries:
            # Ensure required fields
            if "doc_id" in e and e["doc_id"]:
                e["source_conversation"] = title
                e["source_updated_at"] = conv.get("updated_at", "")
                all_entries.append(e)
        
        print(f"✓ ({len(entries)} docs found)")

        if i % LOG_EVERY == 0:
            print(f"     ... {i}/{len(conv_files)} conversations processed, "
                  f"{len(all_entries)} entries accumulated so far\n")

        time.sleep(0.5)  # light pacing to avoid rate limits

    # Write CSV
    out_csv = Path(export_dir).parent / "dc_registry_from_haiku.csv"
    fieldnames = ["doc_id", "title", "scope", "status", "category",
                  "source_conversation", "source_updated_at"]
    
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for e in all_entries:
            row = {k: e.get(k, "") for k in fieldnames}
            writer.writerow(row)

    print(f"\n{'='*70}")
    print(f"✓ Complete. {len(all_entries)} entries written to:")
    print(f"  {out_csv}\n")
    print(f"Summary:")
    print(f"  Conversations processed: {len(conv_files)}")
    print(f"  Skipped (empty/unreadable): {skipped}")
    print(f"  Documents extracted: {len(all_entries)}")
    print(f"  Unique doc_ids: {len(set(e.get('doc_id', '') for e in all_entries))}\n")
    print(f"Next steps:")
    print(f"  1. Review {out_csv.name} for accuracy and false positives")
    print(f"  2. Dedupe by doc_id (same doc appears in multiple chats)")
    print(f"  3. Merge into DC-REG-001 (append new entries, update existing ones)")
    print(f"  4. Check for gaps:")
    print(f"     - Does this capture all your major DC-* documents?")
    print(f"     - Any DC-SIM, DC-SWARM, DC-PLANE, DC-SITE entries?")


if __name__ == "__main__":
    main()
