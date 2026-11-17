# 113 — Table cells keep a usable width in edit mode

Type: fix · Priority: P1 · From backlog: `02-backlog/P1/table-cell-too-small`

## Intent (user)

When a column is added without title, its size is small.

this means editing is very hard because the size of the cell is not recomputed dynamically (and should not)

![image.png](../evidence/image.png)

In edition mode, the cell min-width should be set to an acceptable size (300px ?)

## Autonomous decisions

- Decided by the main session on 2026-10-26 under the user's instruction "pas de questions, full autonome". List these in the PR body under "Autonomous decisions".
- In edit mode only, every table cell gets a min-width (`min-width: 8em`, so an empty new column stays clickable), and the cell being edited gets `min-width: 300px` as the user suggested. Applying 300px to every cell would push most tables into horizontal scroll, hence the split.
- The rendered (read) view does not change.

## Extra round (2026-10-27)

- rounds: 4. Granted by the main session under the user's "full autonome" instruction: heavy CI on the stack top fails in `tableEmptyColumn.test.js` ("Timed out waiting for edit mode"), the real-window test this CR added; run https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40417826156.
- Round 4 scope: find whether it is a CI timing race or a product issue after the rebase, fix it without weakening the test; the reviewer also checks the round-3 change in `test/visual/capture_comment_checks.py` (loosened outline assertion) keeps its intent.
