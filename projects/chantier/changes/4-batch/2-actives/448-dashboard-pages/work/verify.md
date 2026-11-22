# Verify CR-448

Head: 20cac21f5bca4712529866f961dc0f9e5a501c05

All claims judged at 20cac21 unless said.

1. Figures, op, protocol, design checks (spec Evidence 1 to 4). Command, in the worktree's CLI folder:
   `uv run --no-sync python -m pytest tests/test_board_dashboard.py tests/test_server_api_calls.py tests/test_server_protocol.py tests/test_board_design.py tests/test_code_targets.py -q`
   Output: `73 passed in 6.19s`. The test file holds the batch-29 copy (fixture `dashboard_batch29.json`, CR-404/406/418 lead the ranking, total 9318 calls), the median 945 case, the `range: "15"` 400 case, and the registry/sheet-order test.
2. Gate pass: `work/gates/20261122-043534.log` first line `gate CR-448 ... head 20cac21f5bca4712529866f961dc0f9e5a501c05`, last line `result: pass at 20cac21f5bca4712529866f961dc0f9e5a501c05` (just scenario). `evaldry.log` ok (at 9808e1d; only `scenario/` changed since, per the PR).
3. Not-changed claim (Costs files, state.py, AGENTS.md): `git diff --name-only origin/main...HEAD | grep -i "costs\|receipt\|spend-by\|history\|state.py\|AGENTS"` printed nothing.
4. Scope: diff holds the three figure modules, the op (protocol.py, protocol.json, ops.py, docs/server-api.md row), registry/router/store/api/icons/i18n, chart component and sheets, DESIGN.md, tokens, tests: matches spec sections 1 to 6.
5. Screenshots (five, evidence folder), each opened: Dashboard sits between Costs and Configuration; Productivity EN (four tiles, coverage "n of 20 batches", live line for batch-30, held dashed/merged solid); Spending EN by role with a batch read in the readout; FR Spending by model (French words, model legend, outside line, "non reparti"); narrow 375 px one column with bottom nav. No username or home folder shown in any. Gaps are cut lines/empty slots, not zeros.
6. PR description (read with `gh pr view 420`, head 20cac21): renders (sections, fold, five images each captioned with 20cac21), Summary/Deliverables/Changes match the diff, Known gaps lists the UNVERIFIED claim and the accepted gaps, no role name outside Internal references.

Notes: the ranking and its PR links are below the fold of the screenshots and the PR names that as UNVERIFIED live (in Known gaps). Full suite at 20cac21, `python -m pytest tests -q -x`: `1654 passed, 20 skipped in 408.47s`.

Description pass (later, `gh pr view 420 --json body`, head 20cac21, CI checks all pass at that head): claim 6 is withdrawn. The Test plan holds four items and lacks the template's `Review: approved at <sha7>`, `Verified at <sha7>` and `CI green at <sha7>` items (pr-template, Test plan, audit 1). Minor: Changes does not mention the `scenario/` edits (`scenario/README.md`, `scenario/run_scenario.py`) that the diff holds. Sections, fold, SHAs (20cac21), captions, Known gaps and no role name outside Internal references are otherwise right.

NOT VERIFIED

Description pass 2 (`gh pr view 420 --repo gsemet/chantier --json body`, head 20cac21): the Test plan now holds Review, Verified and CI green items at 20cac21 (the Review note is the Driver's note citing the r3 approve at 20cac21, `chantier log 448`); Changes names `scenario/README.md` and `scenario/run_scenario.py`. Sections, fold, captions, Known gaps (UNVERIFIED bullet present) and no role name outside Internal references are right. Claim 6 holds again.

VERIFIED
20cac21f5bca4712529866f961dc0f9e5a501c05
