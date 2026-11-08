---
description: "Register of every scheduled job (cloud tasks, launchd or cron, phone shortcuts, NAS backups): when it runs, the proof it leaves, and the fix when it does not run. Read when a job seems missed or before adding one."
updated: YYYY-MM-DD
---
# Scheduled jobs register

Every recurring job, the proof it leaves on disk, and what to do when the proof is missing.
Copy this file to `notes/scheduled-jobs.md` and fill the table. The dream runs `scripts/jobcheck.py`
against it every week.

Rule: judge a job by its proof, not by a "succeeded" status. A job that never fires logs no error,
and a run that did its work can still show as finished in seconds. Only a missing or stale proof
file shows the truth.

## Jobs
| Job | Runs on | When | Proof | Max age (days) | Fix when missing |
|---|---|---|---|---|---|
| Weekly dream | scheduled agent task | Sun 11:00 | `output/reports/dream-*.md` | 8 | Say "dream" in a session |
| Phone capture | phone shortcut | when used | none | - | No check possible; add a heartbeat file |
| Laptop backup | backup app | daily | `~/Library/Logs/backup.log` | 2 | Run the backup by hand |
| Example disabled job | scheduled agent task | disabled | `output/example.txt` | 8 | Re-enable the task |

## Open questions


## Sources
-
