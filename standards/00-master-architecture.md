# Master Architecture: Self-Improving DAO + Agent System

**Status:** Design reference
**Scope:** This document defines the system every branch (infrastructure, features, business operations, and future branches) inherits from. Branch documents extend this — they do not redefine it. If a branch needs to deviate from something here, the deviation and its reasoning should be stated explicitly in that branch's document.

---

## 1. Purpose

A closed-loop system in which:
- A DAO sets **scope and mandate** for what should be researched/improved.
- Specialized **AI agents** research, test, and draft proposals within that scope.
- The DAO **votes** on proposals before anything ships.
- **Monitoring agents** track real-world impact after implementation.
- **Stakeholder feedback** and monitoring data feed the next scope vote.

The loop is domain-agnostic. What changes per branch is: agent specialization, what counts as ground truth for "did this work," and where the human sign-off threshold sits.

---

## 2. The Core Loop

```
1. DAO Scope Vote          → sets mandate + budget for an agent swarm
2. Agent Research Swarm    → recon, adversarial, defensive, analysis agents work in parallel
3. Proposal Synthesis      → a synthesis agent compiles findings into one structured proposal
4. DAO Review & Vote       → stakeholders (or delegates/council for emergencies) approve or reject
5. Gated Implementation    → staged rollout, automatic circuit breakers, human sign-off above threshold
6. Impact Monitoring       → monitoring agents track the metrics defined in the proposal
7. Stakeholder Feedback    → informs the next scope vote; retrospective vote confirms/reverses
   ↻ loop repeats — scope itself can evolve based on what was learned
```

No agent that researches or drafts a proposal has DAO voting power over that proposal. No agent that proposes a change is also the one that approves or implements it. This separation is structural, not a norm — it should be enforced by tooling (see §6), not just written down.

---

## 3. DAO Governance Layer

### 3.1 Four vote types

| Vote type | Frequency | Who votes | Purpose |
|---|---|---|---|
| **Scope vote** | Infrequent (e.g. monthly/quarterly) | Full DAO | Defines mandate + compute/API budget for an agent swarm |
| **Proposal vote** | Per proposal | Full DAO (standard cycle, e.g. 3–7 days) | Approves/rejects an implementation |
| **Emergency fast-track** | As needed | Smaller multisig council / delegate quorum | Approves time-critical action (e.g. active exploit) within hours, subject to retroactive full-DAO ratification |
| **Retrospective vote** | Post-monitoring window | Full DAO | Confirm, iterate, or roll back based on real impact data |

### 3.2 Voting power design

Pure token-weighted voting is vulnerable to plutocracy and to a compromised/drifting agent that also holds governance tokens. Recommended hybrid:

- **Base layer:** token-weighted or quadratic voting for general proposals.
- **Reputation weighting:** agent-authored proposals carry a visible reputation score (see §6.1 — on-chain agent identity) reflecting that agent's track record of proposals later confirmed by retrospective vote. Low-reputation agents' proposals can still be submitted but are flagged for extra scrutiny.
- **Technical council co-sign:** proposals above a defined blast-radius threshold (§5.3) require sign-off from a designated technical steward group in addition to the token vote, regardless of vote outcome.

### 3.3 On-chain vs. off-chain

Full on-chain voting is transparent and tamper-evident but slow and costly per vote. A common middle ground: off-chain signalling (e.g. Snapshot-style) for scope and proposal votes, with on-chain execution and an immutable audit trail (§6.4) for anything that actually changes production systems or moves treasury funds.

---

## 4. Agent Taxonomy (generic roles)

Every branch specializes these; the roles themselves are constant across branches.

| Role | Function | Never has |
|---|---|---|
| **Recon/Intel** | Gathers external signal (feeds, market data, regulatory changes, user data) | Write access to production |
| **Adversarial/Red-team** | Actively tries to break or find weaknesses in the current system, sandboxed | Unscoped production access |
| **Defensive/Validation** | Tests whether current controls/behavior hold; validates proposed fixes | Authority to self-approve its own validation |
| **Analysis** | Maps exposure, dependencies, blast radius, or attack/opportunity surface | — |
| **Synthesis** | Compiles swarm output into ONE structured proposal (§7) | DAO voting power |
| **Monitoring** | Post-implementation, tracks the metrics the proposal committed to | Implementation authority |
| **Meta-audit** | Watches the other agents; checks outputs against each other; audits agent access/behavior itself | Any operational role — this agent only observes and flags |

