# Registry Organization & Conversation Management Guide
**For D-Central and personal knowledge management**

---

## The Problem You're Solving

You have 500+ documents across 60+ components, with 713 past conversations. You've already hit reconciliation gaps:
- **ProvisioningDAO** claimed by two different places  
- **SHI/connectivity** never unified despite being built in separate chats  
- **SkyLedger ecosystem** touching five different contexts with no single source of truth

This isn't a filing problem — it's a visibility problem. The registry fixes that.

---

## What You Have Right Now

### Files Provided

1. **dc_registry_extracted.csv** (135 documents found)  
   Auto-extracted from 713 conversations using pattern matching. One row per doc ID.  
   Columns: `doc_id`, `mention_count`, `inferred_status`, `source_conversations`, `sample_context`

2. **DC-REG-001-Master-Registry.md** (draft v0.1)  
   Hand-curated registry you started earlier, organized by category with status and scope for major items.

3. **build_registry_local.py**  
   Python script that extracted the CSV above. Reusable — run it again after a batch of new chats.

4. **build_registry_from_export.py**  
   Alternative: processes exports with Haiku API for richer extraction (requires ANTHROPIC_API_KEY).  
   Slower but more accurate at inferring scope and category.

---

## Recommended Structure: Projects + Master Registry

### Use Claude Projects (Built-in)

Projects are Claude's native organizational unit — each has its own chat history and a shared knowledge base.

**Proposed structure:**

```
D-Central Core Architecture
├── network/DAO governance, DID/VC, D-OS, MeshISP, CoN, DC-SIM
├── identity/cryptography, Lakou Protocol, CTS, D-CERT
└── shared knowledge base: DC-REG-001 (master registry)

D-Central Verticals  
├── MeshEats, OpenSecure, SkyLedger, D-Learn, Sod Boys FieldOps
└── shared knowledge base: DC-REG-001 

Algonquin Coursework
├── CST8200/8305/8315/8324, MAT8002, GEN1957
└── shared knowledge base: DC-REG-001

Personal / Career
├── Master Timeline, D-CERT curriculum, job search, Daily Tracker
└── shared knowledge base: DC-REG-001
```

**Why this matters:** When you start a new chat in "D-Central Core Architecture," Claude can see DC-REG-001 immediately and check if you're about to rebuild something that already exists.

---

## Registry Workflow

### 1. Upload DC-REG-001 to Each Project's Knowledge Base

Once you've split conversations into Projects:
- Go to each Project → Settings → Knowledge Base → Upload "DC-REG-001-Master-Registry.md"
- This is a one-time setup

Now when you start a chat in that Project and ask "Have we built X before?", Claude has the context.

### 2. Add a Row Every Time You Close a Document

**Single habit that prevents gaps:** When a chat produces a new document (DC-XXX-001, OS-YYY-ZZZ, etc.), add one line to DC-REG-001 *before* closing the chat:

| DC-MESHISP-ARCH-001 | MeshISP full architecture | Complete | [link to chat] |

That's it. Five seconds per document. This is what would have caught the ProvisioningDAO duplication.

### 3. Rename Chats to Match the Documents They Produce

Auto-generated titles are useless. Rename them to the document ID:

- ❌ "D-Central ISP implementation in Haiti" → Claude's sidebar search can't find it reliably
- ✅ "DC-ISP-HT-001 — Haiti pilot topology and BOM" → Crystal clear, matches registry

**Benefit:** My conversation search (`conversation_search`) now finds the right chat instantly. The sidebar becomes searchable.

### 4. Refresh the CSV Registry Periodically

When you've accumulated a batch of new conversations:
```bash
python3 build_registry_local.py /path/to/export
```

This takes 30 seconds and outputs a fresh `dc_registry_extracted.csv` with any new docs you've discussed. Fold the new rows into DC-REG-001.

---

## Merge Strategy: CSV → Master Registry

You now have:
- **CSV (auto-extracted):** 135 docs, shallow scope/status  
- **DC-REG-001 draft:** Major docs, hand-curated, deeper context

**Merge process:**

1. Open both files
2. For each row in the CSV:
   - If `doc_id` already exists in DC-REG-001 → skip (human version is more complete)
   - If `doc_id` is new → add it to DC-REG-001's appropriate category with status from CSV
3. For rows that overlap, check for conflicts — e.g., if CSV says "draft" but DC-REG-001 says "complete", trust the human version

**Quick dedup in spreadsheet:**
- Sort both by `doc_id`
- Use a VLOOKUP or manual side-by-side comparison to identify new entries
- This takes 10–15 minutes for 135 items

---

## Naming Convention: Document IDs

Your ID scheme already works well — respect it:

| Prefix | Meaning | Example |
|--------|---------|---------|
| `DC-` | D-Central core | DC-ISP-HT-001, DC-MESHEATS-ARCH-001 |
| `OS-` | OpenSecure security vertical | OS-ELECT-ARCH-002, OS-PACS-001 |
| `CST`, `MAT`, `GEN` | Algonquin courses | CST8315, MAT8002, GEN1957 |
| `AC-` (if new) | Algonquin admin/meta | AC-CURRICULUM-001 |

When naming a new document in a chat, use this pattern. Claude will catch it when I search, and the extractor will find it next time.

---

## Critical Known Gaps (From DC-REG-001 Draft)

These exist but didn't surface in the pattern extraction:

- **DC-SWARM-001** — Stigmergic coordination protocol (exists, not re-surfaced)
- **DC-PLANE-001** — Multi-plane sensing architecture (exists, not re-surfaced)
- **DC-SITE-001** — AI-coordinated labor management via biomimicry (exists, not re-surfaced)
- **Numeric BOM/cost docs** — DC-LKB module pricing, SkyLedger SDK pricing (architecture exists, not itemized)

Add these manually to DC-REG-001 when you have them handy.

---

## Long-Term Maintenance

### Weekly/Monthly
- New chat? → Rename it to the doc ID before closing
- New document ID? → Add a row to DC-REG-001 before closing the chat

### Quarterly
- Export your data (Settings → Privacy → Export data)
- Run `python3 build_registry_local.py` to extract new docs
- Merge new entries into DC-REG-001
- Spot-check for duplicates (ProvisioningDAO-style gaps)

### Yearly
- Rebuild your Projects structure if it no longer matches your work
- Re-upload DC-REG-001 to each Project's knowledge base (or confirm it's current)

---

## Why This Works

1. **Registry in knowledge base** → Each new chat knows what exists  
2. **Renamed chats** → My search finds the right conversation  
3. **One-line-per-doc habit** → Gaps surface when they happen, not months later  
4. **Local + periodic refresh** → You own the data, cheap to rerun

This is exactly what DC-STATUS-001 does for design-vs-execution gaps. You're applying the same honesty discipline one level up, across your entire document ecosystem.

---

## Next Steps (In Order)

1. **Review dc_registry_extracted.csv** — spot-check 20 entries for accuracy. How's the status inference? Any obvious false positives?
2. **Decide on Projects** — will you use the four proposed, or a different structure?
3. **Merge CSV + DC-REG-001** — fold new entries into the hand-curated master registry
4. **Upload to Projects** — place DC-REG-001 in each Project's knowledge base
5. **Rename past chats** (optional but useful) — at least the major D-Central work chats
6. **Start the habit** — next chat that produces a document → add a row, rename the chat

That's the entire system. Small habits, big payoff.
