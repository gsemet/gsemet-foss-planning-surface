# /// script
# dependencies = ["playwright", "pillow"]
# ///
"""Round 4 picker shots (not committed): usage picker.py <board url with key> <worktree> <proto dir>"""
import pathlib, subprocess, sys, time
from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

BOARD, TREE, PROTO = sys.argv[1], sys.argv[2], sys.argv[3]
OUT = pathlib.Path(__file__).parent
SHA = subprocess.run(["git", "-C", TREE, "rev-parse", "--short=7", "HEAD"], capture_output=True, text=True).stdout.strip()
SIZES = {"pc": (1400, 860, False), "phone": (375, 812, True)}
server = subprocess.Popen([sys.executable, "-I", "-m", "http.server", "18791", "--bind", "127.0.0.1", "--directory", PROTO], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1.5)

def shoot(b, url, size, board, path):
    w, h, m = SIZES[size]
    c = b.new_context(viewport={"width": w, "height": h}, is_mobile=m, has_touch=m)
    pg = c.new_page()
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("console", lambda x: x.type == "error" and errs.append(x.text))
    pg.goto(url)
    pg.wait_for_timeout(3500)
    if board:
        btn = pg.locator('[data-menu="toggle"]:visible').first
    else:
        btn = pg.locator(".pwrap button:visible").first
    btn.click()
    pg.wait_for_timeout(500)
    pg.screenshot(path=str(path))
    n = pg.locator(".menu .row .ok:visible").count() if board else pg.locator(".pmenu.open .ok").count()
    print(path.name, "checks:", n, "errors:", errs[:3])
    c.close()

def cap(img, text):
    out = Image.new("RGB", (img.width, img.height + 34), (24, 24, 27))
    ImageDraw.Draw(out).text((10, 10), text, fill=(240, 240, 240))
    out.paste(img, (0, 34))
    return out

try:
    with sync_playwright() as p:
        b = p.chromium.launch()
        boot = b.new_page(); boot.goto(BOARD); boot.wait_for_timeout(2000); boot.close()
        for size in SIZES:
            for tag, bp, pp in (("", "*", "*"), ("-project", "alpha", "chantier")):
                pf = OUT / f"proto-picker{tag}-{size}.png"; bf = OUT / f"board-picker{tag}-{size}.png"
                shoot(b, f"http://127.0.0.1:18791/?p={pp}&v=home", size, False, pf)
                shoot(b, f"{BOARD}&p={bp}&v=home", size, True, bf)
                l, r = Image.open(pf).convert("RGB"), Image.open(bf).convert("RGB")
                wide = Image.new("RGB", (l.width + r.width + 8, max(l.height, r.height)), (24, 24, 27))
                wide.paste(l, (0, 0)); wide.paste(r, (l.width + 8, 0))
                cap(wide, f"picker{tag} | {l.width}px | prototype (left) vs board (right) | ref v6-01-project-picker / v6-03-picker-phone | head {SHA} + uncommitted r4").save(OUT / f"compare-picker{tag}-{size}.png")
        b.close()
finally:
    server.kill()
