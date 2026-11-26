import json
import re
import subprocess
import sys
from pathlib import Path

W = Path(r"<worktree>")
BASE = "24111e6d9920a7ff3e8f210613186dd65d802ec8"
sys.path.insert(0, str(W / "evals" / "kit"))

from chantier import driver_prompt, plugin_files, roles_data  # noqa: E402
from chantier.commands.help import load_topics  # noqa: E402

print("module under test:", Path(driver_prompt.__file__).as_posix())


def git(*a):
    return subprocess.run(["git", *a], cwd=W, capture_output=True, check=True).stdout


def size(rev, path):
    try:
        return int(subprocess.run(["git", "cat-file", "-s", f"{rev}:{path}"], cwd=W,
                                  capture_output=True, check=True).stdout)
    except subprocess.CalledProcessError:
        return None


CN = "skills/chantier/cards-next"
files = git("ls-tree", "-r", "--name-only", "HEAD", CN).decode().split()
base_files = set(git("ls-tree", "-r", "--name-only", BASE, CN).decode().split())

print("\n== encoding (BOM, CRLF) over added/changed files")
changed = [l.split("\t") for l in git("diff", "--name-status", f"{BASE}..HEAD").decode().splitlines()]
bad = []
for st, p in changed:
    b = git("show", f"HEAD:{p}")
    if b.startswith(b"\xef\xbb\xbf") or b"\r\n" in b:
        bad.append(p)
    b.decode("utf-8")
print("files:", len(changed), "BOM or CRLF:", bad)

print("\n== role cards at head")
budgets = {"foreman": 4000, "chief-of-staff": 6000, "griller-skill": 4000, "griller": 2000,
           "coder": 1500, "conflict-resolver": 1500, "debugger": 1500, "demo-explorer": 1500,
           "investigator": 1500, "retro-critic": 1500, "spec-critic": 1500, "spec-writer": 1500,
           "inspector": 2000, "verifier": 3000, "cr-driver": 4096, "stack-driver": 4096,
           "release-driver": 3072, "qa-driver": 2048, "floor": 1200, "review-step": 1500}
for n, t in budgets.items():
    s = size("HEAD", f"{CN}/{n}.md")
    print(f"{n}.md head={s} base={size(BASE, f'{CN}/{n}.md')} target={t} " + ("within" if s <= t else f"OVER by {s - t}"))
g = git("show", f"HEAD:{CN}/griller.md").decode()
sec = g[g.index("## Started from the board"):]
print("griller.md section bytes:", len(sec.encode()))

print("\n== shared files: today (references at base) vs head")
for n in ["concepts.md", "pr-template.md", "release-template.md", "status-layout.md", "titles.md",
          "ticket-summary-example.md", "routing.md", "init.md", "review-step.md", "sync-checkout.md",
          "forges/github.md", "forges/gitlab.md", "hosts/claude-code.json", "hosts/copilot.json",
          "hosts/claude-code.md", "hosts/copilot.md", "floor.md", "topics.json", "foreman.md",
          "chief-of-staff.md", "griller.md"]:
    nn = "topics/titles.md" if n == "titles.md" else n
    print(f"{n}: today={size(BASE, 'skills/chantier/references/' + n)} new={size('HEAD', CN + '/' + nn)}")
for n in ["chantier", "chief-of-staff", "griller", "status"]:
    print(f"skill {n}: today={size(BASE, f'skills/{n}/SKILL.md')} new={size('HEAD', f'{CN}/skills/{n}-SKILL.md')}")

print("\n== topic files")
tf = [f for f in files if f.startswith(CN + "/topics/")]
over = [(f.split("/")[-1], size("HEAD", f)) for f in tf if size("HEAD", f) > 1500]
print("topic files:", len(tf), "over 1500:", len(over))
for n, s in over:
    p = f"{CN}/topics/{n}"
    print(f"  {n} {s} base={size(BASE, p)}")
host = [f for f in tf if f.split("/")[-1].startswith("host-")]
print("host topics:", len(host), "total", sum(size("HEAD", f) for f in host), "largest", max(size("HEAD", f) for f in host))
new = [f for f in tf if f not in base_files]
print("topic files new in this diff:", len(new), "largest", max(size("HEAD", f) for f in new))

print("\n== byte-identical copies (blob ids)")
for n in ["floor.md", "hosts/claude-code.json", "hosts/copilot.json"]:
    a = git("rev-parse", f"HEAD:{CN}/{n}").decode().strip()
    b = git("rev-parse", f"{BASE}:skills/chantier/references/{n}").decode().strip()
    print(n, a, b, a == b)

