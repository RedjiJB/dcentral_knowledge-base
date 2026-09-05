---
source_conversation_uuid: 9da1c112-9354-46db-be0a-8e8897da5efe
conversation_title: 'SkyLedger and XaaS model recall'
created_at: 2026-06-10T19:03:39.521127Z
doc_id: DC-INFRA-001
description: 'D-Central full ecosystem infrastructure map including NexNode'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-INFRA-001 — D-Central Ecosystem Infrastructure Map
**Version:** 1.0  
**Classification:** D-Central Architecture Reference  
**Status:** Draft  

---

## 1. Infrastructure Philosophy

D-Central's infrastructure follows one rule: **every layer must be ownable by the cooperative itself.** There is no dependency on AWS, Azure, Google Cloud, Cloudflare, or any centralized provider that can terminate service, surveil traffic, or extract rent. Every hardware tier, network link, storage node, and compute cluster is either cooperatively owned, community-hosted, or open-source self-hostable.

This is not idealism — it is the technical prerequisite for sovereignty.

---

## 2. NexNode — The Edge Compute Substrate

NexNode is D-Central's edge datacenter hardware platform. It is the physical layer that makes every D-Central service real. Without NexNode, the ecosystem is software running on someone else's hardware — which means someone else's rules.

NexNode is deployed in four tiers, each serving a different role in the ecosystem:

---

### NexNode Tier 0 — Sensor Node
**Form factor:** Embedded microcontroller (ESP32, RP2040, Arduino)  
**Power:** <1W, solar or battery operable  
**Role:** The lowest layer of the physical world interface

**What it runs:**
- Environmental sensors (temperature, humidity, pressure, air quality)
- Equipment telemetry (vibration, current draw, GPS)
- WeatherMesh atmospheric sensors
- LoRaWAN / BLE mesh radio for upstream relay
- Tamper-detection and physical security sensors

**Ecosystem connections:**
- Feeds raw sensor data to Tier 1 or Tier 2 nodes
- Carries a hardware DID (provisioned at manufacture)
- SkyLedger drone companion modules are Tier 0 class

---

### NexNode Tier 1 — Home Node
**Form factor:** Mini PC or SBC cluster (Raspberry Pi 5, Intel N100, ARM mini PC)  
**Power:** 10–25W  
**Connectivity:** Wi-Fi 6 + Gigabit Ethernet + LoRa gateway  
**Role:** The cooperative member's sovereign home infrastructure node

**What it runs:**
- HomeDAO client — participates in home cooperative governance
- Local D-VAULT node — encrypted personal data storage
- Mesh networking stack (Babel/BATMAN-adv routing daemon)
- Local AI inference (Ollama, small models ≤7B)
- WeatherMesh ground station (with sensor hat attached)
- SkyLedger Edge Agent (if drone is registered to this operator)
- D-ID wallet (DID key management, VC storage)
- NorthLedger personal finance agent
- VPN gateway for remote cooperative member access

**Hardware reference build:**
- Raspberry Pi 5 (8GB) or Beelink Mini S12 Pro
- 1TB NVMe SSD
- LoRa HAT (SX1276) for sensor relay
- BME280 weather sensor
- UPS HAT (18650 cells, ~4hr backup)
- Total BOM: ~$180–$250 CAD

**Ecosystem connections:**
- Anchors member DID to home mesh
- Provides D-VAULT hot storage for home Zone 3 data
- CTS domestic environment domain sensor gateway
- DCOT transit node if located on a route corridor

---

### NexNode Tier 2 — Community Hub
**Form factor:** Tower server or 1U rackmount  
**Power:** 150–400W  
**Connectivity:** 10GbE LAN + fibre uplink (GPON or FSO) + 5G/LTE backup  
**Role:** The cooperative's shared infrastructure node — the anchor point for a building, block, or small community

**What it runs:**
- Cooperative blockchain validator node (L2 appchain)
- IPFS cluster node (D-VAULT warm storage)
- Fractal DAO OS — governance proposal and voting engine
- NexNode compute pool — accepts jobs from D-Central task queue
- CTS Sensor Gateway — aggregates all Tier 0/1 sensors in zone
- MeshTelecomDAO relay node — mesh ISP backhaul
- AI inference server (medium models, 13B–34B)
- Federated learning aggregation node
- OpenSecure surveillance processing (edge CV, no raw video off-site)
- D-AGORA cooperative marketplace node

