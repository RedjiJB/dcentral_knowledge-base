# DC-REINVEST-PROCUREMENT-RECONCILED-001 — D-Central Reinvestment & Procurement Plans, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `dcentral-reinvestment-procurement-plans` (3 docs).

## Current understanding

Three sequential procurement-planning documents from the same conversation, each claiming in its own
header to supersede the one(s) before it. A prior Stage 4 dedup pass already verified this is **not** a
clean supersession chain by reading all three in full — that verdict is restated and applied here rather
than re-derived, since the Consolidator inherits rather than re-litigates confirmed dedup findings.

**DC-REINVEST-001 (incorporated):** the original 6-tier procurement plan, funded-now vs. cash-flow-
gated vs. SR&ED/IRAP-gated. Tier 0 (protect the live production system: UPS, cloud fallback VM,
invoicing setup, ~$100-200) is fund-immediately. Tier 1 is a second Raspberry Pi 5 dedicated to DC-OS
(~$370-445). Tier 2 is the TrafficMesh PoC, described as "the fastest, cheapest real deliverable in the
whole backlog" (~$250-350). Tier 3 is homelab networking (~$350-600). Tier 4 is cloud-engineering lab
spend (~$50-100/mo, mostly free-tier). **Tier 5 is explicitly deferred** ($11,850-20,750, an
enterprise-scale Phase 0 compute foundation) until SR&ED/IRAP funds actually arrive — explicitly not to
be funded from early client revenue [Tiers 0-5, Recommended Order of Operations].

**DC-REINVEST-002 (incorporated):** replaces only Tier 1's deferred estimate with a right-sized
alternative — a single mini-workstation server ($1,500-2,500) covering CML/Proxmox/AGD-gateway/multi-
client hosting, roughly half DC-REINVEST-001's original enterprise-scale Tier 5 figure. It restates (not
replaces) DC-REINVEST-001's Tier 2 TrafficMesh PoC costs and Tier 4 cloud-lab line unchanged, and adds
new items not in DC-REINVEST-001 at all: CML Personal Plus Cisco licensing (~$470/yr), a "maximum Pi
fleet" BOM (~$2,220-3,115), and DC-AGD sensing hardware (~$1,400-3,000) [§A-G, Grand Total].
**Verified finding: DC-REINVEST-001's Tier 0 protective spend and its own Tier 4 cloud-lab line have no
other copy anywhere in DC-REINVEST-002** — DC-REINVEST-002's own Grand Total table (Server / CML / Pi
fleet / TrafficMesh / DC-AGD / Homelab, one-time $6,730-11,165) omits Tier 0 and Tier 4 entirely, despite
its header's blanket "Supersedes Tier 5 deferral in DC-REINVEST-001" framing actually being accurate only
for Tier 5 specifically, not the whole document.

**DC-REINVEST-003 (incorporated):** restates DC-REINVEST-002's server, CML, Pi fleet, TrafficMesh,
DC-AGD, and homelab sections essentially unchanged, and adds substantial new scope not in either prior
document: an equipment-lease financing structure ($1 buyout, ~$425/mo over 36 months), a home-workstation
budget (laptop, monitors, desk/chair, VPN, UPS), office supplies, home-office rent treatment, and
insurance cost estimates cross-referenced to DC-CORP-FINANCE-001 [§1, §8-11]. **Verified finding:
DC-REINVEST-003's Grand Total Summary — which restates every DC-REINVEST-002 category line for line —
drops DC-REINVEST-002's cloud-lab line (AWS/Azure/GCP + fallback VM, §G in DC-REINVEST-002) entirely**,
despite DC-REINVEST-003's header claiming to supersede DC-REINVEST-002 in full.

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Original 6-tier plan, Tier 0-4 funded/gated items | DC-REINVEST-001, all tiers | incorporated |
| Tier 5 explicit deferral until SR&ED/IRAP funds land | DC-REINVEST-001, Tier 5 | incorporated — superseded-within-topic only for this specific line, see below |
| Right-sized server replacing Tier 5's enterprise estimate | DC-REINVEST-002 §A | incorporated (genuine, accurate supersession of Tier 5 specifically) |
| CML licensing, Pi fleet, DC-AGD sensing (new scope) | DC-REINVEST-002 §B-C, §E | incorporated (additive, not previously covered) |
| TrafficMesh full-track costs (restated from DC-REINVEST-001 Tier 2/Tier 5) | DC-REINVEST-002 §D | incorporated (consistent restatement) |
| Homelab/networking (restated, Proxmox line removed since covered by new server) | DC-REINVEST-002 §F | incorporated |
| Cloud lab spend (restated from DC-REINVEST-001 Tier 4) | DC-REINVEST-002 §G | incorporated — dropped in DC-REINVEST-003, see tension below |
| Equipment-lease financing structure | DC-REINVEST-003 §1 | incorporated (new) |
| Server/CML/Pi-fleet/TrafficMesh/DC-AGD/homelab (restated from DC-REINVEST-002) | DC-REINVEST-003 §2-7 | incorporated (consistent restatement) |
| Home workstation, office supplies, home-office rent, insurance | DC-REINVEST-003 §8-11 | incorporated (new scope) |

## Unresolved tensions

**None of the three documents' self-reported "supersedes" claims hold up as blanket statements when
verified against their own content — this was confirmed in a prior Stage 4 dedup pass and is restated
here rather than re-litigated.** Specifically:

1. DC-REINVEST-002 supersedes DC-REINVEST-001's Tier 5 accurately, but its own Grand Total silently
   omits DC-REINVEST-001's Tier 0 (protective spend, ~$100-200) and Tier 4 (cloud lab, ~$50-100/mo) —
   neither is restated nor explicitly retired. A reader relying only on DC-REINVEST-002 as "the current
   plan" would lose these two real budget line items.
2. DC-REINVEST-003 restates DC-REINVEST-002's categories but drops DC-REINVEST-002's cloud-lab line
   (§G) entirely, again without explicit removal or restatement, despite claiming full supersession.

Because discarding any one of the three documents on the strength of its own supersession claim would
silently lose real budget items (Tier 0 protective spend, the cloud-lab recurring cost), **all three are
retained as necessary reading together** rather than treated as a linear document history where only the
latest matters. This finding is carried forward unchanged from the Stage 4 dedup pass that first
established it.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/business-legal/conversation-artifacts/DC-REINVEST-001-Corporate-Procurement-Plan.md`
- `knowledge-base/d-central/business-legal/conversation-artifacts/DC-REINVEST-002-Full-Immediate-Buildout.md`
- `knowledge-base/d-central/business-legal/conversation-artifacts/DC-REINVEST-003-Master-Procurement-Plan.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/business-legal/conversation-artifacts/DC-REINVEST-001-Corporate-Procurement-Plan.md,
  knowledge-base/d-central/business-legal/conversation-artifacts/DC-REINVEST-002-Full-Immediate-Buildout.md,
  knowledge-base/d-central/business-legal/conversation-artifacts/DC-REINVEST-003-Master-Procurement-Plan.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the three source docs is marked superseded or moved — this was a deliberate Stage 4 decision
(each doc's own "supersedes" header claim was verified inaccurate as a blanket statement), and the
Consolidator does not have authority to alter that status assignment in any case (DC-DEDUP-STD-001's
authority, not this one's).


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

*No cross-references detected to/from other docs/*.md files.*

<!-- AUTO-GENERATED RELATED END -->
