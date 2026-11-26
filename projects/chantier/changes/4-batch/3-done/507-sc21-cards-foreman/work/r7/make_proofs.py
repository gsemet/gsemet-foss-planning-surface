"""Make work/r7/proofs.py from work/r6/proofs.py (the text of a few sections changes for round 7),
and work/r7/briefs.json from work/r6/briefs.json with round 7's new bytes of the three roles whose
card changed. Then proofs.py rewrites evidence/part3-proofs.md."""

import json
import re
import shutil
from pathlib import Path

R7 = Path(__file__).parent
R6 = R7.parent / "r6"

data = json.loads((R6 / "briefs.json").read_text(encoding="utf-8"))
log = (R7 / "briefs7.log").read_text(encoding="utf-8")
for role in ("foreman", "chief-of-staff", "griller"):
    new = int(re.search(rf"^{role} \| new exit 0 bytes (\d+)", log, re.M)[1])
    old = int(re.search(rf"^{role} \| old exit 0 bytes (\d+)", log, re.M)[1])
    assert data["spec"][role]["old"]["bytes"] == old, (role, old)
    data["spec"][role]["new"]["bytes"] = new
(R7 / "briefs.json").write_text(json.dumps(data, indent=1), encoding="utf-8")

src = (R6 / "proofs.py").read_text(encoding="utf-8")


def swap(old: str, new: str, count: int = 1) -> None:
    global src
    assert src.count(old) == count, (old, src.count(old))
    src = src.replace(old, new)


swap('R6 = CR / "work/r6"', 'R6 = CR / "work/r6"\nR7 = CR / "work/r7"')
swap('(R6 / "just-check.log")', '(R7 / "just-check.log")')
swap('assert head == BASE, head', 'assert head == "03f973e4", head')

# header
start = src.index('say("# PART 3 proofs (round 6)"')
end = src.index("# 2\n", start)
src = src[:start] + '''say("# PART 3 proofs (rounds 6 and 7)", "",
    f"Worktree `{WT.as_posix()}`, head `{head}` plus round 7's uncommitted card edits (`foreman.md`, "
    "`chief-of-staff.md`, `griller-skill.md`, `review-step.md`, the four `skills/*-SKILL.md`; no topic). "
    f"`{head}` holds the work of rounds 4 to 6, committed as `bb6a5639` and rebased (`git diff` between "
    f"the two is empty). Comparisons stay against `{BASE}`, the head before round 4. Byte counts are LF "
    "bytes (the checkout has `core.autocrlf=true`). Where the specification says `HEAD` the working "
    "tree is what is compared. Written by `work/r7/proofs.py`.", "")

''' + src[end:]
swap('"Written by `work/r6/proofs.py`.", f"Written by `work/r6/proofs.py`. {say_note}"',
     '"Written by `work/r7/proofs.py`.", f"Written by `work/r7/proofs.py`. {say_note}"')
swap('block("work/r6/proofs.py (proof 2)"', 'block("work/r7/proofs.py (proof 2)"')
swap('New topic files of this uncommitted work (not in `{BASE}`)', 'New topic files since the base (not in `{BASE}`)')

# 4
swap('data = json.loads((R6 / "briefs.json")', 'data = json.loads((R7 / "briefs.json")')
swap('say("## 4. `brief` for all 18 roles", "",',
     'say("## 4. `brief` for all 18 roles", "",\n'
     '    "The new bytes of foreman, chief-of-staff and griller are round 7\'s (`work/r7/briefs7.py`, "\n'
     '    "on the working tree); every other number is round 6\'s, those cards unchanged since. The "\n'
     '    "Verifier\'s run at `03f973e4` gave the six workers the same old-new differences with absolute "\n'
     '    "values 742 lower (cause not traced). Start readings and the direct-mode total: "\n'
     '    "`evidence/acceptance-records.md`.", "",')

# 5
swap('say("", "Quiz case change of round 4:',
     'say("", "Round 7 changed the cards of the Chief of Staff, the Foreman and the Griller (and the "\n'
     '    "review step and the four skill texts): their quiz is owed at the committed head. Plans only: "\n'
     '    "`evidence/acceptance-records.md`.")\n'
     'say("", "Quiz case change of round 4:')

# 8
swap('stage = R6 / "dp-stage"', 'stage = R7 / "dp-stage"')
swap('"(`work/r6/dp-stage/`).", "")', '"(`work/r7/dp-stage/`).", "")')
swap('block("work/r6/proofs.py (proof 8)"', 'block("work/r7/proofs.py (proof 8)"')

# 9 to 12
swap('''"shows nothing under any `tests/` folder). Base and head times were not measured separately.", "",''',
     '''"shows nothing under any `tests/` folder). `just test` seconds at the base and the head (the "
    "Verifier's run): `evidence/acceptance-records.md`.", "",''')
swap('"sibling-card table by hand.", "",',
     '"sibling-card table by hand. Round 7 changed the rows of all four inventories after reading "\n'
     '    "each protecting row\'s cited home (`work/r7/apply.py`, `work/r7/apply_host.py`) and added "\n'
     '    "`evidence/boundaries-split.md`.", "",')
swap('"## 11. Unloaded", "", "Run against the working tree with `--untracked`, since nothing is committed.", "")',
     '"## 11. Unloaded", "", "Run against the working tree, with `--untracked`.", "")')
swap('say("## 12. Gates (round 6, on the uncommitted working tree)", "",',
     'say("## 12. Gates (round 7, on the working tree)", "",')
swap('"which rich drops under `NO_COLOR`); not rerun in round 6. No file of `src/` or `tests/` is "',
     '"which rich drops under `NO_COLOR`); not rerun since. No file of `src/` or `tests/` is "')
swap('new topics: run by `work/r6/proofs.py` (the sections above).",',
     'new topics: run by `work/r7/proofs.py` (the sections above).",')

# gaps
swap('"- Real run not done (child 28). Quiz not run (item 5). Copilot untested.",',
     '"- Real run not done (child 28). Quiz not run (item 5). Copilot untested.",\n'
     '    "- Rules with no full home in the new set (the inventories\' gaps): H-057 (large binaries), "\n'
     '    "H-059 in part (the host\'s settings), FM-026, C-006, C-304, C-885; FM-B006: `judge` does not "\n'
     '    "carry the image note.",')

(R7 / "proofs.py").write_text(src, encoding="utf-8", newline="\n")
print("written")
