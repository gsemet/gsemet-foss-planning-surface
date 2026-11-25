# Feature clip: paste spreadsheet cells into a table

Short name: `clip-paste`. No tracker issue (verbal request of the owner, 2026-11-25).

## Goal

A feature clip of Studio, made with the clip kit and the feature clip recipe as the CR
`short-demo-video-of-the-smart-raw-markdo` (short name `raw-copy-demo`, CR 484) leaves them. It
shows that a table in Studio takes a block of spreadsheet cells as a spreadsheet does: copy the
cells, click a cell of the table, paste. The cells fill from the clicked cell rightwards and
downwards, and the columns and rows the table lacks are added. Moving a list of tasks or figures
from a sheet into a Markdown document is a common chore; the clip shows it done in one paste.

The kit films the VS Code window only (a CDP screencast of its page), so the "spreadsheet" is a
tab-separated file, `tasks.tsv`, open in VS Code's text editor beside Studio. A copy from Excel,
LibreOffice or Google Sheets puts the same tab-separated `text/plain` on the clipboard, and that is
what the table cell reads (`spreadsheetGrid` in `src/page/modules/tableGridPaste.ts`).

The clip shows existing behaviour (`SwRS-MDOKFSTUDIO-TABLE-120`, the paste handler of
`src/page/features/tableCellEditor.ts`, `fillGrid`); no behaviour of the extension changes. One
continuous shot, two captions in turn, two orange marks in turn, combined key badges, 1280x720 at
15 fps, no card, the logo top right, a loop; MP4, WebM and GIF in
`docs/demo-video/clips/paste-spreadsheet-cells/`.

## Dependency and base

- This CR runs after `raw-copy-demo` (`depends.json`). That CR (not merged when this spec is
  written) gives: the Markdown storyboard contract (`## Clip` table with `Length`, `Size`,
  `Frame rate`, `Outputs`, `Cards`, `Logo`, `Setting filmed`, `Filmed on`, `Stage`; one
  `## <n>. <beat>` section per beat with `Time`, `Shot *(filmed)*`, `Text <n> *(on screen)*`,
  `Badge <id>`, `Zoom`, `Mark <id>`; the "Expected paste" fenced block read as `expectedPaste`),
  captions and marks in turn, combined badges `Ctrl+C / ⌘C`, size and frame rate read from the
  storyboard, the key frames `01-selected`, `02-pasted`, `03-zoomed`, `<NN>-mark-<id>`, the tests
  in `docs/demo-video/clip-kit/lib/storyboard.test.mjs` run by `just clip-kit-test` inside
  `just check`, and the clip PR rule (the GIF inline from the PR's head, the MP4 and WebM linked at
  the same head).
- This clip is filmed in **edit mode** (a table cell opens only there). The kit as `raw-copy-demo`
  leaves it wants "Studio in reading mode at the start" in `check`. The CR `clip-drag-list-item`
  (CR 485, pending in batch-09) owns the generic kit change that lifts it: a scenario export
  `checks = { editMode, paste }`, `resolveChecks` and `takeLines` in `lib/check.mjs`, with their
  tests; its spec says the other clips reuse them and do not write their own. This CR uses it as
  CR 485 lands it and changes nothing in the kit. See clip-paste-cells-Q4 (`depends.json` names CR 485).
