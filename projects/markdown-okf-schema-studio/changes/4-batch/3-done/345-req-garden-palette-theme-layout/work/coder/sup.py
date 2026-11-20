import subprocess, re
R = "C:/Users/gaeta/Projets/markdown-okf-schema-studio.worktrees/batch-06-CR-345"
files = subprocess.check_output(["git","ls-files","requirements/tiers"],cwd=R,text=True).split("\n")
sup=set()
for f in files:
    if not f.endswith(".md"): continue
    try: t=open(R+"/"+f,encoding="utf-8").read(3000)
    except: continue
    if re.search(r"^req_lifecycle:\s*superseded", t, re.M):
        m=re.search(r"^id:\s*(\S+)", t, re.M)
        if m: sup.add(m.group(1).strip("'\""))
out = subprocess.check_output(["git","grep","-nE","@(implements|tests)_req","--","src","test","sphinx","skills"],cwd=R,text=True,errors="replace")
for l in out.split("\n"):
    m=re.search(r"@(?:implements|tests)_req\s+(\S+)", l)
    if m and m.group(1) in sup: print(l)
print(len(sup),"superseded")
