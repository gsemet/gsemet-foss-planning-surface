---
title: "CR 268: the cell left with Tab or an arrow key shows its new text"
description: Fix GitHub #335, a moved-from table cell shows stale or empty content after Tab.
status: open
date: 2026-11-10
---

# CR 268: the cell left with Tab or an arrow key shows its new text

> [!NOTE]
> Source: GitHub issue [#335](https://github.com/gsemet/markdown-okf-schema-studio/issues/335).
> Intent: `01-intent.md`.

## The problem

Add a table row, type in its first cell, press <kbd>Tab</kbd>: the editor moves to cell 2 and
cell 1 shows empty. The text is saved in the file (display only, reproduces every time).

Cause, at `ccaf35b8`: `switchTableCell` (`src/page/features/tableCellEditor.ts` L63-85) posts an
autosave without a re-render, then `restoreTableCellContent` puts back the rendered content captured
when the editor opened in that cell. For a new row it is empty; for an existing cell it is the old
text. Tab (`tabThroughTableCells`) and the arrow keys share this path.

## Owner's decisions (2026-11-10, "ok" to every recommendation)

| Question | Decision |
| --- | --- |
| Scope | The general case: any cell left by Tab, Shift+Tab or an arrow key shows the text just typed, in a new row or an existing one. |
| Tests | A failing test first (unit, and a real-input or e2e check where the suite allows), then the fix. |
| Requirement | Complete `SwRS-MDOKFSTUDIO-TABLE-035` with this case (it is `proposed`, not approved: no owner approval needed). |
| Review | Short spec, the owner does not review it before coding. Priority P1. |

## Approved requirements changed

None. `TABLE-035` is `proposed`.

## Done when

- The moved-from cell shows its new text, rendered as the cell renders (inline Markdown), without
  waiting for a re-render, for Tab, Shift+Tab and the four arrow keys.
- The test fails on `ccaf35b8` and passes after the fix; TABLE-035 has a scenario for it.
- The PR follows `.github/PULL_REQUEST_TEMPLATE.md`, with a `CHANGELOG.md` `## Unreleased` line and
  before/after screenshots.
