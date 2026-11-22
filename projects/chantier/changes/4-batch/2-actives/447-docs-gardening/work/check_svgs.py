# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.49"]
# ///
"""Check docs SVGs: parse as XML, <title>/<desc> equal the -texts.md title and description paragraph,
every visible text line of the texts file appears in the SVG, and optionally render to PNG.
Usage: python check_svgs.py <repo root> <out dir> [--render] [names...]"""
import re, sys, pathlib
import xml.etree.ElementTree as ET

root = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
args = [a for a in sys.argv[3:] if not a.startswith("--")]
render = "--render" in sys.argv
docs = root / "docs"
names = args or sorted(p.stem for p in docs.glob("*.svg") if p.stem not in ("logo", "batch-pace"))
ns = "{http://www.w3.org/2000/svg}"
bad = 0


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def svg_text(el):
    return norm("".join(el.itertext()))


for n in names:
    svg = docs / f"{n}.svg"
    tx = docs / f"{n}-texts.md"
    try:
        tree = ET.parse(svg)
    except Exception as e:
        print(f"FAIL {n}: XML {e}"); bad += 1; continue
    r = tree.getroot()
    title = norm(r.find(ns + "title").text or "")
    desc = norm(r.find(ns + "desc").text or "")
    lines = tx.read_text(encoding="utf-8").splitlines()
    ttl = next(l[2:] for l in lines if l.startswith("# "))
    i = lines.index(next(l for l in lines if l.startswith("# ")))
    para = norm(next(l for l in lines[i + 1:] if l.strip()))
    ok = True
    if title != norm(ttl):
        print(f"FAIL {n}: title {title!r} != {ttl!r}"); ok = False
    if desc != para:
        print(f"FAIL {n}: desc differs from the texts paragraph"); ok = False
        import difflib
        for op in difflib.SequenceMatcher(None, desc, para).get_opcodes():
            if op[0] != "equal":
                print("   ", op[0], "svg:", repr(desc[op[1]:op[2]][:140]), "texts:", repr(para[op[3]:op[4]][:140]))
    # visible text: each fenced block's lines (without markdown heading marks) must appear in the svg
    alltext = " ".join(svg_text(t) for t in r.iter(ns + "text"))
    alltext = norm(alltext)
    blocks = re.findall(r"```md\n(.*?)```", tx.read_text(encoding="utf-8"), re.S)
    for b in blocks:
        for l in b.splitlines():
            l = norm(re.sub(r"^#+\s*", "", l)).replace("`", "").replace("*", "")
            if l and not re.sub(r"\W", "", l) in re.sub(r"\W", "", alltext):
                # lines may wrap differently or sit in several text elements: compare by words
                if re.sub(r"\W", "", l):
                    print(f"MISS {n}: {l!r}"); ok = False
    print(("ok   " if ok else "DIFF ") + n)
    bad += not ok
    if render:
        from playwright.sync_api import sync_playwright
        vb = [float(x) for x in r.get("viewBox").split()]
        with sync_playwright() as pw:
            b = pw.chromium.launch(); pg = b.new_page(viewport={"width": int(vb[2]), "height": int(vb[3])})
            pg.goto(svg.as_uri()); pg.screenshot(path=str(out / f"{n}.png")); b.close()
print("problems:", bad)
