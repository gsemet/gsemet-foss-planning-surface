"""Build the data of the 4-view journey prototype: okfreq report + scope titles + Main paths."""
import glob, json, os, re, sys
src, mp_dir = sys.argv[1], sys.argv[2]
D = json.loads(open('data.js').read()[len('window.REQ_DATA='):-1])
groups = {}
for m in re.finditer(r'\{ id: "([^"]+)", title: "([^"]+)", scope: "((?:[^"\\]|\\.)*)"', open(os.path.join(src, 'test/shared/e2eGroups.ts')).read()):
    groups[m.group(1)] = {'title': m.group(2), 'desc': m.group(3).replace('`', '')}
STEP = re.compile(r'^(\d+)\.\s+(.+)$')
BUL = re.compile(r'^\s+-\s+(Option\s+)?(SwRS-[A-Z0-9-]+)(?:\s+\((\w+)\))?:\s*(.+)$')
def parse(text):
    paths, cur = [], None
    for line in text.splitlines():
        h = re.match(r'^####\s+Path\s+\d+:\s*(.+)$', line)
        if h: cur = {'title': h.group(1).strip(), 'steps': []}; paths.append(cur); continue
        if cur is None: continue
        s = STEP.match(line)
        if s: cur['steps'].append({'state': s.group(2).strip(), 'via': None, 'options': []}); continue
        b = BUL.match(line)
        if b and cur['steps']:
            item = {'id': b.group(2), 'kind': b.group(3), 'label': b.group(4).strip()}
            st = cur['steps'][-1]
            if b.group(1): st['options'].append(item)
            elif st['via'] is None: st['via'] = item
    return paths
mp = {}
for f in glob.glob(os.path.join(mp_dir, 'StRS-*.md')):
    mp[os.path.basename(f)[:-3]] = parse(open(f).read())
D['groups'] = groups; D['mainPaths'] = mp
open('journey-data.js', 'w').write('window.REQ_DATA=' + json.dumps(D, separators=(',', ':')) + ';')
print(len(groups), {k: [len(p['steps']) for p in v] for k, v in mp.items()})
