# DC-TRAFFICMESH-CITY-FLEET-RECONCILED-001 — TrafficMesh City Fleet Deployment, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `trafficmesh-city-fleet-deployment` (3 docs).

## Current understanding

Three complementary documents for TrafficMesh's Phase 2 expansion beyond the OC Transpo pilot:
DEPLOY-TM-002 is the expansion logic/revenue/political-prep plan; MKT-TM-GOV-003 is the City-of-Ottawa
pitch-deck narrative built on top of it; OS-PATROL-TM-FLEET-001 is the hardware/deployment-calendar
specification for the fleet categories DEPLOY-TM-002 names. All three are consistent on scale figures
and explicitly cross-reference each other.

**Expansion logic and revenue model (incorporated):** seven fleet categories phased across three sub-
phases (2A: bylaw vehicles + Public Works trucks + contractor kits, Months 1-3; 2B: garbage/recycling
trucks + snow plows, Months 3-6; 2C: street sweepers + parks vehicles, Months 6-9) [§1]. A per-revenue-
source city model: bus stop/lane enforcement ($300-600K/yr), snow-route parking ($400-800K/yr, "currently
near-zero enforcement due to staffing"), accessible parking ($150-300K/yr), plus non-revenue value from
plate-alert police referrals and $500K-1.5M in avoided Public Works survey costs [§2]. A contractor-kit
procurement clause template making captured data city property and kit tampering a contract breach, with
a 10-contractor Phase 2A pilot expanding in 2B [§3]. Political preparation addresses four stakeholder
groups (fiscal conservatives, civil liberties, police, CUPE/city workers) with a stated $500K hardware
cost (500 nodes × $1,000 avg) against a $1.2-2.1M Year-1 revenue projection, a 3-5 month payback [§4].

**City-of-Ottawa pitch narrative (incorporated):** reframes the same expansion as cross-departmental
infrastructure value rather than pure enforcement revenue, giving a per-department value table (Bylaw
$1.5-5M incremental revenue; Public Works $500K-1.5M avoided survey cost; OC Transpo $1-4M annualized;
Police — public-safety value, not quantified; Urban Planning $200-600K avoided traffic-study cost;
Emergency Management — qualitative resilience value) [§2]. The contractor-kit argument is reframed for
a political audience ("you are buying 50 kits that rotate through 500 vehicles," not 500 camera systems)
[§3]. Four named objections and answers, including an explicit distinction from the banned automated-
speed-enforcement category (TrafficMesh mandates human review, which the ban's own stated rationale
doesn't reach) [§4].

**Fleet hardware specification (incorporated):** a three-tier hardware architecture matching DEPLOY-
TM-002's fleet categories — Tier 1 permanent (hardwired, year-round, buses/bylaw/police/Public Works),
Tier 2 seasonal (semi-permanent bracket, IP67 at -30°C for plows Nov-Mar / sweepers Apr-Oct), Tier 3
contractor kit (magnetic/suction mount, <5 min install, no hardwired power) [§1]. A month-by-month
Ottawa seasonal deployment calendar detailing which fleet and violation types are active each month,
including a coldest-months (Dec-Feb) hardware-criticality note and a spring digital-twin-update
high-value window [§2]. A contractor-kit checkout programme: kits issued alongside safety equipment,
signed against LEGAL-CM-015, pooled at roughly 1 kit per 3 active contractors (17-20 kits for 50 active
contractors — consistent with DEPLOY-TM-002's "50-100 contractors active at any time" scale), Polygon
DID registration activated/deactivated on checkout/return, and automatic construction-zone geofence
enforcement activation on kit check-in [§3].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Seven-category fleet expansion phasing | DEPLOY-TM-002 §1 | incorporated |
| City revenue model by source | DEPLOY-TM-002 §2 | incorporated |
| Contractor-kit procurement clause and phased rollout | DEPLOY-TM-002 §3 | incorporated |
| Political stakeholder preparation and Phase 2 cost/payback | DEPLOY-TM-002 §4 | incorporated |
| Cross-departmental value proposition table | MKT-TM-GOV-003 §2 | incorporated |
| Contractor-kit political/cost framing | MKT-TM-GOV-003 §3 | incorporated |
| Objections and answers (incl. ASE-ban distinction) | MKT-TM-GOV-003 §4 | incorporated |
| Three-tier hardware architecture | OS-PATROL-TM-FLEET-001 §1 | incorporated (tiers match DEPLOY-TM-002's fleet categories) |
| Seasonal deployment calendar | OS-PATROL-TM-FLEET-001 §2 | incorporated |
| Contractor kit checkout/tracking/maintenance programme | OS-PATROL-TM-FLEET-001 §3 | incorporated (kit-pool ratio consistent with DEPLOY-TM-002's contractor-count scale) |

## Unresolved tensions

None identified in this pass — all three documents are explicitly designed as companion pieces for the
same expansion effort, and every cross-checkable figure (fleet categories, contractor scale, seasonal
timing) is consistent between them.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/business-legal/CivicMesh/DEPLOY-TM-002-City-Fleet-Expansion-Plan-v1-docx.md`
- `knowledge-base/d-central/business-legal/CivicMesh/MKT-TM-GOV-003-City-of-Ottawa-Pitch-Deck-Narrative-v1-docx.md`
- `knowledge-base/d-central/hardware/sensing-planes/CivicMesh/OS-PATROL-TM-FLEET-001-TrafficMesh-Fleet-Node-Specification-v1-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/business-legal/CivicMesh/DEPLOY-TM-002-City-Fleet-Expansion-Plan-v1-docx.md,
  knowledge-base/d-central/business-legal/CivicMesh/MKT-TM-GOV-003-City-of-Ottawa-Pitch-Deck-Narrative-v1-docx.md,
  knowledge-base/d-central/hardware/sensing-planes/CivicMesh/OS-PATROL-TM-FLEET-001-TrafficMesh-Fleet-Node-Specification-v1-docx.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
