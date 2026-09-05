# DC-IHOSE-BUSINESS-STRATEGY-RECONCILED-001 — OpenVision (IHOSE) Business Strategy Documents, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `ihose-business-strategy-documents` (4 docs).

## Current understanding

Four business-facing OpenVision Platform documents spanning execution (an 18-month implementation
roadmap), go-to-market strategy (a consulting/ecosystem business-model thesis), investor communication
(a board/investor presentation deck), and internal quality review (a documentation-improvement
memo). Two of the four (Ecosystem Business Models, Improvement Recommendations) also carry a second
`topic:` tag for other confirmed clusters and are detailed there for that other content; this
consolidation covers their business-strategy content in full.

**Implementation Roadmap (incorporated):** a detailed 5-phase, 18-month project plan for a 500-camera/
20-site enterprise deployment — Foundation (months 1-3, team hiring/procurement), Development & MVP
(months 4-6, core platform + security audit), Pilot Deployment (months 7-9, 3 sites/75 cameras),
Production Rollout (months 10-12, remaining 17 sites/425 cameras), Optimization & Expansion (months
13-18) [Phase Breakdown]. A detailed project budget totals **$1,691,140** — team $1,112,500 (67%,
including a 5-7 person core team plus installation technicians/training/security consultant),
hardware $397,110 (24%), software/services $101,000 (6%), 5% contingency [Resource Requirements]. Six
named risks (hardware delays, skill gaps, integration complexity, performance at scale, security
vulnerabilities, budget overrun) each carry probability/impact/mitigation/contingency [Risk
Management]. Technical, business, and operational KPI targets (99.9% availability, <500ms video
latency, 30% cost savings vs. commercial, <2hr MTTR) and a full go-live/documentation/business-
readiness checklist close the plan [Success Metrics, Go-Live Checklist].

**Ecosystem Business Models (incorporated, business-strategy portion):** argues OpenVision's open
license (Apache 2.0) lets any deploying organization become a paid consultant to industry peers,
unlike proprietary systems. A worked transit-authority case study shows $3.7M internal deployment
(214% ROI, $7.92M/yr) plus a productized consulting business scaling from $1.315M revenue (Year 2) to
$11.1M revenue (Year 4), for a combined 968% 4-year ROI [Transit Authority as Consultant]. Three more
worked verticals — security-company transformation (12% → 26-31% net margin via managed-analytics
SaaS), construction (safety/progress/theft/subcontractor-tracking use cases totaling $23.94M annual
benefit on $7.48M investment, 320% ROI), and property management/parking (184-194% ROI across
parking/security/amenity optimization) — each end with the same "become a consultant" secondary
business model [Security Company Transformation, Construction Industry Innovation, Property Management
& Parking]. A four-step generic "creating your consulting business" playbook and a three-tier partner
ecosystem (deployment/consulting/technology partners) close the document [Partner Ecosystem Strategy].

**Business Presentation Deck (incorporated):** a 21-slide investor/board deck. Slide 4's 3-year TCO
table gives OpenVision at **$774,430** vs. commercial **$1,120,000** (**31%** savings, an 18-24 month
payback) [Slide 4]. A $62B global market sized across four segments, a go-to-market plan (enterprise
direct → channel expansion → SaaS scale), 3-year financial projections (Year 1 net -$66K, Year 3 net
+$3.4M, break-even month 14), an $800K seed ask with use-of-funds breakdown, and an exit-strategy slide
(strategic acquisition $50-200M, financial buyer $100-500M, IPO path at $50M+ ARR) [Slides 5-19]. An
appendix gives a five-revenue-stream model (professional services, managed services, SaaS multi-
tenant, support subscriptions, module marketplace) and objection-handling scripts [Appendix].

