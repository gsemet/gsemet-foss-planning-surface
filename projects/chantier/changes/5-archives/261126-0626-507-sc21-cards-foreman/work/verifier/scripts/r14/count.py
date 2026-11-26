"""Verifier: how many distinct rule rows the four inventories hold, and what the body counts."""

import collections
import sys
from pathlib import Path

sys.dont_write_bytecode = True
CR = Path("<CR folder>")
sys.path.insert(0, str(CR / "work/r10"))
import audit  # noqa: E402
import inv  # noqa: E402

rows = list(inv.rows())
ids = collections.Counter(r["id"] for _, _, r in rows)
print("table rows parsed", len(rows), "distinct ids", len(ids))
dups = [i for i, v in ids.items() if v > 1]
print("ids met more than once", len(dups), dups[:4], "...", dups[-4:])
per = collections.Counter((name, len(r)) for name, _, r in rows)
print("rows by (file, columns)", dict(per))
extra = [(name, n, r["id"], len(r)) for name, n, r in rows if len(r) != 8]
if extra:
    print("non-8-column rows span lines", extra[0][1], "to", extra[-1][1], "in", sorted({e[0] for e in extra}))

main = [(name, n, r) for name, n, r in rows if len(r) == 8]
text_all, text_main = [], []
for inv_name, r, path, seg in audit.segments():
    if audit.home_files(r["new home"]):
        text_all.append((r["id"], len(r)))
print("audit segments with a text home", len(text_all), "distinct", len({i for i, _ in text_all}),
      "of which 8-column", sum(1 for _, k in text_all if k == 8))
