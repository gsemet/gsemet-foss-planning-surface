# CR-477 verification

Head: 91c934f600c7ec7a0c69a5abfe2573d70c6b31c8

## Claims

1. Restack line, bases, carry, lease refusals (spec sections 1-4). Judged at 91c934f.
   Command (worktree): `uv run --no-sync python -m pytest tests/test_restack_line.py tests/test_place_base.py tests/test_carry_restack.py tests/test_lease_commands.py tests/test_leases.py tests/test_stack_hold.py tests/test_carry_ship.py tests/test_stack_base.py tests/test_access.py -q`
   Output: `178 passed in 125.40s`. PASS.
2. Line limits (every .py at most 400 lines). Command: `wc -l stacks.py orders_apply.py leases.py`.
   Output: 387, 345, 340. PASS.
3. Long gate. Log `work/gates/20261124-142711.log`, first line `gate CR-477 ... head 91c934f600c7ec7a0c69a5abfe2573d70c6b31c8`, last line `result: pass at 91c934f600c7ec7a0c69a5abfe2573d70c6b31c8`. PASS.
4. PR description as posted (`gh pr view 455 --json body,headRefOid`, head 91c934f600c7ec7a0c69a5abfe2573d70c6b31c8), judged again at 91c934f. PASS:
   - Changes lists every file of `git diff --stat origin/main...HEAD` (17 files), including `scenario/run_scenario.py`, `test_leases.py`, `test_stack_hold.py`; Summary and Deliverables match the diff.
   - Known gaps holds the one open question; Test plan boxes filled with 91c934f (local gates at f20227a for check and eval-dry-run, scenario gate at 91c934f, matching claim 3).
   - Review box: log note `r3 approved at f20227a..., committed as 91c934f6` (`chantier log 477`) proves it.
   - Renders (sections, fold, code fence), no images, no role-name failure (product terms of a stack change).

## Verdict

VERIFIED at 91c934f600c7ec7a0c69a5abfe2573d70c6b31c8.
