# DC-VENTURE-GOVERNANCE-PROTOCOL-SUITE-RECONCILED-001 — D-Central Venture & Governance Protocol Suite, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `dcentral-venture-governance-protocol-suite` (5 docs).

## Current understanding

Five tightly interlocking protocol documents defining D-Central's non-technology venture layer: how a
single business (Track 1, Security-Trades Spine) sequences into a conglomerate, how that conglomerate
governs itself, how the founder's path generalizes into a replicable "Principal Track" for others, how
individual venture types are templated for replication, and how templates compose recursively into a
"fractal" of cells/clusters/regions. Two documents (DC-GOV-002, DC-MOGUL-001) explicitly declare a
partial mutual supersession in their own front matter — this is documented evolution, not an
unreconciled conflict, and both remain in force per their own stated terms.

**DC-VENTURE-001 — Venture Sequencing Registry (incorporated):** the reference implementation ("Track
1") sequencing the founder's actual venture portfolio through 5 phases (0: OpenSecure-only foundation
through April 2027; 1: security-construction spine 2027-2029; 2: gym as first cooperative cell
2029-2031; 3: social hub 2031-2034; 4: property layer 2032+), gated by three tests every venture must
pass (funded by an existing business; vertically or horizontally integrated with one; hosts D-Central
infrastructure) [§1-3]. A deliberately late SHI-node insertion timeline (spec-only through month 6,
commercial-form field validation at month 9-12, first residential node in Year 2) explicitly reasoning
that "OS-PACS clients are the landing sites for SHI hardware" rather than a standing consumer launch
[§4]. Five named emergent (not founded, grown) ventures graduating from operational volume [§5], and a
delegation ladder (principal → supervisor → GM → DAO wrapper for community-facing ventures only,
regulated ventures stopping at GM) that recurs as the shared mechanism across all five documents [§6].

**DC-GOV-002 — Conglomerate Governance & Capital Allocation Architecture (incorporated):** the
4-layer governance structure the conglomerate grows into — Company Zero (holding/family office, IP
owner) → operating subsidiaries (hired GMs, Regulated Entity Pattern applied permanently to OpenSecure)
→ DAO/co-op wrapper (community-facing ventures only, e.g. the gym) → Lakou Protocol vault system as
internal capital-allocation machinery [§2]. A fixed capital-allocation cycle (proposal → diligence
package → vault vote → milestone-gated release → repayment as vault contribution) [§3]. A principal
time-model at maturity (weekly exception dashboard, monthly GM reviews, quarterly vault/DAO
governance, annual strategy) paired with a list of duties that remain non-delegable regardless of
scale (statutory licence-holder duties, director/officer liability, primary banking, vision/registry
authorship) [§4]. Explicitly frames this as an end-state that "activates over years, not at launch,"
requiring 3-4 years of founder day-to-day operation first [§5]. Its front matter notes it is
"superseded in part by DC-MOGUL-001" on the framing of the principal as sole conglomerate owner — the
mechanics themselves remain in force.

