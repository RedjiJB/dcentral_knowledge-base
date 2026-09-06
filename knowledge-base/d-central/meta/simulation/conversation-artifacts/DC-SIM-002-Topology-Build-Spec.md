---
source_conversation_uuid: 8f7a2740-7f7b-4f16-b483-d1e161ebb85e
conversation_title: '💬 I have an idea for the dcentra…'
created_at: 2026-08-08T03:34:00.540823Z
doc_id: DC-SIM-002
description: 'Topology and build specification with node inventory and compute sizing'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
topic: "dcentral-simulation-lab-programme"
consolidated_into: docs/DC-DCENTRAL-SIMULATION-LAB-RECONCILED-001.md
---

# DC-SIM-002 — Topology & Build Specification

| Field | Value |
|---|---|
| Document ID | DC-SIM-002 |
| Version | v1.0 |
| Date | August 2026 |
| Author | Toussaint Redji Jean Baptiste |
| Primary input | DC-ISP-ARCH-001 |

---

## 1. Design basis

The topology implements the logical architecture already specified in DC-ISP-ARCH-001.
The addressing plan, VLAN structure and routing policy are **taken from that document,
not invented here.** This framing matters: the emulation is a verification of existing
design work, not a new design exercise.

Subject: **D-Central ISP Initiative (Ontario)**, not the Mesh ISP/MNO layer. Rationale
in DC-SIM-008 §1.

---

## 2. Four-tier topology

```
                    ┌─────────────────────────┐
   TRANSIT          │  Upstream AS (FRR)      │   ── NAT node (optional
                    │  own ASN, eBGP          │       real internet)
                    └───────────┬─────────────┘
                                │ eBGP
                    ┌───────────┴─────────────┐
   ISP EDGE / POP   │  Border-1 ── iBGP ── Border-2  │  (VyOS or FRR)
                    │           │                     │
                    │      OLT (Linux + tc HTB)       │
                    └───────────┬─────────────┘
                                │
   ACCESS           ═══ link filter profiles: FSO weather / GPON contention ═══
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
   ┌────┴─────┐           ┌─────┴────┐           ┌─────┴────┐
   │  SITE A  │           │  SITE B  │           │  SITE C  │
   │ DC-OS GW │◄─WireGuard┤ DC-OS GW ├─WireGuard►│ DC-OS GW │
   │ Switch   │           │ Switch   │           │ Switch   │
   │ 3× svc   │           │ 3× svc   │           │ 3× svc   │
   └──────────┘           └──────────┘           └──────────┘
```

### 2.1 Node inventory

| Tier | Node | Backend | Image | RAM |
|---|---|---|---|---|
| Transit | Upstream AS | Docker | FRR | 512 MB |
| Transit | Internet | — | GNS3 NAT node | — |
| POP | Border-1 | QEMU | VyOS | 1 GB |
| POP | Border-2 | QEMU | VyOS | 1 GB |
| POP | OLT | Docker | Debian + `tc` | 512 MB |
| Site ×3 | DC-OS gateway | QEMU | **Buildroot qcow2 (DC-SIM-003)** | 1 GB |
| Site ×3 | Access switch | QEMU / Docker | IOSvL2 or Open vSwitch | 768 / 256 MB |
| Site ×3 | Vault service | Docker | Stub or real | 256 MB |
| Site ×3 | DID agent | Docker | ACA-Py | 512 MB |
| Site ×3 | Telemetry/camera source | Docker | Stub / MediaMTX | 256 MB |

**Totals:** 5 QEMU nodes, 3 switches, 10 containers. Approximately 12–14 GB.
Comfortable on a 32 GB host.

### 2.2 Access-tier impairment

FSO and GPON are represented as **link filter profiles, not devices.** Each POP-to-site
link carries a named condition set applied by script mid-run.

| Profile | Loss | Added latency | Jitter | Represents |
|---|---|---|---|---|
| `clear` | 0% | 0 ms | 0 ms | Clear air |
| `haze` | 1–2% | 5 ms | 2 ms | Light attenuation |
| `rain` | 8–15% | 20 ms | 10 ms | Heavy rain |
| `fog` | 30–45% | 60 ms | 30 ms | Fog / freezing rain — the severe Ottawa case |
| `outage` | 100% | — | — | Link down |

GPON contention is modelled at the OLT node with `tc` HTB: the split ratio is expressed
as contended upstream bandwidth shared across ONT nodes.

