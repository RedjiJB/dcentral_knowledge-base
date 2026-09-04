# DC-VERIFIABLE-ROLLOUT-001: Verifiable Progressive Rollout Primitive
### Extends `02-features-ux-csat.md`, DC-DAO-AGENT-LOOP-001, DC-AGENT-CREDENTIAL-001. Resolves the decentralized feature-flag gap flagged in `02-features-ux-csat.md` §4.

---

## 0. Reframing the problem

"Decentralized feature flag" undersells what's actually needed. A flag answers *is this feature on*. What this system needs to answer is: *is this feature on for this identity, according to a policy anyone can verify, and is the rollout currently permitted according to safety conditions nobody can fake?* That's a bigger primitive — call it a **verifiable progressive rollout**, not a flag.

The instinct to put everything on a smart-contract-style registry with raw metrics on-chain is worth resisting. The right split is: governance-controlled *policy*, client-computed *assignment*, and attested *aggregate* measurement — three different trust models for three different jobs, not one big trustless database. Almost all of this already exists in D-Central; only the assignment function is genuinely new.

---

## 1. Four composable parts, mapped onto what already exists

| Part | Job | Where it actually lives |
|---|---|---|
| **Registry** | Feature key, rollout ceiling, salt, guardrail thresholds, version, status | A versioned parameter object inside `dc-governance` — the same pattern already used for every other DAO-controlled setting. Not a new service. |
| **Cohort function** | Deterministic assignment: is this identity in the rollout? | New — the one genuinely new primitive. Small, pure, versioned, formally specified (§2). |
| **Attestation** | Aggregate, signed evidence of what happened — never raw per-user events | `dc-attestation` — exactly the mechanism already used for every other measured outcome in this architecture. Not a new service. |
| **Controller** | Reads attestations, checks guardrails, advances or halts within DAO-set bounds | A scoped agent-class credential (§4) — not a new control-plane system. |

Three of the four parts are just this architecture's existing primitives applied to a new use case. That's the whole point of building it this way instead of importing a standalone decentralized-LaunchDarkly design.

---

## 2. Cohort function

```
bucket = hash(protocol_id || feature_id || experiment_id || rollout_epoch || identity) mod 10000
enabled = bucket < rollout_percentage × 100
```

**Computed client-side.** No assignment server, no central database — anyone can independently recompute a given identity's bucket and verify it against the public registry state. This is what "verifiable by anyone" in the original gap actually requires.

**Domain separation matters.** Hashing on identity alone risks the same user landing in a correlated bucket across unrelated experiments — an observer who knows a user's bucket in experiment A can predict their bucket in experiment B if the inputs overlap. Including `feature_id`, `experiment_id`, and `rollout_epoch` in the hash input prevents that: each experiment gets an independent, unpredictable assignment for the same identity.

**Identity choice is a per-experiment decision, not a fixed default.** A raw DID gives durable, sybil-resistant assignment but ties every experiment to a user's persistent identifier. A session- or installation-scoped derived identifier trades some persistence for less cross-experiment linkability. This architecture already has the identity flexibility to support either — the credential/selective-disclosure layer just needs the experiment to declare which identity class it's assigning against, at proposal time, as part of the experiment design fields already specified in `02-features-ux-csat.md` §3.

---

## 3. Governance model — bounds, not step-by-step votes

A proposal to progressively roll out 10% → 25% → 50% → 100% should not require four separate DAO votes. That would make routine, already-approved changes as slow as novel ones, for no safety benefit.

**The DAO votes once**, approving:
- Maximum rollout ceiling (may be less than 100% — full rollout can still require its own retrospective vote, per `02-features-ux-csat.md` §4's existing rule)
- Minimum observation window per step
- Guardrail thresholds
- Whether automatic halting is authorized

**The controller (§4) executes within those bounds** — stepping the rollout percentage up only after an observation window clears with guardrails intact, and halting automatically (not "recommending a halt") the moment a guardrail breaches. This is the same "gated implementation, staged rollout, automatic circuit breakers" discipline already established in `00-master-architecture.md` §5.3 — this document just specifies the mechanism that actually executes it for this branch.

---

## 4. Rollout-controller agent

A new row in DC-AGENT-CREDENTIAL-001 §3's permission table:

| Role prefix | May call | May NOT call |
|---|---|---|
| `monitor.rollout-controller` | Read `dc-attestation` aggregate metrics for its assigned experiment; call a narrowly scoped `dc-governance` function to advance or halt rollout percentage *within the DAO-approved ceiling* | `proposal-engine`, `voting-engine`, `treasury-manager`; cannot advance past the approved ceiling under any condition; cannot authorize permanent full rollout — that still requires the retrospective vote |

This is the same enforcement discipline used everywhere else in this document set: the controller's authority is a property of its credential, not a promise it's been asked to keep. It can halt unilaterally (safety defaults to the more conservative action), but it cannot expand its own authority past what the DAO already approved.

---

## 5. Metrics — attested, aggregate, never raw

Clients don't stream individual events anywhere. They submit periodic, signed aggregate reports — sample size, success/error counts, latency percentiles for their cohort and window — into `dc-attestation`, using the same aggregation-only discipline already specified for federated rollups in DC-AGENT-OBSERVABILITY-001 §5. A malicious client misreporting its own outcome is a real concern for any self-reported metric; this is mitigated the same way any other attested claim in this architecture is — by requiring enough independent reports to make outlier misreporting statistically visible, not by trusting any single client, and by the reporting client's own DID being attached to the attestation, making a pattern of bad-faith reporting traceable.

---

## 6. Sovereignty check

Nothing here requires an external network. The registry lives in `dc-governance` state (already sovereign). The cohort function runs client-side or on `mesh-ai`-hosted compute (already sovereign, per DC-EXPERT-DAO-001 §6's Bittensor-fork clarification). Attestations live in `dc-attestation`, anchored per DC-MESHSTORAGE-ARCHIVE-001's internal witness-quorum model (per DC-EXPERT-DAO-001 §6's correction, not an external log). No public blockchain requirement beyond what the ecosystem already uses for governance and attestation.

---

## 7. Gap registry status

**New — #35 `DC-VERIFIABLE-ROLLOUT-001`** — specified, this document. Resolves the open gap flagged in `02-features-ux-csat.md` §4 and referenced in `05-tooling-and-frameworks.md` §6. Also adds the `monitor.rollout-controller` role to DC-AGENT-CREDENTIAL-001 §3's permission table.

---

*DC-VERIFIABLE-ROLLOUT-001 — reframes "decentralized feature flags" as a verifiable progressive rollout primitive with three separated trust models: governance-controlled policy (existing dc-governance state), client-computed deterministic assignment (the one genuinely new component, domain-separated to prevent cross-experiment correlation), and attested aggregate measurement (existing dc-attestation, no raw telemetry). Specifies a scoped rollout-controller agent role that executes DAO-approved bounds automatically rather than requiring a vote per rollout step, closing the gap without introducing a new payment rail, identity system, or control plane.*
