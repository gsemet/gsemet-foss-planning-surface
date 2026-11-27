import re, subprocess, sys, io
sys.stdout.reconfigure(encoding="utf-8")
def show(rev):
    return subprocess.run(["git","show",rev+":.agents/guidelines/release-process.guidelines.md"],capture_output=True,check=True).stdout.decode("utf-8")
head, base = show("HEAD"), show("origin/main")
card = open(r"C:/Users/gaeta/Projets/chantier/skills/chantier/references/release-template.md",encoding="utf-8").read()
def norm(s): return re.sub(r"\s+"," ",s).strip()
def rows(t): 
    return [l.strip() for l in t.splitlines() if l.startswith("| ") and ("Banned" not in l)]
cr = rows(card); hr = [l for l in rows(head) if l.count("|")==4 and '"' in l]
print("banned rows card", len(cr), "guideline", len(hr), "identical", cr==hr)
def qs(t, start):
    sec = t[t.index(start):]
    out=[]
    for m in re.finditer(r"^(\d{1,2})\. (Does|Is) (.*?)(?=^\d{1,2}\. |\n\n|\Z)", sec, re.M|re.S):
        out.append(norm(m.group(2)+" "+m.group(3)))
    return out[:10]
a, b = qs(card,"### Self-check"), qs(head,"### Self-check")
spec = open(r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/4-batch/2-actives/523-release-notes-kind-first-plain-text-amen/03-change-spec.md",encoding="utf-8").read()
c = qs(spec,'### "Self-check"')
print("questions", len(a), len(b), len(c))
for i,(x,y,z) in enumerate(zip(a,b,c),1):
    print(i, "card==guide" if x==y else "card!=guide", "| spec==guide" if y==z else "| spec!=guide")
    if x!=y: print("   card :",x); print("   guide:",y)
    if y!=z: print("   spec :",z)
def section(t, title):
    lines=t.splitlines(); i=lines.index(title); lvl=len(title.split()[0]); j=i+1; fence=False
    while j<len(lines):
        if lines[j].lstrip().startswith("```"): fence=not fence
        if not fence and re.match(r"#{1,%d} "%lvl, lines[j]): break
        j+=1
    return "\n".join(lines[i:j]).rstrip()
print("--- sections unchanged against origin/main")
for title in ["# Release process guidelines","## Rules of a release","## The release folder","## The steps of a release","## The version PR on top of a stack","## The version PR body","### Publishing","## Announcement thread","## Hero image"]:
    if title=="# Release process guidelines":
        s=lambda t:t[:t.index("## Rules of a release")]
        print(title, s(head)==s(base)); continue
    print(title, section(head,title)==section(base,title))
print("--- headings at head")
for n,l in enumerate(head.splitlines(),1):
    if re.match(r"#{1,4} ",l): print(n,l)
