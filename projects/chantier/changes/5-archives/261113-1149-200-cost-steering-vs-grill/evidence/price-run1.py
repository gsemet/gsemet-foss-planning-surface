import sys, pathlib
sys.path.insert(0, r"C:\Users\gaeta\Projets\chantier.worktrees\batch-15-CR-200\skills\chantier\scripts\cli\src")
from chantier import costs
p = pathlib.Path(sys.argv[1])
claim, close = "2026-11-12T19:42:38.695Z", "2026-11-12T20:12:39.287Z"
win = (claim, close)
for label, st in (("old rule (loose)", None), ("strict rule in the window", win)):
    u = costs.usage(p, claim, close, split=True, steering=st)
    g = u["grill"]
    print(f"{label}: row ${u['usd']:.3f} ({u['calls']} calls); grill ${g['usd']:.3f} ({g['calls']} calls); sum ${u['usd']+g['usd']:.3f}")
u = costs.usage(p, "2026-11-12T19:42:32.259Z", close, split=True, steering=win)
print(f"since open, strict inside window: row ${u['usd']:.3f} ({u['calls']}); grill ${u['grill']['usd']:.3f} ({u['grill']['calls']})")
