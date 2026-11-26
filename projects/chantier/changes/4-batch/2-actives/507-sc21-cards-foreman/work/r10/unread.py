"""Round 10, last check: the rows the audit flags now that are in no review chunk, and the totals."""

import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from audit import check, idf_table, segments  # noqa: E402
from inv import home_files  # noqa: E402

read = {line.split()[1] for line in (HERE / "chunks/index.txt").read_text(encoding="utf-8").splitlines()}
for f in sorted((HERE / "rest").glob("*.txt")):
    for line in f.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("  ") and " -> " in line:
            read.add(line.split()[0])
idf, top = idf_table()
cache = {}
total = textual = flagged = flagged_read = textual_read = 0
new = []
for inv, r, path, seg in segments():
    total += 1
    files = home_files(r["new home"])
    if not files:
        continue
    textual += 1
    textual_read += r["id"] in read
    score = check(seg, files, idf, top, cache)[0]
    if score >= 0.1:
        flagged += 1
        if r["id"] in read:
            flagged_read += 1
        else:
            new.append((r["id"], score, r["new home"]))
print(f"rows {total}; with a text home {textual}; of them in a review chunk {textual_read}; flagged now {flagged}; "
      f"flagged and in a chunk {flagged_read}; flagged and in no chunk {len(new)}")
for row in new:
    print(*row)
