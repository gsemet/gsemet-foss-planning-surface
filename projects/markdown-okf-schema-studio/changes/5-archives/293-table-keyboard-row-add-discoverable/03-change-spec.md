---
title: Change spec - a "Tab: new row" hint in the last cell, and Escape removes an empty row added by Tab
cr: 293
date: 2026-11-11
issue: none
priority: P3
source: QA campaign 271, QA271-13 (Low, observed once)
blast_radius: 2 (the Escape path of the cell editor, fixed for the High QA271-01, now removes a row from the buffer)
inspector: Opus
stack: 290 (bottom), 289, 293, 292, 291, 288 (top)
---

# Change spec: a "Tab: new row" hint in the last cell, and Escape removes an empty row added by Tab

> [!NOTE]
> Source: QA campaign 271, finding QA271-13. Sheet:
> `.agents/changes/4-archives/271-qa-campaign-tables-2026-11-10/06-table-reading-clipboard/c5-3-tab-adds-row-not-discoverable.md`
> (no evidence image: the labels were read from the DOM). Owner's answers: `02-answers.md` (run
> now, third from the bottom of the stack, no GitHub issue). Owner's decision: in the last cell of
> a table, a small hint "Tab: new row" shows; Escape on a row created by Tab that is still empty
> removes that row. Read code on `origin/main` (`33fb65ef`). Rules: `.agents/constitution.md`,
> `AGENTS.md`, `requirements/guidelines/project.guidelines.md` ("During a change").

## Problem

Tab in the last cell of a table adds an empty row and opens the editor in its first cell
(SwRS-MDOKFSTUDIO-TABLE-035). Nothing says so: the cell editor's only labels are "Markdown table
cell", "Done editing" and "Cancel (Esc)". And when the writer pressed Tab by mistake and presses
Escape (or Cancel), the new empty row stays in the buffer, although the button says "Cancel".

Why the row stays: `tabThroughTableCells` inserts the row in the model, posts a **final** save
(`postBlockEditSave(true)`) with a pending navigation to `{ tableRowIndex: newRow,
tableColumnIndex: 0 }`, and the editor reopens after the re-render as a **new** session. Escape in
that session (`cancelTableCellEdit`) has no cell left with typed text, so it cancels that session
only; the row was saved by the previous one.

## Target behaviour

### Hint

- When the open cell is the last cell of the last rendered row of the table (the cell where Tab
  adds a row), the cell editor shows the text **Tab: new row** in its actions row, before Done and
  Cancel, in the description colour and a smaller size, and the text box names it with
  `aria-describedby`. It has a data attribute for tests, for example
  `data-sphinx-preview-table-cell-hint`.
- In every other cell there is no hint. Moving the editor (Tab, Shift+Tab, an arrow, a click, a
  structural button) shows or hides it according to the new cell.
- In a narrow pane the hint wraps or sits on its own line; it never widens the edited cell beyond
  the room of SwRS-MDOKFSTUDIO-TABLE-006 (CR 282) and never pushes Done or Cancel out of view.

### Escape (and Cancel) on an empty row added by Tab

- The reopened session knows that its row was added by Tab: the pending navigation carries a mark
  (for example `addedRow: true` with the model row index) and the reopened edit keeps it
  (`edit.tabAddedRow`).
- When Escape (outside a composition) or the Cancel button is pressed in a cell **of that row**,
  the open cell first goes back to its opening text, as SwRS-MDOKFSTUDIO-TABLE-025 says. If every
  cell of that row is then empty (after trimming spaces), the row is removed from the model and the
  table is saved once (one final `previewEditSave`, one undo step in the source); the editor
  closes. The cells of other rows that were left with Tab, an arrow or a click in the session keep
  their text (TABLE-025 unchanged).
- If a cell of that row holds text (left with Tab inside the row), Escape behaves exactly as
  TABLE-025 today: the row stays.
- The mark lives for that session only: after Done, Enter, a click outside or a final save, a later
  Escape in that row is plain TABLE-025. A row added with the Row below button is not marked.
