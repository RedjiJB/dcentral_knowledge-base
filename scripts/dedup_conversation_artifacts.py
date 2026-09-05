#!/usr/bin/env python3
"""
One-off Stage 4 dedup resolution for the 44 conversation-artifact docs
(scripts/extract_conversation_artifacts.py), applying the verdicts reached
by reading both sides of each flagged pair per DC-DEDUP-STD-001 -- not
trusting each document's own self-reported "Supersedes" line at face value.

Verdicts:
  - DC-REG-001-Master-Registry(-v0.2).md: confirmed EXACT byte-for-byte
    duplicates of files already in registry/ (body-hash match verified).
    Marked status: duplicate, moved to _superseded/.
  - DC-COOP-001 v1.0 -> v2.0: NOT a supersession despite v2.0's own header
    claiming one. v2.0 explicitly states "Tiers 0-10 from v1.0 remain
    unchanged... this document specifies the three new tiers [11-13] in
    full" -- v2.0 is an addendum, v1.0's tiers 0-10 exist nowhere else.
    Both left in place, reconciliation_note added to each explaining why.
  - DC-REINVEST-001/002/003: no clean chain despite each later doc claiming
    to supersede the former. 002 only covers Tier 5 of 001 (Tiers 0-4,
    including protective spend and the cloud-lab budget, are absent). 003
    restates 002's sections but drops the cloud-lab line entirely. All
    three left in place, reconciliation_note added to each.
  - DC-SIM-008 -> DC-SIM-009: genuine partial supersession, self-report
    VERIFIED ACCURATE on reading both -- 009's own header already says
    "Supersedes DC-SIM-008 SS1-6 (open status only; analysis retained)".
    Both left in place (008's analysis is still necessary reading);
    reconciliation_note added to make the verified relationship explicit
    rather than relying on the reader noticing 009's header line.

Usage: python3 scripts/dedup_conversation_artifacts.py
"""

import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
KB = REPO_ROOT / "knowledge-base"
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def add_fields(path: Path, fields: dict, move_to_superseded: bool = False):
    text = path.read_text(encoding="utf-8", errors="replace")
    m = FRONTMATTER_RE.match(text)
    fm_lines = m.group(1).splitlines()
    body = m.group(2)
    for k, v in fields.items():
        fm_lines.append(f'{k}: "{v}"' if "\n" not in v else f"{k}: {v}")
    new_text = "---\n" + "\n".join(fm_lines) + "\n---\n" + body

    if move_to_superseded:
        dest = path.parent / "_superseded" / path.name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(new_text, encoding="utf-8")
        path.unlink()
        print(f"Moved + tagged: {dest.relative_to(REPO_ROOT)}")
    else:
        path.write_text(new_text, encoding="utf-8")
        print(f"Tagged in place: {path.relative_to(REPO_ROOT)}")


def main():
    st = KB / "d-central" / "meta" / "status-tracking" / "conversation-artifacts"
    bl = KB / "d-central" / "business-legal" / "conversation-artifacts"
    sim = KB / "d-central" / "meta" / "simulation" / "conversation-artifacts"

    # 1. DC-REG-001 pair: confirmed exact duplicates of registry/.
    add_fields(
        st / "DC-REG-001-Master-Registry-v0.2.md",
        {
            "status": "duplicate",
            "duplicate_of": "registry/DC-REG-001-Master-Registry-v0.2.md",
            "duplicate_reason": "exact body match (verified byte-for-byte) -- already extracted "
                                 "by hand into registry/ in an earlier session, this conversation-"
                                 "artifact copy is redundant",
        },
        move_to_superseded=True,
    )
    add_fields(
        st / "DC-REG-001-Master-Registry.md",
        {
            "status": "duplicate",
            "duplicate_of": "registry/DC-REG-001-Master-Registry.md",
            "duplicate_reason": "exact body match (verified byte-for-byte) -- already extracted "
                                 "by hand into registry/ in an earlier session, this conversation-"
                                 "artifact copy is redundant",
        },
        move_to_superseded=True,
    )

    # 2. DC-COOP-001 v1.0 / v2.0: verified NOT a supersession, despite v2.0's
    #    own header. Both stay in place.
    add_fields(
        bl / "DC-COOP-001_v1.0_SodBoys_FullRebuild.md",
        {
            "reconciliation_note": "v2.0 (same conversation) declares 'Supersedes: DC-COOP-001 v1.0' "
                                    "in its own header, but reading both shows this is inaccurate as a "
                                    "blanket claim: v2.0's own change log states 'Tiers 0-10 from v1.0 "
                                    "remain unchanged' and only adds Tiers 11-13 in full. v1.0 is the "
                                    "only copy of Tiers 0-10 and must NOT be treated as superseded/"
                                    "removable -- both documents are required together for the complete "
                                    "spec. Verified during Stage 4 dedup, not taken at face value.",
        },
    )
    add_fields(
        bl / "DC-COOP-001_v2.0_SodBoys_FullExpansion.md",
        {
            "reconciliation_note": "This document's own header claims 'Supersedes: DC-COOP-001 v1.0,' "
                                    "but it is actually an addendum, not a replacement -- its own change "
                                    "log confirms 'Tiers 0-10 from v1.0 remain unchanged,' and only Tiers "
                                    "11-13 are specified here. v1.0 must be read alongside this document, "
                                    "not discarded in its favour.",
        },
    )

    # 3. DC-REINVEST-001/002/003: verified no clean supersession chain.
    reinvest_note = (
        "Part of a three-document evolving-plan chain (DC-REINVEST-001/002/003), each later "
        "doc claiming in its own header to supersede the former -- verified NOT a clean chain "
        "on reading all three: 002 only replaces 001's deferred Tier 5 (001's Tier 0 protective "
        "spend and Tier 4 cloud-lab budget have no other copy); 003 restates most of 002's "
        "sections but drops the cloud-lab line entirely. All three left in place, none marked "
        "superseded -- discarding any one would silently lose real budget line items."
    )
    for fn in ("DC-REINVEST-001-Corporate-Procurement-Plan.md",
               "DC-REINVEST-002-Full-Immediate-Buildout.md",
               "DC-REINVEST-003-Master-Procurement-Plan.md"):
        add_fields(bl / fn, {"reconciliation_note": reinvest_note})

    # 4. DC-SIM-008/009: verified genuine, accurate partial supersession.
    add_fields(
        sim / "DC-SIM-008-Open-Architecture-Decisions.md",
        {
            "reconciliation_note": "DC-SIM-009 supersedes this document's OPEN STATUS on items 1-6 "
                                    "(each is now decided) but explicitly retains this document's "
                                    "analysis as necessary reading -- verified accurate on reading both; "
                                    "not marked status: superseded because the analysis here (the two-ISP "
                                    "finding, the FCN reading A/B distinction, etc.) is not restated in "
                                    "DC-SIM-009 and remains required context for the decisions it records.",
        },
    )
    add_fields(
        sim / "DC-SIM-009-Architecture-Decision-Records.md",
        {
            "reconciliation_note": "Supersedes DC-SIM-008's open status on items 1-6 only (verified "
                                    "accurate against its own header claim) -- DC-SIM-008's analysis is "
                                    "not restated here and remains necessary reading alongside these "
                                    "decision records.",
        },
    )

    print("Done.")


if __name__ == "__main__":
    main()
