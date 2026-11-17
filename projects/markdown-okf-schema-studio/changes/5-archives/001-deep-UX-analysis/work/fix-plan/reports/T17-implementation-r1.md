# T17 implementation — round 1

STATUS: DONE

## Summary
Tab / Shift+Tab in a table cell editor now move to the next / previous rendered cell (wrapping rows);
Tab on the last cell inserts a row and the pending navigation reopens the editor in its first cell
after the re-render; Shift+Tab on the first header cell does nothing. The cell textarea commits (final
save) on blur when no pointer press happened in the last 500 ms and focus is outside the editor and
table menu (or the document has no focus). Escape anywhere commits while a cell editor is open and
focus is outside it. `rememberPendingBlockNavigation` accepts explicit row/column indices.

## Files changed
- src/webview/scrollSync.ts — `tabThroughTableCells`, blur commit, capture `pointerdown` timestamp, document Escape listener, `explicitIndices` parameter.
- test/webview/scrollSync.test.ts — 6 new unit tests; fake `RuntimeElement.rows` widened to `number | RuntimeElement[]` and `cells` added (harness only).
- test/integration/realInput.test.ts — RI-T17 (`scenarioTableTab`), registered in `run()`.
- README.md — one sentence in the Edit mode paragraph.

## Tests written first (failing before the fix)
- Unit (6 new tests in scrollSync.test.ts) all failed before the fix, e.g. `actual: 'x', expected: 'y'` (Tab did not move), `actual: 'previewEditOpen', expected: 'previewEditSave'` (no final save on Tab-last / blur / Escape).
- RI-T17 against unmodified scrollSync.ts: `Error: Timed out waiting for Tab to wrap to the cell `beta`.` (log: fix-plan/logs/T17-red-trusted.log)

## Tests added or changed
- Tab/Shift+Tab move between cells and wrap; Shift+Tab on first header cell is a no-op (preventDefault, no message); Tab on last cell posts final save with a new empty row and stores pendingBlockNavigation {tableRowIndex 3, tableColumnIndex 0, sourceLine 20}; blur right after pointerdown does not save; blur without pointerdown saves; Escape via document keydown outside the editor saves exactly once.
- RI-T17: click `one`, Tab -> `beta`, type X, Tab -> `two`, Tab -> editor in new third body row, `gamma`, Tab, `three`, Enter; asserts `| betaX | two |` (padding tolerant) and the `gamma`/`three` row; then click a cell, type Q, `showTextDocument(doc, ViewColumn.One)`: buffer gets `oneQ`, editor closes.

## Existing assertions changed
- None.

## Verification
- `gate.sh T17-impl unit types trusted visual` -> unit PASS, types PASS, trusted PASS (logs/T17-impl-trusted.log), visual PASS vs baseline (0 new failure lines, 4 known moved-coordinate lines) (logs/T17-impl-visual.log)

## Evidence for reviewers
- Screenshot `24-table-tab` (real-input evidence, from trusted run).

## Open points / STOP reason
- The 500 ms pointerdown guard is implemented literally per the task. Consequence: if a user clicks a cell and moves focus away to another VS Code editor within 500 ms, the blur is ignored and the editor stays open. RI-T17 therefore waits 700 ms after the click before the focus-loss part. Not a regression (previous behaviour: never committed).
- Blur check also bails if the textarea has been replaced (`edit.tableInput !== input`), which covers cell switching and menu re-renders.
- For the red run of RI-T17 I briefly restored HEAD's scrollSync.ts and then restored the fixed version (verified by git diff stat).
