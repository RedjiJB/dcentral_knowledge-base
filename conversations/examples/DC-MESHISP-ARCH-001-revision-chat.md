# D-Central ISP implementation in Haiti - Claude

Source: [Claude Chat](https://claude.ai/chat/fc99aa3d-f993-404c-8aee-09bc55305583)
Extracted: 2026-08-23T05:28:35.313Z
🚀 Exported with [Save my Chatbot](https://save.hugocolin.com)!

---

## User

show me full meshisp network architecture

## Claude

Created a file, read a file

Created a file, read a file

That's every layer from this conversation in one place — physical topology through cell tower integration, power tiers, the DAO trees, discovery/routing, services, device provisioning, and economics.

Two things worth your attention before this goes anywhere near a proposal or funder:

The **open items table at the end (§11)** is the honest state of the project — ten blockers, none invented for this doc, all pulled from what surfaced across the actual design work. OB-1 and OB-2 (CONATEL) still gate almost everything else.

The **`ProvisioningDAO` duplication** is the one structural decision sitting unmade the longest. Worth resolving before DC-SIM tries to simulate subscriber onboarding, since right now two DAOs both think they own it.

Dc meshisp arch 001

Document · MD 

Download

## User

so a phone can connect to the mesh throgh the router or cell which ever closer

## Claude

Thought for 19s

Thought for 19s

Close, with one correction: it's not really distance, it's radio availability plus what the phone already does by default — prefer known WiFi over cellular data, same as any phone today. Two real asymmetries worth knowing, though.

**Different identity binding per path**

- **Via WiFi/router (CPE)** — the household's CPE holds the subscription and DID. A stock phone on that WiFi rides the CPE's provisioned connection, same as connecting to home WiFi anywhere — no individual DID needed for basic internet.

- **Via cell tower** — the individual eSIM/SIM identifies the subscriber directly, independent of whose router is nearby.

So "which one you're on" isn't just a signal question, it's also "which entity is actually the billed subscriber right now" — the household account, or the person's own line.

**The one real gap: call continuity across the switch**

If a call is live over VoWiFi through the router and the phone walks out of range onto cellular, that's not automatic just because both networks exist — it needs proper handoff logic (the IMS-style VoWiFi-to-cellular handover pattern), or the call drops and has to reconnect. `VoIPDAO` would need to own that specifically. Worth naming as a real open item rather than assuming it falls out of having both access paths.

For a D-OS Mobile device specifically, this could go further than a stock phone's default behavior — real multi-radio steering (hold low-priority traffic on WiFi, reserve cellular for what actually needs it, make the handoff decision proactively rather than reactively) — same idea as the Tier 1/Tier 2 steering logic from the density-planning material earlier, just applied to WiFi-vs-cellular instead of sub-GHz-vs-CBRS.

## User

wifi should be linked to the individual/device did for individual billing and service tied to vcs as well the router is just the access, remember we are going for universal wifi and internet,

## Claude

Thought for 33s

Thought for 33s

Right — that's a real correction, not a refinement, and it changes what the router *is*. Here's the corrected model.

**Router becomes pure access infrastructure — no subscription lives on it**

The CPE stops being "the household's internet." It's a radio that authenticates whoever associates with it, per-connection, against that person's DID and VC — same mesh-wide SSID everywhere, the way eduroam works: one network name, and any device with a valid credential authenticates anywhere it sees that signal, not just at "its" router.



```
DEVICE requests association (mesh-wide SSID, everywhere)
 ▼
ROUTER relays auth request — it holds no subscriber data itself
 ▼
DID resolved → subscription VC checked (active? tier? not revoked?)
 ▼
ProvisioningDAO / Governor approves the session
 ▼
QOSDAO policy pulled dynamically for THIS session
 — bandwidth/priority follows the person's plan,
 not a static config baked into the router
 ▼
Session key issued → device online
 ▼
BillingDAO meters against the person's DID,
regardless of which router carried it
```

This is the actual mechanism that makes "universal WiFi and internet" real rather than aspirational — a person's service follows them across any CPE in the mesh, the same way their VC-based routing to security or healthcare already follows them regardless of which node picks up the request.

**One thing this genuinely adds that didn't exist before: roaming settlement**

If a router in Cluster A is now regularly serving someone whose subscription and billing live in Cluster B, that router's owner is carrying someone else's traffic. That needs the same pattern as the FCN marketplace already uses for nodes earning tokens by hosting compute — a router earns a cut when it serves a non-local subscriber, settled through the token layer. Without this, universal access quietly becomes "everyone free-rides on whoever built the densest coverage," which undermines the whole cooperative-ownership premise.

**One real open design question, worth pinning down rather than assuming:** does a person's phone and laptop share one identity for billing purposes, or does each physical device get its own device-DID subordinate to the person's DID? The BEC pattern already gives you the template — a device can hold its own DID for attestation while still acting on behalf of a person/site's sub-DAO membership. Same shape here: probably each device gets its own DID for session attestation, authorization derived from that device-DID's link to the person-DID that actually holds the subscription VC.

**Worth carrying over from the identity-routing work earlier:** authentication at association should use selective disclosure — the router needs proof of "valid subscriber, tier X," not the person's full DID and history on every connect. Same principle as the routing-key rotation in the DID-to-DID messaging spec — the access layer shouldn't become a system-wide log of exactly which person was standing near which router at what time, unless that's a tradeoff made deliberately, not by default.

Want this folded into DC-MESHISP-ARCH-001 as a proper revision — §9 rewritten around identity-bound universal access instead of device-class provisioning?

## User

but there is still vlans that users can access and configure from their own router, but the universal wifi is always up for guests and other mesh members, each physical device gets its own did but it can be linked to a persons individiual did yes fold it in

## Claude

Viewed 2 files, edited 2 files

Viewed 2 files, edited 2 files

Folded in. §9 is fully rewritten around the corrected model, and two new open items are added to §11 that this change actually surfaces — they weren't there before, not padding.

The load-bearing sentence in the new version: **the router holds no subscriber data on the universal layer.** Everything — billing, plan, priority — resolves off the device-DID → person-DID → subscription VC chain at the moment of association, not off which physical box someone happened to connect to. That's what makes "universal WiFi" actually universal instead of just "every router has its own guest network."

Two things worth flagging now rather than later:

**QoS separation** — without an explicit budget split, a busy universal layer will eat into the owner's own private VLAN performance on the same radio. Worth deciding whether that's a hard partition or a priority weighting.

**Non-D-OS device enrollment** — stock phones get a device-DID through some companion step, since there's no OS-level DID stack to generate one natively. That step isn't designed yet, and it's the actual on-ramp for most real-world subscribers on day one.