- Escape in a row added by Tab, then Meta+z in the source, gives back the empty row (the removal
  is its own undo step); a second Meta+z undoes the Tab.

## Code anchors (origin/main)

- `src/page/features/tableCellEditor.ts` (609 lines):
  - `cancelTableCellEdit` (lines 99-113, `@implements_req TABLE-025`): the Escape and Cancel path;
  - `tabThroughTableCells` (lines 115-154, `@implements_req TABLE-035`): the row insert and the
    `rememberPendingBlockNavigation(edit.target, "end", undefined, { tableRowIndex: newRow,
    tableColumnIndex: 0 })` call (lines 141-150);
  - `renderTableCellEditor` (line 248 on): the actions row `cellActions` with
    `blockEditor.createEditorButtons(edit)` (around lines 494-498), where the hint goes;
  - the `structural` helper (around line 361) shows how a model change is saved and the editor
    reopened.
- `src/page/features/pageRuntime.ts`: `PendingBlockNavigation` (line 238), `BlockEdit` (the fields
  of an edit), `rememberPendingBlockNavigation(...)` signature (line 482).
- `src/page/features/blockEditor.ts`: `rememberPendingBlockNavigation` and `createEditorButtons`
  (the Cancel button calls the same cancel path as Escape, TABLE-025 "Cancel button after a cell
  left").
- `src/page/features/editMode.ts`, `resumePendingBlockNavigation()` (around lines 160-182): where
  the pending navigation reopens the editor; the mark must reach the new edit there or at
  `openBlockEditor`.
- `src/page/modules/markdownTable.ts`: `deleteRow(model, renderedRow)` (used by the Row − button).
- `src/core/preview/styles/editModeStyles.ts`: the style of the hint (description foreground,
  `0.85em`, wraps).

## Recommended approach

1. `PendingBlockNavigation` and `rememberPendingBlockNavigation` get an optional `addedRow` flag;
   `tabThroughTableCells` sets it; the reopened `BlockEdit` keeps `tabAddedRow = <rendered row
   index>`.
2. `cancelTableCellEdit`: before today's two branches, if `edit.tabAddedRow === edit.tableRowIndex`
   and the row (with the open cell back to its opening text) is all empty, call
   `tableTools.deleteRow(edit.tableModel, edit.tableRowIndex)`, clear `convertedText`, and
   `rt.blockEditor.saveBlockEdit()` (one final save). Mark it `@implements_req
   SwRS-MDOKFSTUDIO-TABLE-025`.
3. In `renderTableCellEditor`, add the hint element when the selected cell is the last cell of the
   last row of its table; `@implements_req SwRS-MDOKFSTUDIO-TABLE-035`.
4. `tableCellEditor.ts` is at 609 lines (limit 800); CRs 292 and 291 above also add code here: keep
   this change compact, or put the hint and the empty-row test in a small module
   (`src/page/modules/tableTabRow.ts`).

## Requirements

No `approved` requirement is touched (none in the bundle carries `approved_by`): no owner
agreement needed.

- **SwRS-MDOKFSTUDIO-TABLE-035** (`proposed`, `stable`; amend). Normative text: add "and, in the
  last cell of the table, the cell editor SHALL show the hint Tab: new row". Add a scenario
  (nominal) "The last cell shows the Tab hint": the hint in the last cell of the last row, none in
  any other cell, it follows the editor when it moves, and the text box names it with
  `aria-describedby`. Amend "Tab in the last cell adds a row": the reopened editor remembers that
  its row was added by Tab (see TABLE-025).
- **SwRS-MDOKFSTUDIO-TABLE-025** (`proposed`, `stable`; amend). Normative text: add "When Escape
  or Cancel is pressed in a row that Tab added in the session that opened in it, and every cell of
  that row is empty once the open cell is back to its opening text, the row SHALL be removed and the
  table saved in one edit". Scenarios: (nominal) "Escape on an empty row added by Tab" (one final
  save without the row; the buffer equals the buffer before the Tab, except the text typed in the
  cell where Tab was pressed); (boundary) "Escape on a row added by Tab after typing in it" (text
  typed in its first cell only: the text is dropped and the row removed); (boundary) "A row added
  by Tab with a cell left holding text" (the row stays); (boundary) "A row added with the Row below
  button" (Escape does not remove it); (nominal) the Cancel button does the same as Escape.
