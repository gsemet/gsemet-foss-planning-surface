"""Round 4 proofs, read-only. Run from the worktree:
uv run --no-sync --project . python -I <this file>"""

import json
import re
import subprocess
from pathlib import Path

import chantier
from chantier.commands.help import load_topics
from chantier.driver_prompt import driver_table

WT = Path('C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507')
SKILL = WT / 'skills' / 'chantier'
NEXT = SKILL / 'cards-next'
REFS = SKILL / 'references'
print('chantier from', Path(chantier.__file__).as_posix(), chantier.__version__)

topics = load_topics(NEXT / 'topics.json')
raw = json.loads((NEXT / 'topics.json').read_text(encoding='utf-8'))['topics']
print('topics loaded:', len(topics))
bad = []


def forms(r):
    return list(r.values()) if isinstance(r, dict) else [r]


for name, t in raw.items():
    for r in t['readings']:
        for f in forms(r):
            file, _, head = f.partition('#')
            p = NEXT / file
            if not p.is_file():
                bad.append((name, f, 'missing'))
            elif head and not re.search(r'^## ' + re.escape(head) + r'\s*$', p.read_text(encoding='utf-8'), re.M):
                bad.append((name, f, 'no heading'))
print('readings unresolved:', bad or 'none')

roles = re.findall(r'^  ([a-z][a-z-]*):\s*$', (SKILL / 'roles.yaml').read_text(encoding='utf-8') if (SKILL / 'roles.yaml').exists() else '', re.M)
print('roles in topics:', sorted({r for t in raw.values() for r in t['roles']}))

md = sorted(p for p in NEXT.rglob('*') if p.suffix in ('.md', '.json') and p.name != 'topics.json')
unknown = []
for p in md:
    s = p.read_text(encoding='utf-8')
    for m in re.finditer(r'(?:`|\$CHANTIER )help ([a-z][a-z0-9-]*)', s):
        if m.group(1) not in raw:
            unknown.append((p.relative_to(NEXT).as_posix(), m.group(1)))
    for lst in re.finditer(r'Rare cases[^:]*: ((?:`[^`]+`(?:, )?)+)', s):
        for n in re.findall(r'`(?:help )?([a-z][a-z0-9-]*)`', lst.group(1)):
            if n not in raw:
                unknown.append((p.relative_to(NEXT).as_posix(), n))
print('help names without a row:', unknown or 'none')

over = sorted((p.name, p.stat().st_size) for p in (NEXT / 'topics').glob('*.md') if p.stat().st_size > 1500)
print('topic files:', len(list((NEXT / 'topics').glob('*.md'))), 'over 1500:', len(over))
for n, s in over:
    print('  ', s, n)


def slug(h):
    h = re.sub(r'[`*]', '', h.strip().lower())
    h = re.sub(r'[^\w\- ]', '', h)
    return h.replace(' ', '-')


def anchors(p):
    return {slug(h) for h in re.findall(r'^#{1,6} (.*)$', p.read_text(encoding='utf-8'), re.M)}


broken, into_refs, outside = [], [], []
count = 0
for p in sorted(NEXT.rglob('*')):
    if p.suffix not in ('.md', '.json'):
        continue
    s = p.read_text(encoding='utf-8')
    rel = p.relative_to(NEXT).as_posix()
    if 'references/' in s:
        for line in s.splitlines():
            for m in re.finditer(r'.{0,50}references/.{0,40}', line):
                into_refs.append((rel, m.group(0)))
    if p.suffix != '.md':
        continue
    s = re.sub(r'```.*?```', '', s, flags=re.S)
    for target in re.findall(r'\]\(([^)\s]+)\)', s):
        if re.match(r'[a-z]+:', target):
            continue
        count += 1
        path, _, frag = target.partition('#')
        if rel.startswith('skills/'):
            home = WT / 'skills' / p.name.removesuffix('-SKILL.md')
            if path.startswith('../chantier/references/'):
                q = NEXT / path.removeprefix('../chantier/references/')
            else:
                q = (home / path).resolve()
        else:
            q = (p.parent / path).resolve() if path else p
        if not q.exists():
            broken.append((rel, target))
            continue
        if frag and q.suffix == '.md' and frag not in anchors(q):
            broken.append((rel, target, 'anchor'))
        q = q.resolve()
        if not q.is_relative_to(NEXT.resolve()):
            outside.append((rel, target))
            if q.is_relative_to(REFS.resolve()):
                broken.append((rel, target, 'into references/'))
print('relative links:', count, 'broken:', broken or 'none')
print('resolving outside cards-next:', outside or 'none')
print('text naming references/:')
for r in into_refs:
    print('  ', r)

