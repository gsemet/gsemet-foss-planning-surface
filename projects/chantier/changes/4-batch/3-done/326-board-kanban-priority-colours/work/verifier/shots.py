# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.49"]
# ///
"""Verifier CR-326: argv[1]=worktree root, argv[2]=out dir, argv[3]=label. Scratch surface in a temp folder."""
import json, shutil, sys, tempfile
from pathlib import Path
sys.path.insert(0, sys.argv[1] + "/scripts")
import docs_screenshots as d
from playwright.sync_api import sync_playwright

OUT = Path(sys.argv[2]); LABEL = sys.argv[3]
OUT.mkdir(parents=True, exist_ok=True)
d.OUT = OUT

JS = """() => { const b=document.querySelector('.kanban .board'); const r=b.getBoundingClientRect();
  const main=document.querySelector('.main');
  return {winH:innerHeight, boardBottom:r.bottom, boardSW:b.scrollWidth, boardCW:b.clientWidth,
    mainSH:main.scrollHeight, mainCH:main.clientHeight, docSH:document.documentElement.scrollHeight,
    colScroll:[...document.querySelectorAll('.kanban .col')].map(c=>[c.scrollHeight,c.clientHeight,getComputedStyle(c).overflowY]),
    colh:[...document.querySelectorAll('.kanban .colh')].map(c=>getComputedStyle(c).backgroundColor),
    snap:getComputedStyle(b).scrollSnapType}}"""

def main():
    work = Path(tempfile.mkdtemp(prefix="scratch-"))
    proc = None
    try:
        surface = d.make_surface(work)
        src = surface / "projects/shop-api/changes/2-backlog/P4/archive-old-orders"
        shutil.copytree(src, surface / "projects/shop-api/changes/2-backlog/P3/cold-storage-tiering")
        home = work / "home"; home.mkdir()
        proc, url = d.start_board(surface, home)
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            for size, vp in (("pc", {"width": 1280, "height": 800}), ("phone", {"width": 390, "height": 800})):
                ctx = br.new_context(viewport=vp, locale="en-US", timezone_id="UTC", color_scheme="light",
                                     reduced_motion="reduce", is_mobile=size == "phone", has_touch=size == "phone")
                ctx.route("**/api/board*", d.fix_surface_path)
                page = ctx.new_page()
                d.goto(page, url, "kanban", "shop-api")
                print(LABEL, "kanban", size, json.dumps(page.evaluate(JS)))
                d.shot(page, "kanban", size)
                d.goto(page, url, "triage", "shop-api")
                page.locator('.pi[data-slug="stock-alerts"]').click(position={"x": 6, "y": 6})
                d.settle(page)
                print(LABEL, "triage", size, page.evaluate("""() => [...document.querySelectorAll('.pi')].map(c=>{const s=getComputedStyle(c);return [c.dataset.slug,c.classList.contains('sel'),s.borderLeftColor,s.borderLeftWidth]})"""))
                d.shot(page, "triage", size)
                d.goto(page, url, "batch", "shop-api"); d.shot(page, "batch", size)
                d.goto(page, url, "costs", "mobile-app"); d.shot(page, "costs", size)
                d.goto(page, url, "home", "*"); d.shot(page, "all-projects", size)
                d.goto(page, url, "home", "shop-api")
                print(LABEL, "home", size, page.evaluate("()=>{const m=document.querySelector('.main');return [m.scrollHeight,m.clientHeight,getComputedStyle(m).overflowY]}"))
                d.shot(page, "project", size)
                d.goto(page, url, "config", "shop-api")
                print(LABEL, "config", size, page.evaluate("()=>{const m=document.querySelector('.main');return [m.scrollHeight,m.clientHeight,getComputedStyle(m).overflowY]}"))
                if size == "pc":
                    d.panel(page, url, size)  # CR panel
                    d.goto(page, url, "kanban", "shop-api")
                    page.locator('[data-open^="i:"][data-open*="guest-checkout"]').locator("visible=true").first.click()
                    page.wait_for_selector('[data-key^="file-"]', state="attached"); d.settle(page)
                    d.shot(page, "panel-item", size)
                    d.goto(page, url, "home", "shop-api")
                    page.locator('[data-menu="toggle"]').locator("visible=true").first.click()
                    d.settle(page); d.shot(page, "picker", size)
                ctx.close()
            br.close()
    finally:
        if proc: d.stop(proc)
        shutil.rmtree(work, ignore_errors=True)
main()
