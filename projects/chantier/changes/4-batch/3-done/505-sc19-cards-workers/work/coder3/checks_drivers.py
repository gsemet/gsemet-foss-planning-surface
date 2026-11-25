import json, re, sys
from pathlib import Path
sys.path.insert(0, r"C:\Users\gaeta\Projets\chantier.worktrees\batch-31-CR-505\skills\chantier\scripts\cli\src")
CN = Path(r"C:\Users\gaeta\Projets\chantier.worktrees\batch-31-CR-505\skills\chantier\cards-next")
cards = {"cr-driver": 4096, "stack-driver": 4096, "release-driver": 3072, "qa-driver": 2048}
tj = json.loads((CN/"topics.json").read_text(encoding="utf-8"))["topics"]
mine = {k: v for k, v in tj.items() if any(r in v["roles"] for r in cards)}
# only SC20 topics: those with a file not authored by PART 1 -> all with Driver roles
out = []
print("## cards")
for c, t in cards.items():
    n = len((CN/f"{c}.md").read_bytes()); print(f"| {c} | {t} | {n} | {'over by %d' % (n-t) if n > t else 'within'} |")
print("## topic files")
names = sorted({Path(r).stem for v in mine.values() for r in v["readings"]})
over = []
for n in names:
    b = (CN/"topics"/f"{n}.md").read_bytes()
    if b"\r" in b or b[:3] == b"\xef\xbb\xbf": print("BAD", n)
    print(f"| {n} | 1536 | {len(b)} | {'over by %d' % (len(b)-1536) if len(b) > 1536 else 'within'} |")
print("## links")
known = {p.stem for p in (CN/"topics").glob("*.md")}
forward = ("concepts.md", "pr-template.md", "release-template.md", "forges/")
bad = []
files = [CN/f"{c}.md" for c in cards] + [CN/"topics"/f"{n}.md" for n in names]
for f in files:
    txt = f.read_text(encoding="utf-8")
    for m in re.finditer(r"\]\(([^)#]+)(#[^)]*)?\)", txt):
        tgt = m.group(1)
        if tgt.startswith("http"): continue
        base = f.parent
        if any(tgt.endswith(x) or x in tgt for x in forward): print("forward", f.name, tgt); continue
        if not (base/tgt).resolve().exists(): bad.append((f.name, tgt))
    for m in re.finditer(r"help (?:--for \S+ )?([a-z][a-z0-9-]*)", txt):
        if m.group(1) not in tj: bad.append((f.name, "help " + m.group(1)))
print("unresolved:", bad)
print("## topics.json")
from chantier.commands.help import load_topics
t = load_topics(CN/"topics.json"); print("load_topics ok", len(t))
rn = set(re.findall(r"^  - name: (\S+)", Path(r"C:\Users\gaeta\Projets\chantier.worktrees\batch-31-CR-505\skills\chantier\roles.yaml").read_text(encoding="utf-8"), re.M))
for k, v in mine.items():
    for r in v["readings"]:
        if not (CN/r).exists(): print("MISSING reading", k, r)
    for r in v["roles"]:
        if r not in rn: print("UNKNOWN role", k, r)
    if "review_by" in v and not re.fullmatch(r"\d+\.\d+\.\d+", v["review_by"]): print("BAD review_by", k)
print("## trigger in card")
parts = set()
for k, v in tj.items():
    for r in v["readings"]:
        if Path(r).stem != k and Path(r).stem in tj and len(v["readings"]) > 1: parts.add(Path(r).stem)
print("part rows (reached from their parent row, not named in a card):", sorted(parts))
for c in cards:
    txt = (CN/f"{c}.md").read_text(encoding="utf-8")
    for k, v in tj.items():
        if c in v["roles"] and k not in parts:
            # the card names a topic by `name` (trigger)
            if f"`{k}` ({v['trigger']})" not in txt: print("no line", c, k)
print("## forbidden")
for f in files + [CN/"topics.json"]:
    txt = f.read_text(encoding="utf-8")
    for pat in (r"CR-\d+", r"batch-\d+", r"\bepoch\b", r"20\d\d-\d\d-\d\d"):
        for m in re.finditer(pat, txt): print("FORBIDDEN", f.name, m.group(0))
