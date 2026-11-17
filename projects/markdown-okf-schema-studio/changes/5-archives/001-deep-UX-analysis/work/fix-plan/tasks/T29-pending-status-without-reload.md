# T29 — Pending status without reloading the webview

| Field | Value |
| --- | --- |
| Fixes | [UX-28](../../06-render-churn-and-scroll/UX-28-full-webview-reload-per-keystroke.md) (step 1 of 3) |
| Depends on | T13 |
| Gate | `unit trusted scroll` |
| Risk | Medium (render lifecycle, P-L5, P-N1) |
| Commit message | `perf(vscode): report pending renders without reloading the preview` |

## Goal

While the build queue is `debouncing` or `building`, the host no longer replaces the whole webview
document just to show "Preview pending". It sends a `previewStatus` message, and the runtime
updates the status region in place.

A full document assignment remains for:

- the first render, and any time no rendered document is ready in the webview;
- failures (`stale`/`error`);
- missing source;
- ready renders (until T34).

The host's `preview.webview.html` string must stay exactly what the webview would show after a
reload. Tests read it through `getActivePreviewForTests().html`.

## Context to read first

- `src/extension.ts`: `setPanelHtml`, `setStatus`, `showPending`, `handleQueueState`,
  `updatePreview`, `setMissingSource`, `createPreview`, the `previewReady` branch of
  `handlePreviewSyncMessage`, and `getActivePreviewForTests`.
- `src/preview/webview.ts`: `setPreviewStatus`, `statusMarkup`, `PREVIEW_STATUS_LABELS` (export it
  if needed).
- `src/webview/scrollSync.ts`: the message listener (`sameContext(message) && message.type === …`).

## Allowed files

- `src/extension.ts`
- `src/preview/webview.ts` (export the labels only)
- `src/webview/scrollSync.ts`
- `test/webview/scrollSync.test.ts`
- `test/integration/realInput/harness.ts` (expose the counter in a helper)
- `test/integration/realInput.test.ts` (add RI-T29)
- `test/integration/scroll-sync-suite.ts` (added by the orchestrator after review r2: only the
  setup-only settle wait before the keyboard-navigation `window.scrollY === 0` assertion)

## Steps

1. **Count assignments** (test hook, also the P-P2 budget for later tasks):
   - route **every** `panel.webview.html = …` in `extension.ts` through one function
     `assignWebviewHtml(preview | panel, html)`; grep for `webview.html =`;
   - give it a per-preview counter `htmlAssignments`;
   - expose it in `getActivePreviewForTests()` as `htmlAssignments: number`.
2. **Readiness.**
   - On a valid `previewReady` that matches the current stage, set
     `preview.readyRequestId = value.requestId`.
   - Every `assignWebviewHtml` resets `preview.readyRequestId = undefined`: the new document must
     report ready again.
3. **In-place pending.** In `handleQueueState`, for `debouncing`/`building`: when `preview.stage`
   exists and `preview.readyRequestId === preview.stage.requestId`:
   - update the host string:
     `preview.webview = { …preview.webview, html: setPreviewStatus(preview.webview.html, "pending", message) }`;
   - set `preview.status = "pending"`;
   - post
     `{ type: "previewStatus", documentId, documentVersion, requestId, status: "pending", label: PREVIEW_STATUS_LABELS.pending, message }`
     with the **current stage's** identifiers;
   - do not assign the webview html.

   Otherwise, keep `setStatus(...)` exactly as today.
4. **Runtime.** On `previewStatus` with `sameContext(message)`:
   - find `[data-sphinx-preview-status]`;
   - set its `data-sphinx-preview-status` attribute to `message.status`;
   - set the text of its `strong` to `message.label` with `textContent`;
   - set the text of its `[data-sphinx-preview-status-message]` span (create it if missing) to
     `message.message`, also with `textContent`;
   - remove its diagnostics list, if any.

   Validate that `status` is one of the six known values and that `label`/`message` are strings
   of at most 500 characters; otherwise ignore the message.
