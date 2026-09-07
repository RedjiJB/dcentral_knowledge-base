---
source_conversation: Decentralized family banking framework with modular services
source_conversation_uuid: 76d91c3d-0b67-437f-a5dc-e5841bc93104
original_filename: DC-LKB-003_Lakou_Protocol_v2_Universal_Banking_OS.md
created_at: 2026-05-05T23:13:58.285160Z
content_hash: bdc638ef3411
extraction_note: "Pulled from an artifact created inline in this conversation (create_file tool call), not from a Claude Project knowledge-base doc -- Stage 1/2 extraction only covered Project KB docs, this is a manual follow-up extraction."
---

# Lakou Protocol v2 — Universal Decentralized Banking Operating System

**Document ID:** DC-LKB-003  
**Version:** 0.1  
**Author:** Toussaint Redji Jean Baptiste  
**Supersedes / Extends:** DC-LKB-001, DC-LKB-002  
**Framework:** D-Central Ecosystem  
**Status:** Draft — Architecture Design  
**Date:** 2026-05-05

---

## Abstract

Lakou Protocol v2 expands the original family banking concept into a **Universal Decentralized Banking Operating System (UDBOS)**. Any individual, family, cooperative, community, corporation, or DAO can instantiate a Lakou vault configured as any type of banking institution — retail bank, commercial bank, investment bank, credit union, neobank, private bank, savings and loan association, development bank, or DAO treasury.

Membership is no longer restricted to family units. Any verified DID holder can apply to join a vault according to that vault's membership policy. Each vault type has a curated default module set, but all 50+ modules are available for any vault to enable through governance.

The protocol adds full support for Directed Acyclic Graph (DAG) settlement networks (Hedera Hashgraph, IOTA Tangle), NFT-based financial instruments (loan NFTs, ownership certificates, identity anchors), DeFi protocol integration (AMM liquidity, lending, yield strategies), and zero-knowledge compliance proofs. The companion applications — mobile, web, and desktop — render a professional banking interface that adapts its entire UI to the active vault type and enabled module set.

---

## 1. Protocol Architecture v2

### 1.1 Conceptual Model

The v2 protocol introduces a clean three-level hierarchy:

```
PROTOCOL LAYER (Lakou Foundation)
  ├── Module Registry         — audited module catalog, versioned
  ├── Vault Factory           — deploys new vault instances
  ├── Identity Registry       — DID resolution, VC schema library
  └── Settlement Network      — multi-chain + DAG routing

VAULT LAYER (operator-controlled)
  ├── Vault Type              — determines default UX and module set
  ├── Governance Contract     — DAO rules, quorum, token model
  ├── Module Registry (local) — which modules are active for this vault
  ├── Membership Registry     — member DIDs, roles, weights, VCs
  └── Treasury Contract       — vault funds, reserves, yield

APPLICATION LAYER (user-facing)
  ├── Mobile App (React Native)
  ├── Web App (Next.js — mobile-first responsive)
  ├── Desktop App (Tauri + React)
  └── Open API (FastAPI — third-party integrations)
```

### 1.2 Vault Types

A vault type is a named configuration profile that sets:
- Default enabled module set
- Default governance parameters
- Default membership model
- UI theme and navigation structure
- Regulatory compliance profile

Vault types are not hard constraints. Any vault can enable any module through governance. The vault type is the starting template.

| Vault Type | Analogous Institution | Default Membership |
|---|---|---|
| `FAMILY` | Private family bank | Closed — invite + vote |
| `COMMUNITY` | Credit union / community bank | Open — KYC required |
| `PRIVATE` | Private bank / family office | Invite-only — asset threshold |
| `RETAIL` | Retail bank | Open — standard KYC |
| `COMMERCIAL` | Commercial / corporate bank | B2B — business credential |
| `INVESTMENT` | Investment bank / brokerage | Accredited investor credential |
| `DEVELOPMENT` | Development bank / impact fund | Project-based — stakeholder VC |
| `NEOBANK` | Digital neobank | Open — mobile KYC |
| `DAO_TREASURY` | Web3 protocol treasury | Token-gated — governance token |

### 1.3 External Membership Model

The most significant change from v1. Any Lakou vault can accept external members — individuals who are not family members but want to participate in the vault's financial services.

**Membership application flow:**

```
Applicant
  │
  ├─1─ Resolve vault DID → discover vault's public membership policy
  │
  ├─2─ Present KYC Attestation VC to vault's onboarding endpoint
  │      (or complete KYC flow via vault's VC issuer partner)
  │
  ├─3─ Submit membership application with:
  │      - Member DID
  │      - Desired role (Owner / Member / Associate)
  │      - Supporting credentials (accredited investor, business reg, etc.)
  │      - Proposed capital contribution (for contribution-weighted vaults)
  │
  ├─4─ Governance vote in vault
  │      - COMMUNITY type: auto-approve on KYC pass (51% optional override)
  │      - FAMILY type: explicit vote required
  │      - INVESTMENT type: accredited investor VC auto-gates + 60% quorum
  │
  ├─5─ Membership terms signed (DID-signed acceptance of vault charter)
  │
  └─6─ Governance tokens minted, API access granted, app provisioned
```

**Role capabilities matrix:**

| Capability | Founder | Owner | Member | Associate | Institutional | Observer |
|---|---|---|---|---|---|---|
| Vote on proposals | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| Create proposals | ✓ | ✓ | ✓ | ✗ | ✗ | ✗ |
| Access all enabled modules | ✓ | ✓ | ✓ | Scoped | API only | ✗ |
| Manage other members | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| Emergency vault freeze | ✓ | ✓ | ✗ | ✗ | ✗ | ✗ |
| View vault audit logs | ✓ | ✓ | Own only | ✗ | ✗ | ✗ |
| Governance token transfers | Soulbound | Soulbound | Soulbound | ✗ | ✗ | ✗ |

---

## 2. Complete Module Taxonomy

Modules are organized into 9 verticals matching the 9 banking institution types. Every module implements `ILakouModule` (DC-LKB-002 §3.2). Module IDs follow the pattern `lakou.module.{vertical}.{name}.v{n}`.

---

### 2.1 Retail Banking Modules

**`retail.checking`** — Checking accounts and debit cards  
Core consumer banking. Multi-account support, joint account rules, virtual and physical debit card issuance via BIN sponsorship. ACH, Interac, and SWIFT connectivity. Real-time balance updates via WebSocket feed. Overdraft protection linked to CreditCircle module.

