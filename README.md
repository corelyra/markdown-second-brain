# Second Brain Kit

A plain-Markdown second brain that AI agents read, write and tidy for you. Built and run with
Claude (Claude Code, the Claude desktop app and claude.ai Projects). The files work with any agent
that reads Markdown and can run Python.

## What it is
- One folder of Markdown files. No database, no plugin, no app lock-in.
- A map (`CLAUDE.md`) that gives the agent the rules, the folder layout and how to find things.
- Three procedures the agent follows: **ingest**, **capture** and the weekly **dream**.
- Four small Python scripts (standard library only) for the mechanical work.

## The ideas in it
| Idea | What it does | Where |
|---|---|---|
| Standing rules | Numbered, verbatim rules the agent must not paraphrase | `brain/CLAUDE.md` |
| Progressive loading | Two-line frontmatter on every file; grep descriptions, open only the matches | `brain/CLAUDE.md`, `scripts/build-index.py` |
| Compile, don't file | Ingest distils each source into notes, links them and flags contradictions | `procedures/ingest.md` |
| Write as you go | Agents record facts, decisions and lessons, and route corrections | `procedures/capture.md` |
| Session digests | Short dated digests are the short-term memory | `sessions/` |
| The dream | A weekly pass: enrich, verify, organise, report. Safe fixes applied, fact changes proposed | `procedures/dream.md` |
| Before-copies | Every file the dream touches is copied first, for rollback | `archive/dream-snapshots/` |
| Quarantine | Credentials found during ingest go to a folder agents never read out of | `_sensitive-hold/` |
| Masters and copies | One source of truth; copies for other tools; drift checked weekly | `CLAUDE.md`, `PROJECT-INSTRUCTIONS.md` |
| Watchdog | A read-only health check of the brain itself | `scripts/watchdog.py` |
| Inline and spill | Newest log entries in full, the rest counted and searchable | `scripts/log-recent.py` |
| Writing standard | ASD-STE100 clarity rules plus a banned-word list for AI prose | `notes/writing-standard.md` |

More in [docs/design.md](docs/design.md). Where the ideas came from and how the system changed
over its first few months: [docs/history.md](docs/history.md).

## Repository layout
```
brain/     the empty starter: copy this folder and make it yours
example/   the same structure, filled in for a fictional person (Alex Carter)
docs/      design notes and history
```

## Quick start
1. Copy `brain/` to a synced folder (iCloud Drive, Dropbox, OneDrive) and rename it.
2. Replace every `{{...}}` placeholder in `CLAUDE.md` and `PROJECT-INSTRUCTIONS.md`
   (`grep -rn '{{' .` finds them all; see the table below).
3. Fill `MEMORY.md` with your core facts. Keep it to about 70 lines.
4. Point an agent at the folder:
   - **Claude Code:** run `claude` in the folder. It reads `CLAUDE.md` itself.
   - **Claude desktop app:** add the folder to the session.
   - **claude.ai Project:** fill in `PROJECT-INSTRUCTIONS.md` and paste it into the Project instructions.
5. Drop a document in `Inbox/` and say "process the inbox".
6. Schedule the weekly dream (see "Scheduling the dream" below).
7. Read the dream report in `output/reports/` each week and answer its proposals.
   [example/output/reports/dream-2026-10-25.md](example/output/reports/dream-2026-10-25.md) shows one.

### Placeholders
| Placeholder | Example |
|---|---|
| `{{OWNER_SHORT}}` | Alex |
| `{{OWNER_NAME}}` | Alex Carter |
| `{{CITY}}`, `{{TIMEZONE}}` | Leeds, Europe/London |
| `{{ONE_LINE_ROLE}}` | Product manager at Northwind Analytics |
| `{{LANGUAGES}}` | English |
| `{{STRANDS}}` | work and career, running, home and personal admin |
| `{{DREAM_TIME}}` | Sundays at 19:00 |
| `{{FOLDER_NAME}}` | Alex Brain |

### Scheduling the dream
The dream needs an agent that can open the folder, on a weekly timer.
- **Claude desktop app or claude.ai:** create a scheduled task with the prompt
  `Run procedures/dream.md in <your folder>.` and attach the folder to the task.
- **Claude Code:** run `claude -p "Run procedures/dream.md"` from the folder with cron, launchd or
  Task Scheduler.
- **By hand:** say "dream" in any session that has the folder open.

Check the first run. A scheduled dream that finishes in under a minute probably could not reach the
folder; the next dream's pre-flight checks for this.

Requirements: Python 3.9 or later. No packages.

## Try it on the example
```
cd example
python3 scripts/build-index.py
python3 scripts/watchdog.py
python3 scripts/log-recent.py decisions.md
```
The watchdog reports what a dream would fix. On the example it will flag a missing dream report for
the latest Sunday, and stale dates as time passes: that is the watchdog working.

## Privacy
- Keep your own brain private. The kit ships with no personal content; `example/` is fictional.
- If you version your brain with git, use a **private** repository. `brain/.gitignore` keeps
  `_sensitive-hold/` out of commits.
- Never put passwords, PINs, card numbers, seed phrases or private keys in the brain.

## Not included
- Adapters for email or notes apps. `procedures/ingest.md` describes the pattern for a second inbox;
  add a Standing rule that points the agent at your adapter.

## Credits
The kit builds on other people's ideas. The full story of how each one was used is in
[docs/history.md](docs/history.md).
- [Andrej Karpathy](https://x.com/karpathy): the "LLM Wiki" pattern of compiling sources into a maintained wiki instead of retrieving from raw documents.
- [context-compiler-bootstrap](https://github.com/FrancyJGLisboa/context-compiler-bootstrap) (MIT): a small reference implementation of that pattern.
- [@slash1sol](https://x.com/slash1sol): ask agent swarms for relationships with reasons, not only findings.
- [@colifran_](https://x.com/colifran_): store evidence and its date, so stale claims can be found.
- [@omarsar0](https://x.com/omarsar0): context compaction loses rules first, so keep rules short and separate.
- [@VibeMarketer_](https://x.com/VibeMarketer_): map first, details on demand, and a routing table for corrections.
- Anthropic, [Memory and dreaming for self-learning agents](https://claude.com/code-with-claude/session/sf-memory-and-dreaming-for-self-learning-agents) (Code with Claude, May 2026): progressive loading, agent-written memory and the dreaming pass.
- [ASD-STE100 Simplified Technical English](https://www.asd-ste100.org): the basis of the writing standard.

## Contributing
Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence
MIT. See [LICENSE](LICENSE).
