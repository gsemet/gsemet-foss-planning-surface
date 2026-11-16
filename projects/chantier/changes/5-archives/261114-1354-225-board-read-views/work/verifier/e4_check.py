# /// script
# dependencies = ["playwright"]
# ///
import json, sys
from playwright.sync_api import sync_playwright
U = json.load(open(sys.argv[1]))
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1400,"height":860})
    pg.on("dialog", lambda d: print("DIALOG", d.message))
    for v in ("home","kanban","batch","costs"):
        pg.goto(U["par"] + "&v=" + v); pg.wait_for_selector("#view > *"); pg.wait_for_timeout(1500)
        print(v, "img[src=x]:", pg.locator("img[src='x']").count(), "script in body:", pg.locator("body script").count(), "elements with onerror attr:", pg.locator("[onerror]").count(), "b elements with text 'bold':", pg.locator("b", has_text="bold").count(), "literal markup in text:", "<b>bold</b>" in pg.inner_text("body"))
    pg.goto(U["surf"] + "&p=*&v=kanban"); pg.wait_for_timeout(2000)
    print("p=* v=kanban ->", pg.url[-50:], "| h1:", pg.inner_text("#title"))
    b.close()