**`retail.savings`** — Savings accounts and certificates of deposit  
Interest-bearing savings with configurable yield sources: DeFi lending protocol yield, cooperative pool yield, or traditional bank rate. CD ladder management with automatic roll-over. Goal-based savings buckets with visual progress tracking.

**`retail.mortgage`** — Residential mortgage origination and servicing  
Full mortgage lifecycle: pre-qualification → application → underwriting → closing → servicing. Integrates with `chain.nft_assets` to tokenize the mortgage as a Loan NFT (ERC-3525 semi-fungible). Secondary market: mortgage NFTs can be sold to investors via the `invest.fixed_income` module's marketplace.

**`retail.personal_loan`** — Consumer lending  
Installment loans, personal lines of credit, and auto loans. Credit scoring uses the Lakou Credit Score (LCS) — derived from on-chain repayment history, vault asset coverage, and ZK-verified income proofs. No FICO dependency.

**`retail.card`** — Credit card issuance and management  
Full credit card program: card issuance, credit limit management, statement generation, rewards programs (redeemable in HGUSD or vault governance tokens). Dispute resolution workflow. Fraud detection via on-chain behavioral analysis.

**`retail.insurance`** — Retail insurance products  
Parametric and traditional insurance products: renters insurance, life insurance, travel insurance. Parametric products auto-pay on verified oracle data (weather events via Chainlink, flight delays via IATA feed). Claims are VC-gated — policyholder presents an incident VC to trigger payout.

---

### 2.2 Commercial / Corporate Banking Modules

**`commercial.cash_management`** — Corporate treasury and liquidity  
Multi-entity cash pooling, notional pooling, sweep accounts, and zero-balance accounts. Automated liquidity forecasting using vault transaction history. Integration with `chain.dag_settlement` for intraday liquidity management via Hedera.

**`commercial.trade_finance`** — Letters of credit and trade instruments  
Documentary credits (LC), standby letters of credit, bank guarantees, and bills of exchange. Trade instruments issued as NFTs (ERC-721) with lifecycle management on-chain. Integration with shipping and logistics oracle data for condition-based release.

**`commercial.corporate_lending`** — Term loans and revolving credit  
Syndicated loans, term loans, and revolving credit facilities. Loan participation is tokenized (ERC-3525 Loan NFT) — banks and institutional investors hold fractional loan NFTs and receive proportional interest payments. Covenant monitoring automated via on-chain financial data feeds.

**`commercial.real_estate`** — Commercial real estate finance  
CRE acquisition loans, construction loans, and bridge financing. Property tokenization via `chain.nft_assets`: commercial properties become ERC-721 NFTs with fractional ERC-20 wrapper for investor syndication. Rent income flows directly to NFT holders via smart contract.

**`commercial.payroll`** — Business payroll and HR banking  
Payroll disbursement (fiat via ACH and crypto via stablecoin). Contractor payment in USDC or HGUSD with automatic tax withholding calculation (TaxLedger integration). Payroll schedule NFTs for employees as verifiable pay stubs.

**`commercial.merchant`** — Merchant acquiring and POS  
Merchant account provisioning, payment gateway, and virtual POS. Settlement in fiat, USDC, or HGUSD. Integration with `chain.dag_settlement` for feeless micro-transaction settlement via IOTA.

---

### 2.3 Investment Banking Modules

**`invest.equity`** — Equity trading and research  
Full-service equity trading: market orders, limit orders, stop-loss, and algorithmic orders. Real-time order book via Solana DEX integration (for tokenized equity) and broker-dealer API (for registered securities). Equity research portal with AI-assisted analysis.

**`invest.fixed_income`** — Bond trading and fixed income  
Government bonds, corporate bonds, municipal bonds, and structured products. Secondary market for Loan NFTs minted by `retail.mortgage` and `commercial.corporate_lending`. Bond ladder tool with maturity scheduling and reinvestment automation.

**`invest.derivatives`** — Options, futures, and structured products  
Options chain viewer and trading desk (via regulated broker-dealer API). Structured products: principal-protected notes, basket swaps, and yield-enhanced deposits. DeFi derivatives: perpetuals and options via dYdX and Lyra protocol integration.

**`invest.crypto`** — Cryptocurrency spot trading  
Multi-chain crypto asset trading: BTC, ETH, SOL, HBAR, MATIC, and 200+ altcoins. Order routing across Uniswap v4, Curve, and centralized exchange APIs with best-execution routing. Portfolio rebalancing automation.

**`invest.defi`** — DeFi yield strategies  
Curated DeFi protocol access: Aave v3 (lending), Compound v3 (lending), Uniswap v4 (LP), Curve (stablecoin LP), Lido (staking), and Yearn (yield aggregation). Each protocol must be whitelisted by a vault governance vote before capital deployment. Yield dashboard with APY comparison and risk ratings.

**`invest.ipo`** — IPO participation desk  
Access to IPO allocations via broker-dealer partnership. Token sales and IDOs for blockchain projects. Community IPO pools: multiple vault members pool capital to access minimum allocation thresholds. NFT issuance for IPO participation records.

**`invest.capital_markets`** — Capital raising and bond issuance  
For vaults that want to raise capital: token issuance (DAO tokens, stablecoins, governance tokens), bond issuance on-chain (tokenized bonds as ERC-3525), and equity crowdfunding. Compliant with Reg CF, Reg D, and Reg A+ frameworks.

**`invest.ma_advisory`** — M&A deal room  
Secure virtual deal room for mergers and acquisitions: document vault (FamilyOffice integration), NDA management (DID-signed), financial model sharing (access-controlled by member role), and deal governance (DAO vote for approval). For community and corporate vaults managing strategic transactions.

---

### 2.4 Credit Union / Cooperative Modules

**`coop.membership`** — Cooperative membership equity  
Member shares issuance: each new member receives shares representing their ownership stake. Shares are non-tradeable soulbound tokens (ERC-1155). Share value appreciates with vault performance. Patronage dividends paid proportional to member activity (loans taken, deposits held).

**`coop.lending`** — Cooperative member lending  
Loans from the collective pool at cooperative rates (typically 2–4% below market). Peer-reviewed underwriting: a lending committee (elected governance role) reviews applications above a threshold. Delinquency handled by member solidarity fund before external collections.

