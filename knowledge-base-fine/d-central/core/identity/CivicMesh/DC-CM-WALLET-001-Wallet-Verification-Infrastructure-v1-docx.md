---
source_project: CivicMesh
source_project_uuid: 019e82f3-7ab2-715c-87c1-3e1074a12ab6
doc_uuid: 0c574e89-c359-4a7e-860a-3a31623664e2
original_filename: DC-CM-WALLET-001_Wallet_Verification_Infrastructure_v1.docx
created_at: 2026-06-01T11:32:21.884139+00:00
content_hash: 01af46999555
---

**D-Central Group  |  Confidential**	Section 2 — Legal & Corporate Structure

**DC-CM-WALLET-001**

**D-CENTRAL GROUP**

**CivicMesh Inc.**

Wallet and Verification Infrastructure

| **Document ID** | DC-CM-WALLET-001 |
| --- | --- |
| **Version** | 1.0 |
| **Status** | Draft |
| **Date** | May 2026 |
| **Author** | Toussaint Redji Jean Baptiste |
| **Classification** | Confidential — Technical |
| **SR****&****ED Eligibility** | Moderate — novel integration of mobile DID wallet with enforcement and cooperative credentialing system |
| **Related Documents** | DC-CM-DID-001 │ DC-CM-VC-001 │ DC-CM-APP-002 │ DC-CM-APP-006 │ DC-CM-CERT-001 |

| **Executive Summary** Every entity in the CivicMesh ecosystem that holds a Verifiable Credential needs a wallet — a secure store for their private keys and credentials. This document specifies the wallet infrastructure for three entity types: individual people (technicians, officers, managers, residents), organizations (MSSPs, training providers, municipalities), and hardware nodes (firmware-embedded). It also specifies the public verification infrastructure that any party can use to verify credentials without a wallet. |
| --- |

# **1. Wallet Types by Entity**

| **Entity Type** | **Wallet Type** | **Platform** | **Key Storage** | **Recovery Method** |
| --- | --- | --- | --- | --- |
| Individual (technician, officer, resident) | Mobile wallet — CivicMesh Wallet (or Polygon ID) | iOS, Android | Device secure enclave (biometric-protected) | 12-word seed phrase + backup to encrypted cloud (optional) |
| Organization (MSSP, municipality, training provider) | Web wallet — CivicMesh Org Wallet | Web browser + server-side key management | HSM or KMS (AWS KMS, Google Cloud KMS) for high-security orgs; encrypted database for standard orgs | Key rotation procedure — new key authorized in DID document, old key deauthorized |
| Hardware Node | Firmware-embedded wallet | ATECC608B secure element | Hardware-bound non-exportable private key in ATECC608B | Key cannot be extracted or backed up by design. Tamper event triggers node suspension + key rotation via new secure element provisioning. |
| D-Central Root Authority | Air-gapped HSM | Offline signing ceremony | Hardware Security Module (Thales or similar) | M-of-N threshold signing — multiple D-Central principals required to sign root-level credentials |

# **2. Verification Interfaces**

| **Interface** | **User** | **What It Verifies** | **Access** |
| --- | --- | --- | --- |
| Officer Portal — automatic verification | Municipal enforcement officers | Node credential chain on every evidence package before display | Requires active Officer Authorization Credential |
| MSSP NOC Console — credential monitor | MSSP NOC operators | All credentials in managed communities — expiry, revocation status | Requires active MSSP Operator Credential |
| Technician App — job credential check | Certified technicians | Credential chain of the node they are about to install | Requires active Technician Credential |
| Public Verification API — verify.civicmesh.ca | Anyone — defence counsel, courts, independent auditors | Any evidence package by ID — full credential chain verification result | No account required. Rate limited to prevent abuse. |
| QR Code Verification — in-person | Physical inspection scenarios | Display technician, MSSP, or municipal officer credential as QR code for in-person verification | Mobile wallet — present credential QR code |

# **3. The Political Transparency Argument**

| **The Question Politicians Ask** | 'How do I know the technicians who installed these cameras were qualified?' |
| --- | --- |
| **The Answer** | Scan this QR code on the camera's tamper-evident label. It resolves to verify.civicmesh.ca/{node-id} and returns the full credential chain: the manufacturer's certified status, the technician's certification level and jurisdiction, the MSSP operator's audit status. All verifiable in <2 seconds on any smartphone by any member of the public. |
| **Why This Matters Politically** | Flock Safety, Ring, and ShotSpotter cannot offer this. Their installer qualifications, if they exist, are in a private database. CivicMesh's are on a public blockchain. This is the answer to every transparency concern a city councillor, community advocate, or journalist will raise. |

# **4. Document Control**

| **Ver** | **Date** | **Author** | **Description** |
| --- | --- | --- | --- |
| 1.0 | May 2026 | Toussaint Redji Jean Baptiste | Initial release |

| Classification Notice — This document is CONFIDENTIAL and intended for internal use, legal counsel, and authorized personnel only. Distribution requires written authorization from Toussaint Redji Jean Baptiste. |
| --- |

	Toussaint Redji Jean Baptiste  |  D-Central Ecosystem  |  May 2026	Page  of