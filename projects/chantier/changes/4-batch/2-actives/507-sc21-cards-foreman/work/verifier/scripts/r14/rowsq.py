"""Verifier: show inventory rows by id, or rows whose behaviour matches a pattern."""

import collections
import re
import sys
from pathlib import Path

CR = Path("<CR folder>")
SPLIT = re.compile(r"(?<!\\)\|")
ID = re.compile(r"^(?:FM-B?\d{3}|[A-Z]{1,3}-\d{3,4})$")


def rows():
    for f in sorted((CR / "evidence").glob("cards-inventory-*.md")):
        for n, line in enumerate(f.read_text(encoding="utf-8").split("\n"), 1):
            c = [x.strip() for x in SPLIT.split(line.strip().strip("|"))]
            if len(c) == 8 and ID.match(c[0]):
                yield f.stem.removeprefix("cards-inventory-"), n, c


def show(f, n, c, width):
    print(f"{c[0]} ({f}:{n}) kind={c[5]}")
    print(f"   source: {c[1][:width]} | {c[2][:width]}")
    print(f"   behaviour: {c[3][:width]}")
    print(f"   col5: {c[4][:width]}")
    print(f"   home: {c[6][:width]}")
    print(f"   check: {c[7][:width]}")


mode = sys.argv[1]
if mode == "id":
    want = set(sys.argv[2:])
    for f, n, c in rows():
        if c[0] in want:
            show(f, n, c, 600)
elif mode == "re":
    pat = re.compile(sys.argv[2], re.I)
    for f, n, c in rows():
        if pat.search(c[3]) or pat.search(c[2]):
            print(f"{c[0]} k={c[5]} check={c[7][:70]!r} :: {c[3][:150]} -> {c[6][:70]}")
elif mode == "checks":
    all_rows = list(rows())
    print("rows", len(all_rows))
    c25 = [c for _, _, c in all_rows if "child 25" in c[7].lower()]
    print("rows whose check says child 25:", len(c25), [c[0] for c in c25][:40])
    cnt = collections.Counter(re.sub(r"\d+", "#", c[7])[:50] for _, _, c in all_rows)
    for k, v in cnt.most_common(8):
        print("  ", v, k)
    print("header lines:")
    for f in sorted((CR / "evidence").glob("cards-inventory-*.md")):
        for line in f.read_text(encoding="utf-8").split("\n"):
            if line.startswith("|") and "check" in line.lower() and "kind" in line.lower():
                print("  ", f.name, line[:200])
                break
