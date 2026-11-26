import re
import sys
from collections import Counter
from pathlib import Path

wt = Path(sys.argv[1])
mode = sys.argv[2]


def cells(line):
    parts = re.split(r"(?<!\\)\|", line.strip()[1:-1])
    return [p.strip().replace("\\|", "|") for p in parts]


rows = []
section = None
for line in (wt / "docs/proofs/cards-inventory.md").read_text("utf-8").splitlines():
    if line.startswith("## "):
        section = line[3:]
    elif section == "Rows" and line.startswith("|"):
        rows.append(cells(line))
rows = rows[2:]
opened = {x.split("\t")[0]: x.split("\t") for x in
          (wt / "docs/proofs/cards-inventory-open.tsv").read_text("utf-8").splitlines()[1:]}

if mode == "counts":
    print("rows", len(rows), "open tsv", len(opened))
    print("kinds", sorted(Counter(r[5] for r in rows).items()))
    o = [r for r in rows if r[6].startswith("open: ")]
    print("open rows", len(o), sorted(Counter(r[5] for r in o).items()))
    print("open inferable", sum("inferable" in opened[r[0]][2] for r in o))
    print("homes", Counter(r[6].split(" ")[0] for r in rows).most_common())
    print("checks", Counter(r[7].split(" ")[0] for r in rows).most_common())
    print("rare", sum(r[2] == "none (rare)" for r in rows))
elif mode in ("opena", "openo"):
    for r in rows:
        if not r[6].startswith("open: "):
            continue
        if (r[5] == "a") != (mode == "opena"):
            continue
        extra = ""
        if len(sys.argv) > 3:
            lo, hi = int(sys.argv[3]), int(sys.argv[4])
            i = [x[0] for x in rows if x[6].startswith("open: ") and (x[5] == "a") == (mode == "opena")].index(r[0])
            if not lo <= i < hi:
                continue
        src = r[4].replace("skills/chantier/references/", "R/")
        print(f"{r[0]} [{r[5]}] {r[1]} | {r[2]} | {r[3]} | {src} | {r[6]}")
elif mode == "ids":
    want = sys.argv[3].split(",")
    for r in rows:
        if r[0] in want:
            src = r[4].replace("skills/chantier/references/", "R/")
            print(f"{r[0]} [{r[5]}] {r[1]} | {r[2]} | {r[3]} | {src} | {r[6]} | {r[7]}")
