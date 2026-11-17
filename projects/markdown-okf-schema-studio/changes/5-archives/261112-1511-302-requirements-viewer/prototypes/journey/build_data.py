import json, re, sys, subprocess
d = json.load(open('report.json'))
sha = sys.argv[1]
out = []
for r in d['requirements']:
    fm = r['frontmatter']; text = r['text']
    body = text.split('\n---\n', 1)[1] if '\n---\n' in text else text
    body = body.split('<!-- okf:links:start -->')[0]
    scen = []
    for m in re.finditer(r'### Scenario(?: \((\w+)\))?: (.+?)\n\n((?:- .+\n?)+)', body):
        steps = [re.sub(r'^- ', '', l).strip() for l in m.group(3).strip().split('\n')]
        scen.append([m.group(1) or 'nominal', m.group(2).strip(), steps])
    lc = fm.get('req_lifecycle') or fm.get('status')
    def sec(name):
        m = re.search(r'### ' + name + r'\n\n([\s\S]+?)(?=\n### |\Z)', body)
        return ' '.join(m.group(1).split()) if m else ''
    known = re.search(r'### Known issues?\n\n([\s\S]+?)(?=\n### |\Z)', body)
    out.append({
        'id': r['id'], 't': r['tier'], 's': r['scope'], 'lc': lc,
        'ti': fm.get('title', ''), 'de': ' '.join(str(fm.get('description', '')).split()),
        'un': ' '.join(str(fm.get('user_need', '')).split()) if fm.get('user_need') else '',
        'df': r.get('derives_from') or [], 'sb': r.get('superseded_by') or [],
        'im': r['implementation']['files'], 'te': r['tests']['files'],
        'sc': scen, 'ki': known.group(1).strip() if known else '', 'ra': sec('Rationale and constraints'), 'vn': sec('Verification notes')[:600],
    })
data = {'sha': sha, 'generated': d['generated_at'], 'totals': d['totals'],
        'strsCoverage': d['stakeholder_test_coverage'],
        'scopes': d['scopes'], 'reqs': out}
s = json.dumps(data, separators=(',', ':'))
open('data.js', 'w').write('window.REQ_DATA=' + s + ';')
print(len(s), len(out), sum(1 for x in out if x['lc'] not in ('superseded','deprecated')))
import collections; print(collections.Counter(len(x['sc']) for x in out).most_common(5)); print(sum(1 for x in out if x['ki']))