**Hardware reference build:**
- AMD EPYC 7003 or Intel Xeon E-series (8–16 cores)
- 64–128GB ECC DDR4
- 4TB NVMe (hot) + 16TB HDD (warm storage)
- NVIDIA RTX 3090 / A4000 (AI inference)
- Dual 10GbE NIC
- OpenBMC for remote management
- Total BOM: ~$4,000–$8,000 CAD

**Ecosystem connections:**
- Runs CTS DataAnchor.sol submissions for the zone
- Processes SkyLedger telemetry relay for local fleet
- Hosts HomeDAO governance for building/block cooperative
- Reference hardware for WeatherMesh Relay Node

---

### NexNode Tier 3 — Regional Gateway
**Form factor:** Multi-node rack cluster or purpose-built edge datacenter  
**Power:** 2–20kW  
**Connectivity:** 100GbE core + FSO/fibre mesh uplinks + satellite backup  
**Role:** The regional cooperative's compute infrastructure — serves a district, city sector, or island

**What it runs:**
- Heavy AI inference (LLM serving, 70B+ models, multi-GPU)
- SkyLedger LiDAR and SAR processing pipeline
- IPFS archive node (D-VAULT cold storage, petabyte-scale)
- Regional blockchain full node + RPC endpoint
- MeshTelecomDAO regional ISP core router
- D-VDI (Virtual Desktop Infrastructure) — sovereign remote desktops
- D-Search index and query engine
- Federated learning model aggregation
- Sovereign Cyber Range training environments
- NorthLedger cooperative accounting backend
- RadarNet ground station processing

**Hardware reference build:**
- 3–8× AMD EPYC or Intel Xeon nodes (32–128 cores each)
- 512GB–2TB ECC RAM per node
- All-NVMe storage array (100TB+) + Ceph distributed storage
- 4–8× NVIDIA A100 or H100 (AI/processing cluster)
- 100GbE spine switches (open hardware: Edgecore, FS.com)
- UPS + generator backup (N+1 redundancy)
- Physical security: biometric + DID-gated access
- Total BOM: $80,000–$500,000 CAD depending on scale

**Ecosystem connections:**
- Anchors the regional cooperative's entire digital infrastructure
- SkyLedger: processes all LiDAR point clouds, SAR imagery, flight logs
- TrafficMesh: processes enforcement video at the edge, never centrally
- HMCS: the compute backbone of the Human Mesh Civilization Stack
- Haiti SVL: regional node for Port-au-Prince or Cap-Haïtien deployment

---

## 3. Network Infrastructure

The network is the circulatory system. Without it, NexNode nodes are isolated. D-Central's network is cooperative-owned from edge to core.

### 3.1 Access Layer (Last-Mile)

| Technology | Range | Throughput | Use Case |
|------------|-------|------------|----------|
| **Wi-Fi 6 (802.11ax)** | 50–100m | 1–9.6 Gbps | Home and building access |
| **Wi-Fi 6E (6GHz band)** | 30–60m | Up to 9.6 Gbps | Dense urban, low interference |
| **LoRaWAN** | 2–15km | 0.25–50 kbps | Sensor nodes, IoT, rural areas |
| **BLE Mesh** | 10–30m | 1–2 Mbps | Indoor sensor networks, proximity |
| **DECT-2020 NR** | 1–5km | Up to 25 Mbps | Industrial IoT, unlicensed |
| **5G NR (cooperative MVNO)** | Cell-dependent | 100 Mbps–1 Gbps | Mobile nodes, drone uplink |

### 3.2 Distribution Layer (Neighbourhood / Campus)

| Technology | Range | Throughput | Use Case |
|------------|-------|------------|----------|
| **GPON Fibre** | Up to 20km | 2.5–10 Gbps | Cooperative building fibre |
| **Free Space Optical (FSO)** | 500m–2km | 10–100 Gbps | Point-to-point building links |
| **Point-to-Point microwave** | 1–50km | 1–10 Gbps | Rural distribution, island hops |
| **BATMAN-adv / Babel mesh** | Multi-hop | Variable | Self-healing mesh routing |
| **OpenWRT routers** | Node-level | 1 Gbps | Cooperative-managed mesh CPE |

### 3.3 Backhaul / Core Layer

