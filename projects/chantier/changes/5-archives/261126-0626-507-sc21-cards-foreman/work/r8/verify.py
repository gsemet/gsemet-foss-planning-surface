"""Round 8: for each row to re-home, print its home now and the best sentences of the target."""

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
EV = HERE.parent.parent / "evidence"
W = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507/skills/chantier/cards-next")
sys.path.insert(0, str(HERE))
from targets import TARGETS  # noqa: E402

INDEX = json.loads((W / "topics.json").read_text(encoding="utf-8"))["topics"]
ROW = re.compile(r"^\| ((?:FM|C|G|H)-[0-9A-Z]+) \|")


def cells(line: str) -> list[str]:
    return [c.strip().replace("\x00", "\\|") for c in line.replace("\\|", "\x00").strip().strip("|").split("|")]


rows = {}
for path in sorted(EV.glob("cards-inventory-*.md")):
    for line in path.read_text(encoding="utf-8").split("\n"):
        m = ROW.match(line)
        if m and len(c := cells(line)) == 8:
            rows[c[0]] = c


def words(text: str) -> set[str]:
    return {w.rstrip("s") for w in re.findall(r"[a-z0-9_-]{3,}", text.lower())}


def sentences(target: str, rid: str) -> list[tuple[str, str]]:
    kind, _, value = target.partition(":")
    out = []
    if kind == "topic":
        entry = INDEX.get(value)
        if entry is None:
            return [("?", f"NO TOPIC {value}")]
        for reading in entry["readings"]:
            if not isinstance(reading, str):
                out.append((str(reading), json.dumps(reading)))
                continue
            name = reading.split("#")[0]
            path = W / name
            for n, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
                out += [(f"{name}:{n}", s) for s in re.split(r"(?<=[.;:])\s+", line.strip()) if s]
    elif kind == "card":
        name, nums = value.rsplit(":", 1)
        lines = (W / name).read_text(encoding="utf-8").split("\n")
        out = [(f"{name}:{n}", lines[int(n) - 1]) for n in nums.split(",")]
    else:
        for name in ("hosts/claude-code.md", "hosts/claude-code.json"):
            for n, line in enumerate((W / name).read_text(encoding="utf-8").split("\n"), 1):
                out += [(f"{name}:{n}", s) for s in re.split(r"(?<=[.;:])\s+", line.strip()) if s]
    return out


lo, hi = int(sys.argv[1]), int(sys.argv[2])
for rid in list(TARGETS)[lo:hi]:
    row = rows.get(rid)
    if row is None:
        print(f"{rid}: NO ROW")
        continue
    want = words(row[3])
    scored = sorted(
        ((len(want & words(s)) / max(len(want), 1), at, s) for at, s in sentences(TARGETS[rid], rid)),
        reverse=True,
    )
    print(f"{rid} [{row[5]}] now={row[6][:100]} | chk={row[7][:50]} -> {TARGETS[rid]}")
    print(f"  B: {row[3][:330]}")
    for score, at, s in scored[:2]:
        if score:
            print(f"   {score:.2f} {at}: {s[:230]}")
