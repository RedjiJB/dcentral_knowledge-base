# DC-TAXONOMY-007: Manufacturing, Technician, Healthcare & Security Verticals + Sovereign Cellular Base Station Spec
### Extends DC-TAXONOMY-001–006

---

## 1. New verticals

### 1.1 MeshMake (3D printing / on-demand manufacturing — Shapeways/Xometry-equivalent)

| Primitive | D-Central equivalent | Built from |
|---|---|---|
| Design upload / model marketplace | `mesh-storage`-hosted design files; public catalog or VC-gated private catalog (same pattern as MeshShop wholesale) for proprietary/commissioned designs | `mesh-storage` + `dc-identity` (private catalog gate) |
| Printer capacity discovery | A household/business SHI node with a 3D printer registers as `mesh-compute`-adjacent "physical fabrication capacity" in `dc-registry`'s capability-index — printer specs (bed size, material, resolution) become searchable fields | `dc-registry` capability-index |
| Job dispatch & completion proof | Print job assigned to nearest/cheapest matching printer node; completion attested with a photo/weight/dimension check against the design spec | `dc-attestation` |
| Quality dispute | Same `dc-governance` dispute-jury pattern as any marketplace good | `dc-governance` |
| IP/licensing on designs | Design files can carry a usage-VC (single-print license vs. unlimited vs. commercial-use), checked before the job dispatches | `dc-identity` selective disclosure + `dc-attestation` |
| Material supply chain | Filament/resin vendors list on MeshShop; a print-job proposal can auto-source material from a nearby MeshShop vendor rather than assuming the printer operator stocks everything | MeshShop cross-vertical composition |

Genuinely new physical-capacity type for `dc-registry` (fabrication, not just compute/storage/bandwidth) — worth flagging since it's the first vertical in the whole taxonomy where the "spare capacity" being rented is a *physical machine's output*, not compute cycles or bandwidth.

### 1.2 MeshTech (technician services — IT support, appliance repair, electronics repair; distinct from MeshBuild's licensed-trade/contracting scope)

MeshBuild (licensed contracting: plumbers/electricians/HVAC) already exists for regulated trades. MeshTech covers the *unlicensed* or lighter-credential technical service space — laptop repair, TV mounting, smart-home setup, appliance troubleshooting — which is closer to Lakou Marketplace's gig-task shape than MeshBuild's multi-milestone/permit shape, but deserves its own catalog since "technician" skills are verifiable in a specific way (certifications, not government licenses).

