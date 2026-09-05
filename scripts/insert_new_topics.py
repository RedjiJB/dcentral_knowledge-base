#!/usr/bin/env python3
"""One-off: insert the 23 newly-confirmed security/business-legal topics
(scripts/apply_confirmed_topics.py's TOPICS dict) into knowledge-base/_topics.md
in alphabetical order, matching the existing format, and bump the summary
counts in knowledge-base/_topics_summary.md."""

import re
from pathlib import Path
from apply_confirmed_topics import TOPICS

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_MD = REPO_ROOT / "knowledge-base" / "_topics.md"
SUMMARY_MD = REPO_ROOT / "knowledge-base" / "_topics_summary.md"

HEADING_RE = re.compile(r"^## (.+?) \(\d+ docs?\)\s*$")


def make_section(name, rel_paths):
    lines = [f"## {name} ({len(rel_paths)} docs)", ""]
    for rel in sorted(rel_paths):
        link = rel[len("knowledge-base/"):]
        lines.append(f"- [{link}](./{link})")
    lines.append("")
    return "\n".join(lines)


def main():
    text = TOPICS_MD.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    # Split into preamble + list of (name, section_text)
    sections = []
    preamble = []
    cur_name, cur_lines = None, []
    for line in lines:
        m = HEADING_RE.match(line.rstrip("\n"))
        if m:
            if cur_name is None:
                preamble = cur_lines
            else:
                sections.append((cur_name, "".join(cur_lines)))
            cur_name = m.group(1)
            cur_lines = [line]
        else:
            cur_lines.append(line)
    if cur_name is not None:
        sections.append((cur_name, "".join(cur_lines)))
    else:
        preamble = cur_lines

    existing_names = {n for n, _ in sections}
    added = 0
    for name, rel_paths in TOPICS.items():
        if name in existing_names:
            print(f"Already present, skipping: {name}")
            continue
        sections.append((name, make_section(name, rel_paths) + "\n"))
        added += 1

    sections.sort(key=lambda t: t[0])

    out = "".join(preamble) + "".join(s for _, s in sections)
    TOPICS_MD.write_text(out, encoding="utf-8")
    print(f"Inserted {added} new topic sections into {TOPICS_MD.relative_to(REPO_ROOT)}.")

    total_topics = len(sections)
    total_docs = sum(len(rel_paths) for _, rel_paths in [(n, TOPICS[n]) for n in TOPICS if n in dict(sections)] ) if False else None
    # compute total docs by counting bullet lines across all sections
    total_docs = sum(s.count("\n- [") for _, s in sections)

    summary = SUMMARY_MD.read_text(encoding="utf-8")
    summary = re.sub(
        r"\*\*\d+ confirmed topic clusters, \d+ docs clustered\.\*\*",
        f"**{total_topics} confirmed topic clusters, {total_docs} docs clustered.**",
        summary,
    )
    SUMMARY_MD.write_text(summary, encoding="utf-8")
    print(f"Updated summary: {total_topics} topics, {total_docs} docs.")


if __name__ == "__main__":
    main()
