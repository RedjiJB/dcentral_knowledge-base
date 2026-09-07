# DC-MESHNAV-RECONCILED-001 — MeshNav Architecture & Data Pipeline, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `meshnav-architecture-data-pipeline` (2 docs).

## Current understanding

DC-MN-ARCH-001 is the product/architecture spec for MeshNav (a Waze-competitor navigation app);
DC-MN-DATA-001 is its data pipeline spec. Explicitly cross-referenced and fully consistent on every
shared technical claim.

**Product architecture and competitive positioning (incorporated):** MeshNav's core differentiation
from Waze is data provenance — TrafficMesh's city-fleet nodes generate systematic 24/7 road-condition
data (including overnight, when Waze's crowdsourced reports are sparse), versus Waze's random
civilian-report coverage [§1]. Four features are named as structurally impossible for Waze to replicate:
enforcement-zone transparency (showing active node "Safety Zone" locations, framed as pro-deterrence
rather than violation-avoidance), a per-segment road-condition confidence score, a live plow-coverage
map, and cooperative data ownership (contributors earn D-Credit; Waze's contributor data is owned by
Google with no compensation) [§2]. Revenue model: navigation is free (subsidized by municipal data
agreements), with a paid Premium Fleet tier and an insurance-integration option; the platform is
explicitly ad-free as both a marketing differentiator and cooperative principle [§3].

**Data pipeline (incorporated):** six data sources feed the platform — the TrafficMesh node fleet
(real-time continuous), the Digital Twin engine (24-hour max update cycle per segment, guaranteed),
OC Transpo GTFS-RT (30-second updates), City of Ottawa Open Data (daily batch), contractor-kit GPS
(30-second updates while active), and MeshNav user reports (real-time on submission) [§1]. A road-
condition confidence formula is given explicitly: `confidence(t) = base_confidence × decay_factor(t,
asset_type) × observation_count_weight`, with asset-type-specific decay rates (pavement: 7 days; signs:
30 days; construction zones: 4 hours) and driver-facing display thresholds (<0.4 = "unverified,"
≥0.8 = full confidence) [§2]. The enforcement-zone-transparency feature's technical scope is specified
precisely: shows zone type/active hours/speed threshold, explicitly does NOT show individual node
vehicle location, kit identifiers, or real-time evidence-capture status — and the same deterrence
argument (revenue from violations is "a fallback, not the primary goal") appears identically in both
documents [§3].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Waze competitive-differentiation data-source comparison | DC-MN-ARCH-001 §1 | incorporated |
| Four Waze-cannot-replicate features | DC-MN-ARCH-001 §2 | incorporated |
| Revenue/sustainability model (free tier, fleet tier, insurance, no-ads) | DC-MN-ARCH-001 §3 | incorporated |
| Six-source data pipeline with update frequencies | DC-MN-DATA-001 §1 | incorporated |
| Road-condition confidence formula and display thresholds | DC-MN-DATA-001 §2 | incorporated |
| Enforcement-zone-transparency technical scope and privacy limits | DC-MN-DATA-001 §3 | incorporated (deterrence argument identical across both docs) |

## Unresolved tensions

None identified in this pass — every shared claim (plow-coverage window, enforcement-zone scope and
privacy limits, deterrence-over-revenue framing) is stated identically in both documents.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/mesh-services/sensors-mobility/CivicMesh/DC-MN-ARCH-001-MeshNav-Architecture-v1-docx.md`
- `knowledge-base/d-central/mesh-services/sensors-mobility/CivicMesh/DC-MN-DATA-001-MeshNav-Data-Pipeline-v1-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/mesh-services/sensors-mobility/CivicMesh/DC-MN-ARCH-001-MeshNav-Architecture-v1-docx.md,
  knowledge-base/d-central/mesh-services/sensors-mobility/CivicMesh/DC-MN-DATA-001-MeshNav-Data-Pipeline-v1-docx.md,
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
