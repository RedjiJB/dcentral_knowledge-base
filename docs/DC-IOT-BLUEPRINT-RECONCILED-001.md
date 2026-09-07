# DC-IOT-BLUEPRINT-RECONCILED-001 — D-Central IoT Device Integration Blueprint, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `dcentral-iot-integration-blueprint` (2 docs).

## Current understanding

`d-central-iot-blueprint` is a raw exhaustive device catalog (categories A-G: climate, energy, water,
access control, video/audio, safety, appliances); `dcentral-complete-integration` takes that same
category structure (A-G match exactly) and extends it to 18 total categories (A-R), adding for every
device type its integration path into D-Central's ICN/FCN/federation architecture. The second document
is an explicit architectural extension of the first, not an independent or competing catalog.

**Device catalog (incorporated):** an exhaustive, non-federation-aware inventory across 7 categories
(Climate & Environment, Energy & Power, Water & Fluid Systems, Perimeter & Access Control, Video/Audio/
Communications, Safety & Emergency, Appliances & Home Comfort), each broken into sub-categories with
named device types (e.g., under Energy: metering/management, renewables/storage, grid/demand-response)
[Blueprint §1]. A rough device-count estimate scales from 50-200+ devices for a single-family home to
10,000-1,000,000+ for a smart city/district [Blueprint, Device Count Summary]. A "Next-Level Catalog
Management" section recommends a device registry/CMDB, taxonomy database, device-class templates,
procurement tracking, and an interop-testing lab as the operational scaffolding needed to manage the
catalog at scale [Blueprint, Next-Level Catalog Management].

**Integration architecture (incorporated):** extends the same 7 categories plus 11 more (window
treatments, personal/wellness, office/workspace, retail/hospitality, healthcare, industrial,
agriculture, transportation, smart city, edge compute/gateways, specialty/niche) to 350+ total device
types across 40+ protocols [Integration §Legend, Next Steps]. Every device is mapped to one of four
connection patterns (Direct ICN-native, Gateway/protocol-bridge, Cloud-API bridge, Serial/edge-gateway),
one of three security levels (L1 device-cert+mTLS, L2 adds TPM/SE attestation, L3 adds end-to-end
content encryption + VC authorization), and a federation-value rating (None/Low/Medium/High) reflecting
how much cross-site data sharing benefits that device class [Integration §Legend]. Three worked
integration patterns are given in full (BACnet legacy-protocol bridge, Nest cloud-service bridge, and a
hypothetical native D-Central sensor with zero-touch onboarding) [Integration, Universal Integration
Patterns]. A per-category complexity matrix rates protocol diversity, federation value, and integration
effort — e.g., Industrial (M) and Smart City (P) are both rated "very high" on all three axes, while
Water Systems (C) is rated low effort/medium value [Integration, Integration Complexity Matrix]. A
four-phase rollout plan is given, from a 3-month foundation phase (5 device types, first 10 FCN
functions) through a Year-2+ ecosystem phase (100+ device types, open third-party SDK, full smart-city
integration) [Integration, Next Steps].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Exhaustive 7-category device catalog with device counts by deployment scale | Blueprint §1, Device Count Summary | incorporated |
| Catalog-management operational recommendations | Blueprint, Next-Level Catalog Management | incorporated |
| 18-category, 350+-device-type integration mapping (extends Blueprint's 7 categories) | Integration §Legend | incorporated (explicit extension of Blueprint's own category structure) |
| Connection-pattern, security-level, and federation-value taxonomy | Integration §Legend | incorporated |
| Three worked integration pattern examples (BACnet, Nest, native sensor) | Integration, Universal Integration Patterns | incorporated |
| Per-category integration complexity matrix | Integration, Integration Complexity Matrix | incorporated |
| Four-phase rollout plan (Foundation → Ecosystem) | Integration, Next Steps | incorporated |

## Unresolved tensions

None identified in this pass — the integration document's categories A-G are verified identical in
scope to the catalog document's A-G, confirming it as a direct extension rather than an independent or
conflicting taxonomy.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/verticals/home-trades/D-Central-v2/d-central-iot-blueprint-txt.md`
- `knowledge-base/d-central/verticals/home-trades/D-Central-v2/dcentral-complete-integration-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/verticals/home-trades/D-Central-v2/d-central-iot-blueprint-txt.md,
  knowledge-base/d-central/verticals/home-trades/D-Central-v2/dcentral-complete-integration-md.md,
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
