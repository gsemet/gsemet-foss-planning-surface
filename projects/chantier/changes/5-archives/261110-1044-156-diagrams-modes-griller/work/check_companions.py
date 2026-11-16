import glob, re, sys, os
import xml.etree.ElementTree as E

os.chdir(sys.argv[1])
ns = "{http://www.w3.org/2000/svg}"


def norm(s):
    s = re.sub(r"[`*#]", "", s)
    s = s.replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


bad = 0
for f in sorted(glob.glob("docs/*.svg")):
    if f.endswith("batch-pace.svg"):
        continue
    md = f[:-4] + "-texts.md"
    if not os.path.exists(md):
        print("MISSING", md)
        bad += 1
        continue
    root = E.parse(f).getroot()
    desc = norm(root.find(ns + "desc").text or "")
    lines = open(md, encoding="utf-8").read().split("\n")
    para = ""
    for l in lines[1:]:
        if l.strip():
            para = l
            break
    if norm(para) != desc:
        print("DESC DIFF", f)
        bad += 1
    body = norm("\n".join(lines))
    drawn = []
    for t in root.iter(ns + "text"):
        s = norm("".join(t.itertext()))
        if s:
            drawn.append(s)
            if s not in body:
                print("NOT IN COMPANION", f, repr(s))
                bad += 1
    # converse: lines of md blocks drawn
    alld = " | ".join(drawn)
    inblock = False
    for l in lines:
        if l.startswith("```"):
            inblock = not inblock
            continue
        if inblock:
            n = norm(l)
            if n and n not in alld:
                # may be a multi-text joined (e.g. title + sub)
                print("NOT DRAWN", f, repr(n))
                bad += 1
print("done", bad)
