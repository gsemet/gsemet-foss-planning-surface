# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.49"]
# ///
"""usage: verify-sel.py CHECKOUT ROOTDIR PROJECT -- selected Triage card: border, outline, focus-visible."""
import os, re, subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

checkout, rootdir, project = sys.argv[1:4]
home = Path(rootdir).parent / "home-sel"; (home / "nt").mkdir(parents=True, exist_ok=True)
env = {**{k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}, "HOME": str(home), "USERPROFILE": str(home),
       "CHANTIER_ROOT": rootdir, "CHANTIER_CLAUDE_PROJECTS": str(home / "nt"), "PYTHONUTF8": "1"}
proc = subprocess.Popen(["uv", "run", "--locked", "--project", checkout, "chantier", "board", "--host", "127.0.0.1",
                         "--port", "0"], cwd=rootdir, env=env, stdout=subprocess.PIPE, text=True, encoding="utf-8")
try:
    url = None
    t0 = time.monotonic()
    while time.monotonic() - t0 < 120:
        m = re.match(r"board on (\S+) over", proc.stdout.readline() or "")
        if m:
            url = m[1]
            break
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        page = b.new_context(viewport={"width": 1500, "height": 900}).new_page()
        page.goto(f"{url}&p={project}&v=triage&lang=en" if "?" in url else f"{url}?p={project}&v=triage&lang=en")
        page.wait_for_selector(".pi")
        page.wait_for_timeout(700)
        js = "e=>{const c=getComputedStyle(e);return {border:c.borderTopWidth+' '+c.borderTopStyle+' '+c.borderTopColor,outline:c.outlineStyle,shadow:c.boxShadow,focusVisible:e.matches(':focus-visible'),focus:e===document.activeElement,cls:e.className}}"
        pi = page.query_selector(".pi")
        print("unselected      ", pi.evaluate(js))
        pi.click(position={"x": 30, "y": 10})
        page.mouse.move(5, 5)
        page.wait_for_timeout(400)
        print("selected (click)", page.eval_on_selector(".pi.sel", js))
        page.keyboard.press("Escape")
        page.locator(".pi").first.focus()
        page.keyboard.press("Tab"); page.keyboard.press("Shift+Tab")
        print("keyboard focus  ", page.evaluate("(()=>{const e=document.activeElement;const c=getComputedStyle(e);return {cls:e.className,focusVisible:e.matches(':focus-visible'),outline:c.outlineStyle+' '+c.outlineWidth+' '+c.outlineColor}})()"))
        b.close()
finally:
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)
