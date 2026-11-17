import sys, re, pathlib
root = pathlib.Path("requirements/tiers/swrs")
for i in sys.argv[1:]:
    p = next(root.glob(f"*/SwRS-MDOKFSTUDIO-{i}.md"))
    t = p.read_text(encoding="utf-8").replace("\r\n","\n")
    fm = t.split("---\n")[1]
    keep = re.search(r"^title:.*(?:\n  .*)*", fm, re.M).group(0) + "\n" + re.search(r"^description:.*(?:\n  .*)*", fm, re.M).group(0)
    print("=====", i); print(keep)
    for k in ("derives_from","depends_on","relates_to"):
        m = re.search(r"^"+k+r":.*\n(?:- .*\n)*", fm, re.M)
        if m: print(m.group(0).strip().replace("\n"," "))
    print("\n".join(l for l in t.splitlines() if l.startswith("### ") ))
    m = re.search(r"### Related requirements\n(.*?)\n###", t, re.S)
    if m: print("REL:", m.group(1).strip())
