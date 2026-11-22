# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.49"]
# ///
import importlib.util, json, sys, tempfile, shutil
from pathlib import Path
WT = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-30-CR-459")
EV = Path(__file__).resolve().parent.parent / "evidence"
spec = importlib.util.spec_from_file_location("ds", WT / "scripts" / "docs_screenshots.py")
ds = importlib.util.module_from_spec(spec); spec.loader.exec_module(ds)
from playwright.sync_api import sync_playwright
res = {}
def ctxp(br, w, h, phone=False):
    c = br.new_context(viewport={"width": w, "height": h}, locale="en-US", timezone_id="UTC", color_scheme="light",
        reduced_motion="reduce", is_mobile=phone, has_touch=phone)
    c.clock.set_fixed_time("2026-06-18T10:30:00Z")
    c.route_web_socket("**/api/v1/ws", ds.fix_board_socket)
    c.route("**/api/v1/call/board.get", ds.fix_board_call)
    return c
M = """() => { const g=document.querySelector('.gscroll'), gr=document.querySelector('.graph');
 const svgs=[...document.querySelectorAll('svg.edges:not(.top)')].map(s=>s.getBoundingClientRect().height);
 const lv=[...document.querySelectorAll('.lvl')]; const gb=gr.getBoundingClientRect();
 const maxb=Math.max(...lv.map(l=>l.getBoundingClientRect().bottom))-gb.top;
 return {sw:g.scrollWidth,cw:g.clientWidth,sh:g.scrollHeight,ch:g.clientHeight,gh:gb.height,svgh:svgs,maxbottom:maxb,
  order:lv.map(l=>[...l.querySelectorAll('.node')].map(n=>n.dataset.id)),
  chip:(document.querySelector('[data-fold]')||{}).textContent, exp:(document.querySelector('[data-fold]')||{getAttribute(){}}).getAttribute('aria-expanded'),
  n141:document.querySelectorAll('.node[data-id="CR-141"]').length,
  to148:document.querySelectorAll('svg.edges:not(.top) path[data-from][data-to="CR-148"]').length,
  all:document.querySelectorAll('svg.edges:not(.top) path[data-from]').length,
  pagew:[document.documentElement.scrollWidth, innerWidth]}; }"""
def go(p, url, proj, extra):
    p.goto(f"{url}?p={proj}&{extra}&lang=en"); p.wait_for_selector(".graph .node", state="attached"); ds.settle(p)
work = Path(tempfile.mkdtemp(prefix="ev-")); proc=None
try:
    surf = ds.make_surface(work); home = work/"home"; home.mkdir()
    proc, url = ds.start_board(surf, home)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        c = ctxp(br,1600,900); p = c.new_page()
        go(p,url,"shop-api","v=batch&t=graph")
        res["folded"]=p.evaluate(M)
        p.screenshot(path=str(EV/"desktop-folded.png"))
        go(p,url,"shop-api","v=batch&t=graph"); res["order_reload_same"]=p.evaluate(M)["order"]==res["folded"]["order"]
        p.hover('.node[data-id="CR-148"]'); p.wait_for_timeout(300)
        res["hover"]={"hl":p.evaluate("()=>[...document.querySelectorAll('.node.highlight')].map(n=>n.dataset.id)"),
         "top":p.evaluate("()=>({paths:document.querySelectorAll('svg.edges.top path[data-from]').length,heads:document.querySelectorAll('svg.edges.top path.head').length})"),
         "count":p.evaluate("()=>{const n=document.querySelector('.node[data-id=\"CR-148\"]');return [...n.querySelectorAll('[title]')].map(e=>[e.textContent.trim(),e.title])}")}
        p.screenshot(path=str(EV/"desktop-folded-hover-cr148.png"))
        p.mouse.move(5,5)
        p.click("[data-fold]"); p.wait_for_timeout(300); p.mouse.move(5,5)
        res["unfolded"]=p.evaluate(M); p.screenshot(path=str(EV/"desktop-unfolded.png"))
        p.click("[data-fold]"); p.wait_for_timeout(300)
        res["refolded"]=p.evaluate(M)
        go(p,url,"shop-api","v=batch&t=graph")
        p.focus("[data-fold]"); p.keyboard.press("Enter"); p.wait_for_timeout(300)
        res["kbd_exp"]=p.evaluate("()=>document.querySelector('[data-fold]').getAttribute('aria-expanded')")
        go(p,url,"mobile-app","v=batch&b=batch-01&t=graph")
        res["closed"]={"chip":p.evaluate("()=>document.querySelectorAll('[data-fold]').length"),"nodes":p.evaluate("()=>document.querySelectorAll('.node').length"),"m":p.evaluate(M)}
        p.screenshot(path=str(EV/"desktop-closed-record.png"))
        c.close()
        c = ctxp(br,375,812,True); p=c.new_page()
        go(p,url,"shop-api","v=batch&t=graph")
        res["phone"]=p.evaluate(M); p.screenshot(path=str(EV/"phone-folded.png"), full_page=True)
        br.close()
finally:
    if proc: ds.stop(proc)
    shutil.rmtree(work, ignore_errors=True)
(EV/"measures.json").write_text(json.dumps(res,indent=1),encoding="utf-8")
print(json.dumps(res))
