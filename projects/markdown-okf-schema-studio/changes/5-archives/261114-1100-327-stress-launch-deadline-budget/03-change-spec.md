# Change Specification: size the stress launch deadline to its rounds

Type: ci and test (harness, recipe, workflow and docs only; no change to `src/`). Automatable: the
owner asked for the fix inside the v1.9.1 release, and the Chief of Staff set the goal with no user
impact (02-answers.md). Priority P1: it must merge before the v1.9.1 version PR (CR-323, second
release).
Sources: `01-intent.md`, `02-answers.md`, `intake/request.md`, the CR-326 archive
(`.agents/changes/4-archives/261114-0947-326-flaky-real-window-integration-steps/`), the stress job
logs of heavy run 43581058313 (branch, `stress_repeat=60`) and of push run 43580745427 (`main`,
before CR-326, 20 rounds, green). Code read at `origin/main` `0941cc09` (version 1.9.0).

## Goal

1. The default stress run (the one a version push starts) finishes with a margin of at least a
   third under its launch deadline and under the stress job's `timeout-minutes`, on the current 17
   trusted scenarios and the one Restricted Mode scenario.
2. The launch deadline of a stress run follows its work (rounds times scenarios, from the measured
   per-scenario cost), with a ceiling under the job limit. No fixed 26-minute value is left.
3. No scenario leaves the stress list.
4. The REPEAT guidance (recipe comment, workflow input text, CONTRIBUTING.md, ci.guidelines.md)
   gives the real figures.

## Measurements (what the logs prove)

| Run | Scenarios | Rounds | Wall time of one round (trusted) | Trusted window | Whole stress step |
|-----|-----------|--------|----------------------------------|----------------|-------------------|
| 43580745427 (push `main`, green) | 15 + 1 | 20 | about 63 s | 21.0 min (09:29:53 to 09:50:52) | 22.1 min |
| 43581058313 (branch heavy, red) | 17 + 1 | 60 | 67.3 s (rounds 1 to 23, steady) | cut at 26.0 min, round 23 | 26.3 min |

