---
source_conversation_uuid: 1d87c741-469a-42cd-a427-2182a5784b40
conversation_title: 'Processing conversation exports and registry setup'
created_at: 2026-08-23T06:32:27.243833Z
doc_id: DC-REG-001
description: 'DC-REG-001 v0.2 — merged registry combining hand-curated and auto-extracted entries'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
status: "duplicate"
duplicate_of: "registry/DC-REG-001-Master-Registry-v0.2.md"
duplicate_reason: "exact body match (verified byte-for-byte) -- already extracted by hand into registry/ in an earlier session, this conversation-artifact copy is redundant"
---

# DC-REG-001 — Master Document Registry (v0.2)

**Status:** v0.2 — merged from hand-curated draft (v0.1) + auto-extraction from 713 conversation exports  
**Total unique documents found:** 135 (100 DC-*, 4 OS-*, 28 academic)  
**Last updated:** August 23, 2026  
**Coverage:** Extracted via pattern matching across full conversation export; treat status as directionally correct, titles/scopes as starting points for verification

---

## Critical Use Cases for This Registry

### 1. Starting a new chat in a Project?
Check DC-REG-001 (in the Project knowledge base) to see if you're about to rebuild something that exists.

### 2. Finding an existing document?
Search this registry first. If it's not here but you think it should be, it's either:
- A recent document not yet in the registry (add it when closing the chat)
- A document that needs a formal ID assigned
- A lost doc trapped in a past conversation (use conversation search with keywords)

### 3. Reconciling a gap?
(e.g., "ProvisioningDAO is mentioned in three places with different scopes")  
Use this registry to see all mentions, then follow the `source_conversations` links to read them side-by-side.

---

## Registry Format

Each table row has:
- **ID** — formal document identifier (DC-XXX-001, OS-YYY-ZZZ, etc.)
- **Scope** — one-sentence description of what it covers
- **Status** — complete / draft / referenced-only / executed / unclear
- **Mentions** — how many conversations mention this doc (from auto-extraction)
- **Last touched** — approximate, based on most recent source chat

---

# Core D-Central Documents (100 unique DC-* IDs)

## 1. Architecture & Design (Foundational)

| ID | Scope | Status | Mentions | Notes |
|---|---|---|---|---|
| DC-ARCH-001 | Complete technical documentation for primary architecture | Complete | 1 | 1,356 paragraphs |
| DC-SCALE-001 | Interactive scale economics, Wright's Law cost curve across 1 to 10¹² nodes | Complete | — | Load-bearing design artifact |
| DC-STATUS-001 | Honesty-discipline gap register — design vs. execution across every domain | ~95% designed | — | Meta-registry for implementation gaps |
| DC-GAP-001 | 27 open gaps feeding the critical path | Open | 1 | Tracking doc |
| DC-REG-001 | This document — master document registry | Draft | — | v0.2 |

## 2. Infrastructure & ISP Initiatives

| ID | Scope | Status | Mentions | Notes |
|---|---|---|---|---|
| DC-ISP-ARCH-001 | ISP technical architecture (Ottawa, FSO + GPON topology) | Complete | Ref | Referenced by DC-SIM-002 |
| DC-ISP-TECH-001 | ISP technical specifications (FSO backhaul, GPON last-mile) | Complete | Ref | POC-phase detail |
| DC-ISP-POC-001 | ISP proof-of-concept documentation | Complete | Ref | Field deployment doc |
| DC-ISP-HT-001 | Haiti pilot: 40-household topology and node BOM | Complete | 1 | Non-PAP region, 3-tier topology |
| DC-MESHISP-ARCH-001 | MeshISP full architecture synthesis | Complete | 1 | Unified ISP protocol spec |

## 3. Simulation & Lab (GNS3 Programme)

