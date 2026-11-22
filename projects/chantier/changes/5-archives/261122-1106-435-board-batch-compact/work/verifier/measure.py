"""One-off: measure and shoot the Batch page. usage: measure.py <root> <tag> <outdir> <tmp>"""
import json, sys, tempfile
from pathlib import Path

AFTER = Path(r"C:/Users/gaeta/Projets/chantier.worktrees/batch-30-CR-435")
sys.path.insert(0, str(AFTER / "scripts"))
import docs_screenshots as ds
from playwright.sync_api import sync_playwright

root, tag, out, tmp = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
ds.ROOT = root
tmp.mkdir(parents=True, exist_ok=True)
surface = ds.make_surface(tmp)
home = tmp / "home"
home.mkdir(exist_ok=True)
proc, url = ds.start_board(surface, home)
res = {}
JS_BOX = "(sel)=>{const e=document.querySelector(sel); if(!e) return null; const r=e.getBoundingClientRect(); return {l:r.left,t:r.top,r:r.right,b:r.bottom,w:r.width,h:r.height,disp:getComputedStyle(e).display,cur:getComputedStyle(e).cursor}}"
def shot(page, name):
    page.screenshot(path=str(out / f"{name}-{tag}.png"), animations="disabled", caret="hide")
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        for size, vp in ds.SIZES.items():
            ctx = br.new_context(viewport=vp, locale="en-US", timezone_id="UTC", color_scheme="light",
                reduced_motion="reduce", device_scale_factor=1, is_mobile=size == "phone", has_touch=size == "phone")
            ctx.clock.set_fixed_time("2026-06-18T10:30:00Z")
            ctx.route_web_socket("**/api/v1/ws", ds.fix_board_socket)
            ctx.route("**/api/v1/call/board.get", ds.fix_board_call)
            page = ctx.new_page()
            r = {}
            ds.goto(page, url, "batch", "shop-api")
            page.wait_for_selector(".bhead .kpi, .bhead > *", state="attached"); ds.settle(page)
            r["tabs"] = page.evaluate(JS_BOX, ".tabs")
            r["bhead"] = page.evaluate(JS_BOX, ".bhead")
            r["titlerow"] = page.evaluate(JS_BOX, ".titlerow")
            r["scroll"] = page.evaluate("()=>({sw:document.documentElement.scrollWidth,iw:innerWidth})")
            if tag == "after":
                for k in ("#batch-mode", ".mpill", ".lgpill", ".lghint", ".ms"):
                    r[k] = page.evaluate(JS_BOX, k)
            shot(page, f"batch-{size}")
            if tag == "after":
                for pill, tip in ((".mpill", "#mtip"), (".lgpill", "#lgtip")):
                    t = {}
                    if size == "pc":
                        page.hover(pill)
                    else:
                        page.locator(pill).focus()
                    page.wait_for_timeout(300)
                    t["tip"] = page.evaluate(JS_BOX, tip)
                    t["inViewport"] = page.evaluate("(s)=>{const r=document.querySelector(s).getBoundingClientRect();return r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight}", tip)
                    t["hit"] = page.evaluate("""(s)=>{const tip=document.querySelector(s); const r=tip.getBoundingClientRect();
                        const probe=(x,y)=>{const e=document.elementFromPoint(x,y); return {x:Math.round(x),y:Math.round(y),el:e&&(e.className||e.tagName),inTip:!!(e&&tip.contains(e))}};
                        const out={centre:probe((r.left+r.right)/2,(r.top+r.bottom)/2)};
                        const h=document.querySelector('.bhead'); if(h){const b=h.getBoundingClientRect();
                          const x0=Math.max(r.left,b.left),x1=Math.min(r.right,b.right),y0=Math.max(r.top,b.top),y1=Math.min(r.bottom,b.bottom);
                          out.overBhead = (x1>x0&&y1>y0)? probe((x0+x1)/2,(y0+y1)/2):null;
                          const tiles=[...h.children].map(c=>c.getBoundingClientRect()).filter(c=>c.right>r.left&&c.left<r.right&&c.bottom>r.top&&c.top<r.bottom);
                          out.tilesUnderTip=tiles.length;
                          out.overTile = tiles.length? (()=>{const c=tiles[0];const x=(Math.max(c.left,r.left)+Math.min(c.right,r.right))/2,y=(Math.max(c.top,r.top)+Math.min(c.bottom,r.bottom))/2;return probe(x,y)})():null;}
                        return out}""", tip)
                    r["tip" + pill] = t
                    shot(page, f"batch-{size}-tip-{pill[1:]}")
                    if size == "pc":
                        page.mouse.move(5, 500)
                    else:
                        page.evaluate("document.activeElement.blur()")
            res[size] = r
            if size == "pc":
                ds.goto(page, url, "batch&b=batch-01", "mobile-app")
                page.wait_for_selector(".bhead", state="attached"); ds.settle(page)
                shot(page, "closed-pc")
                res["closed_slot"] = page.evaluate("document.querySelector('#batch-mode')?.innerText")
                res["closed_hidden"] = page.evaluate("document.querySelector('#batch-mode')?.hidden")
            ctx.close()
        br.close()
finally:
    ds.stop(proc)
(out / f"measure-{tag}.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
print(json.dumps(res, indent=1))
