# DC-COMPUTE-SILICON-ARCH-001 — Compute Silicon Class Architecture (v1, generated 2026-09-07)

**Status:** Design spec, 0% executed. Extends [DC-NETWORKING-ARCH-RECONCILED-001](DC-NETWORKING-ARCH-RECONCILED-001.md),
[DC-DCENTRAL-SIMULATION-LAB-RECONCILED-001](DC-DCENTRAL-SIMULATION-LAB-RECONCILED-001.md),
[DC-DAO-AGENT-LOOP-USER-STORIES-001](DC-DAO-AGENT-LOOP-USER-STORIES-001.md), and
[DC-MESHSTORAGE-ARCHIVE-001](DC-MESHSTORAGE-ARCHIVE-001.md). Fills the empty "Tier 3 — Compute & Storage"
slot named but never specified in [UNIFIED_SOURCE_OF_TRUTH_V24](UNIFIED_SOURCE_OF_TRUTH_V24.md) §3.11.3, and the
`mesh-compute`/`mesh-ai` outline entries (same doc, §3.5/§3.7) that currently have no body content.

**Cross-referenced from (bidirectional pointers, added same pass):** DC-NETWORKING-ARCH-RECONCILED-001 (Unresolved
tensions), UNIFIED_SOURCE_OF_TRUTH_V24 (§3.5, §3.7, §3.11.3), DC-DAO-AGENT-LOOP-USER-STORIES-001 (Story 6),
DC-DCENTRAL-SIMULATION-LAB-RECONCILED-001 (DC-SIM-006 discussion), DC-MESHSTORAGE-ARCHIVE-001 (§5), DC-LKB-001
(§6.3, scope note distinguishing financial-rail DePIN), DC-LKB-003 (§4.2, scope note distinguishing IoT/metering-
rail DePIN), DC-DION-API-BACKEND-RECONCILED-001 (§2, naming caution on its own 5-tier hybrid compute mesh),
DC-OPENSECURE-GUARDIAN-SENTINEL-ARCH-RECONCILED-001 (OS-SENTINEL flagged as the strongest cost-justification
candidate found), DC-HCCC-GRAPHRAG-RECONCILED-001 (GPU fleet as a discovery-pipeline candidate), and
DC-IHOSE-HARDWARE-BOM-RECONCILED-001 (A100 cost baseline). Also entered in registry/DC-REG-001-Master-Registry.md
§2.

**Source material:** two external ChatGPT conversations (2026-09-06, not part of the Claude export this repo
otherwise consolidates) exploring a Taalas HC1-style "model-on-silicon" DePIN cooperative, then a compute-architecture
comparison covering FPGA/CGRA/eFPGA/structured-ASIC roles, an accelerator-family naming scheme, and a thin-client/
streaming-compute model. Treated here the same way `conversations/artifacts/*` docs are treated elsewhere in this
repo (e.g. DC-AGD-001): raw ideation brought in and reconciled against existing architecture, not pre-validated fact.

---

## 0. What this closes

D-Central has three separate places that gesture at specialized compute hardware without ever specifying it:

1. **DC-NETWORKING-ARCH-RECONCILED-001 §9.1** names a "GPU Edge/D-District" tier (Tier 2) with NVIDIA L4/RTX
   hardware for AI inference, but treats "GPU" as the only compute-acceleration option — no FPGA, ASIC, or any
   silicon-flexibility spectrum appears anywhere in either source document it consolidates.
2. **UNIFIED_SOURCE_OF_TRUTH_V24 §3.11.3** names "SHI Node Tier 3 — Compute & Storage (mesh-compute, mesh-storage,
   mesh-ai)" as a chapter heading with zero body content — the underlying 280KB source document isn't in this repo.
3. **mesh-ai/mesh-compute** (same ToC, §3.5/§3.7) are described only as forks of existing DePIN compute markets
   (Akash/Golem, Bittensor) — no mechanism for deciding when a workload is worth hardening into dedicated silicon.

This document specifies the missing piece: a hardware-role hierarchy, the mechanism for deciding what to build in
silicon and when, and how that hardware plugs into services D-Central already has (SHI nodes, mesh-ai/mesh-compute,
the simulation lab, DAO-agent-loop node operators, mesh-storage's reward economics, and the existing thin-client
architecture). It does **not** create a new "Tier 0-3" scheme — see §1 on why, given the tier-naming conflict
DC-NETWORKING-ARCH-RECONCILED-001 already flags as unresolved.

