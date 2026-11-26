# Measure `just test` at rest, for the user's ceiling decision

Version 2, 2026-11-21 (over version 1 of the same day). From test-ceiling-Q1 to Q4, the
Destination line and the Chief of Staff's three decisions (02-answers.md), and CR-417's report
(intake/request.md).

## Goal

AGENTS.md says `just test` runs at most 30 s above its 18.5 s of 2026-11-14 (48.5 s) on the user's
Windows machine. CR-417 could only measure on a loaded machine (63.0 to 106.8 s at its head, 73.1
to 93.5 s on main). The user wants the numbers on an idle machine first, then decides between
raising the ceiling and moving or cutting the real-git tests (the writer, carry-ship and
release-tag tests). This CR first brings those numbers, through a study of the Chief of Staff,
and ends with that decision put to the user as test-ceiling-Q5. The user's answer to Q5 makes the
real change, which this CR then carries into a batch; its specification is written then.

## Decisions carried

- test-ceiling-Q1: measure `just test` on an idle machine first, at main's head, naming the
  slowest tests. The ceiling stays as it is until the user decides.
- test-ceiling-Q2: no PR. The measure is a Chief of Staff study subagent; its result is a file
  in the CR's `experiments/`. No worktree, no branch, no commit, no push, no gate owed.
- test-ceiling-Q3: idle means at most 10 % average CPU load over 30 s before each run; the study
  waits up to 30 minutes for it, then stops with no counted run, and returns the load samples
  and the process list naming what loads the machine.
- test-ceiling-Q4: the study runs after batch-30 closes, outside any batch.
- Destination: the CR does not join batch-30. Right after batch-30's close and the main
  checkout's fast-forward, with no batch running, the Chief of Staff starts one study subagent
  that measures and writes the report; the Chief of Staff then asks test-ceiling-Q5.
- test-ceiling-idle-processes (the Chief of Staff): the surface server's and the watchers' own
  `uv` and Python processes do not count in the idle check and the report names them; a `git`,
  `just` or `pytest` process they start counts.
- test-ceiling-clean-check (the Chief of Staff): the clean check is on tracked files only; the
  study never removes or moves an untracked file.
- test-ceiling-study-runs (the Chief of Staff): all five idle runs carry `--durations=30` and a
  junit file, the figures come from the median run; runs done before a 30-minute stop stay in
  the report, marked not counted.

## Who runs it, when, where

- **Who:** one study subagent of the Chief of Staff, started as [concepts](concepts.md), "The
  Chief of Staff's subagents", says: its brief names this CR's folder and `experiments/` as its
  place. It never implements: no commit, no push, no PR, no worktree, no branch.
- **When:** right after batch-30's `close` and the Chief of Staff's fast-forward of the main
  checkout, with no batch running on the project.
- **Where:** in the main checkout, `C:/Users/gaeta/Projets/chantier`, at main's head. Before
  anything else the study checks, read-only:
  - `git -C <main checkout> status --porcelain --untracked-files=no` prints nothing (tracked
    files clean; the untracked files there, such as `.agents/` and stray root files, are left as
    they are: the study never removes or moves one) and `git -C <main checkout> rev-parse --abbrev-ref HEAD` is `main`;
  - `git -C <main checkout> rev-parse HEAD` equals `git -C <main checkout> rev-parse origin/main`
    (the fast-forward done; no fetch by the study). It records the SHA (seven characters).
  If either fails, it runs nothing, writes the report with what it read, and stops.
- **Setup:** `uv sync --locked --project <main checkout>` once (AGENTS.md: the local code runs
  after a sync at the moments the cards name), then the runs below.

## What "idle" means and how the study checks it

The machine is idle for a run when all three hold, checked right before that run (the warm-up
included):

