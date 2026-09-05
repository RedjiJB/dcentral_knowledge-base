# DC-CM-COMMERCIAL-B2B-VEHICLE-FLEET-RECONCILED-001 — CivicMesh Commercial Vehicle Network (B2B Fleet) Programme, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `commercial-b2b-vehicle-fleet-programme` (5 docs).

## Current understanding

Five documents specifying CivicMesh's Tier 4 B2B commercial-vehicle-network (CVN) programme — the
strategic architecture, two of its four agreement-model templates, the technical API integration
layer, and the Commercial Driver Verifiable Credential schema. All five are tightly cross-referencing
and mutually consistent on revenue splits, privacy scoping, and technical mechanisms.

**CVN Programme strategic architecture (incorporated):** extends the node network via four commercial
fleet types (rideshare, rental/car-share, delivery, taxi/licensed operator), arguing commercial
agreements build density in "step changes" (one Enterprise contract = 800-1,200 nodes) versus civilian
opt-in's gradual growth [§1]. Four agreement models each with distinct revenue splits: Model A Fleet
Owner (rental/car-share) 50%/20%/25%/5% (municipality/CivicMesh/fleet/CCSC); Model B Platform Driver
(Uber/Lyft) 50%/20%/22%+3%/5% (driver gets 22%, platform 3%); Model C Delivery Network 55%/20%/20%/5%
(higher municipal share reflecting digital-twin value); Model D Taxi/Licensed Operator 50%/20%/25%/5%
[§2, §4.1]. A technical architecture section defines the per-partner API integration table, the
Commercial Driver Credential field schema, and evidence-package context-enrichment fields
(commercial_tier, platform, on_trip, vehicle_type, route_zone, driver_credential_hash) gated entirely
on explicit driver consent [§3]. A phased go-to-market sequence (Communauto/Enterprise first, delivery
networks second, Uber/Lyft last, reasoning that rideshare is the largest but most legally complex
opportunity) [§5], a privacy-risk/mitigation table per commercial participant type [§6], worker-
protection mechanisms (driver-controlled opt-in, revenue paid directly to driver not employer, no-
adverse-use covenant, CCSC cooperative membership) [§7], and a network-effect projection showing CVN
scaling Ottawa from ~2,000 to ~12,000 nodes by Year 3 versus city-fleet-only growth [§9].

**Fleet Operator Agreement Template — Model A (incorporated):** the legal template for company-owned
fleets (Enterprise, Hertz, Communauto, Zipcar, Turo). Fleet operator obligations (90-day installation
window, 24-hour failure reporting, no renter-identity linkage, no adverse use, monthly roster
reporting) with named consequences of breach [§1]. A revenue/fee table matching the strategic
document's Model A split exactly (fleet operator receives 25% of net citation revenue), plus non-
citation fees (at-cost hardware, per-vehicle installation fee, monthly NOC management fee, negotiated
insurance premium reduction, 5-10% digital-twin data revenue share) [§2]. Data governance clarifies
citation evidence belongs to the municipality, aggregate safety metrics belong to the fleet operator,
and renter identity is never collected [§3]. Insurance facilitation is explicitly a no-guarantee
introduction service, not a guaranteed discount [§4].

**Platform Driver Programme Specification — Model B (incorporated):** the Uber/Lyft-specific
two-component structure — a company-level Platform API Agreement plus an individual, voluntary Driver
Opt-In Programme — explicitly framed as "a driver benefit programme that Uber enables, not a driver
monitoring programme that Uber operates" [Executive Summary]. A permitted/prohibited-use table per API
capability (trip status, driver DID mapping, revenue routing, insurance data feed), each with a named
technical implementation constraint [§1]. A driver-benefits table matching the strategic document's
$450-750/year insurance-reduction and $800-2,400/year citation-revenue estimates exactly [§2.1], an
8-step opt-in process, and five named "cannot be waived" anti-surveillance driver protections (voluntary
opt-in, revenue flows directly to driver, no workforce-management use, opt-out anytime with no penalty,
CCSC membership independent of the Uber relationship) [§2.3]. A pitch-strategy section naming the
correct Uber entry point (driver-experience/earnings team, not legal/policy first) and anticipated
legal objections with prepared answers [§3].

**Commercial Platform API Integration Specification (incorporated):** the technical middleware — a
Platform Webhook Receiver (HMAC-verified per platform), a Redis-cached Context Enrichment Service
(60-second TTL, no PII), a Credential Lifecycle Manager (Veramo SDK + Polygon), a Revenue Attribution
Engine (patronage-wallet-DID routing only), and a Scope Enforcement Gateway that makes out-of-scope
data flows technically impossible rather than merely policy-prohibited [§1]. Detailed inbound/outbound
event tables for Uber/Lyft (trip events, revenue batches, insurer-only safety scores), Enterprise
(vehicle roster, checkout/return events, coverage reports), and delivery networks (route assignment,
completion events, per-incident liability-documentation retrieval) [§2-4]. An SR&ED technical
uncertainty register flagging three open engineering questions: trip-context enrichment latency
race conditions, multi-platform driver revenue attribution, and 60-second credential-revocation
propagation under Polygon network congestion [§5].

