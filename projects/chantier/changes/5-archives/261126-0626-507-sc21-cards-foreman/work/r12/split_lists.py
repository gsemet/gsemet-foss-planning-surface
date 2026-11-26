"""Read-only: every "split into topics" list of the completeness table against r5/gen.py's rule.

Covers the families whose rows are tables with a source cell; a card read from the host-and-shared
family's own rows is marked, not judged.
"""

import json
import re
from pathlib import Path

EV = Path(__file__).resolve().parents[2] / "evidence"
CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
TOPICS = json.loads((CN / "topics.json").read_text(encoding="utf-8"))["topics"]
HOST = "cards-inventory-host-and-shared.md"

got: dict[str, set[str]] = {}
for path in EV.glob("cards-inventory-*.md"):
    if path.name == HOST:
        continue
    for line in path.read_text(encoding="utf-8").split("\n"):
        if not line.startswith("| "):
            continue
        c = [x.strip() for x in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(c) < 8:
            continue
        src = re.search(r"([A-Za-z-]+\.md)", c[4])
        if not src or "topic" not in c[6]:
            continue
        got.setdefault(src.group(1), set()).update(
            n for n in re.findall(r"[a-z0-9][a-z0-9-]*", c[6]) if n in TOPICS
        )
for line in (EV / HOST).read_text(encoding="utf-8").split("\n"):
    m = re.match(r"\| references/(\S+) \|.*split into topics (.*?) \|$", line)
    if not m:
        continue
    name = m.group(1).split("/")[-1]
    listed = set(m.group(2).split(", "))
    mine = "host-and-shared" in line.split("|")[2]
    gone = sorted(listed - got.get(name, set()))
    new = sorted(got.get(name, set()) - listed)
    if gone or new:
        print(name, "(host-and-shared too)" if mine else "", "listed only:", gone, "rows only:", new)
