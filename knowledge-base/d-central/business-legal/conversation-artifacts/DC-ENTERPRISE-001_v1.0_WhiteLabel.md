---
source_conversation_uuid: 7963735d-a671-4b42-806e-651377fd29b2
conversation_title: 'Fixing operational visibility in decentralized construction'
created_at: 2026-06-10T01:34:30.970459Z
doc_id: DC-ENTERPRISE-001
description: 'DC-ENTERPRISE-001 - White-label and hybrid deployment architecture for D-Central'
extraction_method: conversation-artifact (create_file tool-use block, never uploaded to a Project KB)
---

# DC-ENTERPRISE-001 v1.0: D-Central Enterprise Deployment Architecture
## White-Label, Hybrid, and Federated Node Models
**Registry ID:** DC-ENTERPRISE-001 v1.0  
**Parent Documents:** DC-COOP-001 v2.0, DC-NETINFRA-001, DC-B2B-001  
**Status:** Architecture Draft v1.0  
**Date:** 2026-06-09  

---

## The Two-Layer Model

D-Central is built in two separable layers.

**Layer 1 — The Core Platform (open-source):**
All operational systems — D-MOVE, D-ASSET, D-JOB, D-TRAIN, D-CRED, D-SCOUT, D-SUSTAIN, and all 54 registered systems — are open-source under a dual license. The source code is public, forkable, and deployable by anyone. No permission required.

**Layer 2 — The Network (cooperative infrastructure):**
The D-Central cooperative network — shared driver pools, D-MARKET equipment exchange, D-TRAIN credential recognition, D-CRED interoperability, zone pricing intelligence — requires participation. Participation is optional and governed by the cooperative.

An enterprise can take Layer 1 and never touch Layer 2. They get a fully functional, fully sovereign operational platform. If they want Layer 2 capabilities, they connect through the hybrid or full network mode.

This is the same model as:
- Red Hat Enterprise Linux (open-source + paid support + ecosystem)
- GitLab CE vs EE (open core + enterprise features)
- HashiCorp Vault (open-source + enterprise tier)

The difference: D-Central's enterprise tier is cooperatively owned. Revenue from enterprise licenses funds the cooperative network that makes the platform better for everyone.

---

## Licensing Structure

### L0 — Open Source Self-Hosted (Free)
- Fork the repository, deploy on any infrastructure
- Full white-label capability: rebrand completely
- All 54 systems available
- No support contract, no security patch SLA
- No D-Central network access
- Suitable for: technically capable teams who want full sovereignty

**License:** AGPL-3.0 for network services (any hosted modification must be open-sourced)  
**Commercial exception:** Commercial use without AGPL obligations requires L2 or above

### L1 — D-Central Community Edition (Free)
- Binary distribution (no need to manage the build pipeline)
- Community forum support
- Security patch notifications (not automatic)
- One-click module toggles (no custom development needed)
- No network access
- Suitable for: SMEs, cooperatives, non-profits, pilot deployments

### L2 — D-Central Enterprise Edition ($2,000–$8,000/month)
- Everything in L1
- Commercial AGPL exception (can run as a service without open-sourcing)
- Dedicated support with SLA (4-hour response, 24/7 critical)
- SSO/LDAP/SAML integration module
- ERP integration adapters (SAP, Oracle, Sage)
- Compliance documentation package (SOC 2 Type II path, ISO 27001 mapping)
- Quarterly update train (tested, curated)
- Custom module development credits ($5,000/quarter toward bespoke features)
- Suitable for: mid-to-large enterprises, regulated industries, government

### L3 — D-Central Enterprise + Network ($4,000–$15,000/month)
- Everything in L2
- Full D-Central network participation (configurable — see Hybrid section)
- D-MOVE overflow pool access (use network drivers when internal pool is at capacity)
- D-MARKET equipment listing (monetize idle assets)
- D-TRAIN cross-network credential recognition
- D-CRED network interoperability (optional)
- Anonymous operational data exchange (send aggregate data, receive network intelligence)
- Governance rights: one seat at the D-Central cooperative assembly
- Suitable for: enterprises who want operational efficiency + cooperative network effects

