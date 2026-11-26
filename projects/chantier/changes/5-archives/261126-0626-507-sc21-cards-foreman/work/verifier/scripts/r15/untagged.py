"""Verifier r15: inventory rows an existing quiz case tests, with the row's check, beside the case.

Usage: python untagged.py <CR folder> <worktree>
"""
import json
import re
import sys
from pathlib import Path

SPLIT = re.compile(r"(?<!\\)\|")
cr, wt = Path(sys.argv[1]), Path(sys.argv[2])
rows = {}
for f in sorted((cr / "evidence").glob("cards-inventory-*.md")):
    for line in f.read_text(encoding="utf-8").split("\n"):
        c = [x.strip() for x in SPLIT.split(line.strip().strip("|"))]
        if line.startswith("|") and len(c) == 8:
            rows[c[0]] = c
cases = {p.stem: p for p in wt.glob("evals/quiz/*/*.json")}
PAIRS = [
    ("floor-1-chief-of-staff-merge", ["H-412", "C-732", "H-1566"], ["H-399", "H-400", "H-414", "H-422"]),
    ("J29-chief-of-staff-turn-notice", ["H-1026"], ["H-766", "H-1027"]),
    ("floor-3-chief-of-staff-missing-agent", ["C-045"], ["C-044"]),
    ("a8-push-refused-default-branch", ["C-576"], ["FM-545"]),
]


def show(row_id):
    c = rows[row_id]
    named = re.findall(r"\bquiz ([A-Za-z0-9-]+)", c[7])
    print(f"  {row_id} names {named or 'no case'}; child 25: {'child 25' in c[7]}")
    print(f"      behaviour: {c[3]}")
    print(f"      check: {c[7]}")


for case, unnamed, siblings in PAIRS:
    path = cases[case]
    d = json.loads(path.read_text(encoding="utf-8"))
    print(f"== {path.parent.name}/{case} {d['rules']}")
    print(f"  situation: {d['situation']}")
    print(f"  expected: {d['expected']}")
    print(" rows that do not name it:")
    for r in unnamed:
        show(r)
    print(" comparison rows:")
    for r in siblings:
        show(r)
