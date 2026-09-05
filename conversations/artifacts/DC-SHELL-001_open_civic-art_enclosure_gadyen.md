---
source_conversation_uuid: df8f544e-9dca-422f-8bcf-e82e7df6e3b1
conversation_title: 'Modern police'
created_at: 2026-06-20T18:21:12.421156Z
doc_id: DC-SHELL-001
description: 'Open civic-art enclosure layer spec: a sensor-transparent artistic shell system separating functional substrate from artistic skin, with compliance constraints, form/material tiers including Haitian craft traditions, an open licensed design library, a decentralized artisan/designer DID/VC network paralleling the technician network, the beautify-not-conceal constitutional rule, operational benefits, funding, and network effects'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-SHELL-001 — Open Civic-Art Enclosure Layer ("Gadyen")
### Making the infrastructure beautiful, dignified, and community-owned — without making it secret
**Status:** v0.1 · applies to **all visible nodes** (AGD, SHI-exterior, smart poles, gateways) · shares the DID/VC fabric, storage, and governance of DC-AGD-002
**Codename suggestion:** *Gadyen* (Haitian Creole, "guardian/keeper"). Gargoyles were architectural guardians; this reframes a sensor from *thing watching you* to *guardian watching over the community*. Rename freely.

---

## 0. Why this is a real layer, not decoration
The through-line tension of this whole program is: pervasive sensing can feel like occupation. Governance and the privacy floor address the *rights* dimension; this layer addresses the *lived, felt, aesthetic* dimension — infrastructure that **honors a place instead of occupying it.**

**The honest caveat up front:** beauty without accountability is **artwashing** — making surveillance palatable while changing nothing real. This layer is only legitimate *because* the rest of the stack is real: open code, public verifiability, privacy floor, community ownership. **Pretty + accountable = humane design. Pretty + opaque = propaganda.** Keep them together.

---

## 1. The key architectural idea: separate the *substrate* from the *skin*

Define a **standard sensor-transparent interface** — a functional core (the DC-AGD/SHI node + its mount) that any artistic outer form attaches to. Like a phone-case ecosystem, but for civic sensors:

- **Functional substrate** (engineered, CERN-OHL-W): the node, sensors, mounts, acoustic ports, antenna, solar, service hatch. Fixed, certified.
- **Artistic skin** (open, CC-BY-SA): the gargoyle / statue / ironwork / sculptural form that clads it — designed by *anyone*, to the interface spec, without touching the sensor engineering.

This separation is what makes a **decentralized design network possible**: artists design skins against a published spec; the spec guarantees the art can't break the sensing.

---

## 2. The compliance spec — what the art must NOT break

A beautiful shell that muffles the microphone is worse than useless. Every skin must pass **sensor-transparency validation**:

| Constraint | Requirement |
|---|---|
| **Acoustic transparency** | open, unobstructed acoustic paths to mics (critical for gunshot detection); no resonant cavities, no muffling; PTFE-vented apertures aligned to mic ports |
| **Sensor FOV** | unobstructed field of view for cameras, lidar (DCOL), radar, mocap |
| **RF / GPS line-of-sight** | no metal shrouding over GPS/comms antennas (so artisan **metal** forms need dielectric windows there) |
| **Solar exposure** | panel aperture unshaded |
| **Thermal venting** | airflow/heat dissipation for compute preserved |
| **Serviceability** | tool access to the service hatch without destroying the art |
| **Weather + tamper** | maintains IP65+; tamper-evidence preserved |
| **Mount compatibility** | attaches to the standard bracket |

Validation is **attested on-chain** (§4) — a skin isn't "compliant" until tested and signed off, so aesthetics can never silently degrade function.

---

## 3. Form & material tiers (with cost adders per node)

| Tier | Form | Material / craft | **Adder/node** |
|---|---|---|---|
| **T0** | plain functional enclosure | ASA (DC-AGD-001) | $0 |
| **T1** | printed artistic skin | 3D-printed ASA decorative shell | **+$10–40** |
| **T2** | cast sculptural | resin / concrete / ceramic cast from open molds (e.g., gargoyle) | **+$50–300** |
| **T3** | bespoke artisan | hand-made sculpture / **Haitian fer découpé ironwork** | **+$200–2,000+** |

**Haiti's edge:** Croix-des-Bouquets is a world-famous metal-art cluster — artisans *already* hand-cut decorative steel sculpture from recycled oil drums. That existing craft economy can fabricate culturally-rooted sensor guardians, with dielectric windows over antennas. The infrastructure becomes a showcase of Haitian art, made by Haitian hands.

