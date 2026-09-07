# DC-EXPERT-REVIEW-001: Credentialed Sign-Off, Review DAOs & Expert Guilds
### Extends DC-DAO-AGENT-LOOP-001, DC-AGENT-CREDENTIAL-001. Formalizes the "technical steward" / "technical council" / "licensed reviewer" placeholders used throughout the earlier document set.

---

## 0. Two mechanisms, one foundation

- **§1–3: Mandatory sign-off routing.** Every proposal above a domain-relevant threshold requires a credentialed expert vote before it can execute — sourced in-house if the originating DAO has the credentials, routed to a specialized Review DAO if not. Sovereign by default, with one honest carve-out.
- **§4–6: Expert guild DAOs and the challenge arena.** Standing bodies of credentialed specialists that advise, take assigned tasks, and run open crowdsourced challenges — a decentralized bug-bounty/Kaggle pattern, built entirely from machinery this architecture already has (bounty escrow, attestation, voting).

Both run on the same credential type, defined first.

---

## 1. Expert credential (human, parallel to the agent-class credential)

A DID-bound VC, structurally similar to DC-AGENT-CREDENTIAL-001's agent credential but for a human expert, and permissioned differently:

| Field | Purpose |
|---|---|
| `subject_did` | The expert's own DID |
| `domain` | e.g. `security`, `finance`, `legal-compliance`, `protocol-engineering` — namespaced the same way agent roles are |
| `tier` | e.g. `associate` / `senior` / `principal` — gates which sign-off thresholds this expert is eligible to vote on (see §3) |
| `credential_basis` | How this was earned — see §2 |
| `track_record_ref` | Pointer into the attestation history backing this credential's standing |
| `guild_membership` | Which guild DAO(s) this credential grants voting rights in |

**Permission difference from the agent credential:** an expert credential grants scoped `voting-engine` access for sign-off votes in its domain — something no agent-class credential is ever granted (master doc §5.1 still holds without exception; sign-off authority is human-only by design, not an oversight).

---

## 2. Earning the credential, sovereignly — with one honest limitation

**Peer attestation, bootstrapped from a genesis set.** A new expert credential requires a minimum number of attestations from existing, already-credentialed experts in the same domain (or, during initial bootstrap before a domain has enough members, from an adjacent already-established domain). This is fully sovereign — no external body is needed to mint a credential.

**Track-record accrual.** A credential's tier rises as the expert's sign-offs, proposals, and challenge submissions (§5) are later validated by outcome-review — the same accrual pattern already specified for agent reputation (DC-AGENT-CREDENTIAL-001 §4), applied to humans. An expert whose sign-offs consistently precede clean outcome-reviews earns standing over time; one whose sign-offs precede repeated rollbacks does not, visibly.

**The honest limitation:** for domains where the sign-off requirement exists because of real-world legal or regulatory liability — the licensed-human-reviewer floor already set in `03-business-operations.md` §1 for legal/compliance is the clearest example — a sovereignly-bootstrapped peer-attestation credential cannot substitute for an actual bar license or equivalent professional credential. What *can* stay sovereign: the VC representing that license can be verified and used within the system without the system depending on the licensing body's infrastructure day to day. What can't: the underlying legitimacy of "this person is actually licensed to practice law in this jurisdiction" still traces back to something outside D-Central's control, because that's a property of the law, not a limitation of this architecture. Worth stating plainly rather than claiming full sovereignty is achievable everywhere it's wanted — for domains without an external legal-liability requirement (security research on the mesh's own code, protocol engineering, economic modeling), the peer-attestation path is fully sufficient and fully sovereign.

---

## 3. Sign-off routing

1. At synthesis time, a proposal above its branch's blast-radius threshold is tagged with the domain(s) its sign-off requirement falls under (a treasury proposal might need `finance`; a protocol change might need `security` and `protocol-engineering` both).
2. **Routing check:** does the originating DAO/coop have at least N members holding a sufficiently-tiered credential in that domain? (This is the "or if the DAO has sufficiently credentialed people" case.)
   - **Yes** → sign-off vote runs in-house, scoped to only the credentialed members, not the general membership — a domain-gated sub-vote within the originating body.
   - **No** → the proposal, its evidence, and its mandate reference are submitted to the relevant guild's Review DAO (§4). That guild's credentialed membership votes to sign off, reject, or return for revision — functionally identical to an in-house vote, just running in a different governance body scoped for exactly this.
3. **The routing decision and the resulting vote are both attested.** Which body actually signed off on a given proposal, and on what basis, is part of the permanent record — not an implicit fact someone has to reconstruct later.

---

## 4. Guild DAOs — structure

One guild per domain (security, finance, legal-compliance, protocol-engineering, and others as they become warranted), membership gated by holding that domain's credential at or above a minimum tier. Four functions:

