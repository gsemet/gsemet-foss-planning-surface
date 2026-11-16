# Investigation 01: where the stack unit's time goes

Read only. Head: origin/main 9d4136c (worktree batch-18-CR-282, clean). No project file edited;
`scenario/results/` is git-ignored (`git status` stayed clean). Machine: user's Windows 11, Ryzen 7
7800X3D, 16 logical cores, shared with other agents. Load = `Win32_Processor.LoadPercentage`, one
sample just before each run. Command: `uv run --locked python scenario/run_scenario.py --unit stack`,
one run at a time, one unit alone (no competition from other units).

## 1. The three runs (before any edit)

| run | date, start | CPU load before | results folder (under `scenario/results/` of the worktree) | unit s | commands | checks | status |
| --- | --- | ---: | --- | ---: | ---: | --- | --- |
| 1 | 2026-11-15 14:58 | 37 % | `20261115-145822-10844` | 452.9 | 755 | 129/129 | over budget |
| 2 | 2026-11-15 15:06 | 100 % | `20261115-150604-28580` | 421.5 | 650 | 129/129 | over budget |
| 3 | 2026-11-15 15:13 | 44 % | `20261115-151310-29880` | 318.7 | 652 | 129/129 | ok (320) |

Per-case seconds (commands), from each `stack-github.md` "Timing" table:

| case | run 1 | run 2 | run 3 | checks |
| --- | --- | --- | --- | ---: |
| build | 0.5 (8) | 1.2 (8) | 0.5 (8) | 0 |
| stack_batch | 59.8 (256) | 85.4 (151) | 58.2 (153) | 20 |
| base_from_pr | 47.0 (117) | 64.5 (117) | 40.6 (117) | 13 |
| stack_waiver | 28.6 (69) | 35.1 (69) | 21.8 (69) | 10 |
| ready_words | 129.2 (234) | 124.5 (234) | 90.1 (234) | 38 |
| forge_stack_cli | 71.4 (69) | 47.3 (69) | 43.3 (69) | 48 |
| total of the rows | 336.5 (753) | 358.0 (648) | 254.5 (650) | 129 |
| whole unit | 452.4 (755) | 420.9 (650) | 318.4 (652) | |
| not in any row | 115.9 | 62.9 | 63.9 | |

(The printed unit time, 452.9 / 421.5 / 318.7, is a little above the `.md` whole-unit row.) The
spread is 1.4x on the same code: load decides whether the unit is under 320 s. The load sample
before a run is one point, not the run's average (run 1 at 37 % was the slowest), so it is only
a hint. Run 3 is 0.7 s under budget: no margin.

## 2. Which cases grew since 33fc800

The old stack unit (33fc800) was three cases: `stack_batch`, `ready_words`, `forge_stack_cli`
(259.3 s at `--jobs 4`). Now five: 3b18a56 (waiver) added `stack_waiver` and 52eeccd (base read
from the PR) added `base_from_pr`. Function sizes, lines / `check(` calls (`ast`):

| case | 33fc800 | 9d4136c |
| --- | --- | --- |
| stack_batch | 165 / 20 | 169 / 20 |
| base_from_pr | absent | 125 / 13 |
| stack_waiver | absent | 81 / 10 |
| ready_words | 181 / 22 | 231 / 25 |
| forge_stack_cli | 448 / 52 | 481 / 55 |

The two new cases cost 40.6 + 21.8 = 62.4 s in run 3, which is the whole drift (318 against
259). The three old cases grew by 0, 3 and 3 checks. So the drift is two new cases, not slow
growth; and the load spread (318 to 453) is larger than any trim of one case.

## 3. Commands or waits

- No `time.sleep` in the five cases (4085-4255, 4256-4382, 4383-4863, 5823-5905, 5906-6136).
  The sleeps at 2879-3363 and 3912 belong to the `gates` unit's cases. So the time is not waits
  in the cases; it is processes started.
- Transcript of run 3: 414 `chantier` CLI calls (`python -m chantier`, one cold Python each,
  0.14 s for `--help` measured here, about 58 s of start-up before any work), 8 fake `gh` calls
  shown, the rest git, the fake `gh` (a `.cmd` shim that starts Python) and `compileall` gates.
  652 processes over 254.5 s of rows = 0.39 s per process; `git --version` is 0.04 s, so the
  CLI's own work and its internal git children are most of it.
- CLI verbs: `ship` 46, `forge-stack` 41, `gate` 36, `file` 30, `triage` 30, `take` 30, `order`
  29, `agents` 27, `handoff` 24, `stack` 24, `handback` 21, `round` 19, `verdict` 19, `open` 12.
  About 30 CRs are created over the unit, in 11 worlds (`w.reset()` sweeps `4-batch`, then the
  next `open`).
- CLI calls per section (run 3): stack_batch 93, base_from_pr 69, stack_waiver 41, ready_words
  142, forge_stack_cli 69 (27 of them refusals, 48 checks).

### The part outside every row (63 to 116 s, 20 to 25 % of the unit)

