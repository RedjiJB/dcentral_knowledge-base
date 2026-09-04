#!/usr/bin/env python3
"""
Applies the human/agent-confirmed verdicts for the Stage 4 review queue
(registry/dedup-review/*.md, produced by dedup_pass.py) after an actual
reading pass over every flagged pair -- not a re-run of the heuristic.

Verdicts applied here (see registry/dedup-review/_RESOLUTION.md for the
full reasoning per pair):

  - 9 explicit-language candidates: ALL FALSE POSITIVES. The heuristic's
    title-matching matched a generic single word ("Framework", "{Game Suite}")
    rather than a real cross-document reference. Confirmed by reading each
    sentence: all are product-description prose ("DAO governance replaces
    corporate control") or self-referential supersedes: metadata pointing at
    "scattered past conversations", not another indexed doc. No action.

  - 9 SUPERSEDES verdicts among the similarity candidates: same title
    re-uploaded to the same project's KB at a later timestamp with more
    content (confirmed by reading both, not just trusting recency). Older
    doc relocated to <category>/_superseded/<project>/, front matter on
    both sides gets supersedes/superseded_by/status fields.

  - 1 UNRESOLVED verdict (VDI-Solutions D-Central-Ecosystem-Haiti-Integration
    -Framework pair): later doc is smaller than the earlier one despite
    identical opening/TOC -- recency without engagement, contradicts the
    naive "later=bigger=supersedes" pattern the other 9 pairs fit. Per
    DC-DEDUP-STD-001 SS4, "no basis to prefer one" is a valid, expected
    outcome here, not a failure to force past. Both stay canonical, tagged
    status: disputed.
"""

