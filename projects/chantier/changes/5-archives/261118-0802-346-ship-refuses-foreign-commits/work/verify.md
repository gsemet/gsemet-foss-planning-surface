Head: 76a19a47de1683b947e775a712d94ac70e9a40bf

Verdict: VERIFIED

1. New parametrized test, four cases (carried from 76a19a4: same head, no code move)
   Command: uv run --no-sync python -m pytest skills/chantier/scripts/cli/tests/test_carry_ship.py -q
   Output: `8 passed in 15.14s`. Out-of-draft case asserts EXIT_PRECONDITION, no new ship event; the other three assert exit 0 and recorded.

2. Card edits and refusal text (carried from 76a19a4: same head)
   Command: grep -n "merge <cr> <link>" foreman.md chief-of-staff.md; sed on driver.md 326-340 and chief-of-staff.md 1070-1092.
   Output: foreman.md 324, 328, 406 hold `merge <cr> <link>`; chief-of-staff.md 1074 names the one PR; driver.md 330-337 holds the draft-first paragraph; delivery.py:186 says "First put the PR back to draft and ship again".

3. PR description, as posted (gh pr view 312 -R gsemet/chantier, head 76a19a47de1683b947e775a712d94ac70e9a40bf, SHA 76a19a4)
   Command: gh pr view 312 -R gsemet/chantier --json body,headRefOid; git diff --stat origin/main...HEAD
   Output: headRefOid 76a19a47...; diff touches scenario/run_scenario.py, chief-of-staff.md, driver.md, foreman.md, delivery.py, test_carry_ship.py. Changes now lists all six (scenario/run_scenario.py included); Test plan names `76a19a4` for gates, review, verify and CI; Review box `approved at 76a19a4` matches log note "r2 approved at 4bde985, committed as 76a19a4" (read with `chantier log 346`); renders (sections, fold, no images); Known gaps "None" with no UNVERIFIED claim or failed accepted claim; no role name in the description outside Internal references. VERIFIED.
