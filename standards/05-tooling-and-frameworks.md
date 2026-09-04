# Tooling & Frameworks

**Extends:** `00-master-architecture.md` §6. This document is the decision layer — which specific tools implement each part of the stack, and why. Treat this as the most likely document to go stale; revisit before each major branch launch.

---

## 1. Orchestration engine

| Option | Choose when | Trade-off |
|---|---|---|
| **Claude Agent SDK** | Standardizing on Claude across the system; want native hooks, subagent spawning, and MCP integration with the least scaffolding | Less flexible if you need multi-provider model routing |
| **LangGraph** | Need explicit state graphs, multi-provider flexibility, or strong interrupt/resume for human-in-the-loop gates | More setup overhead; worth it given how much of this system depends on staged approval and sign-off gates — the `interrupt()`-style pattern for pausing mid-graph is a good fit even if the rest of the stack is Claude-native, since you can run Claude models inside the graph |
| **CrewAI** | Prototyping the loop fast, before committing to production infrastructure | Least suited to long-term production hardening |

**Recommendation:** prototype the loop in CrewAI or a simple Claude Agent SDK setup, then migrate to LangGraph (or Claude Agent SDK with a custom interrupt layer) once the human-sign-off gates in the guardrails section become load-bearing rather than theoretical.

**Orchestration pattern regardless of engine:** Coordinator archetype (routes work, doesn't generate or decide), Producer/Critic/Judge/Consumer roles kept structurally distinct — Critics propose with no gate authority, Judges make binary go/no-go decisions, and these are never the same agent instance. Composition rules worth adopting: producers never consume their own output; consumers are idempotent on their work item; critic loops are bounded (a fixed max number of revision rounds before escalation, to prevent infinite refinement loops).

**If open-weight models are a requirement** (e.g., inference must run on infrastructure you control, or a closed-API dependency is unacceptable for the project's sovereignty goals): the orchestration engine choice above is unaffected — LangGraph, CrewAI, and the Claude Agent SDK's structural patterns are all model-agnostic at the framework level. What changes is the inference backend each engine calls: point it at a self-hosted or decentralized-inference open-weight model (Llama-, Mistral-, DeepSeek-, or Qwen-class, whichever your validation process has actually confirmed for quality) instead of a closed frontier API. Be explicit with stakeholders about the trade this makes: open-weight models generally trail closed frontier models on complex multi-step reasoning today, which raises the stakes on the evaluation/outcome-review layer (§2) — it's doing more of the quality-assurance work than it would with a stronger model underneath.

---

## 2. Evaluation & observability

This is the tooling that makes the meta-audit agent role (master doc §4) concrete.

| Platform | Best for |
|---|---|
| **Arize Phoenix** | Open source, OpenTelemetry-native tracing + evaluation; good default if you want to self-host and avoid vendor lock-in |
| **Langfuse** | Open source, strong tracing + prompt versioning + LLM-as-judge |
| **LangSmith** | If already on LangGraph — tightest integration |
| **Galileo / Maxim** | Managed eval-to-guardrail pipelines; useful once you're running at a scale where hand-rolled evaluation doesn't keep up |

**Key capability to prioritize:** evaluation that scores the full reasoning trajectory, not just the final output — an "Agent-as-a-Judge" pattern where a full agentic evaluator critiques another agent's intermediate steps and decision process, not just whether the final answer was right. This is what your meta-audit role actually needs; output-only scoring will miss a red-team agent that reached the right severity score through unsound reasoning.

**Practice, not just tooling:** every proposal that's later found to be wrong (via retrospective vote reversal) should become a permanent regression test case in this system, so the same failure mode is caught automatically next time.

---

## 3. Guardrails (independent second layer, alongside hooks)

- **Guardrails AI** (open source) — structural/type/quality validation on agent outputs before they're accepted downstream.
- **Prompt-injection / data-leakage detection** — real-time scanning particularly relevant for any agent that ingests external/untrusted content (e.g. the Recon agents pulling from public feeds, reviews, or support tickets). Lakera Guard is the commercial reference point here; if the project's tooling needs to stay fully open source, NVIDIA's NeMo Guardrails is the closer-fit open alternative, though it's less purpose-built for this specific threat than Lakera's offering — worth evaluating both against your actual threat model rather than defaulting to whichever is open source if the commercial option is materially stronger.

Run these alongside your own hooks (master doc §6.4), not instead of them — hooks are yours to maintain and can have bugs; purpose-built guardrail tooling is maintained against a much broader adversarial-input dataset than you'll build in-house.

---

## 4. Identity & reputation — see DC-AGENT-CREDENTIAL-001 for the full spec

**Superseded:** an earlier version of this document recommended an ERC-8004-style on-chain identity/reputation registry. Dropped — if your identity layer is already DID/VC-based, introducing a second, Ethereum-specific identity standard duplicates trust infrastructure you already have and violates a "no vertical gets its own trust mechanism" discipline worth holding to generally, not just here.

- **DID-based agent credential** with a bound role/tier/scope, issued through your existing identity service.
- **Reputation as an attestation type**, not a separate registry — every outcome-review produces a queryable reputation record against the agent's DID through the same attestation mechanism used for every other trust claim in the system.
- Practical note unchanged: reputation should accrue to the **agent role/configuration**, not to a single ephemeral session — track record needs to persist across the agent's deployed lifetime to be meaningful. If your stack isn't DID/VC-based, ERC-8004 remains a reasonable fallback pattern — the general principle (portable, queryable, third-party-verifiable track record) matters more than the specific standard.

---

## 5. Prompt optimization

- **DSPy** — treats an agent's instructions as optimizable parameters, tuned against a metric rather than hand-edited. Since this system already produces an outcome signal for every proposal (DAO approved/rejected; retrospective vote confirmed/reversed), that signal can directly drive optimization of each agent role's own instructions over time.
- This is the fastest-moving loop in the whole system — instructions can be re-tuned far more often than the infrastructure/proposal loop completes a full cycle. Treat it as a nested loop: the outer loop (master doc §2) improves the *system*; this inner loop improves each agent's *prompts* against the outer loop's own outcome data.

---

## 6. Feature-flag & experimentation (Features/UX branch specifically)

| Platform | Choose when |
|---|---|
| **Statsig** | Want an all-in-one managed suite — flags, experimentation, analytics, session replay — with built-in statistical rigor (CUPED, sequential/Bayesian methods) |
| **GrowthBook** | Want open-source, warehouse-native experimentation with full data ownership |
| **LaunchDarkly** | Release governance, audit trail, and enterprise compliance certification matter more to your DAO than experimentation depth |

**Recommendation for this system specifically:** GrowthBook over Statsig/LaunchDarkly as the primary pick if self-hosting and full data ownership matter — the DAO's need for transparent, auditable experiment results (feeding the retrospective vote) is served better by an open platform than a closed SaaS one. If audit/compliance requirements later dominate over experimentation depth, LaunchDarkly's governance features become the deciding factor despite being closed.

**If the target infrastructure is fully decentralized** (no centralized service operator at all — every node sovereign), none of the three above actually fit — they all assume a central rollout/assignment service. **Resolved: see DC-VERIFIABLE-ROLLOUT-001** for the decentralized-native replacement, built from client-side deterministic cohort assignment, governance-controlled policy bounds, and attested aggregate metrics rather than a central dashboard.

---

## 7. Starter stack (minimum viable version of this whole document)

If building incrementally rather than all at once, this is the smallest set that makes the master architecture's loop actually function end-to-end:

1. LangGraph or CrewAI, self-hosted, calling `mesh-ai` for inference (orchestration) — prototype first
2. `mesh-storage` standard + archive tiers, per DC-MESHSTORAGE-ARCHIVE-001 (memory)
3. Credential-level permission checks for the no-self-approval and sandboxing rules (master doc §5.1, §5.2, DC-AGENT-CREDENTIAL-001 §3) — build these before anything else, since they're the enforcement layer everything else depends on
4. One evaluation platform (Arize Phoenix, open source, is the lowest-friction start)
5. Attestation-based reputation (DC-AGENT-CREDENTIAL-001 §4) and DSPy-based prompt optimization can come later — they improve a working loop, they aren't required to get one running
