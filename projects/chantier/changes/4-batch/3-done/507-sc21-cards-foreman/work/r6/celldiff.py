"""Compare, cell by cell, the Allow rules tables of the host reference with the round-5 backup."""

import re
import sys
from pathlib import Path

old = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
new = Path(sys.argv[2]).read_text(encoding="utf-8").splitlines()


def rows(lines):
    return {
        i + 1: [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]
        for i, line in enumerate(lines)
        if line.startswith("|")
    }


def keyed(table):
    return {cells[0]: (n, cells) for n, cells in table.items()}


o, n = keyed(rows(old)), keyed(rows(new))
for key, (num, cells) in n.items():
    if key not in o:
        print(f"new:{num} no old row: {key[:80]}")
        continue
    onum, ocells = o[key]
    for k, (a, b) in enumerate(zip(ocells, cells)):
        if a != b:
            print(f"--- new:{num} old:{onum} cell {k + 1}/{len(cells)} [{key[:60]}]")
            if len(sys.argv) > 3 and num >= int(sys.argv[3]):
                print(f"  OLD({len(a)}): {a}")
                print(f"  NEW({len(b)}): {b}")
