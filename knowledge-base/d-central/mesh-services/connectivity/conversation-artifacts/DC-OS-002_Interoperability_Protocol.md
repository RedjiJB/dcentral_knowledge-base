---
source_conversation_uuid: 702c2d45-c80d-429a-a545-2850a38a6543
conversation_title: 'Mobile SOC center setup options'
created_at: 2026-07-22T11:23:34.845895Z
doc_id: DC-OS-002
description: 'DC-OS-002: Interoperability and compatible-site protocol for the D-Central OS'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-OS-002 — Interoperability & Compatible-Site Protocol

## How DC-OS Reaches the Wider Internet, and How Sites Become Ecosystem-Native

| Field | Value |
|---|---|
| **Document ID** | DC-OS-002 |
| **Revision** | 1.0 |
| **Classification** | Open Software (AGPL-3.0) + open protocol specification |
| **Author** | Toussaint — D-Central Group Inc. |
| **Status** | Design — Execution pending (see DC-STATUS-001) |
| **Extends** | DC-OS-001 (the ecosystem operating system) |
| **Related** | DC-DEV-001 (mesh-native apps), DC-SHI-SPEC-001/002, DC-FRACTAL-001, DC-LKB-001…003, W3C DID/VC |

---

## 1. Purpose

DC-OS-001 defines how a member navigates the ecosystem. DC-OS-002 defines how DC-OS reaches **outward** — to the open internet and to services that are not (yet) part of the ecosystem — and how any site can become ecosystem-native. It specifies a compatibility gradient from fully mesh-native services down to legacy websites that know nothing about D-Central, so that a member's DC-OS works everywhere while trusting each surface only as far as it has earned.

The design collapses a distinction the conventional web treats as fundamental: "using an app" versus "browsing a site." In DC-OS, a service is a noun in the command grammar whether it runs on the mesh or on the open internet — only the interaction mode and the trust guarantees differ.

## 2. The three interaction modes

A DC-compatible site supports one or more of three modes, in ascending order of capability and required trust.

**2.1 Intent handshake (structured interface).** The site publishes a machine-readable action schema at a well-known endpoint. Instead of the DC-OS agent scraping and clicking a human UI, DC-OS speaks intent directly and the site executes it natively, returning a structured result. This is a clean machine-to-machine exchange: DC-OS expresses "book this, buy that, query this," the site's schema defines the available actions and their parameters, and the result comes back as data rather than a rendered page to be parsed. Form-filling disappears because there is no form — there is an action and a structured response.

**2.2 VC verification.** The member presents selectively-disclosed verifiable credentials, and the site verifies a claim without collecting the underlying data or requiring any form entry. "Prove you are over 18," "prove you hold a valid guard licence," "prove you are a member in good standing," "prove payment capacity" — each answered by a cryptographic proof the member's DID produces, disclosing only the specific claim. The site learns the fact it needs and nothing more; the member uploads no documents and fills no fields.

**2.3 Delegated authority.** The member's DID grants the site a scoped capability to act on their behalf — take a payment, hold a booking, exchange a specific data set. This is the most powerful mode and the most dangerous, and §4 governs it strictly. The grant is never a standing blanket permission; it is a narrow, time-boxed, logged, instantly-revocable capability.

## 3. The compatibility gradient

Services occupy one of three tiers, and DC-OS degrades gracefully down the gradient so it functions against anything.

**3.1 Native / mesh-hosted (best).** The service is a cell or app running on the ecosystem mesh (per DC-DEV-001) — DID-native, VC-native, vault-native. There is no "external handshake" because there is nothing external: the service is addressable as a noun in the DC-OS grammar like any other cell, and interaction is the OS talking to itself. A member's storefront, a cell's booking page, the co-op's services all live here. A mesh-hosted service inherits every ecosystem guarantee for free — DID auth, VC permissions, vault billing, CTS transparency, the refused-departments boundary, and the capture firewall of DC-OS-001 §5 — which means it is **trustworthy by construction**: it cannot secretly track a member because it runs on infrastructure that structurally cannot. This is the on-ramp for any cell to have a public presence that is native rather than bolted-on; the same document a cell publishes as its storefront is simultaneously its DC-OS-addressable interface.

