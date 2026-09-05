---
source_conversation_uuid: df8f544e-9dca-422f-8bcf-e82e7df6e3b1
conversation_title: 'Modern police'
created_at: 2026-06-20T18:21:12.421156Z
doc_id: DC-AGD-003
description: 'AGD-to-SkyLedger drone-as-first-responder integration spec: event/API bridge, governed dispatch policy engine, mission lifecycle, WeatherMesh/airspace gating, provenance continuity, feedback loop, privacy invariants, Canadian BVLOS regulatory constraint, and network effects'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-AGD-003 — AGD × SkyLedger: Drone-as-First-Responder Integration
### How a confirmed gunshot dispatches a SkyLedger drone — the pipeline, the API, the governance
**Status:** v0.1 · execution 0% · bridges DC-AGD-001/002 ↔ DC-SKY-* (SkyLedger)
**Premise:** Detection is passive; **detection → dispatch** is what actually shortens response time. This spec defines the contract between the gunshot network and the drone ecosystem.

> ⚠️ **sky.* service names below are inferred touchpoints — reconcile with the real DC-SKY-* registry.** I'm mapping the *interface*, not redefining SkyLedger's internals.

---

## 0. The market analogue (validate the pattern, then beat it)

| Incumbent | What they prove | Where they're vulnerable |
|---|---|---|
| **ShotSpotter "NAPI" push API → DFR** | The exact pattern: gunshot alert → push lat/long → drone flies to scene, streams video. Integrates with RTCC, LPR, CAD/RMS. | Proprietary black box; false-positive-prone; opaque. |
| **Flock DFR + Aerodome** | Docked rooftop drones, dispatch to 911/LPR/gunshot geo-coords, on-scene in **<90 s**. | Closed platform; ALPR civil-liberties record. |
| **NYPD DFR** | Drones fly **autonomously to the exact lat/long** of gunshot alerts from rooftop docks. | Centralized control; oversight disputes. |
| **DFR metrics (real program)** | 340 calls; beat patrol on-scene 194×; priority-one avg **2:19 vs 3:52** for patrol. | — |

**The EFF critique = our design brief:** false positives + sensors concentrated in marginalized neighborhoods → drones could disproportionately surveil those same communities. **D-Central's differentiation is to make the dispatch pipeline open, governed, cryptographically auditable, privacy-floored, and non-weaponized — the answer to the panopticon critique, not another instance of it.**

Fort Worth's "responsible DFR" features are the floor to match and exceed: incident-only (no roaming patrol); camera to the horizon in transit, tilting to the scene only on arrival; every flight logged and auditable; public dashboard. **We match all of these and add tamper-evident, publicly-verifiable provenance.**

---

## 1. End-to-end flow

```
AGD network                          BRIDGE                         SkyLedger
───────────                          ──────                         ─────────
gunshot.confirmed  ──(signed event)──► Dispatch Policy ──(dispatch ──► sky.dispatch
(multi-node consensus,                  Engine (GOVERNED   request,        │
 location + uncertainty,                gate: thresholds,  signed)    sky.fleet (pick drone)
 confidence)                            geofence, HITL,                sky.weather=WeatherMesh ✓
                                        rate limit, floor)             sky.airspace (authorize) ✓
                                              │                        sky.flight (launch+navigate)
                                              ▼                        sky.stream (live video)
                                        Mission created ◄──────────────┘
                                              │
        footage + telemetry (signed, anchored) ──► shared data fabric ──► authorized consumers
                                              │
                                              ▼
                              FEEDBACK: footage confirms/refutes shot
                              → labels → AGD ML flywheel (DC-AGD-002 §B.6)
```

---

## 2. Integration architecture

Three coupling mechanisms, used together:

