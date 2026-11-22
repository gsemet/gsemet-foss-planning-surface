import json, pathlib, sys
sys.path.insert(0, "test/visual")
import capture
from playwright.sync_api import sync_playwright
m = json.loads(capture.MANIFEST.read_text(encoding="utf-8"))
pd = pathlib.Path(m["pageDirectory"])
sc = [s for s in m["scenarios"] if s["id"].startswith("lifecycle-sync/v11")][0]
with sync_playwright() as p:
    b = p.chromium.launch(args=["--allow-file-access-from-files"])
    ctx = b.new_context(viewport={"width": 900, "height": 700})
    pg = ctx.new_page(); pg.goto((pd / sc["page"]).as_uri()); pg.wait_for_timeout(600)
    pg.locator("[data-sphinx-preview-edit-toggle]").click(); pg.wait_for_timeout(400)
    pg.evaluate("""() => { const r = document.documentElement; window.dispatchEvent(new MessageEvent('message', { data: { type: 'previewRevealLine', line: 47, documentId: r.getAttribute('data-sphinx-preview-document-id'), revision: 1, requestId: 1 } })); }""")
    pg.wait_for_timeout(500)
    print(pg.evaluate("""() => { const mk = document.querySelector('.sphinx-preview-line-marker'); const a = mk.firstElementChild; const cs = getComputedStyle(a); const col = document.getElementById('sphinx-myst-preview-content').getBoundingClientRect();
      return JSON.stringify({editMode: document.documentElement.getAttribute('data-sphinx-preview-edit-mode'), inset: cs.insetInlineStart, left: cs.left, gutter: getComputedStyle(document.documentElement).getPropertyValue('--sphinx-preview-content-gutter'), gutterOnMain: getComputedStyle(document.getElementById('sphinx-myst-preview-content')).getPropertyValue('--sphinx-preview-content-gutter'), markerLeft: mk.getBoundingClientRect().left, colLeft: col.left, fs: getComputedStyle(a).fontSize}); }"""))
    b.close()
