# Feature clip: the block editor and its GFM and MyST palette modes

Short name: `clip-modes`. No tracker issue (verbal request of the owner, relayed by the Chief of
Staff, 2026-11-25).

## Goal

A feature clip of the editor of a normal block and its palette modes, made with the merged clip kit
(`docs/demo-video/clip-kit/`) and the feature clip recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`). In edit mode, a click on a
paragraph opens its block editor: the edition palette above the text box, in GFM mode (the default),
shows the plain Markdown buttons and the GitHub group. Ctrl+Shift+M, then Down, switches the palette
to MyST: the MyST group joins the palette. A zoom then shows the palette, the GitHub alert above the
paragraph and the MyST tip below it: both render the same as before. The writer learns that the
mode is a choice of tools, not of what the page can show. Escape closes the unchanged editor so the
clip loops. One continuous shot of 12.0 s, two captions in turn, three marks in turn, two key badges,
1280x720 at 15 fps, no card, the logo top right; MP4, WebM and GIF. The pull request plays the clip
and the owner reviews the storyboard and the clip there.

The clip shows existing behaviour: the mode select and its keyboard path
(`src/page/modules/editPalette.ts`, `src/page/features/blockSourceEditor.ts`,
`SwRS-MDOKFSTUDIO-PALETTE-001`, `-002`, `-017`, `SwRS-MDOKFSTUDIO-LIFE-169`), the mode's button sets
(`src/core/palette/paletteActions.ts`: modes are additive) and a render that has no mode
(`src/session/features/viewState.ts`, `StRS-MDOKFSTUDIO-CORE-001`). No behaviour of the extension
changes and no rendered syntax changes, so the writing skill
`skills/writing-for-markdown-okf-schema-studio/` is not touched.

## Dependency and base

Built on `origin/main`, alone (block-editor-Q4): no `depends.json`, no dependency on the other clips
of this round. Fetch first: the local `main` is behind `origin/main`. `origin/main` already holds
what this clip uses: the storyboard contract and parser (`lib/storyboard.mjs`, combined badges
`<Ctrl form> / <⌘ form>`), the scenario export `checks = { editMode, paste }` (`resolveChecks`,
`takeLines` in `lib/check.mjs`), the helpers `t.press(chord, badgeId)`, `t.textEdges`, `t.rectOf`
and `t.keyFrame(name)` (`lib/take.mjs`, frames written by `keyFrameTimes` in `lib/encode.mjs`), and
the merged `slash-menu-grid` clip, the closest model (edit mode, a click at the end of a paragraph,
the palette mode read from `data-palette-mode`). This CR makes **no kit change**.

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| block-editor-Q1 | The owner's wish: a clip of the editor of a normal block with its GFM and MyST modes; one CR for this clip | whole spec |
| block-editor-Q2 | The captions, stage and timing of the Griller's storyboard draft are the clip's shape | sections 1, 2, 3 |
| block-editor-Q3 | The batch films a trial take from the draft, puts its pictures in the storyboard, renders and opens the PR with the clip watchable (GIF inline, MP4 and WebM linked at the head); the PR stays a draft until the owner approves storyboard and clip; the deviation from the recipe's order is reported here and in the PR body; a retake after the owner's review is a follow-up of this CR | "The storyboard gate, moved after the take", sections 4, 7 |
| block-editor-Q4 | Built on `origin/main`, alone, no `depends.json` | "Dependency and base" |
| block-editor-Q5 | "Mode" is the palette mode; the clip shows that it changes the buttons only, never the render: Text 2 and marks 2 and 3 on a GitHub alert and a MyST tip that stay the same | sections 2, 3 (`run` steps 4 to 6, `verify`) |
| block-editor-Q6 | GFM then MyST only; Strict and Full are not filmed | sections 2, 3, "Out of scope" |
| block-editor-Q7 | The block is a paragraph, not a list | sections 1, 3 |
| block-editor-Q8 | The switch is filmed with the keyboard: Ctrl+Shift+M then Down, both with badges; fallback: type `m` (badge `M`); filmed on Windows | sections 2, 3, 4 |
| block-editor-Q9 | Stage: a heading, a GitHub alert, one paragraph and a MyST tip | section 1 |
| block-editor-Q10 | 12.0 s, three marks, the loop closed by Escape; `setup` resets the stored mode to GFM before each take; no `depends.json` | sections 2, 3 |

## The storyboard gate, moved after the take

The recipe (a project guideline, section "The storyboard first") has the maintainer review the
storyboard draft before the take. block-editor-Q3 moves that gate after the take, into the pull
request; it does not drop it:

- the batch films a trial take from the draft, puts its pictures and measured times in the
  storyboard, moves it to `docs/demo-video/clips/block-editor-modes/clip.md` with `status: draft`,
  films the take (the trial may be the take when it is clean), renders and opens the PR;
- the PR is a draft (`gh pr create --draft`) until the owner approves the storyboard and the clip;
  the agent never marks it ready; the PR body reports the deviation (section 7);
- the recipe is not changed by this CR.

## What changes

All paths are relative to the repository root.

### 1. The stage: `docs/demo-video/clips/block-editor-modes/stage/release-plan.md`

Copied byte for byte from `work/storyboard/stage/release-plan.md` of this CR's folder (in the
planning surface,
`C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/2-backlog/P2/clip-the-block-editor-and-its-modes-gfm-/`,
or wherever the batch moved the folder), LF line endings, ending with one newline:

```markdown
# Release plan

