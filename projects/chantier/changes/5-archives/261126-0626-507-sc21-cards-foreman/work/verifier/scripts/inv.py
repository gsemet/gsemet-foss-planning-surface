import random
import re
import subprocess
from pathlib import Path

W = "<worktree>"
BASE = "24111e6d"
EV = Path("<CR folder>/evidence")
CN = "skills/chantier/cards-next"


def show(rev, path):
    d = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=W, capture_output=True)
    return d.stdout.decode("utf-8", "replace").split("\n") if d.returncode == 0 else None


tree = subprocess.run(["git", "ls-tree", "-r", "--name-only", "HEAD"], cwd=W, capture_output=True,
                      text=True).stdout.split("\n")
base_tree = subprocess.run(["git", "ls-tree", "-r", "--name-only", BASE], cwd=W, capture_output=True,
                           text=True).stdout.split("\n")


def cells(line):
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


for f in sorted(EV.glob("cards-inventory-foreman.md")):
    text = f.read_text(encoding="utf-8")
    lines = text.split("\n")
    print("\n=====", f.name, len(text.encode()), "bytes")
    print("headings:", [l for l in lines if l.startswith("#")][:60])
    header, rows = None, []
    for n, l in enumerate(lines, 1):
        if l.startswith("|"):
            c = cells(l)
            low = [x.lower() for x in c]
            if "id" in low and "source" in low:
                header = low if ("new home" in low and "behaviour" in low and "kind" in low) else None
                if header is None:
                    print("  other table, line", n, low)
                continue
            if header and re.match(r"`?[A-Z]+-[A-Z]?\d+", c[0] if c else ""):
                rows.append((n, header, c))
        else:
            header = None
    print("rule rows:", len(rows))
    col = lambda h, c, name: next((c[i] for i, x in enumerate(h) if x.startswith(name) and i < len(c)), None)
    empty = [c[0] for _, h, c in rows if not col(h, c, "new home")]
    wrong = [c[0] for _, h, c in rows if len(c) != len(h)]
    kinds = {}
    for _, h, c in rows:
        kinds.setdefault((col(h, c, "kind") or "?")[:1], []).append((h, c))
    print("empty new home:", empty[:10], len(empty), "| rows with wrong cell count:", wrong[:10], len(wrong))
    print("by kind:", {k: len(v) for k, v in sorted(kinds.items())})
    a_bad = []
    for h, c in kinds.get("a", []):
        home = col(h, c, "new home").strip("`")
        if not re.match(r"(card |floor|refusal)", home):
            a_bad.append((c[0], home[:60]))
    print("kind-a rows whose home is not card/floor/refusal:", len(a_bad), a_bad[:20])
    print("kind-a rows marked inferable:", [c[0] for h, c in kinds.get("a", []) if "inferable" in col(h, c, "new home")])
    homes = {}
    for _, h, c in rows:
        m = re.match(r"`?(card|topic|floor|refusal|next|facts|host row|proof file|incidents file|inferable)", col(h, c, "new home") or "")
        homes[m[1] if m else "OTHER"] = homes.get(m[1] if m else "OTHER", 0) + 1
    print("home forms:", homes)
    other = [(c[0], (col(h, c, "new home") or "")[:70]) for _, h, c in rows
             if not re.match(r"`?(card|topic|floor|refusal|next|facts|host row|proof file|incidents file|inferable)", col(h, c, "new home") or "")]
    print("other home forms sample:", other[:8])
    # card homes exist
    missing = []
    for _, h, c in rows:
        for m in re.finditer(r"card `?([A-Za-z0-9_./-]+\.md)", col(h, c, "new home") or ""):
            p = m[1]
            cand = [p, f"{CN}/{p}", f"{CN}/topics/{p}"]
            if not any(x in tree for x in cand) and not any(t.endswith("/" + p) and t.startswith(CN) for t in tree):
                missing.append((c[0], p))
    print("card homes naming a file absent from cards-next:", len(missing), missing[:10])
    # sources resolve
    nofile, outrange, noword = [], [], []
    checked = 0
    for _, h, c in rows:
        src = col(h, c, "source") or ""
        m = re.match(r"`?([^:`]+):(\d+)", src)
        if not m:
            nofile.append((c[0], src[:60]))
            continue
        p = m[1]
        cands = [p] if p in base_tree else [x for x in (f"skills/chantier/references/{p}", f"skills/chantier/{p}", f"skills/{p}") if x in base_tree]
        if not cands:
            nofile.append((c[0], src[:60]))
            continue
        body = show(BASE, cands[0])
        ln = int(m[2])
        if ln > len(body):
            outrange.append((c[0], src))
            continue
        checked += 1
        words = {w.lower() for w in re.findall(r"[A-Za-z_]{4,}", col(h, c, "behaviour") or "")}
        have = {w.lower() for w in re.findall(r"[A-Za-z_]{4,}", body[ln - 1])}
        if words and not words & have:
            noword.append((c[0], src))
    print(f"sources checked: {checked}; unresolved: {len(nofile)} {nofile[:5]}; out of range: {outrange[:5]}; line shares no word: {len(noword)} {noword[:8]}")
    random.seed(507)
    for _, h, c in random.sample(rows, min(5, len(rows))):
        src = col(h, c, "source")
        m = re.match(r"`?([^:`]+):(\d+)", src)
        line = ""
        if m:
            for x in (m[1], f"skills/chantier/references/{m[1]}", f"skills/chantier/{m[1]}", f"skills/{m[1]}"):
                if x in base_tree:
                    line = show(BASE, x)[int(m[2]) - 1]
                    break
        print(f"  SAMPLE {c[0]} kind={col(h, c, 'kind')} home={col(h, c, 'new home')}\n    behaviour: {col(h, c, 'behaviour')[:200]}\n    {src}: {line[:200]}")
    for key in ("walk", "boundar", "script", "SCORECARD", "J11", "J22", "byte for byte", "byte-for-byte"):
        hits = [n for n, l in enumerate(lines, 1) if key.lower() in l.lower()]
        print(f"  mentions '{key}': lines {hits[:8]} ({len(hits)})")
