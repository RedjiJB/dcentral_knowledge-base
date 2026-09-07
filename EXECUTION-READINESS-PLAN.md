# Execution Readiness Plan

**What this is:** two problems, one plan. Part A is the canonical cross-reference fix scoped in the
previous conversation (referential integrity between core services and everything that uses them). Part
B is what that investigation surfaced as a bigger, more urgent gap — the entire corpus's own execution
discipline points at a document that doesn't exist in this repo. Part C is a wider brainstorm of what
else keeps this a design exercise instead of an operating system. Part D is the priority order.

Nothing in this plan has been executed yet — this is the scope, not the result.

---

## Part A — Canonical Cross-Reference Enforcement

### A.1 The problem, named precisely

**Specification drift** (implementations diverging from an agreed canonical spec because nothing checks
new work against it), manifesting as **shadow architecture** (a document builds its own complete
identity/compute/storage stack instead of reusing the canonical one), which is really a **missing
referential-integrity** problem: `taxonomy/DC-TAXONOMY-002.md` §1.1 defines `dc-identity` once,
authoritatively, and nothing requires any other document that talks about DIDs/VCs to link back to it —
the "foreign key" is optional in practice, so it's usually just absent.

**Confirmed scope, not estimated:** 34 of 80 consolidated Stage-6 topics discuss DID/VC/credentialing
content. Exactly 1 (`docs/DC-DION-RECONCILED-001.md`) references `dc-identity`/`did-registrar`/`vc-issuer`
by name — and only because someone specifically went and checked that one case
(`CROSS-POLLINATION-FINDINGS.md`). The other 33 were never checked. Two spot-checked just now
(`DC-CM-WALLET-001`, the OpenSecure Provincial PIV system) both confirmed as genuine independent
stacks, not false alarms.

### A.2 Deliverables

1. **`registry/canonical-concepts.json`** — one entry per core service named in
   `taxonomy/DC-TAXONOMY-001-Service-Dependency-Map.md` and `DC-TAXONOMY-002-Microservices-and-Additional-Verticals.md`
   §1-2 (at minimum: `dc-identity`, `dc-governance`, `dc-attestation`, `dc-credit`, `mesh-storage`,
   `mesh-compute`, `mesh-connectivity`, `mesh-ai`, `mesh-bandwidth`, `mesh-energy`,
   `mesh-sensors-mobility`, `mesh-geo`, `selective-disclosure-engine`). Each entry: canonical doc path +
   defining section + a curated detection-keyword list (e.g. `dc-identity` → `did-registrar`,
   `vc-issuer`, `verifiable credential`, `DID`, `decentralized identity`).
2. **`scripts/detect_canonical_gaps.py`** — greps all 472 docs (live + superseded, for completeness)
   against every service's keyword list; for each hit, checks whether the doc already links to that
   service's canonical doc (front matter or body). Outputs `registry/canonical-gaps-report.md`: one
   section per service, listing every doc that mentions it without linking to it. This is Stage 7's
   `check_drift.py` pattern applied to concepts instead of supersession pointers — mechanical, no
   judgment calls, safe to run unattended.
3. **A reconciliation pass, per flagged doc** — for each real gap (not a false alarm), add a
   `reconciliation_note` (same field DION already carries) plus an `implements_service:` front-matter
   list, without rewriting the document's own content. This mirrors exactly how `consolidated_into:` was
   added in Stage 7 — additive, non-destructive.
4. **Wire it into both views** — an `[[wikilink]]` to the canonical doc in the `## Related` block
   (Obsidian), and a new `Service` node type + `IMPLEMENTS_SERVICE` edge (Neo4j), parallel to how `Topic`/
   `IN_TOPIC` already work.
5. **Make it stick** — add a mechanical check (alongside the existing exhaustiveness check in
   `mark_topic_consolidated.py`) so a *future* Stage 6 consolidation can't be marked done if it uses
   core-service vocabulary without the matching reference.

### A.3 Effort shape

Step 2 (detection) is cheap and mechanical — one script run, minutes. Step 3 (reconciliation) is the real
work and scales with how many gaps step 2 actually finds — `dc-identity` alone was 33 candidates; total
across ~12 services is unknown until the detector runs. **Recommend running steps 1-2 first, standalone,
before committing to the full reconciliation effort in step 3** — you want the real number before
scoping the work, not an estimate.

---

## Part B — The DC-STATUS-001 gap (found during Part A's investigation, more urgent than Part A)

### B.1 What was found

`DC-STATUS-001` does not exist anywhere in this repository — not in `docs/`, not in `knowledge-base/`,
not in `taxonomy/`, not in `registry/`. And yet it is cited, by name, as the authoritative source for the
ecosystem's core execution discipline in **at least 15 separate documents** spanning governance, security,
hardware, mesh-services, and the simulation lab, including:

- The "design-complete, execution-zero artifacts accumulating while the critical path starves" failure
  mode — named explicitly as *the* standing risk pattern, referenced by `DC-MSOC-001`, `DC-TPL-000`,
  `DC-CAMPUS-001`, and others as the reason a given purchase/build should *not* happen yet.
