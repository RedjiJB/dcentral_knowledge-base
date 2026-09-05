---
source_conversation_uuid: 8f7a2740-7f7b-4f16-b483-d1e161ebb85e
conversation_title: '💬 I have an idea for the dcentra…'
created_at: 2026-08-08T03:34:00.540823Z
doc_id: DC-SIM-001
description: 'Core fidelity reference document — what GNS3 can and cannot model'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
topic: "dcentral-simulation-lab-programme"
---

# DC-SIM-001 — Fidelity Reference

| Field | Value |
|---|---|
| Document ID | DC-SIM-001 |
| Version | v1.0 |
| Date | August 2026 |
| Author | Toussaint Redji Jean Baptiste |
| Status | Reference — stable |

---

## 1. The governing principle

GNS3 runs real software on virtual wires.

Everything that is software behaviour transfers faithfully to production. Everything
that is physical — radio, optics, distance, power, thermal, time — does not exist and
cannot be recovered by any configuration.

A single sentence version, for use in the limitations section of any write-up:

> The emulation tests correctness and partition behaviour. It does not test capacity,
> and it contains no physical layer.

---

## 2. Backend fidelity

GNS3 is a controller over four different emulation backends. Fidelity questions are
almost always backend questions.

| Backend | Mechanism | Fidelity | Constraint |
|---|---|---|---|
| **QEMU** | Full machine virtualisation | 1:1 — runs the actual image | Needs KVM for speed; RAM-bound |
| **Docker** | Shared host kernel | High for userspace | No kernel, no boot, no init testing |
| **Dynamips** | MIPS/PPC hardware emulation | Real IOS binaries | Legacy platforms only (2600/3600/3700/7200) |
| **IOU/IOL** | Cisco-internal binaries | High | Licence-restricted — do not use |

**Selection rule.** Use QEMU where the artefact under test is an OS image. Use Docker
for everything else. Dynamips only if a specific legacy IOS feature is required.

### 2.1 ARM emulation penalty

An aarch64 QEMU image on an x86-64 host runs under TCG with no KVM acceleration —
approximately 5–20× slowdown per node. Acceptable for one node, unusable for a
multi-node topology. This drives the dual-architecture build in DC-SIM-003.

---

## 3. Fidelity tiers

### 3.1 Faithful — real production software, real control plane

- **Routing:** FRR, BIRD, VyOS, Cisco IOSv / IOSvL2 / Cat8000v, Arista vEOS,
  Nokia SR Linux, Juniper vMX / vSRX
- **Security:** nftables, iptables, pfSense / OPNsense, WireGuard, strongSwan, OPA
- **Switching logic:** Open vSwitch, IOSvL2 — VLANs, trunking, STP, EtherChannel,
  DHCP snooping, port security all behave correctly
- **Overlay:** Yggdrasil, WireGuard mesh
- **Mesh routing protocols:** BATMAN-adv, Babel, OLSR (see §3.3 for the caveat)
- **ICN:** NFD (NDN), CCN-lite — research-grade but real
- **DTN:** ION, µD3TN — BPv7 store-and-forward
- **Telecom:** Kamailio, FreeSWITCH (SIP), Janus, mediasoup (WebRTC)
- **Mobile core:** Open5GS, free5GC + UERANSIM — AMF, SMF, UPF, N2/N3/N4, simulated gNB/UE
- **Identity:** ACA-Py, Veramo — DID/VC issuance, presentation, resolution
- **Storage:** IPFS, Ceph, MinIO, Garage, SeaweedFS
- **Orchestration:** K3s, wasmtime, WasmEdge, Spin
- **Chain:** Anvil, OP-Stack devnet, Hyperledger, Tendermint
- **Media:** MediaMTX, Owncast, Jellyfin, nginx-rtmp
- **Caching:** Squid, Varnish
- **Transition:** Jool (NAT64/464XLAT), CGNAT via nftables

### 3.2 Approximated — behaviour correct, magnitude asserted

| Item | Method | What is lost |
|---|---|---|
| Link bandwidth | GNS3 link filters, `tc` HTB | Rate is declared, not achieved |
| FSO atmospherics | Scripted loss/latency profiles | No optics, no weather, no distance |
| GPON distribution | Linux node as OLT + `tc` HTB per ONT | No TDMA, no ranging, no real split |
| Switching hardware | Software forwarding | No ASIC, TCAM, hardware queues, microbursts |
| Convergence timing | Real protocol timers | Valid **relative**, not as absolute SLA |

### 3.3 Not modellable at all