| Technology | Reach | Throughput | Use Case |
|------------|-------|------------|----------|
| **Dark fibre lease** | City/region | 100 Gbps+ | Cooperative ISP core |
| **FSO long-range** | 2–10km | 10 Gbps | Inter-hub links without fibre |
| **Starlink (backup)** | Global | 100–500 Mbps | Rural/island fallback |
| **VSAT Ka-band** | Global | 50–150 Mbps | Haiti / Caribbean remote |
| **DTN store-and-forward** | Any | Variable | Disconnected / disaster mode |

### 3.4 Protocol Stack

```
Application     D-Central services (D-VAULT, D-ID, Lakou, SkyLedger...)
                        │
Transport       QUIC / TLS 1.3 (all links encrypted)
                        │
Network         IPv6 native + Yggdrasil (encrypted mesh overlay)
                        │
Routing         Babel (wired/wireless) + BATMAN-adv (wireless mesh)
                        │
Data Link       Ethernet / Wi-Fi 6 / FSO / LoRa
                        │
Physical        Fibre / Copper / RF / Light
```

**Yggdrasil** is the cooperative mesh overlay — every NexNode gets an IPv6 address on the Yggdrasil network, enabling encrypted peer-to-peer connectivity regardless of underlying ISP or NAT topology. This is the backbone that makes D-Central's decentralized services reachable without DNS or centralized routing.

---

## 4. Power Infrastructure

Sovereignty requires power independence. D-Central's power model is cooperative-owned renewable with grid fallback.

### 4.1 Home Node Power (Tier 1)
- Solar panel (100–400W) + MPPT charge controller
- LiFePO4 battery bank (2–10 kWh)
- Automatic grid fallback
- NexNode UPS HAT for brownout protection
- Target: 72-hour autonomous operation

### 4.2 Community Hub Power (Tier 2)
- Rooftop solar array (2–10 kW)
- Battery bank (20–100 kWh, Tesla Powerwall or DIY LFP)
- Grid connection with net metering
- Automatic transfer switch
- Target: 48-hour autonomous operation at full load

### 4.3 Regional Node Power (Tier 3)
- Solar + wind hybrid generation (50 kW+)
- Large battery bank (200 kWh+)
- Generator backup (diesel or biodiesel)
- N+1 UPS on all critical systems
- Target: 7-day autonomous operation

### 4.4 Haiti / Off-Grid Deployments
The Haiti model requires full off-grid capability. All NexNode tiers are designed to operate without grid connection. The Solar + LFP + diesel generator stack is the reference architecture for island and rural deployments where grid reliability cannot be assumed.

---

## 5. Identity Infrastructure (D-ID Layer)

Every device, person, and organization in D-Central has a sovereign identity. This requires:

### 5.1 DID Method
- **Primary:** `did:cheqd` (Cheqd Network — purpose-built for VCs, Cosmos SDK)
- **Fallback:** `did:key` (local, no network dependency)
- **Hardware:** `did:dcentral:drone:<uuid>`, `did:dcentral:node:<uuid>` (custom method)

### 5.2 VC Infrastructure
- **Issuance:** Each cooperative runs a VC issuer node (Affinidi, Walt.id, or custom)
- **Registry:** StatusList2021 revocation lists anchored on cooperative blockchain
- **Storage:** VCs stored in member's D-VAULT; presented via DIF Presentation Exchange
- **Hardware wallets:** NFC-capable smart cards for physical presentation (OpenSecure/PIV)

### 5.3 Key Management
- Tier 1 nodes: software keys in encrypted local store
- Tier 2/3 nodes: Hardware Security Module (HSM) or TPM 2.0
- Drone hardware: Secure element (ATECC608A or equivalent)

---

## 6. Blockchain Infrastructure

D-Central runs its own cooperative blockchain — not Ethereum mainnet (too expensive), not a public L1 (not sovereign).

### 6.1 Chain Architecture
- **Base layer:** Cosmos SDK appchain or Optimism OP Stack L2
- **Consensus:** Tendermint BFT (Cosmos) or PoA with cooperative validators (OP Stack)
- **Validators:** NexNode Tier 2 and Tier 3 nodes operated by cooperative members
- **RPC endpoints:** Served by Tier 3 regional nodes; no reliance on Infura/Alchemy

