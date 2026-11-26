import hashlib, html.parser, json, pathlib, re, sys, urllib.request

work = pathlib.Path(sys.argv[1])
worktree = pathlib.Path(sys.argv[2])
here = work / "verifier" / "r6"
download = here / "dl"
download.mkdir(exist_ok=False)
body = json.loads((here / "pr-540-f9dc2c6-sixth.json").read_text(encoding="utf-8"))["body"]
head = "f9dc2c630b852635e8bffcd0b00b42cc886b293c"
clip = worktree / "docs/demo-video/clips/keyboard-navigation"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "link-check"})
    with urllib.request.urlopen(request, timeout=60) as answer:
        return answer.status, answer.headers.get("Content-Type"), answer.read()


known = {}
for path in sorted((work / "verifier" / "evidence").glob("*.png")):
    known.setdefault(sha(path.read_bytes()), []).append("evidence/" + path.name)
known.setdefault(sha((clip / "keyboard-navigation.gif").read_bytes()), []).append("worktree keyboard-navigation.gif")

print("== images of the posted body, downloaded with no credentials")
for number, (alt, url) in enumerate(re.findall(r"!\[(.*?)\]\((https://[^)\s]+)\)", body), 1):
    status, kind, data = fetch(url)
    (download / f"image-{number}.bin").write_bytes(data)
    print(number, url, status, kind, len(data), sha(data)[:16], "=", known.get(sha(data), ["NO LOCAL MATCH"]))
    print("   alt:", alt)

print("== video links of the posted body")
for url in re.findall(r"https://github\.com/gsemet/[^\s)]+\.(?:mp4|webm)", body):
    status, kind, data = fetch(url)
    local = (clip / url.rsplit("/", 1)[1]).read_bytes()
    print(url.rsplit("/", 1)[1], status, len(data), "at head:", head in url, "same as the worktree file:", data == local)

print("== LFS object ids at the head against the downloaded GIF")
print("sha256 of image 7:", sha((download / "image-7.bin").read_bytes()))


class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.headings, self.heading, self.images, self.tables = [], None, [], []
        self.row, self.cell, self.boxes, self.paragraph, self.paragraphs = None, None, [], None, []

    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if tag in ("h2", "h3"):
            self.heading = []
        if tag == "p":
            self.paragraph = []
        if tag == "table":
            self.tables.append([])
        if tag == "tr":
            self.row = []
        if tag in ("td", "th"):
            self.cell = {"text": [], "images": 0}
        if tag == "img":
            self.images.append((a.get("alt", ""), a.get("src", "").split("?")[0], a.get("data-canonical-src", "").split("?")[0]))
            if self.cell is not None:
                self.cell["images"] += 1
        if tag == "input" and a.get("type") == "checkbox":
            self.boxes.append("checked" in a)

    def handle_endtag(self, tag):
        if tag in ("h2", "h3") and self.heading is not None:
            self.headings.append("".join(self.heading).strip())
            self.heading = None
        if tag == "p" and self.paragraph is not None:
            self.paragraphs.append(" ".join("".join(self.paragraph).split()))
            self.paragraph = None
        if tag in ("td", "th") and self.cell is not None:
            self.row.append((" ".join("".join(self.cell["text"]).split()), self.cell["images"]))
            self.cell = None
        if tag == "tr" and self.row is not None:
            self.tables[-1].append(self.row)
            self.row = None

    def handle_data(self, data):
        if self.heading is not None:
            self.heading.append(data)
        if self.cell is not None:
            self.cell["text"].append(data)
        if self.paragraph is not None:
            self.paragraph.append(data)


page = Page()
page.feed((here / "pr-540-body.html").read_text(encoding="utf-8"))
print("== rendered HTML of the body")
print("headings:", page.headings)
for table in page.tables:
    print("table rows:", len(table), "cells per row:", [len(r) for r in table], "images per row:", [sum(c[1] for c in r) for r in table])
print("images:", len(page.images))
for alt, src, canonical in page.images:
    print("  ", src, "| canonical:", canonical or "-", "|", alt[:60])
print("check boxes:", page.boxes)
for text in page.paragraphs:
    if text.startswith(("Screenshots from", "The re-filmed")):
        print("-", text)
