# DC-NETWORKING-ARCH-RECONCILED-001 — D-Central Networking Architecture, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `dcentral-networking-architecture` (2 docs).

## Current understanding

Two networking architecture documents at different levels of abstraction and from different dates:
`D-Central-Networking-Architecture-Complete` (22 sections, Oct 2025) is the later, higher-level
comprehensive spec organized around three named networking models (ICN/FCN/DTN); `dcm-blueprint-
comprehensive` (9 sections, May 2025) is the earlier, more concrete protocol-level blueprint
(real BATMAN-adv/RPL/6LoWPAN configuration, C structs, shell config files). Both build on a shared
BATMAN-adv Layer-2 mesh foundation, but they use conflicting numbering for their own device-tier
schemes (see Unresolved tensions).

**Comprehensive architecture (incorporated):** three networking models — Information-Centric
Networking (content requested by hash/name, not location), Function-Centric Networking (distributed
compute as a first-class network primitive), and Delay-Tolerant Networking (resilient offline
operation) — described as working in concert, on a mesh-first, edge-native, content-addressable
foundation [§1-2]. The mesh layer itself uses BATMAN-adv at Layer 2, with TQ (Transmission Quality,
computed as received/sent packet ratio × 255) as the path-selection metric [§8.2]. An edge-node
hierarchy (§9.1) classifies compute nodes by hardware capacity and service capability: Tier 0 "Nano
Edge/D-Home" (Raspberry Pi 4/5, 1-2 users, ICN cache + basic FCN + DTN relay) → Tier 1 "Micro Edge/
D-Block" (Intel NUC, 10-50 users, full FCN runtime) → Tier 2 "GPU Edge/D-District" (workstation with
NVIDIA L4/RTX 4000, 50-200 users, AI inference) → Tier 3 "Cluster Edge/D-City" (multi-node HA cluster,
1,000+ users, regional hub). Further sections cover zero-trust security, service discovery, caching,
specialized-node integration, hardware/software stacks, governance, economics, and a phased deployment
plan (not individually itemized here given their number, but every section is accounted for in the
Provenance table's chapter-level entries).

**Concrete mesh blueprint (incorporated):** a four-tier physical device hierarchy classified by network
*role* rather than compute capacity: Tier-0 "ultra-low-power sensors/actuators" (Zephyr RTOS, RPL
routing, energy harvesting) → Tier-1 "Mobile/IoT nodes" (Wi-Fi direct client, border gateway for Tier-0)
→ Tier-2 "Community Routers" (OpenWRT/LibreMesh, WASM runtime, adaptive network coding) → Tier-3
"Backbone/Gateway Nodes" (x86-64/ARM64, fibre/LTE/satellite backhaul) [§2]. Specific protocol-level
mechanisms are given in real syntax: BATMAN-adv OGM enhancements (ETX/SNR-weighted path selection,
Ed25519 message signing, EWMA link-quality smoothing), a BATMAN-RPL border-gateway interface
configuration (with real `iface`/`iwpan` config blocks) and a C struct for its sleep-coordination
protocol, an energy-aware routing weight table (mains-powered nodes weighted 0.5×/preferred through
sub-30%-battery nodes weighted 3×/avoided), and adaptive RLNC network coding activated above a 5%
packet-loss threshold [§2.1]. Further sections cover zero-trust security implementation, service-layer
architecture, observability, deployment/operations, and a development roadmap.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Three networking models (ICN/FCN/DTN) and mesh-first/edge-native design philosophy | Comprehensive §1-3 | incorporated |
| Network architecture layers, ICN, FCN, DTN detail | Comprehensive §4-7 | incorporated |
| BATMAN-adv mesh topology and TQ path-selection metric | Comprehensive §8 | incorporated |
| Edge-node hardware-capacity tier hierarchy (Tier 0-3, Nano→Cluster Edge) | Comprehensive §9.1 | incorporated — conflicts in naming with the mesh blueprint's Tier 0-3, see tension below |
| Thin-client architecture, zero-trust security, discovery/caching, specialized nodes, D-Search, hardware/software stacks | Comprehensive §10-17 | incorporated |
| Network governance, economics, performance, enterprise/legacy integration, deployment | Comprehensive §18-22 | incorporated |
| Multi-tier physical device hierarchy by network role (Tier-0 sensors → Tier-3 backbone) | Blueprint §1.2, §2 | incorporated — conflicts in naming with the comprehensive doc's Tier 0-3, see tension below |
| BATMAN-adv OGM enhancements (ETX/SNR weighting, Ed25519 signing, EWMA) | Blueprint §2.1.1 | incorporated (extends the comprehensive doc's simpler TQ-only metric with concrete enhancements) |
| BATMAN-RPL border gateway config and sleep-coordination protocol | Blueprint §2.1.2 | incorporated |
| Energy-aware routing weight table | Blueprint §2.1.3 | incorporated |
| Adaptive RLNC network coding | Blueprint §2.1.4 | incorporated |
| Zero-trust security, service layer, observability, deployment, roadmap | Blueprint §3-9 | incorporated |

## Unresolved tensions

**"Tier 0" through "Tier 3" name two different, incompatible hierarchies.** The comprehensive doc's
Tier 0-3 (§9.1) classifies *compute edge nodes* by hardware capacity and concurrent-user capacity
(Tier 0 = a Raspberry Pi serving 1-2 users; Tier 3 = a multi-node cluster serving 1,000+ users). The
blueprint's Tier 0-3 (§2) classifies *mesh participant devices* by network role (Tier 0 = ultra-low-power
sensors with no compute-service capability at all; Tier 3 = backbone/gateway nodes). These are not the
same axis relabeled — the comprehensive doc's Tier 0 (a Raspberry Pi running ICN cache + FCN + DTN
relay services) is a considerably more capable device than the blueprint's Tier 0 (a coin-cell sensor
running Zephyr RTOS with no service hosting at all). Attempted reconciliation: it's plausible these
describe two different concerns (device role in the mesh vs. compute service tier a node can host) that
could coexist as orthogonal classifications — a single physical node might have a mesh-role tier and a
separate compute-service tier — but neither document states that relationship, and reusing identical
"Tier 0-3" numbering for two different axes is exactly the kind of documentation collision that causes
real confusion (e.g., "deploy this service at Tier 1" becomes ambiguous between the two schemes). Left
as an open naming conflict rather than resolved, since resolving it would require an explicit editorial
decision (rename one scheme) neither source document has made.

