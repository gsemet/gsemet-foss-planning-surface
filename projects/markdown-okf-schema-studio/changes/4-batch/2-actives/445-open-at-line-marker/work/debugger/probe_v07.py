import json, pathlib, sys
sys.path.insert(0, "test/visual")
import capture
from playwright.sync_api import sync_playwright
m = json.loads(capture.MANIFEST.read_text(encoding="utf-8"))
pd = pathlib.Path(m["pageDirectory"])
sc = [s for s in m["scenarios"] if s["id"].startswith("lifecycle-sync/v07")][0]
with sync_playwright() as p:
    b = p.chromium.launch(args=["--allow-file-access-from-files"])
    ctx = b.new_context(viewport={"width": 900, "height": 700})
    pg = ctx.new_page(); pg.goto((pd / sc["page"]).as_uri()); pg.wait_for_timeout(800)
    pg.evaluate("window.scrollTo(0,0)")
    print(pg.evaluate("""() => { const p = document.querySelector('main p'); const out = {html: p.innerHTML.slice(0, 120), top: p.getBoundingClientRect().top + scrollY, h: p.getBoundingClientRect().height};
      const starts = ['A soft wrapped', 'The second source', 'The third source'];
      const tn = []; const w = document.createTreeWalker(p, NodeFilter.SHOW_TEXT); let n; while (n = w.nextNode()) tn.push(n);
      out.tops = {}; for (const s of starts) { for (const t of tn) { const i = t.data.indexOf(s); if (i >= 0) { const r = document.createRange(); r.setStart(t, i); r.setEnd(t, i + 1); out.tops[s] = Math.round(r.getBoundingClientRect().top + scrollY); } } }
      return JSON.stringify(out); }"""))
    pg.evaluate("""() => { const r = document.documentElement; window.dispatchEvent(new MessageEvent('message', { data: { type: 'previewRevealLine', line: 5, documentId: r.getAttribute('data-sphinx-preview-document-id'), revision: 1, requestId: 1 } })); }""")
    pg.wait_for_timeout(500)
    print(pg.evaluate("JSON.stringify({marker: document.querySelector('.sphinx-preview-line-marker').getBoundingClientRect().top + scrollY, scrollY})"))
    b.close()
