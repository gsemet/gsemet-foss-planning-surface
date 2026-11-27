import sys,re,os,glob
S,F=sys.argv[1],sys.argv[2]
body=open(F+"/pr-body.md",encoding="utf-8").read()
sec=body.split("### The last reading of the open rows")[1].split("### Homes kept")[0]
R="skills/chantier/references/"; C="skills/chantier/scripts/cli/src/chantier/"
def norm(s): return re.sub(r"\s+"," ",s)
miss=[];n=0
for l in sec.splitlines():
    m=re.match(r'^- ([A-Z]+-[A-Z]?\d+): (.*?) (CLI )?`([^`]+)` "(.*)"\s*$',l)
    if not m:
        if re.match(r"^- [A-Z]+-[A-Z]?\d+",l): miss.append(("unparsed",l))
        continue
    n+=1
    i,rule,cli,path,span=m.groups()
    p= C+path if cli else (path if path.startswith(("skills/","agents/")) else R+path)
    if not os.path.exists(p): miss.append((i,"no file",p));continue
    t=open(p,encoding="utf-8").read()
    if span not in t and norm(span) not in norm(t): miss.append((i,"span",p,span))
print("checked",n)
for x in miss: print(x)
