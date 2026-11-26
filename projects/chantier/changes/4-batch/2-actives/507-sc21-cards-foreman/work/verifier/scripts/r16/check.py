"""Recount the cases the inventories name, and read the check cells the posted gap names."""

import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
cr, wt = Path(sys.argv[1]), Path(sys.argv[2])
split = re.compile(r"(?<!\\)\|")
row_id = re.compile(r"^(?:FM-B?\d{3}|[A-Z]{1,3}-\d{3,4})$")
cases = {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in sorted((wt / "evals/quiz").glob("*/*.json"))}
rows = {}
named = {}
for name in ["chief-of-staff", "foreman", "griller", "host-and-shared"]:
    for line in (cr / "evidence" / f"cards-inventory-{name}.md").read_text(encoding="utf-8").split("\n"):
        cell = [x.strip() for x in split.split(line.strip().strip("|"))]
        if not (line.startswith("|") and len(cell) == 8 and row_id.match(cell[0])):
            continue
        rows[cell[0]] = cell
        for case in re.findall(r"\bquiz ([A-Za-z0-9-]+)", cell[7]):
            named.setdefault(case, set()).add(cell[0])
print("rows", len(rows))
print("quiz cases", len(cases), "named", len(set(named) & set(cases)), "unknown", sorted(set(named) - set(cases)))
print("distinct rows naming a quiz case", len(set().union(*named.values())))
unnamed = sorted(set(cases) - set(named))
print("named in no row's check", len(unnamed), unnamed)
for ident in ["H-412", "H-1566", "C-732", "C-045", "H-1026", "C-576"]:
    print(ident, "|", rows[ident][3], "| check:", rows[ident][7])
for case in [
    "floor-1-chief-of-staff-merge",
    "floor-3-chief-of-staff-missing-agent",
    "J29-chief-of-staff-turn-notice",
    "a8-push-refused-default-branch",
]:
    print(case, "named on", sorted(named[case]))
