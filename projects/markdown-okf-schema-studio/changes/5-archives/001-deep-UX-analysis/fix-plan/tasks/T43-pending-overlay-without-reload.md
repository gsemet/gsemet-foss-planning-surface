# T43 — Pending renders without a reload; delayed overlay banner (replaces T29)

| Field | Value |
| --- | --- |
| Fixes | [UX-28](../../06-render-churn-and-scroll/UX-28-full-webview-reload-per-keystroke.md), step 1 |
| Decisions | D-22, which supersedes T29's in-flow design |
| Depends on | T41 |
| Gate | `unit types contracts full visual` |
| Risk | Medium: render lifecycle (P-L5), scroll stability (P-N1), message protocol |
| Commit message | `perf(vscode): keep the preview still while a render is pending` |

## Goal

Today every edit assigns the whole webview document twice:
- once to show "Preview pending", through `handleQueueState` → `setStatus("pending")` →
  `setPanelHtml`;
- once when the render is ready.

After this task, a pending render never assigns the document while a rendered page exists:
- the previous render stays visible and still;
- if the render is still pending after `PENDING_OVERLAY_DELAY_MS = 1500`, the host posts a message,
  and the runtime shows a floating overlay banner that does not move any content;
- the next ready render replaces the page, as today, which removes the overlay.

Expected result: one document assignment per edit burst instead of two, no 23 px jump, and no
flash of the pending page.

## Context to read first

- `src/extension.ts`:
  - `setPanelHtml`, `setStatus`, `showPending`, `handleQueueState`, `updatePreview`;
  - `setMissingSource`, `createPreview`, `disposePreview`, `switchPreviewDocument`;
  - the `previewReady` branch of `handlePreviewSyncMessage`;
  - `isPreviewSyncMessage`, `getActivePreviewForTests`.
- `src/preview/webview.ts`: `PREVIEW_STATUS_LABELS`. Export it if needed.
- `src/preview/previewStyles.ts`: the `[data-sphinx-preview-toolbar]` rules (fixed position near
  line 206), for placing the overlay below the toolbar.
- `src/webview/scrollSync.ts`: the message listener (`sameContext(message) && message.type === …`).
- `logs/T29-blocked.patch`. T29's **steps 1–2** were reviewed and accepted:
  - `assignWebviewHtml` with its `htmlAssignments` counter;
  - `readyRequestId` readiness.

  You may reuse that code. **Do not** reuse its in-place status update of the in-flow banner, nor
  its re-anchoring code: D-22 makes them unnecessary.

## Allowed files

- `src/extension.ts`
- `src/preview/webview.ts`: export the labels only
- `src/preview/previewStyles.ts`: the overlay rule only
- `src/webview/scrollSync.ts`
- `test/webview/scrollSync.test.ts`, `test/webview/previewStyles.test.ts`
- `test/contracts/*`, only if the message-protocol contract lists message types
- `test/integration/realInput/harness.ts`, to expose the counter in a helper
- `test/integration/realInput.test.ts`, to add RI-T43

## Steps

1. **Count assignments.** Route every `panel.webview.html = …` in `extension.ts` through one
   function, `assignWebviewHtml(preview | panel, html)`, with a per-preview counter
   `htmlAssignments`. Expose it as `htmlAssignments: number` in `getActivePreviewForTests()`. This
   is T29 step 1.
2. **Readiness.**
   - `preview.readyRequestId` is set by a valid `previewReady` that matches the current stage.
   - It is reset by every `assignWebviewHtml`.

   This is T29 step 2.
3. **Pending without a reload.** In `handleQueueState`, for `debouncing` and `building`:
   - **If a rendered page exists** (`preview.stage` is defined):
     - set `preview.status = "pending"`;
     - **do not** assign the html, and **do not** change `preview.webview.html`: the host string
       stays what the webview shows;
     - arm the overlay timer (step 4) if it is not already armed.
   - **Otherwise** (no rendered page yet): keep `setStatus(...)` exactly as today.
