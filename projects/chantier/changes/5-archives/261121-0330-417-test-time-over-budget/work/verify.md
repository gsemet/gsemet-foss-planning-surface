# Verify CR-417

Head: d60b8b194d3e66e4dab67133c3599889646a8ec8

Verdict: NOT VERIFIED

All claims judged at d60b8b19 unless stated.

1. Id inventory (d60b8b19 and main 4ed0d56c). Commands: `uv run --locked --group dev pytest --collect-only -q | grep '::' | sort`
   in the CR worktree and in the detached main worktree, each diffed against `evidence/ids-before.txt` (the `::` lines).
   Output: 1419 ids at head, 1419 at main, `diff` prints nothing (SAME) for main vs head and before.txt vs head.
   (`evidence/ids-before.txt` also holds 7 lines of uv noise; the ids are the 1419 `::` lines.) PASS.
2. No assertion lost. `git diff origin/main...HEAD -- skills/chantier/scripts/cli/tests/ | grep -E '^[-+]' | grep assert`:
   every removed assert is moved into a builder (`stack_of.build` asserts `take` code 0; the template builders
   in `access_batch` / `shared_state`), or kept (test_leases lease line kept via `TAKEN[0][0]`). No skip, marker, `-k` or `-m`
   added. test_ff_main fixtures build the same repositories once and rewrite the clone urls. PASS.
3. `just test` measures (`evidence/measures.txt`) equal the PR body: main 77.6/93.5/73.1 s, head 63.0/106.8/80.1 s,
   1405 passed 14 skipped; none idle, marked loaded. Ceiling 48.5 s not met: knowingly, and the Known gaps bullet says so
   with the three figures, test count and profile sums. PASS (as a disclosure).
4. Budgets: `git diff` of `scenario/run_scenario.py` changes only the nine literals; arithmetic from the result files
   (`scenario/results/scenario-20261121-005835-17772.md`, `...-011138-32980.md`): slower*1.25 rounded up to 5 =
   parallel 349.25->350, stack 747.6->750, release 580.5->585, gates 608->610, series-deps 376.5->380, direct 218.6->220,
   surface-board 659.9->660, qa-driver 250.1->255, gitlab 114.75->115. README table equals UNITS (nine budgets) and both
   runs' times (279.4/274.4, 598.1/531.7, 464.4/396.6, 486.4/426.8, 284.6/301.2, 174.9/171.6, 527.9/490.6, 182.9/200.1,
   72.5/91.8; walls 781.0/754.1; sums 3071.1/2884.8). PASS.
5. Diff scope: 15 files, all under `skills/chantier/scripts/cli/tests/`, `scenario/`, and `justfile` (`--dist worksteal`
   in the `test` recipe, an allowed xdist setting). Nothing under `src/`. PASS.
6. FAIL, Evidence 5: both scenario runs ran with the OLD literals (result files show "over budget" against 260/640/420/...).
   The spec asks the second run to be made or repeated with the new literals, no unit warning, all checks passing. No run
   with the new literals exists, and run B had one failed check (surface-board 284/285; solo rerun 285/285 in 424.0 s). The
   flake is in Known gaps; the absence of a run with the new literals (budgets unproven against a run) is not.
7. PR body (as posted, matches `work/pr-body.md`): renders, matches the diff. Known gaps lacks the item of claim 6.
   CI at d60b8b19: `just check (ubuntu-latest)` and `eval-dry-run` green; macos, windows and `just scenario (ubuntu-latest)`
   not yet concluded when read (not judged here).

## Re-verification at d60b8b194d3e66e4dab67133c3599889646a8ec8 (same head, PR body edited)

Head: d60b8b194d3e66e4dab67133c3599889646a8ec8

Command: `gh pr view 393 --json body,statusCheckRollup` at d60b8b19. Output: Known gaps now holds the bullet "No local run was made
with the new budgets: both measuring runs ran with the old literals ...", and the flake bullet; all five checks SUCCESS
(check ubuntu/macos/windows, scenario ubuntu, eval-dry-run). Claim 6 is now disclosed; claims 1-5 carried from the first
judgment at the same SHA (code unchanged). Claim 7 passes.

Verdict: VERIFIED
