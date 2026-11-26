import json
import posixpath
import re
import subprocess
import sys
from pathlib import Path

W = Path("<worktree>")
CR = Path("<CR folder>")
BASE = "24111e6d9920a7ff3e8f210613186dd65d802ec8"
PREV = "03f973e4f0d0756c9b5fa77ed0f888f941745dbe"
CN = "skills/chantier/cards-next"
sys.dont_write_bytecode = True

from chantier import driver_prompt, plugin_files, roles_data  # noqa: E402
from chantier.commands.help import load_topics  # noqa: E402

print("module under test:", Path(driver_prompt.__file__).as_posix())


def git(*a):
    return subprocess.run(["git", *a], cwd=W, capture_output=True, check=True).stdout


def size(rev, path):
    d = subprocess.run(["git", "cat-file", "-s", f"{rev}:{path}"], cwd=W, capture_output=True)
    return int(d.stdout) if d.returncode == 0 else None


print("HEAD", git("rev-parse", "HEAD").decode().strip(), "status:", repr(git("status", "--porcelain").decode()))
files = git("ls-tree", "-r", "--name-only", "HEAD", CN).decode().split()
base_files = set(git("ls-tree", "-r", "--name-only", BASE, CN).decode().split())
tree = set(git("ls-tree", "-r", "--name-only", "HEAD").decode().split("\n"))

print("\n== encoding (BOM, CRLF, utf-8) over added/changed files")
changed = [l.split("\t") for l in git("diff", "--no-renames", "--name-status", f"{BASE}..HEAD").decode().splitlines()]
bad = []
for st, p in changed:
    b = git("show", f"HEAD:{p}")
    if b.startswith(b"\xef\xbb\xbf") or b"\r\n" in b:
        bad.append(p)
    b.decode("utf-8")
print("files:", len(changed), "BOM or CRLF:", bad, "deleted:", [p for s, p in changed if s == "D"])
print("tests touched:", [p for s, p in changed if re.search(r"(^|/)tests/", p)])
print("outside cards-next:", [(s, p) for s, p in changed if not p.startswith(CN + "/")])

print("\n== role cards at head")
budgets = {"foreman": 4000, "chief-of-staff": 6000, "griller-skill": 4000, "griller": 2000,
           "coder": 1500, "conflict-resolver": 1500, "debugger": 1500, "demo-explorer": 1500,
           "investigator": 1500, "retro-critic": 1500, "spec-critic": 1500, "spec-writer": 1500,
           "inspector": 2000, "verifier": 3000, "cr-driver": 4096, "stack-driver": 4096,
           "release-driver": 3072, "qa-driver": 2048, "floor": 1200, "review-step": 1500}
for n, t in budgets.items():
    s = size("HEAD", f"{CN}/{n}.md")
    r = size(BASE, f"skills/chantier/references/{n}.md")
    print(f"{n}.md head={s} prev={size(PREV, f'{CN}/{n}.md')} base-next={size(BASE, f'{CN}/{n}.md')} ref={r} target={t} " + ("within" if s <= t else f"OVER by {s - t}"))
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
    print(f"  {n[:-3]} {s:,} base={size(BASE, p)}")
host = [f for f in tf if f.split("/")[-1].startswith("host-")]
hs = [(size("HEAD", f), f.split("/")[-1]) for f in host]
print("host topics:", len(host), "total", sum(s for s, _ in hs), "largest", max(hs))
other = [f for f in tf if f not in host]
print("other topics:", len(other), "total", sum(size("HEAD", f) for f in other))
new = [f for f in tf if f not in base_files]
print("topic files new since base:", len(new), "largest", max((size("HEAD", f), f.split('/')[-1]) for f in new),
      "new over 1500:", [f for f in new if size("HEAD", f) > 1500])

print("\n== byte-identical copies (blob ids)")
for n in ["floor.md", "hosts/claude-code.json", "hosts/copilot.json"]:
    a = git("rev-parse", f"HEAD:{CN}/{n}").decode().strip()
    b = git("rev-parse", f"HEAD:skills/chantier/references/{n}").decode().strip()
    c = git("hash-object", f"{CN}/{n}").decode().strip()
    d = git("hash-object", f"skills/chantier/references/{n}").decode().strip()
    print(n, "HEAD", a, b, a == b, "hash-object", c, d, c == d)

