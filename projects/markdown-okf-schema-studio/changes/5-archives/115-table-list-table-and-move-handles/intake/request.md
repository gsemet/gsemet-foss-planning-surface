# 115 — Table editing: list-table conversion, stable cells, row and column move handles

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/bug-new-column` (part 2/2: conversion and handles)

## Intent (user)

in a table, click on "new column" just removes the current column title

![image.png](../evidence/image.png)

expected:
- insert a column to the left

Also, I need another button to insert at the right (2 buttons, one to insert before, one to insert after)

same for +1 row

---

Delete row does not work

Delete column does not work

---

click on "list-table" make the table disappears from the block under edition, but it is still here on focus loss (it has just lost all heading cell content

---

the anchors to move lines on the right does not work !!! they appear, i can grab, but not moving lines

---

some time when i click on a table to edit a cell it disappears from the edition box

---

Add equivalent for moving columns (same kind of anchors, on top of the table, above, not inside the cells)

---

> [!NOTE]
> ==> the tests e2e for table edition, convertion back/forth list-table is not covered correctly


| Column 1 | Column 2 | Column 3 | Column 4 |
| --- | --- | --- | --- |
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |


```{list-table}

## Autonomous decisions

- Decided by the main session on 2026-10-26 under the user's instruction "pas de questions, full autonome". List these in the PR body under "Autonomous decisions".
- Converting pipe table <-> `{list-table}` keeps every cell including the header row, and the table stays visible in the edit box.
- Clicking a cell never makes the cell disappear from the edit box (find the cause, add a regression test).
- Row move handles (left, outside the table, as already shipped) actually reorder rows on drop.
- New column move handles above the table, outside the cells, same look and behaviour as the row handles; works for list-table too without breaking its syntax.
- e2e: round-trip conversion, row move, column move, on both table syntaxes.

## Extra round (2026-10-27)

- rounds: 4, coder on **Opus** (escalation after repeated failures). Granted by the main session under the user's "full autonome" instruction.
- Deterministic heavy-CI failure on 120 and 123 (runs https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40453204164 and https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40453209884): `scenarioRowMoves` (tableMoves.ts) "Timed out waiting for the row moved while the cell editor was open"; the buffer shows rows b1, a1, c1 and cell c2X, so a move happened but not the expected one, or a second move was lost. The round-3 `dragTo` wait did not fix it.
- Scope: decide product or test from the buffer evidence (the cell editor shifts the row geometry; a drop target computed from stale boxes is a product bug if a user can hit it). Fix without weakening the test; prove it in a heavy run on the CR 115 branch before restacking.
