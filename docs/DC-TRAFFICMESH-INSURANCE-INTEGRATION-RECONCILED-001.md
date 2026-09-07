# DC-TRAFFICMESH-INSURANCE-INTEGRATION-RECONCILED-001 — TrafficMesh/CivicMesh Insurance Integration & Revenue, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `trafficmesh-insurance-integration-revenue` (5 docs).

## Current understanding

Five tightly cross-referencing documents defining CivicMesh/TrafficMesh's insurance data-product line —
a technical specification, two go-to-market/pricing documents, a TrafficMesh-specific UBI variant, and
the overall revenue model tying insurance API revenue into the broader financial plan. All five are
fully consistent on pricing, tier structure, and privacy constraints.

**Insurance Integration Specification (incorporated):** the core technical spec defining four data-
product tiers via REST API — Tier 1 aggregate corridor-risk feed (no individual consent, community
federation agreement only), Tier 2 individual driving-record API (explicit per-insurer CCSC-member
opt-in via Member App), Tier 3 incident-evidence packages (individual consent or legal authority), Tier
4 premium-reduction community certification [§1]. A detailed Tier 2 consent-flow (insurer DID/Data-
Sharing-Agreement verification → member consent-store check → 403 CONSENT_NOT_FOUND/CONSENT_REVOKED on
failure → anonymized 12-month summary generation → dual audit logging to both member and insurer) [§2].
A UBI backbone section framed as a named SR&ED technical challenge — constructing a behavioral risk
score from enforcement-adjacent data without adverse selection or geographic proxy discrimination —
with an explicit anti-discrimination design principle that corridor risk scores are never applied to
individual drivers based on where they live, only where and how they drive [§3].

**Insurance Partner Pitch Deck (incorporated):** a 12-slide narrative for Canadian P&C insurer actuarial/
innovation teams (Intact, Desjardins, Aviva, SGI), opening with the self-reported-telematics pain point
(40% of drivers modify behavior during telematics periods) before introducing CivicMesh as third-party-
validated data from the same infrastructure that issues citations [Slides 1-2]. Walks through the same
three data tiers as the Integration Specification, a "premium discount flywheel" network-effect
argument, a fraud-reduction pitch, competitive-positioning framing ("first insurer... wins the opt-in
market"), a privacy/compliance slide, and pricing matching the other four documents exactly (Tier 1
$50K-150K/year, Tier 2 $15-25/query, Tier 3 $50-75/package) [Slides 3-11]. Closes with a free 90-day
Tier 1 pilot as the low-friction first ask [Slide 12].

**TrafficMesh Revenue Model (incorporated):** the overall financial plan into which insurance API
revenue feeds as one of five revenue streams alongside MSSP citation-revenue share, NOC management
fees, training certification, and non-insurance data marketplace revenue. A 4-phase revenue
architecture (OC Transpo pilot → city fleet expansion → civilian opt-in + first insurance subscriber →
data marketplace maturity), with the insurance API becoming a named Phase 3 milestone ("first insurance
API subscriber paying annual fee") [§1]. Detailed OC Transpo pilot citation-revenue math (NYC-MTA-ACE-
based volume projections, 20% MSSP share, a conservative $5,000-15,000/month planning figure using the
30th percentile rather than the upper bound) [§2]. An insurance-API-specific revenue table matching the
other documents' per-tier pricing exactly, aggregating to ~$100,000 Year 1 and ~$1.5M Year 3 total
insurance API revenue [§3]. A five-year, five-stream revenue projection table totaling $185K-386K Year 1
through $10.2M-21.3M Year 5 [§4].

**Insurance Data Product Catalogue (incorporated):** a detailed product catalogue restating the same
four tiers with identical pricing to the Integration Specification and Revenue Model, adding concrete
sample-metric detail (e.g., Tier 2's "lane discipline score" specified as a percentile vs. Ottawa
drivers) [§1]. A premium-discount tier schedule — 3-5% for basic community participation, 8-12% for
full individual opt-in, an additional 5-8% clean-record bonus, an additional 2-3% high-coverage-
community bonus, and a separate 8-15% commercial-fleet premium tier — consistent with (and one tier
richer than) the TrafficMesh-specific discount table below [§2].

