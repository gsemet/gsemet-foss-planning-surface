"""claude-code.md against the round-5 copy: the fenced blocks, and the changed lines outside tables."""

import difflib
import re
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
CARD = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next/hosts/claude-code.md")
a = (HERE / "r5/claude-code.before.md").read_text(encoding="utf-8").replace("\r\n", "\n")
b = CARD.read_text(encoding="utf-8").replace("\r\n", "\n")
fa, fb = (re.findall(r"(?ms)^```.*?^```", t) for t in (a, b))
print("fenced blocks:", len(fa), len(fb), "equal:", fa == fb)
for line in difflib.unified_diff(a.split("\n"), b.split("\n"), n=0, lineterm=""):
    if line[:1] in "+-" and not line[1:].startswith("|"):
        print(line[:200])
print("bytes before", len(a.encode()), "now", len(b.encode()))
