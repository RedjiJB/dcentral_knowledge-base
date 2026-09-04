# D-Central Knowledge Base

Repo home for D-Central's numbered standards, taxonomy docs, and document registry — migrated from the loose `Downloads` export staging area.

## Structure

```
standards/   00-05 numbered architecture/ops standards + DC-*-STD-001 pipeline standards
taxonomy/    DC-TAXONOMY-001..009
registry/    DC-REG-001 master document registry (v0.1, v0.2 — both deprecated snapshots)
docs/        Other DC-*-001 specs: agent governance (DAO loop, expert review, credential,
             observability, verifiable rollout) and knowledge-layer/storage architecture
```

## Pipeline standards (new)

Four standards specify an automated extraction → dedup → topic-synthesis → consolidation pipeline meant to eventually replace the manual DC-REG-001 registry process:

1. [DC-DEDUP-STD-001](standards/DC-DEDUP-STD-001.md) — Stage 2.5: assigns canonical/superseded/merged status between artifacts
2. [DC-TOPIC-SYNTH-STD-001](standards/DC-TOPIC-SYNTH-STD-001.md) — Stage 5: clusters sources into topic nodes
3. [DC-CONSOLIDATOR-STD-001](standards/DC-CONSOLIDATOR-STD-001.md) — Stage 6: synthesizes one consolidated document per topic
4. [DC-PIPELINE-STD-001](standards/DC-PIPELINE-STD-001.md) — orchestration: ordering, triggers, failure handling, authority enforcement across all stages

Each stage has a distinct, non-overlapping authority (classify vs. cluster vs. synthesize) — see each standard's §0.

## Status

`registry/DC-REG-001-Master-Registry*.md` are both explicitly self-described as incomplete, unverified snapshots (v0.1 hand-curated, v0.2 regex-extracted from 713 conversation exports). Kept for reference; not maintained going forward. The pipeline above is intended to supersede manual registry upkeep once implemented.
