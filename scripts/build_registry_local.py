#!/usr/bin/env python3
"""
Local, pattern-based registry extractor for Claude export folders.
Identifies document IDs (DC-*, OS-*, CST*, MAT*, GEN*) and contextual scope
without needing API calls. Runs in seconds instead of minutes.

For validation/enrichment, feed the CSV to Haiku in a second pass if desired.
"""

import json
import re
import csv
from pathlib import Path
from collections import defaultdict

# Patterns for document IDs
DOC_PATTERNS = [
    r'\bDC-[A-Z0-9]+-\d{3}\b',      # DC-XXX-001
    r'\bOS-[A-Z0-9]+-\d{3}\b',      # OS-XXX-001
    r'\bCST\d{4}\b',                 # CST8315
    r'\bMAT\d{4}\b',                 # MAT8002
    r'\bGEN\d{4}\b',                 # GEN1957
    r'\bAC-[A-Z0-9]+-\d{3}\b',      # AC-XXX-001
]

# Compile patterns
compiled_patterns = [re.compile(p) for p in DOC_PATTERNS]

def extract_doc_ids(text):
    """Find all document IDs in text."""
    found = set()
    for pattern in compiled_patterns:
        matches = pattern.findall(text)
        found.update(matches)
    return sorted(found)

def extract_context_around_id(text, doc_id, window=300):
    """Get context snippet around a doc ID mention."""
    idx = text.upper().find(doc_id.upper())
    if idx == -1:
        return ""
    start = max(0, idx - window)
    end = min(len(text), idx + len(doc_id) + window)
    return text[start:end].strip()

def infer_status(context_snippet):
    """Guess status from surrounding text."""
    lower = context_snippet.lower()
    if any(w in lower for w in ["complete", "done", "finished", "built", "executed", "finalized"]):
        return "complete"
    elif any(w in lower for w in ["draft", "wip", "in progress", "working", "designing", "prototyping"]):
        return "draft"
    elif any(w in lower for w in ["reference", "reference only", "mentioned", "discussed", "cited"]):
        return "referenced-only"
    elif any(w in lower for w in ["execute", "build", "implement", "deploy", "run", "launch"]):
        return "executed"
    else:
        return "unclear"

def main():
    export_dir = Path("/tmp")
    
    # Find all conversation JSON files
    json_files = list(export_dir.glob("**/*.json"))
    conv_files = []
    
    print(f"Scanning {len(json_files)} JSON files for conversations...")
    for f in json_files:
        try:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            if isinstance(data, dict) and "chat_messages" in data:
                conv_files.append(f)
        except:
            pass
    
    print(f"Found {len(conv_files)} conversation files.\n")
    
    # Extract documents
    doc_registry = defaultdict(lambda: {
        "sources": [],
        "contexts": [],
        "statuses": [],
    })
    
    for i, conv_file in enumerate(conv_files, 1):
        if i % 50 == 0:
            print(f"  {i}/{len(conv_files)} conversations processed...")
        
        with open(conv_file, "r", encoding="utf-8") as f:
            conv = json.load(f)
        
        conv_name = conv.get("name") or conv_file.stem
        conv_text = []
        
        # Flatten messages
        for m in conv.get("chat_messages", []):
            content = m.get("content", [])
            if isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text = block.get("text", "")
                        if text:
                            conv_text.append(text)
        
        full_text = " ".join(conv_text)
        doc_ids = extract_doc_ids(full_text)
        
        # Record each document found in this conversation
        for doc_id in doc_ids:
            context = extract_context_around_id(full_text, doc_id, window=150)
            status = infer_status(context)
            
            doc_registry[doc_id]["sources"].append(conv_name)
            doc_registry[doc_id]["contexts"].append(context[:200])
            doc_registry[doc_id]["statuses"].append(status)
    
    print(f"\nExtracted {len(doc_registry)} unique documents.\n")
    
    # Write CSV
    out_csv = Path("/tmp/dc_registry_extracted.csv")
    
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "doc_id", "mention_count", "inferred_status", 
            "source_conversations", "sample_context"
        ])
        writer.writeheader()
        
        for doc_id in sorted(doc_registry.keys()):
            data = doc_registry[doc_id]
            most_common_status = max(set(data["statuses"]), 
                                     key=data["statuses"].count)
            
            writer.writerow({
                "doc_id": doc_id,
                "mention_count": len(data["sources"]),
                "inferred_status": most_common_status,
                "source_conversations": "; ".join(set(data["sources"])),
                "sample_context": data["contexts"][0] if data["contexts"] else "",
            })
    
    print(f"✓ Written to {out_csv}\n")
    print("Next steps:")
    print("  1. Open dc_registry_extracted.csv and review for accuracy")
    print("  2. Enrich with titles, scopes, categories manually or via Haiku")
    print("  3. Merge into DC-REG-001 tables (dedupe by doc_id)")


if __name__ == "__main__":
    main()
