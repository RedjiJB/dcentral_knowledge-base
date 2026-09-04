---
source_project: CivicMesh
source_project_uuid: 019e82f3-7ab2-715c-87c1-3e1074a12ab6
doc_uuid: 2b70c79e-dc14-47dc-975e-0e412f2989c1
original_filename: DC-CM-APP-008_CivicMesh_Officer_Portal_v1.docx
created_at: 2026-06-01T11:32:19.270638+00:00
content_hash: 0ce03c0cb9d5
---

**D-Central Group  |  Confidential**	Section 2 — Legal & Corporate Structure

**DC-CM-APP-008**

**D-CENTRAL GROUP**

**CivicMesh Inc.**

CivicMesh Officer Portal — Product Specification

| **Document ID** | DC-CM-APP-008 |
| --- | --- |
| **Version** | 1.0 |
| **Status** | Draft |
| **Date** | May 2026 |
| **Author** | Toussaint Redji Jean Baptiste |
| **Classification** | Confidential — Technical |
| **Primary Audience** | Municipal bylaw officers, OC Transpo enforcement, authorized municipal personnel |
| **Platform** | Web — desktop-first, tablet-compatible for field use |
| **Related Documents** | DC-CM-APP-001 │ DC-CM-ARCH-001 |

# **1. Purpose and Legal Design Constraint**

Legal admissibility is the primary design constraint. Every officer action — view time, review decision, dismissal reason, DID signature timestamp — is logged immutably. The portal technically enforces the human review requirement: citation issuance is blocked without an officer DID signature. It is architecturally impossible to issue a citation without a human officer reviewing the evidence.

# **2. Evidence Queue Design**

| **Queue Type** | **Entry Criteria** | **Minimum Officer Action Before Confirm** |
| --- | --- | --- |
| Fast-Track Queue | Confidence ≥ 0.90 AND ALPR confidence ≥ 0.95 | Video must play for minimum 3 seconds (enforced by timer lock on Confirm button). One-tap confirm with pre-filled citation draft. |
| Standard Review Queue | Confidence 0.70–0.89 OR ALPR 0.70–0.94 | Officer must: (1) watch full clip, (2) manually confirm violation type from dropdown, (3) confirm or correct plate read, (4) add review notes (optional but encouraged). Confirm available only after all steps. |
| Manual Review Queue | Flagged by MSSP NOC for unusual circumstances, or referred from Fast-Track if officer has concerns | Full review required + mandatory review notes. Supervisor countersignature for any citation in this queue. |

# **3. Credential Verification Display**

| **Chain Status Badge** | Every evidence package displays a badge: GREEN (full chain verified on Polygon), AMBER (chain valid but credential expiring within 30 days), RED (verification failed — package excluded from enforcement queue) |
| --- | --- |
| **Verification Detail** | Officer taps badge to see: node DID, manufacturer credential status, installer credential (technician name, certification level, installation date), MSSP operator credential status, firmware version and hash |
| **Public Verifiability** | 'Verify independently' button opens verify.civicmesh.ca/{package-id} in new tab — defence counsel can verify the same chain from any device without logging in |

# **4. Citation Workflow**

| **Step** | **Action** | **System Behaviour** |
| --- | --- | --- |
| 1 | Officer DID signature on confirmed package | Signature recorded with timestamp to audit log. Citation issuance unlocked. |
| 2 | MTO registered owner lookup | API query to MTO plate registry (where authorized). Owner details pre-filled in citation form. |
| 3 | Citation generation | Automated provincial offence notice generated per HTA requirements. Includes: evidence package reference, officer DID (as badge number equivalent), confidence scores, credential chain summary. |
| 4 | Citation delivery | Mail / email / owner portal notification (per municipal agreement with MTO) |
| 5 | Revenue attribution | Citation amount, node ID, community ID, MSSP ID, officer ID logged for patronage calculation and transparency reporting |

# **Document Control**

| **Ver** | **Date** | **Author** | **Description** |
| --- | --- | --- | --- |
| 1.0 | May 2026 | Toussaint Redji Jean Baptiste | Initial release |

| Classification Notice — This document is CONFIDENTIAL and intended for internal use, legal counsel, and authorized personnel only. Distribution requires written authorization from Toussaint Redji Jean Baptiste. |
| --- |

	Toussaint Redji Jean Baptiste  |  D-Central Ecosystem  |  May 2026	Page  of