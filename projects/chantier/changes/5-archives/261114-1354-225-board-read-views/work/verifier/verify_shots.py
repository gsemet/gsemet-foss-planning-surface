# /// script
# dependencies = ["playwright"]
# ///
"""Verifier's throwaway browser proofs for CR-225 (not committed).
usage: verify_shots.py <urls.json>  with keys surf, par, ser, stk, main (board urls with keys)"""

import json
import pathlib
import subprocess
import sys

from playwright.sync_api import sync_playwright

U = json.load(open(sys.argv[1]))
OUT = pathlib.Path(__file__).parent / "evidence"
OUT.mkdir(exist_ok=True)
SHA = "7987e83"
problems, dialogs, foreign = [], [], []


def watch(page, tag, base):
    page.on("console", lambda m: m.type in ("error", "warning") and problems.append(f"{tag} console {m.type}: {m.text}"))
    page.on("pageerror", lambda e: problems.append(f"{tag} pageerror: {e}"))
    page.on("requestfailed", lambda r: problems.append(f"{tag} failed {r.url}: {r.failure}"))
    page.on("response", lambda r: r.status >= 400 and problems.append(f"{tag} HTTP {r.status} {r.url}"))
    page.on("request", lambda r: foreign.append(r.url) if not r.url.startswith(base) and not r.url.startswith(("data:", "blob:")) else None)
    page.on("dialog", lambda d: (dialogs.append(d.message), d.dismiss()))


def origin(u):
    return u.split("/?")[0] + "/"


def ctx(b, phone=False):
    if phone:
        return b.new_context(viewport={"width": 375, "height": 812}, is_mobile=True, has_touch=True)
    return b.new_context(viewport={"width": 1400, "height": 860})


def go(page, key, p=None, v=None, wait=2500):
    url = U[key] + (f"&p={p}" if p else "") + (f"&v={v}" if v else "")
    page.goto(url)
    page.wait_for_selector("#view > *", timeout=20000)
    page.wait_for_timeout(wait)


def text(page, sel):
    return page.locator(sel).inner_text()


