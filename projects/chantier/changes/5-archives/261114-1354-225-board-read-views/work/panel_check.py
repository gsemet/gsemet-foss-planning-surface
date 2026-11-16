# /// script
# dependencies = ["playwright"]
# ///
"""Throwaway check of the board's file panel (round 3). Not part of the repository.

usage: panel_check.py <s1 url with key> <s3 url with key>
s1 = this repo's planning folder (a scratch copy), s3 = the same with the E4 markups.
"""

import pathlib
import sys

from playwright.sync_api import sync_playwright

S1, S3 = sys.argv[1], sys.argv[2]
SHOTS = pathlib.Path(__file__).parent / "shots"
SHOTS.mkdir(exist_ok=True)
problems: list[str] = []
requests: list[str] = []
dialogs: list[str] = []


def watch(page, tag):
    page.on("console", lambda m: m.type in ("error", "warning") and problems.append(f"{tag} console {m.type}: {m.text}"))
    page.on("pageerror", lambda e: problems.append(f"{tag} pageerror: {e}"))
    page.on("requestfailed", lambda r: problems.append(f"{tag} failed {r.url}: {r.failure}"))
    page.on("response", lambda r: r.status >= 400 and problems.append(f"{tag} HTTP {r.status} {r.url}"))
    page.on("request", lambda r: requests.append(r.url))

    def on_dialog(d):
        dialogs.append(d.message)
        d.dismiss()

    page.on("dialog", on_dialog)


def base(url):
    return url.split("?")[0]


def goto(page, url, query):
    page.goto(f"{base(url)}{query}")
    page.wait_for_selector(".view > *", timeout=20000)
    page.wait_for_timeout(700)


def open_card(page, text):
    page.locator(".card", has_text=text).first.click()
    page.wait_for_selector("#panel.open .doc .info", timeout=10000)
    page.wait_for_timeout(500)


def tree_text(page):
    return page.evaluate("() => [...document.querySelectorAll('#panel .tree > *')].map(e => e.className + '|' + e.textContent.trim().replace(/\\s+/g, ' '))")


def run_s1(browser, name, size, mobile):
    ctx = browser.new_context(viewport={"width": size[0], "height": size[1]}, is_mobile=mobile, has_touch=mobile)
    page = ctx.new_page()
    watch(page, name)
    page.goto(S1)
    page.wait_for_timeout(1500)
    goto(page, S1, "?v=kanban")
    # the CR's own folder: the specification is the first file
    open_card(page, "CR-225")
    first = page.inner_text("#panel .doc .info")
    print(name, "CR-225 first file:", first[:90])
    print(name, "headings in doc:", page.evaluate("() => [...document.querySelectorAll('#panel .doc h3,#panel .doc h4')].length"))
    page.screenshot(path=str(SHOTS / f"{name}-panel-spec.png"))
    page.keyboard.press("Escape")
    page.wait_for_timeout(500)
    print(name, "closed by Escape:", "open" not in page.get_attribute("#panel", "class"))
    # visualization-backend's folder: images, data.js listed by size
    open_card(page, "CR-222")
    rows = tree_text(page)
    dirs = [r for r in rows if r.startswith("dir|")]
    print(name, "dirs:", dirs)
    print(name, "own+dirs count:", len(rows))
    big = [r for r in rows if "data.js" in r]
    print(name, "data.js row:", big)
    before = len(requests)
    page.locator("#panel .tree button", has_text="data.js").first.click()
    page.wait_for_timeout(600)
    print(name, "data.js view:", page.inner_text("#panel .doc")[:140].replace("\n", " "))
    print(name, "data.js fetched as text:", any("data.js" in u and "/file?" in u for u in requests[before:]))
    page.locator("#panel .tree button", has_text=".png").first.click() if page.locator("#panel .tree button", has_text=".png").count() else page.locator("#panel .tree button", has_text=".jpg").first.click()
    page.wait_for_timeout(1200)
    img = page.evaluate("() => { const i = document.querySelector('#panel .doc img'); return i ? [i.naturalWidth, i.src.slice(-60)] : null }")
    print(name, "image:", img)
    page.screenshot(path=str(SHOTS / f"{name}-panel-image.png"))
    # stays open and on its file through the live refresh (the poll is 5 s)
    on = page.evaluate("() => document.querySelector('#panel .tree button.on')?.dataset.file")
    page.wait_for_timeout(7000)
    on2 = page.evaluate("() => document.querySelector('#panel .tree button.on')?.dataset.file")
    print(name, "kept its file after refresh:", on == on2 and on is not None, "open:", "open" in page.get_attribute("#panel", "class"))
    page.keyboard.press("Escape")
    ctx.close()


def run_s3(browser, name, size, mobile):
    ctx = browser.new_context(viewport={"width": size[0], "height": size[1]}, is_mobile=mobile, has_touch=mobile)
    page = ctx.new_page()
    watch(page, name)
    page.goto(S3)
    page.wait_for_timeout(1500)
    for view in ("home", "kanban", "batch", "costs"):
        goto(page, S3, f"?v={view}")
        page.screenshot(path=str(SHOTS / f"{name}-e4-{view}.png"))
        print(name, view, "injected nodes:", page.evaluate("() => document.querySelectorAll('.view b, .view img, .view script').length"))
    goto(page, S3, "?v=kanban")
    open_card(page, "CR-225")
    rows = tree_text(page)
    print(name, "evil rows:", [r for r in rows if "evil" in r])
    page.locator("#panel .tree button", has_text="evil.html").first.click()
    page.wait_for_timeout(500)
    print(name, "evil.html view:", page.inner_text("#panel .doc")[:100].replace("\n", " "))
    print(name, "nodes made by evil.html:", page.evaluate("() => document.querySelectorAll('#panel .doc script, #panel .doc img, #panel .doc iframe').length"))
    page.locator("#panel .tree button", has_text="evil.svg").first.click()
    page.wait_for_timeout(500)
    print(name, "evil.svg view:", page.inner_text("#panel .doc")[:120].replace("\n", " "))
    page.screenshot(path=str(SHOTS / f"{name}-e4-panel-svg.png"))
    page.locator("#panel .tree button", has_text="evil.md").first.click()
    page.wait_for_timeout(500)
    print(name, "evil.md nodes:", page.evaluate("() => document.querySelectorAll('#panel .doc script, #panel .doc img, #panel .doc iframe, #panel .doc a').length"))
    page.screenshot(path=str(SHOTS / f"{name}-e4-panel-md.png"))
    page.keyboard.press("Escape")
    goto(page, S3, "?v=kanban")
    page.locator(".card", has_text="evil-item").first.click()
    page.wait_for_selector("#panel.open .doc .info")
    page.wait_for_timeout(500)
    print(name, "item panel title:", page.inner_text("#panel h2"))
    print(name, "item doc nodes:", page.evaluate("() => document.querySelectorAll('#panel .doc script, #panel .doc img, #panel .doc b').length"))
    page.screenshot(path=str(SHOTS / f"{name}-e4-panel-item.png"))
    ctx.close()


with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, size, mobile in (("desktop", (1400, 860), False), ("phone", (375, 812), True)):
        run_s1(browser, name, size, mobile)
        run_s3(browser, name, size, mobile)
    browser.close()

print("DIALOGS:", dialogs)
print("PROBLEMS:", len(problems))
for line in problems:
    print(" ", line)
