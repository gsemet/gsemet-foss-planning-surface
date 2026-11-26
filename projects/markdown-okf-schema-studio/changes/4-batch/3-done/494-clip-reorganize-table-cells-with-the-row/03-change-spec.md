# Feature clip: move table rows and columns by their handles

Short name: `table-anchors`. No tracker issue (verbal request of the owner, 2026-11-25).

## Goal

After the first clip stack (PRs 502 to 509) the owner asked for six more clips, one CR each; this
is the one the owner called "reorganize table cells with the row and column anchors". In edit mode
the reader drags a body row of a pipe table by its handle to the top, then a column by its handle
to the first place, without retyping a cell. The raw text of the same file, open beside the page,
follows each move: whole lines change order for the row, and every line's cells change order for
the column, each cell keeping its own spacing so the raw table stays aligned. One continuous shot:
the two drags in Studio on the left, then a zoom on the raw text on the right; two captions in
turn, two orange marks in turn, 1280x720 at 15 fps, no card, the logo top right, a loop, 12.0 s;
MP4, WebM and GIF; a draft PR whose description plays the clip.

The clip shows Studio's existing table row and column moves (`src/page/features/tableRowMove.ts`,
`src/page/modules/markdownTable.ts`, `SwRS-MDOKFSTUDIO-TABLE-002` for the row,
`SwRS-MDOKFSTUDIO-TABLE-007` for the column, from `StRS-MDOKFSTUDIO-TABLE-002`); no behaviour of the
extension changes.

## Dependency and base

