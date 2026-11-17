# T29 implementation — round 3

STATUS: STOP

## Summary
Finding 1 was implemented as specified, but it exposes a failure in an existing integration test that
the pre-authorized settle wait does not fix. Per the task, any other failure of an existing test is a
STOP.

## Files changed (all under )
- src/webview/scrollSync.ts — `applyPreviewStatus`: `const keepPosition = window.scrollY > 0 || Boolean(editAnchor?.element);`
  and `if (keepPosition) applyAnchor();` (comment updated). `applyAnchor` untouched.
- test/webview/scrollSync.test.ts — new tests (helper `bannerPushingHarness`):
  "T29: an in-place pending status keeps an open editor still at the top of the page" and the companion
  "T29: an in-place pending status at the top of the page without an editor does not scroll" (scrollY stays 0).
- test/integration/scroll-sync-suite.ts — UNCHANGED (the settle wait was tried and removed, see below).

## Test written first, red on the pre-change tree
`AssertionError [ERR_ASSERTION]: editor block viewport top moved from 500 to 523` (banner 23 px).
(First draft measured the mapping instead of the inserted editor element and passed vacuously; fixed
before the code change.) After the change: unit 587 pass / 0 fail, contracts 2 pass.

## Gate `T29-impl3 unit types contracts full visual`
- unit, types, contracts: PASS. visual: PASS vs baseline (0 new failure lines).
- full: FAIL, scroll-sync-suite keyboard-navigation, `assert.equal(window.scrollY, 0)`: `22 !== 0`
  (logs/T29-impl3-full.log, 12 scenarios passed before it).
- I added the amended settle wait (phase "ready" and status "success" in keyboardFrame) before that
  assertion and reran: still `22 !== 0`. Diagnostic run (logs/T29-impl3-diag-full.log), polling after the
  wait at 0, 500 and 1500 ms: `scrollY=22 status=success sh=899` each time. So the 22 px is not a
  transient while the banner is visible. The page stays scrolled by 22 after the render is ready.
- Likely cause (not verified in code): with the editor open at the top, the pending banner now makes
  `applyAnchor` scroll the page by the banner height (that is the requested behaviour). The following
  ready reload keeps scrollY 22, and the banner is gone, so the keyboard-navigation flow ends scrolled
  22 px down instead of 0. Before T29 the pending page was a reload and scrollY stayed 0.
- I removed the wait and the diagnostic, so scroll-sync-suite.ts is byte-identical to the base again
  (git diff empty), and the tree compiles.

## Decision needed
Either the ready reload must restore the top position (for example when the page was scrolled only by
the banner), which is outside the Allowed files, or the keyboard-navigation expectation needs a
different treatment. I did not change either.

## Existing assertions changed
None.
