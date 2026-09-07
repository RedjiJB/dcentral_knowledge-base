# DC-DCENTRAL-SIMULATION-LAB-RECONCILED-001 — D-Central Simulation Lab Programme (DC-SIM Suite), Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `dcentral-simulation-lab-programme` (10 docs).

## Current understanding

A ten-document suite (DC-SIM-000 through DC-SIM-009), all conversation-artifact extractions from a
single authoring session, scoping a GNS3-based network-emulation programme whose primary objective is to
convert DC-OS from a written specification into a bootable, testable binary artefact and verify the
D-Central ISP network architecture (DC-ISP-ARCH-001) before hardware purchase. Unusually for this
pipeline, the suite is internally self-reconciling: DC-SIM-009 explicitly supersedes DC-SIM-008's open-
question status (not its analysis) via a `reconciliation_note` on both documents, verified accurate
against each document's own header claim, and no other cross-document conflict was found.

**DC-SIM-000, Master Index (incorporated):** defines the programme's primary objective (boot DC-OS,
verify DC-ISP-ARCH-001) and secondary objectives (a CST-Networking portfolio artefact, offered-load
sizing inputs for procurement, a permanent staging environment), the nine-document reading map, and an
explicit **stop condition** — DC-OS boots on a physical Raspberry Pi 5, peers into the simulated topology
through the Cloud bridge, and passes Scenario 1 of DC-SIM-004 — with a 4-6 week target duration and four
named scope-breach indicators (adding a fourth site for symmetry, standing up Open5GS early, buying
hardware before hitting the node ceiling, starting ns-3 work).

**DC-SIM-001, Fidelity Reference (incorporated):** the governing technical principle — "GNS3 runs real
software on virtual wires... it does not test capacity, and it contains no physical layer" — elaborated
across four emulation backends (QEMU 1:1 fidelity, Docker high-fidelity-userspace-only, Dynamips legacy-
only, IOU/IOL licence-restricted), three fidelity tiers (faithful: FRR/BIRD/VyOS routing, nftables/
WireGuard security, Open5GS+UERANSIM mobile core, IPFS/Ceph storage, K3s orchestration; approximated:
link bandwidth, FSO/GPON conditions, switching hardware; and not-modellable-at-all: RF/spectrum,
beamforming, optics, physical devices, TEE attestation, long-duration effects), and two explicitly named
"traps that produce actively wrong conclusions" (mesh link-quality metrics are fiction in GNS3; distributed
LLM tensor/pipeline-parallel inference will appear viable in emulation and fail in deployment because GNS3
links run at host memory speed). A per-subsystem coverage assessment for seven D-Central subsystems (ISP
Initiative — highest value, verifies an existing document rather than inventing a design; Mesh ISP/MNO
layer — 60% off-the-shelf/25% must-be-written/15% not modellable, with a metering-and-attestation agent
identified as "the single load-bearing novel component"; distributed storage — best fit; distributed
compute — scheduling faithful, capacity meaningless; local LLM — weakest fit, stub-based workaround;
media/verticals — build one real instance plus parameterized stubs; SHI node — network/service plane only,
roughly half the spec; campus network — closest to complete coverage). A table of what the programme
cannot answer at any fidelity (physical, hardware-validity, economic, human/governance, regulatory,
temporal, and demand questions), closing with a complementary-tools table (containerlab, ns-3, GNU Radio/
Sionna, Foundry/cadCAD, real OpenWRT routers).

**DC-SIM-002, Topology & Build Specification (incorporated):** a four-tier topology (transit/upstream AS,
ISP edge/POP with dual VyOS borders and a Linux+`tc` OLT, three access-tier sites each with a DC-OS
gateway/switch/three services) built explicitly from DC-ISP-ARCH-001's existing addressing/VLAN/routing
design rather than inventing a new one, with a full node inventory (5 QEMU nodes, 3 switches, 10
containers, ~12-14 GB total), a named link-impairment profile table (`clear`/`haze`/`rain`/`fog`/`outage`
representing FSO weather conditions as asserted, not simulated, optics), a four-scenario decomposition
(routing core, service partition, policy propagation, traffic/sizing) chosen so each independently fits
in 32GB and is independently debuggable, a three-tier compute-sizing table (baseline/comfortable/
distributed), a repository layout, and a seven-step build order culminating in the Cloud bridge and full
scenario run.