Built on `origin/main`, alone (Q4): the clip kit (`docs/demo-video/clip-kit/`), the recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`) and the clips of the first stack
(`drag-list-item`, `paste-spreadsheet-cells`, `slash-menu-grid`, `theme-switch` and the others) are
merged there. No `depends.json`; this CR depends on none of the five other clips of this round.
Fetch first: the local `main` is behind `origin/main`.

What the kit gives, as merged (read on `origin/main`, nothing to add): the Markdown storyboard
contract (`## Clip` table; one `## <n>. <beat>` section per beat with `Time`, `Shot *(filmed)*`, at
most one `Text <n> *(on screen)*`, `Zoom`, `Mark <id>`), `MAX_LENGTH = 12` in
`lib/storyboard.mjs` (a `Length` of 12.0 is allowed, over 12 is refused), one zoom per clip, marks
in turn inside the zoom hold, the scenario's `checks = { editMode, paste }` (`resolveChecks`,
`takeLines` in `lib/check.mjs`), the helper `t.keyFrame(name)` and the key frames
`<name>.png`, `03-zoomed.png`, `<NN>-mark-<id>.png` (`keyFrameTimes` in `lib/encode.mjs`), and the
clip PR rule (the GIF inline from the PR's head, the MP4 and WebM linked at the same head).

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| table-anchors-Q1 | Filed from the owner's request: "reorganize table cells with the row and column anchors", one of six more clips | Goal |
| table-anchors-Q2 | The captions, stage and timing of the storyboard draft `work/storyboard/clip.md` (stage `work/storyboard/stage/launch-checklist.md`) are the Griller's proposal | "Where this spec differs from the draft", sections 1 to 3 |
| table-anchors-Q3 | The batch films the trial take from the draft, puts its pictures in the storyboard, renders the clip and opens the PR with the clip watchable; the owner reviews the storyboard and the clip on that PR, which stays a draft until the owner approves; the recipe's gate is moved after the take, not dropped; the deviation is reported here and in the PR body; a retake after the owner's review is a follow-up of this CR | "The storyboard gate, moved after the take", section 7, "Out of scope" |
| table-anchors-Q4 | Built on `origin/main`, alone, no `depends.json` | "Dependency and base" |
| table-anchors-Q5 | The captions say "handle", not "anchor" | section 2 (Text 1), review notes |
| table-anchors-Q6 | The stage is one padded pipe table, `launch-checklist.md`: Task, Team, Due, a header and 4 body rows | section 1 |
| table-anchors-Q7 | The row move first ("Fix the login bug" to the top), then the column move ("Due" to the first place), then one zoom on the raw text with two marks | sections 2 and 3 |
| table-anchors-Q8 | Both moves are mouse drags, filmed like `drag-list-item` (CDP mouse in edit mode); the Alt+arrow keys are not filmed; no kit change | section 3, "Out of scope" |
| table-anchors-Q9 | 12.0 s, the kit's maximum, two captions; if the trial take cannot fit, drop Mark 1 (the row stays visible in the zoom) and shorten the zoom, never lengthen the clip | sections 2 and 4 |
| table-anchors-Q10 | A pipe table, not a `{list-table}` | section 1, "Out of scope" |

From `01-intent.md`: 1280x720 at 15 fps, two captions in turn, marks in turn, no card, the logo top
right, a loop, the clip in `docs/demo-video/clips/table-anchors/`.

## The storyboard gate, moved after the take

The recipe, a project guideline (section "The storyboard first"), has the maintainer review and edit
the storyboard draft before the take. Q3 moves that gate after the take, into the pull request; it
does not drop it. This is a deviation from a project guideline, decided under the owner's rule of
the first clip stack, and reported as such:

- the batch films a trial take from the draft, puts its pictures and measured times in the
  storyboard, moves it to `docs/demo-video/clips/table-anchors/clip.md` with `status: draft`, films
  the take (the trial take may be the take when it is clean), renders and opens the PR;
- the PR is a draft (`gh pr create --draft`) until the owner approves the storyboard and the clip in
  it; the agent never marks it ready; the PR body reports the deviation (section 7);
- the recipe's storyboard order is not changed by this CR.

## What the code settles

Facts of Studio on `origin/main`, read to name the real controls (no choice made here):

- **The handles** (`src/page/features/tableRowMove.ts`, `addHandle`) are buttons
  `button.okf-list-editor-handle.okf-table-row-handle` (row, `data-okf-row="<rowIndex>"`,
  `aria-label` "Move table row", `title` "Drag to move row (Alt+Up, Alt+Down)") and
  `button.okf-list-editor-handle.okf-table-col-handle` (column, `data-okf-col="<cellIndex>"`,
  `aria-label` "Move table column", `title` "Drag to move column (Alt+Left, Alt+Right)"), all
  `draggable="true"`, in one layer `[data-okf-row-handle-layer]` appended to the frame's `body`.
  They exist in edit mode only, for a mapped pipe table of at least two body rows (row handles) and
  two columns (column handles). The row index is the rendered `rowIndex`: the header is 0, so the
  third body row "Fix the login bug" is `data-okf-row="3"`; "Due" is `data-okf-col="2"`. The stage
  gives 7 handles (4 rows, 3 columns). Row handles sit just left of the table, centred on their
  row; column handles sit just above the table, centred on their column; a table with less than
  32 px on its left is pushed right (`data-okf-row-shift`).
- **The drag is HTML drag and drop**: `dragstart` on the handle marks the row (or the column's
  cells) with `data-okf-row-dragging` (`data-okf-col-dragging`); `dragover` on a row or a cell, or
  anywhere over the table and its handle strip (`zoneTarget`), shows `data-okf-row-drop` /
  `data-okf-col-drop` `"before"` or `"after"` on the target; the half of the target's box decides
  (vertical for a row, horizontal for a column). On drop the page asks the host for the table's
  source (`previewEditOpen`), moves the row or the column (`moveRow` / `moveColumn`), serializes and
  saves the whole table as one final edit (`previewEditSave`): one edit, one undo.
- **The second drag waits for the render of the first**: after a move, `settleTimer` (up to 5 s)
  and `pending` make `busy()` true, and `startDrag` refuses a drag (`preventDefault`) until the
  render of the edit rebuilds the handles (`refresh`). After the render the handle of the moved row
  or column takes the focus (`focusAfterRender`), so a focus ring may show on it.
- **The raw result is the draft's expected text.** `moveColumn` keeps each cell segment and its
  padding verbatim (`test/page/modules/tableColumnMove.test.ts`, "a moved pipe column keeps the
  padding and the outer pipes of every line as written"); applied to the stage (row 3 to 1, then
  column 2 to 0) through `createMarkdownTableTools` on this machine, it gives exactly the text of
  section 1.
- **A CDP mouse drag reaches HTML drag and drop in the preview webview** in a real window: the
  merged `drag-list-item` take (`docs/demo-video/clips/drag-list-item/scenario.mjs`,
  `check.json` "scenario verify passed"). No floating copy follows the pointer in a CDP drag.
- **Edit mode** is off in a fresh profile; the toggle is `[data-sphinx-preview-edit-toggle]`, the
  state `data-sphinx-preview-edit-mode` on the frame's `html`. Studio's custom editor has priority
  `option`: a `.md` file opened by path opens in the text editor; the merged `drag-list-item`
  `setup` reopens the left group with Studio.

## Where this spec differs from the draft

| Draft | This spec | Why |
| --- | --- | --- |
| `status: draft for the owner's review`, the opening paragraph of a review draft | `status: draft`, the opening paragraph of a live storyboard (as `drag-list-item/clip.md`) | the file becomes the live storyboard in the clip folder (recipe) |
| `Filmed on`: "VS Code 1.147.0 (the kit's pinned version), extension VSIX built from the branch" | "Windows, VS Code <version from check.json>, extension <version> VSIX built from the branch" | the batch's take, as the merged clips write it |
| Pictures `frames/row-drag.png`, `row-dropped.png`, `column-drag.png`, `column-dropped.png` | the same names, made by `t.keyFrame("row-drag")` and the like (section 3) | the kit's key frame names (`^[a-z][a-z0-9-]*$`) |
| The review notes "Handle selectors", "The row drop", "The column drop", "Not checked by the author" (an author's plan) | moved into the scenario (section 3); the live storyboard keeps the notes a reviewer needs and the measured times | the live storyboard describes the clip, not the plan of the take |
| Times 0.9, 1.2, 2.5, 4.2, 4.5, 5.8, 7.0, 7.1, 11.2 s, marks 7.6 to 9.1 s and 9.1 to 10.6 s | the take's own times, same beats and order, `Length` 12.0 s | the recipe: the storyboard follows the take |

Everything else is carried as written: the stage, the two drags and their order, the layout (Studio
left in edit mode, the text editor right), the zoom on the raw table with the heading in view, the
two texts with their accents, the two marks and their order, the expected result, and the loop
note.

## What changes

All paths are relative to the repository root.

### 1. The stage: `docs/demo-video/clips/table-anchors/stage/launch-checklist.md`

The draft's stage, exactly (LF line endings, a final newline):

```markdown
# Launch checklist

| Task                | Team  | Due   |
| ------------------- | ----- | ----- |
| Write the notes     | Docs  | Mon   |
| Build the packages  | Build | Tue   |
| Fix the login bug   | QA    | Today |
| Publish the release | Docs  | Wed   |
```

After the row move (the scenario's intermediate check):

```markdown
# Launch checklist

| Task                | Team  | Due   |
| ------------------- | ----- | ----- |
| Fix the login bug   | QA    | Today |
| Write the notes     | Docs  | Mon   |
| Build the packages  | Build | Tue   |
| Publish the release | Docs  | Wed   |
```

After the column move (the scenario's `EXPECTED`, and the storyboard's "Expected result"):

```markdown
# Launch checklist

| Due   | Task                | Team  |
| ----- | ------------------- | ----- |
| Today | Fix the login bug   | QA    |
| Mon   | Write the notes     | Docs  |
| Tue   | Build the packages  | Build |
| Wed   | Publish the release | Docs  |
```

### 2. The live storyboard: `docs/demo-video/clips/table-anchors/clip.md`

The draft `work/storyboard/clip.md`, changed only as "Where this spec differs from the draft" says;
the times are the draft's until the take sets them (section 4), in the same commit as the render.
The content:

````markdown
---
title: Feature clip table-anchors
status: draft
date: <the day of the commit>
---

# Feature clip: table-anchors

**This is the live storyboard.** The clip is built from this file: edit any row marked
*(on screen)*, save, and run `just clip table-anchors render`, then `check`. Rows marked
*(filmed)* describe the footage of the take: changing them means a new take. `**bold**` in a text
takes the orange accent.

The clip is one continuous shot: a row dragged by its handle, then a column dragged by its handle,
in the page on the left, then a zoom on the raw text on the right. It shows two texts in turn.

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
| Filmed on | Windows, VS Code <version from check.json>, extension <version> VSIX built from the branch |
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
| Mark 1 *(on screen)* | Orange outline around the whole line of the moved row (Today, Fix the login bug, QA), 7.6 to 9.1 s |
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

- The owner's word is "anchors"; Studio's UI and docs say "handle" ("Move table row", "Move table
  column"), and "anchor" already names other things in Studio (the anchor icon of a `(label)=`
  target, the Anchor button of the toolbar). The captions say "handle".
- The handles use HTML drag and drop (`draggable`, `dragstart`, `dragover`, `drop`); the kit's
  mouse goes through CDP into the preview webview. A CDP drag shows no floating copy: the dragged
  row or column is dimmed in place and a line shows where it lands.
- Each move is one edit of the whole table, one undo. A moved column keeps each cell's text and
  padding as written, so the padded raw table stays aligned.
- The second drag starts after the render of the first (until then the handles refuse a drag).
  After each move the moved row's or column's handle takes the focus: a focus outline may show on
  it, which is the real behaviour.
- Opening the same file in the text editor beside Studio is done off camera; both show one file, so
  the raw text updates as soon as the page writes.
- The raw screencast runs at about <rawFps from check.json> frames per second: the pointer is drawn
  smooth by the kit, but the drop line and the page change by steps.
- The clip ends with the new order and starts with the old one: the loop seam relies on the kit's
  return to the start.
- Measured by the take: <filmed length, playback rate, press and key frame times, zoom and mark
  times>. Key frames: `frames/row-drag.png`, `frames/row-dropped.png`, `frames/column-drag.png`,
  `frames/column-dropped.png`, `frames/04-mark-1.png`, `frames/05-mark-2.png`. Not checked by the
  author: motion, rhythm, the loop as watched.
````

The `Mark` rows hold commas inside `<what>`: the kit's `timed` reads `^(.*),\s*([\d.]+) to
([\d.]+) s$` (greedy), so only the last comma splits; the storyboard test of section 5 proves both
rows read their times.

### 3. The scenario: `docs/demo-video/clips/table-anchors/scenario.mjs`

In the style of the merged `docs/demo-video/clips/drag-list-item/scenario.mjs` (its helpers `step`,
`editMode`, `editorLines`, `lineSpan`, the `RIGHT_EDITOR` snippet and its `setup` layout are copied,
not imported: each clip's scenario stands alone). The header comment says what is filmed and that
every text and time is in `clip.md`.

- `stage = { "stage/launch-checklist.md": "launch-checklist.md" }`; `open = ["launch-checklist.md"]`;
  `settings = {}`; `checks = { editMode: "on", paste: false }`.
- `export const EXPECTED`: the expected text of section 1 (lines joined with `\n`, a final `\n`);
  a local `AFTER_ROW` holds the intermediate text's non-empty lines.
- `HANDLES = "[data-okf-row-handle-layer] .okf-list-editor-handle"`;
  `ROW_HANDLE = "[data-okf-row-handle-layer] .okf-table-row-handle"`,
  `COL_HANDLE = "[data-okf-row-handle-layer] .okf-table-col-handle"`.
- Local helpers:
  - `handleCentre(frame, selector)`: the centre, in page coordinates, of
    `${ROW_HANDLE}[data-okf-row="3"]` or `${COL_HANDLE}[data-okf-col="2"]`
    (`locator.boundingBox()`); throws naming the handle when it has no box (is edit mode on?);
  - `rowBox(frame, text)`: the box of the `#sphinx-myst-preview-content table tbody tr` whose first
    cell's text is `text` (before the column move the first cell is the Task);
  - `headerCellBox(frame, text)`: the box of the `thead th` whose text is `text`;
  - `pageTable(frame)`: the texts of the header cells and of each body row's cells, in order.
- `setup(t)`, off camera, as `drag-list-item`: the layout (`Split Editor Right`, focus the first
  group, F1, `Reopen Editor With...`, `Markdown OKF-Schema Studio`; each step that does not give its
  result throws, naming it); edit mode on (click `[data-sphinx-preview-edit-toggle]`, poll
  `data-sphinx-preview-edit-mode` until `"on"`, `t.record("readingMode", mode)`, throw otherwise);
  poll until the frame holds 7 `HANDLES` (4 rows, 3 columns), else throw naming the count; park the
  pointer in the blank area below the table, off every block (for example 120 px below the table's
  bottom and 200 px right of its left edge), `t.moveTo(x, y, 0.1)`, then `t.sleep(500)`.
- `run(t)`, timed with `until(seconds)` (the draft's times):
  1. at 0.3 s, `t.moveTo` (0.6 s) to the centre of the row handle `data-okf-row="3"`;
  2. at 1.2 s, the press: `t.ev("click", t.pointer)`, `page.mouse.down()`, `t.moveTo(x + 6, y + 8,
     0.1)` (the move that starts an HTML drag), then `t.moveTo` (about 1.1 s, to end by 2.4 s) to
     the point 40 px right of the left edge of the row "Write the notes" and a quarter of its
     height below its top (the upper half: the line shows before it); `t.keyFrame("row-drag")`; at
     2.5 s, `page.mouse.up()`;
  3. wait, at most 2 s, until `editorLines` reads the lines of `AFTER_ROW` and `pageTable` reads the
     body rows Fix the login bug, Write the notes, Build the packages, Publish the release; else
     throw with what both show (a finding against the feature, never a scenario fix);
     `t.record("afterRow", ...)`; `t.keyFrame("row-dropped")` at about 3.5 s;
  4. wait until the frame again holds 7 `HANDLES` and the column handle `data-okf-col="2"` has a
     box (the render of the row move rebuilt them; read through a fresh `t.frameOf()`), at most
     until 3.9 s, else throw naming what it saw;
  5. at 3.6 s or once step 4 ends, `t.moveTo` (0.5 s) to the centre of the column handle
     `data-okf-col="2"`, reached before the press;
  6. at 4.5 s, the press as in step 2, then `t.moveTo` (about 1.1 s, to end by 5.7 s) to the point a
     quarter of the width of the header cell "Task" right of its left edge, at its vertical centre
     (the left half: the line shows before it); `t.keyFrame("column-drag")`; at 5.8 s,
     `page.mouse.up()`;
  7. wait, at most 2 s, until `editorLines` reads the non-empty lines of `EXPECTED` (each compared
     with `trimEnd`) and `pageTable` reads the header Due, Task, Team and the first body row Today,
     Fix the login bug, QA; else throw as in step 3; `t.keyFrame("column-dropped")` at about 6.8 s;
  8. at 7.1 s, `t.zoom("raw", rect)`: the rectangles of the editor's non-empty lines (the heading to
     "| Wed   | Publish the release | Docs  |"), padded by 24 px;
  9. at 7.6 s, `t.mark("1", rect)`: the editor line "| Today | Fix the login bug   | QA    |"
     (non-empty line 3), with 6 px and 3 px of air as in `drag-list-item`; at 9.1 s,
     `t.unmark("1")`;
  10. at 9.1 s, `t.mark("2", rect)`: from `lineSpan` of characters 0 to 9 of non-empty line 1 (the
      header, `| Due   |`) to the bottom of the same span of non-empty line 6 (the last body row),
      as wide as those nine characters, with the same air; at 10.6 s, `t.unmark("2")`;
  11. at 11.2 s, `t.unzoom("raw")` and `t.moveTo(home.x, home.y, 0.6)`; `until(12.0)`.
- `verify(t)`: poll `t.workspaceFile("launch-checklist.md")` for up to 3 s and throw
  `launch-checklist.md does not hold the expected text. On disk: ${JSON.stringify(text)}` when it
  never equals `EXPECTED`; return `{ text }`.

If the trial take cannot fit 12.0 s (the render of the row move takes longer than step 4 allows, or
the playback rate leaves 0.77 to 1.3), the fallback is Q9's: drop Mark 1 (its row in `clip.md` and
step 9) and shorten the zoom, never a `Length` over 12. Said in the PR.

### 4. Trial take, take and render

On Windows, on this machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`):

```bash
just dev
just package                                   # out/reports/package/markdown-okf-schema-studio.vsix
just clip table-anchors doctor
just clip table-anchors all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

- The trial take (recipe section 1, "A trial first", as merged for a drag clip): (a) the preview
  webview is in the frames; (b) the CDP drag moves what the clip shows: the row (step 3 of `run`
  passes) and the column (step 7 passes); (c) the result shows on screen in the page and the raw
  text; (d) the retimed rate is at least the storyboard's frame rate. If (b) fails, stop and report:
  neither the Alt+arrow keys nor a scripted call stand in for the drag the clip shows, and never
  OS-level input or capture.
- The trial take's pictures and measured times go into `clip.md` (Q3); when the trial is clean it
  may be the take.
- Every time in `clip.md` follows the take (playback rate inside 0.77 to 1.3), in the same commit as
  the render; `Length` stays 12.0 s (Q9); the two captions run end to end from 0 to 12.0, the marks
  inside the zoom hold.
- Commit together (recipe rule): `clip.md`, `scenario.mjs`, `stage/launch-checklist.md`,
  `table-anchors.mp4`, `.webm`, `.gif` (Git LFS through `.gitattributes`), `poster.png`,
  `contact-sheet.png`, `first-last.png`, `frames/*.png`, `check.json`.

### 5. Tests and docs

- `docs/demo-video/clip-kit/lib/storyboard.test.mjs`: a test "the shipped table-anchors clip.md
  reads as the clip the owner reviews", modelled on the `drag-list-item` and `slash-menu-grid` ones:
  it reads the shipped `docs/demo-video/clips/table-anchors/clip.md` from the repository (path from
  the test file's own location, at the head under test, never a copy) with `parseClip` and asserts:
  1280x720, 15 fps, `length` 12; the two captions with the words of section 2 (`**` aside) end to
  end from 0 to `length`; no badge; zoom `raw`; marks `1` and `2` with the times of their rows (a
  constant `MARKS_TABLE` set from the take), in turn, inside the hold; `validateStory` passes with a
  take with no press, zoom `raw` and marks `1`, `2`, on `win32`; and the "Expected result" block of
  `clip.md` equals `EXPECTED` imported from the shipped `scenario.mjs`, character for character.
  A second test: the shipped `stage/launch-checklist.md` is the text of section 1's stage (a
  constant in the test), so a changed stage is seen.
- `docs/demo-video/clip-kit/lib/check.test.mjs`: the test "the shipped scenarios declare their
  checks" gains `table-anchors` (dynamic `import` of the shipped `scenario.mjs`):
  `resolveChecks(checks)` gives `{ editMode: "on", paste: false }`; its title names the table clip.
- `docs/user/editing.md`: under the paragraph "In edit mode a pipe table or a `{list-table}` shows a
  handle left of each body row ... keep their places." (inside the "Inline editing" item, indented
  two spaces as the spreadsheet paste clip there), a blank line, the image
  `![In edit mode, the row "Fix the login bug" is dragged by its handle to the top of a pipe table, then the "Due" column by its handle to the first place: the raw Markdown beside follows each move and every cell keeps its spacing](../demo-video/clips/table-anchors/table-anchors.gif)`,
  then a blank line before "Typing `/` at a line start ...".
- `test/site/siteClips.test.ts`: a test "the shipped editing page plays the table handles clip as
  video", modelled on "the shipped editing page plays the spreadsheet paste clip as video": it
  reads the shipped `docs/user/editing.md`, renders it with `renderMyst` and `clipVideos`, asserts
  `<video src="../demo-video/clips/table-anchors/table-anchors.webm"` and that
  `table-anchors.webm`, `.gif` and `poster.png` exist; marker `// @tests_req SwRS-MDOKFSTUDIO-CORE-095`
  (an added test of an existing SwRS, no SwRS text change); then `just requirements-update`.
- No change to the kit's code, the recipe, `.agents/glossary/common.md`, the writing skill (no
  rendered syntax changes), `README.md`, `CHANGELOG.md` or `docs/releases-notes/` (no `feat` or
  `fix` commit).

