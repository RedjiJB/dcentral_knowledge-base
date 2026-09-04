# DC-DION-RECONCILED-001 — D-Central Intelligence & Operator Network (DION), Consolidated (v2, updated 2026-09-04)

Produced per [DC-CONSOLIDATOR-STD-001](../standards/DC-CONSOLIDATOR-STD-001.md), reconciling the DION
platform docs against D-Central's existing agent/credential/governance architecture per the
confirmed duplication findings in [CROSS-POLLINATION-FINDINGS.md](../CROSS-POLLINATION-FINDINGS.md).

## Current understanding

DION is D-Central's intelligence-gathering and emergency-response vertical: a community-owned
network of sensor-equipped edge nodes, human "Intelligence Network Operators" who maintain and
operate that network professionally, and an AI/human fusion layer that turns raw multi-source
collection into verified, actionable intelligence for emergency responders, news organizations,
businesses, and government agencies [DION-Blueprint].

**The platform's operational layers are genuine, novel content and are incorporated as-is:**

- **Physical infrastructure**: a three-tier hardware model — Community Nodes ($500-1,000, Raspberry
  Pi 5 + basic sensors), Professional Nodes ($3,000-8,000, Jetson AGX Orin + thermal/radar/lidar),
  and Regional Command Centers ($25,000-100,000, GPU clusters + 24/7 staffing) — connected via a
  hierarchical mesh (local WiFi 6E, wide-area LoRaWAN, fiber backbone, satellite backup)
  [DION-Blueprint §1].
- **Multi-INT collection and fusion**: ten parallel collection disciplines (OSINT, IMINT, SIGINT,
  HUMINT, MASINT, GEOINT, CYBINT, FININT, TECHINT, MEDINT), each with its own source list, privacy
  protections (automatic PII redaction, face/plate blurring, metadata-only signals collection), and
  cross-INT correlation into a single fused intelligence output [DION-Blueprint §5].
- **Operator training and career progression**: a four-level certification path (Basic Network
  Operator → Intelligence Analyst → Network Coordinator → Master Operator), each with defined
  training hours, specialization tracks, and earnings ranges ($2,000-4,000/mo at Level 1 up to
  $15,000-30,000/mo at Level 4), delivered through a distributed learning platform with peer
  learning groups and real-world practical assessments (deploying an actual edge node, coordinating
  a simulated emergency) [DION-Credentialing].
- **Application-layer use cases**: emergency response (missing-person search with 5-minute
  mobilization and claimed 95% 24-hour recovery rate, natural-disaster damage assessment, mass-
  casualty triage support), plus news/media, business intelligence, community safety, and government/
  public-services applications, each with named integration partners (FEMA, AP, local police/fire/
  medical services) [DION-Blueprint §7].
- **API surface**: a REST/GraphQL/WebSocket/webhook gateway with a fairly complete GraphQL schema
  for intelligence search, operator/task management, and emergency-alert subscriptions
  [DION-Blueprint §4]. The core docs don't specify an API layer at all, so there's no conflict here
  — this is additive, not overlapping.

**The identity/credential/governance/token layer is duplicated infrastructure, not novel content,**
and is superseded by the existing core mechanisms rather than incorporated as designed:

- **Identity.** DION specifies a bespoke `did:dcentral:operator:` DID method and its own
  `DIONRegistry` smart contract for registering nodes, operators, and organizations
  [DION-Blueprint §2]. The core architecture already covers this: an operator is a DID like any
  other principal, issued through `dc-identity`'s existing `did-registrar` — "not a new identity
  system" is stated explicitly [DC-AGENT-CREDENTIAL-001 §0]. An Intelligence Network Operator is
  structurally the same shape as any other role-scoped DID holder in this architecture; it doesn't
  need its own DID namespace.
- **Credentialing.** DION's `OperatorCredentialingSystem` mints credentials through a custom
  "credential blockchain," separate from the rest of the platform's identity layer
  [DION-Credentialing]. The core mechanism is a `vc-issuer`-minted VC bound to the operator's DID,
  with a schema of `role` / `tier` / `scope` / `mandate_ref` / `commissioner_did` /
  `expiry`/`revocation` [DC-AGENT-CREDENTIAL-001 §2]. DION's four operator levels and specialization
  tracks map directly onto this schema's `role` and `tier` fields rather than needing a parallel
  credential type.
- **Reputation.** DION proposes a non-transferable `REP_TOKEN` with its own earning/decay mechanics
  [DION-Blueprint §3]. The core architecture explicitly considered and rejected a separate
  reputation registry for the same reason this one should be: "reputation is not a separate
  registry... every outcome-review issues a reputation attestation... through the same
  `dc-attestation` envelope every other claim in this architecture uses" [DC-DAO-AGENT-LOOP-001 §1].
  An operator's completed-task history should be queryable the same way a contractor's job history
  already is [DC-AGENT-CREDENTIAL-001 §4].
- **Governance.** DION specifies a full `DIONGovernance` Solidity contract with its own proposal
  types, voting period, and quorum thresholds [DION-Blueprint §3]. The core architecture already has
  `dc-governance` with a role-prefix-to-permission mapping that mechanically enforces "operators
  propose, they never execute unilaterally" at the credential level rather than needing a
  separately-deployed governance contract [DC-AGENT-CREDENTIAL-001 §3, DC-DAO-AGENT-LOOP-001 §4].

## Provenance