- Base: the batch's stack branch that holds CR 485's kit change (CR 485's branch when stacked),
  else `origin/main` once CR 484 and CR 485 are merged (fetch first: the local `main` is behind
  `origin/main`).
- Where CR 484 or CR 485 lands differently from its spec (a field name, a frame name, a test file
  name, the `checks` shape), this CR follows what was merged and says so in the PR's "Autonomous
  decisions".
- The kit needs nothing else for this clip: two logged presses (`copy`, then `paste`) give
  `01-selected.png` (just before the copy) and `02-pasted.png` (0.3 s after the paste) as the kit
  takes them from `take.presses[0]` and `take.presses.at(-1)` (`lib/encode.mjs`). So the scenario
  logs **no other press**: any other key it sends goes through `t.page.keyboard`, not `t.press`.

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| clip-paste-cells-Q1 | The clip is filed from the owner's request for 6 to 7 feature clips made with the recipe, one CR per clip; this CR is this clip only, made with the kit and the recipe as `raw-copy-demo` leaves them | whole spec, "Out of scope" |
| clip-paste-cells-Q2 | The captions, the stage and the timing are the Griller's proposal (`work/storyboard/clip.md` and `work/storyboard/stage/` of this CR's folder); the owner reviews them at the storyboard gate | sections 1, 2 |
| clip-paste-cells-Q3 | The storyboard review is the owner's, in the PR: the batch films the trial take from the Griller's draft, puts its pictures in the storyboard, renders the clip and opens the PR with the clip watchable; the PR stays a draft until the owner approves the storyboard and the clip there (the recipe's gate is moved after the take, not dropped); the deviation is reported in this spec and in the PR body; a retake after the owner's review is a follow-up of this CR | "Deviation from the recipe", section 7, "Out of scope" |

From `01-intent.md` (the request, not an answer): the stage is `tasks.tsv` in VS Code's text editor
beside Studio; the clip is 1280x720 at 15 fps, two captions in turn, several marks in turn, combined
badges, no card, logo top right, a loop; its folder is `docs/demo-video/clips/paste-spreadsheet-cells/`;
the PR shows the GIF inline and links the MP4 and WebM at its head.

### Deviation from the recipe (clip-paste-cells-Q3)

The recipe `docs/demo-video/guidelines/feature-clip-process.guidelines.md`, a project guideline, as
`raw-copy-demo` leaves it ("The storyboard first"), has the maintainer review and edit the
storyboard draft, with a picture per key moment from a trial take, before the take. This CR moves
that gate after the take, by the Chief of Staff's decision under the owner's overnight autonomy:
the batch films the take from the draft `work/storyboard/clip.md` of this CR's folder, puts the
take's pictures and times in the storyboard (committed with `status: draft`), renders the clip and
opens the PR with the clip watchable. The owner reviews the storyboard and the clip in that PR,
which stays a draft until the owner approves both. The gate is moved, not dropped. The PR body
reports the deviation (section 7). A project guideline ranks above an answer (`AGENTS.md`,
"Instruction precedence"): this is the conflict report.

## What changes

All paths are relative to the repository root. No change to `src/`, to an SwRS text, to
`package.json` or the lock files; no new dependency; no change to the kit
(`docs/demo-video/clip-kit/`) beyond the test case of section 5.

### 1. The stage: `docs/demo-video/clips/paste-spreadsheet-cells/stage/`

Copied from `work/storyboard/stage/` of this CR's folder (wherever the batch moved it), byte for
byte. LF line endings and one final newline (the repository's `.gitattributes` gives `eol=lf`).

`stage/release-checklist.md`:

```markdown
# Release 2.4 checklist

| Task | Owner |
| --- | --- |
| Freeze the branch | Ana |
```

`stage/tasks.tsv`: five lines of three values separated by one tab character each, a header line
included (`\t` is a tab):

```text
Task\tOwner\tDue
Freeze the branch\tAna\tMon
Run the migrations\tBen\tTue
Restart the workers\tChen\tWed
Announce the release\tDev\tThu
```

The tabs are real tab characters (the editor or a formatter must not turn them into spaces;
`.editorconfig`'s `indent_style = space` does not apply to the inside of a line, and no formatter
of `just check` reads `.tsv`; check the committed bytes with `od -c` or `git diff --stat`).

The paste goes from the clicked header cell "Task": the header and the existing row take the same
values again; only the column "Due" and three rows are new.

### 2. The live storyboard: `docs/demo-video/clips/paste-spreadsheet-cells/clip.md`

The Griller's draft `work/storyboard/clip.md`, brought into the format of `raw-copy-demo`'s
recipe (section 2 of the recipe) as below. The on-screen texts are the draft's, character for
character. The times are the proposal; the take sets the final ones (section 4), written in the
same commit as the render. The pictures are the kit's key frames.

````markdown
---
title: Feature clip paste-spreadsheet-cells
status: draft
date: <the day of the commit>
---

# Feature clip: paste-spreadsheet-cells

**This is the live storyboard, draft for the maintainer's review.** The clip is built from this
file: edit any row marked *(on screen)*, save, and run `just clip paste-spreadsheet-cells render`,
then `check`. Rows marked *(filmed)* describe the take: changing them means a new take. The clip is
one continuous shot, the copy on the right, the paste on the left, then a zoom on the table, with
two texts in turn; `**bold**` in a text takes the orange accent.

The spreadsheet is `tasks.tsv` in VS Code's text editor: the kit films the VS Code window only, so
a spreadsheet application cannot be in the shot. A copy from a spreadsheet puts the same
tab-separated text on the clipboard, which is what the table cell reads.

## Clip

| Field | Content |
| --- | --- |
| Length | 11.0 s |
| Size *(on screen)* | 1280x720 16:9 |
| Frame rate *(on screen)* | 15 fps |
| Outputs | silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | none of Studio; for the TSV to read as columns, `editor.tabSize` 22, `editor.detectIndentation` off and `editor.renderWhitespace` none in the clip's profile |
| Filmed on | Windows, VS Code <version from check.json>, extension <version> VSIX built from the branch |
| Stage | `stage/release-checklist.md` (Studio, left, edit mode: a table of 2 columns, a header and 1 row) and `stage/tasks.tsv` (text editor, right: 5 lines of 3 tab-separated values, a header included) |

## 1. Copy the cells, paste into the table

![The five lines of tasks.tsv selected in the text editor, before the copy](frames/01-selected.png)

![The table after the paste: three columns and four task rows, the cell editor open on "Task"](frames/02-pasted.png)

| Field | Content |
| --- | --- |
| Time | 0 to 4.8 s (drag 0.3 to 1.8 s, copy at 2.0 s, click on the cell "Task" at 3.2 s, paste at 3.8 s, Done at 4.5 s) |
| Shot *(filmed)* | Studio on `release-checklist.md` (left), `tasks.tsv` (right). The mouse drags over the five lines of `tasks.tsv`. Copy chord. The pointer moves to the table and clicks its header cell "Task": the cell editor opens. Paste chord. The table grows to 3 columns ("Due" added) and 5 lines (3 rows added). A click on Done closes the cell editor. |
| Text 1 *(on screen)* | Copy cells from a sheet, **paste** into a table |
| Badge copy *(on screen)* | Ctrl+C / ⌘C |
| Badge paste *(on screen)* | Ctrl+V / ⌘V |

## 2. Zoom on the table

![Zoom on the table](frames/03-zoomed.png)

![Mark 1 on the added column "Due"](frames/04-mark-1.png)

![Mark 2 on the three added rows](frames/05-mark-2.png)

| Field | Content |
| --- | --- |
| Time | 4.8 to 11.0 s (zoom from 5.0 s, held to 10.0 s, then back to the start for the loop) |
| Shot *(filmed)* | Zoom (at most 2x) on the rendered table in Studio: Task, Owner, Due; four task rows. |
| Zoom | table, hold to 10.0 s |
| Mark 1 *(on screen)* | Orange outline around the added column "Due", 5.6 to 7.2 s |
| Mark 2 *(on screen)* | Orange outline around the three added rows, 7.2 to 8.8 s |
| Text 2 *(on screen)* | Cells fill right and down, **rows and columns** added |

Expected paste, the scenario's check: `release-checklist.md` on disk after the paste (auto-save is
on) is exactly this text:

```markdown
# Release 2.4 checklist

| Task | Owner | Due |
| --- | --- | --- |
| Freeze the branch | Ana | Mon |
| Run the migrations | Ben | Tue |
| Restart the workers | Chen | Wed |
| Announce the release | Dev | Thu |
```

## Review notes

- VS Code's copy also puts `text/html` on the clipboard; the cell editor reads `text/plain` (a text
  with a tab is a grid paste), so the HTML is ignored.
