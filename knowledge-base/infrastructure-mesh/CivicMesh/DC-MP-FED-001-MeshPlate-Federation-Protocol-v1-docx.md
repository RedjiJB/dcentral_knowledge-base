---
source_project: CivicMesh
source_project_uuid: 019e82f3-7ab2-715c-87c1-3e1074a12ab6
doc_uuid: 2bc09a45-75a1-47f9-aeca-97048eb613e9
original_filename: DC-MP-FED-001_MeshPlate_Federation_Protocol_v1.docx
created_at: 2026-06-01T11:32:19.037533+00:00
content_hash: 5aec0bd01a42
---

**D-Central Group  |  Confidential**	Section 2 — Legal & Corporate Structure

**DC-MP-FED-001**

**D-CENTRAL GROUP**

**CivicMesh Inc. / TrafficMesh Technologies Inc.**

MeshPlate Federation Protocol

| **Document ID** | DC-MP-FED-001 |
| --- | --- |
| **Version** | 1.0 |
| **Status** | Draft |
| **Date** | May 2026 |
| **Author** | Toussaint Redji Jean Baptiste |
| **Classification** | Confidential — Technical |
| **SR****&****ED Eligibility** | Moderate — novel hash-based cross-community query protocol |
| **Related Documents** | DC-MP-ARCH-001 │ DC-CM-FED-001 │ REG-MP-001 │ LEGAL-CM-011 |

# **1. Standard LPR Federation (Community → Municipal)**

| **What Federates Automatically** | Plates of vehicles confirmed as violating a city bylaw (snow route, accessible parking) — confirmed citation evidence packages only. These are treated identically to TrafficMesh enforcement evidence. |
| --- | --- |
| **What Does NOT Federate Automatically** | Trusted vehicle registry (resident plates — never shared), visitor log raw data (entry/exit records for private communities), or any plate read not associated with a confirmed violation. |
| **Municipal LPR Integration** | If a municipal partner operates their own ALPR network (e.g. Ottawa Police cruiser ALPR), MeshPlate can federate anonymised violation data (hash + timestamp + GPS) to supplement the municipal network. No plaintext plates in automatic federation. |

# **2. Investigation-Specific Cross-Community Query**

- Requesting officer submits: specific plate (plaintext), case number, legal authority (WARRANT required for historical cross-community queries), time window, justification

- Platform hashes the submitted plate using each relevant community's salt

- Hash query executed against each community's MeshPlate event records — returns matching event records (timestamp, GPS, clip hash) without exposing the community's plate database

- Match results assembled into evidence package with chain of custody: which community, which node, which timestamp, confidence score

- Request logged to public audit trail: case number (visible), plate (not visible), communities queried (aggregate count only), results found (count only)

- Each queried community manager notified: '[Count] plate query executed against your community's MeshPlate records. Reference: [case number]. [Match found / No match] — specific plate not disclosed per privacy protocol.'

- Post-case purge: all plaintext plate data derived from the query purged from investigative access within 30 days of case closure

# **3. No-Data-Broker Covenant**

| **The Covenant** | MeshPlate data — whether hashed or plaintext — will never be sold to, shared with, or accessed by any commercial data broker, insurance data aggregator (other than direct insurer relationships under LEGAL-CM-014), immigration enforcement agency, or political campaign. |
| --- | --- |
| **Technical Enforcement** | The covenant is enforced at the API level: MeshPlate query API endpoints are accessible only to: (a) municipal law enforcement with active federation agreements, (b) community managers for their own community's data, (c) CCSC members for their own vehicle's data. No bulk export API exists. |
| **Open Source Guarantee** | The no-data-broker covenant is written into the AGPL v3 Community Edition licence terms. Any deployment of MeshPlate must comply with the covenant or they are in breach of the licence. |

# **Document Control**

| **Ver** | **Date** | **Author** | **Description** |
| --- | --- | --- | --- |
| 1.0 | May 2026 | Toussaint Redji Jean Baptiste | Initial release |

| Classification Notice — This document is CONFIDENTIAL and intended for internal use, legal counsel, and authorized personnel only. Distribution requires written authorization from Toussaint Redji Jean Baptiste. |
| --- |

	Toussaint Redji Jean Baptiste  |  D-Central Ecosystem  |  May 2026	Page  of