- The "Company Zero incorporation and first invoice" critical-path gate — the single blocking action
  named by `DC-LIC-001`, `DC-VENTURE-001`, `DC-SIM-006`, and `DC-SIM-008` as what everything else in the
  ecosystem is waiting on.
- A specific revenue target ("$1,180-$1,680/month by Month 5-6") attributed to its critical path, in
  `DC-VENTURE-001`.
- The "95% designed, 0% executed" figure that `DC-SIM-000` uses to justify its own scope discipline.

This is a **dangling canonical reference at the highest level of authority in the corpus** — worse than
any individual `dc-identity` gap, because this is the document everything else's execution discipline is
supposedly derived from, and it isn't here to check any of those derived claims against.

### B.2 Two possible explanations, and what each implies

1. **It exists as an unextracted conversation artifact**, the same way `DC-LKB-001/002/003` and the whole
   `DC-SIM-*` series were found — created inline via a `create_file` tool-use block in some conversation,
   never uploaded to a Project KB, and therefore invisible to Stage 2's extraction (which only scans
   project KB docs, not conversation tool-use blocks — a gap `PLAN.md` already flags as systemic: *"an
   unknown number of other DC-*-NNN docs likely exist the same way... Stage 2 as currently built has no
   way to find them systematically"*).
2. **It was never actually written** — referenced in later documents as if it existed because the author
   was working from a mental model of "what the gap analysis would say" rather than a written artifact.

### B.3 Recommended action

1. **Search first, write second.** Before drafting a replacement, do a targeted scan of
   `raw-export/conversations/conversations.json`'s tool-use blocks for `create_file` calls whose content
   mentions `DC-STATUS-001` or matches its described content (a gap/status analysis, the "design vs.
   execution" audit, the incorporation critical path) — same method used to recover `DC-LKB-*`. This is a
   scoped, mechanical search, not a full re-read of the 320MB export.
2. **If found:** extract it into `docs/DC-STATUS-001.md` with the same `extraction_method` front-matter
   convention `DC-LKB-*`/`DC-SIM-*` use, and it immediately becomes checkable — every one of those 15
   citing documents can be verified against what it actually says, not what it's assumed to say.
3. **If genuinely not found anywhere:** it needs to be *written*, but written as reconstruction from its
   15 citations (which collectively describe its content in enough detail to reconstruct the critical
   path and failure-mode framing accurately) rather than invented fresh — and it should carry a front-
   matter note disclosing that it's a reconstruction, not a recovered original.
4. Either way, once it exists: verify each of the 15 citing documents' specific claims about it (the
   revenue figure, the failure-mode framing, the incorporation gate) actually match, and fix any
   documents where a citation drifted from what the real document says.

---

## Part C — Broader brainstorm: what else keeps this "designed, not executed"

The corpus's own recurring self-diagnosis (per the DC-STATUS-001 citations above) is that documentation
accumulates while nothing gets built. Beyond Parts A/B, here's what else stands between this repo and an
actual operating system, roughly grouped:

### C.1 The one piece of real code isn't in this repo

`dcentral-fieldops` (referenced in `docs/PLATFORM_ARCHITECTURE.md` and `docs/SECURITY_AUDIT.md`) is a
real, running, single-tenant codebase — the *only* confirmed piece of executed D-Central code across the
whole corpus. It's not vendored or linked from here. **Action:** add a pointer (repo URL, or a
`reference/dcentral-fieldops-LOCATION.md` note) so anyone reading `PLATFORM_ARCHITECTURE.md`'s migration
plan can actually find the codebase it's migrating *from*. Right now that document assumes the reader
already has the codebase in front of them — true for its original author, not for a future reader of this
vault.

### C.2 DC-SIM-000's own stop condition is the highest-leverage executable step in the entire corpus

Already scoped in exhaustive detail (`docs/DC-DCENTRAL-SIMULATION-LAB-RECONCILED-001.md`): boot a
Buildroot DC-OS image under QEMU, bridge a physical Raspberry Pi 5 into the simulated topology, pass
Scenario 1. This is explicitly called "the first executable artifact in the D-Central stack" by its own
source document (`DC-SIM-003`), and its status is "specification — build not started." **Action:** if one
concrete thing gets built next, this is the candidate with the most supporting design work already done
and the clearest, narrowest stop condition of anything in the corpus.

### C.3 The government-funding paperwork is 100% unwritten

`DC-CM-REG-001` (CivicMesh Document Registry) lists 54 planned documents across 8 tiers — legal
incorporation, IRAP/SR&ED/ISC/Mitacs applications, technical specs — and every single one is marked 📋
**Not Yet Produced**. Several carry explicit urgency notes in their own registry entries: *"File before
spending"* (IRAP), *"Day 1 — non-negotiable"* (SR&ED ledger). This is the CivicMesh-specific instance of
the exact DC-STATUS-001 pattern: the incorporation/funding critical path is fully scoped and entirely
unstarted. **Action:** this 54-document backlog deserves its own tracked punch list (which of the 54 are
true blockers vs. which can wait) — it's currently just prose inside one registry document, not something
anyone's actually working through in order.

