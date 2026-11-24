# Feature clip: insert a card grid from the slash menu

Short name: `clip-slash-grid`. No tracker issue (verbal request of the owner, 2026-11-25).

## Goal

The next feature clip of Studio shows how fast rich MyST structure is written in the page. In edit
mode the writer clicks at the end of a paragraph, makes an empty line and types `/grid`. The slash
menu opens at the caret with Grid highlighted. Enter opens the small "Insert grid" form, and a second
Enter accepts its defaults. The save chord closes the box and the page shows a grid of two cards. A
card grid is a layout plain Markdown lacks, and agents otherwise write it as HTML. That is the selling point.

It is made with the clip kit (`docs/demo-video/clip-kit/`) and the feature clip recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`) as the CR
`short-demo-video-of-the-smart-raw-markdo` (short name `raw-copy-demo`, CR-484 in batch-09) leaves
them: a live Markdown storyboard `clip.md` (`## Clip` table, one `## <n>. <beat>` section per beat,
`Text <n>` captions in turn, `Size` and `Frame rate` fields, `Zoom`, several `Mark <id>` rows,
combined badges `Ctrl+… / ⌘…`), 1280x720 at 15 fps, no card, the logo top right, a loop, and the PR
rule that plays the clip in the PR. That CR's spec is `03-change-spec.md` in its folder
(`changes/4-batch/2-actives/484-short-demo-video-of-the-smart-raw-markdo/` of the planning surface,
or wherever the batch moved it). Where the kit or the recipe as merged differ from that spec, the
merged files win.

This clip is filmed in **edit mode** and **pastes nothing**. The kit as `raw-copy-demo` leaves it
refuses such a take in `check`: "Studio in reading mode at the start" and "no paste-options widget
after the paste" are always required. CR-485 (`clip-drag-list-item`, batch-09) owns the generic kit
change that lifts this: the scenario export `checks = { editMode, paste }`, and the helper
`t.keyFrame(name)` for scenario key frames. This clip uses both and adds no kit change of its own
(see "Dependency and base").

The clip shows existing behaviour: the slash menu (`src/page/modules/slashMenu.ts`), the Grid form
(`src/page/features/editorChrome.ts`, `src/page/modules/cardGridDirectives.ts`,
`SwRS-MDOKFSTUDIO-PALETTE-271`) and the MyST grid rendering. No behaviour of the extension changes.

## Dependency and base

- This CR runs after `raw-copy-demo` (CR-484, `depends.json`) **and after CR-485**
  (`clip-drag-list-item`), whose kit section 5 (scenario `checks`, `t.keyFrame`,
  `resolveChecks`, `takeLines`, `keyFrameTimes`) this clip needs. `depends.json` names only
  CR-484 today, so CR-485 must be added (see the reply to the Chief of Staff).
- Base: CR-485's branch while the batch stacks them (CR-485 sits on CR-484), per
  `.agents/guidelines/stacked-prs.guidelines.md`. Once both are merged, the base is `origin/main`
  (fetch first: the local `main` is behind).
- Where CR-484 or CR-485 lands differently from its spec (a field name, a frame name, the name of
  the `checks` export, a test file name), this CR follows what was merged and says so in the PR's
  "Autonomous decisions".
- If the kit, with those two CRs, still cannot film or render this clip, stop and report the gap.
  This CR does not change the kit.

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| clip-slash-grid-Q1 | Filed from the owner's request: one CR per clip, this clip among seven | Goal |
| clip-slash-grid-Q2 | The captions, stage and timing are the Griller's proposal, the storyboard draft `work/storyboard/clip.md` with its stage `work/storyboard/stage/onboarding.md`; the owner reviews them at the recipe's storyboard gate | sections 1 to 3, "Where this spec differs from the draft" |
| clip-slash-grid-Q3 | The batch does not wait for the storyboard approval before the take. It films a trial take from the draft, puts its pictures in the storyboard, renders the clip and opens the PR with the clip watchable. The owner reviews the storyboard and the clip on that PR, which stays a draft until the owner approves. The recipe's gate is moved after the take, not dropped. The deviation from the recipe's order is reported in this spec and in the PR body. A retake after the review is a follow-up of this CR | "The storyboard gate, moved after the take", section 6, "Out of scope" |

