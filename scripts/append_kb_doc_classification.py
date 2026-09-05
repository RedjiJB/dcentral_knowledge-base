#!/usr/bin/env python3
"""
Safe append path for the classify-kb-doc skill (Stage 3, per-document pass).

Mirrors append_classification.py's rationale exactly: the agent writes the
classification record to a scratch JSON file via the Write tool (no shell
quoting involved), then this script validates and appends it to
knowledge-base/_kb_doc_classified.jsonl. Same taxonomy, same anti-gaming
banned-phrase/opener checks as the conversation classifier, because the
same drift and shortcut-under-pressure failure modes apply here too.

Usage: python3 scripts/append_kb_doc_classification.py <path-to-record.json>
The record file may hold a single JSON object OR a JSON array of objects
(batch mode) -- each is validated in order against the fixed taxonomy and
against records already appended, INCLUDING earlier records in the same
batch (so within-batch duplicate doc_uuids/abstracts are caught too).
Exit 0: all record(s) appended successfully.
Exit 1: validation failed on some record -- nothing from a failing record
  onward is appended; records before the failure are already saved (each
  passes/fails independently against the growing already-classified set).
  The error message names which record (index + doc_uuid) failed.
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


def already_classified_records():
    records = []
    if CLASSIFIED_PATH.exists():
        for line in CLASSIFIED_PATH.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except Exception:
                pass
    return records


def validate(record, existing_records):
    missing = REQUIRED_FIELDS - set(record.keys())
    if missing:
        return f"missing required fields: {missing}"
    if record["primary_category"] not in VALID_CATEGORIES:
        return f"primary_category {record['primary_category']!r} is not in the fixed taxonomy"
    for tag in record.get("secondary_tags", []):
        if tag not in VALID_CATEGORIES:
            return f"secondary_tag {tag!r} is not in the fixed taxonomy"

    existing_uuids = {r["doc_uuid"] for r in existing_records}
    if record["doc_uuid"] in existing_uuids:
        return f"doc_uuid {record['doc_uuid']} is already classified -- refusing to duplicate"

    abstract_lower = record.get("abstract", "").lower()
    if len(abstract_lower) < 20:
        return "abstract is suspiciously short (<20 chars) -- looks like a placeholder, not a real read"
    for banned in BANNED_ABSTRACT_SUBSTRINGS:
        if banned in abstract_lower:
            return (f"abstract contains banned generic phrase {banned!r} -- read the actual document "
                    f"content in the scratch file and write a specific abstract.")
    for opener in BANNED_ABSTRACT_OPENERS:
        if abstract_lower.startswith(opener) or f" {opener}" in abstract_lower[:60]:
            return (f"abstract looks like pasted raw assistant-reply text (starts with/near "
                    f"{opener!r}) instead of a synthesized third-person summary.")

    existing_abstracts = [r.get("abstract", "") for r in existing_records]
    if record["abstract"] in existing_abstracts and record["abstract"]:
        return ("this exact abstract text already appears on another record -- two different "
                "documents should not get an identical abstract. Re-read this document's actual "
                "content and write a specific one.")

    return None


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 scripts/append_kb_doc_classification.py <path-to-record.json>")

    record_path = Path(sys.argv[1])
    if not record_path.exists():
        sys.exit(f"No such file: {record_path}")

    try:
        parsed = json.loads(record_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"Not valid JSON: {e}")

    records = parsed if isinstance(parsed, list) else [parsed]
    if not records:
        sys.exit("Record file is an empty list -- nothing to append.")

    existing = already_classified_records()
    to_append = []
    for i, record in enumerate(records):
        error = validate(record, existing + to_append)
        if error:
            print(f"VALIDATION FAILED at record {i} (doc_uuid={record.get('doc_uuid', '?')}), "
                  f"nothing from this record onward appended: {error}", file=sys.stderr)
            break
        to_append.append(record)

    if not to_append:
        return 1

    CLASSIFIED_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CLASSIFIED_PATH, "a", encoding="utf-8") as f:
        for record in to_append:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            print(f"Appended {record['doc_uuid']} ({record['original_filename']}) -> {record['primary_category']}")

    return 0 if len(to_append) == len(records) else 1


if __name__ == "__main__":
    sys.exit(main())
