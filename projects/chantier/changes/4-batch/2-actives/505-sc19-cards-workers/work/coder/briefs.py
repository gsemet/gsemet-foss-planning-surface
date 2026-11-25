"""Brief bytes, old cards against cards-next, for the 11 roles of SC19 (LF bytes of the brief file)."""
import json
import os
import subprocess
import sys
from pathlib import Path

WT = r"C:\Users\gaeta\Projets\chantier.worktrees\batch-31-CR-505"
PLAN = "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier"
CRF = PLAN + "/changes/1-inbox/simplify-cards-and-prompts"
CARDS = WT + r"\skills\chantier\cards-next"
ROLES = [
    ("coder", "CR-505"), ("conflict-resolver", "CR-505"), ("debugger", "CR-505"),
    ("investigator", "CR-505"), ("verifier", "CR-505"), ("inspector", "CR-505"),
    ("spec-writer", CRF), ("spec-critic", CRF), ("board-griller", CRF),
    ("retro-critic", None), ("demo-explorer", None),
]
hosts = sys.argv[1:] or ["claude"]
out = []
for host in hosts:
    for role, unit in ROLES:
        sizes = {}
        for label, extra in (("old", []), ("new", ["--cards", CARDS])):
            cmd = ["uv", "run", "--locked", "--project", WT, "chantier", "--project", PLAN, "brief", role]
            if unit:
                cmd.append(unit)
            cmd += ["--batch", "batch-31"] + extra
            env = dict(os.environ, CHANTIER_HOST=host)
            p = subprocess.run(cmd, capture_output=True, text=True, cwd=WT, env=env)
            if p.returncode != 0:
                sizes[label] = f"exit {p.returncode}: {(p.stderr or p.stdout).strip()[:160]}"
                continue
            path = None
            for line in p.stdout.splitlines():
                if line.startswith("Read "):
                    path = line[5:].rsplit(" whole", 1)[0]
            sizes[label] = len(Path(path).read_bytes().replace(b"\r\n", b"\n"))
        out.append((host, role, sizes))
        print(host, role, sizes, flush=True)
json.dump(out, open(os.path.join(os.path.dirname(__file__), "briefs-" + "-".join(hosts) + ".json"), "w"))
