# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.49"]
# ///
"""Verifier's run of CR-440's "In a browser" steps on the demo surface, at the worktree's code."""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
WT = Path(r"C:\Users\gaeta\Projets\chantier.worktrees\batch-30-CR-440")
sys.path.insert(0, str(WT / "scripts"))
import docs_screenshots as ds  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

FOLDER = Path(
    "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/2-actives/440-board-triage-polish"
)
EVID = FOLDER / "evidence"
SCR = FOLDER / "work" / "scratch" / "v"
ds.OUT = SCR / "unused"
RES: list[str] = []


def say(step: str, ok: bool, detail: str = "") -> None:
    line = f"step {step}: {'PASS' if ok else 'FAIL'} {detail}"
    print(line, flush=True)
    RES.append(line)


def vis(page, sel):
    return page.locator(sel).locator("visible=true")


def folded_rows(page):
    return page.evaluate(
        "() => [...document.querySelectorAll('section.column-lane[data-col]')].filter(s => s.classList.contains('column-folded')).map(s => s.dataset.col)"
    )


def lane(page, row):
    return page.locator(f'section.column-lane[data-col="{row}"]').locator("visible=true").first


def count_of(page, row):
    return lane(page, row).locator(".column-head .column-count").inner_text()


def go(page, url, view="triage", project="shop-api", lang="en"):
    base = url.split("#", 1)[0]
    sep = "&" if "?" in base else "?"
    page.goto(f"{base}{sep}p={project}&v={view}&lang={lang}")
    page.wait_for_selector("[data-key]", state="attached")
    ds.settle(page)


def shot(page, name):
    page.screenshot(path=str(EVID / name), animations="disabled", caret="hide")
    print("wrote", name, flush=True)


def drag(page, src, dst_sel):
    src.scroll_into_view_if_needed()
    box = src.bounding_box()
    print("drag", src.get_attribute("data-slug"), box, page.locator(dst_sel).locator("visible=true").first.bounding_box(), flush=True)
    page.mouse.move(box["x"] + box["width"] / 2, box["y"] + 10)
    page.mouse.down()
    dbox = page.locator(dst_sel).locator("visible=true").first.bounding_box()
    page.mouse.move(box["x"] + 20, box["y"] + 30, steps=4)
    page.mouse.move(dbox["x"] + dbox["width"] / 2, dbox["y"] + dbox["height"] / 2, steps=12)
    for k in range(4):
        page.mouse.move(dbox["x"] + dbox["width"] / 2 + k, dbox["y"] + dbox["height"] / 2, steps=2)
        page.wait_for_timeout(120)
    over = page.evaluate(
        "() => [...document.querySelectorAll('.column-lane.over')].map(s => s.dataset.col)"
    )
    page.mouse.up()
    page.wait_for_timeout(900)
    ds.settle(page)
    return over


def main() -> None:
    EVID.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="v-", dir=SCR))
    proc = None
    try:
        surface = ds.make_surface(work)
        mark = surface / "projects/shop-api/changes/2-backlog/P2/saved-addresses/work"
        mark.mkdir(parents=True, exist_ok=True)
        (mark / "running-batch").write_text("2026-06-18T09:00:00Z batch-03\n", encoding="utf-8")
        seed = surface / "projects/shop-api/changes/2-backlog"
        shutil.copytree(seed / "P1/stock-alerts", seed / "P2/returns-policy")
        home = work / "home"
        home.mkdir()
        proc, url = ds.start_board(surface, home)
        run(url)
    finally:
        if proc is not None:
            ds.stop(proc)
        shutil.rmtree(work, ignore_errors=True)
    (SCR / "browser-run.log").write_text("\n".join(RES) + "\n", encoding="utf-8")


def run(url: str) -> None:
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        try:
            pc(browser, url)
            phone(browser, url)
        finally:
            browser.close()


def newctx(browser, phone=False):
    ctx = browser.new_context(
        viewport={"width": 390, "height": 844} if phone else {"width": 1400, "height": 860},
        locale="en-US",
        timezone_id="UTC",
        color_scheme="light",
        reduced_motion="reduce",
        device_scale_factor=1,
        is_mobile=phone,
        has_touch=phone,
    )
    ctx.clock.set_fixed_time("2026-06-18T10:30:00Z")
    ctx.route_web_socket("**/api/v1/ws", ds.fix_board_socket)
    ctx.route("**/api/v1/call/board.get", ds.fix_board_call)
    return ctx


