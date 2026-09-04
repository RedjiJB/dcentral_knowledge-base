#!/usr/bin/env python3
"""
Stage 3 classifier: routes the 428 extracted KB docs (in projects/kb-docs/<project>/)
into a topic/vertical folder tree under knowledge-base/<category>/<project-slug>/<doc>.md.

Classification here is by PROJECT, using an explicit name -> category mapping drawn
from the project scope already documented in registry/EXPORT_ANALYSIS.md. This is
deliberately coarse (category-level, not per-document topic clusters) — per
DC-TOPIC-SYNTH-STD-001 §1, fine-grained topic nodes within a category are Stage 5's
job, not Stage 3's. Stage 3 only has to get docs out of "grouped by which Claude
Project they were uploaded to" and into "grouped by subject" at a coarse level.

Docs are COPIED, not moved — projects/kb-docs/ stays as the Stage-2 project-mirror
ground truth; knowledge-base/ is the Stage-3 derived view. If a project's docs later
get reclassified, regenerate knowledge-base/ from projects/kb-docs/ rather than
hand-editing it.

Every project must appear in PROJECT_CATEGORY below (script fails loudly on an
unmapped project, rather than silently dropping docs into an "unsorted" bucket)
so the mapping stays a complete, reviewable decision rather than a slow leak of
false-default classifications.
"""

import shutil
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KB_DOCS_DIR = REPO_ROOT / "projects" / "kb-docs"
OUT_DIR = REPO_ROOT / "knowledge-base"

# Project name (as it appears as a projects/kb-docs/ subfolder slug) -> category.
# Categories mirror registry/EXPORT_ANALYSIS.md's project breakdown.
PROJECT_CATEGORY = {
    "D-Central":                                "dcentral-ecosystem",
    "D-Central-v2":                              "dcentral-ecosystem",
    "D-Central-Live-Development":                "dcentral-ecosystem",
    "D-Central-Business-User-Application":       "dcentral-ecosystem",
    "D-Central-V1":                              "dcentral-ecosystem",
    "D-Central-v1-Phase-1":                      "dcentral-ecosystem",
    "D-Central-x-OBCC":                          "dcentral-ecosystem",
    "D-Central-Hardware-Software-Tech-Stack":    "dcentral-ecosystem",

    "Open-Secure":                               "security-identity",
    "Open-Vision":                               "security-identity",
    "Security-Ecosystem":                        "security-identity",

    "CivicMesh":                                 "infrastructure-mesh",
    "Local-Fediverse":                           "infrastructure-mesh",

    "Haiti-open-framework":                      "haiti-initiative",
    "Haiti-UN-Research":                         "haiti-initiative",
    "Haiti-Project-1":                           "haiti-initiative",
    "The-Division-Haiti":                        "haiti-initiative",

    "IHOSE":                                     "ai-ml-research",
    "Federated-Learning-Platform":               "ai-ml-research",
    "Federated-System-Integration":              "ai-ml-research",

    "Drone-Zoe":                                 "verticals-products",
    "CHOPSHOP":                                  "verticals-products",
    "Bounty":                                    "verticals-products",
    "VDI-Solutions":                             "verticals-products",
    "classIQ":                                   "verticals-products",

    "Algonquin-Courses":                         "academic-training",
    "Comptia-A":                                 "academic-training",
    "How-to-use-Claude":                         "academic-training",

    "API-World-Project":                         "other-experimental",
    "Departments-Project":                       "other-experimental",
    "Codegen":                                   "other-experimental",
    "RTS":                                       "other-experimental",
    "Portfolio-Projects":                        "other-experimental",
}

CATEGORY_TITLES = {
    "dcentral-ecosystem":   "D-Central Ecosystem",
    "security-identity":    "Security / Identity",
    "infrastructure-mesh":  "Infrastructure / Mesh",
    "haiti-initiative":     "Haiti Initiative",
    "ai-ml-research":       "AI / ML / Research",
    "verticals-products":   "Verticals / Products",
    "academic-training":    "Academic / Training",
    "other-experimental":   "Other / Experimental",
}


def slugify(name, maxlen=80):
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", name).strip("-")
    return (slug or "untitled")[:maxlen]


def main():
    if not KB_DOCS_DIR.exists():
        raise SystemExit(f"Missing {KB_DOCS_DIR} — run scripts/extract_project_docs.py first")

    project_dirs = sorted(p for p in KB_DOCS_DIR.iterdir() if p.is_dir())
    unmapped = [p.name for p in project_dirs if p.name not in PROJECT_CATEGORY]
    if unmapped:
        raise SystemExit(
            "Unmapped project folder(s) found — add them to PROJECT_CATEGORY before running:\n  "
            + "\n  ".join(unmapped)
        )

    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir(parents=True)

    category_counts = {cat: 0 for cat in CATEGORY_TITLES}
    category_projects = {cat: {} for cat in CATEGORY_TITLES}

    for proj_dir in project_dirs:
        category = PROJECT_CATEGORY[proj_dir.name]
        dest_dir = OUT_DIR / category / proj_dir.name
        dest_dir.mkdir(parents=True, exist_ok=True)
        doc_files = sorted(proj_dir.glob("*.md"))
        for doc_file in doc_files:
            shutil.copy2(doc_file, dest_dir / doc_file.name)
        category_counts[category] += len(doc_files)
        category_projects[category][proj_dir.name] = len(doc_files)

    # Per-category _INDEX.md
    for category, title in CATEGORY_TITLES.items():
        cat_dir = OUT_DIR / category
        if not cat_dir.exists():
            continue
        index_path = cat_dir / "_INDEX.md"
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(f"# {title}\n\n")
            f.write(f"{category_counts[category]} docs across {len(category_projects[category])} source projects.\n\n")
            f.write("| Project | Doc count |\n|---|---|\n")
            for proj, count in sorted(category_projects[category].items(), key=lambda kv: -kv[1]):
                f.write(f"| [{proj}](./{proj}/) | {count} |\n")

    # Top-level index
    with open(OUT_DIR / "_INDEX.md", "w", encoding="utf-8") as f:
        f.write("# Knowledge Base — Stage 3 Classification\n\n")
        f.write("Docs from `projects/kb-docs/` routed by category (project-level classification;\n")
        f.write("see DC-TOPIC-SYNTH-STD-001 for the finer per-topic clustering pass still to come).\n\n")
        f.write("| Category | Doc count | Projects |\n|---|---|---|\n")
        for category, title in CATEGORY_TITLES.items():
            if category_counts[category]:
                f.write(f"| [{title}](./{category}/_INDEX.md) | {category_counts[category]} | {len(category_projects[category])} |\n")

    total = sum(category_counts.values())
    print(f"Classified {total} docs into {sum(1 for c in category_counts.values() if c)} categories.")
    for category, title in CATEGORY_TITLES.items():
        if category_counts[category]:
            print(f"  {title}: {category_counts[category]}")


if __name__ == "__main__":
    main()
