"""Prototype 02 of the requirements viewer: static pages for one vertical slice.

Slice: all areas (index) -> area "diagrams" -> use case StRS-MDOKFSTUDIO-DIAG-001 -> its behaviours.
Reads journey-data.js (okfreq report + area titles + Main paths). Writes plain HTML pages, one per
view, sharing style.css and app.js. Lists and the metro map are rendered here, so every page reads
without JavaScript; app.js adds search, the theme switch and the Play of a path.

python3 gen.py <journey-data.js> <out_dir>
"""
import html, json, math, os, re, sys

DATA, OUT = sys.argv[1], sys.argv[2]
D = json.loads(open(DATA).read()[len("window.REQ_DATA="):-1])
SHA = D["sha"]
REPO = f"https://github.com/gsemet/markdown-okf-schema-studio/blob/{SHA}/"
AREA, CASE = "diagrams", "StRS-MDOKFSTUDIO-DIAG-001"
OLD = {"superseded", "deprecated"}
PAL = ["#c2410c", "#be185d", "#7c3aed", "#4338ca", "#1d4ed8", "#0369a1", "#0f766e", "#047857",
       "#4d7c0f", "#a16207", "#b45309", "#b91c1c", "#9333ea", "#0e7490", "#475569", "#9d174d"]
SCOPES = [s for s in D["groups"] if s in D["scopes"]]
COL = {s: PAL[i % len(PAL)] for i, s in enumerate(SCOPES)}
R = {r["id"]: r for r in D["reqs"]}
ACTIVE = [r for r in D["reqs"] if r["lc"] not in OLD]
KIDS = {}
for r in ACTIVE:
    for p in r["df"]:
        KIDS.setdefault(p, []).append(r)
PATHS = D["mainPaths"][CASE]
SLICE = KIDS[CASE]  # behaviours of the use case
e = lambda s: html.escape(str(s or ""), quote=True)
sid = lambda i: re.sub(r"^(StRS|SwRS)-MDOKFSTUDIO-", "", i)
title = lambda s: D["groups"][s]["title"]
case_page = "use-case-" + sid(CASE).lower() + ".html"
area_page = "area-" + AREA + ".html"
beh_page = lambda i: "behaviour-" + sid(i).lower() + ".html"
KIND = {"nominal": "nom", "boundary": "bnd", "refusal": "ref"}


def pl(n, word):
    return word + ("" if n == 1 else "s")


def nt(n):
    return f"{n} test" + ("" if n == 1 else "s")


def dots(sc):
    return '<span class="dots">' + "".join(f'<i class="{KIND.get(s[0], "nom")}" title="{e(s[0])}: {e(s[1])}"></i>' for s in sc) + "</span>"


def test_kind(f):
    for pre, k in (("test/integration", "integration"), ("test/visual", "visual"), ("sphinx", "sphinx"), ("test/build", "build")):
        if f.startswith(pre):
            return k
    return "unit"


BASE = "https://gsemet.github.io/markdown-okf-schema-studio/requirements/"  # where the site is published
LEVELS = {  # one social picture per level of the viewer; the page text (title, description) differs per page
    "areas": ("Requirements", "Every feature, from use case to test", None),
    "area": ("Area", "Use cases of one product area", 0),
    "use-case": ("Use case", "What a user does and gets, split into behaviours", 0),
    "behaviour": ("Behaviour", "One rule, tested on its own, linked to its code", 1),
}


def card_html(level):
    """The social card of a level: what the level is, and the chain use case -> behaviour -> code and tests."""
    kind, line, on = LEVELS[level]
    chain = [("Use case", "StRS"), ("Behaviour", "SwRS"), ("Code and tests", "files")]
    steps = "".join(f'<li class="{"on" if i == on else ""}"><b>{t}</b><code>{c}</code></li>' for i, (t, c) in enumerate(chain))
    return f"""<!DOCTYPE html>
<html lang="en" data-theme="cream"><head><meta charset="utf-8"><link rel="stylesheet" href="../style.css"></head>
<body class="card">
<p class="eyebrow"><span class="sw"></span>{e(kind)}</p>
<h1>{e(line)}</h1>
<ol class="chain">{steps}</ol>
<p class="brand"><span class="logo"></span>Markdown OKF-Schema Studio <span>· Requirements</span></p>
</body></html>
"""


