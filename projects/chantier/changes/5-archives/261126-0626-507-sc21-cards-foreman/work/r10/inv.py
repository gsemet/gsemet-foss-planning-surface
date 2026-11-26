"""Round 10: parse every inventory row of evidence/cards-inventory-*.md (shared by the audits)."""

import json
import pathlib
import re
import subprocess

WT = pathlib.Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507")
CHANTIER = WT / "skills/chantier"
CARDS = CHANTIER / "cards-next"
EV = pathlib.Path(__file__).resolve().parents[2] / "evidence"
BASE = "24111e6d"

TOPICS = json.loads((CARDS / "topics.json").read_text(encoding="utf-8"))["topics"]


def cells(line):
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def rows():
    """Every row of the 8-column rule tables: (file, line number, dict)."""
    for inv in sorted(EV.glob("cards-inventory-*.md")):
        header = None
        for n, line in enumerate(inv.read_text(encoding="utf-8").split("\n"), 1):
            if not line.startswith("|"):
                header = None
                continue
            c = cells(line)
            low = [x.lower() for x in c]
            if "id" in low and ("source" in low or "behaviour" in low):
                header = low
                continue
            if not header or set("".join(c)) <= set("-: "):
                continue
            if "behaviour" in header and "new home" in header and "source" in header:
                if len(c) != len(header):
                    print(f"?? {inv.name}:{n} {len(c)} cells for {len(header)}")
                    continue
                yield inv.name, n, dict(zip(header, c))


def readings(name):
    out = []
    row = TOPICS.get(name)
    if row is None:
        return out
    for reading in row["readings"]:
        files = reading.values() if isinstance(reading, dict) else [reading]
        for f in files:
            out.append(f.split("#")[0])
    return out


CARD_RE = re.compile(r"(?:card )?`?((?:skills/|hosts/|forges/|topics/)?[A-Za-z0-9_.-]+\.(?:md|json))(?::(\d+))?")


def home_files(home):
    """The cards-next files a `new home` cell names, with the cited lines."""
    found = {}
    for m in re.finditer(r"\btopics? ((?:`?[a-z0-9-]+`?)(?:(?:, | and )`?[a-z0-9-]+`?)*)", home):
        for name in re.findall(r"[a-z0-9-]+", m[1]):
            if name != "and":
                for f in readings(name):
                    found.setdefault(f, set())
    for m in re.finditer(r"\bfloor \d+", home):
        found.setdefault("floor.md", set())
    for m in CARD_RE.finditer(home):
        f = m[1]
        for cand in (f, f"topics/{f}"):
            if (CARDS / cand).is_file():
                found.setdefault(cand, set())
                if m[2]:
                    found[cand].add(int(m[2]))
                break
    if re.search(r"\bhost rows?\b", home):
        for f in ("hosts/claude-code.json", "hosts/copilot.json"):
            if (CARDS / f).is_file():
                found.setdefault(f, set())
    return found


_SOURCES = {}


def source_lines(path):
    if path not in _SOURCES:
        _SOURCES[path] = None
        for cand in (f"skills/chantier/references/{path}", f"skills/chantier/{path}", path, f"skills/{path}"):
            d = subprocess.run(["git", "show", f"{BASE}:{cand}"], cwd=WT, capture_output=True)
            if d.returncode == 0:
                _SOURCES[path] = d.stdout.decode("utf-8").split("\n")
                break
    return _SOURCES[path]


def source_range(src):
    """(path, first, last) of a `source` cell; None when it is not file:lines."""
    m = re.match(r"`?([^:`\s]+):(\d+)(?:-(\d+))?", src)
    if not m:
        return None
    return m[1], int(m[2]), int(m[3] or m[2])


def norm(text):
    return " ".join(text.replace("\\|", "|").split())
