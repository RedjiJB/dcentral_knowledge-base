---
source_conversation_uuid: 3f5ca7e9-4f80-44bd-980f-eeb4e94eac89
conversation_title: 'Building projects from documentation to implementation'
created_at: 2026-07-06T00:05:45.199518Z
doc_id: DC-PROCUREMENT-001
description: 'Consolidated cross-project procurement plan, compute-first, grounded in the real BOMs from past chats'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# D-Central Consolidated Procurement Plan — DC-PROCUREMENT-001

**Purpose:** Move from documentation to a physical build. This is a single, phased procurement sequence across all projects, ordered so that each purchase unblocks the maximum number of downstream projects. Compute first, as requested.

**Currency:** CAD. Ranges are low–high from your own project BOMs (Mesh Home CUC, DC-AGD-001, DC-TM-BOM-002/003, DC-SHI tier model, Sovereign Cyber Range).

**Core principle:** You are not buying every project. You are buying (1) one shared foundation, then (2) one working prototype of each node type. Replication and scale come only after a prototype is proven.

---

## The dependency map — why compute is first

Almost every project runs on the same foundation. One compute-and-network core serves all of these:

| Project | What it needs from the foundation |
|---|---|
| SHI node / agent cabinet (11-agent) | GPU inference + local LLM host |
| Sovereign Cyber Range (on-prem SOC track) | VM host for Wazuh / TheHive / MISP |
| Acoustic Gunshot Detection (DC-AGD) | Pi-cluster gateway: ML, multilateration, IPFS, chain anchor |
| Federated learning model | On-node compute + differentially-private deltas |
| TrafficMesh / CivicMesh | Backhaul + fleet management host |
| OpenSecure PACS | Access-control head-end + SAFR/analytics |

Build the foundation once and five projects light up. This is the whole reason to sequence compute first.

---

## PHASE 0 — Compute + Network Foundation (build this first)

This is the "Compute/CUC" spec from your Mesh Home doc, which doubles as the agent-cabinet host and the cyber-range VM host.

### 0.1 Core compute node

| Component | Spec | Cost (CAD) |
|---|---|---|
| CPU | AMD Ryzen 9 7950X (16C/32T) | $700–$950 |
| GPU | NVIDIA RTX 4090 24GB GDDR6X | $2,200–$2,800 |
| RAM | 128GB DDR5-5600 ECC (4×32GB) | $600–$1,200 |
| NVMe (OS + models) | 4TB PCIe Gen 5 (Samsung 990 Pro class) | $400–$700 |
| NVMe (data) | 2× 8TB PCIe Gen 4, RAID-1 mirror | $1,200–$2,200 |
| Motherboard | ASUS Pro WS X670E-ACE (ECC, dual NVMe Gen5) | $500–$800 |
| PSU | 1600W 80+ Titanium | $400–$600 |
| Rack UPS | CyberPower OL3000RTXL2U 3000VA online | $900–$1,500 |
| Enclosure | 18U wall-mount server cabinet | $400–$700 |
| **Subtotal** | | **$7,300–$11,450** |

*Runs out of the box: TensorRT, Triton, NIM (local Llama-3-8B / Mistral-7B / Phi-3), DeepStream (150+ streams), Omniverse digital twin. This is your agent-cabinet brain and cyber-range host in one box.*

### 0.2 Network core

| Component | Spec | Cost (CAD) |
|---|---|---|
| Edge router | MikroTik CCR2004 (BGP-capable, 10GbE) | $500–$700 |
| Firewall / zero-trust GW | Netgate 6100 pfSense **or** Protectli VP2420 + OPNsense | $450–$1,200 |
| Managed switch | 48-port PoE++ (802.3bt), 10GbE uplinks | $1,200–$2,500 |
| Cabling / patch / labels | Cat6A, fibre adapters, cable mgmt | $300–$600 |
| **Subtotal** | | **$2,450–$5,000** |

*Enforces the 11-VLAN architecture. PoE++ powers every downstream sensor/camera. Firewall gives you Suricata IDS/IPS + WireGuard for free.*

**PHASE 0 TOTAL: ~$9,750–$16,450 CAD**

---

## PHASE 1 — First shovel-ready node (already Amazon-carted)

The TrafficMesh / CivicMesh enforcement node (DC-TM-BOM-002). This is the closest to done — you already selected open-source substitutions and had a cart going. Build **one** unit as your first real hardware.

| Component | Substitution already chosen | Notes |
|---|---|---|
| Compute | CM4102008 (from PiShop.ca) | Confirmed source |
| Camera | Generic UVC camera | Replaced Viofo dashcam |
| CAN interface | MCP2515 CAN module | Replaced ELM327 |
| OBD processor | **STN2120** | ⚠ STN1170 discontinued — use STN2120 |
| Connectivity | Phone USB tether (PoC) | LTE (Quectel EC25) deferred to Phase 2 |
| TPM | swtpm (software, dev) | Hardware TPM deferred |
| IMU / RTC / watchdog | per DC-TM-BOM-003 | |

