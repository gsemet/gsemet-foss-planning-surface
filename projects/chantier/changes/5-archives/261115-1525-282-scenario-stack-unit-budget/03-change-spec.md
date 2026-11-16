# The scenario's stack unit fits its budget

Short name: `stack-budget`. No issue.

## Goal

The scenario's `stack` unit (forge `github`) must fit its time budget again. In batch-18 it ran
over its budget twice: 344.8 s and 375.6 s, against a budget of 320 s. `scenario/README.md`
still shows 313.9 s as its measured maximum. As things stand, every CR of the next batch can see
a `WARN stack (github) over its budget` line on its long gate. An Inspector or a Verifier then has
to read that line and decide whether it matters, and it is noise. Measure the unit again. Then
either bring it under its budget, or set its budget from the fresh measures. In both cases,
refresh the README's measured columns.

## Background (read-only facts the Driver starts from)

- `scenario/run_scenario.py`, `UNITS` (around line 73): `"stack": (320, ["github"],
  ["stack_batch", "base_from_pr", "stack_waiver", "ready_words", "forge_stack_cli"])`. A budget
  is one literal per unit. A unit over its budget only warns, and its row reads `over budget`.
  The run also prints `WARN <unit> (<forge>) over its budget: <s> s > <budget> s` (around line
  7471). A unit fails only past its hang timeout, `max(HANG_FLOOR_S, 4 * budget)` with
  `HANG_FLOOR_S = 600`, or on a failed check. The units run longest budget first (`queue_`,
  around line 7424).
- `scenario/README.md`, lines 36-59: the table of budgets and of the `--jobs 4` and `--jobs 8`
  times, measured on 2026-11-15 in commit 33fc800, on the user's loaded Windows 11 machine. Then
  the rule: "the budgets are these `--jobs 4` times plus about 25 percent, a loaded-machine
  figure". For `stack`: 259.3 s × 1.25 ≈ 324, so 320.
- Since 33fc800, sixteen commits have touched `run_scenario.py` (from 7b57731 to fa97e70: mode
  switch and `forge-stack unstack`, gate ordering and carry, base read from the PR, `--epoch`
  everywhere, waivers, asks, ship reading the forge). Several of them add checks to the stack
  unit's cases. That is the likely cause of the drift; the measures must confirm it.
- Earlier warnings of the same kind: 270-ship-reads-forge's `verify.md` (stack 517.6 s against
  320 at `--jobs 4` on a loaded machine), and 265-gate-rules (`gates`, 421.4 s against 330).
- The run writes, for each unit, `scenario/results/<stamp>-<pid>/stack-github.md`, with a timing
  table by case and section, and `stack-github.json` (seconds, commands, checks).

## What changes

### 1. Measure (evidence first, before any edit)

On the head of `main` the CR starts from, run the stack unit and read where its time goes:

