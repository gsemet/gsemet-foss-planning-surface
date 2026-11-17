import json,pathlib,re,subprocess,sys
repo=pathlib.Path(sys.argv[1]); ch=repo/'.agents/changes'; req=ch/'requests'
U='https://github.com/gsemet/markdown-okf-schema-studio/pull/'
prs={}
for p in json.loads(subprocess.check_output(['gh','pr','list','-R','gsemet/markdown-okf-schema-studio','--state','all','--limit','80','--json','number,headRefName,state'])):
    prs.setdefault(p['headRefName'],p)
def title(d):
    f=d/'00-request.md'
    if f.exists():
        h=f.read_text().splitlines()[0].lstrip('# ').strip()
        return re.sub(r'^\d{3}\s*[—-]\s*','',h)
    return d.name[4:]
def header(d):
    f=d/'STATE.md'; t=f.read_text() if f.exists() else ''
    g=lambda k: (re.search(rf'{k}: ([^·\n]+)',t) or [None,''])[1].strip()
    br=re.search(r'`([a-z-]+/[^`]+)`',t) or re.search(r'branch ([a-z-]+/\S+)',t)
    return g('status'),g('step'),g('round'),(br[1] if br else '')
BR={'000':'','042':'docs/stacked-prs','029':'test/visual-extension-states'}
PRN={'030':21}
SUBJ={'044':'Flaky linked-target watcher test (P1)','045':'Built-in PlantUML JS engine + file includes','046':'Light animations','047':'Initial state: cream, collapsed bar, GFM','050':'conf.py warning banner + pasted image placement','051':'Perf: zero page reloads while typing','000':'Founding task: Sphinx/MyST live view (tasks 01–07)','052':'Keep the Mac awake during window tests (docs)','048':'Local real VS Code suite on macOS (undo, slash menu)','049':'Branch naming rule (docs)','053':'Dependabot: Pillow 13 and certifi security updates','056':'Refactor: host-neutral core, typed protocol, page bundle (one PR)','057':'CONTRIBUTING: document the npm security overrides','058':'Pasted image sometimes saved as an empty file','059':'Requirements baseline with okfreq: inventories (Sonnet)'}
def prcell(br,cr=''):
    if cr in PRN: n=PRN[cr]; return f'[#{n}]({U}{n}) merged'
    p=prs.get(br)
    return f"[#{p['number']}]({U}{p['number']}) {p['state'].lower()}" if p else '—'
act=[];land=[]
for d in sorted(x for x in req.iterdir() if re.match(r'\d{3}-',x.name)):
    st,step,rnd,br=header(d); br=br or BR.get(d.name[:3],'') or (f'changes-requests/{d.name}' if d.name[:3].isdigit() and int(d.name[:3])>=50 else '')
    status=' · '.join(x for x in [st,step,rnd] if x) or 'briefed'
    act.append(f'| [{d.name[:3]}]({d.name}/00-request.md) | {SUBJ.get(d.name[:3],title(d))} | [{status}]({d.name}/STATE.md) | {("`"+br+"`") if br else "—"} | {prcell(br)} |')
for d in sorted((x for x in (ch/'archives').iterdir() if re.match(r'\d{3}-',x.name)),reverse=True):
    if 0<int(d.name[:3])<24: continue
    st,step,rnd,br=header(d); br=br or BR.get(d.name[:3],'') or (f'changes-requests/{d.name}' if d.name[:3].isdigit() and int(d.name[:3])>=50 else '')
    rep='report.md' if (d/'report.md').exists() else '00-request.md'
    spec='00-request.md' if (d/'00-request.md').exists() else sorted(d.glob('*.md'))[0].name
    land.append(f'| [{d.name[:3]}](../archives/{d.name}/{spec}) | {SUBJ.get(d.name[:3],title(d))} | [report](../archives/{d.name}/{rep}) | {("`"+br+"`") if br else "—"} | {prcell(br,d.name[:3])} |')
bl=[]
for pr in sorted((ch/'backlog').glob('P*')):
    if not pr.is_dir(): continue
    for item in sorted(x for x in pr.iterdir() if x.is_dir()):
        mds=sorted(item.glob('*.md'))
        if not mds: continue
        first=mds[0]
        head=next((l.lstrip('# ').strip() for l in first.read_text(errors='ignore').splitlines() if l.startswith('#')),item.name)
        head=head.replace('|','/')[:90]
        bl.append(f'| {pr.name} | [{item.name}](../backlog/{pr.name}/{item.name}/{first.name}) | {head} | {len(mds)} |')
out=f'''# CR table

Repository: [gsemet/markdown-okf-schema-studio](https://github.com/gsemet/markdown-okf-schema-studio). Process:
[prd-workflow.guidelines.md](../../guidelines/prd-workflow.guidelines.md). Live status:
[ORCHESTRATOR-STATUS.md](ORCHESTRATOR-STATUS.md). Worktree of CR NNN: `../markdown-okf-schema-studio-wt-NNN`.

## Active

| CR (spec) | Subject | Status (STATE.md) | Branch | PR |
| --- | --- | --- | --- | --- |
''' + '\n'.join(act) + '''

## Backlog

Not started yet. Priority folder, item (opens its first file), its title, number of files.

| Priority | Item | Title | Files |
| --- | --- | --- | --- |
''' + '\n'.join(bl) + '''

## Landed

| CR (spec) | Subject | Report | Branch | PR |
| --- | --- | --- | --- | --- |
''' + '\n'.join(land) + '\n'
(req/'ORCHESTRATOR.md').write_text(out)

import datetime
lines=[f"# Orchestrator status — {datetime.datetime.now():%Y-%m-%d %H:%M}",""]
for d in sorted(x for x in req.iterdir() if re.match(r'\d{3}-',x.name)):
    t=(d/'STATE.md').read_text().splitlines()[:4] if (d/'STATE.md').exists() else []
    lines.append(f"- [{d.name}]({d.name}/STATE.md): " + " / ".join(x.strip() for x in t))
lock=req/'WINDOW-TESTS.lock'
lines.append("")
lines.append("Window-test lock: " + (lock.read_text().strip() if lock.exists() else "free"))
caf=subprocess.run(['pgrep','-x','caffeinate'],capture_output=True,text=True).stdout.strip()
lines.append("caffeinate: " + (f"running (pid {caf})" if caf else "not running"))
(req/'ORCHESTRATOR-STATUS.md').write_text("\n".join(lines)+"\n")
