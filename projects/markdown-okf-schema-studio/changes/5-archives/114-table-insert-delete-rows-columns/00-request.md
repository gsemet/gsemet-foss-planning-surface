# 114 — Table editing: insert before/after, delete rows and columns

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/bug-new-column` (part 1/2: insert and delete)

## Intent (user)

in a table, click on "new column" just removes the current column title

![image.png](image.png)

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
- Split of the backlog item bug-new-column: this CR covers insert and delete; CR 115 covers list-table conversion, cell disappearance and move handles.
- Two buttons per axis: insert column left / right, insert row above / below. Inserting never touches existing cell content (the evidence diff shows the current title being wiped).
- Delete row and delete column work, for pipe tables and `{list-table}`; deleting the header row is refused when it is the only header.
- e2e for every button on a pipe table and on a list-table.
