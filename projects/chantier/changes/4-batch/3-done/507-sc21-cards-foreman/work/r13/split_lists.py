"""The completeness table's "split into topics" lists against the row homes of every inventory.

Reads the five family inventories (r5/gen.py's FAMILIES) and the host-and-shared rows (H-...).
A row's topics: the names its home cell gives after `topic` or `topics` that topics.json holds
(r5/gen.py's rule took every topics.json name anywhere in such a cell, so `release.py` or
`--direct` counted as topics `release` and `direct`). Prints each stale list; with --write, rewrites the lists in place.
"""

import collections
import json
import re
import sys
from pathlib import Path

CR = Path(__file__).resolve().parents[2]
BATCH = CR.parents[1]
CN = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
TOPICS = json.loads((CN / "topics.json").read_text(encoding="utf-8"))["topics"]
HOST = CR / "evidence/cards-inventory-host-and-shared.md"
FILES = [
    BATCH / "3-done/505-sc19-cards-workers/evidence/cards-inventory-workers.md",
    BATCH / "3-done/505-sc19-cards-workers/evidence/cards-inventory-drivers.md",
    CR / "evidence/cards-inventory-foreman.md",
    CR / "evidence/cards-inventory-chief-of-staff.md",
    CR / "evidence/cards-inventory-griller.md",
    HOST,
]
SRC = re.compile(r"^`?((?:[\w.-]+/)*[\w.-]+\.(?:md|json))(?::[\d, -]+)?`?$")

LIST = re.compile(r"\btopics? ([a-z0-9-]+(?:(?:, |,? and )[a-z0-9-]+)*)")


def named(home: str) -> set[str]:
    """The topic names a home cell gives after `topic` or `topics` (a prose word is not one)."""
    out = set()
    for m in LIST.finditer(home):
        for n in re.split(r", |,? and ", m.group(1)):
            if n not in TOPICS:
                break
            out.add(n)
    return out


got: dict[str, set[str]] = collections.defaultdict(set)
for path in FILES:
    for line in path.read_text(encoding="utf-8").splitlines():
        if not re.match(r"\| [A-Z]{1,3}-?B?\d", line):
            continue
        c = [x.strip() for x in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(c) < 8:
            continue
        if path == HOST:
            idx = [i for i, x in enumerate(c) if i >= 4 and SRC.match(x)]
            if not idx or idx[-1] + 2 >= len(c):
                continue
            i = idx[-1]
            src, home = SRC.match(c[i]).group(1), c[i + 2]
        else:
            m = re.search(r"([A-Za-z-]+\.md)", c[4])
            if not m:
                continue
            src, home = m.group(1), c[6]
        if path.parent.parent.name.startswith("505-"):
            # CR 505's homes write `topic (new) x`, `topic a (parts b, c)`, `a and b`: its own
            # rule, r5/gen.py's, which its cells (no file name in them) read right.
            if "topic" in home:
                got[src.split("/")[-1]].update(
                    n for n in re.findall(r"[a-z0-9][a-z0-9-]*", home) if n in TOPICS)
            continue
        got[src.split("/")[-1]].update(named(home))

text = HOST.read_text(encoding="utf-8")
out = []
stale = 0
for line in text.split("\n"):
    m = re.match(r"\| references/(\S+) \|.*split into topics (.*?) \|$", line)
    if m:
        name = m.group(1).split("/")[-1]
        listed = m.group(2).split(", ")
        want = sorted(got.get(name, set()))
        if set(listed) != set(want):
            stale += 1
            print(name, "listed only:", sorted(set(listed) - set(want)),
                  "rows only:", sorted(set(want) - set(listed)))
            if want:
                line = line.replace("split into topics " + m.group(2),
                                    "split into topics " + ", ".join(want))
            else:
                line = line.replace("; split into topics " + m.group(2), "")
    else:
        m2 = re.match(r"\| references/(\S+) \|", line)
        if m2 and got.get(m2.group(1).split("/")[-1]) and "split into topics" not in line:
            want = sorted(got[m2.group(1).split("/")[-1]])
            stale += 1
            print("no list but rows home topics:", m2.group(1), want)
            line = line[: -len(" |")] + "; split into topics " + ", ".join(want) + " |"
    out.append(line)
print("stale lists:", stale)
if "--write" in sys.argv:
    HOST.write_bytes("\n".join(out).encode("utf-8"))