**Commercial Driver Verifiable Credential Schema (incorporated):** the CDVC's defining design choice —
issued by the *platform's* DID (Uber Canada, Lyft Canada), not by D-Central Group or CCSC, making it
platform-portable and platform-revocable while remaining cryptographically distinct from the civilian
CCSC membership credential [Executive Summary]. A full W3C VC JSON schema matching the strategic
document's field list exactly (platform, driverStatus, vehicleDIDs, revenueShareRecipient,
insuranceDataShareConsent, insurerDID, tripContextConsent, citationRevenueOptIn) [§1]. A field-by-field
privacy analysis confirming no field carries reversible PII [§2]. A lifecycle section confirming that
platform-driven revocation (e.g., Uber deactivating a driver) does not affect the driver's underlying
CCSC membership or accumulated patronage — consistent with the strategic document's and the Driver
Programme Specification's worker-protection claims [§3]. Multi-platform drivers hold one CDVC per
platform, both linked to the same personal DID [§3-4].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| CVN strategic rationale, density economics, four fleet-type contributions | Programme doc §1 | incorporated |
| Four agreement models and their revenue splits | Programme doc §2, §4.1 | incorporated (splits match exactly across the Model A and Model B template documents) |
| Technical architecture overview (API table, credential schema, context enrichment) | Programme doc §3 | incorporated (consistent with the detailed API Integration Spec and CDVC Schema documents) |
| Go-to-market sequencing and Uber pitch framing | Programme doc §5 | incorporated (consistent with the Driver Programme Specification's own pitch-strategy section) |
| Privacy risk/mitigation table and worker-protection mechanisms | Programme doc §6-7 | incorporated |
| Network-effect node-count projection | Programme doc §9 | incorporated |
| Fleet operator obligations, revenue/fee structure, data governance | Fleet Operator Agreement Template, §1-3 | incorporated (revenue split matches Programme doc's Model A table exactly) |
| Insurance facilitation (no-guarantee introduction service) | Fleet Operator Agreement Template, §4 | incorporated |
| Platform API Agreement scope (permitted/prohibited uses) | Platform Driver Programme Spec, §1 | incorporated |
| Driver benefits, opt-in process, anti-surveillance protections | Platform Driver Programme Spec, §2 | incorporated (dollar figures match Programme doc §5.2 exactly) |
| Uber pitch strategy and anticipated legal objections | Platform Driver Programme Spec, §3 | incorporated |
| Integration layer architecture (webhook receiver, context cache, credential manager, revenue engine, scope gateway) | API Integration Spec, §1 | incorporated |
| Per-partner inbound/outbound event specifications | API Integration Spec, §2-4 | incorporated |
| SR&ED technical uncertainty register | API Integration Spec, §5 | incorporated |
| CDVC platform-issued design and full schema | CDVC Schema, Executive Summary, §1 | incorporated (schema fields match Programme doc §3.2's credential field table exactly) |
| Field-by-field privacy analysis | CDVC Schema, §2 | incorporated |
| Credential lifecycle and multi-platform driver handling | CDVC Schema, §3-4 | incorporated (consistent with worker-protection claims in the Programme doc and Driver Programme Spec) |

## Unresolved tensions

None identified in this pass — all five documents describe one consistent CVN programme design, with
revenue-split figures, driver-benefit dollar estimates, credential schema fields, and worker-protection
guarantees matching exactly everywhere they recur across documents.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/business-legal/CivicMesh/DC-CM-B2B-001-Commercial-Vehicle-Network-Programme-v1-docx.md`
- `knowledge-base/d-central/business-legal/CivicMesh/DC-CM-B2B-002-Fleet-Operator-Agreement-Template-v1-docx.md`
- `knowledge-base/d-central/business-legal/CivicMesh/DC-CM-B2B-003-Platform-Driver-Programme-Specification-v1-docx.md`
- `knowledge-base/d-central/core/identity/CivicMesh/DC-CM-B2B-005-Commercial-Driver-VC-Schema-v1-docx.md`
- `knowledge-base/d-central/core/identity/CivicMesh/DC-CM-B2B-006-Commercial-Platform-API-Integration-Spec-v1-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/business-legal/CivicMesh/DC-CM-B2B-001-Commercial-Vehicle-Network-Programme-v1-docx.md,
  knowledge-base/d-central/business-legal/CivicMesh/DC-CM-B2B-002-Fleet-Operator-Agreement-Template-v1-docx.md,
  knowledge-base/d-central/business-legal/CivicMesh/DC-CM-B2B-003-Platform-Driver-Programme-Specification-v1-docx.md,
  knowledge-base/d-central/core/identity/CivicMesh/DC-CM-B2B-005-Commercial-Driver-VC-Schema-v1-docx.md,
  knowledge-base/d-central/core/identity/CivicMesh/DC-CM-B2B-006-Commercial-Platform-API-Integration-Spec-v1-docx.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
