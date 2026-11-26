import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

wt = Path(sys.argv[1])
mode = sys.argv[2]
BASE = "266b784f008d6d9c6a5e7e1f9eabacefb0552dee"
OLD = "f08cf41"
text = (wt / "docs/proofs/cards-inventory.md").read_text("utf-8")


def cells(line):
    parts = re.split(r"(?<!\\)\|", line.strip()[1:-1])
    return [p.strip().replace("\\|", "|") for p in parts]


def git(*args):
    return subprocess.run(
        ["git", "-C", str(wt), *args], capture_output=True, check=True
    ).stdout.decode("utf-8")


sections = {}
name = None
for line in text.splitlines():
    if line.startswith("## "):
        name = line[3:]
        sections[name] = []
    elif name:
        sections[name].append(line)
rows = [cells(x) for x in sections["Rows"] if x.startswith("|")][2:]
byid = {r[0]: r for r in rows}

if mode == "kinds":
    print("(kind, check) counts:")
    for k, v in sorted(Counter((r[5], r[7].split(" ")[0].rstrip(":")) for r in rows).items()):
        print("  ", k, v)
    a = [r for r in rows if r[5] == "a"]
    homed = [r for r in a if not r[6].startswith("open: ")]
    print("kind a", len(a), "homed", len(homed), "open", len(a) - len(homed))
    print("kind-a homed by check type", Counter(r[7].split(" ")[0] for r in homed))
    for r in homed:
        if r[7].split(" ")[0] != "quote":
            print("   ", r[0], r[6][:50], "|", r[7][:120])
    print("distinct ids", len(byid), "of", len(rows))
    bad = [r[0] for r in rows if not re.fullmatch(r"[A-Z]{1,2}-\d{3}", r[0])]
    print("ids not matching ^[A-Z]{1,2}-\\d{3}$", len(bad))
    print("  B-suffix/prefix", sum("B" in i.split("-")[0] for i in bad), "4-digit", sum(len(i.split("-")[1]) == 4 for i in bad))
    o = [r for r in rows if r[6].startswith("open: ")]
    inf = [r for r in o if "inferable" in r[6]]
    print("open", len(o), "open a", sum(r[5] == "a" for r in o), "inferable", len(inf),
          "inferable kinds", Counter(r[5] for r in inf),
          "others", sum(r[5] != "a" and "inferable" not in r[6] for r in o))
    print("incidents", sorted(r[0] for r in rows if r[6].startswith("incidents")))
    print("homed inferable", sum(r[6].startswith("inferable") for r in rows))
    print("rare", sum(r[2] == "none (rare)" for r in rows))
elif mode == "sections":
    for k, v in sections.items():
        table = [x for x in v if x.startswith("|")]
        print("##", k, "lines", len(v), "table lines", len(table))
    owner = sections.get("For the owner", [])
    sub = None
    n = Counter()
    for x in owner:
        if x.startswith("#") or (x and not x.startswith("|") and not x.startswith(" ")):
            sub = x[:150]
            print("   head:", sub)
        elif x.startswith("|") and not re.match(r"^\|[\s|:-]+$", x):
            n[sub] += 1
    for k, v in n.items():
        print("   table rows incl header", v, "under", k)
elif mode == "checklist":
    name_ = [k for k in sections if "check" in k.lower()]
    print(name_)
    for x in sections[name_[-1]]:
        if x.strip():
            print(x[:260])
elif mode == "sources":
    src = [cells(x) for x in sections["Sources"] if x.startswith("|")]
    print("header", src[0])
    body = src[2:]
    print("table rows", len(body), "last", body[-1])
    tree = {}
    for line in git("ls-tree", "-r", OLD, "--", "skills/chantier/references", "skills").splitlines():
        meta, path = line.split("\t")
        if path.startswith("skills/chantier/references/") or re.fullmatch(r"skills/[^/]+/SKILL\.md", path):
            tree[path] = meta.split()[2]
    tl = tb = 0
    bad = 0
    seen = set()
    for r in body:
        paths = [c.strip("`") for c in r if c.strip("`") in tree]
        if not paths:
            continue
        p = paths[0]
        seen.add(p)
        blob = subprocess.run(["git", "-C", str(wt), "show", f"{OLD}:{p}"], capture_output=True, check=True).stdout
        nl, nb = blob.count(b"\n"), len(blob)
        tl += nl
        tb += nb
        row = " ".join(r)
        if str(nl) not in row or str(nb) not in row or tree[p][:7] not in row:
            bad += 1
            print("mismatch", p, nl, nb, tree[p][:7], r)
    print("source files matched", len(seen), "lines", tl, "bytes", tb, "mismatches", bad)
    print("files in old tree (references + */SKILL.md)", len(tree), "not in table", sorted(set(tree) - seen))
    print("inventory bytes (worktree)", (wt / "docs/proofs/cards-inventory.md").stat().st_size)
    print("inventory bytes (blob)", git("ls-tree", "-l", "HEAD", "--", "docs/proofs/cards-inventory.md").strip())
elif mode == "restored":
    want = sys.argv[3].split(",")
    for i in want:
        r = byid[i]
        m = re.match(r'card (\S+): "(.*)"$', r[6])
        if not m:
            print(i, "HOME NOT A CARD:", r[6])
            continue
        card, span = m[1], m[2]
        path = "skills/chantier/references/" + card
        head = " ".join((wt / path).read_text("utf-8").split())
        base = " ".join(git("show", f"{BASE}:{path}").split())
        s = " ".join(span.split())
        print(i, card, "head:", s in head, "base:", s in base)
    print("count", len(want))
