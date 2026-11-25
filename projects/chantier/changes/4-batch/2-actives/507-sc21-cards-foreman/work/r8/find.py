"""For given row ids, print the full row, its home files and the closest lines of the whole new set."""
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import match  # noqa: E402

rows = {r["id"]: r for r in match.run()}
for rid in sys.argv[1:]:
    r = rows.get(rid)
    if not r:
        print(rid, "not found")
        continue
    want = set(match.toks(r["behaviour"]))
    print(f"== {rid} [{r['home_score']}] home={r['home']}")
    print(f"   {r['behaviour']}")
    ranked = sorted(((match.score(want, t), f, i) for f, i, t in match.units), reverse=True)[:4]
    for s, f, i in ranked:
        mark = "*" if f in r["files"] else " "
        print(f"  {mark}{s:.2f} {f}:{i}: {match.files[f][i - 1][:420]}")
