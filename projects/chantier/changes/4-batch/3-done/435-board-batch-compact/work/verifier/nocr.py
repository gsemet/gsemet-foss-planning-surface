import sys, json
from pathlib import Path
AFTER = Path(r"C:/Users/gaeta/Projets/chantier.worktrees/batch-30-CR-435")
sys.path.insert(0, str(AFTER / "scripts"))
import docs_screenshots as ds
from playwright.sync_api import sync_playwright
F = Path(r"C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/2-actives/435-board-batch-compact")
home = F / "work/scratch/nhome"; home.mkdir(exist_ok=True)
proc, url = ds.start_board(F / "work/scratch/ncr", home)
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        ctx = br.new_context(viewport={"width":1400,"height":860}, locale="en-US", timezone_id="UTC", reduced_motion="reduce")
        ctx.route_web_socket("**/api/v1/ws", ds.fix_board_socket)
        ctx.route("**/api/v1/call/board.get", ds.fix_board_call)
        page = ctx.new_page()
        page.goto(url.split("#")[0] + ("&" if "?" in url else "?") + "v=batch&lang=en")
        page.wait_for_selector("[data-key]", state="attached"); ds.settle(page)
        print(page.url.split("?")[0][:20], page.evaluate("location.search"))
        print(page.evaluate("({slot:document.querySelector('#batch-mode').innerText, hidden:document.querySelector('#batch-mode').hidden, view:document.querySelector('#view').innerText.slice(0,300)})"))
        page.screenshot(path=str(F/"evidence/nocr-pc-after.png"), animations="disabled", caret="hide")
        br.close()
finally:
    ds.stop(proc)
