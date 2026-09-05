---
source_conversation_uuid: 2c6eb4aa-23e4-4e3e-be53-46332d55b214
conversation_title: 'Coworker sessions context'
created_at: 2026-08-16T15:10:28.960082Z
doc_id: DC-AGENT-001
description: 'Formal agent architecture, memory, and orchestration registry document consolidating task/knowledge management and agent tooling decisions'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-AGENT-001 — Agent Architecture, Memory & Orchestration
*Formalizes the task/knowledge/memory layering discussion and the agent orchestration brainstorm into one registry document.*

## 1. Three-Layer Split (the core architectural decision)
Conflating these is what makes agent systems messy. Keep them separate:

| Layer | Tool | Scope |
|---|---|---|
| Task/work management | GitHub Projects (not Jira) | Dev work on the system itself — features, bugs, crew-reported issues. NOT day-to-day crew ops, which the WhatsApp bot already handles. |
| Knowledge base | Obsidian vault, git-backed | Source of truth: architecture docs, SOPs, vendor contacts, runbooks, DC-FOS registry docs |
| Agent runtime memory | pgvector RAG over the vault | What the agent retrieves at query time — vendor lookup, SOP retrieval, process questions |

**Obsidian vault structure:** folder by function (`architecture/`, `runbooks/`, `vendors/`, `incidents/`), not by date — both agents and humans retrieve better from stable, typed structure.

## 2. RAG vs GraphRAG — the decision rule
- **Plain vector RAG (pgvector)** covers ~90% of what the FieldOps crew agent needs. Already have Postgres on the Pi/server — no new service required.
- **GraphRAG** earns its complexity only where relationships matter more than lookup — e.g., D-Central's registry where DC-SKY-001 depends on DC-NETINFRA-001 depends on the Lakou Protocol. **Scope GraphRAG to the D-Central registry itself, not the crew-facing bot.**
- Crew agent retrieval stays **scoped and read-only** from a defined subset of the vault — this is also the leak-prevention boundary from the security audit (see DC-FOS-SECURITY-AND-DESIGN-RESEARCH).

## 3. Operational Management of the Agent Stack
- `SYSTEM-STATUS.md` in the vault, updated by a cron job — last backup, last deploy, agent uptime
- Incident notes as dated Obsidian entries, linked back to the relevant runbook — becomes the postmortem trail
- Every prompt/config change dated and reasoned in git, mirrored to an Obsidian changelog

## 4. Agent Roles & Identity (DC-AGENT-001 core)
- Formal agent roles, permissions, and DID identities, named the same way mesh nodes are
- **Capability tiers**: what an agent can do at trust level 1 vs. 3, tied to DAO reputation where applicable
- Crew-facing vs. admin-facing split is now standard practice, not a one-off fix (from the security audit) — generalize the non-disclosure rules into a reusable **agent constitution template** for every future deployment
- Version and hash agent prompts/configs alongside DC-STATUS-001 — agent capability claims get the same designed-vs-executed honesty audit as everything else in D-Central

## 5. Orchestration Tooling
| Tool | Role |
|---|---|
| n8n | Connective tissue — node-based canvas wired into OpenClaw webhooks, light enough for the Pi/server |
| Langflow / Flowise | Prototyping sandbox for new agent chains, kept out of production |
| CrewAI (open-source) | Role-based squads — dispatcher, inventory-checker, exception-escalator agents |
| LangGraph | Stateful multi-turn loops — e.g., tracking an order discrepancy across several messages |
| AutoGen-style pattern | Admin/diagnostic agent conversing with a monitoring agent before escalating to a human |

**Explicitly out of scope as runtime infrastructure:** Copilot Studio, CrewAI Enterprise, watsonx Orchestrate — centralized SaaS control planes that cut against D-Central's sovereignty premise. Useful as reference architecture, not to be adopted as infrastructure.

## 6. Network/Security Architecture for Agents
- Agent topology mesh-aligned with the DC-ISP three-tier model — edge agent, regional coordinator, hub reasoning layer
- Hard network segmentation — crew agent and admin agent on separate Docker networks, not just separated by prompt
- Circuit breaker pattern between OpenClaw and downstream APIs
- Rate-limiting on crew-facing agent calls to cap runaway cost from message loops
- Health-check dashboard on the admin route only, never public
- MCP as the standard interface between D-Central services and any agent — one integration surface instead of bespoke wiring per tool

## 7. Eval & Research Discipline
- FieldOps-specific eval harness: real crew messages, expected actions, pass/fail scoring
- Weekly human-scored transcript sample against a rubric (helpfulness, hallucination, leak risk)
- Every RAG answer traces to a source doc + version
- Monthly benchmark reruns to catch silent accuracy drift as the vault grows
- Confidence scores on RAG answers, auto-escalating low-confidence replies to a human

## 8. D-Central Integration
- Extend Lakou Protocol DAO governance to agent permissions — capability grants voted the same way treasury actions are
- Position Sod Boys FieldOps as the reference implementation for DC-FOS-001, feeding real operational data back into the formal spec
- Agent hosting/orchestration as a Lakou-funded cooperative service eventually, not something each node buys separately
- Sovereignty tiering — which agent functions must stay Haiti/cooperative-hosted vs. which can safely use external APIs

## 9. Timeline
| Phase | Action |
|---|---|
| Now | git-backed Obsidian vault + pgvector RAG, GitHub Projects — zero new infra |
| Now | DC-AGENT-001 (this document) as a one-page anchor against scope drift |
| This semester | Prototype one CrewAI crew (dispatcher + escalator), scored against the eval harness |
| This semester | Docker network segmentation folded into CST8315 VLAN lab overlap |
| Winter term | Langflow/Flowise sandbox; first DC-STATUS-style audit of the agent stack specifically |
| Spring | GraphRAG pilot scoped to the D-Central registry corpus only; DID-based agent identity |
| Through early 2027 | Federated agent network stays design-only — matches the DC-SIM stop-condition discipline |
| At DC-OS Pi 5 boot milestone | Agent orchestration graduates to a first-class DC-OS service |
| Long-term | Agent hosting becomes a literal DC-ISP revenue/mutual-aid line |

## 10. Explicitly Deferred (design-only, not build-now)
Zero-knowledge proofs for location/hours, agent-to-agent negotiation for the fractal DAO layer, cryptographic action attribution via DID/VC, graph-of-thought reasoning for D-Central queries, live IoT/sensor fusion — all real, all noted, none competing for time against the DC-SIM stop condition.