| ID | Scope | Status | Mentions | Notes |
|---|---|---|---|---|
| DC-SIM-000 | Master index and stop condition for GNS3 simulation programme | Complete | — | Stop condition: DC-OS boots on Pi 5, peers into simulated topology |
| DC-SIM-001 | Fidelity reference — what GNS3 can/can't model | Complete | — | Constraints registry |
| DC-SIM-002 | Topology & build spec, derived from DC-ISP-ARCH-001 | Complete | — | GNS3 blueprint |
| DC-SIM-003 | DC-OS Buildroot dual-architecture build spec | Complete | — | Load-bearing artefact |
| DC-SIM-004 | Test scenario catalogue and measurement methodology | Complete | — | QA framework |
| DC-SIM-005 | Cloud bridge & external integration | Complete | — | Integration layer |
| DC-SIM-006 | Hardware integration roadmap (4 regulatory thresholds) | Complete | — | Staging gates |
| DC-SIM-007 | DAO governance simulation (3 layers) | Complete | — | Gov layer modeling |
| DC-SIM-008 | Architecture decision record — 6 resolved decisions | Complete | — | Design rationale |
| DC-FOUNDATION-01 | Physical Pi 5 lab build (executed, 1,727-line report, 9 closed defects) | **Executed** | — | The one real node that exists |

## 4. Identity, Governance, Operating System

| ID | Scope | Status | Mentions | Notes |
|---|---|---|---|---|
| **D-OS variants spec** | Desktop/Mobile/Internetwork/Web, eBPF enforcement, kernel architecture | Complete | — | Four deployment profiles |
| DC-SHI-SPEC-001 | Consolidated 5-tier SHI node master spec | Complete | — | Canonicalized reference |
| DC-SHI-SPEC-002 | Three-profile node taxonomy (Residential/Commercial-Campus/High-security-Research) | Complete | — | Topology types |
| **CTS v1–v5** | Cooperative Transparency Stack — labor identity & consent foundation | Complete | — | Multi-version progression |
| **D-CERT** | Web3 certification (12 domain DAOs, soulbound tokens) | Complete | — | Credentialing system |
| DC-DEVENV-001 | Development environment spec | Unclear | 1 | — |

## 5. Financial & Economic

| ID | Scope | Status | Mentions | Notes |
|---|---|---|---|---|
| DC-LKB-001 | Lakou Protocol v1 — family banking spec | Complete (Executed) | 2 | Foundation banking system |
| DC-LKB-002 | Lakou Protocol v2 — API design, governance, LMIS, UX flows | Complete | 1 | Enhanced version |
| DC-LKB-003 | Lakou Protocol v3 — Universal Decentralized Banking OS with 9 vault types | Complete | 1 | Full protocol spec |
| DC-LKF-001 | Lakou Fraternity Network — men's social club vertical | Complete (Executed) | 2 | Third-place vertical |
| DC-MONETARY-001 | Multi-tier monetary architecture | Unclear | 3 | Integration point for finance layers |
| DC-FIN-001 | Financial system (referenced in other contexts) | Referenced-only | 1 | — |

## 6. Security Vertical (OpenSecure Integration)

| ID | Scope | Status | Mentions | Notes |
|---|---|---|---|---|
| **OpenSecure suite** | OS-PACS, OS-GUARDIAN, OS-PATROL, OS-SENTINEL, OS-CONCIERGE | Complete (design) | — | Physical-cyber convergence platform |
| OS-ELECT-ARCH-002 | Haiti CIN architecture + card back spec | Complete | Ref | Sovereign identity system |
| OS-APEX-CRED-001 | Extreme high-security credential | Complete | — | RESTRICTED |
| OS-OSIP-001 | Sovereign Identity Platform (forensic query, ZK consent) | Complete | Ref | Privacy-preserving identity layer |
| OS-DCINT-001 | D-Central integration (data sovereignty incentive) | Complete | Ref | — |
| OS-CPFQ-001 | Consented Private Forensic Query | Complete | Ref | Zero-knowledge compliance |

## 7. Verticals: MeshEats, SkyLedger, Sod Boys, D-Learn

