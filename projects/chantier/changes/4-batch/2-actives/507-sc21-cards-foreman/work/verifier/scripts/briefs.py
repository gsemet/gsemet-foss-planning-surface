import os
import re
import subprocess
from pathlib import Path

W = "<worktree>"
P = "<planning>"
SURFACE = "<surface>"
CARDS = W + "/skills/chantier/cards-next"
INBOX = P + "/changes/1-inbox/driver-context-second-cut"
CRF = P + "/changes/4-batch/2-actives/507-sc21-cards-foreman"

ROLES = ["cr-driver", "release-driver", "stack-driver", "qa-driver", "coder", "conflict-resolver",
         "debugger", "inspector", "investigator", "verifier", "spec-writer", "spec-critic",
         "board-griller", "retro-critic", "demo-explorer", "chief-of-staff", "griller", "foreman"]
WORKERS = {"coder", "conflict-resolver", "debugger", "inspector", "investigator", "verifier"}
SPEC = {"spec-writer", "spec-critic", "board-griller"}


def run(args, env_host=None, batch=True):
    env = dict(os.environ)
    env.pop("CHANTIER_BATCH", None)
    if env_host:
        env["CHANTIER_HOST"] = env_host
    cmd = ["uv", "run", "--no-sync", "--project", W, "chantier", "--project", P, "brief", *args]
    if batch:
        cmd += ["--batch", "batch-31"]
    d = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    out = (d.stdout or "").strip()
    err = (d.stderr or "").strip()
    m = re.search(r"^Read (.+) whole, first\.$", out, re.M)
    if d.returncode == 0 and m:
        path = Path(m[1])
        data = path.read_bytes()
        host = re.search(rb"=== host rows: (\w+)", data)
        return 0, len(data), host[1].decode() if host else "?", data.decode()
    return d.returncode, None, None, (err or out)


def clean(t):
    return t.replace(SURFACE, "<surface>").replace(W, "<worktree>")[:220]


print("== all 18 roles, units per the specification (batch-31, host from the record)")
for role in ROLES:
    if role in WORKERS:
        unit = ["CR-507"]
    elif role in SPEC:
        unit = [INBOX]
    elif role == "qa-driver":
        unit = ["O-1", "--lease", "1"]
    elif role == "stack-driver":
        unit = ["stack", "--lease", "1"]
    elif role.endswith("driver"):
        unit = []
    else:
        unit = []
    if role == "foreman":
        unit = []
    for label, extra in (("old", []), ("new", ["--cards", CARDS])):
        code, size, host, text = run([role, *unit, *extra])
        print(f"{role:18} {label} unit={'-' if not unit else Path(unit[0]).name:26} exit={code} bytes={size} host={host}"
              + ("" if code == 0 else " :: " + clean(text)))

print("\n== Drivers with --cards, no unit and with CR unit")
for role, unit in (("cr-driver", []), ("release-driver", []), ("stack-driver", []), ("qa-driver", []),
                   ("cr-driver", ["CR-507", "--lease", "1"])):
    code, size, host, text = run([role, *unit, "--cards", CARDS])
    print(role, unit, "exit", code, size, "" if code == 0 else clean(text))

print("\n== spec roles on a CR folder of the running batch")
for role in sorted(SPEC):
    for label, extra in (("old", []), ("new", ["--cards", CARDS])):
        code, size, host, text = run([role, CRF, *extra])
        print(role, label, "exit", code, size, "" if code == 0 else clean(text))

print("\n== direct-mode read: foreman --epoch 1")
for label, extra in (("old", []), ("new", ["--cards", CARDS])):
    code, size, host, text = run(["foreman", "--epoch", "1", *extra])
    print("foreman --epoch 1", label, "exit", code, size, host,
          "epoch line:", re.findall(r"^epoch: .*$", text, re.M) if code == 0 else clean(text))

print("\n== host copilot (CHANTIER_HOST=copilot, no batch named)")
for role in ["foreman", "chief-of-staff", "griller"]:
    for label, extra in (("old", []), ("new", ["--cards", CARDS])):
        code, size, host, text = run([role, *extra], env_host="copilot", batch=False)
        print(role, label, "exit", code, size, host, "" if code == 0 else clean(text))

print("\n== staged copy: today's driver.md name filled from the new role card (Driver briefs, role only)")
import shutil  # noqa: E402

for role in ["cr-driver", "release-driver", "stack-driver", "qa-driver"]:
    stage = Path(__file__).parent / ("stage-" + role)
    stage.mkdir(exist_ok=True)
    shutil.copyfile(f"{CARDS}/{role}.md", stage / "driver.md")
    shutil.copyfile(f"{CARDS}/floor.md", stage / "floor.md")
    code, size, host, text = run([role, "--cards", stage.as_posix()])
    old = run([role])
    print(role, "old", old[0], old[1], "staged new", code, size, host, "" if code == 0 else clean(text))
