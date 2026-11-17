# T17 — Tab moves between table cells; the cell editor never dangles

| Field | Value |
| --- | --- |
| Fixes | [UX-13](../../02-table-editing/UX-13-tab-leaves-dangling-cell-editor.md) |
| Decisions | D-05, D-01 |
| Depends on | T04, T08, T09 |
| Gate | `unit trusted` |
| Risk | Medium (P-E5 cell switching and leaving the table) |
| Commit message | `fix(vscode): navigate table cells with Tab and close the cell editor on focus loss` |

## Goal

- **Tab / Shift+Tab** in the cell editor move to the next / previous cell, wrapping across rows.
- **Tab on the last cell** inserts a row and continues in its first cell, after the re-render.
- **Shift+Tab on the first header cell** does nothing.
- The cell editor never stays open without focus: when focus leaves the webview without a click
  inside it, the cell is committed and closed.
- **Escape** works wherever focus is while a cell editor is open (it commits, D-01).

## Context to read first

- `src/webview/scrollSync.ts`:
  - `renderTableCellEditor` (keydown: `navigateBlockEdit`, Escape, Enter);
  - `switchTableCell(edit, selectedCell, caretPosition)`;
  - `openMappedEditor` (table branch), `rememberPendingBlockNavigation(target, caretPosition, selectedCell)`;
  - `resumePendingBlockNavigation` (reads `tableRowIndex` / `tableColumnIndex`);
  - the document `click` listener that finalizes a table edit when clicking outside.
- Rendered rows: DOM `table.rows[i]` (header = 0). Model rows: header = 0, delimiter = 1, body
  `i` = DOM `i + 1`. `switchTableCell` already maps between them.

## Allowed files

- `src/webview/scrollSync.ts`
- `src/webview/markdownTable.ts` (only if a helper is needed; keep it pure)
- `test/webview/scrollSync.test.ts`
- `test/integration/realInput.test.ts` (add RI-T17)
- `README.md` (one sentence)

## Steps

1. Write the tests first and record the failures.
2. **Tab / Shift+Tab** in the cell textarea keydown, before Escape/Enter handling: `Tab` without
   Meta/Ctrl/Alt → `preventDefault()`, then:
   - Compute the next or previous DOM cell from `edit.selectedCell.closest("table").rows` (row by
     row, cell by cell).
   - If it exists → `switchTableCell(edit, cell, "end")`.
   - **Shift+Tab at the first header cell** → nothing.
   - **Tab at the last cell of the last row:**
     1. `rememberCellValue()` (store the current input).
     2. `const newRow = tableTools.insertRowAfter(edit.tableModel, edit.tableRowIndex)`.
     3. Record a pending navigation to rendered row `newRow`, column 0, on `edit.target`. Extend
        `rememberPendingBlockNavigation(target, caretPosition, selectedCell, explicitIndices?)` so it
        accepts `{ tableRowIndex, tableColumnIndex }` when no DOM cell exists yet.
     4. `postBlockEditSave(true)`. After the re-render, `resumePendingBlockNavigation` opens the new
        cell.
3. **Focus loss**:
   - Add a capture-phase `pointerdown` listener on `document` that stores `lastPointerDownAt = Date.now()`.
   - In the cell textarea, on `blur`, schedule `window.setTimeout(check, 0)`. `check` does nothing if
     the edit is no longer active, is `finishing`, or `Date.now() - lastPointerDownAt < 500`: a click
     is in progress, and the existing click handlers will switch cells, open another block, or
     finalize.
   - Otherwise, if `document.hasFocus?.()` is false or focus is outside `edit.element` and the
     table menu, call `saveBlockEdit()`.
4. **Escape anywhere**: in the existing document `keydown` listener (or a new one), when
   `key === "Escape"`, `activeBlockEdit?.selectedCell` exists, and the focus is not inside
   `activeBlockEdit.element`, call `saveBlockEdit()`.
5. README, "Edit mode" paragraph: "In a table cell, Tab and Shift+Tab move between cells; Tab on
   the last cell adds a row."

## Tests

**Unit** (fake DOM; extend the table fixture in the harness only as needed):

- Tab from the first body cell → `switchTableCell` to its right neighbour: the editor element is
  re-parented and `tableColumnIndex` increments.
- Tab from the last cell → a final `previewEditSave` whose table text contains a new empty row, and
  the saved `pendingBlockNavigation` state has the new row index and column 0.
- Shift+Tab from the first header cell → no message, the editor is unchanged.
- Blur with no recent pointerdown, after `flushTimers()` → a final save. Blur right after a
  pointerdown → no save.

**Real-input E2E**, scenario **RI-T17** (the T02 `smoke.md` table):

- Click `one`, press `Tab` → the editor shows `beta`'s cell. Type `X`, press `Tab` → `two`'s cell.
  Press `Tab` again on the last cell → after the re-render, an editor is open in a new third body
  row. Type `gamma`, press `Tab`, type `three`, press `Enter`.
- Assert the buffer contains `| betaX |` in that row (T04 keeps the row's own spacing; assert with
  a regex tolerant to padding) and a new row with `gamma` and `three`.
- Click a cell, type `Q`, then focus the VS Code source editor
  (`vscode.window.showTextDocument(doc, ViewColumn.One)`). The cell editor closes and the buffer
  contains `Q`.

## Expected changes to existing tests

None expected. Existing cell-switch and leave-table tests must pass unchanged. They do not use
blur; if one does, STOP and report.

## Must not change

- Arrow-key cell and block navigation, the toolbar actions, the header and last-body-row deletion
  guards, and Enter commits (P-E5).

## Done when

- The `unit` and `trusted` gates pass; RI-T17 passes.
