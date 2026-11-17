---
title: "CR 269: a wide table keeps its Auto breakout while a cell is edited"
description: Opening a cell editor no longer shrinks a wide table to the text column in Auto width.
status: open
date: 2026-11-10
---

# CR 269: a wide table keeps its Auto breakout while a cell is edited

> [!NOTE]
> Intent: `01-intent.md`. Base: `origin/main` at `ede6863e`.

## The problem

In edit mode with Auto width, a wide table breaks out to the page width. When a cell editor opens,
the table shrinks to the text column and scrolls sideways, so the last column is cut. This is the
specified behaviour today: `eligibleWrappers` in `src/page/modules/widthMode.ts` skips any wrapper
marked `data-sphinx-preview-editing="true"` or holding a `textarea`, and the cell field is a
textarea. The rule was written for editors that replace the block with its source; a cell editor
keeps the table rendered.

## Owner's decisions (2026-11-10, "ok" to every recommendation)

| Question | Decision |
| --- | --- |
| Behaviour | A table with an open cell editor keeps its Auto breakout. The column-width rule applies only to editors that replace the block with its source. |
| Source edit | A whole table edited as source keeps the column width, as today; diagrams and code blocks under edit are unchanged. |
| Other width modes | Unchanged. |
| Approved requirement | The owner agrees to change `StRS-MDOKFSTUDIO-LAYOUT-003` (approved): its sentence becomes "An element whose source editor is open keeps the column width; a table whose cell is being edited keeps its Auto breakout". Set `approved_by` (the owner's email, its `default_owner_email`) and `approved_at` to the change time with its UTC offset; the PR lists it under "Approved requirements changed" and requests the owner's review. |
| Linked requirements | `SwRS-MDOKFSTUDIO-LAYOUT-023` (proposed): its "under edit" row splits into source editor (column width) and cell editor (keeps breakout). `SwRS-MDOKFSTUDIO-TABLE-035` (proposed): its row "a layout pass resizes the table box under an open editor (the edited table leaves its Auto breakout)" is updated to the new behaviour; keep the re-scroll on a real resize. LAYOUT-026 and StRS LAYOUT-007 are superseded: untouched. |
| Review | One PR, P1, short spec, the owner does not review it before coding. Screenshots: optional, the PR has its own before and after. |

## Approved requirements changed

- `StRS-MDOKFSTUDIO-LAYOUT-003`: agreed by the owner on 2026-11-10 (see above).

## Done when

- In Auto width, opening, typing in, and moving between cells (Tab, arrows, click) of a wide table
  keeps the table at its breakout width; no column is cut by the editor opening.
- A table opened as a source editor still keeps the column width; Margin and the other modes behave as before.
- A test fails on the unchanged code and passes after; requirements updated as above,
  `just requirements-update`, a dated `requirements/tiers/log.md` entry, a `CHANGELOG.md` `## Unreleased` line.
- Before and after screenshots, light and dark, of a wide table with an open cell editor in Auto.
