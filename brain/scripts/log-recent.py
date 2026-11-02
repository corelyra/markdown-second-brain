#!/usr/bin/env python3
"""Inline & Spill for the long logs (decisions.md, LEARNINGS.md).

Prints the newest entries in full (inline) and only a count and date range for the rest (spill),
so an agent reads what is recent and searches for what is old.

Usage:
  python3 scripts/log-recent.py decisions.md            # last 15 entries in full
  python3 scripts/log-recent.py LEARNINGS.md 30         # last 30 entries
  python3 scripts/log-recent.py decisions.md insurance  # every entry that mentions "insurance", in full

Entries start with a "## " heading. Read-only; the logs stay append-only and untouched.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if len(sys.argv) < 2:
    sys.exit(__doc__)
path = ROOT / sys.argv[1]
arg = sys.argv[2] if len(sys.argv) > 2 else "15"
if not path.is_file():
    sys.exit(f"log-recent.py: {sys.argv[1]} not found in {ROOT}")
text = path.read_text(encoding="utf-8")
plural = lambda n, w: f"{n} {w}" + ("" if n == 1 else "s")
parts = re.split(r"(?m)^(?=## )", text)
head, entries = parts[0], [p.rstrip() for p in parts[1:]]
title = lambda e: e.splitlines()[0][3:]

if arg.isdigit():
    n = int(arg)
    if n < 1:
        sys.exit("log-recent.py: give a count of 1 or more, or a keyword")
    old, new = entries[:-n], entries[-n:]
    print(f"# {path.name}: {plural(len(entries), 'entry').replace('entrys', 'entries')}. Showing the newest {len(new)}.")
    if old:
        print(f"Older entries (spilled): {len(old)}, from \"{title(old[0])[:40]}\" to \"{title(old[-1])[:40]}\".")
        print(f"Search them: python3 scripts/log-recent.py {path.name} <keyword>\n")
    print("\n\n".join(new))
else:
    hits = [e for e in entries if arg.lower() in e.lower()]
    print(f"# {path.name}: {len(hits)} of {len(entries)} entries mention \"{arg}\".\n")
    print("\n\n".join(hits))
