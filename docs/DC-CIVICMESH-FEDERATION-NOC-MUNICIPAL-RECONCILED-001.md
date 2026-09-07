# DC-CIVICMESH-FEDERATION-NOC-MUNICIPAL-RECONCILED-001 — CivicMesh Federation, NOC & Municipal Deployment, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `civicmesh-federation-noc-municipal-deployment` (5 docs).

## Current understanding

Five documents spanning the full stack of CivicMesh's upward data-federation model: the general
federation protocol, the municipal legal agreement template, the MeshPlate-specific federation variant
(already fully detailed in a sibling consolidation), the NOC/community-manager dashboard spec, and a
municipal (Ottawa) go-to-market deployment package. All five are consistent — the same layered-consent
federation model, the same revenue-share structure, and the same transparency/audit mechanisms recur
across every document.

**CivicMesh Federation Protocol (incorporated):** a 5-layer federation hierarchy (Node → Community →
Municipal → Regional → Provincial/Federal), each layer requiring progressively stronger consent (from
none, at Node, up to a court order at Provincial/Federal) [§1]. Standard Layer-1→2 federation is
automatic for evidence packages meeting four criteria (confidence ≥0.70, in-scope violation type, an
active Municipal Data Federation Agreement, public-road origin) and is logged in aggregate without
individual notification [§2]. Federation above Layer 2 follows a 7-step investigation-specific
protocol classifying legal authority (WARRANT/EXIGENT auto-approve, REASONABLE_GROUNDS gets MSSP legal
review, ROUTINE auto-approves within standard scope), with immutable audit logging, 24-hour community
notification, and automatic post-case purge [§3]. A named SR&ED technical challenge — atomically
coupling the audit-log write and the community-notification dispatch — documents two rejected designs
(two-phase commit; log-then-notify) before settling on a transactional approach with async retry, and
flags an open scalability question at 1,000+ concurrent requests [§4]. Public transparency
infrastructure is explicitly framed as a "DeFlock countermeasure" designed to prevent the community-
relationship failure that damaged Flock Safety [§5].

**Municipal Data Federation Agreement (incorporated):** the legal template implementing the Federation
Protocol's Layer-2 mechanics — framed explicitly as "not a surveillance contract" but a data-federation
agreement where the municipality is a data recipient, not an owner [Executive Summary]. Defines what
federates automatically (validated evidence packages, aggregate digital-twin data, infrastructure
defect alerts) versus what requires a specific request (raw video, civilian identities, acoustic clips)
[§1]. A revenue-share table by citation source: city fleet nodes 60-70%/20-25%/10-15%
(municipality/platform/CCSC), civilian opt-in nodes 50%/20%/30% (higher community share to incentivize
participation), contractor nodes 65%/25%/10%, digital-twin subscriptions 20%/60%/20% [§2]. The same
7-step investigation protocol as the Federation Protocol document, restated with MFIPPA-specific
compliance obligations (municipality is the MFIPPA institution, 2-year evidence retention, 90-day
default for other federated data, named prohibited uses including no immigration-authority sharing
without a court order) [§3-4].

**MeshPlate Federation Protocol (incorporated by reference):** this document's full content — automatic
vs. investigation-specific LPR federation, the hash-based cross-community query mechanism, and the
no-data-broker covenant — is already fully detailed in the sibling consolidation
[DC-MESHPLATE-PRIVACY-COMPLIANCE-RECONCILED-001](DC-MESHPLATE-PRIVACY-COMPLIANCE-RECONCILED-001.md).
Its layered-consent structure and the general Federation Protocol document's Layer-2 mechanics are
consistent — both require a warrant for historical cross-community/investigation-specific queries and
both mandate post-case purge and community notification.

**NOC / Community Dashboard Specification (incorporated):** functional requirements for two dashboard
views sharing one data model under different credential-scoped filters. The MSSP NOC view covers fleet
health, a geographic node map, evidence-pipeline health, a chain-of-custody failure monitor, a
federation-request review queue (flagging anything queued >4 hours), an SLA compliance dashboard, and a
one-click annual transparency report generator pre-filled from the audit log [§1]. The community
manager view covers a community-scoped node map, an incident review queue, a revenue dashboard, member
management, and — directly relevant to this topic — a **Law Enforcement Request Log** showing every
federation request affecting that community (date, type, legal authority, status, notification sent),
matching the Federation Protocol's community-notification requirement exactly [§2]. Multi-tenant
isolation (per-community PostgreSQL schema), Kafka/SSE push-based real-time updates, and an immutable,
self-auditable NOC action log close the spec [§3].