for a, b in (('floor.md', 'floor.md'), ('hosts/claude-code.json', 'hosts/claude-code.json'), ('hosts/copilot.json', 'hosts/copilot.json')):
    r = subprocess.run(['git', '-C', str(WT), 'show', f'HEAD:skills/chantier/references/{b}'], capture_output=True, check=True).stdout
    n = (NEXT / a).read_bytes()
    print('cmp', a, 'worktree bytes equal:', n == (REFS / b).read_bytes(), '; equal to HEAD LF:', n.replace(b'\r\n', b'\n') == r)

forbidden = ['Read this short role contract at boot', '# chantier-agent:', 'chantier board']
pat = re.compile(r'batch-\d+|\bCR-\d+|\b20\d\d-\d\d-\d\d\b|\b(?:opus|sonnet|haiku|fable)\b|gpt-\d', re.I)
hits = {}
for p in sorted(NEXT.rglob('*')):
    if not p.is_file():
        continue
    s = p.read_text(encoding='utf-8')
    rel = p.relative_to(NEXT).as_posix()
    for f in forbidden:
        if f in s:
            print('FORBIDDEN', rel, f)
    found = pat.findall(s)
    if found:
        hits[rel] = sorted(set(found))[:6]
    b = p.read_bytes()
    if b.startswith(b'\xef\xbb\xbf'):
        print('BOM', rel)
print('forbidden phrases checked; date/batch/CR/model matches:')
for k, v in hits.items():
    print('  ', k, v)


def headings(p, level='## '):
    s = re.sub(r'^```.*?^```', '', p.read_text(encoding='utf-8'), flags=re.S | re.M)
    return [h for h in s.splitlines() if h.startswith(level)]


tmpl = ('Summary', 'Issues References', 'Deliverables', 'Blast radius', 'Autonomous decisions', 'Known gaps',
        'Changes', 'Human decisions', 'Impacts', 'Test plan', 'Internal references')
for p in (REFS / 'pr-template.md', NEXT / 'pr-template.md'):
    s = p.read_text(encoding='utf-8')
    block = s[s.index('## Summary'):]
    seen = [h[3:].strip() for h in block.splitlines() if h.startswith('## ') and h[3:].strip() in tmpl]
    print('template headings', p.parent.name, seen[:11] == list(tmpl), seen[:11] if seen[:11] != list(tmpl) else '')

# driver table: new file against today's
import chantier.driver_prompt as dp

old = dp.driver_table()
orig = dp.skill_dir
lines = lambda p: p.read_text(encoding='utf-8')
title = dp.DRIVER_TABLE_TITLE


def table(p):
    s = lines(p).replace('\r\n', '\n')
    sec = s[s.index(title + '\n') + len(title) + 1:]
    sec = sec[:re.search(r'^#', sec, re.M).start()]
    return [l for l in sec.splitlines() if l.startswith('|')]


print('driver table equal:', table(NEXT / 'concepts.md') == table(REFS / 'concepts.md'), 'rows', len(table(NEXT / 'concepts.md')))

version = chantier.__version__
for p in sorted((NEXT / 'skills').glob('*.md')):
    name = p.name.removesuffix('-SKILL.md')
    live = (WT / 'skills' / name / 'SKILL.md').read_text(encoding='utf-8')
    new = p.read_text(encoding='utf-8')
    front = lambda s: s[:s.index('\n---\n', 4) + 5]
    title_line = lambda s: next(l for l in s.splitlines() if l.startswith('# '))
    print('skill', name, 'frontmatter', front(live) == front(new), 'title', title_line(live) == title_line(new),
          'version', f'chantier-version: {version}' in new)

from chantier.launch import launcher_line

print('launcher form', launcher_line(Path('<plugin root>')))

print('sizes (LF bytes): file | today | new')
section1 = ['concepts.md', 'pr-template.md', 'release-template.md', 'status-layout.md', 'titles.md',
            'ticket-summary-example.md', 'routing.md', 'init.md', 'review-step.md', 'sync-checkout.md',
            'forges/github.md', 'forges/gitlab.md', 'hosts/claude-code.json', 'hosts/copilot.json',
            'hosts/claude-code.md', 'hosts/copilot.md', 'floor.md']


def lf(p):
    return len(p.read_bytes().replace(b'\r\n', b'\n')) if p.is_file() else None


for f in section1:
    print('  ', f, '|', lf(REFS / f), '|', lf(NEXT / f))
print('   topics/titles.md |', lf(NEXT / 'topics/titles.md'))
for f in sorted((NEXT / 'skills').glob('*.md')):
    name = f.name.removesuffix('-SKILL.md')
    print('  ', f'skills/{f.name}', '|', lf(WT / 'skills' / name / 'SKILL.md'), '|', lf(f))
host = sorted((NEXT / 'topics').glob('host-*.md'))
print('host topics:', len(host), 'bytes', sum(map(lf, host)), 'max', max(map(lf, host)))
