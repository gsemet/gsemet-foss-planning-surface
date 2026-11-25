"""Read-only: the grep checks of 505's two inventories against cards-next, now and at head."""

import re
import subprocess
from pathlib import Path

WT = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507"
CN = Path(WT) / "skills/chantier/cards-next"
EV = Path("C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/"
          "3-done/505-sc19-cards-workers/evidence")
for name in ("workers", "drivers"):
    text = (EV / f"cards-inventory-{name}.md").read_text(encoding="utf-8")
    greps = sorted(set(re.findall(r"grep(?: -\w+)* '([^']+)' ([\w./-]+\.md)", text)))
    broke = []
    for phrase, card in greps:
        now = (CN / card).is_file() and phrase in (CN / card).read_text(encoding="utf-8")
        run = subprocess.run(["git", "-C", WT, "show", f"HEAD:skills/chantier/cards-next/{card}"], capture_output=True)
        head = run.returncode == 0 and phrase in run.stdout.decode("utf-8")
        if head and not now:
            broke.append((phrase, card))
    print(name, "grep checks:", len(greps), "matching at head and no longer:", broke or "none")
