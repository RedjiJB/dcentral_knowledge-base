# DC-OPENSECURE-PROVINCIAL-PIV-CREDENTIAL-RECONCILED-001 — OpenSecure Provincial Security Network: PIV & Credentialing, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `opensecure-provincial-security-network` (6 docs).

## Current understanding

Four of this topic's six member documents — Provincial Autonomous Security Systems Network (PASSN),
Provincial Body Camera Evidence Network (PBCEN), Provincial Security Vehicle Network (PSVN-Fleet), and
Provincial Security Video Network (PSVN) — are the same source files already fully consolidated in
[DC-PROVINCIAL-SECURITY-NETWORK-RECONCILED-001](DC-PROVINCIAL-SECURITY-NETWORK-RECONCILED-001.md) under
topic `provincial-security-network-programs`. Per DC-CONSOLIDATOR-STD-001's sibling-consolidation
pattern, their content is not re-detailed here — see that document for the full three-tier federation
architecture, data-flow scenarios, cost economics, and implementation roadmaps for each of those four
programs. This document covers only the two new members: a province-wide PIV (Personal Identity
Verification) infrastructure spec that ties all seven OpenSecure provincial pillars together under one
credential, and a security-guard-specific credentialing system that is a more narrowly-scoped, partially
overlapping proposal for the same underlying problem.

**Provincial PIV Infrastructure Integration (incorporated):** a unified, FIPS 201-3-compliant PIV
credential infrastructure intended to serve as the trust anchor across all seven provincial OpenSecure
pillars (PSVN, PBCEN, PSVN-Fleet, PASSN, PXRSN, PISN, PSRFIP) — replacing the fragmented "5+ credentials
per person" status quo with one PIV card providing building access (via OS-PACS/Leosac), video-system
login, body-camera tap-to-activate, vehicle assignment, drone authorization, AR-glasses pairing, and
military-mobilization credentials [Executive Summary, Integration with Seven Provincial Pillars]. A
three-component PKI architecture (an offline HSM-protected Root CA, an online HA-clustered Issuing CA
with OCSP/CRL revocation publishing, and Registration Authority enrollment stations), detailed PIV card
hardware specs (Infineon SLE78 secure microcontroller, FIPS 201-3 mandatory/optional data objects,
physical anti-counterfeiting features), and a reader-infrastructure taxonomy spanning desktop/wall-
mounted, mobile/handheld, vehicle-integrated, and specialized (body-camera, drone, AR-glasses) reader
types with province-wide quantity estimates [PIV Infrastructure Architecture]. Worked integration flows
for each of the seven pillars — including a `Leosac` access-policy configuration for OS-PACS, a JWT-based
authorization-token scheme for PSVN camera access, and a tap-to-activate/tap-to-upload chain-of-custody
flow for PBCEN body cameras [Integration with Seven Provincial Pillars §1-4]. A full PIV lifecycle
(enrollment/background-check/issuance, renewal with online and in-person paths, revocation with
immediate and pending-investigation trigger categories, and lost/stolen card recovery), a cryptographic-
standards section (RSA/ECC/AES/SHA-2 algorithm profiles per FIPS 201-3), and its own deployment roadmap
and cost analysis.