**DC-MOGUL-001 — The Principal Track Protocol (incorporated):** generalizes the founder's path into a
replicable ladder open to others, reframing DC-GOV-002's founder-as-sole-owner into "first principal
and protocol author" [Executive Summary]. Venture templates aggregate into "Spines" (proven mutually-
funding venture sequences); Track 1 (Security-Trades) is the reference, with future spines (Hospitality,
Logistics) to be authored by other principals [§2]. A 4-stage Principal Track (Member → Operator →
Steward → Principal), advancement granted by vault-governance vote on published metrics rather than
founder discretion [§3]. The expansion vault generalizes into a venture-studio fund with an explicit,
non-negotiable risk architecture (loss reserve sized to expected failure rate, portfolio-logic
allocation, staged capital so a failing venture loses its next tranche not the vault's principal) and
an explicit disclosure that "the protocol promises access to the ladder, never moguldom" [§4]. The
Regulated Entity Pattern is generalized as a first-class protocol pattern applied by every spine [§5].
Activation gates require Track 1 to prove one profitable regulated venture, one profitable DAO-wrapped
community venture, and one completed vault-financed capital cycle before admitting external stewards
[§7] — directly implementing DC-VENTURE-001's own phase sequence as the proof requirement.

**DC-TPL-000 — The Template Standard (incorporated):** the schema, lifecycle, and changelog discipline
governing every venture template referenced by the other four documents. A mandatory 12-section
template schema (identity, business definition, capital plan, regulatory checklist, delegation ladder,
vault hooks, ecosystem rails, governance configuration, infrastructure hooks, operating playbook,
sporing criteria, changelog) [§2]. Four lifecycle states — Draft, Validated (≥1 instance, 2 consecutive
profitable quarters, vault-vote-certified), Proven (a second, independently-operated instance
independently reaches Validated), Deprecated — with the core rule "no template advances past Draft by
writing; only by operating" [§3]. A changelog-patch discipline making every operational lesson a
versioned template patch that merges upstream so all cells inherit it, explicitly named as "the
capability-inheritance mechanic of DC-SWARM-001 applied to business operations" [§4]. Author
compensation is reputational/indirect only — the commons royalty does not flow to the author personally
[§6]. A guard-rail section explicitly warning that template authorship is "the lowest-cost, highest-
comfort activity in the ecosystem and therefore its most dangerous failure mode," fixing an 80/20
execution-to-authorship ratio during Phases 0-1 [§7].

**DC-FRACTAL-001 — Fractal Cell Architecture (incorporated):** the recursive structure by which
DC-TPL-000 templates compose into a franchise-cooperative hybrid across four layers (venture cell →
local cluster → regional assembly → ecosystem commons), each layer's assembly composed of delegates
from the layer below and funded by scheduled contributions from that layer [§2-3]. A defined "sporing
protocol" (eligibility → proposal → milestone-gated capital allocation → launch with parent-cell
mentorship → template-patch inheritance → independence) directly implementing DC-TPL-000's sporing-
criteria section and DC-GOV-002's capital-allocation cycle [§4]. Explicitly frames what is kept from
franchising (standardization, brand/quality enforcement, royalty) versus what is corrected (member
ownership, bidirectional template improvement, graduation instead of buyout as the exit path) [§6]. A
self-critical validation gate: the document declares itself "structurally validated only when N=2" —
the first spore, launched and operated by someone other than the founder, independently reaching
Validated criteria — and until then explicitly states "this document is design" [§7].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Three-tests gate and 5-phase venture sequence | DC-VENTURE-001 §1-3 | incorporated |
| SHI node insertion timeline | DC-VENTURE-001 §4 | incorporated |
| Emergent ventures and shared delegation ladder | DC-VENTURE-001 §5-6 | incorporated (delegation ladder recurs identically in DC-GOV-002, DC-MOGUL-001, DC-TPL-000, DC-FRACTAL-001) |
| 4-layer conglomerate governance structure | DC-GOV-002 §2 | incorporated — note stated partial supersession by DC-MOGUL-001 (framing only, mechanics unchanged) |
| Capital allocation cycle | DC-GOV-002 §3 | incorporated (directly implemented by DC-FRACTAL-001 §4's sporing protocol) |
| Principal time model and non-delegable duties | DC-GOV-002 §4-5 | incorporated |
| Principal Track ladder (Member→Operator→Steward→Principal) | DC-MOGUL-001 §2-3 | incorporated |
| Venture studio vault and risk architecture | DC-MOGUL-001 §4 | incorporated |
| Regulated Entity Pattern generalization | DC-MOGUL-001 §5 | incorporated (consistent with DC-GOV-002's OpenSecure application and DC-TPL-000 §2.4/§2.8's schema treatment) |
| Activation gates for external stewards | DC-MOGUL-001 §7 | incorporated (directly requires DC-VENTURE-001's own phase-sequence proof points) |
| 12-section mandatory template schema | DC-TPL-000 §2 | incorporated |
| Lifecycle states and "no advancement by writing" rule | DC-TPL-000 §3 | incorporated (Validated/Proven definitions directly referenced by DC-MOGUL-001 §7 and DC-FRACTAL-001 §7) |
| Changelog/patch discipline | DC-TPL-000 §4 | incorporated |
| Authorship economics and guard-rail warning | DC-TPL-000 §6-7 | incorporated |
| Cell anatomy and four-layer recursion | DC-FRACTAL-001 §2-3 | incorporated |
| Sporing protocol | DC-FRACTAL-001 §4 | incorporated |
| Franchise-vs-cooperative corrections | DC-FRACTAL-001 §6 | incorporated |
| Self-declared N=2 validation gate | DC-FRACTAL-001 §7 | incorporated |

## Unresolved tensions

None identified in this pass — the two documents that flag their own partial mutual supersession
(DC-GOV-002 and DC-MOGUL-001) do so explicitly and consistently: DC-MOGUL-001 reframes the founder from
sole conglomerate owner to first principal, while stating plainly that "all DC-GOV-002 mechanics remain
in force," and DC-GOV-002's own front matter concurs. This is a source-stated, reconciled evolution, not
a genuine unresolved conflict. All five documents' shared mechanisms (the delegation ladder, the
Regulated Entity Pattern, the vault capital-allocation cycle, and the Validated/Proven template
lifecycle states) are defined once and referenced identically everywhere they recur.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/core/governance/conversation-artifacts/DC-FRACTAL-001_Fractal_Cell_Architecture.md`
- `knowledge-base/d-central/core/governance/conversation-artifacts/DC-GOV-002_Conglomerate_Governance_Architecture.md`
- `knowledge-base/d-central/core/governance/conversation-artifacts/DC-MOGUL-001_Principal_Track_Protocol.md`
- `knowledge-base/d-central/core/governance/conversation-artifacts/DC-TPL-000_Template_Standard.md`
- `knowledge-base/d-central/core/governance/conversation-artifacts/DC-VENTURE-001_Venture_Sequencing_Registry.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/core/governance/conversation-artifacts/DC-FRACTAL-001_Fractal_Cell_Architecture.md,
  knowledge-base/d-central/core/governance/conversation-artifacts/DC-GOV-002_Conglomerate_Governance_Architecture.md,
  knowledge-base/d-central/core/governance/conversation-artifacts/DC-MOGUL-001_Principal_Track_Protocol.md,
  knowledge-base/d-central/core/governance/conversation-artifacts/DC-TPL-000_Template_Standard.md,
  knowledge-base/d-central/core/governance/conversation-artifacts/DC-VENTURE-001_Venture_Sequencing_Registry.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator. (The partial-supersession relationship between DC-GOV-002 and DC-MOGUL-001 is stated by the source documents themselves, not asserted by this consolidation.)
