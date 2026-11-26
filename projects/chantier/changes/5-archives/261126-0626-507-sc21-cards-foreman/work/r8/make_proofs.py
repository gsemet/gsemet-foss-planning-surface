"""Make work/r8/proofs.py from work/r7/proofs.py (round 8's text of a few sections) and
work/r8/briefs.json from work/r7/briefs.json with round 8's brief bytes. Then proofs.py rewrites
evidence/part3-proofs.md."""

import json
import re
from pathlib import Path

R8 = Path(__file__).parent
R7 = R8.parent / "r7"

data = json.loads((R7 / "briefs.json").read_text(encoding="utf-8"))
log = (R8 / "briefs8.log").read_text(encoding="utf-8")
for role, label in (("foreman", "foreman"), ("chief-of-staff", "chief-of-staff"), ("griller", "griller"),
                    ("coder", "coder CR-507")):
    new = int(re.search(rf"^{label} \| new exit 0 bytes (\d+)", log, re.M)[1])
    old = int(re.search(rf"^{label} \| old exit 0 bytes (\d+)", log, re.M)[1])
    if role != "coder":
        assert data["spec"][role]["old"]["bytes"] == old, (role, old)
    data["spec"][role]["new"]["bytes"] = new
    data["spec"][role]["old"]["bytes"] = old
(R8 / "briefs.json").write_text(json.dumps(data, indent=1), encoding="utf-8")

src = (R7 / "proofs.py").read_text(encoding="utf-8")


def swap(old: str, new: str, count: int = 1) -> None:
    global src
    assert src.count(old) == count, (old, src.count(old))
    src = src.replace(old, new)


def between(start: str, end: str, new: str) -> None:
    global src
    assert src.count(start) == 1, start
    a = src.index(start)
    b = src.index(end, a)
    src = src[:a] + new + src[b:]


swap('R7 = CR / "work/r7"', 'R7 = CR / "work/r7"\nR8 = CR / "work/r8"')
swap('(R7 / "just-check.log")', '(R8 / "just-check.log")')

# header
between('say("# PART 3 proofs (rounds 6 and 7)"', "# 2\n", '''say("# PART 3 proofs (rounds 6 to 8)", "",
    f"Worktree `{WT.as_posix()}`, head `{head}` plus the uncommitted changes of rounds 7 and 8 (under "
    "`cards-next/`: role cards, `review-step.md`, `sync-checkout.md`, the four `skills/*-SKILL.md`, "
    "`topics.json` and topic files, 7 of them new in round 8). "
    f"`{head}` holds the work of rounds 4 to 6, committed as `bb6a5639` and rebased (`git diff` between "
    f"the two is empty). Comparisons stay against `{BASE}`, the head before round 4. Byte counts are LF "
    "bytes (the checkout has `core.autocrlf=true`). Where the specification says `HEAD` the working "
    "tree is what is compared. Written by `work/r8/proofs.py`.", "")

''')
swap('"Written by `work/r7/proofs.py`.", f"Written by `work/r7/proofs.py`. {say_note}"',
     '"Written by `work/r8/proofs.py`.", f"Written by `work/r8/proofs.py`. {say_note}"')
swap('block("work/r7/proofs.py (proof 2)"', 'block("work/r8/proofs.py (proof 2)"')
swap('"the others because this round edits them). `references`', '"the others because this branch edits them). `references`')

# 4
swap('data = json.loads((R7 / "briefs.json")', 'data = json.loads((R8 / "briefs.json")')
between('say("## 4. `brief` for all 18 roles", "",', '    "Command, from the worktree', '''say("## 4. `brief` for all 18 roles", "",
    "The bytes of foreman, chief-of-staff and griller (new) and of coder (new and old) are round 8's "
    "(`work/r8/briefs8.py`, on the working tree); every other number is round 6's, those cards "
    "unchanged since. Coder's old brief is 9,116 bytes in round 8's run and was 9,790 in round 6's; "
    "the Verifier's run at `03f973e4` likewise gave the six workers lower absolute values (cause not "
    "traced). Start readings and the direct-mode total: `evidence/acceptance-records.md`.", "",
''')

# 5
between('say("", "Round 7 changed the cards', 'say("", "Quiz case change of round 4:',
        '''say("", "Rounds 7 and 8 changed the cards of the Chief of Staff, the Foreman, the Griller and the "
    "Coder, the review step, the four skill texts and topics: their quiz is owed at the committed head. "
    "Plans only: `evidence/acceptance-records.md`.")
''')

# 8
swap('stage = R7 / "dp-stage"', 'stage = R8 / "dp-stage"')
swap('"(`work/r7/dp-stage/`).", "")', '"(`work/r8/dp-stage/`).", "")')
swap('block("work/r7/proofs.py (proof 8)"', 'block("work/r8/proofs.py (proof 8)"')

# 10, 12
swap('''    "`evidence/boundaries-split.md`.", "",''', '''    "`evidence/boundaries-split.md`. Round 8 read each section's rows against the cited home and "
    "re-homed those the home did not hold (`work/r8/rehome.py`, `sync.py`, `citefix.py`, "
    "`quotefix.py`), and updated the sibling-card edits (`sibling.py`, `sibling2.py`) and two boundary "
    "rows (`bounds.py`).", "",''')
swap('say("## 12. Gates (round 7, on the working tree)", "",', 'say("## 12. Gates (round 8, on the working tree)", "",')
swap('new topics: run by `work/r7/proofs.py` (the sections above).",',
     'new topics: run by `work/r8/proofs.py` (the sections above).",')

# gaps
swap('''"bytes are rules whose home must be a card (kind a) and the pointer to `help session-shell`; "''',
     '''"bytes are rules whose home must be a card (kind a) and the pointer to `help session-shell` (round "
    "8 added the large-binaries never to `coder.md`, H-057); "''')
between('"- Rules with no full home in the new set', '"- Do not merge:',
        '''"- Rules with no full home in the new set (the inventories' gaps): FM-026, C-304, C-885 in part; "
    "FM-B006: `judge` does not carry the image note.",
    ''')

(R8 / "proofs.py").write_text(src, encoding="utf-8", newline="\n")
print("written")
