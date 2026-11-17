# Tab through a wide table leaves the cell editor outside the visible preview

Severity Medium · Reproduced · Verdict Bug · Requirements: SwRS-MDOKFSTUDIO-TABLE-035 · Area Tables · Side preview · QA210-06 · Replay `scenarios/c5-1-wide-table-tab-editor-offscreen.json` · P2

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![After 9 Tabs the cell editor is not visible](evidence/currently.jpg) | ![A cell editor in view (first column)](evidence/expected.jpg) |
| *Currently: after 9 Tabs (column 10 of 10) the cell editor is at x=1859 in a 393 px pane, so nothing is visible (replay `c5-1` on b9118506; the wrap to column 1 fails the same check).* | *Expected: the editor stays inside the preview on every Tab and Shift+Tab (shot: editor on the first column).* |

The Currently shot is the before-shot the fix PR must reproduce.

## Why this is wrong

An author fills a wide table (10 columns, 24-character cells) with Tab, as in a spreadsheet. In a
393 px side preview the editor ends up at x=964 on the last column and at x=-832 after the row
wrap, outside the pane at both ends: the author types blind and loses track of the cell being
edited. A spreadsheet scrolls to keep the active cell in view, and TABLE-035 promises that Tab
moves the editor to the next cell, which is of no use if that cell is off screen. The first column
already works, so the product only fails when the table is wider than the pane.

## Steps to reproduce

1. Fixture `synth/c5-tables.md` (copy of `assets/synth/c5-tables.md`); open the side preview
   (pane about 393 px), switch to edit mode, unfold the H1 if folded.
2. Click the last cell of the "Wide pipe table" first data row (`LASTCELL`), press Tab: the wrap
   to the first cell of the next row puts the editor at x=-832.
3. Click the first cell and press Tab nine times: the editor sits at x=964 (right edge 1264, pane
   ends at 1139).

## Impact

Lost context while typing in wide tables. No buffer corruption: the diff against the mark is empty
after Escape.

## Where it comes from

`switchTableCell` and `tabThroughTableCells` in `src/page/features/tableCellEditor.ts` do not
scroll the new cell into the table's horizontal scroll container, at the tested commit.

## Suggested direction

Scroll the target cell (inline-nearest) into view after each switch and keep the editor inside the table scroll box. Related, different cause: P3 `auto-width-table-no-horizontal-scroll` (scrollLeft snaps back in Auto width) can defeat the fix in that mode; check both together. Done when: the cell editor stays inside the preview on every Tab and Shift+Tab, wrap included; replay `c5-1` passes.

Uncheck to disagree: [x]

## Test to add

Add a real-input scenario: after every Tab and Shift+Tab the editor rect lies inside `window.innerWidth` (replay `c5-1` promoted). It earns a test because an element off the viewport is an objective invariant that the Auto-width issue can silently break again.

Uncheck to disagree: [x]

Sources: sheet [c5-1](../../../4-archives/210-qa-campaign-2026-10-31/05-table-editing/c5-1-wide-table-editor-offscreen-after-tab.md),
replay [c5-1](../../../../skills/markdown-studio-exploratory-qa-claude/scenarios/c5-1-wide-table-tab-editor-offscreen.json),
[campaign index](../../../4-archives/210-qa-campaign-2026-10-31/00-index.md).
