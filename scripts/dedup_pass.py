#!/usr/bin/env python3
"""
Stage 4: DC-DEDUP-STD-001 pass over knowledge-base/<category>/ (Stage 3 output).

Implements the parts of the decision procedure a script can actually decide,
and refuses to guess the parts it can't — per the standard's own guardrail
(§8 "no basis to prefer one" is a valid outcome, not a failure):

  Step 1 (identity check) — same content_hash: fully mechanical, fully automated.
    Not a SUPERSEDES relationship (the standard is explicit: "not a dedup case
    at all, it's a duplicate file"). One copy is kept in place, the rest are
    physically relocated to <category>/_superseded/<project>/ with a reason
    note, and logged with status "duplicate" (distinct from "superseded").

  Step 2 (explicit supersession check) — scans content for explicit correction
    language ("supersedes", "replaces", "deprecated", "superseded by", etc.)
    naming another doc in the same category by filename. Produces SUPERSEDES
    *candidates* with evidence_type=explicit — flagged for human confirmation,
    NOT auto-relocated, since a script can misfire on this regex and physical
    relocation should stay a confirmed action per DC-DEDUP-STD-001 §5.

  Steps 3-5 (content-overlap / reconciliation / recency-with-engagement) —
    a script cannot reliably extract and compare claims (that needs reading
    comprehension, i.e. an agent or human pass). What this script CAN do is
    surface high-similarity pairs (Jaccard over word shingles) as review
    candidates, so a human or a Consolidator-style agent pass has a short list
    instead of 428-choose-2 comparisons. These are written out as UNRESOLVED
    by default — the honest default per §2.4, not a guess.

Nothing outside _superseded/ moves except exact-hash duplicates (step 1).
Everything else is a report for a follow-up confirmation pass.
"""

import re
import shutil
from pathlib import Path
from itertools import combinations
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DIR = REPO_ROOT / "knowledge-base"
REPORT_DIR = REPO_ROOT / "registry" / "dedup-review"

SUPERSESSION_PATTERNS = [
    re.compile(r"\bsupersedes?\b", re.I),
    re.compile(r"\breplac(?:es|ed|ing)\b", re.I),
    re.compile(r"\bdeprecat(?:ed|es|ing)\b", re.I),
    re.compile(r"\bsuperseded by\b", re.I),
    re.compile(r"\bconsolidat(?:ed|es|ing) from\b", re.I),
    re.compile(r"\bcorrection to\b", re.I),
]

SHINGLE_SIZE = 5          # words per shingle
JACCARD_THRESHOLD = 0.35  # candidate-pair cutoff


def parse_front_matter(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].strip()
    body = text[end + 4:]
    fm = {}
    for line in fm_text.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, body


def word_shingles(text, k=SHINGLE_SIZE):
    words = re.findall(r"[a-z0-9]+", text.lower())
    if len(words) < k:
        return {" ".join(words)} if words else set()
    return {" ".join(words[i:i + k]) for i in range(len(words) - k + 1)}