5. Do not change `updatePreview` in this task.

## Tests

**Unit** (runtime): a `previewStatus` message updates the status element's attribute and texts; a
message with another `requestId`, an unknown status, or a non-string label is ignored. Extend the
fake DOM with a status element only as needed.

**Real-input E2E**, scenario **RI-T29**:

1. Side preview on a fixture; wait for ready; record `htmlAssignments` as `A0` and the current
   frame.
2. `setRenderDelayForTests(500)`. Focus the source editor (`showTextDocument`), and type one
   character with `page.keyboard.type`.
3. Wait until the **same** frame's `[data-sphinx-preview-status]` attribute is `pending`.
4. Assert that `htmlAssignments === A0` at that moment.
5. Reset the delay and wait for ready. Assert that `htmlAssignments - A0 <= 2`, then record the
   exact delta in the note. T30 tightens it to 1.

It must fail before the fix: today the pending state assigns html. Record that.

## Expected changes to existing tests

None expected. Tests that wait for `status === "pending"` through `getActivePreviewForTests`
still see it, because `preview.status` is updated. Tests that grep `html` for the pending label
still see it, because the host string is updated.

**Amended by the orchestrator after round 1 (STOP, test mechanics).** The pending page has always
shown the in-flow status banner (about 23 px; only `success` is visually hidden). Before T29 the
banner arrived through a reload, which `withCurrentFrame` did not measure. It now appears in place
in the live frame. The host also queues a second render about 150 ms after the first ready render
of every opened document. RI-T16 (`scenarioEditModeNoReflow`) therefore measured `before` inside
that pending window: `scrollHeight` was 1005 = 982 + 23.

- **RI-T16, setup only.** Inside `measure()`, before reading the layout, wait until the current
  frame's `[data-sphinx-preview-status]` has the attribute value `success` and the host preview
  `phase === "ready"` (re-resolve the frame with `withCurrentFrame`/`waitFor`, timeout 10 s).
  Apply the same wait to both `before` and `after`. Do not change the two assertions or their
  2 px tolerance. List it in the report.
- **Pre-authorized, same class only.** Another existing real-input scenario may fail only because
  a layout measurement or a position-based locator ran while the in-place pending banner was
  visible. The evidence must show a delta equal to the banner height, or the banner present in the
  failing frame. Apply the same setup-only wait to it, leave its assertions unchanged, and list it
  with that evidence. Any other kind of failure in an existing test is still a STOP.
- No product change for the banner layout in this task (it is unchanged behaviour); a follow-up
  records it.

## Must not change

- First-render pending pages, failure and recovery pages, the missing-source page, and the
  content of the host `html` string.
- Anchoring: no extra scroll on status updates (the `scroll` gate).

## Done when

- The `unit`, `trusted` and `scroll` gates pass; RI-T29 passes.
- `rg -n "webview\.html =" src/extension.ts` shows only `assignWebviewHtml`.

## Amendment after review r2 (orchestrator)

Round 3 fixes review r2 finding 1: `applyPreviewStatus` also re-anchors at scrollY 0 when an
editor anchor is active (`window.scrollY > 0 || Boolean(editAnchor?.element)`), so an open
inline editor never moves under the caret. The plain top-of-page reading case is unchanged.

Expected fallout, pre-authorized: `test/integration/scroll-sync-suite.ts`, keyboard-navigation
check `assert.equal(await keyboardFrame.evaluate(() => window.scrollY), 0)`. It measured 22 in
round 2, while the pending banner was visible. Before that assertion only, add the same setup-only
wait as RI-T16: the current frame's `[data-sphinx-preview-status]` is `success` and
`getActivePreviewForTests()?.phase === "ready"`, with a 10 s timeout. Do not change the assertion.
List it in the report with the measured evidence. Any other failure of an existing test is a STOP.