## The storyboard gate, moved after the take

The recipe, as `raw-copy-demo` leaves it ("The storyboard first"), has the maintainer review and
edit the storyboard draft, with a picture per key moment from a trial take, before the take.
clip-slash-grid-Q3 moves that gate after the take, into the pull request. This was decided by the
Chief of Staff under the owner's overnight autonomy. It deviates from a project guideline and is
reported as such:

- the batch films a trial take from the draft. It puts the trial's pictures and measured times in
  the storyboard and moves the storyboard to `docs/demo-video/clips/slash-menu-grid/clip.md` with
  `status: draft`. Then it films the take, renders and opens the PR;
- the PR is a draft (`gh pr create --draft`) until the owner approves the storyboard and the clip
  in it. The agent never marks it ready;
- the PR body has a section "Deviation from the feature clip process". It says that the storyboard
  was reviewed after the take (clip-slash-grid-Q3), and how a review lands: a change to an
  *(on screen)* row is a render (`just clip slash-menu-grid render`, then `check`), and a change to a
  *(filmed)* row is the follow-up retake;
- the recipe itself is not changed by this CR.

## What the code settles

Facts read on `origin/main`, to name the real controls. No choice is made here.

- **Edit mode** is `<html data-sphinx-preview-edit-mode="on">`, toggled by the button
  `[data-sphinx-preview-edit-toggle]` (`src/page/features/editMode.ts`). In edit mode a click on a
  paragraph opens its text box `[data-sphinx-preview-block-editor] textarea`, with the edition
  palette `[data-sphinx-edit-palette="true"]` above it.
- **The palette mode** shows on the palette as `data-palette-mode`
  (`src/page/modules/editPalette.ts`). A new panel starts in the mode stored for the workspace when
  there is one, else the setting `markdownOkfSchemaStudio.editing.defaultPaletteMode` (default `gfm`)
  (`initialPaletteModeOf`, `src/core/configuration/editingConfiguration.ts`). Grid exists in the
  `myst` mode only (`grid` in `src/core/palette/paletteActions.ts`, `modes: ["myst"]`).
- **Enter in a paragraph's text box** is a newline (`continueOnEnter` continues lists only;
  `src/page/features/blockSourceEditor.ts`). Ctrl+Enter (⌘Enter on macOS) saves and closes the box.
- **The slash menu** opens on `/` at a line start, at the caret (`[data-slash-menu]`, options
  `[data-slash-id]`, the highlighted option `[data-active="true"]`). `/grid` matches Grid by its
  label (an exact prefix, label bonus +10) and Table by its alias `grid` (no label bonus). In MyST
  mode the `myst` group also wins a near tie. So Grid is first and Table second: the draft's first
  review note is settled. Choosing removes the `/grid` query.
- **The Grid form** is `[data-sphinx-directive-panel="grid"]`, titled "Insert grid", with the fields
  `[data-directive-field]` Columns `2`, Gutter `2`, Cards `2`, and empty Headers, Footers and Links
  (`DEFAULT_GRID`). The first field takes the focus. Enter in a field submits valid values
  (`src/page/modules/directivePanel.ts`). Submitting puts the focus back in the text box.
- **The inserted text** (`gridText` and `insertBlockAt`, `src/page/modules/cardGridDirectives.ts`,
  `src/page/modules/editActionHelpers.ts`) goes after the caret. When the text before the caret ends
  with a blank line (the two Enter), no newline is added before it; when nothing follows, none is
  added after it. The caret selects "Card 1". The text box therefore holds the paragraph, one blank
  line, and the grid exactly as the draft's expected result shows. The draft's second review note
  (a stray blank line) is settled by the code; the take still checks it.
- **The rendered cards** are `.myst-grid-card` elements with their titles in `.myst-grid-card-title`
  (`src/core/preview/styles/contentBlockStyles.ts`).