---

## 4. The decentralized artisan/designer network (parallels the technicians)

Same DID/VC pattern as the technician/manufacturer fabric (DC-AGD-002 §A.5):

- **Designer DID** — every contributor identified.
- **Design-Compliance VC** — "this skin passed sensor-transparency validation (acoustic/FOV/RF/solar/thermal/service)"; carries its license + the substrate spec version it fits.
- **Fabricator VC** — certified to fabricate/weatherproof/install a given design to spec.
- **Attribution + remix lineage** — every design records its author and what it forked from; credit is cryptographic and permanent (open-source *with* provenance).
- **Cooperative remuneration** — designs are open (CC-BY-SA), but adoption can route recognition/royalty/patronage to authors via Lakou/D-Credit. An **attribution economy**: artists are credited and can be paid when their design is deployed, without enclosing the commons.

The result mirrors the technician corps: a **credentialed, reputation-bearing, cooperatively-rewarded network of artists and makers**, governed under the same three-DAO structure (the Hardware DAO owns the substrate spec; a new **Civic-Art guild** under the Public/Civic DAO curates the skin library and standards).

---

## 5. The beautify-≠-conceal rule (constitutional)

Add to the DC-AGD-002 floor:
> **Every art-shelled node remains publicly registered, mapped, and verifiable, with its sensing capabilities disclosed.** The skin may change the *form*; it must never change the *fact* that a sensor is there or hide it from the public registry.

The art makes the object dignified, not secret. Transparency lives at the data/governance layer (open API, on-chain, public map); the physical form is humane. This is the line between *humane design* and *covert surveillance* — stay on the right side of it, by rule.

---

## 6. Operational benefits (this earns its cost)

- **Anti-oppression / dignity.** Infrastructure that feels like it belongs to the community, not imposed on it.
- **Vandalism & theft reduction.** This is the non-obvious operational win: in HT-001/HT-002, sensor survivability (theft, destruction) was a top risk. **People protect public art they helped make; they destroy alien surveillance gear.** Community co-creation converts a target into a guarded civic asset — directly improving the survivability that the whole network depends on.
- **Local artist economy / jobs.** Diaspora + local Haitian artists earn through the cooperative — dignity and livelihood, not just sensors.
- **Cultural localization.** Each neighborhood can adopt/remix forms that reflect *its* identity — the network looks like Haiti, not like a foreign deployment.
- **Civic pride flywheel.** Beautiful, locally-made infrastructure invites ownership and participation.

---

## 7. Cost & funding (and why it can be ~net-neutral)

- A modest blended adder (say $50 avg over visible nodes) is **small against the multi-billion national total** (DC-AGD-HT-003-R1) — e.g., $50 × 500k visible nodes ≈ $25M.
- **Different funding pool.** Unlike sensors, the art layer taps **cultural/arts/placemaking/heritage/tourism funding and diaspora cultural philanthropy** — money that won't fund surveillance but *will* fund public art and artisan livelihoods.
- **Vandalism savings offset.** Reduced node loss/replacement in contested areas can offset much of the adder.
- Net: a layer that is partly self-funding through *other* purses and partly pays for itself in survivability.

---

## 8. Network effects (extends DC-AGD-002 §D)
- **Design-library flywheel** — more open designs → more remixing → more adoption → more artists. Classic content/platform effect, on a creative commons.
- **Localization & civic-pride effects** — adoption compounds as communities see their own forms in their own streets.
- **Survivability network effect** — the more community-owned the form, the lower the loss rate, the cheaper the network, the more it scales.

---

## 9. Integration
Applies to every visible node — AGD, SHI exterior housings, smart poles, gateways. Shares the DID/VC fabric, decentralized storage (designs are content-addressed + anchored like any artifact), the three-DAO governance (substrate = Hardware DAO; skin library + standards = Civic-Art guild under the Public/Civic DAO), and folds a **cost adder per node tier** into the capital model.

---

*Next steps: (a) draft the **sensor-transparent interface spec** (the published mount + aperture standard skins must satisfy); (b) the **Civic-Art guild** charter + the Design-Compliance VC schema; (c) fold the shell cost-adder tier into the interactive capital .xlsx; (d) a Croix-des-Bouquets artisan-onboarding pilot (existing craft cluster → first Gadyen forms).*
