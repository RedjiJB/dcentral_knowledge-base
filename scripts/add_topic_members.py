#!/usr/bin/env python3
"""One-off: add new members to EXISTING topic sections in knowledge-base/_topics.md
(apply_confirmed_topics.py's ADDITIONAL_TOPIC_TAGS -- docs that already carried a
different confirmed topic but genuinely also belong to one more, verified by
reading each doc, not by the lexical candidate grouping alone)."""

import re
from pathlib import Path
from apply_confirmed_topics import ADDITIONAL_TOPIC_TAGS

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_MD = REPO_ROOT / "knowledge-base" / "_topics.md"
SUMMARY_MD = REPO_ROOT / "knowledge-base" / "_topics_summary.md"

HEADING_RE = re.compile(r"^## (.+?) \((\d+) docs?\)\s*$")


def main():
    text = TOPICS_MD.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    added_total = 0
    i = 0
    out = []
    while i < len(lines):
        line = lines[i]
        m = HEADING_RE.match(line.rstrip("\n"))
        if m and m.group(1) in ADDITIONAL_TOPIC_TAGS:
            name = m.group(1)
            new_rels = [rel[len("knowledge-base/"):] for rel in ADDITIONAL_TOPIC_TAGS[name]]
            # collect existing section body
            body = [line]
            i += 1
            existing_links = set()
            while i < len(lines) and not HEADING_RE.match(lines[i].rstrip("\n")):
                body.append(lines[i])
                mlink = re.match(r"^- \[(.+?)\]", lines[i])
                if mlink:
                    existing_links.add(mlink.group(1))
                i += 1
            to_add = [r for r in new_rels if r not in existing_links]
            # insert new bullets before trailing blank line(s)
            while body and body[-1].strip() == "":
                trailing = body.pop()
            else:
                trailing = None
            for r in to_add:
                body.append(f"- [{r}](./{r})\n")
                added_total += 1
            new_count = len(existing_links) + len(to_add)
            body[0] = f"## {name} ({new_count} docs)\n"
            if trailing is not None:
                body.append(trailing)
            body.append("\n")
            out.extend(body)
            continue
        out.append(line)
        i += 1

    TOPICS_MD.write_text("".join(out), encoding="utf-8")
    print(f"Added {added_total} new member links to existing topic sections.")

    # recompute totals
    final_text = "".join(out)
    total_topics = len(HEADING_RE.findall(final_text))
    total_docs = final_text.count("\n- [")
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