### 6.2 Smart Contract Platform
- **EVM-compatible** (Solidity, Vyper)
- **Core contracts:** CoopRegistry, DataAnchor, FractalDAORegistry, ConsentEngine, EscrowDAO, Lakou settlement
- **Upgradability:** OpenZeppelin Transparent Proxy pattern; upgrade requires DAO supermajority vote

### 6.3 Cross-Chain Bridges
- IBC (Inter-Blockchain Communication) for Cosmos ecosystem
- LayerZero or Axelar for EVM cross-chain (external cooperative partnerships)
- Manual bridge governance for high-value cross-chain operations

---

## 7. Storage Infrastructure (D-VAULT)

### 7.1 Storage Tiers

| Tier | Technology | Hosted On | Latency | Cost |
|------|-----------|-----------|---------|------|
| Hot | NVMe SSD + Redis cache | Tier 2/3 NexNode | <50ms | High |
| Warm | IPFS (Kubo) pinned | Tier 2/3 NexNode | <500ms | Medium |
| Cold | IPFS + Filecoin | Tier 3 + cooperative archive nodes | Minutes | Low |
| Public | IPFS public gateway | Any node | <100ms | Subsidized |

### 7.2 Data Sovereignty Guarantees
- All data encrypted at rest with client's DID-derived key
- IPFS CIDs are content-addressed — data cannot be silently modified
- Deletion enforced via key rotation + garbage collection + deletion VC
- No D-Central cooperative node can read client data without explicit consent VC

---

## 8. AI / Compute Infrastructure

### 8.1 Inference Tiers

| Tier | Hardware | Models | Use Case |
|------|----------|--------|----------|
| Edge (Tier 1) | CPU + NPU (Pi 5 / N100) | 1B–7B quantized | Personal assistant, local queries |
| Community (Tier 2) | Single GPU (RTX 3090) | 13B–34B | Cooperative analytics, classIQ |
| Regional (Tier 3) | Multi-GPU (A100 cluster) | 70B+ / multimodal | LiDAR processing, SAR, D-VDI |
| Swarm | Federated across nodes | Distributed | Federated learning, large jobs |

### 8.2 AI Stack
- **Runtime:** Ollama (local), vLLM (GPU server), llama.cpp (edge)
- **Model abstraction:** LiteLLM (swappable backend without code changes)
- **Federated learning:** Flower (flwr) framework across NexNode cluster
- **Computer vision:** YOLOv8 / OpenCV (OpenSecure, SkyLedger, TrafficMesh)
- **Geospatial processing:** PDAL (point clouds), GDAL (rasters), OpenDroneMap

---

## 9. SkyLedger-Specific Infrastructure

SkyLedger places unique infrastructure demands on the ecosystem:

### 9.1 Drone Ground Infrastructure
- **Charging pads:** Cooperative-owned autonomous charging stations at Tier 2 hub sites
- **Hangar nodes:** Climate-controlled storage with NexNode Tier 2 co-located
- **Launch pads:** Pre-surveyed takeoff/landing zones registered in SkyLedger Fleet Registry
- **Relay towers:** LoRa + LTE relay nodes extending drone comms range in rural areas

### 9.2 SkyLedger Processing Infrastructure
- **WeatherMesh relay nodes:** Tier 2 NexNode at cooperative sites with anemometer + barometer
- **LiDAR processing cluster:** Tier 3 NexNode with PDAL pipeline (16+ cores, 128GB+ RAM)
- **SAR processing cluster:** Tier 3 NexNode with GPU acceleration (SNAP, PolSARpro, GDAL)
- **Telemetry bus:** MQTT broker (Mosquitto) on Tier 2, retained messages for replay
- **RadarNet nodes:** Software-defined radar processing (GNU Radio) on Tier 2/3

### 9.3 Airspace Infrastructure
- **UTM integration:** API connection to NavCanada / FAA DroneZone / EASA U-space from Tier 3
- **NOTAM oracle:** Automated NOTAM parsing and zone flagging, updated every 15 minutes
- **ADS-B receiver network:** Low-cost ADS-B receivers (FlightAware dongles) at Tier 2 sites for manned aircraft awareness

---

## 10. Full Ecosystem Infrastructure Map

