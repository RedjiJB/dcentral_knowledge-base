# DC-DAO-AGENT-LOOP-USER-STORIES-001: End-to-End User Stories
### Extends DC-DAO-AGENT-LOOP-001, DC-AGENT-CREDENTIAL-001, DC-MESHSTORAGE-ARCHIVE-001, DC-AGENT-OBSERVABILITY-001. Follows the user-story format already established in DC-TAXONOMY-004.

Six stories, chosen to each walk the full loop end to end while covering a different tier, branch, and persona — so together they exercise every mechanism in the four documents above at least once, not just the happy path.

---

## Story 1 — The Coop Steward (infrastructure branch, coop tier)

**As** a technical steward for a coop running several SHI nodes, **I want** repeated service outages investigated and fixed, **so that** members stop losing connectivity during peak hours.

Amara has fielded the same complaint three times this month. She opens `dc-governance` and submits a scope-vote proposal: *"Investigate and remediate recurring mesh-connectivity outages, coop node cluster #4."* The coop's members approve it in the standard cycle.

On approval, `did-registrar` mints a DID for a new agent instance; `vc-issuer` binds an agent-class VC with `role: research.infrastructure`, `tier: coop`, `scope` resolved to cluster #4's public/attested telemetry, and `mandate_ref` pointing back to Amara's proposal. The agent begins reading — its own module's repo, `dc-attestation`'s public record for this cluster's prior incidents, `dc-registry`'s capability index for what's actually deployed there. A second, independently-scoped agent (`role: adversarial.red-team`) spins up in parallel to attempt reproduction against a shadow copy of the cluster.

Both agents' inference calls run against the mesh's open-weight model layer, metered and paid in D-Credit from the coop's treasury sub-account — visible to Amara in real time as a line item, not a mystery bill. Findings from both agents are compiled by a `role: synthesis.proposal-writer` credential into a single proposal, rendered into the coop's MeshWiki space: root cause, a config fix, a migration plan, the red-team agent's confirmation that the fix holds under a second attempt, and a monitoring plan.

The proposal goes to a standard vote. It's below the blast-radius threshold, so no additional technical sign-off is required. It passes. Implementation is staged — canary to one node in the cluster, automatic rollback wired to error-rate and latency thresholds, full rollout after 48 hours clean. A `role: monitor.outcome-review` agent watches the metrics and, after the monitoring window, submits its findings: outage rate down, no regressions. This becomes an outcome-review attestation, referencing both research agents' DIDs — their first entries in a track record anyone can query later.

**Touches:** DC-AGENT-CREDENTIAL-001 (issuance, scope, role separation), DC-DAO-AGENT-LOOP-001 §1–2, `01-infrastructure-cybersecurity.md` §2–4, DC-MESHSTORAGE-ARCHIVE-001 (outcome-review lands in archive tier).

---

## Story 2 — The Individual Commissioner (features/UX branch, individual tier)

**As** a small MeshShop vendor watching checkout abandonment climb, **I want** to know why buyers drop off before paying, **so that** I stop losing sales I can't currently explain.

Julien doesn't run a coop — he's one vendor. Under the individual-tier path (006 §1.3), he funds a mandate directly from his own DID rather than a coop treasury, submitted through the same `proposal-engine` any coop would use. A `role: research.ux-hypothesis` agent is commissioned, scoped — via selective disclosure — to Julien's own shop's checkout funnel data and whatever anonymized cross-shop benchmark data MeshShop already publishes. It cannot see other vendors' unpublished data; the scope field enforces that structurally, not by request.

The agent clusters drop-off points against session data, drafts a falsifiable hypothesis ("simplifying the shipping-method step reduces abandonment by at least 4%"), and defines guardrail metrics alongside the target metric — page-load time and support-ticket volume must not get worse. Because no off-the-shelf decentralized feature-flag service exists yet (flagged as an open gap in `02-features-ux-csat.md`), the experiment cohort is assigned by hashing buyer DIDs deterministically — verifiable, no central assignment service needed.

The proposal still goes through the same vote any human member's would — in this case, MeshShop's own governance body, since the change touches shared checkout infrastructure, not just Julien's storefront. It passes for a scoped experiment, not a permanent change. Results come back after the flagged rollout window: target metric moved, guardrails held. Retrospective vote confirms full rollout.

**Touches:** DC-TAXONOMY-006 §1.3 (individual tier), `02-features-ux-csat.md` §2–5, DC-AGENT-CREDENTIAL-001 §5 (scope as enforcement).

---

## Story 3 — The Auditor (transparency, any tier, public access)

**As** a researcher with no formal role in D-Central, **I want** to verify a specific past governance decision wasn't altered after the fact, **so that** I can cite it in my own published analysis with confidence.

Priya read a claim that a treasury-rebalancing proposal from four months ago was approved under contested circumstances. She doesn't need permission to check — she opens the relevant coop's MeshWiki space, finds the rendered proposal, and follows the drill-down to its underlying attestation record.

The record shows the batch it was anchored in and the Merkle root committed at the time. Priya independently fetches that same root from the transparency log D-Central publishes to outside its own infrastructure — a source no D-Central operator controls — and confirms the two match. The proposal record is exactly what was attested at the time; nothing was quietly edited afterward. Fields that reference anything short of fully public data are hashed rather than shown raw, but the fact and integrity of the record itself is fully verifiable without asking anyone's permission or trusting anyone's word.

