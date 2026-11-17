# `just test` back within its budget

## Goal

`just test` runs again within the budget AGENTS.md sets: at most 30 s above its 18.5 s of
2026-11-14 on the user's Windows machine, so 48.5 s. The slow tests are profiled and sped up; each
keeps what it covers. The budget line in AGENTS.md stays as it is (test-budget-Q1).

Two levers, both required (test-budget-Q2): `just test` runs the suite in parallel with
`pytest-xdist`, and the tests themselves get faster where the profile puts the cost. The Driver may
also speed up the CLI's own code (the STATUS rewriting after each save), with byte-identical
output (test-budget-Q3).

No behaviour of the CLI, the cards or the board changes (the spec critic was not run, on that
ground: test-budget-Q1).

## Where the time goes (measured 2026-11-17, the user's Windows machine, main at 3df17b9)

`uv run --locked --group dev pytest -q --durations=0` (what `just test` runs): 369 passed in
76-79 s; the intake measured 61-63 s on CR-303's Verifier. Of the summed test time, about 33 s is
fixture setup and 39 s is test bodies. A `git` process costs about 0.06 s on this machine, and the
suite starts about 580 subprocesses. A cProfile run of the whole suite (`python -m cProfile -m
pytest`, 94 s under the profiler) names these costs; the Driver re-measures before choosing:

| Cost | Where | Profiled time |
|---|---|---|
| `git rev-parse --git-common-dir`, once per test: the `chantier` fixture's `git_cached` (`tests/conftest.py`) keeps the answer per folder, but each test has a new folder, so its first call is a real process (169 misses) | `core/repo.py` `Repo.find`, reached through `file_cr`, `playbook`, `open_batch` | about 10 s |
| `git remote` in `open_settings` on every `chantier open` (107 calls), though the tests pass `--default-branch` | `commands/opening_record.py` `open_settings` | about 6.6 s |
| The `surface` fixture runs `git init`, `git add` and `git commit` per test (84 processes) and copies the repository again | `tests/conftest.py` `surface` | about 7 s |
| `cost_world.build` opens a batch, takes two CRs and sets agents, for each of 23 tests (17 in `test_spend_check.py`, each about 0.55 s) | `tests/cost_world.py` `build` | about 13 s |
| The STATUS files and the dashboard rewritten after each saved change (506 saves): `write_batch` (`cr_view`, `_events_by_cr`, `_write`) and `write_dashboard` (`dashboard_view`) | `lifecycle/session.py` `RenderedBatch.after_save`, `status/write.py`, `status/views.py` | about 14 s |
| `git rev-parse --show-toplevel` and `--git-common-dir` in external mode (50), and preflight's checkout checks (48) | `core/repo.py` `Repo._external`, `commands/preflight.py` `_check_checkout` | about 5.5 s |
| `test_a_held_port_is_refused_with_the_port_and_the_way_out`: the board probes a port that listens but never answers, and waits out `address._call`'s 2 s timeout | `tests/test_board.py`, `board/address.py` | about 4 s |
| `test_the_eval_sandbox_builds_its_recorded_base`: a subprocess building the eval sandbox's git base | `tests/test_cli_units.py` | about 2.5 s |

Paths under `skills/chantier/scripts/cli/` (`src/chantier/...` and `tests/...`).

## What changes

The Driver profiles first (`--durations=0` and a cProfile run, as above, serially), then does all
three parts below. In part 2 it removes the cost where it lies, largest first; the ways listed fit
the costs measured, and the Driver chooses among them and may find others, within the rules that
follow.