| ID | Scope | Status | Mentions | Notes |
|---|---|---|---|---|
| DC-MESHEATS-ARCH-001 | Home-chef delivery co-op architecture (DC-TPL replicable template) | Complete | — | CA MEHKO counties as launch geography |
| **SkyLedger suite** (DC-SKY-*) | Drone XaaS platform with 12-service catalogue | Complete | — | Full platform spec |
| DC-SKY-PLATFORM-001 | SkyLedger core platform | Complete | — | Service orchestration |
| DC-SKY-MOD-001 | SkyLedger modules | Complete | — | Modular components |
| DC-SKY-INFRA-001 | SkyLedger infrastructure layer | Complete | — | Deployment spec |
| DC-SKY-SDK-001 | SkyLedger SDK | Complete | — | Developer toolkit |
| **Sod Boys FieldOps** | WhatsApp-native field operations (Pi 5, OpenClaw, Claude Sonnet/Haiku backend) | Built | — | 17-file repo scaffold |
| **classIQ / D-Learn** | Touch-frame + edge node classroom system | Complete (design) | — | Education vertical |
| DC-TM-BOM-002/003 | TrafficMesh/CivicMesh hardware BOM | Complete | — | Custom PCB spec (STN2120 correction) |
| DC-TM-TOOLS-001 | TrafficMesh/CivicMesh tools | Complete | — | — |
| DC-TM-DS-001 | TrafficMesh/CivicMesh data schema | Complete | — | — |

## 8. Governance, Coordination, Sensing (Advanced)

| ID | Scope | Status | Mentions | Notes |
|---|---|---|---|---|
| DC-SWARM-001 | Stigmergic coordination protocol | Confirmed (Executed) | — | **Known gap**: not in extraction pass |
| DC-PLANE-001 | Multi-plane sensing architecture (7 planes: acoustic beamforming, UWB, Li-Fi, mmWave, etc.) | Confirmed (Executed) | — | **Known gap**: not in extraction pass |
| DC-SITE-001 | AI-coordinated labor management using biomimicry principles | Confirmed (Executed) | — | **Known gap**: not in extraction pass |
| DC-HMCS-002 | HMCS whitepaper update for full design system | Unclear | 1 | Work-in-progress |

## 9. Emerging / Exploratory

| ID | Scope | Status | Mentions | Notes |
|---|---|---|---|---|
| DC-AGD-001 | AI-generated DAO governance | Executed | 3 | Bio-inspired construction automation context |
| DC-AGD-002 | DAO governance suite (3-DAO model) | Complete | 1 | — |
| DC-AGD-003 | DAO governance integration | Executed | 2 | — |
| DC-AGENT-001 | Service mesh architecture (Docker + Cloudflare) | Unclear | 1 | Blast-radius isolation |
| DC-ASSET-001 | Decentralized networks for construction/landscaping | Unclear | 3 | — |
| DC-BEAM-001 | Audio beams + wearable LENS for private comms | Unclear | 1 | Advanced sensing |
| DC-BEAM-002 | Directional display tier (later phase) | Unclear | 1 | — |
| DC-B2B-001 | B2B operational visibility in decentralized construction | Executed | 1 | Visualization tool |
| DC-COOP-001 | Company rebuilding using D-Central principles | Complete | 2 | Integration reference |
| DC-COMPUTE-001 | Compute scheduling and governance | Executed | 2 | Network effects driver |
| DC-ENERGY-001 | Energy system configuration | Unclear | 1 | Victron + EG4 integration |
| DC-ENERGY-002 | VRM portal integration | Unclear | 1 | — |
| DC-ENERGY-003 | VPP enrollment & demand response | Unclear | 1 | Hydro Ottawa net metering |
| DC-ENERGY-004 | Commissioning checklist | Unclear | 1 | — |
| DC-ENTERPRISE-001 | White-label ecosystem configurator | Unclear | 1 | System count and configuration |
| DC-EVC-001 | EV conversion business for vehicles/equipment | Unclear | 1 | — |
| DC-FOS-001 | OSIRIS platform integration (visualization + incident overlay) | Executed | 3 | — |
| DC-FRACTAL-001 | Fractal property finance (self-financing expansion) | Executed | 2 | Stage financing model |
| DC-FULLSUITE-001 | Additive maximalist feature set | Unclear | 1 | Sensor node expansion, tiering strategy |
| DC-GOV-002 | DAO governance (referenced) | Referenced-only | 2 | — |
| DC-HAITI-001 | Haiti-specific deployment considerations | Unclear | 1 | — |
| DC-IMPACT-001 | Impact measurement | Unclear | 1 | — |
| DC-LIC-001 | Licensing/operations model | Unclear | 1 | — |
| DC-MOGUL-001 | Vault risk model | Unclear | 1 | Loss reserves, portfolio thinking |
| DC-MSOC-001 | Mobile SOC center setup | Unclear | 1 | — |
| DC-DISPATCH-002 | Dispatch system (DID-based routing with VC revocation) | Draft | 1 | Fail-closed design |
| DC-DMCA-001 | DMCA/maritime law integration | Draft | 1 | International scope |
| DC-NET-001 through DC-NET-010 | Networking subsystems (10 specs) | Mixed (1–3 executed/unclear) | — | Routing tiers, DNS, tunnel, failover |
| DC-DEV-001 | Routing tier design (fast vs. accuracy vs. rules) | Executed | 1 | — |
| DC-CAMPUS-001, -002 | Campus node topology options | Unclear | — | — |
| DC-CAMPUS-002 | Individual homes + shared yard structure | Unclear | — | — |

