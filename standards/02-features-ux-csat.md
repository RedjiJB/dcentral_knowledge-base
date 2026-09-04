# Branch: Features, UX & Customer Satisfaction

**Extends:** `00-master-architecture.md` — read that first. This document only covers what's specific to this branch.

**Ground truth:** probabilistic, not binary. A UX change might improve activation — you don't know until you test it. This is the key structural difference from the infrastructure branch: "gated implementation" (master doc §2, step 5) must become an actual controlled experiment here, not just a staged deploy.

---

## 1. Scope Definition

Example scope votes:
- "Reduce onboarding drop-off for [segment]."
- "Improve CSAT for [product area]."
- "Close feature gaps against [competitive set]."
- "Reduce support ticket volume for [issue category]."

---

## 2. Specialized Agent Roles

| Role | Specialization of (master doc §4) | Job |
|---|---|---|
| **User research agent** | Recon/Intel | Clusters support tickets, reviews, session-replay data, NPS/CSAT verbatims for recurring friction points |
| **Analytics agent** | Recon/Intel | Reads funnels, drop-off points, feature adoption curves from product analytics |
| **Competitive research agent** | Recon/Intel | Scans competitor changelogs and review sites for feature gaps |
| **Hypothesis agent** | Analysis | Turns a pain point into a falsifiable claim: target metric, minimum detectable effect, expected direction |
| **Design/prototype agent** | (new, UX-specific) | Proposes UI/UX changes, mockups |
| **Synthesis** | Synthesis | Compiles into one proposal using the template in §3 |
| **Monitoring** | Monitoring | Reads the live experiment (§4) and reports statistical significance, not just raw movement |

---

## 3. Proposal Template Extension

Adds to the master template (§7 of master doc):

```markdown
### Hypothesis
Falsifiable claim: "We believe [change] will move [target metric] by [expected direction/magnitude]
because [evidence from research agents]."

### Target metric + guardrail metrics
- Target metric: the one thing this change is trying to move, and the minimum detectable effect.
- Guardrail metrics: metrics that must NOT get worse (error rate, latency, unrelated CSAT segments,
  accessibility score). List at least two. A proposal that only defines a target metric and no
  guardrails is incomplete — see §5 (Goodhart risk).

### Experiment design
Cohort size, duration, feature-flag rollout percentage, statistical method (see
`05-tooling-and-frameworks.md` for platform-specific options).

### Rollback criteria
Exact thresholds on guardrail metrics that trigger automatic rollback before the
retrospective vote even convenes.

### Qualitative risk
Accessibility, brand, or trust risk not captured by the quantitative metrics above.
```

---

## 4. Feature-Flag / Experimentation Infrastructure

This branch's equivalent of the infrastructure branch's "canary deploy" is a real controlled experiment:

- Ship behind a feature flag to a defined cohort (§3 experiment design).
- Monitoring agents read the flag platform's stats engine directly rather than eyeballing raw numbers — sequential/Bayesian methods matter here because agents evaluating results early and often will otherwise inflate false-positive rates.
- The retrospective vote (master doc §3.1) is informed by actual experiment results, not agent-predicted outcomes. This is a hard rule for this branch: no full rollout without an experiment result behind it, even if the DAO is impatient.
- Kill-switch on guardrail-metric breach should be automatic (flag platform triggers rollback), not wait for a DAO vote — the DAO vote is for "do we adopt this permanently," not "do we stop actively harming a metric right now."

See `05-tooling-and-frameworks.md` for the platform comparison — note that the centralized SaaS options there (Statsig, LaunchDarkly) don't fit a sovereign/cooperative infrastructure model well, and even the self-hosted open-source option (GrowthBook) assumes a centralized rollout service rather than a decentralized cohort mechanism.

**Resolved — see DC-VERIFIABLE-ROLLOUT-001.** What follows is the original open-gap note, kept for context: a decentralized feature-flag primitive didn't exist as a named component. The natural shape, given decentralized infrastructure: cohort assignment via deterministic hashing of the user's own identifier, verifiable by anyone, with rollout-percentage and guardrail thresholds set via governance rather than a SaaS dashboard, and results read from the same permanent-attestation pattern used everywhere else. DC-VERIFIABLE-ROLLOUT-001 specifies this in full — reframed as a verifiable progressive rollout primitive rather than a flag, since the real requirement includes safety-gated automation, not just an on/off toggle.

---

## 5. Goodhart Risk — Specific Guardrails for This Branch

Unlike the infrastructure branch, a metric-optimizing agent here can find ways to move a number that don't reflect the thing you actually care about (e.g., a CSAT-optimizing change that reduces friction by silently reducing functionality). Two mandatory mitigations:

1. **Multiple guardrail metrics are required on every proposal, not optional** — a single target metric with no guardrails is grounds for automatic proposal rejection at the synthesis stage, before it even reaches a DAO vote.
2. **Dissenting-agent requirement:** for any proposal touching a core funnel (signup, checkout, retention-critical flow), run the hypothesis assessment through at least two independent agents (Mixture of Agents pattern, master doc §6.5) and preserve disagreement in the proposal rather than collapsing to consensus.

---

## 6. Reference Walkthrough

1. DAO scope vote: "Reduce onboarding drop-off for new signups."
2. User research + analytics agents cluster friction points from session replay, tickets, and funnel data.
3. Hypothesis agent drafts a falsifiable claim with target + guardrail metrics.
4. Design/prototype agent proposes the change.
5. Synthesis agent compiles the proposal (§3 template).
6. DAO votes to authorize the experiment (not the permanent change).
7. Staged implementation: feature-flagged rollout to defined cohort, automatic kill-switch on guardrail breach.
8. Monitoring agents track significance on the target metric and confirm guardrails held.
9. Stakeholders review results (rendered to Obsidian per master doc §6.2).
10. Retrospective vote: full rollout, iterate, or roll back — based on experiment result, not prediction.
