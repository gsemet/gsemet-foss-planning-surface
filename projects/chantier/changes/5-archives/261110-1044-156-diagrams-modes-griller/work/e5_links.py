import re, glob, os, sys

os.chdir(sys.argv[1])


def slug(h):
    h = h.strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")


def anchors(path):
    tx = re.sub(r"```.*?```", "", open(path, encoding="utf-8").read(), flags=re.S)
    return {slug(x) for x in re.findall(r"^#+\s+(.*)$", tx, flags=re.M)}


bad = 0
n = 0
for md in ["README.md"] + glob.glob("docs/*.md"):
    t = open(md, encoding="utf-8").read()
    tt = re.sub(r"```.*?```", "", t, flags=re.S)
    for m in re.finditer(r"!?\[[^\]]*\]\(([^)\s]+)", tt):
        l = m.group(1)
        if re.match(r"[a-z]+:", l):
            continue
        n += 1
        p, _, a = l.partition("#")
        tgt = os.path.normpath(os.path.join(os.path.dirname(md), p)) if p else md
        if not os.path.exists(tgt):
            print("BROKEN", md, l)
            bad += 1
            continue
        if a and tgt.endswith(".md") and a not in anchors(tgt):
            print("BAD ANCHOR", md, l)
            bad += 1
print("links checked", n, "bad", bad)
