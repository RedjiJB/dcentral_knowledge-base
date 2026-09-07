---
source_conversation: Decentralized family banking framework with modular services
source_conversation_uuid: 76d91c3d-0b67-437f-a5dc-e5841bc93104
original_filename: DC-LKB-001_Lakou_Family_Banking_Protocol.md
created_at: 2026-05-05T22:21:26.618160Z
content_hash: 7b2aaf5c474c
extraction_note: "Pulled from an artifact created inline in this conversation (create_file tool call), not from a Claude Project knowledge-base doc -- Stage 1/2 extraction only covered Project KB docs, this is a manual follow-up extraction."
---

# Lakou — Cooperative Family Banking Protocol

**Document ID:** DC-LKB-001  
**Version:** 0.1 (Concept)  
**Author:** Toussaint Redji Jean Baptiste  
**Framework:** D-Central Ecosystem  
**Status:** Draft — Concept Stage  
**Date:** 2026-05-05

---

## Executive Summary

Lakou is an open-source, decentralized cooperative banking protocol that enables any family to operate a self-sovereign financial institution. Drawing its name from the Haitian Creole word for the family compound — the communal yard at the center of family life — Lakou replaces the dependency on traditional banks with a modular, DAO-governed framework rooted in W3C Decentralized Identifiers (DIDs) and Verifiable Credentials (VCs).

Rather than choosing between a retail bank, a credit union, a family office, or a brokerage, a Lakou family vault can enable any combination of financial modules through a governance vote. The companion application presents the full experience as a familiar banking app — intuitive enough for any family member, powerful enough to rival a private bank.

Lakou is the financial infrastructure layer of the D-Central ecosystem, designed to integrate natively with D-Central ISP nodes, the HomeDAO governance system, the HMCS platform, and the Haiti–Diaspora Sovereign Value Loop.

---

## 1. Vision

The global banking system was not built for families. It was built for institutions, and families are left to piece together fragmented services: a checking account here, a mortgage there, a brokerage somewhere else, a financial advisor they meet once a year. Cooperative credit unions get closer to the ideal, but they lack the modularity, the digital-native identity infrastructure, and the cross-border reach that modern families — especially diaspora families — actually need.

Lakou asserts a different premise: **a family is a financial institution**. It has income, liabilities, investments, insurance needs, estate planning requirements, and cross-border obligations. It deserves a banking core designed around its actual structure.

The W3C DID/VC stack makes this possible. A family can now have a cryptographically verifiable identity that links every member, governs every financial decision, and interoperates with regulated financial infrastructure — without surrendering that identity to any central authority.

---

## 2. Core Principles

**Self-sovereignty.** The family controls its own keys. No bank, no government, and no platform operator can freeze, seize, or censor the vault without the family's cryptographic consent.

**Modularity.** Financial services are modules. A family enables only what it needs. Modules are upgradeable by governance vote, not by a platform admin.

**Open source.** Every component of the protocol — identity, governance, modules, settlement connectors, and companion apps — is open source under AGPLv3. No vendor lock-in.

**Cooperative governance.** The vault is governed as a DAO-cooperative hybrid. Every adult member holds governance weight. Quorum rules, spending limits, and succession logic are encoded — not stored in a lawyer's filing cabinet.

**Regulatory interoperability.** Lakou is not a grey-market system. It uses regulated fiat rails, compliant KYC/AML via Verifiable Credentials, and licensed money transmitter partnerships where required. Compliance is cryptographic, not paper-based.

**D-Central native.** Lakou is designed to run on D-Central ISP infrastructure. Local nodes provide liquidity bridging, offline-capable settlement, and mesh-based transaction routing — especially relevant for the Haiti corridor and other underbanked markets.

---

## 3. Identity Architecture (Layer 1)

### 3.1 Family DID Document

Each Lakou vault is anchored by a **Family DID Document** — a W3C DID document that represents the family unit as a legal and cryptographic entity. The document contains:

- The family's primary DID (method: `did:web`, `did:ion`, or `did:key` depending on deployment context)
- An ordered list of member DIDs linked via `controller` and `verificationMethod` entries
- Governance parameters: quorum threshold, voting weight per role, and succession order
- Service endpoints: vault API, notification webhook, and public credential status list

The Family DID Document is not stored on any single server. It is anchored to a verifiable data registry (VDR) — either a distributed ledger or a content-addressed store — and resolved through the DIF Universal Resolver.

### 3.2 Member Verifiable Credentials

Each family member holds a set of Verifiable Credentials issued into their personal DID wallet:

