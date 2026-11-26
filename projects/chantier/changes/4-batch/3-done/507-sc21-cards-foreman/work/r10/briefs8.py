"""Round 8 (round 7's script, the coder added): `brief` bytes of the roles whose role card changed, with cards-next and today's cards.

Each role runs with `--cards` and at once without it, so the brief file in the surface's git folder
ends with today's cards. `brief` records nothing. `hash` prints every brief file's hash, to compare
before and after.
"""

import hashlib
import re
import subprocess
import sys
from pathlib import Path

WT = "C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507"
SURFACE = Path("C:/Users/gaeta/Projets/gsemet-foss-planning-surface")
PLAN = f"{SURFACE.as_posix()}/projects/chantier"
CARDS = f"{WT}/skills/chantier/cards-next"
BRIEFS = SURFACE / ".git/chantier/briefs"
HERE = Path(__file__).parent


def hashes() -> dict[str, str]:
    return {
        p.relative_to(BRIEFS).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()[:12]
        for p in sorted(BRIEFS.rglob("*"))
        if p.is_file()
    }


def run(args: list[str]) -> str:
    cmd = ["uv", "run", "--no-sync", "--project", WT, "chantier", "--project", PLAN, "brief", *args,
           "--batch", "batch-31"]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=WT)
    found = re.search(r"^Read (.+) whole, first\.$", p.stdout, re.M)
    if p.returncode or not found:
        return f"exit {p.returncode}: {' '.join((p.stderr or p.stdout).split())[:200]}"
    data = Path(found[1]).read_bytes()
    host = re.search(rb"=== host rows: (\w+)", data)
    return f"exit 0 bytes {len(data.replace(b'\r\n', b'\n'))} host {host[1].decode() if host else '?'}"


if sys.argv[1] == "hash":
    for name, digest in hashes().items():
        print(digest, name)
else:
    for args in (["foreman"], ["chief-of-staff"], ["griller"], ["foreman", "--epoch", "1"], ["coder", "CR-507"]):
        print(" ".join(args), "| new", run([*args, "--cards", CARDS]), flush=True)
        print(" ".join(args), "| old", run(args), flush=True)
