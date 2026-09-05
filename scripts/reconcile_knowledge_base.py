#!/usr/bin/env python3
"""
Reconciles the two parallel Stage 3 outputs into one authoritative tree.

Before this script: knowledge-base/ (coarse, project-level Stage 3 classification,
8 categories) carries real accumulated Stage 4/5/6 work -- per-doc dedup status
(status: duplicate/superseded/disputed + duplicate_of/superseded_by/conflicts_with
fields), Stage 5 topic-cluster tags (topic: <slug>), and DION reconciliation notes.
knowledge-base-fine/ (fine-grained, per-document Stage 3 classification, 19
categories) is a clean copy straight from projects/kb-docs/ with no such metadata.

This script rebuilds knowledge-base/ AT THE FINE-GRAINED CATEGORY PATHS, carrying
every doc's accumulated dedup-status and topic-tag front matter forward onto its
new location, then retires knowledge-base-fine/ (its job is done -- it was staging
ground for exactly this merge). It also:
  - fixes a pre-existing formatting bug where content_hash and the next front-matter
    key were written on the same line with no newline between them
  - rewrites duplicate_of/superseded_by/conflicts_with path references (which point
    at other docs by their OLD coarse path) to the NEW fine-grained path
  - consolidates the eight per-category _INDEX.md/_topics.md files into one root
    _INDEX.md (regenerated from the new categories) and one root _topics.md
    (topic-cluster membership carried forward, paths rewritten, no longer
    partitioned by now-defunct coarse category)
  - places docs whose status is duplicate/superseded into a _superseded/ subfolder
    under their new category (matching the old convention); disputed docs stay in
    their normal location, matching how the Stage 4 review left them

Usage: python3 scripts/reconcile_knowledge_base.py
"""

import json
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DOCS_DIR = REPO_ROOT / "projects" / "kb-docs"
OLD_KB_DIR = REPO_ROOT / "knowledge-base"
FINE_KB_DIR = REPO_ROOT / "knowledge-base-fine"
CLASSIFIED_PATH = OLD_KB_DIR / "_kb_doc_classified.jsonl"

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)
EXTRA_KEYS = ("status", "duplicate_of", "duplicate_reason", "superseded_by",
              "supersession_reason", "conflicts_with", "unresolved_reason",
              "reconciliation_note", "topic")

OLD_TOPIC_CATEGORIES = ("academic-training", "ai-ml-research", "dcentral-ecosystem",
                         "haiti-initiative", "infrastructure-mesh", "security-identity",
                         "verticals-products")
TOPIC_LINK_RE = re.compile(r"^-\s*\[.*?\]\(\./(.+?)\)\s*$")
TOPIC_HEADING_RE = re.compile(r"^##\s+(.+?)\s+\(\d+ docs?\)\s*$")


def slugify(name):
    return re.sub(r"[^a-zA-Z0-9._-]+", "-", name).strip("-")


def split_frontmatter_lines(raw_fm):
    """Split raw front-matter text into lines, working around the known bug
    where 'content_hash: <hash>' and the next key ran together with no
    newline (e.g. 'content_hash: abc123status: duplicate')."""
    # Insert a newline before any of our known extra keys if they're glued
    # onto the end of the previous line (no preceding newline).
    fixed = raw_fm
    for key in EXTRA_KEYS:
        fixed = re.sub(rf"(?<!\n)({key}: )", r"\n\1", fixed)
    return [l for l in fixed.split("\n") if l.strip()]


def parse_old_doc(path):
    """Returns (doc_uuid, extras) with accumulated Stage 4/6 fields (dedup
    status, DION reconciliation notes). Does NOT read the front-matter
    'topic:' field -- confirmed by inspection to still carry orphaned
    first-pass auto-clustering slugs (e.g. 'amplifier-default-steward') that
    were superseded by the real Stage 5 subject-check resolution but never
    cleaned out of the doc's own front matter. The per-category _topics.md
    files are the authoritative, human-confirmed topic membership; see
    load_confirmed_topics() below, which sources from those instead."""
    text = path.read_text(encoding="utf-8", errors="replace")
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, {}
    lines = split_frontmatter_lines(m.group(1))
    doc_uuid = None
    extras = {}
    for line in lines:
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k, v = k.strip(), v.strip().strip('"')
        if k == "doc_uuid":
            doc_uuid = v
        elif k in EXTRA_KEYS and k != "topic":
            extras[k] = v
    return doc_uuid, extras


