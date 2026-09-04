#!/usr/bin/env python3
"""
Stage 4 follow-up: catches exact-content duplicates that span CATEGORY
boundaries -- the gap dedup_pass.py explicitly left open (it only compares
within one category, since categories are the current topic-scope proxy).

Same rule as DC-DEDUP-STD-001 SS3 step 1: identical content_hash is not a
judgment call, it's a duplicate file. Canonical = earliest created_at across
the whole knowledge-base/ tree; every other copy (regardless of which
category it landed in) is relocated to its OWN category's _superseded/
folder, with front matter recording which cross-category doc it duplicates.

Already-superseded docs (anything already under a _superseded/ folder) are
excluded from consideration -- they're already resolved, re-flagging them
here would be noise.
"""

import re
from pathlib import Path
from collections import defaultdict
import shutil

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DIR = REPO_ROOT / "knowledge-base"


def parse_front_matter(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm = {}
    for line in text[3:end].strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


def write_with_extra_fm(path, extra_fields):
    text = path.read_text(encoding="utf-8", errors="replace")
    end = text.find("\n---", 3)
    fm_text, body = text[3:end], text[end + 4:]
    addition = "".join(f"{k}: {v}\n" for k, v in extra_fields.items())
    path.write_text("---" + fm_text + addition + "---" + body, encoding="utf-8")


def main():
    all_docs = [f for f in KB_DIR.rglob("*.md")
                if f.name != "_INDEX.md" and "_superseded" not in f.parts]

    by_hash = defaultdict(list)
    for f in all_docs:
        fm = parse_front_matter(f)
        chash = fm.get("content_hash", "")
        if chash:
            by_hash[chash].append((f, fm))

    cross_category_groups = []
    for chash, entries in by_hash.items():
        if len(entries) < 2:
            continue
        categories = {f.relative_to(KB_DIR).parts[0] for f, _ in entries}
        if len(categories) > 1:
            cross_category_groups.append((chash, entries))

    print(f"Found {len(cross_category_groups)} content hashes duplicated across categories "
          f"({sum(len(e) for _, e in cross_category_groups)} docs total).")

    relocated = []
    for chash, entries in cross_category_groups:
        entries.sort(key=lambda fe: fe[1].get("created_at", ""))
        canonical, canonical_fm = entries[0]
        dupes = entries[1:]
        for dup, dup_fm in dupes:
            dest_dir = dup.parent / "_superseded"
            dest_dir.mkdir(exist_ok=True)
            dest = dest_dir / dup.name
            write_with_extra_fm(canonical, {
                "cross_category_duplicate_at": f'"{dup.relative_to(KB_DIR).as_posix()}"'
            })
            write_with_extra_fm(dup, {
                "status": "duplicate",
                "duplicate_of": f'"{canonical.relative_to(KB_DIR).as_posix()}"',
                "duplicate_reason": '"exact content_hash match, different category (same doc uploaded to multiple Claude Projects)"',
            })
            shutil.move(str(dup), str(dest))
            relocated.append((dup.relative_to(REPO_ROOT).as_posix(),
                               dest.relative_to(REPO_ROOT).as_posix(),
                               canonical.relative_to(REPO_ROOT).as_posix()))

    report_path = REPO_ROOT / "registry" / "dedup-review" / "_CROSS_CATEGORY.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# Stage 4 Follow-up — Cross-Category Exact Duplicates\n\n")
        f.write(f"{len(cross_category_groups)} content hashes found duplicated across category boundaries, "
                f"{len(relocated)} docs relocated. Canonical = earliest created_at across the whole "
                f"knowledge-base/ tree, regardless of which category it's in.\n\n")
        f.write("| Original path (now moved) | Relocated to | Canonical (kept) |\n|---|---|---|\n")
        for orig, dest, canonical in relocated:
            f.write(f"| {orig} | {dest} | {canonical} |\n")

    print(f"Relocated {len(relocated)} cross-category duplicates.")
    print(f"Wrote {report_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
