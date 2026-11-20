"""Verifier captures of CR-424: TOC and ordered-list pairs.

usage: python shots.py <worktree root> <before|after> <out dir> <1 if the setting exists>
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright

root = pathlib.Path(sys.argv[1])
prefix = sys.argv[2]
outdir = pathlib.Path(sys.argv[3])
listitems = sys.argv[4] == "1"
src = root / "out/reports/visual/pages/05-long-chapter--light--sticky-3--default.html"
html = src.read_text(encoding="utf-8")
tmp = root / "out/reports/visual/pages/zz-verifier-toc.html"


def variant(li):
    # "toc" lives in initialViewPreferences; the setting is a top-level key of the boot context.
    h = html.replace('"toc":false', '"toc":true', 1)
    return h.replace('"revision":1,', '"revision":1,"listItemsInToc":' + ("true" if li else "false") + ",", 1)


with sync_playwright() as p:
    b = p.chromium.launch()

    def shot(h, w, hgt, name, steps=None):
        tmp.write_text(h, encoding="utf-8")
        pg = b.new_page(viewport={"width": w, "height": hgt})
        pg.goto(tmp.as_uri())
        if steps:
            steps(pg)
        pg.screenshot(path=str(outdir / name))
        pg.close()

    def toc(pg):
        pg.wait_for_selector("[data-sphinx-preview-toc-entry]", state="attached")
        n = pg.locator("[data-sphinx-preview-toc-entry]").count()
        t = pg.locator("[data-sphinx-preview-toc-tick]").count()
        print(prefix, "toc entries", n, "ticks", t)

    shot(variant(listitems), 900, 1000, f"{prefix}-toc-on-light-900.png", toc)
    shot(variant(listitems), 460, 900, f"{prefix}-toc-on-light-460.png", toc)
    if prefix == "after":
        shot(variant(False), 900, 1000, "after-toc-off-light-900.png", toc)

    def ol(pg):
        pg.click("[data-sphinx-preview-edit-toggle]")
        pg.click("main ol > li >> text=Depot reports vehicle availability.")
        pg.wait_for_selector("[data-sphinx-preview-block-editor] textarea")
        print(prefix, "editor:", repr(pg.input_value("[data-sphinx-preview-block-editor] textarea")))
        pg.locator("h2:has-text('Shift changes'), h3:has-text('Shift changes')").first.scroll_into_view_if_needed()
        cdp = pg.context.new_cdp_session(pg)
        nodes = cdp.send("Accessibility.getFullAXTree")["nodes"]
        marks = [
            n["name"]["value"]
            for n in nodes
            if n.get("role", {}).get("value") == "ListMarker" and not n.get("ignored")
        ]
        print(prefix, "list markers:", marks)

    shot(html, 900, 1000, f"{prefix}-ol-item-click-light-900.png", ol)
    tmp.unlink()
    b.close()
