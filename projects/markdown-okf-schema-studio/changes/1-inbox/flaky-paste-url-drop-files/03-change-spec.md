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
   quarantine. Both scenarios join the default `just ci-stress` scenarios even then: the failing
   run and its trace go in the PR body and a follow-up CR is filed; a high measured failure rate
   comes back to the Chief of Staff as a blocked handback naming the rate.
2. pu-Q2, the stress time budget: 11 default rounds for the 21 default scenarios; every guard
   holds unchanged. No change to the margin guard or to the 24-minute ceiling. `table-insert-slash`
   (sibling CR-453, flaky-realinput-t45, batch-07) stays on demand, never in the default plan.
3. The two fixed pauses of these scenarios are replaced now by waits on a state the page reports
   (CI rule 12): `pasteUrl.test.ts:103-115` and `dropFiles.test.ts:107`. Only these two; the other
   pauses of `test/integration/` are out of scope.
4. No product trace: `reportStaleEdit` (`src/session/pageMessages.ts:241`) gets no debug log of a
   dropped page-state message, as decided for CR-425. The traces are test-side only.

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
  same wait before e05f0b51, and because it runs only once per integration run today.

What the logs do not prove: why the host kept `true` for 10 s. The CR-350 diagnosis names the
likely reason, not proved for lack of a host trace: the page's `previewEditModeChanged` named an
older render (the toggle was clicked right after the autosave, before the render it starts reached
the page) and was dropped by `manager.matchesCurrent` (`src/session/previewManager.ts`) through
`reportStaleEdit`, as SwRS-MDOKFSTUDIO-LIFE-169 specifies ("A stale message stores nothing"). That
drop is by design, no product code reads the stored value any more (since b84b0585), and no test
waits for it now: it is not a product bug.

## Causes the CR proves or rules out

- **C1, the observed failure (proved by the logs, fixed by e05f0b51):** the obsolete stored-mode
  wait. The Driver confirms at the head under test that neither test reads
  `storedEditModeForTests`, and the repetition below stays green. The repetition, not this CR's
  code, is what closes C1.
- **C2, waits on time (never observed, removed now, decision 3):**
  - `pasteUrl.test.ts:103-115`: a 30 s loop that clicks the paragraph until the block text box
    stays open, with a fixed 700 ms pause (line 111). It is a retry loop around an action, which CI
    rule 12 forbids by name, and it can never go red on a lost click: it hides one.
  - `dropFiles.test.ts:107`: a fixed 400 ms pause between the `dragOver` and the count of the drop
    marker (`.sphinx-preview-insert-point--drop`), which a slow runner can miss.
- **C3, the state an earlier step leaves (to rule out by the default stress):** in `integration`
  both steps run right after `grid-card-editor-blur` (`test/integration/trusted-suite.ts:295-299`);
  in the stress window they run after `palette` and `checkbox-toggle`, then again after the first
  scenario of the next round. `drop-files` turns edit mode on but its `finally`
  (`dropFiles.test.ts:138`) does not turn it off when the body fails before line 137, unlike
  `pasteUrl.test.ts:156-160`: a failed `drop-files` can leave the next scenario's page in edit
  mode. A.6 closes that gap; the trace records tabs and edit mode for any other leftover.

## What changes

### A. The two scenarios

1. `test/integration/pasteUrl.test.ts:103-115`: replace the comment and the click loop with the
   pattern of `test/integration/editKeys.test.ts:51-53` and `test/integration/saveKey.test.ts:80-84`:
   after `await setEditMode(page, true)` (line 102, kept), one click
   `await withCurrentFrame(page, (frame) => frame.locator("p", { hasText: "Read the guide" }).click())`,
   then the existing `await waitForEditor(page, "[data-sphinx-preview-block-editor] textarea")`
   (line 115). No pause, no loop. The assertion of line 116 stays unchanged.