with sync_playwright() as pw:
    b = pw.chromium.launch()
    # E7: one PC shot each, with the PR column and graph words
    for key, name in (("par", "parallel"), ("ser", "series"), ("stk", "stack")):
        c = ctx(b)
        pg = c.new_page()
        watch(pg, f"e7-{name}", origin(U[key]))
        go(pg, key, v="batch")
        pg.screenshot(path=str(OUT / f"e7-{name}-batch-pc.png"), full_page=True)
        t = text(pg, "#view")
        (OUT / f"e7-{name}-batch-text.txt").write_text(t, encoding="utf-8")
        print("E7", name, "words:", [w for w in ("PRs to review", "Merge", "waits", "not stacked yet", "blocked", "release", "fix", "Level 1", "after") if w.lower() in t.lower()])
        c.close()

    # E4 on par: markup
    c = ctx(b)
    pg = c.new_page()
    watch(pg, "e4", origin(U["par"]))
    for v in ("home", "kanban", "batch", "costs"):
        go(pg, "par", v=v, wait=1500)
        inj = pg.evaluate("() => document.querySelectorAll('#view img[src=\"x\"], #view b, #view script, #panel script').length")
        has = "<b>bold</b>" in pg.locator("#view").inner_text() or "bold" in pg.locator("#view").inner_text()
        print("E4 view", v, "injected nodes:", inj, "markup shown as text:", "<img src=x" in pg.locator("#view").inner_text())
        if v == "kanban":
            pg.screenshot(path=str(OUT / "e4-kanban.png"))
    go(pg, "par", v="kanban")
    pg.locator("[data-open]", has_text="evilbl").first.click()
    pg.wait_for_timeout(1500)
    pt = text(pg, "#panel")
    print("E4 backlog panel has <script> literal:", "<script>alert(2)</script>" in pt, "injected:", pg.evaluate("() => document.querySelectorAll('#panel script, #panel img[src=\"x\"]').length"))
    pg.screenshot(path=str(OUT / "e4-backlog-panel.png"))
    pg.keyboard.press("Escape")
    go(pg, "par", v="kanban")
    pg.locator("[data-open]", has_text="CR-103").first.click()
    pg.wait_for_timeout(1500)
    print("E4 CR panel head:", text(pg, "#panel")[:200].replace("\n", " | "))
    print("E4 CR tree:", text(pg, "#panel .tree, #panel nav, #panel aside")[:300].replace("\n", " | ") if pg.locator("#panel .tree").count() else "no .tree")
    for name in ("evil.svg", "evil.md"):
        loc = pg.locator("#panel").get_by_text(name).first
        if loc.count():
            loc.click()
            pg.wait_for_timeout(1000)
            print("E4", name, "->", text(pg, "#panel")[-260:].replace("\n", " | "), "| injected:", pg.evaluate("() => document.querySelectorAll('#panel script, #panel iframe, #panel object, #panel embed, #panel a[href^=\"javascript\"]').length"))
            pg.screenshot(path=str(OUT / f"e4-{name}.png"))
    print("E4 dialogs:", dialogs)

    # E6: live refresh with panel open
    pg2 = c.new_page()
    watch(pg2, "e6", origin(U["par"]))
    go(pg2, "par", v="batch")
    pg2.locator("[data-open]").first.click()
    pg2.wait_for_timeout(1200)
    before_file = pg2.locator("#panel").inner_text()[:300]
    proj = pathlib.Path(sys.argv[2])
    subprocess.run(["uv", "run", "--project", sys.argv[3], "chantier", "note", "CR-102", "LIVE-REFRESH-MARK", "--batch", "batch-01"], cwd=proj, capture_output=True)
    subprocess.run(["uv", "run", "--project", sys.argv[3], "chantier", "round", "CR-101", "--batch", "batch-01"], cwd=proj, capture_output=True)
    pg2.wait_for_timeout(9000)
    after = pg2.locator("#panel").inner_text()[:300]
    pg2.screenshot(path=str(OUT / "e6-after.png"))
    ev = pg2.evaluate("() => document.body.innerText.includes('r2/3') ")
    print("E6 panel open after:", pg2.locator("#panel.open, #panel[open], #panel:not([inert])").count(), "same file head:", before_file == after, "round r2/3 visible without reload:", ev)
    c.close()

    # E5: CR-222 folder on surf
    c = ctx(b)
    pg = c.new_page()
    watch(pg, "e5", origin(U["surf"]))
    go(pg, "surf", p="chantier", v="kanban")
    pg.locator("[data-open]", has_text="CR-222").first.click()
    pg.wait_for_timeout(2500)
    (OUT / "e5-tree.txt").write_text(pg.locator("#panel").inner_text(), encoding="utf-8")
    pg.screenshot(path=str(OUT / "e5-panel-spec-pc.png"))
    print("E5 tree text:", pg.locator("#panel").inner_text()[:900].replace("\n", " | "))
    dj = pg.locator("#panel").get_by_text("data.js").first
    if dj.count():
        dj.click()
        pg.wait_for_timeout(1500)
        print("E5 data.js view:", pg.locator("#panel").inner_text()[-300:].replace("\n", " | "))
        pg.screenshot(path=str(OUT / "e5-datajs.png"))
    img = pg.locator("#panel").get_by_text(".png").first
    if img.count():
        img.click()
        pg.wait_for_timeout(1500)
        print("E5 img count in panel:", pg.locator("#panel img").count(), "natural width:", pg.evaluate("() => document.querySelector('#panel img')?.naturalWidth"))
        pg.screenshot(path=str(OUT / "e5-panel-image-pc.png"))
    c.close()
    # panel phone
    c = ctx(b, True)
    pg = c.new_page()
    watch(pg, "e5p", origin(U["surf"]))
    go(pg, "surf", p="chantier", v="kanban")
    pg.locator("[data-open]", has_text="CR-222").first.click()
    pg.wait_for_timeout(2500)
    pg.screenshot(path=str(OUT / "panel-phone.png"))
    c.close()

    # E8 / picker / overview
    c = ctx(b)
    pg = c.new_page()
    watch(pg, "e8main", origin(U["main"]))
    go(pg, "main", v="home")
    print("E8 main picker button:", pg.locator("[data-menu]").count(), "| nav:", text(pg, "#side-nav").replace("\n", " | "))
    pg.screenshot(path=str(OUT / "e8-in-project-home.png"))
    c.close()
    for phone in (False, True):
        sz = "phone" if phone else "pc"
        c = ctx(b, phone)
        pg = c.new_page()
        watch(pg, f"e8surf-{sz}", origin(U["surf"]))
        go(pg, "surf", p="chantier", v="home")
        trig = pg.locator("[data-menu]:visible").first
        trig.click()
        pg.wait_for_timeout(500)
        print("E8", sz, "menu:", pg.locator(".menu:visible").first.inner_text().replace("\n", " | ")[:400])
        pg.screenshot(path=str(OUT / f"picker-{sz}.png"))
        print("E8", sz, "nav (project):", text(pg, "#bottom-nav" if phone else "#side-nav").replace("\n", " | "))
        if phone:
            pg.screenshot(path=str(OUT / "bottombar-project-phone.png"))
        pg.locator('[data-project="*"]:visible').first.click()
        pg.wait_for_timeout(1500)
        print("E8", sz, "overview url:", pg.url[-40:], "nav:", text(pg, "#bottom-nav" if phone else "#side-nav").replace("\n", " | "), "| actions place visible btn:", pg.locator(".head button:visible").count())
        pg.screenshot(path=str(OUT / f"overview-{sz}.png"))
        if phone:
            pg.screenshot(path=str(OUT / "bottombar-all-phone.png"))
        # view chosen from the overview
        pg.goto(U["surf"] + "&p=*&v=home")
        pg.wait_for_timeout(1500)
        pg.locator(("#bottom-nav" if phone else "#side-nav") + " button, " + ("#bottom-nav" if phone else "#side-nav") + " a").first.click()
        pg.wait_for_timeout(800)
        print("E8", sz, "after clicking only view on overview:", pg.url[-60:])
        c.close()
    # Escape and Tab/Enter
    c = ctx(b)
    pg = c.new_page()
    watch(pg, "kbd", origin(U["surf"]))
    go(pg, "surf", p="chantier", v="kanban")
    card = pg.locator("[data-open]").first
    card.focus()
    pg.keyboard.press("Enter")
    pg.wait_for_timeout(1200)
    opened = pg.locator("#panel:not([inert])").count()
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(600)
    closed = pg.locator("#panel[inert]").count()
    print("KBD Enter opens:", opened, "Escape closes:", closed)
    # picker closes on Escape / outside
    pg.locator("[data-menu]:visible").first.click()
    pg.wait_for_timeout(300)
    pg.keyboard.press("Escape")
    pg.wait_for_timeout(300)
    print("KBD menu closed by Escape:", pg.locator(".menu:visible").count() == 0)
    c.close()
    b.close()

print("PROBLEMS:", problems)
print("DIALOGS:", dialogs)
print("FOREIGN REQUESTS:", foreign)