### C.4 Every consolidated doc's "Unresolved Tensions" section is a scattered to-do list

All 80 Stage-6 consolidations have an Unresolved Tensions section — some genuinely substantive (the
Haiti-cooperative-resilience topic's discovery of 3 copies of the same master document; the IHOSE/DION
tooling conflicts; the DC-SIM-007→009 revenue-contract correction). Right now these only exist as prose
buried inside 80 separate files. **Action:** a single aggregated `registry/unresolved-tensions-backlog.md`
(mechanically extractable — every doc has that section under a fixed heading) turns 80 scattered
"someone should look into this" notes into one prioritizable list.

### C.5 Near-duplicate content that exact-hash dedup (Stage 4) structurally cannot catch

Stage 4 only catches byte-identical duplicates. Several Stage 6 consolidations surfaced *near*-duplicate
clusters that Stage 4 never touched because they're not exact matches: the Haiti framework's
same-document-three-formats case, OpenVision's four-drafts-of-one-architecture-doc case, ChopShop's three
confirmed pairs plus a four-way README/summary cluster, the two "D-Central Master Explanation" copies, the
likely-related `chatgpt-md`/`chatgpt-organized-md` pair. Each of these was individually flagged as a
"Stage 4 dedup-review candidate" inside its own consolidated doc's Unresolved Tensions section — none has
actually been resolved. **Action:** these are enumerable the same way as C.4 (grep all 80 docs for "dedup
candidate"/"duplicate" in their Unresolved Tensions sections) and form a concrete, scoped Stage-4.5 pass:
near-duplicate detection via content similarity, not hash equality.

### C.6 Registry/index documents can silently drift from the corpus they describe

Already caught once: `TOPOLOGY-SUITE-SUMMARY.md` claims a 10-document suite for services (OS-PACS,
OS-CONCIERGE) that aren't even members of its own topic, while omitting OS-DRONE and the OpenSecure Hub
docs entirely — almost certainly because the summary predates those being written and nobody regenerated
it. **Action:** any other hand-written summary/index document making claims about "what exists" (as
opposed to mechanically-generated ones like `knowledge-base/_INDEX.md`) is a candidate for the same drift
— worth a pass checking every such document's claimed inventory against the actual corpus.

### C.7 No automation actually runs the pipeline's own re-run triggers

`DC-PIPELINE-STD-001` §3 specifies real triggers ("New conversation ingested → triggers 1-3 immediately,
then queues 4-6 re-run"; "Periodic backstop sweep"), but nothing in this repo actually executes on a
trigger — every stage so far has been a manually-invoked skill/script, once, over the existing static
export. **Decision needed, not yet made:** is this corpus a one-time historical migration (in which case
the trigger language in the standard is aspirational/future-facing and that's fine), or is new content
expected to keep arriving (in which case the triggers need real automation — a hook, a scheduled task, or
at minimum a documented manual re-run cadence)?

### C.8 DC-REG-001 (the old manual registry) is deprecated but not formally retired

`README.md` already says both `DC-REG-001-Master-Registry*.md` files are "self-described as incomplete,
unverified... not maintained going forward," and that the new pipeline is "intended to supersede" them —
but nothing points anyone landing on those files toward the replacement (`registry/materialized-manifest.json`
+ `knowledge-base/_INDEX.md`). **Action:** a short redirect note at the top of both old registry files,
pointing at their replacements — cheap, and prevents a future reader from treating a known-stale document
as current.

---

## Part D — Suggested priority order

Ranked by (a) how load-bearing the gap is to everything else, and (b) how cheap the first diagnostic step
is relative to the value of knowing the real scope:

1. **B — find or reconstruct DC-STATUS-001.** Fifteen documents' stated execution discipline is
   unverifiable until this exists. The search step alone (B.3.1) is cheap and might resolve this
   immediately, the way the `DC-LKB-*` search did.
2. **A, steps 1-2 only (registry + detection, no reconciliation yet).** Cheap, mechanical, and tells you
   the *true* scope of the shadow-architecture problem across every core service, not just the 34-topic
   estimate for `dc-identity` alone. Decide on the reconciliation effort (A.2 step 3) only after seeing
   real numbers.
3. **C.5 — enumerate the near-duplicate backlog.** Also cheap (grep 80 files for a known pattern), and
   directly extends work Stage 4 already started but structurally couldn't finish.
4. **C.4 — aggregate the Unresolved Tensions backlog.** Same cheap-enumeration shape as #3, and it's the
   thing that makes #2 and #5 easier to act on once you have a real gap list to prioritize against.
5. **C.2 — the DC-SIM stop condition**, if/when the actual engineering-build phase starts. Everything
   above this line is documentation hygiene; this is the first line item that's actually *building
   something*, and it's the most fully-scoped executable candidate in the whole corpus.
6. **C.1, C.3, C.6, C.7, C.8** — lower urgency, take as-needed rather than in sequence; none blocks the
   others.

Items 1-4 are all cheap diagnostic/enumeration passes before any heavy reconciliation work — the point is
to know the real shape of every gap before committing effort to closing any one of them.
