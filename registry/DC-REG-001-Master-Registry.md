# DC-REG-001 — Master Document Registry (First Pass)

**Status:** Draft v0.1 — reconstructed from a search across past conversations, not a complete inventory. Memory reports 500+ documents across 60+ named components; this pass surfaced the major ones by category. Treat this as a scaffold to correct and extend, not a finished registry.

**Why this exists:** DC-SIM-000 already lists `DC-REG-001` as its parent registry — this fills a slot you'd already reserved, not a new invention. Upload this to each Project's knowledge base once it's corrected, so new chats start with the map instead of rebuilding pieces of it.

**How to use it:** each time a new doc gets produced, add a row here before closing the chat. That single habit is what would have caught the `ProvisioningDAO` duplication and the SHI/connectivity gap before they sat unreconciled for months.

---

## 0. Pending ingestion — staged, not yet processed (2026-09-07)

External sources identified as containing D-Central material not yet in this repo, cloned/copied into
`raw-export/` (git-ignored, per this repo's own convention — staged for extraction, not versioned) as a
checkpoint before the real Stage 3-8 pipeline work runs against them. **None of this has been classified,
deduped, or consolidated yet** — this row exists so the checkpoint survives even though the staged files
themselves aren't tracked in git.

| Source | Location | Scope | Status |
|---|---|---|---|
| 16 GitHub repos (RedjiJB account) | `raw-export/external-repos/` | D-Central, dcentral-platform, dcentral-edge-gateway, dcentral-meshv1, dcentral_solodev, D-Central-Haiti, haiti-digital-commons, fcp-platform, federated-trades-program, federated_graphql, federated_learning_platform, hybridisp-approach, d-central-development-timeline, MeshEats (+ 3 confirmed-empty: dcentral-mesh-poc, MeshCash, D-Central-Diagrams) | Cloned. First-pass architecture-inference summaries exist for all 4 code repos, the 4 Haiti/connectivity repos, and the 5 federated/timeline repos in `raw-export/external-repos-extracted/*.md` (also git-ignored) — explicitly a reconnaissance pass, not exhaustive (see caveats below). One finding already promoted into a committed doc: DC-STATUS-001 §6, code-level corroboration of the 95%/0% doctrine. |
| OneDrive `D Central` folder | `raw-export/onedrive-d-central/` | 815 files, 673 docs (582 md, 91 docx, 12 pdf, 7 txt), 52MB, pre-organized into `00-foundation` through `13-pocs` + `modules/`/`homenode/`/`dev-tools/`, with its own `_archive/` of known duplicates | Copied in full, verified (815 files, 52MB match source). Not yet inventoried category-by-category or classified. |

**Known resolved issue:** `dcentral-meshv1` initially failed to clone — 1,560 of 6,915 tracked blobs in that
repo have a malformed filename pattern (`RealFilename.ext / fake description text` baked into the path
itself, apparently from an AI-generated file-tree scaffold that used `/` as a field separator instead of a
path separator), which Windows rejects as invalid paths. Resolved via a sparse-checkout allowlist of the
5,355 well-formed paths; ~5,120 files actually checked out (a handful of edge-case remainder paths still
excluded, all confirmed to be more of the same junk-placeholder pattern, not real content).

**Known extraction-completeness caveats, not yet resolved (see the architecture-inference docs' own
caveats):** no `.docx` or `.pdf` files were read in this pass (both formats appear in the corpus, e.g.
`sovereign_dao_os_architecture_v1.docx`); the largest Haiti strategy docs were only partially read or
skimmed by section headers rather than read in full; a "critical analysis of the Haiti mesh network plan"
counter-source was identified but not read; MeshEats and D-Central-Haiti had only a subset of their real
files read, not their full corpora. Treat the existing extraction summaries as a map for where to focus a
deeper pass, not as a substitute for one.

**Next steps (not started):** full-depth extraction/reading of the above, then real dedup (this corpus has
confirmed internal duplication — e.g. the same OSS-integration bill-of-materials pasted 3+ times inside one
Haiti doc, the same mesh tier model reprinted 4+ times with escalating language across separate files) and
topic-synthesis/consolidation passes per [[DC-DEDUP-STD-001]]/[[DC-TOPIC-SYNTH-STD-001]]/
[[DC-CONSOLIDATOR-STD-001]], category-by-category for the OneDrive folder.

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
| DC-COMPUTE-SILICON-ARCH-001 | Compute Silicon Class (CPU/GPU/FPGA/CGRA/eFPGA/ASIC) hierarchy, discovery pipeline, thin-client tie-in — fills the empty SHI Tier 3 (Compute & Storage) slot in UNIFIED_SOURCE_OF_TRUTH_V24 §3.11.3 | Complete (design), 0% executed — added this pass |

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
