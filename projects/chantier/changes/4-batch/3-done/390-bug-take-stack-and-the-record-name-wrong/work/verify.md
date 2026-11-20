# Verify CR-390

Head: d25289b9ff166acfd4d2fb16d4d6210757038364

## Claims

1. Unit tests pass at d25289b: `pytest tests/test_stack_base.py tests/test_stack_due.py -q` -> `32 passed in 13.77s`.
2. The new tests fail on the base (8abc1dc6, detached worktree, PYTHONPATH on its src): `9 failed, 5 passed` (cases A, B, B2, C, D, D2, off-place, taken-on-PR, take-vs-row). Head: all pass. (judged at d25289b)
3. Scenario stack unit at d25289b: `python scenario/run_scenario.py --unit stack` -> `stack | github | 177/177 | ... | ok`.
4. Departure (start_base uses stack_start when `not c.stacked or c.start_on`) matches the code and is justified by the scenario; accepted.
5. PR description, as posted (head d25289b): FAILS.
   - `gh pr view 358 --json body`: Autonomous decisions lists only the board `why` word; the start_base `start_on` departure (in work/pr-body.md) is missing from the posted body.
   - Changes omits the delivered `scenario/run_scenario.py` edit (stack unit expectations changed, 22 lines), which `git diff --stat` shows.
   - Test plan still holds `<sha7>` placeholders (draft; to fill at ready).

6. Description pass at d25289b (second start, no move): `gh pr view 358 --repo gsemet/chantier --json body` now lists the start_base departure under Autonomous decisions and the `scenario/run_scenario.py` edit under Changes; both match `git diff --stat origin/<CR-391 branch>..HEAD` (run_scenario.py, board/crs.py, stacks.py, test_stack_base.py) and the diff of `start_base` (`not c.stacked or c.start_on`). Test plan has no placeholders, Verified box unchecked, Known gaps None (no UNVERIFIED claim, no uncaptured evidence pair). Renders clean, no images. Review box `committed as f90ad7b0`: `chantier log CR-390` has `r2 approved at 5cb0f314, committed as f90ad7b0`. CI note at d25289b: all 5 jobs pass. Code and test claims 1-4 carried from this same head (no move).

## Verdict

VERIFIED (code, tests and description at d25289b9ff166acfd4d2fb16d4d6210757038364).

7. Description pass at d25289b9ff166acfd4d2fb16d4d6210757038364 (third start, no move): `gh pr view 358 --repo gsemet/chantier --json body` compared with work/pr-body.md by `diff` after stripping CRs: identical but one blank line. The only change since claim 6 is the Test plan box `Verified at d25289b` now ticked. Sections follow the template, Known gaps None, no images, no STALE mark, role names only in Internal references. Changes match the CR's own files (stacks.py, run_scenario.py, board/crs.py, test_stack_base.py); the other files in `git diff --stat origin/main...HEAD` (opening_record, preflight, git, repo, test_open_no_clone, test_cli_units) belong to the CRs below in the stack. Review box and CI claims carried from claim 6 (no move).

## Verdict

VERIFIED (description at d25289b9ff166acfd4d2fb16d4d6210757038364).

8. Description pass at d25289b9ff166acfd4d2fb16d4d6210757038364 (fourth start, no move): `gh pr view 358 --json body` vs work/pr-body.md, CRs stripped: identical but one blank line. Only change since claim 7: line 65 now `Review: approved, committed in d25289b (rebased onto CR-391)`. `chantier log CR-390`: `r2 approved at 5cb0f314, committed as f90ad7b0`, then the move note `before first push at d25289b9: ... rebased onto CR-391's branch, clean`; `git cat-file -t d25289b` = commit and it is HEAD. The box's SHA is the rebased head named by the move note of the approved round; the old f90ad7b0 is gone from the line. The last `ship` (00:56:40) records no off-note. Other claims carried from claim 7 (no move).

## Verdict

VERIFIED (description at d25289b9ff166acfd4d2fb16d4d6210757038364).
