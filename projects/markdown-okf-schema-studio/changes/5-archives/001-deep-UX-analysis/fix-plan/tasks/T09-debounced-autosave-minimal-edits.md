# T09 — Debounced autosave and minimal source edits

| Field | Value |
| --- | --- |
| Fixes | [UX-02](../../01-inline-block-editing/UX-02-one-undo-stop-per-keystroke.md) |
| Decisions | D-02 |
| Depends on | T08 |
| Gate | `unit trusted scroll` |
| Risk | Medium (P-E3 autosave, P-E6 stale-source protection) |
| Commit message | `fix(vscode): group inline typing into few undo steps with minimal edits` |

## Goal

- Typing in the inline editor writes to the source after **400 ms of inactivity** instead of on
  every keystroke. Blur, Cmd/Ctrl+Enter, Escape, arrow-key block navigation, table cell switch and
  edit mode off still flush immediately.
- Each write replaces only the **changed characters**, not the whole block.
- Result: undoing an inline edit from the source takes one step per typing burst. The source
  editor's cursor, folding and decorations outside the changed characters are not disturbed.

## Context to read first

- `src/webview/scrollSync.ts`: `autosaveBlockEdit`, `postBlockEditSave`, `closeBlockEdit`,
  `switchTableCell`, the `input` listeners in `receiveBlockEditSource` and `renderTableCellEditor`.
- `src/extension.ts`: `drainActiveBlockEdit`, `activeBlockEditSource`, `handlePreviewEditSave`.
  The `applying` and `pendingText` coalescing must stay.
- `test/webview/scrollSync.test.ts` → `createRuntime`: the fake `window` has no timers
  (`conventions.md` §6).

## Allowed files

- `src/mapping/textDiff.ts` (new)
- `src/extension.ts` (`drainActiveBlockEdit` only)
- `src/webview/scrollSync.ts`
- `test/mapping/textDiff.test.ts` (new)
- `test/webview/scrollSync.test.ts` (fake timers and tests)
- `test/integration/realInput.test.ts` (add RI-T09)

## Steps

1. **`src/mapping/textDiff.ts`**, a pure module:

   ```ts
   export interface TextReplacement { start: number; end: number; text: string }
   /** Smallest single replacement turning `before` into `after`. Offsets are in `before`. */
   export function minimalReplacement(before: string, after: string): TextReplacement
   ```

   - Compute the common prefix length `p`, then the common suffix length `s`, with
     `s <= min(before.length, after.length) - p`.
   - Never split a `\r\n` pair: if `before[p - 1] === "\r"` and `before[p] === "\n"`, decrement `p`.
     Apply the same check at the suffix boundary.
   - Never split a UTF-16 surrogate pair: if the character before a boundary is a high surrogate
     (`0xD800`–`0xDBFF`), move the boundary outward by one.
   - Return `{ start: p, end: before.length - s, text: after.slice(p, after.length - s) }`.
2. **Unit tests** `test/mapping/textDiff.test.ts`:
   - identical input → `{ start: n, end: n, text: "" }` or an equivalent empty replacement;
   - insertion in the middle, deletion, replacement;
   - insertion at the start and at the end;
   - `"a\r\nb"` → `"a\r\nXb"` must not split `\r\n`;
   - emoji boundaries;
   - property: `before.slice(0, start) + text + before.slice(end) === after` for 200 random pairs
     (seeded, deterministic).
3. **Host** `drainActiveBlockEdit`: compute `minimalReplacement(edit.lastSavedText, editedText)`.
   Replace only `[sourceStartOffset + start, sourceStartOffset + end)` with `text`, using
   `document.positionAt`. Keep the existing check that the document still contains
   `edit.lastSavedText` at `edit.sourceStartOffset` before applying. When the replacement is empty
   (no change), skip `applyEdit`, keep `lastSavedText` and continue draining.
4. **Webview**:
   - Add `const AUTOSAVE_DELAY_MS = 400;` near the other runtime constants.
   - `autosaveBlockEdit()`: clear `activeBlockEdit.autosaveTimer` if set, then schedule
     `window.setTimeout(() => { if (activeBlockEdit === edit) { edit.autosaveTimer = undefined; postBlockEditSave(false); } }, AUTOSAVE_DELAY_MS)`.
   - `postBlockEditSave(final)`: at the start, when the edit has a pending `autosaveTimer`, clear it.
   - `closeBlockEdit`: clear the pending timer.
   - `switchTableCell`: replace the `autosaveBlockEdit()` call with `postBlockEditSave(false)`
     (immediate flush, D-02).
   - Use `window.setTimeout` / `window.clearTimeout` only.
5. **Fake timers** in `createRuntime` (`scrollSync.test.ts`):
   - add `setTimeout(callback, delay)` and `clearTimeout(id)` to the fake `window`, backed by a
     queue;
   - return `flushTimers()` from the harness; it runs queued callbacks until the queue is empty,
     at most 100 rounds, as `flushFrames` does.
6. **Unit tests** (`scrollSync.test.ts`):
   - five `input` events → no `previewEditSave` before `flushTimers()`, exactly one after, carrying
     the last text;
   - input then blur before flushing → one final save with the last text, and the timer is cleared
     (`flushTimers()` posts nothing more);
   - table cell switch posts immediately.
7. **Real-input E2E**, scenario **RI-T09**:
   - Subscribe to `vscode.workspace.onDidChangeTextDocument` for the fixture.
   - Open "Second paragraph.", press `End`, type ` twenty characters!!` with a 25 ms delay, wait
     1000 ms, then click the heading to commit.
   - Assert: at most 2 content-change events came from the typing, and every change has
     `rangeLength + text.length <= 40`.
   - Then `showTextDocument(fixture, ViewColumn.One)` and execute `undo` **once** → the paragraph
     is back to `Second paragraph.`.

   It must fail before the fix (≈20 events, whole-block ranges). Record the counts.

## Expected changes to existing tests

`scrollSync.test.ts` tests that expect a `previewEditSave` **immediately** after an `input` event
must call `flushTimers()` before asserting. List each one. The expected message content must not
change, apart from the timing.

## Must not change

- The stale-source guard: "The source block changed while it was being edited." still fires when
  the document no longer contains `lastSavedText` at the recorded offset.
- One active inline edit at a time; `finishing` semantics; `pendingBlockNavigation`.
- Checkbox toggles are still refused while an inline edit is open.

## Done when

- The `unit`, `trusted` and `scroll` gates pass; RI-T09 passes.
- The report shows the before/after event counts of RI-T09.