| Credential Type | Issuer | Purpose |
|---|---|---|
| KYC Attestation | Licensed identity verifier | AML/CTF compliance |
| Role Assertion | Family governance contract | Owner / Beneficiary / Trustee / Minor |
| Residency Proof | Government or utility provider | Jurisdictional compliance |
| Accredited Investor | Regulated body | InvestDesk access gating |
| Age Proof (ZK) | Derived from KYC | Age-gated modules (no raw DOB disclosed) |
| Consent Receipt | Lakou protocol | GDPR Article 7 compliance |

Credentials follow the W3C Verifiable Credentials Data Model 2.0. Presentation is handled via OpenID for Verifiable Presentations (OpenID4VP) and the Self-Issued OpenID Provider v2 (SIOP v2) protocol.

### 3.3 Zero-Knowledge Consent Layer

Modules that require sensitive disclosures (age, residency, accreditation) use BBS+ signatures to enable selective disclosure — a member can prove they satisfy a predicate (e.g., "over 18", "resident of Canada") without exposing the underlying credential to the module. This architectural choice means:

- Raw PII never touches module-level code
- Audit logs contain cryptographic proofs, not personal data
- GDPR and PIPEDA compliance is structural, not procedural

---

## 4. Family Bank Core (Layer 2)

### 4.1 Vault Governance Engine

The Lakou vault core is a DAO-cooperative hybrid built on Apache Fineract (open-source banking core) with a governance layer implemented as a Substrate pallet (Polkadot ecosystem) or an EVM-compatible smart contract suite using OpenZeppelin Governor + Timelock.

**Governance token model:**

Every adult family member is minted non-transferable governance tokens (ERC-1155 soulbound) at vault initialization. Weighting is configurable:

- Flat model: every adult holds equal weight (true cooperative)
- Contribution model: weight is proportional to capital contributed
- Hybrid model: flat floor + contribution top-up (recommended default)

Minors hold observer status with no voting weight until they reach the governance age threshold (configurable, default 18).

**Decision types and quorum requirements:**

| Decision Type | Quorum | Veto Rights |
|---|---|---|
| Enable a module | 60% | None |
| Disable a module | 51% | None |
| Loan approval (above threshold) | 67% | None |
| Succession change | 75% | Current owner |
| Vault dissolution | 90% | None |
| Emergency freeze | 51% | Any single member |

### 4.2 Module Registry

The Module Registry is an on-chain contract implementing the EIP-2535 Diamond Standard (upgradeable proxy with modular facets). Each banking module is a registered facet with:

- A module manifest (name, version, required VCs, fee schedule)
- An enable/disable state controlled by governance vote
- A Timelock delay (configurable, minimum 24 hours) between vote and activation
- An interface conformance check against the Lakou Module Interface Standard (LMIS)

No module can be force-activated by any party other than the family's governance vote. The protocol admin key (Lakou Foundation multisig) can publish module upgrades to the registry but cannot activate them in any family's vault.

---

## 5. Banking Modules (Layer 3)

All modules are opt-in. A freshly initialized vault has no modules active. The family enables modules through governance vote.

### 5.1 RetailVault

**Checking accounts, savings accounts, and debit cards.** The entry-level module. Most families start here.

- Multi-member checking accounts with configurable joint access rules
- High-yield savings (yield sourced from DeFi liquidity protocols or partnered credit unions)
- Virtual and physical debit cards (Visa/Mastercard via BIN sponsorship program)
- Automated savings rules (round-ups, recurring sweeps, savings circles)
- Full transaction history with on-chain audit trail

### 5.2 CreditCircle

**Loans, mortgages, and credit scoring.** Operates as an internal cooperative lending pool.

- Inter-family loans (one member borrows from the family pool)
- External mortgage origination (via partnered regulated lenders who accept DID-based KYC)
- Lakou Credit Score: an internal, privacy-preserving score derived from on-chain repayment history and family asset coverage — not the FICO model
- Collateral vaults: tokenized real-world assets (RWA) locked as collateral using ERC-4626

### 5.3 CommercialDesk

**Business banking for family-owned enterprises.** Designed for the family that runs a business.

- Dedicated business sub-accounts linked to the family vault
- Invoicing engine with FIDO2-signed invoice issuance
- Payroll disbursement (domestic and cross-border)
- Accounts receivable / payable ledger with double-entry bookkeeping
- Business expense cards with per-employee limits governed by family vote

### 5.4 PrivateDesk

**Wealth management and portfolio advisory.** Designed for families with accumulated assets.

- Unified portfolio view across all asset classes (traditional, crypto, real estate)
- AI-assisted advisory layer (local LLM, not cloud-processed PII)
- Fee-only advisor access via VC-gated API (advisors present their fiduciary credential)
- Rebalancing engine with configurable risk profiles

