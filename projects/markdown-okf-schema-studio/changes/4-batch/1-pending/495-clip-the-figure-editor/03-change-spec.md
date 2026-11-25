# Feature clip: edit a figure in one form

Short name: `clip-figure`. No tracker issue (verbal request of the owner, 2026-11-25).

## Goal

A feature clip of Studio's figure editor. In edit mode the writer points at a figure, presses its
**Edit figure** button and gets one form for the whole figure: Source, Alt text, Caption, Legend,
Width, Align and Name. They change the caption, set the width to 40%, align the figure right and
give it a name, then apply. The text box holds a clean `{figure}` directive: the untouched lines
are kept as they were and the new option lines are added under them. The save chord shows the
smaller figure floating right of the text. Nobody has to remember the option names or the
directive layout.

The clip is made with the merged clip kit (`docs/demo-video/clip-kit/`) and the feature clip
recipe (`docs/demo-video/guidelines/feature-clip-process.guidelines.md`): one continuous shot, two
captions in turn, two marks in turn, 1280x720 at 15 fps, no card, the logo top right, a loop,
12.0 s. It lives in `docs/demo-video/clips/figure-editor/`. The pull request plays the clip, and the
owner reviews the storyboard and the clip there.

The clip shows existing behaviour: the Edit figure button and the figure form
(`src/page/modules/figurePanel.ts`, `openFigurePanel` and `openFigureEditor` in
`src/page/features/editorChrome.ts`, `SwRS-MDOKFSTUDIO-PALETTE-153`), the text the form writes
(`applyValues` and `serializeFigure` in `src/page/modules/figureDirective.ts`,
`SwRS-MDOKFSTUDIO-PALETTE-160`), and the figure's rendering (`src/core/directives/figure.ts`,
`src/page/modules/figureSizes.ts`, `SwRS-MDOKFSTUDIO-MYST-031`). No behaviour of the extension
changes.

## Dependency and base

- Built on `origin/main`, alone (figure-editor-Q4). There is no `depends.json`, and the CR depends
  on none of the other clips of this round. Fetch first: the local `main` is behind `origin/main`.
- The kit on `origin/main` already has everything this clip needs: the scenario export
  `checks = { editMode, paste }` (resolved by `resolveChecks` in `lib/check.mjs`), the helper
  `t.keyFrame(name)`, the `Size`, `Frame rate`, `Zoom` and several `Mark <id>` rows, combined
  badges, and the clip PR rule. This CR makes **no kit change**. If the kit cannot film or render
  this clip, the Driver stops and reports the gap.