### L4 — D-Central Sovereign Node (Custom partnership)
- Everything in L3
- Branded co-contributor status in D-Central documentation
- Custom protocol development (shape the direction of D-Central's architecture)
- Revenue sharing on network-driven efficiency gains
- Priority access to new systems before public release
- D-BOND investment access (invest in network infrastructure, earn returns)
- Suitable for: large anchor enterprises, governments, international deployments

---

## Three Deployment Modes

### Mode 1: Isolated (Air-Gap Capable)

The enterprise platform operates with zero external connectivity. No data leaves the deployment perimeter. No dependency on D-Central infrastructure.

**Use cases:**
- Defence contractors and military facilities
- Healthcare networks (PIPEDA / HIPAA sensitive data)
- Mining operations at remote sites with no reliable internet
- Government classified facilities
- Any environment where data sovereignty is absolute

**What works:**
- All 54 D-Central systems operate normally
- D-CRED operates as internal-only credit economy
- D-TRAIN issues credentials recognized only within the enterprise
- D-MOVE operates within the company's driver pool only
- D-ASSET tracks only company-owned equipment
- Full offline-first capability (PouchDB/CouchDB sync on local network)

**What doesn't apply:**
- D-MOVE overflow from network drivers
- D-MARKET equipment exchange
- D-TRAIN cross-employer recognition
- D-CRED network convertibility
- Zone pricing intelligence from network data

---

### Mode 2: Hybrid (Selective Connectivity)

The enterprise platform runs privately with a configurable set of connections to the D-Central cooperative network. Each connection is independently toggled. The enterprise controls exactly what flows in and out.

**This is the recommended enterprise mode.** It gives operational sovereignty while accessing the specific network capabilities that generate value for that deployment.

**Hybrid connectivity menu (each independently toggleable):**

| Connection | Inbound Benefit | Outbound Requirement |
|-----------|----------------|---------------------|
| D-MOVE overflow | Network drivers available when internal pool is at capacity | None (just fees) |
| D-MARKET listing | Idle equipment generates rental revenue | Equipment temporarily listed |
| D-MARKET sourcing | Access cooperative equipment inventory for rental | None |
| D-TRAIN recognition | Employees' credentials recognized at all network employers | Credentials issued via D-TRAIN protocol |
| D-CRED compatibility | Internal credits convertible at D-Central exchange rate | Credit issuance follows D-CRED standard |
| Anonymous data sharing | Network routing intelligence, zone pricing data | Anonymized aggregate operational data |
| D-SCOUT intelligence | Network aerial data on areas you haven't surveyed | Anonymized survey data contributions |
| D-WEATHER integration | Ottawa/regional weather operational data | None (public data layer) |

**Privacy architecture for hybrid mode:**

Worker and operational data never leaves the enterprise deployment in identifiable form. The boundary is enforced at the D-HUB API layer:

```
ENTERPRISE INSTANCE
  ├── Private zone (never transmitted): worker identities, client data,
  │   job details, financial records, internal communications
  └── Sharable zone (anonymized before transmission): aggregate routing
      data, equipment utilization rates, regional pricing signals,
      weather impact data, zone demand heat maps

D-CENTRAL NETWORK
  └── Receives only: anonymized aggregates
      Sends back: network intelligence, driver availability, equipment listings
```

---

### Mode 3: Full Network

The enterprise platform is a full participant in the D-Central cooperative network. All network features are active. The enterprise's driver pool, equipment inventory, and operational data are full participants in the cooperative mesh.

**Use cases:**
- Companies that want maximum operational efficiency
- Companies embracing cooperative identity as brand/value proposition
- D-Central Sovereign Node partners building the network

**What this adds over hybrid:**
- Workers' D-IDs fully portable to/from D-Central network employment
- D-MOVE routes blend internal and network workers seamlessly
- Equipment utilization optimized across the full network, not just within the company
- D-CRED fully convertible — employees' credits work everywhere in the network
- Governance participation: vote on D-Central cooperative decisions

---

## What White-Labeling Includes

A white-label deployment of D-Central is a fully rebranded instance. Nothing visible says "D-Central." Everything is the enterprise's own platform.

**Customizable elements:**

| Element | What's Customizable |
|---------|-------------------|
| Platform name | Anything — "PCL FieldOps", "HydroNet Ops", "CareFleet", etc. |
| Logo | Replaced in app header, email templates, reports, PWA icon |
| Colour palette | Primary, secondary, and accent colours applied system-wide |
| Domain | ops.yourcompany.com (custom subdomain or full domain) |
| Module names | "D-MOVE" becomes "Crew Transport", "D-ASSET" becomes "Equipment Hub", etc. |
| D-CRED currency name | "Hydro Points", "PCL Credits", "SiteCoins" — same engine, any name |
| Email templates | All automated emails from the platform branded |
| Report headers | All D-REPORT outputs use enterprise letterhead |
| Mobile app | PWA with custom app icon, splash screen, and brand colours |
| Notification tone | Formal vs. casual language register in system messages |

**Not customizable (protocol layer, cannot change without forking):**
- D-ID structure (W3C DID specification — it's a standard)
- D-TRAIN credential schema (interoperability requires standard format)
- D-HUB API contract (if using network features)
- Core security architecture (encryption, auth flows)

---

## Enterprise Integrations

### Identity and Access Management
- **LDAP/Active Directory:** Employee accounts sync from HR systems. Workers don't create separate accounts — they log in with company credentials.
- **SAML 2.0:** Single sign-on with any enterprise identity provider (Okta, Azure AD, Google Workspace, Ping Identity)
- **SCIM provisioning:** User accounts created/deactivated automatically when employees join or leave
- **MFA:** TOTP, hardware key (FIDO2), or push authentication layered on top of D-ID

### ERP and Work Order Systems
- **SAP PM/PS:** D-JOB work orders sync bidirectionally with SAP Plant Maintenance
- **Oracle Field Service:** D-MOVE routes exported to Oracle for enterprise field service management
- **Microsoft Dynamics 365:** D-ASSET equipment records sync with Dynamics asset management
- **Custom ERP:** REST API adapter for any system with a documented API

### Compliance and Documentation
- **GIS/Mapping integration:** ESRI ArcGIS, Google Maps Platform, Mapbox for enterprise-grade mapping
- **Document management:** D-REPORT outputs to SharePoint, Google Drive, Documentum
- **EHS systems:** D-TRAIN certification records sync to Intelex, Cority, or other EHS platforms
- **Time and attendance:** D-MOVE trip logs export to Kronos, ADP, Ceridian for payroll integration

### Financial Systems
- **Accounts payable:** D-INVOICE syncs to NetSuite, QuickBooks Enterprise, Sage
- **Project accounting:** D-JOB cost codes map to project accounting structures
- **Treasury:** D-TREASURY enterprise edition connects to corporate banking APIs

---

## Industry-Specific Deployments

### Construction (PCL, EllisDon, Graham, Pomerleau)

**White-label name:** "[Company] FieldOps" or "[Company] SiteOps"

**Modules enabled:**
- D-MOVE (crew transport across multiple active job sites in a city)
- D-ASSET (equipment fleet — cranes, excavators, concrete pumps, scaffolding)
- D-JOB (work orders, daily progress reporting, subcontractor coordination)
- D-TRAIN (Red Seal trades, WHMIS, confined space, fall protection, operator certs)
- D-SUSTAIN (crew welfare on remote sites — food, water, PPE)
- D-SCOUT (drone progress monitoring for phased construction)

**Enterprise-specific additions:**
- Subcontractor management (subcontractors operate as candidate nodes with limited access)
- Lien holdback tracking in D-INVOICE
- Safety incident reporting to MOL/WCB/WSIB

**Hybrid mode:** D-TRAIN recognition (workers who leave carry Red Seal equivalents), D-MARKET (idle crane listed in network between lifts)

---

### Healthcare (Hospital networks, home care agencies)

**White-label name:** "[Network] CareFleet" or "[Organization] Mobility"

**Modules enabled:**
- D-MOVE (patient transport, staff transport to home care visits, inter-facility transfers)
- D-ASSET (medical equipment — wheelchairs, oxygen, infusion pumps, portable imaging)
- D-JOB (care visit scheduling, home care work orders)
- D-TRAIN (nursing certifications, CPR/AED, WHMIS healthcare, IPAC)
- D-SUSTAIN (staff welfare for field home care workers)

**Deployment mode: Isolated** (PIPEDA compliance, patient data sensitivity)

**Enterprise-specific additions:**
- PHIPA/PIPEDA compliance layer (data residency in Canada enforced)
- Patient privacy filter (patient identities never visible to drivers beyond first name)
- Electronic medical record (EMR) integration hooks
- On-call emergency dispatch protocol

---

### Mining and Resource Extraction (Remote Sites)

**White-label name:** "[Company] SiteOps" or "[Company] Field"

**Modules enabled:**
- D-MOVE (worker transport in remote camps, shuttle buses to extraction sites)
- D-ASSET (heavy equipment — excavators, haul trucks, drills — integrates with CANbus/J1939 via D-IoT)
- D-JOB (shift work orders, maintenance work orders)
- D-TRAIN (site-specific safety, equipment operator, explosives handling, emergency response)
- D-SUSTAIN (remote camp food, PPE, tools)

**Deployment mode: Isolated with periodic sync** (remote sites with satellite connectivity windows)

**Unique capability:** D-IoT with J1939/CANbus integration turns every machine into a real-time telemetry node. Engine hours, fuel burn, fault codes from the machine's own bus — visible in D-ASSET.

---

### Logistics and Delivery

**White-label name:** "[Company] RouteOps" or "[Company] Fleet"

**Modules enabled:**
- D-MOVE (driver dispatch, multi-stop delivery routing)
- D-ASSET (vehicle fleet management)
- D-JOB (delivery orders)
- D-TRAIN (commercial driver's license, DANGEROUS GOODS, TDG)
- D-CRED (driver incentive economy)

**Hybrid mode:** D-MOVE overflow (surge capacity from cooperative drivers), D-MARKET (vehicle rental at off-peak times)

**This is the Uber for freight equivalent** — except cooperative, no surge pricing, drivers earn equity.

---

### Government / Municipal

**White-label name:** "City of [X] Field Operations" or "[Department] Dispatch"

**Modules enabled:**
- D-MOVE (public works crew dispatch, inspection team mobility)
- D-ASSET (municipal fleet — trucks, equipment, maintenance vehicles)
- D-JOB (work orders, bylaw inspection, infrastructure maintenance)
- D-TRAIN (certified trades, Class B/C licenses, hazmat)
- D-AERIAL (infrastructure inspection, park condition surveys)
- D-SCOUT (municipal property condition monitoring)

**Deployment mode: Isolated with government data sovereignty requirements** (data residency, security classification)

**Procurement advantage:** When a municipal government deploys white-labeled D-Central, they're also advocating for the open-source cooperative model — which aligns with municipal social procurement policies they themselves wrote.

---

## The Federation Protocol

When multiple enterprises run D-Central instances and choose to connect, they federate. Federation is the technical mechanism for the hybrid and full-network modes.

**Protocol: ActivityPub-inspired cooperative federation**

Each D-Central instance is an independent actor in the federation. Instances communicate through signed API messages. No central server holds authority — the D-Central cooperative runs one reference node, but any instance can federate with any other instance directly.

**Federation message types:**
```
DRIVER_AVAILABLE    — "I have a driver going to zone X with N seats available"
EQUIPMENT_LISTED    — "I have a machine available for rental, details attached"
CREDENTIAL_ISSUED   — "Worker DID:xxxx has been certified for [skill], signed by [issuer]"
CREDIT_TRANSFER     — "Transfer N D-CREDITs from DID:xxxx to DID:yyyy"
ZONE_DEMAND         — "High demand for [service] in [zone] this week, anyone have capacity?"
ROUTE_INTELLIGENCE  — "Anonymized: N vehicles transited zone X at time Y, avg speed Z"
```

**Trust model:**
- Each instance has a signing key (Ed25519)
- Messages are signed, timestamps included, replay-protected
- Instance reputation builds over time (did they honor driver overflow commitments? deliver equipment as listed?)
- Reputation score visible to all federation participants
- Low-reputation instances lose access to premium federation features

**Data sovereignty in federation:**
```
Instance A (PCL FieldOps) → sends: DRIVER_AVAILABLE message
  ↳ Contents: driver availability status, vehicle capacity, zone, time window
  ↳ Does NOT include: driver name, license plate, worker ID, internal trip details

Instance B (D-Central Network) → receives the message
  ↳ Can match with a ride request
  ↳ Only shares match confirmation back
  ↳ Never stores PCL's operational data
```

---

## Revenue Model for D-Central as Upstream

Every enterprise license funds D-Central's cooperative infrastructure:

| Source | Year 1 | Year 3 |
|--------|--------|--------|
| L2 Enterprise licenses (3 → 12 companies) | $144,000 | $576,000 |
| L3 Enterprise + Network (1 → 5 companies) | $60,000 | $420,000 |
| L4 Sovereign Node partnerships | $0 | $150,000 |
| Implementation services | $45,000 | $180,000 |
| Custom module development | $30,000 | $120,000 |
| **Total upstream revenue** | **$279,000** | **$1,446,000** |

This revenue funds:
- Core platform development (feature roadmap, security patches)
- D-Central network infrastructure (server costs, federation relay, D-HUB)
- Cooperative governance operations
- Worker equity distributions from network surplus
- D-BOND interest payments to cooperative investors

The more enterprises deploy D-Central, the more resources fund the open-source core — making it better for everyone including Sod Boys. This is the upstream/downstream cooperative model.

---

## New Systems Added

| ID | System | Function |
|----|--------|---------|
| 55 | D-CORE | Platform foundation, module registry, deployment configuration |
| 56 | D-ENTERPRISE | Enterprise integration layer (SSO, ERP, compliance) |
| 57 | D-FEDERATION | Inter-instance protocol, signed message bus, trust model |
| 58 | D-BRANDKIT | White-label configuration, theme engine, asset pipeline |

**Total D-Central system count: 58**

---

## Registry Classification

```
Document ID:      DC-ENTERPRISE-001
Version:          1.0 (Architecture Draft)
Domain:           Enterprise Deployment Architecture
Deployment modes: Isolated · Hybrid · Full Network
License tiers:    L0 (OSS) · L1 (Community) · L2 (Enterprise) · 
                  L3 (Enterprise + Network) · L4 (Sovereign Node)
New systems:      4 (D-CORE, D-ENTERPRISE, D-FEDERATION, D-BRANDKIT)
Total systems:    58
Revenue target:   $279k Year 1 · $1.45M Year 3 (upstream licensing)
Upgrade path:     Each enterprise license strengthens the D-Central
                  cooperative network — upstream and downstream compound
```

---

*Open source means anyone can build on D-Central. Cooperative means everyone who builds on it contributes to its strength. Enterprise licensing funds the infrastructure that keeps the open-source core alive and improving. The model is not extractive — it is self-reinforcing.*
