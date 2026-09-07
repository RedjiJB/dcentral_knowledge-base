# DC-DAO-AGENT-LOOP-001: Recursive DAO-Agent Governance — Implementation Spec
### Extends DC-TAXONOMY-001–006. Fulfills gap registry items #24 (DC-AGENT-CREDENTIAL-001) and #25 (DC-DAO-AGENT-LOOP-001).

---

## 0. What this document adds

DC-TAXONOMY-005 §3 and DC-TAXONOMY-006 §1–3 already specify the loop's *governance shape*: mandate → agent research → proposal → human/staked vote → execution + attestation → recursive outcome-review, three commissioning tiers (ecosystem/coop/individual), a proposal-bounty compensation mechanism, and federated method-learning across tiers. That layer doesn't need re-deriving here.

What's been missing is the **implementation layer** underneath it: how an agent's context is actually assembled run to run, how "agents propose, they never execute unilaterally" (005 §3.3.1) becomes a mechanical enforcement rather than a stated rule, and how the attestation trail becomes genuinely publicly auditable rather than a conceptual promise. This document specifies that layer — built entirely from existing `dcentral-core` primitives, per DC-TAXONOMY-001 §0's own discipline: no new identity system, payment rail, storage layer, or trust mechanism.

It also resolves three open questions raised directly: PII/private-data gating (already solved, see §3), open-source model requirement (see §3), and IPFS-style storage (see §3, and it closes an open gap from DC-TAXONOMY-002 §4 in the process).

---

## 1. Agent-class credential (DC-AGENT-CREDENTIAL-001)

An agent is a DID like any other principal, issued through `dc-identity`'s `did-registrar` — no separate agent-identity system.

**Agent-class VC** (issued by `vc-issuer`), carrying:

| Field | Purpose |
|---|---|
| `role` | e.g. `research.cybersecurity`, `research.ux-hypothesis`, `synthesis.proposal-writer`, `monitor.outcome-review` — determines which `dc-governance` calls this credential is authorized to make (see §4) |
| `tier` | `ecosystem` \| `coop` \| `individual`, per DC-TAXONOMY-006 §1 |
| `scope` | which modules/verticals/mandate this agent is bound to — expressed as a selective-disclosure policy (see §3) |
| `mandate_ref` | the `dc-governance` proposal ID that spawned this agent (the research mandate itself) |
| `commissioner_did` | who's paying — coop treasury sub-account or individual DID, per 006 §1.4 |
| `expiry` / `revocation` | standard VC lifecycle, via `revocation-registry` |

**Reputation is not a separate registry.** Earlier in this conversation, before I had this context, I suggested an ERC-8004-style on-chain identity/reputation registry for agents. Drop that — it's a second trust mechanism duplicating what `dc-attestation` already does. Instead: every outcome-review (005 §3.1 step 6) issues a **reputation attestation** referencing the agent's DID, through the same `dc-attestation` envelope every other claim in this architecture uses. Anyone can query an agent's track record the same way they'd check a contractor's completed-job attestations (004 §2.4) — same mechanism, same disclosure rules, no parallel system.

**Role separation is enforced at the credential level, not the prompt level.** A `research.*` role credential is simply not authorized to call `voting-engine` or `treasury-manager` — this is `dc-governance`'s existing permission model, applied to an agent-class DID exactly as it would be to a human DID with limited standing. "Agents propose, they never execute unilaterally" becomes a permission the credential does not have, not an instruction the agent is trusted to follow.

---

## 2. Agent context package (extends 006 §2)