> [!NOTE]
> Version 2.4 ships on Thursday.

The release adds offline maps and a faster search. Two people review every change.

:::{tip}
Read the upgrade guide before you install.
:::
```

The paragraph (line 6, one-based) is the block whose editor opens; the alert above it and the tip
below it are the two rendered admonitions the clip marks.

### 2. The live storyboard: `docs/demo-video/clips/block-editor-modes/clip.md`

The draft `work/storyboard/clip.md` of this CR's folder, adapted only as follows; every row marked
*(on screen)* keeps its text, and the times follow the take:

- Front matter: `title: Feature clip block-editor-modes`, `status: draft`, `date:` the day of the
  commit.
- Opening paragraph: worded as the merged `theme-switch/clip.md` ("**This is the live
  storyboard.** The clip is built from this file: edit any row marked *(on screen)*, save, and run
  `just clip block-editor-modes render`, then `check`. Rows marked *(filmed)* describe the footage
  of the take: changing them means a new take. `**bold**` in a text takes the orange accent."), then
  "The clip is one continuous shot: a click opens the block editor of a paragraph in GFM mode, one
  shortcut switches the palette to MyST, then a zoom on the palette and the page around it. It shows
  two texts in turn." Drop "draft for review", "Once approved, this file becomes ..." and "The times
  below are the Griller's proposal ...". Keep the paragraph "What "mode" means here" as drafted.
- `## Clip` table as drafted: `Length` `12.0 s` (or the take's value), `Size *(on screen)*`
  `1280x720 16:9`, `Frame rate *(on screen)*` `15 fps`, `Outputs` as drafted, `Cards` `none`,
  `Logo` `top right`, `Setting filmed` as drafted
  (`markdownOkfSchemaStudio.editing.defaultPaletteMode`: `gfm`, the default written out), `Filmed
  on` as the merged clips write it ("Windows, VS Code <version>, extension <version> VSIX built from
  the branch", the versions from `check.json`), `Stage` as drafted.
- The "Off camera (`setup`)" paragraph: kept (as `theme-switch/clip.md` keeps its own), worded as
  section 3's `setup` does it.
- `## 1. The block editor, in GFM mode`: the line "Pictures: ..." replaced by links to the key
  frames `frames/gfm.png` and `frames/mode-select.png`, each with an alt text saying what it shows;
  `Time` with the take's measured times (same shape as drafted); `Shot *(filmed)*` as drafted;
  `Text 1 *(on screen)*` = `Click a block: its editor shows the **GFM** buttons`;
  `Badge mode *(on screen)*` = `Ctrl+Shift+M / ⇧⌘M`.
- `## 2. Switch to MyST`: the line "Pictures: ..." replaced by links to `frames/myst.png`,
  `frames/03-zoomed.png`, `frames/04-mark-1.png`, `frames/05-mark-2.png` and
  `frames/06-mark-3.png`, each with an alt text; `Time` with the take's times; `Shot *(filmed)*` as
  drafted; `Badge down *(on screen)*` = `↓`; `Zoom` = `modes, hold to 10.4 s` (the take's hold);
  `Mark 1 *(on screen)*` = `The MyST buttons of the palette, 5.9 to 7.5 s`;
  `Mark 2 *(on screen)*` = `The rendered GitHub alert, 7.7 to 8.9 s`;
  `Mark 3 *(on screen)*` = `The rendered MyST tip, 9.1 to 10.3 s`;
  `Text 2 *(on screen)*` = `**MyST** adds buttons; the page renders the same`. When the trial
  takes the fallback of block-editor-Q8 (section 4), the badge row becomes `Badge m *(on screen)*` =
  `M` and the `Shot` row says "types `m`".
- "Expected result" list kept as drafted (it is a list, not a `markdown` block: the clip has no
  "Expected paste" and the parser's `expectedPaste` stays `null`), with the counts the take measured
  (section 3, `run` step 3) and the comparison the scenario made (outer HTML, or inner HTML and
  class list, `run` step 4).
- "Review notes": keep the draft's notes (the code sources of every claim, the render without mode,
  the mode effects not filmed, the keyboard switch and the macOS caveat, mark 1 over two rows, the
  pointer back to the margin, the loop and `setup`'s reset). Replace the last note by: the storyboard
  is reviewed in the pull request after the take (block-editor-Q3). Add: Ctrl+Shift+M does not open
  VS Code's Problems panel (VS Code binds it there), since the text box stops the key's propagation
  before the webview forwards it (with what the frames showed); `01-selected` and `02-pasted` are
  the kit's fixed frame names (here just before Ctrl+Shift+M and just after Down), kept and not
  linked; `⇧⌘M` is drawn as one keycap (the kit splits a `⌘` group only when it starts with `⌘`);
  the measured times of the take (as the `slash-menu-grid` "Measured by the take" note, with
  `rawFps`); the key frame list and "Not checked by the author: motion, rhythm, the loop as
  watched."

### 3. The scenario: `docs/demo-video/clips/block-editor-modes/scenario.mjs`

Modelled on `docs/demo-video/clips/slash-menu-grid/scenario.mjs` (copy its helpers `editMode`,
`waitFor`, `boxState`, `union`). No import beyond Node built-ins (none is needed); nothing runs at
import, so the kit's tests can load it. The header comment says what is filmed and that every
caption, badge and time is in `clip.md`.

- `stage = { "stage/release-plan.md": "release-plan.md" }`; `open = ["release-plan.md"]`.
- `settings = { "workbench.editorAssociations": { "release-plan.md":
  "markdown-okf-schema-studio.editor" }, "markdownOkfSchemaStudio.editing.defaultPaletteMode":
  "gfm" }`.
- `checks = { editMode: "on", paste: false }`.
- `export const STAGE`: the text of `stage/release-plan.md`, lines joined with `\n`, ending with one
  newline (as `theme-switch` exports its `STAGE`; a test compares them).
- Constants: `PARAGRAPH = "The release adds offline maps and a faster search. Two people review
  every change."`, `BOX = "[data-sphinx-preview-block-editor] textarea"`,
  `PALETTE = '[data-sphinx-edit-palette="true"]'`, `SELECT = "[data-edit-palette-mode-select]"`,
  `ADMONITIONS` = the selector of the two rendered admonitions in `#sphinx-myst-preview-content`
  (`.admonition`, as the draft names it; the trial confirms it finds exactly two, else the Driver
  uses the class the page gives them, read from `src/core/directives/admonition.ts`'s style
  selector, and says so).
- `paletteState(frame)`: from `PALETTE`, `data-palette-mode`, the select's `value`, the count of
  `button[data-edit-group="github"]`, of `[data-edit-group="myst"]` and of `[data-edit-group="full"]`,
  and whether `document.activeElement` is the select, the text box or another element.
- `setup(t)`, off camera:
  1. `await t.frameOf()`, `t.sleep(1500)`; `release-plan.md` in the workspace equals `STAGE`, else
     throw.
  2. Edit mode as `slash-menu-grid`'s `setup` (click `[data-sphinx-preview-edit-toggle]` until
     `data-sphinx-preview-edit-mode` is `"on"`); `t.record("readingMode", mode)`; throw when not
     `"on"`.
  3. Reset the stored palette mode to GFM (block-editor-Q10: the mode is kept per workspace and the
     clip ends in MyST, and a stored mode wins over `editing.defaultPaletteMode`): click at the end
     of the paragraph (`t.textEdges(frame, "change.", "change.")`, `t.click()`), wait for `BOX`; when
     `data-palette-mode` is not `gfm`, press `ControlOrMeta+Shift+M` with `t.page.keyboard.press`
     (never `t.press`: no badge off camera), type `g` (the select jumps to "GitHub (GFM)"), wait at
     most 1 s for `data-palette-mode="gfm"`; if it is not, `frame.locator(SELECT).selectOption("gfm")`
     (it fires the select's change, which stores the mode) and say so in the review notes. Then press
     Escape (with `t.page.keyboard.press`) until no `BOX` is open, at most twice; throw when the
     mode is not `gfm` at that point, when an editor stays open, or when edit mode is no longer on.
  4. `release-plan.md` on disk still equals `STAGE` (Escape cancelled an unchanged editor).
  5. Record the outer HTML of each of the two `ADMONITIONS` (`t.record("admonitionsBefore", …)`);
     throw when there are not exactly two.
  6. Park the pointer in the page's right margin as `slash-menu-grid` does (`outer.x + outer.width -
     90`, `outer.y + outer.height * 0.45`), `t.sleep(500)`.
- `run(t)`, timed with `until(seconds)` as `slash-menu-grid`, at the draft's times:
  1. at 0.2 s, `t.moveTo` (0.6 s) to the right edge of "change." (`t.textEdges(frame, "change.",
     "change.")`); at 1.0 s, `t.click()`; wait at most 3 s for `BOX`; its value equals `PARAGRAPH`,
     else throw; then `t.moveTo(home.x, home.y, 0.5)` (the palette opens under the click point: no
     tooltip), back by about 1.9 s.
  2. `paletteState`: mode `gfm`, select `gfm`, 9 `github` buttons (Alert, Checkbox, Option, HTML
     table, Collapsible, Footnote, Mermaid, Column alignment, Key), 0 `myst`, 0 `full`, else throw
     with what was found; `t.record("gfm", state)`; at 2.4 s, `t.keyFrame("gfm")`.
  3. at 3.2 s, `t.press("ControlOrMeta+Shift+M", "mode")`; wait at most 1 s until the select has
     the focus, else throw; at 3.6 s, `t.keyFrame("mode-select")`. At 4.5 s, `t.press("ArrowDown",
     "down")`; wait at most 1 s until `data-palette-mode` is `myst`. If it is not (the trial's
     point (c), section 4), the scenario is changed to the fallback of block-editor-Q8:
     `t.press("m", "m")` in place of `ArrowDown`, with the badge row of section 2. Then
     `paletteState`: mode `myst`, select `myst`, the 9 `github` buttons still there, 19 `myst`
     buttons (the 19 the draft lists, from `paletteActions.ts`), 0 `full` (Vega-Lite, Vega and
     PlantUML are Full only), the text box focused, its value still `PARAGRAPH`; else throw (a
     failure here is a finding against the feature, not a scenario fix); `t.record("myst",
     state)`; at 5.0 s, `t.keyFrame("myst")`.
  4. The outer HTML of the two `ADMONITIONS` equals `admonitionsBefore`; else, when the only
     differences are attributes Studio's edit chrome puts on the block element itself (hover or
     selection state), compare their inner HTML and class list instead, record which comparison was
     used (`t.record("renderCompare", …)`) and say it in the review notes; any other difference
     throws (the render would depend on the mode: a finding against `StRS-MDOKFSTUDIO-CORE-001`).
  5. at 5.2 s, `t.zoom("modes", rect)`: the union of the palette, the first admonition (the alert)
     and the second (the tip), padded by 24 px, at most 2x (the kit caps it).
  6. Marks, each an outline padded by 6 px as `slash-menu-grid` pads its mark:
     at 5.9 s, `t.mark("1", union of the boxes of [data-edit-group="myst"] buttons)` (it may span
     two rows: the outline covers both); at 7.5 s, `t.unmark("1")`; at 7.7 s, `t.mark("2", box of
     the alert)`; at 8.9 s, `t.unmark("2")`; at 9.1 s, `t.mark("3", box of the tip)`; at 10.3 s,
     `t.unmark("3")`.
  7. at 10.4 s, `t.unzoom("modes")`; at 11.3 s, `t.page.keyboard.press("Escape")` (no badge: it only
     returns to the start for the loop); wait at most 2 s until no `BOX` is open, else throw;
     `t.moveTo(home.x, home.y, 0.3)`; `until(12.0)`.
- `verify(t)`: no block editor open; the outer HTML (or the comparison `run` used) of the two
  admonitions equals `admonitionsBefore`; `release-plan.md` on disk (`t.workspaceFile`) equals
  `STAGE` byte for byte, read after 800 ms and polled up to 2 s more; each failure throws with what
  was found. Returns `{ gfm, myst, renderCompare }` from `t.notes`.

### 4. Trial take, take and render

On Windows, on this machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`):

```bash
just dev
just package                                   # out/reports/package/markdown-okf-schema-studio.vsix
just clip block-editor-modes doctor
just clip block-editor-modes all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

When the workspace path shown anywhere in the frames holds the user name, run with
`CLIP_SCRATCH=C:/okfclip` (PowerShell: `$env:CLIP_SCRATCH = "C:/okfclip"`) as the merged clips did.

- The trial take (recipe section 1, adapted): (a) the preview webview and the palette are in the
  frames; (b) the click at the end of the paragraph opens its editor in GFM mode (`run` step 2
  passes); (c) Ctrl+Shift+M focuses the select and Down changes it to MyST (`run` step 3 passes);
  if Down does not change the mode, the fallback of block-editor-Q8 (type `m`, badge `M`) is filmed
  and the PR says so; (d) VS Code's Problems panel does not open on Ctrl+Shift+M (the frames after
  the press); (e) the two admonitions are unchanged (`run` step 4); (f) the retimed rate is at least
  the storyboard's frame rate; (g) the loop seam SSIM in [0.98, 1.0).
  If (d) fails (the panel opens), the Driver stops and reports it, with the frames: it is a finding
  against `SwRS-MDOKFSTUDIO-PALETTE-017` in a real window, not a clip fix. The other failures follow
  the recipe.
- The trial's pictures and measured times go into `clip.md` (block-editor-Q3); `Length` and every
  time follow the take (playback rate inside 0.77 to 1.3), in the same commit as the render; the two
  captions stay end to end from 0 to `Length`, the marks inside the zoom hold.
- Commit together (recipe rule): `clip.md`, `scenario.mjs`, `stage/release-plan.md`,
  `block-editor-modes.mp4`, `.webm`, `.gif` (Git LFS through `.gitattributes`), `poster.png`,
  `contact-sheet.png`, `first-last.png`, `frames/*.png`, `check.json`. `frames/` also holds
  `01-selected.png` and `02-pasted.png`, which `keyFrameTimes` writes at the first and last press;
  they are kept as the kit writes them and not linked from `clip.md`.

### 5. Tests (no kit code change)

Each reads the shipped files from the repository, path from the test file's own location, at the
head under test, never a copy. Run by `just clip-kit-test` inside `just check`:

- `docs/demo-video/clip-kit/lib/storyboard.test.mjs` imports `{ STAGE as STAGE_MODES }` from the
  shipped `../../clips/block-editor-modes/scenario.mjs` and gains "the shipped block-editor-modes
  clip.md reads as the clip the owner reviews", modelled on the `slash-menu-grid` case: `parseClip`
  gives 1280x720, 15 fps, the committed `Length`, the two captions (`**` aside) "Click a block: its
  editor shows the GFM buttons" and "MyST adds buttons; the page renders the same", end to end from 0
  to `Length`; badges `{ mode: "Ctrl+Shift+M / ⇧⌘M", down: "↓" }` (or `m: "M"` under the fallback);
  zoom `modes` with the committed hold; marks `1`, `2`, `3` in turn, each inside the hold, with the
  committed times; `expectedPaste` is `null`; `validateStory` passes with a `take` of presses `mode`
  and `down`, zoom `modes`, marks `1`, `2`, `3`, once on `win32` and once on `darwin` (the combined
  badge, and `↓` names no modifier).
- Same file: "the stage of the block-editor-modes scenario is the shipped stage file, byte for byte"
  (as the `theme-switch` case): `STAGE_MODES` equals the shipped `stage/release-plan.md`.
- `docs/demo-video/clip-kit/lib/check.test.mjs`: the test "the shipped scenarios declare their
  checks ..." gains `block-editor-modes`: `resolveChecks` gives `{ editMode: "on", paste: false }`
  (its title names the modes clip too).
- `test/site/siteClips.test.ts`: "the shipped editing page plays the block editor modes clip as
  video", modelled on "the shipped editing page plays the list drag clip as video": reads the shipped
  `docs/user/editing.md`, renders it with `renderMyst` and `clipVideos`, asserts
  `<video src="../demo-video/clips/block-editor-modes/block-editor-modes.webm"` and that
  `block-editor-modes.webm`, `.gif` and `poster.png` exist; marker
  `// @tests_req SwRS-MDOKFSTUDIO-CORE-095` (an added test of an existing SwRS, no SwRS text
  change); then `just requirements-update`.

### 6. Docs

- `docs/user/editing.md`, in the list item on the edition palette: after the sentence that ends
  "Full mode adds, on top of MyST, the [Vega-Lite and Vega chart](charts.md) commands.", a blank
  line, the image indented as the item (two spaces, as the spreadsheet paste clip's image in the same
  page)
  `![In edit mode, a click on a paragraph opens its editor with the GFM buttons; Ctrl+Shift+M then Down switch the palette to MyST, which adds the MyST buttons, while the GitHub alert and the MyST tip around the paragraph render the same](../demo-video/clips/block-editor-modes/block-editor-modes.gif)`,
  a blank line, and the rest of that item ("In edit mode, hovering a figure shows Edit figure ...")
  as a new paragraph of the same item, indented as before (the recipe, section 4: the GIF under the
  entry of the feature).
- No change to the recipe, the glossary, the writing skill, `README.md`, `CHANGELOG.md` or
  `docs/releases-notes/` (no `feat` or `fix` commit).

### 7. Commits and the pull request

- Commits by area (Conventional Commits; no scope on `docs` or `test`):
  `docs: add the block editor modes feature clip` (clip folder, `docs/user/editing.md`),
  `test: check the block editor modes clip's storyboard, stage and docs page` (the kit test cases,
  `siteClips.test.ts`, the files `just requirements-update` changes).
- The PR is opened as a draft (`gh pr create --draft`) and stays a draft until the owner approves
  the storyboard and the clip (block-editor-Q3); the agent does not mark it ready.
- The body follows `.github/PULL_REQUEST_TEMPLATE.md`, the PR guideline and the recipe's clip PR
  rule: the GIF inline from
  `https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/block-editor-modes/block-editor-modes.gif`,
  the MP4 and WebM linked in the same form at the same head; after each push of a new render the
  links move to the new head (`gh pr edit <n> --body-file <file>`); check that the GIF plays in the
  rendered PR page, else the recipe's `-assets` fallback.
- A section "Deviation from the feature clip process": the storyboard review moved from before the
  take into this PR (block-editor-Q3); the take filmed from the Griller's draft; an *(on screen)*
  row the owner changes is a render (`just clip block-editor-modes render` then `check`), a
  *(filmed)* row a retake, a follow-up of this CR. It links `clip.md` for the review.
- What the clip proves (a real click and real keys in a real VS Code window open a paragraph's
  editor in GFM mode and switch its palette to MyST, which adds the 19 MyST buttons and keeps the
  GitHub ones, while the rendered alert and tip do not change and the file is untouched: the take's
  `run` checks and `verify`) and what the owner judges (motion, rhythm, the loop as watched, the
  texts and their accent). It says the request expected a render that changes with the mode, that
  the code has none, and that the clip films what exists (block-editor-Q5).
- "Autonomous decisions": the differences from the draft (section 2), the key frame names, the
  measured times, the admonition comparison used, the `setup` reset path used (`g` or
  `selectOption`), Down or the `m` fallback, the docs placement, `⇧⌘M` as one keycap,
  `CLIP_SCRATCH` if used, the frames `01-selected` and `02-pasted` left as the kit writes them.

## Out of scope

- Any change to `src/`, to an SwRS text, to the writing skill or to the clip kit's code (beyond
  test cases); a change of the recipe.
- A render that changes with the mode (a new feature CR, not this clip, block-editor-Q5).
- The Strict and Full modes, the `/` menu and its ranking, a table cell editor's palette, a list
  block (block-editor-Q6, Q7); a click on the select and its native option list (block-editor-Q8).
- A macOS or Linux take; placing the clip in release notes or the announcement (a release CR does
  it); a retake after the owner's review (a follow-up of this CR, block-editor-Q3); marking the PR
  ready before the owner approves.

## CI

No CI job changes. The new test cases run in `just check` through `just clip-kit-test`, inside the
existing `ci-static` job (Linux and Windows, `.github/workflows/ci.yml`); the site test runs where
`test/site/` tests run today.

- Environment: the CI machine set up by `just dev-ci` from the lock files, Node.js 24 from `.nvmrc`
  through `fnm`. Absent there and present locally: `ffmpeg`, the kit's scratch folder, the VS Code
  download, Remotion, a display. The new tests need none of them: the shipped `clip.md`,
  `scenario.mjs` (loaded, never run) and `stage/release-plan.md`, the shipped `docs/user/editing.md`
  and the clip's committed files (Git LFS checked out as CI does for the merged clips' site tests).
- Before the push: `just clip-kit-test`, `just check` and `just ci-static` on Windows.
- Only the first CI run proves the Linux leg (the dynamic `import` of the scenario from a repository
  path, the byte comparison of the stage with LF endings).

## Host and default matrix

The clip films the shipped default of `editing.defaultPaletteMode` (`gfm`, written out in the
take's settings) and a mode chosen in the page, which is stored per workspace and wins over the
setting; and a shortcut whose modifier depends on the host.

| Host | Settings and stored mode | Expected | Proof |
| --- | --- | --- | --- |
| Windows 11, CDP click and keys | `defaultPaletteMode` `gfm`, stored mode reset to `gfm` by `setup` | GFM palette on open; Ctrl+Shift+M then Down gives MyST, 19 MyST buttons added; render and file unchanged | the take's `run` checks and `verify`, `check.json` ("scenario verify passed") |
| Windows 11 | a stored mode other than `gfm` left by an earlier take | `setup` resets it before frame 0 | `setup`'s throw when the mode is not `gfm` after the reset |
| macOS | same settings | Cmd+Shift+M focuses the select; Down opens the native list instead of changing the value | not proved (no macOS take); stated in the review notes; the badge names both forms |
| Linux | same settings | as Windows | not proved |

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows; the storyboard, stage and checks tests read
   the shipped `clip.md`, `stage/release-plan.md` and `scenario.mjs` at the head under test; the site
   test reads the shipped `docs/user/editing.md`.
2. The trial's seven points (section 4), with what was seen for (a), (c) and (d) (frame names).
3. `just clip block-editor-modes all --vsix ...` passes; `check.json` shows `passed: true`, MP4 and
   WebM 1280x720 at 15 fps, MP4 duration equal to `Length` within one frame, GIF at most 960 px and
   12 fps, loop seam SSIM in [0.98, 1.0), "Studio in edit mode at the start", no paste line,
   `verifyPassed: true`, playback rate inside 0.77 to 1.3, platform `win32`, extension source
   `vsix`.
4. The take's `run` passed steps 2 to 4 (GFM: 9 `github`, 0 `myst`; MyST: 9 `github`, 19 `myst`,
   0 `full`, the text box focused and unchanged; the two admonitions unchanged) and `verify` found
   no editor open, the admonitions unchanged and `release-plan.md` equal to `STAGE`.
5. The agent looks at the contact sheet and every key frame: Studio in edit mode, the paragraph's
   editor with the palette reading "GitHub (GFM)" then "MyST", the badges `Ctrl+Shift+M / ⇧⌘M` and
   `↓` (or `M`), no Problems panel, Text 1 during the GFM beat and Text 2 during the switch and the
   zoom, mark 1 on the MyST buttons, mark 2 on the alert, mark 3 on the tip, in turn, no tooltip at
   frame 0, after the click or at the seam, no editor open at the last frame, no personal name or
   path, no dirty tab. What was not checked (motion, rhythm, the loop as watched) is said.
6. `just requirements-update` leaves the tree clean after its commit; `just preflight` passes (on
   Windows, its static stage).
7. The PR is a draft; its body plays the GIF, links the MP4 and WebM at the head sha and holds the
   "Deviation from the feature clip process" section.

## Open questions

None: `02-answers.md` (block-editor-Q1 to Q10) and the code on `origin/main` settle every point this
specification needs.
