#!/usr/bin/env python3
"""
Stage 5 first-pass candidate generation for ONE category directory (not the
whole knowledge-base/ tree -- topic_synthesis.py assumed knowledge-base/<cat>/
was the top-level layout, which is now knowledge-base/d-central/<cat>/ after
the fine-grained reconciliation).

Deliberately does NOT write topic: front matter or a _topics.md file. The
earlier run of topic_synthesis.py did that on the first pass, and an orphaned
first-pass tag (a garbage lexical slug superseded by the real subject-check
resolution but never cleaned out of the file) turned into a real, separately
tracked data-quality bug discovered during the knowledge-base/knowledge-base-
fine reconciliation. This script writes ONLY a scratch review file --
front matter is touched by a separate confirm step, only for clusters that
survive an actual read.

Same lexical star-clustering method as topic_synthesis.py (word-overlap,
non-transitive clustering, >=2-source minimum) -- a first-pass candidate
generator, not a finished Stage 5 pass. Every cluster still needs a human/
agent subject-check per DC-TOPIC-SYNTH-STD-001 SS4 before being treated as
a confirmed topic.

Usage: python3 scripts/topic_candidates.py <category-dir> <output-scratch.md>
Example: python3 scripts/topic_candidates.py knowledge-base/d-central/security
    conversations/_scratch/security_topic_candidates.md
"""

import re
import sys
from pathlib import Path
from collections import defaultdict, Counter

REPO_ROOT = Path(__file__).resolve().parent.parent

TOPIC_THRESHOLD = 0.15
MIN_OVERLAP_WORDS = 6
GENERIC_CUTOFF = 0.4

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
        return text[end + 4:]
    return text


def star_cluster(docs, sig_words, threshold, min_overlap):
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
            clusters.append([seed])
            continue
        cluster = [seed] + sorted(neighbors)
        clusters.append(cluster)
        remaining -= set(cluster)
    return clusters


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 scripts/topic_candidates.py <category-dir> <output-scratch.md>")

    cat_dir = Path(sys.argv[1]).resolve()
    out_path = Path(sys.argv[2]).resolve()
    if not cat_dir.is_dir():
        sys.exit(f"Not a directory: {cat_dir}")

    docs = sorted(f for f in cat_dir.rglob("*.md") if "_superseded" not in f.parts)
    doc_words = {f: Counter(tokenize(parse_doc(f))) for f in docs}

    doc_count = len(docs)
    doc_freq = Counter()
    for words in doc_words.values():
        for w in set(words):
            doc_freq[w] += 1
    generic = {w for w, c in doc_freq.items() if c / doc_count > GENERIC_CUTOFF}
    sig_words = {f: set(w for w in words if w not in generic) for f, words in doc_words.items()}

    raw_clusters = star_cluster(docs, sig_words, TOPIC_THRESHOLD, MIN_OVERLAP_WORDS)

    topics, ungrouped = [], []
    for members in raw_clusters:
        if len(members) < 2:
            ungrouped.extend(members)
        else:
            combined = Counter()
            for m in members:
                combined.update(sig_words[m])
            top_words = [w for w, _ in combined.most_common(3)]
            topics.append(("-".join(top_words) or "topic", members))

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"# Topic candidates — {cat_dir.as_posix()}\n\n")
        f.write(f"{len(docs)} docs scanned. {len(topics)} candidate clusters "
                f"({sum(len(m) for _, m in topics)} docs), {len(ungrouped)} singleton/ungrouped.\n\n")
        f.write("**Lexical first pass only -- not confirmed. Read each cluster's actual docs before "
                "treating any of this as a real topic.**\n\n")
        for slug, members in sorted(topics, key=lambda t: -len(t[1])):
            f.write(f"## candidate: {slug} ({len(members)} docs)\n\n")
            for m in sorted(members):
                f.write(f"- {m.relative_to(REPO_ROOT).as_posix()}\n")
            f.write("\n")
        if ungrouped:
            f.write(f"## Singletons ({len(ungrouped)})\n\n")
            for m in sorted(ungrouped):
                f.write(f"- {m.relative_to(REPO_ROOT).as_posix()}\n")

    print(f"{len(docs)} docs -> {len(topics)} candidate clusters, {len(ungrouped)} singletons.")
    print(f"Written to {out_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