print("\n== topics.json via load_topics")
topics = load_topics(W / CN / "topics.json")
n_read = 0
forms = []
unresolved = []
from chantier.commands import help as h  # noqa: E402
for t in topics.values():
    for r in t.readings:
        fs = list(r.values()) if isinstance(r, dict) else [r]
        n_read += 1
        forms += fs
        for f in fs:
            path, _, heading = f.partition("#")
            p = W / CN / path
            if not p.is_file():
                unresolved.append((t.name, f))
            elif heading and ("\n## " + heading) not in ("\n" + p.read_text(encoding="utf-8")):
                unresolved.append((t.name, f))
print("topics:", len(topics), "readings entries:", n_read, "forms:", len(forms), "unresolved:", unresolved)
base_cn = json.loads(git("show", f"{BASE}:{CN}/topics.json"))["topics"]
base_ref = json.loads(git("show", f"{BASE}:skills/chantier/references/topics.json"))["topics"]
prev_cn = json.loads(git("show", f"{PREV}:{CN}/topics.json"))["topics"]
head_cn = json.loads(git("show", f"HEAD:{CN}/topics.json"))["topics"]
print("cards-next topics at base:", len(base_cn), "references topics at base:", len(base_ref), "at prev head:", len(prev_cn))
print("missing references names:", sorted(set(base_ref) - set(topics)))
print("missing cards-next base names:", sorted(set(base_cn) - set(topics)))
print("names at prev not at head:", sorted(set(prev_cn) - set(topics)))
print("names new since prev:", sorted(set(topics) - set(prev_cn)))
roles = set(roles_data.names())
print("roles.yaml roles:", len(roles), "unknown topic roles:", sorted({r for t in topics.values() for r in t.roles} - roles))
rv = [t.name for t in topics.values() if t.review_by]
print("review_by topics:", len(rv), sorted({topics[n].review_by for n in rv}))
role_lost = {n: sorted(set(t["roles"]) - set(topics[n].roles)) for n, t in base_ref.items() if n in topics and set(t["roles"]) - set(topics[n].roles)}
print("roles lost per references name:", role_lost)
fm_prev = {n: sorted(set(t["roles"]) - set(topics[n].roles)) for n, t in prev_cn.items() if n in topics and set(t["roles"]) - set(topics[n].roles)}
print("roles lost since prev head:", fm_prev)
read = {f.partition("#")[0] for f in forms}
print("topic files no topic reads:", [f for f in tf if f[len(CN) + 1:] not in read])
for n in ["sync", "direct-mode", "direct-mode-switch", "mode-switch", "ready-asks", "ask-lines", "order-verbs", "order-drop", "worker-shell", "session-shell", "cr-review-step", "long-gate", "refused-push", "titles"]:
    t = topics.get(n)
    print(f"  {n}: " + (f"roles={t.roles} readings={t.readings} trigger={head_cn[n].get('trigger')}" if t else "ABSENT"))

body = (CR / "pr-body.md").read_text(encoding="utf-8")
m = re.search(r"- All topic names: (.*?)\n## The user's boundaries", body, re.S)
listed = [x.strip() for x in m[1].replace("\n", " ").strip().rstrip(".").split(",")]
print("PR list:", len(listed), "dups:", len(listed) - len(set(listed)), "missing:", sorted(set(topics) - set(listed)), "extra:", sorted(set(listed) - set(topics)))
m = re.search(r"Topics marked `review_by: \"0.16.0\"` \((\d+)\), with the reason:(.*?)\n- All topic names", body, re.S)
named = set()
groups = re.split(r"\n  - ", m[2])[1:]
for line in groups:
    label, _, names = line.partition(":")
    got = {x.strip(" .;,") for x in names.replace("\n", " ").split(",")} - {""}
    print("  group:", label[:90].replace("\n", " "), len(got))
    named |= got
print("PR review_by count:", m[1], "named:", len(named), "missing:", sorted(set(rv) - named), "extra:", sorted(named - set(rv)))
print("  from base cards-next/references: review_by names also at base refs:", sorted(set(rv) & set(base_ref)))

