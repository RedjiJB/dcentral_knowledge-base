# DC-DRONE-HARDWARE-RECONCILED-001 — Haiti Drone Cooperative Hardware Selection, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `drone-zoe-hardware-selection-guides` (2 docs).

## Current understanding

Both documents describe the same Haiti Drone Cooperative open-source drone platform matrix (identical
platform names and per-unit costs: SkyMite $390, UrbanHawk $1,208, RangerWing $1,778, EnforcerQuad
$4,085, CargoLifter $7,700). `updated-drone-guide` is explicitly the later revision (filename "updated,"
adds multi-sourcing detail and a new fixed-wing product line not present in the first document) but
does not explicitly supersede the first document's separate sensor-module catalog or its revenue
roadmap — see Unresolved tensions.

**Drone platform matrix (incorporated, consistent across both):** four size tiers — Micro (50-250g:
SkyMite, NanoSpy), Small (250g-2kg: UrbanHawk, RangerWing, StealthQuad), Medium (2-10kg: EnforcerQuad,
SurveillanceWing, GuardianHex), Heavy-Lift (10-25kg: CargoLifter, SkySentinel) — each with a named base
design (e.g., SkyMite = modified Crazyflie 2.1), flight-time/range specs, and a complete bill of
materials with per-component costs in both USD and HTG [Selection-Guide2 §1]. Per-platform costs
identically confirmed by the updated guide's cost-analysis table [Updated-Guide §4].

**Sensor module catalog (incorporated, Selection-Guide2 only):** eight open-source modular sensor
packages (OS-1 basic imaging through OS-8 communications/networking), each with 2-3 open-source
sourcing options costed against a named proprietary alternative (e.g., OS-2 thermal imaging: $217
open-source vs. FLIR Boson 640 at $3,200) [§2]. A module-combination matrix (2-module through
all-8-module combinations, $358-$2,306) maps combinations to named mission profiles [§3]. A
revenue-based development roadmap targets $50K → $150K → $300K → $500K+ cumulative revenue across four
6/12/18/18-month phases [§4]. A manufacturing/scaling strategy and a universal hot-swappable mounting
system close out the document [§5-6].

**Multi-sourced platform options and Flightory fixed-wing line (incorporated, Updated-Guide only):**
for each platform, multiple concrete open-source sourcing options are given with real project links
(e.g., SkyMite: Bitcraze Crazyflie, OpenRC Quadcopter, Hovership 3DFLY Micro, TinyTina 90mm — each with
its own cost and source URL) rather than Selection-Guide2's single fixed BOM per platform [§1]. A new
fixed-wing product line ("Flightory": Pico Talon, Mini Plank, Stallion, Stork, Super Stingray) is
introduced with its own cost figures ($13-40 for design files) and claimed 94-98% cost savings over
proprietary fixed-wing equivalents, positioned as complementary to the multirotor platforms rather than
replacing any of them [§4, Flightory Cost Advantages].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Four-tier drone platform matrix with BOMs | Selection-Guide2 §1 | incorporated (per-unit costs independently confirmed by Updated-Guide's cost table) |
| Eight open-source sensor module packages | Selection-Guide2 §2 | incorporated |
| Module-combination matrix | Selection-Guide2 §3 | incorporated |
| Revenue-based 4-phase development roadmap ($50K→$500K+) | Selection-Guide2 §4 | incorporated — not restated or explicitly superseded by Updated-Guide, see tension below |
| Manufacturing/scaling strategy and mounting system | Selection-Guide2 §5-6 | incorporated |
| Multi-sourced platform options with real project links | Updated-Guide §1 | incorporated (extends Selection-Guide2's single-BOM-per-platform with alternatives) |
| Flightory fixed-wing product line and cost comparison | Updated-Guide §4 | incorporated (new, additive product line) |
| Investment-based 5-phase implementation roadmap ($8K→$100K) | Updated-Guide §3 | incorporated — a different roadmap from Selection-Guide2's, see tension below |
| Updated annual revenue projections ($100K→$750K, Years 1-4) | Updated-Guide §4 | incorporated — different figures and time structure from Selection-Guide2's roadmap, see tension below |

## Unresolved tensions

**Two divergent implementation roadmaps exist for the same cooperative, not reconciled with each other.**
Selection-Guide2 §4 gives a sensor-module-focused, 4-phase, revenue-target roadmap over 36 months
($50,000 → $150,000 → $300,000 → $500,000+ cumulative revenue, keyed to sensor module development
priorities). Updated-Guide §3 gives a platform-focused, 5-phase, investment-figure roadmap also over 36
months plus a 5th regional-expansion phase ($8,000 → $20,000 → $40,000 → $60,000 → $100,000
investment, keyed to drone-platform and Flightory fixed-wing rollout), with its own separate annual
revenue projections ($100,000 → $750,000 across 4 years) that don't match Selection-Guide2's revenue
figures in either amount or time structure. Neither document states whether Updated-Guide's roadmap
replaces Selection-Guide2's, whether they're meant to run in parallel (one for sensor modules, one for
platforms), or whether Updated-Guide's roadmap is the authoritative revision. Left as an open question
rather than assumed to be either superseded or parallel, since a reader trying to build one financial
plan from these documents would get two incompatible sets of numbers depending on which roadmap they use.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/hardware/sensing-planes/Drone-Zoe/drone-selection-guide2-md-f756780a.md`
- `knowledge-base/d-central/hardware/sensing-planes/Drone-Zoe/updated-drone-guide-md-1780e328.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/hardware/sensing-planes/Drone-Zoe/drone-selection-guide2-md-f756780a.md,
  knowledge-base/d-central/hardware/sensing-planes/Drone-Zoe/updated-drone-guide-md-1780e328.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

Neither source doc is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator. (Note for that process: Updated-Guide's filename and content strongly suggest it revises Selection-Guide2's platform matrix specifically — worth a dedup-pass look at whether a formal supersession relationship should be recorded there, distinct from this Consolidator's own boundary against making that call.)


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

*No cross-references detected to/from other docs/*.md files.*

<!-- AUTO-GENERATED RELATED END -->