- The closest shipped models are `docs/demo-video/clips/slash-menu-grid/` (edit mode, typed keys
  with no badge, one badged save chord, an `EXPECTED` constant compared with the storyboard's
  "Expected result" block) and `docs/demo-video/clips/export-html/` (a stage file read from the
  clip folder with `new URL(..., import.meta.url)` in `verify`).

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| figure-editor-Q1 | Filed from the owner's request: a clip of the figure editor (image, caption, label and its options) | Goal |
| figure-editor-Q2 | The captions, stage and timing of the storyboard draft are the Griller's proposal; routine gaps are the Griller's | sections 1 to 3, "Where this spec differs from the draft" |
| figure-editor-Q3 | The batch films a trial take from the draft, puts its pictures in the storyboard, renders, and opens the PR with the clip watchable (GIF inline, MP4 and WebM linked at the PR's head). The PR stays a draft until the owner approves storyboard and clip. The recipe's gate is moved after the take, not dropped; the deviation is reported here and in the PR body. A retake after the owner's review is a follow-up of this CR | "The storyboard gate, moved after the take", sections 4 and 7, "Out of scope" |
| figure-editor-Q4 | Built on `origin/main`, no `depends.json`, independent of the other clips | "Dependency and base" |
| figure-editor-Q5 | The clip edits an existing figure from the Edit figure button, never a new one from the Figure button (its Browse dialog is outside the filmed page) | section 3, "Out of scope" |
| figure-editor-Q6 | Stage: `harbour-guide.md` with a figure of `harbour-light.svg` (400x240, a lighthouse at dusk) and a three-line paragraph under it | section 2 |
| figure-editor-Q7 | Four fields change: Caption, Width `40%`, Align Right, Name `fig-harbour-light`; Source, Alt text and Legend stay as they are | sections 1 and 3 |
| figure-editor-Q8 | 12.0 s; if the trial runs longer, the Name step is dropped first | sections 1, 3 and 4 |
| figure-editor-Q9 | The form is filled from the keyboard after one click in Caption; Tab goes between fields; Align is set with a key, its list never opened; the save chord (`Ctrl+Enter / ⌘Enter`, badged) closes the box inside the one zoom | sections 1 and 3 |

## The storyboard gate, moved after the take

The recipe ("The storyboard first") has the maintainer review the storyboard draft, with a picture
per key moment from a trial take, before the take. figure-editor-Q3 moves that gate after the take,
into the pull request. It deviates from a project guideline and is reported as such:

- the batch films a trial take from the draft, puts the trial's pictures and measured times in the
  storyboard, moves it to `docs/demo-video/clips/figure-editor/clip.md`, films the take, renders and
  opens the PR;
- the PR is a draft (`gh pr create --draft`) until the owner approves the storyboard and the clip in
  it. The agent never marks it ready;
- the PR body has a section "Deviation from the feature clip process". It says that the storyboard
  is reviewed after the take (figure-editor-Q3), and how a review lands: a change to an
  *(on screen)* row is a render (`just clip figure-editor render`, then `check`), and a change to a
  *(filmed)* row is the follow-up retake;
- the recipe itself is not changed.

## What the code settles

Facts read on `origin/main`, to name the real controls. No choice is made here.

- **Edit mode** is `<html data-sphinx-preview-edit-mode="on">`, toggled by
  `[data-sphinx-preview-edit-toggle]`.
- **The Edit figure button** (`installFigureEditButton`, `figurePanel.ts`) is one
  `button[data-sphinx-figure-edit="true"]`, child of the body, text and `aria-label` "Edit figure",
  `hidden` until the pointer hovers a `<figure>` in edit mode. It is placed 6 px below the figure's
  top and 96 px left of its right edge; when that spot is under the sticky preview controls it moves
  left of them. It does not depend on the palette mode.
- **A click on it** (`openFigureEditor`, `editorChrome.ts`) opens the figure's block editor and then
  the form, once the source arrives. The form is `[data-sphinx-figure-panel="true"]`,
  `role="dialog"`, `aria-label="Edit figure"`, titled "Figure", inserted just above the text box
  (`edit.element.insertBefore(panel.element, control)`). The text box stays in place
  (`keepTextInPlace`). **Source is focused first, with its text selected** (`focusFirst`).
- **The fields** are `[data-figure-field="source" | "alt" | "caption" | "legend" | "width" |
  "align" | "name"]`. Caption and Legend are textareas, Align is a `<select>` with the options
  None (`""`), Left, Center and Right (`right`), and the others are one-line inputs. The Tab order is
  Source, Browse..., Alt text, Caption, Legend, Width, Align, Name, Apply, Cancel; Tab wraps only at
  the ends.
- **Keys of the form**: Enter in a one-line field (Name) applies; Enter in Caption or Legend is a
  newline; Ctrl/Cmd+Enter anywhere applies; Escape cancels. **Ctrl/Cmd+A in a text control selects
  that control's text** and is kept away from VS Code (`installSelectAllInControls`,
  `src/page/modules/selectAllKey.ts`).
- **Apply** rewrites the figure's range in the text box as one native edit and closes the form
  (`openFigurePanel`, `onSubmit`); `applyTextEdit` (`src/page/features/textControls.ts`) gives the
  focus back to the text box. The editor stays open. The save chord in the text box saves and closes
  it. The file on disk is written by the kit profile's `files.autoSave` (afterDelay).
- **What Apply writes** (`applyValues`, `serializeFigure`): the opening line and the `:alt:` line
  are kept as read; the new options are appended in the order width, align, name; one blank line
  stays before the body; the edited caption replaces the body. From the stage text this gives
  exactly the draft's expected result (section 1). If the Name step is dropped (figure-editor-Q8),
  the `:name:` line is absent and nothing else changes.
