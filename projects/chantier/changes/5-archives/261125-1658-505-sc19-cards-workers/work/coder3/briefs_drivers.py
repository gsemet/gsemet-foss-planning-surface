import os, subprocess, sys
from pathlib import Path
WT = r"C:\Users\gaeta\Projets\chantier.worktrees\batch-31-CR-505"
PLAN = "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier"
S = Path(r"C:\Users\gaeta\AppData\Local\Temp\claude\f81ba1603abd10b3\c095a20c-9c0e-47ff-9690-11acf58be0b6\scratchpad\stage")
for role in ("cr-driver", "stack-driver", "release-driver", "qa-driver"):
    res = {}
    for label, extra in (("old", []), ("new", ["--cards", str(S / role)])):
        cmd = ["uv", "run", "--locked", "--project", WT, "chantier", "--project", PLAN, "brief", role, "--batch", "batch-31"] + extra
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=WT, env=dict(os.environ, CHANTIER_HOST="claude"))
        if p.returncode != 0:
            res[label] = "exit %d: %s" % (p.returncode, (p.stderr or p.stdout).strip()[:200]); continue
        path = [l[5:].rsplit(" whole", 1)[0] for l in p.stdout.splitlines() if l.startswith("Read ")][-1]
        res[label] = len(Path(path).read_bytes().replace(b"\r\n", b"\n"))
    print(role, res, flush=True)
