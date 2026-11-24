# CR-477 verification

Head: 91c934f600c7ec7a0c69a5abfe2573d70c6b31c8

## Claims

1. Restack line, bases, carry, lease refusals (spec sections 1-4). Judged at 91c934f.
   Command (worktree): `uv run --no-sync python -m pytest tests/test_restack_line.py tests/test_place_base.py tests/test_carry_restack.py tests/test_lease_commands.py tests/test_leases.py tests/test_stack_hold.py tests/test_carry_ship.py tests/test_stack_base.py tests/test_access.py -q`
   Output: `178 passed in 125.40s`. PASS.
2. Line limits (every .py at most 400 lines). Command: `wc -l stacks.py orders_apply.py leases.py`.
   Output: 387, 345, 340. PASS.
3. Long gate. Log `work/gates/20261124-142711.log`, first line `gate CR-477 ... head 91c934f600c7ec7a0c69a5abfe2573d70c6b31c8`, last line `result: pass at 91c934f600c7ec7a0c69a5abfe2573d70c6b31c8`. PASS.
4. PR description as posted (`gh pr view 455 --json body`, PR head 91c934f600c7ec7a0c69a5abfe2573d70c6b31c8). FAIL:
   - Known gaps says "the long gate is not yet run at this head" and that `just eval-dry-run` and the local `scenario` are pending; the gate log above shows a pass at this head, so the text contradicts the evidence.
   - Test plan: `Local gates at f20227a` is not the head (91c934f, which also changed `scenario/run_scenario.py`); `Review: approved at <sha7>`, `Verified at <sha7>` and `CI green at <sha7>` are unfilled placeholders.
   - Details/Changes does not list `scenario/run_scenario.py` (changed in the diff) or `test_leases.py` / `test_stack_hold.py` (updated expected texts).

## Verdict

NOT VERIFIED (the code claims hold; the PR description fails: stale Known gaps, wrong gate SHA, unfilled placeholders, delivered change unmentioned).
