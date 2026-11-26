"""Record the fourth Verifier pass in verify.md (one argument: the path of verify.md)."""

import sys
from pathlib import Path

path = Path(sys.argv[1])
text = path.read_bytes().decode("utf-8")


def replace(old: str, new: str) -> None:
    global text
    assert text.count(old) == 1, (text.count(old), old)
    text = text.replace(old, new)


start = text.index("## Verdict: NOT VERIFIED\n")
end = text.index("## Failed claim\n")
fourth = """## Verdict: VERIFIED

Fourth pass at the same head (no code change). It judges the one change of the posted description since
the third pass and carries every other claim at `5a8a593`. The one failed claim (H3) is resolved.

State, run again: `git rev-parse HEAD` prints `5a8a59398692a0d497ad88c18e5f142de1411638`;
`git status --porcelain --branch` the branch line only. `gh pr view 532 --json
state,isDraft,headRefOid,baseRefName,updatedAt,title`: `OPEN`, draft `true`, base `main`, head
`5a8a593`, `updatedAt 2026-11-26T09:17:30Z`, title `ci: accept trust and security use case paths in a
real VS Code`. `gh pr checks 532`: `checks`, `report`, `static`, `static-windows`, `viewer-graph`,
`visual` `pass`, the other jobs `skipping`. `gh run list --commit <H>`: `45774743144 workflow_dispatch
success attempt 3`, `45773633868 pull_request success attempt 1`, no newer run.

### P1. The only change of the description is the removal of the H3 bullet - VERIFIED

SHA `<H>`. `gh pr view 532 --json body --jq .body > verifier/posted-body-4.md`, then `git diff
--no-index -U0 verifier/posted-body-3.md verifier/posted-body-4.md`: one hunk, `@@ -194 +193,0 @@`,
`-- The delivery may stop after any complete group; the coverage-mode switch lands last.`, no added
line. So sections, fold, tables, links and every other sentence are those the earlier passes judged.
`git diff --no-index -U0 pr-body.md verifier/posted-body-4.md` (the working body): one added empty
last line, nothing else.

### P2. Human decisions as posted, four bullets - VERIFIED

SHA `<H>`. Each is recorded as a decision of the user, and none of an agent's rules remains:
- "one nominal acceptance test; a human step is a simulated input": `<504>/02-answers.md` line 9 (Q3,
  `one nominal path per test`) and line 15 (Q6, `the human act is a simulated input`).
- "Coverage counts test markers; the proof ... is its CI job": line 68 (Q35, `marker-based ... the proof
  a test passes is its bench's CI job`).
- "The three paths not accepted get another kind of test ... the strict marker rule stays":
  `02-answers.md` item 6 and `1-inbox/strs-acceptance-remaining-groups/02-answers.md` line 3 (`the
  owner`).
- "delivered later, as follow-up changes, the switch last": item 7 (`the follow-ups ... the switch last
  ... go to the batch after batch-09`) and the inbox item's line 4 (`the owner, batch09-Q1`).
The "switch last" half of the removed bullet stays in the fourth bullet; stopping at one group stays in
the first "Autonomous decisions" bullet. "Autonomous decisions" is unchanged (P1; T1 to T3).

### P3. The posted description is clean and consistent with the pushed head - VERIFIED

SHA `<H>`. Changed part: P1, P2. Rest: carried (S1 to S7, T1 to T3, V1 to V15), the head and the CI runs
being unchanged. The unchecked "Verified at `5a8a593`: pending" box is left on purpose, not a failure.

"""
text = text[:start] + fourth + text[end:]

replace("## Failed claim\n", "## Claim failed by the third pass (resolved, see P1 and P2)\n")
replace(
    "it land last.` - NOT VERIFIED (first half)\n"
    if "it land last.` - NOT VERIFIED (first half)\n" in text
    else '### H3. Human decisions: "The delivery may stop after any complete group; the coverage-mode '
    'switch lands last." - NOT VERIFIED (first half)\n',
    '### H3. Human decisions: "The delivery may stop after any complete group; the coverage-mode '
    'switch lands last." - was NOT VERIFIED (first half); bullet since removed\n',
)
replace(
    "### S8. Human decisions, the five other bullets - VERIFIED but one line (H3)\n",
    "### S8. Human decisions, the five other bullets - VERIFIED but one line (H3, since removed: P1)\n",
)
replace(
    "verdict, then a description pass). Not a failure. This pass ends NOT VERIFIED, so it stays unchecked.\n",
    "verdict, then a description pass). Not a failure.\n",
)
replace(
    "F6 and F7\n(Human decisions, posted body) fail now only on H3.\n",
    "F6 and F7\n(Human decisions, posted body) failed in the third pass only on H3 and hold now (P1 to P3).\n",
)
replace(
    "## Notes on the third pass\n",
    """## Notes on the fourth pass

- No CI run started or re-run, no tracked file changed, no commit, push or pull request edit.
- Files written, all under `work/`: `verify.md`, `verifier/posted-body-4.md`,
  `verifier/update_verify4.py`.

## Notes on the third pass
""",
)

path.write_bytes(text.encode("utf-8"))
print("updated")
