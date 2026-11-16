# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.49"]
# ///
"""usage: verify-extra.py CHECKOUT ROOTDIR PROJECT SHA7 OUTDIR LABEL
Triage drag on a throwaway copy, focus ring, the cr-folder-self-contained card title, Home first load."""
import json, os, re, subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

checkout, rootdir, project, sha, out, label = sys.argv[1:7]
out = Path(out)
home = Path(rootdir).parent / ("home-x" + label); (home / "nt").mkdir(parents=True, exist_ok=True)
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
assert url
f = {}


def go(page, view, lang="en"):
    base = url.split("#")[0]
    sep = "&" if "?" in base else "?"
    page.goto(f"{base}{sep}p={project}&v={view}&lang={lang}")
    page.wait_for_selector("[data-key]", state="attached")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(700)


try:
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        page = b.new_context(viewport={"width": 1500, "height": 900}).new_page()
        go(page, "kanban")
        f["self_contained_card"] = page.eval_on_selector_all(".card", "e=>e.filter(x=>x.innerText.includes('cr-folder-self-contained')).map(x=>x.querySelector('.ttl').innerText)")
        go(page, "triage")
        f["self_contained_triage"] = page.eval_on_selector_all(".pi", "e=>e.filter(x=>x.innerText.includes('cr-folder-self-contained')).map(x=>x.querySelector('.ttl').innerText)")
        f["data_cols"] = page.eval_on_selector_all("[data-col]", "e=>e.map(x=>x.dataset.col)")
        # keyboard focus ring
        page.mouse.click(700, 5)
        for _ in range(40):
            page.keyboard.press("Tab")
            if page.evaluate("document.activeElement && document.activeElement.classList.contains('pi')"):
                break
        f["focus_on_pi"] = page.evaluate("document.activeElement.classList.contains('pi')")
        f["focus_style"] = page.evaluate("(()=>{const c=getComputedStyle(document.activeElement);return c.outlineStyle+' '+c.outlineWidth+' '+c.outlineColor})()")
        if len(sys.argv) > 7:  # drag
            card = page.query_selector('[data-col="P3"] .pi')
            slug = card.get_attribute("data-slug")
            f["drag_slug"] = slug
            before = page.eval_on_selector_all('[data-col="P4"] .pi', "e=>e.map(x=>x.dataset.slug)")
            page.drag_and_drop(f'[data-slug="{slug}"]', '[data-col="P4"]')
            page.wait_for_timeout(1500)
            f["p1_before"] = before
            f["p1_after"] = page.eval_on_selector_all('[data-col="P4"] .pi', "e=>e.map(x=>x.dataset.slug)")
            f["pi_class_after"] = page.eval_on_selector_all('.pi.drag', "e=>e.length")
        b.close()
finally:
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)
(out / f"extra-{label}-{sha}.json").write_text(json.dumps(f, indent=1, ensure_ascii=False), encoding="utf-8")
print(json.dumps(f, indent=1, ensure_ascii=False))

