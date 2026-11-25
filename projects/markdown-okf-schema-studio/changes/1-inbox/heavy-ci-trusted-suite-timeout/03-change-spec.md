# Reliable heavy CI: split the trusted launch, fix the frame lookup

The heavy CI (the real VS Code `integration` job, run on every push to `main` and on demand with
`gh workflow run ci.yml --ref <branch> -f heavy=true`) fails intermittently. The trusted VS Code
launch (`trusted-suite.js`) runs at about 92 % of its 900 s deadline when healthy, so normal runner
variance pushes it over. The open-at-line step also failed once on a frame lookup that never
returned. This change makes the heavy run reliable: each trusted launch keeps a measured margin
under its deadline, and the frame lookup no longer stops on a frame that cannot be the Studio frame.
Every test that runs today still runs.

No issue.

## Goal

A heavy run that passes when the code is correct, and fails only for a real failure, not because
the trusted window is a few seconds slower than usual or a stray frame did not answer. Right now
`main` is green at 17b779d (run 45713440510), but the heavy run is not reliable: every heavy run
between the green 63ef752 (run 45476952370) and 17b779d failed (45580228461, 45617988132,
45625193289, 45706313890; the causes of the two CR-503 branch runs were not read), the first of
them with no change to the tests or the product.

## Diagnosis (measured, from the CI logs)

### The launch timeout: the suite fills its deadline. No step stalls

The launch deadline is `LAUNCH_DEADLINE_MS = 15 * 60_000` in `test/shared/hangWatchdog.ts`. It is
enforced by `watchLaunch` (`test/shared/launchWatchdog.ts`) around each `runScenario` call of
`test/integration/run-tests.ts`. The trusted launch runs every step of `runTrustedSuite` in
`test/integration/trusted-suite.ts` in one VS Code window.

| Run (job) | Commit | Trusted launch | Result | Where it stopped |
| --- | --- | --- | --- | --- |
| 45476952370 | 63ef752 | 20:08:18 to 20:22:13, about 835 s | green | |
| 45580228461 | 4a47151e | over 900 s | LAUNCH TIMEOUT | `lifecycle` done, 3 short steps left (about 7 s) |
| 45706313890 attempt 1 | 1f209e1 | over 900 s | LAUNCH TIMEOUT | in `diff-preview-scroll` |
| 45706313890 attempt 3 | 1f209e1 | over 900 s | LAUNCH TIMEOUT | `diff-preview-scroll` done, `side-preview-jump` just started |
| 45713440510 | 17b779d | 22:31:07 to 22:44:58, about 831 s | green | |

What the logs prove:

- Every step before the timeout ended with `STEP done` and a normal duration. The last step
  differs from one failure to the next. No step hangs: the heartbeat watchdog (90 s) never fired.
- `git diff 63ef752 4a47151e` changes nothing under `test/integration`, `test/shared` or `src`
  (feature clips, clip kit, docs only). The first red run is the same suite as the last green
  one, on a slower runner.
- The variance comes mostly from `real-input`: 404 s and 405 s on the green runs, 446 s, 455 s and
  449 s on the red runs. `preview-editing` follows it (32 s green, 37 to 38 s red).
- The large steps of the trusted launch on CI: `real-input` 404 to 455 s, `open-at-line-probe`
  178 to 181 s, `tall-block-scroll` 39 to 41 s, `preview-editing` 32 to 38 s, `open-at-line`
  21 to 22 s, `open-at-line-studio` 16 to 17 s. The other steps take seconds each.
- The whole `just ci-integration` step: 1011 s at 63ef752 (20:05:44 to 20:22:35) and 1002 s at
  17b779d, against the step's `timeout-minutes: 20` (1200 s) in `.github/workflows/ci.yml`.

