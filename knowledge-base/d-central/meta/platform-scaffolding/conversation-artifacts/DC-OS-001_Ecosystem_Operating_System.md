---
source_conversation_uuid: 702c2d45-c80d-429a-a545-2850a38a6543
conversation_title: 'Mobile SOC center setup options'
created_at: 2026-07-22T11:23:34.845895Z
doc_id: DC-OS-001
description: 'DC-OS-001: The D-Central Ecosystem Operating System, node-native and orb-native master spec'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-OS-001 — D-Central Ecosystem Operating System

## Master Specification · Revision 1.0 · Node-Native, Orb-Native Interface Layer

| Field | Value |
|---|---|
| **Document ID** | DC-OS-001 |
| **Revision** | 1.0 |
| **Classification** | Open Software (AGPL-3.0) + Open Hardware interface (CERN-OHL-W-2.0) |
| **Author** | Toussaint — D-Central Group Inc. |
| **Status** | Design — Execution pending (see DC-STATUS-001) |
| **Related** | DC-SHI-SPEC-001/002, DC-ORB-SPEC-001, DC-PLANE-001, DC-SWARM-001, DC-LKB-001…003, DC-FRACTAL-001, DC-MOGUL-001, DC-TPL-000, classIQ (DC-CLASSIQ-SPEC-001), Sovereign DAO OS, W3C DID/VC identity layer |

---

## 1. Purpose and philosophy

DC-OS is the operating system of the D-Central ecosystem: the layer through which any member navigates every cell, vault, node, mesh service, template, and governance function of the ecosystem, authenticated by their DID and scoped by their VCs. It is not an operating system in the kernel sense (the node runs Linux underneath); it is the **interaction and navigation grammar** — the shell, command language, and interface model — that makes the entire distributed ecosystem feel like one coherent, navigable machine.

DC-OS is architected against three principles inherited from the ecosystem's core doctrine:

**Keyboard-and-command native, pointer-optional.** The system is driven primarily by shortcuts, commands, and a composable verb grammar — fluid like a graphical programming language, not a menu tree. The mouse is a fallback, never the primary path. This is what the fluency coach (DC-FLUENT) teaches and what makes power-users fast.

**Node-native and orb-native, not screen-native.** DC-OS does not assume a rectangular screen with a pointer. Its primary surfaces are the SHI node (the computer that actually runs it) and the orb (the ambient interface organ through which most members touch it). Conventional screens (phone, laptop) are supported as additional surfaces, but the system is designed so that a member with only an orb and voice, or an orb and a keyboard, has full navigational capability. The screen is one client among several; the node is the computer; the orb is the face.

**Anti-attention-extraction.** Consistent with the SHI and ORB specs, DC-OS has no feed, no scroll, no engagement surface. It appears on genuine need, executes, and recedes. It is a tool for doing, not a place to dwell.

## 2. The two-plane architecture: node-native and orb-native

DC-OS runs as two tightly-coupled planes, mirroring the thin-client model of the orb line.

**2.1 The node plane (the computer).** The SHI node runs the DC-OS core: the command interpreter, the capability resolver (which VCs authorize which verbs), the mesh addressing layer, the local agent runtime (DC-ANIMA), and the vault/identity endpoints. All heavy computation, all persistent state, and the member's self (agent, keys, data) live here or in the mesh — never in the interface surface. A member's DC-OS environment is anchored to their DID and follows them across surfaces because the node and mesh hold it, not the device in hand.

**2.2 The orb plane (the face).** The orb is the primary ambient surface for DC-OS. Per DC-ORB-SPEC-001 it is a thin client: it captures (voice, gesture, presence), displays (ambient spherical output, summoned detail), authenticates (DID session), and connects (to node and mesh) — and holds nothing after the session ends. DC-OS is therefore architected so that its entire interaction model is expressible through the orb's capabilities: voice command, gesture over the orb's sensing field, the orb's spherical/summoned display for output, and ephemeral session authentication. Any orb becomes the member's DC-OS surface on authentication and forgets them on session end.

**2.3 Surface independence.** Because state lives in the node/mesh, DC-OS surfaces are interchangeable. A command begun by voice at a Pebble can be continued by keyboard at a laptop and confirmed by gesture at a Globe — one session, one environment, three surfaces. The system treats every surface as a thin lens onto the same node-anchored environment. Supported surfaces: orb (primary ambient), keyboard/terminal (primary power), voice (universal), conventional screen (detail and legacy), DC-WEAR (glanceable/notification), and the campus Hearth/Beacon (shared/civic).