1. **No batch running.** `$CHANTIER status` (the project's) shows no running batch.
2. **No other test, build or git work.** The study lists the processes with their command line:
   `Get-CimInstance Win32_Process | Where-Object { $_.Name -match '^(just|uv|uvx|git|python|pythonw|pytest)(\.exe)?$' } | Select-Object ProcessId, ParentProcessId, Name, CommandLine`.
   No `just`, `pytest` (a Python whose command line runs pytest), `uv` or `git` process may run
   besides the study's own, with one exception: the own `uv` and Python processes of the surface
   server (`chantier board`, with its writer) and of the watchers (`chantier watch`), told by
   their command line, do not count; the report names them. A `git`, `just` or `pytest` process
   they start counts (a writer sync in progress, for instance), so the study waits and checks
   again.
3. **Low CPU load.** The average CPU load over the 30 s before the run is at most 10 %, read with
   a locale-independent query, six samples 5 s apart:
   `1..6 | % { (Get-CimInstance Win32_Processor | Measure-Object LoadPercentage -Average).Average; Start-Sleep 5 }`.
   The six values and their average are recorded with the run.

When a check fails, the study waits and checks again (a fresh 30 s reading each time, at most one
check a minute), up to 30 minutes from the first failed check before that run. Past 30 minutes
it stops: no further run, and no counted run (no median, no slowest-tests table, no Q5 numbers).
The report is still written, with every load sample taken, the last process list (naming what
loads the machine) and the runs done before, marked as not counted.

## What is measured

1. **Warm-up:** one `just test`, idle-checked, recorded but not counted.
2. **Five idle runs** of `just test` as it ships (`uv run --locked --group dev pytest -q -n auto
   --dist worksteal`), each with `--durations=30 --junitxml=<CR folder>/work/gates/junit-run-<N>.xml`,
   from the main checkout. For each: its wall time (pytest's own "passed in" line and the shell's
   measure, `Measure-Command`), its passed/failed/skipped counts and its load reading. Reported:
   each value, the median, the minimum and the maximum.
3. **The slowest tests**, from the median run: the 30 slowest test ids with their time (setup and
   call), as pytest prints them.
4. **The share of the real-git tests.** The files that run real git, as CR-417 named them, all
   under `skills/chantier/scripts/cli/tests/`:
   - writer: `test_writer_commands.py`, `test_writer_cycle.py`, `test_writer_edges.py`,
     `test_writer_lines.py` (with `writer_rig.py`);
   - carry-ship: `test_carry_ship.py`, `test_gate_carry.py`;
   - release-tag: `test_release_tag.py`, `test_board_prs_release.py`.
   The study confirms, by reading them, that each spawns `git` (or uses `writer_rig.py`), and lists
   separately any other test file that does (for instance `test_external_archive.py`,
   `test_cli_runs.py`), with what it runs. Reported, from the median run's junit summed per file
   and per group: the test count and the summed test time of each group, and their share of the
   whole suite's summed time.
5. **The suite without them:** three idle runs of `just test` with `--ignore=<file>` for each file
   of item 4's three groups; wall time each and the median. This gives the wall-time saving of
   the "move or cut" option directly, since summed times under `-n auto` do not add up to wall
   time.

Also recorded, once: the date, the CPU model and its logical processor count
(`Get-CimInstance Win32_Processor | Select-Object Name, NumberOfLogicalProcessors`), the worker
count `-n auto` used, the Python version `uv run` uses, and the total test count against CR-417's
1419 (the difference, if any, is what batch-30 added or removed).

After the last run: `git -C <main checkout> status --porcelain --untracked-files=no` prints
nothing again.

## Where the numbers go

- **The report:** one file, `experiments/01-just-test-idle.md` in the CR's folder (number-prefixed
  as concepts.md asks of a subagent's file; published with the surface). It holds every number
  above and the idle checks.
- **Raw outputs** (the junit XML files, the full pytest logs, the process lists) in the CR's
  `work/gates/` (or `*.log` files there), which the planning folder's `.gitignore` keeps off git.
  The study keeps no helper script; one it needs goes in `work/gates/` too, never in the
  repository.
- **The report's last lines** give, each on one line: the idle median of item 2 and the idle
  median without the real-git files of item 5. When the study stopped (no idle machine, or the
  checkout not clean or not at main's head), the last line says so and why instead.
- **Then the Chief of Staff** asks the user test-ceiling-Q5, as a numbered question with those
  two medians:
  1. raise the ceiling in AGENTS.md and CONTRIBUTING.md (line 278, which repeats it), to a value
     the numbers support (for instance the idle median plus a margin, both stated);
  2. keep it, and move or cut the real-git tests, with the saving item 5 measured and the
     coverage those tests hold, named per group;
  3. both.
  The answer is recorded in `02-answers.md`; the specification of the change it calls for is
  then written (a version 3 of this file), and that change goes into a batch like any CR.

## Out of scope

- In this study: any change to the repository. No change to the ceiling (AGENTS.md,
  CONTRIBUTING.md) or to the 18.5 s reference; no test cut, moved, marked, skipped or sped up; no
  change to the `test` recipe in `justfile`, to `pyproject.toml`'s pytest options or to the CLI's
  code; no new tool or script shipped for timing.
- A measure on Linux or macOS, or in CI: the ceiling is the user's Windows machine's.
- Runs on a loaded machine labelled "not idle": CR-417's loaded numbers already exist.
- Batch-30: the study neither joins it nor waits inside it.

## Evidence

- `experiments/01-just-test-idle.md` exists in the CR's folder and holds: main's SHA (seven
  characters) and the clean `git status --porcelain --untracked-files=no` of the main checkout
  (tracked files), read before the first run and
  after the last; the machine line; the warm-up run; five idle runs, each with its six load
  samples and their average (at most 10 %), the `status` read and the process list (the surface
  server's and watchers' processes named as not counted); median,
  minimum and maximum; the test count against 1419; the 30 slowest tests; the per-group count,
  summed time and share, and any real-git file found beyond the eight listed; three runs without
  the real-git files and their median; the last two lines with the two medians. Or, when it
  stopped, every load sample, the last process list and why it stopped.
- The junit files and pytest logs sit under the CR's `work/gates/`, not published.
- Nothing else is written: no file in the repository, no commit, no branch, no worktree. No
  `just check`, `just eval-dry-run`, `just scenario` or `just mod` is owed (no PR). No CI job
  changes; no host or default matrix applies (one host, the user's Windows machine; nothing
  configured).

## Open questions

None before the study. After it, the Chief of Staff asks test-ceiling-Q5 (above).
