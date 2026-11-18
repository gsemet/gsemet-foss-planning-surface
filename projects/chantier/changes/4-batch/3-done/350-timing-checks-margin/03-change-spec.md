# Change Specification: timing-bound checks hold on a loaded machine

## Goal

The user's terms (retro of batch-24): timing-bound checks failed under load and cost reruns. The
scenario's reused-pid check and the autosync test wait on a condition with a margin that holds on
a loaded machine, not on a fixed short timeout; a download timeout in CI is retried once.

The three failures seen: the local Windows gate at CR-336 (`order merged does not signal a reused
pid`), `test_board.py::test_join_observe_reports_early_failure_exactly` on macOS (CR-345,
`timeout=1`), and a mypy wheel download timeout in CI's macOS `just check` (CR-343).

## What changes

### 1. Scenario: `scenario/run_scenario.py`, `rails()` (section 19), the reused-pid block

Probable cause (02-answers tc-Q1; the failing run's detail was not kept: its log shows only the failed check's label, and its transcript is gone): `procs.py` treats a recorded pid as live when
`proc.create_time() <= recorded + CLOCK_MARGIN_S` (1 s), `recorded` being the lock's file time.
`reused_lock()` sets the lock's time to `time.time() - 10` at each call, but the sleeper was
started at the top of the block; after about 9 s of section time the sleeper's creation time falls
before the lock's time, the sleeper passes for the recorded process, and `order merged` (the last
of the four checks) signals it. A second cause fits the same symptom: the sleeper exits by itself
120 s after it starts, and the `cancel` and `order merged` checks assert that it lives on, so a
section that runs longer than 120 s on a loaded machine fails them too (02-answers tc-Q6). The
change removes both.

Change:

- The sleeper sleeps 600 s instead of 120 s: `time.sleep(600)` (it is killed at the block's end,
  `sleeper.kill()`; 02-answers tc-Q6).
- Right after `sleeper = subprocess.Popen(...)`, read its creation time once:
  `born = psutil.Process(sleeper.pid).create_time()` (local `import psutil`, as the file already
  does near its end; `psutil` is a locked CLI dependency).
- `reused_lock(cr)`: `back = born - 60` instead of `time.time() - 10`; comment: the lock dates from
  before the sleeper was created, so the sleeper is a reused pid however long the section runs (within the sleeper's 600 s).
- The stale queue ticket: its name's arrival prefix is `f"{int((born - 60) * 10**9):020d}-{sleeper.pid}"`
  and its `os.utime` time is `born - 60`, instead of the two "now minus 10 s" values.
- The check "a lock naming a reused pid is not waited for: the next gate runs at once": the bound
  `time.monotonic() - started < 10` becomes `< 60` (02-answers tc-Q2; a wrong wait would last the
  sleeper's remaining life, well over 60 s). The check's text stays.

No check's text, order or count changes; no other section changes.

### 2. Test: `skills/chantier/scripts/cli/tests/test_board.py`

`test_join_observe_reports_early_failure_exactly`: `autosync_tool.observe_join(proc, timeout=1)`
becomes `timeout=60` (02-answers tc-Q3). `observe_join` returns when the child exits, so the
assertion still proves the exact early diagnostic and the test takes no longer on an idle machine.
`test_join_watch_reports_delayed_failure_exactly` and
`test_join_watch_does_not_report_a_success_that_stays_alive` keep `timeout=0.01`: there the child
blocks on stdin and the short wait is the condition under test, not a margin.

The other short waits of the same autosync group go to 60 s too (02-answers tc-Q7); each returns
as soon as its condition holds, so none is slower on an idle machine:

- `test_join_drains_large_output_without_deadlock`: `observe_join(proc, timeout=3)` becomes
  `timeout=60`.
- `test_join_watch_reports_delayed_failure_exactly` and
  `test_join_watch_does_not_report_a_success_that_stays_alive`: `watcher.join(timeout=3)` and, in
  their `finally`, `proc.wait(timeout=3)` become `timeout=60`.

### 3. CI download retried once: `justfile` and `.github/workflows/ci.yml`

`justfile`, a new recipe beside `lint` (02-answers tc-Q4):

```just
# Fetch the pinned check tools into the caches, running nothing (CI runs it before `check`, retried once)
tools:
    uv sync --locked --group dev
    uv run --locked --group dev --with {{mypy}} --with types-psutil mypy --version
    uvx {{ruff}} --version
    uvx --from {{node}} npx --yes {{biome}} --version
```

It uses the existing `ruff`, `mypy`, `node` and `biome` variables; no pin is copied.

`.github/workflows/ci.yml`, job `check`, one step between "Git identity for the test repositories"
and `- run: just check`:

```yaml
      # A download that times out (seen: a mypy wheel on macOS) is retried once; `just check` is not.
      - name: Fetch the check tools (retried once)
        shell: bash
        run: just tools || just tools
```

`shell: bash` gives `||` on the three runners (Git Bash on Windows). The job's name, matrix and
`continue-on-error` do not change, so the required check names on `main` stay.

## Out of scope

- No CLI change: `procs.py`'s `CLOCK_MARGIN_S` is right; the scenario's setup was wrong.
- No card change, no new test, no new CLI tool.
- No retry in the `scenario` and `eval-dry-run` jobs, no retry of `just check` itself, no uv
  timeout setting (the request names the `just check` download only).
- No other timing bound in the scenario or the tests is touched than those named above.
- A network read inside `just check` itself (e.g. `uv lock --check`'s index read) is not retried;
  only the tool and wheel fetches of `just tools` are (02-answers tc-Q8).
- No CONTRIBUTING.md change (`just` lists the new recipe).

## CI environment (the changed `check` job)

- Runs on `ubuntu-latest`, `macos-15-intel` (named `macos-latest`) and `windows-latest`, with
  `astral-sh/setup-uv@v6` and `extractions/setup-just@v3`.
- Absent there and present locally: a warm uv cache (empty at each run), a warm npm cache for
  `npx` (empty), the user's network state (the runner's own, where the macOS download timed out).
- Only the first CI run proves: the step on the three real runners (bash on Windows, the npm
  fetch), and that `just check` then finds its tools in the caches. A real download timeout and
  its retry cannot be provoked; the retry is proved by its shape (`||`) only.

## Evidence

- `just check` passes in the worktree (Windows), with the changed test.
- `just test -k test_join` passes (the four changed autosync tests).
- `just scenario` passes locally (Windows) and in CI's `just scenario (ubuntu-latest)`; section 19's
  transcript shows the four reused-pid checks green, with the sleeper started at least 60 s after
  the lock's backdated time.
- The CI step, as CONTRIBUTING.md "Daily work" asks for a changed job: with `UV_CACHE_DIR` set to
  a new empty folder outside the repository (the same for both commands), run `just tools` then
  `just check` once on the local machine, in that order; both pass. Quote the two commands and
  their result in the PR.
- The PR's CI: `just check` green on ubuntu and windows, and on macOS (the job may fail on macOS
  without blocking, `continue-on-error`; its log shows the new step ran).
- No `just eval-dry-run` owed (no change under the CLI's `src/` or `evals/kit/`); no `just mod`
  (no change to `hooks/` or `types/`).
