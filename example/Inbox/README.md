# Inbox: drop zone

Drop anything here: .md, .txt, .pdf, .docx, emails saved as text, transcripts, links in a .md file.
Then tell the agent "process the inbox". It distils each item into notes/, people/ or projects/
and moves the original into processed/originals/. Nothing is ever deleted.

Tip: give files a telling name (`2027-01-14-meeting-acme.md`, not `Untitled.txt`). It speeds up filing.

## Bulk drops
A large export (a whole notes app, a mailbox, a photo library) is not a normal inbox item.
Credentials hide in notes whose titles never say "password". Ask the agent to quarantine and read
it deliberately, and do not leave it here where an unattended scheduled run will compile it.

## Captures from a phone
A share-sheet shortcut that writes `YYYY-MM-DD-slug.md` here, with a `Source:` URL line and the
page text under `## Full text`, works well. If `## Full text` is empty, the page was paywalled or
script-heavy: the agent fetches the URL before ingesting.
