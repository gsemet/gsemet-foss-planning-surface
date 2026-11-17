---
title: Clamp the table cell editor to a narrow pane
cr: 282
date: 2026-11-10
issue: none
priority: P2
source: QA campaign 271, QA271-14 (owner decision)
---

# Change spec: clamp the table cell editor to a narrow pane

## Problem

In edit mode the cell being edited is at least 300 px wide. In a pane narrower than about
340 px the table's scroll box is narrower than 300 px, so the edited cell and its editor go past
the right edge of the pane. QA 271 measured it at a 279 px pane: the editor spans x 62-362. Part of
the field and the Done and Cancel buttons are out of view, and no scroll position shows the whole
cell.

At 279 px the content gutter is `clamp(16px, 8vw, 78px)`, about 22 px. A table with row handles
is pushed right by 2.2em (`table[data-okf-row-shift="true"]`). That is why the cell starts at x 62
and the box left for the table is about 200 px wide.

Owner's decision (2026-11-10, `02-answers.md`): clamp the cell editor to the pane instead of
keeping its 300 px minimum. SwRS-MDOKFSTUDIO-TABLE-006 is `status: stable`, so it can be amended
without owner approval.

Replay: none. QA271-14 was a measurement only (no sheet), and branch
`qa/271-table-campaign-replays` (87307e8f) has no replay for it. The new visual scenario below is
the starting test.

## Target behaviour

- The edited cell is at least `min(300 px, room)` wide. The **room** is the widest the table's
  scroll box can be (its containing column, minus the row-handle shift when present), minus
  `2 × CELL_REVEAL_MARGIN` (16 px) and minus the cell's own horizontal padding and borders. With
  this room, the start alignment of `revealCellInTable` puts the whole cell, field and buttons
  inside the box.
- The edit-mode floor of 8em still applies. In a pane so narrow that the room is under 8em, the
  cell is 8em wide and the table scrolls, as today. The clamp never makes the edited cell
  narrower than the other cells.
- When the room is 300 px or more (every pane from about 360 px up), nothing changes.
- The room is measured again when the layout changes under an open editor (pane resize, width
  mode switch), with the same hook that already re-fits the field and re-reveals the cell.
- Outside edit mode nothing changes.

## Code anchors (origin/main)

- `src/core/preview/styles/editModeStyles.ts`, around lines 310-318: the rule
  `html[data-sphinx-preview-edit-mode="on"] ... :where(th, td)[data-sphinx-preview-table-cell-selected="true"] { min-width: 300px; }`
  is the 300 px minimum. Its comment above (8em and "wide enough to type in") is the place to
  explain the clamp.
- `src/page/features/tableCellEditor.ts`:
  - `CELL_REVEAL_MARGIN` and `revealCellInTable(cell, editor)` (lines 21-53): the sideways reveal
    (SwRS-MDOKFSTUDIO-TABLE-035). A target wider than the box is aligned on its start.
  - `switchTableCell` (around line 82 removes `data-sphinx-preview-table-cell-selected` from the
    cell left, line 90 sets it on the new cell).
  - `renderTableCellEditor` (line 245 onward): `resizeInput` (`@implements_req TABLE-006`, line
    264), `edit.resizeTextarea = resizeInput` (line 498), `revealCellInTable(selectedCell, ...)`
    (line 564).
  - `revealOpenCell()` (around line 573): called by the layout pass on resize.
- `src/core/preview/styles/editModeStyles.ts` lines 528-533:
  `table[data-okf-row-shift="true"] { max-width: calc(100% - 2.2em); margin-inline-start: 2.2em }`.
  This is the shift the room must subtract.
- `src/core/preview/styles/tableStyles.ts` lines 10-18: the table (or `.table-wrapper`) is the
  scroll box (`display: block; max-width: 100%; overflow-x: auto`).
- `src/core/preview/styles/contentLayoutStyles.ts` (around line 395): the content root padding is
  `var(--sphinx-preview-content-gutter)`. In Auto, "an element under edit keeps the column
  width", so no breakout applies while the cell editor is open.

## Recommended approach

A pure CSS clamp (`calc(100vw - ...)`, the pattern used for popovers) cannot see the 2.2em
row-handle shift or a table nested in a wrapper. A container query on the content root would
make it a containing block for positioned descendants. So:

1. In `tableCellEditor.ts`, add a small function, for example `fitCellToRoom(cell)`. It measures
   the room of the cell's scroll box (the table, or its `.table-wrapper`), as the content width of
   the box's parent minus the box's non-auto inline-start margin (the row shift), minus
   `2 × CELL_REVEAL_MARGIN`, minus the cell's horizontal padding and borders. It writes the result
   as `--sphinx-preview-cell-editor-room: <n>px` on the selected cell (inline style).
2. Call it in `renderTableCellEditor` before `revealCellInTable`, and in `revealOpenCell` before
   the reveal (the resize path). In `switchTableCell`, and wherever the editor closes, remove the
   property from the cell left, together with the selected attribute.
