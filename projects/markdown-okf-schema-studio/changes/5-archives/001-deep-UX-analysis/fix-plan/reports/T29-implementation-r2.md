# T29 implementation — round 2

STATUS: DONE

## Summary
Finding 1: `applyPreviewStatus` now re-measures and re-anchors after the in-place update
(`measure()`, `applyAnchor()` when the page is scrolled away from the top, `updateStickyHeadings()`),
synchronously and through `programmaticScroll`, so no `previewScroll` echo. Finding 2: `waitForRender` is
restored to its fed90bd body (`htmlAssignmentCount()` kept); no harness-wide wait remains. Finding 3:
the new unit test and real-input scenario RI-T29b were written and run red first against the unfixed
tree, then the fix was added. Finding 5: scenario formatted (settle loop extracted to a helper).

## Files changed (all under )
- src/webview/scrollSync.ts — re-anchor in `applyPreviewStatus` (plus round-1 changes).
- test/webview/scrollSync.test.ts — new unit test (plus round-1 tests).
- test/integration/realInput/harness.ts — `waitForRender` restored exactly; `htmlAssignmentCount()` kept.
- test/integration/realInput.test.ts — RI-T29 formatted, helper `waitForRenderChurnToSettle`, new RI-T29b
  `scenarioPendingKeepsReadingPosition`, RI-T16 `measure()` wait unchanged from round 1.
- src/extension.ts, src/preview/webview.ts — unchanged this round.

## Tests written first (failing before the fix)
- Unit "T29: an in-place pending status keeps the anchored block's viewport top" — red on the round-1 tree:
  `AssertionError: block viewport top moved from 250 to 273`.
- RI-T29b (`scenarioPendingKeepsReadingPosition`, 80 paragraphs, preview wheel-scrolled to scrollY 600,
  editor-to-preview sync switched off with the real anchor button so only the banner can move content) —
  red (logs/T29-impl2-red5-trusted.log):
  `block "Paragraph 15 keeps the reader busy." moved from 23.84375 to 46.234375 when pending appeared (scrollY 600 to 600, banner height 22.390625)`.
  Two earlier red runs (red3/red4) showed -145 px extra from source-to-preview sync after typing; that
  was a test-design problem (sync scroll, not the banner), so the scenario now turns anchoring off.
  Note: on the red tree the trusted run also hit RI-T10 "Timed out waiting for the editor" once (red2).

## Tests added or changed
- unit test above: banner growth of 23 px is compensated, no `previewScroll` posted.
- RI-T29b: real wheel scroll, real typing; the first visible paragraph keeps its viewport top (<= 2 px).
- RI-T29 only reformatted (NIT).

## Existing assertions changed
- None. RI-T16 `measure()` setup wait (round 1, amended task, scrollHeight legitimately includes the
  23 px banner) is kept; assertions and 2 px tolerance untouched. No other per-scenario wait was needed:
  the "moved -22 px", missed-click and detached-element failures disappeared with the fix.

## Verification
- `PLAN/scripts/gate.sh T29-impl2 unit types contracts full visual` -> unit PASS, types PASS,
  contracts PASS, full PASS (200 s), visual PASS vs baseline (0 new failures). Logs: logs/T29-impl2-*.log.
- An intermediate run (label T29-impl2, overwritten by the final run) showed scroll-suite
  keyboard-navigation `assert.equal(window.scrollY, 0)`: `22 !== 0`. Cause: unconditional re-anchor at
  scrollY 0 scrolled the page by the banner height (edit anchor branch). Fixed by re-anchoring only when
  `window.scrollY > 0`; at the very top the content moves down as with the old reload (review's own
  guidance: "at scrollY 0 ... may move down"). This is a refinement of the review's snippet.

## Evidence for reviewers
- Red logs: logs/T29-impl2-red5-trusted.log (RI-T29b), unit red excerpt above.
- RI-T29 delta line is in logs/T29-impl2-full.log (`RI-T29 html assignments for one edit: n`).

## Feedback addressed (rounds 2–3)
- Finding 1: re-anchor added (see above), with unit + real-input tests.
- Finding 2: `waitForRender` restored to fed90bd body.
- Finding 3: red-first evidence recorded without editing source (tests run against round-1 tree).
- Finding 5: formatted.

## Open points / STOP reason
- Finding 4 goes to follow-ups (late `previewReady` with same requestId).
- RI-T29b relies on switching the anchor button off; the state is per preview and disposed with the document.