`run_unit` (7265-7312) times `elapsed` over everything, but the case rows stop before
`write_scope` and before `remove_tree` (7223-7250), which runs in `finally`. `remove_tree`'s
`retry` is the `onexc` handler: `shutil.rmtree` calls it for each entry it fails to delete, and
`retry` starts with `time.sleep(0.5)` before its first try (line 7232). On Windows git's object
files are read-only, so every loose object of the repos (`proj`, `origin.git`, the worktrees)
fails once and costs at least 0.5 s. Probe made here (6 commits): 4 handler calls = 2.0 s exactly.
The gap of 62.9 to 115.9 s equals 126 to 232 read-only entries at 0.5 s. This is the largest
single waste, a fixed sleep and not work, and it counts against the budget (the budget compares
`elapsed`). Not measured directly (the workspace is removed); the evidence plan measures it.

### Run 1's extra 100 commands

Run 1 has 755 commands and `stack_batch` 256 against 151-153. Cause: random searches with one
process per try, in `stack_batch`:
- 4179-4182: `for n in range(1, 50)` amends the commit until the head's first 7 hex characters
  hold a letter (all digits has probability (10/16)^7 = 3.7 %, so rare).
- 4199-4200: `for i in range(2000)` of `git commit-tree` until a commit whose first 7 characters
  are all digits (3.7 % per try, 27 processes expected, up to 2000). Run 1 hit about 100.
  Random per run, since the commit time varies the SHA.

## 4. Candidate waste (lines in `scenario/run_scenario.py` at 9d4136c)

1. `remove_tree` retry (7223-7250, sleep at 7232): sleeps before the first try, once per read-only
   file. Fix: clear the read-only bit and retry at once, sleep only on a second failure. Expected
   60 to 115 s of the unit's seconds, Windows only, and every unit with a git workspace pays it
   (check the other units' gap too; this was not measured).
2. The digits search (4199-4200): make the dangling commit deterministic (a fixed
   `GIT_COMMITTER_DATE` and a counter, or compute the commit SHA in Python with `hashlib.sha1`),
   zero random processes. About 27 git processes on average, 100+ on a bad draw.
3. The amend loop (4179-4182): same idea with a fixed date. Small (0 to a few processes).
4. `forge_stack_cli` (4383-4863): 27 of 69 CLI calls are refusals (`forge-stack create/rebuild/
   show` on a prepared state; `record()` writes the batch by hand, 4396-4410). Refusals that fire
   before any `gh` call can move to pytest, built like `test_mode_switch.py` (the only test file
   that mentions forge-stack). 43 to 71 s, 0.6 to 1 s per command, the slowest per command (the
   fake `gh` starts a second Python). Needs a per-check read to choose which; each moved check
   changes its README bullet to `(test: file::test)`.
5. `ready_words` (5906-6136): the biggest case (90 to 129 s, 142 CLI calls, 38 checks); five
   `w.reset()` (5928, 6037, 6066, 6106, 6144), so five worlds. A check on a freshly prepared
   state that repeats `file`+`triage`+`open` for one word check may share a world. Needs a read
   of its 38 checks; this note does not claim duplicates there.
6. Repeated worlds across the unit: `file`+`triage` x30, `open` x12; `base_from_pr` resets at
   4272, 4325, 4343 (three worlds in 125 lines), `stack_waiver` at 5825. Merge two worlds where
   the second only re-reads.
7. Move a whole case: `base_from_pr` (40 s) or `stack_waiver` (22 s) to a unit with room. At
   33fc800 (`--jobs 4`) direct 100.0 of 125, qa-driver 90.4 of 115, gitlab 61.1 of 95,
   series-deps 154.5 of 190: about 25 to 34 s of room each, so only `stack_waiver` fits, and only
   with fresh measures of that unit (not done). Their coverage bullets move too.
8. The fallback: set the budget by the README rule on a fresh `--jobs 4` figure. No `--jobs 4` run
   was done here, as instructed.

Not found: no `sleep` in the five cases, no obvious CLI call issued twice for one fact (the 129
checks were not read one by one; items 4 to 6 need that).

## 5. Questions only the user can answer

None. (Splitting the unit is out of scope by the specification; case moves stay inside existing units.)

## 6. Evidence plan

Kind of change: test infrastructure (`scenario/run_scenario.py` teardown and helpers,
`scenario/README.md`, maybe pytest), no UI. Rules: `just check` green; the long gate is the
pipeline's `just scenario (ubuntu-latest)`; the Windows run is `chantier gate` on the CR on top.

- Before and after, same technique: `uv run --locked python scenario/run_scenario.py --unit stack`
  three times each, noting date, CPU load, unit seconds, the per-case table and the "not in any
  row" gap (whole unit minus total of the rows), as in section 1. Sample the load before each run
  and say that one comparison alone proves little (1.4x spread on the same code).
- Isolate the teardown: time `remove_tree` itself (a scratchpad probe on a workspace made with
  `--keep`, as in section 3), count its handler calls, and show the seconds before and after the
  fix; two numbers in the PR.
- Per-case effect: the Timing table of `stack-github.md` before and after. For any check that
  moves, the unit's check count before (129) and after, each missing check named with its pytest
  `file::test` or its other unit, and `test_scenario_coverage.py` green.
- One full `just scenario` (`--jobs 4`) at the head after the change for the README rows and the
  claim "no `WARN stack (github)` line"; the Driver decides.
- The README's refreshed table, with its lead sentence (date, machine, load, one run), is itself
  evidence.
- Cannot be shown: Linux CI timing (read the CI job's log table as extra only); the teardown sleep
  is Windows-only, so Linux CI shows no gain from item 1; the load on a shared machine is not
  controlled, hence three runs and a load sample.
