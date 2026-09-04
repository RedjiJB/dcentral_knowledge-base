# Branch: Infrastructure, Cybersecurity, Network & Uptime

**Extends:** `00-master-architecture.md` — read that first. This document only covers what's specific to this branch.

**Ground truth:** relatively objective. A CVE is exploitable or it isn't; a service is up or it isn't; a patch closes the hole or it doesn't. This is why this branch is the recommended starting point (as already agreed) — it's the domain where the loop's monitoring/retrospective stage has the clearest signal, so it's the safest place to prove the system works before trusting it elsewhere.

---

## 1. Scope Definition

Example scope votes this branch is designed for:
- "Monitor and research CVEs affecting our stack."
- "Audit and harden our external attack surface."
- "Improve uptime/incident response for [service]."
- "Reduce mean-time-to-detect for [class of anomaly]."

Scope votes should name the asset boundary explicitly (which systems/environments are in scope) — this boundary is what the sandboxing hook in §4 enforces.

---

## 2. Specialized Agent Roles

| Role | Specialization of (master doc §4) | Job |
|---|---|---|
| **Recon/Intel** | Recon/Intel | Ingests CVE feeds, vendor advisories, dependency graphs; maintains live asset inventory (what's running where, what version, what's exposed) |
| **Red-team** | Adversarial | Attempts reproduction of vulnerabilities against staging/shadow environment; rate-limited, scoped |
| **Blue-team** | Defensive/Validation | Checks whether existing controls (WAF rules, EDR signatures, detection rules) would catch a given technique; validates proposed patches |
| **Attack-surface analyst** | Analysis | Maps exposure and blast radius if a given vulnerability were exploited |
| **Playbook agent** | (new, infra-specific) | Drafts incident response runbooks: detection, containment, eradication, comms, who gets paged |
| **Synthesis** | Synthesis | Compiles the above into one proposal using the template in §3 |
| **Monitoring** | Monitoring | Tracks post-deploy incident rate, false-positive rate, detection latency |

---

## 3. Proposal Template Extension

Adds to the master template (§7 of master doc):

```markdown
### CVE / vulnerability detail
CVE ID (if applicable), CVSS score, exploitability (PoC exists? actively exploited in the wild?),
affected assets from the live inventory.

### Patch / mitigation
Code diff or config change. If no patch exists yet: compensating control
(WAF rule, network segmentation, feature disable) and its coverage gap.

### Response runbook update
Detection signature/query, containment steps, eradication steps, comms template,
on-call paging rule.

### Second red-team pass result
Confirmation that the fix holds under a repeat attempt post-patch, pre-deploy.
```

---

## 4. Guardrails Specific to This Branch

- **Sandboxing enforcement (mandatory):** the `adversarial.*`-role agent's credential `scope` field is bound to the declared asset boundary from the scope vote — the disclosure/access check fails structurally for anything outside it, per DC-AGENT-CREDENTIAL-001 §5. This is enforced at the credential layer, not a prompt instruction.
- **Blast-radius threshold for human sign-off:** any change touching authentication, network segmentation, production database access, or anything with a defined downtime window above [org-defined threshold, e.g. 5 minutes] requires technical steward sign-off regardless of vote outcome.
- **Emergency fast-track is expected to be used most here.** A zero-day does not wait for a 7-day vote. Define in advance: what severity triggers the council path, what the council quorum is, and the maximum time before retroactive full-DAO ratification is required (recommend: 72 hours).
- **No implementation agent may hold both patch-deployment and monitoring-metric-reporting roles** — this prevents an agent from grading its own homework on whether a fix worked.

---

## 5. Tooling for This Branch

- CVE/threat-intel feeds (NVD, vendor advisories, dependency-scanning tools) feeding the Recon agent.
- Sandboxed staging environment with realistic (anonymized) traffic for red-team reproduction.
- Canary deployment + automatic rollback on error-rate/auth-failure/latency thresholds (see `05-tooling-and-frameworks.md` for platform options).
- Permanent audit record via the archive storage tier (DC-MESHSTORAGE-ARCHIVE-001) — for this branch specifically, this doubles as your forensic record if an incident occurs during or after an agent-proposed change, and the Merkle-anchor/independent-log mechanic means it stays tamper-evident even against your own infrastructure operators, not just append-only.

---

## 6. Reference Walkthrough

1. DAO scope vote: "Monitor and research CVEs affecting our stack" (asset boundary + budget defined).
2. Recon agents ingest CVE feeds, match against asset inventory, prioritize by exploitability × exposure.
3. Red-team agents attempt reproduction against staging; blue-team agents check existing control coverage; attack-surface agents map blast radius.
4. Playbook agent drafts the response runbook.
5. Synthesis agent compiles the full proposal (§3 template).
6. DAO votes — fast-tracked via council if critical severity, standard cycle otherwise.
7. Staged implementation: canary → automated health checks → human sign-off if above threshold (§4).
8. Monitoring agents track incident rate, false-positive rate, and confirm the fix holds under a second red-team pass.
9. Stakeholders review the monitoring dashboard (rendered to Obsidian per master doc §6.2), feedback becomes context for the next scope vote.
10. Retrospective vote confirms, iterates, or triggers rollback.
