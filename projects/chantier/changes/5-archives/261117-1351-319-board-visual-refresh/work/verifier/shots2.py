# /// script
# dependencies = ["playwright>=1.49"]
# ///
import json, os, shutil, sys, tempfile, traceback
from pathlib import Path

sys.path.insert(0, "C:/Users/gaeta/Projets/chantier.worktrees/batch-23-CR-319/scripts")
import docs_screenshots as d
from playwright.sync_api import sync_playwright

CR = Path("C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier/changes/4-batch/2-actives/319-board-visual-refresh")
EV = CR / "evidence"
BA = CR / "work/verifier/evidence"
PC = {"width": 1400, "height": 860}
PH = {"width": 390, "height": 844}
facts = {}


def ctx_for(br, vp, phone, lang="en-US"):
    c = br.new_context(viewport=vp, locale=lang, timezone_id="UTC", color_scheme="light", reduced_motion="reduce",
                       device_scale_factor=1, is_mobile=phone, has_touch=phone)
    c.clock.set_fixed_time("2026-06-18T10:30:00Z")
    c.route("**/api/board*", d.fix_surface_path)
    return c


def instance(modify=None, rename=None):
    work = Path(tempfile.mkdtemp(prefix="vf-"))
    surface = d.make_surface(work)
    if rename:
        os.rename(surface / "projects/shop-api", surface / "projects" / rename)
    if modify:
        modify(surface)
    home = work / "home"
    home.mkdir()
    proc, url = d.start_board(surface, home)
    return work, surface, proc, url


def batch_path(surface, proj="shop-api"):
    return surface / "projects" / proj / "changes/4-batch/batch.json"


def modify_arrows(surface):
    p = batch_path(surface)
    b = json.loads(p.read_text(encoding="utf-8"))
    base = dict(b["crs"][-3])

    def mk(i, after):
        c = dict(base)
        c.update(id=f"CR-{i}", title=f"Change Specification: Verifier case {i}", status="queued", order=i - 140,
                 after=after, pr=None, head=None, agent=None, cost_usd=0.0, path=f"4-batch/1-pending/{i}-case", round=0)
        for k in ("phase", "phase_at", "stacked", "rounds", "merged_at"):
            c.pop(k, None)
        c["blocked_reason"] = None
        return c

    b["crs"] += [mk(150, ["CR-149"]), mk(151, ["CR-150"]), mk(152, ["CR-141"])]
    p.write_text(json.dumps(b, indent=1), encoding="utf-8")


def goto(page, url, view, proj, lang="en"):
    base = url.split("#")[0]
    sep = "&" if "?" in base else "?"
    page.goto(f"{base}{sep}p={proj}&v={view}&lang={lang}")
    page.wait_for_selector("[data-key]", state="attached")
    d.settle(page)


def vis(page, sel):
    return page.locator(sel).locator("visible=true").first



def run_A2(br):
    work, surface, proc, url = instance()
    try:
        for name, vp, ph in (("pc", PC, False), ("390", PH, True)):
            c = ctx_for(br, vp, ph)
            page = c.new_page()
            goto(page, url, "home", "shop-api")
            page.evaluate("() => { const m=document.querySelector('.main'); m.scrollTop=m.scrollHeight }")
            page.wait_for_timeout(300)
            page.screenshot(path=str(EV / f"project-section-{name}.png"))
            c.close()
        # menu probe at a row
        for name, vp, ph in (("pc", PC, False), ("390", PH, True)):
            c = ctx_for(br, vp, ph)
            page = c.new_page()
            goto(page, url, "triage", "shop-api")
            page.evaluate("() => { document.querySelector('.main').scrollTop = 400 }")
            page.wait_for_timeout(300)
            vis(page, '[data-menu="toggle"]').click()
            vis(page, '.menu[role="menu"]').wait_for()
            d.settle(page)
            facts[f"menu_probe_{name}"] = page.evaluate("""() => { const rows=[...document.querySelectorAll('.menu[role=menu] [role=menuitem], .menu[role=menu] button')]; const out=rows.map(b=>{const r=b.getBoundingClientRect(); const e=document.elementFromPoint(r.left+r.width/2, r.top+r.height/2); return [b.textContent.trim().slice(0,20), b.contains(e)]}); const h=document.querySelector('.head'); const m=document.querySelector('.menu[role=menu]'); return {rows:out, headZ:getComputedStyle(h).zIndex, menuZ:getComputedStyle(m).zIndex, menuPos:getComputedStyle(m).position, menuTop:m.getBoundingClientRect().top, headBottom:h.getBoundingClientRect().bottom}}""")
            c.close()
        # fonts
        c = ctx_for(br, PC, False)
        page = c.new_page()
        reqs = []
        logs = []
        page.on("response", lambda r: reqs.append((r.url.replace(url.split("?")[0].rstrip("/"), "ORIGIN"), r.status, r.headers.get("content-type"), r.headers.get("content-security-policy"))))
        page.on("console", lambda m: logs.append(f"{m.type}: {m.text}"))
        page.on("pageerror", lambda e: logs.append(f"pageerror: {e}"))
        goto(page, url, "triage", "shop-api")
        facts["responses_font"] = [r for r in reqs if "woff2" in r[0] or r[0].endswith("/") or "index" in r[0] or "css" in r[0]]
        facts["response_hosts"] = sorted({r[0].split("/")[0] + r[0].split("/")[2] if r[0].startswith("http") else r[0][:6] for r in reqs})
        facts["console2"] = logs
        facts["fontcheck"] = page.evaluate("""() => ({h1: (()=>{const s=getComputedStyle(document.querySelector('h1'));return [s.fontFamily.slice(0,10), s.fontWeight]})(), loaded:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+' '+f.weight)})""")
        c.close()
    finally:
        d.stop(proc)
        shutil.rmtree(work, ignore_errors=True)


def run_C2(br):
    work, surface, proc, url = instance(modify=modify_arrows)
    try:
        c = ctx_for(br, {"width": 1400, "height": 1000}, False)
        page = c.new_page()
        goto(page, url, "batch", "shop-api")
        page.screenshot(path=str(EV / "state-before-page.png"))
        before = page.evaluate(POS)
        p = batch_path(surface)
        b = json.loads(p.read_text(encoding="utf-8"))
        for cr in b["crs"]:
            if cr["id"] == "CR-144":
                cr["status"] = "ready"
            if cr["id"] == "CR-143":
                cr["status"] = "merged"
                cr["merged_at"] = "2026-06-18T10:20:00Z"
        p.write_text(json.dumps(b, indent=1), encoding="utf-8")
        page.reload()
        page.wait_for_selector("[data-key]", state="attached")
        d.settle(page)
        page.screenshot(path=str(EV / "state-after-page.png"))
        after = page.evaluate(POS)
        facts["state2_before"] = before
        facts["state2_after"] = after
        c.close()
    finally:
        d.stop(proc)
        shutil.rmtree(work, ignore_errors=True)


with sync_playwright() as pw:
    br = pw.chromium.launch()
    try:
        for fn in (run_A2, run_C2):
            try:
                fn(br)
            except Exception:
                facts[f"ERROR_{fn.__name__}"] = traceback.format_exc()
    finally:
        br.close()
(CR / "work/verifier/facts2.json").write_text(json.dumps(facts, indent=1), encoding="utf-8")
print("done", [k for k in facts if k.startswith("ERROR")])
