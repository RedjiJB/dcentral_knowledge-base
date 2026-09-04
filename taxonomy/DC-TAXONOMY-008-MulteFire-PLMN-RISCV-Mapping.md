# DC-TAXONOMY-008: Mapping MulteFire/PLMN/RISC-V Research onto DC-CELLULAR-BASESTATION-001
### Revises DC-TAXONOMY-007 §2 based on new regulatory/hardware research

---

## 1. The headline revision: CBRS was the wrong default recommendation for a mesh with mobile nodes

DC-TAXONOMY-007 §2.3 recommended CBRS as the primary spectrum path for campus deployment. That needs correcting given what this research surfaces: **CBRS's SAS requires fixed, verified GPS coordinates, and any location drift — including a CBRS radio mounted on a vehicle — triggers an automatic authorization cutoff.** That's a direct architectural conflict, because a huge share of D-Central's own mesh hardware is explicitly mobile: MeshEats/MeshRide/MeshCar/MeshCarDelivery/MeshAssist/TrafficMesh all put mobile nodes in vehicles, and DC-CELLULAR-BASESTATION-001 needs to serve those nodes too, not just fixed household/campus infrastructure.

**Revised recommendation: MulteFire on unlicensed 5 GHz (or 6 GHz NR-U) as the primary sovereign cellular layer, with CBRS reserved only for fixed-position, high-power campus macro coverage where mobility isn't a factor.**

| | CBRS (3.5 GHz, Band 48) | MulteFire (5 GHz unlicensed) |
|---|---|---|
| Registration | Mandatory SAS registration, per-CBSD | **None required** — self-assigned private PLMN, no database |
| Mobile nodes | **Illegal** — GPS drift breaks SAS heartbeat, transmission killed | **Fully legal** — Part 15 rules don't care if the transmitter is moving |
| Recurring cost | SAS subscription fee per base station | None |
| Range/power | Higher (mid-band, more penetration) | Lower (higher frequency, more attenuation) — needs more, smaller cells |
| Fits D-Central's mesh model | Fixed gateway/tower nodes only | **Fits the whole node hierarchy** — SHI nodes, gateway nodes, and mobile nodes all use the same unlicensed-band approach `mesh-connectivity` already uses for WiFi mesh |
| International reach | US-only | 5 GHz UNII rules are shared across US/Canada/Mexico (with LBT compliance needed for EU/Japan/India equivalents) |

This isn't just "cheaper," it's **the actually-consistent choice** — MulteFire uses the *same* unlicensed-spectrum philosophy `mesh-connectivity` already runs on for WiFi mesh, so the cellular layer stops being a separate regulatory regime bolted onto the network and becomes the same sovereignty model applied to a different radio technology.

## 2. The private PLMN is D-Central's cellular-layer identity, and it should be DID-issued

The research confirms MCC 999 is the ITU-T-reserved code for exactly this use case (private, non-routable, non-coordinated networks) — pair it with a self-chosen MNC (e.g., **999-DC** conceptually, actual digits assigned by `dc-registry`) and every D-Central cellular deployment worldwide can share the same private PLMN identity space without coordinating with any external body.

This maps directly onto existing primitives:

| Cellular concept | D-Central primitive |
|---|---|
| PLMN ID (999-XX) | The cellular-layer equivalent of `dc-social-protocol`'s federation namespace — one shared private network identity across every D-Central cellular deployment, campus or household |
| Subscriber record (traditionally HSS) | `dc-identity` — a subscriber isn't a SIM record in a carrier database, it's a DID with a cellular-subscriber-class VC |
| eSIM provisioning (SM-DP+ server) | **A new `dc-identity` microservice**: `esim-provisioner` — issues the cellular profile the same way `vc-issuer` issues any other credential, over-the-air, QR/MDM-pushed. This is the same MeshLine concept from DC-TAXONOMY-003 (DID-linked phone handle) made concrete: the eSIM profile *is* a VC, provisioned through the identity layer that already exists rather than a bespoke telecom-specific system |
| Tracking Area / MME handover state | `mesh-connectivity`'s existing gateway/node hierarchy already tracks node proximity via `dc-registry`'s capability-index; X2-style handover between D-Central cellular nodes is a natural extension of that, not a new discovery mechanism |
| Dual-SIM (public carrier + private network) | Directly enables the backhaul-redundancy design from 007 §2.5 — a device or gateway node can hold a commercial-carrier eSIM *and* the D-Central private-network eSIM simultaneously, exactly matching the "terrestrial cellular backhaul secondary path" tier already specified |