### 6. Host and default matrix

The clip films defaults only (no setting), with mouse drags; the platform changes only the window
and the off-camera chords of the layout.

| Host | VS Code | Settings | Expected | Proof |
| --- | --- | --- | --- | --- |
| Windows 11, CDP mouse drag | the kit's pinned `DEFAULT_CODE_VERSION` (1.147.0 unless moved) | defaults | `launch-checklist.md` equals `EXPECTED`; page and editor show the row then the column order | the take's `run` checks and `verify`, `check.json` ("scenario verify passed") |
| macOS | same | defaults | same | not proved (no macOS take) |
| Linux | same | defaults | same | not proved |

### 7. Commits and the pull request

- Branch from `origin/main`. Commits by area (Conventional Commits; no scope on `docs` or `test`,
  per `.agents/guidelines/git-commit-allowed-scopes.md`):
  `docs: add the table row and column handles feature clip` (clip folder, `docs/user/editing.md`),
  `test: check the table handles clip storyboard and its docs page` (`storyboard.test.mjs`,
  `check.test.mjs`, `siteClips.test.ts`, the files `just requirements-update` changes).
- The PR is opened as a draft (`gh pr create --draft`) and stays a draft until the owner approves
  the storyboard and the clip in it (Q3); the agent does not mark it ready.
