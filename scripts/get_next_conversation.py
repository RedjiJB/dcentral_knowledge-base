#!/usr/bin/env python3
"""
Scoped-context helper for the classify-conversation Skill.

Finds the next unclassified conversation (checking conversations/_classified.jsonl
for done UUIDs) and writes ONLY that conversation's title/summary/excerpt/doc-IDs
to a scratch file -- a few KB, not the 320MB raw export.

This exists specifically so a Claude Code session running the classify-conversation
skill never reads conversations.json directly. Reading a 320MB file into context
to classify one conversation would violate the whole scoped-context premise this
pipeline is built on -- this script does that extraction deterministically, outside
the agent's context window, every time.

Multi-session support: pass --session <name> to run more than one classification
pass concurrently without the two sessions colliding. Each session gets its own
scratch file (conversations/_scratch/current_<name>.json instead of the shared
current.json) and the script claims whichever uuid it hands out in
conversations/_scratch/_claims.json so a second session skips it instead of also
picking it. Claims expire after CLAIM_TTL_SECONDS so a session that dies mid-batch
doesn't permanently block that conversation. Running with no --session behaves
exactly as before (writes conversations/_scratch/current.json, claims as session
"default") -- a single-session pass is unaffected.

Usage: python3 scripts/get_next_conversation.py [--session NAME]
Exit code 0 + writes the scratch file: a conversation is ready to classify.
Exit code 1, no file written: everything is classified (or currently claimed by
another live session), nothing left to do right now.
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

# Windows consoles default stdout/stderr to cp1252, which can't encode emoji that show up
# in real conversation titles (e.g. a leading speech-bubble icon). Reconfigure to UTF-8 with
# a replace fallback so a fancy title never crashes the script after it already did the real
# work (claiming the uuid, writing the scratch file) -- losing only cosmetic characters in
# the printed confirmation line is fine; crashing here is not.
for _stream in (sys.stdout, sys.stderr):
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

REPO_ROOT = Path(__file__).resolve().parent.parent
CONV_PATH = REPO_ROOT / "raw-export" / "conversations" / "conversations.json"
CLASSIFIED_PATH = REPO_ROOT / "conversations" / "_classified.jsonl"
SCRATCH_DIR = REPO_ROOT / "conversations" / "_scratch"
CLAIMS_PATH = SCRATCH_DIR / "_claims.json"
EXCERPT_CHARS = 3000
CLAIM_TTL_SECONDS = 20 * 60  # a claim older than this is treated as a dead/abandoned session

DOC_ID_PATTERNS = [
    re.compile(r"\bDC-[A-Z0-9]+-\d{3}\b"),
    re.compile(r"\bOS-[A-Z0-9]+-\d{3}\b"),
]


def extract_doc_ids(text):
    found = set()
    for pat in DOC_ID_PATTERNS:
        found.update(pat.findall(text))
    return sorted(found)


def flatten_text(conv, limit=EXCERPT_CHARS):
    parts, total = [], 0
    for m in conv.get("chat_messages", []):
        content = m.get("content", [])
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    t = block.get("text", "")
                    if t:
                        parts.append(t)
                        total += len(t)
        if total >= limit:
            break
    return "\n".join(parts)[:limit]


def load_done():
    done = set()
    if CLASSIFIED_PATH.exists():
        with open(CLASSIFIED_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    done.add(json.loads(line)["uuid"])
                except Exception:
                    pass
    return done


def load_claims():
    if not CLAIMS_PATH.exists():
        return {}
    try:
        return json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_claims(claims):
    CLAIMS_PATH.parent.mkdir(parents=True, exist_ok=True)
    CLAIMS_PATH.write_text(json.dumps(claims, ensure_ascii=False, indent=2), encoding="utf-8")


def active_claims_by_others(claims, session, done, now):
    """uuids claimed by a different session, not yet done, within the TTL."""
    active = set()
    for uuid, info in claims.items():
        if uuid in done:
            continue
        if info.get("session") == session:
            continue
        if now - info.get("claimed_at", 0) <= CLAIM_TTL_SECONDS:
            active.add(uuid)
    return active


def prune_claims(claims, done, now):
    """Drop claims that are done or expired, so the file doesn't grow forever."""
    return {
        uuid: info
        for uuid, info in claims.items()
        if uuid not in done and now - info.get("claimed_at", 0) <= CLAIM_TTL_SECONDS
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--session", default="default",
                         help="Session name so concurrent runs don't collide. "
                              "Scratch file becomes current_<session>.json; the "
                              "default session still uses current.json.")
    args = parser.parse_args()
    session = args.session

    scratch_path = (SCRATCH_DIR / "current.json" if session == "default"
                    else SCRATCH_DIR / f"current_{session}.json")

    if not CONV_PATH.exists():
        sys.exit(f"Missing {CONV_PATH}")

    done = load_done()
    now = time.time()
    claims = load_claims()
    claims = prune_claims(claims, done, now)
    blocked = active_claims_by_others(claims, session, done, now)

    with open(CONV_PATH, "r", encoding="utf-8") as f:
        convs = json.load(f)

    remaining = len(convs) - len(done)

    for conv in convs:
        uuid = conv.get("uuid")
        if uuid in done or uuid in blocked:
            continue

        title = conv.get("name") or "(untitled)"
        summary = conv.get("summary") or ""
        excerpt = flatten_text(conv)
        doc_ids = extract_doc_ids(summary + " " + excerpt + " " + title)

        # Claim this uuid for this session before handing it out, so a concurrently
        # running session (different --session value) skips it on its next call.
        claims[uuid] = {"session": session, "claimed_at": now}
        save_claims(claims)

        scratch_path.parent.mkdir(parents=True, exist_ok=True)
        with open(scratch_path, "w", encoding="utf-8") as out:
            json.dump({
                "uuid": uuid,
                "title": title,
                "created_at": conv.get("created_at", ""),
                "summary": summary,
                "excerpt": excerpt,
                "extracted_doc_ids": doc_ids,
                "progress": f"{len(done) + 1}/{len(convs)} classified once this one is appended "
                            f"({remaining - 1} remaining after this one)",
            }, out, indent=2, ensure_ascii=False)

        print(f"Wrote {scratch_path.relative_to(REPO_ROOT)} -- {title[:70]!r} ({remaining} remaining)"
              + (f" [session={session}]" if session != "default" else ""))
        return 0

    if blocked:
        print(f"Nothing free to claim right now -- {len(blocked)} conversation(s) claimed by "
              f"other active session(s); try again shortly.")
    else:
        print("Nothing left to classify.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
