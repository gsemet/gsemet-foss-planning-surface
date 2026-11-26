import json
import re
from pathlib import Path

W = Path("<worktree>/skills/chantier/cards-next")
F = Path("<CR folder>/evidence/cards-inventory-foreman.md")
SEP = "(?<!" + chr(92) * 2 + ")" + chr(92) + "|"
data = json.loads((W / "topics.json").read_text(encoding="utf-8"))
tops = data.get("topics", data)
if isinstance(tops, list):
    tops = {t["name"]: t for t in tops}


def readings(t):
    out = []

    def walk(x):
        if isinstance(x, str) and x.split("#")[0].endswith(".md"):
            out.append(x.split("#")[0])
        elif isinstance(x, dict):
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(t.get("readings", t.get("reading")))
    return out


def words(s):
    return {w.lower()[:6] for w in re.findall(r"[A-Za-z]{4,}", s)}


rows, bad_name, norole, low = 0, [], [], []
for line in F.read_text(encoding="utf-8").split("\n"):
    c = [x.strip() for x in re.split(SEP, line.strip())[1:-1]]
    if len(c) != 8 or not c[0].startswith("FM-"):
        continue
    rid, _, trig, beh, src, kind, home, check = c
    m = re.match(r"`?topic ([a-z0-9-]+)", home)
    if not m:
        continue
    rows += 1
    name = m[1]
    if name not in tops:
        bad_name.append((rid, name))
        continue
    if "foreman" not in tops[name].get("roles", []):
        norole.append((rid, name))
    text = " ".join((W / p).read_text(encoding="utf-8") for p in readings(tops[name]) if (W / p).is_file())
    b = words(beh)
    if len(b) >= 5:
        r = len(b & words(text)) / len(b)
        low.append((r, rid, name, kind, beh))
print("topic-home rows:", rows, "| unknown topic:", bad_name, "| topic without foreman role:", norole[:20], len(norole))
low.sort()
print("share of a row's words found in its topic: <0.5:", sum(x[0] < 0.5 for x in low), "of", len(low))
for r, rid, name, kind, beh in low[:22]:
    print(f"{r:.2f} {rid} {kind} topic {name}: {beh[:230]}")
