import sys,re,os,random
S,F=sys.argv[1],sys.argv[2]
body=open(F+"/pr-body.md",encoding="utf-8").read()
sec=body.split("### The last reading of the open rows")[1].split("### Homes kept")[0]
kind={r.split("\t")[0]:r.split("\t")[1] for r in open(S+"/open.tsv",encoding="utf-8").read().splitlines()[1:]}
inv={}
for l in open(S+"/inventory.md",encoding="utf-8").read().split("## Rows")[1].split("## No-rule lines")[0].splitlines():
    m=re.match(r"^\| ([A-Z]+-[A-Z]?\d+) \| (.*)",l)
    if m:
        c=[x.strip() for x in l.replace(chr(92)+"|",chr(1)).split("|")][1:-1]
        inv[m.group(1)]=c
L={}
for l in sec.splitlines():
    m=re.match(r'^- ([A-Z]+-[A-Z]?\d+): (.*?) (CLI )?`([^`]+)` "(.*)"\s*$',l)
    if m: L[m.group(1)]=m.groups()[1:]
random.seed(int(sys.argv[3]))
ids=[]
for k,nn in (("a",6),("b",6),("c",1),("d",2),("e",9)):
    pool=sorted(i for i in L if kind[i]==k)
    ids+=random.sample(pool,min(nn,len(pool)))
R="skills/chantier/references/"; C="skills/chantier/scripts/cli/src/chantier/"
for i in ids:
    rule,cli,path,span=L[i]
    p= C+path if cli else (path if path.startswith(("skills/","agents/")) else R+path)
    t=re.sub(r"\s+"," ",open(p,encoding="utf-8").read()); s=re.sub(r"\s+"," ",span)
    j=t.find(s)
    c=inv[i]
    print(f"## {i} kind {kind[i]}\n BASE[{c[1]} | {c[2]}] {c[3]}\n PR: {rule}\n HOME {path}: ...{t[max(0,j-220):j+len(s)+200]}...\n")
