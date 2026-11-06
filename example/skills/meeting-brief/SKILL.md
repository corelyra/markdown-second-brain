---
name: meeting-brief
description: "Write a one-page brief before Alex meets a person or organisation. Use when Alex asks to prepare for a meeting or call."
---
# Meeting brief

## Inputs
- Who the meeting is with, and the date. Ask if either is missing.

## Steps
1. Find the person or organisation: grep `^description:` in `people/`, then open the match.
2. Follow its `Related:` line to open projects and notes.
3. Read the newest entries in `decisions.md` that name them: `python3 scripts/log-recent.py decisions.md <name>`.
4. Write the brief to `output/briefs/YYYY-MM-DD-<name>.md`.

## Output
- Who they are, in one line.
- Open items between Alex and them, each with its source file.
- Last decision that involved them, with its date.
- Three questions Alex could ask.

## Checks before you finish
- Every fact cites the file it came from.
- Nothing is invented. Where the brain has no answer, say so.
- 300 words at most.
