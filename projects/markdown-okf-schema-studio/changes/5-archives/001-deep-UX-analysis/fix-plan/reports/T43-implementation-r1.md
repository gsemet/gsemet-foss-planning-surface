# T43 implementation — round 1

STATUS: DONE

## Summary
A pending render over an already rendered page no longer touches the webview document. `handleQueueState` only sets `status = "pending"`, arms a 1500 ms timer (`PENDING_OVERLAY_DELAY_MS`), and posts `previewPendingOverlay`. The runtime then shows a fixed, pointer-transparent `[data-sphinx-preview-pending-overlay]` below the toolbar. The ready render replaces the page as before, which removes the overlay. T29's `assignWebviewHtml` / `htmlAssignments` / `readyRequestId` pieces were reused; its in-place banner and re-anchoring code were not. The first-render pending page, stale/error pages and the missing-source page are unchanged.

## Files changed
- `src/extension.ts`
  - `assignWebviewHtml` is the single funnel, so `webview.html =` appears only inside it. It keeps the `htmlAssignments` counter and resets `readyRequestId` when the string changes.
  - New fields: `readyRequestId`, `shownStatus`, `pendingOverlayTimer`, `pendingOverlayDue`, `pendingOverlayVisible`, `pendingOverlayMessage`, `pendingOverlayShown`.
  - New helpers: `armPendingOverlay`, `showPendingOverlay`, `postPendingOverlay`, `clearPendingOverlay`, `endPendingOverlay`.
  - `previewReady` records `readyRequestId` and posts a due or re-armed overlay.
  - The PlantUML deferred update uses `shownStatus ?? status`.
  - `getActivePreviewForTests()` exposes `htmlAssignments`, `webviewReady`, `pendingOverlayVisible` and `pendingOverlayShown`.
- `src/preview/webview.ts` — `PREVIEW_STATUS_LABELS` exported.
- `src/preview/previewStyles.ts` — overlay rule only.
- `src/webview/scrollSync.ts` — `applyPendingOverlay` and the message-listener branch.
- `test/webview/scrollSync.test.ts`, `test/webview/previewStyles.test.ts` — unit tests.
- `test/integration/realInput.test.ts`, `test/integration/realInput/harness.ts` — RI-T43 and `htmlAssignmentCount()`.

## Tests written first (failing before the fix)
- Unit (`T43-red-unit.log`): 5 new tests failed, no others:
  - `T43: the pending overlay message creates one overlay, outside the content` — `0 !== 1`
  - `T43: a second pending overlay message updates…`
  - `T43: visible false removes the pending overlay`
  - `T43: invalid or foreign pending overlay messages are ignored`
  - `T43: the pending overlay is fixed, pointer-transparent and never in flow` — `the pending overlay rule exists`
- RI-T43 against the old pending path (the handleQueueState branch was temporarily disabled with an env toggle, since removed; `T43-red-trusted.log`): `AssertionError: one html assignment for a fast edit  3 !== 1`. Today's behaviour is debouncing, building and ready, i.e. 3 assignments per edit.

## Tests added or changed
- 4 runtime tests:
  - the message creates one overlay, appended to `body`, with `role=status`, `aria-live=polite`, a `strong` and a `span`, and the content children are unchanged;
  - a second message updates the overlay;
  - `visible:false` removes it;
  - a foreign `requestId` or `documentVersion`, a non-boolean `visible`, non-string or over-500-character texts are ignored.
- 1 style test: the rule has `position: fixed`, `pointer-events: none` and `max-width`, and the label and message are `display: block`.
- RI-T43, real keyboard and mouse:
  - Fast edit: exactly 1 assignment and no overlay.
  - Slow edit (render delay 6 s): the pending status shows with 0 assignments and the same page, and the paragraph top is unchanged (<= 1 px).
  - After 1.5 s the overlay is visible in the same frame, below the toolbar, with the label and message on two lines, and the paragraph is still unchanged.
  - The ready render adds exactly 1 assignment, and the overlay is gone.
  - Screenshot `43-pending-overlay`.

## Existing assertions changed
- None.

## Verification
- `gate.sh T43-impl unit types contracts trusted full` — unit, types and contracts PASS; `full` PASS (`T43-impl-full.log`, 274 s).
- `trusted` failed in that run on the known flake, checkboxToggle "Timed out waiting for one undo to restore the original source" (`T43-impl-trusted.log`). It is the only failure.
- `gate.sh T43-impl-rerun trusted` — PASS (`T43-impl-rerun-trusted.log`).
- `rg -n "webview\.html =" src/extension.ts` shows only the two lines inside `assignWebviewHtml`.
- Visual level: not run (the orchestrator runs it).

## Evidence for reviewers
- Measured RI-T43 deltas, same in `T43-impl-full.log` and `T43-impl-rerun-trusted.log`:
  - `RI-T43 fast edit html assignments: 1`
  - `RI-T43 slow edit: assignments 0, paragraph shift 0 px`. The slow edit gets its single assignment (+1) only when the ready render lands, as asserted at the end of the test.
- Screenshot: `.artifacts/real-input-*/43-pending-overlay.png`, newest directory (derived folder).
- The first red/debug runs are in `T43-dbg-trusted.log`.

## Open points / STOP reason
- RI-T43 uses a render delay of 6 s instead of the 3 s in the task, so the screenshot fits between the overlay (1.5 s) and the ready render.
- `assignWebviewHtml` clears the overlay timer only when the string changes, because VS Code ignores an identical assignment. A first version cleared it on every call and the timer never fired, because something re-assigns the same html while pending. `endPendingOverlay` therefore runs explicitly in the ready and failed branches of `handleQueueState` and posts `visible:false` when the overlay stays in a loaded page (stale to stale with identical html).
- If something replaces a rendered page with a changed string during a pending render (for example link-enrichment html), the overlay is re-armed on the next `previewReady`.
- The task's "Context" mentions `isPreviewSyncMessage`. It is untouched, because `previewPendingOverlay` is a host-to-webview message only.
