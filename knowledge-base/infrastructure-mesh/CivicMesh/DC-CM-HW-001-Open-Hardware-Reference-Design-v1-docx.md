---
source_project: CivicMesh
source_project_uuid: 019e82f3-7ab2-715c-87c1-3e1074a12ab6
doc_uuid: e05cd4e9-2fb6-4351-8c7f-2da8326a222f
original_filename: DC-CM-HW-001_Open_Hardware_Reference_Design_v1.docx
created_at: 2026-06-01T11:32:21.730215+00:00
content_hash: 4b5373004122
---

**D-Central Group  |  Confidential**	Section 2 — Legal & Corporate Structure

**DC-CM-HW-001**

**D-CENTRAL GROUP**

**D-Central Manufacturing Cooperative (DCMC)**

CivicMesh Open Hardware Reference Design

| **Document ID** | DC-CM-HW-001 |
| --- | --- |
| **Version** | 1.0 |
| **Status** | Draft — SR&ED: hardware R&D |
| **Date** | May 2026 |
| **Author** | Toussaint Redji Jean Baptiste |
| **Classification** | Open — CERN-OHL-S v2 |
| **Hardware Licence** | CERN Open Hardware Licence Strong Reciprocal (CERN-OHL-S v2) |
| **Repository** | https://github.com/civicmesh/node-hardware (to be created) |
| **Related Documents** | DC-CM-NODE-PROV-001 │ DC-CM-SUPPLY-001 │ LEGAL-CM-016 │ OS-PATROL-TM-FLEET-001 |

| **Executive Summary** The CivicMesh Open Hardware Reference Design defines the complete hardware specification for a CivicMesh enforcement node. All designs are published under CERN-OHL-S v2 — any manufacturer can produce compatible nodes from the published specifications, but any modifications must be published under the same licence. This prevents proprietary forks. The ATECC608B secure element and the firmware hash in the Node Provenance Credential ensure that any deviation from the certified design breaks the credential chain and disqualifies the node from the enforcement network. |
| --- |

# **1. Node Tier Specifications**

| **Specification** | **Tier 1 — Permanent Fleet** | **Tier 2 — Seasonal Fleet** | **Tier 3 — Contractor Kit** |
| --- | --- | --- | --- |
| Edge Compute | NVIDIA Jetson Orin NX 8GB | NVIDIA Jetson Orin NX 8GB | NVIDIA Jetson Orin NX 8GB (same platform, simplified enclosure) |
| Primary Camera | Sony IMX477 4K, f/2.0, 120° FOV, IR cut filter | Sony IMX477 4K | Sony IMX219 1080p (cost-optimised for temporary deployment) |
| GPS | u-blox ZED-F9P RTK (centimetre-accurate) | u-blox ZED-F9P RTK | u-blox NEO-M9N (metre-accurate — sufficient for citation geolocation) |
| Cellular | Quectel RM520N-GL 5G Sub-6GHz + LTE fallback | Quectel RM520N-GL | Quectel EC21 LTE Cat 1 (sufficient for evidence upload volume) |
| OBD-II | ELM327-compatible hardware adapter, ISO 15765-4 CAN | ELM327-compatible | ELM327-compatible (or 12V DC input if OBD inaccessible) |
| Secure Element | Microchip ATECC608B (hardware-bound private key, non-exportable) | Microchip ATECC608B | Microchip ATECC608A (cost variant — same API, lower memory) |
| Local Storage | NVMe SSD 256GB (evidence buffer + model storage) | NVMe SSD 128GB | eMMC 64GB (sufficient for 6-hour buffer) |
| Power | Hardwired 12V DC from vehicle, 4-hour UPS backup | Hardwired 12V DC, 4-hour UPS | OBD-II primary (5V), 12V DC alternative, 8-hour LiPo battery backup |
| Operating Temperature | -40°C to +85°C operational | -40°C to +85°C | Standard: -20°C to +60°C (contractor environments — less extreme than permanent fleet) |
| Ingress Protection | IP67 (1m submersion 30 min) | IP67 | IP65 (dust-tight + water jets — sufficient for contractor kit) |
| Mounting | Custom vehicle-type bracket (hardwired) | Bolt-mount seasonal bracket | Magnetic + suction mount, <5 min install, no tools |
| Tamper Detection | Enclosure intrusion sensor + accelerometer (mount change detection) | Enclosure intrusion sensor | Tamper-evident seal + firmware checksum on mount change |

