"""Check every #anchor link of README.md, docs/*.md and CONTRIBUTING.md, and that files added under
docs/ are named in README or a docs page. Usage: python check_anchors.py <repo root>"""
import re, sys, pathlib

root = pathlib.Path(sys.argv[1]).resolve()
BLOB = "https://github.com/gsemet/chantier/blob/main/"
RAW = "https://github.com/gsemet/chantier"
files = [root / "README.md", root / "CONTRIBUTING.md", *sorted((root / "docs").glob("*.md"))]
helpjs = root / "skills/chantier/scripts/cli/src/chantier/clients/web/js/views/help-topics.js"


def slug(h):
    h = re.sub(r"`", "", h.strip().lower())
    h = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", h)
    h = re.sub(r"[^\w\- ]", "", h, flags=re.U)
    return h.replace(" ", "-")


def anchors(path):
    out, seen, fence = set(), {}, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("```"):
            fence = not fence
        m = None if fence else re.match(r"#{1,6}\s+(.*)", line)
        if m:
            s = slug(m.group(1))
            n = seen.get(s, 0)
            seen[s] = n + 1
            out.add(s if n == 0 else f"{s}-{n}")
    return out


cache = {}
bad = 0
n = 0


def check(src, target):
    global bad, n
    if target.startswith(BLOB):
        rel = target[len(BLOB):]
    elif target.startswith(RAW):
        rel = "README.md" + target[len(RAW):] if target[len(RAW):].startswith("#") else None
        if rel is None:
            return
    elif re.match(r"\w+://", target) or target.startswith("mailto:"):
        return
    else:
        rel = None
    path, _, frag = (rel if rel is not None else target).partition("#")
    if rel is None:
        dest = (src.parent / path).resolve() if path else src
    else:
        dest = (root / path).resolve()
    n += 1
    if not dest.exists():
        print(f"MISSING FILE {src.relative_to(root)} -> {target}")
        bad += 1
        return
    if frag and dest.suffix == ".md":
        if dest not in cache:
            cache[dest] = anchors(dest)
        if frag not in cache[dest]:
            print(f"BAD ANCHOR  {src.relative_to(root)} -> {target}")
            bad += 1


for f in files:
    text = f.read_text(encoding="utf-8")
    for m in re.finditer(r"\]\(([^)\s]+)\)", text):
        check(f, m.group(1))
for m in re.finditer(r"'(https://github\.com/gsemet/chantier[^']*)'", helpjs.read_text(encoding="utf-8")):
    check(root / "README.md", m.group(1))

corpus = "".join(f.read_text(encoding="utf-8") for f in files)
for p in sorted((root / "docs").iterdir()):
    if p.is_file() and p.suffix == ".md" and not p.name.endswith("-texts.md"):
        if p.name not in corpus.replace(f"docs/{p.name}", p.name) or (
            p.name != "README.md" and f"{p.name}" not in (root / "README.md").read_text(encoding="utf-8")
            and not any(p.name in f.read_text(encoding="utf-8") for f in files if f != p)
        ):
            print(f"UNLINKED    docs/{p.name}")
            bad += 1
print(f"{n} links checked, {bad} problem(s)")
sys.exit(1 if bad else 0)
