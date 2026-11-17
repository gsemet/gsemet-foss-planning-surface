# Diagnosis (Driver, step 1)

Question: does the review-threads Resolve-popover failure show the alert-dropdown window-blur pattern
(page focus lost, active element BODY, editor/popover closed right after a blur)?

Decision: NO (not shown by the evidence). This CR handles review-threads only, branched from
origin/main cb1f2adc. The alert-dropdown item stays separate (PR #194 / CR 180).

Evidence
- Logs examined: stress-b71fac7c.log (heavy main b71fac7c, round 9/20) and
  /private/tmp/claude-502/stress-main-b723-40778781367.log (main b723e176, round 10/20).
- Both runs predate PR #189 (768a04dc is not an ancestor of b723e176): the failure message is the bare
  Playwright text `locator.textContent: Timeout 30000ms exceeded ... waiting for
  [data-okf-comment-popover] [data-okf-comment-resolve]`. No sidecar, host, page-trace or focus dump
  exists, so neither "page focus lost" nor "active element BODY" can be read from them.
- Identical timeline in both: `PASS real-input screenshot: review-annotations/r05-thread-reply`, then 30 s
  of silence, then the timeout (b71fac7c 17:14:00 -> 17:14:31; b723 22:26:38 -> 22:27:10). One
  `[ChatModelSelection] event=no-model-at-toolbar-build` workbench line ~1 s before the timeout in both;
  nothing blur- or focus-related in either log (`grep -i blur|focus` finds none).
- Product code: the comment popover (src/page/modules/commentThreads.ts) closes on an outside
  `pointerdown`, Escape, toggle, or a re-apply that finds no thread/holder. It has no window-blur
  handler, so a window blur alone cannot close it (unlike the block editor, BLOCK-047 commit on leave).
- Failing step differs: alert-dropdown fails with a click on a dropdown option while the editor is open;
  review-threads fails after the Resolve click already succeeded (the sidecar held `resolved: true`; the
  wait is for the popover to show Reopen again).

Conclusion: same cause is unproven and not suggested. The remaining candidate is a re-apply/re-render
race around the Resolve round trip (the popover not reopened, or the page replaced). The test side
must (a) record page focus, request id and trace in the failure dump (#189 has most of it) and
(b) only redo a step when the trace proves a window blur or a page replacement happened.