- 67.3 s for 17 scenarios is 3.96 s of wall time per scenario run (the `PASS ... (N ms)` figures sum
  to about 58 s; the rest is the round's transitions). `save-position` is the slowest (about 11 s).
- Before the first round: about 30 s (compile and bundle about 7 s, VS Code download about 10 s,
  window start about 10 s). The job's steps before the stress step take about 30 s.
- The Restricted Mode window takes about 45 s for 20 rounds (about 2.2 s a round plus its start).
- Projection of the current default (20 rounds of 17): trusted about 22.9 min, stress step about
  24 min, job about 24.5 min. That is under the 26-minute deadline by 12 % and under the 30-minute
  job by 18 %: a slow runner can cut a healthy run, and a third of margin is out of reach at 20
  rounds without raising the job limit.

## Decision

Two parts, both needed:

- **A launch deadline computed from the plan** (the preferred way of 02-answers.md).
- **A default of 12 rounds** instead of 20, so the default run meets the margin with the job's
  30 minutes unchanged. CI rule 11 sets 30 minutes for the stress job and forbids raising a timeout
  to make a run pass; keeping the job limit and sizing the work to it follows that rule. 12 rounds
  of 18 scenarios still run each scenario 12 times on every push to `main`; longer loops stay
  available on a branch with a narrowed list (`stress_repeat`, `stress_scenarios`).

Figures with these values (from the measurements above):

| Default run | Expected | Limit | Margin |
|-------------|----------|-------|--------|
| Trusted window, 12 rounds of 17 | about 13.9 min (30 s start + 12 x 67.3 s) | computed deadline 22.4 min | 38 % |
| Restricted Mode window, 12 rounds of 1 | about 0.6 min | computed deadline 3.2 min | over 80 % |
| Whole job | about 16 min (30 s setup + 30 s build + both windows + upload) | `timeout-minutes: 30` | 47 % |

## Requirements

### R1. The deadline formula, in `test/shared/hangWatchdog.ts`

Add, next to `LAUNCH_DEADLINE_MS` (the one module for every threshold, CI rule 11):

- `STRESS_START_MS = 2 * 60_000`: the window start before the first round (measured about 30 s,
  bounded by the 90-second heartbeat anyway).
- `STRESS_SCENARIO_BUDGET_MS = 6_000`: the budget of one scenario run, 1.5 times the measured
  3.96 s (the factor gives the third of margin). The doc comment cites run 43581058313 and the
  67.3 s round of 17 scenarios.
- `STRESS_DEADLINE_CEILING_MS = 24 * 60_000`: the ceiling, under the 30-minute job less its setup,
  its build and the other window, so the watchdog (which dumps and names the step) always fires
  before the job is killed.
- `stressLaunchDeadlineMs(repeat: number, scenarios: number): number` returns
  `min(STRESS_DEADLINE_CEILING_MS, STRESS_START_MS + repeat * scenarios * STRESS_SCENARIO_BUDGET_MS)`.

Change `launchDeadlineMs(environment)`:

1. A set `STUDIO_LAUNCH_TIMEOUT_MS` still wins and is validated as today (the explicit escape hatch;
   `ci-toc-loop` keeps using it).
2. Else, when `STUDIO_REAL_INPUT_SCENARIO` is `stress`, it returns `stressLaunchDeadlineMs` of the
   stress plan: `repeat` from `hostStressPlan(environment, host)`, and `scenarios` the larger of the
   trusted and the untrusted scenario counts (a window with no plan counts 0). One value for both
   windows keeps the function host-free: the launcher (`launchWatchdog.ts`, `run-tests.ts`) and the
   in-host step budget (`stepBudgetMs` of the stress steps, which returns `launchDeadlineMs`) read
   the same environment and get the same number, as today. An invalid `STUDIO_STRESS_REPEAT` or
   scenario name throws the existing `stressPlan` error, so `run-tests.ts` (line 192) still fails
   before any VS Code starts.
3. Else `LAUNCH_DEADLINE_MS` (15 minutes), as today.

The `defaultRepeat` passed to `hostStressPlan` here is the same as the suites pass (10 today); the
recipe always sets `STUDIO_STRESS_REPEAT`, so it only matters for a direct `npm run
test:integration` with `STUDIO_REAL_INPUT_SCENARIO=stress` and no repeat.

`test/shared/hangWatchdog.ts` importing `test/shared/stressPlan.ts` is a same-folder import of
`test/`; check that `just check` (dependency-cruiser) accepts it, and keep `stressPlan.ts` free of
any import back.

### R2. The launcher says the deadline

When `run-tests.ts` starts a stress launch (trusted or Restricted Mode), it prints one line before
the window opens, for example:
`stress: launch deadline 1344000 ms (12 rounds x 17 scenarios, ceiling 1440000 ms)`, and adds
`; capped: narrow STUDIO_STRESS_SCENARIOS or lower the rounds` when the ceiling applied. With an
explicit `STUDIO_LAUNCH_TIMEOUT_MS` it prints the value and `(STUDIO_LAUNCH_TIMEOUT_MS)`. The line
is what the proof run reports against the stress duration.

### R3. The recipe and the workflow

- `justfile`, `ci-stress`: default `REPEAT=env("STUDIO_STRESS_REPEAT", "12")`; remove the
  `export STUDIO_LAUNCH_TIMEOUT_MS="${STUDIO_LAUNCH_TIMEOUT_MS:-1560000}"` line and its comment (an
  exported value would override the computed one). The REPEAT validation (1 to 100) stays.
- `.github/workflows/ci.yml`, job `stress`: `STUDIO_STRESS_REPEAT: ${{ inputs.stress_repeat || '12' }}`.
  `timeout-minutes: 30` is unchanged.

### R4. The guidance, with the real figures

Write the same figures everywhere, from R1:

- One scenario run costs about 4 s; the computed deadline is 2 min plus 6 s per scenario run, at
  most 24 min.
- The default 12 rounds of all 17 trusted scenarios take about 14 min.
- Up to about 220 scenario runs per window (rounds times scenarios) fit under the ceiling: 12
  rounds of all 17, 60 rounds of 3, 100 rounds of 2. Above that the deadline is capped and the run
  can be cut: narrow `stress_scenarios`.

Places:

- `justfile`: the comment above `ci-stress` (lines 331 to 337: "Above about 20 rounds ... 3.6 s ...
  26-minute launch deadline").
- `.github/workflows/ci.yml`: the `heavy` input description (line 10, "about 10 and 20 minutes":
  stress becomes about 16), the `stress_repeat` input description (line 26, "empty means 20. Above
  about 20"), and the comment above the `stress` job (line 251, "(20 rounds").
- `CONTRIBUTING.md` lines 478 to 479 ("`just ci-stress` raises it to 26"): the stress deadline is
  computed from the rounds and scenarios (formula and ceiling above), `ci-toc-loop` still sets 30.
- `.agents/guidelines/ci.guidelines.md`: rule 11 (line 52, the deadline sentence: add that a stress
  launch computes its own, at most 24 min) and rule 13 (lines 86 to 87, "narrow the scenarios above
  about 20 rounds": replace by the 220-scenario-run figure). The 30-minute job limit of rule 11 is
  unchanged.
- `test/shared/stressPlan.ts` doc comment: no change needed unless it gives a figure; check.

### R5. Tests (fail on the previous code, constitution section 3)

- `test/build/hangWatchdog.test.ts`, a new test:
  - `stressLaunchDeadlineMs(12, 17)` is `2 * 60_000 + 12 * 17 * 6_000` (1 344 000 ms) and
    `stressLaunchDeadlineMs(100, 17)` is the ceiling;
  - `launchDeadlineMs({ STUDIO_REAL_INPUT_SCENARIO: "stress", STUDIO_STRESS_REPEAT: "12" })` equals
    `stressLaunchDeadlineMs(12, STRESS_SCENARIOS_BY_HOST.trusted.length)`;
  - with `STUDIO_STRESS_SCENARIOS: "untrusted-read-only"` the count is 1;
  - an explicit `STUDIO_LAUNCH_TIMEOUT_MS` wins over the stress formula;
  - an invalid `STUDIO_STRESS_REPEAT` throws;
  - the margin guard: for the default plan (12 rounds, the current trusted count), measured cost
    `3_960` ms per scenario run plus 30 s start is at most two thirds of the computed deadline, and
    the ceiling is under `30 * 60_000` minus 3 minutes. This guard fails when the list grows past
    what the default fits, which is the moment to revisit the default (the CR-326 growth went
    unnoticed because nothing checked it).
  - The existing assertions of "CR 173: budgets and the launch deadline ..." keep their intent:
    `stepBudgetMs("real-input", { STUDIO_REAL_INPUT_SCENARIO: "stress", STUDIO_LAUNCH_TIMEOUT_MS: "5000" })`
    still returns 5 000.
- `test/build/test_workflows.py`:
  - `test_stress_dispatch_inputs_reach_the_stress_recipe_through_env`: expect `'12'` (the assertion's
    intent, "the input reaches the recipe with the default", is unchanged; say so in the commit);
  - `test_ci_stress_recipe_quotes_and_validates_repeat` (or a new test next to it, marked
    `@tests_req SwRS-MDOKFSTUDIO-CORE-076` like its neighbours): the recipe's default is `"12"` and
    the recipe does not set `STUDIO_LAUNCH_TIMEOUT_MS`.

### R6. Requirements

No SwRS text names the rounds or the deadline: SwRS-MDOKFSTUDIO-CORE-076 (the heavy jobs gate the
tag) is the requirement the workflow tests carry, and its behaviour is unchanged. No new SwRS, no
`requirements/tiers/log.md` entry (not substantive). Run `just requirements-update` and keep its
output if it changes anything.

## Out of scope

- Raising the stress job's `timeout-minutes` or the integration job's limits.
- Removing, reordering or speeding up a stress scenario (`save-position`'s 11 s included).
- Per-window deadlines (the trusted and the Restricted Mode windows share one computed value).
- The `toc-loop` job and its explicit 30-minute deadline.
- A release-notes entry: the change is CI-only; the v1.9.1 release CR decides whether its notes
  mention it.

## Files

- `test/shared/hangWatchdog.ts` (R1)
- `test/integration/run-tests.ts` (R2; possibly `test/shared/launchWatchdog.ts` if the line is
  printed there)
- `justfile` (R3, R4)
- `.github/workflows/ci.yml` (R3, R4)
- `CONTRIBUTING.md`, `.agents/guidelines/ci.guidelines.md` (R4)
- `test/build/hangWatchdog.test.ts`, `test/build/test_workflows.py` (R5)

## Commits (suggested)

1. `test: compute the stress launch deadline from its rounds and scenarios` (R1, R2, the
   hangWatchdog tests).
2. `ci: run 12 stress rounds by default and drop the fixed 26-minute deadline` (R3, the workflow
   tests, R4 guidance).

## Acceptance

- `just check` and `just preflight` pass.
- Proof run: `gh workflow run ci.yml --ref <branch> -f heavy=true` (default repeat), `integration`
  and `stress` green. Report in the PR and in STATUS: the stress step's duration, the trusted
  window's duration (first `stress:` line to `stress: 12 round(s) passed`), the computed deadline
  printed by R2, the margin under it, and the job's duration against its 30 minutes. Both margins
  are at least a third.
- Optional, not required for the release: one branch run with
  `-f stress_repeat=60 -f stress_scenarios=toc,palette,checkbox-toggle` (180 scenario runs) green
  under its printed deadline, to show the guidance figure holds.

## Open questions

None with a user impact. One trade-off decided here, for the Chief of Staff to overrule if wanted:
the default drops from 20 to 12 rounds (fewer repetitions on every push to `main`) rather than
raising the stress job from 30 to about 45 minutes, which CI rule 11 discourages.
