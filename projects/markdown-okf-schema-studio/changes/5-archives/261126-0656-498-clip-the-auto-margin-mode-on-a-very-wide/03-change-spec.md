# Feature clip: a very wide table in Auto width

Short name: `auto-width`. No tracker issue (verbal request of the owner, relayed by the Chief of
Staff, 2026-11-25).

## Goal

A feature clip of the Width button's Auto mode on a very wide table, made with the merged clip kit
(`docs/demo-video/clip-kit/`) and the feature clip recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`). Studio shows a short page in
Margin, the default: the text sits in the centred column and a table of deploys per service and per
month is cut at that column, most of the year hidden behind a sideways scroll. One click on the Width
button (row 3 of the floating toolbar) sets Auto: the table breaks out of the column, centred, and
shows the twelve months and the total at once, while the heading and the paragraph stay where they
were. A light zoom then marks the broken-out table and the paragraph still in its column. The reader
keeps a comfortable line length and still sees a wide table whole.

One continuous shot of about 10.6 s (11.8 s in the fallback of the loop seam), two captions in turn,
two marks in turn, 1280x720 at 15 fps, no card, the logo top right, a loop; MP4, WebM and GIF. The
pull request plays the clip and the owner reviews the storyboard and the clip there.

The clip shows the existing feature (`src/page/modules/widthMode.ts`, the Width button of
`src/core/preview/previewToolbar.ts`, the view preference `widthMode` of
`src/core/state/previewViewPreferences.ts`, the overflow flag of `src/page/features/scrollCore.ts`;
`SwRS-MDOKFSTUDIO-LAYOUT-020` the button, `SwRS-MDOKFSTUDIO-LAYOUT-044` which tables break out); no
behaviour of the extension changes and no rendered syntax changes (the writing skill
`skills/writing-for-markdown-okf-schema-studio/` is not touched).

## Dependency and base

Built on `origin/main`, alone (auto-width-Q4): no `depends.json`, no dependency on the other clips of
this round, and none on `clip-the-advanced-renderings-tour` either: both versions stay within the
recipe's 12 s (auto-width-Q11). Fetch first: the local `main` is behind `origin/main`.
`origin/main` already holds what this clip uses: the storyboard contract and parser
(`lib/storyboard.mjs`), the scenario export `checks = { editMode, paste }` (`resolveChecks`,
`takeLines` in `lib/check.mjs`), the helper `t.keyFrame(name)` (`lib/take.mjs`, frames written by
`keyFrameTimes` in `lib/encode.mjs`), and the merged `theme-switch` clip, whose shape this clip
follows (a toolbar button clicked in Studio alone in the window, a view choice, the file never
changed). This CR makes **no kit change**.

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| auto-width-Q1 | The owner's wish: the benefit of the auto-margin mode on a very wide table, compared with the same table without the mode; one CR for this clip | whole spec |
| auto-width-Q2 | The captions, stage and timing of the Griller's storyboard draft are the clip's shape | sections 1, 2, 3 |
| auto-width-Q3 | The batch films a trial take from the draft, puts its pictures in the storyboard, renders, and opens the PR with the clip watchable (GIF inline, MP4 and WebM linked at the head); the PR stays a draft until the owner approves storyboard and clip; the deviation from the recipe's order is reported here and in the PR body; a retake after the owner's review is a follow-up of this CR | "The storyboard gate, moved after the take", sections 4, 7 |
| auto-width-Q4 | Built on `origin/main`, alone, no `depends.json` | "Dependency and base" |
| auto-width-Q5 | "Auto-margin mode" is the Width button's Auto mode (Margin, Auto, Full width), the view preference `widthMode`, not a setting; the column is `markdownOkfSchemaStudio.preview.maxContentWidth` (default 960 px); the clip compares Margin with Auto | Goal, sections 2, 3, 6 |
| auto-width-Q6 | Clip `wide-table-auto-width`, one short page `deploys.md` all in view: a heading, a two-line paragraph, a table of deploys per service and month, a closing sentence; the table reuses the style of the wide table of `clip-adapt-the-export-video-long-page-sa` plus a Total column; that CR's folder is not edited | sections 1, 2 |
| auto-width-Q7 | The table is about 950 CSS px in Auto: wider than the column (about 804 px), narrower than the room (the pane minus 32 px); the trial measures it; outside the band it drops the Total column or shortens the table, never a setting | sections 1, 3 (`setup`), 4 |
| auto-width-Q8 | One click, Margin to Auto, no sideways scroll filmed; the same frame before and after | sections 2, 3 |
| auto-width-Q9 | A light zoom close to 1x with two marks in turn: the broken-out table, then the paragraph still in the column | sections 2, 3 |
| auto-width-Q10 | The one-click version (10.6 s, ends in Auto) when `check` passes its seam line; else two more clicks after the zoom, Full width then Margin (11.8 s), so the clip ends where it starts | section 3 ("The seam"), section 4 |
| auto-width-Q11 | Within 12 s in both versions, so no `depends.json` on `clip-the-advanced-renderings-tour` | "Dependency and base" |
| auto-width-Q12 | Every setting at its default; `setup` expands the toolbar, keeps reading mode, Cream and the closed TOC, and clicks the Width button until it reads "Width: Margin"; `checks = { editMode: "off", paste: false }` | section 3 |

## The storyboard gate, moved after the take

The recipe (a project guideline, section "The storyboard first") has the maintainer review the
storyboard draft before the take. auto-width-Q3 moves that gate after the take, into the pull
request; it does not drop it:

- the batch films a trial take from the draft, puts its pictures and measured times in the
  storyboard, moves it to `docs/demo-video/clips/wide-table-auto-width/clip.md` with
  `status: draft`, films the take (the trial may be the take when it is clean), renders and opens
  the PR;
- the PR is a draft (`gh pr create --draft`) until the owner approves the storyboard and the clip;
  the agent never marks it ready; the PR body reports the deviation (section 7);
- the recipe is not changed by this CR.

## What changes

All paths are relative to the repository root. The CR's folder is
`C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/2-backlog/P2/clip-the-auto-margin-mode-on-a-very-wide/`,
or wherever the batch moved it.

### 1. The stage: `docs/demo-video/clips/wide-table-auto-width/stage/deploys.md`

Copied byte for byte from `work/storyboard/stage/deploys.md` of the CR's folder, LF line endings,
ending with one newline: the heading "Deploys by service", the paragraph "Each service ships on its
own train. ... It is wide: one column per month." (one source line, two lines on screen), the
17-column table (Service, Team, Region, Tier, Jan to Dec right-aligned, Total right-aligned) of five
rows (checkout-api, search-index, notifications, media-store, auth-gateway), and the closing sentence
"The totals follow the release calendar of the platform team."

**A stage one can reuse** (the brief: the table style is shared with
`clip-adapt-the-export-video-long-page-sa`, not specified yet). The stage stays plain GFM with no
Studio-only syntax and no reference to the clip, and its table is the shared table: its first 16
columns are, row for row and cell for cell, the 16-column table of that CR's draft stage
`work/storyboard/stage/platform-report.md` (same header, same alignment row, same five rows, same
numbers; checked when this spec was written), and the Total column is the only addition, last.
So the other clip can take this table by dropping its last column, or this one can be rebuilt from
that one by adding it. When the trial must narrow the table (auto-width-Q7), it changes it in this
order, each time measuring again: (1) drop the Total column (the table is then exactly the shared
one); (2) only if still too wide, drop month columns from the end (Dec first). A too narrow table
(no breakout) is not expected (estimate: about 950 px against 804 px). Any change to the table is
written in the storyboard's review notes and in the PR's "Autonomous decisions", naming the change,
so the CR `clip-adapt-the-export-video-long-page-sa` can align its table; that CR's folder is not
edited (auto-width-Q6).

### 2. The live storyboard: `docs/demo-video/clips/wide-table-auto-width/clip.md`

The draft `work/storyboard/clip.md` of the CR's folder, adapted only as follows; every row marked
*(on screen)* keeps its text, and the times follow the take:

- Front matter: `title: Feature clip wide-table-auto-width`, `status: draft`, `date:` the day of the
  commit.
- Opening paragraph: worded as the merged `theme-switch/clip.md` ("**This is the live
  storyboard.** The clip is built from this file: edit any row marked *(on screen)*, save, and run
  `just clip wide-table-auto-width render`, then `check`. Rows marked *(filmed)* describe the footage
  of the take: changing them means a new take. `**bold**` in a text takes the orange accent."), then
  "The clip is one continuous shot: the page in Margin with a very wide table cut at the column, one
  click on the Width button, the same page in Auto with the table broken out of the column, then a
  light zoom and two marks. It shows two texts in turn." Drop "draft for review", "Once approved,
  this file becomes ..." and "The times below are the Griller's proposal ...".
- `## Clip` table as drafted: `Length` `10.6 s` (or the take's value; `11.8 s` or the take's value in
  the fallback), `Size *(on screen)*` `1280x720 16:9`, `Frame rate *(on screen)*` `15 fps`, `Outputs`
  as drafted, `Cards` `none`, `Logo` `top right`, `Setting filmed` as drafted, `Filmed on` written as
  the theme clip does ("Windows, VS Code <version>, extension <version> VSIX built from the branch",
  the versions from `check.json`), `Stage` as drafted (17 columns, or the measured table of
  section 1).
