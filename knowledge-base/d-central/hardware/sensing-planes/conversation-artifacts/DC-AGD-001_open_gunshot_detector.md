---
source_conversation_uuid: df8f544e-9dca-422f-8bcf-e82e7df6e3b1
conversation_title: 'Modern police'
created_at: 2026-06-20T18:21:12.421156Z
doc_id: DC-AGD-001
description: 'Full open-source/open-hardware acoustic gunshot detector reference design with decentralized storage, blockchain anchoring, zero-trust, DID/VC provenance, and public access layer'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-AGD-001 — Open Acoustic Gunshot Detector
### Reference Design: Open-Source / Open-Hardware Node + Decentralized, Publicly-Verifiable Network
**Node codename suggestion:** *Tonnè* (Haitian Creole, "thunder") — fits the impulse-detection function and the Lakou/diaspora naming line. Rename freely.

**Status:** v0.1 design spec · execution 0% · not yet built
**Licenses (proposed):** Hardware — CERN-OHL-W-2.0 · Firmware — Apache-2.0 (or GPLv3) · Models & datasets — CC-BY-SA / open
**Positioning:** The publicly-auditable counter to proprietary black-box systems (ShotSpotter/SoundThinking). Every detection is independently verifiable by anyone, without trusting the operator.

---

## 0. Prior art we build on (don't reinvent)

| Project | What to take from it |
|---|---|
| **SO+ER** (`innesian/soter`) | Closest open-hardware precedent — community-driven gunshot network with open enclosure + PCB + firmware. Study its mistakes/limits; it's centralized-cloud for analysis. |
| **sbts-aru** (`hcfman/sbts-aru`) | Raspberry Pi TDOA localization with **GPS-PPS sub-microsecond time sync**; u-blox NEO-6/7/8M. This is our timing + multilateration backbone. |
| **gabemagee/gunshot_detection** (IEEE 2019) | 1D-CNN (raw audio) + 2D-CNN (spectrogram) **majority-vote ensemble**, ~99% on their set, ~60k samples. Our edge-classifier baseline. |
| **VERA** (`JunweiLiang/VERA_Shooter_Localization`) | Gun-type classification + audio sync ideas. |
| **Phoenix PD CIC** | Open algorithm but AWS-locked → exactly the centralization we replace. |

**Our delta:** device/manufacturer/technician identity via W3C DID+VC, content-addressed decentralized storage, on-chain integrity anchoring, zero-trust verification, cooperative manufacturing, and an open public API. Nobody has assembled this combination.

---

## 1. Acoustic physics (what we actually detect)

A gunshot from a firearm emits up to two distinct acoustic events:

1. **Muzzle blast** — explosive release of propellant gas. Broadband impulse, ~140–170 dB SPL at source, energy concentrated low/mid-band, radiates roughly omnidirectionally. **This is the primary signal for shooter location** (it originates *at the gun*).
2. **Ballistic shockwave ("crack")** — only for supersonic rounds. An *N-wave* (~200–300 µs) generated along the bullet's path; very high-frequency content. It points to the **trajectory**, not the shooter.

**Localization principles:**
- **Network multilateration (TDOA):** Many synchronized nodes hear the muzzle blast at slightly different times → hyperbolic position solve. Needs **≥3 nodes for 2D, ≥4 for 3D**.
- **Single-node bearing (DOA):** A small mic array on one node estimates angle-of-arrival via cross-correlation (GCC-PHAT) between mic pairs.
- **Counter-sniper method:** Time gap between shockwave and muzzle blast + shockwave angle → range to a single shooter even from few nodes.

**Timing budget:** speed of sound ≈ **343 m/s** → 1 ms of clock error ≈ 0.34 m of position error. GPS-PPS sync (sub-µs) makes timing error negligible; real-world accuracy is then dominated by node-position survey accuracy, geometry (GDOP), and urban multipath/reflections.

**Sampling:** 48 kHz captures the muzzle blast well (baseline). To resolve the shockwave N-wave for trajectory work, you want ≥96–192 kHz (research-grade gunshot metrology uses far higher). Note MEMS mic bandwidth (~10–80 kHz) caps true ultrasonic capture — be honest that full shockwave trajectory analysis may need wideband transducers later. **v1 target: muzzle-blast detection + network TDOA localization at 48–96 kHz.**

---

## 2. System architecture (the trust chain)

```
[ Edge Sensor Node ]  →  [ Cluster Gateway ]  →  [ Decentralized Backend ]  →  [ Public Layer ]
  ESP32-S3 + mic array     Raspberry Pi-class        IPFS / IPFS-Cluster          Open API + Map
  GPS-PPS timestamp        heavy ML + multilat        Filecoin pinning             Verification tools
  impulse detect + sign    DID/VC verify              Blockchain anchor (CID+sig)  Trustless audit
  secure-element key       zero-trust mTLS            smart-contract registries    Open datasets
```