- **The file on disk** is written by the kit profile's `files.autoSave: afterDelay` (200 ms)
  (`docs/demo-video/clip-kit/lib/profile.mjs`). The stage file ends with one newline, which stays
  after the block.

## Where this spec differs from the draft

| Draft | This spec | Why |
| --- | --- | --- |
| `Format` row (size, rate, outputs in one cell) | `Size *(on screen)*` = `1280x720 16:9`, `Frame rate *(on screen)*` = `15 fps`, `Outputs` = the rest | the kit, as `raw-copy-demo` leaves it, reads `Size` and `Frame rate` as their own fields |
| The zoom described in the `Time` and `Shot` rows only | a row `Zoom` = `grid, hold to 10.5 s` (or the take's hold) in section 2 | the kit reads the zoom from a `Zoom` row |
| "Pictures: from the batch's trial take" | section 1: `frames/slash-menu.png` and `frames/grid-form.png` (scenario key frames, CR-485's `t.keyFrame`), `frames/01-selected.png` (just before the save chord: the `{grid}` text in the box, "Card 1" selected) and `frames/02-pasted.png` (just after it). Section 2: `frames/03-zoomed.png`, `frames/04-mark-1.png` | one picture per key moment (raw-copy-demo Q40). `01-selected` and `02-pasted` are the kit's fixed names for the first and last logged press, here both the save chord; this is said in the review notes |
| The two Enter, the typed `/grid` and the form's Enter, shown as key actions | typed with `t.page.keyboard` (not logged as presses), so no keycap badge; only the save chord is a logged `t.press` with its `Badge save` row | the kit parser refuses a logged press without a `Badge` row, and the draft has only `Badge save`. The typed text shows in the box itself |
| Status "draft for the owner's review", the opening paragraph of a review draft | `status: draft`, the opening paragraph of a live storyboard | the file becomes the live storyboard in the clip folder (the recipe), and the owner reviews it in the PR (Q3) |
| `Filmed on`: "to be filmed by the batch" | Windows, the VS Code version of `check.json`, the extension version, "VSIX built from the branch" | the batch's take |
| `Setting filmed`: `defaultPaletteMode` `myst` | unchanged, plus a check in the take that the palette shows `data-palette-mode="myst"` | a mode stored for the workspace would win over the setting |
| Review notes 1 and 2 (Grid first? a stray blank line?) | replaced by the facts above: Grid ranks first, and the insertion leaves exactly one blank line; the take checks both | settled by the code |
| Times 11.5 s, 6.2 s, mark 7.0 to 8.8 s, hold to 10.5 s | the take's own times, same beats and order | the recipe: the storyboard follows the take |

Everything else is carried as written: the texts, the stage, the shots, the badge, the mark, the
expected result, the placeholder titles "Card 1" and "Card 2", and the loop note.

## What changes

All paths are relative to the repository root, on the batch's branch for this CR (see "Dependency
and base"). No change to `src/`, to a file of `docs/demo-video/clip-kit/`, to the recipe, to
`package.json` or to a lock file. No new dependency.

### 1. The live storyboard: `docs/demo-video/clips/slash-menu-grid/clip.md`

Start from the draft `work/storyboard/clip.md` of this CR's folder, with only the changes of the
table above. It follows the storyboard format of the recipe as `raw-copy-demo` leaves it.

- Front matter: `title: Feature clip slash-menu-grid`, `status: draft`, `date:` the day of the
  commit.
- The opening paragraph, as in the raw copy clip's live storyboard: "This is the live storyboard.
  The clip is built from this file: edit any row marked *(on screen)*, save, and run
  `just clip slash-menu-grid render`, then `check`. Rows marked *(filmed)* describe the take:
  changing them means a new take." Keep: one continuous shot, two texts in turn, the meaning of
  `**bold**`. Drop "Once approved, this file becomes …" and "The times below are the Griller's
  proposal …".
- `## Clip` table: `Length` (the take's; proposal `11.5 s`, within the kit's 5 to 12), `Size *(on
  screen)*` `1280x720 16:9`, `Frame rate *(on screen)*` `15 fps`, `Outputs` "silent, loops; MP4 (X,
  release), WebM (docs site), GIF 960 px (release notes, docs page)", `Cards` `none`, `Logo` `top
  right`, `Setting filmed`
  "`markdownOkfSchemaStudio.editing.defaultPaletteMode`: `myst` (Grid is a MyST command; the
  default GFM mode does not list it)", `Filmed on` (see the table above), `Stage` "`stage/onboarding.md`
  (Studio, the whole window, edit mode): a heading and one paragraph".
- `## 1. Type /grid, pick Grid`: the four pictures of section 1 with alt texts (the slash menu at
  the caret with Grid highlighted; the Insert grid form with its defaults; the `{grid}` text in the
  box with "Card 1" selected; the box closing on the save chord). `Time` `0 to <t1> s (…)`, with the
  take's action times in the parentheses. `Shot *(filmed)*` as in the draft. `Text 1 *(on screen)*`
  = `Type **/grid** in a block to insert a card grid`. `Badge save *(on screen)*` =
  `Ctrl+Enter / ⌘Enter`.
