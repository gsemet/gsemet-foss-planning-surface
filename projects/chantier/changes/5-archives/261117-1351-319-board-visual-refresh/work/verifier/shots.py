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


def run_A(br):
    work, surface, proc, url = instance()
    try:
        for size, vp in (("pc", PC), ("phone", {"width": 375, "height": 812})):
            c = ctx_for(br, vp, size == "phone")
            page = c.new_page()
            for view in ("batch", "costs", "config"):
                goto(page, url, view, "shop-api")
                if view == "config" and size == "pc":
                    page.set_viewport_size({"width": 1400, "height": 1500})
                    page.locator("details.catalog").evaluate("el => { el.open = true; }")
                    page.locator("section.host").nth(1).evaluate("el => el.scrollIntoView({block: 'start'})")
                    page.wait_for_timeout(300)
                page.screenshot(path=str(BA / f"after-{view}-{size}.png"), animations="disabled", caret="hide")
                if view == "config" and size == "pc":
                    page.set_viewport_size(PC)
            c.close()
        c = ctx_for(br, PC, False)
        page = c.new_page()
        goto(page, url, "home", "shop-api")
        page.screenshot(path=str(EV / "project-home-pc.png"))
        facts["project_text"] = page.evaluate("() => document.querySelector('.main').innerText")
        facts["links"] = page.evaluate("() => [...document.querySelectorAll('.main a')].map(a=>a.href)")
        vis(page, '[data-menu="toggle"]').click()
        vis(page, '.menu[role="menu"]').wait_for()
        d.settle(page)
        page.screenshot(path=str(EV / "picker-menu-pc.png"))
        facts["menu_text"] = vis(page, '.menu[role="menu"]').inner_text()
        c.close()
        c = ctx_for(br, PH, True)
        page = c.new_page()
        goto(page, url, "home", "shop-api")
        page.screenshot(path=str(EV / "project-home-390.png"))
        vis(page, '[data-menu="toggle"]').click()
        vis(page, '.menu[role="menu"]').wait_for()
        d.settle(page)
        page.screenshot(path=str(EV / "picker-menu-390.png"))
        c.close()
        c = ctx_for(br, PC, False)
        page = c.new_page()
        logs = []
        page.on("console", lambda m: logs.append(f"{m.type}: {m.text}"))
        goto(page, url, "triage", "shop-api")
        facts["fonts"] = page.evaluate("""() => ({res:[...performance.getEntriesByType('resource')].filter(r=>/woff2/.test(r.name)).map(r=>r.name.replace(/^http:\\/\\/127\\.0\\.0\\.1:\\d+/,'ORIGIN')),
          origins:[...new Set(performance.getEntriesByType('resource').map(r=>new URL(r.name).origin))].map(o=>o===location.origin?'SAME':o),
          h1:(()=>{const e=document.querySelector('h1');const s=getComputedStyle(e);return [e.textContent.trim(),s.fontFamily,s.fontWeight]})(),
          check:document.fonts.check('500 14px Inter'), check400:document.fonts.check('400 14px Inter'),
          loaded:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+' '+f.weight)})""")
        facts["console"] = logs
        c.close()
        for name, vp, ph in (("pc", PC, False), ("390", PH, True)):
            c = ctx_for(br, vp, ph, "fr-FR")
            page = c.new_page()
            for view in ("batch", "home"):
                goto(page, url, view, "shop-api", "fr")
                page.screenshot(path=str(EV / f"fr-{view}-{name}.png"))
                if view == "batch":
                    facts[f"fr_levels_{name}"] = page.evaluate("() => [...document.querySelectorAll('.lvlh')].map(e=>e.textContent.trim())")
            c.close()
        facts["widths"] = {}
        for w, h in ((390, 844), (375, 812)):
            c = ctx_for(br, {"width": w, "height": h}, True)
            page = c.new_page()
            for view, proj in (("home", "*"), ("home", "shop-api"), ("batch", "shop-api"), ("kanban", "shop-api"), ("triage", "shop-api"),
                               ("prs", "shop-api"), ("costs", "shop-api"), ("config", "shop-api")):
                goto(page, url, view, proj)
                facts["widths"][f"{w}:{view}:{proj}"] = page.evaluate("""() => { const sc=document.querySelector('.main')||document.scrollingElement; return {doc:document.documentElement.scrollWidth, inner:innerWidth, main:sc.scrollWidth, mainClient:sc.clientWidth} }""")
            c.close()
        for name, vp, ph in (("pc", PC, False), ("390", PH, True)):
            c = ctx_for(br, vp, ph)
            page = c.new_page()
            hq = """() => { const m=document.querySelector('.main'); const h=document.querySelector('.head'); const cs=getComputedStyle(h);
                   return {scrollTop:m.scrollTop, scrollH:m.scrollHeight, client:m.clientHeight, pos:cs.position, top:h.getBoundingClientRect().top, cls:h.className, shadow:cs.boxShadow, z:cs.zIndex}}"""
            for view in ("triage", "batch", "costs"):
                goto(page, url, view, "shop-api")
                facts[f"sticky_{name}_{view}_top"] = page.evaluate(hq)
                page.evaluate("() => { document.querySelector('.main').scrollTop = 400 }")
                page.wait_for_timeout(300)
                facts[f"sticky_{name}_{view}_scrolled"] = page.evaluate(hq)
                page.screenshot(path=str(EV / f"sticky-{view}-{name}.png"))
                if view == "triage":
                    vis(page, '[data-menu="toggle"]').click()
                    vis(page, '.menu[role="menu"]').wait_for()
                    d.settle(page)
                    page.screenshot(path=str(EV / f"sticky-triage-{name}-menu.png"))
                    facts[f"menu_above_{name}"] = page.evaluate("""() => { const m=document.querySelector('.menu[role=menu]'); const r=m.getBoundingClientRect(); const e=document.elementFromPoint(r.left+r.width/2, r.top+10); return m.contains(e) }""")
                    page.reload()
                    page.wait_for_selector("[data-key]", state="attached")
                    d.settle(page)
                    page.evaluate("() => { document.querySelector('.main').scrollTop = 400 }")
                    page.wait_for_timeout(300)
                    page.get_by_role("button", name="+ New").locator("visible=true").first.click()
                    page.wait_for_selector("dialog[open]")
                    d.settle(page)
                    page.screenshot(path=str(EV / f"sticky-triage-{name}-new.png"))
                    facts[f"dialog_above_{name}"] = page.evaluate("""() => { const m=document.querySelector('dialog[open]'); const r=m.getBoundingClientRect(); const e=document.elementFromPoint(r.left+r.width/2, r.top+10); return m.contains(e) }""")
                    page.keyboard.press("Escape")
                page.evaluate("() => { document.querySelector('.main').scrollTop = 0 }")
                page.wait_for_timeout(300)
                facts[f"sticky_{name}_{view}_back"] = page.evaluate(hq)
            c.close()
    finally:
        d.stop(proc)
        shutil.rmtree(work, ignore_errors=True)


