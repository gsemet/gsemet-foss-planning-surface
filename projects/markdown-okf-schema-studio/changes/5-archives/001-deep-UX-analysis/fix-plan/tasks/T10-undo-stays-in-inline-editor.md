# T10 — Undo and redo stay inside inline editors

| Field | Value |
| --- | --- |
| Fixes | [UX-03](../../01-inline-block-editing/UX-03-open-with-undo-closes-inline-editor.md) |
| Depends on | T09 |
| Gate | `unit trusted` |
| Risk | Medium (interaction with VS Code key routing; two approaches, test-driven) |
| Commit message | `fix(vscode): keep undo inside the inline editor in the Studio editor` |

## Goal

While focus is in an inline editor (block textarea, table cell textarea, frontmatter control),
Cmd/Ctrl+Z, Cmd/Ctrl+Shift+Z and Cmd/Ctrl+Y:

- undo or redo the last typing **inside that control**;
- never close the inline editor;
- behave the same in the side preview and in the Open With editor.

Outside inline editors, document undo in the Open With editor keeps working as it does today.

## Background (verified in VS Code 1.141's webview host, `pre/index.html`)

VS Code installs `contentWindow.addEventListener('keydown', handleInnerKeydown)` on the webview
frame, in the **bubble** phase. For undo/redo it calls `preventDefault()` and posts `did-keydown`
to the workbench. The workbench then:

- side webview panel: runs undo in the webview, so the native textarea undo works;
- custom text editor: runs the document undo, which is the bug.

Stopping propagation of the keydown at the control prevents both the `preventDefault` and the
`did-keydown`, so the browser performs the native textarea undo.

## Allowed files

- `src/webview/scrollSync.ts`
- `src/extension.ts` (only for approach B)
- `test/webview/scrollSync.test.ts`
- `test/integration/realInput.test.ts` (add RI-T10)

## Steps

1. **Write RI-T10 first** and record its failure:
   - Open With editor (`openStudioEditor`) on the T02 `smoke.md`; edit mode on.
   - Click "Second paragraph.", `End`, type ` abc`, wait 600 ms, type ` def`.
   - Press `${MOD}+Z`.
   - Assert:
     - a textarea is still focused (`frame.evaluate(() => document.activeElement?.tagName) === "TEXTAREA"`);
     - its value ends with ` abc` (the last typing chunk is gone; if Chromium coalesced both
       chunks, accept `Second paragraph.` but the textarea must still be open and focused);
     - after 600 ms, the buffer equals the textarea content.
   - Then `${MOD}+Shift+Z` restores ` def`.
   - Run the same in the **side preview**: it must pass there both before and after.
2. **Approach A (try first).** In the runtime, add one helper and use it in the keydown listeners of
   the block textarea, the table cell textarea, and the frontmatter value and key controls:

   ```js
   function keepUndoInControl(event) {
     const mod = event.metaKey || event.ctrlKey;
     const code = event.keyCode;
     if (mod && !event.altKey && (code === 90 || code === 89)) {
       event.stopPropagation?.();
       return true;
     }
     return false;
   }
   ```

   Call it **first** in each listener; when it returns `true`, return without further handling. Do
   not call `preventDefault`: the browser must perform the native undo. Rerun RI-T10 in both modes.
3. **If and only if** RI-T10 still fails in the Open With editor after approach A, implement
   **approach B**. Document in the report why A failed: what happened, and the log excerpt.
   - Host, `refreshPreview(document)`: when `preview.activeBlockEdit` exists, is not `applying`,
     and the change leaves the edited block **at the same start offset**, keep the session instead
     of clearing it:
     - read the new block text: from `sourceStartOffset` to the offset obtained by adding the
       change's net length delta to the old block end;
     - set `lastSavedText` to it;
     - post `{ type: "previewEditResync", documentId, documentVersion, requestId, editId, text }`
       with the edit's identifiers;
     - do not re-render.

     In any other case, keep today's behaviour.
   - Webview: on `previewEditResync` for the active edit, set `textarea.value` to `text` (minus the
     trailing line ending, as in `receiveBlockEditSource`), restore the caret to
     `min(previousCaret, text.length)`, keep focus, and set `lastPostedText` accordingly.
   - Add the new message type to the `sameContext` handling. It is host → webview only, so
     `isPreviewSyncMessage` does not need it.
   - Unit-test the webview part with a dispatched message.
4. Add unit tests for approach A, whichever approach ships: a keydown `z` with `metaKey` on the
   block textarea calls `stopPropagation` and **not** `preventDefault`; a plain `z` does neither.

## Expected changes to existing tests

None.

## Must not change

- Cmd/Ctrl+S must still reach VS Code: only Z and Y with a modifier are intercepted.
- Document undo in the Open With editor when no inline editor has focus.
- Copy, paste and find shortcuts.

## Done when

- The `unit` and `trusted` gates pass.
- RI-T10 passes in both the side preview and the Open With editor.
- The report states which approach shipped and why.
