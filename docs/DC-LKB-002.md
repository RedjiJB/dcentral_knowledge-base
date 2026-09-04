---
source_conversation: Decentralized family banking framework with modular services
source_conversation_uuid: 76d91c3d-0b67-437f-a5dc-e5841bc93104
original_filename: DC-LKB-002_Lakou_Technical_Specification.md
created_at: 2026-05-05T23:05:27.404999Z
content_hash: 9ffd6d8db9f9
extraction_note: "Pulled from an artifact created inline in this conversation (create_file tool call), not from a Claude Project knowledge-base doc -- Stage 1/2 extraction only covered Project KB docs, this is a manual follow-up extraction."
---

# Lakou — Technical Specification

**Document ID:** DC-LKB-002  
**Version:** 0.1  
**Author:** Toussaint Redji Jean Baptiste  
**Depends on:** DC-LKB-001 (Lakou Concept Document)  
**Status:** Draft  
**Date:** 2026-05-05

---

## Table of Contents

1. [API Architecture](#1-api-architecture)
2. [Governance Token Model](#2-governance-token-model)
3. [Lakou Module Interface Standard (LMIS)](#3-lakou-module-interface-standard-lmis)
4. [Companion App UX Flows](#4-companion-app-ux-flows)

---

## 1. API Architecture

### 1.1 Design Philosophy

The Lakou API is a **module-scoped, DID-authenticated REST + WebSocket API** built on FastAPI. Every endpoint is either public (unauthenticated, read-only vault metadata), member-scoped (authenticated, per-vault), or module-scoped (requires the corresponding module to be enabled in the requesting vault).

The API surface is additive: enabling a module in a vault registers its endpoint group. Disabling a module removes access without deleting data (data is vaulted in IPFS-pinned, vault-key-encrypted blobs; the module's on-chain state is paused, not deleted).

**Key design decisions:**

- No API keys. Authentication is purely DID-based: `DID-Auth-Challenge` → `DPoP-bound JWT`
- Vault-level encryption at rest. The API server never holds decryption keys for vault data — it holds ciphertext and indexes
- Every mutating endpoint requires a `X-Vault-Nonce` header (monotonically incrementing per-vault, prevents replay attacks)
- Endpoints are versioned under `/v1/`. Breaking changes bump to `/v2/`

---

### 1.2 Authentication Flow

Lakou uses a **DID-Auth challenge-response** flow producing a DPoP-bound access token.

```
Client                              API Server
  |                                      |
  |─── POST /v1/auth/challenge ─────────>|
  |    { did: "did:web:alice.example" }  |
  |                                      |
  |<── 200 { challenge: "<nonce>",       |
  |          expiry: <unix_ts> }         |
  |                                      |
  |  Client signs: {                     |
  |    did, challenge, timestamp,        |
  |    jwk_thumbprint(dpop_key)          |
  |  } using DID verification method    |
  |                                      |
  |─── POST /v1/auth/token ─────────────>|
  |    DPoP: <proof_jwt>                 |
  |    Body: { did, signed_challenge }   |
  |                                      |
  |<── 200 {                             |
  |      access_token: <jwt>,            |
  |      token_type: "DPoP",            |
  |      expires_in: 3600,              |
  |      scope: "vault:read vault:write  |
  |             module:retail            |
  |             module:remittance"       |
  |    }                                 |
```

**Token claims (JWT payload):**

```json
{
  "sub": "did:web:alice.example",
  "vault_id": "0xVAULT_ADDRESS",
  "member_role": "owner",
  "module_scopes": ["retail", "remittance", "savings_circle"],
  "governance_weight": 400,
  "cnf": { "jkt": "<dpop_key_thumbprint>" },
  "iat": 1746486000,
  "exp": 1746489600,
  "jti": "<uuid>"
}
```

**DPoP proof (per-request header):**

```json
{
  "typ": "dpop+jwt",
  "alg": "ES256",
  "jwk": { "<public_key>" }
}
{
  "htm": "POST",
  "htu": "https://api.lakou.family/v1/retail/transfer",
  "iat": 1746486120,
  "jti": "<per-request-uuid>",
  "ath": "<sha256(access_token)>"
}
```

---

### 1.3 Base URL Structure

```
https://api.lakou.family/v1/
  auth/          — DID-Auth challenge/token endpoints
  vault/         — Vault metadata, member management, governance
  retail/        — RetailVault module endpoints
  credit/        — CreditCircle module endpoints
  remittance/    — RemittanceGate module endpoints
  savings/       — SavingsCircle module endpoints
  invest/        — InvestDesk module endpoints
  office/        — FamilyOffice module endpoints
  commercial/    — CommercialDesk module endpoints
  tax/           — TaxLedger module endpoints
  insurance/     — InsuranceVault module endpoints
  private/       — PrivateDesk module endpoints
  ws/            — WebSocket upgrade endpoints
```

---

### 1.4 Common Schemas

All responses wrap a `data` envelope with a `meta` block:

```json
{
  "data": { ... },
  "meta": {
    "vault_id": "0x...",
    "request_id": "<uuid>",
    "timestamp": "2026-05-05T09:41:00Z",
    "api_version": "1.0.0"
  }
}
```

**Error schema (RFC 7807 Problem Details):**

```json
{
  "type": "https://api.lakou.family/errors/module-not-enabled",
  "title": "Module not enabled",
  "status": 403,
  "detail": "The InvestDesk module is not enabled for vault 0x...",
  "instance": "/v1/invest/portfolio",
  "vault_id": "0x..."
}
```

**Standard error codes:**

| Code | HTTP | Meaning |
|---|---|---|
| `auth.challenge_expired` | 401 | DID-Auth challenge nonce expired (60s window) |
| `auth.did_mismatch` | 401 | Signed DID does not match token subject |
| `auth.dpop_invalid` | 401 | DPoP proof invalid or replayed |
| `vault.not_found` | 404 | Vault address not registered |
| `vault.quorum_required` | 403 | Action requires a governance vote to proceed |
| `module.not_enabled` | 403 | Module not enabled in this vault |
| `module.pending_vote` | 202 | Module enable/disable vote is in progress |
| `nonce.replay` | 409 | X-Vault-Nonce already consumed |
| `credential.missing` | 403 | Required VC not presented |
| `credential.expired` | 403 | Required VC has expired |

---

### 1.5 Endpoint Catalog

#### `/v1/auth/`

| Method | Path | Auth | Description |
|---|---|---|---|
| `POST` | `/challenge` | None | Request DID-Auth challenge nonce |
| `POST` | `/token` | DPoP + signed challenge | Exchange for DPoP-bound JWT |
| `POST` | `/refresh` | DPoP + refresh token | Refresh access token |
| `DELETE` | `/token` | Bearer | Revoke current token |

#### `/v1/vault/`

| Method | Path | Auth | Description |
|---|---|---|---|
| `GET` | `/` | Bearer | Get vault metadata, module list, governance summary |
| `GET` | `/members` | Bearer | List vault members with roles and governance weights |
| `POST` | `/members/invite` | Bearer + Owner role | Initiate member onboarding with VC verification |
| `DELETE` | `/members/{did}` | Bearer + 67% quorum | Remove a member (triggers governance vote) |
| `GET` | `/modules` | Bearer | List all modules, enabled state, version |
| `POST` | `/modules/{module_id}/enable` | Bearer | Initiate governance proposal to enable module |
| `POST` | `/modules/{module_id}/disable` | Bearer | Initiate governance proposal to disable module |
| `GET` | `/proposals` | Bearer | List all governance proposals |
| `GET` | `/proposals/{id}` | Bearer | Get proposal detail with vote tally |
| `POST` | `/proposals/{id}/vote` | Bearer | Cast a vote (support: 0=against, 1=for, 2=abstain) |
| `POST` | `/proposals/{id}/execute` | Bearer | Execute a passed proposal post-timelock |
| `GET` | `/audit` | Bearer + Owner | Paginated audit log of all vault events |

**`GET /v1/vault/` response:**

```json
{
  "data": {
    "vault_id": "0xABCD...",
    "family_did": "did:web:lakou.jb-family.ca",
    "vault_name": "Jean Baptiste Family Vault",
    "created_at": "2026-01-15T00:00:00Z",
    "member_count": 4,
    "governance_model": "hybrid",
    "quorum_threshold": 0.60,
    "enabled_modules": ["retail", "credit", "savings_circle", "remittance"],
    "net_worth_cad": "47238.50",
    "pending_proposals": 2,
    "chain": "polygon",
    "contract_address": "0xABCD..."
  }
}
```

#### `/v1/retail/`

| Method | Path | Description |
|---|---|---|
| `GET` | `/accounts` | List all accounts (checking, savings, etc.) |
| `POST` | `/accounts` | Open a new sub-account |
| `GET` | `/accounts/{id}` | Account detail with balance and recent transactions |
| `GET` | `/accounts/{id}/transactions` | Paginated transaction history |
| `POST` | `/transfer` | Internal transfer between vault accounts |
| `POST` | `/external-transfer` | Transfer to external account (ACH/Interac) |
| `GET` | `/cards` | List virtual and physical debit cards |
| `POST` | `/cards` | Request a new virtual card |
| `POST` | `/cards/{id}/freeze` | Freeze a card |
| `PUT` | `/savings-rules` | Update automated savings sweep rules |

**`POST /v1/retail/transfer` request:**

```json
{
  "from_account": "acct_checking_001",
  "to_account": "acct_savings_001",
  "amount": "500.00",
  "currency": "CAD",
  "memo": "Monthly savings sweep",
  "idempotency_key": "<uuid>"
}
```

Headers required:
```
Authorization: DPoP <access_token>
DPoP: <per-request proof>
X-Vault-Nonce: 47
```

#### `/v1/remittance/`

| Method | Path | Description |
|---|---|---|
| `GET` | `/corridors` | List available corridors with current rates and fees |
| `GET` | `/quote` | Get a transfer quote (amount, fees, FX rate, ETA) |
| `POST` | `/transfer` | Initiate a remittance transfer |
| `GET` | `/transfer/{id}` | Get transfer status and lifecycle events |
| `GET` | `/recipients` | Saved recipient list (DID-linked) |
| `POST` | `/recipients` | Add a recipient (verifies their DID) |
| `GET` | `/mesh-nodes` | List available D-Central routing nodes for a corridor |

**`POST /v1/remittance/transfer` request:**

```json
{
  "recipient_did": "did:key:z6MkrZ1YaX4uXJDhe4uXJ",
  "amount": "250.00",
  "source_currency": "CAD",
  "destination_currency": "HTG",
  "corridor": "CA-HT",
  "routing_preference": "mesh",
  "memo": "May support",
  "idempotency_key": "<uuid>"
}
```

**`GET /v1/remittance/corridors` response (excerpt):**

```json
{
  "data": {
    "corridors": [
      {
        "id": "CA-HT",
        "name": "Canada → Haiti",
        "source_currency": "CAD",
        "destination_currency": "HTG",
        "fx_rate": "110.00",
        "fee_percent": "0.70",
        "min_fee_cad": "1.00",
        "settlement_asset": "HGUSD",
        "avg_arrival_minutes": 4,
        "routing_options": ["mesh", "swift"],
        "mesh_nodes_online": 3,
        "status": "operational"
      }
    ]
  }
}
```

#### `/v1/vault/proposals/{id}/vote` request:

```json
{
  "support": 1,
  "reason": "Our portfolio is large enough to benefit from ETF access",
  "vc_presentation": "<W3C VP JWT>"
}
```

The `vc_presentation` field is required if the proposal is module-gating one that requires an accreditation credential (e.g., enabling InvestDesk for accredited investor products).

#### `/v1/invest/` (requires InvestDesk module + accredited investor VC for restricted products)

| Method | Path | Description |
|---|---|---|
| `GET` | `/portfolio` | Full portfolio with positions, P&L, allocation |
| `GET` | `/instruments/search` | Search equities, ETFs, crypto, funds |
| `POST` | `/orders` | Place a market or limit order |
| `GET` | `/orders/{id}` | Order status |
| `DELETE` | `/orders/{id}` | Cancel a pending order |
| `GET` | `/defi/protocols` | List approved DeFi protocols (governance-whitelist) |
| `POST` | `/defi/stake` | Stake to a whitelisted protocol |
| `GET` | `/performance` | Time-weighted returns, benchmarks |

**Governance gate for orders:** Any single trade above the vault's `investment_approval_threshold` (configurable, default $5,000 CAD) requires a governance vote before execution. The API returns `vault.quorum_required` and a proposal is automatically drafted.

#### `/v1/office/` (FamilyOffice module)

| Method | Path | Description |
|---|---|---|
| `GET` | `/trusts` | List trust instruments |
| `POST` | `/trusts` | Draft a new trust (generates smart contract) |
| `GET` | `/trusts/{id}` | Trust detail with asset list and beneficiaries |
| `POST` | `/trusts/{id}/fund` | Transfer assets into trust |
| `GET` | `/vault-docs` | List encrypted estate documents |
| `POST` | `/vault-docs` | Upload a document (encrypted with vault key, pinned to IPFS) |
| `GET` | `/vault-docs/{id}` | Download/decrypt a document |
| `GET` | `/succession-plan` | View current succession order and trigger conditions |
| `PUT` | `/succession-plan` | Update succession order (requires 75% quorum) |

---

### 1.6 WebSocket Feeds

Connect via `wss://api.lakou.family/v1/ws/{vault_id}` with a `?token=<access_token>` query param.

**Message envelope:**

```json
{
  "type": "TRANSACTION_CONFIRMED",
  "vault_id": "0x...",
  "timestamp": "2026-05-05T09:41:22Z",
  "data": { ... }
}
```

**Event types:**

| Type | Payload | Description |
|---|---|---|
| `TRANSACTION_CONFIRMED` | transaction object | Any confirmed transaction in any account |
| `REMITTANCE_STATUS` | transfer_id, status, stage | Remittance lifecycle update |
| `PROPOSAL_CREATED` | proposal object | New governance proposal created |
| `VOTE_CAST` | proposal_id, member_did, support | A vote was cast |
| `PROPOSAL_EXECUTED` | proposal_id, result | Proposal executed (passed or failed) |
| `MEMBER_JOINED` | member_did, role | New member joined vault |
| `MODULE_ENABLED` | module_id | Module was activated |
| `PRICE_UPDATE` | instrument, price | InvestDesk price feed (rate-limited, 1/s) |
| `SAVINGS_CIRCLE_PAYOUT` | circle_id, recipient_did, amount | SavingsCircle payout event |

**Client subscription message:**

```json
{
  "action": "subscribe",
  "channels": ["transactions", "governance", "remittance"]
}
```

---

### 1.7 Rate Limiting

| Tier | Limit | Window |
|---|---|---|
| Unauthenticated | 10 requests | 1 minute |
| Authenticated (member) | 300 requests | 1 minute |
| WebSocket feed | 1 connection per vault per member | — |
| InvestDesk orders | 30 orders | 1 hour |
| Remittance transfers | 10 transfers | 1 day |

Rate limit headers on every response:
```
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 247
X-RateLimit-Reset: 1746486060
```

---

## 2. Governance Token Model

### 2.1 Token Contract (Solidity)

The governance token is an **ERC-1155 soulbound** token (non-transferable). Each vault gets its own token ID namespace. Transfer functions are overridden to revert.

```solidity
// SPDX-License-Identifier: AGPL-3.0
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC1155/ERC1155.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

/// @title LakouGovernanceToken
/// @notice Soulbound governance tokens for Lakou family vaults.
///         Each vault has its own token ID. Tokens are non-transferable.
contract LakouGovernanceToken is ERC1155, AccessControl {

    bytes32 public constant VAULT_ADMIN_ROLE = keccak256("VAULT_ADMIN_ROLE");
    bytes32 public constant MODULE_REGISTRY_ROLE = keccak256("MODULE_REGISTRY_ROLE");

    // vault address => total supply of that vault's governance tokens
    mapping(address => uint256) public vaultTotalSupply;

    // vault address => member DID hash => token balance
    // Note: we use the keccak256 of the DID string as the member key
    mapping(address => mapping(bytes32 => uint256)) public memberWeight;

    // vault address => GovernanceConfig
    struct GovernanceConfig {
        WeightModel model;
        uint256 quorumNumerator;     // e.g. 60 = 60%
        uint256 quorumDenominator;   // always 100
        uint256 timelockDelay;       // seconds
        uint256 proposalDuration;    // seconds (voting window)
        uint256 governanceAge;       // minimum age in seconds to hold voting tokens
    }

    enum WeightModel { FLAT, CONTRIBUTION, HYBRID }

    mapping(address => GovernanceConfig) public vaultConfig;

    // vault address => tokenId (unique per vault)
    mapping(address => uint256) public vaultTokenId;
    uint256 private _nextTokenId = 1;

    event VaultInitialized(address indexed vault, uint256 tokenId);
    event TokensMinted(address indexed vault, bytes32 indexed memberDidHash, uint256 amount);
    event TokensBurned(address indexed vault, bytes32 indexed memberDidHash, uint256 amount);

    constructor() ERC1155("") {
        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
    }

    /// @notice Initialize a new vault's governance token namespace
    function initVault(
        address vault,
        GovernanceConfig calldata config
    ) external onlyRole(VAULT_ADMIN_ROLE) {
        require(vaultTokenId[vault] == 0, "Vault already initialized");
        uint256 tokenId = _nextTokenId++;
        vaultTokenId[vault] = tokenId;
        vaultConfig[vault] = config;
        emit VaultInitialized(vault, tokenId);
    }

    /// @notice Mint governance tokens to a member (called by module registry on member onboard)
    function mint(
        address vault,
        bytes32 memberDidHash,
        address memberAddress,
        uint256 amount
    ) external onlyRole(VAULT_ADMIN_ROLE) {
        uint256 tokenId = vaultTokenId[vault];
        require(tokenId != 0, "Vault not initialized");
        memberWeight[vault][memberDidHash] += amount;
        vaultTotalSupply[vault] += amount;
        _mint(memberAddress, tokenId, amount, "");
        emit TokensMinted(vault, memberDidHash, amount);
    }

    /// @notice Burn tokens on member removal or succession
    function burn(
        address vault,
        bytes32 memberDidHash,
        address memberAddress,
        uint256 amount
    ) external onlyRole(VAULT_ADMIN_ROLE) {
        uint256 tokenId = vaultTokenId[vault];
        memberWeight[vault][memberDidHash] -= amount;
        vaultTotalSupply[vault] -= amount;
        _burn(memberAddress, tokenId, amount);
        emit TokensBurned(vault, memberDidHash, amount);
    }

    /// @notice SOULBOUND: Override transfer to revert for all non-mint/burn transfers
    function safeTransferFrom(
        address, address, uint256, uint256, bytes memory
    ) public pure override {
        revert("LakouGovToken: soulbound, non-transferable");
    }

    function safeBatchTransferFrom(
        address, address, uint256[] memory, uint256[] memory, bytes memory
    ) public pure override {
        revert("LakouGovToken: soulbound, non-transferable");
    }

    /// @notice Get voting weight of a member in a vault
    function getWeight(address vault, bytes32 memberDidHash)
        external view returns (uint256) {
        return memberWeight[vault][memberDidHash];
    }

    /// @notice Get total voting supply for quorum calculation
    function getTotalSupply(address vault)
        external view returns (uint256) {
        return vaultTotalSupply[vault];
    }
}
```

---

### 2.2 Voting Weight Models

Three models are available. The vault selects its model at initialization; changing the model requires a 75% quorum vote.

**FLAT model** — every adult member holds equal weight regardless of contribution:

```
weight_per_member = total_supply / adult_member_count
```

At 4 adult members and 1,000 total tokens: 250 tokens each.

**CONTRIBUTION model** — weight is proportional to net capital contributed:

```
weight_i = (contribution_i / sum_all_contributions) * total_supply
```

Contributions are tracked by the RetailVault module (deposits net of withdrawals). Weight is recalculated quarterly or on any transfer event above the `rebalance_threshold`.

**HYBRID model (recommended default)** — flat floor plus contribution top-up:

```
floor_weight  = 0.5 * (total_supply / adult_member_count)
bonus_supply  = total_supply - sum(floor_weights)
bonus_weight_i = (contribution_i / sum_all_contributions) * bonus_supply
weight_i      = floor_weight + bonus_weight_i
```

At 4 members and 1,000 tokens: each member gets a floor of 125 tokens, plus up to 125 bonus tokens based on contribution. This ensures no member can be completely disenfranchised by low contribution.

**Reserve tokens (20% of initial supply)** are held in the vault treasury contract (`LakouTreasury`). They are released through governance proposals for:
- Onboarding new members (allocation from reserve)
- Compensating external advisors (temporary, non-voting advisory tokens — separate token type)
- Funding module upgrade deployments

---

### 2.3 Proposal Contract

```solidity
// SPDX-License-Identifier: AGPL-3.0
pragma solidity ^0.8.20;

import "./LakouGovernanceToken.sol";

/// @title LakouGovernor
/// @notice Proposal lifecycle and vote tallying for a single vault.
///         Each vault deploys its own LakouGovernor instance.
contract LakouGovernor {

    LakouGovernanceToken public immutable govToken;
    address public immutable vault;

    struct Proposal {
        uint256 id;
        address proposer;
        bytes32 proposerDidHash;
        string description;
        bytes callData;            // encoded function call to execute
        address target;            // contract to call on execution
        uint256 voteStart;
        uint256 voteEnd;
        uint256 timelockEnd;
        ProposalState state;
        uint256 forVotes;
        uint256 againstVotes;
        uint256 abstainVotes;
        mapping(bytes32 => bool) hasVoted; // memberDidHash => voted
    }

    enum ProposalState {
        Pending,    // not yet in voting window
        Active,     // voting open
        Defeated,   // voting closed, quorum not met or majority against
        Succeeded,  // voting closed, quorum met, majority for
        Queued,     // in timelock
        Executed,   // executed on-chain
        Expired     // queued but not executed within expiry window
    }

    mapping(uint256 => Proposal) public proposals;
    uint256 public proposalCount;

    event ProposalCreated(uint256 indexed id, bytes32 proposerDidHash, string description);
    event VoteCast(uint256 indexed proposalId, bytes32 indexed voterDidHash, uint8 support, uint256 weight, string reason);
    event ProposalExecuted(uint256 indexed id);
    event ProposalDefeated(uint256 indexed id);

    constructor(address _govToken, address _vault) {
        govToken = LakouGovernanceToken(_govToken);
        vault = _vault;
    }

    /// @notice Create a new governance proposal
    /// @param description Human-readable description
    /// @param target Contract to call on execution (address(0) for off-chain actions)
    /// @param callData ABI-encoded function call, or empty bytes for off-chain
    function propose(
        bytes32 proposerDidHash,
        string calldata description,
        address target,
        bytes calldata callData
    ) external returns (uint256 proposalId) {
        require(
            govToken.getWeight(vault, proposerDidHash) > 0,
            "No governance weight"
        );

        proposalId = ++proposalCount;
        Proposal storage p = proposals[proposalId];
        p.id = proposalId;
        p.proposer = msg.sender;
        p.proposerDidHash = proposerDidHash;
        p.description = description;
        p.callData = callData;
        p.target = target;
        p.voteStart = block.timestamp + 1 hours;  // 1 hour delay before voting opens
        p.voteEnd = p.voteStart + govToken.vaultConfig(vault).proposalDuration;
        p.timelockEnd = p.voteEnd + govToken.vaultConfig(vault).timelockDelay;
        p.state = ProposalState.Pending;

        emit ProposalCreated(proposalId, proposerDidHash, description);
    }

    /// @notice Cast a vote on an active proposal
    /// @param support 0=against, 1=for, 2=abstain
    function castVote(
        uint256 proposalId,
        bytes32 voterDidHash,
        uint8 support,
        string calldata reason
    ) external {
        Proposal storage p = proposals[proposalId];
        require(block.timestamp >= p.voteStart, "Voting not open");
        require(block.timestamp <= p.voteEnd, "Voting closed");
        require(!p.hasVoted[voterDidHash], "Already voted");
        require(support <= 2, "Invalid support value");

        uint256 weight = govToken.getWeight(vault, voterDidHash);
        require(weight > 0, "No voting weight");

        p.hasVoted[voterDidHash] = true;

        if (support == 0) p.againstVotes += weight;
        else if (support == 1) p.forVotes += weight;
        else p.abstainVotes += weight;

        _updateState(proposalId);

        emit VoteCast(proposalId, voterDidHash, support, weight, reason);
    }

    /// @notice Execute a passed and timelock-cleared proposal
    function execute(uint256 proposalId) external {
        Proposal storage p = proposals[proposalId];
        require(p.state == ProposalState.Queued, "Not queued");
        require(block.timestamp >= p.timelockEnd, "Timelock not elapsed");

        p.state = ProposalState.Executed;

        if (p.target != address(0) && p.callData.length > 0) {
            (bool success,) = p.target.call(p.callData);
            require(success, "Execution failed");
        }

        emit ProposalExecuted(proposalId);
    }

    /// @dev Evaluate quorum and majority after each vote, transition state
    function _updateState(uint256 proposalId) internal {
        Proposal storage p = proposals[proposalId];
        if (block.timestamp > p.voteEnd) {
            _finalizeProposal(proposalId);
        }
    }

    function _finalizeProposal(uint256 proposalId) internal {
        Proposal storage p = proposals[proposalId];
        if (p.state != ProposalState.Active && p.state != ProposalState.Pending) return;

        uint256 totalSupply = govToken.getTotalSupply(vault);
        uint256 cfg_num = govToken.vaultConfig(vault).quorumNumerator;
        uint256 quorumRequired = (totalSupply * cfg_num) / 100;
        uint256 totalVotes = p.forVotes + p.againstVotes + p.abstainVotes;

        if (totalVotes < quorumRequired || p.forVotes <= p.againstVotes) {
            p.state = ProposalState.Defeated;
            emit ProposalDefeated(proposalId);
        } else {
            p.state = ProposalState.Queued;
        }
    }
}
```

---

### 2.4 Quorum Calculation Reference

For a vault with 1,000 total tokens, 4 members (hybrid model: TR=400, MJ=250, PJ=200, RJ=150):

| Action | Quorum % | Min tokens needed | Minimum member combo |
|---|---|---|---|
| Enable module | 60% | 600 | TR+MJ (650), TR+PJ (600) |
| Disable module | 51% | 510 | TR+MJ (650), TR+PJ (600) |
| Loan above threshold | 67% | 670 | TR+MJ+abstain (650 short — needs TR+MJ+PJ=850) |
| Succession change | 75% | 750 | TR+MJ+PJ (850) |
| Vault dissolution | 90% | 900 | All four (1000) |
| Emergency freeze | 51% | 510 | Any single member above 510: TR alone (400 — fails), TR+RJ (550 — passes) |

**Quorum denominator is total issued supply**, not total possible supply. This matters when members have not yet cast votes — quorum is assessed at vote close, not in real time.

---

### 2.5 Succession Logic

When a member's death is confirmed via a government-issued Death Certificate Verifiable Credential (issued by a recognized VC issuer registered with the vault), the `LakouSuccession` contract executes:

```solidity
// SPDX-License-Identifier: AGPL-3.0
pragma solidity ^0.8.20;

/// @title LakouSuccession
/// @notice Handles post-mortem token redistribution and asset transfers.
contract LakouSuccession {

    struct SuccessionRule {
        bytes32 deceasedDidHash;
        bytes32[] heirDidHashes;       // ordered by priority
        uint256[] heirWeightShares;    // shares summing to 100
        uint256 vestingPeriodDays;     // delay before heir receives full weight
    }

    mapping(address => SuccessionRule[]) public vaultRules;

    // Minimum VC issuers trusted for death certificates (by DID)
    mapping(bytes32 => bool) public trustedIssuers;

    event SuccessionTriggered(
        address indexed vault,
        bytes32 indexed deceasedDidHash,
        bytes32[] heirDidHashes
    );

    /// @notice Register or update a succession rule (requires 75% quorum)
    function setRule(
        address vault,
        SuccessionRule calldata rule
    ) external {
        // Called by LakouGovernor after a 75% quorum vote
        vaultRules[vault].push(rule);
    }

    /// @notice Trigger succession after verifying a death certificate VC
    /// @param deathCertVpJwt W3C Verifiable Presentation JWT containing the death cert VC
    function triggerSuccession(
        address vault,
        bytes32 deceasedDidHash,
        string calldata deathCertVpJwt
    ) external {
        // 1. Verify the VP signature
        // 2. Check the issuer's DID is in trustedIssuers
        // 3. Check the subject of the VC matches deceasedDidHash
        // 4. Check VC is not expired and not revoked (status list check)
        // 5. Execute token redistribution per SuccessionRule
        // 6. Update vault member list
        // 7. Emit event

        emit SuccessionTriggered(vault, deceasedDidHash, _getHeirs(vault, deceasedDidHash));
    }

    function _getHeirs(address vault, bytes32 did)
        internal view returns (bytes32[] memory) {
        SuccessionRule[] memory rules = vaultRules[vault];
        for (uint i = 0; i < rules.length; i++) {
            if (rules[i].deceasedDidHash == did) return rules[i].heirDidHashes;
        }
        return new bytes32[](0);
    }
}
```

**Succession trigger flow:**

```
Death Certificate VC issued by government registrar
  └─> Family or executor presents VP to LakouSuccession.triggerSuccession()
        └─> VC verified (issuer trust, signature, revocation status)
              └─> deceasedDidHash matched to SuccessionRule
                    └─> Token redistribution executed
                          └─> VestingSchedule created for heirs
                                └─> Vault member list updated
                                      └─> WS event MEMBER_SUCCESSION emitted
```

---

### 2.6 Member Onboarding Flow (State Machine)

```
INVITED
  │  (family owner calls /vault/members/invite with candidate DID)
  ▼
PENDING_KYC
  │  (candidate completes KYC with trusted VC issuer)
  │  (issues KYC Attestation VC to candidate's DID wallet)
  ▼
PENDING_ROLE_VOTE
  │  (governance vote: what role and weight allocation for new member?)
  │  (requires 51% quorum)
  ▼
PENDING_ACCEPTANCE
  │  (candidate reviews vault charter and signs acceptance with their DID key)
  ▼
ACTIVE_MEMBER
  │  (governance tokens minted, API access granted)
  ▼
  (ongoing) ─── SUSPENDED ─── REMOVED ─── SUCCESSION_PENDING ─── INACTIVE
```

---

## 3. Lakou Module Interface Standard (LMIS)

### 3.1 Design Principle

Every module in Lakou is a **Diamond facet** (EIP-2535) plus a **FastAPI router** plus a **module manifest**. The Diamond proxy dispatches on-chain calls; the FastAPI router handles off-chain API requests; the manifest declares dependencies, required VCs, and fee schedules.

A module that implements LMIS correctly can be:
- Listed in the Lakou Module Registry
- Enabled/disabled by any vault through governance vote
- Upgraded independently without affecting other modules
- Audited for interface conformance by the registry

---

### 3.2 Solidity Interface (ILakouModule)

```solidity
// SPDX-License-Identifier: AGPL-3.0
pragma solidity ^0.8.20;

/// @title ILakouModule — Lakou Module Interface Standard v1.0
/// @notice All Lakou modules MUST implement this interface.
///         Modules are EIP-2535 Diamond facets registered in the Module Registry.
interface ILakouModule {

    // ─── Identity ─────────────────────────────────────────────────────────────

    /// @notice Canonical module identifier (e.g. keccak256("lakou.module.retail.v1"))
    function moduleId() external pure returns (bytes32);

    /// @notice Semver string (e.g. "1.0.0")
    function moduleVersion() external pure returns (string memory);

    /// @notice Human-readable name
    function moduleName() external pure returns (string memory);

    // ─── Credential Requirements ─────────────────────────────────────────────

    /// @notice Array of required VC type hashes that a member must hold
    ///         to access this module's endpoints.
    ///         e.g. [keccak256("KYCAttestation"), keccak256("AccreditedInvestor")]
    function requiredCredentials() external pure returns (bytes32[] memory);

    /// @notice VC types required for VAULT-level access (not per-member)
    ///         e.g. the vault must have a regulatory license VC for CommercialDesk
    function requiredVaultCredentials() external pure returns (bytes32[] memory);

    // ─── Lifecycle Hooks ──────────────────────────────────────────────────────

    /// @notice Called by the Diamond after governance vote passes to enable this module.
    ///         Module initializes its storage namespace here.
    /// @param vault The vault address enabling this module
    /// @param initData ABI-encoded initialization parameters
    function onEnable(address vault, bytes calldata initData) external;

    /// @notice Called before module is disabled. Module should snapshot state
    ///         for potential re-enable. Must not delete user data.
    /// @param vault The vault address disabling this module
    function onDisable(address vault) external;

    /// @notice Called when a new member is added to the vault.
    ///         Module can provision member-specific storage or default states.
    /// @param vault The vault address
    /// @param memberDidHash keccak256 of the new member's DID string
    function onMemberAdded(address vault, bytes32 memberDidHash) external;

    /// @notice Called when a member is removed from the vault.
    ///         Module should archive member's data, not delete it.
    /// @param vault The vault address
    /// @param memberDidHash keccak256 of the removed member's DID string
    function onMemberRemoved(address vault, bytes32 memberDidHash) external;

    /// @notice Called when a module upgrade is proposed.
    ///         Returns true if this module approves the upgrade (can check version compatibility).
    /// @param newImplementation Address of the proposed replacement facet
    function onUpgradeProposed(address newImplementation) external view returns (bool);

    // ─── Fee Schedule ─────────────────────────────────────────────────────────

    struct FeeSchedule {
        uint256 monthlyFeeWei;       // 0 if module is free
        uint256 transactionFeesBps;  // basis points on transactions, 0 if none
        address feeToken;            // ERC-20 address, or address(0) for native ETH
        address feeRecipient;        // Lakou Foundation multisig or address(0) for free
    }

    /// @notice Returns the fee schedule for this module version
    function feeSchedule() external pure returns (FeeSchedule memory);

    // ─── Health & Compliance ──────────────────────────────────────────────────

    /// @notice Returns true if the module is functioning correctly (used by registry)
    function healthCheck() external view returns (bool);

    /// @notice Returns the regulatory jurisdictions this module is compliant with
    ///         (ISO 3166-1 alpha-2 country codes)
    function supportedJurisdictions() external pure returns (string[] memory);
}
```

---

### 3.3 Module Manifest (JSON Schema)

Each module publishes a `lakou-module.json` manifest in its repository root. The Module Registry validates this manifest before listing.

```json
{
  "$schema": "https://registry.lakou.family/schemas/module-manifest-v1.json",
  "module_id": "lakou.module.remittance.v1",
  "version": "1.0.0",
  "name": "RemittanceGate",
  "description": "Cross-border transfer module with D-Central mesh routing",
  "author": "Lakou Foundation",
  "license": "AGPL-3.0",
  "repository": "https://github.com/lakou-protocol/modules/tree/main/remittance-gate",
  "contract": {
    "chain": "polygon",
    "address": "0x...",
    "abi_url": "https://registry.lakou.family/abis/remittance-gate-v1.json",
    "audit_url": "https://audits.lakou.family/remittance-gate-v1.pdf"
  },
  "api": {
    "router_module": "lakou_modules.remittance.router",
    "base_path": "/remittance",
    "openapi_url": "https://registry.lakou.family/openapi/remittance-gate-v1.json"
  },
  "required_credentials": [
    {
      "type": "KYCAttestation",
      "vc_type_hash": "0x...",
      "scope": "member",
      "description": "AML/KYC identity verification"
    }
  ],
  "required_vault_credentials": [],
  "fee_schedule": {
    "monthly_fee_usd": "0.00",
    "transaction_fees_bps": 70,
    "fee_description": "0.70% on transfer amount, min CA$1.00"
  },
  "dependencies": ["lakou.module.retail.v1"],
  "governance_requirements": {
    "enable_quorum_percent": 60,
    "disable_quorum_percent": 51,
    "timelock_hours": 24
  },
  "supported_jurisdictions": ["CA", "US", "HT", "FR", "GB"],
  "data_schema_version": "1.0",
  "min_lakou_core_version": "1.0.0"
}
```

---

### 3.4 Diamond Facet Registration

The `LakouModuleRegistry` is the Diamond proxy controller. It manages the mapping of function selectors to facet addresses.

```solidity
// SPDX-License-Identifier: AGPL-3.0
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/utils/introspection/IERC165.sol";

/// @title LakouModuleRegistry
/// @notice Central registry for all Lakou module facets.
///         Vaults reference this registry via the Diamond proxy.
contract LakouModuleRegistry {

    struct ModuleRecord {
        bytes32 moduleId;
        string version;
        address implementation;   // facet address
        bytes4[] selectors;       // function selectors this facet handles
        bool audited;             // flag set by Lakou Foundation multisig after audit
        bool deprecated;          // deprecated versions cannot be newly enabled
        uint256 registeredAt;
    }

    // moduleId => version string => ModuleRecord
    mapping(bytes32 => mapping(string => ModuleRecord)) public modules;

    // vault address => moduleId => enabled
    mapping(address => mapping(bytes32 => bool)) public vaultModuleEnabled;

    // vault address => moduleId => version string currently active
    mapping(address => mapping(bytes32 => string)) public vaultModuleVersion;

    address public immutable foundation;  // Lakou Foundation multisig (can publish modules)

    event ModulePublished(bytes32 indexed moduleId, string version, address implementation);
    event ModuleEnabled(address indexed vault, bytes32 indexed moduleId, string version);
    event ModuleDisabled(address indexed vault, bytes32 indexed moduleId);

    modifier onlyFoundation() {
        require(msg.sender == foundation, "Registry: not foundation");
        _;
    }

    constructor(address _foundation) {
        foundation = _foundation;
    }

    /// @notice Publish a new module version (Foundation only — does not auto-enable any vault)
    function publishModule(
        bytes32 moduleId,
        string calldata version,
        address implementation,
        bytes4[] calldata selectors
    ) external onlyFoundation {
        require(
            IERC165(implementation).supportsInterface(type(ILakouModule).interfaceId),
            "Registry: does not implement ILakouModule"
        );
        modules[moduleId][version] = ModuleRecord({
            moduleId: moduleId,
            version: version,
            implementation: implementation,
            selectors: selectors,
            audited: false,
            deprecated: false,
            registeredAt: block.timestamp
        });
        emit ModulePublished(moduleId, version, implementation);
    }

    /// @notice Mark a module version as audited (Foundation multisig)
    function markAudited(bytes32 moduleId, string calldata version)
        external onlyFoundation {
        modules[moduleId][version].audited = true;
    }

    /// @notice Enable a module for a vault (called by LakouGovernor post-vote)
    /// @dev This is the callData target in governance proposals for module enablement
    function enableModule(
        address vault,
        bytes32 moduleId,
        string calldata version,
        bytes calldata initData
    ) external {
        // Only callable via the vault's own Governor (enforced by msg.sender check)
        ModuleRecord memory rec = modules[moduleId][version];
        require(rec.implementation != address(0), "Registry: module not found");
        require(rec.audited, "Registry: module not audited");
        require(!rec.deprecated, "Registry: module deprecated");

        vaultModuleEnabled[vault][moduleId] = true;
        vaultModuleVersion[vault][moduleId] = version;

        // Call lifecycle hook
        ILakouModule(rec.implementation).onEnable(vault, initData);

        emit ModuleEnabled(vault, moduleId, version);
    }

    /// @notice Disable a module for a vault (called by LakouGovernor post-vote)
    function disableModule(address vault, bytes32 moduleId) external {
        string memory version = vaultModuleVersion[vault][moduleId];
        address impl = modules[moduleId][version].implementation;

        ILakouModule(impl).onDisable(vault);

        vaultModuleEnabled[vault][moduleId] = false;

        emit ModuleDisabled(vault, moduleId);
    }

    /// @notice Check if a module is enabled for a vault (used by API auth middleware)
    function isEnabled(address vault, bytes32 moduleId)
        external view returns (bool) {
        return vaultModuleEnabled[vault][moduleId];
    }
}
```

---

### 3.5 Reference Implementation: RetailVault

The FastAPI router implementation (Python):

```python
# lakou_modules/retail/router.py

from fastapi import APIRouter, Depends, Header
from .models import Account, Transaction, TransferRequest, TransferResponse
from .service import RetailVaultService
from ..auth import require_module_scope, VaultContext

router = APIRouter(prefix="/retail", tags=["RetailVault"])

@router.get("/accounts", response_model=list[Account])
async def list_accounts(
    ctx: VaultContext = Depends(require_module_scope("retail"))
):
    """List all accounts in the vault."""
    svc = RetailVaultService(ctx.vault_id)
    return await svc.get_accounts(ctx.member_did)

@router.get("/accounts/{account_id}/transactions")
async def get_transactions(
    account_id: str,
    page: int = 1,
    per_page: int = 25,
    ctx: VaultContext = Depends(require_module_scope("retail"))
):
    svc = RetailVaultService(ctx.vault_id)
    return await svc.get_transactions(account_id, page, per_page)

@router.post("/transfer", response_model=TransferResponse)
async def internal_transfer(
    request: TransferRequest,
    x_vault_nonce: int = Header(..., alias="X-Vault-Nonce"),
    ctx: VaultContext = Depends(require_module_scope("retail"))
):
    """
    Transfer between vault accounts.
    Idempotent on idempotency_key.
    Requires X-Vault-Nonce to prevent replay.
    """
    svc = RetailVaultService(ctx.vault_id)
    await svc.verify_nonce(x_vault_nonce, ctx.member_did)
    return await svc.execute_transfer(request, ctx.member_did)
```

```python
# lakou_modules/retail/models.py

from pydantic import BaseModel, Field
from decimal import Decimal
from datetime import datetime
from enum import Enum
from uuid import UUID

class AccountType(str, Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    BUSINESS = "business"
    TRUST = "trust"

class Account(BaseModel):
    id: str
    vault_id: str
    account_type: AccountType
    name: str
    currency: str = "CAD"
    balance: Decimal
    available_balance: Decimal
    created_at: datetime
    joint_members: list[str] = []  # member DIDs with access

class TransactionDirection(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"

class Transaction(BaseModel):
    id: str
    account_id: str
    direction: TransactionDirection
    amount: Decimal
    currency: str
    description: str
    module_source: str  # which module generated this transaction
    counterparty: str | None = None
    timestamp: datetime
    settled: bool
    on_chain_tx: str | None = None  # chain txhash if applicable

class TransferRequest(BaseModel):
    from_account: str
    to_account: str
    amount: Decimal = Field(gt=0, le=Decimal("50000"))
    currency: str = "CAD"
    memo: str | None = None
    idempotency_key: UUID

class TransferResponse(BaseModel):
    transfer_id: str
    status: str  # "completed", "pending", "failed"
    debit_transaction: Transaction
    credit_transaction: Transaction
    completed_at: datetime | None = None
```

---

### 3.6 Reference Implementation: RemittanceGate

```python
# lakou_modules/remittance/service.py

import asyncio
from decimal import Decimal
from dataclasses import dataclass
from .models import TransferRequest, TransferStatus, MeshRoute
from ..blockchain.hgusd import HGUSDBridge
from ..identity.vc_verifier import VCVerifier
from ..mesh.routing import DCentralMeshRouter

@dataclass
class QuoteResult:
    source_amount: Decimal
    source_currency: str
    destination_amount: Decimal
    destination_currency: str
    fx_rate: Decimal
    fee_amount: Decimal
    fee_percent: Decimal
    settlement_asset: str       # "HGUSD" or "USDC"
    routing: str                # "mesh" or "swift"
    estimated_minutes: int
    quote_expiry_unix: int

class RemittanceService:

    def __init__(self, vault_id: str):
        self.vault_id = vault_id
        self.hgusd_bridge = HGUSDBridge()
        self.vc_verifier = VCVerifier()
        self.mesh_router = DCentralMeshRouter()

    async def get_quote(
        self,
        amount: Decimal,
        source_currency: str,
        destination_currency: str,
        corridor: str,
        routing_preference: str = "mesh"
    ) -> QuoteResult:
        """
        Returns a signed quote valid for 60 seconds.
        Routing preference "mesh" uses D-Central nodes;
        "swift" uses SWIFT correspondent banking.
        """
        fx_rate = await self._get_fx_rate(source_currency, destination_currency)
        destination_amount = amount * fx_rate

        # Fee calculation: 0.70% with CA$1.00 floor
        fee_bps = Decimal("70")  # 0.70%
        fee_amount = max(amount * fee_bps / Decimal("10000"), Decimal("1.00"))
        net_source = amount + fee_amount

        if routing_preference == "mesh":
            nodes = await self.mesh_router.get_available_nodes(corridor)
            eta = 4 if len(nodes) >= 2 else 15
        else:
            eta = 1440  # 1 business day via SWIFT

        return QuoteResult(
            source_amount=net_source,
            source_currency=source_currency,
            destination_amount=destination_amount,
            destination_currency=destination_currency,
            fx_rate=fx_rate,
            fee_amount=fee_amount,
            fee_percent=fee_bps / Decimal("100"),
            settlement_asset="HGUSD" if corridor == "CA-HT" else "USDC",
            routing=routing_preference,
            estimated_minutes=eta,
            quote_expiry_unix=int(asyncio.get_event_loop().time()) + 60
        )

    async def execute_transfer(
        self,
        request: TransferRequest,
        sender_did: str,
        vault_context: dict
    ) -> TransferStatus:
        """
        Transfer lifecycle:
        1. Verify sender KYC VC
        2. Verify recipient DID
        3. Debit source account via RetailVault
        4. Mint HGUSD (or USDC) on source chain
        5. Route through D-Central mesh to destination node
        6. Trigger cash-out at destination agent
        7. Return transfer ID and initial status
        """
        # Step 1: KYC check
        await self.vc_verifier.require_vc(
            holder_did=sender_did,
            vc_type="KYCAttestation"
        )

        # Step 2: Recipient DID resolution and verification
        recipient_doc = await self._resolve_did(request.recipient_did)
        if not recipient_doc:
            raise ValueError("Recipient DID could not be resolved")

        # Step 3: Debit — delegated to RetailVault module
        debit_tx = await self._debit_vault_account(
            vault_id=self.vault_id,
            account_id=request.from_account,
            amount=request.amount + request.quoted_fee,
            memo=f"RemittanceGate → {request.corridor}"
        )

        # Step 4: Mint settlement asset
        settlement_tx = await self.hgusd_bridge.mint(
            amount_usd=request.amount,
            recipient_address=request.recipient_did
        )

        # Steps 5-6: Async — handled by mesh relay worker
        transfer_id = await self._enqueue_mesh_relay(
            settlement_tx=settlement_tx,
            recipient_did=request.recipient_did,
            destination_currency=request.destination_currency,
            corridor=request.corridor
        )

        return TransferStatus(
            transfer_id=transfer_id,
            status="processing",
            stage="mesh_relay_queued",
            source_debit_tx=debit_tx.id,
            settlement_tx_hash=settlement_tx.hash,
            estimated_completion_minutes=4
        )

    async def _resolve_did(self, did: str) -> dict | None:
        # Universal Resolver call
        import httpx
        async with httpx.AsyncClient() as client:
            r = await client.get(
                f"https://resolver.lakou.family/1.0/identifiers/{did}"
            )
            return r.json().get("didDocument") if r.status_code == 200 else None
```

---

## 4. Companion App UX Flows

### 4.1 Information Architecture

The app's navigation is **module-aware**: only sections whose corresponding module is enabled appear in the bottom navigation and drawer menu. A vault running only RetailVault + RemittanceGate shows a 3-tab bottom nav (Home, Send, Vault). A vault with all 10 modules shows the full 5-tab nav plus a "More" drawer.

```
Bottom Nav (always visible):
  Home        — dashboard, balances, recent activity
  Send        — transfer, remittance (shown if RetailVault OR RemittanceGate)
  Vote        — governance proposals (always shown)
  Modules     — module management (always shown)
  Vault       — profile, members, DID, settings

Drawer / More (shown when 5+ modules enabled):
  Invest      — InvestDesk
  Office      — FamilyOffice
  Circle      — SavingsCircle
  Business    — CommercialDesk
  Tax         — TaxLedger
  Insurance   — InsuranceVault
```

---

### 4.2 Onboarding Flow

**Screen 1 — Welcome**
- Lakou wordmark
- Tagline: "Your family's bank. Sovereign, modular, open."
- Two CTAs: "Create vault" / "Join a vault"

**Screen 2 — Create vault: Vault name**
- Input: Family vault name (e.g. "Jean Baptiste Family Vault")
- Helper: "This becomes part of your family's DID — choose something you'll be happy with long-term"

**Screen 3 — Choose DID method**
- Option A: `did:web` — requires a domain you own (recommended for families with web presence)
- Option B: `did:key` — device-generated, no infrastructure required (best for mobile-first)
- Option C: `did:ion` — Bitcoin-anchored, censorship-resistant (recommended for Haiti corridor)

**Screen 4 — Create your member DID**
- If device has no existing DID wallet → generate new key pair on-device (secure enclave)
- If device has an existing DID wallet → import via QR or passphrase
- Hardware key option: "I have a YubiKey / Ledger" → FIDO2 or hardware wallet flow

**Screen 5 — KYC / VC issuance**
- "To enable financial modules, one or more members need a KYC credential"
- Option A: "Verify now" → redirect to Lakou's trusted VC issuer partner (in-app WebView)
- Option B: "Skip for now — start with non-regulated modules only"
- Progress indicator: Identity → Verified ✓

**Screen 6 — Governance model selection**
- Three cards: Flat (equal weight), Contribution (proportional), Hybrid (recommended)
- Tap each card for explanation
- Select quorum threshold: slider from 51% to 75% (default 60%)
- Proposal duration: 1 day / 3 days / 7 days

**Screen 7 — First modules**
- "Which services does your family need?" (multi-select)
- Module tiles with icons and one-line descriptions
- Note: KYC-gated modules are marked with a lock icon if KYC not yet complete
- Pre-selected: RetailVault (required, cannot deselect)

**Screen 8 — Invite members**
- "Add family members to your vault"
- Share invite link → generates one-time invite URL containing challenge nonce
- Invited member completes their own DID creation + KYC flow
- Vault owner approves each joiner (or governance auto-approves at < N members)

**Screen 9 — Vault initialized**
- Animation: vault door opening
- "Your vault is live"
- Summary: vault DID, modules enabled, members, governance config
- CTA: "Open your vault"

---

### 4.3 Home Dashboard Screen

**Header row:**
- Left: "Lakou" wordmark in teal
- Right: bell icon (notification badge if proposals need attention)

**Net worth card (RetailVault + InvestDesk combined):**
- Total vault net worth (sum of all account balances + portfolio value)
- Month-over-month change in CAD and percentage
- Tap: opens detailed breakdown (accounts + investments)

**Quick actions row (module-aware):**
- Send (RetailVault) — internal transfer
- Receive — show vault QR
- Remit (RemittanceGate) — shown if RemittanceGate enabled
- Invest (InvestDesk) — shown if InvestDesk enabled
- Pay (CommercialDesk) — shown if CommercialDesk enabled
- "More" if > 4 actions

**Recent activity feed:**
- Last 5 transactions across all modules
- Each row: module icon (color-coded) + description + amount + relative time
- Module color coding:
  - RetailVault: teal
  - RemittanceGate: blue
  - InvestDesk: amber
  - SavingsCircle: purple
  - CreditCircle: coral

**Pending governance banner (shown when proposals active):**
- "2 proposals need your vote"
- Tap: navigates to Governance screen

---

### 4.4 RemittanceGate Send Flow

**Step 1 — Select recipient**
- Search field: search by name or DID
- Recent recipients list (DID-verified, shown with member avatar + name + DID truncated)
- "New recipient" → enter DID manually or scan QR
- DID resolution happens in background; checkmark appears when DID resolves

**Step 2 — Enter amount**
- Large numpad-style amount input
- Currency selector: CAD / USD / EUR
- Live conversion display: "= 27,500 HTG" (updates as amount is typed)
- Live fee calculation: "Fee: CA$1.87 (0.7%)"
- "Best rate" badge if mesh routing is selected over SWIFT

**Step 3 — Routing selection (advanced users only — collapsed by default)**
- Recommended: D-Central mesh (fastest, cheapest)
- Alternative: SWIFT (slower, higher fee, more corridors)
- Mesh node health indicator: "3 Ottawa nodes online ✓"

**Step 4 — Review & confirm**
- Summary card: recipient name + DID, amount, fee, destination amount in HTG, ETA
- Transfer route visualization: "Ottawa → D-Central relay → Port-au-Prince cash agent"
- "Confirm" button (requires biometric re-auth)
- Processing animation: pulsing dots showing relay stages

**Step 5 — Transfer status**
- Stage indicators: Initiated → Mesh relay → Cash agent notified → Confirmed
- Push notification when status changes
- Share receipt: PDF or link (contains public transfer data, no PII)

---

### 4.5 Governance Proposal Flow

**Proposals list:**
- Tabs: Active | Voted | Decided
- Each active proposal card:
  - Title + short description
  - Vote progress bar (for votes / total supply)
  - Time remaining (humanized: "18 hours", "5 days")
  - My vote status badge: "Not voted" / "Voted for" / "Voted against"

**Proposal detail screen:**
- Full proposal description (markdown rendered)
- Proposer: member avatar + name
- Created: timestamp
- Voting period: start → end
- Timelock: "Executes 24h after close if passed"
- Vote tally: for / against / abstain with governance weights
- Member vote list (public within vault): each member's vote shown
- Action: large "Vote for" / "Vote against" buttons
- If VC required (e.g., enabling InvestDesk): "Present your accreditation credential" prompt before voting

**Vote casting:**
- Select support (for / against / abstain)
- Optional reason field (stored on-chain in proposal state)
- Biometric confirmation
- TX confirmation: chain transaction hash shown
- WS event `VOTE_CAST` updates the tally in real time

**Creating a proposal:**
- FAB (floating action button) on proposals list
- Select proposal type: Module management / Vault settings / Spending / Custom
- For module management: dropdown of available modules from registry
- Title + description fields
- Preview: shows what the proposal callData will execute
- Submit: creates on-chain proposal, broadcasts via WS to all members

---

### 4.6 FamilyOffice Screen (when enabled)

**Sub-sections:**
- Estate vault (encrypted documents)
- Trusts
- Succession plan
- Generational timeline

**Estate vault:**
- Document list: will, deed, insurance policies, birth certificates
- Each document: name + file type + upload date + access log count
- Upload: end-to-end encrypted before upload; key derived from vault DID key
- Access: biometric auth required; access events logged on-chain
- Share: generate time-limited decryption link for a specific member's DID

**Trust management:**
- List of active trusts: name + type + total assets
- Trust detail: beneficiaries, trustee, corpus assets, distribution rules
- Assets inside trust are shown separately from vault's unrestricted holdings
- Distribution history: chronological list of distributions

**Succession plan:**
- Visual: member cards with succession arrows between them
- Current succession order (drag to reorder — initiates governance proposal)
- Trigger conditions: "On death certificate VC confirmation by [issuer]"
- Vesting schedule: how quickly heir receives full governance weight

**Generational timeline:**
- Visual calendar of future events: member governance age thresholds, trust distribution dates, review cadences

---

### 4.7 SavingsCircle Screen (when enabled)

**Active circles:**
- Circle name + members (shown as overlapping avatar initials)
- Round: "Round 3 of 8" + progress bar
- My turn indicator: "Your payout: Round 5" (highlighted if current)
- Contribution amount + due date

**Circle detail:**
- Member order (drag to view rotation schedule)
- Contribution history: each member's payments (public within circle)
- Smart contract address: tap to view on explorer
- Dispute button: if a member misses a contribution, initiates DAO arbitration flow

**Create a circle:**
- Name + contribution amount per period + period length (weekly/monthly)
- Member selection: search by DID within vault, or invite external vaults
- Rotation order: manual selection or randomized
- Smart contract preview: shows the Solidity parameters that will be deployed
- Deploy: requires governance vote if circle involves external vault members

**Cross-vault circles:**
- When a SavingsCircle includes members from multiple Lakou vaults, each participant's vault governance must approve joining
- Circle state is managed by a shared contract; payout routing handled by RemittanceGate if cross-currency

---

### 4.8 Desktop App Specifics

The desktop app (Tauri + React) presents the same five primary sections with additional capabilities:

**Family office dashboard (full-width, desktop-only):**
- Left sidebar: section navigation
- Main panel: scrollable content
- Right panel: contextual actions + recent activity

**Multi-sig governance signing:**
- When a proposal requires on-chain execution, the transaction is assembled client-side
- Hardware wallet users (YubiKey FIDO2, Ledger): transaction is presented for signing on device
- Threshold signing: if vault requires 2-of-N signers, desktop shows pending co-signers

**Statement export:**
- Date range picker
- Format: PDF (formatted), CSV (machine-readable), GAAP double-entry journal
- Scope: single account, all accounts, all modules, tax year

**Accountant API access:**
- "Grant access" flow: select scope (read-only, specific modules, date range)
- Generates a VC-gated API credential: the accountant presents their CPA credential VC to claim a scoped access token
- Access log: shows when the accountant last accessed, which endpoints

**Vault admin console:**
- Module management (same as mobile but with more detail: contract addresses, ABI, version history)
- Member management: add/remove, weight history, KYC credential status
- Governance history: all proposals, votes, executions with chain references
- Backup: encrypted vault configuration export (for disaster recovery or vault migration)

---

## Appendix A — Module Selector to API Path Mapping

| Module | Selector | API Path | Required VC |
|---|---|---|---|
| RetailVault | `0x1a2b3c4d` | `/retail` | KYCAttestation |
| CreditCircle | `0x2b3c4d5e` | `/credit` | KYCAttestation |
| CommercialDesk | `0x3c4d5e6f` | `/commercial` | KYCAttestation + BusinessRegistration |
| PrivateDesk | `0x4d5e6f7a` | `/private` | KYCAttestation |
| FamilyOffice | `0x5e6f7a8b` | `/office` | KYCAttestation |
| InvestDesk | `0x6f7a8b9c` | `/invest` | KYCAttestation (+ AccreditedInvestor for restricted) |
| SavingsCircle | `0x7a8b9c0d` | `/savings` | KYCAttestation |
| RemittanceGate | `0x8b9c0d1e` | `/remittance` | KYCAttestation |
| InsuranceVault | `0x9c0d1e2f` | `/insurance` | KYCAttestation |
| TaxLedger | `0x0d1e2f3a` | `/tax` | KYCAttestation |

---

## Appendix B — Error Handling Decision Tree

```
API request received
  ├── Is DPoP token valid?
  │     NO  → 401 auth.dpop_invalid
  ├── Is vault_id in token known?
  │     NO  → 404 vault.not_found
  ├── Is module referenced in path enabled?
  │     NO  → 403 module.not_enabled
  │     PENDING → 202 module.pending_vote
  ├── Does member hold required VC?
  │     NO  → 403 credential.missing
  │     EXPIRED → 403 credential.expired
  ├── Is X-Vault-Nonce fresh and unconsumed?
  │     NO  → 409 nonce.replay
  ├── Does action require quorum?
  │     YES + quorum not met → 403 vault.quorum_required
  │                            (+ proposal auto-drafted, proposal_id in response)
  └── Execute action → 200 / 201 / 204
```

---

## Appendix C — Document History

| Version | Date | Changes |
|---|---|---|
| 0.1 | 2026-05-05 | Initial technical specification |

---

*Lakou is a component of the D-Central Ecosystem.*  
*Document ID: DC-LKB-002 · Depends on: DC-LKB-001*  
*Author: Toussaint Redji Jean Baptiste*
