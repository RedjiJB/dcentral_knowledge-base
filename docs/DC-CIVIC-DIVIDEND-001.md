# DC-CIVIC-DIVIDEND-001: CivicDividendModule (Lakou Module Interface Standard)

### Extends DC-CIVIC-EDUCATION-001 and DC-LKB-002 §3 (LMIS). Fulfills gap registry item #26.

---

## 0. What this is

A Lakou module, conforming to LMIS v1.0 (`ILakouModule`, DC-LKB-002 §3.2), that disburses the Civic Dividend (DC-CIVIC-EDUCATION-001 §3) into a citizen's own vault on each assessment cycle. Not a new payment rail — it reads the citizen's existing Citizen Competency VCs, computes tier per DC-CIVIC-EDUCATION-001 §3's eligibility table, and triggers a standard Lakou settlement through whatever module the vault already uses for inbound transfers (typically RetailVault). The disbursement source is out of scope here — this module only concerns itself with eligibility computation and the on-chain record of what was paid and why.

---

## 1. Required credentials

Per `ILakouModule.requiredCredentials()` — held by the **member** (the citizen), not the vault:

```solidity
function requiredCredentials() external pure returns (bytes32[] memory) {
    bytes32[] memory creds = new bytes32[](2);
    creds[0] = keccak256("CitizenshipVC");           // DC-CIVIC-EDUCATION-001 hard gate
    creds[1] = keccak256("CitizenCompetencyVC");     // one or more, per domain — §2 below iterates these
    return creds;
}
```

`requiredVaultCredentials()` returns an empty array — eligibility is a property of the member, not the vault. A family vault with several members may have some eligible and others not; the module computes per-member, not per-vault.

---

## 2. Eligibility computation

On each disbursement trigger (§4), the module:

