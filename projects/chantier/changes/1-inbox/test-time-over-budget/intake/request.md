# just test and scenario units over their time budgets on main

Priority P2. Measured by CR-409's Driver (batch-29), 2026-11-20, on the user's Windows machine.

`just test` takes 58-68 s at CR-409's head (1199 tests, `-n auto`), above AGENTS.md's ceiling (at most 30 s above the 18.5 s of 2026-11-14, so 48.5 s). CR-409's own 37 tests add about 3 s across the workers, so main already breaks the ceiling. The slowest tests are in test_carry_ship.py and test_release_tag.py (2-5 s each).

The scenario's units also warn over budget: `direct` 143.7 s against 135 s, `qa-driver` 136.3 s against 115 s (with `parallel` already tight, 248-261 s against 260 s, from an earlier batch).

Measure main's baseline on an idle machine, bring `just test` back under the ceiling (speed up or merge the slowest tests; they check the structure and the refusals, the workflow belongs to the scenario), and re-measure the scenario units' budgets.
