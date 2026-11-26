"""Verifier r15: rows whose behaviour matches a pattern, with their quiz / child 25 marks.

Usage: python find.py <CR folder> <name> <regex> [<name> <regex> ...]
"""
import re
import sys
from pathlib import Path

SPLIT = re.compile(r"(?<!\\)\|")
ID = re.compile(r"^(?:FM-B?\d{3}|[A-Z]{1,3}-\d{3,4})$")
cr = Path(sys.argv[1])
rows = []
for f in sorted((cr / "evidence").glob("cards-inventory-*.md")):
    for line in f.read_text(encoding="utf-8").split("\n"):
        c = [x.strip() for x in SPLIT.split(line.strip().strip("|"))]
        if line.startswith("|") and len(c) == 8 and ID.match(c[0]):
            rows.append(c)
pairs = sys.argv[2:]
for name, pat in zip(pairs[::2], pairs[1::2]):
    rx = re.compile(pat, re.I)
    print(f"##### {name}: /{pat}/")
    for c in rows:
        if rx.search(c[3]):
            marks = re.findall(r"(quiz [A-Za-z0-9-]+|child 25: [^;|]+)", c[7])
            print(f"  {c[0]} {marks} :: {c[3][:230]}")
