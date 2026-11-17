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
            for view, proj in (("home", "*"), ("home", "shop-api"), ("batch", "shop-api"), ("triage", "shop-api")):
                d.goto(page, url, view, proj)
                page.screenshot(path=str(OUT / f"{view}-{proj.replace('*','all')}-{size}.png"))
                if view == "home":
                    page.evaluate("document.querySelector('.main').scrollTo(0, 99999)"); page.wait_for_timeout(200)
                    page.screenshot(path=str(OUT / f"{view}-{proj.replace('*','all')}-{size}-bottom.png"))
            d.goto(page, url, "triage", "shop-api")
            page.evaluate("document.querySelector('.main').scrollTo(0, 300)")
            page.wait_for_timeout(300)
            print(size, "scrolled class:", page.evaluate("document.getElementById('head').className"), "scrollTop", page.evaluate("document.querySelector('.main').scrollTop"))
            page.screenshot(path=str(OUT / f"scrolled-{size}.png"))
            page.evaluate("document.querySelector('.main').scrollTo(0, 0)")
            if size == "pc":
                page.click("[data-menu=toggle]"); page.wait_for_selector(".menu[role=menu]")
                page.screenshot(path=str(OUT / "menu-pc.png"))
            print(size, "font", page.evaluate("[getComputedStyle(document.querySelector('h1')).fontFamily, getComputedStyle(document.querySelector('h1')).fontWeight, document.fonts.check('500 14px Inter')]"))
            print(size, "hscroll ok", page.evaluate("document.documentElement.scrollWidth <= innerWidth"))
            print(size, "console", logs)
            ctx.close()
        br.close()
finally:
    if proc is not None: d.stop(proc)
    shutil.rmtree(work, ignore_errors=True)
