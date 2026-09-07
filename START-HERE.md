# START HERE — D-Central Knowledge Base Onboarding Guide

**Read this note first, in Obsidian, with this repo open as your vault.** It assumes you know nothing
about D-Central, nothing about how this knowledge base was built, and nothing about Obsidian beyond
having installed it. Every step below is something you physically click or type — there is no step that
assumes prior familiarity.

Checkboxes are real Obsidian tasks — click them to check off as you go, so you can close this note and
resume later exactly where you left off.

---

## Phase 0 — Set up the vault for maximum visibility (do this once, ~15 minutes)

### 0.1 Open the vault

- [ ] Launch Obsidian.
- [ ] On the vault-switcher screen, click **"Open folder as vault"**.
- [ ] Select `C:\Users\jredj\dcentral-knowledge-base`, click **Select Folder**.
- [ ] If asked "open in new window or replace," either is fine — pick new window if you want to keep
      other vaults open elsewhere.

### 0.2 Turn on the views you'll actually need

- [ ] Right sidebar: confirm the **Backlinks** pane is visible (icon looks like an arrow curving into a
      page). If you don't see it: click the `+` at the bottom of the right sidebar → **Backlinks**.
- [ ] Right sidebar: also add **Outline** (`+` → Outline) — this gives you a clickable table of contents
      for whatever note is open, which matters because several consolidated docs in this vault are
      2,000+ words with 5-6 headed sections.
- [ ] Left ribbon (the thin strip of icons on the far left edge): confirm the **Graph view** icon is
      there (looks like connected dots). If the ribbon is hidden, go to **Settings → Appearance** and
      toggle "Show ribbon" on.

### 0.3 Turn on frontmatter visibility

Every document in this vault has structured metadata at the top (topic, category, status, etc.) — you
want to actually see it, not just the prose.

- [ ] **Settings** (gear icon, bottom-left) → **Editor** → confirm **"Properties in document"** is set to
      **"Visible"** (this is the default in recent Obsidian versions — just confirm, don't need to change
      if already visible).
- [ ] Open any file under `knowledge-base/d-central/` to confirm you see a small gray box at the top
      showing fields like `source_project`, `topic`, `content_hash` before the actual document text
      starts. That box is the frontmatter, rendered.

### 0.4 Set up Graph View groups (so the graph is legible, not a hairball)

- [ ] Click the **Graph view** icon in the left ribbon.
- [ ] A panel opens on the right with **Filters**, **Groups**, **Display**, **Forces** sections.
- [ ] Under **Groups**, click **"+ New group"**.
  - Query: `path:knowledge-base/_topics`
  - Pick a distinct color (e.g. orange) — these are your 80 topic hub notes, the connectors between
    document clusters.
- [ ] Click **"+ New group"** again.
  - Query: `path:docs/DC-`
  - Pick a different color (e.g. green) — these are the 80 Stage-6 consolidated documents, the
    "finished answer" for each topic.
- [ ] Under **Forces**, drag **"Repel force"** up a bit (~1.2×) so the ~470-node graph spreads out enough
      to read individual clusters instead of one dense ball.
- [ ] Close the panel (click the graph icon again) — your groups and force settings are saved
      automatically and will still be there next time you open Graph view.

### 0.5 Pin this note so you can always get back to it

- [ ] With this note (`START-HERE.md`) open, right-click its tab at the top → **Pin**. Now it always
      stays open as your home base no matter what else you navigate to.

### 0.6 (Optional, power-user) Install the Dataview community plugin

This lets you build live tables from frontmatter — e.g. "show me every doc where `status: disputed`" —
without writing Cypher. Skip this section entirely if you just want to read; everything in Phase 1
onward works without it.

- [ ] **Settings → Community plugins** → turn off **Restricted mode** (Obsidian will warn you about
      running third-party code — this is a real warning, community plugins are unreviewed code; Dataview
      specifically is extremely widely used and safe, but the general caution is legitimate).
- [ ] Click **Browse**, search **"Dataview"**, click **Install**, then **Enable**.
- [ ] Test it: open any note, add a code block:
  ````
  ```dataview
  TABLE status, topic FROM "knowledge-base/d-central" WHERE status = "disputed"
  ```
  ````
  You should get back exactly 2 rows — the two genuinely unresolved duplicate pairs Stage 4 found.