def run_B(br):
    work, surface, proc, url = instance(rename="agentic-planning-surface")
    try:
        for name, vp, ph in (("pc", PC, False), ("390", PH, True)):
            c = ctx_for(br, vp, ph)
            page = c.new_page()
            goto(page, url, "home", "agentic-planning-surface")
            page.screenshot(path=str(EV / f"picker-long-{name}.png"))
            facts[f"long_{name}"] = page.evaluate("""() => { const t=[...document.querySelectorAll('[data-menu="toggle"]')].find(e=>e.getBoundingClientRect().width>0);
               const r=t.getBoundingClientRect(); const all=[...t.querySelectorAll('*')].map(e=>({tag:e.tagName,cls:String(e.getAttribute('class')),t:e.textContent.trim().slice(0,40),r:e.getBoundingClientRect().toJSON(),ov:getComputedStyle(e).textOverflow,sw:e.scrollWidth,cw:e.clientWidth}));
               return {btn:r.toJSON(), kids:all}}""")
            vis(page, '[data-menu="toggle"]').click()
            vis(page, '.menu[role="menu"]').wait_for()
            d.settle(page)
            page.screenshot(path=str(EV / f"picker-long-{name}-menu.png"))
            c.close()
    finally:
        d.stop(proc)
        shutil.rmtree(work, ignore_errors=True)


MEAS = """() => [...document.querySelectorAll('svg.edges path[data-from]')].map(p => { const L=p.getTotalLength(); const e=p.getPointAtLength(L); const q=p.getPointAtLength(L-1); const m=p.getScreenCTM();
    const pt=new DOMPoint(e.x,e.y).matrixTransform(m); const pq=new DOMPoint(q.x,q.y).matrixTransform(m); const to=document.querySelector(`.node[data-id="${p.dataset.to}"]`).getBoundingClientRect();
    const from=document.querySelector(`.node[data-id="${p.dataset.from}"]`).getBoundingClientRect();
    const dy=(to.top+to.height/2)-(from.top+from.height/2);
    return {edge:p.dataset.from+'->'+p.dataset.to, tipX:+pt.x.toFixed(1), targetLeft:+to.left.toFixed(1), gapPx:+(to.left-pt.x).toFixed(1), tipY:+pt.y.toFixed(1), withinCardY:pt.y>=to.top&&pt.y<=to.bottom, lastDirDx:+(pt.x-pq.x).toFixed(3), lastDirDy:+(pt.y-pq.y).toFixed(3), bend:Math.round(dy)} })"""
