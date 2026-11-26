"""Print low-scoring inventory rows, with the best line elsewhere, for review by eye."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
W = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
rows = json.loads((HERE / "match.json").read_text(encoding="utf-8"))
inv_name, lo, hi, start, count = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
sel = [
    r for r in rows
    if r["inv"] == inv_name and r["files"] and r["kind"][:1] not in "bf" and lo <= r["home_score"] < hi
]
print(f"{len(sel)} rows; showing {start}..{start + count}")
cache = {}


def line(at):
    if not at:
        return ""
    f, n = at.rsplit(":", 1)
    body = cache.setdefault(f, (W / f).read_text(encoding="utf-8").split("\n"))
    return body[int(n) - 1]


for r in sel[start:start + count]:
    home = r["home"].replace("the rule it applies:", "rule:")
    print(f"{r['id']} [{r['home_score']:.2f}] H={home[:110]} | S={r['source']}")
    print(f"  B: {r['behaviour'][:260]}")
    if r["best_score"] > r["home_score"] + 0.12:
        at = r["best_at"]
        print(f"  ?{r['best_score']:.2f} {at}: {line(at)[:160]}")
