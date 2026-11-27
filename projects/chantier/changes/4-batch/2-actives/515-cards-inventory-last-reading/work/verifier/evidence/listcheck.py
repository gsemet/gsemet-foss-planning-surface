import sys,re,os,glob,ast,collections
text=open("docs/protective-rules.md",encoding="utf-8").read()
R="skills/chantier/references/"; C="skills/chantier/scripts/cli/src/chantier/"
def norm(s): return re.sub(r"\s+"," ",s)
code={}
for f in glob.glob(C+"**/*.py",recursive=True):
    tree=ast.parse(open(f,encoding="utf-8").read())
    strs=[]
    for n in ast.walk(tree):
        if isinstance(n,ast.Constant) and isinstance(n.value,str): strs.append(n.value)
        if isinstance(n,ast.JoinedStr):
            strs.append("".join(v.value if isinstance(v,ast.Constant) else "{}" for v in n.values))
    code[f]=[norm(s) for s in strs]
floor={}
for l in open(R+"floor.md",encoding="utf-8").read().splitlines():
    m=re.match(r"(\d+)\. (.*)",l)
    if m: floor[m.group(1)]=m.group(2)
rows=[]
for l in text.splitlines():
    if l.startswith("| ") and not l.startswith("| id |"):
        c=[x.strip() for x in l.split("|")][1:-1]
        rows.append(c)
print("rows",len(rows),dict(collections.Counter(r[2] for r in rows)),"cells!=4",[r[0] for r in rows if len(r)!=4])
ids=[i for r in rows for i in r[0].split("/")]
print("dup ids",[i for i,n in collections.Counter(ids).items() if n>1])
for pref in "PABCDN":
    nums=sorted(int(i[1:]) for i in ids if re.fullmatch(pref+r"\d+",i))
    print(pref,len(nums),"max",nums[-1],"missing",sorted(set(range(1,nums[-1]+1))-set(nums)))
tok=re.compile(r'(floor \d+|refusal of `[^`]+`|(?:hook )?`[^`"]*\.(?:md|json|tsx|py)`(?: \([^)]*\))?) (?=")')
total=0;miss=[]
for r in rows:
    if r[2]=="`to add`" and r[0] not in ("P11",): 
        if '"' in r[3]: print("to add with quote",r[0],r[3])
        continue
    h=r[3]
    ms=list(tok.finditer(h))
    if not ms: miss.append((r[0],"no span",h))
    for k,m in enumerate(ms):
        end=ms[k+1].start() if k+1<len(ms) else len(h)
        seg=h[m.end():end]
        j=seg.rfind('"'); span=seg[1:j]
        # strip trailing parenthetical wrappers
        for cut in ('" (`','" and '):
            if cut in span: span=span.split(cut)[0]
        src=m.group(1); total+=1
        if src.startswith("floor"):
            n=src.split()[1]; ok= span in floor.get(n,"")
        elif src.startswith("refusal"):
            hits=[f for f,ss in code.items() if any(norm(span) in s for s in ss)]
            ok=bool(hits); print("REFUSAL",r[0],src,repr(span),[h_.replace(C,"") for h_ in hits])
        else:
            p=re.search(r"`([^`]+)`",src).group(1)
            if not p.startswith(("skills/","agents/","hooks/")) and p!="AGENTS.md": p=R+p
            if not os.path.exists(p): ok=False
            else:
                t=open(p,encoding="utf-8").read()
                ok= span in t or norm(span) in norm(t) or (p.endswith(".json") and span.replace('"','\\"') in t)
        if not ok: miss.append((r[0],src,span))
print("spans checked",total)
for x in miss: print("MISS",x)
