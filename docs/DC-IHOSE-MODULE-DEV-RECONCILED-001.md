# DC-IHOSE-MODULE-DEV-RECONCILED-001 — OpenVision Module Development, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `ihose-module-development` (2 docs).

## Current understanding

Two module-development guides for the same OpenVision Platform, both version 1.0, both describing a
containerized custom-analytics-module framework — but they specify genuinely different, incompatible
SDK interfaces for the same framework (see Unresolved tensions). Everything outside the core SDK
interface (module types taxonomy, Docker/Kubernetes deployment mechanics, monitoring/metrics approach)
is consistent between them.

**Module framework concept (incorporated, consistent):** custom analytics run as isolated containers
communicating with the core platform via standardized interfaces, avoiding any need to modify core
platform code [03-Module-Development-Guide §Introduction; development.md §Overview]. Both name similar
module-type taxonomies — 03-Module-Development-Guide's four types (Frame Processor, Stream Analyzer,
Event Generator, Integration Module) and development.md's four types (Analytics, Integration,
Processing, Notification Modules) overlap conceptually (both single out "Integration Module/Modules" by
name) without being an identical list — this reads as two independently-drafted but non-contradictory
categorizations rather than a conflict, since neither claims to be the exhaustive canonical taxonomy.

**Deployment and operations (incorporated, consistent):** both specify Docker containerization with a
CUDA/Python base image, Kubernetes deployment via `kubectl`/manifests, resource requests/limits in the
same units (memory in Gi, CPU in millicores, optional GPU), and a module registry/marketplace for
publishing modules with a `module.yaml` manifest [03-Module-Development-Guide §Containerization,
§Deployment, §Module Marketplace equivalent not present but registration flow matches;
development.md §Module Deployment, §Module Marketplace]. Both recommend Prometheus-style custom metrics
(Counter/Histogram) for monitoring [03-Module-Development-Guide §Monitoring & Operations;
development.md §4. Metrics and Monitoring]. Both point to the same community resources
(community.openvision.io, github.com/openvision/modules).

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Module-framework concept and containerized-module philosophy | 03-Module-Development-Guide §Introduction; development.md §Overview | incorporated |
| Module-type taxonomies (overlapping, not identical) | 03-Module-Development-Guide §Module Types; development.md §Module Types | incorporated (independently-drafted, non-contradictory categorizations) |
| Docker/Kubernetes deployment mechanics | 03-Module-Development-Guide §Containerization, §Deployment; development.md §Module Deployment | incorporated |
| Metrics/monitoring approach (Prometheus Counter/Histogram) | 03-Module-Development-Guide §Monitoring & Operations; development.md §4 Metrics and Monitoring | incorporated |
| Module registry/marketplace publishing flow | 03-Module-Development-Guide §Module Registration; development.md §Module Marketplace | incorporated |
| SDK class hierarchy, method signatures, return types | Both, §Development Workflow (03-Module-Development-Guide) / §Module SDK (development.md) | incorporated — genuinely conflicting, see tension below |

## Unresolved tensions

**The two documents specify incompatible SDK interfaces for the same module framework version.**
03-Module-Development-Guide has modules subclass a single `VideoModule` base class (imported from
`openvision.module`), overriding `process_frame(self, frame, metadata)`, which **returns a dict**
(`{'detections': [...], 'processing_time_ms': ...}`). development.md has modules subclass a
`BaseModule`/`AnalyticsModule`/`IntegrationModule` hierarchy (imported from `openvision.sdk`), with an
explicit `initialize(config)` lifecycle method not present in 03-Module-Development-Guide's shown
example, and `process_frame` **returns a list of `Detection` objects** (a typed class with `class_name`,
`confidence`, `bbox`, `metadata` fields) rather than a dict. These are not stylistic variations of the
same interface — the import path, base class name, method set, and the process_frame return type all
differ. Attempted reconciliation: it's plausible these represent two SDK generations (e.g., a simpler
early interface vs. a more structured typed one) or two different language-independent framing choices
by two different technical writers, but neither document states a version history, a deprecation, or a
relationship to the other. A developer following one guide's code examples against the other guide's
described SDK would get import errors. Left as an open conflict rather than assumed to be either the
current or superseded interface.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/security/IHOSE/03-Module-Development-Guide-docx.md`
- `knowledge-base/d-central/security/IHOSE/development-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/security/IHOSE/03-Module-Development-Guide-docx.md,
  knowledge-base/d-central/security/IHOSE/development-md.md,
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
