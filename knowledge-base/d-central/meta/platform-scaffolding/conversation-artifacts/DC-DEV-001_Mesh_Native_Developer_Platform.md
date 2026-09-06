---
source_conversation_uuid: 702c2d45-c80d-429a-a545-2850a38a6543
conversation_title: 'Mobile SOC center setup options'
created_at: 2026-07-22T11:23:34.845895Z
doc_id: DC-DEV-001
description: 'DC-DEV-001: the developer platform for natively deploying and managing apps, services, SaaS, and real-world services on the mesh'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
topic: "dcentral-developer-ecosystem-os-specs"
consolidated_into: docs/DC-DEV-OS-RECONCILED-001.md
---

# DC-DEV-001 — Mesh-Native Developer Platform

## How Developers Build, Deploy, and Manage Apps, Services, SaaS, and Real-World Services on the D-Central Mesh

| Field | Value |
|---|---|
| **Document ID** | DC-DEV-001 |
| **Revision** | 1.0 |
| **Classification** | Open Software (AGPL-3.0) |
| **Author** | Toussaint — D-Central Group Inc. |
| **Status** | Design — Execution pending (see DC-STATUS-001) |
| **Related** | DC-OS-001 (grammar/capability), DC-OS-002 (interop/compatible sites), DC-SHI-SPEC-001/002 (node compute), DC-FRACTAL-001 (cells/clusters), DC-LKB-001…003 (vaults/billing), DC-MOGUL-001 (Principal Track), DC-TPL-000, DC-CLASSIQ-SPEC, W3C DID/VC |

---

## 1. Purpose

Every other ecosystem document assumes cells *have* software — a gym's booking system, the NOC's monitoring, classIQ, the vault modules, a member's storefront. DC-DEV-001 specifies how that software gets **built, deployed, run, billed, and managed natively on the mesh** — the platform layer that turns D-Central from an ecosystem you use into an ecosystem you can *build on*. It is the ecosystem's answer to what AWS + Vercel + Stripe + an app store are to the conventional internet, rearranged around the ecosystem's own primitives: DID identity, VC permissions, node compute, mesh addressing, vault billing, and the refused-departments boundary.

