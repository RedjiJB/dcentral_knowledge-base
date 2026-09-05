---
source_conversation_uuid: 8f7a2740-7f7b-4f16-b483-d1e161ebb85e
conversation_title: '💬 I have an idea for the dcentra…'
created_at: 2026-08-08T03:34:00.540823Z
doc_id: DC-SIM-005
description: 'Cloud bridge and external hardware integration reference'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
topic: "dcentral-simulation-lab-programme"
---

# DC-SIM-005 — Cloud Bridge & External Integration

| Field | Value |
|---|---|
| Document ID | DC-SIM-005 |
| Version | v1.0 |
| Date | August 2026 |
| Author | Toussaint Redji Jean Baptiste |

---

## 1. Mechanism

GNS3 nodes normally live in an isolated virtual network — packets travel between virtual
NICs and never reach anything outside. **The Cloud node is the door.**

Placed on the canvas, it exposes the host's interfaces as connection points. Linking a
topology node to it bridges that node's virtual NIC to something real. Traffic crosses
in both directions.

### 1.1 Bridge targets

| Target | Reach | Use |
|---|---|---|
| **Host loopback / host stack** | Host only | Browser reaches services inside the topology. All the media demo needs. |
| **TAP interface** | Host, isolated subnet | Topology on its own subnet without touching physical hardware |
| **Physical NIC** | Real LAN segment | **How the Pi 5 joins the topology** |
| **NAT node** (related, distinct) | Outbound only | Package installs, DNS, NTP, real APIs |

### 1.2 Directionality — the commonly missed point

**NAT is one-way out.** **Cloud is two-way.** External things can reach *into* the
topology, which is what makes real clients and real hardware possible.

---

## 2. What the bridge converts

The generalisable rule:

> The Cloud bridge converts **hardware you own** from invisible to visible, at the scale
> you own it. It never converts physics, distance, or population.

| Bridged item | Becomes visible |
|---|---|
| Real Pi 5 | Boot, thermals under load, real inference speed, SD/NVMe behaviour, power draw if metered |
| Real camera | Actual stream characteristics |
| Real access switch | PoE, ASIC forwarding, port security on real silicon |
| Real AP | Wireless, roaming, RF — **for that one AP, in that one room** |
| Phone / laptop | Real client behaviour against simulated services |
| 802.1X supplicant | Authentication against simulated RADIUS |

### 2.1 What it does not convert

**Scale and geography.** One real AP is not a campus RF plan — co-channel interference
cannot be extrapolated from a single radio in an apartment. One real Pi is not a fleet.
Cable runs, distances, closet placement, PoE budget across 200 ports, and
building-scale propagation stay invisible regardless of how many devices are attached.

**Hardware not owned.** Bridging does not conjure an FSO head, an OLT, a LiDAR unit or a
blue light pole. This is a purchasing constraint, not a technical one.

**Physics.** Beamforming remains untouched at any level of bridging. A bridged array
yields the array's *output*, never the phase processing. Acoustic beamforming needs
microphones in a room; RF beamforming needs an SDR and GNU Radio. Neither is a network
problem — see DC-SIM-001 §3.3.

**Radio, structurally.** Bridging is Ethernet. An AP's RF behaviour stays entirely on the
wireless side of the AP; what arrives at the Ethernet port is frames with all RF context
stripped. Airtime metrics, retry counts, RSSI and interference never cross the bridge.
This is why a bridged AP does not give mesh RF — mesh link quality is a property of the
links *between* nodes, and those nodes are inside GNS3 with no radios.

### 2.2 The correct approach for mesh RF

Do not bridge — build. Two or three real OpenWRT routers running BATMAN-adv on actual
radios, then bridge that mesh into the topology as a single segment. Real airtime
metrics, real link quality, real healing on unplug. GNS3 supplies the WAN and services
around it.

Cost is roughly a few hundred dollars and yields more real mesh behaviour than any
amount of emulation. Still not a neighbourhood: no distance, no obstruction, no
co-channel neighbours, no mobility.

---

## 3. The full-hardware inversion

A structural point worth recording.

**At full hardware, GNS3 stops being the thing doing the work.** If every device is real,
the result is not a model of a network — it is a network, with GNS3 reduced to a bridge
with a diagram attached.

There is a crossover point. Early on, each piece of bridged hardware adds fidelity
cheaply. Past roughly half the stack, GNS3 becomes overhead: an emulator maintained to
orchestrate things that do not need emulating, with every fault now having two possible
homes.

**What remains out of reach even at full hardware:**

- **Geography.** FSO heads two metres apart on a bench give real optics and real
  alignment, but no atmospheric path, no fog, no scintillation over distance. A patch
  cable between real OLT and ONT is not 12 km of fibre with a 1:32 split.
- **Scale.** Twenty real subscribers is not four hundred. Contention, oversubscription
  and broadcast domain behaviour do not extrapolate from a bench.
- **Weather and season.** Ottawa freezing rain, Haitian heat and humidity, a year of
  thermal cycling. Time is not compressible.
- **The entire non-technical layer.** CRTC, poles, ROW permits, demand, unit economics.

**Conclusion.** Full hardware on a bench is a **staging lab**, not a model. Valuable —
it validates that the stack integrates before it goes on a pole. But it answers "does
this work when assembled," not "does this work when deployed." Only a field pilot answers
the second, which DC-ISP-POC-001 already scopes with its 18-week timeline.

**Corollary.** The emulation programme is valuable precisely *because* it is what can be
done without the hardware. Once the full stack exists, most of the programme's value has
already been spent.

---

## 4. Operational hazards

**Bridging leaks, both directions.** Topology DHCP offers, STP BPDUs and OSPF hellos
reach the real LAN; real LAN broadcast traffic enters the topology. Never bridge to a
production network segment.

**Promiscuous mode.** If the GNS3 VM runs under VMware or VirtualBox, the vswitch must
allow promiscuous mode. Otherwise bridging **fails silently** — no error, nothing
arrives.

**MAC learning.** Dozens of virtual MACs appearing on one physical port will annoy a
managed switch and may trip port security.

**The Cloud node is not a switch.** It is a bridge point. Multiple topology nodes needing
one physical segment require a switch between them and the Cloud node.

**Host NIC becomes the bottleneck**, shared with everything else on the machine.

---

## 5. Recommended physical build

A USB Ethernet adapter (approximately $20) dedicated to a small unmanaged switch
connecting only the Raspberry Pi and the GNS3 host. Bridge to that adapter.

Zero leak risk, real hardware in the topology, and the home network is unaffected. This
is the reference configuration for the programme stop condition.

```
┌──────────────────┐
│   GNS3 host      │
│  ┌────────────┐  │      ┌──────────────┐      ┌──────────┐
│  │ Topology   │──┼──────┤  USB NIC     ├──────┤ Unmanaged│
│  │ Cloud node │  │      │  (dedicated) │      │  switch  │
│  └────────────┘  │      └──────────────┘      └────┬─────┘
│                  │                                  │
│  Built-in NIC ───┼──── home network (isolated)      │
└──────────────────┘                            ┌─────┴─────┐
                                                │  Pi 5     │
                                                │  DC-OS    │
                                                └───────────┘
```
