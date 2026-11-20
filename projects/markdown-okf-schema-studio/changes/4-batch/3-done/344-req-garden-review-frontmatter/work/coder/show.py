import sys, pathlib, re
root = pathlib.Path("requirements/tiers/swrs")
for i in sys.argv[1:]:
    p = next(root.glob(f"*/SwRS-MDOKFSTUDIO-{i}.md"))
    t = p.read_text(encoding="utf-8").replace("\r\n","\n")
    t = re.sub(r"^(implemented_in_files|tested_in_files):\n(- .*\n)+", "", t, flags=re.M)
    t = re.sub(r"<!-- okf:links:start -->.*", "", t, flags=re.S)
    t = re.sub(r"^(uuid|project|status|origin|tier|annotation_exemption|exemption_reason|default_owner_email):.*\n", "", t, flags=re.M)
    print("=====", p); print(t)
