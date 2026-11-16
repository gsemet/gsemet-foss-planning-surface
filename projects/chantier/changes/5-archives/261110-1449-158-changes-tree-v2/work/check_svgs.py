"""Check the six redrawn SVGs of CR-158 against their -texts.md companions.

stdlib only. Usage: python check_svgs.py <docs-dir>

Only the fenced blocks of a -texts.md are compared (the headings are notes).

1. desc: the SVG's <desc> equals the first paragraph of its -texts.md.
2. title: the SVG's <title> equals the first heading of the -texts.md.
3. words: every word of every <text> is in the -texts.md body, and every
   word of the -texts.md body is in the SVG (emoji and markup ignored).
4. old names: the six SVGs and their -texts.md hold none of 3-requests,
   4-archives, 5-trash, 4-batches, batch-<n>/ (the file name batch-lifecycle.svg is
   not a path and is allowed).
"""
import html
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

NAMES = [
    "cr-folder-lifecycle",
    "cr-lifecycle",
    "cr-lifecycle-simple",
    "how-chantier-works",
    "batch-lifecycle",
    "how-chantier-works-simple-foreman",
]
OLD = [r"4-batches", r"3-requests", r"4-archives", r"5-trash", r"batch-&lt;n&gt;/", r"batch-<n>/", r"batch-\d+/"]
NS = "{http://www.w3.org/2000/svg}"


def words(s):
    s = re.sub(r"[^\w\-./…→⇄·≤]+", " ", s, flags=re.UNICODE)
    out = set()
    for w in s.split():
        w = w.strip(".,;:·/")
        if w and re.search(r"[A-Za-z0-9]", w):
            out.add(w)
    return out


def svg_texts(path):
    root = ET.parse(path).getroot()
    title = root.find(NS + "title").text
    desc = root.find(NS + "desc").text
    chunks = []
    for el in root.iter(NS + "text"):
        chunks.append("".join(el.itertext()))
    return title, desc, chunks


def md_parts(path):
    lines = path.read_text(encoding="utf-8").split("\n")
    title = lines[0].lstrip("# ").strip()
    desc = lines[2].strip()
    body_lines, fenced = [], False
    for ln in lines[3:]:
        if ln.startswith("```"):
            fenced = not fenced
        elif fenced:
            body_lines.append(ln)
    body = "\n".join(body_lines)
    return title, desc, body


def main():
    docs = Path(sys.argv[1])
    problems = 0
    for n in NAMES:
        svg, md = docs / f"{n}.svg", docs / f"{n}-texts.md"
        st, sd, chunks = svg_texts(svg)
        mt, md_d, body = md_parts(md)
        res = []
        if st != mt:
            res.append(f"title differs: {st!r} vs {mt!r}")
        if " ".join(sd.split()) != " ".join(md_d.split()):
            res.append("desc differs from the first paragraph of the -texts.md")
        sw = words(" ".join(chunks))
        mw = words(body)
        for w in sorted(sw - mw):
            res.append(f"in the SVG, not in the -texts.md: {w}")
        for w in sorted(mw - sw):
            # words of the md that sit only in the markup, not drawn
            res.append(f"in the -texts.md, not in the SVG: {w}")
        for label, src in (("svg", svg.read_text(encoding="utf-8")), ("md", md.read_text(encoding="utf-8"))):
            for pat in OLD:
                for m in re.finditer(pat, src):
                    res.append(f"old name in {label}: {m.group(0)}")
        status = "OK" if not res else "FAIL"
        print(f"{n}: {status} ({len(chunks)} texts, {len(sw)} words)")
        for r in res:
            print("   " + r)
        problems += len(res)
    print("RESULT:", "all in step, no old names" if problems == 0 else f"{problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
