# /// script
# dependencies = ["playwright>=1.49"]
# ///
import shutil, sys, tempfile
from pathlib import Path
sys.path.insert(0, "C:/Users/gaeta/Projets/chantier.worktrees/batch-23-CR-319/scripts")
import docs_screenshots as d
from playwright.sync_api import sync_playwright
OUT = Path(sys.argv[1])

def fix(route):
    r = route.fetch(); b = r.json()
    b["served"] = d.SURFACE_SHOWN
    b["served_origin"] = "git@github.com:demo/planning-surface.git"
    for p in b["projects"]:
        p["repo_path"] = f"/home/demo/{p['id']}"
        p["origin"] = f"https://github.com/demo/{p['id']}.git" if p["id"] != "shop-api" else ""
    route.fulfill(response=r, json=b)

work = Path(tempfile.mkdtemp(prefix="chantier-r1-"))
proc = None
try:
    surface = d.make_surface(work)
    home = work / "home"; home.mkdir()
    proc, url = d.start_board(surface, home)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for size, vp in (("pc", {"width": 1400, "height": 860}), ("phone", {"width": 390, "height": 844})):
            ctx = br.new_context(viewport=vp, locale="en-US", is_mobile=size == "phone", has_touch=size == "phone")
            ctx.route("**/api/board*", fix)
            page = ctx.new_page()
            logs = []
            page.on("console", lambda m: logs.append(m.text))
            for view, proj in (("home","*"),("home","shop-api"),("batch","shop-api"),("triage","shop-api"),("kanban","shop-api"),("prs","shop-api"),("costs","shop-api"),("config","shop-api"),("overview","*")):
                try:
                    d.goto(page, url, view, proj)
                except Exception as e:
                    print("goto fail", view, e); continue
                page.screenshot(path=str(OUT / f"{view}-{proj.replace('*','all')}-{size}.png"), full_page=False)
                if view == "batch":
                    print(size, "batch", page.evaluate("""() => { const h=[...document.querySelectorAll('.lvlh')].map(e=>e.textContent.trim()); const g=document.querySelectorAll('.grp,.gh').length; const hd=document.querySelector('svg.edges .head, svg.edges marker'); const heads=[...document.querySelectorAll('svg.edges path')].length; return {levels:h, oldGroups:g, paths:heads, nodes:document.querySelectorAll('.node').length, badges:document.querySelectorAll('.node .sb').length, merged:document.querySelectorAll('.node .band, .node .nm').length, fonts: document.fonts.status}; }"""))
                    print(size, "edges", page.evaluate("""() => [...document.querySelectorAll('svg.edges path')].map(p => { const r=p.getBoundingClientRect(); const L=p.getTotalLength(); const e=p.getPointAtLength(L); const m=p.getScreenCTM(); const pt=new DOMPoint(e.x,e.y).matrixTransform(m); const ends=[...document.querySelectorAll('.node')].map(n=>n.getBoundingClientRect()).filter(b=>Math.abs(b.left-pt.x)<3 && pt.y>b.top && pt.y<b.bottom).length; return {endX:Math.round(pt.x), touches:ends, marker:p.getAttribute('marker-end')}; })"""))
                    page.hover(".lgpill"); page.wait_for_timeout(200)
                    page.screenshot(path=str(OUT / f"batch-legend-{size}.png"))
            print(size, "console", logs)
            ctx.close()
        br.close()
finally:
    if proc is not None: d.stop(proc)
    shutil.rmtree(work, ignore_errors=True)
