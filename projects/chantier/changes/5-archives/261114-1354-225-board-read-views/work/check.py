# /// script
# dependencies = ["playwright"]
# ///
"""Throwaway check of the board's reading views: console errors, failed requests, screenshots."""

import json
import pathlib
import sys
import urllib.request

KEY = sys.argv[1]
ONLY = sys.argv[2] if len(sys.argv) > 2 else ""
BASE = "http://127.0.0.1:8792/" if ONLY else "http://127.0.0.1:8791/"
SHOTS = pathlib.Path(__file__).parent / "shots"
SHOTS.mkdir(exist_ok=True)

from playwright.sync_api import sync_playwright  # noqa: E402

problems: list[str] = []


def watch(page, tag):
    page.on("console", lambda m: m.type in ("error", "warning") and problems.append(f"{tag} console {m.type}: {m.text}"))
    page.on("pageerror", lambda e: problems.append(f"{tag} pageerror: {e}"))
    page.on("requestfailed", lambda r: problems.append(f"{tag} failed {r.url}: {r.failure}"))
    page.on("response", lambda r: r.status >= 400 and problems.append(f"{tag} HTTP {r.status} {r.url}"))


with sync_playwright() as p:
    browser = p.chromium.launch()
    for name, size in (("desktop", (1400, 860)), ("phone", (375, 812))):
        ctx = browser.new_context(viewport={"width": size[0], "height": size[1]})
        page = ctx.new_page()
        watch(page, name)
        page.goto(f"{BASE}?k={KEY}")
        page.wait_for_timeout(1500)
        boards = json.loads(page.evaluate("fetch('api/board').then(r => r.text())"))
        project = next((x["id"] for x in boards["projects"] if x.get("batch")), boards["projects"][0]["id"])
        print("project", project, [(x["id"], x.get("batch")) for x in boards["projects"]])
        for view, proj in ((("overview", "*"),) if ONLY else (("home", project), ("kanban", project), ("batch", project), ("costs", project))):
            page.goto(f"{BASE}?p={proj}&v={view}")
            page.wait_for_selector(f".{view}", timeout=20000)
            page.wait_for_timeout(600)
            page.screenshot(path=str(SHOTS / f"{name}-{view}.png"), full_page=False)
            facts = page.evaluate(
                "() => ({cards: document.querySelectorAll('.card').length, nodes: document.querySelectorAll('.node').length,"
                " edges: document.querySelectorAll('svg.edges path[data-from]').length, rows: document.querySelectorAll('tbody tr').length,"
                " tiles: document.querySelectorAll('.kpi').length, empty: document.querySelectorAll('.empty').length,"
                " overflowX: document.documentElement.scrollWidth > window.innerWidth})"
            )
            print(name, view, facts)
        if name == "desktop" and not ONLY:
            page.goto(f"{BASE}?p={project}&v=batch")
            page.wait_for_timeout(1000)
            node = page.locator(".node").first
            node.hover()
            lit = page.evaluate("() => [document.querySelectorAll('.node.dim').length, document.querySelectorAll('.node.hl').length]")
            print("hover dim/hl", lit)
            page.screenshot(path=str(SHOTS / "desktop-batch-hover.png"))
            node.click()
            page.wait_for_timeout(300)
            print("panel open after node click:", page.evaluate("() => document.getElementById('panel').className"))
            page.keyboard.press("Escape")
            page.set_viewport_size({"width": 1000, "height": 700})
            page.wait_for_timeout(500)
            print("edges after resize", page.evaluate("() => document.querySelectorAll('svg.edges path[data-from]').length"))
            page.goto(f"{BASE}?p={project}&v=costs")
            page.wait_for_timeout(800)
            page.click("[data-recompute]")
            page.wait_for_timeout(600)
            print("recompute button:", page.inner_text("[data-recompute]"))
            page.wait_for_timeout(5000)
            print("recompute button later:", page.inner_text("[data-recompute]"))
            page.screenshot(path=str(SHOTS / "desktop-costs-recompute.png"))
            page.goto(f"{BASE}?p={project}&v=kanban")
            page.wait_for_timeout(800)
            page.locator(".card").first.click()
            page.wait_for_timeout(400)
            print("panel after card click:", page.evaluate("() => document.getElementById('panel').className"))
            page.screenshot(path=str(SHOTS / "desktop-kanban-open.png"))
        ctx.close()
    browser.close()

print("PROBLEMS:", len(problems))
for line in problems:
    print(" ", line)
