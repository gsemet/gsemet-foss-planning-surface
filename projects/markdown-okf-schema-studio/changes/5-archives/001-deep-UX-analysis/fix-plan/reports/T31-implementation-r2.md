# T31 implementation — round 2

STATUS: DONE

## Summary
Both review findings are addressed. H1, case A, case B and the docs sentence are unchanged.

## Files changed (round 2, test only)
- `test/integration/realInput.test.ts`
  - Finding 2 (NIT): the `captureAfter` caption in `scenarioFocusChangeKeepsPreviewStill` now says
    "the page scroll and the cell's position on screen stayed within 4 px".
  - Finding 1 (MINOR): new RI-T31b `scenarioHiddenPreviewCatchesUp`, registered after RI-T31 in `run()`.

## RI-T31b scenario
Generated document of 1500 lines (300 sections, plain headings and two-line paragraphs; the
repository fixture has only 163 lines, too short for a 200-line scroll). Steps:
1. Open the side preview; wait until it is rendered and visible.
2. Hide it by opening `other.txt` in the preview's group (`preserveFocus`); wait for `panel.visible === false`.
3. `revealRange` the source editor 200 lines down (AtTop); wait until the editor top moved by at least 150.
4. `panel.reveal(viewColumn, true)`; wait for `panel.visible`.
5. Assert (polled, 10 s) that the preview's anchor block (last `[data-sphinx-source-line]` block whose
   top is at or above the reading line) spans, within 2 lines, the editor's top line.

Measured: editor top line 196, anchor distance 1 (log line `RI-T31b: ...`).

Note for future authors: the "other editor" must not be a Markdown file. The preview follows the
active Markdown editor, so `other.md` retargeted the preview to the other file (first attempt failed
for that reason: `lastSourceScrollLine` undefined). `other.txt` hides the panel without retargeting.

## Base behaviour (reasoning only, no sources swapped)
RI-T31b passes on the base too. The base calls `restorePreviewState` on every visible
`onDidChangeViewState`, which includes the hidden -> visible transition, so the catch-up ran there
as well. The test is a regression guard for H1 (it protects the branch H1 narrowed), not a
reproduction of a bug.

## Existing assertions changed
None. Code added only. (The diagnostic probe used while debugging was removed.)

## Verification
- `PLAN/scripts/gate.sh T31-impl2 unit types full` -> compile PASS, unit PASS, types PASS, full PASS
  (log: `PLAN/logs/T31-impl2-full.log`). RI-T31 case A and B numbers unchanged
  (Y0=Y1=Y2=1200; cell top 415.17 / 415.56 / 415.56).
- Earlier runs with names `T31-impl2b/c/d` were debugging runs of the failing first attempt (b, c
  FAIL, d PASS).