print("\n== topics.json via load_topics")
topics = load_topics(W / CN / "topics.json")
n_read = 0
forms = []
for t in topics.values():
    for r in t.readings:
        fs = list(r.values()) if isinstance(r, dict) else [r]
        n_read += 1
        forms += fs
print("topics:", len(topics), "readings entries:", n_read, "forms:", len(forms))
base_cn = json.loads(git("show", f"{BASE}:{CN}/topics.json"))["topics"]
base_ref = json.loads(git("show", f"{BASE}:skills/chantier/references/topics.json"))["topics"]
print("cards-next topics at base:", len(base_cn), "references topics at base:", len(base_ref))
print("missing references names:", sorted(set(base_ref) - set(topics)))
print("missing cards-next base names:", sorted(set(base_cn) - set(topics)))
roles = set(roles_data.names())
print("roles.yaml roles:", len(roles), "unknown topic roles:", sorted({r for t in topics.values() for r in t.roles} - roles))
rv = [t.name for t in topics.values() if t.review_by]
print("review_by topics:", len(rv), sorted({topics[n].review_by for n in rv}))
fm_base = sorted(n for n, t in base_ref.items() if "foreman" in t["roles"])
print("references foreman rows:", fm_base)
print("  lost the foreman role:", [n for n in fm_base if "foreman" not in topics[n].roles])
role_lost = {n: sorted(set(t["roles"]) - set(topics[n].roles)) for n, t in base_ref.items() if n in topics and set(t["roles"]) - set(topics[n].roles)}
print("  roles lost per references name:", role_lost)
for n in ["writer-off", "mode-switch", "handover", "lost-outside", "lease", "refused-push", "refused-rebase", "direct-mode", "direct", "sync"]:
    t = topics.get(n)
    print(f"  {n}: " + (f"roles={t.roles} review_by={t.review_by} readings={t.readings}" if t else "ABSENT"))
read = {f.partition("#")[0] for f in forms}
print("topic files no topic reads:", [f for f in tf if f[len(CN) + 1:] not in read])
# PR body names
body = Path(r"<CR folder>/pr-body.md").read_text(encoding="utf-8")
m = re.search(r"- All topic names: (.*?)\n## Human decisions", body, re.S)
listed = {x.strip() for x in m[1].replace("\n", " ").strip().rstrip(".").split(",")}
print("PR list:", len(listed), "missing:", sorted(set(topics) - listed), "extra:", sorted(listed - set(topics)))
m = re.search(r"Topics marked `review_by: \"0.16.0\"` \((\d+)\), with the reason:(.*?)\n- All topic names", body, re.S)
named = set()
for line in m[2].split("\n  - "):
    if ":" in line:
        named |= {x.strip(" .;,") for x in line.split(":", 1)[1].replace("\n", " ").split(",")}
named.discard("")
print("PR review_by count:", m[1], "named:", len(named), "missing:", sorted(set(rv) - named), "extra:", sorted(named - set(rv)))

print("\n== help <name> printed by the CLI source at head")
out = git("grep", "-hoE", r"help [a-z][a-z-]*", "HEAD", "--", "skills/chantier/scripts/cli/src").decode().split("\n")
names = sorted({o.split()[1] for o in out if o})
print(names)
print("backticked/CHANTIER help names missing:")
out = git("grep", "-hoE", r"(\$CHANTIER |`chantier |`)help [a-z][a-z-]*", "HEAD", "--", "skills/chantier/scripts/cli/src").decode().split("\n")
print(sorted({o.split()[-1] for o in out if o} - set(topics)))

print("\n== help <topic> names cited in cards-next")
cited = {}
for f in files:
    if not f.endswith((".md", ".json")) or f.endswith(("hosts/claude-code.json", "hosts/copilot.json")):
        continue
    text = git("show", f"HEAD:{f}").decode()
    for mm in re.finditer(r"(?<![A-Za-z-])help ([a-z][a-z0-9]*(?:-[a-z0-9]+)*)(?=[`\s.,;:)\"]|$)", text):
        pre = text[max(0, mm.start() - 14):mm.start()]
        if "$CHANTIER " in pre or pre.endswith("`") or "chantier " in pre:
            cited.setdefault(mm[1], set()).add(f[len(CN) + 1:])
print("cited names:", len(cited), "not in topics.json:", {k: sorted(v) for k, v in cited.items() if k not in topics})

