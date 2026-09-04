---
source_project: CivicMesh
source_project_uuid: 019e82f3-7ab2-715c-87c1-3e1074a12ab6
doc_uuid: cba728b2-6468-4344-89fb-5548e132db40
original_filename: DC-CS-NODE-001_CommunityShield_Node_Specification_v1.docx
created_at: 2026-06-01T11:32:21.987366+00:00
content_hash: 339e975a75d0
---

**D-Central Group  |  Confidential**	Section 2 — Legal & Corporate Structure

**DC-CS-NODE-001**

**D-CENTRAL GROUP**

**CivicMesh Inc. / TrafficMesh Technologies Inc.**

CommunityShield Node Specification

| **Document ID** | DC-CS-NODE-001 |
| --- | --- |
| **Version** | 1.0 |
| **Status** | Draft |
| **Date** | May 2026 |
| **Author** | Toussaint Redji Jean Baptiste |
| **Classification** | Confidential — Technical |
| **SR****&****ED Eligibility** | Strong — on-device face/plate blurring AI, privacy-preserving enrollment protocol |
| **Related Documents** | DC-CS-ARCH-001 │ DC-CM-HW-001 │ DC-CM-PRV-001 │ DC-CM-DID-001 |

# **1. Compatible Hardware Specification**

| **Attribute** | **Minimum Requirement** | **Recommended** | **Notes** |
| --- | --- | --- | --- |
| Video resolution | 1080p @ 15fps | 4K @ 30fps | Higher resolution improves face/plate detection accuracy for blurring |
| On-device inference | ARM Cortex-A53 or equivalent (Raspberry Pi CM4) | Rockchip RK3588 or NVIDIA Jetson Nano | Required for on-device blurring — cannot be cloud-processed |
| Local storage interface | NVR NAS via RTSP/ONVIF | Synology DS923+ with 4TB HDD | Community-owned storage — not cloud |
| Weather rating | IP65 | IP67 | Ottawa winters require at minimum IP65 |
| Operating temperature | -20°C to +50°C | -40°C to +65°C | Permanent outdoor installations need full range |
| Night vision | IR cut filter + IR LEDs (10m minimum) | Starlight sensor (no IR required) — 30m | IR can be visible to subjects — starlight preferred for discreet operation |
| Connectivity | 802.11ac WiFi to community NAS | PoE (Power over Ethernet) preferred | PoE eliminates battery/power adapter reliability issues in Canadian climate |

# **2. On-Device Privacy Processing Pipeline**

| **Face Detection** | MobileNetV3-SSD face detection model running on device. All faces in frame detected and bounding boxes extracted before any data leaves the device. |
| --- | --- |
| **Face Blurring** | GaussianBlur applied to all detected face bounding boxes with radius proportional to face size. Minimum blur radius ensures face is not recognizable. Applied before any frame is transmitted or stored on NAS. |
| **Plate Blurring** | ALPR model identifies all license plates in frame. Non-subject vehicle plates blurred. Subject vehicle plate (violation subject) hashed rather than blurred — plaintext plate never transmitted except in confirmed enforcement packages. |
| **Non-Event Frame Discard** | Frames where no motion detection threshold is exceeded are discarded on-device. Only motion-triggered frames are stored to NAS. Reduces storage and eliminates continuous recording of non-events. |
| **SR****&****ED Challenge** | Achieving face detection + plate detection + dual blurring at 30fps on ARM Cortex-A53 without dropping below 15fps for the primary motion detection pipeline. Model quantization and pipeline parallelization are active areas of investigation. |

# **3. Community Network Enrollment Protocol**

- Node owner installs compatible hardware and connects to community NAS

- Node owner opens CivicMesh Member App → Add Node → Scan node QR code or enter serial number

- Node registers with community NOC — DID provisioned (did:key initially, upgraded to did:ethr on activation)

- Node owner completes consent flow in Member App — selects which data sharing programmes to opt in to

- Community manager reviews new node enrollment in Manager Dashboard — approves or requests additional information

- On manager approval: node DID activated, NodeActivationCredential issued, node appears on community map

# **Document Control**

| **Ver** | **Date** | **Author** | **Description** |
| --- | --- | --- | --- |
| 1.0 | May 2026 | Toussaint Redji Jean Baptiste | Initial release |

| Classification Notice — This document is CONFIDENTIAL and intended for internal use, legal counsel, and authorized personnel only. Distribution requires written authorization from Toussaint Redji Jean Baptiste. |
| --- |

	Toussaint Redji Jean Baptiste  |  D-Central Ecosystem  |  May 2026	Page  of