def load_confirmed_topics(old_path_to_uuid):
    """Parses the 7 per-category _topics.md files (the human-confirmed Stage 5
    output, per DC-TOPIC-SYNTH-STD-001 §4) for topic-name -> [doc_uuid] using
    each file's own bullet-linked doc paths, resolved through old_path_to_uuid.
    This is the authoritative topic membership -- see parse_old_doc's docstring
    for why front-matter 'topic:' tags are not used instead."""
    topics = {}
    for cat in OLD_TOPIC_CATEGORIES:
        path = OLD_KB_DIR / cat / "_topics.md"
        if not path.exists():
            continue
        current_topic = None
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            hm = TOPIC_HEADING_RE.match(line)
            if hm:
                current_topic = hm.group(1).strip()
                topics.setdefault(current_topic, [])
                continue
            lm = TOPIC_LINK_RE.match(line)
            if lm and current_topic:
                old_rel = f"{cat}/{lm.group(1)}"
                uuid = old_path_to_uuid.get(old_rel)
                if uuid:
                    topics[current_topic].append(uuid)
    return {t: uuids for t, uuids in topics.items() if uuids and t.lower() != "ungrouped"}


def main():
    if not CLASSIFIED_PATH.exists():
        sys.exit(f"Missing {CLASSIFIED_PATH} -- run classify-kb-doc pass first.")

    records = [json.loads(l) for l in CLASSIFIED_PATH.read_text(encoding="utf-8").splitlines() if l.strip()]

    # 1. Find every clean source doc (doc_uuid -> Path in projects/kb-docs/).
    source_docs = {}
    for path in sorted(KB_DOCS_DIR.glob("*/*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        if not m:
            continue
        front = {}
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                front[k.strip()] = v.strip()
        if front.get("doc_uuid"):
            source_docs[front["doc_uuid"]] = path

    # 2. Walk the OLD coarse tree: collect doc_uuid -> extras, and
    #    old_relpath -> doc_uuid (for remapping duplicate_of/superseded_by).
    old_extras = {}
    old_path_to_uuid = {}
    for path in OLD_KB_DIR.rglob("*.md"):
        if path.name.startswith("_"):
            continue
        rel = path.relative_to(OLD_KB_DIR).as_posix()
        doc_uuid, extras = parse_old_doc(path)
        if not doc_uuid:
            continue
        old_path_to_uuid[rel] = doc_uuid
        if extras:
            old_extras[doc_uuid] = extras

    # 2b. Confirmed Stage 5 topic membership (doc_uuid -> [topic names]),
    #     sourced from the human-confirmed _topics.md files, not front matter.
    confirmed_topics = load_confirmed_topics(old_path_to_uuid)
    doc_confirmed_topics = {}
    for topic, uuids in confirmed_topics.items():
        for uuid in uuids:
            doc_confirmed_topics.setdefault(uuid, []).append(topic)

    # 3. Compute each doc's NEW relative path (category/project/[_superseded/]file).
    new_relpath = {}
    doc_meta = {}
    for rec in records:
        uuid = rec["doc_uuid"]
        src = source_docs.get(uuid)
        if not src:
            continue
        extras = old_extras.get(uuid, {})
        status = extras.get("status", "")
        project_slug = slugify(rec["source_project"])
        subdir = "_superseded/" if status in ("duplicate", "superseded") else ""
        rel = f"{rec['primary_category']}/{project_slug}/{subdir}{src.name}"
        new_relpath[uuid] = rel
        doc_meta[uuid] = {"src": src, "rec": rec, "extras": extras}

    def remap_path_field(value):
        """duplicate_of/superseded_by/conflicts_with store an OLD coarse
        relative path (relative to knowledge-base/). Resolve it through the
        old-path->uuid->new-path chain; if unresolvable, keep the original
        value with a note (shouldn't happen for the docs in this pipeline,
        but don't silently drop information if it does)."""
        candidate = value.strip('"')
        target_uuid = old_path_to_uuid.get(candidate)
        if target_uuid and target_uuid in new_relpath:
            return f"knowledge-base/{new_relpath[target_uuid]}"
        return f"{value} [unresolved during reconciliation -- old path, target not found in new tree]"

    # 4. Write every doc at its new path with reconstructed front matter.
    if OLD_KB_DIR.exists():
        for child in OLD_KB_DIR.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            elif child.name not in ("_kb_doc_classified.jsonl",):
                child.unlink()

    placed = 0
    for uuid, meta in doc_meta.items():
        src, rec, extras = meta["src"], meta["rec"], meta["extras"]
        text = src.read_text(encoding="utf-8", errors="replace")
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
        base_fm, body = m.group(1), m.group(2)

        fm_lines = base_fm.splitlines()
        for key in ("status", "duplicate_of", "duplicate_reason",
                    "superseded_by", "supersession_reason",
                    "conflicts_with", "unresolved_reason", "reconciliation_note"):
            if key in extras:
                val = extras[key]
                if key in ("duplicate_of", "superseded_by", "conflicts_with"):
                    val = remap_path_field(val)
                    fm_lines.append(f'{key}: "{val}"')
                else:
                    fm_lines.append(f"{key}: {val}")
        for topic in doc_confirmed_topics.get(uuid, []):
            fm_lines.append(f"topic: {topic}")

        dest = OLD_KB_DIR / new_relpath[uuid]
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text("---\n" + "\n".join(fm_lines) + "\n---\n" + body, encoding="utf-8")
        placed += 1

    # 5. Regenerate root _INDEX.md from the new category structure.
    from collections import defaultdict
    cat_counts = defaultdict(lambda: {"docs": 0, "projects": set()})
    for uuid, meta in doc_meta.items():
        cat = meta["rec"]["primary_category"]
        cat_counts[cat]["docs"] += 1
        cat_counts[cat]["projects"].add(meta["rec"]["source_project"])

    index_lines = [
        "# Knowledge Base — Stage 3 Classification (fine-grained, per-document)",
        "",
        "Docs from `projects/kb-docs/` routed by per-document content classification",
        "(see PLAN.md's Stage 3 reconciliation note). Dedup status (Stage 4) and topic",
        "clusters (Stage 5) are carried forward as front-matter fields on each doc and",
        "summarized in `_topics.md`.",
        "",
        "| Category | Doc count | Projects |",
        "|---|---|---|",
    ]
    for cat in sorted(cat_counts):
        c = cat_counts[cat]
        index_lines.append(f"| `{cat}` | {c['docs']} | {len(c['projects'])} |")
    (OLD_KB_DIR / "_INDEX.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    # 6. Consolidate topic clusters into one root _topics.md, paths rewritten.
    topics = defaultdict(list)
    for uuid in doc_meta:
        for t in doc_confirmed_topics.get(uuid, []):
            topics[t].append(new_relpath[uuid])
    topic_lines = [
        "# Stage 5 Topic Clusters (consolidated)",
        "",
        "Carried forward from the original per-category `_topics.md` files after the",
        "Stage 3 fine-grained reconciliation -- topic membership is unchanged, only the",
        "document paths were rewritten to their new fine-grained-category locations.",
        "See [TOPIC-RESOLUTION.md](../TOPIC-RESOLUTION.md) for the reasoning behind",
        "every split/merge/demotion. Docs in one topic may now span several fine",
        "categories -- that's expected; topics are semantic clusters, independent of",
        "the taxonomy category a document's own content earned it.",
        "",
    ]
    for topic in sorted(topics):
        paths = topics[topic]
        topic_lines.append(f"## {topic} ({len(paths)} docs)")
        topic_lines.append("")
        for p in sorted(paths):
            topic_lines.append(f"- [{p}](./{p})")
        topic_lines.append("")
    (OLD_KB_DIR / "_topics.md").write_text("\n".join(topic_lines), encoding="utf-8")

    total_topic_docs = sum(len(v) for v in topics.values())
    summary_lines = [
        "# Stage 5 Topic Synthesis — Summary (consolidated)",
        "",
        "Subject-checked per DC-TOPIC-SYNTH-STD-001 §4 -- see "
        "[TOPIC-RESOLUTION.md](../TOPIC-RESOLUTION.md) for every split/merge/demotion.",
        "",
        f"**{len(topics)} confirmed topic clusters, {total_topic_docs} docs clustered.** "
        "See [_topics.md](./_topics.md) for full membership -- no longer partitioned by "
        "category folder, since fine-grained per-document categories cut across the old "
        "coarse partitions.",
        "",
    ]
    (OLD_KB_DIR / "_topics_summary.md").write_text("\n".join(summary_lines), encoding="utf-8")

    # 7. Retire knowledge-base-fine/ -- its job (staging this merge) is done.
    if FINE_KB_DIR.exists():
        shutil.rmtree(FINE_KB_DIR)

    print(f"Reconciled {placed} docs into knowledge-base/ at fine-grained category paths.")
    print(f"Carried forward {len(old_extras)} docs' dedup/topic metadata.")
    print(f"Consolidated {len(topics)} topic clusters into knowledge-base/_topics.md.")
    print(f"Retired {FINE_KB_DIR.relative_to(REPO_ROOT)}/.")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
