# DC-DEV-OS-RECONCILED-001 — D-Central Ecosystem OS & Developer Platform, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `dcentral-developer-ecosystem-os-specs` (2 docs).

## Current understanding

DC-OS-001 specifies the ecosystem's interaction/navigation layer (the "shell"); DC-DEV-001 specifies the
platform for building and deploying third-party software on top of it (the "app runtime"). DC-DEV-001
explicitly builds on DC-OS-001's grammar and is internally consistent with it on every shared concept.

**DC-OS-001, the ecosystem operating system (incorporated):** not a kernel-level OS — a
node-native/orb-native interaction grammar layered over Linux, built on three stated principles
(keyboard/command-native with pointer as fallback; node-and-orb-native rather than screen-native; and
structurally anti-attention-extraction — no feed, no scroll) [§1]. Runs as two coupled planes: the node
plane holds all state, computation, and the member's identity/keys; the orb plane is a stateless thin
client that authenticates on session start and forgets the member on session end, making any orb usable
as any member's surface [§2]. Its command grammar is composable verb-noun-pipe (`vault.household.balance
| filter debt | pay`), addressable via keyboard, voice, or orb gesture as three front-ends to one
underlying grammar, mediated by an agent (DC-ANIMA) that translates natural language to grammar
expressions for non-power-users [§3]. Authentication is DID-based with no username/password; every
capability is VC-gated, verbs simply don't resolve without the right credential rather than failing
after the fact; scope follows the DC-FRACTAL-001 recursion layers (household → cell → cluster →
commons); and regulated-operation verbs resolve only for the specifically named accountable licensed
human, never a DAO vote or delegated credential [§4]. Capture/telemetry capability is built in but
structurally bounded: self-scoped, DID-owned, consent-gated capture is a first-class verb, while
verbs that would capture *another* person for a third party's benefit simply do not exist in the
grammar — enforced at the capability-resolver level, not by policy [§5]. Stated build path: start with
a terminal-only, keyboard-driven grammar on one real node navigating one real vault and cell — orb and
gesture front-ends come only once an orb physically exists [§9].

**DC-DEV-001, the developer platform (incorporated):** the platform for building, deploying, billing,
and managing software natively on the mesh — the ecosystem's analogue to "AWS + Vercel + Stripe + an app
store," rearranged around DID identity, VC permissions, node compute, mesh addressing, and vault billing
[§1]. Two inversions define it: compute is federated node capacity rather than a datacenter (the
scheduler places workloads on a developer's own node, a cell's node, a cluster server, or opted-in
borrowed capacity), and a deployed app is addressable as an ecosystem noun in DC-OS-001's own grammar
(`app.booking.gym001`) rather than living in a separate app-store namespace [§2]. Apps declare a
manifest (compute/data requirements, required VCs, exposed verbs, billing model) that the capability
resolver mechanically enforces as the only contract — an app cannot exceed its declared access [§3, §7].
Identity, permissions, and billing are explicitly inherited rather than built by each app: DID
authentication, VC-to-verb authorization, and vault-metered billing through the Lakou rails, with no
app-level login system, credential-checking, or Stripe integration [§4]. "Real-world services"
(dispatch, delivery, monitoring) are treated as the same deployment model as pure software, just with
more physical fulfillment attached, and are explicitly still bound by the regulated-entity pattern
(an app orchestrates regulated work, it does not become the licensee) [§5]. A developer lifecycle
runs from DID authentication through scaffolding, local test, deployment, and vault metering, with
successful apps promotable to DC-TPL templates and their authors eligible for the Principal Track
(DC-MOGUL-001) [§6]. The same three structural boundaries as DC-OS-001 apply at the platform level:
the manifest is an enforced contract, refused-department restrictions (no surveillance/attention-
extraction/enforcement apps) apply to third-party apps too, and data sovereignty is default-on (apps
run on the data owner's own infrastructure, no silent migration) [§7]. Stated build path mirrors
DC-OS-001's: formalize packaging/addressing/permissioning/billing against the ecosystem's own first
three real workloads (the Company Zero agent cabinet, terminal-only DC-OS, and the classIQ stack)
before building a federated scheduler or third-party onboarding for an empty marketplace [§8].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| DC-OS-001 purpose and three founding principles | DC-OS-001 §1 | incorporated |
| Two-plane (node/orb) architecture and surface independence | DC-OS-001 §2 | incorporated |
| Verb-noun-pipe command grammar and command palette | DC-OS-001 §3 | incorporated |
| DID/VC identity, capability scoping, regulated-boundary enforcement | DC-OS-001 §4 | incorporated |
| Capture/telemetry boundary (self-scoped only, structurally refused for surveillance) | DC-OS-001 §5 | incorporated |
| Orb interface detail and node-native runtime services | DC-OS-001 §6-7 | incorporated |
| DC-OS-001 honest status and terminal-first build path | DC-OS-001 §9 | incorporated |
| DC-DEV-001 purpose, platform inversions (federated compute, apps as nouns) | DC-DEV-001 §1-2 | incorporated |
| App manifest, packaging, scheduler placement, addressing | DC-DEV-001 §3 | incorporated |
| Inherited identity/permissions/billing/transparency/distribution | DC-DEV-001 §4 | incorporated |
| Real-world/physical services as the same deployment model | DC-DEV-001 §5 | incorporated |
| Developer lifecycle and Principal Track economics | DC-DEV-001 §6 | incorporated |
| Platform-level structural boundaries (manifest enforcement, refused departments, data sovereignty) | DC-DEV-001 §7 | incorporated |
| DC-DEV-001 honest status and minimal-first build path | DC-DEV-001 §8 | incorporated |

## Unresolved tensions

None identified in this pass — DC-DEV-001 is explicitly built as a layer on top of DC-OS-001's grammar
(reusing its noun/verb/VC model rather than defining a competing one), both documents state the
identical "design-stage, execution-zero" status and cite the same dependency chain (DID/VC layer, mesh
addressing, vault rails, real node compute), and both independently arrive at the same build-path
philosophy — don't build the general platform before there are real, specific workloads to run on it.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/meta/platform-scaffolding/conversation-artifacts/DC-DEV-001_Mesh_Native_Developer_Platform.md`
- `knowledge-base/d-central/meta/platform-scaffolding/conversation-artifacts/DC-OS-001_Ecosystem_Operating_System.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/meta/platform-scaffolding/conversation-artifacts/DC-DEV-001_Mesh_Native_Developer_Platform.md,
  knowledge-base/d-central/meta/platform-scaffolding/conversation-artifacts/DC-OS-001_Ecosystem_Operating_System.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

Neither source doc is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

*No cross-references detected to/from other docs/*.md files.*

<!-- AUTO-GENERATED RELATED END -->
