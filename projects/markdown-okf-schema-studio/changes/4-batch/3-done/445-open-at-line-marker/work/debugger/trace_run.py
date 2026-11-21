"""Runs the v04 scenario through the real harness (run_scenario) and logs what happens to the marker."""
import json, pathlib, sys
sys.path.insert(0, "test/visual")
import capture
from playwright.sync_api import sync_playwright
m = json.loads(capture.MANIFEST.read_text(encoding="utf-8"))
sc = [s for s in m["scenarios"] if s["id"] == sys.argv[1]][0]
pd = pathlib.Path(m["pageDirectory"])
INIT = """
window.__log = [];
let _acq; Object.defineProperty(window, 'acquireVsCodeApi', { configurable: true, get() { return _acq; }, set(f) { _acq = () => { const api = f(); const pm = api.postMessage; api.postMessage = (m) => { if (m.type === 'previewFindReplace') window.__log.push('POST previewFindReplace dryRun=' + m.dryRun + ' marker=' + document.querySelectorAll('.sphinx-preview-line-marker').length); return pm(m); }; return api; }; } });
const _rm = Element.prototype.remove;
Element.prototype.remove = function() { if (this.classList && this.classList.contains('sphinx-preview-line-marker')) window.__log.push('remove() stack ' + new Error().stack.split(String.fromCharCode(10)).slice(1,7).join(' | ')); return _rm.apply(this, arguments); };
const t0 = performance.now();
const log = (m) => window.__log.push(Math.round(performance.now() - t0) + 'ms ' + m);
document.addEventListener('pointerdown', (e) => log('pointerdown on ' + (e.target.tagName||'') + ' ' + (e.target.className||'') + ' trusted=' + e.isTrusted), true);
document.addEventListener('focusin', (e) => log('focusin ' + e.target.tagName), true);
window.addEventListener('message', (e) => { if (e.data && e.data.type === 'previewRevealLine') log('previewRevealLine received'); }, true);
new MutationObserver((recs) => { for (const r of recs) { for (const n of r.addedNodes) if (n.classList && n.classList.contains('sphinx-preview-line-marker')) log('marker added'); for (const n of r.removedNodes) if (n.classList && n.classList.contains('sphinx-preview-line-marker')) log('marker REMOVED ' + new Error().stack); } }).observe(document, {childList: true, subtree: true});
"""
with sync_playwright() as p:
    b = p.chromium.launch(args=["--allow-file-access-from-files"])
    ctx = b.new_context(viewport={"width": sc["width"], "height": sc["height"]})
    ctx.add_init_script(INIT)
    page = ctx.new_page()
    page.check_trace = capture.CheckTrace(); page.check_trace.attach(page)
    page.step_recorder = capture.StepRecorder()
    _orig = page.check_trace.run
    def _run(name, fn, _o=_orig):
        try: page.evaluate("n => window.__log.push(Math.round(performance.now()) + 'ms >> check ' + n)", name)
        except Exception: pass
        return _o(name, fn)
    page.check_trace.run = _run
    page.goto((pd / sc["page"]).as_uri())
    log0 = page.evaluate("window.__log")
    print("after goto:", log0)
    fails = []; res = {"actions": [], "finalState": {}}
    try:
        capture.run_scenario(page, sc, fails, res)
    except Exception as e:
        print("exc", e)
    print("log:", "\n".join(page.evaluate("window.__log")))
    print("visualMessages", page.evaluate("JSON.stringify(window.visualMessages.map(m=>m.type))"))
    print("markers now", page.evaluate("document.querySelectorAll('.sphinx-preview-line-marker').length"))
    print("actions", res["actions"])
    b.close()
