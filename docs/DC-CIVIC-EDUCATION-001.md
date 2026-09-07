# DC-CIVIC-EDUCATION-001: Civic Competency Framework on D-Central Primitives

### Maps the Civic Civilization Charter (lifelong education, specialization, credentialing, citizenship dividend) onto existing `dc-identity`, `dc-governance`, `dc-attestation`, and Lakou primitives. Extends DC-AGENT-CREDENTIAL-001's credential-schema pattern and DC-TAXONOMY-006's tiering to a new principal class: the citizen learner.

---

## 0. What this is

Not a new identity, governance, or banking system. Every mechanism the external Civic Civilization Charter proposes — decentralized identity for citizens, verifiable education/fitness/civic credentials, a competency-gated dividend, an independent adjudication body, cultural-governance routing, phased rollout — already has a working counterpart in this repo:

| Charter concept | Existing D-Central primitive |
|---|---|
| Citizen DID at birth | `did-registrar` (same mechanism DC-AGENT-CREDENTIAL-001 uses for agents) |
| Verifiable competency credentials (18 CSSS articles + specialization) | `vc-issuer`, new VC schema (§2 below) |
| Public existence-proof / private score vault split | `selective-disclosure-engine` — already enforces exactly this split, not a new policy |
| Civic participation / service record | `dc-attestation` (same outcome-review mechanism already used for agent and contractor reputation) |
| Constitutional Court of Competence | `dc-governance` + `proposal-engine`, scoped analogous to DC-EXPERT-DAO-001's review body |
| Cultural Identity Module (local tradition layer, elder authority) | `CulturalGovernance` contract pattern from `DC-BLOCKCHAIN-EDUCATION-FEDERATION-RECONCILED-001` §Solutions Roadmap — CULTURAL/MORAL/COMMUNITY proposal routing to elder-council/religious-leader approval, already specified |
| Citizenship dividend disbursement | Lakou (`DC-LKB-001/002/003`) vault module — a new `CivicDividendModule` alongside its existing modules |
| Transition gap / phased rollout | `DC-VERIFIABLE-ROLLOUT-001`'s staged-percentage rollout controller, and the Blockchain Education Federation's own 5-7 year 4-phase precedent |
| Rolling 3-year assessment cycle | `dc-attestation` expiry/renewal semantics, same as any other time-bound credential |

This document specifies the one genuinely new piece: the **citizen competency credential schema** and its permission/eligibility mapping. Everything else is reuse.

---

## 1. Issuance

1. A citizen DID is minted via `did-registrar` at birth (or naturalization — see §6), exactly as DC-AGENT-CREDENTIAL-001 mints an agent DID. No new registrar logic.
2. Credential issuers — academies, Child Commons supervisors, community kitchens, guild mentors, the assessment system itself — are themselves DIDs holding an `issuer.education.*` role credential (mirrors DC-AGENT-CREDENTIAL-001 §2's `role` field pattern), so issuance authority is itself a verifiable, revocable credential, not a hardcoded allowlist.
3. `vc-issuer` mints a **Citizen Competency VC** per domain per the schema in §2, bound to the citizen's DID.
4. The citizen presents domain-scoped proofs wherever eligibility must be checked (dividend tier calculation, academy admission, service-completion gate) — the same presentation flow any DID uses against any `dcentral-core` service.

---

## 2. Credential schema — Citizen Competency VC

| Field | Type | Purpose |
|---|---|---|
| `subject_did` | DID | The citizen's own DID |
| `domain` | string, namespaced | e.g. `csss.mathematics`, `csss.navigation`, `specialization.physics`, `civic.service-hours`, `physical.functional-capability` — one credential per domain, not one monolithic score |
| `level` | enum | `novice` \| `foundational` \| `proficient` \| `advanced` \| `expert` — matches the Charter's Competency Profile scale |
| `evidence_type` | enum | `demonstrated` (portfolio/project/service, per DC-attestation outcome-review) \| `assessed` (standardized/adaptive test result) |
| `issuer_did` | DID | The academy, mentor, or assessment instance that issued it |
| `issued_at` / `expiry` | timestamp | Expiry set to the rolling 3-year assessment window (§4) — not annual |
| `revocation_pointer` | reference | Entry in `revocation-registry`, same as any other credential type |
| `scope` | selective-disclosure policy | Governs what a verifier can learn: existence-of-credential-at-this-level is publicly provable; the underlying test responses, portfolio content, or raw score never leave the citizen's vault unless the citizen's own disclosure policy grants it |

This is the direct implementation of the Charter's ledger split (public existence-proof / private vault): `scope` is not a description of intended privacy, it is the same enforceable policy object `selective-disclosure-engine` already evaluates for every other credential type in this system (DC-AGENT-CREDENTIAL-001 §5's point applies identically here — a verifier cannot be reasoned into learning more than the policy allows, because the read call itself fails the check).

