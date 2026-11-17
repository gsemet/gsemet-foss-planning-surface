# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.49"]
# ///
"""CR-304 browser checks: before (base worktree) and after (head worktree) on scratch copies of docs/demo."""
from __future__ import annotations

import json, os, re, shutil, subprocess, sys, time
from contextlib import contextmanager
from pathlib import Path

from playwright.sync_api import sync_playwright

AFTER = Path(r"C:\Users\gaeta\Projets\chantier.worktrees\batch-22-CR-304")
BEFORE = Path(r"C:\Users\gaeta\Projets\chantier.worktrees\batch-22-CR-304-verify-base")
SCR = Path(r"C:\Users\gaeta\AppData\Local\Temp\claude\f81ba1603abd10b3\91f1382a-eacd-437e-b5a8-f9e545753a8c\scratchpad\run3")
EVID = Path(r"C:\Users\gaeta\Projets\gsemet-foss-planning-surface\projects\chantier\changes\4-batch\2-actives\304-ui-feedback-large-screen\evidence")
SIZES = {"2560": (2560, 1440), "2940": (2940, 1280), "1400": (1400, 860), "375": (375, 812)}
PRO = "shop-api"
HEAD = "| Step | Owner | Input | Output | Duration | Risk | Notes | Rollback | Reviewer | Status |"
SEP = "|" + " --- |" * 10
ROWS = "\n".join(
    "| step-%d | the delivery team | the carrier lead time table and warehouse settings | computed delivery date for each postcode | 12 minutes on average | medium, depends on carrier feeds | long note about the cut-off hour and the weekend rule %d | revert the migration and restore the previous settings | reviewer-%d | done |" % (i, i, i)
    for i in range(6))
WIDE = f"# Round 3\n\n{HEAD}\n{SEP}\n{ROWS}\n"
COVERED = []


def git(*a, cwd):
    subprocess.run(["git", "-c", "core.autocrlf=false", "-c", "user.name=v", "-c", "user.email=v@example.com", *a], cwd=cwd, check=True, capture_output=True)


def card(d, title):
    (d / "intake").mkdir(parents=True)
    (d / "intake" / "request.md").write_text("Request: a plain paragraph of text.\n", encoding="utf-8")
    (d / "summary.json").write_text(json.dumps({"schema": 1, "title": title, "sources": {}, "summary": "s", "origin": {"kind": "verbal"}, "labels": [], "summarized": "2026-06-17T16:05:00Z"}), encoding="utf-8")


def make_surface(side: str) -> Path:
    root = SCR / side
    if root.exists():
        shutil.rmtree(root)
    s = root / "surface"
    shutil.copytree(AFTER / "docs" / "demo", s)
    ch = s / "projects" / PRO / "changes"
    for i in range(6):
        card(ch / "2-backlog" / "P3" / f"card-{i}", f"Card number {i} of the six")
    (ch / "2-backlog" / "P3" / "card-0" / "01-intent.md").write_text("---\ntype: cr-intent\nid: card-0\nstatus: raw\n---\n\n# Card zero\n\nFRONTMATTER-ITEM first paragraph shown on the card.\n", encoding="utf-8")
    card(ch / "2-backlog" / "P1" / "fm-p1", "Frontmatter item in P1")
    (ch / "2-backlog" / "P1" / "fm-p1" / "01-intent.md").write_text("---\ntype: cr-intent\nid: fm-p1\n---\n\n# T\n\nFRONTMATTER-ITEM-P1 paragraph on the card.\n", encoding="utf-8")
    sj = ch / "2-backlog" / "P1" / "stock-alerts" / "summary.json"
    j = json.loads(sj.read_text(encoding="utf-8")); j["group"] = "checkout-polish"; sj.write_text(json.dumps(j), encoding="utf-8")
    (ch / "4-batch" / "2-actives" / "145-delivery-dates" / "work" / "r3.md").write_text(WIDE, encoding="utf-8")
    git("init", "-q", "-b", "main", cwd=s); git("add", "-A", cwd=s); git("commit", "-q", "-m", "demo", cwd=s)
    st = s / ".git" / "ai-autosync"; st.mkdir()
    (st / "control.json").write_text(json.dumps({"enabled": True}), encoding="utf-8")
    (st / "status.json").write_text(json.dumps({"state": "ok", "message": "", "updated_at": 1781778000.0}), encoding="utf-8")
    return s