- The drag covers the five whole lines; the last line break is not selected (a final line break
  would be dropped anyway). A partial first or last line would paste a partial cell.
- The paste goes from the clicked cell: clicking the header cell "Task" makes the header and the
  existing row take the same values again; only "Due" and the three rows are new, which the marks
  show.
- After the paste the cell editor reopens in the cell "Task"; Done closes it. Escape is Cancel and
  is not used.
- The clip ends with the larger table and starts with the small one: the loop seam is the kit's
  cross-fade back to the first frame.
- The raw screencast runs at about <rawFps from check.json> frames per second: the selection grows
  by steps.
````

Changes from the Griller's draft, all of form or settled by the code (listed in "Autonomous
decisions"):

- the `Format` row split into `Size`, `Frame rate` and `Outputs` (the kit reads them); the `Zoom`
  row added to section 2 (the kit reads the zoom from it; id `table`, the hold the section's `Time`
  states); the pictures linked to the kit's key frames; "Expected result" renamed "Expected paste",
  so `parseClip` returns it as `expectedPaste` and the test of section 5 compares it with the
  scenario;
- the closing of the cell editor: Done (a visible click, no key without a badge, nothing opened on
  the page; the code: the Done button `button[aria-label="Done editing"]` of the cell editor,
  `blockEditor.createEditorButtons`). The draft left it to the trial between a click below the
  table, Done and Ctrl+Enter. If Done misbehaves in the take, a click on the empty page below the
  table may replace it only if it opens nothing (no block editor, no selection outline), and the
  `Shot` row and the review note say which was filmed;
