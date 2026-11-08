---
description: "What any agent writes into the brain during and at the end of a session: the write-as-you-go rules and the session digest that feeds the weekly dream."
updated: 2026-11-06
---
# Capture: writing memory while working

Agents do best when they are free to record what they judge worth keeping. This is the licence,
and its limits.

## During the session: write as you go
Record without asking when the owner states something plainly or a document proves it:
- a fact about a topic, person, organisation or project: straight into its file (`procedures/ingest.md`, steps 4 to 8);
- a decision the owner makes: a dated entry in `decisions.md`;
- a lesson from something that went wrong or right: a dated entry in `LEARNINGS.md`;
- a to-do the owner names ("to do", "for later", "eventually"): a line in `TODO.md` under `## Open`;
- a stable fact about the owner: write the detail into its fact file (note, person or project) first.
  In `MEMORY.md` add or change at most a one-line summary with a link to that file, and only if it
  belongs in every session's head (`MEMORY.md` is the hub of a star schema).

Ask first when a fact would overwrite something already held, belongs to another household member,
is sensitive, or is your own inference. Your conclusions are not facts; they go in the digest as
questions, not into notes.

### Correction routing
When the owner corrects you, the correction is often worth more than the fixed output. Route it:

| What the owner gives you | Where it goes |
|---|---|
| A fact | the matching `notes/`, `people/` or `projects/` file |
| A choice between options | `decisions.md` |
| A preference they repeat | `AGENTS.md`, Standing rules (propose it; the owner approves) |
| A technique that worked | `procedures/<name>.md` or `skills/<name>/SKILL.md` |
| A sequence they want repeated | a scheduled task that follows a procedure |
| Something that must never happen | a mechanical gate (script check, folder rule), not prose |

## At the end: the session digest
Before signing off from any session that touched the brain or learned something worth keeping,
append to `sessions/YYYY-MM-DD.md` (create it if absent; several sessions can share a day):

```
## HH:MM  <tool, model: e.g. Claude Code, Claude / Antigravity, Gemini / OpenCode, a local model>  <one-line topic>
- Asked: what the owner wanted
- Learned: facts stated or proven, each with its source
- Changed: brain files written, one path per line
- Open: loose ends, contradictions noticed, questions for the owner
```

Five to fifteen lines. Facts only; no transcript. This is the dream's raw material, so an
unrecorded session is invisible to it. A session that learned nothing writes nothing.

Every approved tool with the folder open follows this procedure and writes its own digest. Note in
the digest any usage limit the tool hit. One tool writes at a time (AGENTS.md, "One brain, many tools").

Chat surfaces that cannot write to this folder should tell the owner to drop the fact in `Inbox/`.
