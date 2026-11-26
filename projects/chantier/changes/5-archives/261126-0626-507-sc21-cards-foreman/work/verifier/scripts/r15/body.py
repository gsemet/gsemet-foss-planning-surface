import json, sys, io, difflib
cr, scratch = sys.argv[1], sys.argv[2]
d = json.load(open(cr + '/work/verifier/pr487-r15.json.log', encoding='utf-8'))
posted = d.pop('body')
print(d)
local = open(cr + '/pr-body.md', 'rb').read()
print('local bytes', len(local), 'bom', local[:3] == b'\xef\xbb\xbf', 'crlf', b'\r' in local)
l = local.decode('utf-8')
p = posted.replace('\r\n', '\n')
print('posted chars', len(posted), 'crlf in posted', '\r' in posted, 'bom', posted.startswith('\ufeff'))
print('posted == local', p == l, 'rstrip equal', p.rstrip() == l.rstrip())
for x in difflib.unified_diff(l.splitlines(), p.splitlines(), 'local', 'posted', lineterm='', n=1):
    print(x)
open(scratch + '/posted-r15.md', 'w', encoding='utf-8', newline='\n').write(p)
old = open(cr + '/work/verifier/r14-pr-body-posted.md', encoding='utf-8').read().replace('\r\n', '\n')
print('--- diff old posted (r14) -> posted now')
for x in difflib.unified_diff(old.splitlines(), p.splitlines(), 'r14', 'now', lineterm='', n=0):
    print(x)