**MeshPlate Municipal Deployment Package (incorporated):** an Ottawa-specific go-to-market package
applying the general federation model to a named municipal customer (City of Ottawa, Ottawa Police
Service, Ottawa Parking Authority) — a four-department value proposition table with dollar estimates
[§1], the same hash-before-store/no-national-database/annual-transparency-reporting architecture as the
sibling MeshPlate consolidation, explicitly extended with an Ottawa Information and Privacy Commissioner
reporting channel [§2]. A police-integration protocol (OfficerAuthorizationCredential issuance, an
Amber Alert fast-path pushing a plate hash to all active fleet nodes, and the standard warrant-gated
investigation query for routine cases) consistent with the general Federation Protocol's WARRANT/
EXIGENT auto-approval classification [§3]. A city-council presentation framework contrasting MeshPlate
Ottawa against Flock Safety on data ownership, national-database absence, and revenue-sharing grounds
[§4].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| 5-layer federation hierarchy and consent model | Federation Protocol §1 | incorporated |
| Standard automatic federation criteria | Federation Protocol §2 | incorporated (consistent with Municipal Data Federation Agreement §1's federated/non-federated data list) |
| Investigation-specific 7-step protocol | Federation Protocol §3 | incorporated (restated consistently in Municipal Data Federation Agreement §3 and MeshPlate Municipal Deployment Package §3) |
| Consent-gate atomicity design and SR&ED history | Federation Protocol §4 | incorporated |
| Public transparency / "DeFlock countermeasure" framing | Federation Protocol §5 | incorporated |
| Federation scope and revenue-share table by citation source | Municipal Data Federation Agreement §1-2 | incorporated |
| MFIPPA obligations, retention, prohibited uses, breach notification | Municipal Data Federation Agreement §4 | incorporated |
| Transparency obligations (public log, annual report, community notification) | Municipal Data Federation Agreement §5 | incorporated (consistent with Federation Protocol §5) |
| MeshPlate-specific federation mechanics (hash queries, no-data-broker covenant) | MeshPlate Federation Protocol | incorporated by reference — fully detailed in [DC-MESHPLATE-PRIVACY-COMPLIANCE-RECONCILED-001](DC-MESHPLATE-PRIVACY-COMPLIANCE-RECONCILED-001.md) |
| MSSP NOC dashboard functional requirements | NOC Dashboard Spec §1 | incorporated |
| Community manager dashboard, including Law Enforcement Request Log | NOC Dashboard Spec §2 | incorporated (matches Federation Protocol's community-notification requirement) |
| Multi-tenant data architecture | NOC Dashboard Spec §3 | incorporated |
| Ottawa municipal value proposition and department-level estimates | Municipal Deployment Package §1 | incorporated |
| Ottawa-specific privacy architecture (IPC reporting) | Municipal Deployment Package §2 | incorporated (extends the general MeshPlate privacy architecture with a named oversight body) |
| Police integration protocol (credentials, Amber Alert fast-path) | Municipal Deployment Package §3 | incorporated (consistent with Federation Protocol's WARRANT/EXIGENT classification) |
| City council presentation framework | Municipal Deployment Package §4 | incorporated |

## Unresolved tensions

None identified in this pass — the five documents describe one consistent, layered federation model at
increasing levels of legal, technical, and go-to-market detail, and every revenue-share figure, consent
requirement, and notification timeline that appears in more than one document matches across all of
them.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/business-legal/CivicMesh/DEPLOY-MP-001-MeshPlate-Municipal-Deployment-Package-v1-docx.md`
- `knowledge-base/d-central/business-legal/CivicMesh/LEGAL-CM-011-Municipal-Data-Federation-Agreement-v1-docx.md`
- `knowledge-base/d-central/core/governance/CivicMesh/DC-CM-FED-001-CivicMesh-Federation-Protocol-v1-docx.md`
- `knowledge-base/d-central/core/observability/CivicMesh/DC-CM-NOC-001-NOC-Dashboard-Specification-v1-docx.md`
- `knowledge-base/d-central/security/CivicMesh/DC-MP-FED-001-MeshPlate-Federation-Protocol-v1-docx.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/business-legal/CivicMesh/DEPLOY-MP-001-MeshPlate-Municipal-Deployment-Package-v1-docx.md,
  knowledge-base/d-central/business-legal/CivicMesh/LEGAL-CM-011-Municipal-Data-Federation-Agreement-v1-docx.md,
  knowledge-base/d-central/core/governance/CivicMesh/DC-CM-FED-001-CivicMesh-Federation-Protocol-v1-docx.md,
  knowledge-base/d-central/core/observability/CivicMesh/DC-CM-NOC-001-NOC-Dashboard-Specification-v1-docx.md,
  knowledge-base/d-central/security/CivicMesh/DC-MP-FED-001-MeshPlate-Federation-Protocol-v1-docx.md,
]
reconciled_against: [DC-MESHPLATE-PRIVACY-COMPLIANCE-RECONCILED-001.md (sibling consolidation covering DC-MP-FED-001 in full detail)]
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

**References:**
- [[DC-MESHPLATE-PRIVACY-COMPLIANCE-RECONCILED-001|DC-MESHPLATE-PRIVACY-COMPLIANCE-RECONCILED-001 — MeshPlate Federation & CivicMesh Privacy Compliance, Consolidated (v1, generated 2026-09-05)]]

<!-- AUTO-GENERATED RELATED END -->
