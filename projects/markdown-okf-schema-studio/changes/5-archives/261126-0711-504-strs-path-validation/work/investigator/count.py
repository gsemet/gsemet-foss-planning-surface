import re,sys,glob,collections,yaml,os
root=sys.argv[1]
def fm(p):
    t=open(p,encoding='utf8',newline='').read()
    m=re.match(r'^---\r?\n(.*?)\r?\n---',t,re.S)
    return yaml.safe_load(m.group(1)),t
res=collections.Counter(); perarea=collections.defaultdict(collections.Counter)
paths=collections.Counter(); scen=collections.Counter(); heads=collections.Counter()
crlf=0
for tier in ('strs','swrs'):
    for p in glob.glob(f'{root}/requirements/tiers/{tier}/*/*.md'):
        if not os.path.basename(p).startswith(('StRS-','SwRS-')): continue
        d,t=fm(p)
        if '\r\n' in t: crlf+=1
        lc=d.get('req_lifecycle'); ex=d.get('annotation_exemption') is True
        live=lc in('draft','proposed','approved')
        res[(tier,lc,'exempt' if ex else 'nonex')]+=1
        if tier=='strs' and live:
            ph=re.findall(r'^#### Path (\d+): ',t,re.M); paths[len(ph)]+=1
            perarea[d['scope']]['strs']+=1
            if lc=='approved': perarea['_']['approved']+=1
            if 'scenarios' in d: print('has scenarios',p)
        if tier=='swrs' and live and not ex:
            perarea[d['scope']]['swrs']+=1
            h=re.findall(r'^### Scenario(?: \(([a-z]+)\))?:?( .*)?$',t,re.M)
            scen[len(h)]+=1
            for k,_ in h: heads[k]+=1
for k,v in sorted(res.items(),key=str):print(k,v)
print('strs paths dist',dict(paths)); print('swrs scen-count dist',dict(sorted(scen.items()))); print('kinds',dict(heads)); print('crlf',crlf)
for a,c in sorted(perarea.items()):print(a,dict(c))