def page(name, crumbs, body, color=None, desc="", card=None):
    crumb = "".join(
        (f'<span class="sep">/</span>' if i else "")
        + (f'<a href="{h}">{e(t)}</a>' if h else f'<span aria-current="page">{e(t)}</span>')
        for i, (t, h) in enumerate(crumbs))
    style = f' style="--c:{color}"' if color else ""
    social = ""
    if card:
        img = BASE + "og/" + card["level"] + ".png"
        social = (f'<meta property="og:type" content="website">\n<meta property="og:site_name" content="Markdown OKF-Schema Studio">\n'
                  f'<meta property="og:title" content="{e(card["title"])}">\n<meta property="og:description" content="{e(desc)}">\n'
                  f'<meta property="og:url" content="{BASE + name}">\n<meta property="og:image" content="{img}">\n'
                  f'<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">\n'
                  f'<meta property="og:image:alt" content="{e(LEVELS[card["level"]][0] + ": " + LEVELS[card["level"]][1])}">\n<meta name="twitter:card" content="summary_large_image">')
    doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(crumbs[-1][0])} · Studio requirements</title>
<meta name="description" content="{e(desc)}">
{social}
<link rel="stylesheet" href="style.css">
<script>document.documentElement.dataset.theme = localStorage.getItem("req-theme") || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "cream");</script>
</head>
<body{style}>
<header class="top"><div class="in">
  <a class="home" href="index.html">Studio requirements</a>
  <nav class="crumbs" aria-label="Breadcrumb">{crumb}</nav>
  <button class="btn" id="search-open" type="button" aria-label="Search">Search <kbd>/</kbd></button>
  <button class="btn" id="theme" type="button" aria-label="Switch theme">Theme</button>
</div></header>
<main>
{body}
</main>
<footer><div class="in">Prototype 02 · one vertical slice of the real requirements (area Diagrams, use case DIAG-001) · okfreq report at commit <a href="https://github.com/gsemet/markdown-okf-schema-studio/tree/{SHA}">{SHA[:8]}</a></div></footer>
<div class="search" id="search" hidden><div class="box"><div class="bar"><input id="q" type="search" placeholder="Search use cases, behaviours, files" autocomplete="off"><button class="btn" id="search-close" type="button">Close</button></div><div id="results" class="results"></div></div></div>
<script src="search-index.js"></script>
<script src="app.js"></script>
</body>
</html>
"""
    open(os.path.join(OUT, name), "w").write(doc)


# ---------------------------------------------------------------- index: the areas
def index():
    n_cases = sum(1 for r in ACTIVE if r["t"] == "StRS")
    n_beh = sum(1 for r in ACTIVE if r["t"] == "SwRS")
    rows = []
    for s in SCOPES:
        cs = [r for r in ACTIVE if r["s"] == s and r["t"] == "StRS"]
        bs = [r for r in ACTIVE if r["s"] == s and r["t"] == "SwRS"]
        live = s == AREA
        inner = (f'<span class="sw" style="background:{COL[s]}"></span><span class="name">{e(title(s))}</span>'
                 f'<span class="desc">{e(D["groups"][s]["desc"])}</span>'
                 f'<span class="num">{len(cs)}</span><span class="num">{len(bs)}</span>')
        rows.append(f'<a class="arow" href="{area_page}">{inner}</a>' if live else f'<div class="arow off" title="Not part of this prototype">{inner}</div>')
    body = f"""
