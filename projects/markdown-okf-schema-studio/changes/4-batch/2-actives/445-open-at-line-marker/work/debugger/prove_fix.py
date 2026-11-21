"""Proof: the same scenarios pass when the reveal message is sent after the pre-scroll checks (as a pageAction would)."""
import json, pathlib, sys
sys.path.insert(0, "test/visual")
import capture
from playwright.sync_api import sync_playwright
m = json.loads(capture.MANIFEST.read_text(encoding="utf-8"))
pd = pathlib.Path(m["pageDirectory"])
orig = capture.check_page_actions
def with_reveal(page, scenario, failures):
    msg = scenario["_reveal"]
    send = lambda: page.evaluate("""(line) => { const r = document.documentElement; window.dispatchEvent(new MessageEvent('message', { data: { type: 'previewRevealLine', line,
      documentId: r.getAttribute('data-sphinx-preview-document-id'), revision: Number(r.getAttribute('data-sphinx-preview-document-version')), requestId: Number(r.getAttribute('data-sphinx-preview-request-id')) } })); }""", msg)
    if scenario.get("_revealLast"):
        orig(page, scenario, failures); send()
    else:
        send(); orig(page, scenario, failures)
    page.wait_for_timeout(300)
capture.check_page_actions = with_reveal
ids = [s["id"] for s in m["scenarios"] if "line-marker" in s["id"]]
with sync_playwright() as p:
    b = p.chromium.launch(args=["--allow-file-access-from-files"])
    for sid in ids:
        sc = [s for s in m["scenarios"] if s["id"] == sid][0]
        hm = sc["render"]["hostMessages"][0]["data"]["line"] if False else None
        # the page file was rendered with the host message; strip nothing: re-dispatch after the checks instead
        line = None
        import re
        txt = (pd / sc["page"]).read_text(encoding="utf-8")
        line = int(re.search(r'previewRevealLine\?","line\?":(\d+)|"previewRevealLine","line":(\d+)', txt).group(1) or re.search(r'"previewRevealLine","line":(\d+)', txt).group(1))
        sc["_reveal"] = line; sc["_revealLast"] = bool(sc.get("pageActions"))
        ctx = b.new_context(viewport={"width": sc["width"], "height": sc["height"]})
        page = ctx.new_page()
        page.check_trace = capture.CheckTrace(); page.check_trace.attach(page)
        page.step_recorder = capture.StepRecorder()
        # load the page without its own early message: block it by dropping the setTimeout dispatch
        page.add_init_script("const _st = window.setTimeout; window.setTimeout = (f, d, ...a) => (String(f).includes('hostContext') ? 0 : _st(f, d, ...a));")
        page.goto((pd / sc["page"]).as_uri())
        fails = []
        capture.run_scenario(page, sc, fails, {"actions": [], "finalState": {}})
        if sid[-14:] != "light-900" or True:
            st = page.evaluate("""() => { const mk = document.querySelector('.sphinx-preview-line-marker'); const t = document.querySelector("p[aria-current='location']"); const b = (e) => e && (({top, bottom, height}) => ({top: Math.round(top), bottom: Math.round(bottom), h: Math.round(height)}))(e.getBoundingClientRect());
              return JSON.stringify({marker: b(mk), para: b(t), curr: [...document.querySelectorAll('[aria-current]')].map(e => e.tagName), details: [...document.querySelectorAll('details')].map(d => d.open), scrollY, forced: matchMedia('(forced-colors: active)').matches}); }""")
            print("   state", st)
        print(sid, "->", "PASS" if not fails else "FAIL " + "; ".join(f.detail[:110] for f in fails))
        ctx.close()
    b.close()