**`coop.rosca`** — Rotating savings and credit associations  
Formalized susu, tontine, and ROSCA structures. Smart-contract enforced: contributions, rotation order, payout schedule, and late penalties are all on-chain. Cross-vault circles supported: members from different Lakou vaults can join a shared circle. Arbitration via DAO dispute resolution.

**`coop.insurance_pool`** — Cooperative insurance  
Member-funded risk pooling. Members contribute to a shared insurance pool; claims are verified via VC attestation and paid from the pool. Surplus at year-end distributed as member dividends. Reinsurance option: link pool to professional reinsurer via smart contract.

**`coop.dividends`** — Patronage dividend distribution  
Automatic calculation and distribution of patronage dividends based on member activity metrics. Dividends issued in vault stablecoin or vault governance tokens. Tax reporting integration (TaxLedger) for cooperative dividend income.

---

### 2.5 Private Banking / Wealth Management Modules

**`private.wealth`** — Portfolio management and advisory  
Unified portfolio across all asset classes: traditional equities, fixed income, real estate, private equity, crypto, DeFi, and alternatives. AI advisory engine (local LLM — no cloud PII processing) generates personalized recommendations. Fee-only advisor access via VC-gated API credential.

**`private.family_office`** — Multi-generational wealth and estate planning  
Digital trust instruments (living trusts, testamentary trusts, dynasty trusts) as smart contracts. Estate vault: encrypted document storage with biometric-gated access. Succession automation triggered by Death Certificate VC. Generation-skipping tax optimization via TaxLedger integration.

**`private.alternatives`** — Alternative investments  
Private equity co-investments, venture capital fund interests, hedge fund allocations, real estate syndications, fine art, collectibles, and timberland. Alternative assets tokenized as NFTs (ERC-721) with fractional ERC-20 wrapper for liquidity. Secondary market access for private equity NFTs.

**`private.philanthropy`** — Charitable giving and impact  
Donor-advised fund (DAF) as a sub-vault with pass-through to qualified charities. Charitable remainder trust structure on-chain. Philanthropic impact tracking: grant disbursements linked to on-chain outcome data from partner NGOs. Charitable deduction documentation for TaxLedger.

**`private.concierge`** — Personal banker and concierge services  
Dedicated relationship manager assignment (integrated via CRM API). Priority transaction routing (expedited KYC, same-day wire processing). Club membership and lifestyle concierge via partner API integrations. Private event access and co-investment opportunity notifications.

---

### 2.6 Savings & Loan Modules

**`sl.thrift`** — Traditional thrift institution operations  
Savings passbook accounts, share certificates, and holiday club accounts. Traditional thrift governance: mutual savings bank charter rules implemented as smart contract parameters. Thrift mutual ownership: depositors hold mutual ownership NFTs entitling them to a share of vault surplus.

**`sl.mortgage_pool`** — Mortgage-focused savings pool  
Community mortgage pool: depositors fund a shared mortgage lending pool. Interest income distributed to depositors proportional to their deposit. Mortgage origination underwritten by the pool; loans tokenized as Loan NFTs held by the pool contract.

---

### 2.7 Development Banking Modules

**`dev.project_finance`** — Infrastructure and industrial project loans  
Large-scale project financing: infrastructure, energy, water, and industrial projects. Project loans tokenized as ERC-3525 Loan NFTs with tranched principal. Impact measurement oracle: project outcome data from verified third-party assessors triggers milestone-based disbursements.

**`dev.agriculture`** — Agricultural lending and crop insurance  
Farm loans, equipment financing, and seasonal credit lines. Crop insurance using Chainlink weather oracle: parametric payouts triggered by drought, flood, or frost events. Agricultural land tokenization: farmland as NFT collateral. Integration with satellite crop monitoring data.

**`dev.impact`** — Impact investing and ESG management  
ESG-scored investment portfolio with real-time ESG data from oracle feeds. UN SDG alignment tracking. Carbon credit management: tokenized carbon credits (ERC-1155) tradeable on-chain. Impact report generation for institutional LPs and development finance institutions.

**`dev.microfinance`** — Small business and micro-lending  
Micro-loans from $50 to $10,000 for unbanked and underbanked borrowers. Credit scoring via alternative data: mobile money history, community vouching (attested by DID), and cooperative repayment track record. Group lending model: Grameen-style mutual guarantee groups encoded as smart contracts.

**`dev.grants`** — Grant management and disbursement  
Grant program administration: application intake, review workflow, award letters as VCs, and milestone-based disbursement. Grant funds held in escrow contract; disbursed on proof of milestone completion (attested by verifier VC). Integration with public funding databases (USAID, World Bank, IDB).

---

### 2.8 Neobank Modules

**`neo.instant_pay`** — Real-time payment rails  
Sub-second payment confirmation via Hedera Hashgraph DAG settlement. Integration with national real-time payment networks: RTP (US), Faster Payments (UK), Interac e-Transfer (CA). QR code and NFC payment initiation. Request-to-pay workflow.

**`neo.virtual_card`** — Virtual card issuance and management  
Instant virtual Visa/Mastercard issuance via BIN sponsorship partner. Single-use cards for online security. Per-merchant spending limits. Freeze/unfreeze in real time. Apple Pay and Google Pay integration via tokenization API.

**`neo.open_banking`** — PSD2-style open banking APIs  
Outbound: share vault data (with consent) to third-party fintech apps, accounting software, and tax services. Inbound: aggregate data from external bank accounts (read-only) for unified financial view. Consent management dashboard: revoke third-party access with one tap.

**`neo.budgeting`** — AI-powered spending analysis  
Transaction categorization using local LLM (no cloud PII). Spending trend analysis, anomaly detection, and budget recommendations. Net worth tracking over time. Savings rate benchmarking. Predictive cash flow projection.

---

### 2.9 DAO Treasury Modules

**`treasury.reserve`** — Protocol reserve management  
DAO treasury management: multi-sig controlled reserve accounts, diversified asset allocation, and yield strategy. Runway calculator: given current burn rate, project treasury longevity. Proposal-gated spending: any disbursement above threshold requires on-chain governance vote.

**`treasury.stablecoin`** — Stablecoin issuance and management  
Deploy and manage a vault-native stablecoin (e.g., HGUSD for Haiti corridor). Collateralization management: over-collateralization ratio monitoring, liquidation triggers. Peg stability mechanisms: algorithmic reserve adjustments and backstop AMM pool.