- **The rendering** (`SwRS-MDOKFSTUDIO-MYST-031`): the `<figure>` gets the class `align-right`
  (floats right, `src/core/directives/figure.ts`), its `<img>` carries `data-okf-width="40%"`
  (applied by `figureSizes.ts`), the `:name:` becomes the id, and the caption is the body.

## Where this spec differs from the draft

| Draft | This spec | Why |
| --- | --- | --- |
| `status: draft for the owner's review`, the opening paragraph of a review draft | `status: draft`, the opening paragraph of a live storyboard | the file becomes the live storyboard in the clip folder (the recipe), reviewed in the PR (Q3); as the shipped `slash-menu-grid/clip.md` |
| "The pointer clicks in Caption; its text is selected and replaced" | the click puts the caret in Caption; `ControlOrMeta+A` through `t.page.keyboard` (no badge, not a logged press) selects its text, then the new caption is typed over it | a click in a textarea does not select its text; Ctrl/Cmd+A stays in the control (`selectAllKey.ts`). A badge would need a `Badge` row the draft does not have |
| "Align is set to Right from the keyboard ("r")"; fallback `selectOption` | "r" first; if the trial shows the value unchanged, `ArrowDown` presses until `right`; only if both fail, the draft's `selectOption` fallback, said in the review notes and the PR | keeps the filmed action a key as long as one works (Q9) |
| "Pictures: from the batch's trial take" | section 1: `frames/button.png`, `frames/form.png`, `frames/filled.png`; section 2: `frames/03-zoomed.png`, `frames/04-mark-1.png`, `frames/05-mark-2.png`, `frames/rendered.png` (the draft's names). `frames/01-selected.png` and `frames/02-pasted.png`, which the kit writes at the one logged press (the save chord), are kept and not linked | `t.keyFrame` names; the kit's fixed names |
| `Filmed on`: "to be filmed by the batch" | Windows, the VS Code version of `check.json`, the extension version, "VSIX built from the branch" | the batch's take |
| Times proposed by the Griller | the take's own times, same beats and order, `Length` 12.0 s at most | the recipe: the storyboard follows the take; the kit refuses more than 12 s |

Everything else is carried as written: both *(on screen)* texts, the badge, the two marks, the
zoom, the stage, the shots, the expected result and the review notes.

## What changes

All paths are relative to the repository root. No change to `src/`, to a file of
`docs/demo-video/clip-kit/` other than its test files, to the recipe, to `package.json` or to a lock
file. No new dependency.

### 1. The live storyboard: `docs/demo-video/clips/figure-editor/clip.md`

Start from the draft `work/storyboard/clip.md` of this CR's folder (in the planning surface,
`C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/2-backlog/P2/clip-the-figure-editor/`,
or wherever the batch moved the folder), with only the changes of the table above.

- Front matter: `title: Feature clip figure-editor`, `status: draft`, `date:` the day of the commit.
- Opening paragraph, as in `slash-menu-grid/clip.md`: "This is the live storyboard. The clip is
  built from this file: edit any row marked *(on screen)*, save, and run
  `just clip figure-editor render`, then `check`. Rows marked *(filmed)* describe the take: changing
  them means a new take. The text of an *(on screen)* row is the clip's exact text (`**bold**` takes
  the orange accent)." Keep the paragraph on the one continuous shot and the two texts in turn. Drop
  "Once approved, this file becomes ..." and "The times below are the Griller's proposal ...".
- `## Clip` table as drafted: `Length` `12.0 s` (or the take's, at most 12), `Size *(on screen)*`
  `1280x720 16:9`, `Frame rate *(on screen)*` `15 fps`, `Outputs`, `Cards` `none`, `Logo`
  `top right`, `Setting filmed` "none (default palette mode and Cream theme; edit mode is set off
  camera)", `Filmed on` (the take's), `Stage` as drafted. The "Off camera (`setup`)" line as drafted.
