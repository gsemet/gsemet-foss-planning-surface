import json, sys, difflib, re, getpass, os, subprocess

cr = sys.argv[1]
surface_commit = sys.argv[2]
rel = 'projects/markdown-okf-schema-studio/changes/4-batch/2-actives/504-strs-path-validation/work/pr-body.md'


def norm(text):
    return text.replace('\r\n', '\n').rstrip('\n').split('\n')


old = json.load(open(cr + '/work/verifier/pr524.json', encoding='utf-8'))
new = json.load(open(cr + '/work/verifier/pr524-final.json', encoding='utf-8'))
raw = open(cr + '/work/pr-body.md', 'rb').read()
local = raw.decode('utf-8')
verified = subprocess.run(['git', '-C', cr, 'show', surface_commit + ':' + rel],
                          capture_output=True, check=True).stdout.decode('utf-8')

for k in ('number', 'state', 'isDraft', 'headRefOid', 'baseRefName', 'baseRefOid', 'title', 'mergeable', 'mergeStateStatus'):
    print(k + ':', new.get(k))
print('title unchanged since verified pass:', old['title'] == new['title'])

o, n, l, v = norm(old['body']), norm(new['body']), norm(local), norm(verified)
print('lines: verified-posted', len(o), 'verified-file', len(v), 'posted-now', len(n), 'file-now', len(l))
print('posted-now == file-now:', n == l)
print('verified-posted == file at', surface_commit, ':', o == v)
print('--- verified posted body -> posted body now')
for d in difflib.unified_diff(o, n, 'verified', 'posted', n=0, lineterm=''):
    print(d)
print('--- Test plan section, posted now')
inside = False
for i, line in enumerate(n, 1):
    if line.startswith('## '):
        inside = line.strip() == '## Test plan'
    if inside:
        print(i, line)

body = new['body']
home = os.path.expanduser('~')
for name in sorted({getpass.getuser(), os.path.basename(home)}):
    print('username hits', len(re.findall(re.escape(name), body, re.I)))
print('home path hits', len(re.findall(r'[A-Za-z]:[\\/]Users|/home/\w+|/Users/\w+', body)))
print('images', len(re.findall(r'!\[|<img', body)))
print('stale', len(re.findall('STALE', body)), 'UNVERIFIED', len(re.findall('UNVERIFIED', body)))
print('fold open', body.count('<details>'), 'close', body.count('</details>'))
print('BOM in file', raw.startswith(b'\xef\xbb\xbf'))
top = body.partition('## Internal references')[0]
hits = re.findall(r'\bCR[- ]?\d{3}\b|batch-\d+|work/[a-z]|\bO-\d+\b|\bA-\d+\b|\bQ\d{1,2}\b|\bD\d{1,2}\b|Verifier|Inspector|Coder|Foreman|Driver|Chief of Staff|round \d', top)
print('internal reference hits before the section:', hits)
