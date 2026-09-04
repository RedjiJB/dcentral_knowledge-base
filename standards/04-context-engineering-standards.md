# Standard: Context Engineering for Agent Roles

**Extends:** `00-master-architecture.md` §6 (Technology Stack). This document defines exactly what goes into every agent's context package, regardless of branch. Every agent role across every branch document should have one of these filled out before it's deployed.

---

## 1. Why this exists

Two failure modes, both costly:
- **Too much context:** facts buried in a long context get ignored (models attend unevenly across a long window); stale or contradictory context actively degrades output quality, not just wastes tokens ("context poisoning") — this happens often in multi-stage pipelines where an early agent's incomplete answer gets silently carried forward as fact by later agents.
- **Too little context:** the agent fills gaps with plausible-sounding invention instead of flagging the gap.

The operating discipline is four operations applied deliberately, not by default: **Write** (persist task state so it isn't lost), **Select** (retrieve only what's relevant when the source pool is noisy), **Compress** (summarize only after key facts are structured, not before), **Isolate** (separate contexts across domains/agents so they don't collide — a red-team agent's context and a UX-research agent's context should never share a pool).

---

## 2. The Context Package (6 components, required for every agent role)

### 2.1 Role
One narrow, bounded mandate with a concrete definition of "done."

**Bad:** "Help improve security."
**Good:** "Given the current CVE feed and our live asset inventory, identify vulnerabilities with CVSS ≥ 7.0 affecting assets in [scope], and rank by exploitability × exposure. Done = a ranked list with evidence, handed to the red-team agent for reproduction attempts."

A vague role invites the agent to self-expand scope — this is where both context bloat and off-target proposals originate.

### 2.2 Scoped context (retrieval, not dump)
Pull only what's relevant to this specific task from the memory layer (Neo4j / Obsidian per master doc §6.2):
- Recent related proposals (last N, or last N days, in this scope)
- Current metric baselines relevant to this task
- Prior outcomes for similar past proposals (what worked, what didn't, and why)

Do **not** hand the agent the full knowledge base "to be safe." If retrieval is noisy, that's a signal to improve the retrieval query (Select), not to widen the window.

**Standing instruction files** (the always-loaded part, as opposed to per-task retrieval) should stay lean — target well under 150 lines, lead with concrete examples and specific file/data references rather than general philosophy. If it scrolls more than two or three screens, the agent will skim it, not follow it. Anything reusable across many tasks belongs in a Skill (master doc §6.3), not in this always-loaded file.

### 2.3 Numbered, sequential steps
Break the task into an explicit ordered checklist, not an open-ended goal.

**Template:**
```
1. [Retrieve/pull specific data]
2. [Process/analyze — cluster, rank, cross-reference]
3. [Cross-reference against existing knowledge — check for duplicates/known issues]
4. [Form a specific output — hypothesis, finding, assessment]
5. [Validate or test that output against a defined check]
6. [Write the proposal/finding in the standard schema — see 2.5]
```

Numbered steps make the agent's *process* auditable after the fact by the meta-audit agent (master doc §4), not just its output.

### 2.4 Concrete examples (2–3, few-shot)
Include one strong past output and one weak one, each with a one-line note on why it landed where it did. Abstract quality descriptions ("be thorough," "be rigorous") don't transfer reliably; a worked example of the actual filled-in template does. This is also where tone and rigor bar get set without a separate style guide.

### 2.5 Exact output schema
Give the agent the literal structure to fill in — matching the proposal template in master doc §7 plus the branch-specific extension. Prefer a schema the next agent in the chain (synthesis, or a downstream tool) can parse deterministically:

```json
{
  "finding_id": "string",
  "role": "string (which agent role produced this)",
  "confidence": "0-1 float",
  "evidence": ["string, string, ..."],
  "recommendation": "string",
  "dissent": "string or null — disagreement from other agents on this same task, preserved verbatim"
}
```

Ambiguous output format is one of the most common silent failure points in a multi-agent pipeline — the next agent has to guess what a field means, and guesses compound.

### 2.6 Tools and guardrails
List only the tools this role actually needs (least privilege) — a UX-research agent doesn't need production write access; a synthesis agent doesn't need direct DAO vote-execution access. Boundaries are enforced by hooks (master doc §6.4), not by prose telling the agent what not to do. An instruction is a suggestion the model can drift from over a long session; a hook is a gate it structurally cannot pass.

---

## 3. SOUL.md Template (identity layer, master doc §6.1)

**Implementation note:** in the reconciled architecture, the agent's `role` field on its credential (DC-AGENT-CREDENTIAL-001 §2) is the durable identity pointer; this template is the versioned content that role points to, stored on the standard storage tier (not archived — it gets revised) and referenced by role type rather than duplicated per agent instance. The template itself, and the discipline of keeping it separate from per-task context, is unchanged below — only where it lives and how it's addressed has changed.

Separate from the context package above — this is loaded once per agent role and rarely changes.

```markdown
# SOUL: [Agent Role Name]

## Identity
Who this agent is, in one paragraph. Not what it does today — what kind of
agent it is, stably, across every run.

## Values
The 3-5 things this agent optimizes for, in priority order, and what it
explicitly does NOT optimize for (e.g. "thoroughness over speed;
never inflates severity to seem more useful").

## Voice
How this agent communicates in its outputs — terse/technical,
narrative, etc. Should match how the DAO actually wants to read proposals
from this role.

## Boundaries
What this agent will refuse or escalate rather than decide unilaterally,
independent of any specific task's instructions.
```

---

## 4. Memory Schema — see DC-MESHSTORAGE-ARCHIVE-001 for the full spec

Superseding the graph-database-specific version of this section: memory now maps onto storage tiers plus the attestation record, not a standalone database schema.

| Tier | Contents | Retention |
|---|---|---|
| **Standard storage — working state** | Current task/session state, working variables, draft findings | Cleared or superseded at session/task end |
| **Archive tier — durable record** | Finalized proposals and their outcomes | Permanent, Merkle-anchored (DC-MESHSTORAGE-ARCHIVE-001 §1) |
| **Attestation record — reasoning trace** | *Why* an agent concluded what it did — every finding an agent submits should reference the evidence and steps that produced it, captured as part of the attestation itself, not a separate database relationship | Permanent, queried by meta-audit agents and by future agents doing outcome-review |

Proposals render into a shared wiki space in human-readable form, organized by branch (`/infrastructure/`, `/features/`, `/business-ops/`), with each proposal linked to its supporting findings — this is what stakeholders actually read before a vote. See DC-DAO-AGENT-LOOP-001 §3 for why this replaced a standalone note-taking app in the reconciled design.

---

## 5. Role-based isolation

Different agent roles get different, non-overlapping default context scopes. A red-team agent's context pool and a UX-research agent's context pool should not share a retrieval index by default — cross-branch context sharing should be an explicit, logged exception (e.g., "this finding from the infra branch is relevant to a UX proposal"), not the default behavior.
