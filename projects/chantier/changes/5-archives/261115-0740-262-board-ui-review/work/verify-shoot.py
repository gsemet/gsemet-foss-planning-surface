# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.49"]
# ///
"""usage: verify-shoot.py CHECKOUT ROOTDIR PROJECT SHA7 OUTDIR LABEL
Starts `chantier board` of CHECKOUT on ROOTDIR (a throwaway copy), screenshots Kanban, Triage, Costs
and Home in en and fr, writes facts as JSON."""
import json, os, re, subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

checkout, rootdir, project, sha, out, label = sys.argv[1:7]
out = Path(out); out.mkdir(parents=True, exist_ok=True)
home = Path(rootdir).parent / ("home-" + label); (home / "nt").mkdir(parents=True, exist_ok=True)
env = {**{k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}, "HOME": str(home),
       "USERPROFILE": str(home), "CHANTIER_ROOT": rootdir, "CHANTIER_CLAUDE_PROJECTS": str(home / "nt"),
       "PYTHONUTF8": "1"}
proc = subprocess.Popen(["uv", "run", "--locked", "--project", checkout, "chantier", "board", "--host",
                         "127.0.0.1", "--port", "0"], cwd=rootdir, env=env, stdout=subprocess.PIPE,
                        text=True, encoding="utf-8")
url = None
t0 = time.monotonic()
while time.monotonic() - t0 < 120:
    line = proc.stdout.readline()
    if not line:
        break
    m = re.match(r"board on (\S+) over", line)
    if m:
        url = m[1]
        break
assert url, "no board"
facts = {}


def go(page, view, lang):
    base = url.split("#")[0]
    sep = "&" if "?" in base else "?"
    page.goto(f"{base}{sep}p={project}&v={view}&lang={lang}")
    page.wait_for_selector("[data-key]", state="attached")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(700)


def shot(page, name, lang):
    page.screenshot(path=str(out / f"{name}-{lang}-{label}-{sha}.png"))


def text(page, sel):
    return page.inner_text(sel) if page.query_selector(sel) else None


try:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for lang in ("en", "fr"):
            ctx = b.new_context(viewport={"width": 1500, "height": 900}, locale="fr-FR" if lang == "fr" else "en-US")
            page = ctx.new_page()
            f = facts.setdefault(lang, {})
            go(page, "kanban", lang)
            cols = lambda: page.eval_on_selector_all("[data-key^=col-]", "els=>els.map(e=>[e.dataset.key,e.querySelector('h2').innerText,e.querySelector('.c').innerText,e.querySelectorAll('.card').length,(e.querySelector('.cards .none')||{}).innerText||''])")
            f["body_top"] = page.inner_text("body")[:400]
            f["cols"] = cols()
            shot(page, "kanban", lang)
            f["count_line"] = text(page, ".filters .count")
            f["pf_present"] = page.eval_on_selector_all("[data-pf]", "e=>e.map(x=>x.dataset.pf)")
            f["card_titles"] = page.eval_on_selector_all(".card .ttl", "e=>e.map(x=>x.innerText)")
            f["pri_tags_before"] = page.eval_on_selector_all(".col .row-tags .tag", "e=>[...new Set(e.map(x=>x.innerText))]")
            for bkt in ("P3", "P4"):
                if page.query_selector(f'[data-pf="{bkt}"]'):
                    page.click(f'[data-pf="{bkt}"]')
            page.wait_for_timeout(400)
            f["cols_p3p4_off"] = cols()
            f["body_top_after_toggle"] = page.inner_text("body")[:400]
            f["pri_tags_after"] = page.eval_on_selector_all(".col .row-tags .tag", "e=>[...new Set(e.map(x=>x.innerText))]")
            shot(page, "kanban-p3p4-off", lang)
            go(page, "triage", lang)
            shot(page, "triage", lang)
            pi = page.query_selector(".pi")
            if pi:
                f["triage_card_html"] = pi.evaluate("e=>e.outerHTML")[:900]
                f["triage_card_classes"] = pi.get_attribute("class")
                hov = page.query_selector(".pi")
                hov.hover()
                page.wait_for_timeout(400)
                f["hover_transform"] = hov.evaluate("e=>getComputedStyle(e).transform")
                f["hover_shadow"] = hov.evaluate("e=>getComputedStyle(e).boxShadow")
                shot(page, "triage-hover", lang)
                pi.click(position={"x": 30, "y": 10})
                page.wait_for_timeout(300)
                page.mouse.move(5, 5)
                page.wait_for_timeout(300)
                f["sel_count"] = len(page.query_selector_all(".pi.sel"))
                if f["sel_count"]:
                    f["sel_style"] = page.eval_on_selector(".pi.sel", "e=>{const c=getComputedStyle(e);return {outline:c.outlineStyle+' '+c.outlineWidth+' '+c.outlineColor,shadow:c.boxShadow,hasChk:!!e.querySelector('.chk')}}")
                shot(page, "triage-selected", lang)
            go(page, "costs", lang)
            shot(page, "costs", lang)
            f["costs_text"] = page.inner_text("body")[:1800]
            f["hist_rows"] = page.eval_on_selector_all("[data-hist]", "e=>e.map(x=>x.dataset.hist)")
            if f["hist_rows"]:
                page.click("[data-hist]")
                page.wait_for_timeout(300)
                f["unfold_rows"] = page.eval_on_selector_all("tr.sub tbody tr", "e=>e.length")
                shot(page, "costs-unfolded", lang)
                page.click("[data-hist]")
                page.wait_for_timeout(300)
                f["refold_rows"] = page.eval_on_selector_all("tr.sub tbody tr", "e=>e.length")
            go(page, "home", lang)
            shot(page, "home", lang)
            f["home_text"] = page.inner_text("body")[:2500]
            ctx.close()
        b.close()
finally:
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)
(out / f"facts-{label}-{sha}.json").write_text(json.dumps(facts, indent=1, ensure_ascii=False), encoding="utf-8")
print("done", out)