- `## 1. Edit figure, fill the form`: the pictures `frames/button.png` (the Edit figure button over
  the figure), `frames/form.png` (the Figure form, filled from the directive, Source focused),
  `frames/filled.png` (the four new values in the form, just before Enter), each with an alt text
  saying what it shows. `Time` `0 to <t1> s (...)` with the take's action times. `Shot *(filmed)*` as
  drafted, with "its text is selected (Ctrl+A in the field) and replaced". `Text 1 *(on screen)*` =
  `**Edit figure** opens one form for the whole figure`.
- `## 2. The directive, then the page`: the pictures `frames/03-zoomed.png`, `frames/04-mark-1.png`,
  `frames/05-mark-2.png` and `frames/rendered.png`, with alt texts. `Time` `<t1> to <Length> s
  (...)`. `Shot *(filmed)*` as drafted. `Zoom` = `figure, hold to <s> s` (proposal 11.0). `Mark 1
  *(on screen)*` = `Orange outline around the three new option lines in the text box, <from> to <to>
  s`; `Badge save *(on screen)*` = `Ctrl+Enter / ⌘Enter`; `Mark 2 *(on screen)*` = `Orange outline
  around the rendered figure and its caption, <from> to <to> s`; `Text 2 *(on screen)*` = `Apply
  writes the **options** into the file`. The captions run end to end from 0 to `Length`; both marks
  lie inside the zoom hold, in turn.
- "Expected result" paragraph and its `markdown` fenced block as drafted, character for character
  (`harbour-guide.md` on disk is that text followed by one newline), then the three bullets read
  from the preview after the save chord, as drafted.
- "Review notes": every note of the draft, with these changes:
  - the note on `applyValues` and `serializeFigure` drops "The take proves it" for "The take checks
    it in the text box and on disk";
  - the note on the click in Caption says that the click places the caret and Ctrl+A (no badge)
    selects the field's text;
  - the note on Align says which key set it at the take ("r", or `ArrowDown`), or that the
    `selectOption` fallback was used and the shot shows only the value change;
  - added: `01-selected` and `02-pasted` are the kit's fixed key frame names, both at the save chord,
    and not linked;
  - added: the measured times and the raw screencast rate (`rawFps` of `check.json`), as the shipped
    `slash-menu-grid/clip.md` says them;
  - added: the storyboard is reviewed in the pull request after the take (figure-editor-Q3); not
    checked by the author: motion, rhythm, the loop as watched;
  - if the Name step was dropped (figure-editor-Q8): say so, with the measured length that made it
    necessary; the expected result, Mark 1 ("the two new option lines") and the bullets lose the name
    and the id.

### 2. The stage: `docs/demo-video/clips/figure-editor/stage/`

- `harbour-guide.md`: the draft's `work/storyboard/stage/harbour-guide.md`, byte for byte (LF, one
  final newline): the heading "Harbour guide", one sentence, the `{figure}` of `harbour-light.svg`
  with `:alt: A lighthouse on a rock at dusk` and the caption "The harbour light.", and the
  three-line paragraph.
- `harbour-light.svg`: the draft's `work/storyboard/stage/harbour-light.svg`, byte for byte (400x240;
  `*.svg` is plain text with LF in `.gitattributes`, not Git LFS).

### 3. The scenario: `docs/demo-video/clips/figure-editor/scenario.mjs`

In the shape of `clips/slash-menu-grid/scenario.mjs`. It imports Node built-ins only (`node:fs`
for `readFileSync`), does nothing at import, so the kit tests can load it. A header comment says
what is filmed and that every caption, badge and time is in `clip.md`.

- `stage = { "stage/harbour-guide.md": "harbour-guide.md", "stage/harbour-light.svg":
  "harbour-light.svg" }`; `open = ["harbour-guide.md"]`.
- `settings`: `"workbench.editorAssociations": { "harbour-guide.md":
  "markdown-okf-schema-studio.editor" }` only (every Studio setting at its default).
- `checks = { editMode: "on", paste: false }`.
- `export const EXPECTED`: the "Expected result" block of `clip.md`, lines joined with `\n`, no
  final newline. Constants `CAPTION = "Harbour light at dusk, from the north pier."`,
  `WIDTH = "40%"`, `NAME = "fig-harbour-light"`; `STAGE_MD` and `STAGE_SVG` are
  `new URL("stage/harbour-guide.md", import.meta.url)` and the same for the SVG, read only inside
  `setup` and `verify`.
