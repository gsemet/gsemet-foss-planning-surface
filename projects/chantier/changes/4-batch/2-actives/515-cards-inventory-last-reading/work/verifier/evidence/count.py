import sys,re,collections
S,F=sys.argv[1],sys.argv[2]
rows=[l.rstrip("\n").split("\t") for l in open(S+"/open.tsv",encoding="utf-8")][1:]
kind={r[0]:r[1] for r in rows}
print("rows",len(rows),"unique",len(kind),dict(sorted(collections.Counter(kind.values()).items())))
body=open(F+"/pr-body.md",encoding="utf-8").read()
sec=body.split("### The last reading of the open rows")[1].split("### Homes kept")[0]
lines=re.findall(r"^- ([A-Z]+-[A-Z]?\d+): ",sec,re.M)
print("pr lines",len(lines),"unique",len(set(lines)))
print("not open:",[i for i in lines if i not in kind])
print("per kind",dict(sorted(collections.Counter(kind.get(i) for i in lines).items())))
open(S+"/listed.txt","w").write("\n".join(lines))
