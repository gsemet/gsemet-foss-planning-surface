CRLF=chr(13)+chr(10)
LF=chr(10)
import re,glob
ROOT="C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-06-CR-346/requirements/tiers"
P="MDOKFSTUDIO-"
def full(a):
    if a.startswith(("SwRS-","StRS-")): return a
    return ("StRS-" if a.startswith("S") else "SwRS-")+P+a
def path(a):
    kind=("strs" if a.startswith("StRS") or (not a.startswith("SwRS") and a.startswith("S")) else "swrs")
    pre="StRS" if kind=="strs" else "SwRS"
    a=a.replace("SwRS-","").replace("StRS-","").replace(P,"")
    return glob.glob(f"{ROOT}/{kind}/*/{pre}-{P}{a}.md")[0].replace(chr(92),"/")
def rd(a):
    return open(path(a),encoding="utf-8",newline="").read().replace(CRLF,LF)
def wr(a,t):
    p=path(a)
    nl=CRLF if CRLF.encode() in open(p,"rb").read() else LF
    open(p,"w",encoding="utf-8",newline="").write(t.replace(CRLF,LF).replace(LF,nl))
def split_fm(t):
    m=re.match(r"---\n(.*?\n)---\n",t,re.S)
    return m.group(1),t[m.end():]
def get_list(a,key):
    fm,_=split_fm(rd(a))
    m=re.search(rf"^{key}:(?: \[\])?\n((?:- .*\n)*)",fm,re.M)
    if not m: return []
    return [l[2:].strip() for l in m.group(1).splitlines()]
def set_list(a,key,items,after=None):
    t=rd(a); fm,body=split_fm(t)
    block=(f"{key}:\n"+"".join(f"- {i}\n" for i in items)) if items else f"{key}: []\n"
    pat=re.compile(rf"^{key}:(?: \[\])?\n(?:- .*\n)*",re.M)
    if pat.search(fm): fm=pat.sub(lambda m:block,fm,count=1)
    else:
        # insert before a key in 'after' list or at end
        for k in (after or ["derived_by","default_owner_email"]):
            m=re.search(rf"^{k}:",fm,re.M)
            if m: fm=fm[:m.start()]+block+fm[m.start():]; break
        else: fm+=block
    wr(a,"---\n"+fm+"---\n"+body)
def drop(a,key,ids):
    ids=[full(i) for i in ids]
    cur=get_list(a,key); new=[c for c in cur if c not in ids]
    if new!=cur: set_list(a,key,new)
    return cur!=new
def add(a,key,ids):
    cur=get_list(a,key)
    for i in ids:
        i=full(i)
        if i not in cur: cur.append(i)
    set_list(a,key,cur)
def body_replace(a,old,new,count=0):
    t=rd(a)
    assert old in t,(a,old[:40])
    wr(a,t.replace(old,new) if not count else t.replace(old,new,count))
def insert_scenarios(a,text):
    t=rd(a)
    for h in ("### Related requirements","### Verification notes","<!-- okf:links:start -->"):
        i=t.find(h)
        if i>=0: break
    else: i=len(t)
    wr(a,t[:i]+text.strip("\n")+"\n\n"+t[i:])
def add_verif(a,line):
    t=rd(a)
    i=t.find("<!-- okf:links:start -->")
    if i<0: i=len(t)
    j=t.find("### Verification notes")
    assert j>=0,a
    head=t[:i].rstrip("\n")+"\n"+"- "+line.lstrip("- ")+"\n"
    wr(a,head+("\n"+t[i:] if i<len(t) else ""))

import json
def get_desc(a):
    fm,_=split_fm(rd(a))
    from ruamel.yaml import YAML
    d=YAML(typ="safe").load(fm)
    return d["description"].strip()
def set_desc(a,new):
    """replace the description in the frontmatter and the matching first paragraph of the body"""
    t=rd(a); fm,body=split_fm(t)
    old=get_desc(a)
    m=re.search(r"^description:.*\n(?:[ \t]+.*\n)*",fm,re.M)
    fm=fm[:m.start()]+"description: "+json.dumps(new,ensure_ascii=False)+"\n"+fm[m.end():]
    # body: paragraph under Normative behavior starting with old
    assert old in body,(a,"desc not in body")
    body=body.replace(old,new,1)
    wr(a,"---\n"+fm+"---\n"+body)
def extend_desc(a,extra):
    d=get_desc(a)
    set_desc(a,d+" "+extra)

def extend_desc(a,extra):
    """append a sentence to the fm description and to the last paragraph of Normative behavior"""
    t=rd(a); fm,body=split_fm(t)
    d=get_desc(a)
    m=re.search(r"^description:.*\n(?:[ \t]+.*\n)*",fm,re.M)
    fm=fm[:m.start()]+"description: "+json.dumps(d+" "+extra,ensure_ascii=False)+"\n"+fm[m.end():]
    i=body.find("### Normative behavior")
    j=body.find("\n### ",i+5)
    sec=body[i:j].rstrip("\n")
    body=body[:i]+sec+" "+extra+"\n"+body[j:]
    wr(a,"---\n"+fm+"---\n"+body)
def drop_related(a,idfrag):
    t=rd(a)
    lines=[l for l in t.split("\n") if not (l.startswith("- ") and idfrag in l.split(":")[0] and "SwRS" in l and "Related" not in l)]
    wr(a,"\n".join(lines))