- `setup(t)`, off camera:
  1. wait for the preview frame (`t.frameOf()`); throw if `harbour-guide.md` in the workspace
     differs from the clip's stage file, or if the page's `figure` has the class `align-right` (a
     previous take must not leak);
  2. edit mode as in the grid scenario (click `[data-sphinx-preview-edit-toggle]` when
     `data-sphinx-preview-edit-mode` is not `on`, re-reading a fresh frame), `t.record("readingMode",
     mode)`, throw unless `on`;
  3. record `data-sphinx-preview-theme-mode` of the page; throw when it names a theme other than
     Cream (a previous take must not leave another theme);
  4. throw if a block text box (`[data-sphinx-preview-block-editor] textarea`) or a figure form is
     open;
  5. wait until the figure's `<img>` has a natural width above zero (the SVG loaded);
  6. park the pointer in the page's empty right margin, away from the figure, so no Edit figure
     button and no hover outline show at frame 0; `t.sleep(500)`.
- `run(t)`, with an `until(seconds)` clock as in the grid scenario, at the draft's times as targets,
  with the recipe's pacing (moves 600 to 900 ms, 400 ms before a click or a chord):
  1. at about 0.2 s, `t.moveTo` (0.6 s) onto the figure's image (`t.rectOf` of the `figure img`);
     wait up to 2 s for `[data-sphinx-figure-edit="true"]` to be visible; `t.keyFrame("button")`;
  2. `t.moveTo` to the button's centre; at about 1.6 s, `t.click()`; wait up to 3 s for
     `[data-sphinx-figure-panel="true"]` and the text box; throw unless the fields read Source
     `harbour-light.svg`, Alt text `A lighthouse on a rock at dusk`, Caption `The harbour light.`,
     Legend, Width, Align and Name empty, and the focused element is the Source field;
     `t.record("formAtOpen", values)`; `t.keyFrame("form")`;
  3. at about 2.8 s, `t.moveTo` to the Caption field and `t.click()`;
     `t.page.keyboard.press("ControlOrMeta+A")`; throw unless the Caption field is focused with all
     its text selected; `t.page.keyboard.type(CAPTION, { delay: 25 })` (about 1 s);
  4. `Tab`, `Tab` (Legend, then Width), throw unless Width is focused; type `40%`;
  5. `Tab` (Align), press `r`; when its value is not `right`, press `ArrowDown` up to three times
     until it is; when it still is not, the draft's fallback `selectOption("right")` on the field,
     `t.record("alignBy", "r" | "ArrowDown" | "selectOption")`. The list is never opened (no click on
     the select, no Alt+Down);
  6. `Tab` (Name), throw unless Name is focused; type `fig-harbour-light`; throw unless the four
     fields read the new values and Source, Alt text and Legend are unchanged;
     `t.keyFrame("filled")`;
  7. at about 5.6 s, `t.page.keyboard.press("Enter")` (Name is a one-line field: Enter applies);
     wait up to 2 s for the form to be gone; throw unless the text box value equals the figure part
     of `EXPECTED` (from the line `:::{figure} harbour-light.svg` to its closing `:::`; the block
     editor of the figure holds that directive alone) and the text box has the focus; move the pointer back to the rest point;
  8. at about 6.2 s, `t.zoom("figure", rect)`: the union of the text box and the paragraph under it,
     padded 24 px (the kit limits the zoom to 2x). The rectangle is chosen so the rendered figure
     after the save also lies inside it; if the trial shows the figure outside, the rectangle is
     widened, never a second zoom;
  9. Mark 1 around the three new option lines in the text box (their rectangle: the box's
     left and right padding edges, the top of the `:width:` line to the bottom of the `:name:` line,
     measured with the textarea's line height and padding, or a mirror element; a few pixels of
     air), at the storyboard's times, then `t.unmark("1")`;
  10. at about 8.6 s, `t.press("ControlOrMeta+Enter", "save")`; wait up to 5 s for the text box to
      close and for the `figure` to have the class `align-right`; throw otherwise, with any status
      text the page shows; `t.keyFrame("rendered")` once its caption reads `CAPTION`;
  11. Mark 2 around the rendered figure and its caption (`t.rectOf` of the `figure`), at the
      storyboard's times, then `t.unmark("2")`;
  12. at about 11.0 s, `t.unzoom("figure")`; end at the rest point by 12.0 s.

  If the trial cannot fit 12 s at a playback rate inside 0.77 to 1.3, the typing of the name in
  step 6 is dropped first (figure-editor-Q8): Tab still goes to the empty Name field and Enter
  there applies; `EXPECTED` and `clip.md` lose the `:name:` line, Mark 1 covers two lines, and
  `verify` loses the id check.
