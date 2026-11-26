"""Throwaway: base card -> topics, read from the family inventories' `source` and `new home` columns."""

import collections
import re
import sys
from pathlib import Path

CH = Path("C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch")
DIRS = {
    "workers": CH / "3-done/505-sc19-cards-workers/evidence/cards-inventory-workers.md",
    "drivers": CH / "3-done/505-sc19-cards-workers/evidence/cards-inventory-drivers.md",
    "chief": CH / "2-actives/507-sc21-cards-foreman/evidence/cards-inventory-chief-of-staff.md",
    "foreman": CH / "2-actives/507-sc21-cards-foreman/evidence/cards-inventory-foreman.md",
    "griller": CH / "2-actives/507-sc21-cards-foreman/evidence/cards-inventory-griller.md",
}


def rows(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        if re.match(r"\| [A-Z]{1,3}-?\d", line):
            yield [x.strip() for x in re.split(r"(?<!\\)\|", line)[1:-1]]


for name, path in DIRS.items():
    if not path.exists():
        print(name, "MISSING", path)
        continue
    by = collections.defaultdict(collections.Counter)
    n = 0
    for c in rows(path):
        n += 1
        if len(c) < 8:
            continue
        src = re.findall(r"([A-Za-z-]+\.md)", c[4])[:1]
        home = c[6]
        for t in re.findall(r"topic `?([a-z0-9-]+)", home):
            for s in src:
                by[s][t] += 1
        if not re.findall(r"topic `?([a-z0-9-]+)", home):
            for s in src:
                by[s]["(other)"] += 1
    print(f"== {name}: {n} rows")
    for s, v in by.items():
        print(" ", s, " ".join(f"{t}:{k}" for t, k in v.most_common()))
