---
source_conversation_uuid: fc99aa3d-f993-404c-8aee-09bc55305583
conversation_title: 'D-Central ISP implementation in Haiti'
created_at: 2026-08-13T03:06:36.336567Z
doc_id: DC-REG-001
description: 'Compiling a first-pass master registry of D-Central documents reconstructed from past conversations'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-REG-001 — Master Document Registry (First Pass)

**Status:** Draft v0.1 — reconstructed from a search across past conversations, not a complete inventory. Memory reports 500+ documents across 60+ named components; this pass surfaced the major ones by category. Treat this as a scaffold to correct and extend, not a finished registry.

**Why this exists:** DC-SIM-000 already lists `DC-REG-001` as its parent registry — this fills a slot you'd already reserved, not a new invention. Upload this to each Project's knowledge base once it's corrected, so new chats start with the map instead of rebuilding pieces of it.

**How to use it:** each time a new doc gets produced, add a row here before closing the chat. That single habit is what would have caught the `ProvisioningDAO` duplication and the SHI/connectivity gap before they sat unreconciled for months.

---

## 1. Foundational / meta

| ID | Scope | Status |
|---|---|---|
| DC-STATUS-001 | Honesty-discipline gap register — design vs. execution across every domain | ~95% designed, 0% executed (as of last update) |
| DC-GAP-001 | 27 open gaps feeding the critical path | Open |
| DC-SCALE-001 | Interactive scale economics, 1 to 10¹² nodes, Wright's Law cost curve | Complete (design) |
| DC-REG-001 | This document | Draft, this pass |

## 2. Core network & simulation

| ID | Scope | Status |
|---|---|---|
| DC-SIM-000 | Master index, stop condition, scope discipline for GNS3 programme | Complete (design) |
| DC-SIM-001 | Fidelity reference — what GNS3 can/can't model | Complete |
| DC-SIM-002 | Topology & build spec, derived from DC-ISP-ARCH-001 | Complete |
| DC-SIM-003 | DC-OS Buildroot dual-architecture build spec | Complete — load-bearing artefact |
| DC-SIM-004 | Test scenario catalogue, measurement methodology | Complete |
| DC-SIM-005 | Cloud bridge & external integration | Complete |
| DC-SIM-006 | Hardware integration roadmap, 4 regulatory thresholds | Complete |
| DC-SIM-007 | DAO governance simulation (3 layers) | Complete |
| DC-SIM-008 | Architecture decision record — 6 resolved decisions | Complete |
| DC-ISP-ARCH-001 | Source topology DC-SIM-002 derives from | Referenced, not re-surfaced this pass |
| DC-ISP-TECH-001 / -POC-001 | ISP technical/POC docs, FSO + GPON, Ottawa | Referenced |
| DC-ISP-HT-001 | Haiti pilot: non-PAP topology + node BOM | Complete — built this conversation |
| DC-MESHISP-ARCH-001 | Full MeshISP architecture synthesis | Complete — built this conversation |
| DC-FOUNDATION-01 | Physical Pi 5 lab build, executed, 1,727-line report, 9 closed defects | **Executed** — the one node that's real |

## 3. Identity, governance, OS

| ID | Scope | Status |
|---|---|---|
| Sovereign DAO OS (13-part ref) | Identity, governance, networking, OS/kernel, device ecosystem, energy, apps, economics, distribution, scaling | Complete (design) |
| D-OS variants spec | Desktop/Mobile/Internetwork/Web, eBPF enforcement, kernel architecture | Complete |
| DC-SHI-SPEC-001 | Consolidated 5-tier SHI node master spec | Complete |
| DC-SHI-SPEC-002 | Three-profile node taxonomy (Residential/Commercial-Campus/High-security-Research) | Confirmed, canonicalized |
| CTS v1–v5 | Cooperative Transparency Stack — labor/identity foundation | Complete |
| D-CERT | Web3 certification, 12 domain DAOs, soulbound tokens | Complete |

## 4. Financial / economic

| ID | Scope | Status |
|---|---|---|
| DC-LKB-001/002 | Lakou Protocol v1 — family banking | Complete |
| DC-LKB-003 | Lakou Protocol v2 — Universal Decentralized Banking OS, 9 vault types | Complete |
| DC-LKF-001 | Lakou Fraternity Network — men's social club vertical | Complete |

## 5. Security vertical

| ID | Scope | Status |
|---|---|---|
| OpenSecure suite | OS-PACS, OS-GUARDIAN, OS-PATROL, OS-SENTINEL, OS-CONCIERGE | Complete (design), Stage 1 (subcontract installs) is the live bootstrap path |
| OS-ELECT-ARCH-002 (+ADD-001) | Haiti CIN architecture + card back spec | Complete |
| OS-APEX-CRED-001 | Extreme high-security credential | Complete — RESTRICTED |
| OS-OSIP-001 | Sovereign Identity Platform, forensic query, ZK consent | Complete |
| OS-DCINT-001 | D-Central integration, data sovereignty incentive layer | Complete |
| OS-CPFQ-001 | Consented Private Forensic Query | Complete |

## 6. Other verticals

| ID | Scope | Status |
|---|---|---|
| DC-MESHEATS-ARCH-001 | Home-chef delivery co-op, DC-TPL replicable template | Complete — CA MEHKO counties as launch geography |
| SkyLedger (DC-SKY-PLATFORM-001, -MOD-001, -INFRA-001, -SDK-001) | Drone XaaS, 12-service catalogue | Complete |
| DC-TM-BOM-002/003, DC-TM-TOOLS-001, DC-TM-DS-001 | TrafficMesh/CivicMesh hardware BOM, custom PCB | Complete — STN2120 correction applied |
| Sod Boys FieldOps | WhatsApp-native field ops, Pi 5 + OpenClaw | Built, 17-file repo scaffold |
| classIQ / D-Learn | Touch-frame + edge node classroom system | Complete (design) |

## 7. Academic / personal

| ID | Scope | Status |
|---|---|---|
| Master Timeline | V23+, credential path Algonquin → Harvard postdoc | Living document |
| CST8200/8305/8315/8324 lab manuals | Windows/Linux/routing/programming coursework | Executed per-course |
| MAT8002 materials | Boolean algebra, number systems, stats/probability | Complete |
| GEN1957 | Prometheus review, "The Jupiter Line" short story | Complete |
| D-CERT curriculum mapping | Algonquin course → D-Central equivalent | Complete |

---

## Known gaps in this registry itself

- Numeric BOM/cost docs (DC-LKB module pricing, SkyLedger SDK pricing) not itemized here — this pass tracked architecture docs, not every artifact.
- DC-SWARM-001, DC-PLANE-001, DC-SITE-001 confirmed to exist in memory but not re-surfaced by this search pass — add on next pass.
- No timestamps captured per doc — worth adding a "last touched" column so staleness is visible at a glance, the same instinct behind DC-STATUS-001.
- This document was assembled from conversation search snippets, not a full read of each source chat — treat titles/status as directionally right, verify before treating as authoritative.
