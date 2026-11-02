# decisions: audit log

Append only; never edit past entries. Newest at the bottom.
Format: a dated `## YYYY-MM-DD: what was decided` heading, then `- Why:` and `- Source:` lines.
Read with `python3 scripts/log-recent.py decisions.md` (newest 15) or add a keyword to search.
