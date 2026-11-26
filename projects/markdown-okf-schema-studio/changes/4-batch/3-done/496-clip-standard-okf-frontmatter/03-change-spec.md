# Feature clip: edit the standard OKF frontmatter in place

Short name: `clip-okf-fm`. No tracker issue (verbal request of the owner, relayed by the Chief of
Staff, 2026-11-25).

## Goal

A feature clip of what Studio does with the standard OKF frontmatter of a page when no schema
applies, made with the merged clip kit (`docs/demo-video/clip-kit/`) and the feature clip recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`). A short release note, open in
Studio in edit mode, has the standard fields `title`, `description`, `status`, `date` and a `tags`
list; Studio shows them as a plain Names and Values table above the page, and the body shows the
field with `= this.status`. The pointer clicks the `draft` value of the `status` row: a text box
opens in the cell; `published` is typed over it and saved with Ctrl+Enter / ⌘Enter. The table row
and the body line both read `published`. Then a zoom on the table and the page marks the `status`
row, then the "Status: published" line. A user sees that the frontmatter is part of the page, not
hidden YAML to edit by hand. One continuous shot of about 11.5 s, two captions in turn, two marks in
turn, one save badge, 1280x720 at 15 fps, no card, the logo top right, a loop; MP4, WebM and GIF.
The pull request plays the clip and the owner reviews the storyboard and the clip there.

The clip lives in `docs/demo-video/clips/okf-frontmatter/`. It shows the existing feature: the
generic properties table (`src/core/frontmatter/propertiesTable.ts`, SwRS FMSCHEMA-005 and
FMSCHEMA-006), the click on a value cell in edit mode (`src/page/features/pageInput.ts`, FMEDIT-001),
the YAML text box of a field without a schema (`src/page/features/frontmatterValueEditor.ts`,
FMEDIT-004) and the value in the body (`src/core/render/frontmatterValues.ts`, CORE-079). No
behaviour of the extension changes and no rendered syntax changes, so the writing skill
`skills/writing-for-markdown-okf-schema-studio/` is not touched.

It is the first of two twin clips: `okf-schema-bundle-frontmatter` (CR
`clip-frontmatter-in-an-okf-schema-bundle`) films the same page inside an OKF Schema bundle. Both use
the same page and fields, the same `status` edit to `published`, the same click and save badge, the
same two marks and the same caption voice ("verb a **word**"), so what differs on screen is what the
schema brings.

## Dependency and base

Built on `origin/main`, alone (okf-fm-Q4): no `depends.json`, no dependency on the twin or on the
other clips of this round. Fetch first: the local `main` is behind `origin/main`. `origin/main`
already holds what this clip uses: the storyboard contract and parser (`lib/storyboard.mjs`), the
scenario export `checks = { editMode, paste }` (`resolveChecks`, `takeLines` in `lib/check.mjs`), the
helpers `t.keyFrame(name)`, `t.rectOf`, `t.textEdges` (`lib/take.mjs`), and the merged
`slash-menu-grid` clip, an edit mode clip with one save badge, whose scenario this clip follows. This
CR makes **no kit change**.

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| okf-fm-Q1 | The owner's wish: a clip of "what we do on standard OKF frontmatter"; one CR for this clip | whole spec |
| okf-fm-Q2 | The captions, stage and timing of the Griller's storyboard draft are the clip's shape | sections 1, 2, 3 |
| okf-fm-Q3 | The batch films a trial take from the draft, puts its pictures in the storyboard, renders, and opens the PR with the clip watchable (GIF inline, MP4 and WebM linked at the head); the PR stays a draft until the owner approves storyboard and clip; the deviation from the recipe's order is reported here and in the PR body; a retake after the owner's review is a follow-up of this CR | "The storyboard gate, moved after the take", sections 4, 7 |
| okf-fm-Q4 | Built on `origin/main`, alone, no `depends.json` | "Dependency and base" |
| okf-fm-Q5 | The stage is one short release note with `title`, `description`, `status`, `date` and a `tags` list; no `type`, no `_schema/` folder, so Studio shows the generic Names and Values table | sections 1, 3 |
| okf-fm-Q6 | The clip edits `status` from `draft` to `published` in the YAML text box and saves with Ctrl+Enter / ⌘Enter, shown as one badge | sections 2, 3 |
| okf-fm-Q7 | The body shows the field with `= this.status`; the second mark is on that line, inside the one zoom | sections 1, 2, 3 |
| okf-fm-Q8 | Kept consistent with the twin clip: same page and fields, same edit, same click and save badge, same two marks (the `status` row, then the "Status:" line), same caption voice, about the same length | sections 2, 3, 6 |
| okf-fm-Q9 | 11.5 s, inside the 12 s limit; no longer kit limit | sections 2, 4 |

## The storyboard gate, moved after the take

The recipe (section "The storyboard first") has the maintainer review the storyboard draft before
the take. okf-fm-Q3 moves that gate after the take, into the pull request; it does not drop it:

- the batch films a trial take from the draft, puts its pictures and measured times in the
  storyboard, moves it to `docs/demo-video/clips/okf-frontmatter/clip.md` with `status: draft`,
  films the take (the trial may be the take when it is clean), renders and opens the PR;
- the PR is a draft (`gh pr create --draft`) until the owner approves the storyboard and the clip;
  the agent never marks it ready; the PR body reports the deviation (section 7);
- the recipe is not changed by this CR.

## What changes

All paths are relative to the repository root.

### 1. The stage: `docs/demo-video/clips/okf-frontmatter/stage/release-note.md`

Copied byte for byte from `work/storyboard/stage/release-note.md` of this CR's folder (in the
planning surface,
`C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/2-backlog/P2/clip-standard-okf-frontmatter/`,
or wherever the batch moved the folder), LF line endings, ending with one newline:

```markdown
---
title: Release 2.4
description: What ships in the spring release.
status: draft
date: 2026-11-25
tags:
  - release
  - spring
