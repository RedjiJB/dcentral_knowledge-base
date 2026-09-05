---
source_conversation_uuid: 8f7a2740-7f7b-4f16-b483-d1e161ebb85e
conversation_title: '💬 I have an idea for the dcentra…'
created_at: 2026-08-08T03:34:00.540823Z
doc_id: DC-SIM-003
description: 'DC-OS Buildroot dual-architecture build specification'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-SIM-003 — DC-OS Build Specification

| Field | Value |
|---|---|
| Document ID | DC-SIM-003 |
| Version | v1.0 |
| Date | August 2026 |
| Author | Toussaint Redji Jean Baptiste |
| Status | Specification — build not started |
| Priority | **Highest in the programme** |

---

## 1. Why this document is first

The largest single return from the emulation programme is not the topology. It is that
GNS3 forces DC-OS to stop being a specification and become a bootable binary.

DC-OS currently exists as written architecture. Buildroot plus a QEMU node makes it a
thing that boots, fails, gets debugged, and gets fixed — and it is the same image that
lands on the Raspberry Pi 5. This is the first executable artefact in the D-Central
stack, and it alone justifies the programme.

Everything else in this suite is scaffolding around this image.

---

## 2. The architecture collision, and the resolution

**The problem.** The target hardware is aarch64 (Pi 5). GNS3 runs QEMU on an x86-64
host. An aarch64 guest on an x86-64 host runs under TCG with no KVM acceleration —
roughly 5–20× slowdown per node. Tolerable for one node; unusable for a multi-site
topology.

**The resolution.** Buildroot is designed so that target architecture is a build
variable, not a rewrite. Package selection, service configuration and the filesystem
overlay live in a `BR2_EXTERNAL` tree; two defconfigs reference the same tree with
different toolchains.

```
dcos-buildroot/                  ← BR2_EXTERNAL tree
├── external.desc                ← declares tree name/description
├── external.mk                  ← includes package makefiles
├── Config.in                    ← menuconfig entries for custom packages
├── configs/
│   ├── dcos_aarch64_defconfig   ← Pi 5 target, real hardware
│   └── dcos_x86_64_defconfig    ← GNS3 target, native speed
├── package/                     ← custom package definitions
│   ├── dcos-did-agent/
│   ├── dcos-vault/
│   └── dcos-metering/           ← see DC-SIM-001 §5.2
└── overlay/                     ← filesystem overlay, identical both targets
    ├── etc/
    └── opt/dcentral/
```

**Result:** same DC-OS, same services, same configuration files, different toolchain.
The emulation stays honest because it runs the actual image; it stays fast because the
image is native.

### 2.1 Buildroot over Yocto

Yocto's layer model pays off when a team maintains many products from a shared base.
This is one person who needs a bootable image within a quarter. Buildroot is
substantially simpler, builds faster, and produces smaller images.

Revisit only if multiple divergent hardware products need a shared BSP.

---

## 3. Image contents

| Component | Package | Purpose |
|---|---|---|
| Init | BusyBox init or systemd | Startup ordering |
| Routing | FRR | BGP, OSPF, BFD |
| Firewall | nftables | Segmentation, CGNAT |
| Tunnel | WireGuard | Inter-site mesh |
| Policy | OPA | DAO policy enforcement point |
| Identity | DID agent | See DC-SIM-008 §2 for resolution model |
| Metering | `dcos-metering` | **To be written** — DC-SIM-001 §5.2 |
| Observability | Structured logging to collector | Required for all scenarios |
| Config | Ansible-managed or Nix-declared | Shared with real hardware |

### 3.1 Output targets

| Target | Format | Consumer |
|---|---|---|
| x86-64 | `.qcow2` | GNS3 QEMU appliance |
| aarch64 | `.img` (SD/NVMe) | Raspberry Pi 5 |

Both must build reproducibly from a single `make` invocation with the appropriate
defconfig, from a clean checkout.

---

## 4. GNS3 appliance registration

The qcow2 is registered as a custom appliance template via a `.gns3a` file specifying:
architecture, default RAM (1 GB), NIC model (`virtio-net-pci`), adapter count (minimum
4 for a gateway), console type (`telnet` on serial), and category (`router`).

Fidelity is 1:1 by construction — every node boots the actual artefact, not a model of it.

---

## 5. What the emulation tests, and what it does not

**Tested faithfully:** boot sequence, init and service startup order, service dependency
failures, recovery after unclean shutdown, configuration drift across a fleet, upgrade
paths, all network and service-plane behaviour.

**Not tested:** anything hardware-specific — Pi thermals, GPIO, real NIC drivers, power
loss mid-write, SD card corruption, TPM and secure boot, real inference performance.

These require the physical Pi bridged in through the Cloud node (DC-SIM-005), which is
why that bridge is the highest-leverage step in the programme.

---

## 6. Acceptance criteria

The image is considered complete for v1 when:

1. Both defconfigs build from clean checkout with no manual intervention
2. The x86-64 image boots in GNS3 to a login prompt in under 30 seconds
3. FRR establishes BGP with a neighbour and installs routes
4. nftables loads the segmentation ruleset at boot
5. WireGuard establishes a tunnel to a peer site
6. The aarch64 image boots on the physical Pi 5
7. The Pi peers into the simulated topology through the Cloud bridge
8. Scenario 1 of DC-SIM-004 passes

**Criteria 6–8 constitute the programme stop condition (DC-SIM-000 §3).**