A "mesh-native app" spans a spectrum: a pure-software SaaS, a service that coordinates real-world work (dispatch, delivery, booking), and a physical/cyber hybrid (a cell's operational software plus its sensors). DC-DEV-001 targets all three, because in this ecosystem they are the same deployment model with different amounts of physical world attached.

## 2. The core idea: an app is a cell's software, and compute is the mesh

Two inversions of the conventional model define the platform.

**Compute is federated node capacity, not a datacenter.** The mesh is a fabric of SHI nodes (residential through campus) and cluster/campus servers, each with real compute (per DC-SHI-SPEC-001/002 and DC-SCALE-001's distributed-compute regime). A mesh-native app runs on this capacity — placed on the developer's own node, a cell's node, a cluster server, or, with consent and payment, borrowed capacity from other nodes. The platform's scheduler places workloads the way a cloud places containers, except the "region" is a household, a cell, or a campus, and the capacity is member-owned and vault-metered.

**An app is addressable as an ecosystem noun.** Per DC-OS-001, everything is a noun in the command grammar. A deployed app registers as a noun (`app.booking.gym001`, `service.dispatch.cluster3`) and its capabilities become verbs, VC-gated like every other verb. There is no separate "app store namespace" bolted on — apps live in the same addressing and permission system as vaults and cells, which is what makes them native rather than hosted-alongside.

## 3. The deployment model

**3.1 The app manifest.** A mesh-native app declares itself in a manifest: its compute requirements (CPU/RAM/GPU/storage, and whether it needs sensor or actuator access), its data requirements (what it reads/writes, at what scope in the fractal), the VCs it requires of its users, the capabilities (verbs) it exposes, its billing model (vault metering), and its declared data-handling under CTS. The manifest is the contract the platform enforces — an app cannot access data or capabilities it did not declare, checked at the capability-resolver level (OPA-first, per the SHI agent architecture).

**3.2 Packaging.** Apps package as OCI containers (the Part A classIQ stack is the reference — Docker Compose services on a node) or as lighter node-native functions for small workloads. The ecosystem is container-first because that is what already runs on the nodes; no bespoke runtime is imposed. A registry (the ecosystem's own, mesh-hosted) holds signed images; signatures chain to the developer's DID so provenance is verifiable.

**3.3 Placement and the scheduler.** The developer requests placement — `deploy app.booking.gym001 → node.gym001` for a single cell, or `→ cluster3` for a shared service, or `→ mesh (region=cluster3, replicas=3)` for a distributed one. The scheduler honors data-locality and sovereignty rules: an app handling a cell's data runs on that cell's or cluster's nodes by default and does not silently migrate members' data off their own infrastructure. Borrowed capacity (running on other members' nodes) is opt-in on both sides, consideration flows through vaults, and sensitive-data workloads are pinned by policy.

**3.4 Addressing and discovery.** On deploy, the app registers in the mesh addressing layer and becomes reachable through DC-OS grammar and (if it opts in) as a DC-compatible site per DC-OS-002 — the same deployment is simultaneously an OS-addressable service and, optionally, a public mesh-hosted site. This is the unification the interop protocol describes: a mesh-hosted app has no "external handshake" because it is already inside.

## 4. Identity, permission, and billing are inherited, not built

The platform's central developer benefit: an app inherits the ecosystem's hard problems already solved.

**Identity & auth** — users authenticate by DID; the app never builds a login system, stores passwords, or runs its own account database. It declares required VCs and the capability resolver enforces them.

**Permissions** — authorization is VC-to-verb, ecosystem-wide and portable. An app trusts a member's guard-licence VC or food-handler VC without verifying credentials itself.

**Billing** — the app declares a vault-metering model (per-call, subscription, usage, revenue-share to the commons per DC-TPL-000) and the Lakou rails handle payment, payout, and the commons royalty. No Stripe integration, no separate billing stack; money is a native primitive.

**Data & transparency** — the app's declared data handling is published under CTS; members can see what any app they use does with their data, and the manifest is the enforced truth, not a privacy policy nobody reads.

**Distribution** — a deployed app is discoverable through DC-OS and, if public, as a mesh-hosted site; there is no gatekept app store taking a platform tax. The only economic flow to the commons is the transparent template/commons royalty the app itself declares.

## 5. Real-world services (the physical dimension)

Mesh-native apps are not limited to software, because the ecosystem's cells are physical. A "service" app coordinates real-world work by combining software capabilities with the ecosystem's operational cells:

A **dispatch/booking service** exposes verbs (`book`, `dispatch`, `schedule`) that route to a cell's human operators and, where relevant, its sensors — a home-repair booking app dispatches a DC-TPL-CON tradesperson, informed by the target node's sensor context (the SHI "service provider arrives already knowing" principle). A **delivery/logistics service** coordinates MeshRide and cluster logistics capacity. A **monitoring service** (the NOC) is a mesh-native app consuming sensor telemetry and producing human-actionable events. The pattern: **software verbs on the mesh, fulfilled by cells in the physical world, billed through vaults, credentialed by VCs, coordinated by the same scheduler and addressing layer as pure-software apps.** This is why the ecosystem does not distinguish "SaaS" from "real-world service" at the platform layer — they are one deployment model with different amounts of physical fulfillment attached.

The regulated boundary (DC-LIC-001) applies: a service app coordinating regulated work (dispatching licensed guards, booking clinical care) routes the accountable action to the named licensed human; the app orchestrates, it does not become the licensee.

## 6. Developer lifecycle & the Principal Track

Developers are members, and building on the mesh is a venture path. The lifecycle: a developer authenticates by DID; scaffolds an app against the manifest schema and the DC-OS grammar SDK; tests locally on their own node; deploys to a target cell/cluster; meters through vaults; and iterates with observability (logs, metrics, and — self-scoped only, per the DC-OS-001 capture boundary — telemetry of infrastructure they own). Apps themselves are **DC-TPL templatable**: a proven app (a booking system, a monitoring config) becomes a template other cells deploy, moving Draft → Validated → Proven and spreading through the fractal with upstream patches. A developer who authors widely-adopted apps climbs the Principal Track (DC-MOGUL-001) as a software Principal, earning through their own deployments plus the commons appreciation of what they authored — the same economics as any other spine, applied to code.

## 7. The boundaries (built into the platform, not policy notes)

Three constraints are structural, enforced by the platform, because a developer platform is exactly where an ecosystem's guarantees are won or lost:

**The manifest is the enforced contract.** An app cannot exceed its declared data/capability access; the resolver blocks undeclared access at runtime. There is no "trust the developer" gap.

**The refused departments apply to apps.** The platform will not run apps whose declared purpose is surveillance of people for third parties, attention-extraction/engagement-farming, or enforcement/force — the same refusals that bound the whole ecosystem, enforced at the manifest-review and capability-resolver layers. The capture/telemetry boundary of DC-OS-001 §5 applies to every app: self-scoped and owned-infrastructure capture only; no verb exists to surveil a person for someone with power over them.

**Data sovereignty by default.** An app runs on the data owner's own or cluster infrastructure by default and does not migrate members' data off their nodes without explicit, scoped, revocable consent (DC-OS-002 delegation rules). Borrowed compute is opt-in and vault-metered on both sides.

## 8. Honest status & build path

DC-DEV-001 is design-stage and depends on primitives that do not yet exist in execution: the DID/VC layer, the mesh addressing layer, vault rails, and real node compute. It is therefore *later* on the critical path than the things it would host. The rational first step is minimal and internal: a **single-node deployment path for the ecosystem's own first apps** — the Company Zero agent cabinet, the terminal-only DC-OS, and the Part A classIQ stack all run as containers on one node today, and formalizing "how an app is packaged, addressed, permissioned, and vault-metered on one node" against those three real workloads is the seed of the platform. The federated scheduler, borrowed-compute market, public mesh-hosting, and third-party developer onboarding come only once there are multiple nodes, a real identity layer, and real apps worth hosting. Building the full platform before there is a single deployed app to run on it would be the DC-STATUS-001 failure mode at the infrastructure layer — so the platform grows from the ecosystem's own first three apps outward, not from a spec of a marketplace with nothing in it.


<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Topics:**
- [[knowledge-base/_topics/dcentral-developer-ecosystem-os-specs|dcentral-developer-ecosystem-os-specs]]

**Consolidated into:**
- [[docs/DC-DEV-OS-RECONCILED-001]]

<!-- AUTO-GENERATED RELATED END -->
