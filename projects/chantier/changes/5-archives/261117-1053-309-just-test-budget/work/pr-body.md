## Summary

`just test` had grown to 62-104 s on a loaded Windows machine, above the 48.5 s budget the project sets (18.5 s plus 30 s). This PR runs the suite in parallel with `pytest-xdist` and removes the largest per-test costs (a `git` process per test, a surface and a cost world rebuilt per test, a 2 s wait in one board test). No CLI behaviour changes and no test loses an assertion.

## Deliverables

Wall time of `just test` on the author's Windows machine (16 logical cores, the count `-n auto` uses), three runs each, in seconds. Base is `ab9b0b5` (the PR's base). The machine was busy during these runs, so the base figures are higher than earlier quiet runs (62-79 s); the head median of 21 s stays far inside the 48.5 s budget either way.

| Run | Runs | Median |
|---|---|---|
| Base, serial (as base runs it) | 87, 104, 98 | 98 |
| Head, parallel (`just test`) | 22, 21, 16 | 21 |
| Head, serial (`just test -n 0`) | 44, 43, 45 | 44 |

```
just test            # pytest -q -n auto, parallel
just test -n 0       # serial; -k and other arguments still pass through
```

- Choices: each session fixture (`surface_template`, the cost-world template) is built once per xdist worker in its own `tmp_path_factory` folder; a seeded git answer is used only while the test's repository is untouched.
- Collected tests: `pytest --collect-only -q` gives the same 369 test ids at base and head (the two lists were compared and are identical); none disappeared.
- Slowest tests, serial (`pytest -n 0 --durations=25`, top 6 of 25, call or setup seconds; the lists were taken at the base's parent commit `3df17b9`, which this PR's base only follows by one formatting commit, and at the head):

| Base | Head |
|---|---|
| 4.10 `test_a_held_port_is_refused_with_the_port_and_the_way_out` | 2.00 `test_the_eval_sandbox_builds_its_recorded_base` |
| 1.47 `test_the_eval_sandbox_builds_its_recorded_base` | 1.21 `test_an_external_surface_gets_the_planning_folder_and_the_project_stays_clean` |
| 0.85 `test_preflight_reads_the_settings_files_for_allow_rules` | 1.16 `test_preflight_reads_the_settings_files_for_allow_rules` |
| 0.83 `test_an_external_surface_gets_the_planning_folder_and_the_project_stays_clean` | 1.01 `test_a_bad_long_gate_key_is_refused_with_its_line_by_gate_playbook_and_preflight` |
| 0.62-0.44 setup of 17 `test_spend_check.py` cases (cost world per test) | 0.92 `test_preflight_warns_on_missing_allow_rules_and_never_fails_on_them` |
| 0.44 `test_files_and_functions_are_small_and_the_imports_have_no_cycle` | 0.92 `test_the_plugin_runs_with_no_setup_and_writes_only_in_the_planning_folder[claude]` |

The held-port test and the 17 cost-world setups left the list; the head list tops out at about 2 s, and its figures are higher in places because that serial run was on a busier machine. The full lists are named under Internal references.

## Blast radius

Grade: **1**. Test infrastructure, the dev dependency group and the `test` recipe only; a plain `git revert` restores the previous behaviour.

## Autonomous decisions

- The CLI's own code is not changed: the STATUS rewriting cost is file I/O (about 30 ms per save in the profile), and skipping unchanged writes would alter the modification times the board fingerprints, so no byte-identical win was found without risk. The suite is inside the budget with the two other levers.
- The eval sandbox test (about 1.8 s, a real subprocess) and preflight's git checks are left as they are.

## Known gaps

- Linux and macOS are covered by CI alone; the timings come from one Windows machine.

<details>
<summary>Details</summary>

## Changes

- `pyproject.toml`, `uv.lock`: `pytest-xdist` joins the `dev` group.
- `justfile`: the `test` recipe runs `pytest -q -n auto {{args}}`.
- `skills/chantier/scripts/cli/tests/conftest.py`: the `repo` fixture seeds its copy's common git folder; a session `surface_template` replaces `git init`/`add`/`commit` per test.
- `skills/chantier/scripts/cli/tests/cost_world.py`: the world is built once per worker and copied per test, with the environment re-pointed.
- `skills/chantier/scripts/cli/tests/test_board.py`: the held-port test keeps its real listening port and its assertions, and no longer waits out the probe's 2 s timeout.

## Human decisions

- The test-time budget line stays as it is (18.5 s plus 30 s); the slow tests are sped up, keeping what each covers.
- Both levers are used: `pytest-xdist` runs the suite in parallel, and the tests themselves get faster. Not one or the other.
- The CLI's own code may be sped up with byte-identical output; that would make the long gate due before the PR.

## Impacts

No visual change. Contributors run `just test` in parallel; `just test -n 0` runs it serially.

## Test plan

- [x] No behaviour change: the same 369 tests pass in parallel and serially; `uv lock --check` passes with the new lock.
- [x] Local gates at `23e0b01`: `just check` and `just test -n 0`.
- [x] Evidence: base `ab9b0b5`, head `23e0b01`, timings above.
- [x] Review: approved at `23e0b01` (carried from `e35193b`, a clean rebase).
- [x] Verified at `23e0b01`: tests, collected ids, lock and held-port claims checked at that head.
- [x] CI green at `23e0b01`, including `just scenario (ubuntu-latest)`: due because the root `pyproject.toml` and `uv.lock` change.

## Internal references

CR-309 `just test` back within its budget. Work files: `work/durations-base.txt`, `work/durations-head.txt` (full top-25 lists), `work/collect-base.txt`, `work/collect-head.txt`, `work/measure.txt`.

</details>
