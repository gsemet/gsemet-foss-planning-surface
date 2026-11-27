import sys,re
S=sys.argv[1]
kind={r.split("\t")[0]:r.split("\t")[1] for r in open(S+"/open.tsv",encoding="utf-8").read().splitlines()[1:]}
listed=set(open(S+"/listed.txt").read().split())
out=[]
for l in open(S+"/inventory.md",encoding="utf-8").read().split("## Rows")[1].split("## No-rule lines")[0].splitlines():
    c=[x.strip() for x in l.replace(chr(92)+"|",chr(1)).split("|")][1:-1]
    if c and c[0] in kind and c[0] not in listed:
        out.append(f"{c[0]} {kind[c[0]]} [{c[2][:50]}] {c[3][:260]}")
open(S+"/unlisted.txt","w",encoding="utf-8").write("\n".join(out))
print(len(out),sum(map(len,out)))
