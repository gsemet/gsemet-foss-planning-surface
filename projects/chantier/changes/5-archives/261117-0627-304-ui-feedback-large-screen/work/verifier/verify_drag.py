# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.49"]
# ///
"""CR-304 check 4 only: drag and drop at 2940 x 1280, before and after (reuses verify_board.py's helpers)."""
import json, subprocess
from pathlib import Path

src = (Path(__file__).parent / "verify_board.py").read_text(encoding="utf-8").rsplit("\nmain()", 1)[0]
g = {"__name__": "vb"}
exec(compile(src, "verify_board.py", "exec"), g)
from playwright.sync_api import sync_playwright

SCR = g["SCR"]


def drag(pw, side, url, surface):
    r = {}
    br = pw.chromium.launch()
    page = br.new_context(viewport={"width": 2940, "height": 1280}, locale="en-US", timezone_id="UTC", reduced_motion="no-preference").new_page()
    g["goto"](page, url, "triage")
    t0 = g["tree"](surface)
    # an inbox card onto a card of the full P3 row (a group is made)
    src_el = page.locator('.tcol[data-col="inbox"] .pi[data-slug="csv-product-import"]')
    src_el.drag_to(page.locator('.tcol[data-col="P3"] .pi[data-slug="card-3"]'), timeout=8000)
    page.wait_for_selector("dialog[open]", timeout=4000)
    page.fill("dialog[open] input", "newgroup")
    page.locator('dialog[open] [data-do="ok"]').click(); page.wait_for_timeout(1500)
    g["shot"](page, side, "2940", "c4-after-card-on-card")
    t1 = g["tree"](surface)
    r["card_on_card_diff"] = [x for x in t1 if x not in t0] + ["-" + x for x in t0 if x not in t1]
    # a group by its handle to P2
    h = page.locator('.tcol[data-col="P1"] [data-gdrag="checkout-polish"]')
    h.drag_to(page.locator('.tcol[data-col="P2"]'), timeout=8000); page.wait_for_timeout(1500)
    g["shot"](page, side, "2940", "c4-after-group-to-P2")
    t2 = g["tree"](surface)
    r["group_to_p2_diff"] = [x for x in t2 if x not in t1] + ["-" + x for x in t1 if x not in t2]
    br.close()
    return r


procs, out = [], {}
try:
    sides = {}
    for side, code in (("before", g["BEFORE"]), ("after", g["AFTER"])):
        s = g["make_surface"](side)
        p, url = g["start"](side, code, s)
        procs.append(p); sides[side] = (url, s)
        print(side, "pid", p.pid, flush=True)
    with sync_playwright() as pw:
        for side in ("before", "after"):
            try:
                out[side] = drag(pw, side, *sides[side])
            except Exception as e:  # noqa
                out[side] = {"ERROR": repr(e)[:400]}
    out["same_diffs"] = out.get("before", {}).get("card_on_card_diff") == out.get("after", {}).get("card_on_card_diff") and out.get("before", {}).get("group_to_p2_diff") == out.get("after", {}).get("group_to_p2_diff")
    (SCR / "drag.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
finally:
    for p in procs:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
