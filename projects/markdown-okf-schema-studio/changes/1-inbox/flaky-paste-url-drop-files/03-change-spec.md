# Change Specification: flaky real-window paste-url and drop-files tests

No tracker issue (verbal request, batch-06 retro, 2026-11-20).

## Goal

The real VS Code window step `paste-url` failed on CI without a related change (three runs, four
attempts), and `drop-files` belongs to the same family. The owner wants the flake filed, its cause
found, and both scenarios added to the default stress scenarios of `just ci-stress`, so a race
in either one shows up on every push to `main`. A flake is a bug, fixed at its cause and proved by
repetition (CI rule 12 of `.agents/guidelines/ci.guidelines.md`).

All line numbers below are at `origin/main` 5a84db8b (version 1.11.0).

## Decisions carried from `02-answers.md`

1. pu-Q1, the rule from flaky-realinput-t45: if the cause is not found, the CR ships what it
   proved plus traces in the CI log that catch the next failure. No automatic retry, no
   quarantine.
2. Both scenarios join the default `just ci-stress` scenarios, as the request says, within the
   rules of `.agents/guidelines/ci.guidelines.md`. How they fit in the stress time budget is open
   (Open question 1).

## What the failure logs prove

| Run, attempt | Head | Contains e05f0b51? | Result |
| --- | --- | --- | --- |
| 44647675614, 1 | 768570c (CR-350 branch) | no | `STEP failed: paste-url (12560 ms): Timed out waiting for the workspace to remember edit mode off.` |
| 44647675614, 2 | 768570c | no | same, 12422 ms |
| 44690391950, 2 | 412ca69 (CR-350 branch) | no | same, 12643 ms |
| 44715893690, 1 | 06eda91 (CR-424 branch, 2026-11-20 10:57) | no | same, 13194 ms, stack `pasteUrl.test.js:175` |