- `verify(t)`: after `t.sleep(800)`, poll `harbour-guide.md` with `t.workspaceFile` (as the grid
  scenario does). Throw, with the file's text in the message, unless it equals `EXPECTED + "\n"`.
  Then, read from the preview frame: the `figure` has the class `align-right`, its `img` has
  `data-okf-width` `40%`, the element with id `fig-harbour-light` is that figure (or holds its
  image, as MYST-031 renders the id), the caption text is `CAPTION`, no block text box is open.
  `harbour-light.svg` on disk equals the clip's stage SVG byte for byte (`readFileSync` of both as
  buffers). A difference is a finding against the feature (recipe, section 6), reported with what
  was found, never fixed in the scenario. Return `{ text, alignBy, formAtOpen }` from the notes.

### 4. Trial take, take and render

On Windows, on this machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`):

```bash
just dev
just package                     # out/reports/package/markdown-okf-schema-studio.vsix
just clip figure-editor doctor
just clip figure-editor all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

- The trial take (recipe, section 1) proves the recipe's points, plus these: (e) the CDP pointer
  hover shows the Edit figure button and its click opens the form; (f) Ctrl/Cmd+A, typed text and
  Tab reach the form's fields in the webview; (g) a key sets Align to Right with its list closed (or
  the fallback is recorded); (h) Enter in Name applies and the text box holds the expected
  directive; (i) the save chord closes the box and the figure floats right at 40%; (j) the zoom
  rectangle holds both the directive and the rendered figure. If (e), (f), (h) or (i) fails, stop
  and report: no script that sets a field's value (other than Align's recorded fallback) or calls a
  page function stands in for the filmed action.
- The trial's pictures and measured times go into `clip.md` (Q3), then the take that ships is filmed.
  `Length` (at most 12.0 s, playback rate inside 0.77 to 1.3), the section times, the zoom hold and
  the mark times follow that take, in the same commit as the render. Over 12 s: the Name step goes
  first (Q8); if the clip is still too long, stop and report.
