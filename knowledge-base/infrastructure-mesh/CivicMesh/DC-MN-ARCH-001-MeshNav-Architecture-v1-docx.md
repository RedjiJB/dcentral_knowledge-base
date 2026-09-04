---
source_project: CivicMesh
source_project_uuid: 019e82f3-7ab2-715c-87c1-3e1074a12ab6
doc_uuid: 4652a9fb-cd88-4fe2-82d5-9a2ede098f74
original_filename: DC-MN-ARCH-001_MeshNav_Architecture_v1.docx
created_at: 2026-06-01T11:32:21.854234+00:00
content_hash: bd09238d65a2topic: condition-coverage-continuous
---

**D-Central Group  |  Confidential**	Section 2 — Legal & Corporate Structure

**DC-MN-ARCH-001**

**D-CENTRAL GROUP**

**CivicMesh Inc.**

MeshNav Architecture — Navigation Platform

| **Document ID** | DC-MN-ARCH-001 |
| --- | --- |
| **Version** | 1.0 |
| **Status** | Draft — SR&ED: strong |
| **Date** | May 2026 |
| **Author** | Toussaint Redji Jean Baptiste |
| **Classification** | Confidential — Technical |
| **SR****&****ED Eligibility** | Strong — novel road intelligence data fusion pipeline from city fleet node network for navigation |
| **Related Documents** | DC-MN-DATA-001 │ OS-PATROL-TM-TWIN-001 │ DC-CM-ARCH-001 │ MKT-MN-001 |

| **Executive Summary** MeshNav is a navigation platform built on TrafficMesh's road intelligence data layer. The key competitive differentiation from Waze: TrafficMesh generates 24/7 road condition data from scheduled city fleet operations regardless of civilian traffic volume. At 3am — when Waze has almost no data — Ottawa's plows are running, and MeshNav has current road condition data for every street they've covered. The platform is not just a Waze clone with better data: it has features that are structurally impossible for Waze to offer (enforcement zone transparency, digital twin road conditions, guaranteed overnight coverage). |
| --- |

# **1. Data Sources and Superiority Over Waze**

| **Data Category** | **Waze** | **MeshNav** | **MeshNav Advantage** |
| --- | --- | --- | --- |
| Road condition data | Crowdsourced user reports — random coverage, no data at low traffic times | City fleet node observations — systematic coverage, 24/7 including overnight | Superior at night and weekends when Waze has sparse data |
| Pothole/defect locations | User manual reports — reactive, often delayed | Digital twin continuous update — detected by plow/sweeper passes, often within hours of formation | Proactive detection vs reactive reporting |
| Construction zones | User reports — often inaccurate or stale | Contractor kit GPS — real-time boundary with sub-30-second update | Real-time vs stale |
| Enforcement zone alerts | Police reports (vague) | Active node locations with enforcement type — school zone timing, construction zone speed, bylaw patrol corridors | Specific and time-accurate vs vague |
| Winter road status | User reports | Plow pass confirmation — real-time coverage map | Authoritative vs crowdsourced |
| Transit integration | Basic transit display | OC Transpo real-time positions from node fleet + platform data | Integrated vs superficial |

# **2. Features Waze Cannot Build**

| **Feature** | **Why Waze Cannot Offer It** | **MeshNav Implementation** |
| --- | --- | --- |
| Enforcement zone transparency | Waze shows police sightings (user-reported) but cannot show the enforcement network's own node locations — it doesn't have the data | Active CivicMesh node positions shown on map as 'Safety Zone' — driver knows enforcement is nearby. Deterrence effect. Complements enforcement rather than helping violators avoid it. |
| Road condition confidence score | Waze doesn't have systematic road condition data — only spot reports from drivers | Each road segment in MeshNav shows last-observed condition with confidence score from digital twin. Drivers can see pavement quality before choosing a route. |
| Plow coverage live map | Waze has no relationship with city plow operations | During snow events, MeshNav shows which streets have been plowed in the last 4 hours based on plow kit GPS tracks. First-in-market feature for Ottawa winter driving. |
| Cooperative data ownership | Waze data is owned by Google. Contributors receive nothing. | MeshNav contributors (opted-in node owners, manual reporters) earn D-Credit for verified contributions. Data is cooperative-owned. |

# **3. Revenue and Sustainability Model**

| **Free Tier** | All navigation features free for all users. Funded by the municipal data agreement — cities pay for the road intelligence layer, which subsidizes the navigation product. |
| --- | --- |
| **Premium Fleet Tier** | $[TBD]/month per vehicle for commercial fleets. Includes: enhanced road condition data (raw digital twin access), API access, priority plow coverage alerts, construction zone advance notification. Target: logistics companies, taxi and rideshare operators, delivery fleets. |
| **Insurance Integration** | Opted-in drivers who share their driving data with their insurer receive premium reductions. MeshNav is the data collection interface — the app that both navigates and (with consent) records the driving session for insurance purposes. |
| **No Advertising** | MeshNav is explicitly ad-free. Funded by municipal agreements and fleet subscriptions. This is a marketing differentiator and a cooperative principle. |

# **4. Document Control**

| **Ver** | **Date** | **Author** | **Description** |
| --- | --- | --- | --- |
| 1.0 | May 2026 | Toussaint Redji Jean Baptiste | Initial release |

| Classification Notice — This document is CONFIDENTIAL and intended for internal use, legal counsel, and authorized personnel only. Distribution requires written authorization from Toussaint Redji Jean Baptiste. |
| --- |

	Toussaint Redji Jean Baptiste  |  D-Central Ecosystem  |  May 2026	Page  of