def start(side: str, code: Path, surface: Path):
    home = SCR / side / "home"; (home / "no-transcripts").mkdir(parents=True)
    env = {**{k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}, "HOME": str(home), "USERPROFILE": str(home), "CHANTIER_ROOT": str(surface), "CHANTIER_CLAUDE_PROJECTS": str(home / "no-transcripts"), "PYTHONUTF8": "1"}
    cmd = ["uv", "run", "--locked", "--project", str(code), "chantier", "board", "--host", "127.0.0.1", "--port", "0", "--clock", "2026-06-18T10:30:00Z"]
    p = subprocess.Popen(cmd, cwd=surface, env=env, stdout=subprocess.PIPE, text=True, encoding="utf-8")
    t0 = time.monotonic()
    while time.monotonic() - t0 < 180:
        line = p.stdout.readline()
        if not line:
            break
        m = re.match(r"board on (\S+) over", line)
        if m:
            return p, m[1]
    raise SystemExit("no address " + side)


def tree(surface: Path):
    out = []
    base = surface / "projects" / PRO / "changes"
    for f in sorted(base.rglob("*")):
        rel = f.relative_to(base).as_posix()
        if f.is_dir() or rel.startswith(("4-batch", "5-arch")):
            continue
        extra = ""
        if f.name == "summary.json":
            extra = " group=%s" % json.loads(f.read_text(encoding="utf-8")).get("group")
        elif f.suffix == ".json":
            extra = " " + f.read_text(encoding="utf-8").replace("\n", "")[:200]
        out.append(rel + extra)
    return out


def goto(page, url, view):
    base = url.split("#")[0]; sep = "&" if "?" in base else "?"
    page.goto(f"{base}{sep}p={PRO}&v={view}&lang=en")
    page.wait_for_selector("[data-key]", state="attached")
    page.wait_for_load_state("networkidle"); page.wait_for_timeout(500)


def vis(page, sel):
    return page.locator(sel).locator("visible=true")


def panel_open(page):
    return page.evaluate("document.querySelector('#panel').classList.contains('open')")


def vparam(page):
    return page.evaluate("new URL(location.href).searchParams.get('v')")


def shot(page, side, size, name):
    EVID.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(EVID / f"{side}-{size}-{name}.png"), animations="disabled", caret="hide")


def open_first_item(page):
    vis(page, '[data-open^="i:"]').first.click()
    page.wait_for_selector('[data-key^="file-"]', state="attached"); page.wait_for_timeout(400)


def view_btn(page, view):
    try:
        vis(page, f'[data-view="{view}"]').first.click(timeout=4000)
    except Exception:
        COVERED.append(view)
        page.evaluate("v => [...document.querySelectorAll('[data-view=\"' + v + '\"]')].filter(e => e.offsetParent).pop().click()", view)
    page.wait_for_timeout(600)


@contextmanager
def sect(r, name):
    try:
        yield
    except Exception as e:  # noqa
        r[name + "_ERROR"] = repr(e)[:300]


