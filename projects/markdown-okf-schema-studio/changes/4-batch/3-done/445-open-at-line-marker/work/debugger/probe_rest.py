import json, pathlib, sys
sys.path.insert(0, "test/visual")
import capture
from playwright.sync_api import sync_playwright
m = json.loads(capture.MANIFEST.read_text(encoding="utf-8"))
pd = pathlib.Path(m["pageDirectory"])
def find(prefix): return [s for s in m["scenarios"] if s["id"].startswith(prefix)][0]
def reveal(page, line):
    page.evaluate("""(line) => { const r = document.documentElement; window.dispatchEvent(new MessageEvent('message', { data: { type: 'previewRevealLine', line,
      documentId: r.getAttribute('data-sphinx-preview-document-id'), revision: Number(r.getAttribute('data-sphinx-preview-document-version')), requestId: Number(r.getAttribute('data-sphinx-preview-request-id')) } })); }""", line)
    page.wait_for_timeout(500)
with sync_playwright() as p:
    b = p.chromium.launch(args=["--allow-file-access-from-files"])
    # v12 forced colours
    sc = find("lifecycle-sync/v12")
    ctx = b.new_context(viewport={"width": sc["width"], "height": sc["height"]}, forced_colors="active")
    pg = ctx.new_page(); pg.goto((pd / sc["page"]).as_uri()); pg.wait_for_timeout(600); reveal(pg, 22)
    print("v12", pg.evaluate("""() => { const mk = document.querySelector('.sphinx-preview-line-marker'); const a = document.querySelector('.sphinx-preview-line-marker-arrow'); const c = getComputedStyle(mk), d = getComputedStyle(a); return JSON.stringify({bg: c.backgroundColor, border: d.borderInlineStartColor, bl: d.borderLeftColor, forced: matchMedia('(forced-colors: active)').matches}); }"""))
    ctx.close()
    # v11 edit mode list
    sc = find("lifecycle-sync/v11")
    ctx = b.new_context(viewport={"width": sc["width"], "height": sc["height"]})
    pg = ctx.new_page(); pg.goto((pd / sc["page"]).as_uri()); pg.wait_for_timeout(600)
    pg.locator("[data-sphinx-preview-edit-toggle]").click(); pg.wait_for_timeout(400)
    pg.add_style_tag(content='html[data-sphinx-preview-edit-mode="on"] .sphinx-preview-line-marker-arrow { inset-inline-start: calc(var(--sphinx-preview-content-gutter, 16px) - 13px - 1.5em - 6px) !important; }')
    reveal(pg, 47)
    print("v11", pg.evaluate("""() => { const a = document.querySelector('.sphinx-preview-line-marker-arrow').getBoundingClientRect(); const out = []; for (const h of document.querySelectorAll('[data-okf-row-handle-layer] *, .okf-table-row-handle, .okf-table-col-handle, .okf-list-item-handle, [data-okf-block-handle]')) { const x = h.getBoundingClientRect(); if (x.width && x.height && !(x.right <= a.left || x.left >= a.right || x.bottom <= a.top || x.top >= a.bottom)) out.push({cls: h.className, l: Math.round(x.left), r: Math.round(x.right), t: Math.round(x.top), b: Math.round(x.bottom)}); } return JSON.stringify({arrow: {l: Math.round(a.left), r: Math.round(a.right), t: Math.round(a.top), b: Math.round(a.bottom)}, overlaps: out}); }"""))
    # v07 lineTops
    ctx.close()
    # gallery dropdown
    g = [s for s in m["scenarios"] if s["fixture"] == "38-myst-gallery"][0]
    ctx = b.new_context(viewport={"width": 900, "height": 700})
    pg = ctx.new_page(); pg.goto((pd / g["page"]).as_uri()); pg.wait_for_timeout(600); reveal(pg, 13)
    print("gallery dropdown", pg.evaluate("JSON.stringify({open: document.querySelectorAll('details[open]').length, marker: document.querySelectorAll('.sphinx-preview-line-marker').length})"))
    b.close()
