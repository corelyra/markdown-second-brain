#!/usr/bin/env python3
"""Add one link to a file's Related: line, so the linked file gains an inbound link.

Usage: python3 scripts/relate.py [--dry-run] <file that gets the link> <file to link to>
  Both paths are written from the brain's root, e.g.
  python3 scripts/relate.py notes/home-insurance.md people/harbour-lettings.md

The script reads the file, changes it and writes it in one step:
- It adds the relative path to the Related: line, or makes the line under the one-line summary.
- It refuses when the line already holds five paths (procedures/dream.md: two to five).
- It makes a before-copy in archive/dream-snapshots/<today>-relate/ (never overwrites one).
- It sets the frontmatter `updated` to today.
Links only: it adds no facts. Exit code 0 when the link is there afterwards, 1 when refused.
"""
import datetime as dt, os, re, shutil, sys
from pathlib import Path

args = [a for a in sys.argv[1:] if a != "--dry-run"]
DRY = "--dry-run" in sys.argv[1:]
if len(args) != 2 or any(a.startswith("--") for a in args):
    sys.exit(__doc__)
ROOT = Path(__file__).resolve().parent.parent
TODAY = dt.date.today().isoformat()
host, target = ROOT / args[0], ROOT / args[1]
for p in (host, target):
    if not p.is_file():
        sys.exit(f"relate.py: {p.relative_to(ROOT)} does not exist")
if host.parts[len(ROOT.parts)] not in ("notes", "people", "projects"):
    sys.exit("relate.py: the file that gets the link must be in notes/, people/ or projects/")
if host == target:
    sys.exit("relate.py: a file cannot link to itself")

link = os.path.relpath(target, host.parent).replace(os.sep, "/")
lines = host.read_text(encoding="utf-8").split("\n")
low = lambda s: s.lower()

rel_i = next((i for i, l in enumerate(lines) if l.startswith("Related:")), None)
if rel_i is not None:
    have = [x.strip() for x in lines[rel_i][len("Related:"):].split(",") if x.strip()]
    if low(link) in map(low, have):
        print(f"already linked: {args[0]} names {link}")
        sys.exit(0)
    if len(have) >= 5:
        sys.exit(f"relate.py: refused, the Related: line of {args[0]} already holds {len(have)} paths; choose another file")
    lines[rel_i] = "Related: " + ", ".join(have + [link])
else:
    title = next((i for i, l in enumerate(lines) if l.startswith("# ")), None)
    if title is None:
        sys.exit(f"relate.py: refused, {args[0]} has no '# Title' line")
    summary = next((i for i in range(title + 1, len(lines)) if lines[i].strip()), None)
    if summary is None or re.match(r"(#|[-*|>] ?|\d+\. |```)", lines[summary]):
        sys.exit(f"relate.py: refused, {args[0]} has no one-line summary under its title; add the link by hand")
    lines.insert(summary + 1, "Related: " + link)

for i, l in enumerate(lines[:8]):
    if l.startswith("updated:"):
        lines[i] = "updated: " + TODAY
        break
if DRY:
    print(f"dry run: {args[0]} would gain 'Related: ... {link}'")
    sys.exit(0)
snap = ROOT / "archive" / "dream-snapshots" / f"{TODAY}-relate" / args[0]
if not snap.exists():
    snap.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(host, snap)
host.write_text("\n".join(lines), encoding="utf-8")
print(f"linked: {args[0]} now names {link}")
