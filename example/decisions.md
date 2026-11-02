# decisions: audit log

Append only; never edit past entries. Newest at the bottom.
Format: a dated `## YYYY-MM-DD: what was decided` heading, then `- Why:` and `- Source:` lines.
Read with `python3 scripts/log-recent.py decisions.md` (newest 15) or add a keyword to search.

## 2026-10-12: Use flat Markdown folders for the second brain
- Why: readable by people and agents, no app lock-in, works in any synced folder.
- Source: Alex, in conversation, 12 Oct 2026.

## 2026-10-20: Renew contents insurance with the current insurer
- Why: the renewal quote matched the cheapest comparison quote; switching saved nothing.
- Source: Inbox/processed/2026-10-20-home-insurance-renewal.md
