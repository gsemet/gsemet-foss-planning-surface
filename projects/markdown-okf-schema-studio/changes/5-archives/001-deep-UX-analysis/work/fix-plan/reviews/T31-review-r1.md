# T31 review — round 1

Base: fed90bd · Reviewed diff: 3 files, about +90/-1

## Gates
compile PASS, unit PASS, types PASS, full PASS (trusted, scroll, reload) — `logs/T31-impl-full.log`.
No new failure compared with the T00 baseline.

## Done-when
- [x] unit, trusted and scroll gates pass — evidence: `logs/T31-impl-*.log`.
- [x] RI-T31 passes with before/after numbers. Case A: Y0=Y1=Y2=1200, before and after H1. The report
  says plainly that UX-29 case 1 did not reproduce. Case B: the cell top was 415.17 before the
  click, 415.56 at 100 ms, and 415.56 with the editor open.
- [x] The docs sentence was added under R6.

## Decision on H1: keep it
- `syncEditorToPreview` runs on every `onDidChangeTextEditorVisibleRanges` and posts to every
  matching preview. It has no visibility check. So while the panel is visible with anchoring on,
  each editor scroll already reaches the preview. An active → visible catch-up adds nothing.
- With anchoring off, `restorePreviewState` returns early because of the
  `scrollPreviewWithEditor` guard. So the old focus-change path did nothing in that case. No user
  behaviour is lost there.
- When the panel only regains focus, the one thing the old path could do was re-take ownership for
  the editor. It overrode a preview-led anchor with the floored editor top line, which is the
  mechanism UX-29 describes. H1 also matches the documented intent of `restorePreviewState`.
- Hidden → visible still calls `restorePreviewState`. `wasVisible` starts at `panel.visible` and is
  updated on every event, so the logic is correct.

## Protected features checked
- P-N1 (R4–R6 and the hidden-panel catch-up): the scroll suite passes unchanged. The
  hidden → visible branch is kept, and the code is correct by reading. No test exercises the
  transition itself: `restorePreviewStateForTests` calls `restorePreviewState` directly and skips
  the handler. See finding 1.
- P-N2: untouched; still covered by the scroll suite.
- R7 / D-18 (T18 anchor): case B measures the selected cell's viewport top, which R7 keeps fixed.
  The table is at least 250 px below the frame top, which is stricter than the 150 px required.
  - The same locator is used for all three samples: `td` whose text is exactly "tracker". The cell
    stays in the DOM.
  - The 100 ms sample would catch the bug sheet's 178 px early jump, so the test is not weaker
    than case 2.

## Findings
1. [MINOR] `src/extension.ts`:`createPreview`. The hidden → visible branch of
   `onDidChangeViewState` has no automated test. Follow-up: add an integration scenario that does
   the following.
   - Open the side preview, then open another editor in the preview's group so the panel is hidden.
   - Scroll the source editor by 200 lines.
   - Reveal the panel again (`panel.reveal`, or reopen it from the tab).
   - Assert that the preview's anchor line is within 2 lines of the editor's top line.
2. [NIT] `test/integration/realInput.test.ts`:`scenarioFocusChangeKeepsPreviewStill`. The
   `captureAfter` caption says "scrollY stayed within 4 px". Case B now measures the cell's viewport
   top, so the caption should say that.

## Existing assertions changed
None. (`git diff fed90bd -- test/` adds code only.)

VERDICT: PASS