**`treasury.monetary_policy`** — DAO monetary parameters  
Interest rate governance for vault-issued stablecoin. Reserve ratio management. Token supply governance: minting and burning proposals. Inflation management for governance tokens. Economic parameter dashboards for token holder visibility.

---

### 2.10 Blockchain / DLT Infrastructure Modules

**`chain.nft_assets`** — NFT minting and asset tokenization  
Universal NFT minting interface supporting ERC-721 (unique assets), ERC-1155 (multi-edition), and ERC-3525 (semi-fungible — ideal for loan NFTs and fractional ownership). Asset types:
- Loan NFTs: represent a debt obligation with embedded payment schedule
- Ownership NFTs: represent fractional real estate, art, or fund interests
- Identity NFTs: DID-anchored membership credentials
- Certificate NFTs: proof of deposit, insurance policy, trade finance instrument
- Membership NFTs: cooperative share certificates, DAO voting tokens

**`chain.dag_settlement`** — DAG network settlement integration

*Hedera Hashgraph:* High-throughput (10,000+ TPS), final settlement in 3–5 seconds, deterministic finality. Used for: retail micro-transactions, remittance settlement, stablecoin transfers, and DeFi operations that need fast finality without rollback risk.

*IOTA Tangle:* Feeless micro-transactions for IoT and DePIN contexts. Used for: D-Central ISP metered bandwidth payments, smart meter utility billing, agricultural IoT sensor-triggered insurance payouts.

Integration pattern:
```python
# chain/dag/hedera.py
from hashgraph import HederaClient, AccountId, TransferTransaction, Hbar

class HederaSettlement:
    def __init__(self, operator_id: str, operator_key: str, network: str = "mainnet"):
        self.client = HederaClient.for_mainnet() if network == "mainnet" \
                      else HederaClient.for_testnet()
        self.client.set_operator(AccountId.from_string(operator_id), operator_key)

    async def transfer_hgusd(
        self,
        from_account: str,
        to_account: str,
        amount_usd: Decimal,
        memo: str
    ) -> str:
        """
        Transfer HGUSD stablecoin on Hedera.
        Returns consensus transaction ID.
        """
        tx = (
            TransferTransaction()
            .add_token_transfer(HGUSD_TOKEN_ID, AccountId.from_string(from_account), -int(amount_usd * 100))
            .add_token_transfer(HGUSD_TOKEN_ID, AccountId.from_string(to_account),   int(amount_usd * 100))
            .set_transaction_memo(memo)
        )
        receipt = await tx.execute(self.client)
        return str(receipt.transaction_id)
```

**`chain.defi_bridge`** — DeFi protocol integration  
Permissioned DeFi access: each external protocol must be whitelisted by vault governance before capital can be deployed. Supported protocols (v1):
- Aave v3 (supply, borrow, repay)
- Compound v3 (supply, borrow)
- Uniswap v4 (swap, LP provision)
- Curve Finance (stablecoin LP)
- Lido (ETH staking → stETH)
- Yearn Finance (vault strategies)

Each interaction generates a DefiActivity VC — a verifiable record of the action for audit and tax purposes, issued by the vault's signing key.

**`chain.zk_compliance`** — Zero-knowledge regulatory compliance  
ZK proof generation for regulatory requirements that require disclosure without full data exposure:
- Age proof: prove "member is over 18" without revealing DOB
- Residency proof: prove "member is resident of Canada" without revealing address
- AML proof: prove "member passed AML screening" without revealing screening database match
- Accreditation proof: prove "member meets accredited investor threshold" without revealing net worth
- Sanctions screening: prove "member is not on OFAC/UN sanctions list" using ZK set membership proof

Circuit implementations: SnarkJS (Groth16), with Circom circuits published open-source.

**`chain.cross_chain`** — Cross-chain bridging and atomic swaps  
Atomic swaps between chains without centralized bridge risk. Supported chains: Ethereum, Polygon, Optimism, Arbitrum, Solana, Hedera, IOTA, BNB Chain. Bridge protocols: LayerZero (message passing), Chainlink CCIP (cross-chain interoperability), Wormhole (Solana bridge).

**`chain.dao_governance`** — On-chain governance integration  
Full on-chain governance for vaults that want maximum decentralization: proposals, votes, and executions all recorded on-chain. Compatible with Snapshot (off-chain signaling) and Tally (on-chain execution). Delegation support: members can delegate their governance weight to another member's DID.

---

## 3. Professional UI Standards by Banking Vertical

Each vault type renders a distinct professional interface. The application detects the vault type at login and loads the appropriate UI profile.

### 3.1 UI Theme Architecture

```typescript
// app/themes/vault-theme.ts

export type VaultTheme = {
  vaultType: VaultType;
  palette: ColorPalette;
  typography: TypographyProfile;
  navigation: NavigationProfile;
  density: 'compact' | 'standard' | 'spacious';
  moduleOrder: string[];
}

const themes: Record<VaultType, VaultTheme> = {
  FAMILY: {
    palette: { primary: '#0F7B5C', accent: '#B8860B', surface: 'neutral' },
    typography: { display: 'Playfair Display', body: 'Inter' },
    navigation: { style: 'bottom-tab', maxTabs: 5 },
    density: 'standard',
  },
  RETAIL: {
    palette: { primary: '#1A56DB', accent: '#0EA5E9', surface: 'cool-neutral' },
    typography: { display: 'DM Sans', body: 'DM Sans' },
    navigation: { style: 'side-drawer', maxTabs: 8 },
    density: 'standard',
  },
  INVESTMENT: {
    palette: { primary: '#0F172A', accent: '#F59E0B', surface: 'dark-premium' },
    typography: { display: 'IBM Plex Sans', body: 'IBM Plex Sans' },
    navigation: { style: 'top-nav-desktop', maxTabs: 10 },
    density: 'compact',
  },
  PRIVATE: {
    palette: { primary: '#1C1917', accent: '#D4AF37', surface: 'warm-ivory' },
    typography: { display: 'Cormorant Garamond', body: 'Raleway' },
    navigation: { style: 'side-nav-minimal', maxTabs: 6 },
    density: 'spacious',
  },
  COMMUNITY: {
    palette: { primary: '#059669', accent: '#6366F1', surface: 'warm-green' },
    typography: { display: 'Nunito', body: 'Nunito' },
    navigation: { style: 'bottom-tab-with-drawer', maxTabs: 6 },
    density: 'standard',
  },
  NEOBANK: {
    palette: { primary: '#7C3AED', accent: '#06B6D4', surface: 'pure-white' },
    typography: { display: 'Syne', body: 'Outfit' },
    navigation: { style: 'bottom-tab-minimal', maxTabs: 5 },
    density: 'standard',
  },
  // ... other vault types
};
```

