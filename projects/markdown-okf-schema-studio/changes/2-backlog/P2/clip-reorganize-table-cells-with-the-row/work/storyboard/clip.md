---
title: Feature clip table-anchors
status: draft for the owner's review
date: 2026-11-25
---

# Feature clip: table-anchors

**This is the live storyboard, draft for review.** Edit any row marked *(on screen)*: the text is
the clip's exact text (`**bold**` takes the orange accent). Rows marked *(filmed)* describe the
footage of the take: changing them means a new take. Once approved, this file becomes
`docs/demo-video/clips/table-anchors/clip.md` and the clip is rendered from it.

The clip is one continuous shot: a row dragged by its handle, then a column dragged by its handle,
in the page on the left, then a zoom on the raw text on the right. It shows two texts in turn. The
times below are the Griller's proposal; the batch's trial take sets the real ones and adds the
pictures.

## Clip

| Field | Content |
| --- | --- |
| Length | 12.0 s |
| Size *(on screen)* | 1280x720 16:9 |
| Frame rate *(on screen)* | 15 fps |
| Outputs | silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | none: every setting at its default |
| Filmed on | Windows, VS Code 1.147.0 (the kit's pinned version), extension VSIX built from the branch |
| Stage | `stage/launch-checklist.md` opened twice: in Studio (left, edit mode) and in the built-in text editor (right). A pipe table of 3 columns (Task, Team, Due), a header and 4 body rows, its cells padded to the column width |

## 1. Drag a row, then a column, by its handle

![The row "Fix the login bug" dragged by its handle above "Write the notes": the drop line shows where it lands](frames/row-drag.png)

![The row at the top of the table, in the page and in the raw text](frames/row-dropped.png)

![The column "Due" dragged by its handle left of "Task": the drop line shows where it lands](frames/column-drag.png)

![The column "Due" first, in the page and in the raw text](frames/column-dropped.png)

| Field | Content |
| --- | --- |
| Time | 0 to 7.0 s (row: pointer on the handle of "Fix the login bug" at 0.9 s, press at 1.2 s, drag 1.2 to 2.4 s with the drop line shown, drop at 2.5 s, the page and the raw text show the new row order by 3.5 s; column: pointer on the handle above "Due" at 4.2 s, press at 4.5 s, drag 4.5 to 5.7 s with the drop line shown, drop at 5.8 s, the new column order by 6.8 s) |
| Shot *(filmed)* | Studio in edit mode on `launch-checklist.md` (left), the same file as raw text (right). The pointer moves to the handle left of the third body row, "Fix the login bug" (title "Drag to move row (Alt+Up, Alt+Down)"), presses and drags it up onto the upper half of the first body row, "Write the notes", then drops. The row is dimmed while it is dragged and a line above "Write the notes" shows where it lands. The table shows Fix the login bug, Write the notes, Build the packages, Publish the release; the raw text on the right changes to the same order. The pointer then moves to the handle above the "Due" column (title "Drag to move column (Alt+Left, Alt+Right)"), presses and drags it left onto the left half of the "Task" header cell, then drops. The column is dimmed while it is dragged and a line on the left of "Task" shows where it lands. The table reads Due, Task, Team; every line of the raw text changes to the same column order. |
| Text 1 *(on screen)* | Drag a row or a column by its **handle** |

## 2. Zoom on the raw text

![Mark 1 on the moved row in the raw text](frames/04-mark-1.png)

![Mark 2 on the moved column in the raw text](frames/05-mark-2.png)

| Field | Content |
| --- | --- |
| Time | 7.0 to 12.0 s (zoom from 7.1 s, held to 11.2 s, then back to the start for the loop) |
| Shot *(filmed)* | Zoom (at most 2x) on the table in the text editor (right), the heading in view. |
| Zoom | raw, hold to 11.2 s |
| Mark 1 *(on screen)* | Orange outline around the moved row line "\| Today \| Fix the login bug \| QA \|", 7.6 to 9.1 s |
| Mark 2 *(on screen)* | Orange outline around the first cell of every table line, the "Due" column (header, delimiter and the 4 body rows), 9.1 to 10.6 s |
| Text 2 *(on screen)* | The **raw table** follows, each cell keeps its spacing |

Expected result, the scenario's check: `launch-checklist.md` on disk (auto-save is on) is exactly
this text:

```markdown
# Launch checklist

| Due   | Task                | Team  |
| ----- | ------------------- | ----- |
| Today | Fix the login bug   | QA    |
| Mon   | Write the notes     | Docs  |
| Tue   | Build the packages  | Build |
| Wed   | Publish the release | Docs  |
```

## Review notes

- The feature: `src/page/features/tableRowMove.ts` (row and column handles, drag and drop, the
  drop zone, Alt+arrow keys) and `src/page/modules/markdownTable.ts` (`moveRow`, `moveColumn`,
  `serialize`: a moved row keeps its source line; a moved column keeps each cell's text and
  padding verbatim, so a padded table stays aligned). Requirements: SwRS-MDOKFSTUDIO-TABLE-002
  (row) and SwRS-MDOKFSTUDIO-TABLE-007 (column), from StRS-MDOKFSTUDIO-TABLE-002. User docs:
  `docs/user/editing.md`, the paragraph on the table handles; the clip's GIF goes under it.
- The owner's word is "anchors"; Studio's UI and docs say "handle" ("Move table row", "Move table
  column"), and "anchor" already names other things in Studio (the anchor icon of a `(label)=`
  target, the Anchor button of the toolbar). The captions say "handle".
- The handles use HTML drag and drop (`draggable`, `dragstart`, `dragover`, `drop`), like the list
  item handles of the merged `drag-list-item` clip, and the scenario drives them the same way:
  `t.ev("click", ...)`, `page.mouse.down()`, `t.moveTo(...)`, `page.mouse.up()` through CDP into
  the preview webview, in edit mode (`checks = { editMode: "on", paste: false }`). A CDP drag shows
  no floating copy: the dragged row or column is dimmed in place and a line shows where it lands.
- Handle selectors: `[data-okf-row-handle-layer] .okf-table-row-handle[data-okf-row="3"]` (the
  third body row; rendered row index 3, the header is 0) and
  `[data-okf-row-handle-layer] .okf-table-col-handle[data-okf-col="2"]` (the "Due" column).
  `setup` waits for 7 handles (4 rows, 3 columns) after edit mode is on, then parks the pointer
  below the table.
- The row drop: the pointer ends on the upper quarter of "Write the notes", so the drop line shows
  above it and the row lands first (move from rendered row 3 to 1). The column drop: the pointer
  ends on the left quarter of the "Task" header cell, so the line shows on its left and the column
  lands first (move from column 2 to 0). Each move is one edit of the whole table.
- The second drag waits for the render of the first: until then the handles refuse a new drag
  (the page's rows are stale). The scenario checks the raw text and the page after each drop before
  it goes on; a different result is a finding against the feature, not a scenario fix.
- After each move the moved row's or column's handle takes the focus, so a focus outline may show
  on it in the frames; this is the real behaviour and stays in the clip.
- The table is short (3 narrow columns, lines of 39 characters) so it fits the left half at
  1280x720 with its row handles, and the raw lines fit the right half without wrapping. If the table
  is pushed right for its handles, that is the real behaviour.
- The clip ends with the new order and starts with the old one: the loop seam relies on the kit's
  return to the start, as in `drag-list-item`.
- Not checked by the author: the times (the trial take sets them), motion, rhythm, the loop as
  watched.
