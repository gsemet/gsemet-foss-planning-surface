# Verify CR-448

Head: b1eac8799c415d8322ca7c849488800ece4b0b66

## Move judged: rebase onto 906e5fd1 (head b1eac879, previous 20cac21f)

All claims below judged at b1eac8799c415d8322ca7c849488800ece4b0b66. Claims of the earlier list that this move does not touch (screenshots, scope of figures, Costs files unchanged) are carried from 20cac21: the CR's own patch is the same apart from the conflict file and the count line.

A. Dashboard behaviour at the new head. `uv run --no-sync --project . python -m pytest tests/test_board_dashboard.py tests/test_board_design.py tests/test_server_api_calls.py -q -p no:cacheprovider` (worktree, CLI folder tests): `66 passed in 9.33s`. The design test merged with main's (`test_a_batch_view_draws_the_batch_folder_chip_not_a_priority` from CR-436 and the dashboard registry/sheet-order test both present: `git diff 906e5fd1 HEAD -- .../test_board_design.py` shows only the +14 dashboard test added after main's).
B. Ops count consistent. `python -I -c "from chantier.board.api import ops; print(len(ops.HANDLERS))"` printed `21` (main's 20 plus `dashboard.get`); `scenario/run_scenario.py:1680` and `scenario/README.md:459` say "the 21 ops"; `docs/server-api.md:84` has the `dashboard.get` row.
C. Nothing of main lost. `git merge-base --is-ancestor 906e5fd1 HEAD` true; `git log --oneline origin/main..HEAD` lists only the two CR commits (1ed3fcef, b1eac879); `git diff 906e5fd1 HEAD --name-only` holds only dashboard/chart files, the op wiring (ops.py, protocol.py/json, server-api.md, scenario count, DESIGN.md, tokens, index.html, registry/router/store/api/i18n/icons) and two tests; no file of CR-433/CR-436 (batch-*.js, crs.py, times.py, launch.py, card.js, ...) differs from main.
D. CI at the head (`gh pr view 420`): head `b1eac879...`; `just check (ubuntu-latest)` SUCCESS, `just eval-dry-run` SUCCESS; macOS, Windows and `just scenario (ubuntu-latest)` still pending when read.
E. Gate pass: the log `work/gates/20261122-083233.log` opens with `gate CR-448 ... head b1eac8799c415d8322ca7c849488800ece4b0b66` but was still running (last line `waiting for the long gate of CR-439`) when read: no pass at this head yet. The CLI refuses hand-back until it passes; that is the Driver's.
F. PR description not re-judged (not asked); only the move was.

VERIFIED

(Earlier judgment at 20cac21f follows.)

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
