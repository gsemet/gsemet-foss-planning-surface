"""Verifier: HOMES under the PR's stated rule, and the PR body's per-key list."""
import ast, re, subprocess
WT = "<worktree>"
BASE = "fbdb53d2a2860a95257235dc7f592ab0e75ce45e"
P = "skills/chantier/scripts/cli/tests/test_card_homes.py"
REFS = f"{WT}/skills/chantier/references"
def homes(rev):
    s = subprocess.run(["git", "-C", WT, "show", f"{rev}:{P}"], capture_output=True, text=True, encoding="utf-8", check=True).stdout
    d = [n for n in ast.parse(s).body if isinstance(n, ast.Assign) and n.targets[0].id == "HOMES"][0]
    return {k: [f"topic {t}" for t in v[0].split()] + v[1] for k, v in ast.literal_eval(d.value).items()}
base, head = homes(BASE), homes("HEAD")
doc = open(f"{WT}/docs/protective-rules.md", encoding="utf-8").read().splitlines()
rows = []
for line in doc:
    c = [x.strip() for x in line.replace(chr(92) + "|", chr(1)).split("|")]
    if len(c) >= 6 and c[3] in ("`held`", "`restored here`"):
        rows.append((c[1], c[4]))
def section(path, h):
    t = open(path, encoding="utf-8").read()
    m = re.search(r"^(#+) " + re.escape(h) + r".*$", t, re.M)
    rest = t[m.end():]
    n = re.search(r"^#{1,%d} " % len(m.group(1)), rest, re.M)
    return " ".join((rest[:n.start()] if n else rest).split())
def named(home):
    kind, _, name = home.partition(" ")
    out = []
    for rid, cell in rows:
        if kind == "topic":
            hit = re.search(r"`topics/" + re.escape(name) + r"(-p\d+)?\.md`", cell)
        elif kind == "floor":
            hit = re.search(r"floor " + name + r"\b", cell)
        elif kind == "card":
            path, _, h = name.partition("#")
            spans = re.findall(r"`" + re.escape(path) + r'` "(.*?)"(?=;|$)', cell)
            hit = spans and (not h or any(" ".join(s.split()) in section(f"{REFS}/{path}", h) for s in spans))
        elif kind == "skill":
            hit = re.search(r"skills/" + re.escape(name) + r"/SKILL\.md", cell)
        elif kind == "host":
            hit = re.search(r"host row `" + re.escape(name) + "`", cell)
        if hit:
            out.append(rid)
    return out
bad = [(k, h, h in head.get(k, []), named(h)) for k, v in base.items() for h in v
       if (h.startswith("floor ") or bool(named(h))) != (h in head.get(k, []))]
added = [(k, h) for k, v in head.items() for h in v if h not in base.get(k, [])]
print("base", len(base), sum(map(len, base.values())), "head", len(head), sum(map(len, head.values())))
print("mismatches against the rule:", bad)
print("homes added:", added)
print("removed keys:", {k: v for k, v in base.items() if k not in head})
body = open(f"{WT.split('/chantier.worktrees')[0]}/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/2-actives/515-cards-inventory-last-reading/work/pr-body.md", encoding="utf-8").read()
seg = body.split("### Homes kept in `test_card_homes.py`", 1)[1].split("Keys removed", 1)[0]
print(seg.strip().splitlines()[0:3])
err = 0
seen = []
for line in seg.splitlines():
    m = re.match(r"- `(test_\w+)`: (\d+) kept, (\d+) dropped\. (.*)$", line)
    if not m:
        continue
    k, nk, nd, rest = m[1], int(m[2]), int(m[3]), m[4]
    seen.append(k)
    items = re.findall(r"`([^`]+)` \(([^)]*)\)", rest)
    listed = [h for h, _ in items]
    if (nk, nd) != (len(head[k]), len(base[k]) - len(head[k])) or sorted(listed) != sorted(head[k]):
        err += 1
        print("COUNT/NAMES", k, nk, nd, len(head[k]), len(base[k]) - len(head[k]), set(listed) ^ set(head[k]))
    for h, ids in items:
        got = set(named(h))
        claimed = {x.strip() for x in ids.split(",")}
        if h.startswith("floor ") and not got:
            print("   floor with no line:", k, h, ids)
            continue
        if claimed != got:
            err += 1
            print("IDS", k, h, "PR only:", sorted(claimed - got), "list only:", sorted(got - claimed))
print("keys in PR list", len(seen), "missing", set(head) - set(seen), "errors", err)
