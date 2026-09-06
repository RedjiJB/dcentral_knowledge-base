---
source_conversation_uuid: 2c6eb4aa-23e4-4e3e-be53-46332d55b214
conversation_title: 'Coworker sessions context'
created_at: 2026-08-16T15:10:28.960082Z
doc_id: DC-REINVEST-002
description: 'Full immediate buildout plan replacing deferred Tier 5, right-sized server + max Pi fleet + AGD + SHI + CML licensing'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
reconciliation_note: "Part of a three-document evolving-plan chain (DC-REINVEST-001/002/003), each later doc claiming in its own header to supersede the former -- verified NOT a clean chain on reading all three: 002 only replaces 001's deferred Tier 5 (001's Tier 0 protective spend and Tier 4 cloud-lab budget have no other copy); 003 restates most of 002's sections but drops the cloud-lab line entirely. All three left in place, none marked superseded -- discarding any one would silently lose real budget line items."
topic: "dcentral-reinvestment-procurement-plans"
consolidated_into: docs/DC-REINVEST-PROCUREMENT-RECONCILED-001.md
---

# DC-REINVEST-002 — Full Immediate Buildout
*Supersedes Tier 5 deferral in DC-REINVEST-001. Everything scoped now, right-sized instead of enterprise-scale, so the real total is lower than the original $11.8K–20.75K deferred estimate — but it's still real money. Fund it knowingly (see note above).*

---

## A. Central Server (replaces "Pi as edge doing everything")

Right-sized to actually run CML nested virtualization, Proxmox, the FieldOps core, and future multi-client hosting — without the noise/power draw of old enterprise rack gear.

| Option | Cost (CAD) | Notes |
|---|---|---|
| **New mini-workstation build** (Ryzen 9 or similar, 64–128GB RAM, 2TB NVMe) | $1,500–2,500 | Recommended — quiet, efficient, sized for CML + Proxmox + client hosting |
| Used enterprise rack server (Dell R730-class, dual Xeon, 128GB) | $400–900 | Cheaper upfront, but loud and power-hungry for home use — factor in electricity cost |

**This server functionally replaces the original Phase 0 compute foundation estimate** ($9,750–16,450) — that figure assumed enterprise-scale buildout. A right-sized single host covers CML, the cyber range, the AGD gateway, and multi-client capacity for a fraction of that.

**Recommended: $1,500–2,500**

---

## B. Cisco Modeling Labs (CML) — real Cisco licensing

| Item | Cost (CAD) | Notes |
|---|---|---|
| CML Personal Plus (40 nodes) | ~$470/yr (349 USD) | Legit Cisco IOS-XE/XR/NX-OS images, replaces gray-area image sourcing |
| Runs on the new server above | $0 additional | Needs the 32GB+ RAM host from Section A |

**Recommended: ~$470/yr recurring**

---

## C. Maximum Pi Fleet

| Role | Qty | Cost each (CAD) | Subtotal |
|---|---|---|---|
| DC-OS boot node (DC-SIM stop condition) | 1 | ~$270–305 | $270–305 |
| TrafficMesh v0 | 1 (already owned) | — | $0 |
| DC-AGD sensing prototypes | 3 | ~$270–305 | $810–915 |
| SHI prototype nodes (cross-tier mesh validation) | 2–3 | ~$270–305 | $540–915 |
| Accessories (case, cooler, PSU, SSD) per unit | 6–7 new units | ~$100–140 | $600–980 |

**Subtotal: ~$2,220–3,115** (boards + accessories, excluding the TrafficMesh unit you already own)

*Note: SHI hardware BOM isn't formally scoped yet the way TrafficMesh is — DC-SHI-SPEC-001 covers the VLAN/network design, not a physical parts list. I priced these as bare Pi 5 units; if you want a real DC-SHI-BOM-001 with sensor/actuator specifics per tier, that's worth doing before ordering, not guessing at.*

---

## D. TrafficMesh — full track, no deferral

| Phase | Cost (CAD) |
|---|---|
| PoC Tier A+B (full-featured node) | $250–350 |
| Phase 2 custom PCB (DC-TM-BOM-002) | $300–600 |
| Phase 3 production node (DC-TM-BOM-003) | $400–700 |

**Subtotal: $950–1,650**

---

## E. DC-AGD Sensing (hardware beyond the Pi boards above)

| Item | Cost (CAD) |
|---|---|
| 3× AGD sensor/prototype kits (per prior BOM) | $1,400–3,000 |

---

## F. Homelab / Networking (supports server + fleet)

| Item | Cost (CAD) |
|---|---|
| Managed 802.1Q switch, PoE-capable | $40–90 |
| Dedicated firewall/router | $150–220 |
| Used Cisco gear (physical CST8315 practice, optional now that CML exists) | $50–120 (optional — CML may replace this need) |

**Subtotal: $190–430** (Proxmox host line item removed — covered by Section A now)

---

## G. Cloud (parallel, from the multi-cloud lab track)

| Item | Cost (CAD) |
|---|---|
| AWS/Azure/GCP lab spend | $50–100/mo |
| Cloud fallback VM (FieldOps) | $10–20/mo |

---

## Grand Total — Everything, Now

| Category | Low (CAD) | High (CAD) |
|---|---|---|
| Server | $1,500 | $2,500 |
| CML license (yr 1) | $470 | $470 |
| Pi fleet + accessories | $2,220 | $3,115 |
| TrafficMesh (all phases) | $950 | $1,650 |
| DC-AGD sensing | $1,400 | $3,000 |
| Homelab/networking | $190 | $430 |
| **One-time total** | **$6,730** | **$11,165** |
| **Recurring** | **~$60–120/mo** | (cloud + CML amortized) |

**This is roughly half the original deferred estimate**, because right-sizing the server replaced the enterprise-scale Phase 0 figure. Still a real number that needs a real funding source before ordering — personal capital, credit, or an active IRAP conversation.

## Still Missing Before This Is Fully Ordered
- SHI physical hardware BOM (DC-SHI-BOM-001) — not yet scoped, priced here as bare boards only
- Confirmed funding source for the $6,730–11,165


<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Topics:**
- [[knowledge-base/_topics/dcentral-reinvestment-procurement-plans|dcentral-reinvestment-procurement-plans]]

**Consolidated into:**
- [[docs/DC-REINVEST-PROCUREMENT-RECONCILED-001]]

<!-- AUTO-GENERATED RELATED END -->