- `## 2. Zoom on the grid`: the pictures `frames/03-zoomed.png` and `frames/04-mark-1.png`.
  `Time` `<t1> to <Length> s (…)`. `Shot *(filmed)*` as in the draft. `Zoom` = `grid, hold to <s> s`.
  `Mark 1 *(on screen)*` = `Orange outline around the two cards, <from> to <to> s`. `Text 2 *(on
  screen)*` = `A MyST **card grid**, rendered in place`.
- The captions run end to end from 0 to `Length`; the mark lies inside the zoom hold.
- The "Expected result" paragraph and its `markdown` fenced block, as in the draft, character for
  character (the file on disk is that text followed by one newline). The paragraph now reads: "the
  scenario's check: `onboarding.md` on disk (auto-save is on) is exactly this text, followed by one
  newline". The parenthesis about the trial confirming the blank lines goes (settled by the code).
- "Review notes":
  - the draft's notes on the placeholder titles ("Card 1", "Card 2", "Content"; a typed title would
    add 2 s or more; the owner may ask for it) and on the loop seam;
  - Grid ranks first for `/grid` in MyST mode, and Table second (its alias "grid"); the take checks
    the highlighted entry before Enter;
  - only the save chord has a keycap badge. The two Enter, `/grid` and the form's Enter are typed
    and show in the box;
  - `01-selected` and `02-pasted` are the kit's fixed key frame names (here, just before and just
    after the save chord);
  - with the default GFM mode, `/grid` lists only Table and opens its size grid. That case is not
    filmed;
  - the measured raw screencast rate (`rawFps` of `check.json`);
  - the storyboard is reviewed in the PR after the take (clip-slash-grid-Q3).

### 2. The stage: `docs/demo-video/clips/slash-menu-grid/stage/onboarding.md`

The draft's `work/storyboard/stage/onboarding.md`, byte for byte (`# Onboarding`, a blank line,
`Welcome to the team. Pick the track that fits your first week.`, one final newline, LF).

### 3. The scenario: `docs/demo-video/clips/slash-menu-grid/scenario.mjs`

It follows the shape of `docs/demo-video/clips/raw-copy-balance-edges/scenario.mjs` and of CR-485's
scenario. It imports nothing, so a test can load it without VS Code. It exports `stage`, `open`,
`settings`, `checks`, `EXPECTED`, `setup`, `run` and `verify`. It uses the kit's helpers only
(`t.moveTo`, `t.click`, `t.textEdges`, `t.rectOf`, `t.press`, `t.keyFrame`, `t.zoom`, `t.unzoom`,
`t.mark`, `t.unmark`, `t.sleep`, `t.frameOf`, `t.workspaceFile`, `t.record`, `t.page`).
`t.rectOf(frame.locator(…))` gives an element of the preview webview in page coordinates.

