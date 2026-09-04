# D-Central Knowledge Base — Session Context

This repo runs an 8-stage extraction/dedup/topic-synthesis/consolidation pipeline over a Claude
export (743 conversations, 33 projects, 428 KB docs). Full status: [PLAN.md](PLAN.md). Pipeline
standards: [standards/DC-PIPELINE-STD-001.md](standards/DC-PIPELINE-STD-001.md) and its siblings
(`DC-DEDUP-STD-001`, `DC-TOPIC-SYNTH-STD-001`, `DC-CONSOLIDATOR-STD-001`).

## If asked to classify conversations (Stage 2)

Use the `classify-conversation` skill (`.claude/skills/classify-conversation/SKILL.md`) — it defines
the full role, fixed taxonomy, numbered steps, output schema, and guardrails. Do not improvise a
different classification scheme; the whole point of the fixed taxonomy is consistency across
hundreds of independent invocations.

**Never read `raw-export/conversations/conversations.json` directly** — it's 320MB. Always go through
`scripts/get_next_conversation.py`, which extracts one conversation's scoped context to
`conversations/_scratch/current.json`.

A `PostToolUse` hook (`.claude/settings.json` → `scripts/validate_classification.py`) mechanically
rejects malformed classification records (invented category, missing fields, duplicate UUID) — this
is enforcement, not just instruction, so a bad record can't silently accumulate.

## General orientation

- `docs/` — core D-Central architecture specs (identity, credentialing, DAO-agent-loop, banking) plus
  Consolidator output (`DC-DION-RECONCILED-001.md` is the first worked example)
- `knowledge-base/` — Stage 3-5 output: 428 docs classified by category, deduped, clustered into
  topics. Regeneratable from `projects/kb-docs/` via the scripts in `scripts/` — don't hand-edit.
- `registry/dedup-review/` and `TOPIC-RESOLUTION.md` / `CROSS-POLLINATION-FINDINGS.md` — worked
  examples of the dedup and topic subject-check passes, useful as calibration references for how
  much rigor each stage expects.
- Raw export (`raw-export/`) is git-ignored — it's extraction input, not versioned content.

## Working style expected in this repo

Every non-mechanical judgment call (dedup verdicts, topic splits/merges, consolidation) should be a
real read-and-decide pass, not a rubber-stamp of a script's heuristic output — see the git history for
worked examples (the topic clusters that got corrected after being wrongly split by "different Claude
Project = different subject," or the DION/core architecture-duplication finding). Flag genuine
unresolved conflicts explicitly rather than forcing a verdict without a real basis.