---

## 3. Eligibility mapping (credential set → dividend tier)

Mechanical enforcement, checked by `dc-governance` at disbursement time — not a self-reported claim the citizen presents once and is trusted on:

| Dividend tier | Required credential set |
|---|---|
| Provisional | Citizenship VC present; enrollment-status VC active; no completed-service gate check yet |
| Standard | All 18 `csss.*` domains at `proficient`; ≥1 `specialization.*` domain at `proficient`; `civic.service-hours` VC marking 18–25 mandatory service complete (or an `civic.service-alternative` VC recording an approved substitute) |
| Advanced | Standard, plus ≥1 `specialization.*` at `advanced` or ≥2 at `proficient`; multi-year `civic.service-hours` attestation history |
| Distinguished | Advanced, plus ≥1 `specialization.*` at `expert`; `civic.leadership` attestation |

A `CivicDividendModule` on the citizen's Lakou vault (extending the existing modular pattern in `DC-LKB-002`) queries this credential set on each disbursement cycle and computes tier automatically — the same way any Lakou module reads a family's verified financial state before executing a governed action. No manual eligibility review needed for the common case; the Constitutional Court (§5) only hears disputes.

**Hard gates, enforced the same way DC-AGENT-CREDENTIAL-001 §3 enforces "agents never call `voting-engine`":** a missing `civic.service-hours` credential (and no approved alternative) blocks every tier above nothing, mechanically, regardless of how strong the citizen's other domain credentials are. A missing Citizenship VC blocks all tiers, full stop. Neither is a policy a disbursement reviewer might overlook — the module's query simply returns no eligible tier.

---

## 4. Assessment cycle as credential expiry

The Charter's rolling three-year demonstrate-or-test window is not new infrastructure — it is `expiry` on the Citizen Competency VC (§2), exactly as any other time-bound credential in this system expires and requires renewal. A citizen with strong `evidence_type: demonstrated` credentials accumulated through the three years renews automatically on outcome-review; a citizen with `evidence_type: assessed` credentials nearing expiry is flagged for retest by the same mechanism `dc-attestation` already uses to flag any credential approaching expiry.

---

## 5. Constitutional Court of Competence → scoped DAO body

Modeled directly on DC-EXPERT-DAO-001's existing review-body pattern, not a new governance primitive:

- Judges hold an `issuer.judicial.competence` role credential (DC-AGENT-CREDENTIAL-001-style role/scope/tier schema, human principals instead of agent instances), term-limited and staggered.
- Confirmation of judges routes through `dc-governance`'s `proposal-engine`/`voting-engine`, scoped to a body outside the education-credentialing DIDs themselves — mirroring DC-AGENT-CREDENTIAL-001 §3's rule that no role is self-authorizing.
- Appeals against a tier denial or a credential revocation are submitted as proposals scoped to this body only; the body's ruling is itself an attestation, auditable the same way any `dc-attestation` outcome-review is.

---

## 6. Cultural Identity Module → existing `CulturalGovernance` pattern