POS = """() => Object.fromEntries([...document.querySelectorAll('.node')].map(n=>{const r=n.getBoundingClientRect(); const l=n.closest('.lvl'); return [n.dataset.id,{lvl:l.querySelector('.lvlh').textContent.trim(), idx:[...l.querySelectorAll('.node')].indexOf(n), x:Math.round(r.left), y:Math.round(r.top), h:Math.round(r.height), state:n.querySelector('.sb').textContent.trim()}]}))"""


def run_C(br):
    work, surface, proc, url = instance(modify=modify_arrows)
    try:
        c = ctx_for(br, {"width": 1400, "height": 1000}, False)
        page = c.new_page()
        goto(page, url, "batch", "shop-api")
        page.screenshot(path=str(EV / "batch-arrows-pc.png"))
        facts["edges"] = page.evaluate(MEAS)
        facts["levels"] = page.evaluate("() => [...document.querySelectorAll('.lvl')].map(l=>[l.querySelector('.lvlh').textContent.trim(), ...[...l.querySelectorAll('.node')].map(n=>n.dataset.id+':'+n.querySelector('.sb').textContent.trim())])")
        facts["no_groups"] = page.evaluate("() => document.querySelectorAll('.grp,.gh').length")
        facts["page_has_Merged_word"] = page.evaluate("() => /Merged/.test(document.querySelector('.main').innerText)")
        facts["node_colors"] = page.evaluate("() => [...document.querySelectorAll('.node')].map(n=>[n.dataset.id,getComputedStyle(n.querySelector('.sb')).color,getComputedStyle(n).backgroundColor,getComputedStyle(n).borderTopColor])")
        facts["main_text"] = page.evaluate("() => document.querySelector('.main').innerText")
        big = max(facts["edges"], key=lambda e: abs(e["bend"]))
        facts["bigedge"] = big
        tid = big["edge"].split("->")[1]
        box = page.locator(f'.node[data-id="{tid}"]').bounding_box()
        clip = {"x": max(0, box["x"] - 110), "y": max(0, box["y"] - 60), "width": 260, "height": box["height"] + 120}
        c.close()
        c = br.new_context(viewport={"width": 1400, "height": 1000}, locale="en-US", timezone_id="UTC", device_scale_factor=3, reduced_motion="reduce")
        c.clock.set_fixed_time("2026-06-18T10:30:00Z")
        c.route("**/api/board*", d.fix_surface_path)
        page = c.new_page()
        goto(page, url, "batch", "shop-api")
        page.screenshot(path=str(EV / "arrow-closeup-bend.png"), clip=clip)
        c.close()
        c = ctx_for(br, {"width": 1400, "height": 1000}, False)
        page = c.new_page()
        goto(page, url, "batch", "shop-api")
        before = page.evaluate(POS)
        page.locator('.node[data-id="CR-144"]').screenshot(path=str(EV / "state-before-CR-144.png"))
        page.locator('.node[data-id="CR-143"]').screenshot(path=str(EV / "state-before-CR-143.png"))
        page.screenshot(path=str(EV / "state-before-page.png"))
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
        after = page.evaluate(POS)
        facts["state_before"] = before
        facts["state_after"] = after
        page.locator('.node[data-id="CR-144"]').screenshot(path=str(EV / "state-after-CR-144.png"))
        page.locator('.node[data-id="CR-143"]').screenshot(path=str(EV / "state-after-CR-143.png"))
        page.screenshot(path=str(EV / "state-after-page.png"))
        facts["edges_after_state"] = page.evaluate(MEAS)
        c.close()
        c = ctx_for(br, PH, True)
        page = c.new_page()
        goto(page, url, "batch", "shop-api")
        page.screenshot(path=str(EV / "batch-arrows-390.png"))
        facts["edges_phone"] = page.evaluate(MEAS)
        c.close()
    finally:
        d.stop(proc)
        shutil.rmtree(work, ignore_errors=True)


with sync_playwright() as pw:
    br = pw.chromium.launch()
    try:
        for fn in (run_A, run_B, run_C):
            try:
                fn(br)
            except Exception:
                facts[f"ERROR_{fn.__name__}"] = traceback.format_exc()
    finally:
        br.close()
(CR / "work/verifier/facts.json").write_text(json.dumps(facts, indent=1), encoding="utf-8")
print("done", [k for k in facts if k.startswith("ERROR")])
