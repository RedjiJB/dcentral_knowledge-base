# DC-OPENSECURE-PATROL-SENTINEL-IMPL-RECONCILED-001 — OS-PATROL & OS-SENTINEL Implementation Guides, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `opensecure-patrol-sentinel-implementation` (2 docs).

## Current understanding

Two deployment-runbook documents for two different Open-Secure products: OS-PATROL is mobile
fleet/vehicle-tracking hardware; OS-SENTINEL is the fixed-camera AI surveillance platform (already
covered architecturally in the consolidated `opensecure-guardian-sentinel-architecture` and
`opensecure-guardian-sentinel-topology` topics). Same shared phase-based deployment-guide template
(Executive Summary → Pre-Deployment Planning → numbered phases → Post-Deployment → Troubleshooting),
scaled very differently to match each product's actual deployment complexity.

**OS-PATROL implementation (incorporated):** a fast, low-cost deployment — 1-2 days per vehicle, a
2-person team (automotive + IT), $800-1,500/vehicle hardware+install cost, plus a 1-day centralized
Traccar-server setup [§Executive Summary]. Five phases: Server Setup (1 day) → Vehicle Hardware
Installation (4-6 hours) → Software Configuration (2 hours) → Testing & Validation (1 hour) → Go-Live,
followed by Post-Deployment and a Troubleshooting Guide [§Phase Overview through §Troubleshooting
Guide].

**OS-SENTINEL implementation (incorporated):** a substantially larger, longer deployment — 2-4 weeks
for a 10-100 camera site, a 3-4 person team (electrician + low-voltage tech + IT), $15,000-100,000
total system cost, scaling to 1,000+ cameras per site [§Executive Summary]. Eight phases: Site Survey
(2-3 days, produces CAD drawings and a cable plan) → Infrastructure Deployment (5-7 days, PoE
switches/cabling) → Camera Installation (5-10 days) → NVR/VMS Deployment (2-3 days) → AI Analytics
Deployment (2-3 days, detection-model rollout) → Testing & Validation (2-3 days) → Go-Live (1 day) →
Post-Deployment, followed by a Troubleshooting Guide [§Phase Overview through §Troubleshooting Guide].

**Why the scale difference is expected, not a conflict:** OS-PATROL is per-vehicle hardware
installation (a bounded, repeatable unit task), while OS-SENTINEL is a full facility infrastructure
build-out (site survey, electrical/low-voltage cabling, camera mounting at scale, AI model deployment)
— the ~10-20x difference in deployment timeline and cost per project reflects genuinely different scope
of work, not an inconsistency between overlapping claims about the same system.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| OS-PATROL deployment timeline, team, and cost | OS-PATROL Implementation Guide §Executive Summary | incorporated |
| OS-PATROL 5-phase deployment sequence | OS-PATROL Implementation Guide §Phase Overview through §Post-Deployment | incorporated |
| OS-PATROL troubleshooting guide | OS-PATROL Implementation Guide §Troubleshooting Guide | incorporated |
| OS-SENTINEL deployment timeline, team, and cost | OS-SENTINEL Implementation Guide §Executive Summary | incorporated |
| OS-SENTINEL 8-phase deployment sequence | OS-SENTINEL Implementation Guide §Phase Overview through §Post-Deployment | incorporated |
| OS-SENTINEL troubleshooting guide | OS-SENTINEL Implementation Guide §Troubleshooting Guide | incorporated |

## Unresolved tensions

None identified in this pass — the two guides describe genuinely different-scope deployments (per-
vehicle hardware install vs. full-site infrastructure build-out) for two different products, and the
large difference in timeline/cost/team-size between them is explained by that scope difference rather
than being an unexplained inconsistency.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/security/Open-Secure/OS-PATROL-Implementation-Guide-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Implementation-Guide-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/security/Open-Secure/OS-PATROL-Implementation-Guide-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Implementation-Guide-md.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

Neither source doc is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

*No cross-references detected to/from other docs/*.md files.*

<!-- AUTO-GENERATED RELATED END -->