### 5.5 FamilyOffice

**Multi-generational wealth, estate planning, and trust administration.** The most powerful module.

- Digital trust instruments: living trusts, testamentary trusts, and charitable trusts stored as smart contracts
- Estate vault: encrypted document storage (will, deed, insurance policies) with biometric-gated access
- Succession logic: automatic asset transfer rules triggered by death certificate VC (issued by a recognized registry)
- Generation transfer: automatic re-weighting of governance tokens when a member reaches majority
- Philanthropic endowment sub-accounts with transparent disbursement tracking

### 5.6 InvestDesk

**Securities, ETFs, commodities, crypto, and DeFi.** Full-spectrum investment module.

- Traditional brokerage via partnered regulated broker-dealer (SEC/IIROC registered)
- Crypto trading via non-custodial DEX aggregator + optional custodial bridge
- DeFi yield: staking, lending, and liquidity provision with family governance approval per protocol
- Structured products: family-designed baskets and target-date instruments
- Portfolio performance reporting with tax lot tracking

### 5.7 SavingsCircle

**Susu / tontine / ROSCA cooperative savings.** Culturally rooted savings infrastructure.

- Create formal rotating savings and credit associations within or across family vaults
- Programmable contribution schedules, payout rotation, and late penalty rules
- Smart-contract enforced — no informal trust required
- Cross-vault circles: multiple family vaults join a circle (diaspora savings networks)
- Audit trail and dispute resolution via DAO arbitration

### 5.8 RemittanceGate

**Cross-border transfer rails, optimized for underserved corridors.** The Haiti corridor module.

- Direct family-to-family transfers via D-Central mesh nodes
- Stablecoin bridge: send USDC, recipient receives local fiat via partnered cash-out agents
- Haiti Gourde (HTG) stablecoin: HGUSD peg maintained by the Haiti–Diaspora Sovereign Value Loop
- Sub-1% fee target via DePIN liquidity routing (vs. 5–10% Western Union rates)
- Offline-capable: transfer initiation survives connectivity outages via FSO-backhaul relay

### 5.9 InsuranceVault

**Cooperative insurance products.** The family as a risk-pooling unit.

- Parametric insurance: auto-pay on verifiable trigger events (e.g., NOAA weather data triggers flood payout)
- Life insurance: term life underwritten by cooperative pool with VC-gated claim verification
- Health expense pool: family-governed medical expense sharing (not a licensed insurer — a sharing arrangement)
- Property insurance: for families with tokenized RWA collateral in CreditCircle

### 5.10 TaxLedger

**Tax reporting, optimization, and cross-jurisdictional compliance.** Powered by OpenFisca.

- Automatic transaction categorization for tax purposes
- Multi-jurisdictional support (Canada, US, Haiti, France, EU)
- Tax lot optimization for InvestDesk transactions
- T4/T5/T3, 1040/1099, and Form W-8 generation (exportable to accountant API)
- Estate freeze and inter-generational gift tax modeling

---

## 6. Settlement Layer (Layer 4)

### 6.1 Fiat Rails

Lakou connects to fiat payment infrastructure via open-banking APIs and regulated money transmitter partnerships:

- ACH (US), Interac e-Transfer (Canada), SEPA (EU), Faster Payments (UK)
- SWIFT for international correspondent banking
- Local cash-in/cash-out agent networks for unbanked markets (Haiti, Caribbean)

### 6.2 Stablecoin Layer

On-chain settlement uses fully reserved stablecoins:

- USDC (Circle) for USD-denominated transactions
- EURC (Circle) for EUR-denominated transactions
- HGUSD: a proposed Haiti Gourde stablecoin anchored to the D-Central Haiti–Diaspora Value Loop (detailed in DC-HDR-001)

### 6.3 D-Central DePIN Integration

D-Central ISP nodes deployed in Ottawa, Montreal, and eventually Port-au-Prince serve as local liquidity relay points. This means:

- Settlement traffic for remittances can route through owned infrastructure
- Offline transaction queuing during internet outages (critical for Haiti)
- Node operators earn routing fees in HGUSD, creating a closed economic loop

**Scope note:** this is financial-rail DePIN (liquidity routing, remittance settlement) — a distinct concept from
compute DePIN (node operators contributing GPU/FPGA/ASIC capacity for AI inference), which is specified separately
in [DC-COMPUTE-SILICON-ARCH-001](DC-COMPUTE-SILICON-ARCH-001.md). The two share the node-operator reward pattern
in spirit but not in mechanism — do not conflate this section with mesh-ai/mesh-compute's DePIN.

