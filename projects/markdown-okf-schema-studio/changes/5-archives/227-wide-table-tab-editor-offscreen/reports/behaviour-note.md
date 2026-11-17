# Behaviour change: Tab through a wide table keeps the cell editor in view

## Today

In edit mode, a table wider than the preview scrolls sideways in its own box, but Tab, Shift+Tab and the
arrow keys move the cell editor without scrolling that box. Measured headless (393 px pane, 10 columns of
24-character cells, Margin and Auto identical): the editor (300 px wide) is at x=280..580 after the first Tab
and x=1870..2170 on column 10, while the table's scrollLeft stays 0. With the table scrolled to the end and the
last cell clicked, Tab wraps to column 1 of the next row with the editor at x=-1558 (off the left edge). Only
the table bar's "Row 2 of 2 · column 1 of 10" tells the author where they type.

## After

Each keyboard move to another cell (Tab, Shift+Tab, ArrowLeft/Right/Up/Down at the text edge, the row wrap in
both directions) scrolls the table box sideways, instantly and by the smallest amount, so the selected cell and
its editor are fully inside the box. The page never scrolls vertically for it (the edit anchor keeps the row
where it is). A move to a cell already in view does not scroll.

## Requirements touched

- SwRS-MDOKFSTUDIO-TABLE-035 (proposed): new scenario "Tab in a table wider than the pane" (editor inside the
  pane after every Tab and Shift+Tab, wrap included), verification notes updated.
- No approved requirement changes. StRS-MDOKFSTUDIO-TABLE-006 (proposed) unchanged.

## Choices the item left open (proposal in bold)

1. Which moves reveal: **every cell switch (Tab, Shift+Tab, the four arrows) and the editor reopening after a
   re-render (Tab on the last cell adds a row; structural toolbar buttons)**. A click on a partly visible cell:
   **also revealed** (the editor is 300 px wide, wider than a cell, and would otherwise stick out), the cell moving
   only by its hidden part.
2. Scroll amount: **minimal ("nearest"), plus a 16 px margin so the shaded overflow edge never covers the editor
   text**; a cell or editor wider than the box is aligned on its start (the text start stays readable).
3. Smooth or instant: **instant** (holding Tab must not queue animations; tests stay deterministic).
4. What must be inside the box: **the union of the cell and the editor element** (the editor can be wider than
   its cell).
5. Home and End inside a cell (TABLE-035 "neither the page nor the table scrolls"): **unchanged**, they never
   switch cell.
6. Test: **real-input scenario (replay c5-1 promoted): after every Tab and Shift+Tab, wrap included, the editor
   rect lies inside window.innerWidth; run in Margin and Auto**, plus unit tests in
   test/page/runtimeTableCellEditor.test.ts (target right of the box, left of the box, already visible: no scroll).

## P3 auto-width-table-no-horizontal-scroll

**Different cause, left in P3.** There the scroll is lost on a layout pass in Auto width: `widthMode.update()`
(src/page/modules/widthMode.ts:128-141, called from stabilizeLayout in src/page/features/scrollCore.ts:434 on
resize, visualViewport resize, the content ResizeObserver and image loads) uncaps the table to measure it, which
clamps its scrollLeft to 0, and nothing restores it. `update()` skips a table whose cell editor is open
(widthMode.ts:106-107), so it cannot undo this fix while the author tabs; measured: scrollLeft 600 kept with
the editor open, reset to 0 in read mode and in edit mode without an editor. (Round 0 could not reproduce the
"snap within 50 ms without any layout change" nor the dead wheel from the P3 note; a layout pass was needed.)

## Shots (before, 393 px, Margin, edit mode)

- /private/tmp/claude-502/cr227-driver/shots/before-tab-last-column-cream.png / -dark.png: after 9 Tabs, bar says
  "column 10 of 10", no editor visible.
- /private/tmp/claude-502/cr227-driver/shots/before-tab-wrap-cream.png / -dark.png: table scrolled to the end, last
  cell clicked, Tab: bar says "Row 2 of 2 · column 1 of 10", editor off the left edge.