1. **A parallel runner** (test-budget-Q2):
   - `pytest-xdist` joins the `dev` dependency group in the root `pyproject.toml`
     (`[dependency-groups] dev`, today `["pytest>=8"]`), locked in `uv.lock` (`uv lock`;
     `just lint`'s `uv lock --check` passes).
   - The `test` recipe in `justfile` (today `uv run --locked --group dev pytest -q {{args}}`) runs
     the suite in parallel (`-n auto` or an equivalent set in the recipe or in
     `[tool.pytest.ini_options]`); `{{args}}` still pass through, so `just test -k <name>` and a
     serial run (`just test -n 0`) keep working.
   - Every test passes under the parallel run, on Linux, macOS and Windows, and still passes
     serially: no test depends on another's order or shared state. A session-scoped fixture
     (`repo_template`, and the ones part 2 adds) runs once per worker under xdist; each must stay
     right that way (its own `tmp_path_factory` folder per worker, nothing written outside it).
2. **Tests and fixtures** (`skills/chantier/scripts/cli/tests/`), also required (test-budget-Q2):
   the parallel runner alone does not close the CR.
   - Answer once what a test's repository makes certain, without a git process: the common git
     folder of the `repo` fixture's copy is its own `.git`. A seeded answer holds only while the
     test does not change what it answers (a test that removes the remote, moves the repository or
     makes a worktree gets the real git answer).
   - Build the external surface once per session, like `repo_template`, and copy it per test.
   - Build the cost world once (session or module scope) and copy its folder per test, with the
     environment each test sets (`CHANTIER_CLAUDE_PROJECTS`, `CLAUDE_CODE_SESSION_ID`,
     `CHANTIER_BATCH`) re-pointed at the copy, when what it holds (batch record, paths, times) stays
     right for each test after the copy; or share one world among the parametrized cases that only
     read it.
   - In the held-port test, keep the refusal it checks (exit code, the one error line, the port
     and `--port` named) without waiting out the probe's timeout.
3. **The CLI's own code** (`skills/chantier/scripts/cli/src/chantier/`), allowed
   (test-budget-Q3), where the cost is in the code itself: chiefly the STATUS rewriting after each
   save (`RenderedBatch.after_save`, `status/write.py`, `status/views.py`, about 14 s profiled), and
   git calls repeated within one command. A faster way to the same output: every message, exit
   code, written file and its bytes stay the same; a refusal still refuses. Such a change makes
   `just scenario` due before the PR (AGENTS.md's long gate).
4. Nothing in `AGENTS.md`, the cards, `agents/`, `com.github.copilot/agents/`, the scenario or the
   CI files changes.

Rules for every change:

- What a test covers stays: no assertion is removed or weakened, no test is skipped or marked to
  run elsewhere. A test id that disappears (two tests merged to share one expensive world, say)
  is listed in the PR with the test that now holds its assertions.
- The CLI's behaviour does not change; a test that used a real git answer to check a refusal still
  gets it.
- The tests keep calling the CLI in-process (AGENTS.md; an xdist worker is a pytest process that
  calls the CLI in-process like the serial run) and stay portable: `just check` passes on Linux,
  macOS and Windows.
- `pytest-xdist` is the one new dependency (test-budget-Q2); no other is added.

## Decisions

- test-budget-Q1: speed up the slow tests, keeping what they cover; the budget line in AGENTS.md
  stays.
- test-budget-Q2: both levers: `pytest-xdist` (dev dependency, locked in `uv.lock`) runs
  `just test` in parallel, and the tests themselves get faster (git per test, `cost_world` rebuilt
  per test, the `surface` fixture, the held-port wait). Not one or the other.
- test-budget-Q3: the Driver may speed up the CLI's own code (the STATUS rewriting after each
  save) with byte-identical output; then `just scenario` is due before the PR.

## Out of scope

- Restating the budget (test-budget-Q1: the line stays).
- `just scenario`, `just lint`, the eval kit's own speed.
- Any change of behaviour, message or output of the CLI.

## Evidence

- Before and after, on the user's Windows machine: `just test` three times each, the wall times
  and their median, at the PR's base (serial, as base runs it) and head (parallel, as the new
  recipe runs it); the after median at most 48.5 s. In the PR's Deliverables, with the machine
  named and its core count (what `-n auto` uses).
- The tests' own speed, apart from the runner: at the PR's head, `just test -n 0` (serial) three
  times, its median beside the base's, so a reviewer sees that part 2 cut time on its own.
- `uv run --locked --group dev pytest -q -n 0 --durations=25` at base and head (serial, so the
  durations compare), the two lists in the PR, so a reviewer sees which costs moved.
- `uv run --locked --group dev pytest --collect-only -q -n 0` at base and head (at base without
  `-n 0`, which it does not know yet): the collected test ids are the same set, or each difference
  is listed with where its assertions went.
- `just check` passes, which now runs the suite under xdist, on Linux, macOS and Windows (CI's
  `just check` matrix in `.github/workflows/ci.yml`); and `just lint`'s `uv lock --check` passes
  with the new lock.
- When the CLI's code changes (part 3): `just scenario` passes at the PR's head, per AGENTS.md's
  long gate (CI's `just scenario (ubuntu-latest)` job, green at the head). A change to the tests alone
  needs none; for a head that changes only the tests, `pyproject.toml`, `uv.lock` and
  `justfile`, see open question 1.

## Open questions

None. The Chief of Staff settled the last one (2026-11-17): adding `pytest-xdist` changes the root
`pyproject.toml` and `uv.lock`, which also lock the CLI's package, so `just scenario` is due before
the PR whether or not the Driver touches the CLI's code (part 3): the pipeline's
`just scenario (ubuntu-latest)` job green at the PR's head.
