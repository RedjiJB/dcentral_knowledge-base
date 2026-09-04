# Branch: Business Operations

**Extends:** `00-master-architecture.md` — read that first. This document only covers what's specific to this branch.

This branch is actually five sub-branches with very different ground-truth quality. Open them in the order below — not because the later ones are less valuable, but because the loop's monitoring/retrospective stage only works if there's a real signal to monitor, and that signal gets progressively fuzzier and slower down this list.

---

## Recommended sequencing

| Order | Sub-branch | Ground truth | Blast radius type | Sign-off posture |
|---|---|---|---|---|
| 1 | Compliance/Legal | Objective, external (a regulation applies or it doesn't) | Legal/regulatory exposure | Standard threshold, similar rigor to infra branch |
| 2 | Finance/Treasury | Clean but high-stakes (P&L, runway are measurable) | Financial, often irreversible | Tightest — multisig + technical council mandatory above a low dollar threshold |
| 3 | Customer Support Ops | Measurable, moderate lag (resolution time, CSAT) | Operational | Standard threshold |
| 4 | Product/Growth | Contestable, slow feedback (weeks/months) | Strategic/reputational | Tighter than infra — see §4 |
| 5 | People/HR Ops | Slow, high human stakes, easy to get wrong | Affects people's jobs/livelihoods | Advisory-only for an extended period — see §5 |

---

## 1. Compliance / Legal Operations

**Scope examples:** "Monitor regulatory changes affecting [jurisdiction/product area]." "Review contracts against our standard playbook."

**Agent roles:** Recon agent (regulatory feed monitoring), Analysis agent (contract review against playbook), Synthesis, Monitoring (tracks compliance-gap closure rate).

**Proposal template extension:**
```markdown
### Regulatory basis
Specific regulation/clause, jurisdiction, effective date, source citation.

### Current exposure
What in our current operations conflicts, and since when.

### Remediation
Policy/contract/process change required, with legal review sign-off requirement flagged.
```

**Guardrail specific to this sub-branch:** no agent-drafted legal or compliance change goes live without a licensed human reviewer's sign-off — this is a hard floor, not a threshold, given the professional/regulatory liability involved.

**Integration note:** the permit/inspection attestation pattern already established elsewhere in this architecture (a municipal inspector issuing a pass/fail attestation directly into a project's trail) generalizes cleanly here — a regulator or licensing body can become an attestation issuer for compliance findings without adopting the whole governance stack, the same extension point already used for licensed-trade work.

---

## 2. Finance / Treasury Operations

**Scope examples:** "Monitor treasury composition and runway." "Research yield/rebalancing opportunities within [risk band]."

**Agent roles:** Recon agent (market/yield monitoring), Analysis agent (risk modeling), Synthesis, Monitoring (tracks realized vs. proposed outcome).

**Proposal template extension:**
```markdown
### Current position
Treasury composition, runway, relevant exposure.

### Proposed action
Specific trade/allocation change, with worst-case scenario explicitly modeled.

### Reversibility
Can this be unwound, at what cost, within what timeframe.
```

**Guardrail specific to this sub-branch:** this is the highest-consequence sub-branch in the entire system — a bad autonomous financial action is often unrecoverable in a way a bad patch or a bad UX experiment is not.
- Mandatory multi-party governance co-sign above a DAO-defined threshold, no exceptions for vote outcome — the treasury service's existing staged/milestone release pattern (already used for multi-stage escrow elsewhere in this architecture) is the natural mechanism, not a new approval system.
- Reputation weighting (per DC-AGENT-CREDENTIAL-001 §4 — an agent's attested track record) should carry the most weight here of any sub-branch — an agent's proposal-accuracy history is the closest thing to due diligence available before real capital moves.
- No emergency fast-track path for this sub-branch by default. Speed is rarely the right trade-off against capital risk; if one is added, its threshold should be materially stricter than the infrastructure branch's.

---

## 3. Customer Support Operations

**Scope examples:** "Reduce resolution time for [ticket category]." "Improve support tooling for [issue type]."

**Agent roles:** Analysis agent (ticket pattern clustering), Synthesis, Monitoring (resolution time, CSAT, ticket volume).

**Proposal template extension:** same shape as the Features/UX branch's hypothesis + guardrail-metric format (`02-features-ux-csat.md` §3) — support-ops changes are effectively small UX experiments and should be treated with the same rigor, including the Goodhart guardrails in that document's §5.

---

## 4. Product / Growth

**Scope examples:** "Research roadmap opportunities in [area]." "Propose growth experiments for [channel]."

**Ground truth caution:** this is where I'd be most careful. Success here is contestable and feedback loops run weeks to months, which means an agent swarm can easily optimize a proxy metric nobody actually wanted moved, and nobody will notice for a long time.

**Mitigations required before opening this sub-branch:**
- Define the actual success metric and its measurement window explicitly at scope-vote time, not left implicit.
- Require the Mixture-of-Agents pattern (master doc §6.5) on every roadmap/strategy proposal — no single-agent strategic recommendations.
- Retrospective vote window is longer than other branches by design; don't compress it to match the infra branch's cadence just for consistency.

---

## 5. People / HR Operations

**Recommendation: open this sub-branch last, and keep it advisory-only for an extended period.**

Agents may surface data (attrition patterns, engagement signals, process friction) to inform human decision-makers. Agents should **not** have proposal-and-vote authority over anything that materially affects individual people's roles, compensation, or employment status, even with token-weighted DAO approval standing between the proposal and reality. The asymmetry here — a bad infra patch is usually recoverable, a bad decision about someone's job often isn't — means this sub-branch's design should prioritize human judgment over throughput far more than any other branch in this document.

If and when this sub-branch does move beyond advisory-only, that decision deserves its own dedicated design review, not a default inherited from the rest of this system.