---

## 5. Guardrails and Safety

These are non-negotiable across every branch. A branch document may tighten these; it may not loosen them.

1. **No self-approval.** Research/proposal agents and implementation/approval authority are always different agents or different systems, and neither has a DAO vote.
2. **Sandboxed adversarial testing.** Red-team-type agents operate against staging/shadow environments or explicitly scoped, rate-limited production targets — never unscoped live access.
3. **Staged rollout + automatic circuit breakers.** Every implementation canaries first; automatic rollback triggers on defined metric thresholds before full rollout.
4. **Expert sign-off — see DC-EXPERT-DAO-001 for the full spec.** Every proposal in a domain with a designated review body requires sign-off before execution, alongside the standard vote — not gated by a blast-radius threshold, standing on every proposal that domain applies to. A well-staffed coop may self-certify through its own quorum of credentialed members; otherwise the proposal routes to a specialized, domain-scoped review DAO drawn from across the ecosystem. Neither the vote nor the sign-off substitutes for the other.
5. **Sybil/plutocracy resistance.** See §3.2.
6. **Dissent is preserved, not collapsed.** When agents disagree (e.g. differing severity assessments), the proposal surfaces both views rather than presenting a single synthesized voice.
7. **Immutable audit trail.** Every agent action, proposal version, and vote is logged and hash-anchored. Post-incident forensics must not depend on trusting the same system under investigation.

---

## 6. Technology Stack

### 6.1 Identity layer — see DC-AGENT-CREDENTIAL-001 for the full spec
- **Agent-class DID/VC credential**, issued through the existing identity service rather than a separate on-chain registry — the credential carries role, tier, scope (as an enforceable selective-disclosure policy, not a description), and the mandate that authorized the agent's existence.
- **Per-role instruction template** (values, voice, boundaries), versioned and stored alongside the credential's role type — the "who this agent is" layer, kept separate from per-task context.
- **Reputation as an attestation type**, not a separate registry — every outcome-review produces a reputation record queryable against the agent's DID through the same attestation mechanism used for every other trust claim in the system. This is what makes reputation-weighting (§3.2) meaningful instead of arbitrary, without introducing a second trust system alongside the DAO's existing one.

### 6.2 Memory layer — see DC-MESHSTORAGE-ARCHIVE-001 for the full spec
- **Standard storage tier** (erasure-coded, IPFS/Filecoin-compatible) — working state, session context, versioned per-role templates. Ephemeral by nature, superseded over time.
- **Archive tier** (Merkle-anchored, permanent) — final proposals, vote outcomes, execution attestations, and outcome-review findings. This is what lets a meta-audit agent trace a bad proposal back to a specific prior record, and what lets old findings actually inform new proposals, with tamper-evidence that survives even against the system's own operators.
- **Human-facing knowledge base** — proposals render into a wiki space (shared federated protocol, not a separate proprietary app) scoped per governance body, for stakeholder review ahead of a vote.
- If structured graph-style retrieval is wanted beyond content-addressed storage, use a content-addressable-storage-native option rather than a standalone centralized graph database, to stay consistent with the storage model above.

### 6.3 Capability layer
- **Skills** — reusable, versioned playbooks (e.g. "how we structure a proposal for branch X"). This is the DAO's accumulated institutional knowledge of *how things are done here*.
- **Instructions** — narrow, per-invocation system prompts. Keep these lean (see `04-context-engineering-standards.md`); anything reusable belongs in a Skill, not a bloated instruction file.

### 6.4 Control layer
- **Hooks** — deterministic code fired at fixed points in an agent's execution (before/after a tool call, session start/end). This is the actual enforcement mechanism for §5's guardrails: a `PreToolUse` hook that blocks a red-team agent from touching anything outside declared scope, a `PostToolUse` hook that writes every action to the audit log, a hook that blocks any agent from calling vote-execution tools directly.
- In a DID/VC-based implementation, this is realized as **credential-level permission checks** rather than a separate hooks runtime: scope enforcement happens at the identity-service's disclosure check, role-based call authorization happens at the governance-service's call boundary. See DC-AGENT-CREDENTIAL-001 §3 and §5 for the concrete mapping. The principle is identical either way — enforcement is structural, not a instruction the agent is trusted to follow.
- **Guardrail platforms** (e.g. structural/output validation, prompt-injection detection) as an independent second enforcement layer alongside hooks — hooks are yours to maintain and can have bugs; purpose-built guardrail tooling is battle-tested against adversarial input.

