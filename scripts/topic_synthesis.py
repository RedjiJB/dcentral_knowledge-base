#!/usr/bin/env python3
"""
Stage 5: DC-TOPIC-SYNTH-STD-001 -- cluster each category's surviving docs
(knowledge-base/<category>/, excluding _superseded/) into topic nodes finer
than "whole category".

Per the standard, this pass does NOT write prose (that's the Consolidator,
Stage 6) and does NOT relocate files (topic membership is a graph/index
concern -- physical materialization is Stage 7). It only decides what the
topics are and tags membership.

Method (a first-pass LEXICAL clustering, not semantic -- see caveats below):
  1. Tokenize each doc's body, drop stopwords and category-generic terms
     (anything appearing in >40% of the category's docs -- a crude IDF cut
     so "D-Central" or "mesh" don't dominate every cluster in that category).
  2. Pairwise Jaccard similarity on the remaining significant-word sets,
     requiring both a minimum ratio AND a minimum overlap count (guards
     against two short docs looking "similar" off a handful of shared words).
  3. STAR clustering, not connected-components: repeatedly pick the
     unclustered doc with the most direct (non-transitive) neighbors above
     threshold as a cluster seed, group it with only its direct neighbors,
     remove them, repeat. An earlier connected-components version chained
     transitively and collapsed entire categories into one "topic" (e.g.
     110/115 Infrastructure/Mesh docs in a single cluster) -- exactly the
     "keyword-clustering, too coarse" failure DC-TOPIC-SYNTH-STD-001 SS8
     warns about. Star clustering only groups docs directly similar to a
     seed, so two docs that are each similar to a popular hub but not to
     each other don't get merged transitively.
  4. A cluster of 1 (no doc similar enough to any other) is NOT forced into
     a topic -- DC-TOPIC-SYNTH-STD-001 SS1 requires >=2 sources for a topic
     node to be eligible. Singletons are listed separately as "ungrouped".
  5. Topic name = top 3 significant words shared across the cluster's docs
     (by combined frequency), joined with hyphens -- a placeholder label,
     not a designed name; SS4's actual calibration test (can you write one
     honest 2-4 sentence abstract without "and"?) needs a human/agent
     reading pass this script cannot do.

CAVEAT this script is honest about: word-overlap clustering is exactly the
failure mode DC-TOPIC-SYNTH-STD-001 SS8 warns against ("keyword-clustering
instead of subject-clustering"). This pass is a candidate-generation first
draft, not a finished Stage 5 -- every cluster should get a human/agent
subject-check before being treated as a real topic node, same as the dedup
pass's similarity candidates needed an actual reading pass before they
became verdicts.

Output: knowledge-base/<category>/_topics.md (this category's clusters +
ungrouped docs) and knowledge-base/_topics_summary.md (roll-up). Each
clustered doc gets a `topic:` front-matter field added for traceability.
"""

import re
from pathlib import Path
from collections import defaultdict, Counter

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DIR = REPO_ROOT / "knowledge-base"

TOPIC_THRESHOLD = 0.15
MIN_OVERLAP_WORDS = 6  # minimum shared significant words, on top of the ratio, to count as a link
GENERIC_CUTOFF = 0.4  # word appearing in >40% of a category's docs is too generic to define a topic

STOPWORDS = set("""
a an the and or but if then else for of to in on at by with from as is are was were be been being
this that these those it its it's their they them he she his her we our you your i not no yes can
could would should will shall may might must do does did done have has had having so such very more
most other some any all each every both few many much own same than too also just about into over
under again further once here there when where why how what which who whom above below between
""".split())


def tokenize(text):
    return [w for w in re.findall(r"[a-z']{3,}", text.lower()) if w not in STOPWORDS]


