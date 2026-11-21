# just test back under its ceiling; scenario budgets re-measured

## Goal

`just test` runs again within the project's ceiling on the user's Windows machine: at most 30 s
above its 18.5 s of 2026-11-14, so 48.5 s (AGENTS.md, CONTRIBUTING.md). No check is lost for it.
The scenario's nine unit budgets are set again from a new measure, and the measured section of
`scenario/README.md` says what was measured, when and how.

Origin: CR-409's Driver (batch-29, 2026-11-20) measured `just test` at 58 to 68 s (1199 tests,
`-n auto`), and the scenario's units `direct` at 143.7 s against 135 s and `qa-driver` at 136.3 s
against 115 s, with `parallel` at 248 to 261 s against 260 s.

## Decisions

The user asks no questions on this CR. The Chief of Staff settled every open point on 2026-11-20;
`02-answers.md` holds them (A1 to A12), and this specification carries each:

1. The ceiling does not change (A1). AGENTS.md and CONTRIBUTING.md are not edited.
2. The measure of `just test` is pytest's own last line, on three runs in a row, on the idle
   Windows machine; under the ceiling means each of the three at most 48.5 s (A2).
3. A measure taken on a loaded machine is recorded as loaded and proves nothing (A3).
4. Only time savings that keep every assertion are allowed (A4, listed below).
5. No check moves from pytest to the scenario (A5).
6. Nothing under `skills/chantier/scripts/cli/src/` changes (A6).
7. An inventory of the test ids, before and after, proves that no coverage is lost (A7).
8. The scenario's units are not sped up: their budgets are re-set (A8).
9. A unit's budget is the slower of two idle full runs plus 25 percent, rounded up to the next
   5 s, for the nine units alike (A9).
10. The measured section of `scenario/README.md` is rewritten from that measure (A10).
11. No guard is added, on the time or on the README's budget column (A11).
12. The work starts with the costliest files and stops under the ceiling or at the third round
    (A12).

## What changes

### 1. The baseline (before any edit)

At main's head, in the CR's worktree, on the user's Windows machine with nothing else running on
it (no other `just test`, `just scenario`, `chantier gate` or eval):