---

## 1. Silicon Class — a fourth, orthogonal axis (not a third Tier 0-3)

DC-NETWORKING-ARCH-RECONCILED-001's "Unresolved tensions" section already documents two incompatible Tier 0-3
schemes coexisting in the repo: the comprehensive doc's compute-capacity axis (Nano/Micro/GPU/Cluster Edge) and the
blueprint's network-role axis (sensor/mobile/router/backbone). Reusing "Tier" for a third, silicon-flexibility axis
would compound exactly the collision that section warns about. This document therefore introduces a distinctly
named axis — **Silicon Class** — that any node, at any existing Tier, can be assigned independently:

| Silicon Class | Role | Analogy | Where it plugs into existing Tiers |
|---|---|---|---|
| **CPU** | Orchestration: OS, APIs, DBs, auth, scheduling, node management, controlling other classes | The manager | Present implicitly at every existing Tier 0-3 node; not previously named as a distinct role |
| **GPU** | Flexible frontier: new/experimental/training models, workloads with no ASIC yet | The flexible heavy-duty worker | Already named at Tier 2 "GPU Edge/D-District" (NVIDIA L4/RTX) — this document makes its *role*, not just its presence, explicit |
| **FPGA** | The lab: prototype a workload before committing silicon; fully rewritable | Digital LEGO | New — no existing D-Central hardware doc mentions FPGA |
| **CGRA** | Faster-iterating middle lab tier: word-level reconfiguration instead of FPGA's bit-level, used for rapid quantization/precision sweeps | LEGO made of bigger blocks | New |
| **Structured ASIC** | Factory floor: only for workloads proven stable and high-volume; 98% generic base wafer, 2% custom top-metal print | The mass-printed book | New |
| **eFPGA** | Escape hatch embedded inside a Structured ASIC — a small reprogrammable island alongside frozen silicon | The locked diary with an erasable page | New |
| **Deterministic processor (LPU-class)** | Predictable-timing coordination for latency-sensitive pipelines (agent handoffs, industrial control, real-time audio) — not a magic internet traffic controller; Internet propagation delay is physics, not something this hardware removes | The traffic conductor | New |

A single physical node can carry a Tier (compute capacity or network role, per the existing schemes) *and* a Silicon
Class independently — e.g. a Tier 2 "GPU Edge" node could later be paired with, or partially replaced by, a
Structured ASIC once a workload at that node justifies it (§3).

### 1.1 The layman's version (kept verbatim from source material — useful for onboarding non-technical coop members)

Imagine opening a restaurant. You could build a kitchen for exactly one dish — "Chicken Sandwich #1" — but that's a
bad kitchen. Instead you build a kitchen with ovens, grills, refrigerators, knives, and mixers, and *then* make
chicken sandwiches, burgers, steak, or pizza with the same equipment. **A Structured ASIC is the kitchen. AI models
are the recipes.** Building one ASIC per model is the "one dish" mistake; building one ASIC around the mathematics
a whole model *family* shares (matrix multiplication, attention, quantized arithmetic) is the kitchen.

The progression from flexible to fixed, restated as a ladder (the exact ordering isn't universal — FPGA and CGRA
trade off differently depending on workload — but conceptually):

```
CPU  → flexible, general-purpose (orchestration, anything, not fastest at AI math)
  │
GPU  → massively parallel and flexible (the current default for anything new)
  │
CGRA → reconfigurable acceleration, word-level blocks, fast iteration
  │
FPGA → reconfigurable acceleration, bit-level, slower iteration but finer control
  │
ASIC → extremely specialized, fastest and cheapest per operation, cannot be rewired
```

---

## 2. The discovery pipeline (the mechanism, not just the hardware list)

The important design principle from the source material is not "which chips exist" but **how D-Central decides
what to harden into silicon** — it doesn't guess, its own usage data tells it:

```
mesh-ai / mesh-compute traffic
        ↓
"Is this workload stable, common, and high-volume?"
        ↓ yes                              ↓ no
FPGA prototype                    stays on GPU (flexible frontier)
        ↓
CGRA iteration (quantization/precision sweep — see §2.1)
        ↓
benchmark: accuracy vs. speed vs. power vs. memory
        ↓
Structured ASIC candidate
        ↓
mass deployment across cooperative node operators (§5)
```

This pipeline is the mechanism `mesh-ai`/`mesh-compute` currently lack — it turns those two outline entries from
static fork-descriptions into an actual operating model for when to mint a new hardware SKU.

### 2.1 Quantization/precision validation (belongs under mesh-ai, not as a standalone service)

Before any workload reaches the CGRA/FPGA stage, its precision floor needs validating — does INT4 hold acceptable
accuracy versus FP16, etc. This is genuinely new content (no existing D-Central doc does model-compression
validation) and is scoped here as a sub-function of the mesh-ai discovery pipeline, not a separate product line.

### 2.2 Cost-justification gate

Per the explicit constraint this scoping pass was given ("as long as the cost makes sense"), a workload only
proceeds past the FPGA stage if it is simultaneously: (a) architecturally stable across multiple months of
production traffic, (b) high-volume enough that per-unit ASIC cost beats per-unit GPU-rental cost at the
cooperative's actual traffic level, and (c) latency- or cost-sensitive enough that the win matters to a paying
workload. Checked against concrete existing D-Central workloads:

| Existing target | Fit | Why |
|---|---|---|
| **DC-AGD-001 gunshot detector's CNN ensemble** (Raspberry Pi 5 gateway tier) | **Strong** | Fixed model, high-volume, latency-sensitive classification — exactly the profile the pipeline is built for. An ASIC/eFPGA slot-in at the gateway tier is a natural upgrade, not a stretch |
| **OS-SENTINEL AI video surveillance** ([DC-OPENSECURE-GUARDIAN-SENTINEL-ARCH-RECONCILED-001](DC-OPENSECURE-GUARDIAN-SENTINEL-ARCH-RECONCILED-001.md)) | **Strong — likely the best-evidenced candidate in the repo** | Already built on fixed, well-known model families (YOLOv8, ONNX-portable models) with an explicit sub-100ms latency requirement and existing GPU/TPU acceleration (NVIDIA CUDA, Google Coral TPU, Intel OpenVINO) already deployed — this is production-shaped evidence of a stable, high-volume, latency-critical workload, not a hypothetical one |
| **DC-HCCC-GRAPHRAG** ([DC-HCCC-GRAPHRAG-RECONCILED-001](DC-HCCC-GRAPHRAG-RECONCILED-001.md)) | **Moderate** | Already provisions a dedicated 2-4 GPU-node Kubernetes cluster for production — a real GPU-fleet workload the discovery pipeline (§2) should watch, though GraphRAG's retrieval/embedding step is less obviously a single stable "model family" than a classifier or diffusion model |
| **IHOSE deployment** ([DC-IHOSE-HARDWARE-BOM-RECONCILED-001](DC-IHOSE-HARDWARE-BOM-RECONCILED-001.md)) | **Reference only** | An earlier BOM pass specs 4× NVIDIA A100 GPU nodes per Enterprise-tier site — real GPU capital already budgeted elsewhere in the repo, useful as a cost baseline for any future ASIC vs. GPU comparison, not itself a workload to harden |
| **mesh-storage** | **Weak** | I/O-bound, not compute-bound — Silicon Class doesn't apply here regardless of tier |
| **TrafficMesh** | **No fit yet** | No compute hardware is specified for TrafficMesh nodes at all (grepped clean of FPGA/ASIC/GPU/processor terms) — nothing to harden until a compute workload exists there in the first place |

### 2.3 Acceleration expectations — targets, not promises

The source material is explicit that ASIC gains should be framed as **engineering targets calibrated against real
published results, not a guaranteed multiplier promised before any chip is built.** Cited external benchmarks as of
the source conversation: NVIDIA reports up to 4.68× acceleration for an LTX-2.5 video pipeline via software
optimization alone; HunyuanVideo research shows ~3.7× single-GPU acceleration; a 5-second 720p video went from 71s
to 29s (~2.4×) without a new ASIC; NVIDIA's Sol engine reports up to 4.52× for a 33B multimodal video model; OpenAI's
Jalapeño inference accelerator is reported as substantially more efficient per watt than Nvidia's GB300 on selected
inference workloads. None of these are D-Central's own numbers — they're cited to calibrate what "specialized
hardware" realistically buys before committing to build any of it.