- Commit together (the recipe's rule): `clip.md`, `scenario.mjs`, `stage/harbour-guide.md`,
  `stage/harbour-light.svg`, `figure-editor.mp4`, `.webm`, `.gif` (Git LFS through
  `.gitattributes`), `poster.png`, `contact-sheet.png`, `first-last.png`, `frames/*.png`,
  `check.json`.

### 5. Kit tests on the shipped clip

In `docs/demo-video/clip-kit/lib/`, run by `just clip-kit-test` inside `just check` (`node:test`,
Node built-ins only). Every case reads the shipped files from the repository at the head under test
(paths from the test file's own location), never a copy.

- `storyboard.test.mjs`: a case "the shipped figure-editor clip.md reads as the clip the owner
  reviews", modelled on the slash-menu-grid case: `parseClip` of
  `../../clips/figure-editor/clip.md`; size 1280x720, 15 fps, `length` the committed value (at most
  12); two captions with the texts of section 1 (`**` stripped as that case does), end to end from 0
  to the length; badges exactly `["save"]`; zoom `figure`; marks `1` and `2` in that order, in turn,
  inside the hold; `validateStory` passes on `win32` and `darwin` with a take logging the press
  `save`, the zoom `figure` and the marks `1` and `2`; and the "Expected result" block of the file
  equals `EXPECTED` imported from the shipped `scenario.mjs`, character for character (the same
  regular expression as the grid case).
- `storyboard.test.mjs` (or the file the grid case's import sits in): the stage `harbour-guide.md`
  holds the figure part of `EXPECTED` with the caption "The harbour light." and only the `:alt:`
  option, i.e. it is the text the clip starts from (a guard that the stage and the expected result
  are the same figure); and `stage/harbour-light.svg` starts with `<svg` and declares
  `width="400" height="240"`.
- `check.test.mjs`: the test "the shipped scenarios declare their checks ..." gains
  `figure-editor`, resolving to `{ editMode: "on", paste: false }`; its title names the figure clip
  too.
- `just check` and `just format`. If a size or unused-export script fails on a new file, fix the
  file, not the script.

### 6. The docs page and its site test

- `docs/user/editing.md`: in the palette bullet, the sentence on the figure form ends with
  "Escape keeps the figure as inserted." Split the bullet there: a blank line, the clip's GIF
  indented two spaces like the paste clip's GIF of the same bullet, a blank line, then "Editing a
  table cell adds ..." continues as the bullet's next paragraph (indented two spaces):

  ```markdown
    ![In edit mode, Edit figure over a figure opens one form: the caption is retyped, Width set to 40%, Align to Right and Name to fig-harbour-light; Apply writes the new option lines under the kept alt line, and Ctrl+Enter / ⌘Enter shows the smaller figure floating right of the text](../demo-video/clips/figure-editor/figure-editor.gif)
  ```

  The site build turns it into a looping video because the WebM is beside it
  (`SwRS-MDOKFSTUDIO-CORE-095`, unchanged).
- `test/site/siteClips.test.ts`: a test "the shipped editing page plays the figure editor clip as
  video", modelled on the paste clip's test of `docs/user/editing.md`: it reads the shipped
  `docs/user/editing.md`, renders it with `renderMyst` and `clipVideos`, asserts
  `<video src="../demo-video/clips/figure-editor/figure-editor.webm"`, asserts that the paste clip's
  video is still there, and that `figure-editor.webm`, `.gif` and `poster.png` exist in the clip
  folder. Marker `// @tests_req SwRS-MDOKFSTUDIO-CORE-095` (a new test of an existing SwRS, no SwRS
  text change). Then `just requirements-update`.
- No change to `README.md`, `CHANGELOG.md`, `docs/releases-notes/` (no `feat` or `fix` commit), the
  writing skill (no rendered syntax changes), the glossary, the recipe or `AGENTS.md`.

### 7. Commits and the pull request

- Commits by area, Conventional Commits (`.agents/guidelines/git-commit-message.guidelines.md`), no
  scope on `docs` or `test`:
  1. `docs: add the figure editor feature clip` (the clip folder, `docs/user/editing.md`, the kit
     test cases of section 5);
  2. `test: play the figure editor clip on the editing page of the docs site`
     (`siteClips.test.ts` and the requirements files `just requirements-update` changes).
- A draft PR (`gh pr create --draft`) on `main`, until the owner approves the storyboard and the clip
  (Q3). The body follows `.github/PULL_REQUEST_TEMPLATE.md`, the PR guideline and the recipe's clip
  PR rule: the GIF inline as
  `![...](https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/figure-editor/figure-editor.gif)`,
  the MP4 and WebM linked in the same form at the same head. Each push of a new render moves the
  three links to the new head (`gh pr edit <n> --body-file <file>`). Check in the rendered PR page
  that the GIF plays; if not, the `-assets` fallback, said in the body.
- The body states what the clip proves: in a real VS Code window on Windows, the Edit figure button
  opens the form filled from the directive, the keyboard fills it, Apply writes the expected
  directive (kept `:alt:` line, new width, align and name lines), and the save renders the figure at
  40% floating right with its new caption and id; `harbour-guide.md` holds exactly the expected text
  (the take's checks, `verify` and the `check.json` lines). It states what the owner judges: motion,
  rhythm, the loop as watched, the texts and times. It links `clip.md`.
- The section "Deviation from the feature clip process" (see "The storyboard gate, moved after the
  take").
- "Autonomous decisions": the click then Ctrl/Cmd+A in Caption (no badge); how Align was set (and the
  fallback, if used); the key frame names; the zoom rectangle; whether the Name step was kept; the
  GIF's place and alt text in `editing.md`; the site test; the stage tests.

## Out of scope

- Any change to `src/`, to an SwRS text, to the clip kit's code or to the recipe.
- The Figure button and its Browse dialog (figure-editor-Q5), the Browse... button of the form, the
  Legend field, a `{ref}` to the named figure, an image converted to a figure.
- A macOS or Linux take; placing the clip in release notes, an announcement or the README.
- Marking the PR ready before the owner approves; a retake after the owner's review (a follow-up of
  this CR, figure-editor-Q3).
- The other clips of the round.

## CI

No CI job changes. The new kit test cases run in `just check` through `just clip-kit-test`, inside
the existing `ci-static` job (Linux and Windows, `.github/workflows/ci.yml`); the site test runs
where `test/site/` tests run today.

- Environment: a runner set up by `just dev-ci` from the lock files, Node.js 24 from `.nvmrc`
  through `fnm`. Absent there and present locally: `ffmpeg`, the kit's scratch folder, the VS Code
  download, Remotion, a display. The tests need none of them: they parse the shipped `clip.md`,
  import the shipped `scenario.mjs` (never run), read the shipped stage files and render the
  shipped `docs/user/editing.md`; the committed outputs come from Git LFS, checked out as CI does for
  the other clips' site tests.
- Before the push: `just clip-kit-test`, `just check` and `just ci-static` pass on Windows; their
  output goes in the evidence.
- Only the first CI run proves the Linux leg (the scenario imported from a repository path, the LFS
  files present for the site test).

## Host and default matrix

The clip depends on the host (the save chord and Ctrl/Cmd+A) and films Studio's defaults (no Studio
setting; the Edit figure button does not depend on the palette mode).

| Host | VS Code | Settings | Expected | Proof |
| --- | --- | --- | --- | --- |
| Windows 11, CDP pointer and keys, `Ctrl+A` and `Ctrl+Enter` | pinned `DEFAULT_CODE_VERSION` | defaults (GFM palette mode, Cream) | the form opens filled, Apply writes the expected directive, the save renders the figure right at 40% with its caption and id | the take's `run` checks and `verify`, `check.json` "scenario verify passed" |
| macOS, `⌘A` and `⌘Enter` | same | defaults | same | not proved (no macOS take) |
| Linux | same | defaults | same | not proved |

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows. The storyboard, `EXPECTED`, stage and
   `checks` tests read the shipped `clip.md`, `scenario.mjs` and stage files at the head under test;
   the site test reads the shipped `docs/user/editing.md`. No prepared text stands in for a shipped
   file.
2. The trial's points (e) to (j), with what was seen and the frame names; how Align was set.
3. `just clip figure-editor doctor` passes, then `all --vsix ...`. `check.json` shows `passed: true`;
   MP4 and WebM at 1280x720 and 15 fps, the MP4 duration equal to `Length` within one frame; a GIF
   of at most 960 px and 12 fps; a loop seam SSIM in [0.98, 1.0); "Studio in edit mode at the start"
   and no paste line; `verifyPassed: true`; a playback rate inside 0.77 to 1.3; platform `win32`,
   extension source `vsix`.
4. The agent looks at the contact sheet and every key frame and checks: `button` (the Edit figure
   button over the figure, no other tooltip), `form` (the Figure form filled from the directive,
   above the text box), `filled` (the four new values), `03-zoomed` and `04-mark-1` (the directive
   with the three new lines under `:alt:`, the outline on them), `rendered` and `05-mark-2` (the
   smaller figure floating right, the paragraph wrapping on its left, the outline on the figure and
   its caption), Text 1 in section 1 and Text 2 in section 2, the keycap `Ctrl+Enter / ⌘Enter` at the
   save; no personal name or path, no stray tooltip; the tab's dirty dot only while typing. It names
   what was not checked: motion, rhythm and the loop as watched.
5. `just requirements-update` leaves the tree clean after its commit; `just preflight` passes (on
   Windows, its static stage).
6. The draft PR plays the GIF and links the MP4 and WebM at the head sha (or the `-assets`
   fallback, said so) and says the storyboard review is the owner's, in that PR.

## Open questions

None for the owner: `02-answers.md` (figure-editor-Q1 to Q9) and the code settle every point this
specification needs.
