import re,sys,glob,yaml,os
ROOT="requirements/tiers"
P="MDOKFSTUDIO-"
def path(id):
    kind="strs" if id.startswith("StRS") else "swrs"
    f=glob.glob(f"{ROOT}/{kind}/*/{id if id.startswith(('StRS','SwRS')) else ''}.md")
    return f[0] if f else None
def full(short):
    # short like PALETTE-045 or StRS-PALETTE-001
    if short.startswith(("StRS-","SwRS-")):
        k,r=short.split("-",1); return f"{k}-{P}{r}" if not r.startswith(P) else short
    return f"SwRS-{P}{short}"
def load(id):
    p=path(id); t=open(p,encoding="utf-8").read()
    m=re.match(r"---\n(.*?)\n---\n",t,re.S)
    return p,t,yaml.safe_load(m.group(1))
def setlist(id,key,vals):
    p,t,fm=load(id)
    m=re.match(r"---\n(.*?)\n---\n",t,re.S)
    head=m.group(1)
    block=(f"{key}: []" if not vals else f"{key}:\n"+"\n".join(f"- {v}" for v in vals))
    pat=re.compile(rf"^{key}:(?: \[\])?\n(?:- .*\n?)*|^{key}: \[\]$|^{key}:$",re.M)
    if re.search(rf"^{key}:",head,re.M):
        # replace key line and following '- ' lines
        lines=head.split("\n"); out=[];i=0
        while i<len(lines):
            if lines[i].startswith(key+":"):
                out.extend(block.split("\n")); i+=1
                while i<len(lines) and lines[i].startswith("- "): i+=1
            else: out.append(lines[i]); i+=1
        head2="\n".join(out)
    else:
        raise SystemExit(f"{id}: no key {key}")
    open(p,"w",encoding="utf-8",newline="\n").write("---\n"+head2+"\n---\n"+t[m.end():])
if __name__=="__main__":
    cmd=sys.argv[1]
    if cmd=="show":
        for s in sys.argv[2:]:
            p,t,fm=load(full(s))
            print(fm["id"].split(P)[1],fm["req_lifecycle"],"|",fm["title"],"| D:",[x.split(P)[1] for x in fm.get("derives_from") or []],"| dep:",[x.split(P)[1] for x in fm.get("depends_on") or []],"| rel:",[x.split(P)[1] for x in fm.get("relates_to") or []])

def setbody(id, body):
    """Replace the authored body (after frontmatter, before okf:links) with body."""
    p,t,fm=load(id)
    m=re.match(r"---\n(.*?)\n---\n",t,re.S)
    rest=t[m.end():]
    i=rest.find("<!-- okf:links:start -->")
    tail=rest[i:] if i>=0 else ""
    out=t[:m.end()]+"\n"+body.strip("\n")+"\n"+("\n"+tail if tail else "")
    open(p,"w",encoding="utf-8",newline="\n").write(out)
def getbody(id):
    p,t,fm=load(id)
    m=re.match(r"---\n(.*?)\n---\n",t,re.S)
    rest=t[m.end():]
    i=rest.find("<!-- okf:links:start -->")
    return rest[:i] if i>=0 else rest
def addkey(id,key,vals,after="derives_from"):
    p,t,fm=load(id)
    m=re.match(r"---\n(.*?)\n---\n",t,re.S)
    head=m.group(1)
    if re.search(rf"^{key}:",head,re.M): return setlist(id,key,vals)
    lines=head.split("\n");out=[];i=0
    while i<len(lines):
        out.append(lines[i])
        if lines[i].startswith(after+":"):
            i+=1
            while i<len(lines) and lines[i].startswith("- "): out.append(lines[i]); i+=1
            out.extend((f"{key}: []" if not vals else f"{key}:\n"+"\n".join(f"- {v}" for v in vals)).split("\n"))
            continue
        i+=1
    open(p,"w",encoding="utf-8",newline="\n").write("---\n"+"\n".join(out)+"\n---\n"+t[m.end():])
def setfield(id,key,value):
    """Set a scalar frontmatter field (single line)."""
    p,t,fm=load(id)
    m=re.match(r"---\n(.*?)\n---\n",t,re.S)
    head=m.group(1); lines=head.split("\n"); out=[]; i=0; done=False
    while i<len(lines):
        if lines[i].startswith(key+":"):
            out.append(f"{key}: {value}"); done=True; i+=1
            while i<len(lines) and lines[i].startswith("  "): i+=1
        else: out.append(lines[i]); i+=1
    if not done: raise SystemExit("no "+key)
    open(p,"w",encoding="utf-8",newline="\n").write("---\n"+"\n".join(out)+"\n---\n"+t[m.end():])