---

## 7. Companion Applications (Layer 5)

### 7.1 Design Philosophy

The companion apps deliberately look and feel like a traditional banking app. This is intentional. The decentralized infrastructure is invisible to daily users. A family member who wants to check their balance, send money, or pay a bill should not need to understand DID documents or smart contracts.

The apps are module-aware: only the modules the family has enabled appear in the navigation. A vault running only RetailVault + RemittanceGate looks like a simple checking + remittance app. A vault running all 10 modules looks like a full private bank.

### 7.2 Mobile App (React Native)

- iOS and Android
- Biometric auth (FaceID / fingerprint) backed by FIDO2 device credential bound to the member's DID
- Full feature set for all enabled modules
- Push notifications for transactions, governance votes, and savings circle payouts
- Offline-capable: view balances and queue transactions without connectivity

### 7.3 Desktop App (Tauri + React)

- macOS, Windows, Linux
- Full family office dashboard: multi-account overview, net worth tracker, investment performance
- Document vault access (FamilyOffice module)
- Multi-sig governance signing: hardware wallet support (Ledger, YubiKey)
- Accountant export: generates GAAP-compliant reports and tax packages
- Admin console: module management, member onboarding, governance history

### 7.4 Open API (FastAPI + OpenAPI 3.1)

Third-party integrations are scoped via VC-gated OAuth 2.0 + DPoP tokens:

- Accountants and advisors present their professional credential VC to request scoped read access
- Payroll and HR systems connect via CommercialDesk API
- Tax software pulls transaction data via TaxLedger API
- The API is also the integration surface for future D-Central ecosystem products (HMCS, HomeDAO, OpenSecure)

---

## 8. Technical Stack

| Layer | Component | Technology |
|---|---|---|
| Identity | DID resolution | DIF Universal Resolver |
| Identity | VC wallet | Spruce DIDKit / Veramo |
| Identity | ZK proofs | SnarkJS + BBS+ |
| Governance | DAO contracts | OpenZeppelin Governor + Timelock |
| Governance | Module proxy | EIP-2535 Diamond |
| Banking core | Account ledger | Apache Fineract |
| Banking core | Double-entry | Plain Accounts (open source) |
| Settlement | Fiat connectivity | Open-banking APIs + Plaid/Truelayer |
| Settlement | On-chain | Polygon PoS / Optimism L2 |
| API | REST + async | FastAPI, Celery, Redis |
| API | Real-time | WebSocket (account feeds) |
| Mobile | Cross-platform | React Native + Expo |
| Desktop | Native wrapper | Tauri (Rust) |
| Desktop | UI | React + TypeScript |
| Data | Primary store | PostgreSQL (per-vault, encrypted) |
| Data | Chain indexing | The Graph Protocol |
| Infrastructure | D-Central nodes | OpenWrt + NetBox + Ansible |

---

## 9. Governance Token Model

At vault initialization, the founding member mints the initial governance token supply (configurable, default 1,000 tokens). Distribution:

- **Founder allocation:** 40% held by the primary account holder
- **Member pool:** 40% distributed equally among verified adult members at enrollment
- **Reserve:** 20% held in the vault treasury, released via governance vote (e.g., for adding new members, compensating advisors, or funding module upgrades)

Tokens are non-transferable (ERC-1155 soulbound). They cannot be sold, delegated to non-members, or inherited directly — instead, succession logic in the FamilyOffice module handles the reissuance of tokens to heirs after a governance-confirmed succession event.

---

## 10. Regulatory Framework

Lakou operates within, not outside, regulated financial systems. The compliance strategy by layer:

**Identity layer:** KYC/AML is performed by a licensed identity verifier who issues a credential. The vault itself never stores raw PII — it stores a cryptographic proof that KYC was completed. This satisfies FinCEN, FINTRAC (Canada), and FATF Travel Rule requirements via credential-based attestation.

**Banking modules:** Regulated activities (deposit-taking, lending, securities dealing) are performed by licensed partner institutions. Lakou is the interface and governance layer; the regulated entity sits behind it. This is the same model used by neobanks like Chime (backed by Bancorp) — Lakou makes it composable.

**Remittance:** RemittanceGate operates under money services business (MSB) registration where required. In corridors where stablecoin transfer does not trigger MSB classification (e.g., self-hosted wallet to self-hosted wallet), no license is required.

**Securities:** InvestDesk routes through a registered broker-dealer for regulated securities. Crypto trading can be non-custodial (no license required for self-custody).

---

## 11. Haiti–Diaspora Integration