### 6.5 Orchestration
- **Inference runs on open-weight models via a decentralized inference layer**, not a closed proprietary API — the orchestration framework calls into this layer for every model invocation. This is a deliberate trade: open-weight models generally trail closed frontier models on complex multi-step reasoning today, which makes the outcome-review/recursion step (§2, step 7) more load-bearing than it would be otherwise, not just a nice-to-have.
- Choose one primary orchestration engine (agent SDK with native hooks/subagents/MCP integration, or a graph-based framework with strong interrupt/resume support for human-in-the-loop gates) — this layer is open source and model-agnostic regardless of which inference backend it calls. See `05-tooling-and-frameworks.md` for the comparison and recommendation.
- **Orchestration pattern:** Coordinator archetype routes work between Producer (research), Critic (proposes, no gate authority), Judge (binary go/no-go), and Consumer (implements) roles. Critics and Judges are never the same agent — mixing them creates deadlock and defeats the no-self-approval rule in §5.1.
- **Mixture of Agents (MoA)** for high-stakes assessments: run the same assessment task across 2–3 independent agents and have an aggregator agent reconcile them into a confidence-weighted output, rather than trusting one agent's unverified take.

---

## 7. Standard Proposal Template

Every branch extends this; no branch removes a field.

```markdown
## Proposal: [title]

### Problem statement + evidence
What was found, by which agent(s), with what confidence, against what data.

### Proposed change
Code diff / config change / architecture change / policy change.

### Migration plan
Steps, rollback plan, blast radius if it goes wrong.

### Testing evidence
What was validated, in what environment, by which agent(s).

### Operational impact
Cost, on-call/ops load, downtime window, affected stakeholders.

### Monitoring plan
Exact metrics that will determine success at the retrospective vote,
including guardrail metrics (things that must NOT get worse).

### Dissenting views
Any agent disagreement on severity, approach, or risk — preserved verbatim,
not resolved into a single voice.

### Reputation context
Proposing agent's track record (from on-chain reputation, §6.1).
```

---

## 8. Cross-Branch Standards

- **Context engineering** for every agent role follows `04-context-engineering-standards.md` — role, scoped retrieval, numbered steps, examples, output schema, tool/guardrail attachment.
- **Evaluation and observability** stack (tracing, LLM-as-judge, regression suites) is shared infrastructure across branches — see `05-tooling-and-frameworks.md`. A proposal caught as bad in production becomes a permanent regression test, regardless of which branch produced it.
- **Ground-truth discipline:** before opening a new branch, define explicitly what "the proposal worked" means and how it will be measured. The further a domain's success metric is from an objective, fast-feedback signal, the tighter the human sign-off threshold should be — not looser.

---

## 9. Document Set

| Document | Covers |
|---|---|
| `00-master-architecture.md` | This document — shared governance, agents, stack, guardrails |
| `01-infrastructure-cybersecurity.md` | Cybersecurity, network, uptime, IT branch |
| `02-features-ux-csat.md` | Product features, UX, customer satisfaction branch |
| `03-business-operations.md` | Finance, compliance, support, growth, people-ops branches |
| `04-context-engineering-standards.md` | Agent context package standard, SOUL.md/instructions templates, memory schema |
| `05-tooling-and-frameworks.md` | Orchestration, evaluation, guardrails, identity, experimentation tooling — choices and rationale |
| `DC-AGENT-CREDENTIAL-001.md` | Full agent-class DID/VC credential spec — schema, permission mapping, reputation, lifecycle |
| `DC-MESHSTORAGE-ARCHIVE-001.md` | Permanent-archive storage tier spec — what's archived, Merkle-anchoring, redaction discipline |
| `DC-DAO-AGENT-LOOP-001.md` | Reconciliation of this document set with the wider D-Central taxonomy's existing primitives |
| `DC-AGENT-OBSERVABILITY-001.md` | Real-time monitoring stack redesigned for decentralized, content-addressed storage |

**Note:** this document set predates the D-Central taxonomy integration. Where this document references identity, memory, or tooling choices, treat DC-AGENT-CREDENTIAL-001, DC-MESHSTORAGE-ARCHIVE-001, and DC-DAO-AGENT-LOOP-001 as authoritative — they reflect the reconciled architecture; this document has been updated in the relevant sections but §7's proposal template and §3-5's governance/guardrail structure remain the source of truth for those pieces.
