# /// script
# requires-python = ">=3.11"
# dependencies = ["playwright>=1.49"]
# ///
"""usage: drive.py <chantier checkout> <out dir> <tag>   (verifier's browser checks, scratch surface)"""
import json, os, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(sys.argv[1]); OUT = Path(sys.argv[2]); TAG = sys.argv[3]
DEMO = Path(r"C:\Users\gaeta\Projets\chantier.worktrees\batch-22-CR-305\docs\demo")
OUT.mkdir(parents=True, exist_ok=True)
SIZES = {"pc": {"width": 1400, "height": 860}, "phone": {"width": 375, "height": 812}}
LONG = "../../../../some/very/long/relative/path/to/the/code/repository/checkout/that/goes/on/and/on/"
git = ("git", "-c", "user.name=v", "-c", "user.email=v@example.com")


def mk(tmp):
    s = tmp / "surface"
    shutil.copytree(DEMO, s)
    (s / "projects/shop-api/checkout.yml").write_text(f"repo: {LONG}\nworktrees: .worktrees\n", encoding="utf-8")
    (s / "projects/mobile-app/checkout.yml").write_text("worktrees: .worktrees\n", encoding="utf-8")
    for a in (("init", "-q", "-b", "main"), ("add", "-A"), ("commit", "-q", "-m", "x")):
        subprocess.run([*git, *a], cwd=s, check=True)
    solo = tmp / "solo"
    (solo / ".agents/changes").mkdir(parents=True)
    subprocess.run([*git, "init", "-q", "-b", "main"], cwd=solo, check=True)
    return s, solo


def start(root, home):
    env = {**{k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}, "HOME": str(home), "USERPROFILE": str(home),
           "CHANTIER_ROOT": str(root), "CHANTIER_CLAUDE_PROJECTS": str(home / "nt"), "PYTHONUTF8": "1"}
    (home / "nt").mkdir(parents=True, exist_ok=True)
    p = subprocess.Popen(["uv", "run", "--no-sync", "--project", str(ROOT), "chantier", "board", "--host", "127.0.0.1", "--port", "0", "--clock", "2026-06-18T10:30:00Z"],
                         cwd=root, env=env, stdout=subprocess.PIPE, text=True, encoding="utf-8")
    t = time.monotonic() + 90
    while time.monotonic() < t:
        l = p.stdout.readline()
        m = re.match(r"board on (\S+) over", l)
        if m:
            return p, m[1]
    raise SystemExit("no address")


def stop(p):
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
    p.wait(30)


def go(page, url, v, pr, lang):
    b = url.split("#")[0]
    sep = "&" if "?" in b else "?"
    q = f"p={pr}&" if pr else ""
    page.goto(f"{b}{sep}{q}v={v}&lang={lang}")
    page.wait_for_selector("[data-key]", state="attached")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(500)


def vis(page, sel):
    return page.locator(sel).locator("visible=true").first


def run():
    tmp = Path(tempfile.mkdtemp(prefix="verif-"))
    report = {}
    try:
        s, solo = mk(tmp)
        for name, root, proj in (("surface", s, "*"), ("solo", solo, None)):
            p, url = start(root, tmp / ("h" + name))
            try:
                with sync_playwright() as pw:
                    br = pw.chromium.launch()
                    for size, vp in SIZES.items():
                        for lang in (("en", "fr") if name == "surface" else ("en",)):
                            ctx = br.new_context(viewport=vp, locale="en-US", timezone_id="UTC", color_scheme="light",
                                                 reduced_motion="reduce", is_mobile=size == "phone", has_touch=size == "phone")
                            ctx.clock.set_fixed_time("2026-06-18T10:30:00Z")
                            page = ctx.new_page()
                            go(page, url, "home", proj, lang)
                            key = f"{name}-{size}-{lang}"
                            m = {}
                            m["has_all_projects_text"] = page.get_by_text(re.compile("All projects|Tous les projets|overview ·")).count()
                            has_pick = page.locator('[data-menu="toggle"]').count() > 0
                            m["picker_present"] = has_pick
                            m["picker_btn"] = vis(page, '[data-menu="toggle"]').inner_text() if has_pick else None
                            m["scroll_w"] = page.evaluate("document.documentElement.scrollWidth")
                            m["sidebar_w"] = page.evaluate("(()=>{const e=document.querySelector('.ws');return e?e.getBoundingClientRect().width:null})()")
                            m["side_w"] = page.evaluate("(()=>{const e=document.querySelector('.side, aside, .sidebar, nav');return e?e.getBoundingClientRect().width:null})()")
                            m["first_col_w"] = page.evaluate("(()=>{const e=document.querySelector('.overview td.who');return e?e.getBoundingClientRect().width:null})()")
                            m["overview_titles"] = page.evaluate("[...document.querySelectorAll('.overview [title]')].map(e=>e.title)")
                            m["page_text"] = page.inner_text("body")[:1800]
                            page.screenshot(path=str(OUT / f"{TAG}-{key}-closed.png"), animations="disabled")
                            if has_pick:
                                vis(page, '[data-menu="toggle"]').click()
                                page.wait_for_timeout(400)
                                m["menu"] = page.locator(".menu").first.inner_text()
                                m["menu_titles"] = page.evaluate("[...document.querySelectorAll('.menu [title]')].map(e=>e.title)")
                                page.screenshot(path=str(OUT / f"{TAG}-{key}-menu.png"), animations="disabled")
                            report[key] = m
                            ctx.close()
                    br.close()
            finally:
                stop(p)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    (OUT / f"{TAG}-measures.json").write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    print("done", TAG)


run()
