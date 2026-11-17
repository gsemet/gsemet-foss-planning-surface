# T31 implementation — round 1

STATUS: DONE

## Summary
UX-29 case 1 did not reproduce before the change: case A (wheel the preview, click into the editor,
type) gave Y0=Y1=Y2=1200 before any fix. H1 is applied and kept for review: `restorePreviewState`
now runs only on a hidden -> visible transition (P-N1 still passes in the full gate). Under the
orchestrator's amendment, case B no longer measures scrollY (the in-flow toolbar legitimately
scrolls the page, T18 R7); it measures the clicked cell's viewport top.

## Files changed
- `src/extension.ts` — `createPreview`: `wasVisible` tracking; catch-up only on hidden -> visible (H1).
- `test/integration/realInput.test.ts` — RI-T31 (`scenarioFocusChangeKeepsPreviewStill`), registered last in `run()`; `node:fs`/`node:path` imports.
- `docs/scroll-anchoring.md` — one sentence under R6: a panel that only changes focus keeps its anchor; only a hidden panel that becomes visible catches up with the editor.
- Temporary diagnostic logging used in the first attempt was removed (nothing left).

## Tests written first (failing before the fix)
- RI-T31 as first written: case A passed before the fix (`Y0=1200 Y1=1200 Y2=1200`); case B measured
  scrollY and failed (`1600 -> 1658`) with and without H1, resolved by the orchestrator as the R7
  anchor (test mechanics). No test failed because of the H1 bug, because it did not reproduce.

## Tests added or changed
- RI-T31 case A (unchanged): preview scrollY within 4 px after clicking the editor and after typing.
- RI-T31 case B (metric changed under the amendment, scrollY -> clicked cell's viewport top): table
  wheeled to at least 250 px below the frame top; cell top measured before the click, 100 ms after,
  and with the cell editor open; both deltas <= 4 px.

## Existing assertions changed
- None.

## Verification
- `PLAN/scripts/gate.sh T31-impl unit types full` -> compile PASS, unit PASS, types PASS, full PASS
  (log: PLAN/logs/T31-impl-full.log; includes trusted, scroll, reload).
- Case A: Y0=1200 Y1=1200 Y2=1200 (UX-29 case 1 did not reproduce before the change).
- Case B cell top: before=415.17, after100ms=415.56, editorOpen=415.56 (deltas 0.39 px each).

## Evidence for reviewers
- Screenshot `26-focus-change-still` in the real-input evidence folder.
- Round 1 host log: no scroll message followed the cell click.

## Open points
- H1 is kept for review; it did not change any measured number.
