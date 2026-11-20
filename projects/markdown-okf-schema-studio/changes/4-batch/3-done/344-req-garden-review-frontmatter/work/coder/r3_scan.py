import sys, re, json, pathlib, subprocess
from ruamel.yaml import YAML
SC = ["review-annotations","frontmatter-editing","frontmatter-schema"]
root = pathlib.Path("requirements/tiers")
def fm(p):
    t = p.read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
    end = t[1:].index("---")+1
    return YAML(typ="safe").load("\n".join(t[1:end]))
reqs = {}
for tier in ("strs","swrs"):
    for sc in SC:
        for p in sorted((root/tier/sc).glob("*.md")):
            if p.name=="index.md": continue
            d = fm(p); reqs[d["id"]] = d
MK = re.compile(r'^\s*(?:(?:#|//|/\*|\*|<!--)\s*)?(@implements_req|@tests_req)\s+([A-Za-z][A-Za-z0-9_-]*)')
def classify(line):
    if MK.match(line): return "marker"
    t=line.strip()
    if t=="": return "blank"
    if re.match(r'^(//|#|/\*|\*|<!--)',t) or t.endswith("*/") or t.endswith("-->"): return "comment"
    return "code"
files = subprocess.check_output(["git","ls-files","src","test"],text=True).split("\n")
marks = {}  # id -> list of (kind,file,line,blocksize)
blocks_over = []
for f in files:
    if not f or not re.search(r'\.(ts|tsx|mjs|js|py|md)$',f): continue
    try: lines = pathlib.Path(f).read_text(encoding="utf-8").replace("\r","").split("\n")
    except Exception: continue
    cur=None; blocks=[]
    for i,l in enumerate(lines):
        k=classify(l)
        if k=="code": cur=None
        elif k=="marker":
            if cur is None: cur={"ms":[]}; blocks.append(cur)
            m=MK.match(l); cur["ms"].append((m.group(1),m.group(2),i+1))
    for b in blocks:
        ids={x[1] for x in b["ms"]}
        for kind,id_,ln in b["ms"]:
            marks.setdefault(id_,[]).append((kind,f,ln,len(ids)))
        if len(ids)>3: blocks_over.append((f,b["ms"][0][2],len(ids),sorted(ids)))
out={"reqs":reqs,"marks":marks,"over":blocks_over}
if __name__=="__main__":
    mode=sys.argv[1]
    inforce=lambda d: d["req_lifecycle"] in ("draft","proposed","approved")
    if mode=="gaps":
        for id_,d in reqs.items():
            if "SwRS" in id_ and inforce(d):
                ms=marks.get(id_,[])
                imp=[m for m in ms if m[0]=="@implements_req" and m[1].startswith("src/")]
                tst=[m for m in ms if m[0]=="@tests_req" and m[3]<=3 and m[1].startswith("test/")]
                exempt=d.get("annotation_exemption")
                if (not imp and not exempt) or not tst:
                    print(id_.replace("SwRS-MDOKFSTUDIO-",""), "imp",len(imp), "tst",len(tst), "ex",exempt, "| all tests:", [(m[1].split('/')[-1],m[2],m[3]) for m in ms if m[0]=="@tests_req"][:4])
    if mode=="stale":
        for id_,ms in marks.items():
            if id_ in reqs and not inforce(reqs[id_]): print(id_, [(m[0][1:3],m[1],m[2]) for m in ms])
    if mode=="over":
        for b in blocks_over:
            if any(x.split("-MDOKFSTUDIO-")[-1].split("-")[0] in ("REVIEW","FMEDIT","FMSCHEMA") for x in b[3]) or True: print(b[0],b[1],b[2],[x.replace("MDOKFSTUDIO-","") for x in b[3] if re.match(r'(Sw|St)RS-MDOKFSTUDIO-(REVIEW|FMEDIT|FMSCHEMA)',x)])
    if mode=="id":
        for i in sys.argv[2:]:
            print(i,[(m[0][1:3],m[1],m[2],m[3]) for m in marks.get("SwRS-MDOKFSTUDIO-"+i,marks.get("StRS-MDOKFSTUDIO-"+i,[]))])