### 3.2 InvestDesk — Professional Trading Interface

The InvestDesk module renders a professional-grade trading and portfolio management interface comparable to Bloomberg, Fidelity, or a private brokerage portal.

**Layout (desktop):**
```
┌─────────────────────────────────────────────────────────┐
│  NAVIGATION RAIL (left, 64px)                           │
│  Portfolio | Markets | Orders | Research | DeFi | NFTs  │
├──────────────┬──────────────────────┬───────────────────┤
│  WATCHLIST   │  MAIN CANVAS         │  ORDER PANEL      │
│  (240px)     │  (fills)             │  (320px)          │
│              │                      │                   │
│  Asset list  │  Chart / screener /  │  Order ticket     │
│  with live   │  portfolio view /    │  Position detail  │
│  prices      │  research feed       │  P&L calculator   │
│              │                      │                   │
├──────────────┴──────────────────────┴───────────────────┤
│  POSITIONS BAR — scrollable horizontal position summary  │
└─────────────────────────────────────────────────────────┘
```

**Key screens:**

*Portfolio overview:*
- Asset allocation donut chart (traditional / crypto / DeFi / alternatives / cash)
- Performance chart: daily / MTD / YTD / inception; benchmark comparison
- Top holdings table: position, weight, day change, unrealized P&L
- Risk metrics: portfolio volatility, Sharpe ratio, max drawdown, beta
- Income forecast: projected dividends, staking rewards, DeFi yield

*Market / Screener:*
- Global search: all asset classes in one search bar (stocks, ETFs, bonds, crypto, DeFi pools)
- Screener filters: market cap, P/E, dividend yield, sector, ESG score, TVL (for DeFi), chain
- Watchlist management: custom lists with price alerts

*Order ticket:*
- Asset: auto-populated from search or watchlist
- Order type: Market / Limit / Stop / Trailing Stop / TWAP / DCA schedule
- Quantity: shares, dollars, or percentage of portfolio
- Routing: traditional broker-dealer (regulated securities) / DEX (crypto/DeFi)
- Governance gate: display "This order requires vault governance approval" if above threshold
- Fee preview: commission, spread, gas estimate (for on-chain orders)

*DeFi Yield desk:*
- Protocol cards: each whitelisted protocol shown with current APY, TVL, audit status, risk rating
- Position management: current allocations with claimable yield displayed
- Yield calendar: projected income by date
- One-click harvest and compound
- Protocol risk scorecard: smart contract audit, TVL stability, impermanent loss calculator

*NFT Asset vault:*
- Gallery view: owned NFTs with current floor price and estimated value
- Loan NFT manager: held mortgage and corporate loan NFTs with payment schedule
- Fractionalize: wrap NFT into ERC-20 for liquidity
- Marketplace listing: list NFTs for secondary sale directly from vault
- Ownership certificate viewer: cooperative shares, fund interests, real estate fractional tokens

### 3.3 Private Banking Interface

The Private Banking vault renders a luxury, editorial-quality interface designed for HNW clients.

