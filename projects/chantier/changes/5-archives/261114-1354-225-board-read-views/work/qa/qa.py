# /// script
# dependencies = ["playwright", "pillow"]
# ///
"""Final QA shots for CR-225 (not committed). Serves the prototype copy over a scratch surface's
project, shoots it and the board at 1400x860 and 375x812, and writes compare-<view>-<pc|phone>.png
(prototype left, board right, captioned with the view, the width, the v6 reference and the head).

usage: qa.py <board url with key> <planning folder of the project> <worktree> <project id>
The board must serve the same planning folder (a surface whose project is <project id>).
"""

import pathlib
import shutil
import subprocess
import sys
import time

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

BOARD, PLAN, TREE, PROJECT = sys.argv[1], pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]), sys.argv[4]
HERE = pathlib.Path(__file__).parent
SHOTS = HERE / "shots"
SHOTS.mkdir(exist_ok=True)
PROTO_SRC = pathlib.Path(
    "C:/Users/gaeta/Projets/chantier/.agents/changes/4-batch/2-actives/222-visualization-backend/prototype"
)
PORT = 18790
SHA = subprocess.run(["git", "-C", str(TREE), "rev-parse", "--short=7", "HEAD"], capture_output=True, text=True).stdout.strip()

# view -> (board view, prototype p, v6 reference for the pc, for the phone)
VIEWS = {
    "home": ("home", PROJECT, "v6-09-impeccable-home", "v6-15-semantics-home-phone"),
    "kanban": ("kanban", PROJECT, "v6-13-semantics-kanban-pc", "v6-11-impeccable-phone"),
    "batch": ("batch", PROJECT, "v6-12-semantics-batch-pc", "v6-14-semantics-batch-phone"),
    "costs": ("costs", PROJECT, "none (no v6 shot of Costs)", "none (no v6 shot of Costs)"),
    "all": ("home", "*", "v6-16-all-projects-home-only-pc", "v6-17-all-projects-home-only-phone"),
}
SIZES = {"pc": (1400, 860, False), "phone": (375, 812, True)}


def prepare():
    proto = HERE / "proto"
    if proto.exists():
        shutil.rmtree(proto)
    shutil.copytree(PROTO_SRC, proto, ignore=shutil.ignore_patterns("v1", "data.js"))
    subprocess.run([sys.executable, "-I", str(PROTO_SRC / "snapshot.py"), str(PLAN), str(proto / "data.js")], check=True)
    return proto


def caption(img, text):
    bar = Image.new("RGB", (img.width, 34), (24, 24, 27))
    ImageDraw.Draw(bar).text((10, 10), text, fill=(240, 240, 240))
    out = Image.new("RGB", (img.width, img.height + 34), (24, 24, 27))
    out.paste(bar, (0, 0))
    out.paste(img, (0, 34))
    return out


def compare(view, size, ref):
    left = Image.open(SHOTS / f"proto-{view}-{size}.png").convert("RGB")
    right = Image.open(SHOTS / f"board-{view}-{size}.png").convert("RGB")
    wide = Image.new("RGB", (left.width + right.width + 8, max(left.height, right.height)), (24, 24, 27))
    wide.paste(left, (0, 0))
    wide.paste(right, (left.width + 8, 0))
    text = f"{view} | {left.width}px | prototype (left) vs board (right) | ref {ref} | head {SHA}"
    caption(wide, text).save(SHOTS / f"compare-{view}-{size}.png")


def shoot(browser, url, path, size):
    w, h, mobile = SIZES[size]
    ctx = browser.new_context(viewport={"width": w, "height": h}, is_mobile=mobile, has_touch=mobile)
    page = ctx.new_page()
    errors = []
    page.on("console", lambda m: m.type == "error" and errors.append(m.text))
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.goto(url)
    page.wait_for_selector("#view", state="attached", timeout=20000)
    page.wait_for_timeout(3500)
    page.screenshot(path=str(path))
    ctx.close()
    return errors


def main():
    proto = prepare()
    server = subprocess.Popen(
        [sys.executable, "-I", "-m", "http.server", str(PORT), "--bind", "127.0.0.1", "--directory", str(proto)],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    print("prototype server pid", server.pid)
    time.sleep(1.5)
    base = BOARD.split("?")[0]
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            # the first load carries the key; the later ones keep it
            boot = browser.new_page()
            boot.goto(BOARD)
            boot.wait_for_timeout(2000)
            boot.close()
            for name, (bview, pp, pc_ref, phone_ref) in VIEWS.items():
                for size, ref in (("pc", pc_ref), ("phone", phone_ref)):
                    errs = shoot(browser, f"http://127.0.0.1:{PORT}/?p={pp}&v={bview}", SHOTS / f"proto-{name}-{size}.png", size)
                    bp = "*" if pp == "*" else PROJECT
                    errs += shoot(browser, f"{BOARD}&p={bp}&v={bview}", SHOTS / f"board-{name}-{size}.png", size)
                    compare(name, size, ref)
                    print(name, size, "errors:", errs[:3])
            browser.close()
    finally:
        server.kill()


main()
