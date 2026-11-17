# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.49"]
# ///
import json, os, re, subprocess, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright

V = Path(sys.argv[1]); OUT = Path(sys.argv[2]); WT = Path(sys.argv[3])
surf = V / "surface"
home = V / "home"
env = {**{k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}, "HOME": str(home),
       "USERPROFILE": str(home), "PYTHONUTF8": "1", "CHANTIER_CLAUDE_PROJECTS": str(home / "nt")}
cmd = ["uv", "run", "--no-sync", "--project", str(WT), "chantier", "--project", "shop-api",
       "board", "--host", "127.0.0.1", "--port", "0", "--clock", "2026-06-18T10:30:00Z"]
p = subprocess.Popen(cmd, cwd=surf, env=env, stdout=subprocess.PIPE, text=True, encoding="utf-8")
try:
    url = None
    t = time.monotonic()
    while time.monotonic() - t < 90:
        line = p.stdout.readline()
        if not line:
            break
        m = re.match(r"board on (\S+) over", line)
        if m:
            url = m[1]
            break
    base = url.split("#")[0]
    sep = "&" if "?" in base else "?"
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        page = b.new_page(viewport={"width": 1400, "height": 860}, locale="en-US")
        page.goto(f"{base}{sep}p=shop-api&v=config&lang=en")
        page.wait_for_selector('.config[data-key="config"]')
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(500)
        page.screenshot(path=str(OUT / "after-config-pc-full.png"), full_page=True)
        txt = page.inner_text(".config")
        i = txt.find("Copilot models")
        print("has Copilot models list:", i >= 0)
        print(txt[i:i + 500] if i >= 0 else "")
        print("overridden text:", "overridden by" in txt)
        b.close()
finally:
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
    p.wait(timeout=30)
    print("stopped", p.pid)