**3.2 DC-compatible (good).** An ordinary internet site, hosted anywhere, that has adopted the protocol — action schema, VC verification, and optionally delegation endpoints. It stays on the normal web and speaks the ecosystem's language. This is the interoperability target that lets the outside world become reachable *without* joining the ecosystem: a business can serve DC-OS members natively while remaining an independent web business. Adoption is incremental — a site can support only VC verification (no more passwords for DC members), or add the intent handshake, or add delegation, in any order.

**3.3 Legacy (fallback).** A site that knows nothing about D-Central. DC-OS's agent interacts with it the conventional way — navigating its human UI and filling its forms using the member's DID-held profile and VC data, with confirmation on anything consequential (the autocomplete and intent-translation capability of DC-OS). This works everywhere, assumes nothing of the site, trusts it least, and degrades gracefully: the member still gets assisted, credential-backed form-filling even on a site that has never heard of the ecosystem.

The gradient means one member experience across the whole internet: DC-OS tries the most native mode a service supports and falls back as needed, so the member simply expresses intent and the OS handles how much of it the far side can meet.

## 4. Delegated authority — the hard boundary

Delegated authority is where interoperability can recreate exactly the harm the ecosystem exists to refuse: the "this app may act on your behalf forever" permission that becomes silent, unbounded, unrevocable access. The protocol therefore constrains every grant structurally, not as a policy note:

**Narrow by default.** A grant authorizes a specific action on a specific resource for a specific purpose — "charge $40 for this booking," not "access my payment methods." The capability names exactly what it permits; anything not named is denied.

**Expiring by default.** Every grant carries an expiry. A booking hold expires when the booking resolves or the window closes; a one-time payment authority is consumed on use. Standing grants (a recurring subscription) are possible but must be explicit, separately consented, and visible in the member's active-grants list.

**Logged always.** Every grant and every action taken under it is recorded to the member's own DC-OS, visible in one place. There is no delegated action the member cannot see after the fact.

**Revocable instantly.** The member revokes any grant from their own DC-OS at any time, and revocation is immediate and enforced at the capability layer — not a request the far side may honor, but a capability the ecosystem stops recognizing. A revoked grant cannot be exercised even mid-transaction.

These four are hard requirements. A site requesting delegation that cannot be expressed as a narrow, expiring, logged, revocable capability does not get delegation — it falls back to per-action confirmation (mode 2.1 with the member approving each consequential step). The powerful capability is admitted only inside constraints that make its abuse structurally impossible, the same discipline the capture boundary applies in DC-OS-001 §5.

## 5. The well-known endpoint and discovery

A DC-compatible site advertises its capabilities at a well-known path (the ecosystem's reserved discovery URI), returning its action schema, the VC types it accepts, its delegation endpoints (if any), its declared data handling (for CTS-style display to the member before they interact), and — if mesh-hosted — its DC-OS noun address. DC-OS reads this on first contact and caches it, so a member's OS knows, before the member acts, exactly what a site can do natively and what will fall back to assisted interaction. Mesh-hosted services register this automatically on deploy (DC-DEV-001 §3.4); DC-compatible sites publish it themselves; legacy sites simply return nothing and get the fallback path.

## 6. Boundaries

The refused-departments boundary and the capture firewall of DC-OS-001 apply to every mode: DC-OS will not present credentials to, or accept delegation from, a service whose declared purpose is surveillance-for-third-parties, attention-extraction, or enforcement/force, and it never exposes more of the member's data than the specific claim or action requires. VC verification is always selective-disclosure minimal. The member's data sovereignty is preserved across the whole gradient — even in legacy fallback, the member's profile data lives in their DID vault and is released field-by-field with confirmation, never handed over wholesale.

## 7. Honest status & build path

DC-OS-002 depends on DC-OS-001, the DID/VC layer, and (for the native tier) the mesh-hosting of DC-DEV-001 — none of which exist in execution yet. The rational first step is the *legacy fallback* mode against one real need: DID-backed, VC-assisted form-filling from a member's own profile on the ordinary web, which is useful the moment there is one member with a populated DID vault, and requires no cooperation from any site. The intent handshake and VC verification become meaningful once there are DC-compatible sites to talk to; the native tier arrives with mesh-hosting. Delegated authority is built last and most carefully, because its constraints (§4) are the whole point and must be enforced at a capability layer that itself must be proven first. Specifying the marketplace of compatible sites before a single site or a single populated DID exists would be the DC-STATUS-001 failure mode — so this protocol, too, grows from one member's real profile filling one real form outward.