- **RF and spectrum, entirely.** No 802.11 PHY/MAC, no interference, no hidden node,
  no MU-MIMO, no spatial streams, no mobility, no roaming, no propagation
- **Beamforming, RF or acoustic.** This is DSP and physics, not networking. Belongs to
  NumPy/MATLAB, GNU Radio, ns-3/Sionna, or real hardware
- **Optics and fibre plant.** Link budgets, fog, freezing rain, scintillation, splice loss
- **Physical devices.** Cameras, HID readers, LiDAR, sensors, poles, drones, solar,
  batteries, enclosures — traffic can be generated on their behalf; the devices cannot exist
- **TEE-backed attestation.** No hardware root of trust, no secure enclave
- **Line rate and hardware QoS.** Throughput is bounded by host CPU
- **PTP and deterministic timing**
- **SIM provisioning, carrier interconnect, SS7/PSTN reality**
- **Long-duration effects.** Certificate expiry, disk fill, config drift, upgrade debt —
  simulations run for hours; infrastructure fails over years

### 3.4 Two traps that produce actively wrong conclusions

These are the cases where the emulation does not merely omit information but supplies
false information. Both must be named explicitly in any write-up.

**Mesh link quality metrics are fiction.** BATMAN-adv and Babel select paths using
link-quality estimates derived from real signal conditions. In GNS3 every link is either
perfect or artificially impaired by a filter. The mesh will converge correctly for
reasons that do not exist. Convergence *behaviour* is real; the *inputs* to convergence
are not.

**Distributed LLM inference will appear viable when it is not.** Tensor and pipeline
parallelism across nodes (llama.cpp RPC, exo, Petals) require sub-millisecond
interconnect. GNS3 links run at host memory speed, so layer-split inference across a
simulated WAN will succeed in emulation and fail in deployment. This directly affects
SHI distributed inference modelling. Federated learning (Flower) is the latency-tolerant
alternative and models correctly.

---

## 4. Scale ceilings

Per-node RAM, measured working figures:

| Node type | RAM | Notes |
|---|---|---|
| Alpine / Docker service | 128–512 MB | Dozens per host |
| FRR / VyOS router | 512 MB – 1 GB | |
| DC-OS Buildroot qcow2 | 512 MB – 1 GB | Minimal by design |
| IOSvL2 switch | 768 MB | |
| Full Linux VM | 2–4 GB | |
| Open5GS core (all NFs) | 4–6 GB total | |
| Ollama, one instance | 8–16 GB | One only |

Approximate ceilings on 16 GB: 50–100+ Docker nodes, 20–25 minimal QEMU nodes,
10–12 IOSv nodes.

---

## 5. D-Central subsystem coverage

### 5.1 D-Central ISP Initiative (DC-ISP-ARCH-001)

Highest-value target. The addressing plan, routing architecture, resilience design and
deployment phasing are directly loadable — the emulation *verifies a document already
written* rather than inventing a design.

Modellable: logical topology, both transit options (Option A eBGP/ASN/IXP peering,
Option B single upstream), OLT-to-ONT logical distribution, customer VLAN structure,
mesh peering VLAN on the ONT, CGNAT/IPv6 dual-stack, failover paths.

Not modellable: everything physical in DC-ISP-TECH-001, all of Li-Fi, and the entire
contents of DC-ISP-POC-001 (BOM, costs, timeline, CRTC registration, pole attachments).

### 5.2 Mesh ISP / MNO layer

Approximate split: **60% runs on off-the-shelf software, 25% must be written,
15% is not modellable.**

**Runs today:** BATMAN-adv/Babel, Yggdrasil, NFD/CCN-lite, ION/µD3TN, Kamailio/Janus,
Open5GS + UERANSIM, CGNAT/IPv6, FRR/BGP, Squid/Varnish/IPFS, ACA-Py, chain devnet.

**Must be written — nothing off the shelf does any of it:**

1. **Metering and attestation agent.** Proof-of-Relay, Proof-of-Bandwidth,
   Proof-of-Latency, Proof-of-Cache. Specified, not built. The token economy has no
   input without it. *This is the single load-bearing novel component.*
2. **Intent compiler.** Translates the declarative intent block (`min_bw`, `max_rtt`,
   `jitter_max`, `privacy`, `reliability`, `budget`) into routing policy, `tc` classes
   and path selection.
3. **FCN resolution layer** — blocked on the decision in DC-SIM-008 §2.
4. **DAO policy bridge.** On-chain registry → OPA → enforced node configuration.
5. **Billing and settlement.** Metering output → revenue split → payout.