<h1>Requirements of Markdown OKF-Schema Studio</h1>
<p class="lead">Every feature of Studio is written down at three levels, each one linked to the next.</p>
<ol class="layers">
  <li><b>Use case</b><span>What a user does and gets, from start to end. Written for a person.</span><code>StRS · {n_cases}</code></li>
  <li><b>Behaviour</b><span>One rule the software follows, small enough to test on its own.</span><code>SwRS · {n_beh}</code></li>
  <li><b>Code and tests</b><span>The files that implement each behaviour and the tests that check it.</span><code>{D["totals"]["combined_coverage_percent"]}% linked</code></li>
</ol>
<h2>Areas</h2>
<p class="hint">Requirements are grouped by product area. In this prototype only <b>Diagrams</b> can be opened.</p>
<div class="areas"><div class="arow head"><span></span><span class="name">Area</span><span class="desc">Covers</span><span class="num">Use cases</span><span class="num">Behaviours</span></div>{"".join(rows)}</div>
"""
    page("index.html", [("Areas", None)], body, desc="Every feature of Studio written down as use cases, behaviours, code and tests, each linked to the next.",
         card={"level": "areas", "title": "Requirements of Markdown OKF-Schema Studio"})


# ---------------------------------------------------------------- area: its use cases
def area():
    cases = [r for r in ACTIVE if r["s"] == AREA and r["t"] == "StRS"]
    beh = [r for r in ACTIVE if r["s"] == AREA and r["t"] == "SwRS"]
    items = []
    for r in cases:
        n = len(KIDS.get(r["id"], []))
        live = r["id"] == CASE
        need = re.sub(r"^As an? [^,]+, ", "", r["un"] or "")
        inner = f'<span class="id">{sid(r["id"])}</span><span class="t">{e(r["ti"])}</span><span class="need">{e(need)}</span><span class="meta">{n} behaviours</span>'
        items.append(f'<li><a class="stop" href="{case_page}">{inner}</a></li>' if live else f'<li><div class="stop off" title="Not part of this prototype">{inner}</div></li>')
    body = f"""