- the TSV columns: `editor.tabSize` 22, `editor.detectIndentation` off and `editor.renderWhitespace`
  none set for every language in the profile (the draft scoped `tabSize` to `[plaintext]`; the
  language VS Code gives a `.tsv` file is not proved, and nothing else in the shot is a text
  editor). `renderWhitespace` none keeps the selected tabs from showing as arrows;
- the review notes that the trial was to settle are written as facts, to be confirmed by the take
  (the note on `text/html`, the closing).

If the parser of CR 484 refuses two marks that touch (mark 1 ends at 7.2 s where mark 2 starts),
start mark 2 at 7.3 s and say so in "Autonomous decisions".

### 3. The scenario: `docs/demo-video/clips/paste-spreadsheet-cells/scenario.mjs`

In the style of `clips/raw-copy-balance-edges/scenario.mjs`: a header comment naming the scene
(spreadsheet cells, as tab-separated text in a text editor, copied and pasted into a header cell of
a Studio table in edit mode) and saying every text, badge and time is in `clip.md`; it imports
nothing, so a test can load it without VS Code. Selectors are Studio's own
(`src/page/features/tableCellEditor.ts`, `src/page/features/blockEditor.ts`).

- `stage = { "stage/release-checklist.md": "release-checklist.md", "stage/tasks.tsv": "tasks.tsv" }`;
  `open = ["release-checklist.md"]`.
- `settings`:
  `"workbench.editorAssociations": { "release-checklist.md": "markdown-okf-schema-studio.editor" }`
  (Studio opens the file, as in the raw copy clip; `tasks.tsv` stays the text editor),
  `"editor.tabSize": 22`, `"editor.detectIndentation": false`, `"editor.renderWhitespace": "none"`.
  No Studio setting.
- `checks = { editMode: "on", paste: true }` (CR 485's export; `paste` true: the scenario records
  `pasteWidgets`, which proves no VS Code paste-options widget showed).
- `export const EXPECTED`: the "Expected paste" text of section 2, the lines joined with `\n`, one
  final `\n`.
- Helpers, local to the scenario:
  - `editorLines(page)`: the non-empty `.monaco-editor .view-lines .view-line` of the text editor,
    top to bottom, with their text rectangles in page coordinates (as the raw copy scenario's
    `editorLines`).
  - `editMode(t)`: `{ frame, mode }`, the value of `data-sphinx-preview-edit-mode` on the frame's
    `document.documentElement`, read from a fresh frame with retries (the raw copy scenario's
    `readingMode`).
  - `tableShape(frame)`: the texts of the `th` of the first `table` in
    `#sphinx-myst-preview-content`, and the texts of the cells of each `tbody tr`.
  - `box(locator)`: `locator.boundingBox()` (page coordinates for a frame locator) as `{ x, y, w, h }`.
