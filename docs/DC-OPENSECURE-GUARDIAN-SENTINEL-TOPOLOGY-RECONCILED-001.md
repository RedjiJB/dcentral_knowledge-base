# DC-OPENSECURE-GUARDIAN-SENTINEL-TOPOLOGY-RECONCILED-001 — OS-GUARDIAN & OS-SENTINEL Network Topology, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `opensecure-guardian-sentinel-topology` (2 docs).

## Current understanding

Companion network-topology specs to the already-consolidated `opensecure-guardian-sentinel-architecture`
technical-architecture pair, covering the same two products from a network-design angle: OS-GUARDIAN's
body-camera docking/upload network, and OS-SENTINEL's fixed-camera AI surveillance network. Same shared
document template (Executive Summary → Network Architecture Overview → product-specific network layers
→ Security → Redundancy/HA → Deployment Scenarios), consistent with the sibling-product pattern already
established for this suite.

**OS-GUARDIAN network topology (incorporated):** an "evidence-grade" network philosophy emphasizing
chain-of-custody, high-bandwidth video streaming, and offline resilience (officers record a full shift
without connectivity) [§Executive Summary]. Network scale table: Small (10-50 officers/cameras, 500GB/
day, 20TB storage, $50K/yr) through Enterprise (1,000+ officers, 50+TB/day, 2+PB storage, $5M+/yr)
[§Network Scale Characteristics]. A three-tier evidence-management network design, a dedicated body-
camera docking network, live-streaming infrastructure, evidence storage network, and access-control
layer round out the spec [§Network Architecture Overview through §Security & Access Control].

**OS-SENTINEL network topology (incorporated):** a "distributed AI-at-the-edge" network philosophy
emphasizing edge inference (detection/recognition/behavior analysis happening at the camera/NVR level,
not centrally), bandwidth optimization (transmitting only alerts/metadata rather than continuous video),
tiered local-to-cloud retention, and multi-site federation over open standards (ONVIF/RTSP/HLS)
[§Executive Summary]. Network scale table: Small (10-50 cameras, 1 site, 500GB/day, $25K/yr) through
Enterprise (1,000+ cameras, 20+ sites, 50+TB/day, custom AI models, $2M+/yr) [§Network Scale
Characteristics] — notably lower cost at every tier than OS-GUARDIAN's equivalent scale (e.g., Small
tier: $25K vs. $50K/yr), consistent with SENTINEL's bandwidth-optimized (metadata-only) design versus
GUARDIAN's full-video-stream requirement. Camera network design, video streaming architecture, storage
architecture, and a dedicated AI processing infrastructure layer round out the spec [§Network
Architecture Overview through §AI Processing Infrastructure].

**Shared pattern (incorporated):** both use identical scale-tier bucketing (Small/Medium/Large/
Enterprise with matching officer/camera-count boundaries: 10-50, 50-200, 200-1,000, 1,000+), suggesting
a deliberately shared network-planning framework across the two sibling products despite their
different bandwidth/cost profiles.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Evidence-grade network philosophy and scale/cost table | OS-GUARDIAN §Executive Summary | incorporated |
| Body camera docking network, live streaming, evidence storage network | OS-GUARDIAN §Network Architecture Overview through §Evidence Storage Network | incorporated |
| Security/access-control and redundancy/DR design | OS-GUARDIAN §Security & Access Control, §Redundancy & Disaster Recovery | incorporated |
| AI-at-the-edge network philosophy and scale/cost table | OS-SENTINEL §Executive Summary | incorporated (cost consistently lower than GUARDIAN's equivalent tier, attributable to metadata-only transmission) |
| Camera network design, video streaming, storage, AI processing infrastructure | OS-SENTINEL §Network Architecture Overview through §AI Processing Infrastructure | incorporated |
| Network security and HA design | OS-SENTINEL §Network Security, §Redundancy & High Availability | incorporated |
| Shared scale-tier bucketing across both products | OS-GUARDIAN + OS-SENTINEL, both §Network Scale Characteristics | incorporated |

## Unresolved tensions

None identified in this pass — the cost differential between the two products at matching scale tiers
is explained by their differing bandwidth models (GUARDIAN's continuous video streaming vs. SENTINEL's
metadata-only transmission), not an unexplained inconsistency.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/security/Open-Secure/OS-GUARDIAN-Network-Topology-md.md`
- `knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Network-Topology-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/security/Open-Secure/OS-GUARDIAN-Network-Topology-md.md,
  knowledge-base/d-central/security/Open-Secure/OS-SENTINEL-Network-Topology-md.md,
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
