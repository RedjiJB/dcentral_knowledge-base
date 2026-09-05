#!/usr/bin/env python3
"""
Mechanical exact-content-hash dedup for one or more knowledge-base/d-central/
category directories -- the same "step 1" mechanical pass dedup_pass.py did
for the original 428 docs, run here against categories that either didn't
exist yet at that time (the fine-grained categories are new) or where the
duplicate was introduced afterward (e.g. two conversation-artifact copies).

For each exact-content-hash group found (excluding anything already under
_superseded/), keeps the doc with the EARLIEST created_at as canonical and
marks every other copy in the group status: duplicate, duplicate_of pointing
at the canonical copy's path, moving it to a _superseded/ subfolder under
its own current location (same convention as the original Stage 4 pass and
scripts/reconcile_knowledge_base.py).

Usage: python3 scripts/dedup_exact_hash.py <category-dir> [<category-dir> ...]
"""

import hashlib
import re
import sys
from pathlib import Path
from collections import defaultdict

REPO_ROOT = Path(__file__).resolve().parent.parent
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def parse(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    front = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            front[k.strip()] = v.strip()
    return front, m.group(2)


def body_hash(path):
    _, body = parse(path)
    return hashlib.sha256(body.encode("utf-8", errors="replace")).hexdigest()


def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 scripts/dedup_exact_hash.py <category-dir> [...]")

    total_resolved = 0
    for cat_arg in sys.argv[1:]:
        cat_dir = Path(cat_arg).resolve()
        by_hash = defaultdict(list)
        for f in cat_dir.rglob("*.md"):
            if "_superseded" in f.parts:
                continue
            by_hash[body_hash(f)].append(f)

        for h, files in by_hash.items():
            if len(files) < 2:
                continue
            files_with_meta = []
            for f in files:
                front, _ = parse(f)
                files_with_meta.append((front.get("created_at", ""), f, front))
            files_with_meta.sort(key=lambda t: t[0])
            canonical_created, canonical_path, _ = files_with_meta[0]

            for created, f, front in files_with_meta[1:]:
                text = f.read_text(encoding="utf-8", errors="replace")
                m = FRONTMATTER_RE.match(text)
                fm_lines = m.group(1).splitlines()
                canonical_rel = canonical_path.relative_to(REPO_ROOT).as_posix()
                fm_lines.append('status: "duplicate"')
                fm_lines.append(f'duplicate_of: "{canonical_rel}"')
                fm_lines.append('duplicate_reason: "exact body-hash match within the same '
                                 'category, resolved during Stage 5 topic-synthesis prep '
                                 '(never went through Stage 4 exact-hash dedup, which only '
                                 'covered the original 428 docs before this fine-grained '
                                 'reclassification)"')
                new_text = "---\n" + "\n".join(fm_lines) + "\n---\n" + m.group(2)

                dest = f.parent / "_superseded" / f.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(new_text, encoding="utf-8")
                f.unlink()
                print(f"Duplicate: {f.relative_to(REPO_ROOT)} -> {dest.relative_to(REPO_ROOT)} "
                      f"(canonical: {canonical_rel})")
                total_resolved += 1

    print(f"\nResolved {total_resolved} exact-duplicate copies.")


if __name__ == "__main__":
    main()
