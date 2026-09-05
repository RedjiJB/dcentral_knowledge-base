# DC-IHOSE-USE-CASES-RECONCILED-001 — OpenVision Use Cases & Business Models, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `ihose-use-cases-business-models` (2 docs).

## Current understanding

Two marketing/business-case documents for the same OpenVision Platform, aimed at different framings of
the same core pitch: 07-Use-Cases-Integration argues per-vertical operational ROI (why deploying
OpenVision pays for itself); 08-Ecosystem-Business-Models argues a second-order business-model
transformation (why a deploying organization can then become a consultant to its industry peers). Where
the two overlap (transit authority figures), they match exactly — a consistency check, not a
duplication concern, since 08-Ecosystem explicitly builds its transit case study on top of 07's numbers.

**Per-vertical use cases and ROI (incorporated, from 07-Use-Cases-Integration):** covers 7 verticals
(Public Transportation, Smart Retail, Manufacturing, Healthcare, Smart Buildings, Critical Infrastructure,
Education) plus an implementation framework. Worked examples with concrete before/after figures include:
dynamic bus scheduling ($400K investment, $730K annual benefit, 183% ROI), onboard bus analytics/fare-
evasion detection ($1.2M investment, $4.75M annual benefit via $2.8M recovered fare evasion + route
optimization, 296% ROI), and multi-modal hub integration ($2.1M investment, $2.44M annual benefit).
Combined transit-authority total: **$3.7M investment → $7.92M/year, 214% ROI, $35.9M 5-year net
benefit** [§Public Transportation Systems]. Retail customer-flow/heat-mapping analysis claims a 15%
sales increase from data-driven product placement, for a $45K investment against $1.14M annual benefit
(2,533% ROI) [§Smart Retail Operations].

**Business-model transformation (incorporated, from 08-Ecosystem-Business-Models):** argues that
OpenVision's Apache 2.0 license (vs. proprietary vendor lock-in) lets a deploying organization become a
paid consultant to its industry peers, creating a second revenue stream on top of the operational ROI
[§The Ecosystem Business Model]. The transit-authority case study is explicitly built as a sequel to
07's figures: same $3.7M initial investment and $7.92M/year operational benefit, plus a 3-phase
consulting-business launch reaching $10.5M cumulative 3-year consulting profit, for a **combined 968%
4-year ROI and $42.2M total 4-year return** [§Transit Authority as Consultant]. Parallel consulting
transformations are argued for security companies (12-15% traditional margin → 40-60% margin business,
with a named case study claiming +89% revenue/+494% profit over 3 years) [§Security Company
Transformation], construction ($7.48M investment, $23.94M annual benefit across safety/progress-
tracking/theft-prevention/subcontractor-management use cases, 320% blended ROI) [§Construction Industry
Innovation], and property management ($250K investment, $459.75K-484.75K annual benefit across parking/
security/amenity optimization) [§Property Management & Parking]. A closing partner-ecosystem strategy
names three partner types (deployment, consulting, technology partners) and a 4-step path for any
deploying organization to build its own consulting business [§Partner Ecosystem Strategy].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Transit authority per-use-case ROI (bus scheduling, onboard analytics, hub integration) | 07-Use-Cases §Public Transportation Systems | incorporated |
| Transit authority combined total ($3.7M→$7.92M/yr, 214% ROI) | 07-Use-Cases §Total Transportation System ROI | incorporated (independently confirmed by 08-Ecosystem's identical figures) |
| Retail customer-flow/heat-mapping ROI | 07-Use-Cases §Smart Retail Operations | incorporated |
| Ecosystem business-model concept (open-source enables consulting, proprietary systems don't) | 08-Ecosystem §The Ecosystem Business Model | incorporated |
| Transit-authority-as-consultant combined 4-year ROI (968%, $42.2M) | 08-Ecosystem §Transit Authority as Consultant | incorporated (explicitly built on 07's transit figures) |
| Security company transformation model and case study | 08-Ecosystem §Security Company Transformation | incorporated |
| Construction industry use cases and total ROI | 08-Ecosystem §Construction Industry Innovation | incorporated |
| Property management use cases and total ROI | 08-Ecosystem §Property Management & Parking | incorporated |
| Partner ecosystem strategy and consulting-business playbook | 08-Ecosystem §Partner Ecosystem Strategy | incorporated |

## Unresolved tensions

None identified in this pass — the one directly overlapping figure set (transit authority operational
ROI) matches exactly between the two documents, and 08-Ecosystem explicitly frames its transit case
study as continuing from 07's numbers rather than restating them independently. Note (not a cross-doc
conflict, but worth flagging for anyone using these figures): every ROI number across both documents is
a marketing projection with no cited independent verification or named real-world deployment — these
read as an illustrative sales case, not audited outcomes.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/business-legal/IHOSE/08-Ecosystem-Business-Models-md.md`
- `knowledge-base/d-central/security/IHOSE/07-Use-Cases-Integration-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/business-legal/IHOSE/08-Ecosystem-Business-Models-md.md,
  knowledge-base/d-central/security/IHOSE/07-Use-Cases-Integration-md.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

Neither source doc is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
