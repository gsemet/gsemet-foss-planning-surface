# The label rename popover covers the first cells of the table below it and swallows their clicks

Severity Low · Reproduced · Verdict Gap · Requirements: none found (SwRS-MDOKFSTUDIO-MYST-038 and BLOCK-041 specify the icon and the popover, not its placement) · Area Labels · Tables · Side preview ·
c1-1 · Replay `scenarios/271-c1-1-label-rename-popover-covers-table-cells.json`

## Currently / Expected

| Currently | Expected |
| --- | --- |
| ![currently](../evidence/c1-1-currently.jpg) | none: no working case shot; the popover should not hide the cells (source: an anchored popover keeps the content it relates to visible). |
| In a 290 px pane the popover (322 px wide) hides the header and the alpha row of the table. | A click on a covered cell closes the popover and opens the cell editor, or the popover sits clear of the table. |

## Why this is wrong

An author who clicks the anchor icon of `(table-label)=` to rename it finds the popover placed
below the icon, which for a table sits at the table's top-left. It covers the header and first row,
and a click on a covered cell is taken by the popover (`pointerdown` on the popover does not close
it), so the cell editor does not open. After a successful rename the popover also stays 5 s. The
author sees "cells that do not open". Escape or a click elsewhere clears it, so it is not page-wide.

## Steps to reproduce

1. Fixture `synth/anchors-tables.md`, side preview, edit mode on.
2. Click the anchor icon left of the first table (label `table-label`).
3. Click the cell `alpha` (under the popover): nothing opens, the popover stays.

## Impact

Brief "blocked" feeling on the first rows of a labelled table; no data loss.

## Where it comes from

`src/page/modules/labelRename.ts` `place()` (top = icon bottom + 6, no avoidance) and the
`pointerdown` handler, at 293366d0.

## Suggested direction

- (x) A pointerdown outside the input (including on covered cells) closes the popover and lets the click through
- ( ) Place the popover above the icon / clear of the table
- ( ) Leave as is

## Test to add

Real-input E2E: open the popover on a label above a table, click a cell under it, assert the cell editor opens.

Uncheck to disagree: [x]

## Done when

- [ ] The replay scenario passes.
