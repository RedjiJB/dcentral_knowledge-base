---
source_conversation_uuid: 702c2d45-c80d-429a-a545-2850a38a6543
conversation_title: 'Mobile SOC center setup options'
created_at: 2026-07-22T11:23:34.845895Z
doc_id: DC-TPL-000
description: 'DC-TPL-000: The Template Standard'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
topic: "dcentral-venture-governance-protocol-suite"
---

# DC-TPL-000 — The D-Central Venture Template Standard

**Registry ID:** DC-TPL-000
**Status:** Active Standard (governs all DC-TPL series documents)
**Owner:** Company Zero as Protocol Steward
**Related:** DC-MOGUL-001, DC-FRACTAL-001, DC-VENTURE-001, DC-GOV-002, DC-LIC-001, DC-LKB-001…003

---

## 1. Purpose

This standard defines the schema, lifecycle, changelog discipline, and validation criteria for all venture templates in the DC-TPL registry series. A template is the primary work product of the ecosystem's authorship workstream; a venture is an execution instance of a template in a given area. Templates make instance #002 cheaper and safer than instance #001, in perpetuity, for every cell in the fractal architecture (DC-FRACTAL-001).

## 2. Template schema (mandatory sections)

Every DC-TPL document contains the following twelve sections. A template missing any section cannot advance past Draft.

**2.1 Identity.** Template ID, version, lifecycle state, author, instance registry (list of all cells running this template with location and state).

**2.2 Business definition.** The service or product, customer, revenue model, and unit economics with honest ranges, updated from instance actuals at every version increment.

**2.3 Capital plan.** Total capital requirement, staging schedule with milestone gates, expected time to break-even, and loss-scenario bounds. Denominated for vault allocation per DC-GOV-002 §3.

**2.4 Regulatory checklist.** Every licence, registration, insurance, and inspection obligation, jurisdiction-tagged. Where any obligation names an accountable human, the Regulated Entity Pattern (DC-LIC-001 §4) is invoked and the DAO governance boundary is drawn explicitly in §2.8.

**2.5 Delegation ladder.** The operator progression (principal operates → supervisor → GM → DAO wrapper where applicable) with hiring triggers expressed as revenue or volume thresholds, and the GM compensation model (profit-share / equity earn-in structure).

**2.6 Vault hooks.** Contribution schedule to the operating reserve, expansion, community, and member-benefit vaults; royalty to the commons; repayment terms for vault-financed launches.

**2.7 Ecosystem rails.** How the instance consumes the shared infrastructure: DID/VC credentialing of staff, Lakou Protocol payment and payroll flows, agent-cabinet back-office services, OS-PACS/NOC monitoring of its physical site, procurement-first through ecosystem supply lines, and sensor/telemetry contribution to the mesh under Cooperative Transparency Stack rules.

**2.8 Governance configuration.** The DAO wrapper specification for community-facing operations (membership classes, voting scope, assembly cadence) and the explicit exclusion zone for regulated operations. The three refused departments apply within every template without exception.

**2.9 Infrastructure hooks.** Which D-Central hardware and services deploy in the instance's site (SHI-class nodes, mesh coverage, sensing planes per DC-PLANE-001) and at which phase of the instance's maturity.

**2.10 Operating playbook.** The day-one through day-365 operational sequence: site selection criteria, launch checklist, staffing ratios, pricing guidance, and the known failure modes with countermeasures.

**2.11 Sporing criteria.** The conditions under which this instance may seed a new cell per DC-FRACTAL-001 §4: profitability duration, vault reserve level, trained-operator availability, and template state (Validated or better).

**2.12 Changelog.** Append-only, per §4 below.

## 3. Lifecycle states

**Draft.** Authored but never operated. A Draft may be revised freely by the steward. No vault capital may be allocated against a Draft template except to the reference instance operated by the template's author.

**Validated.** At least one instance has reached sustained profitability (minimum two consecutive quarters of positive operating income with vault contributions current). Validation is granted by vault governance vote on published CTS metrics, not by the author's declaration.

**Proven.** At least one additional instance, launched and operated by someone other than the original author, has independently reached the Validated criteria. Only Proven templates are offered to external Stewards in the DC-MOGUL-001 Principal Track without a co-operating mentor arrangement.

**Deprecated.** Superseded by a newer template or retired by governance vote. Running instances continue under their launch version with a migration path documented.

Advancement is one-way except by governance vote. The core rule of the standard: **no template advances past Draft by writing; only by operating.**

## 4. Changelog discipline

Every operational lesson is a template patch, not merely a business fix. When an instance encounters a permit surprise, a staffing-ratio correction, an insurance exclusion, a pricing error, or any material deviation from the playbook, the operating cell files a patch entry: date, instance, section affected, the lesson, and the revision. Patches merge upstream at version increments so that all cells inherit — the capability-inheritance mechanic of DC-SWARM-001 applied to business operations. A cell that withholds material patches is in breach of its template licence and its vault standing.

## 5. Versioning

Semantic versioning: major (schema-breaking or capital-plan restructure), minor (playbook and checklist revisions), patch (corrections). Instances record their launch version; the delta between launch version and current version is reviewed at each quarterly assembly.

## 6. Authorship economics

Template authors (initially the founder; eventually any Principal contributing per DC-MOGUL-001 §3 Stage 4) are credited in the template identity block. The commons royalty defined in each template's §2.6 sustains the registry, shared services, and transparency infrastructure — it does not flow to the author personally. Author compensation is reputational (DID/VC-recorded authorship) and indirect (the author's own instances benefit from every upstream patch).

## 7. Guard rail

Template authorship is the lowest-cost, highest-comfort activity in the ecosystem and therefore its most dangerous failure mode per DC-STATUS-001. The standing ratio during DC-VENTURE-001 Phases 0–1 is 80% execution, 20% authorship. The gate for the entire DC-TPL series remains unchanged: Company Zero incorporation and the first paid invoice.
