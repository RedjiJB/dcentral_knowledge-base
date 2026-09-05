# DC-OPENPIV-PACS-INTEGRATION-RECONCILED-001 — OpenPIV + OS-PACS Integration Suite, Consolidated (v1, generated 2026-09-05)

Per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), topic `openpiv-pacs-integration-suite` (4 docs).

## Current understanding

Four documents building a single integration story at different scales: a hands-on one-day Quick Start
Guide for a single test PIV card, a 60-week implementation roadmap for OpenPIV alone, a field
deployment checklist combining OpenPIV with OS-PACS for a 50-door/500-user facility, and a technical
integration guide detailing exactly how the two systems connect.

**OpenPIV Quick Start Guide (incorporated):** a one-day (4-8 hour), ~$100-budget path to a single
working PIV card authenticating a Linux login — an hour-by-hour timeline covering PC/SC environment
setup, OpenFIPS201 applet build-and-load via GlobalPlatformPro, and a quick Dogtag CA deployment with
a sample PIV Authentication certificate profile [Shopping List, Day 1 Timeline]. This is the same
toolchain (OpenFIPS201, GlobalPlatformPro, Dogtag, piv-tool/OpenSC) the Implementation Roadmap's
Phase 1 sprints describe at much greater length — the Quick Start Guide is a condensed, single-card
version of that same Sprint 1.1-1.3 sequence, using identical hardware recommendations (NXP JCOP3
J3H145 cards, ACR38U-I1 or Identiv SCR3500 readers) and troubleshooting guidance.

**OpenPIV Implementation Roadmap (incorporated):** a 5-phase, 60-week sprint plan building OpenPIV
standalone (no OS-PACS integration yet) — Phase 1 Foundation (weeks 1-12: dev environment, Dogtag PKI,
OpenFIPS201 smart-card programming, Linux/SSH client middleware), Phase 2 Enrollment System (weeks
13-24: PostgreSQL schema, FastAPI backend, React enrollment portal, biometric processing, IAL-1/2/3
identity-proofing levels), Phase 3 Physical Access Control (weeks 25-36: Leosac deployment, OSDP
reader hardware, door-control wiring, access-policy engine, monitoring), Phase 4 Windows/macOS
Integration (weeks 37-48), and Phase 5 Hardening & Production (weeks 49-60: security audit, FIPS 201
gap analysis, CA redundancy, load testing, go-live) [Phases 1-5]. Named success criteria include
certificate issuance <15 minutes, authentication latency <2 seconds, and 99.5% uptime [Success
Criteria Checklist].

**OpenPIV + OS-PACS Deployment Checklist (incorporated):** a concrete field-deployment guide for a
50-door/500-user facility, structured as a 5-week installation timeline (week 1 infrastructure setup,
weeks 2-3 door-by-door hardware installation, week 4 system integration/testing, week 5 mass
enrollment and go-live) [Installation Timeline]. A detailed hardware BOM: OpenPIV equipment ($8,320
one-time, $750/year recurring for cards) plus OS-PACS per-door hardware (~$430/door × 50 doors =
$21,500, using Raspberry Pi 4 controllers, HID Signo 40 or Identiv uTrust readers, electric strike or
maglock) plus shared infrastructure ($3,920 for switches/UPS/tools), for a **grand total of $41,740**
including $8,000 labor — $835/door, $83/user — claimed as a 60-70% savings against a $75,000-$100,000
proprietary system estimate [Hardware Bill of Materials]. Extensive per-door and system-wide
installation, testing (functionality/performance/failover/security), and go-live checklists [Week 2
through Week 5].

