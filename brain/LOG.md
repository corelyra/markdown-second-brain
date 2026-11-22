# LOG: what happened to the brain, in order

Append only; never edit past entries. Newest at the bottom. One entry per operation.
Format: a `## [YYYY-MM-DD] op | title` heading, then one to three lines: files changed, anything flagged.
Ops: `ingest` (a source compiled), `query` (an answer filed as a brief), `lint` (a dream or lint run),
`restructure` (folders, procedures or the map changed).
Read with `python3 scripts/log-recent.py LOG.md` (newest 15), add a keyword to search,
or list the headings: `grep '^## \[' LOG.md | tail -20`.
