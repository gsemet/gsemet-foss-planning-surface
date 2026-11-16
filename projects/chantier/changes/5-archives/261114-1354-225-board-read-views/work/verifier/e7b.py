# /// script
# dependencies = ["playwright"]
# ///
import json, sys
from playwright.sync_api import sync_playwright
U = json.load(open(sys.argv[1])); OUT = sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width":1400,"height":1000})
    for k, n in (("par","parallel"),("ser","series"),("stk","stack")):
        pg.goto(U[k] + "&v=batch"); pg.wait_for_selector("#view > *"); pg.wait_for_timeout(2500)
        pg.screenshot(path=f"{OUT}/e7b-{n}-batch-pc.png")
        open(f"{OUT}/e7b-{n}-pr-column.txt","w",encoding="utf-8").write(pg.inner_text("#view"))
    b.close()