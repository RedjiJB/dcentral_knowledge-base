# DC-EXPERT-DAO-001: Credentialed Expert Review, Advisory & Bounty Network
### Extends DC-DAO-AGENT-LOOP-001, DC-AGENT-CREDENTIAL-001. Addresses two requirements: mandatory domain sign-off on every proposal, and a standing expert network for advisory consensus and crowdsourced problem-solving.

---

## 0. Why one spec covers both functions

Sign-off review and advisory/bounty work both depend on the same thing: a credential proving someone actually has the domain expertise they claim. Building two separate systems to check that would duplicate trust infrastructure the taxonomy's own discipline rules out. One credential type, one scoped-DAO pattern, two modes of operation.

---

## 1. Expert credential

A new VC type, issued through the existing identity service — not a new identity system.

| Field | Purpose |
|---|---|
| `subject_did` | The expert's own DID |
| `domain` | e.g. `security`, `finance`, `legal`, `civil-engineering`, `public-health` — namespaced, extensible |
| `credentialing_path` | `licensed` (attested by an existing external licensing/professional body, same extension pattern already used for inspector/permit attestations) or `peer-attested` (accumulated through track record inside the Expert DAO itself — see §4) |
| `reputation_ref` | Pointer to this DID's attestation history, same mechanism as agent reputation (DC-AGENT-CREDENTIAL-001 §4), now extended to humans |

**Bootstrapping note, stated honestly:** `peer-attested` credentialing has a cold-start problem — the first cohort of experts in a new domain has no prior track record to be attested against. Reasonable resolution: seed each new domain with `licensed` experts (external professional credentials get you in the door), and let `peer-attested` standing accrue from there as bounty/advisory work builds a track record inside the system. This isn't fully solved by this spec — it's a deliberate policy choice for whoever launches a new domain's Expert DAO to make explicitly, not something the credential mechanics alone resolve.

---

## 2. Specialized review DAO (the sign-off body)

A `dc-governance` scoped instance — same primitive a coop uses — except membership eligibility is gated on holding the relevant domain's expert credential, rather than being tied to a coop's own member list. One per domain (`SecurityReviewDAO`, `FinanceReviewDAO`, `LegalReviewDAO`, etc.), drawing members from across the entire ecosystem.

---

## 3. Mandatory sign-off mechanism

**This is now a standing requirement, not a threshold-gated option.** Every proposal that falls into a domain with a designated review DAO requires sign-off before execution — replacing the earlier "human sign-off tier" in `00-master-architecture.md` §5.4, which only activated above a blast-radius threshold. Sign-off and the standard governance vote are both required; neither substitutes for the other.

**Routing logic:**

1. On submission, a proposal's domain is checked against the registry of designated review domains (security, finance, legal, and others as the ecosystem adds them).
2. **Self-certification path:** if the originating coop already has at least a defined quorum of members holding that domain's expert credential (e.g., three, ecosystem-configurable per domain), the coop may sign off internally through its own quorum vote — no external routing required. This keeps a well-staffed coop autonomous rather than forcing every decision through a central body.
3. **Routed path:** if the originating body doesn't meet that quorum, the proposal routes to the domain's specialized review DAO, which reviews and either signs off or rejects.
4. Either path produces a **sign-off attestation** — same mechanism as every other record in this architecture, referencing the proposal, the reviewing DID(s), and their credentials.
5. **Emergency fast-track** (005 §3.3, `01-infrastructure-cybersecurity.md` §4): the emergency council itself must include or immediately consult at least one credentialed expert in the relevant domain — sign-off isn't waived for speed, it's compressed into the same emergency path rather than skipped.

---

## 4. Advisory / think-tank function

Beyond mandatory sign-off, a domain's review DAO can be consulted voluntarily — a scope vote or an in-progress proposal can request advisory input even when formal sign-off isn't required for that specific decision. Members can also act proactively: proposing research directions, voting on which open problems the domain considers most pressing, and giving feedback on agent-drafted findings before they reach a formal vote. This is the "specialized think tank" function — standing expertise available for consultation, not just gatekeeping.

---

## 5. Bounty / competition function

A crowdsourced problem-solving mechanic, built entirely on the existing marketplace bounty/escrow mechanism — no new payment rail.

