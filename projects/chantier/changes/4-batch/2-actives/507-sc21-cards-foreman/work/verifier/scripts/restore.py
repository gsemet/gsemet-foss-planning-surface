"""Re-run `brief` without --cards for every brief file my probes overwrote with the new cards."""

import subprocess

MAIN = "<worktree>"
P = "<planning>"
INBOX = P + "/changes/1-inbox/driver-context-second-cut"
CALLS = [[r, "CR-507"] for r in ("coder", "conflict-resolver", "debugger", "inspector", "investigator", "verifier")]
CALLS += [[r, INBOX] for r in ("spec-writer", "spec-critic", "board-griller")]
CALLS += [[r] for r in ("retro-critic", "demo-explorer", "chief-of-staff", "griller", "foreman")]
for call in CALLS:
    cmd = ["uv", "run", "--no-sync", "--project", MAIN, "chantier", "--project", P, "brief", *call,
           "--batch", "batch-31"]
    d = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(call[0], "exit", d.returncode, "" if d.returncode == 0 else (d.stderr or d.stdout)[:200])
