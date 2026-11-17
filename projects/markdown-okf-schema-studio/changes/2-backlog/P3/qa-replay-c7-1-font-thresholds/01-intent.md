# QA replay c7-1 depends on font and theme metrics

Type: test-flake risk · Priority: P3 · Filed 2026-11-01 from CR 228 (round 2 inspector review)

## Today

The replay `scenarioToolbarExpandKeepsFirstLinesClear` in `test/integration/qa210Replays.ts` has two
hard-coded thresholds: the expanded toolbar must be taller than 120 px (inside a `waitFor`, so it can
time out), and `besideToolbar` is a one-shot check that the first paragraph starts above the
toolbar's bottom edge. Both depend on fonts and theme metrics, so a font change on the Linux runner
could fail them for a reason unrelated to the fix. (The original c7-1 bug, the toolbar covering the
first lines, was fixed by the narrow-toolbar change; only this test robustness is left.)

## Expected

Derive the thresholds from measured elements (the toolbar collapsed height, the paragraph line
height) instead of fixed pixels, and retry the one-shot check.

Proof: the scenario passes with a changed font size or theme; it still fails on the pre-fix layout.
