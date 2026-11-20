import re,glob,io
P="MDOKFSTUDIO-"
def path(i):
    if i.startswith("st:"):
        return glob.glob("requirements/tiers/strs/*/StRS-"+P+i[3:]+".md")[0]
    g=glob.glob("requirements/tiers/swrs/*/SwRS-"+P+i+".md")
    return g[0]
def load(i):
    return open(path(i),encoding="utf-8",newline="").read()
def save(i,t):
    open(path(i),"w",encoding="utf-8",newline="").write(t)
def q(s):
    if re.search(r"[:#\[\]{}&*!|>'\"%@`,]|^[-?]",s) :
        return "'"+s.replace("'","''")+"'"
    return s
def set_scalar(t,key,val):
    pat=re.compile(rf"^{key}:.*(?:\n  .*)*",re.M)
    assert pat.search(t),key
    return pat.sub(lambda m:f"{key}: {q(val)}",t,count=1)
def set_list(t,key,items):
    full=[("SwRS-" if not x.startswith(("StRS-","SwRS-")) else "")+x for x in items]
    full=[x if x.startswith(("StRS-","SwRS-")) else x for x in full]
    full=[re.sub(r"^(StRS|SwRS)-(?!MDOKFSTUDIO)",r"\1-"+P,x) for x in full]
    pat=re.compile(rf"^{key}:(?: \[\])?\n?(?:- .*\n)*",re.M)
    m=pat.search(t); assert m,key
    new=f"{key}: []\n" if not full else f"{key}:\n"+"".join(f"- {x}\n" for x in full)
    return t[:m.start()]+new+t[m.end():]
def get_list(t,key):
    m=re.search(rf"^{key}:(?: \[\])?\n?((?:- .*\n)*)",t,re.M)
    return [x[2:] for x in m.group(1).split("\n") if x] if m else []
def split(t):
    a,b=t.split("\n---\n",1)
    pre,post=(b.split("<!-- okf:links:start -->",1)+[None])[:2]
    return a+"\n---\n",pre,post
def set_body(t,body):
    fm,pre,post=split(t)
    return fm+"\n"+body.strip("\n")+"\n"+("\n<!-- okf:links:start -->"+post if post is not None else "")
def get_body(t):
    return split(t)[1].strip("\n")
