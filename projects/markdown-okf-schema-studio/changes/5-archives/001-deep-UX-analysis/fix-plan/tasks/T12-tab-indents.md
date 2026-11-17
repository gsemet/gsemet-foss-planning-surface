# T12 — Tab and Shift+Tab indent and outdent in the raw-Markdown editor

| Field | Value |
| --- | --- |
| Fixes | [UX-05](../../01-inline-block-editing/UX-05-tab-commits-instead-of-indenting.md) |
| Decisions | D-04, D-01 (Escape then Tab is the keyboard exit route) |
| Depends on | T11 |
| Gate | `unit trusted` |
| Risk | Low–medium (keyboard trap must stay escapable) |
| Commit message | `fix(vscode): indent and outdent with Tab in the inline editor` |

## Goal

In the **block** textarea:

- Tab indents and Shift+Tab outdents, without closing the editor.
- **List lines** move by their own marker width; other lines move by 4 spaces.
- **Collapsed caret on a non-list line:** Tab inserts 4 spaces at the caret.
- **Exiting:** Escape closes the editor (keeping the text, T08). The next Tab then moves focus as
  usual.

Table cell textareas are handled by T17. Frontmatter controls keep the native Tab (focus moves,
blur saves).

## Context to read first

- T11's `src/webview/textEditing.ts` and `applyTextEdit`.
- The block textarea keydown listener in `receiveBlockEditSource`.

## Allowed files

- `src/webview/textEditing.ts`
- `src/webview/scrollSync.ts`
- `test/webview/textEditing.test.ts`
- `test/webview/scrollSync.test.ts`
- `test/integration/realInput.test.ts` (add RI-T12)
- `README.md` (one sentence)

## Pure function

Add `indentSelection(value, selectionStart, selectionEnd, outdent: boolean): TextEdit | undefined`
to `createTextEditingTools`:

1. The affected lines are those intersecting `[selectionStart, selectionEnd]`. With a non-empty
   selection that ends exactly at the start of a line, exclude that last line, as code editors do.
2. **Unit per line:** if the line matches the T11 list regex (after an optional quote prefix), the
   unit is the marker plus the following spacing width (`- ` → 2, `10. ` → 4). Otherwise the unit
   is 4.
3. **Collapsed caret, `outdent === false`, non-list line:** insert 4 spaces at the caret.
4. **Indent:** prefix each affected line with `unit` spaces. Insert them after the quote prefix
   when there is one.
5. **Outdent:** remove from each line up to `unit` leading spaces (after the quote prefix), or one
   leading tab. If nothing can be removed on any line, return `undefined`.
6. Return one edit replacing the whole affected line range, with `selectionStart` and
   `selectionEnd` shifted so the same text stays selected. A collapsed caret moves with its line's
   indentation.

## Runtime wiring

In the block textarea keydown handler, for `Tab` with no Meta, Ctrl or Alt: compute
`indentSelection(…, event.shiftKey)`. Always call `event.preventDefault()`, so focus does not leave
the editor, and apply the edit if there is one, with the same fallback as T11.

## Tests

Write first, and show the failures:

1. `textEditing.test.ts`:
   - indent `- a` → `  - a`;
   - indent `1. a` → `   1. a`;
   - indent a two-line selection;
   - outdent `    - a` → `  - a`;
   - outdent with nothing to remove → `undefined`;
   - a collapsed caret mid-prose → 4 spaces at the caret;
   - the selection is preserved;
   - quote prefix: `> - a` → `>   - a`.
2. `scrollSync.test.ts`: keydown Tab on the block textarea → `preventDefault` called; the value is
   indented; no `previewEditSave` with `final: true` is posted; the editor element is still
   present.
3. **Real-input E2E**, scenario **RI-T12**, using the T11 nested-list fixture:
   - click "Refrigerated goods", press `${MOD}+End`, `Home`, `Tab`;
   - assert that the textarea is still focused and the line gained 2 spaces;
   - `Shift+Tab` → back to the original;
   - `Escape`, then `Tab` → focus is no longer in a textarea.

   It must fail before the fix.

## Expected changes to existing tests

None expected. If a test asserts that Tab blurs and commits the **block** editor, STOP and report
it.

## Must not change

- The table cell editor's Tab (T17), frontmatter controls' Tab, Cmd/Ctrl+Enter, Escape, arrows.

## Done when

- The `unit` and `trusted` gates pass; RI-T12 passes.
- README, "Edit mode" paragraph: "Tab and Shift+Tab indent and outdent lines; press Escape to
  leave the editor."
