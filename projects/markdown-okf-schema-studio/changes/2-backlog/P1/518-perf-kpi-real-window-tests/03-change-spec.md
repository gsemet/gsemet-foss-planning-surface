# Real-window performance KPI job with maximums, also local on Windows

## Goal

The owner wants performance measured in a real VS Code window on a complex rendering case, given as
KPI scores, with requirements that set the maximum each score must meet (`intake/request.md`,
`02-answers.md`).

First scope: the document of issue 547 (https://github.com/gsemet/markdown-okf-schema-studio/issues/547),
two paths: text selection and comment creation. Each score is a median time in milliseconds and its
ratio to the maximum (1 or less means met). The campaign runs in GitHub CI, where an exceeded maximum
turns the job red and so blocks a release, and by a local command, to compare, on Linux, macOS and
Windows.

This CR ends at the report files (`out/reports/perf/kpi.json`, `kpi.md`), the CI job, the maximums and
their requirement (answer 9). The page of the scores on the GitHub Pages site is the CR
`perf-kpi-pages`, stacked above this one.

## Base and place in batch-09

Directly above CR-517 `perf-547-comment-update-and-author` (`changes/4-batch/1-pending/517-*`), itself
directly above CR-516 `perf-547-slow-comment-selection`; `perf-kpi-pages` sits above this CR. The
maximums are measured after the whole fix of issue 547, as answer 4's "after the fix" says: on a head
that holds both CR-516 and CR-517.

What this CR builds on, from CR-516's `03-change-spec.md`, Part 1, at the head where it is merged:
the deterministic generator of the issue's document in `test/probe/`; the real-window scenario
`perf-547` (`STUDIO_REAL_INPUT_SCENARIO=perf-547`, beside `test/integration/performanceProbe.ts`), one
window launch per run, which writes `out/reports/probe/perf-547.json` with every sample and the median
per interaction, among them `selectionRelease` (from the mouse release that ends a selection to the
Comment button shown) and `commentCreate` (from the save of a new comment to its highlight drawn).
CR-517 adds the `authorWait` samples to that report; they are not a KPI here. Neither CR sets a limit.
This CR never repeats the measure: it runs the scenario three times, turns its samples into scores,
checks them against the maximums and runs it in CI. It replaces CR-516's manual CI job and local
command (answer 7).

## Decisions (from `02-answers.md`)

1. Answer 1 (next batch) is replaced by answer 2: the campaign goes into the running batch batch-09,
   with the fix of issue 547 (owner, in perf547-Q1: "Tu vas en profiter de ce fix pour rajouter la
   campagnes de PKI demander").
2. Where it runs (answer 3, "C. Les deux"): in GitHub CI, which carries the maximums, and by a local
   command used to compare.
3. An exceeded maximum (answer 4, "A. Job rouge"): requirements with a maximum and a wide margin;
   exceeding it fails the heavy job, so it blocks a release. The margin is about twice the median
   measured after the fix.
4. First cases (answer 5, "B. Ticket 547 seul"): selection and comment creation on the issue 547
   document only; other cases later.
5. Score form (answer 6, "A. ms et ratio"): the median time and the ratio measured / maximum; 1 or
   less means met.
6. CR-516's manual job and local command (answer 7, "A. Les remplacer"): this CR removes them; the
   `perf` job and `just perf-kpi` are the only entries. A one-off measure is then a full heavy run.
7. `just preflight` on Linux and macOS (answer 8, "A. Comparer"): it runs the campaign and shows the
   differences without failing on a maximum; only CI enforces the maximums.
8. The site page (answer 9, "A. Deux CR"): `perf-kpi-pages`, above this CR; this CR is mergeable
   without waiting for it.
9. Windows (answer 10, "B. Windows dès batch-09", as the Chief of Staff reads it): the local comparison
   command `just perf-kpi` also runs on Windows, in this CR. The other real-window stages stay on
   Linux and macOS, and `just preflight` on Windows keeps running the static stage only.

Repetition: the owner asked for the real-window analysis to be run "2 ou 3 fois pour avoir un peu de
stabilité" (perf547-Q1). The campaign follows it: three window launches per run.

## What changes

### The KPI definitions and the maximums: `test/shared/perfKpi.ts` (new)

- `PERF_KPIS`, one entry per KPI, in this order:
  - `comment-selection`: "Text selection on the issue 547 document": the samples `selectionRelease`
    of `perf-547.json` (from the mouse release that ends a text selection to the Comment button
    shown).
  - `comment-create`: "Comment creation on the issue 547 document": the samples `commentCreate` of
    `perf-547.json` (from the save of a new comment to its highlight drawn).
  Each entry holds its id, title, the requirement scenario it checks (`SwRS-...#S1`, `#S2`, see
  "Requirements") and `maximumMs`.
- The KPI reads the samples of the report as CR-516 writes them; it never reads the report's own
  medians, since it pools the samples of three launches.
- `maximumMs` is about twice the median of the first heavy CI run of this branch (the CI runner, not
  a local machine), whose base holds CR-516 and CR-517, rounded up to the next 10 ms. The run id that
  gave each value is written in a comment next to it, and in the SwRS's rationale.
- Pure functions, no I/O: `median(samples)` (odd count: the middle; even: the mean of the two
  middle values), `scoreKpi(kpi, samples)` giving `{ id, title, requirement, samples, medianMs,
  maximumMs, ratio, met }` with `ratio = medianMs / maximumMs` rounded to two decimals and `met`
  true when `medianMs <= maximumMs`. No sample for a KPI is an error that names the KPI, never a
  score of 0.

### The campaign script: `test/integration/perfKpiCampaign.ts` (new, compiled to `out/test/integration/perfKpiCampaign.js`)

- Reads the reports of the three launches from `out/reports/perf/runs/run-<k>.json` (k = 1, 2, 3:
  `out/reports/probe/perf-547.json`, copied there by the target after each launch), pools the
  samples `selectionRelease` and `commentCreate` over the three launches, scores them with `scoreKpi`.
- Writes `out/reports/perf/kpi.json`:
  `{ "schema": 1, "commit": <full sha>, "runId": <STUDIO_E2E_RUN_ID, or "local">, "startedAt",
  "machine": { "os", "cpuModel", "cpus" }, "launches": 3, "kpis": [ <one score per KPI> ] }`
  (`os` is `process.platform`: `linux`, `darwin` or `win32`), and `out/reports/perf/kpi.md`, the same
  table in Markdown. These two files are the contract `perf-kpi-pages` reads.
- Prints one line per KPI: `<id>: median <m> ms, maximum <M> ms, ratio <r> (<met|OVER>)
  [<n> samples]`.
- `--enforce` (CI): exit 1 when a KPI is over its maximum, last line
  `perf KPI: FAILED, <id> <m> ms > <M> ms` (every KPI over, comma-separated); else last line
  `perf KPI: all <n> KPIs within their maximums`. Without `--enforce` (comparison): exit 0
  whatever the ratios, an over KPI marked `OVER (CI maximum)`, last line
  `perf KPI: compared on this machine, the maximums hold for the CI runner`.
- Either mode: a missing run report or a KPI without samples exits 1 and names the launch or KPI.
- Carries `@tests_req <the new REVIEW SwRS>#S1` at the check of `comment-selection` and `#S2` at
  the check of `comment-create` (one marker per scenario, at the comparison).

### Justfile

- `ci-perf MODE="enforce": (_require-unlocked-screen "ci-perf")` (new), the CI job's target. `MODE`
  is `enforce` (the default, what CI runs) or `compare`; any other value stops at once with
  `ci-perf: MODE must be enforce or compare, got "<value>"`, exit 2. It removes `out/reports/perf/`,
  runs the scenario `perf-547` three times, one window launch each, in the launcher's perf mode
  (`{{ npm }} run test:integration -- --perf-only --launch <k>`, k = 1, 2, 3; see "The perf launches
  leave the integration stage's report alone"), copies each launch's `out/reports/probe/perf-547.json`
  to `out/reports/perf/runs/run-<k>.json`, then runs `node out/test/integration/perfKpiCampaign.js`,
  with `--enforce` in `enforce` mode only. Last line `ci-perf: passed` or `ci-perf: FAILED` (CI
  guideline rule 8); in `compare` mode a pass reads `ci-perf: passed (compared, maximums not
  enforced)`. A launch that fails stops the target red; there is no retry (rule 9). It runs on
  Linux, macOS and Windows; it has no Windows stop line.
- `perf-kpi` (new), the local comparison command: `just ci-perf compare`, then last line
  `perf-kpi: done`. It fails only when a launch or the measure fails.
- Both stop with exit code 3 on a locked screen, like `ci-integration` (`_require-unlocked-screen`;
  `STUDIO_SCREEN_LOCKED=1` forces it on every OS; there is no lock probe on Windows, as on Linux).
- `preflight`, on Linux and macOS: runs `just ci-perf compare` after `just ci-acceptance` and before
  `ci-report`, counted in the failures (a failed launch or measure, never a maximum; exit 3, a locked
  screen, counts as a failure as it does for `ci-integration`). Its exit 3 does not join the
  `locked` list that skips `ci-report` and `ci-gallery`: those two stages do not read the perf run,
  so they run and judge the same stages as without it, and preflight prints `ci-perf: skipped, the
  screen is locked` for it. On Windows it
  still runs the static stage only; the skip line becomes `preflight: visual, viewer-graph,
  integration, acceptance, perf, report and gallery stages skipped on Windows; CI runs them (just
  perf-kpi compares the performance KPIs on this machine)`.
- CR-516's local command for its measure is removed (answer 7), under the name CR-516 gives it at
  the head this CR is based on; the scenario itself stays, and still runs by hand with
  `STUDIO_REAL_INPUT_SCENARIO=perf-547 npm run test:integration -- --trusted-only`.

### The perf launches leave the integration stage's report alone

Today a `STUDIO_REAL_INPUT_SCENARIO=... npm run test:integration -- --trusted-only` run goes through
`runIntegration` (`test/integration/run-tests.ts`), which rewrites
`out/reports/e2e/integration-manifest.json` with that run's own fields; `scripts/e2e-campaign.mjs
report`, called by `ci-report`, reads that file as the integration stage. The trusted launch also
writes its heartbeat file, any hang dump (`HANG_DUMP_ROOT`) and any capture or evidence of the
harness (`E2E_SCREENSHOT_ROOT`) under `out/reports/e2e/`. Run three times by `ci-perf`, the launches
would replace the integration stage's report that preflight's `ci-report` then judges, and the perf
artifact would carry a perf-run `integration-manifest.json`. The change:

- A launcher mode `--perf-only --launch <k>` in `test/shared/runnerArgs.ts`: `{ mode: "perf",
  launch: k }`, `k` an integer from 1 to 3. Refused, before any manifest is written and any VS Code
  starts, with a line naming the reason: a missing or other `--launch`, `--perf-only` with a scope
  flag or with `--acceptance-only` or `--group`, and a `STUDIO_REAL_INPUT_SCENARIO` set to anything
  but `perf-547`.
- In that mode `run-tests.ts` makes the one trusted launch of the scenario `perf-547` (it sets
  `STUDIO_REAL_INPUT_SCENARIO=perf-547` for the launch itself) and never calls `runIntegration`: it
  writes no `integration-manifest.json`. Its own record is
  `out/reports/perf/runs/launch-<k>/launch-manifest.json` (`status` running, then passed or failed,
  `launch`, `command`, `instanceId`, `revision`, `dirty`, `startedAt`, `completedAt`), and a failed
  launch exits 1 as today.
- `test/reportPaths.ts`: when `STUDIO_PERF_LAUNCH=<k>` is set, `E2E_REPORT_ROOT` is
  `out/reports/perf/runs/launch-<k>/` instead of `out/reports/e2e/`, so `E2E_SCREENSHOT_ROOT`,
  `HANG_DUMP_ROOT` and the default root of `heartbeatFileFor` follow it, in the launcher and in the
  extension host. The perf mode has `STUDIO_PERF_LAUNCH` set in its own process before these
  modules load (a re-exec or a dynamic import, the implementer's choice, proved by the test below)
  and passes it in `extensionTestsEnv`. Unset, every path is as today.
- `ci-perf` does not call `node scripts/e2e-campaign.mjs begin`: it writes no `campaign-*.json` and
  invalidates no stage manifest. `out/reports/probe/perf-547.json` is CR-516's file; `ci-report` and
  `ci-gallery` read nothing under `out/reports/probe/` or `out/reports/perf/` in this CR.
- A locked screen stops `ci-perf` in `_require-unlocked-screen`, before any launch: it writes nothing
  and does not remove `out/reports/perf/` either.
- Result: after `ci-perf` (either mode, a locked screen included), `out/reports/e2e/`,
  `out/reports/acceptance/` and `out/reports/visual/` are what they were before, file for file, so
  what `ci-report` and `ci-gallery` judge does not change. In CI the perf job's upload of the whole
  `out/reports/` keeps its layout (`perf/kpi.json`, `perf/kpi.md`, `perf/runs/run-<k>.json`), with
  `perf/runs/` now also holding the `launch-<k>/` folders; its only `e2e/` content is the
  `e2e/hang-dumps/post-step/` that `just ci-hang-dump` writes after the step.
- A hand run of the scenario with `--trusted-only` still writes the integration manifest, as every
  hand scenario run does today; CONTRIBUTING.md, "Performance KPIs", points to `just perf-kpi`
  instead.

### Windows: what stops the local command today, and what changes

Found on main 5f0746d, by reading the code the command runs, on the owner's Windows machine with
Git for Windows:

- The justfile: `preflight` stops after the static stage on Windows, and CONTRIBUTING.md, "Windows",
  says the real VS Code stages run on Linux and macOS only. No `ci-*` real-window target refuses
  Windows by itself: the recipes run in Git for Windows' bash, and `{{ npm }}` already calls
  `npm.cmd` through `fnm`. `ci-perf` and `perf-kpi` therefore need no Windows branch.
- The input does not go through the system's pointer: the real-window suites connect Playwright to
  the window over its loopback debugging port (`--remote-debugging-port`, `test/integration/run-tests.ts`;
  `chromium.connectOverCDP`, `test/integration/realInput/harness.ts`). Nothing in that path is
  specific to Linux or macOS, but it has never run on Windows in this repository (see "Evidence").
  Shortcuts already use `Control` off macOS (`MOD` in `harness.ts`).
- VS Code: `run-tests.ts` uses `/Applications/Visual Studio Code.app/...` when it exists, else
  `downloadAndUnzipVSCode`, which asks for the build of the running system; `STUDIO_VSCODE_EXECUTABLE`
  picks another build. Unchanged; only its comment and CONTRIBUTING.md name `Code.exe` on Windows.
  That download has never been used on Windows in this repository (see "Evidence").
- A `perf-547` launch runs the steps `setup` and `preview-smoke` before its scenario
  (`scenarioSteps` in `test/integration/trusted-suite.ts` gives `setup`, `preview-smoke`,
  `real-input` to every scenario it does not list; CR-516's specification does not make `perf-547`
  skip them). Neither has run on Windows either.
- Blocker 1, `/tmp`: `runScenario` in `run-tests.ts` creates the launch's workspace directory with
  `fs.mkdtempSync(path.join("/tmp", ...))` and puts `{ "path": "/tmp" }` as the second workspace
  folder. On Windows `/tmp` is `\tmp` on the current drive, which does not exist on a normal machine:
  the `mkdtempSync` fails before VS Code starts. Change: both use `shortTemporaryRoot()` of
  `test/shared/runIsolation.ts` (`os.tmpdir()` on Windows, still `/tmp` on Linux and macOS, so those
  are unchanged). The workspace definition is built by a pure helper
  (`trustedWorkspaceDefinition(workspaceRoot, temporaryRoot)`) so that a unit test checks it.
  `reload-suite.ts` and `scroll-sync-suite.ts` keep their own `/tmp` (the scenario does not run them;
  out of scope).
- Blocker 2, the hang watchdog's process list: `listProcesses` in `test/shared/hangDump.ts` runs
  `ps -A -o pid=,ppid=,args=`; Git for Windows' `ps` refuses it (`ps: unknown option -- A`). The
  watchdog catches the error and kills only its root pids, and a `runTests` launch has none: a launch
  that passes its deadline on Windows is reported but its VS Code stays open. Change: on `win32`,
  `listProcesses` reads `powershell.exe -NoProfile -NonInteractive -Command "Get-CimInstance
  Win32_Process | Select-Object ProcessId,ParentProcessId,CommandLine | ConvertTo-Json -Compress"`,
  turned into the same `ProcessEntry` list by a pure `parseWindowsProcessList(json)` (an array or a
  single object; a null `CommandLine` becomes `""`). The process list of a hang dump (the
  `ps -eo ...` call) uses the same list on Windows. `process.kill(pid, "SIGKILL")` already ends a
  process on Windows. Linux and macOS keep `ps`.
- Window focus: `ensureTestWindowFocused` (`test/integration/windowFocus.ts`) returns at once off
  macOS, and Windows then takes the path Linux takes (the workbench focus settled over CDP where the
  suites need it). Unchanged. Whether Windows' foreground rules keep a newly launched window from
  getting the input the scenario sends is not known before a Windows run (see "Evidence").
- No lock probe on Windows (as on Linux): a locked session is not detected before the launches.

### CI workflow: `.github/workflows/ci.yml`

- New heavy job `perf`, built like `integration` (CI guideline rules 1, 3, 11, 13): `needs:
  release-check`, the same `if` as `integration` (every push to `main`, a dispatch with `heavy`,
  never a pull request), `runs-on: ubuntu-latest`, `timeout-minutes: 15`, output `artifact:
  e2e-perf-attempt-${{ github.run_attempt }}`. Steps: checkout with LFS, LFS pull and fsck, Node,
  uv, just, `just dev-ci`, then `xvfb-run --auto-servernum -s "-screen 0 2600x1440x24" just ci-perf`
  with `timeout-minutes: 10` and `STUDIO_VIEWPORT_GUARD: strict`, then `just ci-hang-dump` and the
  upload of `out/reports/` as `e2e-perf-attempt-<n>`, both `if: always()`. Both timeouts are set
  again to about twice the healthy duration of the first CI run (rule 11), the step's below the
  job's.
- `tag-release`: `needs` gains `perf`. The refusal step and the tag step require
  `needs.perf.result == 'success'` on a version change, like `stress`; the "Release not tagged"
  summary and the `::error::` line list `perf: $PERF`.
- The `heavy` input's description names the perf job.
- `checks` is unchanged: `perf` is not one of its needs (the real VS Code jobs are not, CI rule 13),
  so a red `perf` on a push without a version change shows as a red job and does not fail `checks`.
  Its red blocks a version change at `tag-release` (decision 3).
- CR-516's manual job is removed (answer 7): its `workflow_dispatch` input, its job and its
  `just ci-<name>` target, under the names CR-516 gives them.
- `report`, `pages`, `reports_from_caller` and `scripts/select_e2e_run.py` are not touched here:
  bringing the perf report into `studio-reports` and the site belongs to `perf-kpi-pages`.

### Requirements (okfreq)

Created with `okfreq new ... --lifecycle proposed` (IDs from okfreq, never by hand), then
`just requirements-update` and a dated entry in `requirements/tiers/log.md` under the date of the change.

- New SwRS in scope `review-annotations`, derives from `StRS-MDOKFSTUDIO-REVIEW-003` ("A reviewer
  comments, replies, resolves and deletes...", approved; its authored text is not changed). Title:
  "Selection and comment creation on a large document stay under their maximums". Scenarios:
  - `S1 (nominal): Text selection` - GIVEN the generated issue 547 document in the preview of a real
    VS Code window on the CI runner (`ubuntu-latest`, virtual screen) - WHEN a text selection ends by
    a mouse release, over three window launches - THEN the median time to the Comment button shown
    is at most `<maximumMs of comment-selection>` ms.
  - `S2 (nominal): Comment creation` - the same GIVEN - WHEN a new comment is saved, over three
    window launches - THEN the median time to its highlight drawn is at most `<maximumMs of
    comment-create>` ms.
  `verification_method: test`; criteria: `just ci-perf` on the CI runner. Rationale: the maximums
  are about twice the medians of the named CI run, after the whole fix of issue 547; a machine other
  than the CI runner compares, it does not judge. `@implements_req` sits at the code that produces
  the two paths at the head under test: the selection handling of `src/page/modules/commentCompose.ts`
  and `handleCreate` of `src/session/features/comments.ts` (where CR-516 and CR-517 leave them).
- `SwRS-MDOKFSTUDIO-CORE-076` (proposed): the normative text names `perf` among the heavy jobs a
  version change needs; new scenario `S13 (boundary): The performance KPI job` (the job runs where
  `integration` runs; a red `perf` on a version change makes `tag-release` refuse and list it; it
  does not fail `checks`). S5's table and S6's table gain `perf` where they list the heavy jobs. Any
  scenario or line CR-516 added for its manual job is removed with the job.
- The Windows changes of the test harness are test tooling: no SwRS (no product behaviour changes).
- No approved requirement's authored text changes, so no owner agreement is needed (project
  guidelines, "Approved requirements").

### Guidelines and docs

- `.agents/guidelines/ci.guidelines.md`: rule 7 (preflight runs `ci-perf` in `compare` mode, the one
  `ci-*` target it runs with another argument than CI: the maximums hold for the CI runner only); rule
  11 (the `perf` job, 15 minutes, its test step 10, set to twice its healthy duration once
  measured); rule 13 (`perf` is a real VS Code job run on every push to `main` and on a heavy
  dispatch; it is not part of `checks`; CR-516's on-demand job line removed); rule 14 (`tag-release`
  needs `checks` and the four heavy jobs; "Release not tagged" lists `perf`); the recovery section
  (`perf` among the jobs re-run by "Re-run failed jobs"; its artifact output).
- `CONTRIBUTING.md`: a short "Performance KPIs" section: what is measured, the score (median, ratio
  to the maximum), `just ci-perf` (CI, enforces) and `just perf-kpi` (local, compares; Linux, macOS
  and Windows; preflight compares on Linux and macOS), the report folder `out/reports/perf/`, that a
  one-off measure on a branch is a heavy dispatch, and that a maximum changes in
  `test/shared/perfKpi.ts` and its SwRS in the same PR. "Windows": the real VS Code stages run on
  Linux and macOS only, except `just perf-kpi`, which needs an unlocked desktop session and
  downloads VS Code once (or uses `STUDIO_VSCODE_EXECUTABLE` set to a `Code.exe`). Any mention of
  CR-516's removed command or job goes.
- `AGENTS.md`, "Main targets": `just perf-kpi` and `just ci-perf` added to the CI job list; CR-516's
  removed command or job, if it was listed, goes.
- `docs/how-we-test.md`, when CR-507 is below this CR in the stack (CR-507 adds the page and a
  drift test that fails while a job of `ci.yml` is not named on it): in "The test levels", the
  `perf` job, in the form of the page's other levels: what it runs (the `perf-547` scenario three
  times, one window launch each, its medians scored against the maximums of
  `test/shared/perfKpi.ts`), its folders (`test/shared/perfKpi.ts`,
  `test/integration/perfKpiCampaign.ts`), its commands (`just ci-perf` in CI, which enforces the
  maximums; `just perf-kpi` locally, which compares, also on Windows), its CI job (`perf`), when it
  runs (every push to `main` and a dispatch with `heavy`, never a pull request; a red `perf` blocks
  a version change at `tag-release`), and its marker (`@tests_req <the new REVIEW SwRS>#S1` and
  `#S2`). CR-516's manual job, if the page names it, goes with the job. When CR-507 is above this CR,
  CR-507 names the job itself (its H15) and this CR does not touch the page.
- `.agents/glossary/common.md`: **KPI score** (a median time in ms of one measured path and its
  ratio to its maximum, `scoreKpi` in `test/shared/perfKpi.ts`) and **Performance maximum** (the
  time a KPI's median must not pass on the CI runner, set by a SwRS and `PERF_KPIS`).

## Out of scope

- The fix of issue 547, its measure and generator (CR-516, CR-517).
- The Pages site page, its header link, and bringing the perf report into `studio-reports`
  (`report`, `pages`, `scripts/select_e2e_run.py`): `perf-kpi-pages`.
- Other complex rendering cases, documents or paths (decision 4).
- A history of scores across runs or releases; a mark out of 100 (decision 5); counts in place of
  times, a CPU calibration or a dedicated machine.
- The other real-window stages on Windows (`ci-integration`, `ci-acceptance`, `ci-stress`, the
  reload and scroll-sync suites' `/tmp`), and a `perf` job on a Windows CI runner.
- `npm run probe`, `test/probe/previewProbe.ts` and `test/integration/performanceProbe.ts`: unchanged,
  no limit added.
- A claim of conformance to a standard (the request asked about "ISO 28149").

## Evidence

- Unit (`just check`, so also on Windows in the `static-windows` job):
  - `test/build/perfKpi.test.ts`: `median` with odd and even counts; `scoreKpi` at the maximum (met,
    ratio 1.00), 1 ms over (not met), no sample (error naming the KPI); the shipped `PERF_KPIS` has
    the two ids in order; the maximums of the shipped `test/shared/perfKpi.ts` equal the numbers in
    S1 and S2 of the new REVIEW SwRS, read from that file at the head under test.
  - The campaign script on prepared run reports in a temporary folder (a prepared text only for the
    refusal cases the shipped files cannot hold: a KPI over its maximum, a missing run, a run without
    samples): `--enforce` exits 1 with the FAILED line naming the KPI, without `--enforce` exits 0
    with `OVER (CI maximum)`, a missing run exits 1 in both. Paired with the shipped-file check
    above. `kpi.json` carries `machine.os`.
  - `parseWindowsProcessList`: an array, a single object, a null `CommandLine`, an empty list; and
    `processTree` finding a launch by a Windows user-data path (backslashes, a drive letter) in the
    command line. On `win32` only (skipped elsewhere, so proved by `static-windows`): `listProcesses()`
    returns an entry for `process.pid` whose parent is `process.ppid`.
  - `trustedWorkspaceDefinition`: its workspace folders are the workspace root and the given
    temporary root, with `"/tmp"` on Linux and macOS (unchanged) and `os.tmpdir()` on Windows (a
    prepared root on the other systems).
  - `test/build/runnerArgs.test.ts`: `--perf-only --launch 2` gives `{ mode: "perf", launch: 2 }`;
    `--launch 0`, `4`, `x` or missing, `--perf-only` with `--trusted-only`, `--acceptance-only` or
    `--group`, and `STUDIO_REAL_INPUT_SCENARIO=probe` are refused with their line.
  - `test/build/reportPaths.test.ts` (new): in a child Node process with `STUDIO_PERF_LAUNCH=2`, `E2E_REPORT_ROOT`,
    `E2E_SCREENSHOT_ROOT`, `HANG_DUMP_ROOT` and `heartbeatFileFor(...)` are under
    `out/reports/perf/runs/launch-2/`; without it, under `out/reports/e2e/` as today.
  - The perf mode of `run-tests.ts`, with the VS Code launch replaced by a stub (a seam added for
    it): in a temporary `out/reports/` holding an `e2e/integration-manifest.json` and an
    `e2e/campaign-integration.json`, a passed and a failed perf launch leave both files byte for
    byte, write `perf/runs/launch-<k>/launch-manifest.json` with the status, and the failed one
    exits 1.
  - `test/build/test_workflows.py`: the `perf` job's `if` for each event (push to `main`, heavy and
    plain dispatch, pull request); its artifact name carries the attempt; the `tag-release` truth
    table with `perf` (a version change tags only with `checks` and the four heavy jobs `success`;
    every other `perf` result runs the refusal step, whose summary lists `perf`); `checks` does not
    need `perf`; every `needs.<job>` reference is a need; CR-516's input and job are gone; `ci-perf`
    with an unknown `MODE` exits 2; `perf-kpi` runs `ci-perf compare`; `preflight` runs `ci-perf
    compare` after `ci-acceptance` and before `ci-report` off Windows and prints the new skip line on
    Windows; with `ci-perf` stubbed to exit 3, preflight still runs `ci-report` and `ci-gallery` and
    counts one failure; `ci-perf` passes `--perf-only --launch <k>` and never calls
    `e2e-campaign.mjs begin`; `ci-perf` has no Windows stop; `ci-perf` and `perf-kpi` stop with exit 3 on a locked screen
    (`STUDIO_SCREEN_LOCKED=1`) and `ci-perf` ends with its passed or FAILED line.
  - With CR-507 below: CR-507's drift test of `docs/how-we-test.md` passes with the `perf` job in
    `ci.yml` and without CR-516's removed job.
- Requirements: `just requirements-update`, `just requirements-lint`, `just check-markers`, and
  `okfreq validate --check-links --project-root .` with CI's okfreq version.
- Real window in CI, on the branch (CI guideline rule 13): `gh workflow run ci.yml --ref <branch> -f
  heavy=true`. First run, on a base that holds CR-516 and CR-517: the `perf` job measures; its
  medians set `maximumMs` and the SwRS numbers (decision 3), and its duration sets the two timeouts
  (rule 11). Second run, at the head with the maximums: `perf` green with both ratios at most 1; the
  `e2e-perf-attempt-<n>` artifact holds `perf/kpi.json`, `perf/kpi.md` and the three run reports.
  That artifact holds no `e2e/integration-manifest.json` and no `e2e/campaign-*.json`. The two run
  ids go in the PR's test plan.
- Real window on Windows, on the implementer's Windows machine when the conditions of
  `.agents/guidelines/local-worktree.guidelines.md` for window tests are met (an unlocked desktop
  session, no other VS Code test window): `just perf-kpi` makes three launches, writes
  `out/reports/perf/kpi.json` with `machine.os` `win32` and two scored KPIs, and ends with
  `perf-kpi: done`, and `out/reports/e2e/` is the same before and after (absent stays absent); then
  one launch with `STUDIO_LAUNCH_TIMEOUT_MS` set below a launch's length stops
  with `LAUNCH TIMEOUT`, a hang dump under `out/reports/perf/runs/launch-<k>/hang-dumps/` whose process list is not empty, and no VS Code process of that
  user-data directory left (checked with the same CIM query). The PR's test plan gives the output's
  last lines and the two KPI lines. When the conditions are not met, the PR says so, and the Windows
  launches stay unproved.
- Real window on Linux or macOS, when a machine is at hand: `just preflight` runs `ci-perf compare`
  and does not fail on an over KPI, and a listing with checksums of `out/reports/e2e/`,
  `out/reports/acceptance/` and `out/reports/visual/` taken after `ci-acceptance` and again after
  `ci-perf` is the same; `ci-report` then reports the integration stage of `ci-integration`.
  Otherwise the unit and `test_workflows.py` checks above stand alone, said as such.
- `just preflight` (on Windows the static stage only; CI runs the others).
- What only CI proves: the timings under the virtual screen and their spread between runner
  instances; the job's healthy duration; the red of an exceeded maximum in a real run is not forced
  (no knob is added to lower a maximum), it is proved by the unit tests of the exit code and the
  `ci-perf` FAILED line.
- What stays unproved until a run on a Windows machine, none of it ever run on Windows in this
  repository: that `downloadAndUnzipVSCode` gives a Windows build that starts and loads the
  extension under development; that a launch with `--remote-debugging-port` accepts Playwright's
  `connectOverCDP` and that mouse and keyboard input over that port works as on Linux and macOS;
  that the `setup` step (`pinStoredWorkspaceChoices`, `ensureTestWindowFocused`) and the
  `preview-smoke` step (`test/integration/fixtures/preview.md` opened, the preview command, its
  checks) pass before the scenario; that the input sent over CDP reaches a newly launched window
  under Windows' foreground rules (no focus wait is added off macOS); that the
  scenario's drags fit the desktop's screen size and scaling; the launch time with the Windows build
  of VS Code and the antivirus; the behaviour on a locked Windows session, which is not detected
  beforehand. A failure found there is fixed in this CR before it is mergeable.

No host or default matrix: nothing in this CR depends on the agent host or on a shipped default
versus a configured setting.

## Open questions for the Chief of Staff

None.
