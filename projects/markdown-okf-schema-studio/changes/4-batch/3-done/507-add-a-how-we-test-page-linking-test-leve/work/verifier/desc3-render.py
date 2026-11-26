import re, sys
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.c = {}; self.h = []; self.imgs = []; self.cur = None; self.paras = []; self.buf = None; self.boxes = []
    def handle_starttag(self, t, a):
        a = dict(a); self.c[t] = self.c.get(t, 0) + 1
        if t in ("h1", "h2", "h3"): self.cur = [t, ""]
        if t == "img": self.imgs.append((a.get("alt"), a.get("data-canonical-src") or a.get("src")))
        if t == "p": self.buf = ""
        if t == "input": self.boxes.append((a.get("type"), "checked" in a))
        if t == "br" and self.buf is not None: self.buf += " "
    def handle_endtag(self, t):
        if self.cur and t == self.cur[0]: self.h.append(tuple(self.cur)); self.cur = None
        if t == "p" and self.buf is not None: self.paras.append(" ".join(self.buf.split())); self.buf = None
    def handle_data(self, d):
        if self.cur: self.cur[1] += d
        if self.buf is not None: self.buf += d

for name in sys.argv[1:]:
    s = open(name, encoding="utf-8").read(); p = P(); p.feed(s)
    print("==", name.rsplit("/", 1)[-1])
    print("headings:", [h[1].strip() for h in p.h])
    print("counts:", {k: p.c.get(k, 0) for k in ("table", "tr", "ul", "li", "input", "img", "p", "br", "details", "pre")})
    print("task boxes:", len(p.boxes), "all checked:", all(b[1] for b in p.boxes))
    print("mermaid:", len(re.findall(r'data-type="mermaid"|lang="mermaid"', s)))
    for alt, src in p.imgs: print("img:", repr(alt), src.rsplit("/", 2)[-2][:7], src.rsplit("/", 1)[-1])
    i = next(i for i, t in enumerate(p.paras) if t.startswith("Header before"))
    for t in p.paras[i:i + 8]: print("p:", t)
    print("literal markup left:", re.findall(r">[^<]*(?:\*\*|\]\(|!\[)[^<]*<", s))
