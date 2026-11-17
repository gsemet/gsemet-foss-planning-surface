# T31 review — round 2

Base: fed90bd. Scope of this round: the new RI-T31b `scenarioHiddenPreviewCatchesUp` and the caption fix
in `test/integration/realInput.test.ts`. Source (`src/extension.ts`) is unchanged since round 1.

## A. Scope
- Only `test/integration/realInput.test.ts` changed this round, adding code only. It is an allowed file.
  No frozen behaviour is touched.

## B. Correctness
- The caption fix (round-1 NIT) is done.
- H1 is unchanged. `wasVisible` plus `becameVisible` still calls `restorePreviewState` on hidden → visible.

## C. Tests: is RI-T31b a real guard for the hidden → visible catch-up?
Setup checks:
- Hidden panel: yes. `other.txt` is opened in `panel.viewColumn` with `preserveFocus`, then
  `waitFor(!panel.visible)`. Using a `.txt` file avoids retargeting the preview, which is a sound choice.
- Editor scroll while hidden: yes. `revealRange` happens after the hide, it is awaited (>= 150 lines),
  and there is a 300 ms settle.
- Polling: the scenario uses `waitFor` (10 s), the assertion is non-trivial (an anchor-span distance of
  2 lines or less, with infinity when no block is found), and the editor really moved, so the check is
  not vacuous.
- Cleanup: `withDocument` calls `closeAllEditors()` and `fixture.dispose()`. `other.txt` is written
  inside the fixture directory (`path.dirname(document.uri.fsPath)`), so it is removed with the
  fixture, and its editor is closed by `closeAllEditors`. OK.

The problem is that the test does not depend on the catch-up.
- The panel is created with `retainContextWhenHidden: true` (extension.ts ~2393).
- `syncEditorToPreview`, which is wired to `onDidChangeTextEditorVisibleRanges` (~2450), has no
  `panel.visible` check. It posts `sourceScroll` to the panel whatever its visibility.
- A retained hidden webview stays alive and receives `postMessage`. VS Code hides retained webviews
  with `visibility: hidden` on the overlay, so layout is kept and the webview's scroll handler can
  apply the anchor while the panel is hidden.
- So the 200-line editor scroll most likely already reaches the preview while it is hidden. On reveal,
  the preview is already at the right line, whether or not `restorePreviewState` runs.
- The report confirms only that the test passes on base, and base also runs the catch-up. Nobody ran
  the test with the hidden → visible branch removed. Its failing power is therefore unproven, and by
  the reasoning above it is very likely nil.

Check C.11 (a test that would pass without the behaviour is not evidence) fails for the purpose of
this round, which was to add a P-N1 regression guard.

## D. Regressions
- The gates pass (compile, unit, types, full; logs `T31r2-*`). RI-T31 case A/B numbers are unchanged.
- P-N1: the behaviour is preserved by reading, but it is still not guarded. P-N2 and R7/D-18 are
  unchanged since round 1.

## Findings
1. [MAJOR] `test/integration/realInput.test.ts`:`scenarioHiddenPreviewCatchesUp`. The test is very
   likely to pass with the hidden → visible `restorePreviewState` call removed, because the retained
   hidden webview already receives `sourceScroll` from `syncEditorToPreview`. Required:
   - Temporarily delete the `if (becameVisible) restorePreviewState(preview)` call locally, run
     RI-T31b, and put the failing excerpt in the report. Then restore the call.
   - If the test does not fail, make it depend on the catch-up. Options:
     - (a) Assert through a test hook that a `sourceScroll`/restore is posted on the transition. For
       example, count the `restorePreviewState` calls via a `...ForTests` counter, or record the
       posted messages after `panel.reveal`.
     - (b) Make the hidden-phase messages not reach the webview. For example, scroll the editor in a
       way that does not update the preview while hidden (such as a stale anchor set via an existing
       test hook), then reveal.
   - Option (a) is the simplest real guard.

VERDICT: CHANGES REQUESTED
