## Summary

`just scenario`, the scripted run of the whole CLI with no model, was one long sequence on one temporary repository, replayed whole for GitLab: about 25 minutes per forge on a Windows machine, and every new change added its cases to the same sequence. This PR splits it into nine independent units, each in its own temporary world, run four at a time; GitLab runs only its forge-specific unit. The pure refusals move to in-process, parametrized pytest. A structure test keeps every coverage bullet of `scenario/README.md` mapped to a unit or a test, and a standing rule keeps the scenario from growing back. A hung unit is killed and fails the run; slowness alone only warns.

On the machine of the measurement (loaded by other sessions) the full run goes from 1472.9 s (GitHub) plus 1456.3 s (GitLab) to a wall time of 449.8 s with 4 units at a time and 354.0 s with 8. The Windows measurement misses the 5-minute target on a loaded machine; the GitHub Linux run takes 1 min 43 s (see Known gaps).

## Deliverables

Before and after, same machine (Windows 11, 16 cores, loaded):

| | before (one forge, then the other) | after, `--jobs 4` | after, `--jobs 8` |
| --- | --- | --- | --- |
| wall time | 1472.9 s + 1456.3 s | 449.8 s | 354.0 s |
| sum of the units | one sequence | 1671.6 s | 1940.0 s |
| `just test` (pytest) | 72 tests, 21.7 s | 100 tests, about 29 s | |

The slowest units at `--jobs 4`: `release` 333 s, `gates` 262 s, `stack` 259 s. The per-unit table is printed on every run (checks, commands started, seconds, budget, status).

```text
UNITS = {name: (budget_s, forges, [case, ...])}   # parallel, stack, release, gates, series-deps,
                                                  # direct, surface-board, qa-driver, gitlab
uv run --locked python scenario/run_scenario.py [--jobs N] [--unit NAME]... [--forge github|gitlab]
```

Choices: nine units whose cases do not share a world; a unit over its budget warns, a hung unit fails; the pure refusals (playbook configuration, cost reading for both hosts, rail and gate refusals, opening and restore, triage moves) live in pytest; the pytest fixtures cache git's answers so the suite got faster rather than slower.

## Blast radius

Grade: 1

Only the scenario, its README, the tests, the `justfile` recipe and two documentation lines change; nothing under the CLI's `src/`. A `git revert` restores the old single sequence.

## Autonomous decisions

- The two checks lost in the move to pytest (a paused batch's CR page keeps its cost, its link to the batch and its Merged box; the batch's STATUS.md gives each CR's cost) were put back in `test_cost_reading.py` after review.
- `scenario/run_scenario.py` keeps its own formatting: an accidental whole-file format was undone, so its diff is the real edits only.
- `just test` was brought down by caching git's repository-folder answer per folder and building the test repository once per session, not by dropping tests.
- Unit budgets are the measured `--jobs 4` time plus about 25 percent (parallel 260, stack 320, release 420, gates 330, series-deps 190, direct 125, surface-board 250, qa-driver 115, gitlab 95 seconds), from a loaded machine.
- The rebase onto the merged removal of the legacy readers dropped the `(legacy: ...)` marker of the coverage test and the README bullets for the removed cases.

## Known gaps

- The under-5-minutes target is not met by the measurement on this machine (449.8 s with 4 units, 354.0 s with 8, loaded by other sessions); `release` alone takes 333 s, so splitting it is what would close this.
- No quiet-machine timing and no three consecutive green runs yet; the one Linux CI run read, `just scenario` on ubuntu-latest at `fb7d936`, took 1 min 43 s.
- The scratch-branch demonstrations the specification lists (a deliberately broken unit or coverage bullet shown to fail) were not run; the structure test and the hang timeout are covered by their own checks only.
- The long gate ran on Windows only; Linux and macOS are covered by CI alone.
- The unit budgets come from a loaded run and should be lowered after a quiet one.
- Some cases stay in the scenario rather than in pytest (second pause and live close refusals, dependency cycles, granted-fix refusals, board padding, crafted driver lines, the "preflight once" slimming of the main batch).

<details>
<summary>Details</summary>

## Changes

- `scenario/run_scenario.py`: a `UNITS` table, a parallel runner (`--jobs`, `--unit`, `--forge`), a per-case and per-section timer, a count of the commands the scenario starts, a hang timeout, the per-unit table; duplicate checks cut; ported cases removed.
- `scenario/README.md`: units, options, the measurement, "Adding a case", every coverage bullet marked `(unit:)` and/or `(test:)`.
- `skills/chantier/scripts/cli/tests/`: `batch_helpers.py`, `cost_world.py`, `test_playbook_config.py`, `test_cost_reading.py`, `test_cost_copilot.py`, `test_rail_refusals.py`, `test_gate_refusals.py`, `test_opening_and_restore.py`, `test_triage_moves.py`, `test_scenario_coverage.py` (the coverage contract), and `conftest.py` (cached git answers, a repository template).
- `justfile`, `AGENTS.md`, `CONTRIBUTING.md`: the recipe and the rules on tests and on adding a case.

## Human decisions

- Units run 4 at a time by default, a fixed number the option `--jobs` can change.
- A hung unit (past 600 s, or 4 times its budget if longer) is killed and fails the run; slowness alone only warns.
- The README's coverage list is the contract: a structure test checks that each bullet maps to a unit or a test, and a standing rule keeps the scenario from growing back.
- GitLab runs only its forge-specific unit; the calls that need real processes stay in the scenario, the pure refusals go to pytest.
- The 5-minute target is set to hold on the maintainer's Windows machine for both forges and on Linux CI.

## Impacts

No visual change; `just scenario` runs units in parallel and prints a table; the CLI is unchanged.

## Test plan

- [x] New or changed tests (the coverage test and the ported refusals)
- [x] Local gates at `fb7d936`: `just check` pass (100 passed), `just scenario` pass (all nine units, exit 0), run by the long gate on Windows
- [x] Evidence: before at `4ecc7cd`, after at `fb7d936`: the two full runs in the Deliverables table
- [x] Review: approved at `6c5c55d`, carried to `fb7d936` (budgets and README only)
- [x] Verified at `fb7d936`
- [x] CI green at `fb7d936`: all five jobs pass (`gh pr checks 211`)

## Internal references

- CR-254 fast-scenario; work files `work/step0-baseline.md`, `work/r3.md`, `work/r4.md`, `work/r5.md`, `work/conflicts.md`, `work/gates/`.

</details>