# **2. Firmware Architecture**

| **Licence** | GNU GPL v3 — published on GitHub with reproducible builds. Every firmware release has a published SHA-256 hash included in the Node Provenance Credential. |
| --- | --- |
| **Boot Sequence** | Secure boot → firmware hash verification against ATECC608B-stored hash → model integrity check → DID key availability check → cellular connectivity test → NOC registration ping → evidence pipeline ready |
| **Model Loading** | AI models loaded from NVMe storage. Model hash verified against firmware-embedded expected hash on every boot. Model updates pushed via authenticated OTA from MSSP NOC — update verified before applying. |
| **Privacy Processing Pipeline** | Frame capture → violation candidate detection (YOLOv8) → if candidate: face detection → GaussianBlur on detected faces → ALPR on subject vehicle → hash non-subject plates → evidence package assembly → ATECC608B signing → cellular upload |
| **Offline Buffer** | If cellular connectivity drops, evidence packages queued in NVMe buffer (up to 6 hours at normal violation rate). Packages uploaded in order when connectivity restored. Timestamps are GPS-anchored — connectivity loss does not affect evidence timestamp integrity. |
| **Tamper Response** | On enclosure intrusion sensor trigger: (1) alert sent to NOC via LTE; (2) evidence package generation suspended; (3) node DID suspension request sent to platform; (4) local log of tamper event with timestamp. Evidence captured after tamper event is automatically flagged. |

# **3. SR****&****ED Hardware R****&****D Register**

| **Hardware Challenge** | **Technical Uncertainty** | **Investigation Approach** |
| --- | --- | --- |
| IP67 at -40°C with standard silicone seals | Shore hardness of standard silicone increases significantly below -30°C, potentially breaking the IP67 seal. Target material not identified. | Test multiple seal materials (standard silicone, low-temp silicone, EPDM, fluorosilicone) in temperature chamber. Document each failure mode and temperature threshold. |
| Battery performance at -40°C | LiPo batteries lose 60–80% capacity at -40°C. 8-hour backup target may be unachievable with standard cells. | Test multiple cell chemistries (LiFePO4, Li-SOCl2, heated LiPo) and battery management strategies. Document capacity vs temperature curves for each. |
| 5-minute install on diverse vehicle types | Universal magnetic/suction mount that maintains secure attachment on roof surfaces ranging from flat steel (easy) to curved fibreglass (hard) during vehicle operation at highway speeds. | Prototype multiple mount designs. Test on: flat steel roof, curved van roof, fibreglass box truck. Measure retention force at simulated highway vibration. Document failures. |
| Jetson Orin NX at -40°C continuous operation | NVIDIA specs Jetson Orin NX for -25°C minimum. Operating at -40°C requires active thermal management. | Design and test heating element circuit. Measure power consumption impact. Document thermal regulation algorithm. |

# **4. Document Control**

| **Ver** | **Date** | **Author** | **Description** |
| --- | --- | --- | --- |
| 1.0 | May 2026 | Toussaint Redji Jean Baptiste | Initial release |

| Classification Notice — This document is CONFIDENTIAL and intended for internal use, legal counsel, and authorized personnel only. Distribution requires written authorization from Toussaint Redji Jean Baptiste. |
| --- |

	Toussaint Redji Jean Baptiste  |  D-Central Ecosystem  |  May 2026	Page  of