| Workload | Today on a good GPU | Specialized-accelerator target | Basis |
|---|---|---|---|
| Image generation | seconds/image | sub-second to a few seconds | extrapolated from cited software-only gains above |
| High-quality image | ~5-30 sec | ~1-10 sec | same |
| Short video | tens of sec → minutes | seconds → tens of seconds | same |
| Longer/high-res video | minutes+ | potentially dramatically reduced | same |
| Speech transcription | real-time or faster | many simultaneous streams (batch-parallel, not per-stream speedup) | §3.2 |
| Voice synthesis | near real-time | many simultaneous voices | §3.2 |
| Audio generation | seconds/minutes | much faster batch generation | §3.2 |

**The metric that actually matters is throughput-per-dollar, not raw multiplier.** Source example: a GPU doing 100
images/hour at $10/hour versus an ASIC doing 500 images/hour at $2/hour is "5× faster," but the real business change
is 5× throughput at 1/5 the cost — cheaper inference makes AI usage economical for customers who couldn't
previously justify it, which is the actual growth lever, not the speed number by itself.

**Why video and multimodal workloads specifically justify this pipeline more than a single image does:** a
5-second video at 24fps is 120 frames, and modern video models don't generate 120 independent images — they model
relationships across space *and* time, which is why attention cost and token count are the dominant bottleneck
(cited: current video research identifies attention and total video-token count as the major cost driver). Those
are exactly the "matrix math, attention, sparse attention, transformer layers, memory movement, VAE, quantization"
operations §3's fixed-accelerator column targets.

---

## 3. ASIC + eFPGA hybrid ("core-and-shell") — the model-family standardization answer

A structured ASIC cannot be re-etched to run a different model, even within the same model family (different
checkpoints have different physical weights). The source material's answer, adopted here: **don't build silicon for
one model — build it for the mathematics shared by a model family**, and keep an eFPGA escape hatch for whatever
changes next.

```
                D-Central ASIC
                      │
     ┌────────────────┴────────────────┐
     │                                  │
Fixed accelerator                Programmable layer (eFPGA)
     │                                  │
Matrix/GEMM, attention,          Model config, quantization,
FFN, VAE ops, diffusion          adapters, new kernels
timestep ops
     │                                  │
     └────────────────┬─────────────────┘
                       │
                High-speed memory
                       │
                    Output
```

This is the same pattern already implicit in mesh-ai's LoRA-adapter concept from the Taalas-derived source
conversation: frozen base weights in silicon, small rewritable layer for task-specific adaptation.

### 3.1 Per-operation hardware treatment (concrete design table, kept from source material)

For an image/video-generation ASIC specifically, the source material lays out which mathematical operations get
hardwired versus left programmable — worth preserving at this level of detail since it's the actual design
argument, not just the conclusion:

| Layer/operation | ASIC treatment |
|---|---|
| Matrix multiplication | Hard accelerator |
| Attention | Hard accelerator |
| FFN (feed-forward network) | Hard accelerator |
| Quantized arithmetic | Hard accelerator |
| Diffusion timestep operations | Hard accelerator |
| VAE operations | Accelerated |
| Memory movement | Highly optimized |
| Model-specific operators | Programmable (eFPGA) |
| New quantization formats | Programmable/eFPGA |
| New model architectures | FPGA/GPU fallback |
| Experimental models | FPGA/CGRA/GPU |

Rationale for why this specific split works for image/video specifically: modern Diffusion Transformer (DiT) models
spend the overwhelming majority of their compute on repeated matrix operations and iterative denoising steps that
recur across nearly every model in the family, regardless of which specific checkpoint is running — that's the
"common mathematics" §3 argues for hardening, while scheduler logic, conditioning mechanisms, and VAE variants
(which do change between model generations — e.g. a shift from a pure DiT to a multimodal autoregressive/MoE
architecture) stay on the programmable layer.

### 3.2 Generative Media Accelerator — the broader-than-images argument