## 3. Wi-Fi-side roaming (802.11k/r/v) closes the gap the earlier docs left implicit

DC-TAXONOMY-007 didn't specify how WiFi-side mesh roaming actually works at the protocol level — this research fills that in cleanly, and it's a direct fit for `mesh-connectivity`'s existing single-SSID-equivalent mesh behavior:

- **802.11k** — neighbor-list awareness (an AP tells a client which nearby APs exist) → this is functionally what `dc-registry`'s capability-index already provides at the network-discovery layer; the WiFi radio layer needs its own local implementation of the same idea
- **802.11v** — network-directed steering (network nudges a client toward a better AP) → maps onto `mesh-connectivity`'s existing load/coverage optimization goals
- **802.11r** — fast cryptographic handover (<50ms) by caching keys across the mesh → this is the WiFi-layer analog of what MulteFire's X2/GTP-U handover does at the cellular layer; **both roaming layers should derive their session keys from the same underlying DID-linked credential**, so a device roaming between a MulteFire cell and a WiFi mesh AP isn't running two separate authentication systems, just two radio-layer expressions of one `dc-identity`-issued credential

## 4. Unified dual-radio architecture (revises the 007 §2.4 diagram)

```
                    ┌───────────────────────────────────────┐
                    │  dc-identity: esim-provisioner +       │
                    │  subscriber-VC issuance (one DID,      │
                    │  one credential, both radio layers)    │
                    └───────────────┬─────────────────────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                                            │
   ┌──────────▼──────────┐                     ┌───────────▼──────────┐
   │  Cellular layer       │                     │  Wi-Fi mesh layer     │
   │  MulteFire, 5GHz       │                     │  802.11k/r/v, single  │
   │  unlicensed, PLMN       │                     │  SSID roaming across   │
   │  999-XX, Open5GS EPC   │                     │  all nodes             │
   │  (self-hosted, no SAS) │                     │  (mesh-connectivity)   │
   └──────────┬──────────┘                     └───────────┬──────────┘
              │                                            │
              └─────────────────────┬────────────────────┘
                                    │
                    ┌───────────────▼─────────────────────┐
                    │  Gateway node (backhaul selection:   │
                    │  fiber > cellular-MVNO > satellite > │
                    │  mesh-local, per DC-TAXONOMY-007 §2.5)│
                    └───────────────────────────────────────┘
```

Fixed-position campus macro-coverage (e.g., a stadium, a large open quad) is the one case where CBRS's higher power/range genuinely earns its complexity — worth keeping as an optional third layer for specific fixed sites within a campus deployment, registered through the SAS/CPI process precisely because those sites don't need mobility, not as the network's default.

## 5. RISC-V — where it fits and where it genuinely doesn't (revises nothing in 007, adds detail)

This research sharpens something 007 didn't get into: RISC-V is a legitimate sovereignty target for parts of the stack, not all of it.

| Layer | RISC-V viable? | Why |
|---|---|---|
| Host OS / EPC (Open5GS) / control-plane RAN logic (RRC, upper MAC) | **Yes** | Scalar compute, no SIMD/FFT bottleneck — a RISC-V SBC can run Open5GS and the non-PHY RAN stack fine |
| PHY layer (FFT, Turbo/LDPC decode) | **Not yet practically** | Needs mature vector extensions (RVV 1.0 at wide VLEN) that current affordable RISC-V silicon mostly lacks; x86/ARM SIMD or an FPGA co-processor (the same LimeSDR FPGA gateware already in the stack) remains the practical choice for the actual radio math |
| `mesh-connectivity` router/gateway nodes generally (non-cellular) | **Yes, and arguably preferred** | Routing/packet-forwarding is control-plane work, exactly where RISC-V already succeeds in commercial routers (OpenWrt, FRRouting); RISC-V's Zbkb/Zvkn crypto extensions directly accelerate the WireGuard-style tunneling `mesh-vpn` (DC-TAXONOMY-005 §2) needs, in silicon, without a proprietary crypto chip |
| RF front-end / power amplifiers | **No** — this layer was never a silicon/ISA question in the first place; GaN/SAW duplexer fabrication is a materials-and-fab problem, not something RISC-V vs. ARM vs. x86 touches at all |

