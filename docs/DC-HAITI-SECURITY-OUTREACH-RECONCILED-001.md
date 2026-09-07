# DC-HAITI-SECURITY-OUTREACH-RECONCILED-001 — Haiti Open-Source Security Framework Outreach, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `haiti-security-framework-outreach` (2 docs).

## Current understanding

Both documents are companion pieces from the same outreach effort — an introduction from Bob Rae to
Mr. Côté-Fournier (Deputy Director, Haiti Division) proposing an open-source, cooperatively-owned
security framework for Haiti. Both open with the identical cover-letter paragraph. `security-email` is
the full, exhaustive version (5,100+ lines); `haiti-security-proposal` is a shorter, more polished
companion (roughly 500 lines) covering much of the same thesis with some independent framing detail.

**Core thesis (incorporated, consistent across both):** Haiti's security sector should shift from
foreign-dependent aid models (cited failure precedent: 1990s structural-adjustment programs that
destroyed Haitian rice farming; cited current parallel: the MSS Kenyan mission and foreign community-
policing aid reinforcing rather than reducing security dependence) to a dual cooperative-ownership +
open-source model, where the two elements are explicitly stated as interdependent — open source without
cooperative structure stays fragmented and under-resourced; cooperative structure without open source
lacks technical flexibility [security-email, Background and Original Vision; haiti-security-proposal,
Open-Source Institutional Security Framework].

**Detailed framework (incorporated, security-email — the fuller document):** an extensive "Sovereignty
Stack" covering physical assets (equipment ownership), local data processing/storage, software systems,
national federation of local cooperatives, and physical security for the digital infrastructure itself
[§Digital Infrastructure and Software Systems]; a token-based cooperative economic system with a
described technical architecture, liquidity/circulation mechanics, and an "economic flywheel" framing
[§Implementing the Token-Based Economic System]; and a 5-phase, 24-month implementation roadmap with
Kreyòl-named phases (Premye Defans/Emergency Foundation, Baz Solid/Sovereignty Establishment, Kapasite
Grandi/Capability Expansion, Inite ak Fòs/Federation Development, Souverènte Konplè/Comprehensive
Sovereignty) [§Comprehensive Implementation Roadmap]. Comparative international framing draws on the EU
Open Source Strategy/OSOR, Estonia's X-Road, France's BlueMind, and Spain's CONSUL as precedent for
government open-source adoption [§Europe's Open Source Governance Model].

**Practical mechanics (incorporated, haiti-security-proposal — the shorter companion, adding detail not
found in the excerpted portion of security-email):** a worked example of federated CCTV across a
neighborhood's NGO/business/church, contrasting current isolated-system weaknesses (incompatible
systems, no shared threat intelligence, single points of failure) against a proposed modular/open-
standards federated mesh [§Integrated Cooperative Security Systems in Practice]; a tiered participation
model for families/small organizations (resource-contributor vs. subscription-participant tiers)
[§Integrated Cooperative Security Systems in Practice]; an "Open Training Repository and Credentialing
Ledger" giving portable, blockchain-anchored security-personnel certifications across organizations
[§Integrated Cooperative Security Systems in Practice]; and an explicit proposal to legitimize and
professionalize existing community self-defense groups ("bwa kale") through the cooperative's training
and equipment access, rather than attempting to suppress them [§Integrated Cooperative Security Systems
in Practice].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Core cooperative + open-source interdependence thesis, structural-adjustment historical framing | security-email, Background and Original Vision; haiti-security-proposal, Open-Source Institutional Security Framework | incorporated (consistent across both) |
| EU open-source governance precedent (X-Road, BlueMind, CONSUL) | security-email, Europe's Open Source Governance Model | incorporated |
| Sovereignty Stack (physical assets, data, software, federation, physical security) | security-email, Digital Infrastructure and Software Systems | incorporated |
| Token-based cooperative economic system | security-email, Implementing the Token-Based Economic System | incorporated |
| 5-phase, 24-month Kreyòl-named implementation roadmap | security-email, Comprehensive Implementation Roadmap | incorporated |
| Federated CCTV worked example and current-system weaknesses | haiti-security-proposal, Integrated Cooperative Security Systems in Practice | incorporated |
| Tiered family/small-org participation model | haiti-security-proposal, Integrated Cooperative Security Systems in Practice | incorporated |
| Open Training Repository / portable blockchain credentialing | haiti-security-proposal, Integrated Cooperative Security Systems in Practice | incorporated |
| "Bwa kale" community self-defense group legitimization proposal | haiti-security-proposal, Integrated Cooperative Security Systems in Practice | incorporated |

## Unresolved tensions

None identified as a genuine conflict — both documents share the identical cover letter and core thesis,
and the shorter document's additional detail (worked examples, tiered participation, bwa kale
integration) reads as elaboration rather than contradiction. One structural oddity worth flagging as an
observation rather than a cross-document tension: `security-email`'s own internal structure contains
what appears to be a near-duplicate "Comprehensive Implementation Roadmap: Building Sovereign Security
Infrastructure" section heading twice (at two different points in the file, each followed by its own
set of Phase 1-5 subsections covering the same phase names and month ranges) — this looks like an
editing/drafting artifact within the single source file rather than two different roadmaps, but it was
not fully diffed line-by-line given the document's length; a future pass should verify whether the two
copies are identical or diverge.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/haiti-diaspora/Federated-Learning-Platform/security-email-md.md`
- `knowledge-base/d-central/haiti-diaspora/Haiti-open-framework/haiti-security-proposal-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/haiti-diaspora/Federated-Learning-Platform/security-email-md.md,
  knowledge-base/d-central/haiti-diaspora/Haiti-open-framework/haiti-security-proposal-md.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

Neither source doc is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

*No cross-references detected to/from other docs/*.md files.*

<!-- AUTO-GENERATED RELATED END -->