1. **Event-driven (primary):** AGD publishes `gunshot.confirmed` to the data-fabric pub/sub (libp2p gossipsub, per DC-AGD-002 §B). SkyLedger's intake subscribes, geofenced to its coverage. Loose coupling, reactive, no AGD↔SkyLedger hard dependency.
2. **Dispatch API (stateful):** the bridge calls `POST /sky/v1/dispatch` with the signed event; gets a `mission_id`; tracks lifecycle via `GET /sky/v1/mission/{id}` + status webhooks/stream.
3. **The Bridge Connector:** a governed component with **its own DID**, sitting between the networks. It runs the **Dispatch Policy Engine** (§4) and is the single accountable chokepoint — every dispatch decision flows through it and is logged. Not "AGD calls drone directly"; a governed gate in between.

---

## 3. Contracts (signed, provenance-carrying)

**Dispatch Request** (bridge → SkyLedger):
```json
{
  "request_id": "uuid",
  "source_event": { "event_id": "..", "cid": "ipfs://..", "anchor_tx": ".." },
  "location": { "lat": .., "lon": .., "uncertainty_m": .. },
  "confidence": 0.0, "node_count": N, "rounds_est": ..,
  "policy_decision": { "auto": false, "hitl_required": true, "rule_id": ".." },
  "constraints": { "no_scan_transit": true, "incident_only": true, "non_weaponized": true },
  "bridge_did": "did:dcent:bridge:..",
  "signature": ".."
}
```
**Mission** (SkyLedger → fabric): `mission_id`, assigned `drone_did`, accepted/rejected + reason, ETA, live `stream_uri`, telemetry CIDs, footage CID, completion + anchor. All signed by the **drone's device DID** — provenance continues across the boundary.

---

## 4. The Dispatch Policy Engine (the governed gate)

**Never hardwire "gunshot → drone."** A policy layer decides *whether* to dispatch, governed by the **Civic DAO + local jurisdiction sub-DAO** (DC-AGD-002 §A) and bound by the **constitutional floor**:

- **Confidence + consensus threshold** — require ≥N corroborating nodes and ≥X confidence before *any* dispatch. This is the primary false-positive→over-dispatch defense (directly answers the EFF critique).
- **Geofence / no-fly** — only within authorized, airspace-clear areas.
- **Rate limiting & dedup** — one mission per incident; cap simultaneous launches.
- **Time/area rules** — governed, transparent (not opaque), with published equity review of where dispatch is enabled (the sensor-placement-disparity concern is a *governed, auditable* decision).
- **Human-in-the-loop (default)** — a credentialed dispatcher confirms launch. **Human-on-the-loop** (auto-launch, human can abort) only where explicitly authorized by the local sub-DAO. **Never silent fully-autonomous dispatch by default.**
- **Every decision logged + anchored** — including *non*-dispatch decisions (transparency both ways).

---

## 5. Pre-launch gating (SkyLedger side, before any motor spins)

- **`sky.weather` = WeatherMesh** — wind, precip, visibility, temp vs the drone's flight envelope. No-go if unflyable.
- **`sky.airspace`** — authorization + deconfliction via NAV CANADA / NavDrone; check controlled-airspace status, NOTAMs, altitude ceiling. **This is a hard gate** (see §9).
- **`sky.fleet`** — nearest available drone with battery/range to reach the location and return; dock health.
- **`sky.geo`** — geofence / no-fly / privacy-exclusion zones (schools, etc. per policy).
- Any failed gate → mission rejected with a logged reason; AGD event still recorded (detection ≠ dispatch).

---

## 6. sky.* touchpoints (reconcile with DC-SKY registry)

| Function | Inferred service | Role in DFR flow |
|---|---|---|
| Mission intake/orchestration | `sky.dispatch` | Accept request, run the mission |
| Drone availability/assignment | `sky.fleet` | Pick the drone + dock |
| Launch + autonomous navigation | `sky.flight` / `sky.autopilot` | Fly to lat/long |
| Flyability | `sky.weather` (**WeatherMesh**) | Go/no-go |
| Airspace authorization | `sky.airspace` | NavDrone/deconfliction |
| Live video/sensor downlink | `sky.stream` / `sky.vision` | Real-time overwatch |
| Dock/charge | `sky.dock` / `sky.charge` | Drone-in-a-box |
| Geofencing | `sky.geo` | No-fly/privacy zones |
| Provenance/anchoring | `sky.ledger` | Sign + anchor telemetry/footage |

