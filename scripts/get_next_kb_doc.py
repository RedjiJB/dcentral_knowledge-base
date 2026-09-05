#!/usr/bin/env python3
"""
Scoped-context helper for the classify-kb-doc Skill (Stage 3, per-document pass).

Stage 3 originally classified all 428 KB docs at PROJECT granularity (classify_docs.py):
a 33-entry project->category lookup table, coarse by design at the time. This script
is the per-DOCUMENT replacement -- same scoped-context pattern as
get_next_conversation.py for Stage 2: find the next unclassified doc (checking
knowledge-base/_kb_doc_classified.jsonl for done doc_uuids), write ONLY that one
doc's front matter + content to a scratch file, so a classification session never
has to hold more than one document in context at a time.

Source of truth for "what needs classifying" is every .md file under
projects/kb-docs/**/*.md (the Stage-2 project-mirror extraction) PLUS every .md file
under conversations/artifacts/*.md (the Stage-2 gap-fill: docs created inline in a
conversation via create_file and never uploaded to a Project -- see
extract_conversation_artifacts.py) -- NOT the derived knowledge-base/ tree, which
stays a Stage-3 output. Conversation-artifact docs have no doc_uuid of their own
(they carry doc_id instead, e.g. "DC-SIM-003", which is NOT always unique -- a doc_id
can have multiple revisions/versions as separate files); the artifact's filename stem
is used as its doc_uuid instead, since that IS guaranteed unique.

Usage: python3 scripts/get_next_kb_doc.py [--count N]
Exit 0 + writes conversations/_scratch/current_kb_doc.json: one or more docs ready to classify.
  --count 1 (default): writes a single doc object (backward compatible shape).
  --count N > 1: writes a JSON array of up to N doc objects (batch mode) so a
  classification pass can read/write several documents per invocation instead
  of one round-trip per document.
Exit 1, no file written: everything is classified.
"""

import argparse
import json
import re
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DOCS_DIR = REPO_ROOT / "projects" / "kb-docs"
ARTIFACTS_DIR = REPO_ROOT / "conversations" / "artifacts"
CLASSIFIED_PATH = REPO_ROOT / "knowledge-base" / "_kb_doc_classified.jsonl"
SCRATCH_PATH = REPO_ROOT / "conversations" / "_scratch" / "current_kb_doc.json"
CONTENT_CHARS = 4000

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def parse_doc(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = FRONTMATTER_RE.match(text)
    front, body = {}, text
    if m:
        raw_front, body = m.group(1), m.group(2)
        for line in raw_front.splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                front[k.strip()] = v.strip()
    return front, body


def load_done():
    done = set()
    if CLASSIFIED_PATH.exists():
        for line in CLASSIFIED_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                done.add(json.loads(line)["doc_uuid"])
            except Exception:
                pass
    return done


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=1,
                         help="Number of unclassified docs to hand out at once (default 1).")
    args = parser.parse_args()
    count = max(1, args.count)

    if not KB_DOCS_DIR.exists():
        sys.exit(f"Missing {KB_DOCS_DIR}")

    done = load_done()
    project_docs = sorted(KB_DOCS_DIR.glob("*/*.md"))
    artifact_docs = sorted(ARTIFACTS_DIR.glob("*.md")) if ARTIFACTS_DIR.exists() else []
    all_docs = project_docs + artifact_docs
    remaining = len(all_docs) - len(done)

    batch = []
    for path in all_docs:
        if len(batch) >= count:
            break
        front, body = parse_doc(path)
        is_artifact = path in artifact_docs
        doc_uuid = path.stem if is_artifact else front.get("doc_uuid", "")
        if not doc_uuid or doc_uuid in done:
            continue

        batch.append({
            "doc_uuid": doc_uuid,
            "source_project": "conversation-artifacts" if is_artifact else front.get("source_project", ""),
            "original_filename": path.name if is_artifact else front.get("original_filename", ""),
            "relative_path": str(path.relative_to(REPO_ROOT)).replace("\\", "/"),
            "created_at": front.get("created_at", ""),
            "content_hash": front.get("content_hash", ""),
            "content_excerpt": body.strip()[:CONTENT_CHARS],
        })

    if not batch:
        print("Nothing left to classify.")
        return 1

    SCRATCH_PATH.parent.mkdir(parents=True, exist_ok=True)
    progress = (f"{len(done) + len(batch)}/{len(all_docs)} classified once this batch is appended "
                f"({remaining - len(batch)} remaining after this batch)")

    if count == 1:
        # Backward-compatible single-object shape.
        record = dict(batch[0])
        record["progress"] = progress
        with open(SCRATCH_PATH, "w", encoding="utf-8") as out:
            json.dump(record, out, indent=2, ensure_ascii=False)
        print(f"Wrote {SCRATCH_PATH.relative_to(REPO_ROOT)} -- {batch[0]['original_filename']!r} "
              f"({remaining} remaining)")
    else:
        with open(SCRATCH_PATH, "w", encoding="utf-8") as out:
            json.dump({"progress": progress, "docs": batch}, out, indent=2, ensure_ascii=False)
        print(f"Wrote {SCRATCH_PATH.relative_to(REPO_ROOT)} -- {len(batch)} docs "
              f"({remaining} remaining before this batch)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