- No new SwRS. `just requirements-update`, generated files committed, a dated entry in
  `requirements/tiers/log.md`.
- Writing skill: no change (no rendered syntax changes).

## Tests first (each fails on origin/main)

1. **Unit, runtime**: a new file `test/page/runtimeTableCellTabRow.test.ts` (not
   `runtimeTableCellEditor.test.ts`, which is at 1 499 lines), with the harness of
   `test/page/runtimeTableCellEscape.test.ts` / `runtimeTableCellEditor.test.ts`
   (`createRuntimeHarness`). Cases:
   - the hint is present in the last cell of the last row and absent in the first cell, and it
     appears after Tab into the last cell and disappears after Shift+Tab out of it
     (`@tests_req SwRS-MDOKFSTUDIO-TABLE-035`);
   - Tab in the last cell, the re-render answered, Escape in the new first cell: one final save
     whose text is the table without the new row (`@tests_req SwRS-MDOKFSTUDIO-TABLE-025`);
   - the same with Cancel clicked;
   - the same after typing "x" in the new first cell: the row is still removed;
   - Tab inside the new row with "x" typed in its first cell, then Escape in its second cell: the
     row stays with "x" (TABLE-025 as today);
   - Row below button, then Escape in the new row: no row removal.
2. **Real input**: a new `test/integration/realInput/tableTabRow.ts` (scenario `table-tab-row`,
   registered in `test/integration/realInput/run.ts`), on the second table of
   `synth/c5-reading.md`: click `3`, the hint "Tab: new row" is visible; Tab: the buffer gains
   one row; Escape: the buffer equals the mark taken before the Tab; Meta+z in the source gives the
   empty row back. `@tests_req SwRS-MDOKFSTUDIO-TABLE-025`, `@tests_req SwRS-MDOKFSTUDIO-TABLE-035`.
   Runs in the heavy CI run.
3. **Visual**: two scenarios `table-editing/v30-cell-tab-hint-light-900` and
   `table-editing/v31-cell-tab-hint-dark-360` (next free numbers at the time of writing; re-check
   at rebase), in a new file `test/visual/tableTabHintScenarios.ts`, fixture `08-okf-schema`, edit
   mode, the cell editor opened in the last cell of the last row (a new `editTarget`, or a selector
   scroll and click in a new capture module `test/visual/capture_table_tab_hint.py` imported by
   `test/visual/capture.py`, never by `capture_edit_checks.py`). The check asserts the hint text,
   that it lies inside the cell editor and the viewport, and that Done and Cancel are still fully
   in view. `@tests_req SwRS-MDOKFSTUDIO-TABLE-035`.

### Replay

None: QA271-13 has no replay (`Replay none` in the sheet, "observed once"), and commit `87307e8f`
holds none for it. The real-input scenario above is the starting test. It uses
`synth/c5-reading.md`, added by CR 289 below in the stack; do not add it again.

## Acceptance checks (the Verifier runs each at the pushed head)

| # | Claim | Command (from the worktree root) |
| --- | --- | --- |
| A1 | The new unit tests pass | `fnm exec -- npm run compile && fnm exec -- node scripts/node-test.mjs unit "out/test/page/runtimeTableCellTabRow.test.js"` |
| A2 | They fail on the base | the same command in a detached worktree of the base with the new file copied in: the hint and removal cases fail |
| A3 | The Escape and Tab tests of the base still pass | `fnm exec -- node scripts/node-test.mjs unit "out/test/page/runtimeTableCell*.test.js"` |
| A4 | The hint shows and fits, light and dark | `fnm exec -- npm run visual:render && uv run --no-sync --group docs python test/visual/capture.py --group table-editing` passes, v30 and v31 included |
| A5 | Tab then Escape leaves the buffer as before, in a real window | the heavy CI run at the head is green and its integration log names `table-tab-row`; `table-escape` (QA271-01) still passes there |
| A6 | Traceability | `uv run --no-sync --group requirements okfreq validate --check-links --project-root .` passes; `git grep -n "@tests_req SwRS-MDOKFSTUDIO-TABLE-025" -- test/page/runtimeTableCellTabRow.test.ts test/integration/realInput/tableTabRow.ts` |
| A7 | Gates | `just check` and `just preflight` pass |