- `just test` three times in a row; keep pytest's last line of each (`N passed, M skipped in
  X s`).
- `just test --durations=0 -p no:cacheprovider` once, its output kept: the profile. Sum it by
  file, calls and setups apart.
- `uv run --locked --group dev pytest --collect-only -q` once, its output kept: the list of test
  ids before the change.

A figure for orientation only, taken on a loaded machine on 2026-11-20 at main `4ed0d56c`: 1405
passed, 14 skipped in 89.0 s. The calls and setups of 0.8 s or more summed to `test_writer_cycle.py`
66 s, `test_carry_ship.py` 64 s, `test_writer_edges.py` 47 s, `test_release_tag.py` 13 s,
`test_store_command_table.py` 12 s, `test_surface_writes.py` 10 s, `test_external_archive.py` 6 s,
`test_batch_end.py` 5 s. The slowest single tests took 4 to 8 s each. What they share: each
builds its state with real git processes (worktrees, clones, a bare origin, fetches, rebases), and a
process start is slow on Windows.

### 2. The tests (`skills/chantier/scripts/cli/tests/`)

Work down the profile, the costliest file first, and measure after each file. The files to expect,
from the figure above:

- `writer_rig.py` (the `rig` fixture and its `make`: a copy of the bare origin, then `git remote
  add`, `fetch`, `branch -u`, `remote set-head` and a second `clone` for every test) and its users
  `test_writer_cycle.py` and `test_writer_edges.py`.
- `test_carry_ship.py` (the `stack` and `stack3` fixtures: a batch opened, each CR taken, one `git
  worktree add` per CR, for every test).
- `test_release_tag.py` (`test_ff_main`: a repository and its remote built with git for each of
  its cases; `test_ff_main_command_runs_the_shipped_script`).
- `test_store_command_table.py` and `test_surface_writes.py` (setups of 2 to 3 s).
- `conftest.py` (`repo`, `surface`, `repo_template`, `surface_template`), where a prepared state
  shared by several files belongs.

Allowed, and nothing else:

- A prepared state built once, per session or per module, and copied for each test, as
  `repo_template` and `surface_template` already do. A copied git repository must stay correct
  where it is copied: worktrees and remotes hold absolute paths, so a template that has them is
  repaired or re-pointed after the copy, and the test's result must not depend on the template's
  folder.
- Fewer git processes for the same state: one command in place of several, a state written to
  disk in place of the commands that build it, when git's own behaviour is not what the test
  checks.
- Tests that build the same state merged into one test, or into one parametrized test; each
  assertion is kept, with a message that tells which former test it came from when the merge would
  hide it.
- A duplicate removed: a test whose every assertion another test already makes. The PR names
  both.
- pytest's and xdist's own settings (how tests are spread over the workers), in `pyproject.toml`'s
  `[tool.pytest.ini_options]` or in the `test` recipe of the `justfile`, provided the plain `just
  test` still runs every test.

Refused:

- A skip, a marker, a `-k` or `-m` filter, or a separate recipe that takes a test out of the plain
  `just test`.
- A fake in place of real git where real git is what the test checks: the writer's commit,
  rebase, conflict, stash and push (`test_writer_cycle.py`, `test_writer_edges.py`), the carry's
  comparison of patches (`test_carry_ship.py`, `test_gate_carry.py`), the fast-forward of main
  (`test_release_tag.py`).
- A weaker assertion, or a refusal of the CLI that is no longer checked.
- A check moved to `scenario/run_scenario.py`.
- Any edit under `skills/chantier/scripts/cli/src/`. A saving that needs one is not made; the
  Driver names it in its hand-back as an idea for the inbox.

`scenario/README.md`'s coverage list names tests by `(test: <file>::<test>)`. Each test renamed,
merged or removed is renamed there in the same commit; `test_scenario_coverage.py` fails
otherwise.

### 3. The scenario's budgets (`scenario/run_scenario.py`)

Only the nine budget literals of `UNITS` change (today: `parallel` 260, `stack` 640, `release`
420, `gates` 400, `series-deps` 260, `direct` 135, `surface-board` 700, `qa-driver` 115, `gitlab`
75). No case is added, moved, sped up or removed; `JOBS` and `HANG_FLOOR_S` stay.

The measure: two full runs of `just scenario` (no argument: both forges, `--jobs 4`) at the CR's
head, after the tests' change, on the idle Windows machine. Each run's table is in
`scenario/results/scenario-<stamp>-<pid>.md`. For each unit, the new budget is the slower of its
two times plus 25 percent, rounded up to the next 5 s. The rule is applied to the nine units,
upward or downward.

### 4. The scenario's README (`scenario/README.md`)

The measured section is rewritten: from the paragraph "Measured on 2026-11-15 ..." to the
paragraph that ends "... and lower the budgets". It holds:

- the date, the machine and the load of the measure (idle, and what idle means: section 1);
- the rule of a budget (the slower of two idle `--jobs 4` runs plus 25 percent, rounded up to
  5 s), and that under load a unit may warn, since a unit over its budget only warns;
- one table: the nine units, each with its budget as `UNITS` holds it and its time in run A and
  run B; the wall time and the sum of the units for each run.

The stale figures go: `direct` 125 and `surface-board` 300 in the table, the `stack` paragraph's
older runs, the `--jobs 8` sentence. The sentence saying that under 300 s on a quiet Linux machine
is not proven stays as it is, unless the PR's own CI run of `just scenario (ubuntu-latest)` gives
the units' times: then the README quotes them, with the run's date. The rest of the README does
not change, but the coverage list's test names (section 2).

## If the ceiling cannot be met

Said plainly: this CR does not change the ceiling, and it does not buy time with coverage. If, at
the end of the third round, one of the three idle runs is still above 48.5 s with every allowed
saving made on the costliest files, the Driver:

- delivers what it has (the suite is faster, no check is lost);
- writes in the PR's Known gaps: "`just test` at X s on an idle machine, ceiling 48.5 s", with
  the three figures, the number of tests, and the profile's sum by file at its head;
- says in its hand-back what is left and why it cannot go without a refused means (a fake of git,
  a test out of the default run, a CLI change).

The ceiling's change is then the user's decision, in a CR of its own that the Chief of Staff
files; AGENTS.md's figure dates from 2026-11-14 and the suite has grown since (1199 tests at
CR-409's head, 1405 at main `4ed0d56c`).

## Out of scope

- AGENTS.md's and CONTRIBUTING.md's ceiling.
- The CLI's source, the cards, the agents, the hooks, the eval kit, the CI workflow.
- Speeding up, moving or removing a scenario case; a new unit; `JOBS`.
- A test or a CI step that fails when `just test` is slow.
- A test that compares the README's budget column with `UNITS`.
- The proof of the scenario under 300 s on a quiet Linux machine.

## Evidence

No CI job is added or changed. Nothing here depends on the host or on a shipped default: no host
and default matrix.

In the CR's evidence, and summed up in the PR's Deliverables:

1. `just test`, idle, three runs at main's head and three at the CR's head: pytest's last line of
   each, the date, and what "idle" was checked against. Each of the three at the CR's head is at
   most 48.5 s, or the Known gaps line of the section above is there. A run on a loaded machine is
   marked loaded and counts for nothing; with no idle run at all, Known gaps says "no idle measure
   of `just test`".
2. The inventory: the test ids of `pytest --collect-only -q` at main's head and at the CR's head.
   Every id gone or renamed is listed with the test id that now holds each of its assertions. An
   id with no destination fails the CR. The Verifier checks the list against the diff: it opens
   each merged or removed test in main and finds its assertions at the head.
3. The profile's sum by file, before and after, for the files changed.
4. `just check` green at the head (it runs the whole suite, `test_scenario_coverage.py` included,
   which reads `scenario/README.md` and `scenario/run_scenario.py` from the repository as they
   ship at that head).
5. The two full `just scenario` runs at the CR's head on Windows: their two result files' tables,
   all checks passing, and for each unit the arithmetic from its two times to its new literal. In
   the second run, made or repeated with the new literals in place, no unit warns over its budget.
6. `scenario/README.md`'s table equals `UNITS` for the nine budgets, and its two columns equal the
   two runs of point 5.
7. The diff touches only `skills/chantier/scripts/cli/tests/`, `scenario/run_scenario.py` (the
   nine literals), `scenario/README.md` and, if a setting of pytest or xdist changed,
   `pyproject.toml` or the `justfile`'s `test` recipe.

Gates, from the project's rules: `just check` before the first push, at the rebased head. `just
eval-dry-run` is not owed (nothing under the CLI's `src/` or `evals/kit/` changes). The scenario
changes, so the long gate is owed: `just scenario (ubuntu-latest)` green at the PR's head. `just
mod` is not owed.

## Open questions

None. The one point left to the user is conditional: the ceiling, if the section "If the ceiling
cannot be met" applies.