- A header comment describes the scene and says that every caption, badge and time is in `clip.md`.
- `stage = { "stage/onboarding.md": "onboarding.md" }`; `open = ["onboarding.md"]`.
- `settings`: `"workbench.editorAssociations": { "onboarding.md": "markdown-okf-schema-studio.editor" }`
  and `"markdownOkfSchemaStudio.editing.defaultPaletteMode": "myst"`.
- `checks = { editMode: "on", paste: false }` (CR-485's export).
- `export const EXPECTED`: the "Expected result" block of `clip.md`, its lines joined with `\n`,
  without a final newline.
- `setup(t)`, off camera:
  - wait for the preview frame (`t.frameOf()`);
  - throw if `onboarding.md` in the workspace differs from the shipped stage file, or if a
    `.myst-grid-card` is in the page (a previous take must not leak);
  - edit mode: if `data-sphinx-preview-edit-mode` is `off`, click `[data-sphinx-preview-edit-toggle]`
    and wait for `on`, reading the attribute from a fresh frame as the raw copy scenario's
    `readingMode` helper does. Record it with `t.record("readingMode", mode)` (CR-485 compares it with
    `checks.editMode`) and throw unless `on`;
  - throw if a block text box is open;
  - park the pointer at a rest point in the page's empty right margin. The clip starts and ends there.
- `run(t)`, with an `until(seconds)` clock as in the raw copy scenario. The draft's times are the
  targets. Follow the recipe's pacing: moves of 600 to 900 ms, 400 ms before a click or a chord, and
  typing at about 120 ms per character so `/grid` reads.
  1. Move to the right edge of the paragraph's last character
     (`t.textEdges(frame, "week.", "week.").to`) and `t.click()` at about 0.8 s. Wait up to 3 s for
     `[data-sphinx-preview-block-editor] textarea`. Throw unless its value is
     `Welcome to the team. Pick the track that fits your first week.` and the caret is at its end
     (a click point, a scenario fix: "the caret is not at the end of the paragraph"). Throw unless
     `[data-sphinx-edit-palette="true"]` has `data-palette-mode="myst"`, with the message "the
     palette is not in MyST mode: a mode stored for the workspace wins over
     editing.defaultPaletteMode".
  2. At about 1.6 s, `t.page.keyboard.press("Enter")` twice, about 200 ms apart. Throw unless the
     value now ends with `week.\n\n`.
  3. From about 2.0 s, `t.page.keyboard.type("/grid", { delay: 120 })`. Wait up to 2 s for
     `[data-slash-menu]`. Record the `data-slash-id` of its options in order
     (`t.record("slashOptions", […])`). Throw unless the highlighted option
     (`[data-active="true"]`) is `grid` and `table` is listed after it. Then call
     `t.keyFrame("slash-menu")`.
  4. At about 3.4 s, `t.page.keyboard.press("Enter")`. Wait up to 2 s for
     `[data-sphinx-directive-panel="grid"]`. Throw unless its fields Columns, Gutter and Cards read
     `2`, `2`, `2`. Then call `t.keyFrame("grid-form")`.
  5. At about 4.6 s, `t.page.keyboard.press("Enter")`. Wait for the panel to be gone. Throw unless
     the text box value equals `EXPECTED` from the paragraph line on (the paragraph, one blank line,
     the grid) and the selected text is `Card 1`.
  6. At about 5.8 s, `t.press("ControlOrMeta+Enter", "save")`. Wait up to 5 s for the text box to
     close and for two `.myst-grid-card` whose `.myst-grid-card-title` texts are `Card 1` and
     `Card 2`, in that order. Record them (`t.record("cards", […])`). If the box stays open, throw
     with any status text the page shows.
  7. Move back to the rest point. At about 6.4 s, `t.zoom("grid", rect)`: the union of the paragraph
     and the two cards, padded 24 px (the kit limits the zoom to 2x).
  8. `t.mark("1", rect)` around the union of the two `.myst-grid-card` rectangles, with a few
     pixels of air, then `t.unmark("1")`, at the storyboard's mark times.
  9. At about 10.5 s, `t.unzoom("grid")`. End at the rest point near the length.
- `verify(t)`: after `t.sleep(800)` (auto-save), read `onboarding.md` with `t.workspaceFile`. Throw,
  with the file's text in the message, unless it equals `EXPECTED + "\n"`. Return
  `{ slashOptions, cards }` from the recorded notes. A difference is a finding against the feature
  (recipe, section 6), reported with the file's text, never fixed in the scenario.

### 4. Trial take, take and render

On Windows, on this machine, with the screen unlocked and no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`):

```bash
just dev
just package                     # out/reports/package/markdown-okf-schema-studio.vsix
just clip slash-menu-grid doctor
just clip slash-menu-grid all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

- The trial take (recipe, section 1) proves the recipe's points, plus these three. (e) The keys
  typed through CDP reach the text box and open the slash menu. (f) Enter picks Grid, and Enter in
  the form inserts the grid. (g) `ControlOrMeta+Enter` saves, and the page renders the two cards. If
  (e), (f) or (g) fails, stop and report. No script that sets the text box's value or calls a page
  function stands in for the filmed action.
- The trial's pictures and measured times go into `clip.md` (Q3), then the take that ships is
  filmed. `Length` (5 to 12 s, playback rate inside 0.77 to 1.3), the section times, the zoom hold
  and the mark times follow that take, in the same commit as the render.
- If the parser refuses `⌘Enter`, or the keycaps do not read `Ctrl` `Enter` and `⌘` `Enter`, write
  the macOS group as `⌘+Enter`. This needs a render, not a take.
- `verify` and `run`'s checks must hold. A failure is reported with what Studio showed
  (`failure.png`, the recorded notes) as a finding against the feature, and the clip waits.
- Commit together (the recipe's rule): `clip.md`, `scenario.mjs`, `stage/onboarding.md`, the
  outputs `slash-menu-grid.mp4`, `.webm` and `.gif` (Git LFS through `.gitattributes`),
  `poster.png`, `contact-sheet.png`, `first-last.png`, `frames/*.png` and `check.json`.

### 5. The docs page and its site test

- `docs/user/slash-menu.md`: after the bullet list (after "- The menu stays inside the window …")
  and before the existing screenshot, add the clip's GIF (the recipe's section 4):

  ```markdown
  ![In edit mode, /grid is typed on an empty line of a paragraph's text box: the slash menu highlights Grid, Enter opens the Insert grid form, Enter again inserts a MyST grid, and Ctrl+Enter / ⌘Enter renders two cards](../demo-video/clips/slash-menu-grid/slash-menu-grid.gif)
  ```

  The site build turns it into a looping video because the WebM is beside it
  (`SwRS-MDOKFSTUDIO-CORE-095`, unchanged). The screenshot stays.
- `test/site/siteClips.test.ts`: add a test "the shipped slash menu page plays the grid clip as
  video", modelled on "the shipped settings page plays the raw copy clip as video". It reads the
  shipped `docs/user/slash-menu.md` from the repository at the head under test, renders it with
  `renderMyst` and `clipVideos` as that test does, and asserts
  `<video src="../demo-video/clips/slash-menu-grid/slash-menu-grid.webm"`. It also asserts that
  `slash-menu-grid.webm`, `.gif` and `poster.png` exist in the clip folder. Marker:
  `// @tests_req SwRS-MDOKFSTUDIO-CORE-095` (a new test of an existing SwRS, no SwRS text change).
  Then run `just requirements-update`.
- No change to `README.md`, `docs/releases-notes/`, `CHANGELOG.md` (no `feat` or `fix` commit), the
  writing skill (no rendered syntax changes), the glossary or `AGENTS.md`.

### 6. Kit tests on the shipped clip

These go in CR-485's and CR-484's test files, run by `just clip-kit-test` inside `just check`
(`node:test`, `node:assert/strict`, Node built-ins only).

- `docs/demo-video/clip-kit/lib/storyboard.test.mjs` gains a case on the **shipped**
  `docs/demo-video/clips/slash-menu-grid/clip.md`. The file is read from the repository at the head
  under test (path from the test file's location, never a copy) with `parseClip`. The case asserts:
  - the length equals the committed value, the size is 1280x720, and the rate is 15 fps;
  - there are exactly two captions, with the texts `Type **/grid** in a block to insert a card grid`
    and `A MyST **card grid**, rendered in place` (as the parser returns them, `**` kept or stripped
    as it does), end to end from 0 to the length;
  - there is one badge, `save` = `Ctrl+Enter / ⌘Enter`, the zoom is `grid`, and one mark `1` lies
    inside the hold;
  - `validateStory` passes on `win32` and on `darwin`, with a take that logs the press `save`, the
    zoom `grid` and the mark `1`.
- The same file, or the file CR-485 puts its scenario tests in, also checks this clip's
  `EXPECTED`. It imports the constant from the shipped `scenario.mjs` and asserts it equals the
  `markdown` fenced block after the line that starts with "Expected result" in the shipped
  `clip.md`, character for character. The test extracts that block itself; the kit's
  `expectedPaste` reads only an "Expected paste" line.
- CR-485's test that resolves the `checks` of each shipped scenario covers `slash-menu-grid` and
  gives `{ editMode: "on", paste: false }`. If that test lists the clips by name, add this one.
- `just check` and `just format`. If a size or unused-export script fails on a new file, fix the
  file, not the script.

### 7. The pull request

- Commits by area, Conventional Commits (`.agents/guidelines/git-commit-message.guidelines.md`), no
  scope on `docs` or `test`:
  1. `docs: add the slash menu grid feature clip` (the clip folder, `docs/user/slash-menu.md`, the
     kit test cases of section 6);
  2. `test: play the grid clip on the slash menu page of the docs site` (`siteClips.test.ts` and the
     requirements files that `just requirements-update` changes).
- A draft PR (`gh pr create --draft`) in the batch's stack, until the owner approves the
  storyboard and the clip (Q3). The body follows `.github/PULL_REQUEST_TEMPLATE.md`, the PR
  guideline and the clip PR rule of `raw-copy-demo`. Impacts shows the GIF inline as
  `![…](https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/slash-menu-grid/slash-menu-grid.gif)`,
  with the MP4 and WebM linked in the same form at the same head sha. Each push of a new render moves
  the three links to the new head (`gh pr edit <n> --body-file <file>`). Check in the rendered PR
  page that the GIF plays. If it does not, push the three files to the `-assets` side branch as the
  recipe says, and say so in the body.
- The body states what the clip proves. In a real VS Code window on Windows, `/grid` in MyST mode
  highlights Grid first, the form takes its defaults, and the save renders two cards. `onboarding.md`
  holds exactly the expected text (the take's checks and `verify`, and the `check.json` lines). It
  also states what the owner judges: motion, rhythm, the loop as watched, and the texts and times
  of the storyboard. It links `clip.md`.
- The section "Deviation from the feature clip process" (see "The storyboard gate, moved after the
  take").
- "Autonomous decisions" lists the choices this spec made where the answers are silent:
  - the storyboard field split and the `Zoom` row;
  - the scenario key frames `slash-menu` and `grid-form`;
  - the unbadged Enter keys and the typed `/grid`;
  - the click point at the end of the paragraph;
  - the MyST mode check;
  - the dependency on CR-485's kit `checks` and `t.keyFrame`;
  - the GIF's place and alt text in `slash-menu.md`;
  - the site test;
  - the test that compares the "Expected result" block with `EXPECTED`.

## Out of scope

- Any change to `src/`, to an SwRS text or to the clip kit, its recipe or its existing tests' logic.
  The kit gaps are CR-485's.
- Typing real card titles over "Card 1" (the draft's note; the owner may ask at the review). Also
  out: the Card form, the other form fields (headers, footers, links), the palette's Grid button,
  the GFM default mode's `/grid` (Table).
- A macOS or Linux take. The retake after the owner's review is a follow-up of this CR (Q3).
- Marking the PR ready before the owner approves. Placing the clip in release notes, an
  announcement or the README.
- The other feature clips (their own CRs).

## CI

No CI job changes. The new kit test cases run in `just check` through `just clip-kit-test`, inside
the existing `ci-static` job (Linux and Windows, `.github/workflows/ci.yml`). The site test runs
where `test/site/` tests run today.

- Environment: a CI runner set up by `just dev-ci` from the lock files, with Node.js 24 from
  `.nvmrc` through `fnm`. Absent there but present locally: `ffmpeg`, the kit's scratch folder, the
  VS Code download, Remotion and a display. The tests need none of them: they parse the shipped
  `clip.md`, import the shipped `scenario.mjs`, and render the shipped `docs/user/slash-menu.md`.
  The clip's committed outputs come from Git LFS, checked out as CI does for the raw copy clip's
  site test.
- Before the push: `just clip-kit-test`, `just check` and `just ci-static` pass on Windows. Their
  output goes in the evidence.
- Only the first CI run proves the Linux leg: path handling, the dynamic `import` of the shipped
  scenario from a repository path, and the LFS files present for the site test.

## Host and default matrix

The clip depends on the host (the save chord) and on a configured value that is not the shipped
default (`editing.defaultPaletteMode`, filmed `myst`; the default is `gfm`).

| Host | VS Code | defaultPaletteMode | Expected | Proof |
| --- | --- | --- | --- | --- |
| Windows 11, `Ctrl+Enter` through CDP | pinned `DEFAULT_CODE_VERSION` | `myst` (scenario setting, no stored workspace mode) | Grid first for `/grid`, form defaults 2/2/2, two cards rendered, `onboarding.md` equals the expected text | the take's `run` checks and `verify`, `check.json` "scenario verify passed" |
| macOS, `⌘Enter` | same | `myst` | same | not proved (no macOS take) |
| Linux | same | `myst` | same | not proved |
| any | same | `gfm` (default) or `strict` | `/grid` lists Table only (alias), Enter opens the size grid | not filmed; stated in the storyboard's review notes |
| any | same | `myst` setting, another mode stored for the workspace | the stored mode wins | not filmed; the take throws on it (step 1) |

The kit tests run on Windows locally and on Linux and Windows in `ci-static`.

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows. The storyboard, `EXPECTED` and `checks`
   tests read the shipped `clip.md` and `scenario.mjs` at the head under test. The site test reads
   the shipped `docs/user/slash-menu.md`. No prepared text stands in for a shipped file.
2. `just clip slash-menu-grid doctor` passes, then `all --vsix …`. `check.json` shows:
   - `passed: true`;
   - MP4 and WebM at 1280x720 and 15 fps, with the MP4 duration equal to `Length` within one frame;
   - a GIF of at most 960 px and 12 fps;
   - a loop seam SSIM in [0.98, 1.0);
   - "Studio in edit mode at the start" and no paste line;
   - `verifyPassed: true`;
   - a playback rate inside 0.77 to 1.3;
   - platform `win32` and extension source `vsix`.
3. The agent looks at the contact sheet and every key frame, and checks:
   - `slash-menu`: the menu at the caret, Grid highlighted, Table under it;
   - `grid-form`: "Insert grid" with 2, 2, 2;
   - `01-selected`: the `{grid}` text with "Card 1" selected;
   - `02-pasted`: the box closing;
   - `03-zoomed` and `04-mark-1`: the two cards side by side, with the outline around both;
   - Text 1 in section 1 and Text 2 in section 2, and the keycap `Ctrl+Enter / ⌘Enter` at the save;
   - no tooltip, no personal name or path, no dirty tab.

   The report also names what was not checked: motion, rhythm and the loop as watched.
4. `just requirements-update` leaves the tree clean after its commit. `just preflight` passes (on
   Windows, its static stage).
5. The PR body plays the GIF and links the MP4 and WebM at the head sha (or on the `-assets` branch,
   said so). The PR is a draft.

## Open questions

None for the owner. The answers and the code settle the clip. The dependency on CR-485 is an
ordering fact, settled by clip-slash-grid-Q4: `depends.json` names CR 485.