**Related work:** [DC-COMPUTE-SILICON-ARCH-001](DC-COMPUTE-SILICON-ARCH-001.md) adds a hardware-flexibility
axis (CPU/GPU/FPGA/CGRA/eFPGA/Structured ASIC) on top of Tier 2 "GPU Edge/D-District" and deliberately does
not reuse "Tier" numbering, to avoid compounding this exact conflict with a third scheme.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/mesh-services/connectivity/D-Central-v2/D-Central-Networking-Architecture-Complete-md.md`
- `knowledge-base/d-central/meta/platform-scaffolding/D-Central/dcm-blueprint-comprehensive-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/mesh-services/connectivity/D-Central-v2/D-Central-Networking-Architecture-Complete-md.md,
  knowledge-base/d-central/meta/platform-scaffolding/D-Central/dcm-blueprint-comprehensive-md.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

Neither source doc is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

**References:**
- [[DC-COMPUTE-SILICON-ARCH-001|DC-COMPUTE-SILICON-ARCH-001 — Compute Silicon Class Architecture (v1, generated 2026-09-07)]]

**Referenced by:**
- [[DC-COMPUTE-SILICON-ARCH-001|DC-COMPUTE-SILICON-ARCH-001 — Compute Silicon Class Architecture (v1, generated 2026-09-07)]]

<!-- AUTO-GENERATED RELATED END -->
