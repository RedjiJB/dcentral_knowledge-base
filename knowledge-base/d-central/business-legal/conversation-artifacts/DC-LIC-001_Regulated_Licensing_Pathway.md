---
source_conversation_uuid: 702c2d45-c80d-429a-a545-2850a38a6543
conversation_title: 'Mobile SOC center setup options'
created_at: 2026-07-22T11:23:34.845895Z
doc_id: DC-LIC-001
description: 'DC-LIC-001: Regulated licensing pathway registry document'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-LIC-001 — Regulated Licensing Pathway & Regulated Entity Boundary

**Registry ID:** DC-LIC-001
**Status:** Design Complete — Execution Pending (blocked on Company Zero incorporation)
**Owner:** Redji Jean Baptiste (Toussaint), sole director and designated licence holder
**Supersedes:** None
**Related:** DC-VENTURE-001, DC-GOV-002, DC-MOGUL-001, DC-STATUS-001

---

## 1. Purpose

This document defines the pathway from individual licensure to a fully licensed Ontario security agency (OpenSecure), and establishes the Regulated Entity Pattern — the permanent boundary between DAO/cooperative governance and statutorily regulated operations. This pattern generalizes to all future regulated ventures in the D-Central ecosystem.

## 2. Current licensing position

The principal holds a valid Ontario security guard licence under the Private Security and Investigative Services Act, 2005 (PSISA), supported by approximately five years of professional physical security operations experience across enterprise environments. A private investigator licence is an available near-term addition, requiring completion of the approved PI training course and ministry test before application. Both individual licences are digital and must be carried on duty.

The individual licences alone are sufficient for the Phase 0–1 revenue wedge: subcontracting to existing licensed agencies as a licensed guard, and performing technical security-system installation work (OS-PACS), which is not licensable guarding activity under PSISA.

## 3. Agency (business entity) licence — trigger and sequence

The agency licence attaches to a corporation and is required only when OpenSecure begins selling guard or PI services directly to clients. Technical installation and NOC device-health monitoring do not trigger the requirement. The trigger point is the first direct guarding or investigation client, projected at Month 4–6 of the execution roadmap.

Sequence of steps, in order:

1. **Incorporate Company Zero** (federal). This is the prerequisite for everything below.
2. **Extra-provincial registration in Ontario.** PSISA requires a physical Ontario business address; a federal corporation must register in Ontario to operate there.
3. **Structure OpenSecure** as the operating subsidiary (or Company Zero operating as "OpenSecure" until a subsidiary is justified). The principal is sole director and designated accountable licence holder.
4. **Place insurance.** PSISA s.30 requires proof of prescribed insurance for a licence to sell guard or PI services; commercial general liability at the statutory minimum, with professional liability (E&O) added for the installation and monitoring lines as a client-facing and contractual necessity even where not statutorily required.
5. **Prepare the application package** to the Ministry of the Solicitor General, Private Security and Investigative Services Branch: proof of insurance, business plan, corporate documents, and background documentation for every officer and director of the entity.
6. **Submit and budget lead time.** Allow several weeks for processing and insurance placement ahead of the first direct-client contract date.
7. **Post-licensing compliance calendar.** A compliance inspector makes contact within 30 days of licence issue; a full compliance inspection occurs within six months; scheduled inspections recur every two years. Records must be maintained per the Recordkeeping Requirements for Licensed Business Entities regulation, retained a minimum of two years and longer if tied to any open matter. Uniform and vehicle identification regulations apply once guards are fielded under the agency's own brand.

Non-compliance exposure is personal as well as corporate: fines up to $250,000 for the corporation and potential imprisonment of directors and officers. This exposure is the legal foundation of the Regulated Entity Pattern below.

## 4. The Regulated Entity Pattern

Any activity with a statutory accountable human receives a conventional corporate wrapper with a named, licensed, personally liable principal. The DAO and cooperative layers may own the entity and govern capital allocation to it, but never govern its regulated operations.

The division of authority is as follows. The DAO layer decides whether to fund the venture, who the accountable principal is, and how surplus is allocated back into the vault system. The regulated wrapper decides everything operational: staffing, client engagements, compliance, incident response, and regulatory correspondence. The accountable principal answers to the regulator directly and cannot delegate that accountability to a vote.

Known regulated categories requiring this pattern in the current venture roadmap: security agencies (PSISA — designated licence holder), liquor-licensed venues (AGCO — personal responsibility of the licence holder), construction (licensed trades, WSIB registration, building permits), and any future financial-services activity. Alarm monitoring with dispatch capability adds a further layer: insurer acceptance generally requires ULC-listed central station service (CAN/ULC-S561), which is addressed by partnership rather than build in DC-VENTURE-001.

This pattern is consistent with the ecosystem's three refused departments (justice/enforcement, intelligence/surveillance, military/force): OpenSecure sells protection services under provincial law as a boring, inspectable agency. It is not, and can never become, an enforcement arm of the ecosystem.

## 5. Monitoring services — regulatory posture

The NOC tier (device health, uptime, storage, firmware) is unregulated managed-services work and may begin immediately upon first OS-PACS installs. Event triage and video verification remain in-house. Dispatchable alarm monitoring is delivered through partnership with an existing ULC-listed central station, with OpenSecure retaining the higher-margin NOC, analytics, and response-coordination layer. An in-house listed station is a Year 3+ consideration contingent on converged physical/cyber SOC volume, per DC-VENTURE-001 Phase 4.

## 6. Open items

The PI licence course and test have not been scheduled. Insurance broker selection has not begun. The compliance calendar automation belongs in the Company Zero agent cabinet (administration tier) once incorporation completes. All items are blocked behind incorporation, which remains the single highest-priority execution action per DC-STATUS-001.