<p class="eyebrow"><span class="sw" style="background:{COL[AREA]}"></span>Area</p>
<h1>{e(title(AREA))}</h1>
<p class="lead">{e(D["groups"][AREA]["desc"])}</p>
<p class="facts"><b>{len(cases)}</b> use cases · <b>{len(beh)}</b> behaviours · <b>{D["scopes"][AREA]["combined_coverage_percent"]}%</b> linked to code and tests</p>
<h2>Use cases</h2>
<p class="hint">Each stop is a use case. Open one to see how it is split into behaviours.</p>
<ol class="line">{"".join(items)}</ol>
"""
    page(area_page, [("Areas", "index.html"), (title(AREA), None)], body, COL[AREA], D["groups"][AREA]["desc"],
         card={"level": "area", "title": f"{title(AREA)}: use cases and behaviours"})


# ---------------------------------------------------------------- metro layout
def graph():
    S, T, alt = {}, [], 0
    for pi, p in enumerate(PATHS):
        prev = None
        for i, st in enumerate(p["steps"]):
            n = S.get(st["state"])
            if n is None:
                n = {"key": st["state"], "col": prev["col"] + 1 if prev else i, "track": 0 if pi == 0 else 1,
                     "goal": i == len(p["steps"]) - 1, "paths": set()}
                S[st["state"]] = n
            n["paths"].add(pi)
            if prev:
                T.append({"a": prev, "b": n, "via": p["steps"][i - 1]["via"], "path": pi, "step": i - 1, "opt": False})
            for o in st["options"]:
                t = {"key": f"opt{alt}", "col": n["col"] + 0.5, "track": -1 if n["track"] == 0 else 2, "alt": True, "label": o["label"]}
                alt += 1
                T.append({"a": n, "b": t, "via": o, "path": pi, "opt": True})
            prev = n
    seen = {}
    for t in T:
        if t["opt"]:
            k = (t["b"]["col"], t["b"]["track"])
            seen[k] = seen.get(k, 0) + 1
            if seen[k] > 1:
                t["b"]["track"] += (-1 if t["b"]["track"] < 0 else 1) * 0.8 * (seen[k] - 1)
    return S, T


def wrap(text, n):
    lines, cur = [], ""
    for w in str(text).split():
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    return lines + ([cur] if cur else [])


def tspans(x, y, text, n, up=False, lh=15):
    ls = wrap(text, n)
    y0 = y - (len(ls) - 1) * lh if up else y
    return "".join(f'<tspan x="{x:.0f}" y="{y0 + i * lh:.0f}">{e(l)}</tspan>' for i, l in enumerate(ls))


def metro_svg():
    S, T = graph()
    nodes = list(S.values()) + [t["b"] for t in T if t["opt"]]
    cols = max(n["col"] for n in nodes) + 1
    colw, padx, trackh = 220, 90, 165
    mint, maxt = min(n["track"] for n in nodes), max(n["track"] for n in nodes)
    top = 70 - mint * trackh
    W, H = padx * 2 + (cols - 1) * colw, top + maxt * trackh + 100
    P = lambda n: (padx + n["col"] * colw, top + n["track"] * trackh)
    pc = lambda i: "var(--p1)" if i == 0 else "var(--p2)"
    out = [f'<svg class="metro" viewBox="0 0 {W:.0f} {H:.0f}" role="img" aria-label="Map of the use case: states joined by behaviours">']
    for t in T:
        (x1, y1), (x2, y2) = P(t["a"]), P(t["b"])
        d = f"M{x1:.0f},{y1:.0f} L{x2:.0f},{y2:.0f}" if y1 == y2 else f"M{x1:.0f},{y1:.0f} C{x1 + (x2 - x1) * .55:.0f},{y1:.0f} {x2 - (x2 - x1) * .55:.0f},{y2:.0f} {x2:.0f},{y2:.0f}"
        sw = R[t["via"]["id"]]
        sc = [s for s in sw["sc"] if not t["via"]["kind"] or s[0] == t["via"]["kind"]]
        # label position: middle of a straight segment, or a point near the far end of a curve
        if y1 == y2:
            mx, my = (x1 + x2) / 2, y1
        else:
            u = .72 if t["opt"] else .5
            mx = (1 - u) ** 3 * x1 + 3 * (1 - u) ** 2 * u * (x1 + (x2 - x1) * .55) + 3 * (1 - u) * u * u * (x2 - (x2 - x1) * .55) + u ** 3 * x2
            my = (1 - u) ** 3 * y1 + 3 * (1 - u) ** 2 * u * y1 + 3 * (1 - u) * u * u * y2 + u ** 3 * y2
        label = f"{sid(sw['id'])} · {nt(len(sw['te']))}"
        w = len(label) * 7 + 18
        stroke = "var(--alt)" if t["opt"] else pc(t["path"])
        attrs = f'data-path="{t["path"]}" data-step="{t["step"]}"' if not t["opt"] else 'data-option=""'
        shared = (not t["opt"]) and len(t["a"]["paths"]) > 1 and len(t["b"]["paths"]) > 1
        g = [f'<a class="tr" href="{beh_page(sw["id"])}" {attrs}><title>{e(sw["id"])}: {e(sw["ti"])}</title>']
        if shared:
            g.append(f'<path d="{d}" stroke="var(--p2)" stroke-width="13" stroke-linecap="round" fill="none" opacity=".4"/>')
        dash = ' stroke-dasharray="6 6"' if t["opt"] else ""
        g.append(f'<path class="ln" d="{d}" stroke="{stroke}" stroke-width="{2.5 if t["opt"] else 7}" stroke-linecap="round" fill="none"{dash}/>')
        g.append(f'<path class="hit" d="{d}"/>')
        g.append(f'<g transform="translate({mx:.0f},{my:.0f})"><rect class="pill" x="{-w / 2:.0f}" y="-12" width="{w}" height="24" rx="12" stroke="{stroke}"/><text class="pt" y="4" text-anchor="middle">{e(label)}</text>')
        g.extend(f'<circle cx="{(j - (len(sc) - 1) / 2) * 12:.0f}" cy="20" r="4.2" class="{KIND.get(s[0], "nom")}"/>' for j, s in enumerate(sc))
        g.append("</g>")
        if not t["opt"]:
            if y1 == y2:
                g.append(f'<text class="verb" text-anchor="middle">{tspans(mx, my - 24, t["via"]["label"], 30, up=True)}</text>')
            else:
                g.append(f'<text class="verb">{tspans(mx + w / 2 + 10, my + 4, t["via"]["label"], 26)}</text>')
        g.append("</a>")
        out.append("".join(g))
    for n in nodes:
        x, y = P(n)
        cls = "st" + (" goal" if n.get("goal") else "") + (" alt" if n.get("alt") else "")
        r = 7 if n.get("alt") else 15 if n.get("goal") else 12
        text = n.get("label") if n.get("alt") else n["key"]
        if n.get("alt") and n["track"] < 0:
            lab = f'<text text-anchor="middle">{tspans(x, y - 16, text, 30, up=True)}</text>'
        else:
            lab = f'<text text-anchor="middle">{tspans(x, y + (24 if n.get("alt") else 34), text, 30 if n.get("alt") else 24)}</text>'
        out.append(f'<g class="{cls}" data-state="{e(n["key"])}"><circle cx="{x}" cy="{y}" r="{r}"/>{lab}</g>')
    out.append("</svg>")
    return "".join(out)


def metro_list():
    """The same map for narrow screens: one vertical line per path."""
    parts = []
    for pi, p in enumerate(PATHS):
        rows = [f'<h3 class="pname" style="--pc:var(--{"p1" if pi == 0 else "p2"})">Path {pi + 1}: {e(p["title"])}</h3><ol class="vline" style="--pc:var(--{"p1" if pi == 0 else "p2"})">']
        for i, st in enumerate(p["steps"]):
            last = i == len(p["steps"]) - 1
            opts = "".join(f'<a class="vopt" href="{beh_page(o["id"])}"><b>{sid(o["id"])}</b> {e(o["label"])}</a>' for o in st["options"])
            via = ""
            if st["via"]:
                sw = R[st["via"]["id"]]
                via = f'<a class="vvia" href="{beh_page(sw["id"])}"><b>{sid(sw["id"])}</b> · {nt(len(sw["te"]))} {dots(sw["sc"])}<span>{e(st["via"]["label"])}</span></a>'
            rows.append(f'<li class="{"goal" if last else ""}"><span class="vstate">{e(st["state"])}</span>{opts}{via}</li>')
        rows.append("</ol>")
        parts.append("".join(rows))
    return '<div class="metro-list">' + "".join(parts) + "</div>"


def walks():
    S, T = graph()
    out = {}
    for t in T:
        sw = R[t["via"]["id"]]
        n = max(1, len([s for s in sw["sc"] if not t["via"]["kind"] or s[0] == t["via"]["kind"]]))
        out.setdefault(id(t["a"]), []).extend([t["b"]] * n)
    cur = {id(S[PATHS[0]["steps"][0]["state"]]): (S[PATHS[0]["steps"][0]["state"]], 1)}
    total = 0
    for _ in range(8):
        nx = {}
        for _, (n, c) in cur.items():
            for b in out.get(id(n), []):
                total += c
                k = id(b)
                nx[k] = (b, nx.get(k, (b, 0))[1] + c)
        cur = nx
    return total


# ---------------------------------------------------------------- use case: the map
def use_case():
    r = R[CASE]
    on_map = {s["via"]["id"] for p in PATHS for s in p["steps"] if s["via"]} | {o["id"] for p in PATHS for s in p["steps"] for o in s["options"]}
    n_sc = sum(len(R[i]["sc"]) for i in on_map)
    rows = []
    for b in SLICE:
        mark = "" if b["id"] in on_map else '<span class="tag">not on the map</span>'
        rows.append(f'<a class="brow" href="{beh_page(b["id"])}"><span class="id">{sid(b["id"])}</span><span class="t">{e(b["ti"])} {mark}</span><span class="m">{dots(b["sc"])}</span><span class="m">{nt(len(b["te"]))}</span></a>')
    plays = "".join(f'<button class="btn play" type="button" data-play="{i}">Play path {i + 1}</button>' for i in range(len(PATHS)))
    body = f"""