> These are **asserted conditions**, not simulated optics. Any results derived from them
> must be labelled as such.

---

## 3. Scenario decomposition

No single topology covers all edge cases, and attempting one produces an undebuggable
system. The programme is decomposed into four small topologies, each fitting in 32 GB.

| # | Topology | Contents | Answers |
|---|---|---|---|
| 1 | Routing core | Routers only, no services | Convergence, failover, BGP policy |
| 2 | Service partition | Services only, trivial network | Behaviour when a site is isolated |
| 3 | Policy propagation | Chain + OPA + gateways | Vote-to-enforcement time |
| 4 | Traffic and sizing | Stubs at load | Offered-load sizing |

Combined, these cover more than one large topology would, and each is independently
debuggable.

---

## 4. Compute sizing

| Tier | Spec | Capacity | Use |
|---|---|---|---|
| **Baseline** | 32 GB / 8 core / NVMe | ~25 QEMU or 60+ containers | Full four-tier topology. **Recommended starting point.** |
| **Comfortable** | 64 GB / 12–16 core | + Open5GS, one Ollama, storage cluster | Single-operator ceiling |
| **Distributed** | 3 × 32 GB | One compute per site | Real inter-site links |

**RAM is the binding constraint.** CPU matters less for idle topologies but spikes
during convergence and traffic generation. NVMe is not optional — booting twenty QEMU
images from a spinning disk is unworkable.

### 4.1 Distributed GNS3

GNS3 supports multiple compute servers under one controller; inter-host links run over
GRE tunnels between compute hosts.

**Solves:** RAM and CPU ceiling only.

**Does not solve:** the physical layer is still absent. Inter-host links carry real
latency and real MTU behaviour, but as uncontrolled host and LAN noise rather than
modelled conditions.

**Best application:** one compute per site, each Lakou running its own GNS3 host, sites
connected over real network. The inter-site WAN becomes genuine distance and genuine
packets, and a real Pi can be bridged into any of them.

**Requirements:**
- Identical GNS3 versions across all hosts
- MTU 1400 on tunnelled links, or expect silent fragmentation
- Single-host topology working first — debugging is materially harder once a fault
  could be GNS3, a firewall rule, or tunnel MTU

---

## 5. Force multipliers

**Stub mode.** One real instance per service class, N stubs. Every service must ship
with a `--stub` flag that emits realistic request/response traffic without doing real
work. A few hundred lines; the single largest capacity multiplier available.

**Service design constraints for emulation-testability.** All verticals must be built
with: configuration via environment variables, no hardcoded addresses, health endpoints,
structured logs to a collector, and stub mode. Applied from day one this costs nothing;
retrofitted it is expensive.

**containerlab for repeatable runs.** YAML-defined, git-versioned, 100+ nodes, runnable
in CI. Same host as GNS3, different tool.

**Shared configuration management.** Ansible or NixOS driving both the emulated nodes
and the real hardware from the same git repository. If the emulation and the deployment
diverge, the emulation stops being evidence. This is the standard lab-to-production
drift failure and must be solved before stage 2 of DC-SIM-006.

---

## 6. Repository layout

```
dcentral-sim/
├── dcos-buildroot/          # BR2_EXTERNAL tree — see DC-SIM-003
│   ├── external.mk
│   ├── external.desc
│   ├── Config.in
│   ├── configs/
│   │   ├── dcos_aarch64_defconfig
│   │   └── dcos_x86_64_defconfig
│   ├── package/
│   └── overlay/
├── gns3/
│   ├── dcentral.gns3project
│   ├── appliances/          # custom .gns3a definitions
│   └── configs/             # per-node config, version controlled
├── containerlab/
│   └── topologies/
├── profiles/
│   ├── traffic/             # MGEN definitions per service class
│   ├── fso/                 # weather condition sets
│   └── tc/                  # shaping scripts
├── scenarios/               # executable test scripts — see DC-SIM-004
├── results/                 # captures, timings, drop tables
└── docs/                    # this suite
```

---

## 7. Build order

1. DC-OS image builds and boots under QEMU (DC-SIM-003) — **the load-bearing step**
2. Scenario 1 topology: routers only, reachability sweep
3. Convergence testing with BFD
4. Add sites and services
5. Traffic profiles and shaping
6. Cloud bridge, physical Pi joins (DC-SIM-005)
7. Full scenario run, write-up, **stop**
