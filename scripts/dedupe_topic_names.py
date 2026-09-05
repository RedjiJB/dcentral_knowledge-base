#!/usr/bin/env python3
"""Fix a data-quality bug found during Stage 6 prep: 4 topic pairs with
IDENTICAL membership got created under two different slug names (once from
an earlier pass, once when this session's Stage 5 work added a new topic
without checking for an existing near-duplicate). Each doc ended up with two
topic: front-matter lines pointing at the same 2-doc (or 4-doc) group under
different names. Merges each pair to one canonical name: removes the
redundant topic: line from each doc's front matter and removes the
redundant section from knowledge-base/_topics.md."""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_MD = REPO_ROOT / "knowledge-base" / "_topics.md"
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)

# duplicate_name -> canonical_name
MERGES = {
    "mitacs-accelerate-applications": "civicmesh-mitacs-accelerate-applications",
    "civicmesh-security-response-ops-training": "civicmesh-security-response-training",
    "communityshield-residential-deployment": "communityshield-hoa-deployment-package",
    "os-drone-advanced-capabilities": "opensecure-os-drone-advanced-capabilities",
}


def get_section_members(text, name):
    m = re.search(r"^## " + re.escape(name) + r" \(\d+ docs?\)\s*$", text, re.MULTILINE)
    if not m:
        return None, None, None
    next_h = re.search(r"^## ", text[m.end():], re.MULTILINE)
    end = m.end() + (next_h.start() if next_h else len(text) - m.end())
    section = text[m.start():end]
    rels = [l.split("](")[0][3:] for l in section.splitlines() if l.startswith("- [")]
    return m.start(), end, rels


def main():
    text = TOPICS_MD.read_text(encoding="utf-8")

    for dup_name, canon_name in MERGES.items():
        start, end, rels = get_section_members(text, dup_name)
        if start is None:
            print(f"SKIP (section not found): {dup_name}")
            continue
        # remove the duplicate section entirely
        text = text[:start] + text[end:]

        # strip the duplicate topic: line from each member doc's front matter
        for rel in rels:
            path = REPO_ROOT / "knowledge-base" / rel
            if not path.exists():
                print(f"MISSING: {rel}")
                continue
            doc_text = path.read_text(encoding="utf-8", errors="replace")
            m = FRONTMATTER_RE.match(doc_text)
            fm_lines = m.group(1).splitlines()
            fm_lines = [
                l for l in fm_lines
                if l.strip() not in (f'topic: "{dup_name}"', f"topic: {dup_name}")
            ]
            new_text = "---\n" + "\n".join(fm_lines) + "\n---\n" + m.group(2)
            path.write_text(new_text, encoding="utf-8")
        print(f"Merged '{dup_name}' -> '{canon_name}' ({len(rels)} docs)")

    TOPICS_MD.write_text(text, encoding="utf-8")

    total_topics = len(re.findall(r"^## ", text, re.MULTILINE))
    total_docs = text.count("\n- [")
    summary_path = REPO_ROOT / "knowledge-base" / "_topics_summary.md"
    summary = summary_path.read_text(encoding="utf-8")
    summary = re.sub(
        r"\*\*\d+ confirmed topic clusters, \d+ docs clustered\.\*\*",
        f"**{total_topics} confirmed topic clusters, {total_docs} docs clustered.**",
        summary,
    )
    summary_path.write_text(summary, encoding="utf-8")
    print(f"\nUpdated summary: {total_topics} topics, {total_docs} docs.")


if __name__ == "__main__":
    main()