def pc(browser, url):
    ctx = newctx(browser)
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    go(page, url)
    # 1
    rows = ["P1", "P2", "P3", "P4"]
    info = []
    for r in rows:
        b = lane(page, r).locator(".column-fold")
        info.append((r, b.get_attribute("aria-expanded"), b.get_attribute("aria-label"),
                     b.evaluate("e => getComputedStyle(e.querySelector('svg')).transform")))
    say("1", not folded_rows(page) and all(i[1] == "true" for i in info), f"{info}")
    counts0 = {r: count_of(page, r) for r in rows}
    states_html = lane(page, "P2").locator(".column-head").inner_html()
    # 2
    lane(page, "P2").locator(".column-head").click(position={"x": 200, "y": 12})
    page.wait_for_timeout(300)
    hidden = lane(page, "P2").locator(".column-body").evaluate("e => getComputedStyle(e).display")
    pis = vis(page, 'section[data-col="P2"] .pi').count()
    b = lane(page, "P2").locator(".column-fold")
    tr = b.evaluate("e => getComputedStyle(e.querySelector('svg')).transform")
    head_ok = count_of(page, "P2") == counts0["P2"] and bool(lane(page, "P2").locator(".column-head .column-count").count())
    say("2", folded_rows(page) == ["P2"] and hidden == "none" and pis == 0 and
        b.get_attribute("aria-expanded") == "false" and head_ok,
        f"folded={folded_rows(page)} body display={hidden} visible postits={pis} aria-expanded={b.get_attribute('aria-expanded')} label={b.get_attribute('aria-label')!r} svg transform={tr} count {counts0['P2']}->{count_of(page,'P2')} head html before={states_html[:300]!r} after={lane(page,'P2').locator('.column-head').inner_html()[:300]!r}")
    page.mouse.move(5, 5)
    shot(page, "triage-folded-p2-pc-en.png")
    # 3
    stored = page.evaluate("() => localStorage.getItem('chantier.triageFolded')")
    page.reload()
    page.wait_for_selector("[data-key]", state="attached")
    ds.settle(page)
    after_reload = folded_rows(page)
    go(page, url, project="mobile-app")
    other = folded_rows(page)
    go(page, url, project="shop-api")
    say("3", after_reload == ["P2"] and other == ["P2"] and folded_rows(page) == ["P2"],
        f"stored={stored!r} after reload={after_reload} mobile-app triage={other} back={folded_rows(page)}")
    # 4
    btn = page.locator('[data-key="fold-P2"]').locator("visible=true").first
    btn.focus()
    page.keyboard.press("Enter")
    page.wait_for_timeout(300)
    s1 = (folded_rows(page), page.evaluate("() => document.activeElement.dataset.key"))
    page.keyboard.press("Space")
    page.wait_for_timeout(300)
    s2 = (folded_rows(page), page.evaluate("() => document.activeElement.dataset.key"))
    say("4", s1 == ([], "fold-P2") and s2 == (["P2"], "fold-P2"), f"after Enter={s1} after Space={s2}")
    # open P2 for step 5
    page.keyboard.press("Space")
    page.wait_for_timeout(300)
    # 5
    lane(page, "P2").locator(".pi").first.click(position={"x": 6, "y": 6})
    lane(page, "P2").locator(".pi").nth(1).click(position={"x": 6, "y": 6}) if lane(page, "P2").locator(".pi").count() > 1 else None
    sel_before = vis(page, ".selbar").count(), vis(page, ".selbar .n").all_inner_texts()
    nP2 = lane(page, "P2").locator(".pi").count()
    page.locator('[data-key="fold-P2"]').locator("visible=true").first.click()
    page.wait_for_timeout(300)
    bar_after = vis(page, ".selbar").count()
    page.locator('[data-key="fold-P2"]').locator("visible=true").first.click()
    page.wait_for_timeout(300)
    picked = vis(page, ".pi.picked").count()
    r5a = (nP2, sel_before, bar_after, picked)
    # part b: P2 loose post-it + marked CR (saved-addresses, drawn in Running batch)
    running = page.locator('section[data-col="running-batch"] .pi').locator("visible=true")
    run_n = running.count()
    loose = lane(page, "P2").locator(".pi")
    loose_n = loose.count()
    if loose_n:
        loose.first.click(position={"x": 6, "y": 6})
    if run_n:
        running.first.click(position={"x": 6, "y": 6})
    txt1 = vis(page, ".selbar .n").all_inner_texts()
    page.locator('[data-key="fold-P2"]').locator("visible=true").first.click()
    page.wait_for_timeout(300)
    txt2 = vis(page, ".selbar .n").all_inner_texts()
    picked_run = running.locator("xpath=ancestor-or-self::*[contains(@class,'picked')]").count() if run_n else 0
    say("5", nP2 >= 2 and sel_before[0] == 1 and bar_after == 0 and picked == 0 and
        run_n >= 1 and loose_n >= 1 and txt2 and "1" in txt2[0] and "2" in txt1[0],
        f"a: P2 postits={nP2} bar before={sel_before} bar after fold={bar_after} picked after reopen={picked}; b: running postits={run_n} loose P2={loose_n} bar before fold={txt1} after fold={txt2} marked CR (saved-addresses, in Running batch) still selected={page.locator('section[data-col="running-batch"] .pi[aria-label$="selected"]').count()}")
    # leave: clear selection, open P2
    vis(page, '[data-act="clear"]').first.click() if vis(page, ".selbar").count() else None
    page.locator('[data-key="fold-P2"]').locator("visible=true").first.click()  # reopen
    page.wait_for_timeout(300)
    # 6: P2 folded; drag P1 post-it onto head
    if folded_rows(page) != []:
        page.locator('[data-key="fold-P2"]').locator("visible=true").first.click()
    page.locator('[data-key="fold-P2"]').locator("visible=true").first.click()
    page.wait_for_timeout(300)
    c_before = int(count_of(page, "P2"))
    src = lane(page, "P1").locator(".pi").first
    slug1 = src.get_attribute("data-slug")
    over = drag(page, src, 'section[data-col="P2"] .column-head')
    c_after = int(count_of(page, "P2"))
    in_p2_slugs = page.evaluate("() => 0")
    fold_after = folded_rows(page)
    # group by handle: create a group first? check demo has a group in a lane
    grp = page.locator(".gh").locator("visible=true")
    gcount = grp.count()
    gdetail = "no group in demo"
    if gcount:
        g = grp.first
        gname = g.get_attribute("data-gdrag")
        gsize = g.evaluate("e => e.parentElement.querySelectorAll('.pi').length")
        gcol = g.evaluate("e => e.closest('[data-col]').dataset.col")
        if gcol == "P2":
            tgt = "P1"
        else:
            tgt = "P2"
        gdetail = f"group {gname} ({gsize}) from {gcol}"
        if tgt == "P2":
            cb = int(count_of(page, "P2"))
            ov = drag(page, g, 'section[data-col="P2"] .column-head')
            gdetail += f" onto P2: over={ov} count {cb}->{count_of(page, 'P2')} folded={folded_rows(page)}"
    say("6", over == ["P2"] and c_after == c_before + 1 and "P2" in fold_after,
        f"post-it {slug1} P1->P2 head: lit while over={over}; P2 count {c_before}->{c_after}; folded={fold_after}; {gdetail}")
    page.mouse.move(5, 5)
    # 7: select P4 post-it, -> P2
    c7 = int(count_of(page, "P2"))
    p4 = lane(page, "P4").locator(".pi").first
    s7 = p4.get_attribute("data-slug")
    p4.click(position={"x": 6, "y": 6})
    page.locator('.selbar [data-to="P2"]').locator("visible=true").click()
    page.wait_for_timeout(900)
    ds.settle(page)
    say("7", int(count_of(page, "P2")) == c7 + 1 and "P2" in folded_rows(page),
        f"{s7} P4->P2 via selbar: P2 count {c7}->{count_of(page,'P2')} folded={folded_rows(page)}")
    # 8: label filter
    page.locator('[data-lf="checkout"]').locator("visible=true").first.click()
    page.wait_for_timeout(400)
    f_head = (count_of(page, "P2"), lane(page, "P2").locator(".column-head").inner_text().split())
    f_all = {r: (count_of(page, r), lane(page, r).locator(".column-head").inner_text().split()) for r in ["P1", "P2", "P3", "P4"]}
    page.locator('[data-key="fold-P2"]').locator("visible=true").first.click()
    page.wait_for_timeout(300)
    o_head = (count_of(page, "P2"), lane(page, "P2").locator(".column-head").inner_text().split())
    o_pis = lane(page, "P2").locator(".pi").count()
    say("8", f_head == o_head and str(o_pis) == o_head[0],
        f"filter=checkout: folded P2 head={f_head}; opened P2 head={o_head}; visible post-its {o_pis}; folded-state heads of all rows={f_all}")
    page.locator('[data-lf="checkout"]').locator("visible=true").first.click()
    page.wait_for_timeout(300)
    # 9: empty P3
    p3_empty = lane(page, "P3").locator(".pi").count() == 0
    emp_text = lane(page, "P3").locator(".column-body").inner_text()
    page.locator('[data-key="fold-P3"]').locator("visible=true").first.click()
    page.wait_for_timeout(300)
    a = (folded_rows(page), (lane(page, "P3").locator(".column-fold").get_attribute("aria-expanded"), lane(page, "P3").evaluate("e => e.className")))
    page.locator('[data-key="fold-P3"]').locator("visible=true").first.click()
    page.wait_for_timeout(300)
    b = (folded_rows(page), (lane(page, "P3").locator(".column-fold").get_attribute("aria-expanded"), lane(page, "P3").evaluate("e => e.className")))
    page.locator('[data-key="fold-P3"]').locator("visible=true").first.click()
    page.wait_for_timeout(300)
    page.set_viewport_size({"width": 1400, "height": 2000})
    page.wait_for_timeout(400)
    c0 = count_of(page, "P3")
    srcp = lane(page, "P1").locator(".pi").first
    print("step 9 source", srcp.get_attribute("data-slug"), lane(page, "P1").locator(".pi").count(), flush=True)
    ov = drag(page, srcp, 'section[data-col="P3"] .column-head')
    c1 = count_of(page, "P3")
    folded_after_write = folded_rows(page)
    page.set_viewport_size({"width": 1400, "height": 860})
    page.wait_for_timeout(400)
    say("9", p3_empty and a[1][0] == "false" and "column-folded" in a[1][1] and b[1][0] == "true" and "column-folded" not in b[1][1] and "P3" in folded_after_write and c1 == str(int(c0) + 1),
        f"P3 empty={p3_empty} empty text={emp_text.strip()!r}; fold -> {a} (an empty row already hides its body: CSS .column-empty); open -> {b}; write into folded P3 (drop from P1): over={ov} count {c0}->{c1}, folded={folded_after_write}")
    for r in list(folded_rows(page)):
        page.locator(f'[data-key="fold-{r}"]').locator("visible=true").first.click()
        page.wait_for_timeout(200)
    # 10
    page.evaluate("() => { localStorage['chantier.triageFolded'] = 'P9,,{x'; }")
    n_err = len(errors)
    page.reload()
    page.wait_for_selector("[data-key]", state="attached")
    ds.settle(page)
    r10a = folded_rows(page)
    page.evaluate("() => { localStorage['chantier.triageFolded'] = 'P1,P4'; }")
    page.reload()
    page.wait_for_selector("[data-key]", state="attached")
    ds.settle(page)
    r10b = folded_rows(page)
    say("10", r10a == [] and r10b == ["P1", "P4"] and len(errors) == n_err,
        f"'P9,,{{x' -> folded={r10a}; 'P1,P4' -> folded={r10b}; page errors={errors}")
    # 11
    btn = page.locator('[data-key="journal-button"]').locator("visible=true").first
    tip = btn.get_attribute("title")
    btn.click()
    page.wait_for_selector(".dlist")
    ds.settle(page)
    order = page.evaluate("() => [...document.querySelector('.dlist').children].map(e => e.tagName + (e.className ? '.' + e.className.split(' ').join('.') : ''))")
    paras = page.locator(".dlist p.note").all_inner_texts()
    entries = page.locator(".dlist li").all_inner_texts()
    say("11", order[0] == "B" and order[1:4] == ["P.note"] * 3 and order[4].startswith("UL") and order[-1] == "DIV.row" and "rescan" in tip,
        f"tooltip(title)={tip!r}; panel children order={order}; paragraphs={paras}; entries={entries}")
    page.mouse.move(700, 700)
    shot(page, "journal-panel-pc-en.png")
    # 12
    vis(page, "[data-lang]").first.click()
    page.wait_for_timeout(400)
    lang_html = page.evaluate("() => document.documentElement.lang")
    p12 = page.locator(".dlist p.note").all_inner_texts()
    btn12 = page.locator('[data-key="journal-button"]').locator("visible=true").first.get_attribute("title")
    lab12 = {r: page.locator(f'[data-key="fold-{r}"]').locator("visible=true").first.get_attribute("aria-label") for r in ["P1", "P2", "P3", "P4"]}
    say("12", lang_html.startswith("fr") and lab12["P2"] == "Masquer les post-its de P2" and len(p12) == 3,
        f"html lang={lang_html}; paragraphs={p12}; tooltip={btn12!r}; chevron labels={lab12}")
    page.mouse.move(700, 700)
    shot(page, "journal-panel-pc-fr.png")
    vis(page, "[data-lang]").first.click()
    page.wait_for_timeout(400)
    # 14
    n_before = page.locator('[data-key="journal-button"]').locator("visible=true").first.inner_text()
    page.locator('[data-journal="rescan"]').locator("visible=true").first.click()
    page.wait_for_timeout(250)
    toast_txt = page.locator(".toast, [role=status], [role=alert]").all_inner_texts()
    ds.settle(page)
    n_after = page.locator('[data-key="journal-button"]').locator("visible=true").first.inner_text()
    go(page, url, view="home", project="shop-api")
    tile = page.locator("body").inner_text()
    m = [ln for ln in tile.splitlines() if "rescan" in ln.lower() or "written" in ln.lower()]
    say("14", " 0 write" in n_after and any("Counted from now on" in x for x in toast_txt),
        f"button before={n_before!r} after={n_after!r}; toast={toast_txt}; home lines={m}")
    ctx.close()


