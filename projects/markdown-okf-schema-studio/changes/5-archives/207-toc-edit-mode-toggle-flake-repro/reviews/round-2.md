# CR 207 — Inspector review, round 2

Verdict: **APPROVE**

Worktree: `/Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-207` (uncommitted).

## Checks run

- `just check` (output to a file, exit code read directly, no pipe): **exit 0**. Unit 3266/3266
  (one more than round 1), the other suites green; only the pre-existing W2 link warnings.
- New and touched tests, headless: `out/test/build/tocLoop.test.js`,
  `out/test/page/runtimeEditToggleRace.test.js`, `out/test/build/hangWatchdog.test.js`: 19/19 pass.
- `ci.yml` parses (PyYAML); inputs `heavy, toc_loop, toc_delay_ms, gallery`; job timeout 45.
- `just --dry-run ci-toc-loop '1"; echo PWNED; echo "' 0`: the value no longer appears in the
  script body (only `$STUDIO_TOC_LOOP` / `$STUDIO_TOGGLE_DELAY_MS` references).
- No real-window test run (per instructions).

## Round-1 required changes

1. **Shell injection — fixed.** `ci-toc-loop $STUDIO_TOC_LOOP="30" $STUDIO_TOGGLE_DELAY_MS="0"`
   exports the parameters; the body only uses quoted variables. The workflow also validates both
   inputs in a separate step (`^[1-9][0-9]*$`, ≤ 40; `^[0-9]+$`, ≤ 2000 with `10#`) before `just`.
2. **Delay before the click — fixed.** After a non-zero pause, `setEditMode` re-reads the state on
   the same frame, records a mode/render change as `CHANGED WITH NO CLICK during the injected pause`,
   clicks only if the fresh state is still clickable, and the failure message reports the unclicked
   change separately before "click #n reached the toggle…". A mode reached with no click is logged.
   A second pause after the click keeps the wider window.
3. **Theme delay — fixed.** Moved after the wait for the theme to reach the webview in
   `setHostTheme`; the comment matches.
4. **Validate the delay at loop start — fixed.** `runTocLoop` calls `tocLoopRounds` and
   `toggleDelayMaxMs` before round 1 and logs both.
5. **Timeouts, budget, summary — fixed.** (a) Step `timeout-minutes: 35` < job 45, launch deadline
   30 min (`1800000`) < step; `just ci-hang-dump` post-step with `if: always()` before the upload.
   (b) `MAX_TOC_LOOP` = 40, input description and docs say "at most 40, about 30 minutes".
   (c) `toc-loop-summary.json` is rewritten after every round.
6. **Focus dump — fixed.** Each round runs under `withFocusDumpOnFailure`, so the dump is read at
   the failure before the scenario's cleanup ("at the failing step"); the post-cleanup dump is now
   labelled "after the scenario's cleanup".
7. **Docs — fixed.** CONTRIBUTING.md (heavy-dispatch paragraph and watchdog paragraph) and
   `.agents/guidelines/ci.guidelines.md` rule 13 describe the dispatch, rounds/delay bounds,
   deadline and step timeout, and state that it is a repro tool that does not gate merges.
8. **Headless test claim — fixed.** The docstring now lists what is covered and says re-render
   (theme change) and a click that never reaches the page stay open. The stale-saved-state boot case
   was added, both directions (saved state wins, then a click switches from it).

## Round-1 non-blocking items

- Gate on `STUDIO_REAL_INPUT_SCENARIO === "toc-loop"` — done, with a unit test (stray variable and
  `stress` scenario give 0 ms).
- `00` / ` 0` inputs — now rejected by the workflow validation step before `just`.
- Attempt ordering — done: `#n before` is pushed first, then the injected/unclicked entries.

## Regression hunt

No regression found. Default runs are unchanged: the toc-loop job only runs on dispatch with a
non-zero input; `injectToggleDelay` returns 0 outside the `toc-loop` scenario, so `setEditMode` and
`setHostTheme` behave as before in `integration` and `stress` (one extra `canClick` evaluation on
the same state, no extra read). The watchdog change only extends the stress budget rule to
`toc-loop`, covered by a unit test. Pauses (≤ 2 s each) stay far below the 90 s heartbeat and the
10 s `withCurrentFrame` retry window.

## Non-blocking (new)

1. If the webview frame is replaced during the injected pause, the re-read either throws a detached
   frame error (`withCurrentFrame` reruns the whole action on the new frame) or returns mode `null`
   (the click is not counted). In both cases the "changed with no click" evidence is dropped,
   although a frame replacement during the pause is itself the kind of evidence the repro wants.
   Consider recording it in `attempts` (e.g. push a note before retrying / before `continue`).
2. The `ci-toc-loop` recipe comment still talks about `ROUNDS` and `DELAY_MS`; the parameters are
   now `STUDIO_TOC_LOOP` and `STUDIO_TOGGLE_DELAY_MS`.
3. 40 rounds in 30 minutes is an estimate (no measured toc round time with delays). The per-round
   summary makes a deadline kill harmless; adjust `MAX_TOC_LOOP` after the first dispatch if needed.
4. A failed round does not run `workbench.action.closeSidebar` (only a passing round does). The
   next round may start with the sidebar open; harmless for a repro tool, but worth matching.
