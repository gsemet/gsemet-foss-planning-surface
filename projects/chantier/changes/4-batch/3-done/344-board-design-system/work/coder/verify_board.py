# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.49"]
# ///
"""Round 3: serve the demo copy (scratch), open the pages, report console errors, take shots."""
import importlib.util, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(sys.argv[1])
OUT = Path(sys.argv[2])
spec = importlib.util.spec_from_file_location("ds", ROOT / "scripts" / "docs_screenshots.py")
ds = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ds)
from playwright.sync_api import sync_playwright

work = Path(tempfile.mkdtemp(prefix="chantier-verify-"))
proc = None
errors = []
try:
    surface = ds.make_surface(work)
    home = work / "home"
    home.mkdir()
    proc, url = ds.start_board(surface, home)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for size, vp in ds.SIZES.items():
            ctx = b.new_context(viewport=vp, locale="en-US", color_scheme="light", reduced_motion="reduce")
            page = ctx.new_page()
            page.on("console", lambda m: errors.append((size, m.type, m.text)) if m.type in ("error", "warning") else None)
            page.on("pageerror", lambda e: errors.append((size, "pageerror", str(e))))
            for name, v, p in [("home", "home", "*"), ("project", "home", "shop-api"), ("batch", "batch", "shop-api"),
                               ("kanban", "kanban", "shop-api"), ("triage", "triage", "shop-api"),
                               ("config", "config", "shop-api")]:
                ds.goto(page, url, v, p)
                if name == "config":
                    tabs = page.locator(".config .ttab")
                    if tabs.count():
                        tabs.nth(1).click(); ds.settle(page)
                page.screenshot(path=str(OUT / f"{name}-{size}.png"), animations="disabled")
            ctx.close()
        b.close()
finally:
    if proc is not None:
        ds.stop(proc)
    shutil.rmtree(work, ignore_errors=True)
print("ERRORS:", errors)