- The "Off camera (`setup`)" paragraph: kept, as the theme clip keeps its own, worded for this clip:
  "the toolbar expanded (a new workspace starts collapsed), reading mode, the Cream theme and the
  closed TOC (the defaults); the Width button clicked until it reads "Width: Margin", so frame 0 is
  Margin whatever the workspace stored. The button cycles Margin, Auto, Full width."
- `## 1. Margin: the table is cut at the column`: the line "Pictures: ..." replaced by the image
  `frames/margin.png` with an alt text saying what it shows; `Time` with the take's times;
  `Shot *(filmed)*` as drafted; `Text 1 *(on screen)*` = `In **Margin**, a wide table is cut at the
  column`.
- `## 2. Auto: the table takes the width it needs`: the line "Pictures: ..." replaced by the images
  `frames/auto.png`, `frames/04-mark-1.png` and `frames/05-mark-2.png`, each with an alt text;
  `Time` and `Shot *(filmed)*` as drafted, with the take's times; `Zoom` = `page, hold to 9.6 s` (the
  take's hold); `Mark 1 *(on screen)*` = `Orange outline around the table, broken out of the column,
  4.4 to 6.6 s`; `Mark 2 *(on screen)*` = `Orange outline around the paragraph, still in the narrow
  column, 6.8 to 9.0 s`; `Text 2 *(on screen)*` = `In **Auto**, the table breaks out; the text keeps
  its column`. In the fallback version (section 3, "The seam"), the `Time` and `Shot` rows add the two
  clicks after the zoom (Full width, then Margin) and Text 2 runs to the end.
- "Expected result" list kept as drafted (it is what `run` and `verify` check, section 3), with "its
  centre is within 2 px of the pane's centre" read as the centre of the page's client width
  (`document.documentElement.clientWidth / 2`); in the fallback, one more line: after the last click
  the mode is Margin again, the table overflows again, and the paragraph's box is the one of frame 0.
- "Review notes": keep the draft's notes (which tables break out, the sizes, a table wider than the
  room, the toolbar over the table's right end, no animation, the light zoom, the pointer leaving the
  button, the loop seam, the shared table style), each brought up to date with what the trial
  measured: the table's width in Margin (its `clientWidth` and `scrollWidth`) and in Auto, the
  column's and the room's widths, which version was rendered and its seam SSIM, whether the toolbar
  covered the table, how the jump at the click read; any change to the table (section 1); and the
  key frame list with "Not checked by the author: motion, rhythm, the loop as watched."

### 3. The scenario: `docs/demo-video/clips/wide-table-auto-width/scenario.mjs`

Modelled on `docs/demo-video/clips/theme-switch/scenario.mjs` (copy its `pageState` pattern, which
re-reads the preview frame because the webview may reload, its toolbar expansion, its reading mode
and its pointer parking). No import beyond Node built-ins; nothing runs at import, so the kit's
tests can load it. The header comment says what is filmed and that every caption and time is in
`clip.md`.

- `stage = { "stage/deploys.md": "deploys.md" }`; `open = ["deploys.md"]`; `settings = {
  "workbench.editorAssociations": { "deploys.md": "markdown-okf-schema-studio.editor" } }` (no Studio
  setting: `preview.maxContentWidth` stays at 960).
- `checks = { editMode: "off", paste: false }` (auto-width-Q12).
- `export const STAGE`: the text of `stage/deploys.md`, character for character (a test compares
  them, section 5).
- Constants: `WIDTH_BUTTON = "[data-sphinx-preview-width-toggle]"`, `NEXT = { margin: "auto", auto:
  "full", full: "margin" }`, `TITLES = { margin: "Width: Margin", auto: "Width: Auto", full: "Width:
  Full width" }`.
- `layout(t)`: from a fresh frame (retried as `pageState`), returns the page's
  `data-sphinx-preview-width` (on `document.documentElement`), the button's `title`, the toolbar
  state, the edit mode, the page's client width, and for the table and the paragraph: the box of the
  paragraph (`#sphinx-myst-preview-content > p`, the first one), the box of the table's top-level
  block (the child of `#sphinx-myst-preview-content` that holds the `table`), whether that block
  carries `data-sphinx-preview-wide`, and the `table`'s `scrollWidth`, `clientWidth` and
  `data-sphinx-table-overflow`.
- `setup(t)`, off camera: as theme-switch's `setup` for the toolbar (expanded) and reading mode
  (`t.record("readingMode", mode)`; throw when not `"off"`); the TOC is left closed (the default;
  no TOC click; the frames show it closed, section 4); no Theme click (Cream is the default; throw with what is found if the
  theme mode is not `cream`); then click the Width button until `layout` reads `margin` and the title
  "Width: Margin" (at most three clicks, re-reading the frame between clicks); throw otherwise. Then
  check the Margin state of the "Expected result": the table block has no `data-sphinx-preview-wide`,
  its `scrollWidth` exceeds its `clientWidth` by more than 1 and the table carries
  `data-sphinx-table-overflow="true"`; else throw. Then **measure Auto off camera** (auto-width-Q7):
  click once to Auto, wait for the breakout, `t.record("autoWidth", …)` with the table block's width,
  the paragraph's width (the column) and the page's client width minus 32 (the room); throw when the
  block is not wider than the paragraph or still overflows (the table must be narrowed, section 1);
  then click twice more (Full width, Margin) back to Margin and check Margin again. Last, park the
  pointer in the blank area right of the heading, off the toolbar and off every block, as theme-switch
  does, `t.sleep(800)`.
- `run(t)`, timed with `until(seconds)` as theme-switch, `home = { ...t.pointer }`:
  1. read `layout` (`before`); at 0.3 s, `t.moveTo` (0.6 s or as the take needs to arrive near 2.2 s)
     to the centre of the Width button (its `boundingBox()` in the frame, page coordinates);
     `t.keyFrame("margin")` before the click (the pointer near the button, Text 1 on screen);
  2. at 2.5 s, `t.click()` (a real CDP click: the kit draws the ripple);
  3. poll, at most 1.5 s, re-reading the frame, until `layout` reads `auto`, title "Width: Auto",
     the table block carries `data-sphinx-preview-wide`, the block's left edge is left of the
     paragraph's and its right edge right of the paragraph's, its centre is within 2 px of half the
     page's client width, and the table no longer overflows (`scrollWidth <= clientWidth + 1`); and the
     paragraph's left edge and width equal `before`'s within 1 px; `t.record("auto", …)`; else throw
     with what the page shows (a finding against the feature, not a scenario fix);
  4. `t.moveTo(home.x, home.y, 0.5)` so the pointer leaves the toolbar by 3.4 s (no "Width: Auto"
     tooltip in the zoom); at 3.6 s, `t.keyFrame("auto")`;
  5. at 3.8 s, `t.zoom("page", rect)`: the union of the paragraph's box and the table block's box,
     padded by 24 px (the kit caps the zoom at 2x; the result is close to 1x);
  6. at 4.4 s, `t.mark("1", air(table block))`; at 6.6 s, `t.unmark("1")`; at 6.8 s,
     `t.mark("2", air(paragraph))`; at 9.0 s, `t.unmark("2")`; `air` pads by 8 px as theme-switch;
  7. at 9.6 s, `t.unzoom("page")`; `until(10.6)` in the one-click version.

  **The seam** (auto-width-Q10). The trial take films the one-click version. When its `check` passes
  every line, it is the clip. When only the line "loop seam SSIM at least 0.98 and below 1.0" fails,
  the scenario takes the **fallback**, selected by one constant at the top of the file
  (`const BACK_TO_MARGIN = true`), and the batch films it again: after step 7, `t.moveTo` to the
  Width button; at 10.2 s, `t.click()` and poll for `full` (title "Width: Full width"); at 10.8 s,
  `t.click()` and poll for `margin` with the Margin checks of `setup` and the paragraph's box equal to
  `before`'s; `t.moveTo(home.x, home.y, 0.4)`; `until(11.8)`. Text 2 runs to the end; the storyboard
  rows follow (section 2). When both versions fail the seam line, the work stops and reports with
  both measured SSIM values (no third version is invented).

  `t.record("widthModes", …)` holds the modes seen in order.
- `verify(t)`: `deploys.md` on disk (`t.workspaceFile("deploys.md")`) equals `STAGE` byte for byte;
  else throw with the text on disk. Returns `{ modes, auto, unchanged: true }`.

### 4. Trial take, take and render

On Windows, on this machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`):

```bash
just dev
just package                                   # out/reports/package/markdown-okf-schema-studio.vsix
just clip wide-table-auto-width doctor
just clip wide-table-auto-width all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

When the workspace path shown anywhere in the frames holds the user name, run with
`CLIP_SCRATCH=C:/okfclip` (PowerShell: `$env:CLIP_SCRATCH = "C:/okfclip"`) as the export clip did.

- The trial take (recipe section 1, adapted): (a) the preview webview is in the frames, Studio alone
  in the window; (b) the Auto measure of `setup` puts the table inside the band of auto-width-Q7
  (wider than the column, no sideways scroll in Auto); if not, the table is narrowed as section 1
  says and the trial is run again; (c) in Margin the table is cut after a few months with the shaded
  edge, and in Auto all months and the total show, read on `frames/margin.png` and
  `frames/auto.png`; (d) the expanded toolbar's three rows cover neither the table's right end nor
  the Width button's neighbours in the zoom; if they cover the table, say so in the review notes and
  the PR (no setting changes, no kit change); (e) the retimed rate is at least the storyboard's
  frame rate; (f) the loop seam (section 3, "The seam").
- The trial's pictures and measured times go into `clip.md` (auto-width-Q3); `Length` and every time
  follow the take (playback rate inside 0.77 to 1.3), in the same commit as the render; the two
  captions stay end to end from 0 to `Length`, the marks inside the zoom hold.
- Commit together (recipe rule): `clip.md`, `scenario.mjs`, `stage/deploys.md`,
  `wide-table-auto-width.mp4`, `.webm`, `.gif` (Git LFS through `.gitattributes`), `poster.png`,
  `contact-sheet.png`, `first-last.png`, `frames/*.png`, `check.json`.

### 5. Tests (no kit code change)

Each reads the shipped files from the repository, path from the test file's own location, at the
head under test, never a copy. Run by `just clip-kit-test` inside `just check`:

- `docs/demo-video/clip-kit/lib/storyboard.test.mjs` gains "the shipped wide-table-auto-width clip.md
  reads as the clip the owner reviews", modelled on the theme-switch case: `parseClip` gives
  1280x720, 15 fps, the two captions (`**` aside) "In Margin, a wide table is cut at the column" and
  "In Auto, the table breaks out; the text keeps its column", end to end from 0 to `Length`; no badge;
  zoom `page` with the committed hold; marks `1` and `2` in turn inside the hold with the committed
  times; no "Expected paste" block; `validateStory` passes with a `take` of no press, zoom `page`,
  marks `1` and `2`, on `win32`.
- Same file: "the stage of the wide-table-auto-width scenario is the shipped stage file, byte for
  byte", modelled on the theme-switch case: the shipped `stage/deploys.md` equals the scenario's
  `STAGE`.
- `docs/demo-video/clip-kit/lib/check.test.mjs`: the test "the shipped scenarios declare their
  checks ..." gains `wide-table-auto-width`: `resolveChecks` gives `{ editMode: "off", paste: false }`
  (its title names the wide table clip too).
- `test/site/siteClips.test.ts`: "the shipped wide tables page plays the wide table clip as video",
  modelled on "the shipped themes page plays the theme switch clip as video": reads the shipped
  `docs/user/wide-tables.md`, renders it with `renderMyst` and `clipVideos`, asserts
  `<video src="../demo-video/clips/wide-table-auto-width/wide-table-auto-width.webm"` and that
  `wide-table-auto-width.webm`, `.gif` and `poster.png` exist; marker
  `// @tests_req SwRS-MDOKFSTUDIO-CORE-095` (an added test of an existing SwRS, no SwRS text change);
  then `just requirements-update`.

### 6. Docs

- `docs/user/wide-tables.md`: after the existing capture (the linked image
  `margin-break-cream.png`, which the paragraph's last sentence "The capture uses the cream theme."
  introduces), the image
  `![A page in Margin width shows a twelve-month table cut at the text column; one click on the Width button sets Auto and the table breaks out of the column, centred, with every month and the total, while the paragraph keeps its narrow column](../demo-video/clips/wide-table-auto-width/wide-table-auto-width.gif)`
  (the recipe, section 4: the GIF under the entry of the feature).
- No change to the recipe, the glossary, the writing skill, `README.md`, `CHANGELOG.md` or
  `docs/releases-notes/` (no `feat` or `fix` commit).

### 7. Commits and the pull request

- Commits by area (Conventional Commits; no scope on `docs` or `test`):
  `docs: add the wide table Auto width feature clip` (clip folder, `docs/user/wide-tables.md`),
  `test: check the wide table clip's storyboard, stage and docs page` (the kit test cases,
  `siteClips.test.ts`, the files `just requirements-update` changes).
- The PR is opened as a draft (`gh pr create --draft`) and stays a draft until the owner approves
  the storyboard and the clip (auto-width-Q3); the agent does not mark it ready.
- The body follows `.github/PULL_REQUEST_TEMPLATE.md`, the PR guideline and the recipe's clip PR
  rule: the GIF inline from
  `https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/wide-table-auto-width/wide-table-auto-width.gif`,
  the MP4 and WebM linked in the same form at the same head; after each push of a new render the
  links move to the new head (`gh pr edit <n> --body-file <file>`); check that the GIF plays in the
  rendered PR page, else the recipe's `-assets` fallback.
- A section "Deviation from the feature clip process": the storyboard review moved from before the
  take into this PR (auto-width-Q3); the take filmed from the Griller's draft; an *(on screen)* row
  the owner changes is a render (`just clip wide-table-auto-width render` then `check`), a *(filmed)*
  row a retake, a follow-up of this CR. It links `clip.md` for the review.
- What the clip proves (a real click on the Width button in a real VS Code window switches Margin to
  Auto; the very wide table breaks out of the column, centred, and no longer scrolls, while the
  paragraph keeps its column; the file is unchanged: the take's `run` checks and `verify`) and what
  the owner judges (motion, rhythm, the jump at the click, the loop as watched, the texts and their
  accent).
- "Autonomous decisions": the differences from the draft (section 2), the version rendered (one
  click or the fallback) with its seam SSIM, the measured widths, any change to the table (section 1,
  for the CR `clip-adapt-the-export-video-long-page-sa`), the toolbar over the table as seen, the key
  frame names, the docs placement, `CLIP_SCRATCH` if used.

## Out of scope

- Any change to `src/`, to an SwRS text, to the writing skill or to the clip kit's code (beyond test
  cases); a change of the recipe.
- A setting changed for the clip, `preview.maxContentWidth` included (auto-width-Q5, Q7, Q12); Full
  width shown for its own sake (it appears only as a step of the seam fallback); a sideways scroll
  filmed (auto-width-Q8); figures, images or code blocks breaking out; edit mode; the TOC open.
- Editing the CR `clip-adapt-the-export-video-long-page-sa` or its stage (auto-width-Q6).
- A macOS or Linux take; placing the clip in release notes or the announcement (a release CR does
  it); a retake after the owner's review (a follow-up of this CR, auto-width-Q3); marking the PR
  ready before the owner approves.

## CI

No CI job changes. The new test cases run in `just check` through `just clip-kit-test`, inside the
existing `ci-static` job (Linux and Windows, `.github/workflows/ci.yml`); the site test runs where
`test/site/` tests run today.

- Environment: the CI machine set up by `just dev-ci` from the lock files, Node.js 24 from `.nvmrc`
  through `fnm`. Absent there and present locally: `ffmpeg`, the kit's scratch folder, the VS Code
  download, Remotion, a display. The new tests need none of them: the shipped `clip.md`,
  `scenario.mjs` (loaded, never run) and `stage/deploys.md`, the shipped `docs/user/wide-tables.md`
  and the clip's committed files (Git LFS checked out as CI does for the merged clips' site tests).
