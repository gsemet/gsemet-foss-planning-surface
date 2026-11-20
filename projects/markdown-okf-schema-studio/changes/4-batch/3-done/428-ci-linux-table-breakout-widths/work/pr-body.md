## Summary

The table breakout tests check, in a real Chromium page, which preview tables break out of the
688 px text column and which stay in it. They draw their pages in pinned KaTeX fonts, and their
twelve reviewed verdicts were measured on Windows only: the `static` jobs run them through
`just check`, but those machines have no Chromium, so every test skipped.

The Linux `visual` CI job, which installs Chromium, now runs these tests on every pull request and
every push to `main`, and prints the widths and verdicts it measures. A Chromium that cannot start
there fails the job instead of skipping the tests. The Linux widths are not those of Windows (see
the table below), so, by the owner's decision, Windows stays the reference: the tests assert the
twelve verdicts and the column thresholds on Windows, unchanged, and are report-only on Linux, where
they print each difference from the Windows reference and never fail on it.

## Deliverables

`just ci-visual`, the recipe the `visual` job calls, runs the width tests after the visual stage;
both always run, and the recipe passes only when both pass:

```bash
failed=0
npm run test:visual || failed=1
STUDIO_REQUIRE_CHROMIUM=1 npm run test:breakout || failed=1
if [ "$failed" = 0 ]; then echo "ci-visual: passed"; else echo "ci-visual: FAILED" >&2; ...
```

Each run prints the widths it measured (Node test runner diagnostics, also kept in
`out/reports/breakout/tests-breakout.xml`, which the job uploads). `W` breaks out of the 688 px
column, `s` stays in it. Windows: a local run of `npm run test:breakout` with
`STUDIO_REQUIRE_CHROMIUM=1`, on this patch; Linux: the `visual` job of this pull request, run
44725397938, on this patch before a clean rebase onto `main`, which prints the same values as the earlier run 44719229037. Light and
dark give the same values on both platforms.

| Measure | Windows | Linux | Difference |
| --- | --- | --- | --- |
| Cases 1-4 | 688s 688s 688s 688s | 688s 688s 688s 688s | 0 0 0 0 |
| Cases 5-8 | 1068W 735W 748W 338s | 1068W **688s** 742W 339s | 0 **-47, verdict changes** -6 +1 |
| Cases 9-12 | 537s 719W 894W 824W | 542s 721W 879W 798W | +5 +2 -15 -26 |
| Cells that cannot shrink | 1068 972 1068 | 1068 1000 1068 | 0 +28 0 |
| Tick matrix, cell editor open | 719 | 721 | +2 |
| Tick matrix, after a resize to 600 px | 568 | 568 | 0 |

What the tests do, by platform and by `STUDIO_REQUIRE_CHROMIUM`:

| Where | Widths and verdicts | Chromium cannot start |
| --- | --- | --- |
| Windows | verdicts and column thresholds asserted (unchanged); widths printed and compared to the reference | skip; fail with `STUDIO_REQUIRE_CHROMIUM=1` |
| Linux (the `visual` job) | printed, each difference from the Windows reference reported, never a failure | fail (`STUDIO_REQUIRE_CHROMIUM=1`) |
| `just check`, the `static` jobs (no Chromium) | not measured | skip, "no Chromium can start here", as before |

Off Windows, some checks still fail the run: the 688 px column, the pinned fonts loaded, one table
per case and the Full-width cleanup. The cell-edit tests that start from a table that breaks out
(or fits) report a precondition that does not hold on Linux and stop there, without failing.

## Changes

- `test/page/tableBreakout.test.ts`: with `STUDIO_REQUIRE_CHROMIUM=1`, a Chromium that cannot
  start fails the test with the launch error (in the two width tests and the helper the cell-edit
  tests share) instead of skipping it. The tests print their measured widths with `t.diagnostic`.
  Verdict and column-threshold assertions run on Windows; elsewhere they print "differs from the
  Windows reference" for each difference instead of failing. `STUDIO_BREAKOUT_REPORT_ONLY=1` forces the
  report-only path on Windows, for testing it. No case, verdict, threshold, tolerance, column or
  pane changes. The tick matrix comment names both values (719 on Windows, 721 on Linux).
- `package.json`: new script `test:breakout`, spec report to the console and JUnit report to
  `out/reports/breakout/tests-breakout.xml`.
