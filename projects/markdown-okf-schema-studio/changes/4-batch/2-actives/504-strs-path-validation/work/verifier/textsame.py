"""Body and frontmatter differences of requirement files between two revisions, scenario ids ignored."""
import collections
import difflib
import re
import subprocess
import sys

REPO, BASE, HEAD = sys.argv[1:4]
sys.stdout.reconfigure(encoding="utf-8")
FILES = {
    "DIAG-009": "diagrams/SwRS-MDOKFSTUDIO-DIAG-009.md",
    "DIAG-121": "diagrams/SwRS-MDOKFSTUDIO-DIAG-121.md",
    "DIAG-123": "diagrams/SwRS-MDOKFSTUDIO-DIAG-123.md",
    "DIAG-128": "diagrams/SwRS-MDOKFSTUDIO-DIAG-128.md",
    "LAYOUT-023": "layout-width/SwRS-MDOKFSTUDIO-LAYOUT-023.md",
    "CORE-096": "rendering-core/SwRS-MDOKFSTUDIO-CORE-096.md",
}


def get(rev, f):
    return subprocess.run(["git", "-C", REPO, "show", f"{rev}:requirements/tiers/swrs/{f}"], capture_output=True, check=True).stdout.decode("utf-8").replace("\r\n", "\n")


for key, f in FILES.items():
    a, b = get(BASE, f), get(HEAD, f)
    af, ab = a.split("\n---\n", 1)
    bf, bb = b.split("\n---\n", 1)
    na = [re.sub(r"^(### Scenario) (?:S\d+ )?", r"\1 ", x) for x in ab.split("\n")]
    nb = [re.sub(r"^(### Scenario) (?:S\d+ )?", r"\1 ", x) for x in bb.split("\n")]
    d = [x for x in difflib.unified_diff(na, nb, n=0, lineterm="") if not x.startswith(("---", "+++", "@@"))]
    print(f"== {key}: body differences after ignoring scenario ids: {len(d)}")
    for x in d:
        print("  ", x[:220])
    ca = collections.Counter(x for x in na if x.strip())
    cb = collections.Counter(x for x in nb if x.strip())
    print("   same non-blank lines as a multiset (order ignored):", ca == cb, "only base:", [x[:200] for x in (ca - cb)], "only head:", [x[:200] for x in (cb - ca)])
    print("   base order:", [x[13:80] for x in na if x.startswith("### Scenario")])
    fd = [x for x in difflib.unified_diff(af.split("\n"), bf.split("\n"), n=0, lineterm="") if not x.startswith(("---", "+++", "@@"))]
    print("   frontmatter changes:")
    for x in fd:
        print("     ", x[:160])
    ha = [x for x in ab.split("\n") if x.startswith("### Scenario")]
    hb = [x for x in bb.split("\n") if x.startswith("### Scenario")]
    print("   headings base", len(ha), "head", len(hb))
    for x in hb:
        print("     ", x[:140])
