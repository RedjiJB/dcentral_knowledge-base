---
source_conversation_uuid: 8f7a2740-7f7b-4f16-b483-d1e161ebb85e
conversation_title: '💬 I have an idea for the dcentra…'
created_at: 2026-08-08T03:34:00.540823Z
doc_id: DC-SIM-000
description: 'Master index for the DC-SIM document suite'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-SIM-000 — Network Simulation Programme, Master Index

| Field | Value |
|---|---|
| Document ID | DC-SIM-000 |
| Version | v1.0 |
| Date | August 2026 |
| Author | Toussaint Redji Jean Baptiste |
| Status | Draft — scoping complete, build not started |
| Parent registry | DC-REG-001 |

---

## 1. Purpose

This suite documents the scoping of a GNS3-based network emulation programme for the
D-Central ecosystem. It defines what can be modelled faithfully, what cannot, what must
be built to close the gap, and the path from emulation to physical deployment.

The programme has one primary objective and several secondary ones.

**Primary objective.** Convert DC-OS from a written specification into a bootable,
testable binary artefact, and verify the D-Central ISP network architecture
(DC-ISP-ARCH-001) before hardware is purchased.

**Secondary objectives.** Produce a CST-Networking portfolio artefact; generate offered-load
sizing inputs for procurement; establish a permanent staging environment for all future
configuration changes.

---

## 2. Document set

| ID | Title | Purpose |
|---|---|---|
| DC-SIM-000 | Master Index | This document |
| DC-SIM-001 | Fidelity Reference | What GNS3 can and cannot model, by layer |
| DC-SIM-002 | Topology & Build Specification | Node inventory, addressing, compute sizing |
| DC-SIM-003 | DC-OS Build Specification | Buildroot dual-architecture image |
| DC-SIM-004 | Test Scenario Catalogue | Executable scenarios and measurement method |
| DC-SIM-005 | Cloud Bridge & External Integration | Bridging real hardware and traffic |
| DC-SIM-006 | Hardware Integration Roadmap | Staged path from emulation to deployment |
| DC-SIM-007 | DAO Governance Simulation | Contract, economic, and enforcement layers |
| DC-SIM-008 | Open Architecture Decisions | Unresolved questions blocking implementation |

---

## 3. Scope discipline

This programme has a defined stop condition. It is recorded here because the D-Central
registry currently stands at approximately 95% designed and 0% executed
(DC-STATUS-001), and a simulation programme has an unusually high capacity to
generate artefacts that resemble progress without producing executable systems.

> **Stop condition.** DC-OS boots on the physical Raspberry Pi 5, peers into the
> simulated topology through the Cloud bridge, and passes Scenario 1 of DC-SIM-004.
> On reaching this: write up results, publish, stop.

**Target duration:** 4–6 weeks.

Everything in DC-SIM-006 stage 2 and beyond, all of DC-SIM-007 layer 3, and the entire
Mesh ISP/MNO stack described in DC-SIM-001 §5 are explicitly **out of scope for v1**.
They are documented so they are captured, not so they are built.

Indicators that scope has been breached:

- Adding a fourth site because the topology diagram looks unbalanced
- Standing up Open5GS before DC-OS boots
- Purchasing hardware to raise the node ceiling before the node ceiling has been hit
- Beginning ns-3 work of any kind

---

## 4. Reading order

For build: 003 → 002 → 004.
For scoping decisions: 008 → 001.
For deployment planning: 006 → 005.
For governance work: 007 → 008.

---

## 5. Related registry documents

| ID | Relevance |
|---|---|
| DC-ISP-TECH-001 | FSO/GPON hardware spec — source of physical parameters |
| DC-ISP-ARCH-001 | Addressing plan, routing, resilience — primary simulation input |
| DC-ISP-POC-001 | BOM, costs, 18-week timeline — consumer of sizing outputs |
| DC-SHI-SPEC-001 | SHI node spec — partially modellable (see DC-SIM-001 §7) |
| DC-FOUNDATION-01 | Existing Pi 5 lab build — hardware baseline |
| DC-STATUS-001 | Gap analysis — source of the scope discipline above |
| DC-REG-001 | Master registry |
