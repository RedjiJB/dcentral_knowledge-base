#!/usr/bin/env python3
"""
Safe append path for the classify-conversation skill.

The failure mode this fixes: earlier runs had the agent construct a shell
command (PowerShell Add-Content -Value '...') with the classification JSON
inlined directly into the command string. Any abstract containing a quote,
backslash, or a literal sequence like "\n\nHuman:" breaks shell quoting in
ways that are unpredictable and different across shells (PowerShell vs bash).

Fix: the agent writes the record to a small JSON file using the Write tool
(no shell involved, no quoting to get right), then runs this script to
validate + append it. This script does the validation itself (same rules as
validate_classification.py) rather than relying on the shell to get a
one-liner right.

Usage: python3 scripts/append_classification.py <path-to-record.json>
Exit 0: appended successfully.
Exit 1: validation failed, nothing was appended -- fix the record and retry.
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
    "d-central/meta/status-tracking", "d-central/meta/simulation", "d-central/meta/platform-scaffolding",
    "d-central/security", "d-central/academic-personal", "d-central/other",
}

DOC_ID_PATTERN = re.compile(r"^(DC|OS)-[A-Z0-9]+-\d{3}$")

# Generic/templated abstracts a rushed pass falls back to instead of actually reading the
# conversation. This list exists because it already happened once: a batch run wrote
# "Technical work on development and troubleshooting. No D-Central content identified." for 17
# conversations in a row, including several with titles like "D Central: Building a Decentralized
# Ecosystem" that turned out to be a 269KB white paper on the platform's full architecture.
BANNED_ABSTRACT_SUBSTRINGS = [
    "technical work on development and troubleshooting",
    "no d-central content identified",
    "general technical conversation",
    "miscellaneous technical discussion",
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
    for doc_id in record.get("links_to", []):
        if not DOC_ID_PATTERN.match(doc_id):
            return f"links_to entry {doc_id!r} doesn't look like a real doc ID"

    existing_uuids = {r["uuid"] for r in existing_records}
    if record["uuid"] in existing_uuids:
        return f"uuid {record['uuid']} is already classified -- refusing to duplicate"

    abstract_lower = record.get("abstract", "").lower()
    if len(abstract_lower) < 20:
        return "abstract is suspiciously short (<20 chars) -- looks like a placeholder, not a real read"
    for banned in BANNED_ABSTRACT_SUBSTRINGS:
        if banned in abstract_lower:
            return (f"abstract contains banned generic phrase {banned!r} -- this is the exact "
                    f"failure mode that already happened once (see comment at top of this file). "
                    f"Actually read the conversation excerpt and write a specific abstract.")

    existing_abstracts = [r.get("abstract", "") for r in existing_records]
    if record["abstract"] in existing_abstracts and record["abstract"]:
        return ("this exact abstract text already appears on another record -- two different "
                "conversations should not get an identical abstract. Re-read this conversation's "
                "actual content and write a specific one.")

    return None


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python3 scripts/append_classification.py <path-to-record.json>")

    record_path = Path(sys.argv[1])
    if not record_path.exists():
        sys.exit(f"No such file: {record_path}")

    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"Not valid JSON: {e}")

    error = validate(record, already_classified_records())
    if error:
        print(f"VALIDATION FAILED, nothing appended: {error}", file=sys.stderr)
        return 1

    CLASSIFIED_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CLASSIFIED_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Appended {record['uuid']} -> {record['primary_category']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
