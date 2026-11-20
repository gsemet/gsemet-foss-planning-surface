# Verify CR-428 (batch-06)

Head: 9d983cbf6ea991ec180be3c3e522806f533f7f88

PR 436 (base main), `gh pr view 436 --json headRefOid` = 9d983cbf6ea991ec180be3c3e522806f533f7f88.
Rules read: `$CHANTIER rules` (project AGENTS.md, ci, pull-request guidelines and others). All
judgments below are at 9d983cb unless stated. Owner order O-80 applies (Linux report-only, Windows
the reference, Linux differences a Known gap); it replaces the spec's "within 1 px".

## Claims

1. Windows: `STUDIO_REQUIRE_CHROMIUM=1 npm run test:breakout` passes with the Windows widths. VERIFIED.
   Command (after `npm run compile`): `STUDIO_REQUIRE_CHROMIUM=1 npm run test:breakout`. Output:
   `light cases 688s 688s 688s 688s 1068W 735W 748W 338s 537s 719W 894W 824W` (dark identical, both
   "same as the Windows reference"), `unshrinkable cells 1068W 972W 1068W`, `tick matrix open 719
   narrower 568`, `tests 8, pass 8, fail 0, skipped 0`.
2. Chromium out of reach + `STUDIO_REQUIRE_CHROMIUM=1` fails with the launch error. VERIFIED.
   Command: `PLAYWRIGHT_BROWSERS_PATH=<empty folder in work/scratch> STUDIO_REQUIRE_CHROMIUM=1 npm run
   test:breakout`; exit 1, `tests 8, pass 0, fail 7, skipped 1`, each failure
   `Error: Chromium is required (STUDIO_REQUIRE_CHROMIUM=1) and cannot start: browserType.launch:
   Executable doesn't exist at <scratch>\empty-browsers\chromium_headless_shell-1248\...` (path
   shortened here: it shows the home folder). The skipped one is the pinned-font failure test, as
   the PR body's Autonomous decisions say.
3. Same empty folder without the variable skips as before. VERIFIED. `npm run test:breakout`:
   `tests 8, pass 0, fail 0, skipped 8`, exit 0.
4. Report-only path forced on Windows: `STUDIO_BREAKOUT_REPORT_ONLY=1 STUDIO_REQUIRE_CHROMIUM=1 npm
   run test:breakout`: `pass 8, fail 0`, all six report lines "same". It prints no difference
   because the Windows widths equal the reference. VERIFIED that the mode passes; the forced
   difference (a verdict flipped) was NOT reproduced by me (it needs a code edit, which I may not
   make). The coder's logs `work/gates/r2-forced-diff-report-only.log` (pass 8, "differs from the
   Windows reference (report only, light case 5)") and `r2-forced-diff-asserting.log` (pass 7, fail
   1) show it, but a coder log is not proof. The report-only path with real differences is proved
   instead by claim 5 (Linux CI).
5. Linux CI, run 44725397938 at 9d983cb: `gh run view 44725397938 --json headSha,conclusion,jobs`
   gives headSha 9d983cbf6ea991ec180be3c3e522806f533f7f88, conclusion success, `visual`, `static`,
   `static-windows`, `report`, `checks` success, push-only jobs skipped. `gh pr checks 436`: the
   same. VERIFIED. In `work/ci-visual-44725397938.log` (Grep): `test:breakout` runs after
   `test:visual`; `light cases 688s 688s 688s 688s 1068W 688s 742W 339s 542s 721W 879W 798W`
   (dark identical); `light cases: differs from the Windows reference (report only): #6 688s (Windows
   735W), #7 742W (Windows 748W), #8 339s (Windows 338s), #9 542s (Windows 537s), #10 721W (Windows
   719W), #11 879W (Windows 894W), #12 798W (Windows 824W)`; `unshrinkable cells 1068W 1000W 1068W`
   with `#2 1000W (Windows 972W)`; `tick matrix open 721 narrower 568, differs (report only off
   Windows)`; preconditions reported for the cell-edit tests; `tests 8, pass 8, fail 0, skipped 0`;
   `ci-visual: passed` (line 1381). Linux differences never failed the run: the report-only
   behaviour holds. The earlier run 44719229037 (asserting, `tests 8, pass 5, fail 3`,
   `ci-visual: FAILED`) printed the same Linux widths (light cases, unshrinkable, tick matrix
   lines identical).
