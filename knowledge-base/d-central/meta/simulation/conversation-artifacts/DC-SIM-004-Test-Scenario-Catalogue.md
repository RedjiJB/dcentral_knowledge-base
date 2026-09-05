---
source_conversation_uuid: 8f7a2740-7f7b-4f16-b483-d1e161ebb85e
conversation_title: '💬 I have an idea for the dcentra…'
created_at: 2026-08-08T03:34:00.540823Z
doc_id: DC-SIM-004
description: 'Test scenario catalogue with measurement methodology'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
topic: "dcentral-simulation-lab-programme"
---

# DC-SIM-004 — Test Scenario Catalogue

| Field | Value |
|---|---|
| Document ID | DC-SIM-004 |
| Version | v1.0 |
| Date | August 2026 |
| Author | Toussaint Redji Jean Baptiste |

---

## 1. Principle

Every scenario is an **executable script**, not a manual click-through. Results that
cannot be reproduced by re-running a script are anecdotes, not evidence.

All scenarios write to `results/` with a timestamp and the git commit of the topology
and configuration that produced them.

---

## 2. The four proofs, and their ordering

| # | Proof | Confidence | Note |
|---|---|---|---|
| 1 | Service reachability | High | Real routing, real policy |
| 2 | Convergence and failover | High, **relative only** | Valid for comparing timer configs; not an absolute SLA figure |
| 3 | Bandwidth sizing | **Low — see §5** | Offered-load argument, not measurement |
| 4 | Security segmentation | High | Real nftables/ACL code |

**Ordering is not arbitrary.** Reachability is the smoke test gating everything else.
Segmentation runs last, because policy results are meaningless until paths are known-good.
Running these out of order produces days spent debugging a segmentation "failure" that
was a routing bug.

---

## 3. Scenario 1 — Baseline run

The core scenario. Passing this is the programme stop condition.

| Step | Action | Measurement |
|---|---|---|
| 1 | Boot all nodes | Time to full convergence from cold start |
| 2 | Reachability sweep | Every service endpoint reachable from every authorised source; unreachable from every unauthorised one |
| 3 | Baseline load | MGEN profiles per service class, fixed window, uplink shaped to target |
| 4 | FSO degradation | Step `clear → haze → rain → fog`; record loss, latency, and the point at which routing reacts |
| 5 | Hard link failure | Drop primary path; measure reconvergence, BFD tuned vs untuned |
| 6 | Segmentation assertions | Attempt every prohibited flow; confirm each dropped **and logged** |
| 7 | Restore | Verify reconvergence with no flapping and no black holes |

---

## 4. Traffic profiles

Synthetic profiles map to actual D-Central workloads. Generation tools in increasing
order of effort: **iperf3** (throughput), **MGEN** or **D-ITG** (statistical — Poisson,
burst, CBR), **Ostinato** (crafted packets, ships as a GNS3 appliance), **scapy**
(protocol-level control).

| Class | Character | Tool |
|---|---|---|
| Mesh telemetry | Small, frequent, bursty | MGEN Poisson |
| Vault transactions | Small, latency-sensitive, bidirectional | MGEN + real ACA-Py |
| Camera / OpenSecure | Sustained high bitrate | MediaMTX real stream |
| Inter-SHI inference | Large request/response, latency-sensitive | Stub (see DC-SIM-001 §5.5) |
| Bulk sync | Elastic, background | iperf3 |

### 4.1 tcpreplay — the cheapest realism available

Replaying a captured pcap beats guessing at a synthetic profile. Capture from lab
hardware or personally owned devices only.

> **Constraint.** Capturing on an employer's network requires their written
> authorisation. Not worth the ambiguity — use own-equipment captures.

---

## 5. Scenario 3 — bandwidth sizing, and its honest limitation

**GNS3 cannot measure throughput that can be trusted.** Link rates are asserted by a
shaper; forwarding is bounded by host CPU.

What is legitimate: **offered-load modelling.** Define per-service traffic profiles, sum
them against a shaped uplink, and identify the point at which the shaper begins dropping.

This is a sizing **argument**, not a measurement. Labelled as such in the write-up it
remains defensible and is a valid input to the DC-ISP-POC-001 BOM. Presented as measured
throughput it is an overclaim that a technical reviewer will catch immediately.

---

## 6. Scenario 5 — media under degradation

The best demonstration artefact in the programme, and the most legible to a
non-technical audience.

**Setup.** MediaMTX or Owncast on a site node. Stream pushed to it. Player opened in
the host browser via the Cloud bridge (DC-SIM-005).

**Run.** Apply FSO weather profiles to the POP-to-site link in sequence. Observe:
buffering onset, adaptive bitrate ladder stepping down, stall threshold. Then drop the
link entirely — does routing move the stream to the backup path fast enough for playback
to survive, or does the session die and reconnect?

The bitrate is real, the loss is real, the player's reaction is real. **The link capacity
is asserted by a shaper, not achieved by hardware.**

---

## 7. Scenario 6 — partition and recovery

The scenario nobody runs, and the one that matters most for Haiti deployment conditions.
The operating question is not "does the service run" — it is **what every component does
when a site is partitioned for six hours and then returns.**

| Subsystem | Observation |
|---|---|
| Storage (IPFS/Ceph/MinIO/Garage) | Reconciliation on rejoin; conflict handling |
| K3s | Split-brain behaviour; eviction and rescheduling |
| DID/VC (ACA-Py) | Does credential presentation survive 40% loss; graceful resolver timeout; agent recovery on rejoin |
| DTN (ION/µD3TN) | Bundles queue during outage and deliver on reconnect — **the strongest single result available in this programme** |
| Cached inference | Staleness handling |
| Media | Buffering, reconnection |
| UI | Does the dashboard degrade usefully or hang; does a vault transaction show a real error or spin |
| Policy (see DC-SIM-007) | Does a partitioned node enforce stale policy, and for how long |

### 7.1 UI under degradation

Underrated and cheap. Run the UI in a container, reach it from the host browser through
the Cloud bridge, then degrade the link while clicking through real flows. Almost nobody
tests UX under degraded network, and it is the normal condition for the deployment target.

---

## 8. Write-up requirements

Every published result must carry an explicit limitations section stating:

1. FSO and GPON conditions are **asserted**, not simulated optics
2. Bandwidth figures are **offered-load modelling**, not measurement
3. Convergence figures are **relative**, not absolute SLA claims
4. Mesh link-quality metrics, if any mesh results are included, are **fiction** —
   the protocol converges correctly for reasons that do not exist (DC-SIM-001 §3.4)
5. No wireless, RF, or physical-layer claim is supported by any result in this programme

Naming these boundaries reads as rigour. Omitting them and being caught reads as the
opposite.
