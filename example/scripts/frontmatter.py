#!/usr/bin/env python3
"""Add or refresh the two-line YAML frontmatter on notes/, people/ and projects/.

    ---
    description: "<one line: what the file holds, lifted from its summary line>"
    updated: YYYY-MM-DD
    ---

- description comes from the line(s) under '# Title'; for project files whose first line is
  'Status:', it is the title plus that status. Nothing is invented.
- updated is the file's last-modified date. The file's mtime is restored after writing,
  so adding frontmatter does not make every file look freshly edited.
- Existing frontmatter is left alone unless --refresh is given (then 'updated' is re-read
  from mtime and a missing description is filled). A hand-written description is never replaced.

Usage: python3 scripts/frontmatter.py [--dry-run] [--refresh] [paths...]
Run with --dry-run first. Unknown options stop the script instead of being ignored.
"""
import os, re, sys, glob, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIRS = ['notes', 'people', 'projects']
# archive/ is left out by default: it holds before-copies and dream snapshots that must stay
# byte-for-byte as they were. Pass archive paths explicitly if you want them.

def clean(s):
    s = re.sub(r'\*\*|__|`', '', s)
    s = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', s)
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def shorten(s, limit=220):
    if len(s) <= limit:
        return s
    cut = s[:limit]
    m = max(cut.rfind('. '), cut.rfind('; '))
    if m > 60:
        return cut[:m + 1] if cut[m] == '.' else cut[:m] + '...'
    return cut[:cut.rfind(' ')].rstrip(',;:') + '...'

def split_fm(text):
    if text.startswith('---\n'):
        end = text.find('\n---\n', 4)
        if end != -1:
            return text[4:end], text[end + 5:]
    return None, text

def derive(body):
    L = body.split('\n')
    i = 0
    while i < len(L) and not L[i].strip():
        i += 1
    if i >= len(L) or not L[i].startswith('# '):
        return None
    title = clean(L[i][2:])
    i += 1
    while i < len(L) and not L[i].strip():
        i += 1
    para = []
    while i < len(L) and L[i].strip() and not L[i].lstrip().startswith(('#', '|', '- ', '* ', '>')):
        para.append(L[i]); i += 1
    s = clean(' '.join(para))
    if not s or s.startswith('Status:'):
        st = re.search(r'^Status:\s*(.+)$', body, re.M)
        return shorten(title + (' (status: ' + clean(st.group(1)) + ')' if st else ''))
    return shorten(s)

def q(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

def process(path, dry, refresh):
    st = os.stat(path)
    date = datetime.date.fromtimestamp(st.st_mtime).isoformat()
    text = open(path, encoding='utf-8').read()
    fm, body = split_fm(text)
    if fm is not None and not refresh:
        return 'kept'
    fields = {}
    order = []
    if fm is not None:
        for line in fm.split('\n'):
            m = re.match(r'^([A-Za-z_]+):\s*(.*)$', line)
            if m:
                fields[m.group(1)] = m.group(2); order.append(m.group(1))
    if not fields.get('description'):
        d = derive(body)
        if d is None:
            return 'no-title'
        fields['description'] = q(d)
    fields['updated'] = date
    keys = ['description', 'updated'] + [k for k in order if k not in ('description', 'updated')]
    new = '---\n' + '\n'.join(f'{k}: {fields[k]}' for k in keys) + '\n---\n' + body.lstrip('\n')
    if new == text:
        return 'same'
    if not dry:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(new)
        os.utime(path, (st.st_atime, st.st_mtime))
    return 'written'

def main():
    known = {'--dry-run', '--refresh'}
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)
    bad = [a for a in sys.argv[1:] if a.startswith('-') and a not in known]
    if bad:
        sys.exit('frontmatter.py: unknown option ' + ' '.join(bad) + '\n' + __doc__)
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    dry = '--dry-run' in sys.argv
    refresh = '--refresh' in sys.argv
    files = args or sorted(p for d in DIRS for p in glob.glob(os.path.join(ROOT, d, '**', '*.md'), recursive=True)
                           if '/dream-snapshots/' not in p and '/before-copies' not in p)
    tally = {}
    for p in files:
        r = process(p, dry, refresh)
        tally[r] = tally.get(r, 0) + 1
        if r == 'no-title':
            print('NO TITLE:', os.path.relpath(p, ROOT))
    print(tally)

if __name__ == '__main__':
    main()