The source material's strongest structural point: don't build a single-purpose "Image ASIC" — build one shared
**DCA-G1** ("Generative AI Accelerator") die around the mathematics common to *all* generative workloads
(transformers, diffusion, attention, matrix multiplication, convolutions, quantized/sparse inference, tensor ops),
then target it at different workloads purely through firmware/compiler configuration rather than a new chip per
workload:

```
                    D-CENTRAL MEDIA CLOUD
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
      IMAGE               VIDEO               AUDIO
        │                   │                   │
        ▼                   ▼                   ▼
      Voice               Speech              Music
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                     MULTIMODAL AI
```

```
DCA-G1  (one shared die, common generative-math core)
 │
 ├── Image        (firmware/compiler target)
 ├── Video        (firmware/compiler target)
 ├── Voice        (firmware/compiler target)
 ├── Audio        (firmware/compiler target)
 ├── Speech       (firmware/compiler target)
 ├── LLM          (firmware/compiler target)
 └── Multimodal   (firmware/compiler target)
```

Full candidate SKU list from the source material, preserved for reference — **none of these are commitments, they
are candidate names for whatever workload the discovery pipeline (§2) eventually justifies hardening**, and the
repo should build at most the first one or two that real mesh-ai traffic data actually supports:

| Candidate SKU | Target workload |
|---|---|
| DCA-L | LLM inference |
| DCA-I | Image generation |
| DCA-V | Video generation |
| DCA-S | Speech recognition (transcription) |
| DCA-T | Text-to-speech |
| DCA-A | Audio/music generation |
| DCA-M | Multimodal AI |
| DCA-E | Embeddings/search |
| DCA-R | Recommendation/ranking |
| DCA-C | Computer vision |
| DCA-3D | 3D/world generation |
| DCA-Edge | Low-power edge AI |

### 3.3 Adjacent workloads worth naming (voice, transcription, translation) — because mesh-ai isn't only image/video

Concrete pipelines the discovery mechanism (§2) should watch for, since they're independently high-volume,
latency-sensitive candidates and not just theoretical extensions of the image/video case:

- **Speech-to-text (batch):** a business uploading e.g. 100,000 hours of recorded meetings is a textbook
  batch-compute fit — distribute across many ASIC nodes in parallel rather than one long sequential GPU job.
- **Real-time multilingual pipeline:** speech → transcription → translation → voice generation as one chained
  pipeline (e.g. English speech in, French/Haitian Creole/Spanish audio out) — directly relevant given this repo's
  existing Haiti-diaspora communications work; worth flagging as a candidate cross-reference for whoever next
  touches the Haiti integration docs, not specified further here.
- **AI production/filmmaking pipeline:** script → storyboard → characters → images → video → voice → music → sound
  effects → final film, each stage independently accelerable — relevant if D-Central ever exposes a creative-tools
  product surface, noted here only as a long-horizon possibility.

---

## 4. Locality-first regional clustering — resolves rather than duplicates existing topology

The source material explicitly corrects an earlier version of itself: Internet propagation delay is physics, so
compute should route to the *nearest* suitable cluster rather than hopping workloads randomly around the world.
This maps directly onto structure D-Central already has and doesn't need inventing:

- **[D-Central-Ecosystem-Technical-Specification (VDI-Solutions)](../knowledge-base/d-central/meta/platform-scaffolding/VDI-Solutions/D-Central-Ecosystem-Technical-Specification-md.md)**
  already specifies "Local Mesh Clusters" (community-owned edge compute) and "Inter-Cluster Federation" (secure
  tunnels between distant mesh networks) — this is the regional-clustering topology, already named.
- Silicon Class assignment (§1) happens *within* a regional cluster, not across them: a Region's Tier 2/3 nodes
  carry whatever mix of GPU/FPGA/ASIC the cluster's own traffic has justified, and workloads route to the nearest
  cluster carrying the needed class rather than to a globally "optimal" but distant one.

```
                         GLOBAL ROUTER
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
            REGION A       REGION B       REGION C
                │              │              │
         ┌──────┼──────┐       │              │
         ▼      ▼      ▼   (same pattern) (same pattern)
        GPU   ASIC   FPGA
        CPU   (per-region Silicon Class mix, sized to that region's own traffic)
```

A user is always routed to the nearest cluster carrying the Silicon Class its workload needs — never to a
globally "optimal" but physically distant node, since propagation delay cannot be engineered away.