---

## 7. Latency budget — time-to-overwatch

| Stage | Budget | Note |
|---|---|---|
| Detection → multi-node confirmation | ~1–3 s | **consensus reduces false dispatch but adds latency — the core tradeoff** |
| Policy eval + (HITL confirm) | <1 s auto / human-paced if HITL | HITL adds seconds but adds accountability |
| Weather/airspace/fleet gates | <1 s | parallelized |
| Drone-in-a-box launch | ~10–30 s | spin-up + clear dock |
| Flight to scene (1–2 km @ ~15–20 m/s) | ~60–120 s | matches incumbents' "<2 min" |
| **Total to on-scene overwatch** | **~1.5–3 min** | competitive with the 2:19 priority-one benchmark |

Tune the consensus threshold against this budget: tighter consensus = fewer false dispatches, slightly slower. That tradeoff is a **governed parameter**, not a hardcoded constant.

---

## 8. Provenance & zero-trust continuity

The chain of custody **doesn't break at the system boundary**:
`gunshot event (device DID, anchored) → dispatch request (bridge DID, signed) → mission (drone DID) → footage/telemetry (drone DID, CID, anchored)`.
Anyone can verify the whole sequence trustlessly: *this drone flew, because this bridge decided, because this gunshot was detected by these nodes* — each link signed, each artifact content-addressed and anchored. This is what no incumbent offers.

---

## 9. Regulatory constraint — the SkyLedger "Bill 56" (Canada, current)

Canada's **2025 RPAS Regulations (SOR/2025-70)** came into force in two phases (Apr 1 & **Nov 4, 2025**). They opened **lower-risk BVLOS without an SFOC** — *but only in uncontrolled airspace, below 122 m (400 ft), away from aerodromes, and away from densely populated areas (≥1 km).*

**The problem:** urban DFR gunshot response operates **over densely populated areas** — exactly what the lower-risk BVLOS carve-out *excludes*. So autonomous urban DFR still requires:
- a **Special Flight Operations Certificate (SFOC)** (or higher-tier authorization) for populated-area BVLOS;
- an **RPAS Operator Certificate (RPOC)** for the operating org;
- **Level 1 Complex Operations** pilot certification for the humans in/on the loop;
- compliance with the **75% Canadian-ownership** rule for commercial air services (touches D-Central Group Inc. structure + CCPC status you already track).

**Action:** treat SFOC-for-populated-area-BVLOS as the primary blocker, the way Bill 56 anchored TrafficMesh. Phase 1 deployments should target authorized/controlled pilot zones; full urban autonomous DFR is a regulatory project, not just an engineering one. (Map the exact pathway in a dedicated session.)

---

## 10. Privacy & accountability invariants (extend the constitutional floor)

Add these AGD×SkyLedger invariants to the DC-AGD-002 floor — they're both ethics and moat:

- **Non-weaponized, always.** These are observation/overwatch drones. No payload capable of force. Immutable.
- **Incident-only dispatch.** No roaming patrol; a drone launches only against a confirmed, policy-cleared event.
- **No-scan transit.** Camera to the horizon in flight; tilts to the scene only on arrival (matches Fort Worth; enforced in `sky.flight`).
- **Human accountable for every launch** by default (HITL).
- **Publicly-verifiable flight log + dashboard** — every mission logged, anchored, and queryable by the public, with the trustless verifier.
- **Governed, transparent coverage equity** — where dispatch is enabled is a public, auditable Civic-DAO decision, explicitly to prevent the disproportionate-surveillance pattern EFF documented.

---

## 11. Feedback loop (closes the flywheel)

