# Behaviour change: Auto width keeps a wide table's sideways scroll

## Today
In Auto width a table wider than the pane scrolls sideways (wheel, scrollbar, script), and the scroll stays
while nothing else happens. The next layout pass resets it to 0, and the table jumps back to its first column.
A layout pass is a cell editor closing (the content gets shorter), a pane resize, an image load, a content
patch, or a toolbar or TOC change. On each pass `widthMode.update()` (src/page/modules/widthMode.ts:128-141) uncaps
the table to measure it, so the browser clamps `scrollLeft` to 0, and nothing restores the value.
In the CI case, Escape closed the editor. The ResizeObserver (scrollCore.ts:576) then ran stabilizeLayout one
frame later (scrollCore.ts:434), and the scroll the test set in that gap was lost. Locally this needed forced
timing (5/5 then; 0/5 with plain polling). A 3 px resize resets it every time. Margin and Full width are not
affected. We found no idle re-measure loop: a wheel scroll stays until the next layout pass.

## After
In Auto width a layout pass keeps the table's sideways scroll. `update()` notes the scroll of each element it
measures and puts it back after the measurement, clamped to the new maximum. The table no longer jumps back to
its first column when an editor closes, the pane is resized, or an image loads. Breakout widths and centring are
unchanged.

## Requirements touched
- SwRS-MDOKFSTUDIO-LAYOUT-023 (proposed): new scenario "a re-measure keeps the sideways scroll of a wide table".
- No approved requirement changes (StRS-MDOKFSTUDIO-LAYOUT-003 unchanged).

## Choices left open (proposal in bold)
1. Scope of the restore: **every element update() measures (tables, code blocks, wrappers), not only tables**
   (same clamp for a wide `pre`).
2. When the width changes and the old scroll is past the new maximum: **clamp to the new maximum** (do not
   reset to 0, keep the end in view).
3. Proportional restore when the breakout width changes (e.g. pane resize): **no, keep the same pixel offset**
   (clamped), the simplest and the one people expect for small resizes.
4. Tests: **unit T10b (runtimePageControls), plus a headless visual scenario
   layout-width/v91-auto-wide-table-keeps-scroll-light-656 (editor close and 3 px resize)**. Both fail today.
   The wide-table Tab real-input Auto pass is the end-to-end proof on the stack-top heavy run.

## Shots (656 px, Auto, edit mode, after the layout pass)
- /private/tmp/claude-502/cr230-driver/shots/before-auto-scroll-reset-cream.png (1634 -> 0, back at Column01)
- /private/tmp/claude-502/cr230-driver/shots/before-auto-scroll-reset-dark.png (1634 -> 0)
- /private/tmp/claude-502/cr230-driver/shots/before-margin-scroll-kept-cream.png (Margin, contrast: scroll kept)
