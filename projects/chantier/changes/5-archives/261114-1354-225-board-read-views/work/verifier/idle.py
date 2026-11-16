# /// script
# dependencies = ["playwright"]
# ///
import json, sys
from playwright.sync_api import sync_playwright
U = json.load(open(sys.argv[1]))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1400,"height":860})
    pg.goto(U["surf"] + "&p=chantier&v=kanban"); pg.wait_for_selector("#view > *"); pg.wait_for_timeout(3000)
    pg.evaluate("() => { window.__m = 0; new MutationObserver(r => { window.__m += r.filter(x => !(x.target.id==='heard' || x.target.closest?.('#heard'))).length }).observe(document.querySelector('#view'), {childList:true, subtree:true, attributes:true, characterData:true}) }")
    pg.evaluate("() => document.querySelector('#view').scrollTop = 40")
    pg.wait_for_timeout(13000)
    print("mutations in #view over 13 s with no data change:", pg.evaluate("() => window.__m"))
    b.close()