print("\n== help <name> printed by the CLI source at head")
out = git("grep", "-hoE", r"(\$CHANTIER |`chantier |`)help [a-z][a-z-]*", "HEAD", "--", "skills/chantier/scripts/cli/src").decode().split("\n")
print("CLI-cited missing:", sorted({o.split()[-1] for o in out if o} - set(topics)))

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
        heads = [re.sub(r"[^a-z0-9 _-]", "", x.lstrip("# ").lower()).replace(" ", "-")
                 for x in git("show", f"HEAD:{r}").decode().split("\n") if x.startswith("#")]
        if anchor not in heads:
            broken.append((rel, i, t, "anchor"))
print("links:", len(links), "broken:", broken, "into references:", intoref)
print("resolve outside cards-next:", outside)
linked = {posixpath.basename(t.partition('#')[0]) for _, _, t in links}
for n in ["release-template.md", "routing.md", "claude-code.md", "griller-skill.md"]:
    mentions = []
    for f in files:
        if f.endswith(".md"):
            text = git("show", f"HEAD:{f}").decode()
            if n in text:
                mentions.append(f[len(CN) + 1:])
    print(f"  {n}: linked={n in linked} named in={mentions[:8]}")

print("\n== Driver table")
old = driver_prompt.driver_table()
real = plugin_files.skill_dir
stage = Path(__file__).parent / "dp"
(stage / "references").mkdir(parents=True, exist_ok=True)
(stage / "references" / "concepts.md").write_bytes(git("show", f"HEAD:{CN}/concepts.md"))
driver_prompt.skill_dir = lambda: stage
newt = driver_prompt.driver_table()
driver_prompt.skill_dir = real
print("rows old:", len(old), "new:", len(newt), "equal:", old == newt)
c = git("show", f"HEAD:{CN}/concepts.md").decode()
print("'Change Request' present:", c.count("Change Request"))

print("\n== review-step reply block")
def fences(t):
    return re.findall(r"```.*?\n(.*?)```", t, re.S)
a = fences(git("show", f"{BASE}:skills/chantier/references/review-step.md").decode())
b = fences(git("show", f"HEAD:{CN}/review-step.md").decode())
print("fenced blocks old:", len(a), "new:", len(b), "equal:", a == b)

print("\n== skills: frontmatter and version line")
ver = re.search(r'__version__ = "([^"]+)"', git("show", "HEAD:skills/chantier/scripts/cli/src/chantier/__init__.py").decode())
print("__version__", ver[1] if ver else None)
for n in ["chantier", "chief-of-staff", "griller", "status"]:
    old_t = git("show", f"{BASE}:skills/{n}/SKILL.md").decode()
    new_t = git("show", f"HEAD:{CN}/skills/{n}-SKILL.md").decode()
    fm = lambda t: t.split("---")[1]
    print(n, "frontmatter equal:", fm(old_t) == fm(new_t), "version lines:", re.findall(r"chantier-version: (\S+)", new_t))

print("\n== completeness table")
inv = (CR / "evidence/cards-inventory-host-and-shared.md").read_text(encoding="utf-8")
heads = [(mm.start(), mm[0]) for mm in re.finditer(r"^## .*$", inv, re.M)]
start = next(p for p, x in heads if "ompleteness" in x)
end = next((p for p, x in heads if p > start), len(inv))
rows = [l for l in inv[start:end].split("\n") if l.startswith("|")]
refs = [f[len("skills/chantier/references/"):] for f in git("ls-tree", "-r", "--name-only", "HEAD", "skills/chantier/references").decode().split()]
skills = [f for f in tree if re.fullmatch(r"skills/[^/]+/SKILL\.md", f)]
firsts = [l.split("|")[1].strip().strip("`") for l in rows]
def has(x):
    return any(x == f or f.endswith("/" + x) for f in firsts)
print("references files:", len(refs), "SKILL.md:", len(skills), "table rows:", len(rows) - 2)
print("without a row:", [r for r in refs if not has(r)], [s for s in skills if not has(s)])
# every topic named in the completeness table exists
named_topics = set()
for l in rows:
    for mm in re.finditer(r"topics/([a-z0-9-]+)\.md", l):
        named_topics.add(mm[1])
    mm = re.search(r"split into topics ([^|]+)", l)
    if mm:
        named_topics |= set(re.findall(r"`?([a-z][a-z0-9-]*-?[a-z0-9]+)`?", mm[1].split("(")[0]))
files_set = {f.split("/")[-1][:-3] for f in tf}
print("completeness names not a topic file or topic:", sorted(x for x in named_topics if x not in files_set and x not in topics))