### 4.1 The D-Central Distributed Compute Fabric — naming the composite whole

Every node contributes whatever hardware it has; a scheduler decides which class handles a given job:

```
              D-CENTRAL FABRIC
   CPU ─────────┐
   GPU ─────────┤
   FPGA ────────┤
   CGRA ────────┤
   ASIC ────────┤
   Storage ─────┤
   Network ─────┘
                 ↓
            Scheduler  ("what hardware should perform this job?")
                 ↓
          Customer workload
```

Example decision table the scheduler applies (illustrative, not a committed routing spec):

| Request | Routed to | Why |
|---|---|---|
| "Run experimental 70B model" | GPU (or FPGA if prototyping a hardening candidate) | Constantly changing, no ASIC candidate yet |
| "Run 8B customer-support model 100 billion times" | Structured ASIC | Stable, high-volume — §2.2's gate is satisfied |
| "Run new quantization experiment" | CGRA/FPGA | §2.1 precision validation |
| "Ultra-low-latency industrial control" | Deterministic processor | §1's LPU-class role |
| "Hospital wants jurisdiction-restricted inference" | Private geographic node ring | §7's DePIN division, SHI Tier 3+5 crossover |

---

## 5. Thin-client / streaming-compute — already exists, this document connects to it, doesn't replace it

**This is not new territory.** [DC-NETWORKING-ARCH-RECONCILED-001:51](DC-NETWORKING-ARCH-RECONCILED-001.md) already
records that its Comprehensive source (§10-17) specified a full thin-client architecture, and the
[VDI-Solutions Technical Specification](../knowledge-base/d-central/meta/platform-scaffolding/VDI-Solutions/D-Central-Ecosystem-Technical-Specification-md.md)
has a concrete BOM for it: ARM Cortex-A78/Intel N-series thin clients, TPM 2.0, multi-protocol streaming
(RDP/SPICE/WebRTC/Parsec), live VM/container migration under 2 seconds, checkpoint/resurrection every 30-60s. The
"user's machine as thin client, compute happens elsewhere" idea from the source conversation is this existing
architecture, not a new one — what's missing is naming what backs the compute side, which is what §1-§3 supply.

### 5.1 Three delivery levels (new content — not previously distinguished in the existing VDI spec)

The existing spec treats streaming as a single mode (multi-protocol client). The source material's contribution
worth adding: not every workload should stream.

| Level | Use case | Mechanism |
|---|---|---|
| **1. Return a result** | Image generation, transcripts, batch jobs, generated files | No live stream — request, compute, download |
| **2. Interactive streaming** | Video editing, virtual worlds, remote desktops, AI game environments | Full streaming session, as already specified in the VDI thin-client spec |
| **3. Hybrid** | Most real workloads | Local: input, display, encryption, caching, lightweight AI. Remote: heavy compute. Only the result/stream crosses the network |

Bandwidth discipline: don't force everything into Level 2 just because the architecture supports it — Level 1 is
usually cheaper and simpler, and should be the default unless continuous interaction is actually required.

### 5.2 End-to-end hierarchy (how §1-§5 compose into one path from user input to output)

```
                         D-CENTRAL DISTRIBUTED FABRIC
                                     │
                 ┌───────────────────┴───────────────────┐
                 │                                        │
        USER / THIN CLIENT                          NODE NETWORK
                 │                                        │
          ┌──────┴──────┐                  ┌──────────────┼──────────────┐
          ▼             ▼                  ▼              ▼              ▼
        Input        Display              CPU            GPU           FPGA
                                            │              │              │
                                            └──────┬───────┴──────────────┘
                                                    ▼
                                                  CGRA
                                                    ▼
                                                  ASIC
                                                    ▼
                                            Specialized AI
                                                    │
              ┌─────────────────────────────────────┴──────────────────────┐
              ▼                                                            ▼
         AI COMPUTE                                                  AI SERVICES
              │                                                            │
     ┌────────┼────────┐                                    ┌─────────────┼─────────────┐
     ▼        ▼        ▼                                    ▼             ▼             ▼
    LLM     IMAGE    VIDEO                                VOICE        AUDIO      TRANSCRIPTION
     │        │        │                                    │             │             │
     └────────┴────────┴────────────────────────────────────┴─────────────┴─────────────┘
                                          │
                                    USER OUTPUT
                                          │
                                   STREAM / FILE (§5.1 delivery level decides which)
```

