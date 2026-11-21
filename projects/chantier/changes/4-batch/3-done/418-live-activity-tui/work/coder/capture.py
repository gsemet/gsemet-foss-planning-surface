"""Prepare a scratch project in a fresh temporary folder with a running batch (one CR taken, its
lease live), start the worktree's `chantier board` over it, capture `chantier live --once` on both
transports, stop the board by its handle and remove the scratch project.

usage: python capture.py <worktree> <out file>"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

WORKTREE = sys.argv[1]
OUT = Path(sys.argv[2])
CLI = ["uv", "run", "--no-sync", "--project", WORKTREE, "chantier"]
ROOT = Path(tempfile.mkdtemp(prefix="live-demo-"))
DEMO = ROOT / "demo"

env = {k: v for k, v in os.environ.items() if not k.startswith(("CHANTIER_", "CLAUDE_CODE_"))}
env.pop("COPILOT_CLI", None)
env.update(CHANTIER_HOST="claude", CLAUDE_CODE_ENTRYPOINT="claude-desktop", NO_PROXY="127.0.0.1")
env["HOME"] = env["USERPROFILE"] = str(ROOT)
env["COLUMNS"] = "120"


def sh(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    r = subprocess.run(args, cwd=DEMO, env=env, capture_output=True, text=True, encoding="utf-8")
    if check and r.returncode:
        raise SystemExit(f"{args}: {r.returncode}\n{r.stdout}\n{r.stderr}")
    return r


try:
    DEMO.mkdir(parents=True)
    sh("git", "init", "--quiet", "-b", "main", str(DEMO))
    (DEMO / "README.md").write_text("demo\n")
    (DEMO / "AGENTS.md").write_text("# Project instructions\n\nRun `just check`.\n")
    sh("git", "add", ".")
    sh("git", "-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-qm", "init")
    sh("git", "remote", "add", "origin", "git@gitlab.example.com:acme/demo.git")
    folders = []
    for title in ("Export the report as CSV", "Retry a failed upload"):
        out = sh(*CLI, "file", title).stdout.splitlines()
        folder = DEMO / out[0].removeprefix("filed ").split(";")[0]
        (folder / "03-change-spec.md").write_text(f"# {title}\n\nDo it.\n", encoding="utf-8")
        folders.append(str(folder))
    sh(*CLI, "open", *folders, "--default-branch", "main")
    record = json.loads((DEMO / ".agents/changes/4-batch/batch.json").read_text("utf-8"))
    env["CHANTIER_BATCH"] = record["id"]
    sh(*CLI, "foreman", "set", "local_foreman_t", "--epoch", "1")
    print(sh(*CLI, "take", record["crs"][0]["id"], "--epoch", "1").stdout.strip())
    del env["CHANTIER_BATCH"]

    board = subprocess.Popen(
        [*CLI, "board", "--host", "127.0.0.1", "--port", "0", "--ui", "none"],
        cwd=DEMO,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        server = DEMO / ".git" / "chantier" / "server.json"
        deadline = time.monotonic() + 60
        while not (server.exists() and '"port"' in server.read_text("utf-8")):
            if time.monotonic() > deadline:
                raise SystemExit("the board did not start within 60 s")
            try:
                board.wait(0.2)
                raise SystemExit(f"the board ended: {board.returncode}")
            except subprocess.TimeoutExpired:
                pass
        for transport in ("ws", "http"):
            r = sh(*CLI, "live", "--once", "--transport", transport, check=False)
            print(f"== {transport}: exit {r.returncode} {r.stderr.strip()}")
            name = OUT if transport == "ws" else OUT.with_name(OUT.stem + "-http.txt")
            name.write_text(r.stdout.replace(str(ROOT).replace("\\", "/"), "/tmp/live-demo"), "utf-8")
    finally:
        board.terminate()
        board.wait(30)
        print("board stopped:", board.returncode)
finally:
    shutil.rmtree(ROOT, ignore_errors=True)
    print("scratch removed:", not ROOT.exists())
