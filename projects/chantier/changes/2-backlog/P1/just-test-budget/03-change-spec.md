# `just test` back within its budget

## Goal

`just test` runs again within the budget AGENTS.md sets: at most 30 s above its 18.5 s of
2026-11-14 on the user's Windows machine, so 48.5 s. The slow tests are profiled and sped up; each
keeps what it covers. The budget line in AGENTS.md stays as it is (test-budget-Q1).

The change touches the speed of the tests only: no behaviour of the CLI, the cards or the board
changes (the spec critic was not run, on that ground: test-budget-Q1).

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

The Driver profiles first (`--durations=0` and a cProfile run, as above), then removes the cost
where it lies, largest first, until the budget holds with margin. The ways below fit the costs
measured; the Driver chooses among them and may find others, within the rules that follow.

1. **Tests and fixtures** (`skills/chantier/scripts/cli/tests/`):
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
2. **The CLI's own code** (`src/chantier/`), only where the cost is in the code itself (the STATUS
   rewriting, git calls repeated within one command): a faster way to the same output. Every
   message, exit code, written file and its bytes stay the same; a refusal still refuses.
3. Nothing in `AGENTS.md`, the cards, `agents/`, `com.github.copilot/agents/`, the scenario or the
   CI files changes.

Rules for every change:

- What a test covers stays: no assertion is removed or weakened, no test is skipped or marked to
  run elsewhere. A test id that disappears (two tests merged to share one expensive world, say)
  is listed in the PR with the test that now holds its assertions.
- The CLI's behaviour does not change; a test that used a real git answer to check a refusal still
  gets it.
- The tests keep calling the CLI in-process (AGENTS.md) and stay portable: `just check` passes on
  Linux, macOS and Windows.
- No new dependency, unless the user says yes to the open question below.

## Out of scope

- Restating the budget (test-budget-Q1: the line stays).
- `just scenario`, `just lint`, the eval kit's own speed.
- Any change of behaviour, message or output of the CLI.

## Evidence

- Before and after, on the user's Windows machine: `just test` three times each, the wall times
  and their median, at the PR's base and head; the after median at most 48.5 s. In the PR's
  Deliverables, with the machine named.
- `uv run --locked --group dev pytest -q --durations=25` at base and head, the two lists in the
  PR, so a reviewer sees which costs moved.
- `uv run --locked --group dev pytest --collect-only -q` at base and head: the collected test ids
  are the same set, or each difference is listed with where its assertions went.
- `just check` passes (Linux, macOS and Windows, CI's `just check` matrix in
  `.github/workflows/ci.yml`).
- When the CLI's code changes (way 2): `just scenario` passes at the PR's head, per AGENTS.md's
  long gate; a change to the tests alone needs none.

## Open questions

1. A parallel runner (for example `pytest-xdist`, a new dev dependency in `pyproject.toml` and
   `uv.lock`, `-n auto` in `just test`) would cut the wall time on its own, without touching what
   the tests cover. The answer chose to speed up the slow tests; may the Driver also add such a
   runner, or should the budget be met by the tests' own speed alone?
2. May the Driver speed up the CLI's own code (way 2, the STATUS rewriting after each save, about
   14 s profiled), with the same output byte for byte, or should this CR change the tests only?
