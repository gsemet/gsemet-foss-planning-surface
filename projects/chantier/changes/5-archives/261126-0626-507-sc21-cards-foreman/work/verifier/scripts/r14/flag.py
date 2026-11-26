"""Verifier: every row round 10's audit script still flags at this head is among the rows the
hand-read records name (work/r10/chunks, work/r10/rest, plus the three the round note names)."""

import re
import sys
from pathlib import Path

CR = Path("<CR folder>")
R10 = CR / "work/r10"
sys.dont_write_bytecode = True
sys.path.insert(0, str(R10))
import audit  # noqa: E402

ID = r"(?:FM-B?\d+|[A-Z]+-[A-Z]?\d+)"
ROW = re.compile(rf"^({ID})(?: \(\+[^)]*\))?(?::| \[)")

idf, top = audit.idf_table()
cache, flagged, total, textual = {}, [], 0, []
for inv, r, path, seg in audit.segments():
    total += 1
    files = audit.home_files(r["new home"])
    if not files:
        continue
    textual.append(r["id"])
    score, lost, bad = audit.check(seg, files, idf, top, cache)
    if score >= 0.1:
        flagged.append(r["id"])
print("rows", total, "text home", len(textual), "flagged", len(flagged))

read = set()
for d in ("chunks", "rest"):
    ids = set()
    for f in sorted((R10 / d).glob("*.txt")):
        if f.name == "index.txt":
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            m = ROW.match(line)
            if m:
                ids.add(m[1])
    if d == "chunks":
        index = (R10 / "chunks/index.txt").read_text(encoding="utf-8").splitlines()
        ix = {line.split()[1] for line in index if line.strip()}
        print("chunks/index.txt ids", len(ix), "of which in chunk text", len(ix & ids), "text-only", len(ids - ix))
        ids |= ix
    print(d, "row ids", len(ids))
    read |= ids
named = {"C-1032", "FM-B045", "H-120"}
all_read = read | named
print("read-record ids", len(read), "with the three named", len(all_read))
miss = sorted(set(flagged) - all_read)
print("flagged at head and in no hand-read record:", len(miss), miss[:80])
print("text-home rows in a read record:", len(set(textual) & all_read))
