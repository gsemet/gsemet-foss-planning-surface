"""Proof 4: `brief` for every role of roles.yaml, from cards-next and from today's cards.

Bytes are the LF bytes of the brief file each run writes. `brief` records nothing. A refused run
keeps its exact text. Two extra sets, apart from the specified runs: a staging folder for the four
Drivers (roles.yaml names `driver.md`, which cards-next does not hold), as CR-505's evidence did,
and an inbox item for the three folder roles.
"""

import json
import shutil
import subprocess
from pathlib import Path

from chantier.roles_data import load_roles

WT = Path("C:/Users/gaeta/Projets/chantier.worktrees/batch-31-CR-507")
MAIN = "C:/Users/gaeta/Projets/chantier"
PLAN = "C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/chantier"
CRF = PLAN + "/changes/4-batch/2-actives/507-sc21-cards-foreman"
INBOX = PLAN + "/changes/1-inbox/simplify-cards-and-prompts"
CARDS = WT / "skills/chantier/cards-next"
HERE = Path(__file__).parent
STAGE = HERE / "staging"


def lf(path: Path) -> int:
    return len(path.read_bytes().replace(b"\r\n", b"\n"))


def run(role: str, unit: str | None, extra: list[str], cards: Path | None, project=str(WT)):
    cmd = ["uv", "run", "--no-sync", "--project", project, "chantier", "--project", PLAN, "brief", role]
    cmd += ([unit] if unit else []) + extra + ["--batch", "batch-31"]
    if cards is not None:
        cmd += ["--cards", cards.as_posix()]
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", cwd=str(WT))
    out = {"exit": p.returncode, "args": " ".join(cmd[7:])}
    if p.returncode:
        out["text"] = " ".join((p.stderr or p.stdout).split())[:400]
        return out
    for line in p.stdout.splitlines():
        if line.startswith("Read "):
            path = Path(line[5:].rsplit(" whole", 1)[0])
            out["file"], out["bytes"] = path.as_posix(), lf(path)
    return out


roles = [r.name for r in load_roles(WT / "skills/chantier/roles.yaml")]
SPEC = {
    "cr-driver": ("CR-507", ["--lease", "2"]),
    "release-driver": ("CR-507", ["--lease", "2"]),
    "stack-driver": ("stack", ["--lease", "11"]),
    "qa-driver": ("O-1", ["--lease", "1"]),
    **{r: ("CR-507", []) for r in ("coder", "conflict-resolver", "debugger", "inspector", "investigator", "verifier")},
    **{r: (CRF, []) for r in ("spec-writer", "spec-critic", "board-griller")},
    **{r: (None, []) for r in ("retro-critic", "demo-explorer", "chief-of-staff", "griller", "foreman")},
}
result = {"roles": roles, "spec": {}, "drivers_staged": {}, "inbox": {}}
assert sorted(roles) == sorted(SPEC), sorted(set(roles) ^ set(SPEC))
for role in roles:
    unit, extra = SPEC[role]
    new = run(role, unit, extra, CARDS)
    old = run(role, unit, extra, None)
    result["spec"][role] = {"new": new, "old": old}
    print(role, "new", new.get("bytes", new.get("text")), "| old", old.get("bytes", old.get("text")), flush=True)

for role in ("cr-driver", "release-driver", "stack-driver", "qa-driver"):
    folder = STAGE / role
    folder.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CARDS / f"{role}.md", folder / "driver.md")
    shutil.copyfile(CARDS / "floor.md", folder / "floor.md")
    runs = {"role-only": {"new": run(role, None, [], folder), "old": run(role, None, [], None)}}
    if role == "cr-driver":
        runs["CR-507"] = {"new": run(role, "CR-507", ["--lease", "2"], folder),
                          "old": run(role, "CR-507", ["--lease", "2"], None)}
    result["drivers_staged"][role] = runs
    for name, r in runs.items():
        print("staged", role, name, r["new"].get("bytes", r["new"].get("text")), "| old",
              r["old"].get("bytes", r["old"].get("text")), flush=True)

for role in ("spec-writer", "spec-critic", "board-griller"):
    new, old = run(role, INBOX, [], CARDS), run(role, INBOX, [], None)
    result["inbox"][role] = {"new": new, "old": old}
    print("inbox", role, new.get("bytes", new.get("text")), "| old", old.get("bytes", old.get("text")), flush=True)

result["main_cli"] = run("coder", "CR-507", [], CARDS, project=MAIN)
print("main checkout CLI:", result["main_cli"])
(HERE / "briefs.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
