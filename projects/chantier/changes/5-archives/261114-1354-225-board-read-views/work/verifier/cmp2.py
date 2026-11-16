# /// script
# dependencies = ["playwright", "pillow"]
# ///
import json, subprocess, sys, time, pathlib
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright
U = json.load(open(sys.argv[1])); V = pathlib.Path(sys.argv[2]); EV = V / "evidence"; SHA = "7987e83"
srv = subprocess.Popen([sys.executable, "-I", "-m", "http.server", "18791", "--bind", "127.0.0.1", "--directory", str(V / "proto")], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)
def ctx(b, ph):
    return b.new_context(viewport={"width":375,"height":812}, is_mobile=True, has_touch=True) if ph else b.new_context(viewport={"width":1400,"height":860})
def load(pg, board, p, v, side):
    if side == "proto": pg.goto(f"http://127.0.0.1:18791/?p={p}&v={v}")
    else: pg.goto(f"{U['surf']}&p={p}&v={v}")
    pg.wait_for_selector("#view > *", state="attached", timeout=20000); pg.wait_for_timeout(2500)
def act(pg, what, ph, side):
    if what == "picker":
        pg.locator(".pbtn:visible, .ws:visible, [data-menu]:visible").first.click(); pg.wait_for_timeout(500)
    elif what in ("panel", "image"):
        pg.locator("[data-open]", has_text="CR-222").first.click(); pg.wait_for_timeout(2000)
        if what == "image":
            sel = "[data-f$='.png']" if side == "proto" else None
            loc = pg.locator("[data-f$='.png']") if side == "proto" else pg.locator("#panel").get_by_text(".png")
            loc.first.click(); pg.wait_for_timeout(1500)
def comp(name, ref, ph):
    l = Image.open(EV / f"cmp-{name}-proto.png").convert("RGB"); r = Image.open(EV / f"cmp-{name}-board.png").convert("RGB")
    w = Image.new("RGB", (l.width + r.width + 8, max(l.height, r.height)), (24,24,27)); w.paste(l, (0,0)); w.paste(r, (l.width+8, 0))
    out = Image.new("RGB", (w.width, w.height + 34), (24,24,27)); ImageDraw.Draw(out).text((10,10), f"{name} | prototype (left) vs board (right) | ref {ref} | head {SHA}", fill=(240,240,240)); out.paste(w, (0,34)); out.save(EV / f"compare-{name}.png")
with sync_playwright() as pw:
    b = pw.chromium.launch()
    jobs = [("picker-pc","picker","home","v6-01-project-picker",False),("picker-phone","picker","home","v6-03-picker-phone",True),
            ("panel-spec-pc","panel","kanban","v3-06-this-cr-folder",False),("panel-spec-phone","panel","kanban","v6-08-polish-phone",True),
            ("panel-image-pc","image","kanban","v3-06-this-cr-folder",False),
            ("bottombar-project-phone","none","home","v6-08-polish-phone",True)]
    for name, what, view, ref, ph in jobs:
        for side in ("proto","board"):
            c = ctx(b, ph); pg = c.new_page(); load(pg, None, "chantier", view, side)
            try: act(pg, what, ph, side)
            except Exception as e: print("ACT FAIL", name, side, str(e)[:100])
            pg.screenshot(path=str(EV / f"cmp-{name}-{side}.png")); c.close()
        comp(name, ref, ph)
    b.close()
srv.kill()