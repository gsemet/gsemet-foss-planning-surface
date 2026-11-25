"""Make work/r9/proofs.py from work/r8/proofs.py (round 9's text of a few sections). Round 9
changed no role card, so the brief bytes stay work/r8/briefs.json's. Then proofs.py rewrites
evidence/part3-proofs.md."""

from pathlib import Path

R9 = Path(__file__).parent
src = (R9.parent / "r8/proofs.py").read_text(encoding="utf-8")


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


swap('R8 = CR / "work/r8"', 'R8 = CR / "work/r8"\nR9 = CR / "work/r9"')
swap('(R8 / "just-check.log")', '(R9 / "just-check.log")')

# header
between('say("# PART 3 proofs (rounds 6 to 8)"', "# 2\n", '''new_since_head = git("ls-files", "--others", "--exclude-standard")[1].split()
gone = git("ls-files", "--deleted")[1].split()
say("# PART 3 proofs (rounds 6 to 9)", "",
    f"Worktree `{WT.as_posix()}`, head `{head}` plus the uncommitted changes of rounds 7 to 9 (under "
    "`cards-next/`: role cards, `review-step.md`, `sync-checkout.md`, the four `skills/*-SKILL.md`, "
    f"`topics.json` and topic files; {len(new_since_head)} topic files are not in `{head}` and "
    f"{len(gone)} of its files are gone, each split into parts). "
    f"`{head}` holds the work of rounds 4 to 6, committed as `bb6a5639` and rebased (`git diff` between "
    f"the two is empty). Comparisons stay against `{BASE}`, the head before round 4. Byte counts are LF "
    "bytes (the checkout has `core.autocrlf=true`). Where the specification says `HEAD` the working "
    "tree is what is compared. Written by `work/r9/proofs.py`.", "")

''')
swap('"Written by `work/r8/proofs.py`.", f"Written by `work/r8/proofs.py`. {say_note}"',
     '"Written by `work/r9/proofs.py`.", f"Written by `work/r9/proofs.py`. {say_note}"')
swap('block("work/r8/proofs.py (proof 2)"', 'block("work/r9/proofs.py (proof 2)"')

# 4
swap('''(`work/r8/briefs8.py`, on the working tree); every other number is round 6's, those cards "
    "unchanged since.''', '''(`work/r8/briefs8.py`, on round 8's working tree; round 9 changed no role card); every "
    "other number is round 6's, those cards unchanged since.''')

# 5
swap('''say("", "Rounds 7 and 8 changed the cards of the Chief of Staff, the Foreman, the Griller and the "
    "Coder, the review step, the four skill texts and topics: their quiz is owed at the committed head. "''',
     '''say("", "Rounds 7 and 8 changed the cards of the Chief of Staff, the Foreman, the Griller and the "
    "Coder, the review step and the four skill texts, and rounds 7 to 9 changed topics: their quiz is "
    "owed at the committed head. "''')

# 8
swap('stage = R8 / "dp-stage"', 'stage = R9 / "dp-stage"')
swap('"(`work/r8/dp-stage/`).", "")', '"(`work/r9/dp-stage/`).", "")')
swap('block("work/r8/proofs.py (proof 8)"', 'block("work/r9/proofs.py (proof 8)"')

# 10, 12
swap('''"rows (`bounds.py`).", "",''', '''"rows (`bounds.py`). Round 9 re-homed further rows (`work/r9/rehome.py`) and redid the topic "
    "rows of the sibling-card edits (`siblings_rows.py`, checked by `siblings.py`).", "",''')
swap('say("## 12. Gates (round 8, on the working tree)", "",', 'say("## 12. Gates (round 9, on the working tree)", "",')
swap('new topics: run by `work/r8/proofs.py` (the sections above).",',
     'new topics: run by `work/r9/proofs.py` (the sections above).",')

(R9 / "proofs.py").write_text(src, encoding="utf-8", newline="\n")
print("written")
