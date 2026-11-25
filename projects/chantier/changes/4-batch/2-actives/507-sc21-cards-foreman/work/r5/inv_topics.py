"""Every topic an inventory of this CR names exists in the final cards-next/topics.json."""

import json
import re
from pathlib import Path

CR = Path("C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/"
          "2-actives/507-sc21-cards-foreman")
CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
data = json.loads((CN / "topics.json").read_text(encoding="utf-8"))
topics = data.get("topics", data)
for path in sorted((CR / "evidence").glob("cards-inventory-*.md")):
    named = {}
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        cells = re.split(r"(?<!\\)\|", line)
        if len(cells) < 10 or not re.fullmatch(r"\s*[A-Z]+-[A-Z]?\d+\s*", cells[1]):
            continue
        home, check = cells[7], cells[8]
        for name in re.findall(r"\btopic `?([a-z][a-z0-9-]+)`?", home) + re.findall(r"\bhelp ([a-z][a-z0-9-]+)", check):
            named.setdefault(name, n)
    missing = {k: v for k, v in named.items() if k not in topics}
    print(path.name, "topics named:", len(named), "missing:", missing or "none")