**DC-SIM-003, DC-OS Build Specification (incorporated):** identifies the DC-OS bootable-image build as
"the largest single return from the emulation programme" and "the first executable artefact in the
D-Central stack." Resolves the aarch64-target-vs-x86-64-host architecture collision via Buildroot's
`BR2_EXTERNAL` tree pattern (one filesystem overlay, two defconfigs — `dcos_aarch64_defconfig` for the
physical Pi 5, `dcos_x86_64_defconfig` for native-speed GNS3 emulation), explicitly preferring Buildroot
over Yocto for a single-developer, single-quarter timeline. Specifies image contents (FRR routing,
nftables firewall, WireGuard tunnel, OPA policy enforcement, a DID agent, and a not-yet-written
`dcos-metering` package), GNS3 appliance-registration parameters, and eight acceptance criteria — the last
three of which (aarch64 boots on physical Pi 5; Pi peers into the simulated topology via Cloud bridge;
Scenario 1 of DC-SIM-004 passes) are explicitly identified as constituting the programme's stop condition.

**DC-SIM-004, Test Scenario Catalogue (incorporated):** establishes that every scenario must be an
executable, git-commit-stamped script, never a manual click-through. Four ordered proofs (service
reachability — high confidence; convergence/failover — high confidence but relative-only, not an absolute
SLA figure; bandwidth sizing — explicitly low confidence, an offered-load argument rather than a
measurement; security segmentation — high confidence, run last because policy results are meaningless
until paths are known-good). A seven-step baseline Scenario 1 (boot, reachability sweep, baseline load,
FSO degradation stepping through the DC-SIM-002 profiles, hard link failure, segmentation assertions,
restore). A traffic-generation toolchain (iperf3, MGEN/D-ITG, Ostinato, scapy, tcpreplay with an explicit
constraint that captures require the network owner's written authorization). Scenario 5 (media under FSO
degradation, named the programme's best demonstration artefact) and Scenario 6 (partition and recovery
across storage/K3s/DID-VC/DTN/inference/media/UI/policy subsystems, with DTN bundle-queuing named "the
strongest single result available in this programme" and UI-under-degradation flagged as underrated).
Five mandatory write-up limitation disclosures (FSO/GPON asserted not simulated; bandwidth figures are
offered-load modelling not measurement; convergence figures are relative not absolute; mesh link-quality
metrics are fiction; no wireless/RF/physical-layer claim is supported by any result in the programme).

**DC-SIM-005, Cloud Bridge & External Integration (incorporated):** documents the GNS3 Cloud node as the
mechanism bridging virtual topology to real hardware, contrasted with the NAT node (Cloud is two-way,
NAT is outbound-only). A generalizable rule — "the Cloud bridge converts hardware you own from invisible
to visible, at the scale you own it; it never converts physics, distance, or population" — with a table of
what bridging does and does not convert (a real Pi becomes visible for boot/thermal/inference/power
behavior; a real AP's RF is visible "for that one AP, in that one room" but never extrapolates to a
campus RF plan; radio itself never crosses the bridge, since an AP strips RF context before frames reach
the Ethernet port). Recommends building, not bridging, for mesh RF validation (2-3 real OpenWRT routers
running BATMAN-adv, then bridging that mesh as a single segment). Documents "the full-hardware inversion"
— past roughly half the stack bridged, GNS3 becomes overhead rather than the thing doing the work, and a
fully-hardware bench setup is "a staging lab, not a model," answering "does this work when assembled" but
not "does this work when deployed" (the latter answered only by the field pilot DC-ISP-POC-001 already
scopes). Four named operational hazards (bidirectional traffic leakage requiring the topology never be
bridged to a production segment, promiscuous-mode requirements under VMware/VirtualBox, MAC-learning
switch port-security trips, host-NIC bottlenecking) and a recommended physical build (a dedicated ~$20 USB
NIC to an isolated unmanaged switch, isolating the bridge from the home network).

**DC-SIM-006, Hardware Integration Roadmap (incorporated):** frames itself as "a deployment path, with
the emulation as scaffolding," and states the emulation topology becomes the programme's permanent staging
environment rather than being retired once hardware arrives.

**Related work:** DC-COMPUTE-SILICON-ARCH-001 §7 extends this staged-fidelity discipline to compute silicon —
FPGA/CGRA prototyping before any structured-ASIC commitment follows the same simulate-first, graduated-hardware
pattern DC-SIM-006 already applies to networking/gateway hardware. Not incorporated into this consolidation
pass; a forward pointer only, since DC-SIM-006 predates that document.

Two corrections to intuitive build ordering:
sensors do not go first (lowest information, highest liability — any people-sensing device creates PIPEDA
obligations before a single routing result exists); routers and edge go first (a real DC-OS gateway in
the author's own household, "test user zero," no consent obligations). A seven-stage ladder (1: simulated
core + one real gateway in own household; 2: two real sites over real internet — named the cheapest real
result available, highest-value item immediately after the stop condition; 3: environmental sensors and
captured traffic; 4: friendly non-paying users, crossing a "dependency" threshold requiring a rollback
path first; 5: people-sensing hardware, crossing a PIPEDA threshold; 6: money changes hands, crossing a
legal/regulatory threshold identified as "the largest threshold in the ladder" and the same "Company Zero
incorporation and first invoice" step named in DC-STATUS-001; 7: poles/ROW/real FSO spans, crossing a
municipal threshold with named contacts, e.g. Hydro Ottawa pole attachments). Two named failure modes to
solve early (no rollback path from stage 4 onward; lab-to-production configuration drift, solved once via
shared Ansible/NixOS management driving both emulated and real nodes from one git repository — "if the
emulation and the deployment diverge, the emulation stops being evidence").

**DC-SIM-007, DAO Governance Simulation (incorporated):** three separable layers with different tools and
prerequisites — Layer 1 (contract correctness, via Foundry/anvil, OpenZeppelin `Governor`+
`TimelockController`, runs on a laptop with no network) confirms the vote mechanism works but says nothing
about capture; Layer 2 (governance economics, via cadCAD/radCAD agent-based simulation and Echidna/Foundry
invariant fuzzing, also laptop-only) is explicitly named as "where DAOs actually fail" and the layer most
often skipped, modeling voter apathy/quorum collapse, whale capture at 34% holdings, delegation cartels,
flash-borrowed voting, proposal spam, and the timelock-vs-emergency-response tension; Layer 3
(distributed policy enforcement, requiring GNS3) is named "the most genuinely novel work in the entire
programme," specifying an enforcement chain from proposal execution through a to-be-written watcher
daemon and OPA translation layer to nftables/tc/FRR rule regeneration, with propagation-to-enforcement
time as the primary measurement and six adversarial conditions run against DC-SIM-004 Scenario 6. Notes
Layers 1-2 can start immediately and independently of the rest of the suite; Layer 3 is strictly
downstream of the programme stop condition.

**DC-SIM-008, Open Architecture Decisions (incorporated, open status resolved by DC-SIM-009):** identifies
six blocking or roadmap-relevant open decisions, of which items 1-2 gate the build. Item 1: **two distinct,
unreconciled D-Central ISP architectures exist in the registry** — Ontario D-Central ISP Initiative (a
regulated Ottawa business with CRTC registration, FSO/GPON, costed CAD $16-30K/18-week timeline) and the
Mesh ISP/MNO layer (a token-metered cooperative protocol with a 68/20/10 revenue split) — "developed in
separate sessions, sharing FSO/GPON vocabulary but differing in governance, billing and legal footing,"
with the emulation programme electing to model the former since it has an addressing plan the emulation
can verify rather than invent. Item 2: **the FCN (`/fcn/...`) endpoint scheme is ambiguous between two
incompatible resolution models** — literal Named Function Networking (network-layer, cacheable,
DTN-native) versus a service-addressing convention (application-layer, live-host-only) — with materially
different caching, staleness, and safety consequences, recommending a split by side-effect class. Items
3-6 (lawful-intercept fork signalling VC undefined; Li-Fi/VLC phase placement undecided; a Metaverse
raw-camera-vs-metadata-only privacy conflict; SHI/sensing/connectivity documents never unified) are lower
urgency, gating later roadmap stages rather than the v1 build.

**DC-SIM-009, Architecture Decision Records (incorporated):** resolves all six DC-SIM-008 items via six
ADRs, each following a stated general principle — "where 'both' is possible, sequence it so v1 is the
restrictive case and v2 is additive." ADR-001 resolves item 1 by declaring the two ISPs are **layers, not
alternatives** (the Ontario ISP as the licensed carrier Layer A; the Mesh ISP/MNO as a cooperative Layer B
operating as a tenant of Layer A), with the 68/20/10 revenue-split contracts explicitly moved out of the
v1 contract set (correcting DC-SIM-007 §2.1's inclusion of `RevenueRouter`/`FeeCollector` as v1 contracts)
into v2. ADR-002 resolves item 2 by splitting the FCN namespace into `/fcn/q/...` (pure query, cacheable,
Reading A) and `/fcn/x/...` (side-effecting, never cached, Reading B), enforced at the runtime level via
sandboxed WASM execution for `/q/` handlers, with v1 shipping `/x/` only. ADR-003 resolves item 3 via a
per-node `NetworkForkVC` (ROOT/ALT), with v1 shipping ROOT-only and an explicit caveat that whether
cooperative mesh traffic counts as regulated telecommunications is a question for a telecom lawyer, not
this document. ADR-004 defers Li-Fi/VLC to v2/v3 while requiring the in-home access-medium interface stay
pluggable from day one. ADR-005 resolves the Metaverse privacy conflict by reframing consent as unlocking
a local, time-boxed, revocable viewing session rather than publication rights, explicitly noting content-
addressed raw video "can never be un-published" and bystander consent "is not solvable technically." ADR-
006 confirms a three-profile node taxonomy (P1 Residential SHI, P2 Commercial/Campus, P3 High-security/
Research), directing DC-SHI-SPEC-001 and the sensing/connectivity documents be unified into a new
DC-SHI-SPEC-002 that supersedes all three (a DC-DEDUP-STD-001-scope action, not acted on by this
Consolidator pass). Closes with a root-cause observation that ADR-001 and ADR-006 are "the same failure"
— parallel design work across separate sessions producing unreconciled specifications — and proposes a
registry-wide convention requiring every new document declare what it supersedes/extends/conflicts with.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Programme objective, stop condition, scope-discipline indicators | DC-SIM-000, full document | incorporated |
| GNS3 fidelity principle, backend/tier tables, two named traps, subsystem coverage | DC-SIM-001, full document | incorporated |
| Four-tier topology, node inventory, impairment profiles, scenario decomposition, compute sizing | DC-SIM-002, full document | incorporated |
| Buildroot dual-architecture resolution, image contents, acceptance criteria | DC-SIM-003, full document | incorporated |
| Four ordered proofs, baseline Scenario 1, traffic toolchain, Scenarios 5-6, write-up disclosures | DC-SIM-004, full document | incorporated |
| Cloud bridge mechanism, bridge-target table, full-hardware inversion, operational hazards, recommended build | DC-SIM-005, full document | incorporated |
| Ordering corrections, seven-stage hardware ladder, two failure modes (rollback, drift) | DC-SIM-006, full document | incorporated |
| Three governance-simulation layers, minimum contract set, adversarial enforcement conditions | DC-SIM-007, full document | incorporated (its §2.1 v1 contract set corrected by DC-SIM-009 ADR-001, see below) |
| Six open architecture decisions (two D-Central ISPs unreconciled; FCN ambiguity; 4 lower-urgency items) | DC-SIM-008, full document | incorporated (open status resolved by DC-SIM-009; analysis retained as necessary reading per both documents' own reconciliation notes) |
| Six ADRs resolving DC-SIM-008's open items | DC-SIM-009, full document | incorporated |

## Unresolved tensions

None requiring Consolidator-level reconciliation. The suite already carries its own explicit,
verified-accurate reconciliation notes: DC-SIM-009 supersedes DC-SIM-008's open-question *status* on items
1-6 while both documents' own headers agree DC-SIM-008's analysis is not restated and remains necessary
reading (the two-ISP finding, the FCN reading A/B distinction, etc.) — this consolidation follows that
same division rather than treating either document as replacing the other. One internal correction is
worth surfacing explicitly rather than leaving implicit: DC-SIM-007 §2.1 lists `RevenueRouter` and
`FeeCollector` (the 68/20/10 revenue-split contracts) as part of the emulation programme's "minimum
contract set" for v1, but DC-SIM-009's ADR-001 (written after DC-SIM-007, per the suite's own document
numbering and the root-cause note in DC-SIM-009 §7) explicitly states these "move entirely to v2 and out
of the v1 contract set in DC-SIM-007 §2.1." This is a stated, source-acknowledged correction, not an
unreconciled contradiction — DC-SIM-009's ADR-001 is later in the sequence and directly names the
document and section it corrects.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-000-Index.md`
- `knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-001-Fidelity-Reference.md`
- `knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-002-Topology-Build-Spec.md`
- `knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-003-DCOS-Build-Spec.md`
- `knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-004-Test-Scenario-Catalogue.md`
- `knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-005-Cloud-Bridge-External-Integration.md`
- `knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-006-Hardware-Integration-Roadmap.md`
- `knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-007-DAO-Governance-Simulation.md`
- `knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-008-Open-Architecture-Decisions.md`
- `knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-009-Architecture-Decision-Records.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-000-Index.md,
  knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-001-Fidelity-Reference.md,
  knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-002-Topology-Build-Spec.md,
  knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-003-DCOS-Build-Spec.md,
  knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-004-Test-Scenario-Catalogue.md,
  knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-005-Cloud-Bridge-External-Integration.md,
  knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-006-Hardware-Integration-Roadmap.md,
  knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-007-DAO-Governance-Simulation.md,
  knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-008-Open-Architecture-Decisions.md,
  knowledge-base/d-central/meta/simulation/conversation-artifacts/DC-SIM-009-Architecture-Decision-Records.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved by this pass — status assignment belongs to
DC-DEDUP-STD-001, not the Consolidator, including DC-SIM-009's own instruction that DC-SHI-SPEC-001 and
related documents be unified into a new DC-SHI-SPEC-002.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

**Referenced by:**
- [[DC-COMPUTE-SILICON-ARCH-001|DC-COMPUTE-SILICON-ARCH-001 — Compute Silicon Class Architecture (v1, generated 2026-09-07)]]

<!-- AUTO-GENERATED RELATED END -->
