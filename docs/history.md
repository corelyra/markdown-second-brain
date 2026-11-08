# Where this came from, and how it changed

This kit is the shape of a real second brain that one person and a set of Claude agents have run
since late summer 2026. The personal content stays private. This page records where the ideas came
from and what changed over the first few months, including the experiments that were dropped.
Summaries of other people's work below are our reading of it, not their words.

## Origins

### 1. A folder of documents that nobody could read
The starting point was a personal archive of a few hundred documents: contracts, policies, CVs,
payslips, certificates, old project files. The first step was to put them in one synced folder of
plain Markdown, with a `CLAUDE.md` map, and let an agent ingest them.

Using a notes app's vault or a Notion database as the brain itself was considered and rejected.
Plain folders win because people and agents can both read them, nothing locks them to one app,
and they work in any synced folder.

The first ingest moved several hundred documents into `Inbox/processed/`, but `notes/`, `people/` and
`projects/` stayed almost empty. The documents had been **filed, not compiled**.

### 2. Karpathy's "LLM Wiki" pattern
[Andrej Karpathy](https://x.com/karpathy) described the "LLM Wiki" idea in spring 2026. As we read it: let the model **compile** sources into a
maintained wiki once, instead of re-deriving meaning from raw documents on every question (as
retrieval does). The model writes the wiki; the human reads it and steers. The layout has four
parts: raw sources, the compiled wiki, an output folder, and an identity file read before every
session.

This brain already had three of the four parts. What it lacked was the compiler: cross-links,
contradiction flags, an `output/` folder and a standing loop. A small public reference
implementation, [context-compiler-bootstrap](https://github.com/FrancyJGLisboa/context-compiler-bootstrap)
(MIT), helped show the shape. A four-stage plan followed: prune what exists, make ingest compile,
let it run on a schedule, then adopt ideas from further reading.

### 3. Four posts on keeping a machine-written wiki true
Four posts on X shaped the safety and upkeep side. Their figures were not checked, so only the
design ideas were taken. Links go to the authors' profiles:
- **Edges, not just nodes** ([@slash1sol](https://x.com/slash1sol), on agent swarms): if many agents ever ingest in parallel,
  ask for relationships with a reason, and apply "no shared source, no edge". Noted, not built.
- **Memory needs a way to forget** ([@colifran_](https://x.com/colifran_)): store the evidence
  and its date, not only the belief. A stale claim is "no longer safe to assume", not "wrong".
  This became the `Checked: YYYY-MM-DD` line on time-sensitive facts.
- **Compaction eats the rules first** ([@omarsar0](https://x.com/omarsar0)): safety
  rules and episodic notes get summarised at the same rate, but only the rules need exact wording.
  This became the separate, numbered, verbatim **Standing rules** at the top of `CLAUDE.md`.
- **The company brain and its correction loop** ([@VibeMarketer_](https://x.com/VibeMarketer_)): a small map first, details on
  demand, and a routing table for corrections (fact to a note, choice to the decision log,
  repeated preference to a rule, technique to a procedure, dangerous action to a mechanical gate).
  This became the correction routing in `procedures/capture.md`.

### 4. Anthropic's talk on agent memory and "dreaming"
[Memory and dreaming for self-learning agents](https://claude.com/code-with-claude/session/sf-memory-and-dreaming-for-self-learning-agents),
a Code with Claude session (May 2026), watched here some months later. As we understood it,
Anthropic described three lessons from every memory approach that stuck: Markdown as the format,
progressive loading (frontmatter plus grep, never the whole store), and agents free to write what
they judge relevant. It added **dreaming**: an out-of-band batch pass that reads the sessions'
transcripts and the memory store, and writes back a better-organised store.

This produced "memory v2", the largest single change (see the timeline).

## Timeline of changes

| When | Change | Why |
|---|---|---|
| Month 1 | Flat Markdown folders, `CLAUDE.md` map, `MEMORY.md` core facts, first bulk ingest | No lock-in; agents and people read the same files |
| Month 1 | `_sensitive-hold/` quarantine and the "never store credentials" rule | A notes-app export held passwords under titles that never said "password" |
| Month 1 | Phone capture shortcut into `Inbox/`, plus a daily scheduled ingest | Make capture effortless |
| Month 1 | Accuracy audit of the highest-stakes facts | Several facts had drifted between generations of documents |
| Month 1 | `output/` folder: artefacts are built from notes, never from raw inbox files | Part of the LLM Wiki layout |
| Month 1 | Banned-word list for AI writing | Drafts read as machine-written |
| Month 1 | `## Standing context` section in `MEMORY.md` | What is live this month, in every session |
| Month 2 | **Memory v2:** two-line frontmatter on every file and a generated `INDEX.md`; only `MEMORY.md` always loaded; decision and lesson logs load on demand | The decision log alone had grown large enough to crowd every session |
| Month 2 | **Capture:** agents write facts, decisions and lessons as they go, and leave a digest in `sessions/` | Without digests, the dream cannot see what a session learned |
| Month 2 | **Dream:** a weekly pass that applies safe fixes and proposes anything that changes a fact; before-copies in `archive/dream-snapshots/` | Close the loop; rollback without git in a synced folder |
| Month 2 | Standing rules separated from the folder map | Rules must survive long sessions word for word |
| Month 2 | Second inbox: a notes app's inbox folder, ingested by a small script that copies, stamps and files notes | Capture where writing already happens |
| Month 3 | `TODO.md`; every dream report lists open to-dos, document expiries in the next 12 months, and questions raised that week | The weekly report became the one page worth reading |
| Month 3 | Writing standard: ASD-STE100 rules beside the banned-word list | A review of ten real chats showed long sentences, idioms and buried warnings |
| Month 3 | Prompting update: target style first, banned list as an edit check; a definition of a complete answer; partial answers name the gap; **masters and copies**, with the dream checking for drift | [Anthropic's prompting guidance](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview) at the time |
| Month 3 | Notes-app copies used as extra context for every answer | Working notes hold detail the documents lack |
| Month 4 | **Watchdog** script: the brain checks itself (stray files, missed dreams, stale context, long numbers in always-loaded files, missing frontmatter, quiet projects, stale index) | The brain had no check on its own health |
| Month 4 | Reference numbers moved out of `MEMORY.md` into their own note | Sessions that read emails and web pages should not carry those numbers by default |
| Month 4 | **Inline and spill** (`log-recent.py`): the newest log entries in full, a count and date range for the rest | Long logs stay searchable without loading them |
| Month 4 | **Related lines** (chain of recall): two to five links under each summary, added by the dream five files a week | Agents follow links instead of grepping the whole tree |
| Month 4 | 100-word limit for anything read on a phone | Notifications and lists are read on a small screen |
| Month 4 | **One brain, many tools:** `AGENTS.md` becomes the master map; `CLAUDE.md` and `GEMINI.md` become pointers; `skills/` holds skill masters; digests name tool and model; `opencode.json` sets local-agent permissions; ingest ignores instructions inside inbox files | Use Claude, Gemini and a local model on one brain without repeating context. Tested with a canary line and a handoff between tools |

The ideas in the month 4 rows came from an article on X about agent design (not linked here; we could not
find a stable source), adapted to a single-person brain.

## Experiments that were dropped
- **Daily ingest and morning brief.** A weekday ingest with a short brief, later a daily
  morning to-do list. Both were dropped: for a brain of mostly settled records, a weekly dream is enough.
- **Scheduled dream without the folder attached.** The first scheduled dream ran in the cloud and
  could not reach the folder, so it did nothing. It worked once the scheduled task carried the
  folder. The pre-flight first flagged any task that finished in under a minute; that proved wrong
  (see the lessons), and the job check replaced it.
- **Moving working notes to another app.** Working notes moved from one notes app to another for a
  few weeks, then back. The second-inbox pattern survived; the app choice did not matter.
- **Nightly dream.** Considered and rejected in favour of weekly.

## Lessons worth keeping
- The map matters more than the folders. Keep it current or the agent wanders.
- A keyword sweep does not find credentials; reading does. Treat a sweep as a first pass only.
- Never leave an unread bulk import where an unattended scheduled run will compile it.
- Check a "contradiction" arithmetically before recording it. Many conflicts are not conflicts.
- Filing location is weak evidence of authorship.
- A number repeated across many documents is not thereby evidenced. Trace it to its artefact.
- "Not in the brain" is a claim to re-test, not a fact to inherit.
- Write "the documents do not show X", not "X is outstanding". A second brain records; it does not nag.
- Start a local agent inside the brain folder. Started in the home folder, a small model searched
  the whole home directory, read another tool's session files and never reached the brain.
- Check each tool's default permissions. One coding agent ran shell commands without asking until a
  config file in the brain set them to ask.
- Judge a scheduled job by the proof it leaves on disk, never by its status or run time. A backup
  missed two weeks with no error logged, while cloud runs that did their work showed as finished in
  seconds. A register of jobs with their proof files, checked weekly, catches both.
- Keep `MEMORY.md` a lean hub that links out, like the centre of a star schema. Detail written into
  it grows the file every session; detail kept in fact files loads only when needed.
- Scripts that rewrite files must refuse unknown options and skip snapshot folders. One dream run
  added frontmatter to its own before-copies because `--help` was silently ignored.
