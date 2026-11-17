---
title: A wide table narrows when a cell editor opens
description: In Auto width, opening a cell editor shrinks the table to the text column and cuts the last column.
status: inbox
date: 2026-11-10
---

# A wide table narrows when a cell editor opens

> [!NOTE]
> Owner order: second, right after #335. Screenshots: `intake/` (to get from the owner: a 4-column
> table, row 4 of 11, column 2 of 4).

## What the owner sees

In edit mode with Auto width, a wide table breaks out to the page width. When a cell editor opens,
the table shrinks to the text column and scrolls sideways, so the last column is cut.

## It is the specified behaviour

`SwRS-MDOKFSTUDIO-LAYOUT-026`: "When an element is under edit […] SHALL keep it at the column width
in Auto width mode". The same rule is in the `LAYOUT-023` table row, `StRS-MDOKFSTUDIO-LAYOUT-003`
and `-007`. `TABLE-035` scrolls the open cell back into the narrowed box.

Code (at `ccaf35b8`): `src/page/modules/widthMode.ts` `eligibleWrappers` L76-91 skips wrappers
marked `data-sphinx-preview-editing="true"` or holding a textarea; `tableCellEditor.ts`
`revealOpenCell` L547 handles the resize.

The rule fits a block editor, which replaces the rendered block with source text. A cell editor
keeps the table rendered.

## Proposal (recommendation, not decided)

- (x) The table keeps its Auto breakout while a cell editor is open; the column-width rule applies to
  block editors only.
- A whole-block source edit keeps the column width, as today.
- The other width modes are unchanged.

> [!IMPORTANT]
> A requirement change (`LAYOUT-026`, `LAYOUT-023`, `TABLE-035`, the StRS) plus code, in one PR.