| Primitive | D-Central equivalent | Built from |
|---|---|---|
| Technician directory | DID + skill-certification VCs (CompTIA-equivalent, manufacturer-issued repair certs) | `dc-identity` |
| House-call or drop-off repair | Lakou Marketplace listing, single-milestone escrow (simpler than MeshBuild's staged release) | `dc-credit` escrow-engine |
| Remote diagnosis (a lot of IT support doesn't require an in-person visit) | A session over MeshTalk/MeshDM with screen-share, billed per-session via `dc-credit` micropayment | MeshTalk/MeshDM + `dc-credit` |
| Parts sourcing | Same MeshShop cross-composition as MeshMake — technician can source a replacement part from a nearby vendor as part of the job | MeshShop |
| Warranty/comeback tracking | A repair attestation with an implicit warranty window; if the same fault recurs within window, it references the original attestation automatically rather than starting a fresh dispute from zero | `dc-attestation` |

### 1.3 MeshHealth (healthcare — telemedicine, home health aide, pharmacy delivery; deliberately conservative scope given the privacy stakes)

This is the vertical that most needs the selective-disclosure/attestation discipline already built into the architecture, since health data is the most sensitive category anywhere in the system.

| Primitive | D-Central equivalent | Built from |
|---|---|---|
| Provider directory | DID + medical-license-VC (issued by the actual licensing college/board — same issuer-of-record pattern as MeshBuild's municipal permits) | `dc-identity` |
| Telemedicine visit | MeshTalk/MeshDM video session, billed via `dc-credit`; visit-occurred attestation issued for insurance/billing purposes *without* the attestation itself carrying clinical content | `dc-attestation` (metadata-only: "a visit occurred, was billed X, provider was Y" — not "diagnosis was Z") |
| Prescription | Provider issues a prescription-VC directly to the patient's DID; a pharmacy (MeshShop-adjacent, pharmacy-licensed vendor) verifies it before dispensing, and dispensing is itself attested for the patient's own record, again without broadcasting clinical detail | `dc-identity` + `dc-attestation` |
| Home health aide / caregiver | Lakou Marketplace-adjacent listing, but background-check-VC and health-specific certification are mandatory gates before a listing can even be accepted | `dc-identity` + `dc-governance` (stricter acceptance rule than a standard gig listing) |
| Medical records | Held at the patient's own SHI node / Wealthfolio-style local dashboard equivalent for health data — a **MeshHealth local record store**, mirroring exactly the sovereignty argument already made for MeshBank: your health history lives on your own node, and only selective-disclosure proofs (not raw records) ever leave it | Same local-first pattern as MeshBank's Wealthfolio-based dashboard, applied to health data |
| classIQ tie-in | Clinical decision support already named in DC-TAXONOMY-001 §4.8 — classIQ runs against attested-but-not-raw patient data via the same ZK/selective-disclosure pattern | `mesh-ai` + `dc-attestation` |
| Emergency/911 integration | A verified emergency attestation (e.g., from a wearable `mesh-sensors` fall-detection device) can trigger a MeshAssist-style dispatch to the nearest available responder, bypassing normal marketplace matching for true emergencies | `mesh-sensors` + priority dispatch mode |

**Note on regulatory reality:** unlike most other verticals in this taxonomy, MeshHealth cannot be "just architecture" — actual clinical practice is licensed and regulated per-jurisdiction regardless of what infrastructure carries it. The D-Central role here is narrower and more honest than for, say, MeshShop: it's the sovereign data/attestation/payment substrate underneath licensed providers who remain fully accountable to their existing regulatory bodies, not a replacement for licensure or clinical oversight.

### 1.4 MeshGuard (security services — private security patrol, guard dispatch, monitoring; distinct from OpenSecure's sensor/detection infrastructure)

OpenSecure (OS-PACS/GUARDIAN/SENTINEL/PATROL) already covers the *sensor and detection* side of security. MeshGuard is the *human labor* marketplace side — this maps directly onto your own professional background (hotel/casino/contract security operations), so it's worth being precise about the split:

| Primitive | D-Central equivalent | Built from |
|---|---|---|
| Guard/patrol directory | DID + security-license-VC (provincial/state security guard licensing, same issuer-of-record pattern as MeshBuild/MeshHealth) | `dc-identity` |
| Shift booking (a business needs coverage) | Lakou Marketplace listing, scheduled/recurring shift type rather than one-off task | `dc-credit` escrow, recurring |
| Patrol verification (proof the guard actually walked the route, on schedule) | Mobile-node or handheld-device telemetry generates a patrol-completion attestation — this is literally the enterprise systems you already work with (Avigilon/HID/checkpoint-tour systems) re-expressed as `mesh-sensors` + `dc-attestation` instead of a proprietary vendor system | `mesh-sensors` + `dc-attestation` |
| Incident reporting | An incident report becomes an attestation with attached sensor/camera evidence references (via OpenSecure's Frigate-NVR-style pipeline), creating a chain-of-custody record from the moment of detection | `dc-attestation` + OpenSecure integration |
| Access control credentialing (who's allowed where) | This is exactly `dc-identity`'s selective-disclosure pattern applied to physical access — a guest's DID presents an access-VC at a door, same mechanism as VingCard/HID today, just DID-native instead of proprietary-card-native | `dc-identity` (this is a strong, very direct professional-background tie-in worth building first) |
| Facial recognition / SAFR-equivalent | If pursued at all, this is the one place in the entire taxonomy that needs its own explicit privacy/consent framework beyond the standard selective-disclosure pattern, since biometric matching against a watchlist is categorically more sensitive than a credential check — flag as needing dedicated governance review, not a default feature | `mesh-ai` (if pursued) + mandatory `dc-governance` policy layer |

---

## 2. Sovereign open-source cellular base station — technical requirements

### 2.1 What "sovereign cellular" actually means here

Two separable capabilities, often conflated:
1. **Running your own radio access network (RAN)** — the actual cell tower hardware/software that phones connect to
2. **Running your own core network** — subscriber authentication, call/data routing, billing — independent of a carrier's HSS/HLR and core

D-Central sovereignty requires both, but they have very different hardware/spectrum requirements, so the spec splits along that line.

### 2.2 Minimum viable open-source stack

| Layer | Component | Open-source project |
|---|---|---|
| Core network (4G/LTE) | EPC (Evolved Packet Core) | **Open5GS** or **NextEPC** |
| Core network (5G) | 5GC | **Open5GS** (dual 4G/5G support), **free5GC** |
| RAN software (eNodeB/gNodeB) | Baseband processing | **srsRAN** (srsENB/srsGNB) — the most mature, actively maintained option; **OpenAirInterface (OAI)** as the second reference |
| Legacy/2G-3G fallback (useful for older devices, emergency-only redundancy) | GSM stack | **OsmocomBB / Osmocom-based OpenBTS successor** — worth including narrowly for basic-phone/SMS fallback, not as a primary layer |
| Radio hardware (SDR) | Software-defined radio front end | **USRP (Ettus Research) B-series/X-series**, or **LimeSDR** as the lower-cost open-hardware alternative |
| Subscriber identity | SIM provisioning / HSS | Open5GS's own subscriber database, but the subscriber *identity* itself should be `dc-identity`-issued — a SIM-equivalent credential (this is where MeshLine's DID-linked phone handle from DC-TAXONOMY-003 becomes directly relevant: the cellular core's subscriber record and the DID are the same identity, not two parallel systems) |

### 2.3 The spectrum problem — the actual hard constraint, not the software

This is the part that isn't solvable by picking better open-source software: **operating a cellular base station requires licensed spectrum in almost every jurisdiction**, unlike WiFi mesh (`mesh-connectivity`'s existing unlicensed-band approach). Three realistic paths:

1. **CBRS (Citizens Broadband Radio Service, US-specific, 3.5GHz band)** — the one meaningfully "sovereign-friendly" licensed-spectrum option in North America: a tiered access system where a campus/enterprise can register as a General Authorized Access (GAA) user without an auction, coordinated automatically by a Spectrum Access System (SAS). This is almost certainly the right path for a campus deployment specifically, since CBRS was designed for exactly this use case (enterprise/campus private LTE/5G).
2. **Unlicensed/lightly-licensed bands where available** (e.g., some countries have license-exempt LTE bands, or a private-network licensing regime distinct from full carrier spectrum auctions) — jurisdiction-dependent, would need a specific check for wherever a campus deployment actually sits (Canada's own private-network licensing framework differs from CBRS and would need separate research).
3. **MVNO/spectrum-sharing agreement with an actual carrier** — not sovereign in the full sense, but a fallback if licensed spectrum isn't obtainable; the core network and subscriber sovereignty (DID-based identity, D-Central-controlled billing/auth) can still be sovereign even if the radio spectrum itself is leased.

**Recommendation for the campus case specifically: build for CBRS from the start** (in jurisdictions where it applies) since it's the only path that gets you both real cellular coverage *and* genuine spectrum sovereignty without a carrier relationship — and CBRS-capable hardware (USRP/LimeSDR-based eNodeB) is already common in campus private-network deployments elsewhere, so this isn't a novel approach, just one worth deliberately adopting rather than discovering later that spectrum, not software, was the actual blocker.

### 2.4 Campus-scale deployment architecture

Mapping onto your existing Civic Spine/NOC/campus design:

```
                    ┌─────────────────────────┐
                    │   Campus NOC / Civic     │
                    │   Spine (core network:   │
                    │   Open5GS EPC/5GC +      │
                    │   dc-identity subscriber │
                    │   registry)              │
                    └───────────┬─────────────┘
                                │ fiber/backhaul
              ┌─────────────────┼─────────────────┐
              │                 │                 │
     ┌────────▼──────┐ ┌────────▼──────┐ ┌────────▼──────┐
     │ Gateway node    │ │ Gateway node   │ │ Gateway node   │
     │ + small-cell     │ │ + small-cell    │ │ + small-cell    │
     │ eNodeB/gNodeB    │ │ eNodeB/gNodeB   │ │ eNodeB/gNodeB   │
     │ (srsRAN + USRP/  │ │ (srsRAN + USRP/ │ │ (srsRAN + USRP/ │
     │ LimeSDR, CBRS)   │ │ LimeSDR, CBRS)  │ │ LimeSDR, CBRS)  │
     └─────────────────┘ └─────────────────┘ └─────────────────┘
        District A            District B           District C
```

Multiple small-cell radios per district (rather than one large tower) matches both the existing multi-district Civic Spine design and CBRS's actual RF profile (CBRS is a mid-band, moderate-range spectrum — small-cell/distributed-antenna deployment is the normal pattern, not a compromise).

### 2.5 Backhaul redundancy — multi-path by design, not an afterthought

This is where the architecture should explicitly borrow the same tiered-failover thinking already present in the SHI node's own design (household resilience) and scale it to the NOC level:

| Backhaul path | Role | Failover priority |
|---|---|---|
| **Primary: fiber/wired internet** | Normal operations — highest bandwidth, lowest latency, cheapest per-byte | 1st (default) |
| **Secondary: terrestrial cellular backhaul** (an MVNO data SIM in the NOC/gateway equipment, riding on an existing commercial carrier) | Automatic failover if fiber drops — carrier redundancy without depending on the carrier for the campus's own RAN | 2nd |
| **Tertiary: satellite backhaul** (Starlink or equivalent LEO service, since this is what's actually deployable today at reasonable cost/latency vs. legacy GEO satellite) | True redundancy path — survives a scenario where *both* fiber and local cellular infrastructure are down (natural disaster, regional outage), which matters enormously for the Haiti-context resilience goals already central to the ecosystem's design philosophy | 3rd, always-available emergency path |
| **Mesh-local fallback (no backhaul at all)** | Even with zero backhaul, the mesh's own DTN/store-and-forward pattern (already core to the architecture) keeps local services running — local MeshTalk, MeshShop browsing, MeshBank balance checks, and even local emergency dispatch continue to function node-to-node, syncing to the wider network whenever *any* backhaul path returns | Always active, not a "failover" so much as a baseline the network never loses |

**Automatic failover mechanism:** the gateway node's own routing logic should treat backhaul paths the same way `mesh-connectivity` already treats mesh routing — a health-check/heartbeat pattern (reusing `dc-registry`'s existing heartbeat-monitor microservice) triggers automatic path switching without manual intervention, prioritized fiber > cellular > satellite > mesh-local-only.

**Cost note worth naming plainly:** satellite backhaul (Starlink-class) has real recurring cost and should be scoped as *emergency/redundancy capacity*, not primary bandwidth — the campus financial model (same discipline as the existing 10/20/50/100-node cost modeling) should treat it as an insurance line item, sized for "keep critical services alive during an outage," not "carry normal daily traffic."

---

## 3. Updated gap registry addition

32. **DC-MESHMAKE-001** — 3D printing/manufacturing vertical; first vertical requiring a new `dc-registry` capacity type (physical fabrication)
33. **DC-MESHTECH-001** — unlicensed technician services, sibling to MeshBuild but lighter-weight (single-milestone escrow, certification-VC not government-license-VC)
34. **DC-MESHHEALTH-001** — healthcare vertical; explicitly scoped as sovereign data/attestation/payment substrate under existing clinical licensure, not a replacement for it; needs its own privacy review given HIPAA-equivalent stakes
35. **DC-MESHGUARD-001** — security-labor marketplace, sibling to OpenSecure's sensor/detection layer; access-control credentialing (DID-native badge/card replacement) is the most directly buildable piece given existing professional-background alignment; facial-recognition/biometric matching explicitly flagged as needing its own governance review before being treated as a default feature
36. **DC-CELLULAR-BASESTATION-001** — the sovereign cellular spec from §2: Open5GS/srsRAN/USRP-LimeSDR stack, CBRS as the recommended spectrum path for campus deployments, DID-linked subscriber identity replacing a traditional SIM/HSS relationship
37. **DC-BACKHAUL-REDUNDANCY-001** — the tiered fiber→cellular→satellite→mesh-local failover spec from §2.5, including the cost-scoping note that satellite is redundancy capacity, not primary bandwidth

---

*DC-TAXONOMY-007 — extends 001–006. Adds MeshMake (3D printing/manufacturing, the first vertical needing a new physical-fabrication dc-registry capacity type), MeshTech (unlicensed technician services, sibling to MeshBuild), MeshHealth (healthcare, scoped explicitly as sovereign substrate under existing clinical licensure with its own privacy discipline), and MeshGuard (security-labor marketplace, sibling to OpenSecure, with access-control credentialing as the most directly buildable piece given existing professional background). Specifies a sovereign open-source cellular base station stack (Open5GS + srsRAN + USRP/LimeSDR, CBRS as the recommended campus-scale spectrum path, DID-linked subscriber identity) and a tiered backhaul redundancy architecture (fiber primary, cellular secondary, satellite tertiary/emergency, mesh-local always-active baseline) with automatic heartbeat-driven failover.*
