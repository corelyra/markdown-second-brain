#!/usr/bin/env python3
"""Watchdog for the second brain: checks the brain itself, not its facts.

Run by procedures/dream.md step 0 (and by hand when the owner asks "is the brain healthy?").
Prints a Markdown list of findings for the dream report. Read-only: it changes nothing.
Exit code 0 always; an empty list means a healthy brain.

Checks:
 1. Stray files: *.tmp, *.lock, *.part, zero-byte .md files, files outside the naming rules.
 2. Undreamed session digests older than 8 days (a missed dream).
 3. Missing dream report for the most recent Sunday.
 4. MEMORY.md "Standing context" older than 14 days.
 5. Long digit strings (7+ digits) in always-loaded files (MEMORY.md, CLAUDE.md).
 6. Files in notes/, people/, projects/ without description/updated frontmatter.
 7. Active projects not updated for 30+ days.
 8. INDEX.md older than the newest note (index needs a rebuild).
"""
import datetime as dt, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODAY = dt.date.today()
SKIP = {"_sensitive-hold", "archive", ".git", "Inbox", "__pycache__"}
found = []

def add(kind, msg):
    found.append(f"- **{kind}:** {msg}")

def walk():
    for dp, dns, fns in os.walk(ROOT):
        dns[:] = [d for d in dns if d not in SKIP and not d.startswith(".")]
        for f in fns:
            yield Path(dp) / f

def front(p):
    try:
        head = p.read_text(encoding="utf-8", errors="replace")[:1500]
    except OSError:
        return None
    if not head.startswith("---"):
        return {}
    block = head.split("---", 2)[1] if head.count("---") >= 2 else ""
    out = {}
    for line in block.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip('"')
    return out

def date_of(s):
    m = re.search(r"(\d{4}-\d{2}-\d{2})", s or "")
    if not m:
        return None
    try:
        return dt.date.fromisoformat(m.group(1))
    except ValueError:
        return None

# 1. stray files
for p in walk():
    rel = p.relative_to(ROOT)
    if p.suffix in {".tmp", ".lock", ".part", ".crdownload"} or p.name.startswith("~$"):
        add("Stray file", f"`{rel}` (move to archive/stray-files/)")
    elif p.suffix == ".md" and p.stat().st_size == 0:
        add("Empty file", f"`{rel}`")
    elif p.suffix == ".md" and rel.parts[0] in {"notes", "people", "projects"} and re.search(r"[A-Z ]", p.name):
        add("Naming", f"`{rel}` breaks the lowercase-hyphen rule")

# 2. undreamed digests
for p in sorted((ROOT / "sessions").glob("*.md")):
    if p.name == "README.md":
        continue
    d = date_of(p.name)
    if d and (TODAY - d).days > 8:
        add("Missed dream", f"`sessions/{p.name}` is {(TODAY - d).days} days old and not yet dreamed")

# 3. dream report for the last Sunday
last_sun = TODAY - dt.timedelta(days=(TODAY.weekday() + 1) % 7)
reports = list((ROOT / "output" / "reports").glob(f"dream-{last_sun.isoformat()}*.md"))
if not reports:
    add("Dream report", f"no `output/reports/dream-{last_sun.isoformat()}*.md`; the Sunday dream may not have run")

# 4. MEMORY.md standing context
mem = (ROOT / "MEMORY.md").read_text(encoding="utf-8", errors="replace")
m = re.search(r"## Standing context[^\n]*last touched ([0-9]{1,2} \w+ \d{4})", mem)
if m:
    try:
        d = dt.datetime.strptime(m.group(1), "%d %b %Y").date()
        if (TODAY - d).days > 14:
            add("Stale context", f"MEMORY.md \"Standing context\" last touched {m.group(1)} ({(TODAY - d).days} days); refresh what is live this month")
    except ValueError:
        pass
elif "last touched DD Mon YYYY" in mem:
    add("Stale context", "MEMORY.md \"Standing context\" still says DD Mon YYYY; write the date you last updated it, e.g. 1 Nov 2026")
else:
    add("Stale context", "MEMORY.md has no dated \"Standing context\" heading (format: last touched 1 Nov 2026)")

# 5. numbers in always-loaded files
for name in ("MEMORY.md", "CLAUDE.md"):
    txt = (ROOT / name).read_text(encoding="utf-8", errors="replace")
    for i, line in enumerate(txt.splitlines(), 1):
        for hit in re.findall(r"\b\d{7,}\b", line):
            if "ISBN" in line:
                continue
            add("Number in always-loaded file", f"`{name}` line {i} carries a 7+ digit number; move it to notes/reference-numbers.md")

# 6 + 7. frontmatter and stale active projects
for folder in ("notes", "people", "projects"):
    for p in sorted((ROOT / folder).glob("*.md")):
        fm = front(p)
        if fm is None:
            continue
        if "description" not in fm or "updated" not in fm:
            add("Frontmatter", f"`{folder}/{p.name}` lacks description or updated")
            continue
        if folder == "projects":
            body = p.read_text(encoding="utf-8", errors="replace")
            st = re.search(r"^Status:\s*(\w+)", body, re.M)
            up = date_of(fm.get("updated"))
            if st and st.group(1).lower() == "active" and up and (TODAY - up).days > 30:
                add("Quiet project", f"`projects/{p.name}` is active but last updated {up} ({(TODAY - up).days} days)")

# 8. INDEX.md freshness
idx = ROOT / "INDEX.md"
if idx.exists():
    newest = max((p.stat().st_mtime for f in ("notes", "people", "projects") for p in (ROOT / f).glob("*.md")), default=0)
    if newest > idx.stat().st_mtime + 60:
        add("Index", "a note changed after INDEX.md was built; run `python3 scripts/build-index.py`")

print(f"## Watchdog ({TODAY.isoformat()})")
print("\n".join(found) if found else "- Nothing found. The brain looks healthy.")
