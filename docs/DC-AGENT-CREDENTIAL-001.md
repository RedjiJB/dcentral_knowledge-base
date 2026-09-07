# DC-AGENT-CREDENTIAL-001: Agent-Class DID Credential
### Extends DC-TAXONOMY-001–006 and DC-DAO-AGENT-LOOP-001. Formal spec for gap registry item #24.

---

## 0. What this is

Not a new identity system — a new **credential type** within the existing `dc-identity` service. An agent is a DID like any other principal, issued through `did-registrar`, exactly as a person, a node, or a business gets one. What's specific to agents is the shape of the VC bound to that DID, and what `dc-governance` is willing to let a credential of this type do. This document specifies both.

---

## 1. Issuance

1. A commissioning body (per DC-TAXONOMY-006 §1 — ecosystem `dc-governance`, a coop scoped instance, or an individual DID) issues a research mandate through `proposal-engine`.
2. On mandate approval (or, for individual-tier, on the individual simply funding it — 006 §1.3), `did-registrar` mints a new DID for the agent instance.
3. `vc-issuer` mints the agent-class VC, bound to that DID, with the schema in §2.
4. The agent begins operating under that credential. It presents the VC wherever it calls into any `dcentral-core` service, exactly as a human DID would present a credential to access something scoped to it.

---

## 2. Credential schema

| Field | Type | Purpose |
|---|---|---|
| `subject_did` | DID | The agent's own DID |
| `role` | string, namespaced | e.g. `research.cybersecurity`, `research.ux-hypothesis`, `synthesis.proposal-writer`, `monitor.outcome-review`, `adversarial.red-team`. Determines the permission set in §3. |
| `tier` | enum | `ecosystem` \| `coop` \| `individual` (006 §1) |
| `scope` | selective-disclosure policy | Which modules/verticals/data surfaces this agent may read. Expressed the same way any other selective-disclosure policy is expressed in this architecture — not a prose description, an enforceable policy object the `selective-disclosure-engine` evaluates on every read. |
| `mandate_ref` | proposal ID | The `dc-governance` proposal that authorized this agent's existence |
| `commissioner_did` | DID | Who is paying — a coop treasury sub-account DID or an individual DID (006 §1.4) |
| `issued_at` / `expiry` | timestamp | Standard VC lifecycle bounds |
| `revocation_pointer` | reference | Entry in `revocation-registry` |
| `max_proposal_rate` | integer | Proposal-throttle ceiling for this specific credential, on top of the DAO-level throttle (005 §3.3.4) — lets a commissioner cap their own agent's output rate independent of the network-wide limit |

---

## 3. Permission mapping (role → allowed `dc-governance` calls)

This is the mechanical enforcement of "agents propose, they never execute unilaterally" (005 §3.3.1). It is a property of the credential, checked by `dc-governance` at call time — not a behavior the agent is trusted to self-limit.

| Role prefix | May call | May NOT call |
|---|---|---|
| `research.*` | `proposal-engine` (draft/submit), read APIs across `dc-attestation`, `dc-registry`, public `dc-credit` ledger | `voting-engine`, `treasury-manager` |
| `synthesis.*` | `proposal-engine` (compile/finalize a submission from multiple `research.*` outputs) | `voting-engine`, `treasury-manager` |
| `adversarial.*` | Scoped read/probe access to staging/shadow targets declared in `scope`; `proposal-engine` (draft findings) | Any production write path outside `scope`; `voting-engine`; `treasury-manager` |
| `monitor.*` | Read APIs across all services relevant to `scope`; `proposal-engine` (submit outcome-review findings) | `voting-engine`, `treasury-manager` |
| `monitor.rollout-controller` | Read `dc-attestation` aggregate metrics for its assigned experiment; call a narrowly scoped function to advance or halt rollout percentage *within the DAO-approved ceiling* (DC-VERIFIABLE-ROLLOUT-001 §4) | `proposal-engine`, `voting-engine`, `treasury-manager`; cannot advance past the approved ceiling; cannot authorize permanent full rollout |

No role prefix is ever granted `voting-engine` or `treasury-manager` access. If a future role genuinely needs execution authority (there is no current use case for this), that would be a deliberate, separately-reviewed extension to this table — not a default any credential falls into.

---

## 4. Reputation

Not a separate registry (see DC-DAO-AGENT-LOOP-001 §1's note on why an ERC-8004-style registry was considered and dropped). Every outcome-review of a proposal this agent authored or contributed to (005 §3.1 step 6) produces a **reputation attestation** through `dc-attestation`, referencing `subject_did`. This makes an agent's track record queryable through the exact same mechanism as a contractor's completed-job history (004 §2.4) or a delivery driver's rating — no bespoke trust infrastructure for agents specifically.

Practical consequence: a commissioner deciding whether to fund another mandate for a given agent role/configuration can query that DID's attestation history directly, the same way a task-poster on Lakou Marketplace checks a provider's rating before hiring them.

---

## 5. Scope as enforcement, not description

The `scope` field is not documentation of what an agent is *supposed* to look at — it's the actual policy `selective-disclosure-engine` evaluates. A coop-tier agent commissioned to research a MeshBank corridor's remittance latency has a `scope` that resolves to that corridor's public/attested transaction surface and nothing else; it cannot be prompted or reasoned into reading outside it, because the read call itself fails the disclosure policy check. This closes the gap between "the agent was instructed to stay in scope" and "the agent cannot technically leave scope" — the latter is what this credential type is for.

---

## 6. Lifecycle

```
Mandate approved (dc-governance)
   → DID issued (did-registrar)
   → Agent-class VC minted (vc-issuer), scope/role/tier/mandate_ref bound
   → Agent operates: reads (scope-checked), drafts, submits proposals
   → Mandate concludes or expiry reached
   → VC revoked (revocation-registry) — or renewed if the commissioner
     issues a follow-on mandate (recursion, 005 §3.1 step 6)
   → Reputation attestations from any outcome-review remain queryable
     against subject_did indefinitely, independent of credential validity
```

Revocation is immediate and total: a revoked credential fails every subsequent `selective-disclosure-engine` check, so an agent instance cannot continue operating past mandate end or past a commissioner-initiated early revocation (e.g., a coop deciding to shut down a misbehaving agent mid-mandate).

---

## 7. OSS reference

No new microservice, no new reference tag needed beyond what `dc-identity` already carries (Hyperledger Aries/Indy, Veramo — DC-TAXONOMY-003 §2.1). This is a new VC schema and a new `dc-governance` permission table entry, not new infrastructure.

---

## 8. Gap registry status

**#24 `DC-AGENT-CREDENTIAL-001` — specified, this document.**

---

*DC-AGENT-CREDENTIAL-001 — extends 001–006 and DC-DAO-AGENT-LOOP-001. Specifies the agent-class VC schema (role, tier, scope-as-enforceable-policy, mandate binding, commissioner binding, per-credential proposal throttle), the role-to-permission mapping that makes "agents never execute unilaterally" a mechanical property of dc-governance's call-authorization check rather than a stated rule, reputation as an attestation type rather than a separate registry, and the credential lifecycle from mandate approval through revocation.*


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

*No cross-references detected to/from other docs/*.md files.*

<!-- AUTO-GENERATED RELATED END -->