## 3. The command grammar (the graphical-programming-language feel)

DC-OS's interaction core is a composable verb-noun-pipe grammar — designed to feel like a dataflow/graphical programming language that can be typed, spoken, or assembled visually, so the same operation is expressible on a keyboard, by voice, or by gesture-assembled blocks on an orb or screen.

**3.1 Nouns are ecosystem entities.** Everything addressable in the ecosystem is a noun: `vault`, `cell`, `node`, `member`, `template`, `proposal`, `stream`, `credential`, `orb`, `sensor`, `agent`, and their scoped children (`vault.household`, `cell.gym.001`, `stream.energy`). Nouns resolve through the mesh addressing layer and are permission-filtered by the caller's VCs before they are even shown.

**3.2 Verbs are capabilities.** `view`, `pay`, `propose`, `vote`, `route`, `approve`, `deploy`, `credential`, `summon`, `mark`, `yield` (governance and stigmergic verbs included). Each verb is gated: the capability resolver checks the caller's VCs against the verb-on-noun before execution. A member without the treasurer VC simply cannot invoke `pay` on a cluster vault — the verb does not resolve, rather than failing after the fact.

**3.3 Pipes compose.** The power of the grammar is composition, Unix-pipe style: `vault.household.balance | filter debt | pay` or `cell.* | where margin < 0 | summon.report`. This is what gives DC-OS its graphical-programming-language fluidity — small composable operations chained into workflows, which power-users type, casual members speak in natural language (the agent parses intent to grammar), and visual users assemble as connected blocks. All three front-ends target the same underlying pipe grammar.

**3.4 The command palette.** The universal entry point is a summonable palette (the Cmd-K / spotlight model, but ecosystem-wide and surface-independent): invoke it from any surface, type or speak intent, and DC-OS resolves it to a grammar expression, shows the permission-scoped options, and executes. On the orb this is a voice-or-gesture summon; on a keyboard it is a chord; on a screen it is the palette overlay.

**3.5 The agent as universal translator.** DC-ANIMA sits between natural language and the grammar. A member need not learn the grammar to use the system — they speak intent and the agent proposes the grammar expression, shows it, and asks for confirmation on any consequential verb. Power-users bypass the agent and type grammar directly. The fluency coach's job (DC-FLUENT) is precisely to move members from agent-mediated to direct-grammar fluency over time, earning VCs as they go.

## 4. Identity, capability, and scope (DID/VC-native)

**4.1 DID is the login.** There is no username/password. A member authenticates by their decentralized identifier, proven by keys they hold (in a Pebble, a DC-WEAR, or a hardware key). The session is bound to the DID and is ephemeral on shared surfaces.

**4.2 VCs are the permission system.** Every capability in DC-OS is authorized by verifiable credentials. A guard licence VC authorizes security-event verbs; a treasurer VC authorizes vault-payment verbs; a steward VC authorizes cell-deployment verbs; a food-handler VC authorizes kitchen-cell QA verbs. Capability is therefore portable across the whole fractal — the same VC grants the same verbs in any cell or cluster the member operates in. This is how DC-OS navigates "the entire ecosystem using your DID": the grammar is universal, and your VCs light up exactly the subset of it you are authorized to invoke, everywhere, consistently.

**4.3 Scope follows the fractal.** Nouns are scoped by the recursion layers of DC-FRACTAL-001: a member sees and acts on their household layer by default, their cell layer with the relevant role VC, their cluster layer as a delegate, and the commons layer only with commons-level credentials. The same command (`vault.balance`) resolves to different scopes depending on the caller's position in the fractal, and never exposes a layer the caller is not credentialed for.