**Net for D-Central's node hardware roadmap:** RISC-V is a strong candidate for the *general SHI node compute tier* (routing, `mesh-vpn` crypto acceleration, Open5GS hosting, control-plane RAN) — i.e., most of what an SHI node already does — while the actual radio PHY continues to depend on the LimeSDR-class open-hardware SDR board regardless of what CPU architecture drives it. This is worth folding into the SHI node hardware spec as an explicit "control plane can be RISC-V; PHY stays SDR+FPGA" note rather than treating CPU architecture as a single ecosystem-wide choice.

## 6. Cost reality, mapped onto the D-Central financial model

The research's hardware pricing tiers give real numbers to plug into the existing 10/20/50/100-node SHI financial model:

| Tier | Hardware | Fits |
|---|---|---|
| Entry (lab/testing only) | ADALM-PLUTO (~$225–300) | Not viable for a real deployment — 1×1 SISO only, listed here only because the financial model should explicitly exclude it rather than someone mistakenly budgeting for it |
| Mid-range (real small-cell deployment) | Nuand bladeRF 2.0 Micro (~$1,675 CAD) | The realistic per-node cost for a district-level MulteFire small cell in the campus diagram (007 §2.4) |
| Enterprise (carrier-grade, if a fixed CBRS macro site is pursued per §4) | Ettus USRP B210 (~$3,340–4,000 CAD) | Reserved for the optional fixed-CBRS-macro-site case only, not the default mesh deployment |
| Hidden costs (both tiers) | GPSDO ($100–300), duplexers/filters ($50–150/band), antennas ($30–80) | Needs its own line item in the campus cost model — worth naming explicitly since these are easy to underbudget |

This meaningfully lowers the campus deployment's cellular-layer cost relative to what 007 implied by defaulting to CBRS (which also carries an ongoing SAS subscription fee 007 didn't price in) — the mid-range bladeRF tier plus a RISC-V or modest x86 host is the realistic per-district cost for the default MulteFire deployment.

---

## 7. Updated gap registry addition

38. **DC-CELLULAR-BASESTATION-001 revision** — supersede the CBRS-primary recommendation from 007 §2.3 with: MulteFire (5 GHz unlicensed) as the default sovereign cellular layer for all mobile and fixed nodes; CBRS retained only as an optional fixed-macro-site supplement
39. **DC-PLMN-IDENTITY-001** — the private PLMN (999-XX) as D-Central's shared cellular namespace, and the `esim-provisioner` microservice added to `dc-identity` (§2)
40. **DC-DUAL-RADIO-ROAMING-001** — unified MulteFire + 802.11k/r/v architecture where both radio layers derive session credentials from the same DID (§3–4)
41. **DC-NODE-RISCV-SCOPE-001** — explicit hardware-architecture guidance for the SHI node roadmap: RISC-V for control-plane/routing/crypto-acceleration/EPC hosting, x86/ARM/FPGA retained for PHY-layer radio processing (§5)

---

*DC-TAXONOMY-008 — revises DC-TAXONOMY-007 §2 based on new MulteFire/CBRS/RISC-V research. Corrects the earlier CBRS-primary recommendation (CBRS's SAS mandates fixed GPS, which is incompatible with D-Central's own mobile-node verticals) to MulteFire on unlicensed 5 GHz as the default sovereign cellular layer, with CBRS retained only for optional fixed-macro campus sites. Establishes the private PLMN (MCC 999 + self-assigned MNC) as D-Central's shared cellular identity namespace, adds an esim-provisioner microservice to dc-identity, unifies cellular (MulteFire) and Wi-Fi (802.11k/r/v) roaming under one DID-derived credential, and scopes RISC-V's real applicability (control-plane/routing/crypto yes, radio PHY no) for the SHI node hardware roadmap.*