**Design principles:**
- Generous whitespace and serif typography (Cormorant Garamond for headings)
- Gold accent (#D4AF37) on dark neutral base
- No notification badges or urgency — calm confidence
- Data density: minimal on overview, full detail one tap deeper
- Relationship manager always accessible in top-right corner

**Key screens:**

*Wealth overview:*
- Net worth headline: one large number, updated daily (not real-time — reduces anxiety)
- Asset waterfall: a vertical bar chart showing progression from gross assets → liabilities → liquid net worth
- Projected wealth at 10 / 20 / 30 years with configurable assumptions
- Family impact score: philanthropy dollars deployed, ESG portfolio alignment

*Alternatives portfolio:*
- Fund interests: PE, VC, hedge fund allocations with J-curve visualization
- Real estate: property photos + tokenized value + rental yield
- Art and collectibles: gallery-style display with authentication VC and estimated value
- Vintage assets: wine, whisky, classic cars — vault inventory with provenance NFT

*Family office — trust management:*
- Trust structure visualization: family tree overlaid with trust connections
- Asset flows: arrows showing income distribution rules
- Generation wealth timeline: projected wealth at each generation with configurable scenarios
- Document vault: estate plan, will, trust deeds — access with biometric auth

### 3.4 Community Bank Interface

**Design principles:**
- Approachable, warm green palette
- Nunito typeface — friendly, round, accessible
- Emphasis on community features: circle participation, member count, collective savings
- Multilingual: English, French, Haitian Creole (HC) by default; extensible

**Key screens:**

*Community dashboard:*
- Vault stats: total members, collective deposits, total loans outstanding, loans funded this month
- Your position: your deposits, loans, circle participations, governance weight
- Community feed: recent vault activity (anonymized) — "A member received a $2,500 micro-loan," "SavingsCircle Round 4 paid out"
- Active proposals: one-tap voting from dashboard

*SavingsCircle (ROSCA) manager:*
- My circles: list of circles with current round, next payout date, my contribution status
- Circle detail: animated rotation wheel showing member order, countdown to next payout
- Payment: one-tap contribution with confirmation
- History: all past contributions and payouts with verifiable on-chain receipts
- Create a circle: wizard — name, members (search by DID), contribution amount, period, rotation order

*Cooperative lending desk:*
- Loan calculator: enter amount, see estimated rate, monthly payment, total cost
- Apply: 4-step application using VCs for identity and income proof
- My loans: repayment schedule, make payment, extra payment option
- Lending pool health: total pool, amount deployed, default rate, my share

### 3.5 Development Bank Interface

**Design principles:**
- Data-rich, mission-focused
- Map integration: project portfolio shown on geographic map
- Impact metrics prominently displayed alongside financial metrics
- Grant and project management UX drawn from project management tools

**Key screens:**

*Project portfolio map:*
- Interactive map (MapboxGL): each funded project shown as pin with status color
- Click pin: project card — name, borrower, amount, milestone status, impact metrics
- Filter: by sector, country, status, SDG alignment

*Impact dashboard:*
- SDG alignment chart: UN Sustainable Development Goal categories with deployed capital
- Impact metrics: jobs created, hectares irrigated, households electrified, CO2 offset
- Carbon credit portfolio: tokenized carbon credits with current market value
- Impact report generator: auto-generate PDF report for LPs, donors, or regulatory reporting

*Grant management desk:*
- Application pipeline: Kanban board — Received → Under review → Due diligence → Awarded → Monitoring
- Grant agreement: DID-signed document with milestones as smart contract checkpoints
- Disbursement queue: milestone verification → funds release
- Grantee portal: grantees submit progress reports (attested as VCs) to trigger disbursements

---

## 4. Blockchain & DLT Architecture

### 4.1 Multi-Chain Settlement Strategy

Lakou routes transactions to the optimal chain based on:
- Transaction type (high-value vs. micro)
- Speed requirements (real-time vs. T+1)
- Privacy requirements (ZK-enabled chains)
- Cost (gas fees vs. DAG fees)
- Counterparty chain preference

```
┌─────────────────────────────────────────────────────────────┐
│                  Lakou Settlement Router                     │
├──────────────┬──────────────┬──────────────┬────────────────┤
│  Ethereum    │  Polygon PoS │  Hedera      │  IOTA Tangle   │
│  (L1 anchor) │  (retail TX) │  (remittance │  (micro/IoT)   │
│  governance  │  DeFi/NFTs   │   & fast pay │                │
├──────────────┴──────────────┴──────────────┴────────────────┤
│  Optimism L2 │  Solana      │  Cross-chain layer (CCIP)     │
│  (rollup     │  (DEX/NFT    │  LayerZero message passing    │
│   batching)  │   marketplace│                               │
└──────────────┴──────────────┴───────────────────────────────┘
```

**Routing logic:**

| Transaction type | Chain | Reason |
|---|---|---|
| Governance proposals + votes | Ethereum | Security, immutability |
| Module Registry | Polygon | Low gas, EVM compatible |
| Retail transfers < $1,000 | Hedera HBAR | Fast, cheap, finality |
| Remittance (HGUSD) | Hedera | 10,000 TPS, USDC partnership |
| DeFi operations | Polygon / Optimism | EVM, DeFi ecosystem |
| NFT minting | Polygon / Solana | Low mint cost |
| IoT micro-payments | IOTA Tangle | Feeless, M2M |
| High-value settlement > $100K | Ethereum | Security-grade finality |
| Cross-chain bridges | CCIP (Chainlink) | Audited, insured bridges |

### 4.2 DAG Transaction Architecture

Directed Acyclic Graph networks eliminate the traditional blockchain bottleneck (linear blocks). In a DAG:
- Each transaction references 2+ prior transactions (rather than a block)
- Transactions validate each other — no miners or validators needed for basic settlement
- Throughput scales with network activity (more transactions = faster confirmation)

**Hedera Hashgraph integration:**

Hedera uses a DAG-based gossip protocol (hashgraph consensus) achieving:
- 10,000+ TPS sustained throughput
- 3–5 second absolute finality
- Transaction fees: $0.0001 per transaction (fixed, not gas auction)
- HBAR stablecoin: USDC is natively supported on Hedera Token Service (HTS)

Lakou deploys HGUSD as an HTS token (Hedera Token Service) — the same framework USDC uses on Hedera. Transfers are HTS token transfers, not EVM transactions, achieving sub-second confirmation at USD fractions of a cent per transaction.

**IOTA Tangle for DePIN integration:**

IOTA's Tangle is a DAG where each transaction approves two prior ones. No fees. Used for:
- D-Central ISP nodes billing: each 1 MB of bandwidth transferred → one micropayment transaction on IOTA
- Smart meter utility billing: second-by-second electricity metering settled via IOTA
- Agricultural sensor payouts: soil moisture sensor data → parametric insurance payout trigger

**Scope note:** this is IoT/metering-rail DePIN (bandwidth billing, sensor payouts) — distinct from compute DePIN
(GPU/FPGA/ASIC node operators serving AI inference), specified separately in
[DC-COMPUTE-SILICON-ARCH-001](DC-COMPUTE-SILICON-ARCH-001.md).

### 4.3 NFT Financial Instrument Standards

**ERC-721: Unique Asset NFTs**
Used for: unique real estate properties, unique fine art, specific loan agreements, membership certificates with individual history.

**ERC-1155: Multi-Edition and Semi-Fungible NFTs**
Used for: cooperative share certificates (all shares of a given class are identical), carbon credits (all credits from a project batch are fungible), insurance policy certificates.

**ERC-3525: Semi-Fungible Tokens (Loan NFTs)**

ERC-3525 introduces a "slot" concept making it ideal for financial instruments:
```
LoanNFT {
  tokenId: unique identifier for this specific loan
  slot: loan category (e.g., "residential_mortgage_cad_2026")
  value: remaining principal in basis points
}
```

This means:
- Two mortgage loans of the same type (same slot) can be merged or split
- A $100,000 mortgage NFT can be split into 100 × $1,000 fractional tokens for investor syndication
- The value transfers (principal repayments) are tracked within the NFT without minting new tokens

Loan NFT lifecycle:
```
Loan originated → Loan NFT minted (full principal value)
  │
  ├── Loan NFT can be split into fractional tokens → sold to investors
  │   (investor holds fractional Loan NFT, receives proportional interest)
  │
  ├── Monthly repayment → principal decremented in NFT value field
  │
  ├── Loan paid off → NFT burned, release event emitted
  │
  └── Loan default → NFT transferred to liquidation contract
       → Collateral NFT liquidated via auction
```

**Identity NFTs (SBTs — Soulbound Tokens)**

Based on EIP-4973, Identity NFTs are non-transferable attestation tokens bound to a member's address:
- KYC completion SBT: issued by trusted KYC provider, records verification level
- Professional credential SBT: CPA, CFP, lawyer — issued by professional bodies
- Impact participation SBT: records community banking contributions, ROSCA completions
- Loan repayment SBT: records on-time payment history for alternative credit scoring

### 4.4 DeFi Integration Architecture

```
LakouVault
  │
  ├── DeFi Bridge Contract (per vault, deployed on Polygon/Optimism)
  │     │
  │     ├── Protocol Whitelist (governane-controlled mapping)
  │     │     ├── Aave v3 Pool → approved (60% quorum vote)
  │     │     ├── Compound v3 → approved
  │     │     └── Uniswap v4 → approved
  │     │
  │     ├── Allocation Limits (per-protocol, per-asset, set by governance)
  │     │
  │     ├── Harvest & Compound Automation (Gelato Network keeper)
  │     │
  │     └── Emergency Exit (any 51% quorum can pull all DeFi positions)
  │
  └── Yield Distribution Contract
        └── DeFi yield → allocated per member according to deposit weight
```

**AMM Liquidity Pool (Internal FX):**

For vaults operating multiple currencies (common in the Haiti corridor), Lakou deploys an internal Uniswap v4 pool as a vault-controlled AMM:
- Pool pair: HGUSD / USDC
- Liquidity provided by vault treasury and optionally by members
- Members transact at AMM price with no spread markup
- LP fees (0.05%) accrue to vault treasury
- Slippage protection: orders above pool depth threshold route to external exchange

---

## 5. Scalability Architecture

### 5.1 Deployment Models

**Model A — Hosted by Lakou Foundation**  
Suitable for: family vaults, small community vaults (<1,000 members), development phase  
- Vault smart contracts on Polygon mainnet
- API server: Lakou Foundation-managed (multi-region, auto-scaling)
- Data: encrypted vault data on Lakou Foundation servers
- Cost: monthly per-vault subscription fee

**Model B — Self-Hosted (Institutional)**  
Suitable for: community banks with >1,000 members, commercial vaults, regulatory-compliant entities  
- Vault smart contracts on any EVM chain (vault operator's choice)
- API server: operator-deployed via Lakou OS Docker image or Kubernetes helm chart
- Data: operator-controlled PostgreSQL + IPFS node
- Cost: open-source license (AGPL-3.0), no platform fee

**Model C — D-Central Node-Anchored**  
Suitable for: Haiti corridor, underserved markets, offline-capable deployments  
- Vault contract on Hedera (low-cost, high-throughput)
- API server: runs on D-Central ISP nodes (OpenWrt + Docker)
- Data: replicated across D-Central mesh nodes (IPFS)
- Settlement: IOTA Tangle for micro-transactions, Hedera for larger settlements
- Offline-capable: 72-hour transaction queue survives connectivity outages

### 5.2 Database Architecture

```
Per-vault database (PostgreSQL, encrypted at rest):
  ├── members               — member profiles, roles, VC references
  ├── accounts              — financial accounts with encrypted balance history
  ├── transactions          — double-entry ledger
  ├── proposals             — governance proposal data
  ├── votes                 — vote records (on-chain anchored)
  ├── nft_holdings          — vault's NFT inventory with metadata
  └── defi_positions        — current DeFi protocol allocations

Shared infrastructure (chain-indexed, The Graph):
  ├── vault_registry        — all vault addresses and types
  ├── module_registry       — module versions and deployments
  ├── governance_events     — all on-chain governance activity
  └── settlement_events     — cross-vault transfers and remittances

Analytics layer (ClickHouse — append-only):
  ├── transaction_analytics — aggregate spending patterns (anonymized)
  ├── portfolio_analytics   — portfolio performance time series
  └── impact_metrics        — development bank impact data
```

### 5.3 Multi-Tenant Isolation

Each vault is a logically isolated tenant:
- Database: per-vault schema namespace (not row-level isolation — full schema separation)
- Encryption: per-vault encryption key derived from vault DID signing key
- Smart contracts: each vault has its own deployed Governor + module proxy (no shared state)
- API: vault_id is part of every JWT claim; middleware validates on every request

Cross-vault operations (SavingsCircle cross-vault, RemittanceGate, inter-vault lending) use a dedicated cross-vault bridge contract that maintains atomic settlement between isolated vaults.

---

## 6. Regulatory and Compliance Architecture

### 6.1 Modular Compliance Profiles

Different vault types operate under different regulatory frameworks. The compliance profile is a module-level configuration:

| Module | Regulatory Framework | Compliance Mechanism |
|---|---|---|
| Any financial module | AML/KYC (FATF Rec. 10) | KYC Attestation VC from licensed issuer |
| Retail banking | Deposit insurance (CDIC/FDIC) | Deposits held at licensed bank partner |
| RemittanceGate | Money service business (FINTRAC/FinCEN) | MSB registration + Travel Rule via VC |
| InvestDesk (securities) | Securities regulation (SEC/IIROC) | Broker-dealer API partner |
| InvestDesk (crypto) | Self-custodied wallet (no license) | Wallet held by member DID |
| CommercialDesk | Business banking (chartered bank) | Chartered bank partner holds deposits |
| MortgageDesk | Mortgage broker/lender license | State/provincial license per jurisdiction |
| InsuranceVault (licensed product) | Insurance regulatory approval | Licensed insurer partner |
| StablecoinIssuance | Electronic money institution (EMI) | EMI license or exempt (< threshold) |

### 6.2 Travel Rule Compliance (FATF Rec. 16)

For cross-vault transfers and remittances above threshold ($3,000 CAD):

```json
{
  "travel_rule_data": {
    "originator": {
      "did": "did:web:lakou.jb-family.ca",
      "member_did": "did:key:z6MkrZ1...",
      "name": "Toussaint Jean Baptiste",
      "account_number": "acct_001",
      "jurisdiction": "CA"
    },
    "beneficiary": {
      "did": "did:key:z6MkrZ2...",
      "name": "Marie Jean Baptiste",
      "account_jurisdiction": "HT"
    },
    "transaction_amount": "250.00",
    "transaction_currency": "CAD",
    "settlement_asset": "HGUSD"
  }
}
```

Travel Rule data is transmitted using the TRUST protocol (Travel Rule Universal Solution Technology) — a VC-based travel rule data exchange standard — between originating and beneficiary vault systems.

---

## 7. Integration with D-Central Ecosystem

| D-Central Product | Integration |
|---|---|
| D-Central ISP | Settlement routing node, IOTA micropayment integration, offline transaction relay |
| HomeDAO | Governance token interop — household votes contribute to community vault proposals |
| HMCS | Household expense data feeds `neo.budgeting` and `treasury.taxledger` automatically |
| OpenSecure Platform | Physical access badge controlled by vault membership VC |
| Haiti CIN | Government DID as primary identity anchor for Haitian diaspora members |
| Haiti–Diaspora Value Loop | HGUSD stablecoin issuance and peg management |
| Sovereign DAO OS | Vault governance contracts are Sovereign DAO OS modules |
| MeshTelecomDAO | D-Central node operators earn HGUSD routing fees for remittance traffic |
| D-Central Hardware | Hardware wallet integration: signing keys stored in D-Central custom hardware HSM |

---

## 8. Roadmap (v2)

### Phase 1 — Core Protocol (Q3 2026)
- Vault Factory smart contract (all 9 vault types deployable)
- External membership model live
- LMIS v1.1 (updated for v2 modules)
- Hedera HGUSD stablecoin (HTS deployment)
- InvestDesk v1: equity + crypto (broker-dealer API)
- Community vault type: open membership credit union

### Phase 2 — DLT Stack (Q4 2026)
- Hedera DAG settlement for all HGUSD remittances
- IOTA integration for D-Central micropayments
- ERC-3525 Loan NFT for mortgages and corporate loans
- NFT Asset Vault module
- DeFi Bridge: Aave + Uniswap (whitelist governance)
- Cross-chain bridge (Chainlink CCIP)

### Phase 3 — Full Module Suite (Q1–Q2 2027)
- All 45+ modules available in registry
- Private banking vault type: alternatives + concierge
- Development banking vault: project finance + impact metrics
- DAO Treasury vault type
- ZK compliance proofs for all modules

### Phase 4 — Professional Applications (Q3 2027)
- Bloomberg-grade InvestDesk desktop UI
- Community bank branch management console
- Private bank relationship manager CRM integration
- Mobile app localized: English, French, Haitian Creole, Spanish, Portuguese
- Offline-capable desktop (Tauri) with 72-hour transaction queue

### Phase 5 — Ecosystem Integration (2028)
- Full D-Central node network as settlement infrastructure
- Haiti CIN integration for diaspora onboarding
- D-Central Hardware HSM for key management
- Inter-vault credit lines (community banks extend credit to each other)
- Lakou Network Effect: cross-vault SavingsCircles, syndicated loans

---

## Appendix A — Full Module Registry (v2)

| Module ID | Name | Vertical | Requires |
|---|---|---|---|
| `retail.checking` | Checking & debit | Retail | KYCAttestation |
| `retail.savings` | Savings & CDs | Retail | KYCAttestation |
| `retail.mortgage` | Mortgage origination | Retail | KYCAttestation |
| `retail.personal_loan` | Personal loans | Retail | KYCAttestation |
| `retail.card` | Credit cards | Retail | KYCAttestation |
| `retail.insurance` | Retail insurance | Retail | KYCAttestation |
| `commercial.cash` | Cash management | Commercial | KYC + BusinessReg |
| `commercial.trade` | Trade finance | Commercial | KYC + BusinessReg |
| `commercial.lending` | Corporate lending | Commercial | KYC + BusinessReg |
| `commercial.cre` | Commercial real estate | Commercial | KYC + BusinessReg |
| `commercial.payroll` | Payroll & HR banking | Commercial | KYC + BusinessReg |
| `commercial.merchant` | Merchant acquiring | Commercial | KYC + BusinessReg |
| `invest.equity` | Equity trading | Investment | KYC + AccreditedInvestor |
| `invest.fixed_income` | Fixed income | Investment | KYC |
| `invest.derivatives` | Derivatives | Investment | KYC + AccreditedInvestor |
| `invest.crypto` | Crypto spot | Investment | KYC |
| `invest.defi` | DeFi yield | Investment | KYC |
| `invest.ipo` | IPO desk | Investment | KYC + AccreditedInvestor |
| `invest.capital_markets` | Capital markets | Investment | KYC + AccreditedInvestor |
| `invest.ma` | M&A deal room | Investment | KYC + AccreditedInvestor |
| `coop.membership` | Member equity shares | Cooperative | KYC |
| `coop.lending` | Cooperative lending | Cooperative | KYC |
| `coop.rosca` | SavingsCircle / ROSCA | Cooperative | KYC |
| `coop.insurance` | Insurance pool | Cooperative | KYC |
| `coop.dividends` | Dividend distribution | Cooperative | KYC |
| `private.wealth` | Wealth management | Private | KYC |
| `private.office` | FamilyOffice | Private | KYC |
| `private.alternatives` | Alternatives (PE/VC) | Private | KYC + AccreditedInvestor |
| `private.philanthropy` | Philanthropy desk | Private | KYC |
| `private.concierge` | Concierge finance | Private | KYC |
| `sl.thrift` | Thrift operations | S&L | KYC |
| `sl.mortgage_pool` | Mortgage savings pool | S&L | KYC |
| `dev.project` | Project finance | Development | KYC + StakeholderVC |
| `dev.agriculture` | Agriculture lending | Development | KYC |
| `dev.impact` | Impact investing | Development | KYC |
| `dev.microfinance` | Microfinance | Development | KYC |
| `dev.grants` | Grant management | Development | KYC + OrgCredential |
| `neo.instant_pay` | Instant pay rails | Neobank | KYC |
| `neo.virtual_card` | Virtual cards | Neobank | KYC |
| `neo.open_banking` | Open banking API | Neobank | KYC |
| `neo.budgeting` | AI budgeting | Neobank | KYC |
| `treasury.reserve` | Reserve management | DAO Treasury | KYC + DAOMembership |
| `treasury.stablecoin` | Stablecoin issuance | DAO Treasury | KYC + EMIExemption |
| `treasury.monetary_policy` | Monetary policy params | DAO Treasury | KYC + DAOMembership |
| `chain.nft_assets` | NFT asset vault | Blockchain | KYC |
| `chain.dag` | DAG settlement | Blockchain | KYC |
| `chain.defi_bridge` | DeFi protocol bridge | Blockchain | KYC |
| `chain.zk_compliance` | ZK compliance proofs | Blockchain | None |
| `chain.cross_chain` | Cross-chain bridge | Blockchain | KYC |
| `chain.dao_governance` | On-chain governance | Blockchain | KYC + DAOMembership |
| `infra.remittance` | RemittanceGate | Infrastructure | KYC |
| `infra.tax` | TaxLedger | Infrastructure | KYC |
| `infra.reserve_mgmt` | Reserve management | Infrastructure | KYC + OwnerRole |

---

## Appendix B — Document History

| Version | Date | Changes |
|---|---|---|
| 0.1 | 2026-05-05 | Initial v2 protocol design — universal banking OS expansion |

---

*Lakou Protocol v2 is a component of the D-Central Ecosystem.*  
*Document ID: DC-LKB-003 · Extends: DC-LKB-001, DC-LKB-002*  
*Author: Toussaint Redji Jean Baptiste*
