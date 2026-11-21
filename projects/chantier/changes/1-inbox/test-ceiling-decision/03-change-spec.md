# Measure `just test` at rest, for the user's ceiling decision

Version 1, 2026-11-21. From test-ceiling-Q1 (02-answers.md) and CR-417's report (intake/request.md).

## Goal

AGENTS.md says `just test` runs at most 30 s above its 18.5 s of 2026-11-14 (48.5 s) on the user's
Windows machine. CR-417 could only measure on a loaded machine (63.0 to 106.8 s). The user wants
the numbers on an idle machine first, then decides between raising the ceiling and moving or
cutting the real-git tests (the writer, carry-ship and release-tag tests). This CR brings those
numbers and ends with that decision, put to the user. It is a measurement: its deliverable is a
report, not a code change.

## Decisions carried

- test-ceiling-Q1: measure `just test` on an idle machine first, at main's head, naming the
  slowest tests. The ceiling stays as it is until the user decides.

## What "idle" means and how the Driver checks it

The machine is idle for a run when both hold, checked right before that run:

1. **No other chantier work on the machine.** No other Driver, Coder, Verifier, Debugger or
   Conflict-resolver of batch-30 (or of any other batch on this machine) is working, and no
   `just scenario`, `chantier gate`, `just check` or `just test` other than this run is going. The
   Driver reads `$CHANTIER status` (no other CR of the batch in a live round: each is handed back,
   parked, held or done) and lists the processes
   (`Get-Process python, pytest, uv, git, just -ErrorAction SilentlyContinue`): only the surface
   server (`chantier board`) and the steering session's own processes may remain.
2. **Low CPU load.** The average CPU load over 30 s before the run is at most 10 %
   (test-ceiling-Q3), read with a locale-independent query, six samples 5 s apart:
   `1..6 | % { (Get-CimInstance Win32_Processor | Measure-Object LoadPercentage -Average).Average; Start-Sleep 5 }`.
   The six values and their average are recorded with the run.

A run whose check fails is not counted as idle: the Driver waits and checks again (a watch, not
a sleep loop on its turn). How long it waits, and what it records if the machine never goes idle,
is test-ceiling-Q3.

### Running inside batch-30

Batch-30 itself uses the machine (stack mode, 4 slots). This CR therefore measures **last**: its
Driver starts its measurement only once every other CR of batch-30 is handed back (ready, parked,
held or dropped) and before the stack's local `just scenario` run (`chantier gate`) on the top CR,
so that no other Driver, round or gate works during the runs. How the Foreman orders that is
test-ceiling-Q4. While it waits, the Driver holds no slot it does not need.

## What is measured

All runs happen at **main's head** at the time of measuring, in a checkout made for it (a
detached worktree of `origin/main`, removed after; never the main checkout, which batch-30 and the
user's session read live). The Driver records the SHA (seven characters). If batch-30 has merged
CRs into main by then, the test count says so.

Before the first run: `uv sync --locked --project <checkout>` (the cache warm), then one warm-up
`just test`, recorded but not counted.

