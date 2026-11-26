"""Read-only: the forms of the "new home" cells of every inventory the completeness table reads."""

import collections
import re
from pathlib import Path

CR = Path(__file__).resolve().parents[2]
BATCH = CR.parents[1]
FILES = [
    BATCH / "3-done/505-sc19-cards-workers/evidence/cards-inventory-workers.md",
    BATCH / "3-done/505-sc19-cards-workers/evidence/cards-inventory-drivers.md",
    CR / "evidence/cards-inventory-foreman.md",
    CR / "evidence/cards-inventory-chief-of-staff.md",
    CR / "evidence/cards-inventory-griller.md",
]
for path in FILES:
    shapes: collections.Counter = collections.Counter()
    sample: dict[str, list[str]] = collections.defaultdict(list)
    sources: collections.Counter = collections.Counter()
    rows = short = nosrc = 0
    ids = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not re.match(r"\| [A-Z]{1,3}-?B?\d", line):
            if line.startswith("| ") and not re.match(r"\| (id|---)", line):
                ids.append(line[:30])
            continue
        c = [x.strip() for x in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(c) < 8:
            short += 1
            continue
        rows += 1
        m = re.search(r"([A-Za-z-]+\.md)", c[4])
        if not m:
            nosrc += 1
        sources[re.sub(r":.*", "", c[4])] += 1
        s = re.sub(r"[A-Za-z0-9_/<>-]+\.(md|json|py|yaml)(:[0-9, -]+)?", "F", c[6])
        s = re.sub(r"(?<=topic )[a-z0-9-]+", "N", s)
        s = re.sub(r"(?<=host row )[a-z0-9-]+", "N", s)
        s = re.sub(r"(?<=floor )\d+", "N", s)
        s = re.sub(r"(?<=refusal ).*", "R", s)
        s = re.sub(r"(?<=next: line ).*", "R", s)
        shapes[s] += 1
        sample[s].append(f"{c[0]}: {c[6][:110]}")
    print("==", path.name, "rows", rows, "short", short, "no source", nosrc)
    print("  other table lines", len(ids), ids[:3])
    print("  sources", dict(sources))
    for s, n in shapes.most_common():
        print(f"  {n:5} {s[:90]!r}  e.g. {sample[s][0]}")
