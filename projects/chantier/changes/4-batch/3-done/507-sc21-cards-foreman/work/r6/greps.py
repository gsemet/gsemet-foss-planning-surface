"""Read-only: every grep check of the inventories (this CR's four, CR-505's two) against cards-next,
now and at head; and every quoted home line of a closing list against the card's line."""

import re
import subprocess
from pathlib import Path

WT = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507"
CN = Path(WT) / "skills/chantier/cards-next"
BATCH = Path("C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch")
HERE = BATCH / "2-actives/507-sc21-cards-foreman/evidence"
SIB = BATCH / "3-done/505-sc19-cards-workers/evidence"

paths = sorted(HERE.glob("cards-inventory-*.md")) + sorted(SIB.glob("cards-inventory-*.md"))
cache: dict[tuple[str, str], str | None] = {}


def head_text(card: str) -> str | None:
    if ("head", card) not in cache:
        run = subprocess.run(
            ["git", "-C", WT, "show", f"HEAD:skills/chantier/cards-next/{card}"],
            capture_output=True,
        )
        cache[("head", card)] = run.stdout.decode("utf-8") if run.returncode == 0 else None
    return cache[("head", card)]


for path in paths:
    total, bad = 0, []
    for num, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for flags, phrase, card in re.findall(r"grep((?: -\w+)*) '([^']+)' ([\w./-]+\.md)", line):
            total += 1
            card = card.removeprefix("cards-next/")
            now = (CN / card).is_file() and phrase in (CN / card).read_text(encoding="utf-8")
            if not now:
                head = head_text(card)
                was = "at head: yes" if head is not None and phrase in head else "at head: no"
                row = line.split("|")[1].strip() if line.startswith("|") else "(prose)"
                bad.append(f"  {path.name}:{num} {row} {card} '{phrase}' ({was})")
    print(f"{path.parent.parent.name}/{path.name}: {total} grep checks, {len(bad)} not matching")
    for item in bad:
        print(item)
