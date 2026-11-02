# _sensitive-hold: quarantine

Files that hold credentials, recovery codes, card or account numbers, or identity numbers land here
when an agent finds them during ingest.

## Rules for agents
- You may move a file INTO this folder. Say so in your report.
- Never ingest, quote, summarise, copy or move anything OUT of this folder.
- Never open images in this folder.
- In session digests, write only "one file moved to _sensitive-hold" and the original filename.

## Rules for the owner
- Move each secret into a password manager, then move the file to `_to_delete/` or remove it yourself.
- Never sync this folder to a public place. The kit's `.gitignore` excludes it.
