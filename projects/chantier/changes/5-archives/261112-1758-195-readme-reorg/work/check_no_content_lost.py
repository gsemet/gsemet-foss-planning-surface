import subprocess, pathlib, sys
root = pathlib.Path(sys.argv[1])
base = subprocess.run(["git","show","origin/main:README.md"],cwd=root,capture_output=True,check=True).stdout.decode("utf-8").split("\n")
removed = [l for l in base[230:491] if l.strip()]
pages = "".join((root/"docs"/n).read_text(encoding="utf-8")+"\n" for n in ["boards.md","gates.md","agents-and-models.md","planning-folder.md","hosts.md","costs.md"])
plines = {l.rstrip() for l in pages.split("\n")}
rw=[("](#the-remote-board)","](boards.md#the-remote-board)"),("](#batch-modes)","](../README.md#batch-modes)")]
def norm(l):
    l=l.rstrip()
    for a,b in rw: l=l.replace(a,b)
    return l
plines_n = plines | {l.lstrip("#").strip() for l in plines}
miss=[l for l in removed if norm(l) not in plines and norm(l)[1:] not in plines and norm(l) not in plines_n]
# headings lowered by one are allowed
miss=[l for l in miss if not (l.startswith("### ") and l[1:] in plines)]
print(len(removed),"non-blank lines checked;",len(miss),"missing")
for m in miss: print("MISSING:",m)
sys.exit(1 if miss else 0)
