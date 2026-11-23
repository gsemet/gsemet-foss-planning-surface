"""Probe: Start-writing gap of 20-empty-document (dark, 900) with the CI marker (1-1) and with no blank run (as a 0-byte file gives)."""
import pathlib, sys
from playwright.sync_api import sync_playwright
src = pathlib.Path(sys.argv[1]); scratch = pathlib.Path(sys.argv[2]); scratch.mkdir(parents=True, exist_ok=True)
html = src.read_text(encoding="utf-8")
assert 'data-okf-blank-runs="1-1"' in html
variants = {"fixture-newline": html, "fixture-0-byte": html.replace('data-okf-blank-runs="1-1"', 'data-okf-blank-runs=""')}
with sync_playwright() as p:
    b = p.chromium.launch()
    for name, text in variants.items():
        f = scratch / (name + ".html"); f.write_text(text, encoding="utf-8")
        page = b.new_page(viewport={"width": 900, "height": 700})
        page.goto(f.as_uri()); page.wait_for_timeout(500)
        page.locator("[data-sphinx-preview-edit-toggle]").click(); page.wait_for_timeout(300)
        r = page.evaluate("""() => { const b=document.querySelector('.sphinx-preview-insert-point--start button').getBoundingClientRect();
          const c=document.querySelector('#sphinx-myst-preview-content').getBoundingClientRect();
          return {buttonTop:b.top, contentTop:c.top, blankBlocks:document.querySelectorAll('.sphinx-preview-blank-lines').length}; }""")
        print(name, r)
    b.close()