| Claim cluster | Sources | Status |
|---|---|---|
| Hardware tiers, mesh network infrastructure | DION-Blueprint §1 | incorporated |
| Multi-INT collection & fusion | DION-Blueprint §5 | incorporated |
| Operator training levels, career progression, practical assessment | DION-Credentialing | incorporated |
| Emergency response / news / business / government use cases | DION-Blueprint §7 | incorporated |
| API/GraphQL surface | DION-Blueprint §4 | incorporated (additive — core docs are silent here) |
| Identity: `did:dcentral:operator:` + `DIONRegistry` | DION-Blueprint §2 | superseded-within-topic → `dc-identity`/`did-registrar` (DC-AGENT-CREDENTIAL-001 §0) |
| Credentialing: custom credential blockchain | DION-Credentialing | superseded-within-topic → `vc-issuer` agent/operator-class VC (DC-AGENT-CREDENTIAL-001 §2) |
| Reputation: `REP_TOKEN` | DION-Blueprint §3 | superseded-within-topic → `dc-attestation` reputation attestations (DC-DAO-AGENT-LOOP-001 §1, DC-AGENT-CREDENTIAL-001 §4) |
| Governance: `DIONGovernance` contract | DION-Blueprint §3 | superseded-within-topic → `dc-governance` role-permission mapping (DC-AGENT-CREDENTIAL-001 §3) |
| Payment/token economics: `INTEL_TOKEN` | DION-Blueprint §3 | superseded-within-topic → `dc-credit` payroll disbursement + vault-native stablecoin settlement (DC-TAXONOMY-002 §1.2, DC-LKB-003 §"payroll & payment rails") — see resolution below |

## Unresolved tensions

None remaining — the one tension flagged in the prior version of this document (DION's operator
payment mechanism) is now resolved; see below.

### Resolved since v1 (operator payment mechanism)

**Update:** DC-LKB-001/002/003 (the Lakou Protocol banking docs) were pulled into this repo after
v1 of this document flagged the payment question as unresolved. They confirm D-Central already has
a general-purpose payment/settlement layer this routes through cleanly:

- `dc-credit` — D-Central's core payments/settlement microservice — already handles "payroll
  disbursement," "recurring micropayment," and "milestone-released crowdfunding... a natural
  extension of the escrow engine" [DC-TAXONOMY-002 §1.2]. This is a direct fit for DION's need to pay
  thousands of human operators: base salary as recurring disbursement, per-task/emergency-response
  bonuses as milestone-released payments — no new token required for the payment *mechanism* itself.
- The Lakou docs additionally show D-Central's actual pattern for a corridor-specific settlement
  currency: a vault-native stablecoin (e.g. `HGUSD` for the Haiti corridor), collateralized and
  peg-stabilized, used for payroll/merchant settlement over `dc-credit`'s plumbing, with governance
  tokens kept strictly non-transferable/soulbound and separate from the payment currency
  [DC-LKB-003, "MeshBank stablecoin module" / payroll & merchant-account sections]. This is the
  opposite design from DION's proposal, where `INTEL_TOKEN` conflates governance, payment, and
  reward-multiplier logic into one transferable utility token.

**Recommendation, updated:** DION's operator compensation (base salary, task-completion payments,
emergency-response bonuses) should route through `dc-credit`, denominated in a stablecoin (following
the Lakou pattern) rather than a new speculative utility token. `REP_TOKEN`'s replacement
(`dc-attestation` reputation attestations, already noted above) stays non-transferable and fully
separate from payment — consistent with how Lakou keeps governance tokens and payment currency
strictly apart.

## Sources consulted (exhaustive list)

- `knowledge-base/verticals-products/Bounty/D-Central-Intelligence-Operator-Network-Complete-Platform-Blueprint-md.md` (DION-Blueprint)
- `knowledge-base/verticals-products/Bounty/Operator-Credentialing-System-for-D-Central-Intelligence-Network-md.md` (DION-Credentialing)
- `docs/DC-AGENT-CREDENTIAL-001.md`
- `docs/DC-DAO-AGENT-LOOP-001.md`
- `docs/DC-LKB-001.md`, `docs/DC-LKB-002.md`, `docs/DC-LKB-003.md` (added in v2, resolves the payment-mechanism tension)
- `taxonomy/DC-TAXONOMY-002-Microservices-and-Additional-Verticals.md` (§1.2, `dc-credit` definition)

## Consolidation metadata

```
consolidates: [
  knowledge-base/verticals-products/Bounty/D-Central-Intelligence-Operator-Network-Complete-Platform-Blueprint-md.md,
  knowledge-base/verticals-products/Bounty/Operator-Credentialing-System-for-D-Central-Intelligence-Network-md.md,
]
reconciled_against: [
  docs/DC-AGENT-CREDENTIAL-001.md,
  docs/DC-DAO-AGENT-LOOP-001.md,
  docs/DC-LKB-001.md,
  docs/DC-LKB-002.md,
  docs/DC-LKB-003.md,
]
supersedes_prior_consolidation: DC-DION-RECONCILED-001 v1 (this same doc, in-place update rather than
  a separate versioned file, since no downstream consumer has referenced v1 yet)
generated_by: consolidator-pass (manual, per DC-CONSOLIDATOR-STD-001)
```

**Note on authority boundary**: this document does not mark the source DION docs `superseded` or
move them to `_superseded/` — per DC-CONSOLIDATOR-STD-001 §0, that status assignment belongs to the
dedup/status process (DC-DEDUP-STD-001), not the Consolidator. The two DION source docs remain in
place at their original path with a `reconciliation_note` front-matter field pointing here.
