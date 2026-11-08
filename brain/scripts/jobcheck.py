#!/usr/bin/env python3
"""Job check: did every scheduled job really run?

Reads the register in notes/scheduled-jobs.md and checks the proof each job leaves on disk.
A "succeeded" status or a short run time proves nothing; a fresh proof file does.

Register format (a Markdown table under "## Jobs"):
  | Job | Runs on | When | Proof | Max age (days) | Fix when missing |
  - Proof: a path in backticks. Relative paths start at the brain folder; ~ and absolute paths
    work; a glob (*) matches the newest file. Write "none" when the job leaves no proof.
  - Max age: whole days. A job whose "When" cell contains "disabled" is skipped.

Usage:
  python3 scripts/jobcheck.py

Read-only. Python 3, standard library only. Prints a Markdown table for the dream report.
"""
import glob, os, re, sys, time
from datetime import datetime
from pathlib import Path

if len(sys.argv) > 1:
    sys.exit(__doc__)
ROOT = Path(__file__).resolve().parent.parent
REG = ROOT / "notes" / "scheduled-jobs.md"
if not REG.is_file():
    sys.exit("jobcheck.py: notes/scheduled-jobs.md not found; copy templates/scheduled-jobs.md there first")

text = REG.read_text(encoding="utf-8")
m = re.search(r"(?ms)^## Jobs\s*\n(.*?)(?=^## |\Z)", text)
rows = []
for line in (m.group(1) if m else "").splitlines():
    if not line.startswith("|") or re.match(r"^\|\s*-", line):
        continue
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    if len(cells) < 5 or cells[0].lower() == "job":
        continue
    rows.append(cells)

def newest(pattern):
    p = os.path.expanduser(pattern)
    if not os.path.isabs(p):
        p = str(ROOT / p)
    hits = [h for h in glob.glob(p) if os.path.isfile(h)]
    return max(hits, key=os.path.getmtime) if hits else None

out, bad = [], []
for job, runs_on, when, proof, max_age, *rest in rows:
    fix = rest[0] if rest else ""
    if "disabled" in when.lower():
        out.append((job, when, "SKIPPED", "disabled")); continue
    pm = re.search(r"`([^`]+)`", proof)
    if not pm or proof.lower().startswith("none"):
        out.append((job, when, "UNCHECKED", "no proof file registered")); continue
    hit = newest(pm.group(1))
    if not hit:
        out.append((job, when, "MISSING", f"`{pm.group(1)}` not found")); bad.append((job, fix)); continue
    age = (time.time() - os.path.getmtime(hit)) / 86400
    try:
        limit = float(re.findall(r"[\d.]+", max_age)[0])
    except IndexError:
        out.append((job, when, "UNCHECKED", f"`{Path(hit).name}` {age:.1f} days old; no max age")); continue
    status = "OK" if age <= limit else "LATE"
    out.append((job, when, status, f"`{Path(hit).name}` {age:.1f} days old (max {limit:g})"))
    if status != "OK":
        bad.append((job, fix))

print(f"Job check, {datetime.now():%d %b %Y %H:%M}\n")
print("| Job | When | Status | Proof |\n|---|---|---|---|")
for r in out:
    print("| " + " | ".join(r) + " |")
print()
if bad:
    print(f"{len(bad)} job(s) need a look:")
    for job, fix in bad:
        print(f"- {job}: {fix or 'see notes/scheduled-jobs.md'}")
else:
    print("Every checked job left fresh proof.")