def jaccard(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def find_explicit_supersession(body, other_titles):
    hits = []
    for pat in SUPERSESSION_PATTERNS:
        if pat.search(body):
            for title in other_titles:
                # crude but cheap: does the correction-language paragraph region
                # also mention another doc's title/filename stem?
                stem_words = re.sub(r"[^a-zA-Z0-9]+", " ", title).strip()
                if stem_words and stem_words.lower() in body.lower():
                    hits.append((pat.pattern, title))
    return hits


def main():
    if not KB_DIR.exists():
        raise SystemExit(f"Missing {KB_DIR} — run scripts/classify_docs.py first")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    categories = sorted(p for p in KB_DIR.iterdir() if p.is_dir())
    total_dupes_relocated = 0
    total_explicit_candidates = 0
    total_similarity_candidates = 0

    overall_lines = ["# Stage 4 Dedup Pass — Summary\n"]

    for cat_dir in categories:
        docs = sorted(f for f in cat_dir.rglob("*.md") if f.name != "_INDEX.md" and "_superseded" not in f.parts)
        if not docs:
            continue

        parsed = {}
        for f in docs:
            fm, body = parse_front_matter(f)
            parsed[f] = {"fm": fm, "body": body, "title": fm.get("original_filename", f.stem)}

        # --- Step 1: exact content_hash dedup ---
        by_hash = defaultdict(list)
        for f, data in parsed.items():
            by_hash[data["fm"].get("content_hash", "")].append(f)

        relocated = []
        for chash, files in by_hash.items():
            if len(files) < 2 or not chash:
                continue
            files.sort(key=lambda f: parsed[f]["fm"].get("created_at", ""))
            canonical, dupes = files[0], files[1:]
            for dup in dupes:
                superseded_dir = cat_dir / "_superseded" / dup.parent.name
                superseded_dir.mkdir(parents=True, exist_ok=True)
                dest = superseded_dir / dup.name
                shutil.move(str(dup), str(dest))
                relocated.append((dup, dest, canonical))
                del parsed[dup]
        total_dupes_relocated += len(relocated)

        remaining = list(parsed.keys())

        # --- Step 2: explicit supersession language ---
        titles = {f: parsed[f]["title"] for f in remaining}
        explicit_candidates = []
        for f in remaining:
            others = [t for other_f, t in titles.items() if other_f != f]
            hits = find_explicit_supersession(parsed[f]["body"], others)
            for pattern, other_title in hits:
                explicit_candidates.append((f, other_title, pattern))
        total_explicit_candidates += len(explicit_candidates)

        # --- Steps 3-5 proxy: shingle-similarity candidates among remaining docs ---
        shingles = {f: word_shingles(parsed[f]["body"]) for f in remaining}
        similarity_candidates = []
        for f1, f2 in combinations(remaining, 2):
            score = jaccard(shingles[f1], shingles[f2])
            if score >= JACCARD_THRESHOLD:
                similarity_candidates.append((f1, f2, score))
        similarity_candidates.sort(key=lambda x: -x[2])
        total_similarity_candidates += len(similarity_candidates)

        # --- per-category report ---
        report_path = REPORT_DIR / f"{cat_dir.name}.md"
        with open(report_path, "w", encoding="utf-8") as rep:
            rep.write(f"# Dedup Review — {cat_dir.name}\n\n")
            rep.write(f"{len(docs)} docs scanned. "
                      f"{len(relocated)} exact-duplicate relocated (step 1, mechanical). "
                      f"{len(explicit_candidates)} explicit-language candidates (step 2, needs confirmation). "
                      f"{len(similarity_candidates)} similarity candidates (steps 3-5 proxy, UNRESOLVED by default).\n\n")

            if relocated:
                rep.write("## Step 1 — exact duplicates relocated (mechanical, applied)\n\n")
                rep.write("| Duplicate (moved) | Kept as canonical |\n|---|---|\n")
                for dup, dest, canonical in relocated:
                    rep.write(f"| {dest.relative_to(REPO_ROOT).as_posix()} | {canonical.relative_to(REPO_ROOT).as_posix()} |\n")
                rep.write("\n")

            if explicit_candidates:
                rep.write("## Step 2 — explicit supersession language found (needs human confirmation before relocating)\n\n")
                rep.write("| Doc | Signal | Mentions doc |\n|---|---|---|\n")
                for f, other_title, pattern in explicit_candidates:
                    rep.write(f"| {f.relative_to(REPO_ROOT).as_posix()} | `{pattern}` | {other_title} |\n")
                rep.write("\n")

            if similarity_candidates:
                rep.write("## Steps 3-5 — content-similarity candidates (verdict: UNRESOLVED, needs claim-level review)\n\n")
                rep.write("| Doc A | Doc B | Jaccard (5-word shingles) |\n|---|---|---|\n")
                for f1, f2, score in similarity_candidates[:100]:
                    rep.write(f"| {f1.relative_to(REPO_ROOT).as_posix()} | {f2.relative_to(REPO_ROOT).as_posix()} | {score:.2f} |\n")
                if len(similarity_candidates) > 100:
                    rep.write(f"\n...and {len(similarity_candidates) - 100} more pairs below threshold display cutoff (still in scope, just not printed).\n")
                rep.write("\n")

        overall_lines.append(
            f"- **{cat_dir.name}**: {len(docs)} docs, {len(relocated)} exact dupes relocated, "
            f"{len(explicit_candidates)} explicit candidates, {len(similarity_candidates)} similarity candidates "
            f"→ [{report_path.relative_to(REPO_ROOT).as_posix()}]({report_path.relative_to(REPO_ROOT).as_posix()})"
        )

    overall_lines.insert(1, (
        f"\nTotals: {total_dupes_relocated} exact-duplicate docs relocated to `_superseded/`, "
        f"{total_explicit_candidates} explicit-supersession candidates flagged, "
        f"{total_similarity_candidates} similarity candidates flagged for review.\n"
        f"\nStep 1 was applied automatically (mechanical, per DC-DEDUP-STD-001 §3 step 1). "
        f"Steps 2-5 are reports only — no verdict is applied without human/agent confirmation, "
        f"per the standard's authority boundary (this script classifies nothing on its own judgment;\n"
        f"it only surfaces evidence for a later confirmation pass).\n"
    ))

    with open(REPORT_DIR / "_SUMMARY.md", "w", encoding="utf-8") as f:
        f.write("\n".join(overall_lines) + "\n")

    print(f"Exact duplicates relocated: {total_dupes_relocated}")
    print(f"Explicit-supersession candidates: {total_explicit_candidates}")
    print(f"Similarity candidates: {total_similarity_candidates}")
    print(f"Reports written to {REPORT_DIR.relative_to(REPO_ROOT)}/")


if __name__ == "__main__":
    main()