- `justfile`, recipe `ci-visual`: runs `test:breakout` with `STUDIO_REQUIRE_CHROMIUM=1` after
  `test:visual`, even when that one failed. `.github/workflows/ci.yml` does not change.
- `test/build/test_workflows.py`: a new test reads the shipped `ci-visual` recipe and `package.json`
  and checks that the recipe runs the width tests with Chromium required, after the visual stage.
- `CONTRIBUTING.md`: what `just ci-visual` runs now includes the width tests, which assert on
  Windows and are report-only on Linux; the `static` jobs skip them for lack of Chromium.

## Impacts

No visual change: CI and test harness only. The `visual` job takes a few more seconds (about 10 s
on Windows) and goes red when Chromium cannot start or a check that holds on every platform fails.
No product code changes.

## Blast radius

The `visual` job is part of the required checks; a width difference on Linux does not block a
merge, a Chromium that cannot start does. A `git revert` restores the previous job.

Grade: 2

## Autonomous decisions

- The widths stay printed on every run, in the job's log and its JUnit report, rather than only in
  this description, so a later drift is visible without a new measurement.
- The test that makes the pinned font fail on purpose still skips without Chromium, even with
  `STUDIO_REQUIRE_CHROMIUM=1`: only the width and cell-edit tests are required to run.
- Report-only is chosen by platform (`win32` asserts), not by a CI variable, so a Linux developer
  sees the same report as CI.

## Known gaps

- Linux widths differ from Windows, and the verdicts hold on Windows only: case 6 stays in the
  column on Linux (688s) where it breaks out on Windows (735W); cases 7, 9, 10, 11 and 12, the
  second cell that cannot shrink and the open tick matrix move by 2 to 28 px (runs 44719229037 and
  44725397938). Not fixed here: by the owner's decision Linux is report-only and Windows stays the
  reference.
- The new workflow test is not shown failing on the previous code by a run: the recipe step and the
  `test:breakout` script it looks up are absent from `main`'s `justfile` and `package.json`
  (7644edd), so its lookups would raise, but pytest was not run on that tree.
- The forced-difference runs were not repeated on the committed patch: with a verdict changed by hand, a local
  run passed under `STUDIO_BREAKOUT_REPORT_ONLY=1` and failed without it, before the commit. The
  Linux `visual` run 44725397938 shows the report-only path with real differences instead.

## Test plan

- [x] New or changed tests: the new workflow test passes on this patch (`test_workflows.py`, 76
      passed). **UNVERIFIED:** that it fails on the previous code: its lookups find neither the
      recipe step nor the script in `main`'s `justfile` and `package.json` (7644edd), but pytest was
      not run on that tree
- [x] Requirements: No behaviour change (CI and test harness only; the test markers are unchanged)
- [x] Changelog: No user-facing change
- [x] Local gates: `just preflight` (its static stage on Windows, which runs `just check`) passes
      on this patch, carried to `9f17229` by a clean rebase; on Windows, `STUDIO_REQUIRE_CHROMIUM=1 npm run test:breakout` passes
      8 of 8, also with `STUDIO_BREAKOUT_REPORT_ONLY=1`, and with Chromium out of reach fails naming
      the launch error (it skips all 8 without `STUDIO_REQUIRE_CHROMIUM`). **UNVERIFIED:** with a
      verdict changed by hand, it passes under `STUDIO_BREAKOUT_REPORT_ONLY=1` and fails without it
      (local logs before the commit, not repeated on the committed patch)
- [x] Review: approved on this patch, carried to `9f17229` by a clean rebase
- [x] CI green at `9f17229` (`gh pr checks 436`): `checks`, `report`, `static`, `static-windows`
      and `visual` pass (run 44731420675; earlier run 44725397938 on this patch before the rebase); the `visual` log prints the Linux widths, each difference
      from the Windows reference, and `ci-visual: passed`. The push-only jobs skip on a pull request

## Internal references

- Follow-up of the pinned-font change of the table breakout tests (#429), built on the font-load
  hang fix (#433).
- CR-428 ci-linux-table-breakout-widths. Forced-difference logs: `work/gates/r2-forced-diff-report-only.log`
  and `work/gates/r2-forced-diff-asserting.log`; CI logs: `work/ci-visual-44719229037.log`,
  `work/ci-visual-44725397938.log`; gate log `work/gates/20261120-120424.log`.