<p class="eyebrow"><span class="sw" style="background:{COL[AREA]}"></span>Use case {sid(CASE)}</p>
<h1>{e(r["ti"])}</h1>
<blockquote class="need">{e(r["un"])}</blockquote>
<h2>How it is split</h2>
<p class="hint">Circles are the states a user goes through. Each label between two states is a <b>behaviour</b>: one rule, tested on its own. The thick lines are the paths this use case describes; dashed lines are other outcomes at a state, tested too.</p>
<div class="map">
  <div class="maptools">{plays}<span class="legend"><i class="lp1"></i>path 1 <i class="lp2"></i>path 2 <i class="lalt"></i>other outcome <span class="dots"><i class="nom"></i></span>nominal <span class="dots"><i class="bnd"></i></span>boundary <span class="dots"><i class="ref"></i></span>refusal scenario</span></div>
  {metro_svg()}
  {metro_list()}
</div>
<p class="facts">This map has {walks():,} different ways through it in 8 steps or fewer. Instead of testing each one end to end, the <b>{len(on_map)}</b> behaviours on the map are tested one by one, with <b>{n_sc}</b> scenarios.</p>
<h2>Behaviours of this use case</h2>
<div class="blist">{"".join(rows)}</div>
"""
    page(case_page, [("Areas", "index.html"), (title(AREA), area_page), (sid(CASE), None)], body, COL[AREA],
         f"{walks():,} ways through this use case; its {len(on_map)} behaviours are tested one by one, with {n_sc} scenarios.",
         card={"level": "use-case", "title": f"Use case {sid(CASE)}: {r['ti']}"})


# ---------------------------------------------------------------- behaviour
def behaviour(b):
    where = ""
    for pi, p in enumerate(PATHS):
        for i, st in enumerate(p["steps"]):
            if st["via"] and st["via"]["id"] == b["id"]:
                dots_html = "".join(f'<span class="{"cur" if j == i else ""}"><i></i>{"<b></b>" if j < len(p["steps"]) - 1 else ""}</span>' for j in range(len(p["steps"])))
                where = f'<div class="where" style="--pc:var(--{"p1" if pi == 0 else "p2"})"><div class="track">{dots_html}</div><p>Step {i + 1} of path {pi + 1} in <a href="{case_page}">{sid(CASE)}</a>: from “{e(st["state"])}” to “{e(p["steps"][i + 1]["state"])}”.</p></div>'
                break
            if any(o["id"] == b["id"] for o in st["options"]):
                where = f'<div class="where" style="--pc:var(--alt)"><p>Another outcome at step {i + 1} of path {pi + 1} in <a href="{case_page}">{sid(CASE)}</a>, in the state “{e(st["state"])}”.</p></div>'
        if where:
            break
    if not where:
        where = f'<div class="where"><p>Part of <a href="{case_page}">{sid(CASE)}</a>, outside the paths drawn on its map.</p></div>'
    rule = re.sub(r"\bSHALL( NOT)?\b", lambda m: f"<strong>{m.group(0)}</strong>", e(b["de"]))

    def gwt(s):
        cols = {"GIVEN": [], "WHEN": [], "THEN": []}
        last = "GIVEN"
        for x in s[2]:
            k = x.split(" ", 1)[0]
            if k in cols:
                last = k
            cols[last].append(re.sub(r"^(GIVEN|WHEN|THEN|AND)\s+", "", x))
        return "".join(f'<div><b>{k.capitalize()}</b>{"<br>".join(e(v) for v in vs)}</div>' for k, vs in cols.items())

    scen = "".join(f'<details class="scn"><summary><span class="k {KIND.get(s[0], "nom")}">{e(s[0])}</span>{e(s[1])}</summary><div class="gwt">{gwt(s)}</div></details>' for s in b["sc"]) or '<p class="hint">Stated as one rule, without scenarios.</p>'

    def files(fs, kind=False):
        if not fs:
            return '<p class="hint">None.</p>'
        out = []
        for f in fs:
            k = f.rfind("/")
            tag = f'<span class="tag">{test_kind(f)}</span>' if kind else ""
            out.append(f'<li><a href="{REPO + f}"><span class="dir">{e(f[:k + 1])}</span>{e(f[k + 1:])}</a>{tag}</li>')
        return '<ul class="files">' + "".join(out) + "</ul>"

    known = f'<details class="known"><summary>Known limits ({b["ki"].count("Known issue")})</summary><p>{e(b["ki"]).replace(chr(10), "<br>")}</p></details>' if b["ki"] else ""
    sibs = SLICE
    k = sibs.index(b)
    pager = '<nav class="pager">' + (f'<a href="{beh_page(sibs[k - 1]["id"])}">← {e(sibs[k - 1]["ti"])}</a>' if k else "<span></span>") + (f'<a class="next" href="{beh_page(sibs[k + 1]["id"])}">{e(sibs[k + 1]["ti"])} →</a>' if k < len(sibs) - 1 else "") + "</nav>"
    body = f"""
