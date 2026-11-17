"""Write one prototype per step of the journey, from site.html and journey-data.js.

python3 build_steps.py <out_dir> [--inline]
"""
import json, sys
out, inline = sys.argv[1], '--inline' in sys.argv
site = open('site.html').read()
data = open('journey-data.js').read().replace('</', '<\\/')
STEPS = [
    {"file": "00-design-system.html", "name": "Design system"},
    {"file": "01-areas.html", "name": "Areas", "start": "#/"},
    {"file": "02-area.html", "name": "An area", "start": "#/area/diagrams"},
    {"file": "03-use-case.html", "name": "A use case", "start": "#/use-case/StRS-MDOKFSTUDIO-DIAG-001"},
    {"file": "04-behaviour.html", "name": "A behaviour", "start": "#/behaviour/SwRS-MDOKFSTUDIO-DIAG-015"},
    {"file": "05-search.html", "name": "Search", "start": "#/", "search": "mermaid"},
]
nav = [{"file": s["file"], "name": s["name"]} for s in STEPS]
for i, s in enumerate(STEPS):
    if "start" not in s: continue
    cfg = f'<script>window.PROTO_STEPS={json.dumps(nav)};window.PROTO_CURRENT={i};window.PROTO_START={json.dumps(s["start"])};' + (f'window.PROTO_SEARCH={json.dumps(s["search"])};' if "search" in s else '') + '</script>'
    src = '<script>' + data + '</script>' if inline else '<script src="journey-data.js"></script>'
    html = site.replace('<script src="journey-data.js"></script>', cfg + src)
    open(f'{out}/{s["file"]}', 'w').write(html)
D = json.loads(open('journey-data.js').read()[len('window.REQ_DATA='):-1])
areas = [D['groups'][k]['title'] for k in D['groups'] if k in D['scopes']]
ds = open('ds.html').read().replace('<!--DS-CONFIG-->', f'<script>window.PROTO_STEPS={json.dumps(nav)};window.DS_AREAS={json.dumps(areas)};</script>')
open(f'{out}/00-design-system.html', 'w').write(ds)
print('written', [s["file"] for s in STEPS if "start" in s])