- `setup(t)`, off camera:
  1. `await t.frameOf()`, `t.sleep(1500)`; open `tasks.tsv` beside it as the raw copy scenario
     opens `notes.md`: `Control+p`, type `tasks.tsv`, `Control+Enter`, `t.sleep(1500)`. Studio is
     on the left, the text editor on the right;
  2. throw unless `editorLines` gives 5 lines (`tasks.tsv` is open and shows its five lines) and
     unless the x of "Owner" on line 1 and of "Ana" on line 2 differ by less than 4 px (the tab
     size holds: the values read as columns);
  3. edit mode on: if `editMode` is not `on`, click `[data-sphinx-preview-edit-toggle]` in the frame
     and poll until `on` (at most 20 tries of 250 ms); `t.record("readingMode", mode)` (the key
     keeps CR 485's name; it holds `data-sphinx-preview-edit-mode`); throw unless `on`;
  4. throw unless `tableShape` gives headers `Task`, `Owner` and one row `Freeze the branch`,
     `Ana`, and no `[data-sphinx-preview-table-cell-editor]` is open;
  5. park the pointer at the rest point: the blank area of the text editor, 80 px below the bottom
     of line 5, at the x of line 1's start plus 120 px (`t.moveTo(x, y, 0.1)`, `t.sleep(500)`). The
     clip starts and ends there.
- `run(t)`, the filmed action, on the `until(seconds)` schedule of the raw copy scenario, at the
  storyboard's times:
  1. at 0.3 s, the selection in the text editor: `t.moveTo` (0.5 s) to 1 px right of the left edge
     of line 1's text, at its vertical middle; `t.ev("click", t.pointer)`;
     `await t.page.mouse.down()`; `t.sleep(80)`; `t.moveTo` (0.9 s) to 12 px right of the right
     edge of line 5's text, at its vertical middle; `t.sleep(60)`; `await t.page.mouse.up()`;
  2. throw unless the editor shows a selection on five rows: the distinct tops of
     `.monaco-editor .view-overlays .selected-text` give 5 (record `selectedRows`);
  3. at 2.0 s, `t.press("ControlOrMeta+C", "copy")`;
  4. at 2.2 s, `t.moveTo` (0.8 s) to the centre of the text of the `th` "Task" in the frame; at
     3.2 s, `t.click()`; wait at most 2 s for `[data-sphinx-preview-table-cell-editor] textarea`
     whose value is `Task`, else throw "the cell editor did not open on the header cell Task";
  5. at 3.8 s, `t.press("ControlOrMeta+V", "paste")`; `t.sleep(250)`; record `pasteWidgets` =
     `page.locator(".post-edit-widget").count()`, throw unless 0;
  6. wait at most 3 s until `tableShape` gives headers `Task`, `Owner`, `Due` and the four rows of
     `EXPECTED`, and the cell editor's textarea is open again with the value `Task` (TABLE-120:
     "reopen the editor in that cell"); else throw with what the page shows. A difference is a
     finding against the feature (recipe, section 6), never fixed in the scenario;
  7. at 4.1 s, `t.moveTo` (0.4 s) to the centre of the cell editor's `button[aria-label="Done editing"]`;
     at 4.5 s, `t.click()`; wait at most 2 s until no `[data-sphinx-preview-table-cell-editor]`
     remains, else throw;
  8. at 5.0 s, `t.zoom("table", rect)`: the box of the `table`, padded by 24 px, then grown around
     its centre to at least half the window's width and half its height (a zoom of at most 2x)
     and clamped to the window;
  9. at 5.6 s, `t.mark("1", rect)`: the union of the third `th` and the four third `td` (the column
     "Due"), with 6 px of air left and right and 3 px above and below, as the raw copy scenario
     does; at 7.2 s, `t.unmark("1")`;
  10. at 7.2 s (or 7.3 s, section 2), `t.mark("2", rect)`: the union of the 2nd, 3rd and 4th
      `tbody tr` (the three added rows), with the same air; at 8.8 s, `t.unmark("2")`;
  11. at 10.0 s, `t.unzoom("table")` and `t.moveTo(home.x, home.y, 0.6)`; `until(11.0)`.
- `verify(t)`: poll `t.workspaceFile("release-checklist.md")` for up to 3 s (auto-save is
  `afterDelay`, 200 ms) and throw
  `` `release-checklist.md does not hold the expected text. On disk: ${JSON.stringify(text)}` ``
  when it never equals `EXPECTED`; return `{ text }`. A difference (for example a delimiter cell
  other than `---` for the added column) is a finding against the feature: it stops the work and
  is reported with the text on disk; the storyboard is not changed to match.

### 4. Take and render

On Windows, on the batch's machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`):