**Not modellable:** RF and spectrum, SIM provisioning, carrier interconnect, PSTN/SS7
reality, TEE-backed attestation, spectrum leases, MVNO agreements, CRTC obligations.

**Minimum condition for a faithful mesh ISP run:** the metering agent. Everything else
can be assembled from packages in a few weekends. Without it the result is a competent
mesh network with a token diagram attached to it.

### 5.3 Distributed storage

Best fit in the ecosystem. Replication, erasure coding, quorum and self-healing are
defined by network behaviour, so they model faithfully. Kill a site mid-write, restore,
observe reconciliation — a real result.

### 5.4 Distributed compute

K3s scheduling, node eviction and pod rescheduling on site loss are faithful. WASM
runtimes execute correctly, covering the FCN function execution model. All nodes share
one host CPU: **scheduling decisions are faithful, capacity decisions are meaningless.**

### 5.5 Local LLM and distributed AI

Weakest fit. See §3.4. Workable pattern: run **one** real Ollama instance; make every
other inference node a stub emitting request/response traffic with realistic payload
sizes and timing. The answerable question is what inference traffic does to the network.

### 5.6 Media and adjacent verticals

D-Health, D-Learn, D-Finance, D-Market, D-Stream all run as containers and exercise the
network faithfully — but individually teach very little. A parameterised stub emitting
the same traffic profile produces identical network results at a fraction of the cost.
**Build the stub; do not deploy twelve real applications.**

Media has one exception: real video through a real player is the best available
demonstration artefact. See DC-SIM-004 Scenario 5.

### 5.7 SHI node

The emulation shows the **network and service plane only** — approximately half the
specification.

Visible: DC-OS boot and service startup order, DID agent, vault services, storage
replication to peers, WireGuard tunnel, nftables segmentation between household and
service VLANs, DNS/DHCP, upstream failover, UI behaviour under degradation, recovery
after partition, config drift across a fleet.

Invisible: the entire five-tier hardware architecture, all sensing tiers (Levels 1–5),
power, battery, solar, thermal, enclosure, and real on-device inference performance.

### 5.8 Campus network

Closest to complete coverage, because a campus is mostly a network.

Visible: core/distribution/access topology, VLAN design, inter-VLAN routing, STP,
EtherChannel, DHCP snooping, port security, 802.1X policy logic, ACLs and zone
segmentation, redundancy, multi-building routing, offered-load capacity planning.

Invisible: wireless entirely — including AP placement, roaming and RF planning, which
is usually the hardest part of a real campus design. Also PoE budgets, cable runs and
distances, closet placement, ASIC/TCAM behaviour, and every physical device
(blue light poles, cameras, Level 4/5 sensing under DC-SENSE-SERVICE-001).

**Comparative note.** For SHI the emulation covers the smaller half — it is a hardware
product with software on it. For campus it covers the larger half — it is a network
with hardware attached. Campus therefore yields more validated design per hour spent.

---

## 6. What the programme cannot answer, at any fidelity

Recorded so that no write-up overclaims.

| Domain | Examples |
|---|---|
| Physical | RF, optics, weather, power, thermal, mounting |
| Hardware validity | BOM correctness, supply, field durability |
| Economic | Unit economics, token velocity, 68/20/10 solvency, whether $16–30K suffices |
| Human | Whether members vote; whether governance resists capture; cooperative dynamics under financial stress |
| Regulatory | CRTC, spectrum, pole attachments, interconnect |
| Temporal | Month-18 behaviour — cert expiry, disk fill, drift, upgrade debt |
| Demand | Whether anyone wants this at a price that works |

The last row is the largest unanswered question in the ecosystem and is not technical.
The emulation answers *does the network design hold*. It was never going to answer the
other one.

---

## 7. Complementary tools

| Tool | Covers | When |
|---|---|---|
| **containerlab** | YAML topologies, 100+ containers, git-versioned, CI-runnable | All repeatable runs |
| **ns-3** | 802.11 PHY/MAC, interference, propagation | Any wireless/mesh RF claim |
| **GNU Radio / Sionna** | RF signal chains, propagation | Beamforming, SDR |
| **NumPy / MATLAB** | Array processing, delay-and-sum | Acoustic beamforming (DC-PLANE-001) |
| **Foundry / cadCAD** | Contract correctness, token economics | DC-SIM-007 layers 1–2 |
| **Real OpenWRT routers** | Actual mesh RF at desk scale | Mesh link-quality validation |

**Recommended division of labour:** GNS3 for the visual demonstration and the QEMU
DC-OS image; containerlab for anything run more than twice.
