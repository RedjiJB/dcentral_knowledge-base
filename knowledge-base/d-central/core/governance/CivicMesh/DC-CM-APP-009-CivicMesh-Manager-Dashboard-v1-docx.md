---
source_project: CivicMesh
source_project_uuid: 019e82f3-7ab2-715c-87c1-3e1074a12ab6
doc_uuid: 51b4b1e1-6a8c-4839-b71a-a40ad611fdc9
original_filename: DC-CM-APP-009_CivicMesh_Manager_Dashboard_v1.docx
created_at: 2026-06-01T11:32:20.310339+00:00
content_hash: 30505e33dfb2
topic: "civicmesh-noc-manager-dashboard-specifications"
---

**D-Central Group  |  Confidential**	Section 2 — Legal & Corporate Structure

**DC-CM-APP-009**

**D-CENTRAL GROUP**

**CivicMesh Inc.**

CivicMesh Manager Dashboard — Product Specification

| **Document ID** | DC-CM-APP-009 |
| --- | --- |
| **Version** | 1.0 |
| **Status** | Draft |
| **Date** | May 2026 |
| **Author** | Toussaint Redji Jean Baptiste |
| **Classification** | Confidential — Technical |
| **Primary Audience** | HOA boards, condo property managers, campus security managers, business park operators |
| **Platform** | Web — desktop and tablet |
| **Related Documents** | DC-CM-APP-001 │ DC-CM-ARCH-001 |

# **1. Purpose**

Community safety management platform for non-technical community managers. All platform complexity is hidden. What the manager sees: are my nodes working, what happened today, how much revenue was generated, and was my data accessed by anyone. Nothing more complex than this on the main screen.

# **2. Primary Sections**

| **Section** | **Description** |
| --- | --- |
| Community Overview | Node coverage map (public-facing version available for community bulletin board). Incident volume this week/month. Active alerts needing manager attention. Revenue summary (fines collected, fees paid, net to community, CCSC distributions to node owners this month). |
| Incident Queue | Evidence packages requiring community manager review for private property enforcement. Clip player with one-tap confirm/dismiss. Resident notification workflow (auto-draft notification to violating vehicle owner where registered in community member directory). All decisions logged with manager DID. |
| Member Management | Node owner registry: name, DID, consent status, active nodes, patronage earned this year. CCSC membership status. Annual meeting attendance and voting record. Onboarding workflow for new node owners. |
| Law Enforcement Access Log | Every law enforcement data request visible to community manager: date, legal authority type, data type requested, status (approved/denied), community notification sent. Full detail — no redactions for community manager view. |
| Transparency Report | One-click generate annual transparency report for community distribution. Pre-filled from audit log data. Manager reviews before publishing. Download as PDF for distribution at AGM. |
| Privacy Complaints | Receive member complaints, log resolution steps, track open/closed status. Export complaint log for annual report. |

# **3. Public Node Map**

| **Purpose** | Every community with CivicMesh must publish a map of their active node locations. This is a CCSC bylaws and municipal transparency requirement — not optional. |
| --- | --- |
| **Content** | Node locations (GPS coordinates rounded to nearest 10m for privacy of exact installation address), node type (camera, LPR, acoustic), status (active/inactive) |
| **Access** | Public URL: community.civicmesh.ca/{community-id}/nodes — no login required. QR code for community bulletin board. |

# **Document Control**

| **Ver** | **Date** | **Author** | **Description** |
| --- | --- | --- | --- |
| 1.0 | May 2026 | Toussaint Redji Jean Baptiste | Initial release |

| Classification Notice — This document is CONFIDENTIAL and intended for internal use, legal counsel, and authorized personnel only. Distribution requires written authorization from Toussaint Redji Jean Baptiste. |
| --- |

	Toussaint Redji Jean Baptiste  |  D-Central Ecosystem  |  May 2026	Page  of