**TrafficMesh Insurance Integration Specification, OS-PATROL variant (incorporated):** the TrafficMesh/
mobile-enforcement-specific application of the same insurance data products — corridor risk score, UBI
driving-behavior record (drawn from opted-in node-owning drivers' own dashcam footage rather than
third-party enforcement footage), collision corridor analysis via near-miss detection, and a seasonal
risk-adjustment product framed as replacing insurers' weather-data-only estimates with "ground truth"
[§1]. A UBI backbone technical design detailing the specific behavior-extraction methods (following-
distance estimation from camera + OBD-II speed, hard-braking events, construction/school-zone
compliance) and an explicit privacy constraint that insurers receive only statistical summaries (e.g.
"87th percentile following distance"), never location traces [§2]. A premium discount tier table
matching the Data Product Catalogue's first four tiers exactly (3-5%/8-12%/+5-8%/+2-3%), adding an
explicit "~25% maximum combined discount" figure for a fully-engaged clean-record participant not
stated numerically in the Catalogue document [§3].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Four-tier data-product API architecture | Insurance Integration Specification §1 | incorporated (pricing matches all four other documents exactly) |
| Tier 2 consent-flow mechanics | Insurance Integration Specification §2 | incorporated |
| UBI backbone SR&ED challenge and anti-discrimination design | Insurance Integration Specification §3 | incorporated (consistent with the OS-PATROL variant's privacy constraint) |
| Insurer pitch narrative and free-pilot ask | Insurance Partner Pitch Deck, Slides 1-12 | incorporated |
| 4-phase revenue architecture and OC Transpo pilot math | TrafficMesh Revenue Model §1-2 | incorporated |
| Insurance API revenue table and 5-year total projection | TrafficMesh Revenue Model §3-4 | incorporated (per-tier figures match the Pitch Deck and Data Product Catalogue exactly) |
| Detailed product catalogue with sample metrics | Insurance Data Product Catalogue §1 | incorporated |
| Premium discount tier schedule (5 tiers incl. commercial fleet) | Insurance Data Product Catalogue §2 | incorporated (consistent with, one tier richer than, the OS-PATROL variant's table) |
| TrafficMesh-specific data products (corridor risk, UBI, collision analysis, seasonal adjustment) | OS-PATROL Insurance Integration §1 | incorporated |
| UBI behavior-extraction methods and privacy constraint | OS-PATROL Insurance Integration §2 | incorporated |
| Premium discount tiers and ~25% maximum combined figure | OS-PATROL Insurance Integration §3 | incorporated |

## Unresolved tensions

None identified in this pass — all five documents state identical per-tier pricing, identical or non-
conflicting discount-tier percentages, and consistent privacy/consent constraints (individual data
available only for opted-in drivers, statistical summaries only, no geographic proxy discrimination)
wherever the same figures recur across documents.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/business-legal/CivicMesh/MKT-INS-001-Insurance-Partner-Pitch-Deck-Narrative-v1-docx.md`
- `knowledge-base/d-central/core/economics/CivicMesh/DC-CM-INS-001-Insurance-Integration-Specification-v1-docx.md`
- `knowledge-base/d-central/core/economics/CivicMesh/FIN-TM-001-TrafficMesh-Revenue-Model-v1-docx.md`
- `knowledge-base/d-central/core/economics/CivicMesh/MKT-INS-002-Insurance-Data-Product-Catalogue-v1-docx.md`
- `knowledge-base/d-central/core/economics/CivicMesh/OS-PATROL-TM-INS-001-TrafficMesh-Insurance-Integration-v1-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/business-legal/CivicMesh/MKT-INS-001-Insurance-Partner-Pitch-Deck-Narrative-v1-docx.md,
  knowledge-base/d-central/core/economics/CivicMesh/DC-CM-INS-001-Insurance-Integration-Specification-v1-docx.md,
  knowledge-base/d-central/core/economics/CivicMesh/FIN-TM-001-TrafficMesh-Revenue-Model-v1-docx.md,
  knowledge-base/d-central/core/economics/CivicMesh/MKT-INS-002-Insurance-Data-Product-Catalogue-v1-docx.md,
  knowledge-base/d-central/core/economics/CivicMesh/OS-PATROL-TM-INS-001-TrafficMesh-Insurance-Integration-v1-docx.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

*No cross-references detected to/from other docs/*.md files.*

<!-- AUTO-GENERATED RELATED END -->
