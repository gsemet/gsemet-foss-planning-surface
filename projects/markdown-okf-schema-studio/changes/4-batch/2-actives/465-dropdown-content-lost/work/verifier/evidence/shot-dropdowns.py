import sys, pathlib
from playwright.sync_api import sync_playwright
d = pathlib.Path(sys.argv[1]); prefix = sys.argv[2]; dest = pathlib.Path(sys.argv[3]); dest.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    for theme in ["light", "dark"]:
        pg = b.new_page(viewport={"width": 900, "height": 520})
        pg.goto((d / f"page-{theme}.html").as_uri())
        pg.screenshot(path=str(dest / f"{prefix}-{theme}.png"), full_page=True)
        print(theme, pg.evaluate("document.querySelectorAll('details').length"), pg.evaluate("[...document.querySelectorAll('details')].map(d=>d.outerHTML.slice(0,160))"))
    b.close()
