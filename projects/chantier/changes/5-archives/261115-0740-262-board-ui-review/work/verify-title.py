"""usage: verify-title.py CHECKOUT ROOTDIR PROJECT -- starts the board, prints backlog item titles from the state API."""
import json, os, re, subprocess, sys, time, urllib.request
from pathlib import Path
from urllib.parse import urlparse, parse_qs

checkout, rootdir, project = sys.argv[1:4]
home = Path(rootdir).parent / "home-title"; (home / "nt").mkdir(parents=True, exist_ok=True)
env = {**{k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}, "HOME": str(home), "USERPROFILE": str(home),
       "CHANTIER_ROOT": rootdir, "CHANTIER_CLAUDE_PROJECTS": str(home / "nt"), "PYTHONUTF8": "1"}
proc = subprocess.Popen(["uv", "run", "--locked", "--project", checkout, "chantier", "board", "--host", "127.0.0.1",
                         "--port", "0"], cwd=rootdir, env=env, stdout=subprocess.PIPE, text=True, encoding="utf-8")
try:
    url = None
    t0 = time.monotonic()
    while time.monotonic() - t0 < 120:
        line = proc.stdout.readline()
        m = re.match(r"board on (\S+) over", line or "")
        if m:
            url = m[1]
            break
    u = urlparse(url)
    key = parse_qs(u.query).get("k") or parse_qs(u.fragment)
    base = f"{u.scheme}://{u.netloc}"
    print("url", url)
    import http.cookiejar
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    op.open(url).read()
    st = json.load(op.open(f"{base}/api/projects/{project}/state"))
    for b, items in st["backlog"].items():
        for i in items:
            print(b, i["item"], "=>", i["title"])
finally:
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)


