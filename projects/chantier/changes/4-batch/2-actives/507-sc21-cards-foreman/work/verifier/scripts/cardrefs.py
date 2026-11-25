import re
from pathlib import Path

W = Path("<worktree>/skills/chantier/cards-next")
EV = Path("<CR folder>/evidence")
SEP = "(?<!" + chr(92) * 2 + ")" + chr(92) + "|"


def words(s):
    return {w.lower()[:5] for w in re.findall(r"[A-Za-z]{4,}", s)}


for name in ("foreman", "chief-of-staff", "griller", "host-and-shared"):
    header = None
    low, n = [], 0
    for line in (EV / f"cards-inventory-{name}.md").read_text(encoding="utf-8").split("\n"):
        if not line.startswith("|"):
            header = None
            continue
        c = [x.strip() for x in re.split(SEP, line.strip())[1:-1]]
        lc = [x.lower() for x in c]
        if "id" in lc:
            header = lc if all(any(x.startswith(k) for x in lc) for k in ("behaviour", "kind", "new home")) else None
            continue
        if not header or len(c) != len(header):
            continue
        get = lambda k: next(c[i] for i, x in enumerate(header) if x.startswith(k))
        if not get("kind").startswith("a"):
            continue
        refs = re.findall(r"([A-Za-z0-9_./-]+\.md):(\d+)", get("new home"))
        if not refs:
            continue
        text = ""
        bad = []
        for f, ln in refs:
            p = next((x for x in (W / f, W / "topics" / f) if x.is_file()), None)
            if p is None:
                bad.append(f)
                continue
            body = p.read_text(encoding="utf-8").split("\n")
            if int(ln) <= len(body):
                text += " " + body[int(ln) - 1]
            else:
                bad.append(f"{f}:{ln}")
        n += 1
        b = words(get("behaviour"))
        r = len(b & words(text)) / len(b) if b else 1
        if bad or r < 0.2:
            low.append((round(r, 2), c[0], get("new home")[:60], bad, get("behaviour")[:200]))
    print(f"== {name}: kind-a rows with a file:line home: {n}; under 20% shared words or bad ref: {len(low)}")
    for x in sorted(low)[:25]:
        print("  ", *x, sep=" | ")