3. CSS: the selected-cell rule becomes
   `min-width: max(8em, min(300px, var(--sphinx-preview-cell-editor-room, 300px)));`. Without
   the property (first paint, or a cell the runtime did not reach) the behaviour is today's.
4. Mark the new function `@implements_req SwRS-MDOKFSTUDIO-TABLE-006`. `revealCellInTable` stays
   as it is.

The room does not depend on the cell width (only on the parent column), so measuring it in the
layout pass cannot feed back on itself. The developer may pick another measure if it meets the
criteria below. The CSS fallback must stay 300 px.

`src/page/features/tableCellEditor.ts` is 603 lines (limit 800). `editModeStyles.ts` is 562.

## Requirements

- **SwRS-MDOKFSTUDIO-TABLE-006** (stable, amend). In the description and the normative text,
  "the cell being edited at least 300 px wide" becomes "the cell being edited at least 300 px
  wide, or as wide as the table's box allows in a narrower pane, never under 8em". Amend the
  "Long text wraps" scenario ("grows to 300 px when it was narrower, or to the room of a narrower
  pane") and the "Minimum cell width in edit mode" scenario. Add a boundary scenario, "Pane
  narrower than the cell minimum": at a 280 px pane, a table with row handles, the cell editor
  open in the first column. The edited cell, its field and Done and Cancel are fully inside the
  table's scroll box and inside the viewport, and the cell is at least 8em wide. Add a Window
  resize line: the room is measured again. Update the verification notes (new unit test file, new
  visual scenario, generalised width rule of `check_cell_editor_chrome`) and the criteria ("a cell
  that was narrower than 300 px must be 300 px wide" becomes "... must be min(300 px, room)
  wide").
- **SwRS-MDOKFSTUDIO-LAYOUT-023** (stable, wording only): lines 82 and 121 say "the 300 px
  minimum width of the edited cell". Make that "the minimum width of the edited cell
  (SwRS-MDOKFSTUDIO-TABLE-006)". There is no behaviour change for Auto breakout: at panes where
  the clamp bites, the table is already capped by the pane.
- SwRS-MDOKFSTUDIO-BLOCK-257 refers to "its own minimum width (see TABLE-006)" with no number, so
  it needs no change. SwRS-MDOKFSTUDIO-TABLE-035 (the reveal) is unchanged. It is only relied on.
- Run `just requirements-update`, and add a dated entry in `requirements/tiers/log.md`.
- Writing skill: no change, because no rendered syntax changes.

## Tests first (each fails on origin/main)

1. **Unit, runtime**: a new file `test/page/runtimeTableCellRoom.test.ts`. It cannot go in
   `test/page/runtimeTableCellEditor.test.ts`, which is 1 499 lines against a limit of 1 500. Use
   the harness of `runtimeTableCellEditor.test.ts` (`createRuntimeHarness`, the fake scroll-box
   table near its line 765). Tag each test `@tests_req SwRS-MDOKFSTUDIO-TABLE-006`. Cases:
   - a cell opened in a table whose column is 200 px gets
     `--sphinx-preview-cell-editor-room` = 200 − 32 − padding/borders;
   - with the row shift, the shift is subtracted as well;
   - in a wide column the property is 300 px or more, so the CSS keeps 300 px;
   - Tab to the next cell moves the property: the cell left no longer has it;
   - a window resize under the open editor (`dispatchWindow("resize")` + `flushFrames()`) writes
     the new room;
   - closing the editor (Done, Escape) leaves no cell with the property.
2. **Unit, CSS**: `test/core/preview/previewStyles.test.ts`, test "in edit mode table cells keep
   a minimum width and the edited cell is wider" (around line 1399). Today it asserts
   `min-width: 300px;`. It now asserts the `max(8em, min(300px, var(--sphinx-preview-cell-editor-room, 300px)))`
   form. The assertion changes because the owner's decision changes the minimum (QA271-14). Say
   so in the commit body, as constitution section 3 requires. The file is 1 448 lines, so keep the
   change to a few lines.
3. **Visual, narrow pane**: a new scenario in group `table-editing` (next free number at the time
   of writing: `table-editing/v29`; see the stack note). For example
   `table-editing/v29-cell-editor-clamped-light-280`, plus `v30-...-dark-280` if the dark pair is
   wanted. Fixture `08-okf-schema`, the same table and cell target as `edit-table-wrapped-*`
   (`editTarget: "table-cell"`, `editMode: true`), with a viewport `{ width: 280, height: 800 }`
   (a new constant next to `NARROW360` in `test/visual/scenarioAssertions.ts`, or inline). Map
   its short id in `test/visual/scenarioIds.ts` and give it a description there. The check goes in
   a new module `test/visual/capture_table_cell_room.py`, imported by `capture_edit_checks.py`
   (1 494 lines, limit 1 500), with `@tests_req SwRS-MDOKFSTUDIO-TABLE-006`. It asserts that:
   - the edited cell's border box, the textarea and both buttons are inside the table's scroll
     box and inside `[0, innerWidth]`, with 1 px tolerance;
   - the cell is at least 8em wide (computed from the cell's font size);
   - the cell is narrower than 300 px (the clamp actually applied in this scenario).
   Save an `open` step shot.
4. **Visual, existing check**: in `check_cell_editor_chrome`, replace the hard rule
   `cellWidth < 299 -> fail` and its `original_bounds["width"] < 299` exception with the expected
   minimum `min(299, room)`, where room is read in the same `page.evaluate`, or with "at least
   299 px, or the cell fills its box less the reveal margins". Without this, the v29 scenario
   (and any cell check at 360 px) fails on the old rule. Keep the net line change in
   `capture_edit_checks.py` at 6 lines or fewer, or move the width rule into the new module.
   Scenarios v01-v05 (900 and 460 px) must pass unchanged. At 460 px the room is close to 300 px,
   so confirm v03 and v05 still assert the column-width rule.
5. **Real window**: `test/integration/tableEmptyColumn.test.ts` asserts the edited header is
   300 px or more in a wide VS Code window. It stays as it is and must still pass. No new
   real-window test is needed.

## Files expected to change

- `src/core/preview/styles/editModeStyles.ts` (the selected-cell rule and its comment)
- `src/page/features/tableCellEditor.ts` (room measure; calls in `renderTableCellEditor`,
  `revealOpenCell`, `switchTableCell` and on close)
- `test/page/runtimeTableCellRoom.test.ts` (new)
- `test/core/preview/previewStyles.test.ts` (one assertion)
- `test/visual/capture_table_cell_room.py` (new)
- `test/visual/capture_edit_checks.py` (import, new branch or call, generalised width rule)
- `test/visual/scenarioDefinitions2.ts` (new scenario next to `edit-table-wrapped-*`), or a new
  small scenario file if that one is near its limit
- `test/visual/scenarioIds.ts` (id mapping and description)
- `test/visual/scenarioAssertions.ts` (only if a 280 px viewport constant is added)
- `requirements/tiers/swrs/table-editing/SwRS-MDOKFSTUDIO-TABLE-006.md`
- `requirements/tiers/swrs/layout-width/SwRS-MDOKFSTUDIO-LAYOUT-023.md` (wording)
- `requirements/tiers/log.md`, plus the files `just requirements-update` regenerates (indexes,
  coverage, StRS link lists)
- `docs/releases-notes/` entry for the next version, if the release process asks for one per fix

## Blast radius

- Only the edited cell in edit mode, and only when the room is under 300 px (panes under about
  360 px, or a narrow column next to a TOC). Read view, other cells, the 8em floor and the
  properties table are untouched.
- The sideways reveal (TABLE-035), the Auto breakout measure (LAYOUT-023: a narrower edited cell
  can only make a table less likely to break out) and the row and column handles (the handle
  layer reads the cell boxes, which now stay in the pane) depend on the edited cell's width.
- Risk: a stale room after a width-mode switch if `revealOpenCell` is not reached on that path.
  Test 1's resize case covers the resize path. Check a width-mode switch by hand at 280 px.

## Gates

- `just check` (format, types, boundaries, file-size ratchet, unused exports, markers, unit,
  contract, requirements lint).
- Headless visual of the group: `npm run visual:render && uv run --no-sync --group docs python
  test/visual/capture.py --group table-editing`. It covers v01-v05, the new v29 (v30) and v24/v25
  at 360 px.
- Heavy CI run on the branch:
  `gh workflow run ci.yml --ref <branch> -f heavy=true`, for the real VS Code integration and
  stress jobs, with `tableEmptyColumn` among them.
- `just preflight` before the PR is marked ready.

## Screenshots expected in the PR

- Before (origin/main) and after, at a 280 px pane, light theme, cell editor open in the first
  column of the `08-okf-schema` table. Before: the field and Done/Cancel run off the right edge.
  After: the whole cell, field and buttons are inside the pane. Use the `open` step shot of the
  new scenario, and the same capture on origin/main for "before".
- After at 460 px (`table-editing/v03`), to show that a normal pane is unchanged.

## Stack note (CRs 277-282)

The files this CR touches that the other table CRs are likely to touch:
`src/page/features/tableCellEditor.ts` (277 stale preview, 280 comment mark after undo),
`test/visual/capture_edit_checks.py` (1 494 lines, a ratchet hot spot),
`test/visual/scenarioIds.ts` and the `table-editing/vNN` numbering,
`requirements/tiers/log.md` and the generated requirement files (they always conflict). This CR's
code is self-contained (one CSS rule, one new function and three call sites), so it can go at the
top of the stack and be rebased last. If another CR also adds a `table-editing` scenario, the
later one takes the next free number when it rebases.

## Open questions

None. The 8em floor taking precedence over the clamp follows the existing edit-mode rule: the
clamp exists to keep the editor in view, and the floor exists to keep a cell usable.