4. **Overlay timer.**
   - One timer per preview, `PENDING_OVERLAY_DELAY_MS = 1500`.
   - When it fires while `preview.status === "pending"` and the stage is unchanged, set
     `preview.pendingOverlayVisible = true` and post this message, with the current stage's
     identifiers:

     ```
     { type: "previewPendingOverlay", documentId, documentVersion, requestId, visible: true,
       label: PREVIEW_STATUS_LABELS.pending, message }
     ```
   - If `readyRequestId !== stage.requestId` at that moment, so the page is still loading, post it
     on the next matching `previewReady` instead.
   - Clear the timer and set `pendingOverlayVisible = false` on:
     - every `assignWebviewHtml`;
     - a ready, failed or stale result;
     - dispose;
     - a document switch.
   - Expose `pendingOverlayVisible` in `getActivePreviewForTests()`.
5. **Runtime.** On `previewPendingOverlay` with `sameContext(message)`:
   - Validate the message: `visible` is a boolean, and `label` and `message` are strings of at most
     500 characters. Otherwise ignore it.
   - `visible: true`: create or update a single element `[data-sphinx-preview-pending-overlay]`
     with `role="status"` and `aria-live="polite"`. It holds a `strong` with the label and a
     `span` with the message, both set with `textContent`.
   - `visible: false`: remove it.
6. **Style** (`previewStyles.ts`):
   - `[data-sphinx-preview-pending-overlay]` uses `position: fixed` and `pointer-events: none`;
   - it sits at the top right, just below the floating toolbar; read the toolbar's offsets;
   - it uses VS Code theme tokens, for example `--vscode-editorWidget-background`,
     `--vscode-editorWidget-border` and `--vscode-foreground`, with a small radius and shadow;
   - the label and the message are on separate lines (G6);
   - `max-width` keeps it inside the view at narrow widths (G2);
   - it must never change layout: no element in normal flow.
7. Leave `updatePreview` and the ready path as they are, apart from the assignment funnel.

## Tests

**Unit**, runtime (`scrollSync.test.ts`):
- the overlay message creates one overlay with the label and message texts;
- a second message updates it, and does not duplicate it;
- `visible: false` removes it;
- a message with another `requestId`, a non-boolean `visible` or a non-string label is ignored;
- showing the overlay does not insert anything before or inside the content root. The fake DOM's
  content children are unchanged.

**Unit**, styles (`previewStyles.test.ts`): the overlay rule has `position: fixed` and
`pointer-events: none`.

**Real-input E2E, scenario RI-T43:**
1. Open the side preview on a fixture with several paragraphs and wait for ready.
2. Scroll the preview a little, then record:
   - `A0 = htmlAssignments`;
   - the current frame;
   - `top0 = getBoundingClientRect().top` of a mid-page paragraph.
3. **Fast render.** Type one character in the source with `page.keyboard.type`, and wait for
   ready. Assert:
   - `htmlAssignments - A0 === 1`;
   - `pendingOverlayVisible` was never true. Sample it while waiting, or expose a per-preview
     `pendingOverlayShown` count.
4. **Slow render.** Run `setRenderDelayForTests(3000)`, type one character, then:
   - while pending, before 1.5 s: `htmlAssignments` is unchanged, the frame is the same, and the
     paragraph's top equals `top0` within 1 px;
   - after 1.5 s: the same frame shows `[data-sphinx-preview-pending-overlay]`, visible, and the
     paragraph's top still equals `top0` within 1 px;
   - capture the evidence screenshot `43-pending-overlay`.
5. Reset the delay and wait for ready. Assert that `htmlAssignments` grew by exactly 1 for that
   edit and that the overlay is gone. Reset the delay in a `finally` block.
6. Record that steps 3 and 4 fail before the fix: today the pending state assigns the html.

## Expected changes to existing tests

None expected. The only integration assertion on `"pending"` html, `stockCoexistence.test.ts`
lines 219–220, covers the first opening, where there is no rendered page yet; it is unchanged.

Pre-authorized, of the same kind only: an existing test that waited for the in-flow pending banner
*during an edit on a rendered page* may wait on `getActivePreviewForTests()?.status === "pending"`
instead. List it with the evidence. Any other failure of an existing test is a STOP.

## Must not change

- First-render pending pages, failure and recovery pages (`stale`, `error`), and the
  missing-source page.
- The host `html` string always equals what the webview shows.
- Anchoring and scroll: no scroll change on pending (the scroll suite in `full`).
- The frozen findings UX-22, UX-24 and UX-34.

## Done when

- `unit types contracts full visual` pass, and RI-T43 passes.
- `rg -n "webview\.html =" src/extension.ts` shows only `assignWebviewHtml`.
