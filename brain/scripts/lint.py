#!/usr/bin/env python3
"""Lint for the second brain: checks the compiled notes as a wiki, not their facts.

Run by procedures/dream.md step 0, and by hand when the owner says "lint the brain".
Prints a short Markdown list for the dream report. Read-only: it changes nothing.
Exit code 0 always.

Usage: python3 scripts/lint.py [--all]
  --all   list every finding, not only the first five of each kind

Checks:
 1. Orphans: files in notes/, people/, projects/ that no other file links to.
 2. Dead links: a path with a folder in it, ending in .md, that points at no file.
 3. Uncited sources: Markdown copies in Inbox/processed/ that no note names
    (filed, not compiled), counted per folder. Folders listed in CONTEXT below are
    searched as context and never compiled; their count is information only.
 4. Unsourced files: notes, people or projects with nothing under "## Sources".
 5. LOG.md: missing, or its newest entry is more than 14 days older than the newest note.
"""
import collections, datetime as dt, os, re, sys, unicodedata
from pathlib import Path

args = sys.argv[1:]
if [a for a in args if a != "--all"]:
    sys.exit(__doc__)
ALL = "--all" in args

ROOT = Path(__file__).resolve().parent.parent
TODAY = dt.date.today()
WIKI = ("notes", "people", "projects")
# Folders under Inbox/processed/ that hold context copies (a notes app export, transcripts).
# Name them here, e.g. ("notes-app", "voice-memos").
CONTEXT = ()
PATH = re.compile(r"(?<![\w/.<{~-])((?:\.\./)*[\w][\w./-]*\.md)\b")
PROCESSED = ROOT / "Inbox" / "processed"

def norm(s):
    """Some file systems store names decomposed and ignore case; compare in one form."""
    return unicodedata.normalize("NFC", str(s)).lower()

def read(p):
    return p.read_text(encoding="utf-8", errors="replace")

def body(text):
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[end + 5:]
    return text

def updated(p):
    m = re.search(r"^updated:\s*(\d{4}-\d{2}-\d{2})", read(p)[:600], re.M)
    return m.group(1) if m else ""

def resolve(token, src):
    """A link is written from the file's folder, the brain's root or Inbox/processed/."""
    for base in (src.parent, ROOT, PROCESSED):
        p = Path(os.path.normpath(base / token))
        if p.is_file() and norm(p).startswith(norm(ROOT) + "/"):
            return p
    return None

def show(items, fmt=lambda x: f"`{x}`"):
    head = items if ALL else items[:5]
    more = "" if ALL or len(items) <= 5 else f" (+{len(items) - 5} more; run with --all)"
    return ", ".join(fmt(x) for x in head) + more

wiki = [p for d in WIKI for p in sorted((ROOT / d).glob("*.md"))]
briefs = sorted((ROOT / "output" / "briefs").glob("*.md"))
hubs = [ROOT / n for n in ("MEMORY.md", "TODO.md", "decisions.md", "LEARNINGS.md")]
# The map names example paths, so it counts for inbound links but not for dead ones.
quiet = [ROOT / "AGENTS.md"]
linkers = wiki + briefs + [p for p in hubs if p.is_file()]

inbound = {norm(p): 0 for p in wiki}
dead = []
corpus = []
for src in linkers + [p for p in quiet if p.is_file()]:
    text = body(read(src))
    corpus.append(norm(text))
    for token in sorted(set(PATH.findall(text))):
        if "YYYY" in token:
            continue
        target = resolve(token, src)
        if target is None:
            # A bare file name is shorthand, never a dead link.
            if "/" in token and src not in quiet:
                hint = ""
                if token.startswith("sessions/") and (ROOT / "sessions" / "dreamed" / Path(token).name).is_file():
                    hint = " (now in sessions/dreamed/)"
                dead.append((str(src.relative_to(ROOT)), token + hint))
        elif norm(target) in inbound and norm(target) != norm(src):
            inbound[norm(target)] += 1
corpus = "\n".join(corpus)

found = []
orphans = sorted((p for p in wiki if not inbound[norm(p)]), key=updated, reverse=True)
if orphans:
    found.append(f"- **Orphans:** {len(orphans)} of {len(wiki)} files have no inbound link. Newest first: "
                 + show([p.relative_to(ROOT) for p in orphans]))
if dead:
    files = len({s for s, _ in dead})
    found.append(f"- **Dead links:** {len(dead)} in {files} files. "
                 + show(dead, lambda d: f"`{d[0]}` names `{d[1]}`"))

# A copy counts as cited when a note names its path, with or without "Inbox/processed/" in front.
total, uncited = collections.Counter(), collections.Counter()
if PROCESSED.is_dir():
    for p in PROCESSED.rglob("*.md"):
        rel = p.relative_to(PROCESSED)
        if "originals" in rel.parts or p.name == "README.md":
            continue
        top = rel.parts[0] if len(rel.parts) > 1 else "(top level)"
        total[top] += 1
        if norm(rel) not in corpus:
            uncited[top] += 1
work = [k for k in sorted(total) if k not in CONTEXT and uncited[k]]
if work:
    n, m = sum(uncited[k] for k in work), sum(total[k] for k in total if k not in CONTEXT)
    found.append(f"- **Uncited sources:** {n} of {m} copies in `Inbox/processed/` are named by no note. Per folder: "
                 + ", ".join(f"{k} {uncited[k]}/{total[k]}" for k in work))
ctx = [k for k in CONTEXT if total[k]]
if ctx:
    found.append("- **Context folders (information only):** "
                 + ", ".join(f"{k} {uncited[k]}/{total[k]} uncited" for k in ctx))

unsourced = []
for p in wiki:
    m = re.search(r"^## Sources\s*\n(.*?)(?=^## |\Z)", read(p), re.M | re.S)
    if not m or not re.search(r"\w", m.group(1)):
        unsourced.append(p.relative_to(ROOT))
if unsourced:
    found.append(f"- **Unsourced:** {len(unsourced)} files have nothing under `## Sources`: " + show(unsourced))

log = ROOT / "LOG.md"
if not log.is_file():
    found.append("- **Log:** LOG.md is missing")
else:
    dates = re.findall(r"^## \[(\d{4}-\d{2}-\d{2})\]", read(log), re.M)
    stamps = [d for d in (updated(p) for p in wiki) if d]
    if dates and stamps:
        gap = (dt.date.fromisoformat(max(stamps)) - dt.date.fromisoformat(max(dates))).days
        if gap > 14:
            found.append(f"- **Log:** a note was updated on {max(stamps)} but the newest LOG.md entry is {max(dates)}; an ingest or a session did not log")

print(f"## Lint ({TODAY.isoformat()})")
print("\n".join(found) if found else "- Nothing found. The wiki is clean.")
