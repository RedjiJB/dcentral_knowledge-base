---
source_conversation_uuid: 702c2d45-c80d-429a-a545-2850a38a6543
conversation_title: 'Mobile SOC center setup options'
created_at: 2026-07-22T11:23:34.845895Z
doc_id: DC-MSOC-001
description: 'DC-MSOC-001: Mobile SOC specification registry document'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-MSOC-001 — Mobile Security Operations Capability Specification

**Registry ID:** DC-MSOC-001
**Status:** Registered — Deliberately Parked (no capital authorized before Phase 2 trigger)
**Owner:** OpenSecure / Sovereign Cyber Range initiative
**Related:** DC-VENTURE-001, DC-STATUS-001, Sovereign Cyber Range Network v2

---

## 1. Purpose and position in the roadmap

This document captures the mobile SOC concept so that it exists in the registry without competing for capital on the critical path. The capability is explicitly *not* a prerequisite for revenue; it is unlocked by revenue. Its three roles at maturity are: on-site assessment and incident-response delivery for OS-PACS clients, SR&ED-relevant test platform, and the Sovereign Cyber Range's physical training and demonstration unit.

## 2. Capability tiers

### Tier A — Fly-away kit (Phase 2 asset, ~$3,000–5,000 CAD)

A rugged transit case (Pelican class) containing a mini-PC or NUC-class node sized for SIEM ingestion and a small number of VMs (64 GB RAM minimum), a managed switch, a portable firewall appliance (Protectli/Netgate class), a network TAP/SPAN capability for client-network capture, and LTE plus optional Starlink uplink. Operator laptops run the standing software stack. The kit doubles as a cyber-range demo rig at events and as the field-assessment toolkit for OS-PACS engagements.

**Acquisition trigger:** OpenSecure subcontract revenue flowing and first OS-PACS direct client signed (roughly Month 6–12). The kit must be justifiable as a billable-engagement tool, not a speculative build.

### Tier B — Enclosed trailer build (Phase 3 asset, ~$10,000–15,000 CAD)

A tandem-axle enclosed cargo trailer, 7×14 to 8.5×20, built out as a deployable operations room. Detaches from the tow vehicle, keeps capital far below a van conversion, and serves as the Sovereign Cyber Range's mobile training and demonstration unit.

Build-out requirements: closed-cell spray-foam insulation with a mini-split or rooftop AC unit sized for both equipment and occupied operator shifts; a 10–15 kWh LiFePO4 battery bank with a 3 kW+ inverter, shore-power inlet, roof solar, and a quiet inverter generator as tertiary power; a shock-mounted transit rack (never a static rack) for the compute, switching, and firewall stack; and a crank-up or pneumatic mast carrying antennas, Starlink, and camera payloads. Connectivity is Starlink primary with LTE failover.

**Acquisition trigger:** OS-PACS recurring (Stage 2) revenue sustaining the monitoring tier, Year 2 or later.

### Tier C — Vehicle conversion (deferred indefinitely)

High-roof extended cargo van (Transit/Sprinter/ProMaster class, 3500-series payload) or 16-ft cube van. Registered here only for completeness; the ~$70K+ properly outfitted cost is not justified until the trailer proves utilization, and possibly never if the trailer suffices.

## 3. Software stack (common to all tiers)

Security Onion or Wazuh as the SIEM core, Zeek and Suricata for network telemetry, Velociraptor for endpoint triage during incident-response engagements, and the standing threat-intel feeds from the cyber-range environment. The stack is identical to the fixed cyber-range tracks so that training, tooling, and playbooks transfer without modification.

## 4. Registry discipline

No purchase order against this document may be raised before its tier trigger condition is met and confirmed against the Lakou vault capital-allocation process in DC-GOV-002. This clause exists because DC-STATUS-001 identified the ecosystem's standing failure mode as design-complete, execution-zero artifacts accumulating while the critical path starves.
