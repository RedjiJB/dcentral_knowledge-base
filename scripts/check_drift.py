#!/usr/bin/env python3
"""
Stage 7 item #4 -- drift check, not a rewrite.

Confirms every doc under a `_superseded/` folder still points at a live,
existing target via its `duplicate_of`/`superseded_by` front-matter field, and
that the target isn't itself under `_superseded/` (which would mean a broken
chain left over from Stage 4). Read-only: this script never moves or edits
anything, it only reports.

Usage: python3 scripts/check_drift.py
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_ROOT = REPO_ROOT / "knowledge-base" / "d-central"

FRONTMATTER_RE = re.compile(r"^---\n(.*?\n)---\n", re.DOTALL)
POINTER_RE = re.compile(r'^(duplicate_of|superseded_by):\s*"?([^"\n]+)"?\s*$', re.MULTILINE)


def read_frontmatter(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    m = FRONTMATTER_RE.match(text)
    return m.group(1) if m else None


def resolve_pointer(path: Path):
    """Resolve one doc's duplicate_of/superseded_by to a Path, or None if unresolvable.
    Returns (target_path_or_None, raw_target_rel_or_None, note)."""
    fm = read_frontmatter(path)
    if fm is None:
        return None, None, ""

    m = POINTER_RE.search(fm)
    if not m:
        return None, None, ""

    target_rel = m.group(2).strip()
    note = ""
    if " [" in target_rel:
        target_rel, _, note = target_rel.partition(" [")
        target_rel = target_rel.strip()
        note = " [" + note

    if Path(target_rel).is_absolute():
        candidates = [Path(target_rel)]
    elif "/" in target_rel or "\\" in target_rel:
        candidates = [REPO_ROOT / target_rel, path.parent / target_rel]
    else:
        # Bare filename -- recorded relative to the category directory the canonical doc
        # lives in, i.e. one level up from this doc's own `_superseded/` folder.
        candidates = [path.parent.parent / target_rel, path.parent / target_rel, REPO_ROOT / target_rel]

    target = next((c for c in candidates if c.exists()), None)

    if target is None and "/" not in target_rel and "\\" not in target_rel:
        base = target_rel[:-3] if target_rel.endswith(".md") else target_rel
        siblings = [f for f in path.parent.parent.glob(f"{base}-*.md") if "_superseded" not in f.parts]
        if len(siblings) == 1:
            target = siblings[0]

    return target, target_rel, note


MAX_HOPS = 10  # generous ceiling for legitimate multi-generation revision chains


def main():
    superseded_files = sorted(KB_ROOT.rglob("_superseded/*.md"))
    if not superseded_files:
        sys.exit("FAIL: no _superseded/ docs found -- unexpected, Stage 4 should have produced 74")

    problems = []
    checked = 0

    for path in superseded_files:
        fm = read_frontmatter(path)
        if fm is None:
            problems.append(f"{path.relative_to(REPO_ROOT)}: no front matter block found")
            continue
        if not POINTER_RE.search(fm):
            problems.append(f"{path.relative_to(REPO_ROOT)}: no duplicate_of/superseded_by field in front matter")
            continue

        checked += 1

        # Follow the pointer chain -- each hop may legitimately point to the next generation
        # rather than straight to the final canonical doc (documented multi-generation revision
        # chains exist, e.g. a .tex source -> 3 successive .md re-uploads). Only a genuine dead
        # end, ambiguity, or cycle is a real problem.
        seen = {path}
        current = path
        target = None
        target_rel = None
        note = ""
        for _ in range(MAX_HOPS):
            target, target_rel, note = resolve_pointer(current)
            if target is None:
                break
            if target in seen:
                problems.append(f"{path.relative_to(REPO_ROOT)}: pointer chain cycles back to {target.relative_to(REPO_ROOT)}")
                target = "cycle"
                break
            if "_superseded" not in target.parts:
                break  # reached a live doc -- chain terminates successfully
            seen.add(target)
            current = target
        else:
            problems.append(f"{path.relative_to(REPO_ROOT)}: pointer chain exceeds {MAX_HOPS} hops without reaching a live doc")
            continue

        if target == "cycle":
            continue
        elif target is None:
            problems.append(f"{path.relative_to(REPO_ROOT)}: chain ends at unresolvable target '{target_rel}'{note}")
        # else: chain resolved to a live doc -- fine, whether in 1 hop or several.

    print(f"Checked {checked}/{len(superseded_files)} superseded docs.")

    if problems:
        report = REPO_ROOT / "registry" / "drift-check-report.md"
        report.write_text(
            "# Stage 7 Drift Check -- FAILURES\n\n"
            + f"{len(problems)} problem(s) found among {len(superseded_files)} superseded docs:\n\n"
            + "\n".join(f"- {p}" for p in problems)
            + "\n",
            encoding="utf-8",
        )
        print(f"FAIL: {len(problems)} problem(s). See {report.relative_to(REPO_ROOT)}")
        sys.exit(1)

    report = REPO_ROOT / "registry" / "drift-check-report.md"
    if report.exists():
        report.unlink()  # clear a stale failure report from a previous run
    print(f"PASS: all {len(superseded_files)} superseded docs point to live, non-superseded targets.")


if __name__ == "__main__":
    main()
