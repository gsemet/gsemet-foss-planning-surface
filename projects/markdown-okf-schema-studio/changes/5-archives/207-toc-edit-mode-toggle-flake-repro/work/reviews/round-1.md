# CR 207 — Inspector review, round 1

Verdict: **CHANGES REQUIRED**

Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-207` (uncommitted).

## Checks run

- `just check`: exit 0 (unit 3265/3265, the remaining gates green; only pre-existing W2 link warnings).
- New and touched tests, headless: `out/test/build/tocLoop.test.js`,
  `out/test/page/runtimeEditToggleRace.test.js`, `out/test/build/hangWatchdog.test.js`: 18/18 pass.
- `ci.yml` parses (PyYAML); inputs `heavy, toc_loop, toc_delay_ms, gallery`. actionlint/yamllint are
  not installed (not installed, per instructions).
- `just --dry-run ci-toc-loop '1"; echo PWNED; echo "' 0`: shows the value spliced into the bash
  source (see item 1).

## What is fine

- Default behaviour unchanged: `toc-loop` runs only on `workflow_dispatch` with `toc_loop` not empty
  and not `0`; push/PR runs and `heavy`/`stress` are untouched; `injectToggleDelay` returns 0 without
  the env var, so the shared `setEditMode` and the `toc` stress entry behave as before.
- No weakened assertion, no retry added, no `force: true`, no skipped test. The watchdog change only
  gives `toc-loop` the same launch-deadline budget as `stress`, and has a unit test.
- Workflow inputs reach the step through `env:` (no `${{ }}` inside `run:`).
- Artifact path: `toc-loop-summary.json` goes to `out/reports/e2e/`, inside the uploaded `out/reports/`;
  the artifact name `toc-loop-attempt-N` does not collide with other jobs' names.
- Loop semantics: a failed round is logged with its #205 attempt record, the loop goes on, and the
  step fails at the end if any round failed.

## Required changes

1. **Shell injection through the justfile.** The workflow passes the inputs safely to `just`, but
   `ci-toc-loop` splices `{{ ROUNDS }}`/`{{ DELAY_MS }}` into the bash source of a shebang recipe
   (the `export` line and both `echo` lines). Dry-run proof: the value `1"; echo PWNED; echo "`
   becomes `STUDIO_TOC_LOOP="1"; echo PWNED; echo ""`. Use exported parameters
   (`ci-toc-loop $STUDIO_TOC_LOOP="60" $STUDIO_TOGGLE_DELAY_MS="0":` and `"$STUDIO_TOC_LOOP"` in the
   body), or read the values from env only. You can also check them in the workflow step
   (`[[ $TOC_LOOP =~ ^[0-9]+$ ]]`) before calling just.
2. **The delay before the click makes the diagnosis wrong.** In `setEditMode`
   (`test/integration/realInput/harness.ts`), the delay sits between the state read and the click,
   so `before.state` can be up to 2 s old. Say a render changes the mode during the delay. The click
   then toggles from a mode the helper never recorded, and the failure says "click #n reached the
   toggle in the page and the page shows mode X (it showed Y before the click)". That blames the
   page for something the injected delay caused. When a delay was injected, read and record the
   state again right before the click. Log in `attempts` whether the mode or render changed with no
   click. That change is the evidence the CR is looking for (a render restored the mode). The
   failure message must report it separately from "the page ignored a click". Keep clicking so the
   wider race window stays.
3. **The theme delay is in a place where it widens nothing.** In `setHostTheme`
   (`test/integration/tocWindow.ts`), the delay comes before the wait for the theme to reach the
   webview, so it mostly overlaps theme propagation. Move it, or add a second one, after that wait.
   The gap between the theme landing in the webview and the first toggle read/click is then random
   from 0 up. That is the "render restored the mode, theme path" suspect #205 names. Fix the comment
   to match.
4. **Check `STUDIO_TOGGLE_DELAY_MS` when the loop starts.** Today a bad `toc_delay_ms` throws inside
   `setEditMode` on the first click of every round. The run then reports "N rounds, 0 clean, N
   failed" for a config error. Call `toggleDelayMaxMs()` at the top of `runTocLoop`, next to
   `tocLoopRounds()`, so the run fails before round 1, and log the parsed values.
5. **Timeouts, budget and a summary that survives.** (a) The launch deadline is 40 min
   (`2400000`) inside a 45-min job, after checkout, LFS, `just dev-ci`, compile and bundle, so the
   job timeout can fire before the watchdog writes its dump. Give the test step a `timeout-minutes`
   below the job's, keep the deadline below that, and add the `just ci-hang-dump` post-step
   (`if: always()`, before upload), like `integration` (CI rule 11). (b) `MAX_TOC_LOOP = 300` cannot
   fit in 40 min (stress manages about 20 rounds of the whole plan in 18 min, and a toc round with
   two theme switches is not cheap). Cap the input at what fits, or document the rounds per dispatch,
   and fix the input description. (c) Write `toc-loop-summary.json` after every round, not only at
   the end, so a deadline kill keeps the tally of clean and failed rounds.
6. **The focus dump is read after cleanup but labelled "after the failure".** `runTocLoop` calls
   `workbenchFocusDump` after `scenarioToc`'s `finally` has closed the editors and restored the
   theme, so it shows the empty group, not the failing step. Label it "after the scenario's cleanup",
   as `run()` does. Also capture an at-failure dump, which is what the owner asked for (#218/#220).
   For example, wrap the round with `withFocusDumpOnFailure` so the dump is read at the failing
   `setEditMode` before cleanup, or use `takeFailureFocusDump()` if it gets set.
7. **Docs.** CONTRIBUTING.md (the heavy-dispatch paragraph near line 256 and the watchdog paragraph
   near line 436, which list `ci-stress` and its deadline) and `.agents/guidelines/ci.guidelines.md`
   (on-demand real-window jobs) must mention the `toc_loop`/`toc_delay_ms` dispatch, its deadline,
   and that it is a repro tool that does not gate merges.
8. **The headless test claims more than it shows.** The docstring of
   `test/page/runtimeEditToggleRace.test.ts` concludes that "the remaining suspects are the real
   window". The tests cover rapid clicks, patches between clicks, and a boot from saved state. They
   do not cover a full re-render (theme change), or a boot where the saved state and the host's
   `initialEditMode` disagree (`src/page/runtime.ts:356`: the saved state wins). Tone the claim down
   to what is tested. Better, add the disagreement case: a reloaded webview whose saved state is
   stale is a real suspect and can be tested headless.

## Non-blocking

- Gate `injectToggleDelay` on `STUDIO_REAL_INPUT_SCENARIO === "toc-loop"`, so a stray env var can
  never slow down the normal integration job.
- `toc_loop` values such as `00` or ` 0` pass the job `if`, then fail in `tocLoopRounds` (good,
  loud). Validating in the workflow step (item 1) would catch them earlier.
- In `attempts`, the "injected ... ms" entries come before the `#n before {...}` entry of the same
  click. Push the "before" record first so the timeline reads in order.