**Provincial Security Guard Universal Credential System (incorporated):** a narrower-scoped proposal
("SecureGuard Provincial Identity System," SGPIS) addressing specifically the security-guard credential-
fragmentation problem — guards currently carrying multiple company-specific badges with no province-wide
standardization or interoperability [Executive Summary, Problem Being Solved]. A three-tier federation
model (Ministry of Public Safety as provincial trust anchor operating a Dogtag-CA-based root PKI and a
PostgreSQL Security Guard Registry; security companies as Tier 2 employers who grant/revoke site access
through a company portal; client sites as Tier 3 enforcement points via OS-PACS) [System Architecture].
A full OpenAPI 3.0 specification for guard-verification, employment-registration, ministry-only
revocation, and certificate-validation endpoints, plus a worked company-side PostgreSQL schema
(`guards`, `sites`, `guard_site_access`, `ministry_sync_log` tables) [Technical Implementation]. Five
worked data-flow scenarios (certification/issuance, employment/site assignment, daily access operations,
multi-site guard scenarios, and revocation scenarios), a governance section splitting Ministry/security-
company/guard responsibilities, a detailed cost model (Ministry one-time setup $1,025,000, annual
operating $355,000 funded by $50/year/guard fees; per-company setup and annual costs claimed 44-53%
cheaper than proprietary alternatives), a data-classification/threat-model privacy section, and a
standards-compliance table (FIPS 201, NIST SP 800-73, ISO 27001, OpenID Connect, OAuth 2.0, GDPR/PIPEDA)
naming the specific open-source components used (OpenPIV, Leosac, Dogtag PKI, OpenSC).

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Autonomous drone/robot fleet federation, UTM, data-flow scenarios, cost economics | Provincial Autonomous Security Systems Network (PASSN) | referenced — fully detailed in [DC-PROVINCIAL-SECURITY-NETWORK-RECONCILED-001](DC-PROVINCIAL-SECURITY-NETWORK-RECONCILED-001.md) |
| Body-camera evidence hub, blockchain chain-of-custody, legal/regulatory framework | Provincial Body Camera Evidence Network (PBCEN) | referenced — fully detailed in the sibling document above |
| Patrol-vehicle federation, LPR privacy, cost economics | Provincial Security Vehicle Network (PSVN-Fleet) | referenced — fully detailed in the sibling document above |
| Fixed-camera video federation, AI federated-learning training, governance/policy | Provincial Security Video Network (PSVN) | referenced — fully detailed in the sibling document above |
| Provincial PIV PKI architecture, card hardware, reader taxonomy | Provincial PIV Infrastructure Integration, PIV Infrastructure Architecture | incorporated |
| Seven-pillar integration flows (OS-PACS, PSVN, PBCEN, PSVN-Fleet, PASSN, PISN, PXRSN, PSRFIP) | Provincial PIV Infrastructure Integration, Integration with Seven Provincial Pillars | incorporated |
| PIV lifecycle management, cryptographic standards, deployment roadmap, cost analysis | Provincial PIV Infrastructure Integration, remaining sections | incorporated |
| SGPIS three-tier guard-credential federation, Ministry PKI (Dogtag), APIs, database schema | Provincial Security Guard Universal Credential System, Executive Summary through Technical Implementation | incorporated |
| SGPIS data-flow scenarios, governance, cost model, privacy/threat model, standards compliance, roadmap | Provincial Security Guard Universal Credential System, remaining sections | incorporated |

## Unresolved tensions

**The two new documents propose two independently-authored, only partially reconcilable PIV/PKI
architectures for what is substantially the same underlying problem (province-wide security-credential
issuance), and neither cross-references the other.** The PIV Infrastructure Integration document
describes a generic, vendor-named (Thales Luna HSM) Root/Issuing CA architecture intended to serve all
seven provincial pillars as a shared trust anchor. The Security Guard Universal Credential System
document independently specifies a Ministry PKI built specifically on Dogtag Certificate Authority for
guard credentials alone, with its own separate cost structure ($1,025,000 Ministry setup / $355,000
annual operating, funded by $50/year/guard fees) that is not stated as a subset or superset of the PIV
Infrastructure Integration document's own cost analysis. Because the two documents scope their PKI
proposals differently (universal seven-pillar infrastructure vs. guard-specific credentialing) rather
than making directly comparable claims about the same system, this is not treated as a numeric
contradiction requiring reconciliation — but a reader implementing either proposal should be aware a
single province would need to decide whether guard credentials ride on the universal PIV Infrastructure
Integration CA or on SGPIS's own separate Dogtag-based CA, since the source documents themselves never
resolve which one is authoritative.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/core/identity/Open-Secure/Provincial-PIV-Infrastructure-Integration-md.md`
- `knowledge-base/d-central/core/identity/Open-Secure/Provincial-Security-Guard-Universal-Credential-System-md.md`
- `knowledge-base/d-central/security/Open-Secure/Provincial-Autonomous-Security-Systems-Network-md.md`
- `knowledge-base/d-central/security/Open-Secure/Provincial-Body-Camera-Evidence-Network-md.md`
- `knowledge-base/d-central/security/Open-Secure/Provincial-Security-Vehicle-Network-md.md`
- `knowledge-base/d-central/security/Open-Secure/Provincial-Security-Video-Network-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/core/identity/Open-Secure/Provincial-PIV-Infrastructure-Integration-md.md,
  knowledge-base/d-central/core/identity/Open-Secure/Provincial-Security-Guard-Universal-Credential-System-md.md,
  knowledge-base/d-central/security/Open-Secure/Provincial-Autonomous-Security-Systems-Network-md.md,
  knowledge-base/d-central/security/Open-Secure/Provincial-Body-Camera-Evidence-Network-md.md,
  knowledge-base/d-central/security/Open-Secure/Provincial-Security-Vehicle-Network-md.md,
  knowledge-base/d-central/security/Open-Secure/Provincial-Security-Video-Network-md.md,
]
reconciled_against: [
  docs/DC-PROVINCIAL-SECURITY-NETWORK-RECONCILED-001.md,
]
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