Saved logs: `5-archives/261120-0859-350-ci-gallery-on-dispatch/work/ci-44647675614.log` and
`work/diagnosis.md` (the CR-350 debugger's analysis), and
`5-archives/261120-1146-424-external-pr-404-list-item-edit/work/ci-44715893690.log`, in the
planning surface. `gh run view <id> --log-failed` gives them again while GitHub keeps them.

- Every failure is the same wait: `waitFor("the workspace to remember edit mode off",
  () => storedEditModeForTests() !== true)`, at the end of `test/integration/pasteUrl.test.ts`.
  Each attempt took the healthy 2.4 to 2.9 s of the step plus the 10 s default of `waitFor`
  (`test/integration/realInput/harness.ts:51-68`): everything before that wait passed.
- Commit e05f0b51 (CR-425, "test: stop three real-window tests failing at random", on `main`
  since 2026-11-20 12:45) removed that wait from `pasteUrl.test.ts`, `dropFiles.test.ts` and
  `findInPreview.test.ts`. All four failing heads predate it (`git merge-base --is-ancestor
  e05f0b51 <head>` is false for each).
- Since e05f0b51, about 20 heavy runs of `integration` (pushes to `main` and dispatches, from
  44731534776 to 44882733071) never failed at `paste-url` or `drop-files`; their failures were
  other steps (`empty-blocks`, `open-at-line`) or visual captures. The on-demand stress run
  44719877177 (`stress_repeat=30`, `paste-url,drop-files,checkbox-toggle`, at the CR-425 head) was
  green: 90 scenario runs in 187 s, about 2.1 s each.
- `drop-files` never failed in any saved log or run found. It joins this CR because it carried the
  same wait before e05f0b51, and because it now runs only once per integration run.

What the logs do not prove: why the host kept `true` for 10 s. The CR-350 diagnosis names the
likely reason, not proved for lack of a host trace: the page's `previewEditModeChanged` named an
older render (the toggle was clicked right after the autosave, before the render it starts reached
the page) and was dropped by `manager.matchesCurrent` (`src/session/previewManager.ts`) through
`reportStaleEdit` (`src/session/pageMessages.ts:241`), as SwRS-MDOKFSTUDIO-LIFE-169 specifies ("A
stale message stores nothing"). That drop is by design and no product code reads the stored value
any more (since b84b0585), so it is not a product bug, and no test waits for it now.

## Causes the CR proves or rules out

- **C1, the observed failure (proved by the logs, fixed by e05f0b51):** the obsolete stored-mode
  wait. The Driver confirms it at the head under test: `git grep -n storedEditModeForTests --
  test/integration/pasteUrl.test.ts test/integration/dropFiles.test.ts` finds nothing, and the
  repetition below stays green. The repetition, not this CR's code, is what closes C1.
- **C2, still in the code (never observed, to rule out by repetition):** waits on time instead of a
  state the product reports, which CI rule 12 forbids:
  - `pasteUrl.test.ts:104-115`: the loop that clicks the paragraph until the block text box stays
    open, with a fixed 700 ms pause (line 111) between two checks;
  - `dropFiles.test.ts:107`: a fixed 400 ms pause between the `dragOver` and the count of the drop
    marker (`.sphinx-preview-insert-point--drop`), which a slow runner can miss.
  If a proof run below fails at one of them, the Driver fixes it in this CR with a readiness signal
  the page reports (CI rule 12). Whether to replace them before any failure is Open question 2.
- **C3, the suite order (to rule out by the default stress):** in `integration` both steps run
  right after `grid-card-editor-blur` (`test/integration/trusted-suite.ts:295-299`); in the stress
  window they run after `palette` and `checkbox-toggle`, then again after the first scenario of the
  next round. A failure that shows only in one order points at a state an earlier step leaves (open
  tabs, edit mode, focus); the trace below records it.

## What changes

### A. Both scenarios in the default stress plan

1. `test/shared/stressPlan.ts`: move `"paste-url"` and `"drop-files"` from
   `STRESS_ON_DEMAND_SCENARIOS` to the end of `STRESS_SCENARIOS_BY_HOST.trusted`, after
   `"checkbox-toggle"`, with a comment naming the runs above (the paste-url failures were the
   stored-mode wait removed by e05f0b51; drop-files carried the same wait). Then either remove
   `STRESS_ON_DEMAND_SCENARIOS` (empty, so `just check`'s unused-export check flags it) and its uses
   in `hostStressPlan`, or keep it empty if another reader remains; the Driver checks with `just
   check`. Rewrite the docblock of `STRESS_ON_DEMAND_SCENARIOS` or drop it with the constant.
2. `test/integration/realInput/run.ts:103-106`: drop the "on demand only" comment; the table keys
   stay in the same order, and the start assertion (`run.ts:112-114`) then compares with the
   trusted list only if the on-demand list is removed.
3. `test/build/stressPlan.test.ts:61-69`: the CR-425 test ("never in the default plan") becomes a
   test that both names are in the default trusted plan (`hostStressPlan({}, "trusted")`) and still
   run alone when named (`STUDIO_STRESS_SCENARIOS=paste-url,drop-files`), and never in the
   untrusted window. This changes an assertion's intent: say so in the commit message and the PR
   body (constitution, section 3: the owner asked for it).
4. The time budget, as the owner answers Open question 1. The facts the Driver needs:
   - The default stress launch deadline is `min(24 min, 2 min + rounds x scenarios x 6 s)`
     (`stressLaunchDeadlineMs`, `test/shared/hangWatchdog.ts:78-80`); the trusted window is the
     larger one, so `scenarios` is its count: 19 today, 21 after A.1.
   - `test/build/hangWatchdog.test.ts:323-328` ("the default stress plan keeps a third of margin")
     asserts `30 s + rounds x scenarios x 3.96 s <= 2/3 x deadline`, at `STUDIO_STRESS_REPEAT: "12"`.
     At 12 rounds x 21 scenarios: 1,027,920 ms against 960,000 ms: `just check` fails. At 11
     rounds: 944,760 ms against 960,000 ms: it passes. At 10 rounds: 861,600 ms against 920,000
     ms: it passes.
   - Measured on CI (trusted window, 12 rounds x 19 scenarios): 833 s (run 44882733071), 836 s
     (44764608171), 923 s (44777704200), 928 s (44830737763), that is 3.65 to 4.07 s per scenario
     run; `paste-url` and `drop-files` take about 2.1 s each (run 44719877177). CR-425 measured
     4.06 s for 19 names, about 3.87 s for 21.
   - Whichever option, the default stays at or under "about 220 scenario runs per window" (CI
     rule 13, justfile comment at lines 361-363) or the Driver updates those texts with the new
     numbers, and the margin guard is never weakened to make it pass (CI rule 11: never raise a
     timeout to make a run pass).
   - Option (a), 11 default rounds (231 runs): change `"12"` to `"11"` in the `ci-stress` default
     (`justfile:364`), `${{ inputs.stress_repeat || '12' }}` in `.github/workflows/ci.yml:342`,
     the `stress_repeat` input description (`ci.yml:34`, "empty means 12") and the `heavy` input
     description if its minutes change (`ci.yml:10`), the two assertions of
     `test/build/test_workflows.py:671` and `:687`, the default-plan literals of
     `test/build/hangWatchdog.test.ts:309-317` and `:324` (better: one exported constant for the
     default rounds, read by the tests, so they cannot drift), and the justfile comment (lines
     361-363: "The default 11 rounds of all 21 trusted scenarios take about N min", with N from
     the first CI run). Option (b), 10 rounds: the same places with `10`. Option (c), keep 12
     rounds: only by a change the owner approves to the margin guard or to the 24-minute ceiling
     (`STRESS_DEADLINE_CEILING_MS`, CI rule 11's "at most 24 min", and the `<= 27 min` assertion
     of `hangWatchdog.test.ts:327`), which CI rule 11 forbids as written.
5. `requirements/tiers/log.md`: a dated entry (the stress plan's default list and, if changed, its
   default rounds; the C1 evidence in one sentence). No SwRS describes the stress list or its
   rounds (`git grep -n -i "stress" -- requirements/tiers/swrs` names only `CORE-076`, which is
   about which jobs run, not their scenarios); the Driver runs that grep again and changes nothing
   else. No behaviour of the extension changes, so no SwRS changes unless Open question 3 adds a
   product log.

### B. Traces in the CI log (decision 1, and CI rule 12: failure messages carry diagnostics)

Each scenario writes one trace that explains its next failure, in `integration` and in `stress`,
without changing what it checks:

1. A small pure formatter in `test/shared/` (for example `realWindowTrace.ts`, exported
   `formatScenarioTrace(name, snapshot)`), so a node unit test in `test/build/` checks its output
   without a VS Code window. It writes one line, `<scenario> failure trace: <JSON>`, with the host
   state from `getActivePreviewForTests()` (`phase`, `requestId`, `documentVersion`,
   `webviewReady`, `deferredWorkPending`, `blockEditOpen`, `pageEditorOpen`, `contentPatches`,
   `htmlAssignments`, `panelActive`), the source document's `version` and text, the page's edit
   mode (`data-sphinx-preview-edit-mode` of the current frame's `html`) and whether a current frame
   was found, the open editor tabs (`vscode.window.tabGroups`, label and input type per group), the
   step's last progress marker, and the scenario's `failures` list so far.
2. `test/integration/pasteUrl.test.ts` and `test/integration/dropFiles.test.ts`: a `catch` around
   the scenario body (before the existing `finally`, which stays) that collects the snapshot,
   prints the trace with `console.error`, and rethrows the original error unchanged. Collecting the
   snapshot is best effort and bounded (each Playwright call through the harness's bounded frame
   lookup, `findCurrentFrame`, `harness.ts`); an error while collecting is printed inside the trace
   and never replaces the scenario's error.
3. Progress markers (`markProgress`, `test/shared/hangWatchdog.ts:159`) at each phase of both
   scenarios (preview ready, edit mode on, text box open, each paste or drop, autosave, edit mode
   off), so a `STEP TIMEOUT` names the phase and the trace carries it.
4. No retry, no raised timeout, no change to any existing wait's duration or assertion.

### C. Proof by repetition

See Evidence. If a proof run fails at `paste-url` or `drop-files`, the Driver reads the trace,
writes what it proves in the CR folder (`work/`), and fixes the cause in this CR when the trace
names it (C2: a readiness signal; a product misbehaviour: fix the product and its SwRS). When the
cause stays unfound, the CR ships A and B with the failing run named in the PR body's Known gaps
(decision 1); never a retry, a quarantine or a narrowed default list (but see Open question 4).

## Out of scope

- `checkbox-toggle`, `realinput-t45`, `previewmanager-162`: filed separately.
- Any change to the integration job, its order of steps, or the `toc-loop` job.
- `findInPreview.test.ts` (it lost the same wait in e05f0b51 and is already in the default stress
  plan).
- A product change, unless the trace proves one is needed (C) or the owner asks for the product
  log (Open question 3).

## CI environment

- The `stress` job (`.github/workflows/ci.yml:313-353`): `ubuntu-latest`, `timeout-minutes: 30`,
  `just dev-ci` then `xvfb-run -s "-screen 0 2600x1440x24" just ci-stress`, VS Code downloaded by
  the test runner at each run (no cache of it), no secrets, `STUDIO_VIEWPORT_GUARD=strict`. It runs
  on every push to `main` (advisory, `continue-on-error`, except on a version change, where it
  blocks `tag-release`, CI rule 14) and on `gh workflow run ci.yml --ref <branch> -f heavy=true`.
  Never on a pull request (CI rule 13).
- What the local Windows machine lacks: Xvfb and a free desktop (a real-window run opens a window
  on the desktop shared with other agents; `ci-stress` needs an unlocked screen); `just preflight`
  on Windows runs the static stage only. So the stress proof and the run times are CI-only.
- Before the push: `just check` (it runs `test/build/stressPlan.test.ts`,
  `test/build/hangWatchdog.test.ts`, `test/build/test_workflows.py` and the formatter's unit test),
  `just requirements-update`, `just preflight`.
- Only CI proves: the duration of the new default plan against its deadline (the launcher prints
  `stress: launch deadline ... ms (<rounds> rounds x 21 scenarios ...)` and `stress: <rounds>
  round(s) passed`), both scenarios green in every default round, and the trace lines appearing in
  the job log (only on a failure; the unit test proves their content).

## Evidence

1. `just check` passes at the pushed head; `test/build/stressPlan.test.ts` asserts both names in the
   default trusted plan; `test/build/test_workflows.py` reads `.github/workflows/ci.yml` and the
   `justfile` from the repository at the head under test (they already do: keep it so, no prepared
   copy) and asserts the default rounds the owner chose.
2. The formatter's unit test (`test/build/`) checks one trace line from a fixed snapshot: the
   prefix `<scenario> failure trace: `, valid JSON, each field of B.1, and an error while collecting
   printed inside the trace. The `catch` of B.2 is one shared helper (for example
   `withFailureTrace(name, collect, body)` in `test/shared/`), used by both scenarios, and a second
   case checks it with a fake body that throws: the original error is rethrown unchanged and the
   trace is printed once.
3. `git grep -n storedEditModeForTests -- test/integration/pasteUrl.test.ts
   test/integration/dropFiles.test.ts` prints nothing at the head under test (C1).
4. A heavy dispatch on the branch, default stress: `gh workflow run ci.yml --ref <branch> -f
   heavy=true -f gallery=false`; the `stress` job is green, its log shows `<rounds> rounds x 21
   scenarios` and the stress step's duration is recorded in the PR body against the deadline; the
   `integration` job is green at both steps.
5. A focused loop: `gh workflow run ci.yml --ref <branch> -f heavy=true -f gallery=false -f
   stress_repeat=60 -f stress_scenarios=paste-url,drop-files` (120 scenario runs, under the 220 of
   CI rule 13); green.
6. After the merge, the stress job of the push to `main` runs the new default and is read (CI rule
   13: read each job's result, the run stays green with a red advisory stress).

Default and configured values (the stress plan depends on `STUDIO_STRESS_SCENARIOS` and
`STUDIO_STRESS_REPEAT`), one line per cell, each checked by `test/build/stressPlan.test.ts` or
`test_workflows.py`:

- `STUDIO_STRESS_SCENARIOS` empty, trusted window: the 21 default names, `paste-url` and
  `drop-files` last.
- `STUDIO_STRESS_SCENARIOS` empty, untrusted window: `untrusted-read-only` only.
- `STUDIO_STRESS_SCENARIOS=paste-url,drop-files`, trusted: those two, in that order; untrusted:
  nothing to run.
- `STUDIO_STRESS_REPEAT` empty (justfile) and `inputs.stress_repeat` empty (workflow): the default
  rounds of Open question 1; set: the given rounds.

## Open questions for the owner

1. **How do the two scenarios fit the stress time budget?** At today's 12 default rounds, 21
   scenarios break the "third of margin under the deadline" guard (A.4: 1,028 s expected against
   960 s), and CR-425 kept them out of the default list for that reason. Options: (a) 11 default
   rounds for every scenario (all guards hold unchanged, 231 runs per window, about 8% fewer
   repetitions each); (b) 10 rounds (more margin, 210 runs, about 17% fewer); (c) keep 12 rounds by
   changing the margin guard or the 24-minute ceiling, which CI rule 11 forbids as written and
   would need a guideline change. The spec writer leans to (a), which changes no rule.
2. **Replace the two time-based waits now (C2)?** `pasteUrl.test.ts:104-115` (click loop with a
   700 ms pause) and `dropFiles.test.ts:107` (400 ms pause before counting the drop marker) never
   failed, but CI rule 12 forbids waits on time. In this CR before any failure, or only if a proof
   run fails there (the spec's default), or in a separate CR?
3. **A product-side trace too?** B adds test-side traces only. CR-425 decision 4 kept out a debug
   log of a dropped page-state message (type, page identity, host stage identity) in
   `reportStaleEdit`; it would name a stale drop if a race of this family comes back, at the cost of
   a product change (and an SwRS, LIFE-169). Add it here, or keep it out?
4. **If a proof run fails and the cause is not found:** decision 1 says ship what is proved plus
   traces. Do both scenarios still join the default stress list then? A red `stress` stays
   advisory on ordinary pushes, but on a version push it blocks the release tag (CI rule 14) until
   a re-run of the failed jobs is green.
