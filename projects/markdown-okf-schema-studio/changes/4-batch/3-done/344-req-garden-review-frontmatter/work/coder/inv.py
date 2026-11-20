import sys, pathlib
from ruamel.yaml import YAML
root = pathlib.Path("requirements/tiers")
def fm(p):
    t = p.read_text(encoding="utf-8").replace("\r\n","\n").split("\n")
    end = t[1:].index("---")+1
    return YAML(typ="safe").load("\n".join(t[1:end]))
scopes = sys.argv[1].split(",")
tier = sys.argv[2]
for sc in scopes:
    for p in sorted((root/tier/sc).glob("*.md")):
        if p.name=="index.md": continue
        d = fm(p)
        if d["req_lifecycle"] in ("superseded","deprecated") and "all" not in sys.argv: continue
        pre = lambda l: [x.replace("StRS-MDOKFSTUDIO-","S:").replace("SwRS-MDOKFSTUDIO-","") for x in (l or [])]
        print(d["id"].replace("SwRS-MDOKFSTUDIO-","").replace("StRS-MDOKFSTUDIO-",""), d["req_lifecycle"][:4], "|", d["title"][:60], "| df:", ",".join(pre(d.get("derives_from"))), "| dep:", ",".join(pre(d.get("depends_on"))), "| rel:", ",".join(pre(d.get("relates_to"))))
