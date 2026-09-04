# Registry System — Quick Start

**Problem:** 500+ docs across 60+ components, scattered across 713 chats. You hit reconciliation gaps (ProvisioningDAO duplication, SHI/connectivity never unified).

**Solution:** Master registry + small habits = visibility.

---

## What You Have Right Now

✅ **dc_registry_extracted.csv** — 135 unique documents auto-found  
✅ **DC-REG-001-Master-Registry-v0.2.md** — Merged hand-curated + auto-extracted  
✅ **REGISTRY_ORGANIZATION_GUIDE.md** — Full workflow  
✅ **build_registry_local.py** — Extract new docs from exports (30 seconds, no API key needed)  
✅ **build_registry_from_export.py** — Alternative: use Haiku for richer metadata (requires API key)

---

## Three Steps to Activate

### 1. Set Up Projects (5 min)

Create these in claude.ai:
- **D-Central Core Architecture** (network, DAO, identity, D-OS)
- **D-Central Verticals** (MeshEats, OpenSecure, SkyLedger, Sod Boys)
- **Algonquin Coursework** (CST, MAT, GEN courses)
- **Personal/Career** (Master Timeline, job search)

### 2. Upload Registry to Each Project (2 min)

For each Project:
- Settings → Knowledge Base → Upload **DC-REG-001-Master-Registry-v0.2.md**
- That's it. Now every new chat in that Project can see the full registry.

### 3. Start the Habit (Going Forward)

Every time you close a chat that produced a document:

```
1. Add one row to DC-REG-001 in your notes:
   | DC-XXX-001 | One-sentence scope | Complete | [today's date] |

2. Rename the chat:
   ❌ "Building the ISP architecture"
   ✅ "DC-ISP-HT-001 — Haiti pilot topology"
```

That's the entire system. Small, repeatable, massive payoff.

---

## If You Want to Enrich the Registry

Run this quarterly after exporting new conversations:

```bash
python3 build_registry_local.py /path/to/unzipped/export
# Outputs: dc_registry_extracted.csv

# Then merge new rows into DC-REG-001 manually (10 min)
```

---

## Why This Works

**Before:** 713 chats, flat list, ProvisioningDAO in three places, gaps invisible  
**After:** Each Project knows what exists. Gaps surface when they happen.

Same discipline as DC-STATUS-001 (design vs. execution), applied to the registry itself.

---

## What the Extraction Found

- **135 unique documents** across your 713 conversations
- **100 DC-\* documents** (core D-Central)
- **4 OS-\* documents** (OpenSecure)
- **28 academic** (CST, MAT, GEN courses)

See **DC-REG-001-Master-Registry-v0.2.md** for the full list organized by category.

---

## Known Gaps (Add These Manually)

These exist but didn't surface in pattern extraction:
- DC-SWARM-001 (stigmergic coordination)
- DC-PLANE-001 (multi-plane sensing)
- DC-SITE-001 (AI labor coordination)

---

## Next: Read These in Order

1. **QUICK_START.md** ← You are here
2. **DC-REG-001-Master-Registry-v0.2.md** — The actual registry (browse by category)
3. **REGISTRY_ORGANIZATION_GUIDE.md** — Full workflow + maintenance (detailed version of this)

Then activate the Projects and upload the registry. Done.