def run_side(pw, side, url, surface, size, res):
    w, h = SIZES[size]; phone = size == "375"
    br = pw.chromium.launch()
    ctx = br.new_context(viewport={"width": w, "height": h}, locale="en-US", timezone_id="UTC", color_scheme="light", reduced_motion="no-preference", device_scale_factor=1, is_mobile=phone, has_touch=phone)
    page = ctx.new_page()
    r = res.setdefault(f"{side}/{size}", {})
    with sect(r, "c1a"):
        goto(page, url, "kanban")
        open_first_item(page)
        r["c1_open_on_kanban"] = panel_open(page)
        shot(page, side, size, "c1-panel-open-kanban")
        view_btn(page, "home")
        r["c1_leftbar_home_view"] = vparam(page)
        r["c1_leftbar_home_panel_open"] = panel_open(page)
        shot(page, side, size, "c1-after-leftbar-home")
    with sect(r, "c1b"):
        goto(page, url, "home")
        r["c1_home_openables"] = vis(page, '[data-open]').count()
        vis(page, '[data-open]').first.click(); page.wait_for_timeout(700)
        r["c1_home_panel_open"] = panel_open(page)
        shot(page, side, size, "c1-home-panel-open")
        try:
            vis(page, '[data-go="batch"]').first.click(timeout=4000)
        except Exception:
            r["c1_seebatch_link_covered_by_panel"] = True
            page.evaluate("document.querySelector('[data-go=\"batch\"]').click()")
        page.wait_for_timeout(700)
        r["c1_seebatch_view"] = vparam(page)
        r["c1_seebatch_panel_open"] = panel_open(page)
        shot(page, side, size, "c1-after-see-batch")
    with sect(r, "c1c"):
        goto(page, url, "kanban")
        open_first_item(page)
        view_btn(page, "home")
        page.go_back(); page.wait_for_timeout(800)
        r["c1_back_view"] = vparam(page)
        r["c1_back_panel_open"] = panel_open(page)
        shot(page, side, size, "c1-after-back")
    with sect(r, "c1d"):
        goto(page, url, "kanban")
        vis(page, '[data-open^="i:"][data-open*="saved-addresses"]').first.click()
        page.wait_for_selector('[data-key^="file-"]', state="attached"); page.wait_for_timeout(400)
        vis(page, '[data-file$="03-change-spec.md"]').first.click(); page.wait_for_timeout(500)
        vis(page, '[data-key="edit-start"], [data-edit="start"]').first.click(); page.wait_for_selector("textarea")
        page.fill("textarea", page.input_value("textarea") + "\nunsaved edit\n")
        view_btn(page, "home")
        page.wait_for_selector("dialog[open]", timeout=4000)
        r["c1_dialog_asked"] = True
        shot(page, side, size, "c1-edit-asks")
        page.locator('dialog[open] [data-do="cancel"]').click(); page.wait_for_timeout(600)
        r["c1_stay_view"] = vparam(page)
        r["c1_stay_panel_open"] = panel_open(page)
        r["c1_stay_edit_kept"] = "unsaved edit" in page.input_value("textarea")
        shot(page, side, size, "c1-edit-stay")
    with sect(r, "c3"):
        goto(page, url, "triage")
        r["c3_pi_widths"] = page.evaluate("""() => { const o={}; for (const c of document.querySelectorAll('.tcol')) { o[c.dataset.col] = [...c.querySelectorAll('.pi')].filter(e=>e.offsetParent).map(e=>Math.round(e.offsetWidth)); } return o; }""")
        r["c3_col_widths"] = page.evaluate("""() => Object.fromEntries([...document.querySelectorAll('.tcol')].map(c=>[c.dataset.col, Math.round(c.getBoundingClientRect().width)]))""")
        r["c3_p3_layout"] = page.evaluate("""() => { const cards=[...document.querySelectorAll('.tcol[data-col="P3"] .pi')]; const tops=[...new Set(cards.map(e=>Math.round(e.offsetTop)))]; const dom=cards.map(e=>e.dataset.slug); const v=[...cards].sort((a,b)=>(a.offsetTop-b.offsetTop)||(a.offsetLeft-b.offsetLeft)).map(e=>e.dataset.slug); return {rows:tops.length, cards:cards.length, domOrder:dom.join(','), sameAsVisualOrder: dom.join()===v.join()}; }""")
        r["c3_group"] = page.evaluate("""() => { const f=document.querySelector('.tcol[data-col="P1"] .grpf'); if(!f) return null; const fr=f.getBoundingClientRect(); const m=[...f.querySelectorAll('.pi')].map(e=>e.getBoundingClientRect()); return {frameW:Math.round(fr.width), memberW:m.map(b=>Math.round(b.width)), members:m.length, inside:m.every(b=>b.left>=fr.left-1&&b.right<=fr.right+1&&b.top>=fr.top-1&&b.bottom<=fr.bottom+1)}; }""")
        r["c3_tri_scroll"] = page.evaluate("(() => { const t=document.querySelector('.tri'); return t? {scrollW:t.scrollWidth, clientW:t.clientWidth, overflowX:getComputedStyle(t).overflowX}:null })()")
        shot(page, side, size, "c3-triage")
    with sect(r, "c2"):
        if not phone:
            bars = []; tilts = []
            n = vis(page, ".pi").count()
            for i in range(n):
                c = vis(page, ".pi").nth(i)
                c.scroll_into_view_if_needed(); c.hover(); page.wait_for_timeout(220)
                b = page.evaluate("""() => [...document.querySelectorAll('.tbody,.lanes')].filter(e=>e.scrollWidth>e.clientWidth && ['auto','scroll'].includes(getComputedStyle(e).overflowX)).map(e=>(e.closest('[data-col]')?.dataset.col||e.className)+':'+e.scrollWidth+'>'+e.clientWidth)""")
                tr = c.evaluate("e => getComputedStyle(e).transform")
                if b: bars.append([i, b])
                tilts.append(tr != "none")
            r["c2_cards_hovered"] = n
            r["c2_hovers_showing_hbar"] = len(bars)
            r["c2_hbar_sample"] = bars[:2]
            r["c2_tilted_on_hover"] = f"{sum(tilts)}/{n}"
            page.locator('.tcol[data-col="P3"] .pi').nth(1).scroll_into_view_if_needed()
            page.locator('.tcol[data-col="P3"] .pi').nth(1).hover(); page.wait_for_timeout(300)
            shot(page, side, size, "c2-hover-p3")
            page.locator('.tcol[data-col="inbox"] .pi').first.hover(); page.wait_for_timeout(300)
            shot(page, side, size, "c2-hover-inbox")
    with sect(r, "c4"):
        if size == "2940":
            goto(page, url, "triage")
            t0 = tree(surface)
            src = page.locator('.tcol[data-col="inbox"] .pi').first
            slug = src.get_attribute("data-slug")
            src.drag_to(page.locator('.tcol[data-col="P3"] .pi[data-slug="card-3"]'), timeout=8000); page.wait_for_timeout(1500)
            shot(page, side, size, "c4-after-card-on-card")
            t1 = tree(surface)
            r["c4_card_on_card_diff"] = [x for x in t1 if x not in t0] + ["-" + x for x in t0 if x not in t1]
            h = page.locator('[data-gdrag]').first
            gname = h.get_attribute("data-gdrag")
            h.scroll_into_view_if_needed(); h.drag_to(page.locator('.tcol[data-col="P2"]'), timeout=8000); page.wait_for_timeout(1500)
            shot(page, side, size, "c4-after-group-to-P2")
            t2 = tree(surface)
            r["c4_group_to_p2_diff"] = [x for x in t2 if x not in t1] + ["-" + x for x in t1 if x not in t2]
            r["c4_dragged"] = [slug, gname]
    with sect(r, "c5"):
        out = {}
        for v in ("triage", "kanban", "home"):
            goto(page, url, v)
            txt = page.evaluate("document.body.innerText")
            out[v] = {"shows_card0_paragraph": "FRONTMATTER-ITEM first" in txt, "shows_fm_p1_paragraph": "FRONTMATTER-ITEM-P1" in txt, "shows_raw_frontmatter": ("type: cr-intent" in txt) or ("--- type" in txt)}
            shot(page, side, size, f"c5-{v}")
        r["c5_frontmatter_text"] = out
    with sect(r, "c6"):
        goto(page, url, "batch")
        vis(page, '[data-key^="open-c:CR-145"], [data-key^="node-open-c:CR-145"]').first.click()
        page.wait_for_selector('[data-key^="file-"]', state="attached"); page.wait_for_timeout(500)
        vis(page, '[data-file$="r3.md"]').first.click(); page.wait_for_timeout(800)
        r["c6"] = page.evaluate("""() => { const p=document.querySelector('#panel'); const pr=p.getBoundingClientRect(); const d=p.querySelector('.doc'); const t=d&&d.querySelector('table'); const out={panelW:Math.round(pr.width), panelLeft:Math.round(pr.left), vw:innerWidth, pageHScroll: document.documentElement.scrollWidth>document.documentElement.clientWidth};
          if(d){const dr=d.getBoundingClientRect(); out.docW=Math.round(dr.width); out.docScrollW=d.scrollWidth; out.docOverflowX=getComputedStyle(d).overflowX;}
          if(t){const tr=t.getBoundingClientRect(); out.tableW=Math.round(tr.width); out.tableScrollW=t.scrollWidth; out.tableRight=Math.round(tr.right); out.panelRight=Math.round(pr.right); out.tableDisplay=getComputedStyle(t).display; out.cellWidths=[...t.querySelectorAll('tbody tr:first-child td')].map(c=>Math.round(c.getBoundingClientRect().width)); out.rowH=Math.round(t.querySelector('tbody tr').getBoundingClientRect().height);}
          return out; }""")
        shot(page, side, size, "c6-wide-table-panel")
    ctx.close(); br.close()


def main():
    sides = {}; procs = []
    try:
        for side, code in (("before", BEFORE), ("after", AFTER)):
            s = make_surface(side)
            p, url = start(side, code, s)
            procs.append(p); sides[side] = (url, s)
            print(side, url, "pid", p.pid, flush=True)
        res = {}
        with sync_playwright() as pw:
            for size in SIZES:
                for side in ("before", "after"):
                    url, s = sides[side]
                    try:
                        run_side(pw, side, url, s, size, res)
                    except Exception as e:  # noqa
                        res.setdefault(f"{side}/{size}", {})["FATAL"] = repr(e)[:300]
                    print(side, size, "done", flush=True)
        res["covered_view_clicks_by_js"] = COVERED
        (SCR / "results.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
    finally:
        for p in procs:
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)


main()
