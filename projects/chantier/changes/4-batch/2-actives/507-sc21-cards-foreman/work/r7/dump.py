"""Write each protecting row beside the text of every line its home cites (reading aid)."""
import re
import sys
from pathlib import Path

import inv

WT = Path(sys.argv[1])
W = WT / "skills/chantier/cards-next"
SRC = WT / "skills/chantier/scripts/cli/src/chantier"
OUT = Path(__file__).parent
REF = re.compile(r"([A-Za-z0-9_./-]+\.(?:md|json|py|ya?ml)):(\d+(?:\s*,\s*\d+)*)(?:-(\d+))?")


def find(f):
    for p in (W / f, W / "topics" / f, SRC / f, WT / f, WT / "skills/chantier" / f):
        if p.is_file():
            return p
    hits = [p for p in SRC.rglob(Path(f).name)]
    return hits[0] if len(hits) == 1 else None


def cited(home):
    out = []
    for f, nums, end in REF.findall(home):
        p = find(f)
        if p is None:
            out.append(f"!! no file {f}")
            continue
        body = p.read_text(encoding="utf-8").split("\n")
        ns = [int(x) for x in nums.split(",")]
        if end:
            ns = list(range(ns[0], int(end) + 1))
        for n in ns:
            t = body[n - 1] if n <= len(body) else "!! past end"
            out.append(f"{p.relative_to(WT).as_posix().replace('skills/chantier/', '')}:{n}: {t}")
    for m in re.finditer(r"floor ((?:\d+)(?:\s*,\s*\d+)*)", home):
        body = (W / "floor.md").read_text(encoding="utf-8").split("\n")
        for n in m[1].split(","):
            hit = [t for t in body if t.startswith(n.strip() + ". ")]
            out.append(f"floor {n.strip()}: {hit[0] if hit else '!! none'}")
    return out


for name in inv.NAMES:
    groups = {}
    for _, d in inv.rows(name):
        if d["kind"].startswith("a") or d["id"].startswith("FM-B"):
            groups.setdefault(d["new home"], []).append(d)
    text = []
    for home, ds in sorted(groups.items()):
        text.append(f"\n######## HOME: {home}")
        text += [f"  >> {c}" for c in cited(home)]
        for d in ds:
            text.append(f"  - {d['id']} [{d['kind']}] ({d['source']}) {d['behaviour']}")
    (OUT / f"dump-{name}.txt").write_text("\n".join(text), encoding="utf-8", newline="\n")
    print(name, sum(len(x) for x in groups.values()), len("\n".join(text)))
