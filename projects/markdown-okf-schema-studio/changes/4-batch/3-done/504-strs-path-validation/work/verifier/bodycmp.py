import json, sys, difflib, io, re, getpass, os
cr = sys.argv[1]
posted = json.load(open(cr + '/work/verifier/pr524.json', encoding='utf-8'))
local = open(cr + '/work/pr-body.md', encoding='utf-8').read()
p = posted['body'].replace('\r\n', '\n').rstrip('\n').split('\n')
l = local.replace('\r\n', '\n').rstrip('\n').split('\n')
print('title:', posted['title'])
print('posted lines', len(p), 'local lines', len(l), 'chars', len(posted['body']))
for d in difflib.unified_diff(l, p, 'local', 'posted', n=0, lineterm=''):
    print(d)
body = posted['body']
home = os.path.expanduser('~')
names = {getpass.getuser(), os.path.basename(home)}
for n in sorted(names):
    print('username hits', len(re.findall(re.escape(n), body, re.I)))
for m in re.finditer(r'[A-Za-z]:[\\/]Users[^\s`]*|/home/\w+|/Users/\w+', body):
    print('path hit', m.group(0))
print('images', len(re.findall(r'!\[|<img', body)))
top, _, rest = body.partition('## Internal references')
for m in re.finditer(r'\bCR[- ]?\d{3}\b|batch-\d+|work/[a-z]|\bO-\d+\b|\bA-\d+\b|\bQ\d{1,2}\b|\bD\d{1,2}\b|Verifier|Inspector|Coder|Foreman|Driver|Chief of Staff|round \d', top):
    s = m.start()
    print('ref:', m.group(0), '|', top[max(0, s-60):s+40].replace('\n', ' '))
print('stale', len(re.findall('STALE', body)), 'UNVERIFIED', len(re.findall('UNVERIFIED', body)))
print('fold open', body.count('<details>'), 'close', body.count('</details>'))
