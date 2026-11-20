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

**UNVERIFIED:** the idle timing of `just test` (three runs, each at most 48.5 s) and the new scenario budgets: figures are added here when measured.

## Blast radius

Grade: 1

Tests, one pytest option and the scenario's budget numbers only; nothing the CLI ships changes. A plain `git revert` restores the previous state.

## Autonomous decisions

- `--dist worksteal` in the `test` recipe: it spreads the slow tests better over the workers and still runs every test.

## Known gaps

- **UNVERIFIED:** `just test` under 48.5 s on an idle machine; no idle measure yet (the machine was loaded with other work, 62 to 100 percent CPU, at every run so far: 84 to 235 s).

<details>
<summary>Details</summary>

## Changes

- `skills/chantier/scripts/cli/tests/`: `writer_rig.py`, `conftest.py`, `store_spy.py`, `cost_world.py`, `stack_world.py` (new), and the setups of `test_access.py`, `test_batch_end.py`, `test_board_prs.py`, `test_carry_ship.py`, `test_gate_carry.py`, `test_leases.py`, `test_release_tag.py`.
- `justfile`: `--dist worksteal`.
- `scenario/run_scenario.py` budgets and `scenario/README.md` measured section: to come from the two idle runs.

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
