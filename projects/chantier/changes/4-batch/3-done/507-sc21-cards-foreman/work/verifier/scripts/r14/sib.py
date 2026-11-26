"""Verifier: every `file line` of the body's edited-lines table is in the host inventory's
sibling-card table, and the reverse."""
import re, runpy, sys
from pathlib import Path
here = Path(__file__).parent
g = runpy.run_path(str(here / "table.py"), run_name="t")
listed, CR, head_tree = g["listed"], g["CR"], g["head_tree"]
inv = (CR / "evidence/cards-inventory-host-and-shared.md").read_text(encoding="utf-8").split("\n")
a = inv.index("## Sibling-card edits")
b = next(i for i in range(a + 1, len(inv)) if inv[i].startswith("## "))
sib = {}
for row in inv[a:b]:
    if not row.startswith("| ") or row.startswith(("| file:line", "| ---")):
        continue
    cell = row.split("|")[1].strip()
    for m in re.finditer(r"(?P<f>[\w./-]+\.(?:md|json)):(?P<n>\d+(?:-\d+)?(?:,\s*\d+(?:-\d+)?)*)", cell):
        ns = g["numbers"](m["n"])
        sib.setdefault(m["f"], set()).update(ns)
miss = {f: sorted(ns - sib.get(f, set())) for f, ns in listed.items() if ns - sib.get(f, set())}
extra = {f: sorted(ns - listed.get(f, set())) for f, ns in sib.items() if ns - listed.get(f, set())}
print("SIB files", len(sib), "listed in body not in sibling table:", miss)
print("SIB in sibling table not in body:", extra)