## Screenshots expected in the PR

- After only for the hint (the base has none: one "before" shot of the same cell shows Done and
  Cancel alone): light at 900 px and dark at 360 px, the editor in the last cell with "Tab: new
  row" next to Done and Cancel. Use the `open` step shots of v30 and v31 and the same captures on a
  detached worktree of the base.
- The Escape removal has no picture: the PR states it with the buffer diff of the real-input
  scenario.

## CHANGELOG line (`## Unreleased`)

- In the last cell of a table, the cell editor now shows "Tab: new row". If you press Tab there
  by mistake, Escape (or Cancel) in the new row, still empty, removes it again.

## Files expected to change

- `src/page/features/tableCellEditor.ts` (hint, Escape branch, the mark on Tab)
- `src/page/features/pageRuntime.ts` (`PendingBlockNavigation`, `BlockEdit`, signature)
- `src/page/features/blockEditor.ts` (`rememberPendingBlockNavigation`)
- `src/page/features/editMode.ts` (`resumePendingBlockNavigation` passes the mark)
- `src/core/preview/styles/editModeStyles.ts` (hint style)
- optionally a new `src/page/modules/tableTabRow.ts`
- `test/page/runtimeTableCellTabRow.test.ts` (new)
- `test/integration/realInput/tableTabRow.ts` (new), `test/integration/realInput/run.ts`
- `test/visual/tableTabHintScenarios.ts` (new), `test/visual/capture_table_tab_hint.py` (new),
  `test/visual/capture.py`, `test/visual/scenarios.ts`, `test/visual/scenarioIds.ts`,
  `test/visual/scenarioAssertions.ts` (only for a new `editTarget` or flag)
- `test/core/preview/previewStyles.test.ts` only if a style assertion is wanted for the hint
- `requirements/tiers/swrs/table-editing/SwRS-MDOKFSTUDIO-TABLE-035.md`,
  `requirements/tiers/swrs/table-editing/SwRS-MDOKFSTUDIO-TABLE-025.md`, `requirements/tiers/log.md`
  and the generated requirement files
- `CHANGELOG.md`

## Shared with the other CRs of the stack

- `src/page/features/tableCellEditor.ts`: 292 (paste listener on the cell text box) and 291
  (contained tables) touch it too. This CR sits below them: its hunks are in `cancelTableCellEdit`,
  `tabThroughTableCells` and the actions row; keep them there.
- `src/page/features/pageRuntime.ts`, `blockEditor.ts`, `editMode.ts` (`PendingBlockNavigation`
  and `resumePendingBlockNavigation`): 291 adds the table's ordinal in its container to the same
  structure and function.
- `test/integration/realInput/run.ts`, `test/visual/capture.py`, `scenarios.ts`, `scenarioIds.ts`,
  `scenarioAssertions.ts`, the `table-editing/vNN` numbers (v30-v31 here; 292 and 291 take the
  next), `requirements/tiers/log.md` and the generated requirement files, `CHANGELOG.md`.
- `SwRS-MDOKFSTUDIO-TABLE-035`: 291 may add a line for contained tables.

## Blast radius

2. The hint is cosmetic, but the Escape change writes to the buffer (it removes a row) on the path
that QA271-01 (High, data loss) just fixed. Risks: removing a row that was not empty (the trim and
the "every cell" test must read the model, not the DOM), removing a row added by another path, and
a mark that survives into a later session. The tests above cover each.

## Open questions

None. Two choices follow the owner's words and are listed as "Autonomous decisions" in the PR:
text typed in the new row and dropped by Escape still counts as "still empty" (Escape drops it
first, TABLE-025), and Cancel does the same as Escape (TABLE-025 already makes them one path).
