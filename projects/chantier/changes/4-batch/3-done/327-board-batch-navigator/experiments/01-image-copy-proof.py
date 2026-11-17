# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.49"]
# ///
"""Dev-time proof of the Costs page's "Copy as image", in the browsers installed here.

Usage: 01-image-copy-proof.py <repo-root> <label> <out-folder>
Serves the board over 127.0.0.1 on a copy of docs/demo (via scripts/docs_screenshots.py), clicks
"Copy as image" with a real click, reads image/png back from the clipboard, saves it.
"""
import base64, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

root, label, out = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3])
sys.path.insert(0, str(root / "scripts"))
import tempfile, shutil
import docs_screenshots as d

tmp = Path(tempfile.mkdtemp(prefix="imgcopy-"))
surface = d.make_surface(tmp)
proc, url = d.start_board(surface, tmp / "home")
try:
    with sync_playwright() as pw:
        for name, kw in (("chrome", {"channel": "chrome"}), ("msedge", {"channel": "msedge"}),
                         ("firefox", {})):
            try:
                browser = (pw.firefox if name == "firefox" else pw.chromium).launch(**kw)
            except Exception as e:
                print(f"{name}: not available ({str(e).splitlines()[0][:80]})")
                continue
            ctx = browser.new_context(viewport={"width": 1400, "height": 900}, locale="en-US")
            if name != "firefox":
                ctx.grant_permissions(["clipboard-read", "clipboard-write"])
            page = ctx.new_page()
            msgs = []
            page.on("console", lambda m: msgs.append(m.text))
            d.goto(page, url, "costs", "mobile-app")
            page.locator('[data-key="copy-receipt"]').first.click()
            page.wait_for_timeout(2500)
            toast = page.locator(".toast").all_inner_texts()
            try:
                data = page.evaluate("""async () => {
                  const items = await navigator.clipboard.read();
                  const types = items.flatMap(i => i.types);
                  const b = await items[0].getType('image/png');
                  const buf = new Uint8Array(await b.arrayBuffer());
                  let s = ''; for (const c of buf) s += String.fromCharCode(c);
                  return {types, b64: btoa(s)};
                }""")
                png = base64.b64decode(data["b64"])
                f = out / f"{label}-{name}.png"
                f.write_bytes(png)
                print(f"{name}: {label}: clipboard types {data['types']}, {len(png)} bytes, toast {toast}")
            except Exception as e:
                print(f"{name}: {label}: clipboard read failed: {str(e)[:120]}; toast {toast}; console {msgs[:3]}")
            browser.close()
finally:
    d.stop(proc)
    shutil.rmtree(tmp, ignore_errors=True)
