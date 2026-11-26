"""Verifier: the Known gap's row figures counted on distinct rows, with the author's own read set."""

import collections
import sys
from pathlib import Path

sys.dont_write_bytecode = True
CR = Path("<CR folder>")
R10 = CR / "work/r10"
sys.path.insert(0, str(R10))
import audit  # noqa: E402
import inv  # noqa: E402

# the read set exactly as work/r10/unread.py builds it, plus the three rows its output names
read = {line.split()[1] for line in (R10 / "chunks/index.txt").read_text(encoding="utf-8").splitlines()}
for f in sorted((R10 / "rest").glob("*.txt")):
    for line in f.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("  ") and " -> " in line:
            read.add(line.split()[0])
named = {"C-1032", "FM-B045", "H-120"}
all_rows = list(inv.rows())
main = [r for _, _, r in all_rows if len(r) == 8]
relisted = [r for _, _, r in all_rows if len(r) != 8]
print("parsed rows", len(all_rows), "| rule rows (8 columns)", len(main), "distinct", len({r["id"] for r in main}),
      "| relisted in a closing list", len(relisted))
text_rows = [r for r in main if inv.home_files(r["new home"])]
text_ids = {r["id"] for r in text_rows}
print("rule rows with a text home", len(text_rows), "distinct", len(text_ids))
print("relisted rows with a text home", sum(1 for r in relisted if inv.home_files(r["new home"])))
for label, s in (("author read set", read), ("author read set + 3 named", read | named)):
    hit = text_ids & s
    print(f"{label}: ids {len(s)}; text-home rule rows among them {len(hit)}; text-home rule rows not read {len(text_ids - s)}")
idf, top = audit.idf_table()
cache, flagged = {}, set()
for name, r, path, seg in audit.segments():
    files = audit.home_files(r["new home"])
    if files and len(r) == 8 and audit.check(seg, files, idf, top, cache)[0] >= 0.1:
        flagged.add(r["id"])
print("rule rows flagged now", len(flagged), "| flagged and outside read+named", sorted(flagged - read - named))
