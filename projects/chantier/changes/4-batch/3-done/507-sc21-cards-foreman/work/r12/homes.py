"""Read-only: each inventory row of "completeness" for one source card, against r5/gen.py's rule."""

import json
import re
from pathlib import Path

EV = Path(__file__).resolve().parents[2] / "evidence"
CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
SOURCE = "chief-of-staff-merge.md"
TOPICS = json.loads((CN / "topics.json").read_text(encoding="utf-8"))["topics"]

got: dict[str, list[str]] = {}
for path in EV.glob("cards-inventory-*.md"):
    if path.name == "cards-inventory-host-and-shared.md":
        continue  # r5/gen.py reads that family from its own rows, the others by cell
    for line in path.read_text(encoding="utf-8").split("\n"):
        if not line.startswith("| "):
            continue
        c = [x.strip() for x in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(c) < 8:
            continue
        src = re.search(r"([A-Za-z-]+\.md)", c[4])
        if not src or src.group(1) != SOURCE:
            continue
        for name in re.findall(r"[a-z0-9][a-z0-9-]*", c[6]):
            if name in TOPICS and re.search(r"topic", c[6]):
                got.setdefault(name, []).append(c[0])
text = (EV / "cards-inventory-host-and-shared.md").read_text(encoding="utf-8")
row = next(t for t in text.split("\n") if t.startswith(f"| references/{SOURCE} "))
listed = row.split("split into topics ", 1)[1].split(" |")[0].split(", ")
for topic in sorted(got):
    print(topic, len(got[topic]), got[topic][:4])
print("listed, not from a row:", sorted(set(listed) - set(got)))
print("from a row, not listed:", sorted(set(got) - set(listed)))