What they do not prove: why a runner is slower. That does not matter for this change: a launch
that needs about 92 % of its deadline when healthy breaks CI rule 11 ("a budget about twice its
healthy duration").

Conclusion, under heavy-ci-Q2: the suite is too long for one launch. It is split into launches,
each with a measured margin under its deadline.

### The `locator.count` timeout of the open-at-line step

Run 45706313890 attempt 2 (job 139543061116):
`STEP failed: open-at-line (12624 ms): TIMEOUT: locator.count did not return within 10000 ms (frame )`,
from `frameCall` in `test/integration/realInput/harness.ts`. The step failed 12.6 s after it
started, so the failing call is the first frame lookup of `run()` in
`test/integration/openAtLine.test.ts`: `pageMarks(page)` (`test/integration/openAtLineHelpers.ts`),
then `findCurrentFrame(page)`.

`findCurrentFrame` loops over `page.frames()` and calls
`frame.locator("#sphinx-myst-preview-content").count()` on every frame. It skips only frames that
throw a "detached" error. The frame that timed out has an empty URL (`(frame )`): it never committed
a document, so a Playwright call that needs its execution context does not return. Such a frame can
never be the Studio frame. Earlier in the same window, during `stock-coexistence`, the log shows
`CodeWindow: failed to load (reason: <unknown>, code: -3)`. That is a lead, not a proof, that a
frame was left without a document.

What the log does not prove: which frame it was, or why it had no URL. The Driver first reads the
`e2e-integration-attempt-2` artifact of run 45706313890 (`out/reports/e2e/hang-dumps/` if
present, the window state, the VS Code log tails) and writes in the PR what it proves and what it
does not (CI rule 12).

## What changes

### 1. Two trusted launches instead of one (`test/integration/trusted-suite.ts`, `run-tests.ts`)

The steps of `runTrustedSuite` are split into two parts. Each part runs in its own VS Code window,
with its own user-data directory, heartbeat file and launch deadline (900 s each, unchanged). The
split is chosen on the measured durations, so that each part takes about half the deadline:

- **Part 1** (estimated 400 to 430 s on CI): `setup`, `preview-smoke`, `project-features`,
  `hostile-html`, `stock-coexistence`, `open-at-line`, `open-at-line-probe`,
  `open-at-line-studio`, `checkbox-toggle`, `radio-choice`, `table-empty-column`,
  `edit-toolbar-cover`, `tall-block-scroll`, `block-actions`, `find-in-preview`, then every step of
  the `remainingSteps` list (`edit-keys` to `workspace-disposal`), in their current order.
- **Part 2** (estimated 440 to 500 s on CI): `setup`, `preview-smoke`, `real-input`,
  `preview-editing`. This is the order of the existing real-input-only path, where `real-input`
  follows `setup` and `preview-smoke` directly.

The order inside each part is today's order. Only the `remainingSteps` group moves: it now runs
after `find-in-preview` in a window that has not run `real-input` and `preview-editing`. Before
the PR, the Driver checks that none of those steps relies on state left by `real-input` or
`preview-editing` (fixtures, settings, open tabs, the side bar). If one does, use the contiguous
split instead: part 1 = `setup` to `find-in-preview`, part 2 = `setup`, `preview-smoke`,
`real-input`, `preview-editing`, then `remainingSteps`. Report which split was taken and why. The
contiguous split is allowed only when part 2 still meets the margin of section "Evidence".

Mechanism (one suite file, so the `@tests_req` markers, `test/shared/e2eGroups.ts` and the SwRS
method lines that name `test/integration/trusted-suite.ts` stay valid):

- The part is selected by an environment variable passed through `extensionTestsEnv` (for example
  `STUDIO_TRUSTED_PART=1|2`). An unknown value fails at once with a clear message. A missing value
  fails too, except on the `STUDIO_REAL_INPUT_SCENARIO` paths (the next point).
- Every `STUDIO_REAL_INPUT_SCENARIO` path of `runTrustedSuite` (`drop-files`, `paste-url`,
  `block-actions`, `window-switch-keys`, `empty-column`, `toolbar-cover`, `find-in-preview`,
  `tall-block-scroll`, `stress`, `toc-loop`, `probe`, the named real-input scenarios) keeps running
  in a single launch exactly as today. `just ci-stress`, `just ci-toc-loop` and
  `STUDIO_REAL_INPUT_SCENARIO=probe npm run test:integration -- --trusted-only` (CONTRIBUTING.md)
  behave the same.
- `run-tests.ts` `main()`: the full run and `--trusted-only` (without
  `STUDIO_REAL_INPUT_SCENARIO`) run part 1, then part 2, as two `runScenario` launches. The rest
  of the order is unchanged: scroll-sync, untrusted, trusted part 1, trusted part 2, standalone,
  reverse-migration, reload. Each part:
  - gets its own CDP port (the `browserSuite` test covers both parts);
  - gets its own heartbeat file (`heartbeatFileFor(instanceId, <distinct name>)`);
  - has a launch name that tells the parts apart, so a `LAUNCH TIMEOUT` or `LAUNCH HANG` line and
    its dump folder say which part stopped (for example `trusted-suite.js part 2/2`);
  - runs `withSuiteWatchdog` with a suite label that names the part, so the heartbeat's
    `suite` field names it too.
- The frontmatter evidence block of `runScenario` (today `if (suiteName === "trusted-suite.js")`,
  which rewrites `frontmatter-e2e-*` manifests and `FRONTMATTER-LATEST.md`) runs after the part
  that runs `preview-editing`, the step that writes that evidence. The `suiteResult` note in
  `test/integration/previewEditing.test.ts` ("Parent must record trusted-suite exit after
  serializer and workspace disposal ...") is reworded to say which launch's exit it records. This
  is a text change, not an assertion change.
- `integration-manifest.json` keeps `scope: "trusted"` for `--trusted-only`.
- The comment on `STEP_BUDGETS_MS` in `test/shared/hangWatchdog.ts` ("the whole trusted window
  takes 265 to 400 s locally and about 1.1 times that on CI") is replaced by the measured CI
  durations of the two parts. No budget, deadline or `timeout-minutes` value changes:
  `LAUNCH_DEADLINE_MS`, `STEP_BUDGETS_MS`, `STUDIO_LAUNCH_TIMEOUT_MS`, the step's 20 minutes and
  the job's 30 minutes stay as they are (heavy-ci-Q2, CI rule 11).
- `test/build/hangWatchdog.test.ts` (unit, runs in `just check`) gets checks that the two parts
  of the full run get distinct heartbeat file names and launch names, if that logic lives in a
  unit-testable place (`test/shared/`). Keep the selection of the steps of a part out of
  `vscode`-dependent code where that is cheap, so a unit test can assert this: parts 1 and 2
  together hold every step of today's full trusted run exactly once, in the stated order. This
  test is the proof that "every test that runs today still runs".

### 2. The frame lookup skips frames that cannot be the Studio frame (`realInput/harness.ts`)

`findCurrentFrame` must not let one frame without a document fail the step. The fix:

- Before any Playwright call that needs the frame's execution context, select candidates by what
  is known without one: the frame's URL. A frame whose URL is empty or `about:blank`, or is not a
  VS Code webview URL, is skipped. The Driver checks the exact URL shape of a Studio webview frame
  in the real window (a `vscode-webview://` URL) and filters on what it sees, not on a guess.
- A `frameCall` timeout on a candidate frame (a webview URL) still fails the step, named as
  today. The 10 s `FRAME_CALL_TIMEOUT_MS` stays. A hang on a real Studio frame is a real failure.
- When `findCurrentFrame` finds no frame and its caller's `waitFor` times out, the failure message
  lists the frames it saw (URL, and whether each was skipped and why), so the next failure explains
  itself (CI rule 12, "Failure messages carry diagnostics").
- No sleep, no retry loop around the call. The change is a deterministic filter on a known
  property.

If the artifact of attempt 2 contradicts this theory (for example the timed-out frame was a real
Studio webview), drop the theory: write what the artifact shows in the PR. Do not patch the timeout.
If the cause cannot be found within the CR, name it in Known gaps with its evidence
(heavy-ci-Q3).

`findCurrentFrame` is used by most real-window steps (`waitForEditor` and the real-input harness),
so the filter must keep every one of them finding its frame. The full heavy run is that check.

### 3. Docs

- `CONTRIBUTING.md`: where it describes the integration windows, say that the trusted window runs
  as two launches, and which steps each holds (or point to the part selection in
  `trusted-suite.ts`).
- `.agents/guidelines/ci.guidelines.md` needs no change: the 15-minute launch deadline it names
  stays.

### 4. Requirements

No product behaviour changes, so no SwRS changes. The `@tests_req` markers stay in
`trusted-suite.ts`. Run `just requirements-lint` and `just requirements-update` and confirm they
produce no diff beyond what this change implies. A diagnosis that finds a product bug reopens the
CR (spec critic note in `02-answers.md`). File it as a "Known issue" per the requirements
guidelines; do not fix it here.

## Decisions carried from `02-answers.md`

- heavy-ci-Q1: the CR is added to batch-09.
- heavy-ci-Q2: the cause is fixed. Raising `STUDIO_LAUNCH_TIMEOUT_MS` (or any deadline, budget or
  `timeout-minutes`) alone, skipping or quarantining a test, or re-running until green is not a
  fix. The suite is too long for one launch, so it is split into launches, each within its
  deadline. The measured durations before and after are stated in the PR. Every test that runs
  today still runs.
- heavy-ci-Q3: the proof is a heavy run green at the PR head, twice in a row on the same head. A
  failure that cannot be fixed within the CR goes in Known gaps with its evidence, never hidden.
  Added after the CoS's fact of 2026-11-25: two green runs prove little against an intermittent
  failure, so the margin criteria of "Evidence" also apply.
- heavy-ci-Q4: the stack driver places the CR as low in the stack as it can once it is ready. It
  waits for no other CR.
- CoS fact (2026-11-25): `main` is green at 17b779d (run 45713440510). The failure is intermittent
  and close to the deadline. The goal is a reliable heavy run, not turning a red `main` green.
- heavy-ci-Q5: "under 1200 s, stated" is enough for the whole `ci-integration` step. No sharding
  into parallel jobs, no change to the probe's fixed pauses. The PR names the step's remaining
  margin (about 15 %) in Known gaps, with the two ways to widen it as a follow-up.
- heavy-ci-Q6: the bar is 600 s per trusted part. `real-input` is not split.
- heavy-ci-Q7: the frame filter and the diagnostics in the failure message are enough. No new
  stress scenario. The PR says in Known gaps that two green runs do not prove the frame lookup
  fixed.

## CI environment

The `integration` job of `.github/workflows/ci.yml`:

- Runs on `ubuntu-latest` (a fresh GitHub-hosted Linux runner): `just dev-ci`, then
  `xvfb-run --auto-servernum -s "-screen 0 2600x1440x24" just ci-integration` (step
  `timeout-minutes: 20`, `STUDIO_VIEWPORT_GUARD: strict`), then `just ci-hang-dump` and the upload
  of `out/reports/` as `e2e-integration-attempt-<n>` (job `timeout-minutes: 30`).
- VS Code is downloaded by `@vscode/test-electron` (no local VS Code). The display is Xvfb, with no
  window manager focus history. Workspace and user-data directories live in `/tmp`. The runner's
  speed varies from run to run: that variance is the cause here.
- What the local machine has that CI does not: an installed VS Code, a real display and a warm
  disk cache. The owner's machine is Windows, where the real-window suite is not the reference
  (`run-tests.ts` builds a `/tmp` workspace). Only the heavy CI run proves the timings and the
  frame filter on the CI runner.
- No job, step, target or workflow input is added or renamed, so `test/build/test_workflows.py`
  is not affected. `just ci-integration` still runs `npm run test:integration`.

## Evidence

Before the push (local, on the Driver's machine):

- `just check`: formatting, TypeScript, boundaries, file size (`trusted-suite.ts` and
  `run-tests.ts` stay under 1 500 lines), unused exports, and unit tests, including the new unit
  test that the two parts hold every step of today's trusted run exactly once, in order, and the
  distinct heartbeat and launch names.
- `just preflight` (on Windows, its static stage; CI runs the others).
- Where a real-window run is possible (Linux or macOS with a display),
  `npm run test:integration -- --trusted-only` passes and prints both parts' `STEP` lines. On the
  owner's Windows machine this is replaced by the heavy run below; say so in the PR.

Only the CI run proves (heavy-ci-Q3, plus the margin criteria):

1. Two heavy runs in a row on the same PR head, `gh workflow run ci.yml --ref <branch> -f heavy=true`,
   both with `integration` and `stress` green.
2. In each of the two runs, read from the job log (`STEP start: setup` to the last `STEP done` of
   each part):
   - each trusted part takes **at most 600 s** (two thirds of its 900 s deadline, a margin of
     300 s or more, four times the 76 s spread seen between the green and red runs);
   - the whole `just ci-integration` step stays under its 1200 s limit, with its duration stated.
3. The PR states a table of durations before and after: trusted launch, each part, `real-input`,
   `open-at-line-probe`, and the whole `ci-integration` step. "Before" comes from runs 45476952370
   and 45713440510; "after" from the two heavy runs, with their run ids.
4. Each part's log shows its own launch name in its `STEP` heartbeat context, and the full step
   list across both parts matches today's list (the `STEP done` names in the log, compared with
   the 63ef752 log).
5. `stress` stays green (its single trusted launch on the `STUDIO_REAL_INPUT_SCENARIO=stress` path
   is unchanged), so `--trusted-only` with a scenario still uses one launch.
6. The open-at-line steps pass in both runs. The PR states what the attempt-2 artifact showed, and
   that the frame filter is in place. One `locator.count` failure in hundreds of runs cannot be
   proven fixed by two runs: the PR says so.

Each criterion is checked on both runs. A run that passes but misses the 600 s margin of a part is
not a pass: rebalance the parts (move a step group between them, in order) and run twice again.

## Out of scope

- New tests or scenarios beyond the unit test of the part split; new product behaviour.
- The acceptance job of CR-505.
- Sharding `integration` into parallel CI jobs. It would change `report`, `gallery`, `pages`,
  `tag-release` and the per-attempt artifact outputs (heavy-ci-Q5).
- Shortening the fixed waits (`settle(...)`) of `open-at-line-probe` (about 180 s, mostly fixed
  pauses over 28 jumps) or of `real-input` (heavy-ci-Q5).
- Changing any deadline, budget, `timeout-minutes` or `STUDIO_LAUNCH_TIMEOUT_MS` value.

## Known gaps the PR states

- **The step's own margin** (heavy-ci-Q5). After the split, the whole `just ci-integration` step
  stays near 1000 to 1030 s against its 1200 s limit, a margin of about 15 %: each extra window adds
  about 15 s of startup. That is below CI rule 11's "about twice the healthy duration". The PR names
  the measured margin and the two follow-ups that would widen it: sharding `integration` into
  parallel CI jobs, or replacing the fixed pauses of `open-at-line-probe` (about 180 s) with
  readiness signals.
- **The frame lookup is not proven fixed** (heavy-ci-Q7). One `locator.count` failure in many runs
  cannot be proven gone by two green runs, and the open-at-line steps are not stress scenarios. The
  PR says so, and points to the frame filter and the new diagnostics in the failure message as what
  makes a next failure explain itself.
