"""Parse the four inventories; shared by the round-7 checks."""
import re
from pathlib import Path

CR = Path(__file__).resolve().parents[2]
EV = CR / "evidence"
NAMES = ("foreman", "chief-of-staff", "griller", "host-and-shared")
SEP = "(?<!" + chr(92) * 2 + ")" + chr(92) + "|"


def cells(line):
    return [c.strip() for c in re.split(SEP, line.strip())[1:-1]]


def rows(name):
    """Yield (line number, dict) of every rule row of one inventory."""
    header = None
    for i, line in enumerate((EV / f"cards-inventory-{name}.md").read_text(encoding="utf-8").split("\n"), 1):
        if not line.startswith("|"):
            header = None
            continue
        c = cells(line)
        low = [x.lower() for x in c]
        if "id" in low:
            ok = all(any(x.startswith(k) for x in low) for k in ("behaviour", "kind", "new home"))
            header = low if ok else None
            continue
        if not header or len(c) != len(header) or set(c[0]) <= set("-: "):
            continue
        d = {}
        for k, v in zip(header, c):
            for key in ("id", "role", "trigger", "behaviour", "source", "kind", "new home", "check"):
                if k.startswith(key):
                    d[key] = v
        yield i, d