---

# Academic & Personal Documents

| ID | Scope | Status | Mentions |
|---|---|---|---|
| **Master Timeline** | V23+, credential path Algonquin → Harvard postdoc | Living document | — |
| **CST8182–8609** | Algonquin course codes (28 courses tracked) | Mixed (unclear → complete) | 1 each |
| **MAT8002** | Boolean algebra, number systems, stats/probability (completed) | Complete | 1 |
| **GEN1957** | Prometheus film review + "The Jupiter Line" short story | Complete | 1 |

---

## Known Gaps in This Registry

### Intentionally Deferred (Exist, Not Surfaced in This Pass)
- DC-SWARM-001 (stigmergic coordination)
- DC-PLANE-001 (multi-plane sensing)
- DC-SITE-001 (biomimicry labor management)

### Missing Numeric/Cost Details
- DC-LKB module pricing and SKU breakdowns
- SkyLedger SDK pricing and service tiers
- Drone operation cost models

### Missing Timestamps
This registry tracks status but not "last touched" — worth adding a `updated_at` column in the next refresh so you can see which docs are stale.

### Extraction Method Limitations
- Extracted via regex pattern matching across 713 conversations
- Status inferred from surrounding text (may be directionally wrong)
- Titles are doc IDs only — true titles pulled from DC-REG-001 draft or interpolated
- Some course codes (CST, MAT, GEN) are documents; others are just references

---

## Reconciliation Discipline (Next Steps)

1. **Verify top-priority documents** (DC-ISP-HT-001, DC-MESHEATS-ARCH-001, DC-LKB-003, OpenSecure suite)  
   Do the statuses match your actual progress?

2. **Collapse duplicates** where they exist  
   (E.g., if ProvisioningDAO appears in three places with different scopes, which one is canonical?)

3. **Fill in the known gaps**  
   (DC-SWARM-001, DC-PLANE-001, DC-SITE-001 — you know these exist, add them with full scope)

4. **Add a "Last Touched" column** on next refresh  
   Use the `source_conversations` to pick the most recent mention date

5. **Run the extraction script quarterly**  
   `python3 build_registry_local.py /path/to/export` finds new docs automatically

---

## How to Use This Going Forward

- **In a Project chat:** Ask me "Have we built X before?" and reference DC-REG-001 in the knowledge base
- **Across Projects:** Paste this doc (or a summary) when you need to find something that spans multiple contexts
- **One-line-per-doc habit:** Every time you produce a new document, add a row here before closing the chat (DC-STATUS-001 discipline, applied one level up)

This is your source of truth. Keep it alive.


<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Duplicate of:** registry/DC-REG-001-Master-Registry-v0.2.md (unresolved path, see registry/materialized-manifest.json)

<!-- AUTO-GENERATED RELATED END -->
