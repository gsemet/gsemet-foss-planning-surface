import re
import subprocess
from pathlib import Path

W = "<worktree>"
EV = Path("<CR folder>/evidence")
SEP = "(?<!" + chr(92) * 2 + ")" + chr(92) + "|"
BASES = ["24111e6d", "bf4e4c42"]
trees = {b: subprocess.run(["git", "ls-tree", "-r", "--name-only", b], cwd=W, capture_output=True, text=True).stdout.split("\n") for b in BASES}
cache = {}


def body(b, p):
    if (b, p) not in cache:
        cache[b, p] = subprocess.run(["git", "show", f"{b}:{p}"], cwd=W, capture_output=True).stdout.decode("utf-8", "replace").split("\n")
    return cache[b, p]


def words(s):
    return {w.lower() for w in re.findall(r"[A-Za-z_]{3,}", s)}


for name in ("foreman", "chief-of-staff", "griller"):
    n, fail = 0, []
    header = None
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
        m = re.match(r"`?([^:`]+):(\d+)(?:-(\d+))?", get("source"))
        if not m:
            fail.append((c[0], "unparsed", get("source")[:60]))
            continue
        a, z = int(m[2]), int(m[3] or m[2])
        for b in BASES[:1]:
            p = next((x for x in (m[1], f"skills/chantier/references/{m[1]}", f"skills/chantier/{m[1]}", f"skills/{m[1]}") if x in trees[b]), None)
            if p is None:
                fail.append((c[0], "no file", m[1]))
                break
            text = " ".join(body(b, p)[a - 1:z])
            n += 1
            if words(get("behaviour")) and not words(get("behaviour")) & words(text):
                fail.append((c[0], get("source"), get("behaviour")[:80]))
    print(f"{name}: rows checked over the whole source range at 24111e6d: {n}; rows sharing no word: {len([f for f in fail if f[0] != "---"])} {[f for f in fail if f[0] != "---"][:8]}")