- The PR body follows `.github/PULL_REQUEST_TEMPLATE.md`, the PR guideline and the clip PR rule: the
  GIF inline from
  `https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/table-anchors/table-anchors.gif`,
  the MP4 and WebM linked with the same form at the same head; after each push of a new render the
  links move to the new head (`gh pr edit <n> --body-file <file>`); check that the GIF plays in the
  rendered PR page (else the `-assets` fallback the kit's PR rule names).
- A section "Deviation from the feature clip process": the recipe's storyboard review before the
  take was moved after it, into this PR, under the owner's rule of the first clip stack (Q3); the
  take was filmed from the Griller's draft; how a review lands: an *(on screen)* row changed by the
  owner is a render (`just clip table-anchors render` then `check`), a *(filmed)* row is a retake,
  a follow-up of this CR.
- The body states what the clip proves (real drags by the row and column handles in a real VS Code
  window move a row then a column, the raw table follows with each cell's spacing kept: the take's
  checks and `verify`) and what the owner judges (motion, rhythm, the loop as watched, the absence
  of a floating drag image, the focus ring on the moved handle, the texts, "handle" for the owner's
  "anchor"); it links `clip.md` for the storyboard review.
- "Autonomous decisions": the differences from the draft (section above), the key frame names, the
  wait for the render between the two drags, the times, and the Q9 fallback if it was used.

## Out of scope

- Any change to `src/` or to an SwRS text; the keyboard moves (Alt+Up, Alt+Down, Alt+Left,
  Alt+Right); a `{list-table}`; a move while a cell editor is open; a table inside a quote or an
  admonition.
- A floating drag image (the CDP drag has none): written in the review notes, not fixed.
- Any change to the clip kit or the recipe; a macOS or Linux take; placing the clip in release notes
  or the announcement (a release CR does it).
- A retake after the owner's review (a follow-up of this CR, Q3); marking the PR ready before the
  owner approves the storyboard and the clip; a change of the recipe's storyboard order.

## CI

No CI job changes. The new kit tests run in `just check` through `just clip-kit-test`, inside the
existing `ci-static` job (Linux and Windows, `.github/workflows/ci.yml`); the site test runs where
`test/site/` tests run today. They need no `ffmpeg`, VS Code download, Remotion or display: they
read the shipped `clip.md`, `scenario.mjs`, stage, `docs/user/editing.md` and the clip's committed
files (Git LFS checked out as CI does for the merged clips' site tests).

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows; the storyboard, stage and scenario tests
   read the shipped `clip.md`, `stage/launch-checklist.md` and `scenario.mjs` at the head under
   test; the site test reads the shipped `docs/user/editing.md`.
2. `just clip table-anchors all --vsix ...` passes; `check.json` shows `passed: true`, MP4 and WebM
   1280x720 at 15 fps, MP4 duration 12.0 s within one frame, GIF at most 960 px and 12 fps, loop
   seam SSIM in [0.98, 1.0), "Studio in edit mode at the start", no paste line,
   `verifyPassed: true`, playback rate inside 0.77 to 1.3, platform `win32`, extension source
   `vsix`.
3. The agent looks at the contact sheet and every key frame: Studio on the left in edit mode with
   its 7 handles, the text editor on the right; the drop line above "Write the notes"
   (`row-drag`); the row first in the page and the raw text (`row-dropped`); the drop line left of
   "Task" (`column-drag`); Due, Task, Team in the page and every raw line reordered and aligned
   (`column-dropped`); mark 1 on the line of "Fix the login bug" and mark 2 on the Due cells of all
   six table lines in the zoomed raw text; Text 1 during the drags and Text 2 during the zoom; no
   tooltip (the handles' `title` must not show), no personal name or path, no dirty tab. What was
   not checked (motion, rhythm, the loop as watched) is said.
4. `just requirements-update` leaves the tree clean after its commit; `just preflight` passes (on
   Windows, its static stage).
5. The PR is a draft; its body plays the GIF, links the MP4 and WebM at the head sha and holds the
   "Deviation from the feature clip process" section.

## Open questions

None for the owner: the answers, the draft and the code settle the clip.