```
TIER 3 — REGIONAL GATEWAY (1 per region/city)
├── Multi-node compute cluster (EPYC + A100 GPUs)
├── Petabyte IPFS archive
├── Blockchain full node + RPC
├── LiDAR / SAR processing
├── MeshTelecomDAO core router
├── D-VDI backend
├── FSO/fibre core links
└── Solar + battery + generator (N+1)
        │
        │ 100GbE fibre / FSO
        ▼
TIER 2 — COMMUNITY HUB (1 per building / block / 50–200 members)
├── Tower server (Xeon + RTX GPU)
├── IPFS warm storage (4–16TB)
├── Blockchain validator node
├── CTS Sensor Gateway
├── MeshTelecomDAO relay
├── AI inference (13B–34B)
├── OpenSecure CV processing
├── WeatherMesh relay node
├── SkyLedger telemetry relay
└── Solar + battery (48hr)
        │
        │ GPON fibre / FSO / 10GbE mesh
        ▼
TIER 1 — HOME NODE (1 per household / cooperative member)
├── Mini PC / SBC (Raspberry Pi 5 / N100)
├── Local D-VAULT (1TB NVMe)
├── HomeDAO client
├── Mesh routing daemon
├── Local AI (7B)
├── D-ID wallet
├── WeatherMesh ground station
├── SkyLedger Edge Agent (if drone operator)
└── Solar + LFP battery (72hr)
        │
        │ Wi-Fi 6 / LoRa
        ▼
TIER 0 — SENSOR / DRONE NODES
├── Environmental sensors (BME280, SCD41, etc.)
├── Equipment telemetry (ESP32 + J1939/CANbus)
├── SkyLedger drone fleet (MAVLink + SEA agent)
├── WeatherMesh mobile nodes (airborne sensors)
├── TrafficMesh dashcam nodes
└── OpenSecure perimeter sensors
```

---

## 11. Infrastructure by D-Central Component

| Component | Tier 0 | Tier 1 | Tier 2 | Tier 3 |
|-----------|--------|--------|--------|--------|
| **D-ID / DID-Auth** | Hardware DID on devices | Key wallet | VC issuer node | DID resolver, VC registry |
| **D-VAULT** | — | Hot storage (personal) | Warm storage (cooperative) | Cold archive |
| **Lakou Protocol** | — | Local wallet | Settlement relay | Blockchain node + RPC |
| **CTS** | Worksite sensors | Domestic sensors | Sensor gateway + ZK proofs | Data product publishing |
| **WeatherMesh** | Drone sensors | Ground station | Relay node | Archive + API |
| **SkyLedger** | Drone Edge Agent | Operator console | Telemetry relay + charging | LiDAR/SAR processing |
| **TrafficMesh** | Dashcam node | — | CV processing | Enforcement database |
| **OpenSecure** | Physical sensors | — | CV edge processing | SIEM + audit |
| **NorthLedger** | — | Personal finance | Cooperative accounting | Regional audit |
| **MeshTelecomDAO** | LoRa gateway | Home mesh node | Distribution router | ISP core |
| **D-VDI** | — | Thin client | — | Desktop compute backend |
| **HMCS** | Sensor layer | Member node | Community node | Civilization stack compute |
| **Haiti SVL** | Island sensors | Member node | Island hub | Diaspora bridge |

---

## 12. What Infrastructure Does NOT Exist Yet

The following represent genuine infrastructure gaps that must be built before full ecosystem operation:

| Gap | What's Needed | Priority |
|-----|--------------|----------|
| NexNode hardware spec (official) | Published open hardware design (CERN OHL-W) for each tier | Critical |
| Cooperative blockchain mainnet | Deployed appchain with validators | Critical |
| VC issuance infrastructure | Deployed VC issuer nodes per cooperative | Critical |
| MeshTelecomDAO CRTC registration | ISP license + pole attachment agreements | High |
| SkyLedger drone charging network | Physical charging pads at Tier 2 sites | High |
| RadarNet ground station network | Deployed radar nodes at Tier 2/3 sites | Medium |
| FSO inter-hub links | Deployed optical terminals between Tier 2/3 | Medium |
| Haiti Tier 3 node | Regional gateway for Port-au-Prince / Cap-Haïtien | High |
| NexNode Tier 0 open hardware kit | Manufacturable sensor node BOM + firmware | Medium |

---

*D-Central Sovereign Cooperative Infrastructure*  
*DC-INFRA-001 v1.0 · Draft*
