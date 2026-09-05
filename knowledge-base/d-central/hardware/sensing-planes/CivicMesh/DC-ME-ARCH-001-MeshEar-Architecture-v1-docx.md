---
source_project: CivicMesh
source_project_uuid: 019e82f3-7ab2-715c-87c1-3e1074a12ab6
doc_uuid: 7a0980ae-3d4c-4486-a92e-a0a4b9d815d6
original_filename: DC-ME-ARCH-001_MeshEar_Architecture_v1.docx
created_at: 2026-06-01T11:32:22.549674+00:00
content_hash: 81705ee3a215
---

**D-Central Group  |  Confidential**	Section 2 — Legal & Corporate Structure

**DC-ME-ARCH-001**

**D-CENTRAL GROUP**

**CommunityShield Inc.**

MeshEar Architecture — Community-Owned Acoustic Detection

| **Document ID** | DC-ME-ARCH-001 |
| --- | --- |
| **Version** | 1.0 |
| **Status** | Draft — SR&ED: AI/audio R&D |
| **Date** | May 2026 |
| **Author** | Toussaint Redji Jean Baptiste |
| **Classification** | Confidential — Technical |
| **SR****&****ED Eligibility** | Primary — on-device acoustic classification model, event-triggered architecture, Canadian environment adaptation |
| **Related Documents** | DC-ME-MODEL-001 │ DC-CM-PRV-001 │ REG-ME-001 │ LEGAL-CS-001 |

| **Executive Summary** MeshEar is the community-owned alternative to ShotSpotter — but architecturally different in a way that addresses ShotSpotter's two core failures: (1) ShotSpotter sends every alert to police as Priority 1, creating alert fatigue; (2) ShotSpotter stores audio in a private company's cloud, creating civil liberties concerns. MeshEar processes audio entirely on-device. No raw audio ever leaves the sensor. Only event classification metadata and a 10-second clip (on confirmed detection) are transmitted. Community triage happens before any police dispatch. |
| --- |

# **1. Core Architecture Principles**

| **Principle** | **Technical Implementation** | **Contrast with ShotSpotter** |
| --- | --- | --- |
| No audio retention | Raw audio processed in a rolling 5-second buffer on-device. Buffer overwrites continuously. No audio is stored unless a detection event triggers clip capture. | ShotSpotter stores audio continuously in cloud — creates ongoing privacy exposure |
| Event-triggered only | Microphone is always powered but acoustic model only triggers clip capture when classification confidence exceeds threshold. Not always-on recording. | ShotSpotter records continuously — legal exposure under Criminal Code s.184 (interception of private communications) |
| On-device classification | Acoustic model runs entirely on embedded processor. Only derived classification + 10-second clip transmitted. | ShotSpotter sends audio to cloud servers for processing — raw audio leaves the device |
| 10-second clip maximum | On detection, only 10 seconds of audio (5 seconds before + 5 seconds after detection point) is captured and transmitted. | ShotSpotter transmits audio of indeterminate length |
| Community triage before dispatch | Detection goes to community NOC first. Community manager or security provider decides whether to escalate to police — not automatic. | ShotSpotter alerts go directly to police dispatch as Priority 1 — no community triage |

# **2. Acoustic Classification Events**

| **Event Type** | **Classification Approach** | **Confidence Threshold** | **Dispatch Route** |
| --- | --- | --- | --- |
| Gunshot | Trained gunshot acoustic signature model — distinguishes from backfire, fireworks, construction | 0.85 (high — minimise false positives that dispatch police) | Community NOC → immediate police dispatch if confirmed |
| Glass break | Glass break acoustic signature — distinguishes from impact sounds | 0.80 | Community NOC → private security dispatch |
| Vehicle collision | High-energy impact acoustic signature — distinguishes from minor impacts | 0.75 | Community NOC → review before dispatch (may be minor) |
| Loud altercation | Elevated voice + impact sound combination — disturbance detection | 0.70 | Community NOC → private security dispatch or observation |
| Explosion | High-energy acoustic event — construction, industrial, or security concern | 0.90 (highest — critical event) | Immediate police dispatch + community NOC notification |

# **3. Criminal Code s.184 Legal Design**

| **The Legal Risk** | Criminal Code s.184 prohibits the interception of private communications. Audio recorded in a residential community could capture private conversations — an offence if done without consent. |
| --- | --- |
| **The Architectural Defence** | MeshEar is event-triggered, not continuous. The acoustic model processes audio in a rolling buffer but never stores it unless an event is detected. The 10-second clip is triggered by an acoustic event (gunshot, glass break), not by voice activity. The legal distinction is between wiretapping (capturing private communications — prohibited) and acoustic event detection (detecting non-communicative sounds — not prohibited). |
| **Legal Opinion Required** | REG-ME-001 — legal opinion from criminal law counsel confirming that MeshEar's event-triggered, non-voice-triggered architecture does not constitute interception of private communications under s.184. This opinion must be obtained before any MeshEar deployment. |
| **Community Consent as Additional Protection** | All residents and visitors in a MeshEar-equipped community are notified of the acoustic detection system (same as other safety infrastructure notices). This notice, while not required for s.184 compliance under the architectural argument, provides an additional layer of legitimacy. |

# **4. Document Control**

| **Ver** | **Date** | **Author** | **Description** |
| --- | --- | --- | --- |
| 1.0 | May 2026 | Toussaint Redji Jean Baptiste | Initial release |

| Classification Notice — This document is CONFIDENTIAL and intended for internal use, legal counsel, and authorized personnel only. Distribution requires written authorization from Toussaint Redji Jean Baptiste. |
| --- |

	Toussaint Redji Jean Baptiste  |  D-Central Ecosystem  |  May 2026	Page  of