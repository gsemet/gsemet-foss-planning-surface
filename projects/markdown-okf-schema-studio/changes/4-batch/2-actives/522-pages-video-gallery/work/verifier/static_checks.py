"""Verifier's own static checks of the built site, the README and the VSIX (stdlib only).

Usage: python -I static_checks.py <worktree>
"""
import hashlib
import json
import posixpath
import re
import subprocess
import sys
import zipfile
from html.parser import HTMLParser
from pathlib import Path

root = Path(sys.argv[1])
site = root / "out" / "site"
failures = []


def check(ok, message):
    print(("ok   " if ok else "FAIL ") + message)
    if not ok:
        failures.append(message)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.figures = []
        self.nav = []
        self.navs = 0
        self.scripts = []
        self.h1 = []
        self.stack = []
        self.figure = None
        self.in_nav = False
        self.autoplay = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "autoplay" in attrs:
            self.autoplay += 1
        if tag == "nav" and attrs.get("class") == "site":
            self.in_nav = True
            self.navs += 1
        if tag == "a" and self.in_nav:
            self.nav.append([attrs.get("href"), ""])
        if tag == "figure":
            self.figure = {"id": attrs.get("id"), "videos": [], "sources": [], "h2": "", "p": "", "links": []}
            self.figures.append(self.figure)
        if self.figure is not None:
            if tag == "video":
                self.figure["videos"].append(attrs)
            if tag == "source":
                self.figure["sources"].append(attrs)
            if tag == "a":
                self.figure["links"].append(attrs.get("href"))
        if tag == "script":
            self.scripts.append("")
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "nav":
            self.in_nav = False
        if tag == "figure":
            self.figure = None
        while self.stack:
            if self.stack.pop() == tag:
                break

    def handle_data(self, data):
        if not self.stack:
            return
        top = self.stack[-1]
        if self.in_nav and top == "a":
            self.nav[-1][1] += data
        if self.figure is not None and "figcaption" in self.stack and top in ("h2", "p"):
            self.figure[top] += data
        if top == "script":
            self.scripts[-1] += data
        if top == "h1":
            self.h1.append(data)


def parse(path):
    page = Page()
    page.feed(path.read_text(encoding="utf-8"))
    return page


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


print("== (1) videos.html")
videos_page = parse(site / "videos.html")
clips_root = root / "docs/demo-video/clips"
expected = sorted(d.name for d in clips_root.iterdir() if d.is_dir() and (d / f"{d.name}.webm").is_file())
print(f"clip folders: {len([d for d in clips_root.iterdir() if d.is_dir()])}, with <clip>.webm: {len(expected)}")
ids = [f["id"] for f in videos_page.figures]
print("card ids in page order:", ids)
check(len(videos_page.figures) == 18, f"18 cards (found {len(videos_page.figures)})")
check(ids[:1] == ["short-demo-01"], "presentation video first")
check(ids[1:] == expected and len(expected) == 17, "then the 17 clips in name order, one per folder with a WebM")
check(videos_page.autoplay == 0 and "autoplay" not in (site / "videos.html").read_text(encoding="utf-8"), "no autoplay anywhere on the page")
check(videos_page.h1 == ["Videos"], f"h1 is Videos ({videos_page.h1})")
check(len(videos_page.scripts) == 1, f"one script on the page ({len(videos_page.scripts)})")
for figure in videos_page.figures:
    name = figure["id"]
    clip = name != "short-demo-01"
    folder = f"docs/demo-video/clips/{name}" if clip else "docs/demo-video/short-demo-01/output"
    media = f"{folder}/{name}.{'webm' if clip else 'mp4'}"
    poster = f"{folder}/poster.png"
    v = figure["videos"]
    ok = (
        len(v) == 1
        and "controls" in v[0]
        and v[0].get("preload") == "none"
        and "playsinline" in v[0]
        and "autoplay" not in v[0]
        and v[0].get("poster") == poster
        and ("loop" in v[0]) == clip
        and ("muted" in v[0]) == clip
        and figure["sources"] == [{"src": media, "type": "video/webm" if clip else "video/mp4"}]
        and figure["links"] == [media]
    )
    files = all(
        (site / p).is_file() and sha(site / p) == sha(root / p) and (root / p).read_bytes()[:40] != b"version https://git-lfs.github.com/spec/v1"[:40]
        for p in (media, poster)
    )
    title = "One-minute demo"
    if clip:
        text = (root / folder / "clip.md").read_text(encoding="utf-8")
        row = re.search(r"^\|\s*Text 1 \*\(on screen\)\*\s*\|(.*?)\|\s*$", text, re.M)
        title = row.group(1).replace("**", "").strip() if row else name
    texts = figure["h2"] == title and figure["p"] == name
    check(ok and files and texts, f"card {name}: controls preload=none playsinline poster, no autoplay, loop+muted={clip}, source+fallback {media.rsplit('/', 1)[1]}, site files equal repo files, title {figure['h2']!r}")
