## Summary

The unit test "Auto measures a table again on a real resize while a cell is edited" failed on Windows (also on `main`), so `just preflight` was red there for every change. The test narrowed the preview pane to 760 px and expected the table to shrink, but that only holds when the table's natural width is above what a 760 px pane allows (727 px). The natural width depends on the page font: 705 px with Segoe UI on Windows (measured here); the investigation saw up to 797 px with other fonts (**UNVERIFIED** at this head). The product's re-measure on resize works as intended; the test's assumption was wrong. The test now narrows the pane to 600 px, below the table's natural width with the fonts checked.

## Deliverables

None (test-only fix). Measured at the head (390f6ed): with Segoe UI the table is 705 px wide with the pane at 1100 px and 727 px at 760 px, so the old assertion `727 < 705` failed; with the pane at 600 px the test passes.

**UNVERIFIED:** the widths of other fonts from the investigation (Verdana 797 px, Arial 722 px, Consolas 720 px at 1100 px, 568 px at a 600 px pane, and that 640 and 700 px also pass) are probe results not re-run at this head.

## Blast radius

Grade: **1**. One test changes; no product code. `git revert` restores the previous test.

## Autonomous decisions

- 600 px chosen for the narrower pane: it is below the table's natural width on every font probed (705 to 797 px, **UNVERIFIED** beyond Segoe UI), so the test should no longer depend on the platform font.

## Known gaps

- The Linux result was not run locally (Windows machine); the Linux pass is shown only by the `static` CI job of this PR.
- The font widths other than Segoe UI are unverified (see Deliverables).

<details><summary>Details</summary>

## Changes

- `test/page/tableBreakout.test.ts`: in "Auto measures a table again on a real resize while a cell is edited", `setViewportSize` width 760 becomes 600 and the fit assertion becomes `<= 600`, with a comment saying why.

## Impacts

No visual change; no user-facing change.

## Test plan

- [ ] New or changed tests: the changed test passes on Windows (6 of 6 in `tableBreakout.test.js`); it failed there before the change.
- [ ] Requirements: No behaviour change.
- [ ] Changelog: No user-facing change.
- [ ] Local gates: `npx tsc -p .` and `node scripts/node-test.mjs unit out/test/page/tableBreakout.test.js` at 390f6ed (6 of 6 pass); `just preflight` (Windows static stages) passed at a18fc89, before a clean rebase onto main that left the patch unchanged (carried from a18fc89); CI at 390f6ed: `static`, `static-windows`, `visual` pass.
- [ ] Review
- [ ] CI green

## Internal references

- CR-339 (windows-table-breakout-resize-test).

</details>