- `uv run --locked python scenario/run_scenario.py --unit stack` at least three times, on its own
  (one unit, so the time is the unit's own time with no competition), and one full
  `just scenario` (`--jobs 4`, the default) run. Optionally, also one `--jobs 8` run for the
  README's second column.
- From each `stack-github.md`, record the per-case times (`stack_batch`, `base_from_pr`,
  `stack_waiver`, `ready_words`, `forge_stack_cli`) and the command counts. Note which cases grew
  since 33fc800, and whether the time is spent in commands started (git, the CLI, the fake `gh`)
  or in waits.
- Keep these figures in `work/` (a short table per run: date, machine, load, jobs, unit seconds,
  per-case seconds). They feed the PR's Test plan.

### 2. Decide, then act (the Driver's choice, on the measures)

The answers leave this choice to the agents. Pick one of the following, or combine them, and
justify the choice in the PR's Autonomous decisions with the measures.

- **Bring the unit under its budget.** Remove waste inside the stack unit's cases. For example: a
  sleep or a poll longer than needed, a world rebuilt where an existing one would serve, a check
  repeated across cases, a CLI or git call issued twice for one fact. Also allowed: moving a
  pure refusal on a prepared state to pytest (`skills/chantier/scripts/cli/tests/`), as
  `scenario/README.md` "Adding a case" asks. When a check leaves the scenario, its coverage
  bullet in the README moves from `(unit: stack)` to `(test: <file>::<test>)`, and
  `test_scenario_coverage.py` still passes. No check is dropped: every behaviour the unit proved
  is still proved, in the scenario or in pytest. A case may also move to another existing unit
  when that unit has room under its own budget, with that unit's coverage bullets updated.
- **Set the budget from fresh measures.** Edit the `stack` literal in `UNITS` to the fresh
  `--jobs 4` time plus about 25 percent, the README's own rule, rounded as the other budgets are.
  The new figure must come from the fresh runs, not from batch-18's two figures alone.

The unit keeps its forge (`github`) and its cases' behaviour. The hang timeout follows from the
budget through the existing formula; it is not edited separately.

### 3. Refresh `scenario/README.md`

- The table at lines 40-52: the `stack` row's budget and both measured columns, from the runs of
  step 1 (after the change of step 2). When the Driver ran a full `--jobs 4` (and `--jobs 8`) run,
  refresh every row, plus the wall time and the sum of the units, from that same run. A table
  with rows from different runs says so in its lead sentence.
- The lead sentence (line 36): the date, the machine and its load, as for the current figures.
- The paragraph at lines 54-59: kept true. If the figures change the longest unit, the wall
  time, or the 25 percent rule, say so. If the rule is applied, the text stays as it is.
- Any other budget whose literal changes with a moved case gets its row refreshed too.

### Files

- `scenario/run_scenario.py`: the `stack` literal in `UNITS`, and/or the stack unit's cases
  (`stack_batch`, `base_from_pr`, `stack_waiver`, `ready_words`, `forge_stack_cli` and their
  helpers).
- `scenario/README.md`: the measured table and its paragraphs; the coverage bullets of any check
  that moves.
- `skills/chantier/scripts/cli/tests/`: only if a refusal moves to pytest. `just test` stays
  within its AGENTS.md budget (at most 30 s above 18.5 s on the user's Windows machine).

No card, no CLI code under `skills/chantier/scripts/cli/` (apart from tests), no `hooks/`, no
`types/` and no CI file changes.

## Decisions carried from `02-answers.md`

1. The user planned this CR in the next parallel batch, before the release ("ok pour ces 12 en
   parallel", "oui planifie les 19"). The request's scope stands as written: measure again, then
   bring the unit under its budget or set the budget from fresh measures, and refresh the
   README's measured columns. No behaviour question was left open; the implementation detail
   (which way, which cases) is the agents'.

## Out of scope

- A new scenario unit, for example splitting `stack` in two. `scenario/README.md` says "Never a
  new unit without the user's word", and the answers did not give it. Moving cases into existing
  units is allowed (see step 2).
- Making an over-budget unit fail the run, or changing the hang formula, the `--jobs` default,
  the unit order, or the WARN line.
- Other units' budgets, unless a case moves into them. Their rows are only refreshed with the
  figures of the same run.
- The CI job `just scenario (ubuntu-latest)`. Its definition (`.github/workflows/ci.yml`) does
  not change.
- Lowering every budget for a quiet Linux machine (README lines 57-59 leave that open).

## Environment of the long gate (for reading the evidence)

The CI job `just scenario (ubuntu-latest)` runs `just scenario` on a GitHub-hosted Ubuntu runner
with `setup-uv` and `setup-just`, a fresh uv cache, and a global git identity set by the job. It
has no other load, and a process starts faster there than on Windows. The README's budgets are
loaded-Windows figures, so the Linux job is not where an overrun shows first. CI's time for the
stack unit, read from the job's log table, is extra evidence and is not the basis of the budget.
The CR changes no CI job.

## Evidence

- `work/`: the measures of step 1, before the change, and the same runs after it: at least three
  `--unit stack` runs and one full `just scenario` run on the head of the PR, every check
  passing, the stack row `ok` (not `over budget`), and no `WARN stack (github)` line.
- When cases were trimmed or moved: the stack unit's check count before and after, each missing
  check accounted for (moved to pytest or to another unit, named), and `test_scenario_coverage.py`
  passing.
- `just check` passes (Linux, macOS, Windows in CI). `just test` stays within its budget if
  pytest gained a test.
- The long gate: `just scenario (ubuntu-latest)` green at the PR's head (the CR changes the
  scenario). The batch's Windows run (`chantier gate`, on the CR on top of the stack) shows the
  stack unit within its budget.
- The PR's Test plan quotes the before and after per-case times and the README's new row.

## Open questions for the user

None. The answers leave no behaviour point open. Splitting the unit into a new one would need
the user's word, and this specification keeps it out of scope.
