# c5-1 — Tabbing through a wide table leaves the cell editor outside the visible preview

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced (3 runs) |
| Area | Tables |
| Modes | Side preview (393 px wide pane) |
| Evidence | measured: editor rect `x=-832 w=300` after Tab wrap, `x=964 w=300` on the last column (pane spans 0-393) |
| Related | none |
| Replay | `scenarios/c5-1-wide-table-tab-editor-offscreen.json` (fixture `assets/synth/c5-tables.md`, copy to `synth/`) |

## Use case

An author edits a wide table (10 columns, 24-character cells) and moves with Tab.

## Steps to reproduce

1. Open `synth/c5-tables.md`, open the side preview, switch to edit mode, unfold the H1 if folded.
2. Click the last cell of the "Wide pipe table" first data row (`LASTCELL`).
3. Press Tab (wraps to the first cell of the next row). Then click the first cell and press Tab nine times.

## Expected

The cell editor is fully inside the preview viewport: the table scrolls horizontally to follow the
selected cell, as a spreadsheet does.

## Observed

After the Tab wrap the editor is at `x=-832` (left of the pane); on the last column it overflows
the right edge (`x=964`, right edge 1264 for a pane ending at 1139). The author types blind.
No buffer corruption: diff against mark is empty after Escape.

## Impact

Lost context while typing in wide tables; no visual feedback of the cell being edited.

## Where it comes from

`src/page/features/tableCellEditor.ts` `switchTableCell` / `tabThroughTableCells` (no scrollIntoView
of the new cell inside the table's horizontal scroll container).

## Suggested direction

Scroll the target cell (inline-nearest) into view after each switch, and keep the editor within the
table scroll box.

## Test to add

Real-input scenario above: after Tab, editor rect inside `window.innerWidth`.

## Done when

The replay scenario passes both checks.