2. `test/integration/dropFiles.test.ts:107`: replace the 400 ms pause with
   `await waitFor("the drop marker", async () => await withCurrentFrame(page, (frame) =>
   frame.locator(".sphinx-preview-insert-point--drop").count()) === 1, <budget>)`, budget about
   twice its healthy duration (5 s), then keep the `expect("drop marker count while dragging", ...)`
   on the count read after the wait, so a miss is still recorded with the count it saw. Its intent
   is unchanged (one marker while dragging).
3. Progress markers (`markProgress`, `test/shared/hangWatchdog.ts:159`) at each phase of both
   scenarios (preview ready, edit mode on, text box open or drop marker shown, each paste or drop,
   autosave, edit mode off), so a `STEP TIMEOUT` names the phase and the trace carries it.
4. No retry, no raised timeout, no other change to an existing wait's duration or assertion.
5. Both tests keep their `@tests_req` markers (PALETTE-264 in `pasteUrl.test.ts`, PALETTE-004 in
   `dropFiles.test.ts`). The SwRS Method lines change only if they describe the click loop or the
   pause (`git grep -n -i "700\|click until\|400 ms" -- requirements/tiers/swrs/palette-slash`).
6. `test/integration/dropFiles.test.ts`, `finally` (line 138): add the best-effort
   `try { await setEditMode(page, false); } catch { }` that `pasteUrl.test.ts:156-160` has, before
   `disposeActivePreviewForTests()`, with its comment ("a failure here must not hide the
   scenario's own result"). `test/build/integrationEditModeRestore.test.ts` keeps passing.

### B. Traces in the CI log (decision 1, and CI rule 12: failure messages carry diagnostics)

Each scenario writes one trace that explains its next failure, in `integration` and in `stress`,
without changing what it checks:

1. A shared helper in `test/shared/` (for example `realWindowTrace.ts`):
   - `formatScenarioTrace(name, snapshot)`, pure: one line, `<scenario> failure trace: <JSON>`.
   - `withFailureTrace(name, collect, body)`: runs `body`; on an error it first prints the original
     error (`<scenario> failed: <error and stack>`, `console.error`), then runs `collect` under one
     overall bound of 5 s (`withTimeout`, `test/shared/hangWatchdog.ts`; the harness's
     `findCurrentFrame` is bounded per call only, so the overall bound is needed), prints the trace,
     and rethrows the original error unchanged. A timeout or an error of `collect` is printed inside
     the trace (`"collectError": ...`) and never replaces the scenario's error.
2. The snapshot holds the host state from `getActivePreviewForTests()` (`phase`, `requestId`,
   `documentVersion`, `webviewReady`, `deferredWorkPending`, `blockEditOpen`, `pageEditorOpen`,
   `contentPatches`, `htmlAssignments`, `panelActive`), the source document's `version` and text,
   whether a current frame was found and its `html` attribute `data-sphinx-preview-edit-mode`, the
   open editor tabs (`vscode.window.tabGroups`: label and input type per group), the step's last
   progress marker, and the scenario's `failures` list so far.
3. `pasteUrl.test.ts` and `dropFiles.test.ts`: the body inside `try` goes through
   `withFailureTrace`; the existing `finally` blocks stay (with A.6). The collector lives in
   `test/integration/` (it imports `vscode` and the harness); the build test exercises
   `withFailureTrace` with a fake collector.

### C. Both scenarios in the default stress plan, at 11 rounds

1. `test/shared/stressPlan.ts`: move `"paste-url"` and `"drop-files"` to the end of
   `STRESS_SCENARIOS_BY_HOST.trusted`, after `"checkbox-toggle"`, with a comment naming the runs
   above (the paste-url reds were the stored-mode wait removed by e05f0b51; drop-files carried the
   same wait). **Keep `STRESS_ON_DEMAND_SCENARIOS`**, empty after the move, still read by
   `hostStressPlan` and by `test/integration/realInput/run.ts:113`; rewrite its docblock (steps
   that `STUDIO_STRESS_SCENARIOS` may name but the default plan does not run, because the default
   rounds would pass the deadline margin; empty today). Sibling CR-453 refills it with
   `table-insert-slash`, and this CR goes first in the stack. An empty exported array is still
   read, so `just check`'s unused-export check passes; if it flags it, report it rather than
   delete the constant.
2. `test/integration/realInput/run.ts:103-106`: move the two table entries above the on-demand
   comment and rewrite it (the key list is the default trusted list, then the on-demand list; both
   open their own CDP connection, like `checkbox-toggle`). The start assertion (`run.ts:112-114`)
   stays.
3. `test/build/stressPlan.test.ts:61-69`: the CR-425 test ("never in the default plan") becomes a
   test that both names are in the default trusted plan (`hostStressPlan({}, "trusted")`), still run
   alone when named (`STUDIO_STRESS_SCENARIOS=paste-url,drop-files`), and never in the untrusted
   window; plus a check that `STRESS_ON_DEMAND_SCENARIOS` names nothing in the default list. This
   changes an assertion's intent at the owner's request: say so in the commit message and the PR
   body (constitution, section 3).
4. Default rounds 12 → 11 (decision 2). One exported constant `DEFAULT_STRESS_REPEAT = 11` in
   `test/shared/stressPlan.ts`, and every place below reads it or is checked against it:
   - the code defaults that today say `10` (used only when `STUDIO_STRESS_REPEAT` is unset, which
     `just ci-stress` and the workflow never leave): `stressPlan` (`stressPlan.ts:20`),
     `hostStressPlan` (`:102`), `test/integration/realInput/run.ts:115` and
     `test/shared/hangWatchdog.ts:84-85` move to `DEFAULT_STRESS_REPEAT` (drop the literal);
     `test/build/stressPlan.test.ts:11` asserts the constant instead of `10`;
   - `justfile:364`, `ci-stress REPEAT=env("STUDIO_STRESS_REPEAT", "11")`, and its comment at lines
     361-363 ("The default 11 rounds of all 21 trusted scenarios take about N min", N from the
     first CI run; "Up to about 220 scenario runs per window ... 11 rounds of all 21, 60 rounds of 3,
     100 rounds of 2");
   - `.github/workflows/ci.yml:342`, `${{ inputs.stress_repeat || '11' }}`; the `stress_repeat`
     input description (`ci.yml:34`, "empty means 11"); the comment above the `stress` job
     (`ci.yml:307-308`, "... scenarios (12 rounds, ..."); the `heavy` input description (`ci.yml:10`, "about 10
     and 16 minutes") with the measured minutes;
   - `test/build/test_workflows.py:671` and `:687` (the literals), and the test name
     `test_ci_stress_recipe_defaults_to_12_rounds_and_leaves_the_deadline_computed` (`:685`),
     renamed to say 11 rounds; these tests read `ci.yml` and the `justfile` from the repository, so
     they guard the shipped files;
   - `test/build/hangWatchdog.test.ts:309-317` and `:324`: `STUDIO_STRESS_REPEAT:
     String(DEFAULT_STRESS_REPEAT)` for the default-plan cases, and the comment at `:314` ("CR 328:
     19 scenarios x 12 rounds meet the ceiling") rewritten for 21 x 11 (231 runs, deadline capped at
     24 min, so the default line still says "capped"). The assertions that pass an explicit
     non-default value (`"0"`, `"100"`) stay.
   The margin guard (`hangWatchdog.test.ts:323-328`) is not changed: at 11 rounds x 21 scenarios it
   computes 944,760 ms against 960,000 ms and passes.
5. Facts behind decision 2, for the PR body: the stress launch deadline is `min(24 min, 2 min +
   rounds x scenarios x 6 s)` (`hangWatchdog.ts:78-80`); 12 x 21 would compute 1,027,920 ms against
   960,000 ms and fail the guard. Measured on CI, trusted window, 12 rounds x 19 scenarios, between
   the `stress: 12 round(s) of` and `stress: 12 round(s) passed` lines (the window start, about 15
   to 25 s, is before the first line and not counted): 833 s (run 44882733071), 836 s
   (44764608171), 923 s (44777704200), 928 s (44830737763), that is 3.65 to 4.07 s per scenario
   run; `paste-url` and `drop-files` take about 2.1 s each (run 44719877177).
6. Other mentions: `.agents/guidelines/ci.guidelines.md` names no default round count (rule 13's
   "about 220 scenario runs" and rule 11's "at most 24 min" hold); CONTRIBUTING.md:500 names the
   formula only. The Driver greps for `12 rounds`, `12 round`, `all 19`, `19 scenarios`, `|| '12'`
   and `"12"` near `STRESS` after the change, and fixes what describes the default. The sibling
   CR-453 spec names no 12-round default today; if a later edit of it does, it is stale against
   this CR.
7. `requirements/tiers/log.md`: a dated entry (both scenarios in the default stress plan at 11
   rounds, the two fixed pauses replaced, the C1 evidence in one sentence). No SwRS describes the
   stress list or its rounds (`git grep -n -i "stress" -- requirements/tiers/swrs` names only
   `CORE-076`, about which jobs run); the Driver runs it again. No product behaviour changes, so no
   other SwRS change beyond A.5. `just requirements-update` after the change.

### D. Proof by repetition, and a red proof run

If a proof run fails at `paste-url` or `drop-files`, the Driver reads the trace, writes what it
proves in the CR folder (`work/`), and fixes the cause in this CR when the trace names it (a wait on
a state the page reports; a product misbehaviour: fix the product and its SwRS). When the cause
stays unfound, the CR ships A, B and C as decided (decision 1): the failing run and its trace in
the PR body's Test plan and Impacts, a follow-up CR filed for the Chief of Staff; when the measured
failure rate is high (more than one failing run in the proof runs below), the Driver hands back
blocked with the rate instead. Never a retry, a quarantine or a narrowed default list.

## Out of scope

- `checkbox-toggle`, `realinput-t45` (CR-453, which adds `table-insert-slash` on demand after this
  CR), `previewmanager-162`: filed separately.
- The other fixed pauses of `test/integration/` (decision 3).
- Any change to the integration job, its order of steps, or the `toc-loop` job.
- `findInPreview.test.ts` (it lost the same wait in e05f0b51 and is already in the default stress
  plan).
- A product change, including a log in `reportStaleEdit` (decision 4), unless a trace proves a
  product misbehaviour (D).

## CI environment

- The `stress` job (`.github/workflows/ci.yml:313-353`): `ubuntu-latest`, `timeout-minutes: 30`,
  `just dev-ci` then `xvfb-run -s "-screen 0 2600x1440x24" just ci-stress`, VS Code downloaded by
  the test runner at each run (no cache of it), no secrets, `STUDIO_VIEWPORT_GUARD=strict`. It runs
  on every push to `main` (advisory, `continue-on-error`, except on a version change, where it
  blocks `tag-release`, CI rule 14) and on `gh workflow run ci.yml --ref <branch> -f heavy=true`.
  Never on a pull request (CI rule 13). The `integration` job runs both scenarios once, in the same
  environment, with a 20-minute test step.
- What the local Windows machine lacks: Xvfb and a free desktop (a real-window run opens a window
  on the desktop shared with other agents; `ci-stress` needs an unlocked screen); `just preflight`
  on Windows runs the static stage only. So the stress proof, the trace in a real window and the
  run times are CI-only.
- Before the push: `just check` (it runs `test/build/stressPlan.test.ts`,
  `test/build/hangWatchdog.test.ts`, `test/build/test_workflows.py` and the helper's unit test),
  `just requirements-update`, `just preflight`.
- Only CI proves: the duration of the new default plan against its deadline (the launcher prints
  `stress: launch deadline ... ms (11 rounds x 21 scenarios ...)` and `stress: 11 round(s)
  passed`), both scenarios green in every default round and in the focused loop, and the trace
  lines in a real job log (Evidence 5).

## Evidence

1. `just check` passes at the pushed head: `test/build/stressPlan.test.ts` asserts both names in
   the default trusted plan, `STRESS_ON_DEMAND_SCENARIOS` disjoint from it, and the default rounds
   equal to `DEFAULT_STRESS_REPEAT` (11); `test/build/test_workflows.py` reads
   `.github/workflows/ci.yml` and the `justfile` from the repository at the head under test (no
   prepared copy) and asserts `'11'` in both; the margin guard passes unchanged.
2. The helper's unit test (`test/build/`): `formatScenarioTrace` gives one line with the prefix
   `<scenario> failure trace: `, valid JSON and each field of B.2; `withFailureTrace` with a body
   that throws prints the original error first, then the trace once, and rethrows the same error
   object; with a collector that never settles it prints the trace with a `collectError` after the
   5 s bound (use a short bound in the test through a parameter); with a collector that throws,
   the scenario's error is still the one rethrown.
3. At the head under test, `git grep -n -E "storedEditModeForTests|setTimeout\(resolve, (700|400)\)"
   -- test/integration/pasteUrl.test.ts test/integration/dropFiles.test.ts` prints nothing (C1, C2).
4. A heavy dispatch on the branch, default stress: `gh workflow run ci.yml --ref <branch> -f
   heavy=true -f gallery=false`; `integration` green at both steps; `stress` green, its log shows
   `11 rounds x 21 scenarios`, and the stress step's duration goes in the PR body against the
   24-minute deadline.
5. The trace in a real window: a throwaway commit on a separate branch (never pushed to the PR
   branch, deleted afterwards) that forces one failure in each scenario after its first phase (for
   example a `throw new Error("forced failure for the trace proof")` after the first paste and after
   the first drop). Two dispatches, because a stress round stops at its first failure:
   `gh workflow run ci.yml --ref <throwaway> -f heavy=true -f gallery=false -f stress_repeat=1 -f
   stress_scenarios=paste-url` and the same with `drop-files`. Quote in `work/` and in the PR body
   the two `... failed:` and `... failure trace:` lines from the `stress` job logs.
6. A focused loop at the documented maximum: `gh workflow run ci.yml --ref <branch> -f heavy=true
   -f gallery=false -f stress_repeat=100 -f stress_scenarios=paste-url,drop-files` (200 scenario
   runs, under the about 220 of CI rule 13; computed deadline 2 min + 200 x 6 s = 22 min, under the
   24-minute ceiling); green.
7. After the merge, the Chief of Staff reads the `stress` job of the push to `main`, which runs the
   new default (CI rule 13: read each job's result, the run stays green with a red advisory
   `stress`), and files a flake if either scenario fails there.

Default and configured values (the stress plan depends on `STUDIO_STRESS_SCENARIOS` and
`STUDIO_STRESS_REPEAT`), one line per cell, each checked by `test/build/stressPlan.test.ts` or
`test_workflows.py`:

- `STUDIO_STRESS_SCENARIOS` empty, trusted window: the 21 default names, `paste-url` and
  `drop-files` last.
- `STUDIO_STRESS_SCENARIOS` empty, untrusted window: `untrusted-read-only` only.
- `STUDIO_STRESS_SCENARIOS=paste-url,drop-files`, trusted: those two, in that order; untrusted:
  nothing to run.
- `STUDIO_STRESS_REPEAT` empty in the justfile and `inputs.stress_repeat` empty in the workflow:
  11 rounds; unset in a direct `npm run test:integration` stress run: `DEFAULT_STRESS_REPEAT`
  (11); set: the given rounds.

## Pull request

The body follows `.github/PULL_REQUEST_TEMPLATE.md` (pull-request guidelines, CI rule 10): Summary,
Deliverables, Changes, Impacts, Blast radius (graded 1 to 3), Test plan; "None" rather than a
deleted section. Written for a reader outside the team: no CR number, batch, agent role or other
internal id in the text; the commits and runs are named by their links. The Test plan carries
Evidence 1 to 6 with run links and the head SHA, the measured stress duration, the two trace lines
of Evidence 5, and, when D applies, the failing run and its trace. The Changes section says that
the stress plan test changed its intent (C.3) and why.

## Open questions for the owner

None: the owner's answers and the Chief of Staff's settlements in `02-answers.md` close every
question of the first draft.