**Touches:** DC-MESHSTORAGE-ARCHIVE-001 §2–3 (batching, anchoring, independent log, redaction discipline), DC-DAO-AGENT-LOOP-001 §5.

---

## Story 4 — The Dissenting Agents (safety mechanism, ecosystem tier)

**As** an ecosystem-tier governance participant, **I want** to see when the system's own agents disagree, **so that** I'm not handed a false sense of consensus on a high-stakes call.

An ecosystem-wide mandate asks for a severity assessment on a vulnerability class affecting multiple mesh modules at once. Three independently-scoped `role: research.cybersecurity` agents are commissioned against the same mandate — a mixture-of-agents assignment, not a single point of failure. Two assess it as high-severity, actively exploitable. One assesses it as moderate, citing a mitigating control the other two didn't weight as heavily.

The `synthesis` agent does not average this into one confident number. All three findings are submitted as separate attestations under the same `mandate_ref`, and the rendered proposal in MeshWiki shows the disagreement explicitly — majority view, minority view, and the specific evidence each cited. The governance body reads both, asks a technical steward to weigh in given the split, and votes to treat it as high-severity pending the steward's confirmation.

Nothing here is a failure. The system worked exactly as intended — one drifting or under-informed agent didn't get to unilaterally set the DAO's risk posture, because dissent was structurally preserved rather than smoothed over by a single synthesized voice.

**Touches:** `00-master-architecture.md` §6.5 (mixture of agents), `00-master-architecture.md` §5.6 (dissent preserved), `01-infrastructure-cybersecurity.md` §4.

---

## Story 5 — The Failed Experiment (recursive correction, coop tier)

**As** a coop member who voted for a UX change, **I want** to know if it turns out to have actually hurt something, **so that** the system corrects course instead of quietly living with a bad outcome.

A proposal to streamline MeshSocial's post-composer passed vote and shipped behind a flagged rollout. Three days in, a guardrail metric — accessibility-tool compatibility — breaches its threshold. The kill-switch fires automatically; the change reverts to the flagged cohort without waiting for a vote, because that's what the guardrail-metric threshold is for.

A `role: monitor.outcome-review` agent submits its findings honestly: target metric did move in the intended direction, but the guardrail breach means the change doesn't ship as proposed. The retrospective vote reads both facts plainly, and the coop votes to send it back for revision rather than force it through. The proposing agent's reputation attestation reflects this outcome accurately — not a black mark for trying, but an honest record that this specific proposal needed a second pass, visible to anyone checking that agent's track record before commissioning it again.

**Touches:** `02-features-ux-csat.md` §4 (kill-switch, retrospective vote), DC-AGENT-CREDENTIAL-001 §4 (reputation reflects real outcomes, not just successes).

---

## Story 6 — The Node Operator (observability, cross-tier)

**As** someone hosting an SHI node that runs coop agent workloads, **I want** to see what's happening on my own node without needing anyone's permission or a central dashboard, **so that** I can catch a misbehaving agent before it becomes everyone else's problem.

Devon's node runs a local OTel Collector alongside the agent workloads it hosts, sampling based on the bandwidth budget Devon has actually allocated — not a billing decision, a resource one. A self-hosted index mirrors the local telemetry for fast querying, and Devon's coop has its own live topology view scoped to just its own agents — Devon can see call graphs, catch a stuck or looping agent, and get alerted automatically if one starts burning D-Credit at an abnormal rate, all without querying anyone else's data or waiting on a central operator.

Only aggregated statistics — agent counts, error rates, proposal throughput — roll up to the ecosystem-wide governance dashboard. Raw span data from Devon's node never leaves it. When Devon checks cost, there's no separate cost dashboard to reconcile against a bill — it's a direct query against the same payment ledger already recording every inference call, already attested, already the source of truth.

**Touches:** DC-AGENT-OBSERVABILITY-001 §2–7 in full — this story is effectively that document's spec walked through from one operator's chair.

**Extension — capacity-contributor vs. pure-consumer roles:** Devon is what DC-COMPUTE-SILICON-ARCH-001 §6 calls a
"Consumer B" — someone whose node carries actual compute hardware (GPU/FPGA/ASIC per that document's Silicon Class
axis) and earns compensation for contributed capacity, distinct from a "Consumer A" who only uses the thin-client
architecture (DC-NETWORKING-ARCH-RECONCILED-001 §10-17) without hosting anything. This story was already written
from Consumer B's chair; the distinction is named explicitly there because nothing before it separated the two
roles.

---

*DC-DAO-AGENT-LOOP-USER-STORIES-001 — six end-to-end walkthroughs exercising every tier (ecosystem, coop, individual), all three branches represented in the earlier document set (infrastructure, features, and the safety/correction mechanisms that apply across all of them), and all four newer specs (credential, archive storage, observability) at least once each. Stories 4 and 5 are deliberately not happy paths — dissent and rollback working as designed are as much a part of "end to end" as a clean success.*


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

**Referenced by:**
- [[DC-COMPUTE-SILICON-ARCH-001|DC-COMPUTE-SILICON-ARCH-001 — Compute Silicon Class Architecture (v1, generated 2026-09-07)]]

<!-- AUTO-GENERATED RELATED END -->
