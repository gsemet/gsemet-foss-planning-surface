# Review round 2 — workbench focus thief (test environment only)

Inspector, 2026-10-29. Worktree `markdown-okf-schema-studio-wt-198`, branch
`change-requests/198-workbench-focus-thief`, uncommitted work against `origin/main` (cb1f2adc).

## Verdict: APPROVE

No blocking item. Three recommended fixes below (1–3) are small and worth taking before the
commit; none changes behaviour.

## Scope

- 6 modified files, 7 new files, all under `test/`. `src/` untouched (`git diff --stat origin/main`).
- Modified: `test/integration/realInput/run.ts`, `reload-suite.ts`, `run-tests.ts`,
  `scroll-sync-suite.ts`, `windowFocus.ts`, `test/shared/stressPlan.ts`.
- New: `test/shared/workbenchFocusDump.ts`, `test/shared/testProfile.ts`,
  `test/shared/alertPickProbe.ts`, `test/integration/realInput/alertPickProbe.ts`, and the unit
  tests `test/build/{workbenchFocusDump,testProfile,alertPickProbe}.test.ts`.

## Checks

| Check | Result |
| --- | --- |
| No product code touched | OK: no `src/` path in the diff |
| No weakened assertion, retry, sleep, raised timeout, skipped test | OK: existing assertions unchanged; the only new bound is the 2 s diagnostic cap of the dump (failure path only); the probe uses the harness `waitFor` default (10 s) |
| Collector read-only and bounded | OK: `readWorkbenchSnapshotInPage` / `readFrameFocusInPage` only read DOM (`activeElement`, `hasFocus`, `getBoundingClientRect`, `getComputedStyle`, `textContent`); `installFocusTraceInPage` only adds passive `focusin`/`focusout`/`blur`/`focus` listeners (ring of 30); no `focus()`, click, keyboard or screenshot. Every evaluate is raced against `WORKBENCH_FOCUS_DUMP_TIMEOUT_MS` with an unref'd timer and a swallowed late rejection; never throws (unit-tested with throwing, synchronously throwing and hanging pages) |
| Untrusted window stays untrusted | OK: the untrusted launch still has no `--disable-workspace-trust` and no `security.workspace.trust.enabled`; `security.workspace.trust.startupPrompt: "never"` is kept (same as before); a unit test forbids the trust names in the profile |
| Settings real for the VS Code in use | OK: checked against local VS Code 1.143.1 (`workbench.desktop.main.js`, built-in `copilot` and `git` package.json): all 17 names exist; `workbench.secondarySideBar.defaultVisibility` enum includes `hidden` (default `visibleInWorkspace`); `update.mode` enum includes `none`; `extensions.autoUpdate: "off"` is honoured by the code (`e==="off"||e===!1||...`); `git.openRepositoryInParentFolders` enum includes `never`. The built-in Copilot extension is `GitHub.copilot-chat` (publisher `GitHub`, name `copilot-chat`, activation `onStartupFinished`), so the flag targets a real id |
| Every setting has a reason | OK: per-entry `reason` + header table; unit test requires a reason on each entry and no duplicate |
| No test depends on chat/Copilot | OK: no integration test uses chat or Copilot; tests that close the auxiliary bar keep working with it hidden by default |
| Probe asserts the user-visible outcome, cannot pass vacuously | OK: the smoke fixture has no alert; the probe waits for the text box to show `> [!TIP]` / `> [!WARNING]`, then Cmd/Ctrl+Enter, then waits for `alertPickApplied(bufferText(source), …)` (host document: `> [!TYPE]` directly above `> Second paragraph.`) and re-asserts it after the editor closes. Any step failure is rethrown with the probe line and `windowFocusReport`. Keyboard path checked against `editPalette.ts` `handleKey`: `caretIndex` starts at -1, so ArrowDown, ArrowDown, Enter picks index 1 = TIP. Mouse path uses `page.mouse` at the option's centre (main-frame coordinates from `boundingBox`), no Playwright actionability |
| Probe is stress only | OK: in `STRESS_SCENARIOS` and `STRESS_SCENARIOS_BY_HOST.trusted` (kept in sync), and in the single-scenario map; not in the integration scenario list |
| Stress cost plausible | OK: on heavy run 40801771278 the stress job took about 21.5 min for 20 rounds (about 58 s per round, `alert-dropdown` about 3.1 s, `toc` about 4.8 s). Two picks per round at about 3 s each adds about 2 min: about 23.5 min against the 30 min job timeout. Acceptable, but it is the largest single addition; watch the heavy duration |
| Compatibility with #206, #200, #193 | OK. #206 (`editorWidgets.ts`, `stepInterruption`, `editorBlurInterruption`) and #200 (`realWindowGaps.ts`, comment thread test) share no file. #193 shares `reload-suite.ts`, `run-tests.ts`, `scroll-sync-suite.ts`: `git apply -3` of this diff onto `origin/change-requests/186-stress-flakes-window-blur` (which contains #193) applies cleanly; the merged result keeps both the heartbeat/`watchLaunch`/`onSpawn` code and the profile lines. The claimed conflicts at `reload-suite.ts` and `run-tests.ts` do not occur with a 3-way apply (adjacent hunks only). The real conflicts are in `realInput/run.ts` and `stressPlan.ts` against the `toc` stress scenario that #205 adds at the same list ends: add/add, keep both entries |
| Gates | `just check`: exit 0 (node tests 3183/3183 + 69/69, pytest 80 passed, `1067 requirements, 0 errors, 0 warnings`); the new unit tests ran and passed. `uv run --group requirements okfreq validate --check-links --project-root .`: `1067 requirements, 0 errors, 0 warnings`, exit 0. Worktree unchanged afterwards |

## Recommended (non-blocking)

1. **Internal CR ids in comments that land in the PR diff.**
   `test/integration/realInput/run.ts:55` (`// CR 198: does a user's alert type pick …`) and
   `test/shared/stressPlan.ts:70` (`// CR 198: the alert type pick …`). The repo has many `CR NNN`
   comments, but these two new ones are read by the external PR reviewer; drop the `CR 198:`
   prefix (the rest of each comment already says what the entry is).
2. **The reload campaign does not get the launch flag.** `reload-suite.ts` writes the profile
   settings but its `spawn` args do not include `...testProfileLaunchArgs()`, while the header of
   `testProfile.ts` says the Copilot Chat extension is disabled "in the test windows the launcher
   starts directly or through runTests". Either append the flag to the reload spawn args (one
   line; it would merge cleanly with #193's `onSpawn` line) or narrow the header comment.
3. **Duplicate writer in the untrusted launch.** `run-tests.ts:44-46` repeats `mkdirSync` +
   `writeFileSync(JSON.stringify(testProfileUserSettings()))` instead of calling
   `writeTestProfileSettings(userDataDirectory)` like the trusted path (line 86). Same output;
   one helper keeps the two windows from drifting.

## Notes for the Driver

- Proof of the dump is by unit test of the builder and collector
  (`test/build/workbenchFocusDump.test.ts`), which the request accepts. The real proof that the
  settings remove the focus thief is still the heavy run (alert-dropdown and review-threads green,
  and the `ALERT-PICK-PROBE` lines in the stress log).
- When stacking above #205, resolve the two list-end conflicts by keeping both `toc` and
  `alert-type-pick-probe`.
- The PR body must not name the CR, the backlog item or the run of another branch by internal id.