1. **Five idle runs** of `just test` (the recipe as it ships: `uv run --locked --group dev pytest
   -q -n auto --dist worksteal`), each with its wall time (pytest's own "passed in" line and the
   shell's measure, e.g. `Measure-Command`), its pass/fail count and its load reading. Reported:
   each value, the median, the minimum and the maximum.
2. **The slowest tests by duration**, from one of the idle runs with
   `just test --durations=30 --junitxml=<scratch>/junit.xml`: the 30 slowest test ids with their
   time (setup and call), as pytest prints them.
3. **The share of the real-git tests.** The files that run real git, as CR-417 named them:
   - writer: `test_writer_commands.py`, `test_writer_cycle.py`, `test_writer_edges.py`,
     `test_writer_lines.py` (with `writer_rig.py`);
   - carry-ship: `test_carry_ship.py`, `test_gate_carry.py`;
   - release-tag: `test_release_tag.py`, `test_board_prs_release.py`;
   all under `skills/chantier/scripts/cli/tests/`. The Driver confirms each one spawns `git` (or
   uses `writer_rig.py`), and lists separately any other file it finds that does (for instance
   `test_external_archive.py`, `test_cli_runs.py`), with what it runs. Reported, from the junit
   report summed per file and per group: the test count and the summed test time of each group,
   and their share of the whole suite's summed time.
4. **The suite without them**: three idle runs of `just test` with `--ignore=` on each file of
   item 3's three groups, wall time each and median. This gives the wall-time saving of the
   "move or cut" option directly, since summed times under `-n auto` do not add up to wall time.

Also recorded, once: the date, the CPU model and its logical processor count
(`Get-CimInstance Win32_Processor | Select Name, NumberOfLogicalProcessors`), the worker count
`-n auto` used, the Python version `uv run` uses, and the total test count (1419 at CR-417).

## Where the numbers go

- The CR's folder: `evidence/just-test-idle.md` (published with the surface), with every number
  above; raw outputs (the junit XML, the full pytest logs) in `work/gates/` or `*.log` files, which
  stay off git.
- The PR: its body carries the same tables (runs, slowest tests, real-git share, the suite without
  them). What the PR's diff holds is test-ceiling-Q2.
- The report ends with **the decision for the user**, written from the numbers, never decided:
  - raise the ceiling in AGENTS.md (and CONTRIBUTING.md line 278, which repeats it), to a value
    the numbers support (for instance the idle median plus a margin, both stated);
  - keep it, and move or cut the real-git tests in a further CR, with the saving item 4 measured
    and the coverage those tests hold, named per group;
  - or both.
  The ready line quotes the idle median and the median without the real-git tests, so the Chief
  of Staff can put the choice to the user as a numbered question.

## Out of scope

- Any change to the ceiling (AGENTS.md, CONTRIBUTING.md) or to the 18.5 s reference.
- Any test cut, moved, marked, skipped or sped up; any change to the `test` recipe in `justfile`,
  to `pyproject.toml`'s pytest options or to the CLI's code.
- A measure on Linux or macOS, or in CI: the ceiling is the user's Windows machine's.
- A new tool or script shipped in the repository for timing (a throwaway script in the session's
  scratch folder is fine and is not committed).

## Evidence

- `evidence/just-test-idle.md` exists in the CR's folder and holds: main's SHA; the machine line;
  the warm-up run; five idle runs, each with its six load samples and their average (at most the
  threshold) and the "no other work" check (status and process list read); median, minimum and
  maximum; the 30 slowest tests; the per-group count, summed time and share; three runs without
  the real-git files and their median; the decision for the user.
- The PR body carries the same tables, and its Known gaps name any run that was not idle
  (test-ceiling-Q3) and any real-git file found beyond the eight listed.
- `git diff origin/main` of the PR touches no file under `skills/`, no `justfile`, no
  `pyproject.toml`, no `AGENTS.md`, no `CONTRIBUTING.md`.
- `just check` passes at the rebased head before the first push (AGENTS.md). The change touches no
  CLI `src/`, no eval kit, no cards and no scenario: no `just eval-dry-run` and no long gate are
  owed. No CI job changes; no host or default matrix applies (one host, the user's Windows
  machine; nothing configured).

## Open questions

- **test-ceiling-Q2: what does the PR's diff hold?** A PR needs a commit.
  1. (recommended) One new file, `docs/test-timings.md`: the idle numbers, the date and main's
     SHA, a durable reference the ceiling's next wording can cite.
  2. No PR: the numbers live in the CR's folder and the ready line only; the CR is handed back
     with no PR.
  3. An empty commit, the numbers in the PR body only.
- **test-ceiling-Q3: the idle threshold, and a machine that never goes idle.**
  1. (recommended) At most 10 % average load over 30 s before each run; the Driver waits up to
     30 minutes for it; past that, it records the runs anyway, each with its load, labels them
     "not idle" in the report and the PR's Known gaps, and hands back.
  2. Same threshold, but past 30 minutes the Driver hands back `blocked` with no numbers, and the
     user frees the machine.
  3. A looser threshold (at most 20 %), no wait limit.
- **test-ceiling-Q4: how the CR measures last in batch-30.**
  1. (recommended) It joins batch-30 with `order add`, and the Foreman starts its Driver only when
     every other CR is handed back, before the stack's local `chantier gate`; no `depends.json`.
  2. `depends.json` on every other CR of batch-30, so the record holds the order.
  3. It leaves batch-30 and runs alone after the batch closes, in a batch of its own or in direct
     mode.