**4.4 The regulated boundary in the OS.** Verbs that touch regulated operations (per DC-LIC-001's Regulated Entity Pattern) require the accountable licensed human's DID specifically — they cannot be satisfied by a DAO vote or delegated credential. DC-OS enforces the regulated boundary at the capability-resolver level: a `dispatch.guard` or `licensed.clinical` verb resolves only for the named accountable human, structurally, so the OS itself cannot be used to route around provincial licensing.

## 5. The capture and telemetry boundary (built in, not bolted on)

DC-OS includes self-scoped capture capability — screen capture, session recording, and infrastructure telemetry (network, system signals) — governed by a hard boundary consistent with the ecosystem's refused intelligence/surveillance department:

Capture is always **user-invoked, self-scoped, DID-owned, and consent-gated**. A member may capture their own screen, record their own session, and inspect telemetry of infrastructure they own or are contracted to defend (the MSSP/NOC case). DC-OS provides these as first-class verbs (`capture.self`, `telemetry.owned`).

DC-OS **structurally refuses** capture of another person for a third party's benefit: no verb resolves that records a worker's screen for a manager, sniffs a member's traffic for a dashboard, or logs a coached person's signals for anyone with power over them. This is enforced at the capability-resolver level — the surveillance verbs do not exist in the grammar, not merely disabled by policy. Sensitive-context suppression (the password-field rule, generalized) is a kernel-level guarantee of the capture subsystem.

This boundary is what lets DC-OS carry powerful capture capability — for security operations, self-directed learning, and personal productivity — without becoming the bossware the same technology becomes everywhere else.

## 6. The interface model on the orb (detailed)

**6.1 Ambient state.** At rest, the orb shows the DC-OS ambient layer per DC-ORB-SPEC-001 §5: presence, gentle status, nothing demanding. DC-OS surfaces information here only on genuine need (a vault alert, a governance vote opening, an exception in a cell the member is responsible for).

**6.2 Summoned interaction.** The member summons DC-OS by voice ("show me the household vault") or gesture (a defined motion over the orb's sensing field). The orb's display renders the summoned view on its spherical or projected surface; the member navigates by voice, gesture, or a paired keyboard. Consequential verbs require explicit confirmation, spoken or gestured.

**6.3 Gesture as grammar.** The orb's sensing field (mocap, mmWave, LiDAR per tier) lets gesture assemble grammar: pointing selects a noun, a directional motion applies a verb, a connecting motion pipes. This is the "graphical programming language" made literally spatial — composing operations in the air over the orb — for members who prefer it to typing or speaking. Gesture, voice, and keyboard are three front-ends to the identical pipe grammar of §3.

**6.4 Session ephemerality.** When the member ends the session or walks away (presence-sensed), the orb wipes the session and returns to ambient. Nothing of the member persists on the orb — the node and mesh hold their environment. This is what makes any orb usable as any member's DC-OS surface.

## 7. Node-native runtime detail

DC-OS core services running on the SHI node: the command interpreter and grammar parser; the capability resolver (VC-to-verb authorization, OPA-first per the SHI agent architecture); the mesh addressing and discovery layer (how nouns across the fractal are located and permission-filtered); the DC-ANIMA agent runtime (natural-language-to-grammar translation, per-member); the vault and identity endpoints (Lakou rails and DID/VC); the capture subsystem with its boundary enforcement (§5); and the surface-session manager (which orchestrates interchangeable surfaces onto one node-anchored environment). All of this runs within the node's existing compute and policy framework from DC-SHI-SPEC-001/002 — DC-OS is a layer on the node, not a separate box.

## 8. Relationship to other ecosystem software

DC-OS is the navigation and interaction layer; it does not replace the applications it navigates. classIQ, the fluency coach, the agent cabinet, the vault modules, the governance tooling, and every cell's operational software are **reached through** DC-OS and **driven by** its command grammar, but each is its own system. The relationship is: DC-OS is the shell and grammar; the applications are the programs; the node is the computer; the orb is the face; the mesh is the network; the DID/VC layer is the identity and permission system.

## 9. Honest status and build path

DC-OS is design-stage, execution-zero, like the rest of the ecosystem per DC-STATUS-001. Its dependencies are real: it needs the DID/VC identity layer, the Lakou vault rails, the mesh addressing layer, and at minimum a node and one orb tier to be meaningful. None of these exist in hardware yet. The rational build path mirrors the orb's: first, a **terminal-only DC-OS** on a single node — the command grammar, capability resolver, and DID/VC auth, driven by keyboard, navigating a handful of real nouns (one vault, one cell). This is buildable in software now and is the natural companion to the Company Zero agent cabinet, since the cabinet's operations are exactly the first verbs worth having. The orb-native and gesture front-ends come only after an orb exists. The graphical/voice/gesture fluidity is the destination; a working keyboard-driven grammar over one real node and one real vault is the first executable step — and it should not be built before there is a real vault and cell for it to navigate, or it becomes another design-complete, execution-zero artifact.