---

# Release 2.4

**Status:** `= this.status`

The spring release brings faster search and a new export menu.
```

No `type` field and no `_schema/` folder anywhere in the stage (okf-fm-Q5): with no string `type`
Studio finds no schema, so `data-okf-schema-found="false"`, the header is Names and Values, no type
icon, no Description column, no title badge (`propertiesTable.ts`, `withDocs = result.schemaFound`).
The twin's page is this page plus `type: note` (and its typo); the two stage files must stay that
close: the batch does not reword this one.

### 2. The live storyboard: `docs/demo-video/clips/okf-frontmatter/clip.md`

The draft `work/storyboard/clip.md` of this CR's folder, adapted only as follows; every row marked
*(on screen)* keeps its text, and the times follow the take:

- Front matter: `title: Feature clip okf-frontmatter`, `status: draft`, `date:` the day of the
  commit.
- Opening paragraph: worded as the merged `slash-menu-grid/clip.md` ("**This is the live
  storyboard.** The clip is built from this file: edit any row marked *(on screen)*, save, and run
  `just clip okf-frontmatter render`, then `check`. Rows marked *(filmed)* describe the take: changing
  them means a new take. The text of an *(on screen)* row is the clip's exact text (`**bold**` takes
  the orange accent)."), then "The clip is one continuous shot: a click on the `status` value, a new
  value typed and saved, then a zoom on the frontmatter table and the page body. It shows two texts
  in turn." and the sentence naming the twin `okf-schema-bundle-frontmatter`. Drop "draft for
  review", "Once approved, this file becomes ..." and "The times below are the Griller's proposal
  ...".
- `## Clip` table as drafted: `Length` `11.5 s` (or the take's value), `Size *(on screen)*`
  `1280x720 16:9`, `Frame rate *(on screen)*` `15 fps`, `Outputs` as drafted, `Cards` `none`, `Logo`
  `top right`, `Setting filmed` `none: every setting at its default (edit mode is a view choice, set
  off camera)` (as `theme-switch` words it), `Filmed on` as the merged clips write it ("Windows, VS
  Code <version>, extension <version> VSIX built from the branch", the versions from `check.json`),
  `Stage` as drafted.
- The "Off camera (`setup`)" paragraph: removed from the committed file, as the merged clips have
  none; its content (toolbar expanded, edit mode on, pointer parked, what frame 0 shows) goes into
  one review note.
- `## 1. Click the value, type, save`: the line "Pictures: ..." replaced by links to the key frames
  `frames/editing.png`, `frames/01-selected.png` and `frames/02-pasted.png` (section 3; the last two
  are the kit's fixed names around the one press, as `slash-menu-grid` links them), each with an alt
  text saying what it shows; `Time` with the take's measured times; `Shot *(filmed)*` as drafted;
  `Text 1 *(on screen)*` = `Click a frontmatter value to **edit** it in place`;
  `Badge save *(on screen)*` = `Ctrl+Enter / ⌘Enter`.
- `## 2. Zoom on the table and the page`: the line "Pictures: ..." replaced by links to
  `frames/03-zoomed.png`, `frames/04-mark-1.png` and `frames/05-mark-2.png`; `Time` with the take's
  times; `Shot *(filmed)*` as drafted; `Zoom` = `table, hold to 10.5 s` (or the take's value);
  `Mark 1 *(on screen)*` = `Orange outline around the `status` row, 7.0 to 8.7 s`; `Mark 2 *(on
  screen)*` = `Orange outline around the "Status: published" line, 8.7 to 10.4 s`; `Text 2 *(on
  screen)*` = `The table and the page show the **new value**`. (Keep the backticks of mark 1 if
  `parseClip` reads the row unchanged, else drop them and say so in "Autonomous decisions"; the twin
  words its mark rows the same way.)
- "Expected result": the draft's prose kept, followed by the whole expected file in a `markdown`
  block, as `slash-menu-grid` does ("... is exactly this text, followed by one newline:"): the stage
  of section 1 with the one line `status: draft` changed to `status: published`, without its final
  newline. The block is the scenario's `EXPECTED`, character for character. The sentence on the
  preview (the `status` row and the body's inline value read `published`) kept.
- "Review notes": keep the draft's notes (behaviour relied on with its SwRS and files, the standard
  fields, how the text is selected and typed, why a string is edited, the status text that may
  flash, with what the frames showed); add the off-camera note above; add the measured times of the
  take ("Measured by the take: ...", as `slash-menu-grid`, with `rawFps`), `01-selected` and
  `02-pasted` as the kit's fixed key frame names (here, just before and just after the save chord),
  and "The storyboard is reviewed in the pull request after the take (okf-fm-Q3). Not checked by the
  author: motion, rhythm, the loop as watched."

### 3. The scenario: `docs/demo-video/clips/okf-frontmatter/scenario.mjs`

Modelled on `docs/demo-video/clips/slash-menu-grid/scenario.mjs` (copy its helpers `editMode`,
`waitFor`, `union`, its timing `until(seconds)` and its edit mode `setup`). No import beyond Node
built-ins; nothing runs at import, so the kit's tests can load it. The header comment says what is
filmed and that every caption and time is in `clip.md`.

- `stage = { "stage/release-note.md": "release-note.md" }`; `open = ["release-note.md"]`;
  `settings = { "workbench.editorAssociations": { "release-note.md": "markdown-okf-schema-studio.editor" } }`
  (no other setting: `frontmatter.propertiesTable` is on by default).
- `checks = { editMode: "on", paste: false }`.
- `export const STAGE`: the text of section 1, joined with `\n`, ending with one newline (the
  shipped stage file, byte for byte; `setup` compares the workspace file to it, as `slash-menu-grid`
  compares to its `shipped`).
- `export const EXPECTED`: `STAGE` with `"status: draft\n"` replaced by `"status: published\n"`,
  without its final newline (the "Expected result" block of `clip.md`).
- Selectors: `ROW = 'tr[data-okf-field="status"]'`, `CELL = \`${ROW} [data-okf-value-cell]\``,
  `BOX = '[data-okf-frontmatter-editor] textarea'`,
  `VALUE = '.okf-frontmatter-value[data-okf-this-field="status"]'`, `TABLE = "[data-okf-properties]"`.
- `setup(t)`, off camera:
  1. `release-note.md` on disk equals `STAGE`, else throw (a leaked previous take).
  2. Edit mode as `slash-menu-grid` (click `[data-sphinx-preview-edit-toggle]` until
     `data-sphinx-preview-edit-mode` is `"on"`); `t.record("editMode", mode)`; throw when not
     `"on"`.
  3. Expand the toolbar only when `[data-sphinx-preview-toolbar-collapse]` has
     `aria-expanded="false"` (as `export-html`'s setup).
  4. Wait (at most 10 s) until the page shows the generic table: `TABLE` with
     `data-okf-schema-found="false"`, header cells "Names" and "Values", no `td.okf-doc`, rows
     `data-okf-field` in source order `title`, `description`, `status`, `date`, `tags`; the
     `status` row has `data-okf-editable="true"` and reads `draft`; the `tags` value shows two items;
     the body's `VALUE` reads `draft`; no `[data-okf-frontmatter-editor]` open. Else throw with what
     was found. `t.record("fields", …)`.
  5. Park the pointer in the empty right margin of the page (as `slash-menu-grid`), `t.sleep(500)`
     (no row tooltip at frame 0 or at the seam: the row's `title` shows on hover).
- `run(t)`, timed with `until(seconds)` at the draft's times:
  1. at 0.3 s, `t.moveTo` (0.6 s) to the centre of the text `draft` in the `status` value cell
     (`t.textEdges` on the cell's text, or the centre of `t.rectOf(frame.locator(CELL))` when the
     text is not unique in the page: "draft" also shows in the body line);
  2. at 1.0 s, `t.click()` (a real CDP click; the kit draws the ripple); poll at most 3 s until
     `BOX` exists and its value, `trimEnd`, is `draft`; else throw (a finding against the feature);
     `t.keyFrame("editing")`; park the pointer back at the rest point (the frontmatter menu may open
     under it);
  3. at 1.8 s, select the box's whole text: `t.page.keyboard.press("ControlOrMeta+A")` (not
     `t.press`: no badge); check `selectionStart` is 0 and `selectionEnd` the value's length, else
     fall back to `box.select()` through the frame and say so in the review notes;
  4. at 2.2 s, `t.page.keyboard.type("published", { delay: 120 })`; check the box value is
     `published`;
  5. at 4.6 s, `t.press("ControlOrMeta+Enter", "save")`; re-read `t.frameOf()` and poll at most 5 s
     until `BOX` is gone, the `status` row's `[data-okf-value-display]` reads `published` and `VALUE`
     reads `published`; `t.record("tableValue", …)`, `t.record("bodyValue", …)`; else throw with
     the status text (`[role=status]`) and what the page shows;
  6. at 6.2 s, `t.zoom("table", rect)`: the union of `TABLE` and the paragraph holding `VALUE`,
     padded by 24 px (the kit caps the zoom at 2x);
  7. at 7.0 s, `t.mark("1", …)` around `ROW` padded by 6 px; at 8.7 s, `t.unmark("1")` and
     `t.mark("2", …)` around the paragraph holding `VALUE` ("Status: published"), padded the same;
     at 10.4 s, `t.unmark("2")`;
  8. at 10.5 s, `t.unzoom("table")` and `t.moveTo(home.x, home.y, 0.6)`; `until(11.5)`.
- `verify(t)`: `release-note.md` on disk (`t.workspaceFile`, auto-save on), polled up to 3 s, equals
  `EXPECTED + "\n"`; else throw with the text on disk (a writer that reformats another line, the
  `date` or the `tags` list, is a finding against the feature, not a scenario fix). Returns
  `{ text, tableValue, bodyValue }`.

### 4. Trial take, take and render

On Windows, on this machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`):

```bash
just dev
just package                                   # out/reports/package/markdown-okf-schema-studio.vsix
just clip okf-frontmatter doctor
just clip okf-frontmatter all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

When the workspace path shown anywhere in the frames holds the user name, run with
`CLIP_SCRATCH=C:/okfclip` (PowerShell: `$env:CLIP_SCRATCH = "C:/okfclip"`), as the export clip did.

- The trial take (recipe section 1, adapted): (a) the whole table (five rows, `tags` as two items)
  and the "Status:" line are in the frames at frame 0; (b) the click opens the text box and the save
  updates the table and the body (steps 2 and 5 of `run` pass); (c) the frontmatter menu or a
  tooltip opened by the click does not cover the `status` row in the frames after the click; if it
  does, keep it as filmed and say so in the review notes and the PR; (d) the status text "Saving
  frontmatter…" / "Saved. Refreshing preview…" seen or not in the zoom, said in the review notes;
  (e) the retimed rate is at least the storyboard's frame rate; (f) the loop seam SSIM in
  [0.98, 1.0).
- The trial's pictures and measured times go into `clip.md` (okf-fm-Q3); `Length` and every time
  follow the take (playback rate inside 0.77 to 1.3, `Length` at most 12 s), in the same commit as
  the render; the two captions stay end to end from 0 to `Length`, the marks inside the zoom hold.
- Commit together (recipe rule): `clip.md`, `scenario.mjs`, `stage/release-note.md`,
  `okf-frontmatter.mp4`, `.webm`, `.gif` (Git LFS through `.gitattributes`), `poster.png`,
  `contact-sheet.png`, `first-last.png`, `frames/*.png`, `check.json`.

### 5. Tests (no kit code change)

Each reads the shipped files from the repository, path from the test file's own location, at the
head under test, never a copy. Run by `just clip-kit-test` inside `just check`:

- `docs/demo-video/clip-kit/lib/storyboard.test.mjs` gains "the shipped okf-frontmatter clip.md
  reads as the clip the owner reviews", modelled on the `slash-menu-grid` case: `parseClip` gives
  1280x720, 15 fps, the committed `Length`, the two captions (`**` aside) "Click a frontmatter value
  to edit it in place" and "The table and the page show the new value", end to end from 0 to
  `Length`; badges `["save"]`; zoom `table`; marks `1`, `2` in turn inside the hold; the "Expected
  result" block equals the scenario's `EXPECTED`; `validateStory` passes with a `take` of press
  `save`, zoom `table`, marks `1` and `2`, on `win32` and on `darwin` (the combined badge).
- Same file: "the stage of the okf-frontmatter scenario is the shipped stage file, byte for byte"
  (as the `theme-switch` case): the scenario's `STAGE` equals the shipped `stage/release-note.md`;
  and "the okf-frontmatter clip changes the status line only": the shipped stage and `EXPECTED + "\n"`
  have the same lines except the one `status:` line, `draft` then `published`; the stage has no
  `type:` line and the clip folder no `stage/_schema/` (okf-fm-Q5, on the shipped files).
- `docs/demo-video/clip-kit/lib/check.test.mjs`: the test "the shipped scenarios declare their checks
  ..." gains `okf-frontmatter`: `resolveChecks` gives `{ editMode: "on", paste: false }` (its title
  names the frontmatter clip too).
- `test/site/siteClips.test.ts`: "the shipped OKF page plays the frontmatter clip as video",
  modelled on "the shipped slash menu page plays the grid clip as video": reads the shipped
  `docs/user/okf.md`, renders it with `renderMyst` and `clipVideos`, asserts
  `<video src="../demo-video/clips/okf-frontmatter/okf-frontmatter.webm"` and that
  `okf-frontmatter.webm`, `.gif` and `poster.png` exist; marker
  `// @tests_req SwRS-MDOKFSTUDIO-CORE-095` (an added test of an existing SwRS, no SwRS text
  change); then `just requirements-update`.

### 6. Docs

- `docs/user/okf.md`: after the paragraph "Studio makes that metadata comfortable to use. ... The
  Markdown body remains a live, editable MyST preview." and before `## Linked-File Annotations`, the
  image
  `![A release note with no schema: a click on the draft value of the status row opens a text box, published is typed and saved, and the frontmatter table and the Status line of the page both read published](../demo-video/clips/okf-frontmatter/okf-frontmatter.gif)`
  (the recipe, section 4: the GIF on the feature's docs page). The twin clip goes to the same place,
  after this one: when the twin is merged first, this GIF goes just before the twin's (no schema
  first, then what a schema adds); the `<!-- TODO: add frontmatter example here -->` comment of the
  "Linked-File Annotations" section is about `x-okf-link` and stays.
- No change to the recipe, the glossary, the writing skill, `README.md`, `CHANGELOG.md` or
  `docs/releases-notes/` (no `feat` or `fix` commit).

### 7. Commits and the pull request

- Commits by area (Conventional Commits; no scope on `docs` or `test`):
  `docs: add the standard OKF frontmatter feature clip` (clip folder, `docs/user/okf.md`),
  `test: check the frontmatter clip's storyboard, stage and docs page` (the kit test cases,
  `siteClips.test.ts`, the files `just requirements-update` changes).
- The PR is opened as a draft (`gh pr create --draft`) and stays a draft until the owner approves
  the storyboard and the clip (okf-fm-Q3); the agent does not mark it ready.
- The body follows `.github/PULL_REQUEST_TEMPLATE.md`, the PR guideline and the recipe's clip PR
  rule: the GIF inline from
  `https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/okf-frontmatter/okf-frontmatter.gif`,
  the MP4 and WebM linked in the same form at the same head; after each push of a new render the
  links move to the new head (`gh pr edit <n> --body-file <file>`); check that the GIF plays in the
  rendered PR page, else the recipe's `-assets` fallback.
- A section "Deviation from the feature clip process": the storyboard review moved from before the
  take into this PR (okf-fm-Q3); the take filmed from the Griller's draft; an *(on screen)* row the
  owner changes is a render (`just clip okf-frontmatter render` then `check`), a *(filmed)* row a
  retake, a follow-up of this CR. It links `clip.md` for the review, and names the twin clip
  `okf-schema-bundle-frontmatter` (its PR when open) so the owner reviews the two side by side.
- What the clip proves (a real click on a frontmatter value in a real VS Code window opens its text
  box, and the save writes the one `status` line and updates the table and the page body: the
  take's `run` checks and `verify`) and what the owner judges (motion, rhythm, the loop as watched,
  the texts and their accent).
- "Autonomous decisions": the differences from the draft (section 2), the key frame names, the
  selection way (Ctrl+A or `select()`), the measured times, the menu, tooltip or status text as
  seen, the docs placement, `CLIP_SCRATCH` if used.

## Out of scope

- Any change to `src/`, to an SwRS text, to the writing skill or to the clip kit's code (beyond test
  cases); a change of the recipe.
- A schema, a `type` field, typed controls, validation, the Description column (the twin's clip,
  okf-fm-Q8); editing a number, boolean, null, date or list value; adding or renaming a key.
- A macOS or Linux take; placing the clip in release notes or the announcement (a release CR does
  it); a retake after the owner's review (a follow-up of this CR, okf-fm-Q3); marking the PR ready
  before the owner approves.

## CI

No CI job changes. The new test cases run in `just check` through `just clip-kit-test`, inside the
existing `ci-static` job (Linux and Windows, `.github/workflows/ci.yml`); the site test runs where
`test/site/` tests run today.

- Environment: the CI machine set up by `just dev-ci` from the lock files, Node.js 24 from `.nvmrc`
  through `fnm`. Absent there and present locally: `ffmpeg`, the kit's scratch folder, the VS Code
  download, Remotion, a display. The new tests need none of them: the shipped `clip.md`,
  `scenario.mjs` (loaded, never run) and `stage/release-note.md`, the shipped `docs/user/okf.md` and
  the clip's committed files (Git LFS checked out as CI does for the merged clips' site tests).
- Before the push: `just clip-kit-test`, `just check` and `just ci-static` on Windows.
- Only the first CI run proves the Linux leg (the dynamic `import` of the scenario from a repository
  path, the line comparison of the stage with LF endings).

No host and default matrix: the clip films every setting at its default (edit mode is a view choice
set off camera), and the properties table, the value editor and `= this.status` do not depend on
the host or on a configured value.

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows; the storyboard, stage and checks tests read
   the shipped `clip.md`, `stage/release-note.md` and `scenario.mjs` at the head under test; the site
   test reads the shipped `docs/user/okf.md`.
2. The trial's six points (section 4), with what was seen for (a), (c) and (d) (frame names).
3. `just clip okf-frontmatter all --vsix ...` passes; `check.json` shows `passed: true`, MP4 and
   WebM 1280x720 at 15 fps, MP4 duration equal to `Length` within one frame, GIF at most 960 px and
   12 fps, loop seam SSIM in [0.98, 1.0), Studio in edit mode at the start, no paste line,
   `verifyPassed: true`, playback rate inside 0.77 to 1.3, platform `win32`, extension source
   `vsix`.
4. The take's `setup` found the generic table (step 4), `run` passed steps 2 and 5 (text box opened
   on `draft`; table and body read `published` within 5 s), and `verify` found `release-note.md`
   equal to `EXPECTED` plus one newline.
5. The agent looks at the contact sheet and every key frame: Studio in edit mode, the Names and
   Values table with five rows and no Description column or type icon, "Status: draft" at frame 0,
   the text box in the `status` cell, `published` in the row and the body after the save, the save
   badge, Text 1 during the edit and Text 2 during the zoom, mark 1 on the `status` row and mark 2
   on the "Status: published" line, no tooltip or hover at frame 0 and at the seam, no personal
   name or path, no dirty tab. What was not checked (motion, rhythm, the loop as watched) is said.
6. `just requirements-update` leaves the tree clean after its commit; `just preflight` passes (on
   Windows, its static stage).
7. The PR is a draft; its body plays the GIF, links the MP4 and WebM at the head sha and holds the
   "Deviation from the feature clip process" section.

## Open questions

None: `02-answers.md` (okf-fm-Q1 to Q9) and the code on `origin/main` settle every point this
specification needs.