**Core invariant (zero-trust):** every *event object* is signed by the originating device's hardware key, its payload is content-addressed (CID) on decentralized storage, and that CID + hash + signature is anchored on-chain. **Anyone can verify a detection end-to-end without trusting the network operator, the gateway, or us.** Trust comes from cryptography + open code, not authority.

Two-tier rationale: array nodes stay cheap/low-power and do first-pass detection; one gateway per cluster does the expensive work (multi-node fusion, ML ensemble, crypto, storage, anchoring). An **all-in-one Pi-class node** variant is supported for sparse/rural deployment.

---

## 3. Hardware — from the components up

### 3.1 Microphone subsystem (the heart)
**Dual-sensitivity design** (pattern validated in high-SPL gunshot metrology and dual-mic detection patents):

- **High-AOP transient channel ×1** — *TDK InvenSense ICS-40638* (analog MEMS, **138 dB SPL AOP**, 35 Hz–20 kHz, wide temp). Won't clip on a close muzzle blast → clean amplitude/timing of the loud event. Needs a good ADC.
- **Array channels ×4** — *Infineon IM72D128* (digital PDM, **IP57 dust/water at the mic**, SNR 72 dB, tight phase/sensitivity matching for arrays, 20 Hz LFRO). Phase matching is what makes beamforming/DOA work. (Alt: *IM69D130*, 130 dB AOP.)

**Array geometry:** v1 = **planar square, ~40–60 mm spacing** on a rigid PCB → reliable azimuth DOA (elevation ambiguous; fine for ground shooters + network TDOA). v2 = **tetrahedral 4-mic** (non-coplanar) for full 3D bearing. Geometry must be defined on the PCB (repeatable) — not by loose 3D-printed jigs — or beamforming calibration drifts per unit.

### 3.2 Compute
- **Edge node:** *ESP32-S3* — vector/AI instructions for TinyML, native I²S/PDM, Wi-Fi/BLE, cheap, low power. Runs ring buffer + impulse trigger + first-pass classifier.
- **Cluster gateway:** *Raspberry Pi 5* (mains/PoE) or *Pi Zero 2 W* (battery) — runs the CNN ensemble, multilateration, IPFS node, DID/VC verification, chain client, public API. (sbts-aru confirms Pi-class is enough for ML + sub-µs timing.)

### 3.3 Time synchronization (mission-critical)
- **u-blox NEO-M9N** (or M8N) GPS with **PPS output** → discipline node clock to GPS, **sub-microsecond** alignment (proven by sbts-aru). Each event carries a GPS-disciplined timestamp.
- Fallback for GPS-denied/indoor: PTP (IEEE-1588) over wired backhaul.

### 3.4 Hardware identity / secure element (anchors the DID)
- **Microchip ATECC608B** or **NXP SE050** secure element — generates/stores the device private key in tamper-resistant silicon. The **device DID is derived from this key**; the key never leaves the chip. Every event signature originates here → unforgeable provenance and the root of zero-trust.

### 3.5 Power & connectivity
- **Power:** PoE (802.3af/at) preferred for fixed urban poles (data + power, one cable); or 12 V + small solar + LiFePO₄ for off-grid (ties to your SHI/Better-Homes solar work).
- **Backhaul:** Ethernet/PoE primary; Wi-Fi secondary; **LoRa/LPWAN** for low-bandwidth alert beaconing where there's no IP backhaul; optional cellular (CAT-M/NB-IoT) for isolated nodes.

### 3.6 Indicative BOM (per edge node)
| Item | Part | Qty |
|---|---|---|
| MCU | ESP32-S3 module | 1 |
| Array mic | Infineon IM72D128 (PDM) | 4 |
| Transient mic | TDK ICS-40638 (analog) + ADC | 1 |
| GPS+PPS | u-blox NEO-M9N | 1 |
| Secure element | ATECC608B / SE050 | 1 |
| Power | PoE PD module / solar+LiFePO₄ | 1 |
| Backhaul | onboard Wi-Fi + opt. LoRa (SX1262) | 1 |
| Misc | conformal coat, connectors, antenna | — |

