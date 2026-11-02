---
description: "The weekly dreaming pass: an out-of-band batch job that verifies, organises and enriches the brain from the week's session digests. Run on the weekly schedule or when the owner says 'dream'."
updated: 2026-11-01
---
# Dream: the weekly consolidation pass

A second-order process with one objective: curate the memory. Sessions write in real time and
make a mess; the dream tidies it between sessions, so the next week's sessions start cleverer.
Runs once a week as a scheduled task, or on request.

## Ground rules
- **Safe fixes are applied; anything that changes a fact is proposed.**
- **Before-copy first.** Before touching any file, copy it to
  `archive/dream-snapshots/YYYY-MM-DD/<same path>` (`cp -n`). This is the rollback. It also works in
  synced folders (iCloud, Dropbox) where git is awkward and deletes are risky.
- Never delete. Never read, quote or move anything out of `_sensitive-hold/`.
- Never copy content outside this folder. Nothing is published.
- If the shell has a time limit per call, work in small steps.
- Do not invent. A fact enters a note only if a session digest or a document states it.

## 0. Pre-flight
1. Read `CLAUDE.md`, `MEMORY.md` and `TODO.md`. Read the newest entries of the long logs with
   `python3 scripts/log-recent.py decisions.md` and `python3 scripts/log-recent.py LEARNINGS.md`.
2. List `sessions/*.md` (not `README.md`, not `dreamed/`). No digests? Still run steps 2 and 3;
   they catch drift that no session reports.
3. Make today's snapshot folder.
4. **Watchdog:** run `python3 scripts/watchdog.py` and paste its output into the report under
   `## Watchdog`. Stray files it names (`.tmp`, `.lock`, empty files): run `mkdir -p archive/stray-files`, then
   `mv -n` them into that folder (apply). Everything else it finds: report, do not fix here.
   If scheduling tools are available, check the brain's own scheduled tasks: report any whose last
   run failed, did not fire in the past 8 days, or finished in under a minute (a sign it never
   reached the folder).

## 1. Enrich: fold the week's sessions into the brain
One digest at a time, oldest first. For each "Learned" line:
- Already held and consistent: nothing to do.
- New and sourced: **apply**. Write it into the right file per `procedures/ingest.md` steps 4 to 8,
  with the digest as the source (`sessions/dreamed/YYYY-MM-DD.md`).
- Contradicts what the brain holds: **propose**. Add it under the note's `## Open questions` as
  "source A says X; source B says Y" and list it in the report.
- A decision or lesson not yet logged: **apply** to `decisions.md` / `LEARNINGS.md`, dated to the session.

Carry every "Open" line into the report. A to-do the owner named goes into `TODO.md` under `## Open`
if it is not there yet (apply). Any question raised, and any expiry, renewal or deadline date
learned in the week, goes into the report as well. Then `mv -n` the digest into `sessions/dreamed/`.

If several agents wrote on the same day, handle each digest separately, then compare: two sessions
that edited the same file in the same week are worth a second look.

## 2. Verify: is what we hold still true?
Report, and fix only the mechanical faults:
- **Deadlines:** any date in the next 60 days across `MEMORY.md`, `projects/`, `notes/` (expiries,
  renewals, contract ends, claims, tax dates). List them, nearest first.
- **Document expiries:** every expiry date for passports, ID cards, driving licences, visas,
  certificates and policies across `MEMORY.md`, `people/` and `notes/`. List those within the next
  12 months (passports need months of lead time), nearest first, and always list any new this week.
- **To-dos:** read `TODO.md`. List every open item, oldest first, with its age in weeks. Move items
  ticked `[x]` to `## Done` (apply). An item whose job the brain now shows as done: propose ticking it.
- **Staleness:** `Checked:` dates older than 12 months on balances, policy terms and deadlines;
  active projects whose `updated` is older than 30 days. List the oldest ten.
- **Broken sources:** paths in `## Sources` that no longer exist. Fix the path if the file obviously
  moved (apply); otherwise list it.
- **MEMORY.md against the notes:** does every figure in MEMORY.md match its note? A mismatch is a
  proposal, never a silent fix.
- **Open questions:** count files with an unresolved `## Open questions` section and name the three oldest.

## 3. Organise: keep the shape clean
Apply:
- `python3 scripts/frontmatter.py notes/*.md people/*.md projects/*.md` (fills missing frontmatter;
  leaves existing descriptions alone). Pass explicit paths.
- A description that no longer matches what the file holds: rewrite it from the file's own content.
- Missing `## Sources`, missing title or summary line, filenames that break the naming rules
  (rename with `mv -n`, then fix inbound links).
- Cross-links between clearly related files (same person, same organisation, same project).
- **Related lines (chain of recall):** pick up to five files that lack a `Related:` line, active
  projects first, then the notes they cite. Add one line directly under the summary: `Related: `
  plus two to five relative paths of files that the file already mentions or that share its person,
  organisation or project. Links only, no new facts. An agent can then follow links from file to
  file instead of grepping the tree. Note in the report how many files still lack the line.
- Compare `PROJECT-INSTRUCTIONS.md` with `CLAUDE.md` and `notes/writing-standard.md`. List any
  difference under "Drift found".
- `Status: done` projects not mentioned in any session for 60 days: move to `archive/`.
- `python3 scripts/build-index.py`, last.

Propose:
- Merging duplicates or near-duplicates; binning thin notes; splitting a file that holds two topics.
- MEMORY.md over about 70 lines: propose which lines to move into notes.
- A preference the owner repeated in two or more sessions: propose it as a Standing rule.
- A procedure an agent had to rediscover: propose a new `procedures/` file.

## 4. Report
Write `output/reports/dream-YYYY-MM-DD.md`, at most one screen:
```
# Dream, <date>
Sessions consolidated: n (list)   Files changed: n   Snapshot: archive/dream-snapshots/<date>/

## Coming up (next 60 days)
## Expiries (next 12 months, plus any new this week)
## To-dos (open items from TODO.md)
## Questions raised this week
## Applied
## Needs the owner (proposals, contradictions, open loops)
## Drift found (stale, broken, oversize)
## Watchdog (output of scripts/watchdog.py and the scheduled-task check)
```
Then append a one-line dated entry to `LEARNINGS.md` only if the dream itself taught something
(a procedure that failed, a check that proved useless). Routine runs do not earn an entry.

Finish with a push notification, if the tool exists: the number of proposals waiting, the number of
open to-dos, and the nearest deadline or expiry.
