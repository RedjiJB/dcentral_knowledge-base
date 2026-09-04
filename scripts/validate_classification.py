#!/usr/bin/env python3
"""
Hook validator for conversations/_classified.jsonl.

Skills are instructions -- a model can still write malformed output despite
being told the schema. This is the mechanical backstop: after every write to
_classified.jsonl, check the last line actually matches the required schema
and that primary_category is one of the fixed taxonomy paths, not an
invented one. Exits non-zero (blocking, per PostToolUse hook convention) on
violation so the session sees the failure immediately instead of it being
discovered 500 records later.

Wired via .claude/settings.json as a PostToolUse hook on Write/Edit.
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CLASSIFIED_PATH = REPO_ROOT / "conversations" / "_classified.jsonl"

REQUIRED_FIELDS = {"uuid", "title", "created_at", "extracted_doc_ids",
                   "primary_category", "secondary_tags", "links_to", "abstract"}

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
    "d-central/meta/status-tracking", "d-central/meta/simulation",
    "d-central/security", "d-central/academic-personal", "d-central/other",
}

DOC_ID_PATTERN = re.compile(r"^(DC|OS)-[A-Z0-9]+-\d{3}$")


def main():
    if not CLASSIFIED_PATH.exists():
        return 0  # nothing to validate yet

    lines = [l for l in CLASSIFIED_PATH.read_text(encoding="utf-8").splitlines() if l.strip()]
    if not lines:
        return 0

    last_line = lines[-1]
    try:
        record = json.loads(last_line)
    except json.JSONDecodeError as e:
        print(f"VALIDATION FAILED: last line of _classified.jsonl is not valid JSON: {e}", file=sys.stderr)
        return 1

    missing = REQUIRED_FIELDS - set(record.keys())
    if missing:
        print(f"VALIDATION FAILED: record missing required fields: {missing}", file=sys.stderr)
        return 1

    if record["primary_category"] not in VALID_CATEGORIES:
        print(f"VALIDATION FAILED: primary_category {record['primary_category']!r} is not in the "
              f"fixed taxonomy -- the skill must pick from the list in SKILL.md, not invent one.",
              file=sys.stderr)
        return 1

    for tag in record.get("secondary_tags", []):
        if tag not in VALID_CATEGORIES:
            print(f"VALIDATION FAILED: secondary_tag {tag!r} is not in the fixed taxonomy.", file=sys.stderr)
            return 1

    for doc_id in record.get("links_to", []):
        if not DOC_ID_PATTERN.match(doc_id):
            print(f"VALIDATION FAILED: links_to entry {doc_id!r} doesn't look like a real doc ID "
                  f"(expected DC-XXX-NNN or OS-XXX-NNN).", file=sys.stderr)
            return 1

    # duplicate-UUID check across the whole file, not just the last line
    seen = set()
    for line in lines:
        try:
            uuid = json.loads(line)["uuid"]
        except Exception:
            continue
        if uuid in seen:
            print(f"VALIDATION FAILED: uuid {uuid} appears more than once in _classified.jsonl.",
                  file=sys.stderr)
            return 1
        seen.add(uuid)

    return 0


if __name__ == "__main__":
    sys.exit(main())
