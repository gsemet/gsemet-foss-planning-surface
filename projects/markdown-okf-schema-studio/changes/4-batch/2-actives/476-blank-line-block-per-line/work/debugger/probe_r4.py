import pathlib, sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 900, "height": 700})
    page.goto(pathlib.Path(sys.argv[1]).resolve().as_uri()); page.wait_for_timeout(500)
    page.locator("[data-sphinx-preview-edit-toggle]").click(); page.wait_for_timeout(300)
    for r in page.evaluate("""() => [...document.querySelectorAll('.sphinx-preview-blank-lines, .sphinx-preview-insert-point--start, .sphinx-preview-insert-point--start button, #sphinx-myst-preview-content')].map(e => [e.tagName, e.className, e.getBoundingClientRect().top, e.getBoundingClientRect().height])"""): print(r)
    b.close()