print("\n== relative links under cards-next")
links = []
for f in files:
    if not f.endswith(".md"):
        continue
    text = git("show", f"HEAD:{f}").decode()
    fence = False
    for i, line in enumerate(text.split("\n"), 1):
        if line.lstrip().startswith("```"):
            fence = not fence
            continue
        if fence:
            continue
        for mm in re.finditer(r"\]\(([^)\s]+)\)", line):
            t = mm[1]
            if t.startswith(("http://", "https://", "mailto:")):
                continue
            links.append((f, i, t))
broken, intoref, outside = [], [], []
tree = set(git("ls-tree", "-r", "--name-only", "HEAD").decode().split("\n"))
import posixpath
for f, i, t in links:
    path, _, anchor = t.partition("#")
    rel = f[len(CN) + 1:]
    if rel.startswith("skills/"):
        skill = rel.split("/")[1].replace("-SKILL.md", "")
        r = posixpath.normpath(posixpath.join(f"skills/{skill}", path)) if path else f
        if r.startswith("skills/chantier/references"):
            r = CN + r[len("skills/chantier/references"):]
    elif rel.startswith("forges/") or "/" not in rel:
        base_dir = "skills/chantier/references" + ("/forges" if rel.startswith("forges/") else "")
        r = posixpath.normpath(posixpath.join(base_dir, path)) if path else f
        if r.startswith("skills/chantier/references"):
            if "references" in path:
                intoref.append((rel, i, t))
            r = CN + r[len("skills/chantier/references"):]
    else:
        r = posixpath.normpath(posixpath.join(posixpath.dirname(f), path)) if path else f
        if r.startswith("skills/chantier/references"):
            intoref.append((rel, i, t))
    ok = r in tree or any(x.startswith(r + "/") for x in tree)
    if not ok:
        broken.append((rel, i, t, r))
    elif not r.startswith(CN):
        outside.append((rel, i, t, r))
    if anchor and ok and r.endswith(".md"):
        heads = [re.sub(r"[^a-z0-9 _-]", "", h.lstrip("# ").lower()).replace(" ", "-")
                 for h in git("show", f"HEAD:{r}").decode().split("\n") if h.startswith("#")]
        if anchor not in heads:
            broken.append((rel, i, t, "anchor"))
print("links:", len(links), "broken:", broken, "into references:", intoref)
print("resolve outside cards-next:", outside)

print("\n== Driver table")
old = driver_prompt.driver_table()
real = plugin_files.skill_dir
stage = Path(__file__).parent / "dp"
(stage / "references").mkdir(parents=True, exist_ok=True)
(stage / "references" / "concepts.md").write_bytes(git("show", f"HEAD:{CN}/concepts.md"))
print("old read from:", (real() / "references" / "concepts.md").as_posix())
driver_prompt.skill_dir = lambda: stage
newt = driver_prompt.driver_table()
driver_prompt.skill_dir = real
print("rows old:", len(old), "new:", len(newt), "equal:", old == newt)
for r in newt:
    print("  ", r)
c = git("show", f"HEAD:{CN}/concepts.md").decode()
print("'Change Request' present:", "Change Request" in c, "'## Startup core' present:", "## Startup core" in c)

print("\n== review-step reply block")
def fences(t):
    return re.findall(r"```.*?\n(.*?)```", t, re.S)
a = fences(git("show", f"{BASE}:skills/chantier/references/review-step.md").decode())
b = fences(git("show", f"HEAD:{CN}/review-step.md").decode())
print("fenced blocks old:", len(a), "new:", len(b), "equal:", a == b)

print("\n== completeness table")
inv = Path(r"<CR folder>/evidence/cards-inventory-host-and-shared.md").read_text(encoding="utf-8")
i = inv.lower().find("completeness")
sect = inv[inv.rfind("\n## ", 0, inv.find("\n", inv.lower().rfind("# completeness") if "# completeness" in inv.lower() else i)):]
heads = [(m.start(), m[0]) for m in re.finditer(r"^## .*$", inv, re.M)]
print("headings:", [h for _, h in heads])
start = next(p for p, h in heads if "ompleteness" in h)
end = next((p for p, h in heads if p > start), len(inv))
rows = [l for l in inv[start:end].split("\n") if l.startswith("|")]
refs = [f[len("skills/chantier/references/"):] for f in git("ls-tree", "-r", "--name-only", "HEAD", "skills/chantier/references").decode().split()]
skills = [f for f in tree if re.fullmatch(r"skills/[^/]+/SKILL\.md", f)]
firsts = [l.split("|")[1].strip().strip("`") for l in rows]
def has(x):
    return any(x == f or f.endswith("/" + x) for f in firsts)
print("references files:", len(refs), "SKILL.md:", len(skills), "table rows:", len(rows) - 2)
print("without a row:", [r for r in refs if not has(r)], [s for s in skills if not has(s)])
