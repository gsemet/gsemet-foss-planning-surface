import sys,re,glob
for a in sys.argv[1:]:
    p=glob.glob(("requirements/tiers/strs/*/StRS-MDOKFSTUDIO-"+a[3:] if a.startswith("st:") else "requirements/tiers/swrs/*/SwRS-MDOKFSTUDIO-"+a)+".md")[0]
    t=open(p,encoding="utf-8").read()
    fm,body=t.split("\n---\n",1)
    keep=[l for l in fm.split("\n") if re.match(r"(id|title|req_lifecycle|approved_by|annotation_exemption):",l)]
    def lst(k):
        m=re.search(rf"^{k}:\s*(\[\])?\n?((?:- .*\n?)*)",fm,re.M)
        return [x[2:].replace("MDOKFSTUDIO-","") for x in m.group(2).split("\n") if x] if m else []
    print("=====",p.split("/")[-1], "|", [k for k in keep if k.startswith(("req_","approved","annot"))])
    print("derives_from",lst("derives_from"),"depends_on",lst("depends_on"),"relates_to",lst("relates_to"))
    body=body.split("<!-- okf:links:start -->")[0]
    print(body.strip())
