import json, os, re, subprocess, sys, time, urllib.request, urllib.error, hashlib, difflib
from pathlib import Path

V = Path(sys.argv[1]); W = Path(sys.argv[2]); WT = Path(sys.argv[3])
code = V / "surface" / "projects" / "shop-api" / ".repo"; surf = V / "surface"; proj = surf / "projects" / "shop-api"
home = V / "home"; home.mkdir(exist_ok=True)
env = {**{k: v for k, v in os.environ.items() if k != "VIRTUAL_ENV"}, "HOME": str(home),
       "USERPROFILE": str(home), "PYTHONUTF8": "1", "CHANTIER_CLAUDE_PROJECTS": str(home / "nt")}
cmd = ["uv", "run", "--no-sync", "--project", str(WT), "chantier", "--project", "shop-api",
       "board", "--host", "127.0.0.1", "--port", "0"]
p = subprocess.Popen(cmd, cwd=surf, env=env, stdout=subprocess.PIPE, text=True, encoding="utf-8")
try:
    url = None
    t = time.monotonic()
    while time.monotonic() - t < 90:
        line = p.stdout.readline()
        if not line:
            break
        print("BOARD:", re.sub(r"(k(ey)?=)[^&\s]+", r"\1ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â¦", line.strip()))
        m = re.match(r"board on (\S+) over", line)
        if m:
            url = m[1]
            break
    base = re.match(r"(https?://[^/?#]+)", url)[1]
    sys.path.insert(0, str(WT / "skills/chantier/scripts/cli/src"))
    from chantier.board import key as keys
    kfs = list((code / ".git").rglob("board.json")) or list(surf.joinpath(".git").rglob("board.json"))
    print("keyfile", kfs)
    secret = json.loads(kfs[0].read_text())
    print("keyfile fields", list(secret))
    sec = secret.get("key") or secret.get("secret") or next(iter(secret.values()))

    def call(method, path, body=None):
        data = None if body is None else json.dumps(body).encode()
        rq = urllib.request.Request(base + path, data=data, method=method,
                                    headers={keys.HEADER: sec, "content-type": "application/json"})
        try:
            with urllib.request.urlopen(rq) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            raw = e.read(); print("HTTP", e.code, raw[:200]); return e.code, (json.loads(raw) if raw[:1] == b"{" else {})

    pid = "shop-api"
    st, view = call("GET", f"/api/projects/{pid}/config")
    print("GET", st)
    (W / "evidence-config-get.json").write_text(json.dumps(view, indent=2), encoding="utf-8", newline="\n")
    yf = proj / "chantier.yaml"
    before = yf.read_text(encoding="utf-8")
    ch = [{"host": "copilot", "role": "inspector", "key": "model", "value": "gpt-6.1-terra"}]
    st, put = call("PUT", f"/api/projects/{pid}/config", {"changes": ch, "base_sha256": view["sha256"], "dry_run": False})
    print("PUT", st, put.get("lines"), put.get("journal"))
    (W / "evidence-config-put.json").write_text(json.dumps(put, indent=2), encoding="utf-8", newline="\n")
    after = yf.read_text(encoding="utf-8")
    d = "".join(difflib.unified_diff(before.splitlines(True), after.splitlines(True), "a/chantier.yaml", "b/chantier.yaml"))
    (W / "evidence-config.diff").write_text(d, encoding="utf-8", newline="\n")
    print(d)
    print("sha match", put.get("sha256") == hashlib.sha256(after.encode()).hexdigest())
    h = put["sha256"]

    def tryc(name, changes, base):
        st, a = call("PUT", f"/api/projects/{pid}/config", {"changes": changes, "base_sha256": base, "dry_run": True})
        print(name, st, a.get("error") or a.get("lines"), "stale" in a)
        return a

    tryc("stale", ch, "0" * 64)
    tryc("default", [{"host": "copilot", "role": "coder", "key": "model", "value": "default"}], h)
    tryc("badkey", [{"host": "copilot", "role": "coder", "key": "skills", "value": "x"}], h)
    tryc("nullhost", [{"host": None, "role": "coder", "key": "model", "value": "x"}], h)
    a = tryc("copilot agent+model", [{"host": "copilot", "role": "coder", "key": "agent", "value": "mine"},
                                      {"host": "copilot", "role": "coder", "key": "model", "value": "gpt-6.1-terra"}], h)
    for r in a.get("view", {}).get("hosts", {}).get("copilot", {}).get("roles", []):
        if r["role"] == "coder":
            print("coder row", r["start"], r.get("refusal"), r["overridden_by"])
    for r in put["view"]["hosts"]["copilot"]["roles"]:
        if r["role"] in ("coder", "inspector"):
            print(r["role"], r["start"], r["overridden_by"], r["model"]["effective"], r["model"]["layers"])
    print("catalog", json.dumps(put["view"]["hosts"]["copilot"]["catalog"][:2])[:400])
    print("claude plans?", any("plans" in m for m in put["view"]["hosts"]["claude"]["catalog"]))
finally:
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
    p.wait(timeout=30)
    print("stopped", p.pid)