1. Queries `dc-identity`'s `selective-disclosure-engine` for the member DID's full set of `CitizenCompetencyVC` credentials where `domain` matches `csss.*` or `specialization.*` (DC-CIVIC-EDUCATION-001 §2) — this returns level/evidence_type/expiry per domain, never the underlying score or portfolio content, exactly as that document's §2 `scope` policy requires. The module never has broader read access than any other verifier.
2. Confirms a valid, unexpired `CitizenshipVC` is present. Absent this, the function returns `TIER_NONE` unconditionally — no branch of this contract can produce a dividend amount without it (DC-CIVIC-EDUCATION-001 §3's hard-gate rule, enforced here as a mechanical early return, not a downstream check that could be skipped).
3. Confirms `civic.service-hours` (or `civic.service-alternative`) is present and unexpired. Absent this, the function returns `TIER_NONE` regardless of how strong every other domain credential is — same hard-gate pattern as citizenship.
4. Evaluates the remaining domain set against DC-CIVIC-EDUCATION-001 §3's table to compute `TIER_PROVISIONAL` / `TIER_STANDARD` / `TIER_ADVANCED` / `TIER_DISTINGUISHED`.
5. Writes the computed tier and the credential-hash set it was computed from to an on-chain `DisbursementRecord` (§5) — an auditable trail of *why* a given amount was paid, without exposing *what* the underlying competency evidence contained.

```solidity
enum DividendTier { NONE, PROVISIONAL, STANDARD, ADVANCED, DISTINGUISHED }

function computeTier(bytes32 memberDidHash) public view returns (DividendTier) {
    if (!_hasValidCredential(memberDidHash, CITIZENSHIP_VC)) return DividendTier.NONE;
    if (!_hasValidCredential(memberDidHash, SERVICE_HOURS_VC) &&
        !_hasValidCredential(memberDidHash, SERVICE_ALTERNATIVE_VC)) return DividendTier.NONE;

    if (_meetsDistinguished(memberDidHash)) return DividendTier.DISTINGUISHED;
    if (_meetsAdvanced(memberDidHash))      return DividendTier.ADVANCED;
    if (_meetsStandard(memberDidHash))      return DividendTier.STANDARD;
    return DividendTier.PROVISIONAL;
}
```

`_meetsStandard`/`_meetsAdvanced`/`_meetsDistinguished` each check the domain-count/level thresholds from DC-CIVIC-EDUCATION-001 §3's table against the credential set fetched in step 1 — omitted here for brevity, specified in full in the reference implementation, not this document.

---

## 3. Lifecycle hooks

```solidity
function onEnable(address vault, bytes calldata initData) external {
    // Registers this vault's members for dividend-eligibility tracking.
    // initData: ABI-encoded (address disbursementSourceModule) — which
    // enabled module on this vault receives the settlement instruction.
}

function onDisable(address vault) external {
    // Snapshots each member's last-computed tier and disbursement history.
    // Does not clear DisbursementRecord history — that is a citizen-owned
    // audit trail, not vault-owned state, and outlives module enablement.
}

function onMemberAdded(address vault, bytes32 memberDidHash) external {
    // Provisions a zero-state eligibility record; does not backfill
    // historical disbursements the member may hold from a prior vault.
}

function onMemberRemoved(address vault, bytes32 memberDidHash) external {
    // Archives, per LMIS's non-deletion rule. The citizen's DisbursementRecord
    // history is independent of any one vault and is portable to whichever
    // vault the citizen's DID is a member of next.
}
```

---

## 4. Disbursement trigger

Fires on the same 3-year expiry cadence as the Citizen Competency VCs (DC-CIVIC-EDUCATION-001 §4) — not a separate schedule. A credential renewal event (issued by `dc-attestation` on outcome-review, or by the assessment system on a retest) is the trigger; `computeTier` re-runs, and if the tier changed, a new disbursement is queued through the vault's configured settlement module (§0). A tier that stays the same on renewal produces a continuation disbursement at the same amount — the module does not require a tier *change* to pay, only a valid, current eligibility computation.

Between renewal cycles, no re-computation occurs — this matches DC-CIVIC-EDUCATION-001 §4's point that the assessment system does not re-examine settled competence more often than the 3-year window requires, and this module inherits that cadence rather than defining its own.

---

## 5. On-chain disbursement record

```solidity
struct DisbursementRecord {
    bytes32 memberDidHash;
    DividendTier tier;
    uint256 amountWei;
    bytes32[] credentialHashesUsed;  // hashes only — never the credential content
    uint256 timestamp;
    bytes32 assessmentCycleId;       // ties record to the 3-year window it was computed under
}
```

This is what makes a disputed tier auditable by the Constitutional Court of Competence (DC-CIVIC-EDUCATION-001 §5) without re-exposing the citizen's underlying scores: the Court can verify which credentials existed and at what level at disbursement time (via existence-proof, per `selective-disclosure-engine`), and whether `computeTier` was applied correctly against DC-CIVIC-EDUCATION-001 §3's table — without ever needing read access to portfolio content, test responses, or raw assessment data.

---

## 6. Fee schedule

```solidity
function feeSchedule() external pure returns (FeeSchedule memory) {
    return FeeSchedule({
        monthlyFeeWei: 0,              // the dividend module itself is free — it is a citizenship
                                        // entitlement, not a paid financial product
        transactionFeesBps: 0,
        feeToken: address(0),
        feeRecipient: address(0)
    });
}
```

No fee is charged for computing or receiving the dividend, consistent with the Charter's rule that eligibility and disbursement are never income- or fee-conditioned.

---

## 7. Module manifest

```json
{
  "$schema": "https://registry.lakou.family/schemas/module-manifest-v1.json",
  "module_id": "lakou.module.civic-dividend.v1",
  "version": "1.0.0",
  "name": "CivicDividendModule",
  "description": "Computes and disburses the Civic Dividend from Citizen Competency VCs per DC-CIVIC-EDUCATION-001",
  "author": "D-Central",
  "license": "AGPL-3.0",
  "contract": {
    "chain": "polygon",
    "address": "0x...",
    "abi_url": "https://registry.lakou.family/abis/civic-dividend-v1.json",
    "audit_url": "https://audits.lakou.family/civic-dividend-v1.pdf"
  },
  "api": {
    "router_module": "lakou_modules.civic_dividend.router",
    "base_path": "/civic-dividend",
    "openapi_url": "https://registry.lakou.family/openapi/civic-dividend-v1.json"
  },
  "required_credentials": [
    { "type": "CitizenshipVC", "vc_type_hash": "0x...", "scope": "member", "description": "Hard gate — citizenship" },
    { "type": "CitizenCompetencyVC", "vc_type_hash": "0x...", "scope": "member", "description": "Per-domain CSSS/specialization/service credentials" }
  ],
  "required_vault_credentials": [],
  "fee_schedule": {
    "monthly_fee_usd": "0.00",
    "transaction_fees_bps": 0,
    "fee_description": "No fee — citizenship entitlement, not a financial product"
  },
  "dependencies": ["lakou.module.retail.v1"],
  "governance_requirements": {
    "enable_quorum_percent": 60,
    "disable_quorum_percent": 51,
    "timelock_hours": 24
  },
  "supported_jurisdictions": ["*"],
  "data_schema_version": "1.0",
  "min_lakou_core_version": "1.0.0"
}
```

`dependencies: ["lakou.module.retail.v1"]` because settlement lands in the member's retail balance by default (§0) — a vault may reconfigure the settlement target via `onEnable`'s `initData`, but RetailVault must exist as the fallback.

`supported_jurisdictions: ["*"]` — unlike RemittanceGate or CommercialDesk, this module is not a regulated financial product requiring per-jurisdiction licensing; it is a credential-eligibility computation plus an internal transfer instruction. Actual cross-border disbursement compliance is the responsibility of whichever settlement module receives the instruction, not this one.

---

## 8. Health check

```solidity
function healthCheck() external view returns (bool) {
    // Returns false if the module cannot reach dc-identity's
    // selective-disclosure-engine to verify credentials — a disbursement
    // must never proceed on stale or unverifiable eligibility data.
}
```

A failed health check blocks disbursement entirely rather than falling back to a cached or assumed tier — consistent with DC-CIVIC-EDUCATION-001's principle that eligibility is always freshly verified against live credential state, never a value the citizen or vault could get stale-cached in their favor.

---

## 9. Gap registry status

**#26 `DC-CIVIC-DIVIDEND-001` — specified, this document.** Companion to #24 (`DC-AGENT-CREDENTIAL-001`) and the not-yet-registered `DC-CIVIC-EDUCATION-001`, which should be registered as #25's sibling under the same civic-credentialing extension line — recommend the user confirm final numbering against whatever else may have entered the registry since #25 was assigned to `DC-DAO-AGENT-LOOP-001`.

---

*DC-CIVIC-DIVIDEND-001 — specifies CivicDividendModule as an LMIS v1.0-conformant Lakou facet: eligibility computed from Citizen Competency VCs via `selective-disclosure-engine` (never exposing underlying scores), hard-gated on Citizenship and service-completion credentials per DC-CIVIC-EDUCATION-001 §3, disbursed on the same 3-year assessment cadence as credential expiry, recorded on-chain as credential-hash references rather than content for Constitutional Court auditability, and charging no fee as a citizenship entitlement rather than a financial product.*
