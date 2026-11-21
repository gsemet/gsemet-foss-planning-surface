## Summary

`just test` had grown past the project's ceiling (18.5 s on 2026-11-14 plus 30 s, so 48.5 s on the maintainer's Windows machine): it took 58 to 109 s on a loaded machine at main. The scripted scenario's per-unit time budgets were stale for the same reason and made two units warn. This change makes the suite's shared test states build once instead of for every test and every parallel worker, and sets the scenario's nine budgets again from a new measure. No check is removed or weakened.

## Deliverables

Test setup before and after (fixtures only; the 1419 test ids are unchanged):

| Where | Before | After |
| --- | --- | --- |
| writer rig (`writer_rig.py`) | bare origin copy, remote setup and a second clone for every test | built once per module, copied per test |
| stack worlds (`stack_world.py`, new) | batch opened, CRs taken, one worktree per CR for every test | one template per run, copied per test with absolute paths rewritten |
| access batch, cost world, store states | built once per parallel worker (16 times) | built once per run |
| `just test` recipe | `-n auto` | `-n auto --dist worksteal` |

Measures, 2026-11-21, Windows 11 (Ryzen 7 7800X3D, 16 logical cores), the CPU load sampled just before each run; pytest's last line, 1405 passed, 14 skipped each. None was idle, so each counts as loaded:

| run | main `4ed0d56c` | CR head |
| --- | --- | --- |
| 1 | 77.6 s (load 35%) | 63.0 s (60%) |
| 2 | 93.5 s (68%) | 106.8 s (16%) |
| 3 | 73.1 s (25%) | 80.1 s (18%) |

Profile (calls and setups of 0.8 s or more, summed by file), main then head: `test_carry_ship.py` 66 to 48 s, `test_writer_cycle.py` 63 to 45, `test_writer_edges.py` 40 to 28, `test_batch_end.py` 22 to 9, `test_release_tag.py` 14 to 5, `test_gate_carry.py` 14 to 4, `test_store_command_table.py` 13 to 5, `test_surface_writes.py` 11 to 2.

Scenario budgets (`UNITS`): two full `just scenario` runs at the head, started at 25% and 54% load, budget = the slower of the two times plus 25 percent, rounded up to 5 s (the README's table has both runs).

| unit | before | A (s) | B (s) | budget |
| --- | ---: | ---: | ---: | ---: |
| parallel | 260 | 279.4 | 274.4 | 350 |
| stack | 640 | 598.1 | 531.7 | 750 |
| release | 420 | 464.4 | 396.6 | 585 |
| gates | 400 | 486.4 | 426.8 | 610 |
| series-deps | 260 | 284.6 | 301.2 | 380 |
| direct | 135 | 174.9 | 171.6 | 220 |
| surface-board | 700 | 527.9 | 490.6 | 660 |
| qa-driver | 115 | 182.9 | 200.1 | 255 |
| gitlab | 75 | 72.5 | 91.8 | 115 |

In run B, surface-board failed one check (284/285: "the server reads the forge once per cycle for the one project with an open PR, and no second hub reads"); alone minutes later it passed 285/285 in 424.0 s. A load-dependent flake, not a change of this CR.

## Blast radius

Grade: 1

Tests, one pytest option and the scenario's budget numbers only; nothing the CLI ships changes. A plain `git revert` restores the previous state.

## Autonomous decisions

- `--dist worksteal` in the `test` recipe: it spreads the slow tests better over the workers and still runs every test.

## Known gaps

- `just test` at 63.0, 106.8 and 80.1 s on a loaded machine (not idle), ceiling 48.5 s, 1405 passed and 14 skipped; main at 77.6, 93.5 and 73.1 s. No idle measure: other chantier sessions (this machine and another project's batch) shared the CPU. The profile's sum by file is in Deliverables; what is left is the writer, carry-ship and release-tag tests that run real git, which stays real. The ceiling's change, if wanted, is the user's decision in a CR of its own.
- The nine scenario budgets rest on two non-idle runs (25% and 54% load), one with a load flake in surface-board; a quiet-machine run may justify lowering them.

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/scripts/cli/tests/`: `writer_rig.py`, `conftest.py`, `store_spy.py`, `cost_world.py`, `stack_world.py` (new), and the setups of `test_access.py`, `test_batch_end.py`, `test_board_prs.py`, `test_carry_ship.py`, `test_gate_carry.py`, `test_leases.py`, `test_release_tag.py`.
- `justfile`: `--dist worksteal`.
- `scenario/run_scenario.py` (the nine budgets) and `scenario/README.md` (the measured section).

## Impacts

No visual change. Developers see a faster `just test`; real git stays where git is what a test checks.

## Test plan

- [ ] New or changed tests: no behaviour change, no test id changed or removed (1419 collected before and after)
- [ ] Local gates at `<sha7>`: `just test`, `just check`
- [ ] Evidence: idle runs before and after
- [ ] Review: approved at `<sha7>`
- [ ] Verified at `<sha7>`
- [ ] CI green at `<sha7>`

## Internal references

CR-417 test-time-over-budget.

</details>
