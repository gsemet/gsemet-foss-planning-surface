"""Score each inventory row against its cited home and against the whole new set (round 8)."""
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

CR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(CR / "work" / "r7"))
import inv  # noqa: E402

WT = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507")
W = WT / "skills/chantier/cards-next"
OUT = Path(__file__).parent

STOP = set(
    "the a an and or of to in on is are be it its that this these those with for as at by from not no"
    " you your their them they he she his her one two when then than so if but only also each every any all"
    " chantier which who what whose how may can must will does do did has have had was were been being"
    " there here into out up off over under after before again once while until whether where why own"
    " same other another more less few many much such very just still yet even too nor per via".split()
)


def toks(s):
    s = s.replace("$CHANTIER", " ").lower()
    out = []
    for w in re.findall(r"--?[a-z][a-z-]+|[a-z0-9_]{3,}(?:[.'][a-z]+)*", s):
        if w in STOP:
            continue
        for part in re.split(r"[-_.']", w.lstrip("-")) if not w.startswith("--") else [w]:
            if len(part) < 3 or part in STOP:
                continue
            for suf in ("ings", "ing", "ies", "ed", "es", "s"):
                if part.endswith(suf) and len(part) - len(suf) >= 3:
                    part = part[: -len(suf)]
                    break
            out.append(part.rstrip("e") if len(part) > 4 else part)
    return out


topics = json.loads((W / "topics.json").read_text(encoding="utf-8"))["topics"]
files = {}
for p in sorted(W.rglob("*")):
    if p.is_file() and p.suffix in (".md", ".json") and p.name != "topics.json":
        files[p.relative_to(W).as_posix()] = p.read_text(encoding="utf-8").split("\n")

units = []  # (file, line, tokens)
for f, body in files.items():
    for i, line in enumerate(body, 1):
        t = set(toks(line))
        if not t:
            continue
        if i < len(body) and len(line) < 140:
            t |= set(toks(body[i]))
        units.append((f, i, t))
df = Counter()
for _, _, t in units:
    df.update(t)
N = len(units)


def idf(w):
    return math.log((N + 1) / (df.get(w, 0) + 1)) + 0.3


def score(want, have):
    tot = sum(idf(w) for w in want)
    return sum(idf(w) for w in want if w in have) / tot if tot else 1.0


def readings(name):
    row = topics.get(name)
    if not row:
        return None
    out = []
    for r in row["readings"]:
        for x in r.values() if isinstance(r, dict) else [r]:
            out.append(x.split("#")[0])
    return out


def home_files(home):
    out = []
    for m in re.finditer(r"topics? ([a-z0-9-]+(?:\s*(?:,|and)\s*[a-z0-9-]+)*)", home):
        for n in re.split(r"\s*(?:,|\band\b)\s*", m[1]):
            out += readings(n) or []
    for m in re.finditer(r"([A-Za-z0-9_./-]+\.(?:md|json))", home):
        f = m[1].replace("skills/chantier/cards-next/", "").replace("cards-next/", "")
        for cand in (f, "topics/" + f, "hosts/" + f):
            if cand in files:
                out.append(cand)
                break
    if "floor" in home:
        out.append("floor.md")
    if "host row" in home:
        out += ["hosts/claude-code.json", "hosts/copilot.json"]
    return list(dict.fromkeys(out))


def best(want, only=None):
    res = (0.0, None, 0)
    for f, i, t in units:
        if only is not None and f not in only:
            continue
        s = score(want, t)
        if s > res[0]:
            res = (s, f, i)
    return res


def run():
    allrows = []
    for name in inv.NAMES:
        for ln, d in inv.rows(name):
            if "source" not in d:
                continue
            home = d["new home"]
            want = set(toks(d["behaviour"]))
            hf = home_files(home)
            hs = best(want, set(hf)) if hf else (None, None, 0)
            gs = best(want)
            allrows.append(
                dict(inv=name, line=ln, id=d["id"], kind=d["kind"], trigger=d.get("trigger", ""),
                     source=d["source"], home=home, behaviour=d["behaviour"], files=hf,
                     home_score=hs[0], home_at=f"{hs[1]}:{hs[2]}" if hs[1] else None,
                     best_score=gs[0], best_at=f"{gs[1]}:{gs[2]}" if gs[1] else None,
                     n=len(want))
            )
    (OUT / "match.json").write_text(json.dumps(allrows, indent=0), encoding="utf-8", newline="\n")
    return allrows


if __name__ == "__main__":
    rows = run()
    for name in inv.NAMES:
        sel = [r for r in rows if r["inv"] == name]
        live = [r for r in sel if r["files"] and r["kind"][:1] not in "bf"]
        for lo, hi in ((0, 0.3), (0.3, 0.45), (0.45, 0.6), (0.6, 1.01)):
            k = [r for r in live if lo <= r["home_score"] < hi]
            print(name, f"home {lo}-{hi}: {len(k)} (elsewhere>=0.6: {sum(r['best_score'] >= 0.6 for r in k)})")