**Est. single prototype unit: ~$150–$400 CAD** (most parts already sourced). Radar + SIM deferred by your earlier decision.

*You already have: multimeter, wire stripper, reflow hot plate, 80W soldering kit. Missing per last review: MCP2515 module, HDMI cable, solder wire, Prime jumper wires, verify the USB hub is powered.*

---

## PHASE 2 — Sensing prototypes (one of each type)

### 2.1 Acoustic Gunshot Detector — one array node + gateway (DC-AGD-001)

| Component | Part | Role |
|---|---|---|
| Edge compute | ESP32-S3 | Per-node capture/edge |
| Direction mic | Infineon IM72D128 PDM array (IP57) | Phase-matched direction |
| Transient mic | TDK ICS-40638 (138 dB-AOP) | Won't clip on blast |
| Timing/GPS | u-blox NEO-M9N + PPS | Sub-µs TDOA sync |
| Secure element | ATECC608B | Device DID anchor |
| Power/comms | Solar + LoRa | Off-grid |
| Gateway | Raspberry Pi cluster | ML + multilateration + IPFS + chain anchor |

**Est. one array node: ~$150–$300** + gateway (Pi cluster) **~$400–$800**. TDOA needs ≥3–4 array nodes for a real fix, but build/bench **one** first, plus the single gateway (gateway is shared with the compute foundation).

### 2.2 SHI sensor stack — one tier, one room first

Per-dwelling tiers from your corrected cost model (compute already covered in Phase 0):

| Tier | Per-dwelling sensor cost |
|---|---|
| Lite | ~$650 |
| Standard | ~$2,920 |
| Full-Structural | ~$9,730 |
| Max | ~$15,410 |

**Recommendation:** buy **one room's worth of Standard-tier** sensors (~$300–$600) to validate the pipeline into your Phase 0 GPU host before committing a whole dwelling. Sensing is capped at Levels 1–3 for residential; LiDAR L4/5 is campus-tier and deferred.

**PHASE 2 TOTAL (prototypes only): ~$1,400–$3,000 CAD**

---

## PHASE 3 — Software / range (mostly OPEX, minimal new hardware)

The Sovereign Cyber Range on-prem SOC track (Wazuh / TheHive / MISP / OpenVAS) runs as **VMs on the Phase 0 host** — no new hardware for the on-prem track. Cloud and Web3 tracks are subscription/testnet, not procurement. Timeline in your own plan: architecture now, infrastructure summer 2027, paid launch Jan 2028. **No hardware purchase required here beyond Phase 0.**

---

## PHASE 4+ — Deferred scale-out (do NOT buy yet)

These are documented but should not be purchased until a prototype above is proven and there's a funding line (Better Homes Loan, HELOC, grant, or revenue):

- **SHI whole-dwelling / multi-property** rollout (Layer 1 energy alone is ~$42,500/home: solar, Victron inverters, EG4 batteries, EVSE).
- **SkyLedger** drone-as-first-responder hardware (requires SFOC for urban BVLOS — regulatory gate before spend).
- **D-Central ISP** FSO/GPON backhaul.
- **Campus L4/L5 LiDAR** sensing ($3K–$15K/node; $50K–$500K L5 clusters).
- **National-scale** anything (your models put full saturation at ~$20B capex — not a personal purchase).

---

## Procurement timeline

| When | Phase | Cash (CAD) | Unlocks |
|---|---|---|---|
| Month 1 | **Phase 0** compute + network | $9,750–$16,450 | Agent cabinet, cyber range host, all gateways |
| Month 1–2 | **Phase 1** TrafficMesh node | $150–$400 | First working hardware (parts mostly in cart) |
| Month 2–4 | **Phase 2** gunshot + SHI room | $1,400–$3,000 | Sensing pipeline validated on GPU host |
| Ongoing | **Phase 3** range (software) | ~$0 hardware | Runs on Phase 0 box |
| Gated | **Phase 4+** scale-out | funding-dependent | Only after prototypes proven |

**Realistic starting outlay to get from zero to a working, multi-project foundation + three live prototypes: ~$11,000–$20,000 CAD.**

---

## Immediate next actions

1. Finalize the Phase 0 compute cart (biggest single line: RTX 4090 — check current pricing before buying; GPU prices move).
2. Close out the Phase 1 cart gaps: MCP2515, HDMI cable, solder wire, powered USB hub check, STN2120 (not STN1170).
3. Decide funding line for Phase 0 (cash vs. HELOC/loan) before the GPU purchase.
4. Confirm which single property hosts the foundation rack.