manifest = json.loads((site / "site-manifest.json").read_text(encoding="utf-8"))
check("videos.html" in manifest["pages"] and "og/videos.png" in manifest["cards"], "site-manifest.json lists videos.html and og/videos.png")
check((site / "og/videos.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", "og/videos.png is a PNG")
html = (site / "videos.html").read_text(encoding="utf-8")
meta = re.findall(r'<meta (?:property|name)="((?:og|twitter):(?:title|description|image))" content="([^"]*)"', html)
for key, value in meta:
    print(f"     meta {key} = {value}")
check(any(k == "og:image" and v.endswith("og/videos.png") for k, v in meta) and any("18 videos" in v for _, v in meta), "social tags name og/videos.png and the count 18")

print("== (3) site header on the built pages")
want = ["Home", "Contributing", "How we ship", "How we test", "Gallery", "Videos", "Requirements"]
with_header, without = [], []
bad = []
for path in sorted(site.rglob("*.html")):
    page = parse(path)
    rel = path.relative_to(site).as_posix()
    if page.navs == 0:
        without.append(rel)
        continue
    with_header.append(rel)
    names = [t for _, t in page.nav]
    targets = []
    for href, _ in page.nav:
        target = posixpath.normpath(posixpath.join(posixpath.dirname(rel), href))
        if target == "." or href.endswith("/"):
            target = posixpath.normpath(posixpath.join(target, "index.html"))
        targets.append(target)
    wanted_targets = ["index.html", "contributing.html", "docs/how-we-ship.html", "docs/how-we-test.html", "gallery.html", "videos.html", "requirements/index.html"]
    if page.navs != 1 or names != want or targets != wanted_targets or not all((site / t).is_file() for t in targets):
        bad.append((rel, names, targets))
print(f"html files: {len(with_header) + len(without)}, with the site header: {len(with_header)}, without: {len(without)}")
print("without header:", without[:20])
print("of which requirements pages with header:", len([p for p in with_header if p.startswith("requirements/")]))
for item in ("index.html", "contributing.html", "docs/how-we-ship.html", "docs/how-we-test.html", "gallery.html", "videos.html", "requirements/index.html", "reports/index.html"):
    check(item in with_header, f"{item} carries the header")
check(not bad, f"every header holds the seven links in order {want}, each resolving to the right existing file ({len(bad)} bad) {bad[:3]}")
print("videos.html header:", parse(site / "videos.html").nav)

print("== (4) README.md at head")
blob = subprocess.run(["git", "-C", str(root), "show", "HEAD:README.md"], capture_output=True, check=True).stdout.decode("utf-8")
lines = blob.replace("\r\n", "\n").split("\n")
section, fence, images = None, False, []
for number, line in enumerate(lines, 1):
    if line.startswith("```") or line.startswith("~~~"):
        fence = not fence
    if not fence and re.match(r"^#{2,3} ", line):
        section = line.lstrip("# ").strip()
    if not fence:
        for alt, target in re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", line):
            images.append((number, section, alt, target))
gifs = {
    "table-anchors": "Highest respect for the raw Markdown",
    "slash-menu-grid": "Edit MyST visually",
    "figure-editor": "Edit MyST visually",
    "diff-side-by-side": "See what changed since the last commit",
    "radio-buttons": "Decide in the page: choices in your plans",
}
shown = [i for i in images if i[3].endswith(".gif")]
for i in shown:
    print(f"     line {i[0]} section {i[1]!r}: {i[3]}")
check(len(shown) == 5, f"exactly five GIF images in README ({len(shown)})")
total = 0
for clip, title in gifs.items():
    target = f"docs/demo-video/clips/{clip}/{clip}.gif"
    found = [i for i in shown if i[3] == target]
    data = (root / target).read_bytes()
    total += len(data)
    text = (root / f"docs/demo-video/clips/{clip}/clip.md").read_text(encoding="utf-8")
    t1, t2 = (re.search(rf"^\|\s*Text {n} \*\(on screen\)\*\s*\|(.*?)\|\s*$", text, re.M).group(1).replace("**", "").strip() for n in (1, 2))
    alt = found[0][2] if found else ""
    from_texts = t1.rstrip(".") in alt and t2.rstrip(".") in alt
    check(len(found) == 1 and found[0][1] == title and data[:6] in (b"GIF89a", b"GIF87a") and from_texts, f"{clip}: once, in {title!r}, real GIF {len(data)} bytes, alt {alt!r} holds Text 1 {t1!r} and Text 2 {t2!r}")
print(f"     five GIFs total: {total} bytes = {total / 1e6:.2f} MB ({total / 2**20:.2f} MiB)")
for still in ("showcase-diff-cream.png", "radio-plan-cream.png", "radio-plan-dark.png"):
    check(still not in blob and (root / "images/readme" / still).is_file(), f"{still}: no longer referenced, file kept")
base = subprocess.run(["git", "-C", str(root), "show", "origin/main:README.md"], capture_output=True, check=True).stdout.decode("utf-8")
check(all(still in base for still in ("showcase-diff-cream.png", "radio-plan-cream.png", "radio-plan-dark.png")) and ".gif" not in base, "origin/main README referenced the three stills and no GIF")
first_h2 = next(n for n, line in enumerate(lines, 1) if line.startswith("## "))
demo = next(n for n, line in enumerate(lines, 1) if line == "**One-minute demo**")
link = next(n for n, line in enumerate(lines, 1) if n > demo and line.startswith("https://github.com/user-attachments/assets/"))
check(demo < link < first_h2, f"demo title line {demo} and link line {link} come before the first '## ' heading at line {first_h2}: {lines[first_h2 - 1]!r}")
base_lines = base.replace("\r\n", "\n").split("\n")
check(lines[link - 1] in base_lines, "demo link unchanged from origin/main")
top = next((n, line) for n, line in enumerate(lines, 1) if line.startswith("[VS Code Marketplace]"))
check(top[0] < demo and "gallery.html) | [Videos](https://gsemet.github.io/markdown-okf-schema-studio/videos.html) | [Requirements]" in top[1], f"top line {top[0]} links videos.html after the gallery link")
edit = [i for i in images if i[1] == "Edit MyST visually"]
names_now = [i[3].rsplit("/", 1)[1] for i in edit]
base_section = base.replace("\r\n", "\n").split("\n### Edit MyST visually\n")[1].split("\n##")[0]
names_base = [t.rsplit("/", 1)[1] for t in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", base_section)]
at = names_base.index("showcase-myst-edit.png") + 1
check(names_now == names_base[:at] + ["slash-menu-grid.gif", "figure-editor.gif"] + names_base[at:], f"Edit MyST visually keeps every image of origin/main {names_base}, the two GIFs right after the editing still: {names_now}")
for _, title, _, target in shown:
    if "slash-menu" in target or "figure-editor" in target:
        n = next(i[0] for i in shown if i[3] == target)
        check(lines[n - 2] == "" and lines[n - 3].rstrip().endswith(":"), f"lead-in line above {target.rsplit('/', 1)[1]}: {lines[n - 3]!r}")
diff = subprocess.run(["git", "-C", str(root), "diff", "-U0", "origin/main...HEAD", "--", "README.md"], capture_output=True, check=True).stdout.decode("utf-8")
long = [l[1:] for l in diff.split("\n") if l.startswith("+") and not l.startswith("+++") and len(l) - 1 > 100 and not l[1:].startswith(("![", "|", "[VS Code"))]
check(not long, f"no added prose line over 100 columns {long}")

print("== (5) VSIX")
vsix = root / "out/reports/package/markdown-okf-schema-studio.vsix"
version = json.loads((root / "package.json").read_text(encoding="utf-8"))["version"]
with zipfile.ZipFile(vsix) as archive:
    names = archive.namelist()
    readme_name = next(n for n in names if n.lower() == "extension/readme.md")
    packaged = archive.read(readme_name).decode("utf-8")
print(f"VSIX {vsix.name}: {len(names)} entries, readme entry {readme_name}, package version {version}")
urls = [u for u in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", packaged) if u.endswith(".gif")]
for url in urls:
    print("     " + url)
prefix = f"https://media.githubusercontent.com/media/gsemet/markdown-okf-schema-studio/v{version}/docs/demo-video/clips/"
check(sorted(urls) == sorted(f"{prefix}{c}/{c}.gif" for c in gifs), f"the five GIFs point to media.githubusercontent.com at tag v{version}")
check(not re.search(r"\]\(docs/demo-video", packaged), "no relative docs/demo-video image or link left in the packaged readme")
leaked = [n for n in names if "demo-video" in n or n.endswith((".gif", ".webm", ".mp4"))]
check(not leaked, f"nothing from docs/demo-video, no gif/webm/mp4 in the VSIX {leaked[:5]}")
docs = sorted({n for n in names if n.startswith("extension/docs/")})
print("     VSIX docs entries:", docs)
check("[Videos](https://gsemet.github.io/markdown-okf-schema-studio/videos.html)" in packaged, "packaged readme top line links videos.html")
print()
print(f"failures: {len(failures)}")
sys.exit(1 if failures else 0)