The Charter's requirement that a fixed share of history/language/arts credentials be satisfiable through local/indigenous tradition, and that cultural decisions route to elder/traditional authority rather than pure token-vote, is **already specified** in `DC-BLOCKCHAIN-EDUCATION-FEDERATION-RECONCILED-001`'s `CulturalGovernance` contract: it routes CULTURAL-type proposals to mandatory elder-council approval, MORAL-type to religious-leader approval, COMMUNITY-type to a traditional-consensus gate before any token vote opens. A `csss.arts-humanities` or `csss.global-civilization` credential satisfied through a local tradition is issued by an `issuer.education.cultural` DID under elder-council attestation, using this exact routing — no new contract needed, only a new issuer role scoped to the pattern.

This is also the mechanism that answers the Charter's "portability from village to global scale" requirement: the CulturalGovernance routing is per-community by construction (each community's elder council is its own DID-scoped authority), so the same credential schema runs identically whether deployed for one village or federated across many, exactly as the education-federation's 3-tier institution/network/community governance model already federates across differently-sized deployments.

---

## 7. Naturalization / talent-immigration pathway

Elite-talent recognition (Charter Part XII.2) maps to the same credential-import pattern `DC-BLOCKCHAIN-EDUCATION-FEDERATION-RECONCILED-001`'s "Emerging Technology Integration" module already specifies for W3C VC wallets with international portability (EBSI/Europass/CARICOM-CXC recognition): a foreign credential is imported as a `csss.*` or `specialization.*` VC at whatever level it verifiably maps to, issued by a recognized cross-border issuer DID, then treated identically to a domestically-issued credential for every purpose in §3 except one — the Citizenship VC gate is independent and cannot be satisfied by any credential import, per the Charter's hard rule that citizenship alone gates the dividend.

---

## 8. Transition gap

Per the Charter's own Part XII.3, the rollout sequencing from a present-day population into this credential architecture is not specified here. `DC-VERIFIABLE-ROLLOUT-001`'s staged-percentage rollout controller and the Blockchain Education Federation's 5-7 year, 4-phase precedent (Foundation → Preparation → Integration → Sovereignty) are the closest existing analogs and should be the starting point for that follow-on document, not assumed solved by this one.

---

## 9. Gap registry status

**#25b `DC-CIVIC-EDUCATION-001` — specified, this document.** Follows the identical extension pattern as #24 (`DC-AGENT-CREDENTIAL-001`): new credential type + permission table on existing `dc-identity`/`dc-governance`/`dc-attestation`, no new microservice. Companion spec `DC-CIVIC-DIVIDEND-001` (gap #26) implements the disbursement side as an LMIS-conformant Lakou module consuming the credential schema defined here. Recommend the user confirm final numbering against the live registry — #25 was already assigned to `DC-DAO-AGENT-LOOP-001`, so this and #26 may need renumbering rather than the placeholder suffix used here.

---

## 10. OSS reference

No new microservice. Reuses `dc-identity` (Hyperledger Aries/Indy, Veramo — DC-TAXONOMY-003 §2.1), `dc-governance`'s `proposal-engine`/`voting-engine`, `dc-attestation`, `selective-disclosure-engine`, and a new Lakou vault module (`DC-LKB-002`'s modular pattern). This is a new VC schema, a new eligibility-mapping table, and one new Lakou module — not new infrastructure.

---

*DC-CIVIC-EDUCATION-001 — specifies the Citizen Competency VC schema (domain/level/evidence-type, scope-as-enforceable-disclosure-policy, 3-year expiry-as-assessment-cycle), the credential-set-to-dividend-tier eligibility mapping enforced mechanically by `dc-governance` at disbursement time, the Constitutional Court of Competence as a scoped DAO body on the DC-EXPERT-DAO-001 pattern, and the Cultural Identity Module as a direct reuse of the already-specified `CulturalGovernance` elder/religious-authority routing contract. Draws its external requirements from the Civic Civilization Charter (see companion artifact) and its implementation substrate entirely from existing D-Central specs — DC-AGENT-CREDENTIAL-001, DC-EXPERT-DAO-001, DC-VERIFIABLE-ROLLOUT-001, DC-LKB-001/002/003, and DC-BLOCKCHAIN-EDUCATION-FEDERATION-RECONCILED-001.*


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

*No cross-references detected to/from other docs/*.md files.*

<!-- AUTO-GENERATED RELATED END -->