**OpenPIV + OS-PACS Integration Guide (incorporated):** the technical mechanism connecting the two
systems — the Card Authentication certificate (slot 9E) is the shared credential doing double duty for
both logical and physical access, read via OSDP (HID Signo, full certificate extraction) or Wiegand
(Identiv uTrust, card-serial-only with a database lookup fallback) [Hardware Integration]. A certificate
sync script polls Dogtag CA every 5 minutes and writes to new OS-PACS database tables
(`piv_certificates`, `certificate_validation_cache`, `piv_access_log`) [Software Integration]. A custom
Leosac module (`libpivauth.so`) performs certificate-chain verification, expiration checking, and OCSP-
backed revocation checking with a local cache and a documented fail-open policy when OCSP is
unreachable [Certificate Validation at Doors]. A revocation script chains Dogtag CA revocation, OS-PACS
database update, and door-controller cache clearing, with a stated propagation-time table (Dogtag CA
and OS-PACS database: immediate; online controllers: <5 minutes via next OCSP check; offline
controllers: <1 hour via cache expiration) [Revocation & Termination]. A separate cost analysis states
a **total system cost of $21,410** for the same 500-user/50-door scale ($42.82/user, $428.20/door),
compared against named proprietary competitors (Lenel $45K, HID PACS $38K, Avigilon ACM $42K),
concluding a 63% 5-year TCO savings [Cost Analysis].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| One-day single-card quick start (hardware shopping list, PC/SC setup, applet load, quick Dogtag CA) | OpenPIV Quick Start Guide, Shopping List / Day 1 Timeline | incorporated (condensed version of the Implementation Roadmap's Phase 1 sprints, using the same tools and hardware recommendations) |
| 60-week, 5-phase OpenPIV standalone implementation plan | OpenPIV Implementation Roadmap, Phases 1-5 | incorporated |
| Success criteria and ongoing-maintenance schedule | OpenPIV Implementation Roadmap, Success Criteria / Ongoing Maintenance | incorporated |
| 5-week field deployment timeline for 50 doors/500 users | Deployment Checklist, Installation Timeline | incorporated |
| Hardware BOM and $41,740 grand total (60-70% savings vs. $75-100K proprietary) | Deployment Checklist, Hardware Bill of Materials | incorporated — see tension below |
| Installation, testing, and go-live checklists | Deployment Checklist, Weeks 2-5 | incorporated |
| Shared Card-Auth-certificate architecture (OSDP vs. Wiegand readers) | Integration Guide, Hardware Integration | incorporated |
| Certificate sync script and OS-PACS database schema extension | Integration Guide, Software Integration | incorporated |
| Leosac PIV Auth module (chain/expiry/OCSP validation, fail-open) | Integration Guide, Certificate Validation at Doors | incorporated |
| Revocation propagation mechanism and timing table | Integration Guide, Revocation & Termination | incorporated |
| $21,410 total cost (63% 5-year TCO savings vs. named proprietary systems) | Integration Guide, Cost Analysis | incorporated — see tension below |

## Unresolved tensions

**Two documents computing the total system cost for the identical scale (500 users, 50 doors) arrive at
very different figures, with no cross-reference reconciling them.** The Deployment Checklist states a
grand total of $41,740 ($835/door, $83/user, including $8,000 labor), while the Integration Guide states
$21,410 ($428.20/door, $42.82/user) — roughly half. The two documents also compare against different
proprietary baselines (Deployment Checklist: a generic "$75,000-$100,000" estimate for 60-70% savings;
Integration Guide: named competitors Lenel/HID/Avigilon at $38-45K for a 63% *5-year TCO* savings claim,
a different metric than a one-time hardware cost). Attempted reconciliation: the Integration Guide's
figure appears to exclude installation labor and uses somewhat lower per-door reader/hardware unit
prices than the Deployment Checklist's BOM (e.g., the Checklist's $220 HID Signo 40 reader vs. the
Integration Guide's generic "$150" NFC reader line item) — but neither document states that the other's
figure is a different scope or an earlier/superseded estimate. Left unresolved rather than picking one
total as authoritative.

## Sources consulted (exhaustive list)

- `knowledge-base/d-central/security/Open-Secure/OpenPIV-Implementation-Roadmap-md.md`
- `knowledge-base/d-central/security/Open-Secure/OpenPIV-OS-PACS-Deployment-Checklist-md.md`
- `knowledge-base/d-central/security/Open-Secure/OpenPIV-OS-PACS-Integration-Guide-md.md`
- `knowledge-base/d-central/security/Open-Secure/OpenPIV-Quick-Start-Guide-md.md`

## Consolidation metadata

```
consolidates: [
  knowledge-base/d-central/security/Open-Secure/OpenPIV-Implementation-Roadmap-md.md,
  knowledge-base/d-central/security/Open-Secure/OpenPIV-OS-PACS-Deployment-Checklist-md.md,
  knowledge-base/d-central/security/Open-Secure/OpenPIV-OS-PACS-Integration-Guide-md.md,
  knowledge-base/d-central/security/Open-Secure/OpenPIV-Quick-Start-Guide-md.md,
]
reconciled_against: []
supersedes_prior_consolidation: none
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

None of the source docs is marked superseded or moved — status assignment belongs to DC-DEDUP-STD-001, not the Consolidator.
