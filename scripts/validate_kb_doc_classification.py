#!/usr/bin/env python3
"""
Hook validator for knowledge-base/_kb_doc_classified.jsonl.

Mirrors validate_classification.py's mechanical backstop for the conversation
classifier: after every write, check the last line matches the required
schema and primary_category is one of the fixed taxonomy paths. Wired via
.claude/settings.json as a PostToolUse hook on Write/Edit/Bash.
"""

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLASSIFIED_PATH = REPO_ROOT / "knowledge-base" / "_kb_doc_classified.jsonl"

REQUIRED_FIELDS = {"doc_uuid", "source_project", "original_filename", "relative_path",
                   "primary_category", "secondary_tags", "abstract"}

VALID_CATEGORIES = {
    "d-central/core/identity", "d-central/core/governance", "d-central/core/economics",
    "d-central/core/attestation-storage", "d-central/core/observability",
    "d-central/mesh-services/connectivity", "d-central/mesh-services/compute",
    "d-central/mesh-services/storage", "d-central/mesh-services/energy",
    "d-central/mesh-services/sensors-mobility", "d-central/mesh-services/ai",
    "d-central/mesh-services/bandwidth", "d-central/mesh-services/geo",
    "d-central/verticals/commerce", "d-central/verticals/social-comm",
    "d-central/verticals/health", "d-central/verticals/mobility",
    "d-central/verticals/home-trades", "d-central/verticals/manufacturing",
    "d-central/hardware/shi-node", "d-central/hardware/campus",
    "d-central/hardware/sensing-planes", "d-central/hardware/wearables-display",
    "d-central/business-legal", "d-central/haiti-diaspora",
    "d-central/meta/status-tracking", "d-central/meta/simulation", "d-central/meta/platform-scaffolding",
    "d-central/security", "d-central/academic-personal", "d-central/other",
}

BANNED_ABSTRACT_SUBSTRINGS = [
    "technical work on development and troubleshooting",
    "no d-central content identified",
    "general technical conversation",
    "miscellaneous technical discussion",
    "portfolio/technical work",
    "description based on conversation content",
    "description based on document content",
]

BANNED_ABSTRACT_OPENERS = [
    "i'll help", "i'd be happy", "i see you", "i'll create", "i'll review",
    "i'll look into", "great—here's", "great-here's", "here is a comprehensive",
    "here's a comprehensive", "i have reviewed", "i'll structure", "below is a",
]


def main():
    if not CLASSIFIED_PATH.exists():
        return 0

    lines = [l for l in CLASSIFIED_PATH.read_text(encoding="utf-8").splitlines() if l.strip()]
    if not lines:
        return 0

    last_line = lines[-1]
    try:
        record = json.loads(last_line)
    except json.JSONDecodeError as e:
        print(f"VALIDATION FAILED: last line of _kb_doc_classified.jsonl is not valid JSON: {e}", file=sys.stderr)
        return 1

    missing = REQUIRED_FIELDS - set(record.keys())
    if missing:
        print(f"VALIDATION FAILED: record missing required fields: {missing}", file=sys.stderr)
        return 1

    if record["primary_category"] not in VALID_CATEGORIES:
        print(f"VALIDATION FAILED: primary_category {record['primary_category']!r} is not in the "
              f"fixed taxonomy.", file=sys.stderr)
        return 1

    for tag in record.get("secondary_tags", []):
        if tag not in VALID_CATEGORIES:
            print(f"VALIDATION FAILED: secondary_tag {tag!r} is not in the fixed taxonomy.", file=sys.stderr)
            return 1

    abstract_lower = record.get("abstract", "").lower()
    if len(abstract_lower) < 20:
        print("VALIDATION FAILED: abstract is suspiciously short (<20 chars).", file=sys.stderr)
        return 1
    for banned in BANNED_ABSTRACT_SUBSTRINGS:
        if banned in abstract_lower:
            print(f"VALIDATION FAILED: abstract contains banned generic phrase {banned!r}.", file=sys.stderr)
            return 1
    for opener in BANNED_ABSTRACT_OPENERS:
        if abstract_lower.startswith(opener) or f" {opener}" in abstract_lower[:60]:
            print(f"VALIDATION FAILED: abstract looks like pasted assistant-reply text "
                  f"(starts with/near {opener!r}).", file=sys.stderr)
            return 1

    seen_uuids = set()
    seen_abstracts = {}
    for line in lines:
        try:
            rec = json.loads(line)
        except Exception:
            continue
        uuid = rec.get("doc_uuid")
        if uuid in seen_uuids:
            print(f"VALIDATION FAILED: doc_uuid {uuid} appears more than once.", file=sys.stderr)
            return 1
        seen_uuids.add(uuid)
        abstract = rec.get("abstract", "")
        if abstract:
            if abstract in seen_abstracts and seen_abstracts[abstract] != uuid:
                print(f"VALIDATION FAILED: identical abstract used for two different docs "
                      f"({seen_abstracts[abstract]} and {uuid}).", file=sys.stderr)
                return 1
            seen_abstracts[abstract] = uuid

    return 0


if __name__ == "__main__":
    sys.exit(main())