- Before the push: `just clip-kit-test`, `just check` and `just ci-static` on Windows.
- Only the first CI run proves the Linux leg (the dynamic `import` of the scenario from a repository
  path, the byte comparison of the stage with LF endings).

## Host and default matrix

What the clip shows depends on a shipped default: the column is `preview.maxContentWidth` at its
default 960 px, and the width mode starts at its default, Margin. The clip films the defaults only.

| Host | VS Code | Settings and view | Expected | Proof |
| --- | --- | --- | --- | --- |
| Windows 11, CDP click | pinned `DEFAULT_CODE_VERSION` | `maxContentWidth` 960 (default), width mode Margin then Auto | Margin: the table overflows the column; Auto: it breaks out, centred, no overflow, the paragraph unmoved | the take's `run` checks and `verify`, `check.json` ("scenario verify passed") |
| macOS | same | same | same | not proved (no macOS take) |
| Linux | same | same | same | not proved |
| any | same | `maxContentWidth` other than 960 | the band of auto-width-Q7 moves; the table may stay in the column or still scroll | not filmed (out of scope) |

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows; the storyboard, stage and checks tests read
   the shipped `clip.md`, `stage/deploys.md` and `scenario.mjs` at the head under test; the site test
   reads the shipped `docs/user/wide-tables.md`.
