import hashlib, html.parser, json, pathlib, re, sys, urllib.request

work = pathlib.Path(sys.argv[1])
worktree = pathlib.Path(sys.argv[2])
here = work / "verifier" / "r5"
download = here / "dl"
download.mkdir(exist_ok=False)
body = json.loads((here / "pr-540-f9dc2c6-closing.json").read_text(encoding="utf-8"))["body"]


def sha(data):
    return hashlib.sha256(data).hexdigest()


known = {}
for path in sorted((work / "verifier" / "evidence").glob("*.png")):
    known.setdefault(sha(path.read_bytes()), []).append("evidence/" + path.name)
gif = "docs/demo-video/clips/keyboard-navigation/keyboard-navigation.gif"
known.setdefault(sha((worktree / gif).read_bytes()), []).append("worktree " + gif)
known.setdefault(sha((work / "attach" / "keyboard-navigation.gif").read_bytes()), []).append("work/attach/keyboard-navigation.gif")

print("== downloads of the attachment links of the posted body, no credentials")
for number, (alt, url) in enumerate(re.findall(r"!\[(.*?)\]\((https://github\.com/user-attachments/assets/[0-9a-f-]+)\)", body), 1):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "link-check"}), timeout=60) as answer:
        data = answer.read()
        status, kind = answer.status, answer.headers.get("Content-Type")
    (download / f"image-{number}.bin").write_bytes(data)
    print(number, url.rsplit("/", 1)[1], status, kind, len(data), sha(data)[:16], "=", known.get(sha(data), ["NO LOCAL MATCH"]))
    print("   alt:", alt)

print("== title pairs")
for pair in ("alert-title-click", "admonition-title-click"):
    before = (work / "verifier" / "evidence" / f"before-{pair}.png").read_bytes()
    after = (work / "verifier" / "evidence" / f"after-{pair}.png").read_bytes()
    print(pair, "before == after:", before == after, sha(before)[:16], sha(after)[:16])

print("== video links of the posted body")
for url in re.findall(r"https://github\.com/gsemet/[^\s)]+\.(?:mp4|webm)", body):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "link-check"}), timeout=60) as answer:
        data = answer.read()
        status = answer.status
    local = (worktree / "docs/demo-video/clips/keyboard-navigation" / url.rsplit("/", 1)[1]).read_bytes()
    print(url.rsplit("/", 1)[1], status, len(data), "same as the worktree file:", data == local)


class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.headings, self.heading, self.images, self.tables = [], None, [], []
        self.row, self.cell, self.items, self.stack, self.boxes = None, None, [], [], []

    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if tag in ("h2", "h3"):
            self.heading = []
        if tag == "table":
            self.tables.append([])
        if tag == "tr":
            self.row = []
        if tag in ("td", "th"):
            self.cell = {"text": [], "images": 0}
        if tag == "img":
            self.images.append((a.get("alt", ""), a.get("src", "").split("?")[0]))
            if self.cell is not None:
                self.cell["images"] += 1
        if tag == "li":
            self.stack.append([])
        if tag == "input" and a.get("type") == "checkbox":
            self.boxes.append("checked" in a)

    def handle_endtag(self, tag):
        if tag in ("h2", "h3") and self.heading is not None:
            self.headings.append("".join(self.heading).strip())
            self.heading = None
        if tag in ("td", "th") and self.cell is not None:
            self.row.append((" ".join("".join(self.cell["text"]).split()), self.cell["images"]))
            self.cell = None
        if tag == "tr" and self.row is not None:
            self.tables[-1].append(self.row)
            self.row = None
        if tag == "li" and self.stack:
            self.items.append(" ".join("".join(self.stack.pop()).split()))

    def handle_data(self, data):
        if self.heading is not None:
            self.heading.append(data)
        if self.cell is not None:
            self.cell["text"].append(data)
        if self.stack:
            self.stack[-1].append(data)


page = Page()
page.feed((here / "pr-540-body.html").read_text(encoding="utf-8"))
print("== rendered HTML of the body")
print("headings:", page.headings)
for table in page.tables:
    print("table rows:", len(table), "cells per row:", [len(r) for r in table])
    for r in table:
        print("  ", r)
print("images:", len(page.images))
for alt, src in page.images:
    print("  ", src, "|", alt[:70])
print("check boxes:", page.boxes)
for item in page.items:
    if item.startswith(("New or changed tests", "Requirements, at", "Changelog, at", "Local gates", "Review:", "CI green")):
        print("-", item[:200])
