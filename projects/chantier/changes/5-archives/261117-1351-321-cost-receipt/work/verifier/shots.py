# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.49"]
# ///
"""Verifier: capture the Costs page of the head in three states, plus the two mock-ups."""
import importlib.util
import json
import shutil
import sys
import tempfile
from pathlib import Path

R = Path(sys.argv[1])
OUT = Path(sys.argv[2])
MOCK = Path(sys.argv[3])
spec = importlib.util.spec_from_file_location("ds", R / "scripts" / "docs_screenshots.py")
ds = importlib.util.module_from_spec(spec)
sys.modules["ds"] = ds
spec.loader.exec_module(ds)
from playwright.sync_api import sync_playwright  # noqa: E402

OUT.mkdir(parents=True, exist_ok=True)


def run_case(name, project, mutate):
    Path("C:/vfdemo").mkdir(exist_ok=True); work = Path(tempfile.mkdtemp(prefix="vf-", dir="C:/vfdemo"))
    proc = None
    try:
        surface = ds.make_surface(work)
        home = work / "home"
        home.mkdir()
        mutate(surface)
        proc, url = ds.start_board(surface, home)
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            for size, vp in ds.SIZES.items():
                ctx = b.new_context(
                    viewport=vp, locale="en-US", timezone_id="UTC", color_scheme="light",
                    reduced_motion="reduce", device_scale_factor=1,
                    is_mobile=size == "phone", has_touch=size == "phone",
                )
                ctx.clock.set_fixed_time("2026-06-18T10:30:00Z")
                ctx.route("**/api/board*", ds.fix_surface_path)
                page = ctx.new_page()
                ds.goto(page, url, "costs", project)
                page.wait_for_function("() => !document.body.innerText.includes('recomputing')", timeout=30000)
                page.screenshot(path=str(OUT / f"after-{name}-{size}.png"),
                                animations="disabled", caret="hide")
                txt = page.locator("[aria-label^='Cost receipt']").first.inner_text()
                print("TEXT", name, size, txt.replace("\n", " | ")[:400])
                ctx.close()
            b.close()
    finally:
        if proc:
            ds.stop(proc)
        shutil.rmtree(work, ignore_errors=True)


def strip(surface):
    p = surface / "projects/mobile-app/changes/5-archives/batches/batch-02.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    d["cost_receipt"] = None
    p.write_text(json.dumps(d), encoding="utf-8")


run_case("full", "mobile-app", lambda s: None)
run_case("norecord", "mobile-app", strip)
run_case("notcomputed", "shop-api", lambda s: None)
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for f, size in (("final-costs.html", "pc"), ("final-costs-phone.html", "phone")):
        ctx = b.new_context(viewport=ds.SIZES[size], is_mobile=size == "phone")
        pg = ctx.new_page()
        pg.goto((MOCK / f).as_uri())
        pg.wait_for_timeout(800)
        pg.screenshot(path=str(OUT / f"mockup-{size}.png"))
        ctx.close()
    b.close()
