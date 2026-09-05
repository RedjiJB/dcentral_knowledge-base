#!/usr/bin/env python3
"""One-off: split 'federation-sovereignty-cooperative-platforms' -- confirmed during
the Stage 6 Consolidator prep read to conflate two unrelated projects' docs purely
because an earlier lexical pass matched on generic words ('sovereignty', 'cooperative',
'federation') -- into two real topics:

  - ihose-federation-ecosystem-partnership-framework (5 IHOSE docs: partner program /
    federation / ecosystem framework content)
  - federated-learning-platform-community-sovereignty-cooperative (6 Federated Learning
    Platform docs: community-owned education/professional-resource-sharing platform)

Rewrites each doc's topic: front-matter line and rewrites the corresponding section of
knowledge-base/_topics.md.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOPICS_MD = REPO_ROOT / "knowledge-base" / "_topics.md"
OLD_TOPIC = "federation-sovereignty-cooperative-platforms"

IHOSE_TOPIC = "ihose-federation-ecosystem-partnership-framework"
IHOSE_DOCS = [
    "knowledge-base/d-central/business-legal/IHOSE/IMPROVEMENT-RECOMMENDATIONS-md.md",
    "knowledge-base/d-central/core/governance/IHOSE/IHOSE-Federation-Ecosystem-Framework-md.md",
    "knowledge-base/d-central/meta/platform-scaffolding/IHOSE/IHOSE-Complete-Technical-Specification-Combined-md.md",
    "knowledge-base/d-central/meta/platform-scaffolding/IHOSE/Iron-Horse-IHOSE-Complete-Technical-Specification-docx.md",
    "knowledge-base/d-central/meta/platform-scaffolding/IHOSE/IronHorse-md.md",
]

FLP_TOPIC = "federated-learning-platform-community-sovereignty-cooperative"
FLP_DOCS = [
    "knowledge-base/d-central/business-legal/Federated-Learning-Platform/Universal-TDP-and-Derivative-Markets-Framework-md.md",
    "knowledge-base/d-central/core/economics/Federated-System-Integration/comprehensive-professional-cooperative-analysis-md.md",
    "knowledge-base/d-central/core/governance/Federated-System-Integration/comprehensive-government-public-sector-analysis-md.md",
    "knowledge-base/d-central/haiti-diaspora/Federated-Learning-Platform/Enhanced-Educational-Sovereignty-Framework-Complete-Technical-Integration-md.md",
    "knowledge-base/d-central/haiti-diaspora/Federated-Learning-Platform/Integrated-Community-Sovereignty-Platform-16-Sector-Integration-md.md",
    "knowledge-base/d-central/haiti-diaspora/Federated-Learning-Platform/comprehensive-educational-sovereignty-md.md",
]

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def retag(path: Path, new_topic: str):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = FRONTMATTER_RE.match(text)
    fm_lines = m.group(1).splitlines()
    fm_lines = [l for l in fm_lines if l.strip() not in (f'topic: "{OLD_TOPIC}"', f"topic: {OLD_TOPIC}")]
    fm_lines.append(f'topic: "{new_topic}"')
    new_text = "---\n" + "\n".join(fm_lines) + "\n---\n" + m.group(2)
    path.write_text(new_text, encoding="utf-8")


def main():
    for rel in IHOSE_DOCS:
        retag(REPO_ROOT / rel, IHOSE_TOPIC)
    for rel in FLP_DOCS:
        retag(REPO_ROOT / rel, FLP_TOPIC)
    print(f"Retagged {len(IHOSE_DOCS)} IHOSE docs -> {IHOSE_TOPIC}")
    print(f"Retagged {len(FLP_DOCS)} Federated-Learning-Platform docs -> {FLP_TOPIC}")

    text = TOPICS_MD.read_text(encoding="utf-8")
    heading_re = re.compile(r"^## " + re.escape(OLD_TOPIC) + r" \(\d+ docs?\)\s*$", re.MULTILINE)
    m = heading_re.search(text)
    if not m:
        raise SystemExit(f"Old topic heading not found: {OLD_TOPIC}")
    start = m.start()
    # find end of this section (next "## " heading or EOF)
    next_heading = re.search(r"^## ", text[m.end():], re.MULTILINE)
    end = m.end() + (next_heading.start() if next_heading else len(text) - m.end())

    def section(name, rel_paths):
        lines = [f"## {name} ({len(rel_paths)} docs)", ""]
        for rel in sorted(rel_paths):
            link = rel[len("knowledge-base/"):]
            lines.append(f"- [{link}](./{link})")
        lines.append("")
        lines.append("")
        return "\n".join(lines)

    new_sections = section(IHOSE_TOPIC, IHOSE_DOCS) + section(FLP_TOPIC, FLP_DOCS)
    new_text = text[:start] + new_sections + text[end:]
    TOPICS_MD.write_text(new_text, encoding="utf-8")
    print(f"Replaced 1 section with 2 sections in {TOPICS_MD.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
