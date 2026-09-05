---
source_conversation_uuid: 2c6eb4aa-23e4-4e3e-be53-46332d55b214
conversation_title: 'Coworker sessions context'
created_at: 2026-08-16T15:10:28.960082Z
doc_id: DC-REINVEST-003
description: 'Consolidated master procurement plan superseding DC-REINVEST-001/002, with lease decision and full home office scope'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-REINVEST-003 — Master Infrastructure & Procurement Plan
*Supersedes DC-REINVEST-001 and DC-REINVEST-002. Final scope: everything, financed via equipment lease ($1 buyout) + shareholder loan, not deferred.*

## 1. Financing Structure
- **Equipment: $1 buyout capital lease** — higher monthly payment than FMV, but guarantees ownership at term end, matches "not downsizing" / long-term-hold intent
- **Estimated lease payment: ~$425/month**, term ~36 months
- Corp buys/leases everything directly — expensed or CCA-deducted at the corporate level, not personal write-offs

## 2. Central Server
| Item | Cost (CAD) |
|---|---|
| New mini-workstation build (Ryzen 9-class, 64–128GB RAM, 2TB NVMe) | $1,500–2,500 |
- Replaces the original enterprise-scale Phase 0 compute estimate
- Runs: FieldOps core, DC-OS control plane, Proxmox, CML, future multi-client hosting

## 3. Cisco Modeling Labs (CML)
| Item | Cost (CAD/yr) |
|---|---|
| CML Personal Plus (40 nodes) | ~$470 |
- Real, legally licensed Cisco IOS images — replaces gray-area GNS3 image sourcing
- Requires the server above (32GB+ RAM, nested virtualization)

## 4. Maximum Pi Fleet
| Role | Qty | Cost (CAD) |
|---|---|---|
| DC-OS boot node (DC-SIM stop condition) | 1 | $270–305 |
| TrafficMesh v0 | 1 (already owned) | $0 |
| DC-AGD sensing prototypes | 3 | $810–915 |
| SHI prototype nodes (cross-tier mesh) | 2–3 | $540–915 |
| Accessories (case/cooler/PSU/SSD), 6–7 new units | — | $600–980 |
| **Subtotal** | | **~$2,220–3,115** |

*SHI hardware BOM not yet formally scoped (DC-SHI-SPEC-001 covers network design, not parts) — draft DC-SHI-BOM-001 before ordering those units.*

## 5. TrafficMesh — Full Track
| Phase | Cost (CAD) |
|---|---|
| PoC Tier A+B (full-featured node) | $250–350 |
| Phase 2 custom PCB (DC-TM-BOM-002) | $300–600 |
| Phase 3 production node (DC-TM-BOM-003) | $400–700 |
| **Subtotal** | **$950–1,650** |

## 6. DC-AGD Sensing
| Item | Cost (CAD) |
|---|---|
| 3× sensor/prototype kits | $1,400–3,000 |

## 7. Homelab / Networking
| Item | Cost (CAD) |
|---|---|
| Managed 802.1Q PoE switch | $40–90 |
| Dedicated firewall/router | $150–220 |
| Used Cisco gear (optional, CML may replace need) | $50–120 |
| **Subtotal** | **$190–430** |

## 8. Home Workstation
| Item | Cost (CAD) |
|---|---|
| Work laptop (32GB RAM, dev-capable) | $1,500–2,500 |
| Monitor(s), 1–2 | $250–500 each |
| Desk + ergonomic chair | $300–800 |
| Business VPN | $60–120/yr |
| UPS for workspace | $80–150 |

## 9. Office Supplies
| Item | Cost (CAD) |
|---|---|
| Business laser all-in-one (print/scan/copy/fax) | $150–350 |
| Cable management | $20–40 |
| Basic supplies | $30–50 |

## 10. Home Office Rent (if arrangement is used)
- Corp leases a defined % of home from owner, based on actual rent paid (not applicable the same way if renting — check lease terms for sublet/business-use restrictions first)
- Illustrative placeholder: ~$270–360/month — replace with real numbers before using
- **Simpler default if renting or lease terms are restrictive:** skip this structure, let salary cover personal rent like a normal paycheck

## 11. Insurance (cross-ref DC-CORP-FINANCE-001)
- ~$2,300–5,500/yr — folded into monthly model as ~$192–458/mo

## Grand Total Summary
| Category | One-time (CAD) | Recurring |
|---|---|---|
| Server | $1,500–2,500 | — |
| CML | — | ~$470/yr |
| Pi fleet | $2,220–3,115 | — |
| TrafficMesh | $950–1,650 | — |
| AGD | $1,400–3,000 | — |
| Homelab | $190–430 | — |
| Home workstation | $2,190–4,070 | $60–120/yr (VPN) |
| Office supplies | $200–440 | — |
| Equipment financed via lease instead of lump sum | — | ~$425/mo |
| Insurance | — | $2,300–5,500/yr |
| Home office rent | — | ~$270–360/mo (placeholder) |

**See DC-FINANCIAL-MODEL-001 for the full monthly cash-flow model built from these numbers.**