def parse_doc(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        fm_text, body = text[3:end], text[end + 4:]
    else:
        fm_text, body = "", text
    return fm_text, body


def write_topic_field(path, topic_slug):
    text = path.read_text(encoding="utf-8", errors="replace")
    end = text.find("\n---", 3)
    fm_text, body = text[3:end], text[end + 4:]
    if "\ntopic:" in fm_text or fm_text.startswith("topic:"):
        return  # already tagged
    text = "---" + fm_text + f"topic: {topic_slug}\n" + "---" + body
    path.write_text(text, encoding="utf-8")


def star_cluster(docs, sig_words, threshold, min_overlap):
    """Non-transitive clustering: repeatedly seed a cluster from the doc with
    the most direct neighbors, group it with only those direct neighbors,
    remove them all, repeat. Avoids single-link chaining collapsing a whole
    category into one cluster."""
    edges = defaultdict(set)
    doc_list = list(docs)
    for i, f1 in enumerate(doc_list):
        for f2 in doc_list[i + 1:]:
            a, b = sig_words[f1], sig_words[f2]
            if not a or not b:
                continue
            overlap = len(a & b)
            if overlap < min_overlap:
                continue
            score = overlap / len(a | b)
            if score >= threshold:
                edges[f1].add(f2)
                edges[f2].add(f1)

    remaining = set(doc_list)
    clusters = []
    while remaining:
        seed = max(remaining, key=lambda f: len(edges[f] & remaining))
        neighbors = edges[seed] & remaining
        if not neighbors:
            remaining.discard(seed)
            clusters.append([seed])  # singleton, filtered out by caller
            continue
        cluster = [seed] + sorted(neighbors)
        clusters.append(cluster)
        remaining -= set(cluster)
    return clusters


def main():
    categories = sorted(p for p in KB_DIR.iterdir() if p.is_dir())
    summary_lines = ["# Stage 5 Topic Synthesis — Summary\n",
                      "First-pass lexical clustering (word-overlap, not semantic). "
                      "Every cluster needs a human/agent subject-check before being treated as a "
                      "confirmed topic node -- see caveats in scripts/topic_synthesis.py.\n"]

    total_topics = 0
    total_clustered_docs = 0
    total_ungrouped = 0

    for cat_dir in categories:
        docs = sorted(f for f in cat_dir.rglob("*.md")
                       if f.name not in ("_INDEX.md", "_topics.md") and "_superseded" not in f.parts)
        if len(docs) < 2:
            continue

        doc_words = {}
        for f in docs:
            _, body = parse_doc(f)
            doc_words[f] = Counter(tokenize(body))

        # category-generic word cutoff
        doc_count = len(docs)
        doc_freq = Counter()
        for words in doc_words.values():
            for w in set(words):
                doc_freq[w] += 1
        generic = {w for w, c in doc_freq.items() if c / doc_count > GENERIC_CUTOFF}

        sig_words = {f: set(w for w in words if w not in generic) for f, words in doc_words.items()}

        raw_clusters = star_cluster(docs, sig_words, TOPIC_THRESHOLD, MIN_OVERLAP_WORDS)

        topics = []
        ungrouped = []
        for members in raw_clusters:
            if len(members) < 2:
                ungrouped.extend(members)
                continue
            combined = Counter()
            for m in members:
                combined.update(sig_words[m])
            top_words = [w for w, _ in combined.most_common(3)]
            topic_slug = "-".join(top_words) if top_words else f"topic-{len(topics)+1}"
            topics.append((topic_slug, members))

        for topic_slug, members in topics:
            for m in members:
                write_topic_field(m, topic_slug)

        total_topics += len(topics)
        total_clustered_docs += sum(len(m) for _, m in topics)
        total_ungrouped += len(ungrouped)

        topics_path = cat_dir / "_topics.md"
        with open(topics_path, "w", encoding="utf-8") as f:
            f.write(f"# Topics — {cat_dir.name}\n\n")
            f.write(f"{len(docs)} docs scanned. {len(topics)} topic clusters formed "
                    f"({sum(len(m) for _, m in topics)} docs), {len(ungrouped)} left ungrouped "
                    f"(no other doc in this category was similar enough -- not forced into a topic, "
                    f"per DC-TOPIC-SYNTH-STD-001 SS1's >=2-source requirement).\n\n")
            f.write("**First-pass lexical clustering — needs a human/agent subject-check per doc cluster "
                    "before being treated as a confirmed topic node.**\n\n")
            for topic_slug, members in sorted(topics, key=lambda t: -len(t[1])):
                f.write(f"## {topic_slug} ({len(members)} docs)\n\n")
                for m in sorted(members):
                    f.write(f"- [{m.relative_to(cat_dir).as_posix()}](./{m.relative_to(cat_dir).as_posix()})\n")
                f.write("\n")
            if ungrouped:
                f.write(f"## Ungrouped ({len(ungrouped)} docs)\n\n")
                for m in sorted(ungrouped):
                    f.write(f"- [{m.relative_to(cat_dir).as_posix()}](./{m.relative_to(cat_dir).as_posix()})\n")

        summary_lines.append(
            f"- **{cat_dir.name}**: {len(docs)} docs → {len(topics)} topics "
            f"({sum(len(m) for _, m in topics)} docs clustered), {len(ungrouped)} ungrouped "
            f"→ [{topics_path.relative_to(REPO_ROOT).as_posix()}]({topics_path.relative_to(REPO_ROOT).as_posix()})"
        )

    with open(KB_DIR / "_topics_summary.md", "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines) + "\n")
        f.write(f"\n**Totals**: {total_topics} topic clusters, {total_clustered_docs} docs clustered, "
                f"{total_ungrouped} ungrouped.\n")

    print(f"Formed {total_topics} topic clusters across {len(categories)} categories.")
    print(f"{total_clustered_docs} docs clustered, {total_ungrouped} left ungrouped.")
    print(f"Wrote {KB_DIR.relative_to(REPO_ROOT)}/_topics_summary.md and per-category _topics.md files.")


if __name__ == "__main__":
    main()