Drone footage/sensors **confirm or refute** the detection (shooter seen? casings? or just fireworks?). Those labels feed back into AGD's governed ML retraining (DC-AGD-002 §B.6) → fewer false positives → fewer needless dispatches → more trust. **The drone makes the ear smarter.** This is a cross-system data network effect that incumbents' siloed stacks capture far less of.

---

## 12. SDK / API surface

- **`agd-sdk`** gains: subscribe to `gunshot.confirmed`, inspect policy decisions, verify dispatch provenance.
- **`sky-sdk`** gains: `dispatch(event)`, `mission(id)`, mission status stream, footage/telemetry fetch+verify.
- **Bridge SDK**: register policy rules (governed), simulate dispatch (dry-run), audit log export.
- All dispatch/mission objects use the **shared signed-event envelope** (DC-AGD-002 §B.2) → other systems (OSIRIS, digital twin, OS-PATROL, CTS) consume the same stream without bespoke glue.

---

## 13. Network effects (deepens DC-AGD-002 §D.5, ecosystem fusion)

- **Super-additive fusion:** gunshot + drone overwatch + (TrafficMesh ALPR / vehicle) + digital-twin replay is worth far more than any single feed — and each added system raises the value of every other. SoundThinking already monetizes the ShotSpotter→PlateRanger(LPR)→DFR chain; **you do the same, but open and verifiable, so the value accrues to the commons.**
- **Cross-system data flywheel:** the feedback loop (§11) means drones improve detection improves dispatch precision improves trust improves adoption.
- **Shared dispatch substrate:** once the bridge exists for gunshots, the *same* governed dispatch pipeline serves any future AGD-platform modality (glass-break, structure fire, medical) → one integration, many triggers. Marginal cost of the next trigger → near zero.
- **Reuse the asset:** SkyLedger gains a high-value, recurring demand source (DFR missions); AGD gains kinetic response. Each network makes the other more deployable — classic two-network cross-side effect.

---

## 14. Roadmap

1. **Simulated dispatch (Day-1):** wire `gunshot.confirmed` → bridge → **dry-run** dispatch (no real flight). Prove the policy engine, schemas, provenance, latency budget end-to-end. Zero regulatory exposure; start SR&ED docs.
2. **HITL pilot in an authorized zone:** real drone-in-a-box, human-confirmed launch, in a controlled/SFOC-approved area. Validate time-to-overwatch + footage feedback loop.
3. **Weather/airspace integration:** WeatherMesh + NavDrone gates live.
4. **Provenance + public dashboard:** anchored missions + trustless verifier + public flight log.
5. **Regulatory project (parallel track):** RPOC + Level 1 Complex + populated-area SFOC pathway.
6. **Multi-modal:** generalize the bridge to other AGD-platform triggers.

---

## 15. Open gaps / risks
- **Regulatory** — populated-area autonomous BVLOS is the gating constraint (§9); engineering can run ahead in sim + authorized zones.
- **False-positive over-dispatch** — the central ethical risk; consensus thresholds + HITL + governed equity are the mitigations; measure relentlessly.
- **Latency vs consensus** tradeoff — governed parameter, not a constant.
- **Airspace deconfliction** at scale — multiple drones + manned aircraft; lean on NavDrone + `sky.airspace`.
- **Privacy of overflight** — no-scan transit + incident-only + public log; defend as a floor.
- **Drone failure modes** — lost-link, battery, dock unavailability; fail safe + logged.
- **sky.* mapping** — reconcile inferred services with the real DC-SKY-* registry.

---

*Next deep-dives: (a) the Dispatch Policy Engine as governed on-chain rules + the HITL console, (b) the full mission-lifecycle state machine + retry/abort semantics, (c) the populated-area SFOC/RPOC regulatory pathway for Ontario, (d) the WeatherMesh + NavDrone go/no-go gate spec, (e) the footage→label→retrain feedback implementation.*
