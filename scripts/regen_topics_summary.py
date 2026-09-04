#!/usr/bin/env python3
"""Regenerates knowledge-base/_topics_summary.md from the current per-category
_topics.md files (post subject-check resolution). Run after resolve_topic_review.py."""
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DIR = REPO_ROOT / "knowledge-base"

lines = ["# Stage 5 Topic Synthesis — Summary\n",
         "Subject-checked per DC-TOPIC-SYNTH-STD-001 SS4 -- see [TOPIC-RESOLUTION.md](../TOPIC-RESOLUTION.md) "
         "for every split/merge/demotion applied to the first-pass lexical clustering.\n"]

total_topics = total_clustered = total_ungrouped = 0
for cat_dir in sorted(p for p in KB_DIR.iterdir() if p.is_dir()):
    tp = cat_dir / "_topics.md"
    if not tp.exists():
        continue
    text = tp.read_text(encoding="utf-8")
    m = re.search(r"(\d+) docs\. (\d+) confirmed topics \((\d+) docs\), (\d+) ungrouped", text)
    if not m:
        continue
    total_docs, n_topics, n_clustered, n_ungrouped = map(int, m.groups())
    total_topics += n_topics
    total_clustered += n_clustered
    total_ungrouped += n_ungrouped
    rel = tp.relative_to(REPO_ROOT).as_posix()
    lines.append(f"- **{cat_dir.name}**: {total_docs} docs -> {n_topics} topics "
                 f"({n_clustered} docs clustered), {n_ungrouped} ungrouped -> [{rel}]({rel})")

lines.append(f"\n**Totals**: {total_topics} confirmed topic clusters, {total_clustered} docs clustered, "
             f"{total_ungrouped} ungrouped.\n")

(KB_DIR / "_topics_summary.md").write_text("\n".join(lines), encoding="utf-8")
print(f"Totals: {total_topics} topics, {total_clustered} clustered, {total_ungrouped} ungrouped.")