1. **Problem posting.** Any DAO, coop, or an agent itself (an agent's research can surface a problem worth crowdsourcing to human experts, not just AI agents) posts a challenge: problem statement, evaluation criteria, deadline, reward pool.
2. **Escrow.** Funded through the existing staged-release treasury mechanism, same pattern already used for marketplace escrow.
3. **Submission.** Any expert holding the relevant domain credential (or, for domains an ecosystem chooses to open more broadly, any marketplace participant) submits a solution.
4. **Evaluation.** Peer expert vote, optionally pre-screened or ranked by an agent (`role: monitor.*`-class) before final human judgment — a genuine bridge between the agent research loop and human expert deep-dives, not two separate systems.
5. **Reward distribution** on acceptance, per the challenge's stated split (winner-take-all, leaderboard-style, or per-accepted-partial-solution, set at posting time).
6. **Adoption.** A winning solution either becomes a formal proposal through the standard `proposal-engine` pipeline, or is recorded as an attested finding that future agents can read as prior art — closing the loop back into the research context sources DC-DAO-AGENT-LOOP-001 §2 already specifies.
7. **Reputation.** A track record of accepted bounty solutions accrues to the expert's DID via `reputation_ref` (§1) — the same mechanism agents use, now shared.

---

## 6. Sovereignty audit — corrections required by "nothing outside the ecosystem's own infrastructure"

This requirement changes three things recommended earlier in this document set. Stated plainly rather than left inconsistent:

**Independent transparency log (DC-MESHSTORAGE-ARCHIVE-001 §2, §5).** That document recommended anchoring Merkle roots to a log "outside dcentral-core's own operational control" — specifically an external project — as protection against the ecosystem's own operators rewriting history. That's an external dependency, which now conflicts with full sovereignty. **Fix:** replace the external log with an internal N-of-M independent-witness quorum — a randomly selected set of node operators from different, unaffiliated coops co-sign each batch's Merkle root. "Independent" no longer means "outside the ecosystem," it means "no single party inside the ecosystem controls the witness set," achieved by drawing witnesses from enough different coops that no one operator or coalition plausibly controls a majority. This preserves the anti-insider-tampering property without leaving the ecosystem's own infrastructure.

**Arweave / IPFS / Filecoin (DC-MESHSTORAGE-ARCHIVE-001 §1, §5) — resolved, not just flagged.** The original concern stands as stated: these are open protocols, but the live public networks are external infrastructure the ecosystem would be a client of, not infrastructure it operates. The resolution turned out to already be established elsewhere in the taxonomy: `mesh-storage`'s own OSS reference tags Storj as *"already the fork base"* — meaning D-Central runs its own independent network built on Storj's open-source code, not a connection to the live Storj network. Applying that same discipline to IPFS/Filecoin's content-addressing design and Arweave's endowment economic model resolves the archive tier the same way: fork the techniques, run them on D-Central's own nodes, pay the endowment in D-Credit. See DC-MESHSTORAGE-ARCHIVE-001 §0 and §5 for the full mechanism. This was never actually a sovereignty-versus-permanence trade-off — it just hadn't been stated explicitly for this tier yet.

**`mesh-ai` as a "Bittensor-fork" (referenced throughout, originating in the base taxonomy).** A fork of Bittensor's open-source code, run as the ecosystem's own independent network, is sovereign. Connection to the actual public Bittensor chain and its external validator/miner economy is not. Worth confirming explicitly which one is meant, since the difference matters a great deal here and "fork" is ambiguous between the two.

**Orchestration engine (`05-tooling-and-frameworks.md` §1).** The Claude Agent SDK option assumes calling Anthropic's hosted API — an external dependency, and one that also conflicts with the earlier open-source-model requirement. Drop it as an option for production use here; LangGraph or CrewAI, self-hosted, calling `mesh-ai` for inference, is the sovereign-compatible choice already identified as the fallback.

What doesn't need correction: OpenTelemetry, the OTel Collector, Arize Phoenix, Langfuse, DuckDB, ClickHouse, Grafana, Guardrails AI, and NeMo Guardrails are all open-source software you run on your own nodes — dependencies on code, not on someone else's operated service. Self-hosting open-source software is consistent with full sovereignty; depending on an external network or hosted API, even a decentralized or open one, is not.

---

## 7. Gap registry status

**New — #34 `DC-EXPERT-DAO-001`** — specified, this document. Also resolves the "human sign-off tier" inconsistency in `00-master-architecture.md` §5.4 (updated to reference this document) and DC-DAO-AGENT-LOOP-001 §4's guardrail table (same update).

**Resolved since original publication:**
- Archive-tier permanence — resolved by DC-MESHSTORAGE-ARCHIVE-001's §0/§5 update: fork the IPFS/Filecoin and Arweave techniques onto D-Central's own infrastructure, same discipline mesh-storage already applies to its Storj base. No external network dependency.

**Still flagged, requires deliberate confirmation:**
- `mesh-ai`'s relationship to the public Bittensor network needs explicit confirmation.

---

*DC-EXPERT-DAO-001 — specifies the expert credential (domain, licensed or peer-attested credentialing path, shared reputation mechanism with agents), the specialized review DAO as a domain-scoped instance of the existing governance primitive, mandatory (not threshold-gated) sign-off with a self-certification path for well-staffed coops, the advisory/think-tank consultation function, and a bounty/competition mechanic built entirely on the existing marketplace escrow rails. Also performs a sovereignty audit against "nothing outside the ecosystem's own infrastructure," correcting the independent-transparency-log recommendation to an internal witness-quorum design, and flagging (without silently resolving) two real external-dependency decisions: archive-tier storage and mesh-ai's network boundary.*
