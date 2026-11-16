# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.49"]
# ///
"""usage: verify-sel2.py CHECKOUT ROOTDIR PROJECT SHA7 OUTDIR -- selected vs unselected Triage card, en+fr, plus sidebar line."""
import json, os, re, subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
checkout, rootdir, project, sha, out = sys.argv[1:6]
home = Path(rootdir).parent / "home-sel2"; (home / "nt").mkdir(parents=True, exist_ok=True)
env = {**{k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}, "HOME": str(home), "USERPROFILE": str(home),
       "CHANTIER_ROOT": rootdir, "CHANTIER_CLAUDE_PROJECTS": str(home / "nt"), "PYTHONUTF8": "1"}
proc = subprocess.Popen(["uv", "run", "--locked", "--project", checkout, "chantier", "board", "--host", "127.0.0.1", "--port", "0"],
                        cwd=rootdir, env=env, stdout=subprocess.PIPE, text=True, encoding="utf-8")
try:
    url = None; t0 = time.monotonic()
    while time.monotonic() - t0 < 120:
        m = re.match(r"board on (\S+) over", proc.stdout.readline() or "")
        if m: url = m[1]; break
    base = url.split("#")[0]; sep = "&" if "?" in base else "?"
    js = "e=>{const c=getComputedStyle(e);return {borderColor:c.borderTopColor,borderWidth:c.borderTopWidth,boxShadow:c.boxShadow,outline:c.outlineStyle,cls:e.className}}"
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for lang in ("en", "fr"):
            page = b.new_context(viewport={"width": 1500, "height": 900}).new_page()
            page.goto(f"{base}{sep}p={project}&v=triage&lang={lang}")
            page.wait_for_selector(".pi"); page.wait_for_timeout(800)
            print(lang, "sidebar line:", page.eval_on_selector_all(".project, [class*=proj]", "e=>e.map(x=>x.innerText.replace(/\\n/g,' | ')).slice(0,4)"))
            pis = page.query_selector_all(".pi")
            unsel = pis[1] if len(pis) > 1 else pis[0]
            print(lang, "unselected", unsel.evaluate(js))
            page.query_selector(".pi").click(position={"x": 30, "y": 10})
            page.mouse.move(5, 5); page.wait_for_timeout(500)
            print(lang, "selected  ", page.eval_on_selector(".pi.sel", js))
            print(lang, "check mark:", page.eval_on_selector(".pi.sel", "e=>[...e.querySelectorAll('*')].filter(x=>/chk|check/.test(x.className)).map(x=>x.className)"))
            page.screenshot(path=str(Path(out) / f"triage-selected-{lang}-after-{sha}.png"))
            page.keyboard.press("Escape")
            page.locator(".pi").first.focus(); page.keyboard.press("Tab"); page.keyboard.press("Shift+Tab")
            print(lang, "kbd focus  ", page.evaluate("(()=>{const e=document.activeElement;const c=getComputedStyle(e);return {cls:e.className,fv:e.matches(':focus-visible'),outline:c.outlineStyle+' '+c.outlineWidth+' '+c.outlineColor}})()"))
        b.close()
finally:
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)
