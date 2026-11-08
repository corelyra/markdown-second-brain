---
description: "Fictional register of Alex's scheduled jobs: the weekly dream and the phone capture shortcut, with the proof each leaves. Read when a job seems missed."
updated: 2026-10-25
---
# Scheduled jobs register

Fictional example. Every job, the proof it leaves on disk, and the fix when the proof is missing.
Related: procedures/dream.md, scripts/jobcheck.py

Rule: judge a job by its proof, not by a "succeeded" status.

## Jobs
| Job | Runs on | When | Proof | Max age (days) | Fix when missing |
|---|---|---|---|---|---|
| Weekly dream | scheduled agent task | Sun 11:00 | `output/reports/dream-*.md` | 8 | Say "dream" in a session |
| Phone capture | phone shortcut | when used | none | - | No check possible; add a heartbeat file |

## Open questions
- Should the phone shortcut write a heartbeat file each night, so the job check can prove it ran?

## Sources
- Fictional; written for the example brain.
