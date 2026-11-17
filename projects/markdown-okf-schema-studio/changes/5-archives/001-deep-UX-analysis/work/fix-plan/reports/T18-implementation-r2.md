# T18 implementation — round 2

STATUS: DONE

## Summary
Round 1 left the 460 px table toolbar partly under the sticky band. Cause: the reveal ran once, then the status line wrapped ("Saving Markdown…"), the bar grew, and the R7 anchor restore pushed its top back up (measured barTop 13.7 against band bottom 30.6). The reveal now re-runs after anchor restores when the bar size changes, and measures the real band bottom and the preview controls. capture.py got the strict check first.

## Files changed (under )
- test/visual/capture.py — strict check: usableTop = visible sticky band bottom (else 0); fails "table action bar is hidden under the sticky band or preview controls" if barTop < usableTop - 1 or elementFromPoint at the centre of any [data-sphinx-table-operation] button lands outside the toolbar. New bottom <= tableTop + 1 and covered == 0 checks kept.
- src/webview/scrollSync.ts — new `toolbarUsableTop(bar)` (max of reading offset, measured band bottom, preview controls bottom + 4 when they overlap the bar horizontally). `revealTableToolbar` uses it, refreshes the `anchor` line after its scroll (MINOR 3). `applyAnchor` (edit-anchor branch) re-calls the reveal when the toolbar height changed (`edit.tableMenuHeight`), which also covers the first appearance. A user scroll or a cell switch with an unchanged bar never moves the page. The explicit call after insertion was removed (applyAnchor does it).
- test/webview/scrollSync.test.ts — helper `openTableForToolbarReveal` now exposes a mutable bar rect; one new test.
- test/integration/realInput.test.ts — RI-T18: fixed 300 ms sleep replaced by `waitFor` on a stable cell top (NIT 4).

## Tests written first (failing before the fix)
- capture.py strict check against the round 1 code: visual gate FAIL, 2 new lines (08-okf-schema dark/light, which includes the edit-table-wrapped-*-460 case): `table action bar is hidden under the sticky band or preview controls: {'barTop': 13.65, 'barBottom': 90.05, 'usableTop': 30.59, 'controlsBottom': 50, 'unreachable': 0}` (log of that run: logs/T18-impl-visual.log at the time; overwritten by the final run).
- Unit "a later layout change that pushes the toolbar above the reading offset is revealed again": new behaviour; round 1 code had no reveal in applyAnchor, so scrollY would stay 300.

## Tests added or changed
- Unit test above: bar grows and ends at top 20 under a 65 px offset, so scroll goes up by exactly 45; a further pass with unchanged bar size does not move the page.
- Existing reveal tests (exact delta, already visible, cell would leave viewport) pass unchanged.

## Existing assertions changed
- None this round (helper return value extended only).

## Verification
- `PLAN/scripts/gate.sh T18-impl unit types trusted visual` → compile/unit (507 pass)/types/trusted (incl. RI-T18) PASS; visual PASS vs baseline, 0 new failure lines, with the strict check active (logs/T18-gate-r2.out, logs/T18-impl-visual.log).

## Evidence for reviewers
- logs/visual-T18-impl/edit-table-wrapped-dark-460.png (and light): I viewed the dark one; the bar (Row +, Row −, Col +, Col −) is fully visible below the band, nothing under the preview controls, the table below it.
- scenarios.ts untouched.

## Feedback addressed
- BLOCKER 1: capture.py strict check added, failure demonstrated, now passes.
- BLOCKER 2: bar re-revealed after layout changes using measured band/controls bottom; unit test added.
- MINOR 3: anchor line refreshed after the reveal scroll.
- NIT 4: waitFor on stable cell top.

## Open points
- The re-reveal in applyAnchor triggers only when the bar height changes, to avoid page jitter on manual scroll or cell switches.