Lakou is purpose-designed for the Haiti–Diaspora remittance corridor, which currently processes approximately USD 3.5 billion per year at a 5–10% fee rate.

The RemittanceGate module, combined with D-Central ISP mesh nodes and the HGUSD stablecoin, targets:

- Sub-1% transfer fees for family-to-family remittances
- Same-day settlement (vs. 1–5 business days for wire transfers)
- Offline queuing for recipients in areas with unreliable connectivity
- Integration with the Haiti CIN (Carte d'Identification Nationale) sovereign identity stack (DC-CIN-001) for recipient verification

The SavingsCircle module formalizes the existing informal susu/tontine networks used by the Haitian diaspora — bringing them on-chain with smart-contract enforcement while preserving their cultural form.

---

## 12. Integration with D-Central Ecosystem

| D-Central Product | Integration Point |
|---|---|
| D-Central ISP | Settlement routing, offline relay, DePIN liquidity |
| HomeDAO | Governance token interoperability, household voting |
| HMCS | Household expense categorization feeds TaxLedger |
| OpenSecure Platform | Physical access tied to vault member credentials |
| Haiti CIN | Recipient identity verification for RemittanceGate |
| Haiti–Diaspora Value Loop | HGUSD stablecoin issuance and redemption |
| Sovereign DAO OS | Lakou vault governance runs on top of Sovereign DAO OS |

---

## 13. Roadmap

### Phase 1 — Foundation (Q3–Q4 2026)
- Family DID Document specification finalized
- Member VC schema library published
- RetailVault module: MVP with Fineract backend
- Governance contract: flat-weight model
- Mobile app: account overview + send/receive

### Phase 2 — Core Modules (Q1–Q2 2027)
- CreditCircle module: inter-family loans
- SavingsCircle module: ROSCA smart contract
- RemittanceGate module: USDC bridge + Haiti corridor pilot
- Desktop app: full dashboard
- TaxLedger module: Canadian and US tax reporting

### Phase 3 — Advanced Verticals (Q3–Q4 2027)
- FamilyOffice module: trust contracts + estate vault
- InvestDesk module: broker-dealer API integration
- CommercialDesk module: business banking
- HGUSD stablecoin: Haiti Gourde peg launch

### Phase 4 — Ecosystem Integration (2028)
- Full D-Central ecosystem integration
- PrivateDesk module: wealth management AI
- InsuranceVault module: cooperative insurance
- Cross-vault SavingsCircles: multi-family networks
- D-Central node liquidity program launch

---

## 14. Open Questions (For Development)

1. Which DID method should be the canonical default for mobile-first deployments where users cannot self-host a `did:web` server? (`did:ion` is the leading candidate.)
2. Should the governance contract be deployed on Polygon, Optimism, or a Substrate-based appchain? The answer affects gas costs for low-income users in Haiti.
3. What is the minimum viable licensed partner stack for Canadian launch? (FINTRAC MSB + one bank partner for CDIC-insured deposit holding.)
4. How does the FamilyOffice trust module interact with provincial estate law (Ontario, Quebec) — does a smart-contract trust need to be registered with the court?
5. Should the governance token model support quadratic voting as an alternative to linear weighting?

---

## Appendix A — Glossary

| Term | Definition |
|---|---|
| DID | Decentralized Identifier (W3C standard) — a globally unique identifier controlled by its subject |
| VC | Verifiable Credential (W3C standard) — a cryptographically verifiable claim about a subject |
| DAO | Decentralized Autonomous Organization — governance by smart contract |
| LMIS | Lakou Module Interface Standard — the interface contract all modules must implement |
| HGUSD | Haiti Gourde USD-pegged stablecoin — proposed D-Central stablecoin for the Haiti corridor |
| VDR | Verifiable Data Registry — the registry where DIDs are anchored |
| ROSCA | Rotating Savings and Credit Association — the formal term for susu/tontine |
| RWA | Real-World Asset — a tokenized representation of a physical asset |
| DPoP | Demonstration of Proof-of-Possession — OAuth 2.0 sender-constrained access token standard |

---

## Appendix B — Document History

| Version | Date | Changes |
|---|---|---|
| 0.1 | 2026-05-05 | Initial concept draft |

---

*Lakou is a component of the D-Central Ecosystem. Document ID: DC-LKB-001.*  
*Author: Toussaint Redji Jean Baptiste*


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

**References:**
- [[DC-COMPUTE-SILICON-ARCH-001|DC-COMPUTE-SILICON-ARCH-001 — Compute Silicon Class Architecture (v1, generated 2026-09-07)]]

<!-- AUTO-GENERATED RELATED END -->
