"""Probe: widths of the six blank-line blocks, the content column, a paragraph (96-blank-lines-six, light, 900)."""
import pathlib, sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(); page = b.new_page(viewport={"width": 900, "height": 700})
    page.goto(pathlib.Path(sys.argv[1]).resolve().as_uri()); page.wait_for_timeout(500)
    page.locator("[data-sphinx-preview-edit-toggle]").click(); page.wait_for_timeout(300)
    print(page.evaluate("""() => { const c=document.querySelector('#sphinx-myst-preview-content');
      const w=e=>Math.round(e.getBoundingClientRect().width*10)/10;
      return {content:w(c), p:w(c.querySelector('p')), blocks:[...c.querySelectorAll('.sphinx-preview-blank-lines')].map(w),
        pad:getComputedStyle(c).paddingLeft+'/'+getComputedStyle(c).paddingRight}; }"""))
    b.close()