def phone(browser, url):
    ctx = newctx(browser, phone=True)
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    go(page, url)
    nav = page.evaluate("() => getComputedStyle(document.documentElement).getPropertyValue('--nav-height')")
    navpx = page.evaluate("() => { const d = document.createElement('div'); d.style.height = 'var(--nav-height)'; document.body.appendChild(d); const h = d.getBoundingClientRect().height; d.remove(); return h; }")
    head = page.locator('section[data-col="P2"] .column-head').locator("visible=true").first
    h = head.bounding_box()["height"]
    head.tap(position={"x": 120, "y": 8})
    page.wait_for_timeout(300)
    f1 = folded_rows(page)
    head.tap(position={"x": 120, "y": 8})
    page.wait_for_timeout(300)
    f2 = folded_rows(page)
    head.tap(position={"x": 120, "y": 8})
    page.wait_for_timeout(300)
    f3 = folded_rows(page)
    page.locator('section[data-col="P4"] .column-head').locator("visible=true").first.tap(position={"x": 120, "y": 8})
    page.wait_for_timeout(300)
    page.locator('section[data-col="P2"]').locator("visible=true").first.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    page.mouse.move(1, 1)
    shot(page, "triage-folded-phone.png")
    print("phone folded now", folded_rows(page), flush=True)
    page.locator('[data-key="journal-button"]').locator("visible=true").first.tap()
    page.wait_for_selector(".dlist")
    ds.settle(page)
    wrap = page.evaluate("() => { const e = document.querySelector('.dlist'); return [e.scrollWidth, e.clientWidth, innerWidth, document.documentElement.scrollWidth]; }")
    say("13", h >= navpx and f1 == ["P2"] and f2 == [] and f3 == ["P2"] and wrap[0] <= wrap[1],
        f"--nav-height={nav.strip()} ({navpx}px); head height={h}px; tap folds={f1}, tap opens={f2}, tap folds again={f3}, then P4 folded; panel scrollWidth/clientWidth/viewport/doc={wrap}; page errors={errors}")
    page.locator(".dlist").scroll_into_view_if_needed()
    page.wait_for_timeout(300)
    shot(page, "journal-panel-phone.png")
    ctx.close()


if __name__ == "__main__":
    main()