```bash
just dev
just package          # out/reports/package/markdown-okf-schema-studio.vsix, from the branch
just clip paste-spreadsheet-cells doctor
just clip paste-spreadsheet-cells all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

- A trial first (the recipe's section 1), adapted to this clip: (a) the preview webview and the
  text editor are in the frames; (b) the CDP mouse drag selects the five lines in the text editor
  (`run` step 2); (c) the CDP copy chord in the text editor and the paste chord in the cell editor
  carry the tab-separated text (`run` step 6; if the copy does not reach the clipboard, the kit's
  `CLIP_KEY_COMMANDS=1` fallback, which rides the editing command on the key event, is allowed and
  said in the PR); (d) the retimed rate is at least the storyboard's frame rate. If (b) or (c)
  fails otherwise, stop and report: no scripted clipboard write and no OS-level input or capture
  stands in for the copy the clip shows.
- The take's frames give the storyboard's pictures (Q3: the pictures of the take, not of a separate
  trial before the take).
- `Length` and every time in `clip.md` follow the take (playback rate inside 0.77 to 1.3), in the
  same commit as the render; the captions stay end to end from 0 to `Length`, the marks inside the
  zoom hold, in turn.
- Commit together (the recipe's rule): `clip.md`, `scenario.mjs`, `stage/`,
  `paste-spreadsheet-cells.mp4`, `.webm`, `.gif` (Git LFS through `.gitattributes`), `poster.png`,
  `contact-sheet.png`, `first-last.png`, `frames/*.png`, `check.json`.

### 5. Tests

`node:test` and `node:assert/strict`, Node built-ins only, no ffmpeg, no VS Code, no network:

- `docs/demo-video/clip-kit/lib/storyboard.test.mjs` (CR 484's file) gains a case that reads the
  **shipped** `docs/demo-video/clips/paste-spreadsheet-cells/clip.md` from the repository (path
  from the test file's own location, at the head under test, never a copy) with `parseClip`, and
  asserts: length equal to the committed value; size 1280x720; 15 fps; exactly two captions, in
  order, with the texts `Copy cells from a sheet, **paste** into a table` and
  `Cells fill right and down, **rows and columns** added` (as the parser returns them, `**` kept
  or stripped as CR 484's parser does), end to end from 0 to the length; badges `copy` =
  `Ctrl+C / ⌘C` and `paste` = `Ctrl+V / ⌘V`; zoom `table`; marks `1` and `2`, in turn, inside the
  hold. It imports `EXPECTED` from the shipped `scenario.mjs` and asserts it equals the
  `expectedPaste` of the shipped `clip.md`, character for character (with the final newline
  handled as CR 484's raw copy case does). It runs `validateStory` on the parsed story with a
  `take` listing presses `copy` and `paste`, zoom `table` and marks `1`, `2`, for `win32` and for
  `darwin`: both pass.
- The test of CR 485 that reads each clip's shipped `scenario.mjs` and passes its `checks` to
  `resolveChecks` gains this clip: `paste-spreadsheet-cells` gives `{ editMode: "on", paste: true }`.
- `test/site/siteClips.test.ts`: a test "the shipped editing page plays the spreadsheet paste clip
  as video", modelled on "the shipped settings page plays the raw copy clip as video": it reads the
  shipped `docs/user/editing.md`, renders it with `renderMyst` and `clipVideos`, asserts the
  `<video src="../demo-video/clips/paste-spreadsheet-cells/paste-spreadsheet-cells.webm"` and that
  `paste-spreadsheet-cells.webm`, `.gif` and `poster.png` exist; marker
  `// @tests_req SwRS-MDOKFSTUDIO-CORE-095` (an added test of an existing SwRS, no SwRS text
  change); then `just requirements-update`.
- No prepared text: every case reads a shipped file.

### 6. Docs

- `docs/user/editing.md`, in the "Inline editing" item, after the sentence "Editing a table cell
  adds the inline buttons (bold, italic, link, colour, emoji and so on) to the row and column bar.":
  one sentence, then the clip's GIF on its own line, indented two spaces as the item's lines are
  (the recipe's section 4: under the entry of the feature; the page has no sentence on the
  spreadsheet paste today):
  - `Cells copied from a spreadsheet (tab-separated text) and pasted into an open table cell fill the
    cells from that one, rightwards and downwards; the columns and rows the table lacks are added,
    in one undo step.` (the behaviour of `SwRS-MDOKFSTUDIO-TABLE-120`, unchanged);
  - `![Five lines of tab-separated tasks are copied from a text editor with Ctrl+C / ⌘C and pasted with Ctrl+V / ⌘V into the header cell of a two-column table in Studio: a Due column and three rows are added](../demo-video/clips/paste-spreadsheet-cells/paste-spreadsheet-cells.gif)`.
- The site turns the GIF into a video of the WebM (`SwRS-MDOKFSTUDIO-CORE-095`, unchanged).
- No change to the recipe (CR 484 and CR 485 give everything this clip uses), to
  `.agents/glossary/common.md`, `README.md`, `CHANGELOG.md` or `docs/releases-notes/` (no `feat` or
  `fix` commit), or to the writing skill (no rendered syntax changes).

### 7. Commits and the pull request

- Commits by area, Conventional Commits (`.agents/guidelines/git-commit-message.guidelines.md`), no
  scope on `docs` or `test`:
  1. `docs: add the paste spreadsheet cells feature clip` (the clip folder, `docs/user/editing.md`);
  2. `test: check the spreadsheet paste clip's storyboard and its docs page` (the kit test cases,
     `siteClips.test.ts`, the requirements files `just requirements-update` changes).
- The branch sits in batch-09's stack above CR 485 (`.agents/guidelines/stacked-prs.guidelines.md`):
  the PR targets the branch below it until that merges, and is restacked by the agent that owns
  the stack. CR 485 also adds a clip to `docs/user/editing.md` and a test to
  `test/site/siteClips.test.ts`: the restack keeps both.
- The PR body follows `.github/PULL_REQUEST_TEMPLATE.md`, the PR guideline and the clip PR rule of
  the recipe: Impacts shows the GIF inline from
  `https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/paste-spreadsheet-cells/paste-spreadsheet-cells.gif`
  and links the MP4 and WebM with the same form at the same head; after each push of a new render,
  the links move to the new head (`gh pr edit <n> --body-file <file>`); check that the GIF plays in
  the rendered PR page; if not, the three files go to the `-assets` side branch as the recipe says,
  and the body says so.
- The body states what the clip proves: on Windows, in a real VS Code window, five tab-separated
  lines copied from a text editor and pasted into the header cell "Task" of a two-column table
  fill the table from that cell, add the column "Due" and three rows, reopen the cell editor in
  "Task", and the file on disk is exactly the expected text (the take's `run` checks and `verify`,
  `check.json`). It states what the owner judges: motion, rhythm, the loop as watched (the table
  shrinks back at the seam), the texts and their accent, the tab-separated file standing for a
  spreadsheet. It links `clip.md` for the storyboard review.
- The PR is opened as a draft (`gh pr create --draft`) and stays a draft until the owner approves
  the storyboard and the clip in it (clip-paste-cells-Q3); the agent does not mark it ready. Its
  body has a section "Deviation from the recipe": the recipe's storyboard review before the take
  was moved after it, by the Chief of Staff's decision under the owner's overnight autonomy; the
  take was filmed from the Griller's draft; the owner's review of `clip.md` and of the clip happens
  on this PR, before it leaves draft; a retake after that review is a follow-up of this CR.
- "Autonomous decisions": the changes to the draft listed in section 2 (fields split, `Zoom` row,
  "Expected paste", Done to close the cell editor, the editor settings for every language); the
  rest point; the zoom box rule (at most 2x); the marks' boxes; the selection check on five rows;
  `checks` with `paste` true; the docs sentence and alt text; the test cases; any difference
  between CR 484 or CR 485 as merged and their specs.

## Out of scope

- Any change to `src/`, to an SwRS text or to the kit's code; the feature is filmed as it behaves.
- A real spreadsheet application in the shot (the kit films the VS Code window only), a paste into
  a body cell, a `{list-table}`, a paste of a single value or of text without a tab.
- A macOS or Linux take (macOS Cmd+C and Cmd+V stay not proved in a real window).
- A retake after the owner's review (a follow-up of this CR, clip-paste-cells-Q3); marking the PR
  ready before the owner approves the storyboard and the clip.
- Placing the clip in release notes, an announcement or the README.
- The other planned feature clips (their own CRs).

## CI

No CI job changes. The new test cases run in `just check` through `just clip-kit-test` (CR 484),
inside the existing `ci-static` job (Linux and Windows, `.github/workflows/ci.yml`); the site test
runs where `test/site/` tests run today.

- Environment: the CI machine set up by `just dev-ci` from the lock files, Node.js 24 from `.nvmrc`
  through `fnm`. Absent there and present locally: `ffmpeg`, the kit's scratch folder, the VS Code
  download, Remotion, a display. The tests need none of them: the shipped `clip.md`,
  `scenario.mjs` and `docs/user/editing.md` read from the repository, and the clip's committed
  files (Git LFS checked out as CI does for the raw copy clip's site test).
- Before the push: `just clip-kit-test`, `just check` and `just ci-static` on Windows; the outputs
  go in the evidence.
- Only the first CI run proves the Linux leg (the dynamic `import` of the shipped scenario from a
  repository path, path handling, the LFS files present for the site test).

## Host and default matrix

The clip depends on the host (the platform's copy and paste chords; Windows filmed). It films no
Studio setting: every Studio setting is at its shipped default. The editor settings of the profile
only lay out the TSV.

| Host | VS Code | Studio settings | Expected | Proof |
| --- | --- | --- | --- | --- |
| Windows 11, `Ctrl+C` / `Ctrl+V` through CDP | pinned `DEFAULT_CODE_VERSION` (1.147.0 unless moved) | defaults | the table gains "Due" and three rows; the cell editor reopens on "Task"; `release-checklist.md` equals the expected text | the take's `run` checks and `verify`, `check.json` ("scenario verify passed") |
| macOS, `⌘C` / `⌘V` | same | defaults | same | not proved (no macOS take); the real-window test `test/integration/realInput/tableGridPaste.ts` covers the paste on the CI's platforms |
| Linux | same | defaults | same | not proved by the clip (same integration test) |

The new tests run on Windows locally and on Linux and Windows in `ci-static`.

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows; the storyboard case reads the shipped
   `clip.md` and imports the shipped `scenario.mjs` at the head under test; the site test reads the
   shipped `docs/user/editing.md` and the committed clip files.
2. `just clip paste-spreadsheet-cells doctor` passes, then `all --vsix ...`: `check.json` shows
   `passed: true`, MP4 and WebM 1280x720 at 15 fps, the MP4 duration equal to `Length` within one
   frame, GIF at most 960 px and 12 fps, loop seam SSIM in [0.98, 1.0), "Studio in edit mode at
   the start", `pasteWidgets: 0`, `verifyPassed: true`, playback rate inside 0.77 to 1.3, platform
   `win32`, extension source `vsix`.
3. The agent looks at the contact sheet and every key frame: `01-selected` shows the five lines
   selected with no whitespace arrows and the values in columns; `02-pasted` shows the table with
   Task, Owner, Due and four rows, the cell editor on "Task"; `03-zoomed` the table zoomed, no cell
   editor; `04-mark-1` the outline on the column "Due" with its header; `05-mark-2` the outline on
   the three added rows; Text 1 during the copy and paste, Text 2 during the zoom; the badges
   `Ctrl+C / ⌘C` and `Ctrl+V / ⌘V`; no tooltip; no personal name or path; no dirty tab. What was not
   checked (motion, rhythm, the loop as watched) is said.
4. The raw copy clip is not affected (no kit code change); `just clip-kit-test` keeps its cases
   green.
5. `just requirements-update` leaves the tree clean after its commit; `just preflight` passes (on
   Windows, its static stage).
6. The PR is a draft; its body plays the GIF and links the MP4 and WebM at the head sha (or on the
   `-assets` branch, said so), and holds the "Deviation from the recipe" section.

## Amendment (2026-11-25, Chief of Staff, owner asleep): no reopen check, no Done click

The trial take showed that after the CDP paste the table is correct (Task, Owner, Due, four rows) but the TABLE-120 cell editor does not reopen on "Task" (3 of 3 runs, also after Ctrl+A). The real-input integration test passes the reopen check, so this may be a CDP artefact; it is not established, and it is filed apart as a bug. This amendment overrides the steps above:

- Step 6 no longer waits for the cell editor to reopen: it waits only for `tableShape` to give the headers `Task`, `Owner`, `Due` and the four rows of `EXPECTED`, and `pasteWidgets` of 0.
- Step 7 (the move to Done and the click on `button[aria-label="Done editing"]`) is dropped; the scene ends on the pasted table. The storyboard's "Done" beat and its timing (Done at 4.5 s) go with it; the zoom of step 8 follows the paste directly.
- The reopen check stays covered by the real-input integration test. The clip makes no claim about the editor reopening.

## Open questions

None. The dependency on CR 485 is settled by clip-paste-cells-Q4: `depends.json` names CR 485, and this CR goes above it in the stack.