**Phase 0 done.** Everything below is reading and clicking, no more setup.

---

## Phase 1 — What is this repo, mechanically? (~20 minutes)

Before touching D-Central's actual content, understand what you're looking at: this vault is the output
of an 8-stage pipeline that took a raw Claude.ai export (743 conversations + 33 projects) and turned it
into a organized, deduplicated, cross-referenced knowledge base. Read these in order:

- [ ] Open **[[README]]** — the repo's own map of itself: what each top-level folder
      (`standards/`, `taxonomy/`, `docs/`, `knowledge-base/`, etc.) contains and why.
- [ ] Open **[[PLAN]]** — read only the top section, "Stage-by-stage status" table. This tells you, as of
      right now, exactly how much of the pipeline is done (all 8 stages, confirmed complete) and where
      the raw source material came from.
- [ ] Open **[[CLAUDE]]** — this is the file that tells *me* (Claude) how to behave in this repo. Skim it
      once so you understand what rules govern how this vault gets updated going forward.

**Checkpoint — you should now be able to answer:** *Where did all these documents originally come from,
and what were the 8 processing steps applied to them?* If not, re-read `PLAN.md`'s stage table.

---

## Phase 2 — The pipeline's own rulebook (~25 minutes)

These are the standards documents that governed *how* every judgment call in this vault was made — read
them so you can evaluate whether a given consolidated document did its job well, rather than taking it on
faith.

- [ ] **[[standards/DC-PIPELINE-STD-001]]** — the master orchestration doc. §1 shows the canonical
      8-stage order (this is the same list `PLAN.md` tracks against).
- [ ] **[[standards/DC-DEDUP-STD-001]]** — the rules for Stage 4 (which duplicate gets kept, which gets
      moved to `_superseded/`, and the "no basis to prefer one" escape hatch for genuine ties — this is
      why 2 documents in this vault carry `status: disputed` instead of a forced verdict).
- [ ] **[[standards/DC-TOPIC-SYNTH-STD-001]]** — the rules for Stage 5 (when documents get clustered into
      one topic vs. left alone). §4's "calibration test" (can you write one honest 2-4 sentence abstract
      without "and" joining two unrelated ideas?) is worth remembering — it's the actual test applied to
      all 59 first-pass clusters.
- [ ] **[[standards/DC-CONSOLIDATOR-STD-001]]** — the rules for Stage 6 (what every `docs/DC-*-
      RECONCILED-*.md` file is required to contain: Current Understanding, Provenance, Unresolved
      Tensions, Sources Consulted, Consolidation Metadata — five sections, always, mechanically checked).

**Checkpoint:** open any file under `knowledge-base/_topics/` (pick one at random) → follow its
"Consolidated doc" link → confirm the target actually has all 5 of those section headers. This is you
verifying the rulebook was actually followed, not just trusting it was.

---

## Phase 3 — What D-Central actually is (the architecture, ~40 minutes)

Now the real content. Read these in this exact order — each one assumes the previous one.

- [ ] **[[standards/00-master-architecture]]** — the foundational design: a closed-loop DAO + AI-agent
      system. Read §1-2 (Purpose, Core Loop) carefully; skim §3+ for now, you'll come back to it.
      **Key idea to hold onto:** agents research and propose, they never unilaterally execute — a DAO
      vote gates every real action. This single rule shapes almost everything else in this vault.
