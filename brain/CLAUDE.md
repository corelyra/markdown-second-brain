# {{OWNER_SHORT}}'s Second Brain: the map

A plain-Markdown knowledge base. You, the agent, are reading its map. Load little, search well,
write what you learn, and let the weekly dream tidy up after you.

## Standing rules (verbatim; never paraphrase or drop these)
1. Everything here is confidential. Never copy contents outside this folder unless {{OWNER_SHORT}} asks.
2. Never store passwords, PINs, card numbers, seed phrases or private keys. Write `[redacted]`.
3. `_sensitive-hold/` is never ingested, quoted or copied out. Read its README first.
4. Never delete. Move to `archive/` (or `_to_delete/` if {{OWNER_SHORT}} asks for removal).
5. Never invent facts, figures, dates, reference numbers or people. Say plainly when the brain does not know.
6. When sources disagree, record both and let {{OWNER_SHORT}} decide. Never overwrite silently.
7. Records belonging to other household members appear only where they touch {{OWNER_SHORT}}'s own documents. Ask before filing them.
8. Before you draft any prose reply for {{OWNER_SHORT}}, read `notes/writing-standard.md` and apply it. Code, quotations and pasted text are exempt.
<!-- Add your own rules below, one per line, each with a date and a one-line reason.
     Examples of the kind that earn a place:
9. For any question about email, search <your mail adapter> first (see `notes/<mail-access>.md`).
10. Never chase me for updates on <thing>; I report outcomes myself (<date>).
11. Never cite or draw facts from the sources listed in `notes/excluded-sources.md` (<date>). -->

Masters: this file and `notes/writing-standard.md`. `PROJECT-INSTRUCTIONS.md` and any copy you paste
into other tools are copies. Change the master first, then the copies.

## Owner
{{OWNER_NAME}}, {{CITY}} ({{TIMEZONE}}).
{{ONE_LINE_ROLE}}. Writes in {{LANGUAGES}}.
Strands that live here: {{STRANDS}}.

## Always loaded
@MEMORY.md

Everything else loads on demand. `decisions.md` and `LEARNINGS.md` are long logs. When a past
choice or lesson may apply, run `python3 scripts/log-recent.py decisions.md` (newest 15 entries),
or add a keyword to search the rest.

## How to find things (progressive loading)
1. Every file in `notes/`, `people/`, `projects/` opens with a two-line frontmatter:
   `description` (what it holds, when to read it) and `updated` (last edit).
2. Search the descriptions first, then open only the files that match:
   `grep -H '^description:' notes/*.md people/*.md projects/*.md | grep -i <word>`
   `INDEX.md` holds the same lines as one list (generated; for surfaces without grep).
3. Still nothing? Full-text grep over `notes/ people/ projects/`, then `Inbox/processed/` for detail
   or original wording, then `INGEST-REPORT.md` (the fact may sit in an unreadable document).
4. Follow `Related:` lines from file to file before you grep the whole tree again.
5. Cite the file you drew from, e.g. *(source: notes/home-insurance.md)*.
Never read the whole tree.

## How to write (agents record what they judge worth keeping)
- Follow `procedures/capture.md`: write facts, decisions and lessons as you go, and ask only where
  it says to.
- Before you finish a session that touched the brain, append a digest to `sessions/YYYY-MM-DD.md`.
  The weekly dream consolidates from those digests; an unrecorded session is invisible to it.
- New file: copy a `templates/` skeleton, fill the frontmatter, then run `python3 scripts/build-index.py`.

## Procedures (procedural memory; open the one you need)
| Procedure | When |
|---|---|
| `procedures/ingest.md` | "process the inbox", "ingest this", files waiting in `Inbox/`, or "remember that..." |
| `procedures/capture.md` | during and at the end of every working session |
| `procedures/dream.md` | {{DREAM_TIME}} (scheduled task), or when {{OWNER_SHORT}} says "dream" |

## Folder map
| Path | What lives there | Rule |
|---|---|---|
| `Inbox/` | Raw drop zone: articles, PDFs, meeting notes, emails, transcripts | Ingest, then move to `Inbox/processed/` |
| `Inbox/processed/` | Markdown copies of every ingested original, each starting with a `Source:` line; the originals themselves in `processed/originals/` | Detail and original wording only |
| `notes/` | One topic per file: accounts, policies, tenancies, cars, certifications, tax, recipes | Extend before creating |
| `people/` | People AND organisations: employers, clients, landlords, banks, insurers, clinics, family | One per file |
| `projects/` | Work with `Status: active / paused / done` and `Next step:` | One per file |
| `sessions/` | Session digests, dated; consolidated ones move to `sessions/dreamed/` | Short-term memory; not a source of truth until dreamed |
| `procedures/` | How-to files for repeatable jobs | Follow them; propose changes, don't drift |
| `output/` | Finished artefacts: `briefs/`, `reports/` (dream reports live here), `posts/` | Built from notes, never from `Inbox/` |
| `archive/` | Dormant projects, stale notes, `dream-snapshots/` (before-copies) | Searched only on request |
| `_sensitive-hold/` | Quarantined credentials, recovery material, identity numbers | See Standing rule 3 |
| `templates/` | Skeletons for note, person, project | Copy, don't edit |
| `scripts/` | `build-index.py`, `frontmatter.py`, `log-recent.py`, `watchdog.py` (all read the folder they sit in) | Python 3, standard library only |
| `MEMORY.md` | Core facts about {{OWNER_SHORT}}, always loaded | About 70 lines; curated |
| `TODO.md` | Running to-do list (no-deadline admin, loose ends) | Add when {{OWNER_SHORT}} names a to-do; the dream reports it weekly |
| `decisions.md` | Dated decisions: what, why, source | Append; never edit past entries |
| `LEARNINGS.md` | Dated lessons | Append |
| `INDEX.md` | Generated list of every file's description | Never edit by hand |
| `INGEST-REPORT.md` | Originals that could not be read | Check before "not in the brain" |
| `PROJECT-INSTRUCTIONS.md` | Text for a claude.ai Project (or any chat tool without folder access) | Keep in step with this map |

## Naming and format
- Lowercase, hyphens, no spaces, no dates: `home-insurance.md`, `acme-ltd.md`. Companies go in
  `people/` under the company name. Year-spans allowed where the year is the topic (`job-search-2027.md`).
- Dated filenames only in `output/` and `sessions/`.
- Every file: frontmatter, `# Title`, a one-line summary, an optional `Related:` line, the body, `## Sources` last.
- Plain Markdown: headings, bullets, tables. Link related files by relative path. No wiki-link syntax,
  no embedded databases.

## Answering
A complete answer gives the fact, the file it came from, when that file was last checked, and any
open question the brain records on the subject.
Answer in the language {{OWNER_SHORT}} asks in.
If notes record a contradiction, show both sides. If the brain lacks the answer, say so.
If the brain holds only part of the answer, give that part, name what is missing, and say where the
rest may sit: email, `INGEST-REPORT.md`, or a file still in the inbox. For facts from outside the
brain, name the source and say how sure you are.