1. **Sign-off votes** routed in from other DAOs per §3.
2. **Standing advisory output** — position papers and consensus statements, rendered into the shared wiki space, citable by any DAO's governance discussion without a formal request. This is the "think tank" function named directly — a guild doesn't only react to routed requests, it can publish guidance proactively.
3. **Assigned tasks** — any DAO or coop can post a scoped task (not necessarily a sign-off, just work — "audit our node-onboarding flow for social-engineering risk") to a guild, matched to available members by credential and declared availability, compensated the same way any commissioned work is (006 §1.4's bounty pattern).
4. **The challenge arena** (§5).

Guilds vote on their own internal matters — accepting new members through the §2 peer-attestation flow, adopting a consensus statement — using the same `voting-engine` any DAO already uses. No separate voting mechanism needed; a guild is a DAO, scoped by credential-gated membership instead of open membership.

---

## 5. Crowdsourced challenge arena

Any DAO, coop, individual, or a `research.*`-role agent acting on a DAO's behalf can post a **challenge**: a scoped problem statement, an evaluation method, and a reward pool escrowed in D-Credit the same way MeshBuild's milestone escrow already works. Two evaluation shapes, matching the two patterns named directly:

**Objective / leaderboard (Kaggle-style).** The challenge defines a held-out test set or a measurable criterion; submissions are scored automatically and ranked; the reward pool splits across the top-N submissions per a formula disclosed up front. Fits: performance/optimization problems, model-quality challenges ("best anomaly-detection method for mesh-sensors data"), anything with a clean objective metric.

**Peer-judged (bug-bounty style).** Submissions are evaluated by a randomly-selected panel drawn from the relevant guild's credentialed membership — randomly selected specifically to resist collusion — against a rubric disclosed up front. Reward tiers reflect severity/impact, the same triage discipline real bug-bounty programs use. Fits: security vulnerability disclosure, compliance gap-finding, anything where "correct" isn't a single number.

Every submission, evaluation, and payout is attested. A challenge's complete history — who submitted what, how it was scored, who won — becomes part of the same public/verifiable record as everything else in this architecture, not a separate leaderboard someone has to trust on faith.

**Winning a challenge produces a proposal input, not an execution right.** A winning submission that's meant to become an actual system change still goes through the standard proposal pipeline (DC-DAO-AGENT-LOOP-001 §2) — this keeps "propose, don't unilaterally execute" intact even for challenge-sourced work, the same discipline applied everywhere else in this architecture.

---

## 6. Interplay with the agent loop

- **A guild can itself be the subject of a research mandate.** An ecosystem-tier mandate asking "does our security guild have adequate coverage for [emerging vulnerability class]" is a valid `research.*` agent task — its findings can recommend recruiting more guild members or posting a challenge.
- **Agents can participate in challenges** where appropriate — a `research.*` agent submitting a candidate fix to a posted bug-bounty-style challenge. Any agent-submitted entry into a peer-judged challenge must be visibly tagged as agent-submitted in the record, so the judging panel and anyone reading the history later aren't misled about who's actually competing. This isn't a restriction on agents entering — it's the same disclosure discipline this architecture already applies everywhere else, now applied to challenge provenance.

---

## 7. OSS / pattern references

No new identity or voting infrastructure needed — this reuses `dc-identity`'s existing VC tooling and `dc-governance`'s existing voting/escrow machinery entirely. For the challenge-arena *pattern* specifically (not as dependencies to adopt, since neither is DID/VC-native or decentralized in governance): Gitcoin's permissionless grants/bounty coordination is a reasonable prior-art reference for the objective/leaderboard shape; established bug-bounty triage platforms are a reasonable prior-art reference for the peer-judged severity-tiering shape. Worth studying both for UX and triage-rubric conventions, not worth depending on either as infrastructure.

---

## 8. Gap registry status

**#34 `DC-EXPERT-REVIEW-001` — specified, this document.**

---

*DC-EXPERT-REVIEW-001 — extends DC-DAO-AGENT-LOOP-001 and DC-AGENT-CREDENTIAL-001. Specifies a human expert credential (domain, tier, peer-attestation basis, track-record accrual — sovereign by default, with an explicit carve-out for domains where sign-off exists because of real-world professional licensure, which cannot be sovereignly generated). Specifies sign-off routing: in-house if the originating DAO holds sufficient credentialed membership, otherwise routed to a specialized Review DAO — with the routing decision itself attested. Specifies guild DAOs as credential-gated standing bodies with four functions (routed sign-off, proactive advisory output, assigned tasks, and a crowdsourced challenge arena supporting both objective/leaderboard and peer-judged/bug-bounty evaluation), with challenge outcomes feeding the standard proposal pipeline rather than executing directly.*


<!-- AUTO-GENERATED RELATED START (scripts/build_docs_graph.py) -->

## Related (auto-generated)

*No cross-references detected to/from other docs/*.md files.*

<!-- AUTO-GENERATED RELATED END -->
