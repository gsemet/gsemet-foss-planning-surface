"""Verifier: `brief` bytes at the head, in-process, with `write_file` captured so that no file is
written in the surface's git folder. Bytes are the LF bytes of the text the run would write."""

import contextlib
import io
import json
import shutil
import sys
from pathlib import Path

from chantier import cli
from chantier.commands import brief as brief_mod
from chantier.roles_data import load_roles

WT = Path("<worktree>")
PLAN = "<planning>"
CRF = PLAN + "/changes/4-batch/2-actives/507-sc21-cards-foreman"
INBOX = PLAN + "/changes/1-inbox/simplify-cards-and-prompts"
CARDS = WT / "skills/chantier/cards-next"
HERE = Path(__file__).parent
STAGE = HERE / "dp"

captured: list = []


def capture(path, text, *a, **k):
    captured.append((Path(path), text))


brief_mod.write_file = capture


def run(role, unit=None, extra=(), cards=None):
    argv = ["--project", PLAN, "brief", role, *([unit] if unit else []), *extra, "--batch", "batch-31"]
    if cards is not None:
        argv += ["--cards", Path(cards).as_posix()]
    captured.clear()
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = cli.main(argv)
        except SystemExit as e:
            code = e.code
    if code or not captured:
        return {"exit": code, "text": " ".join((err.getvalue() or out.getvalue()).split())[:300]}
    path, text = captured[-1]
    data = text.replace("\r\n", "\n").encode("utf-8")
    return {"exit": code, "bytes": len(data), "name": path.name, "text_body": text}


def show(r):
    return r.get("bytes", r.get("text"))


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
assert sorted(roles) == sorted(SPEC), sorted(set(roles) ^ set(SPEC))
print("roles", len(roles))
keep = {}
ok_new = ok_both = 0
for role in roles:
    unit, extra = SPEC[role]
    new = run(role, unit, extra, CARDS)
    old = run(role, unit, extra, None)
    ok_new += "bytes" in new
    ok_both += "bytes" in new and "bytes" in old
    keep[role] = (new, old)
    print("spec", role, "| today", show(old), "| new", show(new))
print("new exit 0:", ok_new, "of", len(roles), "| both exit 0:", ok_both)

for role in ("cr-driver", "release-driver", "stack-driver", "qa-driver"):
    folder = STAGE / role
    folder.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(CARDS / f"{role}.md", folder / "driver.md")
    shutil.copyfile(CARDS / "floor.md", folder / "floor.md")
    new, old = run(role, None, [], folder), run(role, None, [], None)
    keep["staged " + role] = (new, old)
    print("staged", role, "| today", show(old), "| new", show(new))

for role in ("spec-writer", "spec-critic", "board-griller"):
    new, old = run(role, INBOX, [], CARDS), run(role, INBOX, [], None)
    keep["inbox " + role] = (new, old)
    print("inbox", role, "| today", show(old), "| new", show(new))

e_new = run("foreman", None, ["--epoch", "1"], CARDS)
e_old = run("foreman", None, ["--epoch", "1"], None)
keep["foreman epoch"] = (e_new, e_old)
print("foreman --epoch 1 | today", show(e_old), "| new", show(e_new))
c_new, c_old = keep["chief-of-staff"]
print("direct mode | today", c_old["bytes"] + e_old["bytes"], "| new", c_new["bytes"] + e_new["bytes"])

for key in ("chief-of-staff", "griller", "coder", "staged cr-driver", "inbox spec-writer"):
    new, old = keep[key]
    for side, r in (("new", new), ("old", old)):
        (HERE / f"brief-{key.replace(' ', '-')}-{side}.txt").write_text(r.get("text_body", ""), encoding="utf-8", newline="\n")
