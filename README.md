# D-Central Knowledge Base

Repo home for D-Central's numbered standards, taxonomy docs, and document registry — migrated from the loose `Downloads` export staging area.

## Structure

```
standards/     00-05 numbered architecture/ops standards + DC-*-STD-001 pipeline standards
taxonomy/      DC-TAXONOMY-001..009
registry/      DC-REG-001 registry snapshots (deprecated) + extracted registry CSVs
docs/          Other DC-*-001 specs: agent governance (DAO loop, expert review, credential,
               observability, verifiable rollout) and knowledge-layer/storage architecture,
               plus platform/security/dual-lab architecture docs and the V24 unified source of truth
reference/     V24 reading lists, unified taxonomy docs, research-field/DePIN matrices, master timeline
scripts/       build_registry*.py (legacy) + extract_conversations.py (current Stage 1/2 extractor)
conversations/ Stage 1 extraction output: index of all 743 conversations + worked dedup example
projects/      Stage 1 index (33 projects) + Stage 2 artifacts: all 428 KB docs extracted to
               projects/kb-docs/<project>/<doc>.md, indexed in projects/_kb_docs_index.md
knowledge-base/ Stage 3 classification: the same 428 docs routed by category (dcentral-ecosystem,
               security-identity, infrastructure-mesh, haiti-initiative, ai-ml-research,
               verticals-products, academic-training, other-experimental) — regeneratable via
               scripts/classify_docs.py, do not hand-edit
raw-export/    Unzipped Claude export (conversations.json, project JSONs, memories) — git-ignored,
               this is extraction *input*, regenerate from the export zips + scripts/extract_conversations.py
```

Not included: the raw export zips themselves, installers/binaries, coursework, and ungrouped scratch
files from the Downloads staging area.

## Extraction status

See [PLAN.md](PLAN.md) for exactly where the real 743-conversation / 33-project export stands against
the eight pipeline stages, and what the next concrete extraction step is.

## Pipeline standards (new)

Four standards specify an automated extraction → dedup → topic-synthesis → consolidation pipeline meant to eventually replace the manual DC-REG-001 registry process:

1. [DC-DEDUP-STD-001](standards/DC-DEDUP-STD-001.md) — Stage 2.5: assigns canonical/superseded/merged status between artifacts
2. [DC-TOPIC-SYNTH-STD-001](standards/DC-TOPIC-SYNTH-STD-001.md) — Stage 5: clusters sources into topic nodes
3. [DC-CONSOLIDATOR-STD-001](standards/DC-CONSOLIDATOR-STD-001.md) — Stage 6: synthesizes one consolidated document per topic
4. [DC-PIPELINE-STD-001](standards/DC-PIPELINE-STD-001.md) — orchestration: ordering, triggers, failure handling, authority enforcement across all stages

Each stage has a distinct, non-overlapping authority (classify vs. cluster vs. synthesize) — see each standard's §0.

## Status

`registry/DC-REG-001-Master-Registry*.md` are both explicitly self-described as incomplete, unverified snapshots (v0.1 hand-curated, v0.2 regex-extracted from 713 conversation exports). Kept for reference; not maintained going forward. The pipeline above is intended to supersede manual registry upkeep once implemented.
