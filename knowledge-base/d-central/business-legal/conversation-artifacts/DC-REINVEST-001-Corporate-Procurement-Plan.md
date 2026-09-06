---
source_conversation_uuid: 2c6eb4aa-23e4-4e3e-be53-46332d55b214
conversation_title: 'Coworker sessions context'
created_at: 2026-08-16T15:10:28.960082Z
doc_id: DC-REINVEST-001
description: "Master reinvestment and procurement plan combining this session's backlog items with existing TrafficMesh/D-Central BOM data, sequenced against the corporate compensation strategy"
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
reconciliation_note: "Part of a three-document evolving-plan chain (DC-REINVEST-001/002/003), each later doc claiming in its own header to supersede the former -- verified NOT a clean chain on reading all three: 002 only replaces 001's deferred Tier 5 (001's Tier 0 protective spend and Tier 4 cloud-lab budget have no other copy); 003 restates most of 002's sections but drops the cloud-lab line entirely. All three left in place, none marked superseded -- discarding any one would silently lose real budget line items."
topic: "dcentral-reinvestment-procurement-plans"
consolidated_into: docs/DC-REINVEST-PROCUREMENT-RECONCILED-001.md
---

# DC-REINVEST-001 — Corporate Reinvestment & Procurement Plan
*How D-Central backlog spending gets funded, sequenced, and expensed once the corp is live.*

## Funding Mechanism (from this session)
- All purchases below made **by the corporation directly** — vendor invoice to the corp, paid from corp account, expensed at the corp level (not personal write-offs)
- Reduces corp taxable income before the 11.2–12.2% small business rate applies
- Genuine R&D hardware (TrafficMesh sensors, DC-OS node, homelab test gear) is a capital expenditure — worth noting for later SR&ED claims, since capital expenditure eligibility was restored under the 2025 SR&ED expansion
- Sequence below is ordered by **funded-now** vs. **waits for cash flow** vs. **waits for SR&ED/IRAP**

---

## Tier 0 — Fund Immediately (client revenue already covers this)
Protects the live, revenue-generating system. Highest priority regardless of everything else.

| Item | Cost (CAD) | Notes |
|---|---|---|
| UPS for Sod Boys production Pi | ~$80–150 | Prevents dirty shutdown on power blip |
| Small cloud fallback VM (Hetzner/DO) | ~$10–20/mo | Recurring, corp operating expense |
| GST/HST-registered invoicing setup | $0 | Admin, not hardware |

**Subtotal: ~$100–200 one-time + ~$15/mo recurring**

---

## Tier 1 — DC-SIM / DC-OS Stop Condition (highest strategic priority)
This converts months of simulated GNS3 work into the actual proof point.

| Item | Cost (CAD) | Notes |
|---|---|---|
| Raspberry Pi 5 (8GB or 16GB) — **dedicated to DC-OS**, separate from the TrafficMesh unit | ~$270–305 | Price elevated due to 2025–26 memory market |
| Active cooler case, USB-C PD power supply, NVMe SSD (skip microSD for this one — DC-OS deserves real I/O) | ~$100–140 | |

**Subtotal: ~$370–445**
**Decision needed:** confirm this is a *second* Pi, since the first is committed to TrafficMesh v0.

---

## Tier 2 — TrafficMesh PoC (already scoped, ~80% procured per prior BOM)
Pulled directly from DC-TM-POC-001 — no re-derivation needed.

| Phase | Cost (CAD) | Status |
|---|---|---|
| PoC Tier A (UVC camera, ELM327 OBD-II, USB-C car charger) | $60–90 | Not yet ordered |
| PoC Tier B (GPS w/ PPS, X1202 UPS HAT, fuse tap harness) | +$150–220 | Next phase |
| PoC Tier C stretch (MCP2515 CAN, USB-Ethernet dongle, RTC) | +$30–60 | Optional |
| **Full-featured PoC total** | **$250–350 all-in** | Milestone: full CivicMesh evidence pipeline in the Hyundai |

**Subtotal: ~$250–350** — this is the fastest, cheapest real deliverable in the whole backlog. Order this first if cash is tight.

---

## Tier 3 — Homelab Expansion (parallel, supports both CST8315 and TrafficMesh broker)

| Item | Cost (CAD) | Priority |
|---|---|---|
| Managed 802.1Q switch (TP-Link TL-SG108E or TL-SG2210P PoE) | $40–90 | Highest — enables real VLAN work from DC-SHI-SPEC-001 |
| Dedicated firewall/router (N100 mini PC + OPNsense, or MikroTik) | $150–220 | |
| Used Proxmox host (broker + cyber range) | $150–300 | Conditional on dc-node-01 networking being resolved |
| Used Cisco gear (CST8315 practice) | $50–120 | Optional |

**Subtotal: ~$350–600**

---

## Tier 4 — Cloud Engineer Multi-Cloud Portfolio (this session's addition)

| Item | Cost (CAD) | Notes |
|---|---|---|
| AWS / Azure / GCP lab spend | ~$50–100/mo while active | Free tiers cover most of it; budget a buffer |
| Oracle Cloud, Cloudflare Workers/D1/R2 | $0 | Free tier sufficient |
| Terraform/OpenTofu, CI/CD | $0 | Open source |

**Subtotal: ~$50–100/mo during active lab work, otherwise $0**

---

## Tier 5 — Deferred Until SR&ED/IRAP Cash Actually Lands

| Item | Cost (CAD) | Trigger |
|---|---|---|
| TrafficMesh Phase 2 custom PCB (DC-TM-BOM-002) | $300–600 | After PoC validates the concept |
| TrafficMesh Phase 3 production node (DC-TM-BOM-003) | $400–700/node | After PCB phase proves out |
| DC-AGD sensing prototypes (3 nodes) | $1,400–3,000 | Same skill set as TrafficMesh, second thesis proof |
| Phase 0 shared compute foundation (agent cabinet, cyber range, AGD gateway host) | $9,750–16,450 | **Explicitly deferred** until SR&ED refund or IRAP contribution actually flows — don't fund this from early client revenue |

**Subtotal: deferred, ~$11,850–20,750 when it's time**

---

## Recommended Order of Operations
1. **Tier 0** — protect the live system (do this regardless, small $)
2. **Tier 2 (PoC Tier A+B)** — cheapest real D-Central deliverable, ~$250–350, kicks off the first SR&ED ledger entry
3. **Tier 1** — second Pi 5 for DC-OS, once Tier 2 is ordered and cash allows
4. **Tier 3** — homelab, in parallel, as CST8315 coursework demands it
5. **Tier 4** — cloud lab spend, ongoing, small and flexible
6. **Tier 5** — hold. Do not fund from early client revenue. This is what the SR&ED/IRAP money is *for*.

**Running total to get everything through Tier 4 funded: roughly $1,100–1,700 CAD one-time, plus ~$65–115/month recurring.**


<!-- AUTO-GENERATED RELATED START (scripts/build_obsidian_graph.py) -->

## Related (auto-generated)

**Topics:**
- [[knowledge-base/_topics/dcentral-reinvestment-procurement-plans|dcentral-reinvestment-procurement-plans]]

**Consolidated into:**
- [[docs/DC-REINVEST-PROCUREMENT-RECONCILED-001]]

<!-- AUTO-GENERATED RELATED END -->
