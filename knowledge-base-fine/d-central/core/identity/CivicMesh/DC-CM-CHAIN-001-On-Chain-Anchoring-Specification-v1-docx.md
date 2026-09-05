---
source_project: CivicMesh
source_project_uuid: 019e82f3-7ab2-715c-87c1-3e1074a12ab6
doc_uuid: 355c3b2d-3ba0-492e-8b16-6b577409d87e
original_filename: DC-CM-CHAIN-001_On-Chain_Anchoring_Specification_v1.docx
created_at: 2026-06-01T11:32:22.633395+00:00
content_hash: 1cdde985cd89
---

**D-Central Group  |  Confidential**	Section 2 — Legal & Corporate Structure

**DC-CM-CHAIN-001**

**D-CENTRAL GROUP**

**CivicMesh Inc.**

On-Chain Anchoring Specification — Polygon PoS

| **Document ID** | DC-CM-CHAIN-001 |
| --- | --- |
| **Version** | 1.0 |
| **Status** | Draft — SR&ED: blockchain R&D |
| **Date** | May 2026 |
| **Author** | Toussaint Redji Jean Baptiste |
| **Classification** | Confidential — Technical |
| **SR****&****ED Eligibility** | Strong — novel application of Polygon blockchain to enforcement evidence admissibility and cooperative credential governance |
| **Related Documents** | DC-CM-DID-001 │ DC-CM-VC-001 │ DC-CM-WALLET-001 │ REG-DID-001 |

| **Executive Summary** This document specifies what CivicMesh records on the Polygon PoS blockchain, why those specific items are on-chain (rather than off-chain), the smart contract architecture, and the gas cost model. The guiding principle is minimal on-chain footprint: only what requires immutability, public verifiability, or decentralized governance is recorded on-chain. Evidence content, personal information, and operational data stay off-chain. |
| --- |

# **1. What Goes On-Chain vs. Off-Chain**

| **Data** | **On-Chain?** | **Rationale** | **Storage Location** |
| --- | --- | --- | --- |
| DID registration and key rotation events | ✅ On-chain | Requires immutability and public verifiability — anyone must be able to verify a DID without trusting CivicMesh | Polygon — ERC-1056 style DID registry |
| Credential revocation status (StatusList2021) | ✅ On-chain | Revocation must be checkable by anyone, any time, without calling CivicMesh — court-required availability | Polygon — StatusList2021 smart contract |
| Issuer authorization registry | ✅ On-chain | Defines which DIDs are authorized to issue which credential types — must be immutable and publicly auditable | Polygon — Trust Registry smart contract |
| Node activation and deactivation events | ✅ On-chain | Creates a permanent, publicly verifiable record of when each node was operational — supports evidence admissibility | Polygon — Node Registry smart contract |
| Credential content (full VC JSON) | ❌ Off-chain | Too large and too frequently updated for on-chain storage. Contains holder-controlled data. | IPFS (content-addressed) or holder wallet |
| Evidence package content | ❌ Off-chain | Too large, contains PII, community-private data | MinIO/S3 (community-isolated) |
| Audit log entries | ❌ Off-chain | Too frequent for on-chain (1,000s per day), community-private | PostgreSQL append-only log |
| Personal information of any kind | ❌ Never on-chain | Immutability of blockchain makes PII deletion (PIPEDA right to erasure) impossible — PII must never touch the chain | Off-chain only |

# **2. Smart Contract Architecture**

| **Contract** | **Purpose** | **Key Functions** | **Upgrade Pattern** |
| --- | --- | --- | --- |
| CivicMeshDIDRegistry | DID registration and key rotation — adapted from ERC-1056 | registerDID(did, publicKey), rotateDID(did, oldKey, newKey), revokeDID(did, key) | Non-upgradeable — immutability is the value |
| CivicMeshTrustRegistry | Issuer authorization — which DIDs can issue which credential types | authorizeIssuer(issuerDID, credentialType), revokeIssuer(issuerDID, credentialType), isAuthorized(issuerDID, credentialType)→bool | Upgradeable (OpenZeppelin TransparentProxy) — governance can authorize new credential types |
| CivicMeshStatusList | Credential revocation — StatusList2021 implementation | updateStatusList(issuerDID, statusListCredential), getStatus(credentialId)→bool | Non-upgradeable per issuer — each issuer's list is a separate contract instance |
| CivicMeshNodeRegistry | Node activation/deactivation events | activateNode(nodeDID, communityId, msspDID), deactivateNode(nodeDID, reason), getNodeStatus(nodeDID)→{active,activatedAt,community} | Upgradeable — node types may expand |

# **3. Gas Cost Analysis — Polygon PoS**

| **Operation** | **Gas Units (est.)** | **MATIC Cost (at 30 gwei)** | **USD Cost (at $0.50/MATIC)** |
| --- | --- | --- | --- |
| DID registration (new entity) | ~100,000 | ~0.003 MATIC | ~$0.0015 |
| DID key rotation | ~60,000 | ~0.0018 MATIC | ~$0.0009 |
| Credential revocation (StatusList update) | ~50,000 | ~0.0015 MATIC | ~$0.0008 |
| Issuer authorization | ~80,000 | ~0.0024 MATIC | ~$0.0012 |
| Node activation | ~70,000 | ~0.0021 MATIC | ~$0.0011 |
| Node deactivation | ~40,000 | ~0.0012 MATIC | ~$0.0006 |

At scale: 10,000 node activations = ~$11 USD in gas costs. 100,000 technician credential issuances = ~$150 USD. Gas costs are negligible relative to programme value.

# **4. Testnet Development Plan**

| **Phase** | **Network** | **Purpose** | **Timing** |
| --- | --- | --- | --- |
| Development | Polygon Mumbai Testnet | All smart contract development and unit testing — free transactions | Months 1–9 |
| Integration Testing | Polygon Amoy Testnet | Integration testing with real credential flows — free transactions | Months 8–12 |
| Pilot | Polygon PoS Mainnet | OC Transpo pilot with real enforcement credentials — live blockchain | Month 12+ |
| Production | Polygon PoS Mainnet | Full production deployment | Month 18+ |

# **5. Document Control**

| **Ver** | **Date** | **Author** | **Description** |
| --- | --- | --- | --- |
| 1.0 | May 2026 | Toussaint Redji Jean Baptiste | Initial release |

| Classification Notice — This document is CONFIDENTIAL and intended for internal use, legal counsel, and authorized personnel only. Distribution requires written authorization from Toussaint Redji Jean Baptiste. |
| --- |

	Toussaint Redji Jean Baptiste  |  D-Central Ecosystem  |  May 2026	Page  of