**Improvement Recommendations (incorporated, business-strategy portion):** a documentation self-review
recommending more visual storytelling, deeper financial modeling (sensitivity analysis, Monte Carlo),
stronger third-party proof points, implementation tools (calculators, decision frameworks), risk
quantification, and vertical-specific depth [Executive Summary, §1]. Its own worked example of a
"visual ROI comparison chart" states OpenVision's 3-year TCO as **$819K** against Genetec ($1,015K),
Milestone ($925K), and Verkada ($1,200K) [§1.A].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| 5-phase 18-month implementation plan and $1.69M project budget | Implementation Roadmap, Phase Breakdown / Resource Requirements | incorporated |
| Risk register and KPI targets | Implementation Roadmap, Risk Management / Success Metrics | incorporated |
| Ecosystem/consulting business-model thesis and 4 worked verticals | Ecosystem Business Models | incorporated |
| Partner ecosystem strategy | Ecosystem Business Models, Partner Ecosystem Strategy | incorporated |
| Investor deck: problem/solution/market/competitive slides | Business Presentation Deck, Slides 1-7, 13 | incorporated |
| Investor deck: TCO table, business models, GTM, financial projections, seed ask, exit strategy | Business Presentation Deck, Slides 4, 9-12, 19 | incorporated — see tension below re: TCO figure |
| Documentation-improvement recommendations | Improvement Recommendations, Executive Summary / §1 | incorporated |
| Worked TCO comparison chart example | Improvement Recommendations §1.A | incorporated — see tension below |

## Unresolved tensions

**Three of this topic's documents each state a different OpenVision 3-year TCO figure for the same
500-camera deployment, with no cross-reference reconciling them.** The Business Presentation Deck's
own Slide 4 table computes OpenVision at $774,430 (vs. $1,120,000 commercial, 31% savings). The
Improvement Recommendations doc's worked example chart states $819K (vs. Genetec $1,015K). The sibling
consolidation [DC-IHOSE-QUICKSTART-RECONCILED-001](DC-IHOSE-QUICKSTART-RECONCILED-001.md) documents a
third figure, $819,430 vs. $890,000 commercial (a ~8% savings figure), from the QUICK-START.md doc.
Attempted reconciliation: the Improvement Recommendations and QUICKSTART figures agree closely ($819K
vs. $819,430) and could plausibly be the same underlying calculation, but the Business Presentation
Deck's $774,430 doesn't match either, and none of the three documents states which one supersedes the
others or explains the difference in commercial-comparison baseline ($1,120,000 vs. $890,000 vs.
$1,015,000 for the same competitor category). Left unresolved rather than picking one as authoritative.

**The Business Presentation Deck contains an internal inconsistency between its own slides.** Slide 1's
headline claims "70% Cost Savings," and this "70%" figure recurs on Slide 13 ("70% cost savings, equal
features") and in the closing Presentation Tips ("70% savings over 3 years vs. commercial solutions").
But Slide 4's own cost table computes the savings as $345,570 / $1,120,000 = 30.8%, not 70%. Attempted
reconciliation: none — this reads as a marketing headline figure that was never updated to match the
deck's own detailed cost table, rather than a different (and unstated) basis of comparison.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/business-legal/IHOSE/06-Implementation-Roadmap-md.md`
- `knowledge-base/d-central/business-legal/IHOSE/08-Ecosystem-Business-Models-md.md`
- `knowledge-base/d-central/business-legal/IHOSE/BUSINESS-PRESENTATION-md.md`
- `knowledge-base/d-central/business-legal/IHOSE/IMPROVEMENT-RECOMMENDATIONS-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/business-legal/IHOSE/06-Implementation-Roadmap-md.md,
  knowledge-base/d-central/business-legal/IHOSE/08-Ecosystem-Business-Models-md.md,
  knowledge-base/d-central/business-legal/IHOSE/BUSINESS-PRESENTATION-md.md,
  knowledge-base/d-central/business-legal/IHOSE/IMPROVEMENT-RECOMMENDATIONS-md.md,
]
reconciled_against: [DC-IHOSE-QUICKSTART-RECONCILED-001.md (surfaces a third, partially-matching TCO figure)]
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
