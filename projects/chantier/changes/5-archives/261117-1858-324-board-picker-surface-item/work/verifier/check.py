"""Verifier's browser check: python check.py <head worktree> <code root> <label> <out folder>"""
import sys, tempfile, shutil, importlib.util
from pathlib import Path

HEAD = Path(sys.argv[1])
ROOT = Path(sys.argv[2])  # the code under test
LABEL = sys.argv[3]
OUT = Path(sys.argv[4])
OUT.mkdir(parents=True, exist_ok=True)

spec = importlib.util.spec_from_file_location("ds", HEAD / "scripts" / "docs_screenshots.py")
ds = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ds)
ds.ROOT = ROOT
from playwright.sync_api import sync_playwright

work = Path(tempfile.mkdtemp(prefix="v324-"))
proc = None


def state(page):
    return page.evaluate("() => location.search")


def open_menu(page):
    page.locator('[data-menu="toggle"]').locator("visible=true").first.click()
    page.locator('.menu[role="menu"]').locator("visible=true").first.wait_for()


def surface_row(page):
    return page.locator('.menu .row[data-project="*"]').locator("visible=true").first


try:
    surface = ds.make_surface(work)
    home = work / "home"
    home.mkdir()
    proc, url = ds.start_board(surface, home)
    base = url.split("#")[0]
    sep = "&" if "?" in base else "?"
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        ctx = browser.new_context(viewport=ds.SIZES["pc"], locale="en-US", timezone_id="UTC", color_scheme="light", reduced_motion="reduce")
        ctx.route("**/api/board*", ds.fix_surface_path)
        page = ctx.new_page()
        for view in ["costs", "triage", "kanban", "batch", "prs", "config", "home"]:
            page.goto(f"{base}{sep}p=shop-api&v={view}&lang=en")
            page.wait_for_selector("[data-key]", state="attached")
            ds.settle(page)
            before = state(page)
            open_menu(page)
            surface_row(page).click()
            ds.settle(page)
            after = state(page)
            print(f"[{LABEL}] from {view}: {before} -> {after}")
            page.go_back()
            ds.settle(page)
            print(f"[{LABEL}]   back: {state(page)}")
        page.goto(f"{base}{sep}p=shop-api&v=costs&lang=en")
        ds.settle(page)
        open_menu(page)
        surface_row(page).click()
        ds.settle(page)
        open_menu(page)
        sfc = page.locator(".menu .row[data-project=\"*\"]").locator("visible=true").first
        print(f"[{LABEL}] on overview: sfc class={sfc.get_attribute('class')!r} ok={sfc.locator('.ok').count()}")
        page.locator('.menu .row[data-project="mobile-app"]').locator("visible=true").first.click()
        ds.settle(page)
        print(f"[{LABEL}] picked mobile-app: {state(page)}")
        open_menu(page)
        rows = page.locator(".menu .row").locator("visible=true")
        for i in range(rows.count()):
            r = rows.nth(i)
            print(f"[{LABEL}]   row {i}: class={r.get_attribute('class')!r} ok={r.locator('.ok').count()} text={r.inner_text()!r}")
        print(f"[{LABEL}] menu children: {page.locator('.menu > *').evaluate_all('els => els.map(e => e.tagName + \".\" + e.className)')}")
        print(f"[{LABEL}] weights: sfc={page.locator('.menu .row[data-project="*"] .who > b').first.evaluate('e => getComputedStyle(e).fontWeight')} proj={page.locator('.menu .row:not([data-project="*"]) .who > b').first.evaluate('e => getComputedStyle(e).fontWeight')}")
        print(f"[{LABEL}] padL: sfc={sfc.evaluate('e => getComputedStyle(e).paddingLeft')} proj={page.locator('.menu .row:not([data-project="*"])').first.evaluate('e => getComputedStyle(e).paddingLeft')}")
        page.goto(f"{base}{sep}p=shop-api&v=home&lang=fr")
        ds.settle(page)
        open_menu(page)
        print(f"[{LABEL}] FR header: {page.locator('.menu .row[data-project=\"*\"]').locator('visible=true').first.inner_text()!r}")
        page.goto(f"{base}{sep}p=*&v=costs&lang=en")
        ds.settle(page)
        print(f"[{LABEL}] typed ?p=*&v=costs -> {state(page)}")
        page.reload()
        ds.settle(page)
        print(f"[{LABEL}] reload -> {state(page)}")
        page.goto(f"{base}{sep}p=*&v=home&lang=en")
        ds.settle(page)
        page.goto(base)
        ds.settle(page)
        print(f"[{LABEL}] bare address after choosing surface on Home -> {state(page)}")
        for size, vp, mob in (("pc", ds.SIZES["pc"], False), ("phone", ds.SIZES["phone"], True)):
            c = browser.new_context(viewport=vp, locale="en-US", timezone_id="UTC", color_scheme="light", reduced_motion="reduce", is_mobile=mob, has_touch=mob)
            c.route("**/api/board*", ds.fix_surface_path)
            p = c.new_page()
            p.goto(f"{base}{sep}p=shop-api&v=kanban&lang=en")
            p.wait_for_selector("[data-key]", state="attached")
            ds.settle(p)
            open_menu(p)
            ds.settle(p)
            p.screenshot(path=str(OUT / f"{LABEL}-picker-{size}.png"), animations="disabled", caret="hide")
            c.close()
        browser.close()
finally:
    if proc:
        ds.stop(proc)
    shutil.rmtree(work, ignore_errors=True)