006 §2 already names the five context sources an agent should read (own repo, module/vertical specs, public ledger history, `dc-attestation` public record, `dc-registry` capability index) and states the privacy boundary (scoped to what's already publicly disclosed). What it doesn't yet specify is the shape of what an agent is handed at invocation time. Six components, mapped onto what already exists:

1. **Role** — the agent-class VC's `role` + `scope` fields *are* the role definition. No separate identity artifact needed; a per-role instruction template (versioned, stored per §3 below) supplies voice/tone/rigor bar, referenced by the credential's `role` value.
2. **Scoped context** — exactly 006 §2's five sources, already correctly bounded by the public/attested disclosure line. This is a more complete answer than the Neo4j-based retrieval I proposed earlier in this conversation, which duplicated a scoping mechanism you'd already solved.
3. **Numbered steps** — per-role task templates (retrieve → analyze → cross-reference against `dc-attestation`'s public record for prior art → draft → self-validate → submit in the standard schema). Stored per §3.
4. **Examples** — 2–3 worked past proposals per role (one that passed vote and held up under outcome-review, one that didn't), pulled directly from `dc-attestation`'s own public record — you don't need to curate a separate example set, the attestation trail already contains it.
5. **Output schema** — the standard `dc-governance` proposal schema (already defined by `proposal-engine`), with the bounty reference (006 §1.4) and `mandate_ref` attached.
6. **Tools/guardrails** — scoped by the agent-class VC (§1) plus the enforcement layer in §4.

---

## 3. Resolving the three stated constraints

### PII / private data gated behind DIDs and VCs

This needs no new mechanism. It's precisely `dc-identity`'s `selective-disclosure-engine`, already the operative privacy boundary for every vertical in this taxonomy (006 §2's own framing: agent research context is scoped to what a service *already publishes*). The one addition specific to agents: an agent-class VC's `scope` field should itself be expressed as a selective-disclosure policy, so a coop-tier agent researching a MeshBank corridor is cryptographically restricted to that corridor's public/attested surface — not merely instructed to stay in scope, the way a prompt-level instruction would be.

### Open-source models

`mesh-ai` (Bittensor-fork, validator-consensus miners) is already the inference layer — agents should run against `mesh-ai` subnets through the `dc.ai` XaaS namespace (001 §4.3), not a proprietary API. The orchestration framework sitting on top (LangGraph or equivalent) doesn't need to change — it's already open source and model-agnostic; only the inference backend moves, from a closed frontier API to whichever open-weight models `mesh-ai`'s validator set has actually verified for quality (Llama-, Mistral-, DeepSeek-, or Qwen-class, depending on what the subnet currently runs).

Worth stating plainly rather than glossing over: open-weight models generally trail closed frontier models on complex multi-step reasoning as of today. That's a real trade against sovereignty, not a free swap. Practical consequence: proposal-bounty sizing (006 §1.4) may need tuning with that quality ceiling in mind, and outcome-review (005 §3.1 step 6) carries more weight as the actual check on proposal quality than it would with a stronger model — the recursive review step isn't optional polish here, it's load-bearing.

### IPFS-style storage

`mesh-storage` already lists IPFS/Filecoin as an OSS reference (003 §2.2), and 002 §4 flagged an open decision point: `mesh-storage` as specified is Storj-style erasure-coded/repairable, not permanent-archive, and Arweave's permanent model isn't explicitly covered. The agent audit trail this document specifies is the concrete workload that gap exists for — worth resolving it now rather than leaving it open:

- **Per-role templates, versioned specs** → standard `mesh-storage`, erasure-coded — these get superseded over time, they don't need permanence.
- **Attestation trail** (proposal, execution, outcome-review records) → this is the permanent-archive case. Batch attestation records into a Merkle tree, anchor the root into the existing `dc-attestation` envelope, commit the root to an Arweave-or-equivalent permanent layer on a fixed schedule. Scope this as `mesh-storage: archive tier` — a **mode** of the existing module, not a new one, consistent with how `mesh-vpn` was scoped as a mode of `mesh-connectivity` rather than a ninth module (003 §4.4). This directly resolves the 002 §4 open decision point.
- **Human-readable proposal review** → drop Obsidian, which I suggested earlier without this context. **MeshWiki already exists for exactly this** (collaborative reference docs, `revision-history-engine`), and every member already has one DID across every vertical rather than a second login. Proposals render into a MeshWiki space scoped per governance body — ecosystem-wide space, or a coop's own scoped instance.
- **If a queryable graph layer is still wanted** on top of the content-addressed store (for the kind of structured retrieval Neo4j would have given), an IPFS-native option (e.g. OrbitDB) keeps it consistent with the IPFS-like mandate instead of introducing a centralized graph database as a new dependency.

---

## 4. Guardrail enforcement (extends 005 §3.3, 006 §1.4)

The guardrails this conversation worked out earlier (no self-approval, sandboxed adversarial testing, staged rollout, human sign-off above a blast-radius threshold, dissent preserved not collapsed, immutable audit trail) map onto existing mechanisms rather than a separate "hooks" control plane:

| Guardrail | Mechanism |
|---|---|
| No self-approval | Credential `role` permission boundary (§1) — a `research.*` or `synthesis.*` credential structurally cannot call `voting-engine` or `treasury-manager` |
| Sandboxed adversarial testing | Scope field (§1) restricts a red-team-role agent's `dc-registry`-discoverable targets to explicitly declared staging/shadow nodes |
| Staged rollout + rollback | `treasury-manager`'s existing milestone-release pattern (already used for MeshBuild's multi-stage escrow, 005 §1.3) — release funds/deploy in stages gated on attestation, not all at once |
| Expert sign-off (mandatory per domain, not threshold-gated) | Internal expert quorum (coop self-certification) or specialized review DAO (routed by domain) — see DC-EXPERT-DAO-001 |
| Dissent preserved | Multiple agents assigned to the same mandate (mixture-of-agents pattern) submit independent findings as separate attestations under the same `mandate_ref`, rather than one synthesis agent collapsing disagreement before it's visible |
| Immutable audit trail | `dc-attestation`, extended with the permanent-archive tier in §3 |
| Proposal-spam throttle | Already specified — `dc-governance`-set rate limit on agent-originated proposals (005 §3.3.4) |

---

## 5. Public audit / transparency (extends `dc-attestation`)

The "public audit portal" concept from earlier in this conversation is not a new system — it's the public-facing view of `dc-attestation`'s own record, rendered through MeshWiki (§3) for human readability, with drill-down to the raw attested record for anyone who wants it. The redaction/commitment pattern (publish a hash, keep sensitive raw data access-controlled) is exactly what `selective-disclosure-engine` + `zk-proof-service` already do for every other claim type in this architecture — an agent's research process gets the same treatment as an inventory count or an income-for-lending proof, not a bespoke privacy mechanism.

One honest caveat carried over from earlier in this conversation: whichever model runs on `mesh-ai`, its full internal reasoning trace may not be recoverable at the raw token level depending on the model's own output behavior — what's captured and attested is the model's tool calls, its structured decision output (§2), and whatever reasoning output the model does surface. Worth confirming this against whichever specific open-weight model `mesh-ai`'s subnet actually runs, rather than assuming full raw chain-of-thought will always be available.

---

## 6. What to discard from earlier in this conversation, now that this context exists

Stated plainly, since silently dropping these without comment would be worse than flagging them:

- **ERC-8004 / on-chain identity registry** — drop. `dc-identity` (W3C DID/VC) already covers this; a second identity standard duplicates trust infrastructure the taxonomy explicitly rules out.
- **Neo4j** — drop as specified (a standalone proprietary-leaning graph database dependency); if graph-structured retrieval is still wanted, use an IPFS-native option instead (§3).
- **Obsidian** — drop; MeshWiki already fills this role natively.
- **Statsig / LaunchDarkly** (commercial feature-flag SaaS, from the features/UX branch discussion) — reconsider against GrowthBook specifically, which was already the more open-source-aligned recommendation in that earlier comparison, given the open-source mandate now stated explicitly.
- **Claude Agent SDK / closed-model inference** — the orchestration layer can stay (framework choice is separate from model choice); inference moves to `mesh-ai` per §3.

---

## 7. Gap registry — status update

- **#24 `DC-AGENT-CREDENTIAL-001`** — specified, §1.
- **#25 `DC-DAO-AGENT-LOOP-001`** — implementation layer specified, §2–5; governance shape remains as already specified in 005 §3.
- **New — #32 `DC-MESHSTORAGE-ARCHIVE-001`** — permanent-archive tier of `mesh-storage` (Merkle-batched, Arweave-anchored attestation trail), resolving the open decision point flagged in 002 §4.

---

*DC-DAO-AGENT-LOOP-001 — extends 001–006. Specifies the agent-class credential (DID + role/tier/scope/mandate-bound VC, reputation as an attestation type rather than a separate registry), the agent context package (role, scoped context, numbered steps, examples, output schema, tools — mapped onto 006 §2's existing context sources), and guardrail enforcement as credential-level permissions and existing dc-governance/dc-attestation mechanisms rather than a separate control plane. Resolves the DID/VC-native PII boundary (already solved by selective-disclosure-engine), the open-source model requirement (mesh-ai/dc.ai in place of proprietary inference, with an explicit note on the resulting quality trade-off), and the IPFS-like storage requirement (mesh-storage archive tier for the attestation trail, MeshWiki for human-readable proposal review) — closing the Arweave/permanent-archive gap left open in 002 §4. Flags five recommendations from earlier discussion (ERC-8004, Neo4j, Obsidian, Statsig/LaunchDarkly, closed-model inference) for removal or substitution now that the existing dcentral-core/mesh-ai/mesh-storage primitives are in view.*


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

*No cross-references detected to/from other docs/*.md files.*

<!-- AUTO-GENERATED RELATED END -->
