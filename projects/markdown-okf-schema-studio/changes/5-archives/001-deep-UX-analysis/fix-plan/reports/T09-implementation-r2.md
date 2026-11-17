# T09 implementation — round 2

STATUS: DONE

## Summary
Fixes review r1 finding 1 only. The webview now flushes a pending debounced autosave when the page
is hidden or disposed: `pagehide` on `window`, and `visibilitychange` on `document` when
`visibilityState === "hidden"`. Both call a new `flushPendingAutosave()` which, only when
`activeBlockEdit.autosaveTimer` is set, calls the existing `postBlockEditSave(false)` (it clears the
timer). No new message type, the editor is not closed, no backtick/`${`/backslash added.

## Files changed
- src/webview/scrollSync.ts — `flushPendingAutosave` plus two listeners.
- test/webview/scrollSync.test.ts — fake `document.visibilityState`, harness `setVisibilityState`, 3 tests.

## Tests written first (failing before the fix)
- Not observed failing: the tests were added in the same step as the listeners, and I did not
  revert the fix to record a failure. Without the listeners no event handler exists, so the two
  flush tests would see zero `previewEditSave` messages.

## Tests added or changed
- pagehide flushes a pending autosave without waiting for the timer — exactly one non-final save, no `flushTimers()`, timer cleared.
- visibilitychange to hidden flushes a pending autosave without waiting for the timer — same for the document event.
- hide events post nothing when no edit is pending or the page stays visible — pagehide/hidden with no input, and visible visibilitychange after input, post no save.

## Existing assertions changed
- none

## Verification
- `gate.sh T09-impl unit types` → PASS (434 pass, 0 fail; logs/T09-impl-unit.log, T09-impl-types.log, T09-impl-compile.log)
- trusted/scroll not re-run this round (webview-only listener addition, no integration changes).

## Evidence for reviewers
- none

## Feedback addressed (rounds 2–3)
- Finding 1: flush on pagehide and visibilitychange-hidden as described. Finding 2 (NIT): unchanged.

## Open points / STOP reason
- None.