- [ ] **[[taxonomy/DC-TAXONOMY-001-Service-Dependency-Map]]** — the map of every core service D-Central
      is built from and how they depend on each other. This is the single most important reference
      document in the whole vault — nearly everything downstream either builds on one of these services
      or (as you'll see in Phase 5) *should* have and didn't.
- [ ] **[[taxonomy/DC-TAXONOMY-002-Microservices-and-Additional-Verticals]]** — splits `dcentral-core`
      into its 5 real independent services. §1.1 specifically defines `dc-identity` (`did-registrar` +
      `vc-issuer`) — remember this section, you'll use it directly in Phase 5.
- [ ] Skim (don't deep-read yet) **[[taxonomy/DC-TAXONOMY-003-OSS-Tags-and-Missing-Verticals]]** through
      **[[taxonomy/DC-TAXONOMY-009-802-1X-Unified-Access]]** — just get a sense of what each one covers by
      its title and first paragraph. You'll return to specific ones as needed once you're exploring a
      particular vertical.

**Checkpoint:** you should now be able to name the 5 core services under `dcentral-core` and explain what
`dc-identity` actually consists of, from memory, without looking.

---

## Phase 4 — The agent/governance layer in detail (~30 minutes)

These flesh out the "closed-loop DAO" idea from `00-master-architecture.md` into concrete, implementable
specs.

- [ ] **[[docs/DC-DAO-AGENT-LOOP-001]]** — the full agent-loop spec.
- [ ] **[[docs/DC-DAO-AGENT-LOOP-USER-STORIES-001]]** — the same system, told as concrete worked
      scenarios. Read this even if the previous doc felt abstract — the user stories make it click.
- [ ] **[[docs/DC-AGENT-CREDENTIAL-001]]** — how an individual AI agent gets an identity. Notice its own
      opening line: *"Not a new identity system — a new credential type within the existing `dc-identity`
      service."* This is a document explicitly built to reuse the core service from Phase 3, not invent
      its own — hold this up as the example of "doing it right," because Phase 5 will show you cases that
      didn't.
- [ ] **[[docs/DC-EXPERT-DAO-001]]** and **[[docs/DC-EXPERT-REVIEW-001]]** — how specialist review fits
      into the loop.
- [ ] **[[docs/DC-AGENT-OBSERVABILITY-001]]** and **[[docs/DC-VERIFIABLE-ROLLOUT-001]]** — how the system
      watches itself and rolls out changes safely.
- [ ] **[[docs/DC-KNOWLEDGE-LAYERS-001]]** and **[[docs/DC-MESHSTORAGE-ARCHIVE-001]]** — where all of this
      actually gets stored/remembered long-term (this is the same memory-tier design
      `standards/04-context-engineering-standards.md` from Phase 2 assumes exists).

**Checkpoint:** pick one `docs/DC-LKB-00{1,2,3}` file (Lakou Protocol banking — the economic engine behind
payouts in this loop) and read it now too; it's short and it's the thing that makes "agents propose,
DAO approves, someone actually gets paid" concrete.

---

## Phase 5 — Explore by topic, and practice spotting the gaps yourself (~1-2 hours, self-paced)

This is where you stop following a fixed order and start exploring — but with a specific skill to
practice: **checking whether a topic's content actually reuses the core services from Phase 3, or quietly
reinvented its own version.**

### 5.1 The browsing pattern

- [ ] Open the **[[knowledge-base/_topics_summary]]** note — one paragraph, tells you there are 80
      confirmed topics and points at the full list.
- [ ] Open **[[knowledge-base/_topics]]** — the full list of all 80 topics with their member documents.
      This is your menu. Scroll it once just to see the range (blockchain/education, Haiti-focused
      clusters, CivicMesh/TrafficMesh, OpenSecure/IHOSE security platforms, D-Central core narrative,
      ChopShop — an unrelated personal project that happened to share the export).
- [ ] Pick any topic name that sounds interesting. Instead of clicking its raw member docs directly, go
      to **`knowledge-base/_topics/<that-topic-name>.md`** first — every topic has a hub note there
      listing its consolidated doc and every member, e.g. open
      **[[knowledge-base/_topics/blockchain-education-federation]]** as a worked example right now.
- [ ] From the hub note, click through to its **Consolidated doc** link first (read that one fully) —
      *then* dip into 1-2 raw member docs only if the consolidated doc's "Unresolved Tensions" section
      makes you want to see the original wording.

### 5.2 The specific gap-hunting exercise

Do this once, on a topic of your choosing, to build the muscle:

- [ ] Open the consolidated doc for your chosen topic (`docs/DC-*-RECONCILED-*.md`).
- [ ] Use Obsidian's search (`Ctrl+Shift+F`) for `did-registrar` or `dc-identity` scoped to that one file
      (`Ctrl+F` within the open note instead, if you just want to search this file).
- [ ] If the doc discusses any kind of identity, credential, or verification and *doesn't* mention those
      terms — you've just found a candidate for the same gap already confirmed in this vault: **34 of the
      80 consolidated topics discuss DID/VC/credentialing content, and only 1
      (`docs/DC-DION-RECONCILED-001.md`) actually references the core `dc-identity` service by name.** The
      other 33 (e.g. CivicMesh's wallet infrastructure, the OpenSecure Provincial PIV system, Haiti Drone
      Zoe's credentialing platform) each built a fully independent identity mechanism, never checked
      against the core spec.
- [ ] Open **[[docs/DC-DION-RECONCILED-001]]** as the positive example — this is the one topic where that
      exact reconciliation was actually done. Compare its "Current Understanding" section (which
      explicitly cites `did-registrar`/`vc-issuer`) against a topic you suspect didn't do this.
- [ ] Read **[[CROSS-POLLINATION-FINDINGS]]** — this is the write-up of that exact DION discovery, and it
      names other categories worth checking the same way (a `verticals-products` cluster and an
      `ai-ml-research` cluster both showed 50%+ overlap with core D-Central vocabulary).

**Checkpoint:** you should now be able to open any random consolidated doc in this vault and, within two
minutes, form a real opinion on whether it reused D-Central's core services correctly or quietly
reinvented something — the same judgment call `DC-DION-RECONCILED-001` required someone to make by hand.

---

## Phase 6 — See the whole shape at once (Graph View + Neo4j, ~20 minutes)

By now you've read documents one at a time. This phase is about seeing the *shape* of the whole
corpus.

- [ ] Open **Graph view** (`Ctrl+G`, or the ribbon icon). With the groups from Phase 0.4 active, you
      should see: a scatter of small nodes (raw documents), pulled toward orange nodes (topic hubs), each
      orange node connected onward to one green node (its consolidated doc).
- [ ] Click on one green node (a consolidated doc) — everything not directly connected to it dims. This
      is "show me everything that fed into this one finished answer," visually.
- [ ] Find a node with **no connections at all** drifting at the edge of the graph — that's one of the 96
      documents Stage 5 correctly left ungrouped (nothing else in the corpus was close enough in subject
      to cluster it with). Open it and see why it stands alone.
- [ ] If you have Neo4j running (see `docs/NEO4J-RASPBERRY-PI-SETUP.md` if not), open
      `http://<pi-ip>:7474` in a browser and run:
      ```cypher
      MATCH (d:Document) WHERE NOT (d)-[:IN_TOPIC]->() RETURN d.path, d.category
      ```
      — same "ungrouped documents" question as above, but as an exact list instead of visual
      spotting. Compare the two approaches: Obsidian for browsing/intuition, Neo4j for a precise answer.

---

## Phase 7 — Registry and status files (reference material, read as needed)

You don't need to read these front-to-back — know they exist and what each answers:

- [ ] **[[knowledge-base/_INDEX]]** — the single-page numeric summary of every stage's output (doc
      counts, dedup counts, topic counts). Your go-to when you just want "how big is this, exactly."
- [ ] **[[TOPIC-RESOLUTION]]** — the detailed reasoning behind every topic split/merge/demotion decision
      in Stage 5, including the "different Claude Project ≠ different subject" correction. Read this if
      you ever wonder *why* two seemingly-unrelated projects' docs ended up in the same topic.
- [ ] `registry/consolidated-topics.json` and `registry/materialized-manifest.json` — not meant to be
      read as prose; these are the machine-readable versions of everything Phases 5-6 showed you visually.
      Open them only if you're about to write a script or a Cypher query against this corpus and need the
      exact schema.

---

## What "fully acclimated" looks like

You're done with this guide once you can, unprompted:
1. Explain what `dc-identity`, `dc-governance`, and `dc-attestation` each do, and name one document that
   correctly reuses each.
2. Pick any of the 80 topics and know exactly which file to open first (its hub note) and where to look
   if you're skeptical of its conclusions (its "Unresolved Tensions" section).
3. Tell the difference between "this vault's own governing rules" (Phase 2, `standards/`), "what
   D-Central actually is" (Phase 3-4, `taxonomy/` + `docs/`), and "the raw material those rules were
   applied to" (Phase 5, `knowledge-base/`).
4. Independently spot a case like the DION/dc-identity gap in a topic nobody's checked yet.

From here, the corpus is yours to explore associatively — follow whatever `[[link]]` looks interesting
and trust the structure to get you back to solid ground.
