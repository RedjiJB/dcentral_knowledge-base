---
source_conversation_uuid: 8f7a2740-7f7b-4f16-b483-d1e161ebb85e
conversation_title: '💬 I have an idea for the dcentra…'
created_at: 2026-08-08T03:34:00.540823Z
doc_id: DC-SIM-006
description: 'Staged hardware integration roadmap from emulation to deployment'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
topic: "dcentral-simulation-lab-programme"
consolidated_into: docs/DC-DCENTRAL-SIMULATION-LAB-RECONCILED-001.md
---

# DC-SIM-006 — Hardware Integration Roadmap

| Field | Value |
|---|---|
| Document ID | DC-SIM-006 |
| Version | v1.0 |
| Date | August 2026 |
| Author | Toussaint Redji Jean Baptiste |
| Status | Roadmap — stages 2+ out of scope for v1 |

---

## 1. Position of this document

Everything else in this suite is modelling. **This is a deployment path**, with the
emulation as scaffolding. It is the answer to the execution gap recorded in
DC-STATUS-001, and it is the point at which D-Central stops being designed and starts
being built.

The emulation topology does not retire as hardware arrives. It becomes the permanent
**staging environment** — every configuration change goes there first, indefinitely.

---

## 2. Two corrections to the intuitive ordering

**Sensors do not go first.** Sensors are the lowest-information, highest-liability
starting point. They teach least about network design, and any sensor that detects people
— cameras, Wi-Fi sensing, anything in Levels 1–3 of the sensing taxonomy — creates PIPEDA
obligations before a single routing result exists.

Environmental sensors (power, temperature, soil) are fine early. **People-sensing belongs
after a written consent and retention policy exists, not before.**

**Routers and edge go first**, because that is where the design risk sits. A real DC-OS
gateway on real hardware, in your own household, with your own devices as clients.
You are test user zero: no consent forms, no obligations, and every fault is yours to
debug at 2am without affecting anyone else.

---

## 3. The ladder

| Stage | Content | Threshold crossed |
|---|---|---|
| **1** | Simulated core, one real DC-OS gateway, own household as clients | — |
| **2** | Two real sites over real internet, WireGuard, no FSO | — |
| **3** | Environmental sensors, real captured traffic profiles | — |
| **4** | Friendly users, non-paying, explicitly labelled a lab | ⚠️ **Dependency** |
| **5** | People-sensing hardware | ⚠️ **PIPEDA** |
| **6** | Money changes hands | ⚠️ **Legal / regulatory** |
| **7** | Poles, ROW, FSO on real spans | ⚠️ **Municipal** |

**Stage 1 is the programme stop condition.** Stages 2–7 are documented so the path is
captured, not so they are started.

### 3.1 Threshold detail

**Stage 4 — dependency.** People now rely on the system. The ability to tear down and
rebuild on a whim is lost. Support becomes an ongoing obligation. Requires a rollback
path (§4) before entry.

**Stage 5 — PIPEDA.** Consent mechanism, retention policy, access and deletion process,
breach procedure. The `MetaverseConsentVC` question from the Mesh ISP integration
(DC-SIM-008 §5) becomes blocking here.

**Stage 6 — legal.** Corporate entity, CRTC Facilities-Based Provider registration, tax
registration and remittance. **The largest threshold in the ladder, and it is legal
rather than technical.** This is the "Company Zero incorporation and first invoice" step
identified as the critical ungated action in DC-STATUS-001.

**Stage 7 — municipal.** Hydro Ottawa pole attachment agreement
(`ss-permits@hydroottawa.com`), City of Ottawa ROW and road cut permits. Long lead times;
begin enquiries well before technical readiness.

### 3.2 Stage 2 is the cheapest real result available

Two real sites over real internet with WireGuard tests the entire multi-site design with
zero optics risk, zero regulatory exposure, and near-zero cost. It should be considered
the highest-value item immediately after the stop condition.

---

## 4. Two failure modes that will bite

### 4.1 No rollback path

From stage 4 onward, the ability to fail back to a known-working state while
experimenting is mandatory. Build it **before** it is needed:

- A second path that works when the primary is being modified
- A known-good configuration, tagged in git
- A documented, tested revert procedure
- A maintenance window convention communicated to users

### 4.2 Lab-to-production drift

The classic killer. Solved once, at the start:

> The same configuration management — Ansible or NixOS — drives both the emulated nodes
> and the real hardware, from the same git repository.

If the emulation and the deployment diverge, the emulation stops being evidence, and
every result produced by DC-SIM-004 becomes worthless. This is not optional and it is
cheap at stage 1, expensive at stage 4.

---

## 5. What the ladder still cannot answer

Even at stage 7, the following remain outside every technical process in this suite:

- Whether unit economics close
- Whether the 68/20/10 revenue split leaves node operators solvent
- Whether members vote, and whether governance resists capture
- Whether cooperative dynamics hold when money is involved
- Whether demand exists at a price that works

The last is the largest unanswered question in the ecosystem. It is answered by stage 6 —
a real invoice to a real customer — and by nothing before it.