*Order-of-magnitude:* edge node ~ low-tens of USD in parts at small volume; gateway adds a Pi-class board. (Don't quote firm prices — source live at build time.)

---

## 4. 3D-printed enclosure

- **Material:** **ASA** (UV-stable for outdoor sun) over PETG/PLA; PC-blend for harsh climates. Conformal-coat the PCB regardless.
- **Ingress:** target **IP65+**. Mic acoustic ports sealed with **PTFE / Gore acoustic vent membranes** (waterproof + breathable, passes sound, blocks rain/dust). Add a **pressure-equalization vent** (Gore) to stop condensation pumping.
- **Acoustics:** short, equal-length acoustic channels to each array mic; avoid resonant cavities; keep the array geometry exactly as on the PCB. Drip edges/shrouds over ports.
- **Mount:** pole/wall bracket, downtilt, tamper-evident fasteners (tamper = a signed alert event).
- **Tooling:** **FreeCAD** or **OpenSCAD** (parametric, open) so spacing/geometry are reproducible and forkable. Publish STEP + STL + source.

---

## 5. Firmware & detection pipeline

**On node (ESP32-S3):**
1. Continuous **ring buffer** (e.g., last few seconds, transient-only by design — see §6).
2. **Impulse trigger:** amplitude threshold + crest factor / kurtosis + rise-time. Cheap gate before ML.
3. **Feature extraction:** envelope, rise/decay, spectral shape, MFCC; detect **muzzle-blast + shockwave pairing**.
4. **Edge classifier:** TinyML **1D-CNN (raw) + 2D-CNN (spectrogram) ensemble** (baseline from the IEEE work) → P(gunshot) + class. Hard-negative training set is essential: fireworks, backfires, construction, slamming doors, nail guns, thunder.
5. On positive: capture window, **GPS-timestamp**, **sign with secure element**, compute per-node **DOA bearing** (GCC-PHAT across array), emit signed event.

**On gateway (Pi):**
6. **Network corroboration:** confirm only when **≥N nodes** detect within a space-time-consistent window → kills the bulk of false positives (single-node false alarms don't propagate).
7. **TDOA multilateration:** combine muzzle-blast arrival times across ≥4 nodes (Chan/Bancroft closed-form → Gauss-Newton refine) → lat/lon + uncertainty ellipse.
8. **Optional human/community review** queue before public "confirmed" status (learning from ShotSpotter's accuracy disputes — keep a review + correction loop, all logged).

**False positives are THE hard problem.** Strategy = good hard-negative dataset + multi-node consensus + uncertainty reporting + open review. Never present a detection as certainty; always publish confidence + node count + geometry quality.

---

## 6. Privacy-by-design (a pillar, not a footnote)

This is your single strongest legitimacy and legal argument, so engineer it in:

- **Transient-only capture.** The device is designed to capture/retain only short impulsive events that pass the trigger — *not* a continuous speech-quality stream. Discard non-events on-device.
- **No continuous conversation retention.** Document and prove this in the open firmware (auditors can read it).
- **Edge processing.** Classification happens on-device; raw ambient audio doesn't leave the node by default.
- **Short, content-addressed snippets only**, with a clear retention/expiry policy enforced by smart contract.
- **Why it matters:** acoustic sensors raise wiretap/recording-law and civil-liberties concerns (and proprietary systems have faced litigation over exactly this). Transient-only + fully open code + public audit is the clean answer. Confirm deployment-jurisdiction recording law before any field unit goes live (Canada/Ontario specifics to map separately, like you did with Bill 56 for TrafficMesh).

---

## 7. Decentralized data & trust layer

### 7.1 Signed event object (schema sketch)
```json
{
  "event_id": "uuid",
  "device_did": "did:dcent:...",
  "gps_time": "2026-06-20T...Z (PPS-disciplined)",
  "location_estimate": { "lat": .., "lon": .., "uncertainty_m": .. },
  "node_detections": [ { "did": "..", "toa": "..", "bearing_deg": .., "confidence": .. } ],
  "class": "gunshot",
  "confidence": 0.0,
  "audio_snippet_cid": "ipfs://Qm...",   // transient only
  "model_version": "..",
  "firmware_hash": "..",
  "manufacturer_vc": "ipfs://..",         // provenance
  "technician_install_vc": "ipfs://..",   // who installed/calibrated
  "signature": "secp256r1(secure_element)"
}
```

### 7.2 Decentralized storage
- **IPFS** for snippet + metadata (content-addressed → tamper-evident: change a byte, the CID changes).
- **IPFS-Cluster / Filecoin** pinning across the **technician + manufacturer cooperative nodes** → no single point of deletion. Retention/expiry encoded as policy.

### 7.3 Blockchain anchoring (integrity, not storage)
- Anchor **only** `{CID, payload hash, device DID, signature, timestamp}` on-chain. **Never** put raw audio on-chain (cost/privacy).
- **Smart contracts:**
  - *Node registry* — DID ↔ device, manufacturer VC, calibration status.
  - *Event registry* — anchored CIDs, immutable chain-of-custody.
  - *Access log* — who queried what, when (transparency works both ways).
  - *Staking / reputation* — technicians & manufacturers stake; bad data / tampering slashes (ties to D-Credit / Lakou mechanics).
- **Chain choice:** public low-cost L2 (max public verifiability, censorship resistance) **vs** D-Central consortium chain (cooperative governance). Recommend: anchor to a public L2 for trustless public audit, with the cooperative running validators/pinners. Decide alongside Lakou.

### 7.4 Zero-trust architecture
- No trust by network location. **Every** node→gateway→service→user interaction is authenticated (DID-based) and authorized **per request**; **mTLS** everywhere; all messages signed.
- Device identity rooted in the **secure element** (§3.4). Compromising the network gives you nothing you can forge — events are independently verifiable against on-chain anchors.

### 7.5 W3C DID + VC fabric (the cooperative supply chain)
- **Device DID** — derived from secure-element key at manufacture; anchored in node registry.
- **Manufacturer VC** — "Unit X built to spec rev Y, factory-calibrated date Z, by manufacturer M (DID)." Travels with the device.
- **Technician VC(s)** — credential proving certification to install/calibrate; **install and maintenance events are signed by the technician's DID + device DID** → verifiable field provenance.
- **Calibration VC** — periodic re-attestation; expired calibration flags the node's data confidence down.
- **Result:** an unbroken, publicly verifiable chain — *manufactured → installed → calibrated → detected → stored → anchored → served* — every link signed by a known DID. This is the part no existing gunshot system has.

---

## 8. Public access layer (open infrastructure)

- **Open REST/GraphQL API** + **public map** of confirmed events (with confidence, node count, uncertainty ellipse).
- **Trustless verification tool:** paste an event ID → it fetches the CID from IPFS, re-hashes, checks the device signature, and confirms the on-chain anchor — in the browser, no operator trust needed.
- **Open datasets:** anonymized detection history downloadable for researchers, journalists, community oversight.
- **Two-way transparency:** access logs are themselves on-chain.

---

## 9. Repository structure (open by default)

```
/hardware    KiCad PCB, gerbers, BOM (CERN-OHL-W-2.0)
/enclosure   FreeCAD/OpenSCAD source + STEP + STL
/firmware    ESP32-S3 (Apache-2.0/GPLv3)
/gateway     Pi services: ML, multilat, IPFS, chain client, API
/models      trained models + training code + dataset manifest (CC-BY-SA)
/contracts   node/event/access/staking smart contracts
/did-vc      DID method + VC schemas (manufacturer, technician, calibration)
/verify      public browser verification tool
/docs        build guide, calibration procedure, deployment + legal notes
```

---

## 10. Cooperative network model (ties to D-Central finance)
Technicians and manufacturers join as cooperative members holding DIDs/VCs; they stake to pin storage and attest builds/installs; reputation accrues on-chain; bad acts slash stake. Detection data is a public good; the cooperative monetizes manufacturing, installation, calibration, and verified-data services — not the raw public feed. (Detailed economics → cross-reference Lakou Protocol / D-Credit session.)

---

## 11. Build roadmap

1. **Bench prototype (Day-1, near-zero cost):** one ESP32-S3 + a single high-AOP mic; record/trigger on impulses; start a hard-negative dataset (record fireworks, backfires, etc.). *Begin SR&ED-style documentation from line one* — same discipline you flagged for SHI.
2. **Single multi-mic node:** 4-mic array + GPS-PPS; prove per-node DOA bearing.
3. **3-node TDOA testbed:** prove multilateration + sub-µs sync in a controlled space (starter pistol / blank-fire range with permission, or recorded playback).
4. **Decentralized backend:** wire IPFS + signing + on-chain anchor + DID/VC; ship the public verify tool.
5. **Field pilot:** small cluster on poles (PoE), enclosure weatherization, calibration VCs, community review loop. **Resolve recording-law/consent for the jurisdiction first.**
6. **Cooperative manufacturing onboarding** + network scale.

---

## 12. Open risks / gaps to track
- **False positives** — the make-or-break metric; needs a large, local hard-negative dataset and conservative multi-node consensus.
- **Mic clipping vs sensitivity** — dual-channel design mitigates but verify AOP against real close-range muzzle blasts.
- **Node-position survey accuracy** — localization is only as good as your known node coordinates.
- **Urban multipath / reflections** — degrades TDOA; mitigate with geometry + outlier rejection.
- **Shockwave bandwidth** — true trajectory analysis may exceed MEMS bandwidth; scope wideband transducers later.
- **Legal deployment** — recording/wiretap law, and the broader civil-liberties critique of gunshot detection (over-policing, accuracy disputes). Openness + transparency + privacy-by-design are the mitigations; legal review is mandatory before live field use.
- **Dataset bias** — model accuracy varies by environment, firearm, distance; publish confidence honestly.

---

*Next deep-dives available: (a) KiCad schematic + array PCB layout, (b) ESP32-S3 firmware skeleton with the trigger + I²S array capture, (c) the TDOA multilateration math + reference implementation, (d) the DID method + VC JSON schemas, (e) Ontario/Canada recording-law and deployment-legality map.*
