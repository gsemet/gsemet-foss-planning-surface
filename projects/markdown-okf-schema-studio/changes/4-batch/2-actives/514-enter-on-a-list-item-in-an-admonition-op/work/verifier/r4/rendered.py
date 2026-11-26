import sys, html.parser, pathlib
class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(); self.stack=[]; self.items=[]; self.heads=[]; self.h=None
    def handle_starttag(self, t, a):
        if t=="li": self.stack.append([])
        if t in ("h2","h3"): self.h=[]
    def handle_endtag(self, t):
        if t=="li" and self.stack: self.items.append(" ".join("".join(self.stack.pop()).split()))
        if t in ("h2","h3") and self.h is not None: self.heads.append("".join(self.h).strip()); self.h=None
    def handle_data(self, d):
        if self.stack: self.stack[-1].append(d)
        if self.h is not None: self.h.append(d)
p=P(); p.feed(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
print("headings:", p.heads)
for key in ("Clicking the first paragraph of a tight", "Emptying the first block of a box body", "A card of a box loses"):
    found=[i for i in p.items if i.startswith(key)]
    print(len(found), found)