2. The trial's six points (section 4), with the measured widths for (b) and what was seen for (c) and
   (d) (frame names).
3. `just clip wide-table-auto-width all --vsix ...` passes; `check.json` shows `passed: true`, MP4 and
   WebM 1280x720 at 15 fps, MP4 duration equal to `Length` within one frame and within 5 to 12 s, GIF
   at most 960 px and 12 fps, loop seam SSIM in [0.98, 1.0), "Studio in reading mode at the start",
   no paste line, `verifyPassed: true`, playback rate inside 0.77 to 1.3, platform `win32`, extension
   source `vsix`.
4. The take's `run` passed step 3 (Auto, breakout, centred, no overflow, paragraph unmoved within
   1.5 s) and, in the fallback, the return to Margin; `verify` found `deploys.md` equal to `STAGE`.
5. The agent looks at the contact sheet and every key frame: Studio in reading mode in Cream with the
   expanded toolbar and the TOC closed; at frame 0 the table cut at the column after a few months with
   the shaded edge; after the click every month and the total, the table wider than the paragraph on
   both sides, the heading and the paragraph in the same place; Text 1 during beat 1 and Text 2 during
   beat 2; mark 1 on the table and mark 2 on the paragraph in turn; no tooltip at frame 0, in the zoom
   or at the seam; no personal name or path; no dirty tab. What was not checked (motion, rhythm, the
   loop as watched) is said.
6. `just requirements-update` leaves the tree clean after its commit; `just preflight` passes (on
   Windows, its static stage).
7. The PR is a draft; its body plays the GIF, links the MP4 and WebM at the head sha and holds the
   "Deviation from the feature clip process" section.

## Open questions

None: `02-answers.md` (auto-width-Q1 to Q12) and the code on `origin/main` settle every point this
specification needs.