import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def read_fm_and_body(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    end = text.find("\n---", 3)
    fm_text = text[3:end]
    body = text[end + 4:]
    return fm_text, body


def write_with_extra_fm(path, extra_fields):
    fm_text, body = read_fm_and_body(path)
    addition = "".join(f"{k}: {v}\n" for k, v in extra_fields.items())
    new_text = "---" + fm_text + addition + "---" + body
    path.write_text(new_text, encoding="utf-8")


SUPERSEDES_PAIRS = [
    # (newer/canonical, older/superseded, reason)
    ("knowledge-base/dcentral-ecosystem/D-Central-v2/D-Central-Edge-Distribution-Computation-Deep-Dive-md-4aa82ecd.md",
     "knowledge-base/dcentral-ecosystem/D-Central-v2/D-Central-Edge-Distribution-Computation-Deep-Dive-md.md",
     "Same title re-uploaded same project 4.5h later, 2.5x content (78648 vs 31970 chars) -- confirmed expansion, not coincidental overlap."),

    ("knowledge-base/dcentral-ecosystem/D-Central-v2/D-Central-Complete-Fractal-DAO-Governance-Architecture-md-7edde1e7.md",
     "knowledge-base/dcentral-ecosystem/D-Central-v2/D-Central-Complete-Fractal-DAO-Governance-Architecture-md.md",
     "Same title re-uploaded same project 24min later, 2.5x content (77116 vs 30721 chars)."),

    ("knowledge-base/haiti-initiative/Haiti-open-framework/Complete-Enhanced-Open-Source-Cooperative-Resilience-Framework-for-Haiti-md-fa474e23.md",
     "knowledge-base/haiti-initiative/Haiti-open-framework/Complete-Enhanced-Open-Source-Cooperative-Resilience-Framework-for-Haiti-md-d47533bb.md",
     "4-generation revision chain (see complete-framework-tex.md -> base .md -> d47533bb -> fa474e23), each later upload larger. fa474e23 is final/largest (314367 chars)."),

    ("knowledge-base/haiti-initiative/Haiti-open-framework/Complete-Enhanced-Open-Source-Cooperative-Resilience-Framework-for-Haiti-md-d47533bb.md",
     "knowledge-base/haiti-initiative/Haiti-open-framework/Complete-Enhanced-Open-Source-Cooperative-Resilience-Framework-for-Haiti-md.md",
     "Middle generation of the same revision chain -- see fa474e23 entry."),

    ("knowledge-base/haiti-initiative/Haiti-open-framework/Complete-Enhanced-Open-Source-Cooperative-Resilience-Framework-for-Haiti-md.md",
     "knowledge-base/haiti-initiative/Haiti-open-framework/complete-framework-tex.md",
     "Earliest generation: a LaTeX source (confirmed via \\documentclass header and matching pdftitle) of the same document, uploaded ~2.5h before the .md version begins the chain."),

    ("knowledge-base/haiti-initiative/Haiti-open-framework/haiti-security-proposal-md.md",
     "knowledge-base/haiti-initiative/Haiti-open-framework/hait-security-proposal-eng-tex.md",
     "Same memo (same recipient, subject, author) -- .tex LaTeX source vs .md prose version uploaded 30s later; treated as the .md prose version being the refined/final upload."),

    ("knowledge-base/verticals-products/Drone-Zoe/drone-selection-guide2-md-f756780a.md",
     "knowledge-base/verticals-products/Drone-Zoe/drone-selection-guide2-md.md",
     "Same title re-uploaded 6 weeks later, slightly larger (45039 vs 44929 chars)."),

    ("knowledge-base/verticals-products/Drone-Zoe/haiti-drone-cooperative-framework-md-ec202f4d.md",
     "knowledge-base/verticals-products/Drone-Zoe/haiti-drone-cooperative-framework-md.md",
     "Same title re-uploaded 6 weeks later, slightly larger (37524 vs 37340 chars)."),

    ("knowledge-base/verticals-products/Drone-Zoe/haiti-drone-expanded-strategy-md-eb50bcaa.md",
     "knowledge-base/verticals-products/Drone-Zoe/haiti-drone-expanded-strategy-md.md",
     "Same title re-uploaded 6 weeks later, near-identical size (34808 vs 34807 chars, 1.00 Jaccard) -- effectively a mechanical duplicate the content-hash check couldn't catch due to a trivial byte difference."),

    ("knowledge-base/verticals-products/Drone-Zoe/updated-drone-guide-md-1780e328.md",
     "knowledge-base/verticals-products/Drone-Zoe/updated-drone-guide-md.md",
     "Same title re-uploaded 6 weeks later, near-identical size (22234 vs 22228 chars)."),

    ("knowledge-base/verticals-products/Drone-Zoe/Comprehensive-Democratized-Development-Framework-for-Haiti-md-735f60aa.md",
     "knowledge-base/verticals-products/Drone-Zoe/Comprehensive-Democratized-Development-Framework-for-Haiti-md.md",
     "Same title re-uploaded 13 seconds later, nearly double content (61987 vs 33712 chars) -- confirmed expansion within the same upload session."),
]

UNRESOLVED_PAIRS = [
    ("knowledge-base/verticals-products/VDI-Solutions/D-Central-Ecosystem-Haiti-Integration-Framework-md-53dbf869.md",
     "knowledge-base/verticals-products/VDI-Solutions/D-Central-Ecosystem-Haiti-Integration-Framework-md.md",
     "Identical title and opening TOC, but the LATER upload (53dbf869, 19:36) is less than half the size of the EARLIER one (19:35, 130812 chars) -- contradicts the recency-implies-superset pattern every other pair in this batch fit. No explicit correction language, no engagement evidence either direction. Per DC-DEDUP-STD-001 SS4, this is a genuine 'no basis to prefer one' case, not a failure to resolve."),
]

FALSE_POSITIVE_NOTE = (
    "All 9 Step-2 explicit-language candidates flagged by dedup_pass.py were confirmed FALSE POSITIVES "
    "after reading the actual matched sentences. The heuristic matched generic single-word titles "
    "(\"Framework\", \"{Game Suite}\") rather than real cross-document references. Root causes found:\n"
    "  - Product-description prose using \"replaces/supersedes/deprecated\" as ordinary English "
    "(e.g. \"DAO governance replaces corporate control\", \"Replaces boring memorization\").\n"
    "  - Self-referential `supersedes:` front-matter metadata already present in three D-Central-V1 docs, "
    "pointing at \"scattered technical documentation across multiple directories\" (i.e. superseding "
    "unindexed past conversational scatter, not another doc in this corpus) -- not something Stage 4 "
    "needs to act on since there is no corresponding artifact here to relocate.\n"
    "No relocations applied for any of the 9.\n"
)


def resolve_path(rel):
    """A doc referenced as 'newer' in one pair may already have been relocated
    to _superseded/ earlier in this same run (multi-generational chains)."""
    direct = REPO_ROOT / rel
    if direct.exists():
        return direct
    alt = direct.parent / "_superseded" / direct.name
    if alt.exists():
        return alt
    return direct


def apply_supersedes(newer_rel, older_rel, reason):
    newer = resolve_path(newer_rel)
    older = resolve_path(older_rel)
    dest_dir = older.parent if older.parent.name == "_superseded" else older.parent / "_superseded"
    dest_dir.mkdir(exist_ok=True)
    dest = dest_dir / older.name
    if not older.exists():
        print(f"  SKIP (missing): {older_rel}")
        return None
    if older.parent.name == "_superseded":
        # already relocated by an earlier pair in this chain; just add metadata, don't re-move
        write_with_extra_fm(newer, {"superseded_docs": f"[{older.name}]"})
        write_with_extra_fm(older, {
            "status": "superseded",
            "superseded_by": newer.name,
            "supersession_reason": f'"{reason}"',
        })
        return older
    write_with_extra_fm(newer, {"superseded_docs": f"[{older.name}]"})
    write_with_extra_fm(older, {
        "status": "superseded",
        "superseded_by": newer.name,
        "supersession_reason": f'"{reason}"',
    })
    shutil.move(str(older), str(dest))
    return dest


def apply_unresolved(a_rel, b_rel, reason):
    a = REPO_ROOT / a_rel
    b = REPO_ROOT / b_rel
    for p in (a, b):
        write_with_extra_fm(p, {
            "status": "disputed",
            "conflicts_with": b.name if p == a else a.name,
            "unresolved_reason": f'"{reason}"',
        })


def main():
    print("Applying confirmed SUPERSEDES verdicts...")
    moved = []
    for newer, older, reason in SUPERSEDES_PAIRS:
        dest = apply_supersedes(newer, older, reason)
        if dest:
            moved.append((newer, str(dest.relative_to(REPO_ROOT)).replace("\\", "/")))
            print(f"  {older} -> _superseded/ (superseded by {Path(newer).name})")

    print("\nApplying confirmed UNRESOLVED verdicts...")
    for a, b, reason in UNRESOLVED_PAIRS:
        apply_unresolved(a, b, reason)
        print(f"  {a}  <-- disputed -->  {b}")

    resolution_path = REPO_ROOT / "registry" / "dedup-review" / "_RESOLUTION.md"
    with open(resolution_path, "w", encoding="utf-8") as f:
        f.write("# Stage 4 Review Queue — Resolution\n\n")
        f.write("Every item from `_SUMMARY.md`'s review queue was read and given an actual verdict "
                "(not re-run through the heuristic). Results:\n\n")
        f.write("## Explicit-language candidates (9 total)\n\n")
        f.write(FALSE_POSITIVE_NOTE + "\n")
        f.write(f"## SUPERSEDES verdicts applied ({len(SUPERSEDES_PAIRS)})\n\n")
        f.write("| Canonical (kept) | Superseded (moved to _superseded/) | Reason |\n|---|---|---|\n")
        for newer, older, reason in SUPERSEDES_PAIRS:
            f.write(f"| {newer} | {older} | {reason} |\n")
        f.write(f"\n## UNRESOLVED verdicts confirmed ({len(UNRESOLVED_PAIRS)})\n\n")
        f.write("| Doc A | Doc B | Why unresolved |\n|---|---|---|\n")
        for a, b, reason in UNRESOLVED_PAIRS:
            f.write(f"| {a} | {b} | {reason} |\n")

    print(f"\nWrote {resolution_path.relative_to(REPO_ROOT)}")
    print(f"\nTotals: {len(moved)} SUPERSEDES relocations applied, "
          f"{len(UNRESOLVED_PAIRS)} UNRESOLVED confirmed, 9 explicit-candidates dismissed as false positives.")


if __name__ == "__main__":
    main()
