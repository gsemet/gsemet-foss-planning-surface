# T29 implementation — round 1

STATUS: DONE

## Summary
In-place pending status: all `webview.html` assignments go through `assignWebviewHtml` (counter
`htmlAssignments`, readiness `readyRequestId`); `handleQueueState` updates the host string, sets
`status = "pending"` and posts `previewStatus` without assigning html when the loaded document has
reported ready for the current stage; the runtime applies `previewStatus` in place (validated).
All gates pass: unit, types, contracts, full (trusted + scroll + reload; RI-T29 ran and passed), visual.

## Files changed (all under )
- src/extension.ts: `assignWebviewHtml`; `htmlAssignments`, `readyRequestId`; ready recorded on `previewReady`; in-place pending branch; `htmlAssignments` and `webviewReady` in `getActivePreviewForTests`.
- src/preview/webview.ts: `PREVIEW_STATUS_LABELS` exported.
- src/webview/scrollSync.ts: `applyPreviewStatus` + `previewStatus` branch (sameContext, 6-value whitelist, label/message strings <= 500 chars, textContent, creates the message span, removes the diagnostics list).
- test/webview/scrollSync.test.ts: fake DOM selectors/children + 2 T29 tests.
- test/integration/realInput/harness.ts: `htmlAssignmentCount()`; `waitForRender` settle wait (see below).
- test/integration/realInput.test.ts: RI-T29; RI-T16 measure setup.

`rg "webview\.html =" src/extension.ts` matches only inside `assignWebviewHtml`.

## Important implementation finding
VS Code ignores `webview.html = <identical string>`: no document is loaded, no new `previewReady`
comes. So `assignWebviewHtml` resets `readyRequestId` and increments `htmlAssignments` only when the
string differs from the current `panel.webview.html`. Without this, readiness was lost after the
deferred enrichment re-assigns (identical html) and the in-place path was never taken after the first
re-render. Consequence: `htmlAssignments` counts effective document replacements, not calls.

## Tests written first (failing before the fix)
- None recorded. The tests were written after the production code, so there is no red-first run, and
  I did not swap sources to produce one. RI-T29 and the two unit tests were never observed failing
  against the old behaviour.

## Tests added or changed
- unit "T29: a previewStatus message updates the status region in place".
- unit "T29: invalid or foreign previewStatus messages are ignored" (other requestId, unknown status, non-string label, 501-char message).
- RI-T29 (`scenarioPendingWithoutReload`): same frame reaches `pending`, `htmlAssignments` unchanged at that moment, text "Preview pending"; then delta checked <= 2.
  **Logged delta in the final gate run: `RI-T29 html assignments for one edit: 2` (an earlier run logged 1, so it varies between 1 and 2).** The scenario first waits until the render churn after opening has settled (counter unchanged 2.5 s, phase ready, `webviewReady`).

## Existing assertions changed (setup only; no assertion or tolerance changed)
- test/integration/realInput.test.ts `scenarioEditModeNoReflow` (RI-T16): `measure()` now polls until it reads layout together with `[data-sphinx-preview-status] === "success"` and host phase `ready` (one evaluation, 10 s). Assertions and the 2 px tolerance untouched. Evidence: failure was `scrollHeight changed from 1005 to 982` (delta 23 px = pending banner; only `success` is hidden).
- test/integration/realInput/harness.ts `waitForRender` (same class, broader, please review): it now also waits until the host is `success` with an unchanged `htmlAssignments` for 600 ms (20 s timeout). Evidence: with only the RI-T16 fix, ten consecutive runs failed at varying existing scenarios (RI-T10 undo editor timeout, "selected cell moved -22 px", "Cmd/Ctrl+Enter edit to reach the source buffer", "toggled boolean to reach the source buffer", checkboxToggle "Unable to adopt element handle"). Cause: a follow-up render (about 150 ms after the first ready, and a chain after that) now shows the 23 px in-flow banner in place and shifts layout under clicks and measurements, where before it was a silent reload that the tests tolerated through detach retries. After the settle wait all scenarios pass. Assertions untouched.

## Verification
- `PLAN/scripts/gate.sh T29-impl unit types contracts full visual` -> all PASS
  (logs/T29-impl-unit.log, -types, -contracts, -full, -visual). Screen unlocked.
- `tsc` clean; no debug code left (grep).

## Evidence for reviewers
- Screenshot of the earlier RI-T16 failure: .artifacts/real-input-RQg5iN/23-edit-mode-no-reflow.png.
- Banner layout NOT changed (per instruction). Follow-up worth recording: the pending banner is 23 px in flow and shifts content when it appears/disappears in place, and a follow-up render happens right after the first one when a preview opens.

## Open points
- Late-`previewReady` edge (left as instructed): a `previewReady` of the previous document arriving after a html replacement could mark the new stage ready too early; the in-place message would then be lost to a still-loading document, while the host string stays correct. Also, if the runtime finds no `[data-sphinx-preview-status]` element it ignores the message.
- `previewStatus` in-place pending drops non-security diagnostics from the host `webview.diagnostics` (same as `setStatus` did).
- The RI-T29 settle-wait diagnostics (`lastSeen` in the error message) are intentionally kept.