<p class="eyebrow"><span class="sw" style="background:{COL[b["s"]]}"></span>Behaviour {sid(b["id"])}</p>
<h1>{e(b["ti"])}</h1>
<p class="rule">{rule}</p>
{where}
<h2>Scenarios <small>{len(b["sc"])}</small></h2>
<p class="hint">The situations the tests check. Open one to read it.</p>
{scen}
<div class="cols">
  <section><h2>Implemented in <small>{len(b["im"])}</small></h2>{files(b["im"])}</section>
  <section><h2>Tested by <small>{len(b["te"])}</small></h2>{files(b["te"], True)}</section>
</div>
{known}
{pager}
"""
    page(beh_page(b["id"]), [("Areas", "index.html"), (title(AREA), area_page), (sid(CASE), case_page), (sid(b["id"]), None)], body, COL[b["s"]],
         re.sub(r"\s+", " ", b["de"])[:200],
         card={"level": "behaviour", "title": f"Behaviour {sid(b['id'])}: {b['ti']}"})


# ---------------------------------------------------------------- search index (the slice only)
def search_index():
    items = [{"k": "Area", "t": title(AREA), "s": D["groups"][AREA]["desc"], "h": area_page}]
    items.append({"k": "Use case", "t": R[CASE]["ti"], "s": CASE, "h": case_page})
    files = {}
    for b in SLICE:
        items.append({"k": "Behaviour", "t": b["ti"], "s": b["id"] + " " + b["de"], "h": beh_page(b["id"])})
        for f in b["im"] + b["te"]:
            files.setdefault(f, []).append(b)
    for f, bs in sorted(files.items()):
        items.append({"k": "File", "t": f.rsplit("/", 1)[-1], "s": f, "h": beh_page(bs[0]["id"]), "n": len(bs)})
    open(os.path.join(OUT, "search-index.js"), "w").write("window.SEARCH=" + json.dumps(items, separators=(",", ":")) + ";")


os.makedirs(OUT, exist_ok=True)
index()
area()
use_case()
for b in SLICE:
    behaviour(b)
search_index()
os.makedirs(os.path.join(OUT, "cards"), exist_ok=True)
for level in LEVELS:
    open(os.path.join(OUT, "cards", level + ".html"), "w").write(card_html(level))
print("cards:", len(LEVELS))
print("pages:", len([f for f in os.listdir(OUT) if f.endswith(".html")]))