6. New workflow test and recipe. `uv run --no-sync --group docs --group release --group requirements
   pytest test/build/test_workflows.py -q`: `76 passed`. Fails on the previous code: the same test's
   lookup run against `git show origin/main:justfile` prints `old has breakout: False`, and
   `origin/main:package.json` holds 0 `test:breakout`, so the test's `recipe.index(...)` /
   `scripts["test:breakout"]` would raise. VERIFIED (shown by that lookup, not by running pytest on
   the old tree).
7. Diff scope: `git diff --stat origin/main...HEAD` = CONTRIBUTING.md, justfile, package.json,
   test_workflows.py, tableBreakout.test.ts (5 files); `.github` untouched (0 lines). Assertions of
   verdicts and thresholds are unchanged in content, only wrapped in `verify(...)` (asserted when
   `process.platform === "win32"` and not forced report-only). VERIFIED.
8. Gate: `work/gates/20261120-120424.log` first line `gate CR-428 branch chantier/batch-06/cr-428-...
   head 9d983cbf6ea991ec180be3c3e522806f533f7f88`, `$ just preflight`, last line `result: pass at
   9d983cbf6ea991ec180be3c3e522806f533f7f88`. VERIFIED.
9. Review box "approved at 9d983cb": `$CHANTIER log CR-428` has "r2 approved at b4bd496d...,
   committed as 9d983cbf" (10-line log, 2026-11-20T11:04:14Z). The "committed as" SHA is the box's.
   VERIFIED.

## PR body (posted body, and work/pr-body.md)

- Renders: no images, no STALE, sections and tables well formed. The posted body differs from
  work/pr-body.md only in the three places the Driver said (run 44719229037 / d944b37 wording, the
  `at d944b37` test-plan line and the unchecked `CI green` box), which the file fixes; the file's
  values hold at the head (claims 1-8). The posted body must be updated before it is final:
  `diff` shows it still says run 44719229037 at d944b37, "dark cases were not printed" and `[ ] CI
  green`. Not a defect of the file.
- Width table (Windows and Linux, differences) matches the logs of claims 1 and 5 value by value
  (+5 +2 -15 -26, +28, +2, -47 verdict change, -6, +1). Light and dark same: shown in both logs.
- "The visual job takes a few more seconds (about 10 s on Windows)": 8.6 s Windows (`duration_ms
  8579`), 6.8 s Linux. Holds.
- Known gaps lists the Linux differences with the owner's decision. It names case 6, 7, 9-12, the
  second unshrinkable cell and the tick matrix (2 to 28 px); case 8 (+1 px) is not named, within
  the 1 px of the spec, immaterial.
- Imprecise wording (not a failure): "the tests assert the twelve verdicts and the widths on
  Windows". The tests assert the verdicts and the column thresholds (`width <= column + 1`,
  `> column + 1`), and exact widths only as printed reports ("same as the Windows reference"), on
  Windows too. Suggest "verdicts and column thresholds".
- Body claims I cannot prove: (a) "fails without it [forced difference, Windows asserting]" and
  "passes with a forced difference under STUDIO_BREAKOUT_REPORT_ONLY=1": only the coder's logs
  (claim 4); (b) "the new workflow test fails on the previous justfile, run on Windows, at 9d983cb
  (carried from 72cc569)": I showed the lookup fails on origin/main, not pytest on the old tree;
  (c) "run on Windows before the commit 9d983cb": historical, I reran at 9d983cb (claims 1-3).
  The `CI green` line and last edits were not posted yet, so the posted text is not checked for them.

VERIFIED
