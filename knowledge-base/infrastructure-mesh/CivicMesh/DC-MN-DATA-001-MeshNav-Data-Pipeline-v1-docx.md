---
source_project: CivicMesh
source_project_uuid: 019e82f3-7ab2-715c-87c1-3e1074a12ab6
doc_uuid: 84f59bec-4081-45cb-b918-bead52765e1f
original_filename: DC-MN-DATA-001_MeshNav_Data_Pipeline_v1.docx
created_at: 2026-06-01T11:32:20.477554+00:00
content_hash: df9f9579b621
---

**D-Central Group  |  Confidential**	Section 2 — Legal & Corporate Structure

**DC-MN-DATA-001**

**D-CENTRAL GROUP**

**CivicMesh Inc. / TrafficMesh Technologies Inc.**

MeshNav Data Pipeline

| **Document ID** | DC-MN-DATA-001 |
| --- | --- |
| **Version** | 1.0 |
| **Status** | Draft |
| **Date** | May 2026 |
| **Author** | Toussaint Redji Jean Baptiste |
| **Classification** | Confidential — Technical |
| **SR****&****ED Eligibility** | Strong — novel fusion of city fleet enforcement data into navigation-quality road intelligence layer |
| **Related Documents** | DC-MN-ARCH-001 │ OS-PATROL-TM-TWIN-001 │ DC-CM-ARCH-001 |

# **1. Data Sources and Pipeline**

| **Source** | **Data Type** | **Update Frequency** | **Processing Required** |
| --- | --- | --- | --- |
| TrafficMesh node fleet | Road condition observations, violation events, GPS tracks, plow coverage, construction zone boundaries | Real-time continuous — every node pass | Spatial join to road segment, confidence update in digital twin, routing impact calculation |
| Digital Twin engine | Road condition index by segment, infrastructure asset status, defect locations | 24-hour maximum update cycle per segment (guaranteed) | Direct: twin output is nav layer input. Format conversion only. |
| OC Transpo GTFS-RT | Bus real-time positions, delay information, stop arrival predictions | 30-second updates | GTFS-RT → MeshNav transit overlay format conversion |
| City of Ottawa Open Data | Permanent road closures, construction permits, school zone designations, snow route activation schedule | Daily batch update from city open data portal | Geofence polygon construction, activation time rules |
| Contractor kit GPS | Active construction zone real-time boundary | 30-second update while kit is active | Dynamic geofence creation and update |
| MeshNav user reports | Manual hazard/incident reports from users (equivalent to Waze reports) | Real-time on submission | Confidence scoring by report count, age decay, plausibility check |

# **2. Road Condition Confidence Scoring**

| **Challenge** | A road segment observed once by a single node vehicle has low confidence. The same segment observed by 10 vehicles over 3 days has high confidence. Observations age differently for different data types (weather events degrade pavement observations faster than sign observations). |
| --- | --- |
| **Confidence Formula** | confidence(t) = base_confidence × decay_factor(t, asset_type) × observation_count_weight. Decay factor is asset-type-specific: pavement condition decays in 7 days; sign condition decays in 30 days; construction zone decays in 4 hours. |
| **Driver Display** | Segments with confidence <0.4 shown with 'unverified' indicator. Segments with confidence ≥0.8 shown with full confidence indicators. Plow coverage shown as binary (plowed in last 4 hours: yes/no) based on plow kit pass confirmation. |

# **3. Enforcement Zone Transparency Feature**

| **What It Shows** | Active CivicMesh enforcement nodes shown as 'Safety Zone' markers on MeshNav. Driver sees: zone type (school zone, construction zone, bus lane enforcement corridor), active hours, speed threshold. |
| --- | --- |
| **What It Does NOT Show** | Individual node vehicle location (privacy for city staff and contractors), node kit identifiers, or real-time evidence capture status. |
| **Deterrence Argument** | A driver who sees a Safety Zone on MeshNav slows down and complies — the enforcement zone transparency feature creates deterrence without requiring enforcement. This is the more socially beneficial outcome. Revenue from actual violations is a fallback, not the primary goal. |

# **Document Control**

| **Ver** | **Date** | **Author** | **Description** |
| --- | --- | --- | --- |
| 1.0 | May 2026 | Toussaint Redji Jean Baptiste | Initial release |

| Classification Notice — This document is CONFIDENTIAL and intended for internal use, legal counsel, and authorized personnel only. Distribution requires written authorization from Toussaint Redji Jean Baptiste. |
| --- |

	Toussaint Redji Jean Baptiste  |  D-Central Ecosystem  |  May 2026	Page  of