Worked example — "make a 10-second cinematic video": CPU handles prompt processing → GPU runs the video model
→ ASIC (once that model family is hardened, per §2's pipeline) handles the repeated transformer operations → GPU
does final processing → video encoder → edge node → streamed to the user (§5.1 Level 2). The user only sees
"Generating…" then the result — which Silicon Class did the work is an implementation detail the scheduler owns,
not something the client needs to know.

---

## 6. Node operator economics — extends DAO-agent-loop Story 6, does not replace it

[DC-DAO-AGENT-LOOP-USER-STORIES-001 Story 6](DC-DAO-AGENT-LOOP-USER-STORIES-001.md) already has "The Node Operator"
persona (someone hosting an SHI node running coop agent workloads, with D-Credit burn-rate tracking). That persona
is currently hardware-agnostic. The source material's contribution: **two distinct operator roles**, worth naming
explicitly rather than leaving implicit:

- **Consumer A (pure thin-client user):** contributes no hardware, consumes compute via the thin-client architecture
  in §5. Already covered by the existing VDI-Solutions "Mobile Devices" and "Thin Clients" device categories.
- **Consumer B (capacity contributor):** operates a node carrying some Silicon Class mix (GPU/FPGA/ASIC) and earns
  compensation for contributed capacity — this is Story 6's "Node Operator" persona, made explicit rather than
  generic. The VDI-Solutions spec's "Community Edge Nodes" (Micro Node / Standard Node, both already GPU-capable)
  are exactly this operator's hardware.

### 6.1 Reward mechanism — same endowment pattern as mesh-storage, adapted to compute-serving

[DC-MESHSTORAGE-ARCHIVE-001 §5](DC-MESHSTORAGE-ARCHIVE-001.md) specifies an Arweave-derived endowment model for
storage-serving: a one-time D-Credit payment at ingestion, paid out gradually to operators actively serving. The
same shape applies to compute-serving, with the difference that compute has no equivalent of "content" to endow
against — the natural adaptation is an endowment sized against a workload's *projected serving volume* (from the
discovery pipeline's own usage data, §2) rather than a fixed one-time payload. This needs its own line in the SHI
financial model, the same way mesh-storage's archive tier and mesh-vpn's relay-throughput reward each needed one —
not fully specified here, flagged as a follow-on calculation.

---

## 7. Service catalog mapping (six divisions, mapped onto existing docs — not six new docs)

| Division | Maps onto | New content needed |
|---|---|---|
| AI Cloud (inference API, token-as-a-service) | mesh-ai / mesh-compute | ASIC-tier SKU alongside existing GPU-tier auction fork |
| Dev Cloud (FPGA-as-a-Service, hardware-in-the-loop) | **DC-DCENTRAL-SIMULATION-LAB-RECONCILED-001** — DC-SIM-006's staged hardware-integration ladder (simulate → real gateway → real hardware) already applies this exact discipline to networking hardware; this document extends it to compute silicon | Explicit note that FPGA/CGRA experimentation follows the same graduated-fidelity discipline |
| AI Labs (quantization, benchmarking) | mesh-ai, §2.1 above | New sub-function, not a standalone doc |
| Silicon (ASIC compilation, tape-out) | Cooperative treasury/governance docs | Explicitly **phase 3, not now** — requires $30M+ CapEx and foundry access nothing in D-Central's current stage approaches |
| DePIN (node hosting, private rings) | Existing DePIN references (DC-LKB-001 §6.3, DC-LKB-003) are financial-rail DePIN only — this is a genuinely separate, new service: geo-locked private compute rings composing SHI Tier 3 (compute) + Tier 5 (identity/DID-VC jurisdiction proof) | New — flagged, not yet specified in depth |
| Cooperative (treasury, ASIC crowdfunding, rewards) | mesh-storage §5 endowment precedent (§6.1 above), DAO-agent-loop node operator persona | Extension, not new doc |

### 7.1 Division contents, preserved at source level of detail (for whoever scopes each division next)

- **AI Cloud:** inference API, model hosting, token-as-a-service, voice inference, agent execution, batch
  inference, private AI.
- **Dev Cloud:** FPGA-as-a-Service, CGRA-as-a-Service, hardware-in-the-loop testing, hardware CI/CD, accelerator
  development, distributed simulation. (Concretely: "give me 30 minutes on 20 FPGA nodes"; "every time I commit
  hardware code, test it on 100 different FPGA configurations"; "randomly disconnect nodes and see whether my
  system survives" as a fault-testing service.)
- **AI Labs:** quantization testing, model compression, accuracy validation, benchmarking, power optimization,
  latency optimization. Output framed in the source material as a "Silicon Readiness Score" per model (accuracy,
  hardware efficiency, memory reduction, FPGA compatibility, ASIC suitability, recommended precision) — a concrete
  report shape worth keeping if this division is ever built out.
- **Silicon:** ASIC compilation, structured-ASIC design, eFPGA integration, silicon optimization, tape-out
  preparation, prototype manufacturing. **Explicitly gated behind Divisions 1-3 producing real evidence** — the
  source material's own caution: "the cloud tells you what chip to manufacture," not the reverse.
- **DePIN:** node hosting, compute marketplace, storage, bandwidth, geographic compute, private node rings,
  enterprise infrastructure.
- **Cooperative:** member ownership, equipment financing, hardware leasing, treasury, node rewards, research
  grants, ASIC crowdfunding, governance.

### 7.2 The business flywheel (why this is a system, not a chip-manufacturing side quest)

```
        CUSTOMERS
            ↓
     AI CLOUD REVENUE
            ↓
    D-CENTRAL TREASURY
            ↓
   AI HARDWARE RESEARCH
            ↓
     FPGA / CGRA LAB
            ↓
    BETTER ACCELERATOR
            ↓
      ASIC DESIGN
            ↓
    MASS PRODUCTION
            ↓
   CHEAPER AI COMPUTE
            ↓
     MORE CUSTOMERS
            ↓
     MORE REVENUE
            ↓
            ↺
```

Restated as a phase ladder, directly reusable as a roadmap-communication artifact:

1. "AI needs expensive GPUs." (today)
2. "Let's pool GPUs." (mesh-ai/mesh-compute as they exist now)
3. "Let's optimize the AI." (§2.1 quantization)
4. "Let's experiment with FPGAs." (§2, discovery pipeline)
5. "We now know exactly which computations consume the most money." (§2.2 cost-justification gate satisfied)
6. "Let's manufacture silicon specifically for those computations." (§3, ASIC candidate)
7. "D-Central owns part of the AI compute stack instead of merely renting someone else's GPUs." (§7 Silicon
   division — the long-horizon endpoint, not a near-term commitment)

---

## 8. Gap registry status

Not yet assigned a number in DC-GAP-001 or DC-REG-001 — flagged here for whoever next updates those registries.
Closes the empty SHI Tier 3 (Compute & Storage) slot in UNIFIED_SOURCE_OF_TRUTH_V24 §3.11.3 and gives mesh-ai/
mesh-compute (same doc §3.5/§3.7) their first operating mechanism beyond "fork of an existing DePIN market."

---

*DC-COMPUTE-SILICON-ARCH-001 — extends DC-NETWORKING-ARCH-RECONCILED-001, DC-DCENTRAL-SIMULATION-LAB-RECONCILED-001,
DC-DAO-AGENT-LOOP-USER-STORIES-001, and DC-MESHSTORAGE-ARCHIVE-001. Introduces "Silicon Class" as a fourth axis
distinct from the two already-conflicting Tier 0-3 schemes flagged in DC-NETWORKING-ARCH-RECONCILED-001's Unresolved
tensions — deliberately not reusing "Tier" numbering. Specifies the FPGA→CGRA→Structured-ASIC discovery pipeline as
mesh-ai/mesh-compute's operating mechanism, connects to (rather than replaces) the thin-client architecture already
specified in the VDI-Solutions Technical Specification, and extends the DAO-agent-loop Node Operator persona and
mesh-storage's endowment-reward pattern to compute-serving. Silicon fabrication (Division 5, §7) is explicitly
out of scope for D-Central's current stage — this document specifies the discovery pipeline and thin-client/cloud
service layers that would eventually justify it, not the fabrication step itself.*
