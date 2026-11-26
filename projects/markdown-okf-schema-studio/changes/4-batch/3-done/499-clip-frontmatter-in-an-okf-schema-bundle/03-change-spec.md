# Feature clip: the frontmatter in an OKF Schema bundle

Short name: `clip-bundle-fm`. No tracker issue (verbal request of the owner, relayed by the Chief
of Staff, 2026-11-25).

## Goal

A feature clip of what Studio does with the frontmatter of a page that lives in an OKF Schema
bundle, made with the merged clip kit (`docs/demo-video/clip-kit/`) and the feature clip recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`). The page `notes/release-note.md`
says `type: note`, so Studio finds `_schema/note.schema.yaml` and shows the frontmatter as a schema
table (Name, Value, Description, a type icon per field). The page starts with the typo
`status: publshed`: the `status` row is red and the title badge reads ✖ 1. In edit mode a click on
the value opens a select with the schema's values; two ArrowDown keys pick `published`, the save
chord saves, the red row and the badge go away and the body line reads "Status: published". Then a
zoom on the table and the page marks the `status` row, then the "Status:" line. A user sees that
the schema guides and checks the frontmatter, not only shows it.

One continuous shot of about 12 s (at most 12 s), two captions in turn, one badge, two marks in
turn, 1280x720 at 15 fps, no card, the logo top right, a loop; MP4, WebM and GIF. The clip lives in
`docs/demo-video/clips/okf-schema-bundle-frontmatter/`. The pull request plays the clip and the
owner reviews the storyboard and the clip there.

The clip shows existing behaviour: the schema lookup (`SwRS-MDOKFSTUDIO-FMSCHEMA-019`,
`src/core/frontmatter/okfFrontmatter.ts`), the schema table (`FMSCHEMA-029`,
`src/core/frontmatter/propertiesTable.ts`), the validation and the title badge (`FMSCHEMA-084`,
`FMSCHEMA-039`, `src/core/frontmatter/frontmatterValidate.ts`), the value editor opened by a click
(`FMEDIT-001`) and its enum select (`FMEDIT-003`, `src/page/features/frontmatterValueEditor.ts`),
and the inline value `= this.status` (`CORE-079`, `src/core/render/frontmatterValues.ts`). No
behaviour of the extension changes and no rendered syntax changes, so the writing skill
`skills/writing-for-markdown-okf-schema-studio/` is not touched.

## Dependency and base

Built on `origin/main`, alone (bundle-fm-Q4): no `depends.json`, no dependency on the other clips
of this round. Fetch first: the local `main` is behind `origin/main`. `origin/main` already holds
what this clip uses: the storyboard contract and parser (`lib/storyboard.mjs`), the scenario export
`checks = { editMode, paste }` (`resolveChecks`, `takeLines` in `lib/check.mjs`), the helper
`t.keyFrame(name)` (`lib/take.mjs`, frames written by `keyFrameTimes` in `lib/encode.mjs`), a stage
map whose target may sit in a sub-folder (`lib/profile.mjs` creates the parent folder), and the
merged `slash-menu-grid` clip, an edit mode clip in the whole window whose scenario this one is
modelled on. This CR makes **no kit change**.

Its twin `clip-standard-okf-frontmatter` (clip `okf-frontmatter`) is built on `origin/main` alone
too, and both add cases to the same test files and an image to the same docs page (sections 5
and 6). Whichever merges second rebases on the first and keeps both sides (force-with-lease of its
`chantier/<batch>/*` branch is pre-authorized); it does not wait for the other.

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| bundle-fm-Q1 | The owner's wish: a clip of the frontmatter in an OKF Schema bundle, the sibling of `clip-standard-okf-frontmatter`, kept consistent with it; one CR for this clip | whole spec, "Consistency with the twin" |
| bundle-fm-Q2 | The captions, stage and timing of the Griller's storyboard draft are the clip's shape | sections 1, 2, 3 |
| bundle-fm-Q3 | The batch films a trial take from the draft, puts its pictures in the storyboard, renders, and opens the PR with the clip watchable (GIF inline, MP4 and WebM linked at the head); the PR stays a draft until the owner approves storyboard and clip; the deviation from the recipe's order is reported here and in the PR body; a retake after the owner's review is a follow-up of this CR | "The storyboard gate, moved after the take", sections 4, 7 |
| bundle-fm-Q4 | Built on `origin/main`, alone, no `depends.json` | "Dependency and base" |
| bundle-fm-Q5 | The stage is a real bundle: `_schema/note.schema.yaml` at the stage root and `notes/release-note.md` with `type: note`; the schema follows the merged `post-mortem.schema.yaml` (status enum, date with format date, required fields, descriptions) | sections 1, 3 |
| bundle-fm-Q6 | The page starts with the typo `status: publshed`: frame 0 shows the red row and the ✖ 1 badge, and the fix makes them go away | sections 2, 3 (`setup` and `run` step 4) |
| bundle-fm-Q7 | The typed control filmed is the enum select, picked with two ArrowDown keys and saved with Ctrl+Enter / ⌘Enter | sections 2, 3 |
| bundle-fm-Q8 | If the native select popup shows or breaks the screencast, the scenario presses Escape and changes the value with ArrowDown on the closed select; no kit change | section 3 (`run` step 2), section 4 (trial point c) |
| bundle-fm-Q9 | Consistent with the twin: the same page and fields, the same `status` edit to `published`, the same click and save badge, the same two marks (the `status` row, then the "Status:" line), the same caption voice ("verb a **word**"), about the same length; only `type: note` and `_schema/` are added | "Consistency with the twin", sections 1, 2 |
| bundle-fm-Q10 | 12 s, inside the 12 s limit, no `depends.json`, no longer kit limit | sections 2, 4 |

## The storyboard gate, moved after the take

The recipe (a project guideline, section "The storyboard first") has the maintainer review the
storyboard draft before the take. bundle-fm-Q3 moves that gate after the take, into the pull
request; it does not drop it:

- the batch films a trial take from the draft, puts its pictures and measured times in the
  storyboard, moves it to `docs/demo-video/clips/okf-schema-bundle-frontmatter/clip.md` with
  `status: draft`, films the take (the trial may be the take when it is clean), renders and opens
  the PR;
- the PR is a draft (`gh pr create --draft`) until the owner approves the storyboard and the clip;
  the agent never marks it ready; the PR body reports the deviation (section 7);
- the recipe is not changed by this CR.

## Consistency with the twin

The twin clip `okf-frontmatter` films the same page without `type` and without `_schema/`. What
stays the same, and must not drift in this CR: the page's title, description, date, tags, heading,
"Status:" line and sentence; the `status` field edited to `published`; a click on the value cell;
the one badge `save` = `Ctrl+Enter / ⌘Enter`; mark 1 on the `status` row and mark 2 on the
"Status: published" line, inside one zoom on the table and that line; two captions in the voice
"verb a **word**"; edit mode on, the toolbar expanded, the whole window. What differs, all on
screen, is what the schema brings: the Description column and the type icons, the red row and the
✖ 1 badge at frame 0, the select in place of the text box. When the twin's spec or merged files
name a helper, a test title form or a docs placement differently from this spec, the Driver follows
the twin where it is merged and says so in "Autonomous decisions".

## What changes

All paths are relative to the repository root. The clip folder is
`docs/demo-video/clips/okf-schema-bundle-frontmatter/` (below: the clip folder).

### 1. The stage

Copied byte for byte from `work/storyboard/stage/` of this CR's folder (in the planning surface,
`C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/2-backlog/P2/clip-frontmatter-in-an-okf-schema-bundle/`,
or wherever the batch moved the folder), LF line endings, each ending with one newline:

- `<clip folder>/stage/_schema/note.schema.yaml`: an object schema titled `Note`,
  `additionalProperties: true`, required `type`, `title`, `status`, `date`; properties `type`
  (`const: note`), `title` (string, `minLength: 1`), `description` (string), `status` (enum
  `draft`, `published`, `retired`, description "Where the note stands."), `date` (string,
  `format: date`), `tags` (array of strings); each with a one-line description.
- `<clip folder>/stage/notes/release-note.md`:

```markdown
---
type: note
title: Release 2.4
description: What ships in the spring release.
status: publshed
date: 2026-11-25
tags:
  - release
  - spring
---

# Release 2.4

**Status:** `= this.status`

The spring release brings faster search and a new export menu.
```

The typo `publshed` is the stage, on purpose (bundle-fm-Q6). Below the frontmatter, the page is
the twin's `stage/release-note.md` line for line; only the `type: note` line and the `status` value
differ.

### 2. The live storyboard: `<clip folder>/clip.md`

The draft `work/storyboard/clip.md` of this CR's folder, adapted only as follows; every row marked
*(on screen)* keeps its text, and the times follow the take:

- Front matter: `title: Feature clip okf-schema-bundle-frontmatter`, `status: draft`, `date:` the
  day of the commit.
- Opening paragraph: worded as the merged `slash-menu-grid/clip.md` ("**This is the live
  storyboard.** The clip is built from this file: edit any row marked *(on screen)*, save, and run
  `just clip okf-schema-bundle-frontmatter render`, then `check`. Rows marked *(filmed)* describe
  the take: changing them means a new take. The text of an *(on screen)* row is the clip's exact
  text (`**bold**` takes the orange accent)."), then the draft's description of the shot and the
  sentence on the sibling `okf-frontmatter`. Drop "draft for review", "Once approved, this file
  becomes ..." and "The times below are the Griller's proposal ...".
- `## Clip` table as drafted: `Length` `12 s` (or the take's value, at most 12 s),
  `Size *(on screen)*` `1280x720 16:9`, `Frame rate *(on screen)*` `15 fps`, `Outputs` as drafted,
  `Cards` `none`, `Logo` `top right`, `Setting filmed` as drafted, `Filmed on` written as the grid
  clip does ("Windows, VS Code <version>, extension <version> VSIX built from the branch", the
  versions from `check.json`), `Stage` as drafted.
- The "Off camera (`setup`)" paragraph: kept as a review note (the grid clip has none in its body).
- `## 1. Pick a valid value, save`: the line "Pictures: ..." replaced by links to the key frames
  `frames/invalid.png`, `frames/select-open.png`, `frames/picked.png`, `frames/01-selected.png`
  and `frames/02-pasted.png` (section 3; the last two are the kit's fixed names, here just before
  and just after the save chord, as the grid clip says), each with an alt text saying what it
  shows; `Time` with the take's measured times; `Shot *(filmed)*` as drafted;
  `Text 1 *(on screen)*` = `The schema **types** each field: pick a valid value`;
  `Badge save *(on screen)*` = `Ctrl+Enter / ⌘Enter`.
- `## 2. Zoom on the table and the page`: the line "Pictures: ..." replaced by links to
  `frames/03-zoomed.png`, `frames/04-mark-1.png` and `frames/05-mark-2.png`; `Time` and
  `Shot *(filmed)*` as drafted, times from the take; `Zoom` = `table, hold to 11.0 s` (the take's
  value); `Mark 1 *(on screen)*` = `Orange outline around the status row, 7.4 to 9.1 s`;
  `Mark 2 *(on screen)*` = `Orange outline around the "Status: published" line, 9.1 to 10.8 s`
  (times from the take; the draft writes `status` in backticks in mark 1: keep them if `parseClip`
  reads the row unchanged, else drop them and say so in "Autonomous decisions");
  `Text 2 *(on screen)*` = `Studio **validates** the value: the error is gone`.
- "Expected result" paragraph as drafted, followed by a fenced `markdown` block holding the whole
  expected `notes/release-note.md` (the stage with `status: published`), without its final newline:
  the block is the scenario's `EXPECTED`, character for character (as the grid clip).
- "Review notes": keep the draft's notes (the bundle rule and the Restricted Mode remark, the
  behaviour relied on, what differs from the sibling, the select popup risk with what the trial
  showed, the row tooltip, the Description column at 1280x720 with what the trial showed, the
  12 s length); add the off-camera note, the pointer parked after the click (section 3), the
  frontmatter menu beside the open select if it shows, the measured times of the take (as the grid
  clip's "Measured by the take" note) and "The storyboard is reviewed in the pull request after the
  take (bundle-fm-Q3). Not checked by the author: motion, rhythm, the loop as watched."

### 3. The scenario: `<clip folder>/scenario.mjs`

Modelled on `docs/demo-video/clips/slash-menu-grid/scenario.mjs` (copy its `editMode`, `waitFor`
and `union` helpers and its `until` timing). Node built-ins only; nothing runs at import, so the
kit's tests can load it. The header comment says what is filmed and that every caption and time is
in `clip.md`.

- `stage = { "stage/_schema/note.schema.yaml": "_schema/note.schema.yaml", "stage/notes/release-note.md": "notes/release-note.md" }`.
- `open = ["notes/release-note.md"]`.
- `settings = { "workbench.editorAssociations": { "release-note.md": "markdown-okf-schema-studio.editor" } }`
  (a pattern with no `/` matches the file name; if VS Code does not open the file in Studio with
  it, use `"**/release-note.md"` and say so in "Autonomous decisions"). No Studio setting: workspace
  trust is off in the kit's `BASE_SETTINGS`, so the schema lookup runs.
- `checks = { editMode: "on", paste: false }`.
- `export const EXPECTED`: the expected `notes/release-note.md` as a joined array of lines, without
  its final newline (the "Expected result" block of `clip.md`).
- `export const TYPO = "status: publshed"` and `export const FIXED = "status: published"` (used by
  the tests, section 5).
- `setup(t)`, off camera, as the grid clip's `setup`:
  - `t.workspaceFile("notes/release-note.md")` equals the shipped stage (read from
    `new URL("./stage/notes/release-note.md", import.meta.url)` with `node:fs`), else throw;
  - edit mode on (click `[data-sphinx-preview-edit-toggle]` until `data-sphinx-preview-edit-mode`
    is `"on"`), `t.record("readingMode", mode)`, throw when not `"on"`;
  - wait (at most 10 s) for the frame 0 state, else throw with what was found:
    `section[data-okf-properties][data-okf-schema-found="true"]`; the header cells Name, Value,
    Description; the rows `tr[data-okf-field]` `type`, `title`, `description`, `status`, `date`,
    `tags`; exactly one row with class `okf-error`, the `status` row, whose `data-okf-type` is
    `enum` and `data-okf-editable` is `"true"`; `[data-okf-badge]` with `data-okf-errors="1"` and
    the text `✖ 1`; one `.okf-frontmatter-value` reading `publshed`; no
    `[data-okf-frontmatter-editor]` open. `t.record("frame0", …)` with what was read, and the
    `status` row's `title` (the tooltip, expected to hold "must be equal to one of the allowed
    values");
  - park the pointer in the empty right margin of the page (the grid clip's rest point),
    `t.sleep(500)`.
- `run(t)`, timed with `until(seconds)`; the times are the draft's and the take may move them:
  1. at 0.2 s, `t.keyFrame("invalid")`; `t.moveTo` (0.6 s) to the centre of the `status` row's
     `[data-okf-value-cell]`; at 1.2 s, `t.click()` (a real CDP click: the kit draws the ripple);
     wait (at most 3 s) for `[data-okf-frontmatter-editor] select` in that cell, focused, with the
     options "Choose a value...", `draft`, `published`, `retired` and `value` `""` (the disabled
     first entry chosen because `publshed` is not allowed); else throw;
  2. move the pointer back to the rest point (0.5 s), so the row's `title` tooltip and the hover
     do not show (the grid clip does the same after its click); `t.keyFrame("select-open")`. The
     click lands on the value cell before the select exists, and the editor focuses the select by
     script, so no native popup is expected. If the trial's frames show a popup or a broken
     screencast (bundle-fm-Q8), add one `page.keyboard.press("Escape")` here, then check that the
     select is still open in the cell (Escape in the select's `keydown` cancels the editor:
     `frontmatterValueEditor.ts`); if the editor closed, that is a finding, reported, not worked
     around;
  3. at 2.2 s and 2.7 s, `page.keyboard.press("ArrowDown")` (not `t.press`: only the save is a
     badge); after each, read the select's `value`: `draft`, then `published`, else throw (on
     Windows, ArrowDown on a closed select changes its value in place); the file on disk still
     holds `publshed` (a pick alone does not save); `t.keyFrame("picked")`;
  4. at 4.8 s, `t.press("ControlOrMeta+Enter", "save")`; re-read `t.frameOf()` between polls and
     wait (at most 5 s) until no `[data-okf-frontmatter-editor]` is open, no row has class
     `okf-error`, no `[data-okf-badge]` is present, the `status` row's `data-okf-value` is
     `"published"`, and `.okf-frontmatter-value` reads `published`; `t.record("after", …)`; else
     throw with what the page shows (a failure here is a finding against the feature, not a
     scenario fix);
  5. at 6.9 s, `t.zoom("table", rect)`: the union of the `[data-okf-properties]` section and the
     paragraph holding `.okf-frontmatter-value`, padded by 24 px (the kit caps the zoom at 2x);
  6. at 7.4 s, `t.mark("1", …)` on the `status` row's box padded by 6 px; at 9.1 s, `t.unmark("1")`
     and `t.mark("2", …)` on the "Status: published" paragraph's box padded by 6 px; at 10.8 s,
     `t.unmark("2")`;
  7. at 11.0 s, `t.unzoom("table")` and `t.moveTo(home.x, home.y, 0.6)`; `until(12.0)`.
- `verify(t)`: `notes/release-note.md` on disk (`t.workspaceFile`, auto-save on), polled up to
  3 s, equals `EXPECTED` plus one newline, else throw with the text on disk; and
  `_schema/note.schema.yaml` on disk equals the shipped `stage/_schema/note.schema.yaml`, else
  throw. Returns `{ text, frame0, after }`.

### 4. Trial take, take and render

On Windows, on this machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`):

```bash
just dev
just package                                   # out/reports/package/markdown-okf-schema-studio.vsix
just clip okf-schema-bundle-frontmatter doctor
just clip okf-schema-bundle-frontmatter all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

When the workspace path shown anywhere in the frames holds the user name, run with
`CLIP_SCRATCH=C:/okfclip` (PowerShell: `$env:CLIP_SCRATCH = "C:/okfclip"`) as the export clip did.

- The trial take (recipe section 1, adapted), each point with the frame that shows it:
  (a) frame 0 shows the schema table with the Description column and type icons at 1280x720 (not
  collapsed), the red `status` row and the ✖ 1 badge; (b) the click opens the select and step 1
  of `run` passes; (c) no native popup in the frames and the screencast unbroken; else the Escape
  of bundle-fm-Q8 (section 3, step 2); (d) the two ArrowDown keys reach `published` and the save
  clears the row and the badge (steps 3 and 4 pass); (e) the retimed rate is at least the
  storyboard's frame rate; (f) the loop seam SSIM in [0.98, 1.0) (the clip ends with a valid page
  and starts with the typo: the seam relies on the kit's return to the start, as the grid clip).
- The trial's pictures and measured times go into `clip.md` (bundle-fm-Q3); `Length` and every
  time follow the take (playback rate inside 0.77 to 1.3, `Length` at most 12 s), in the same
  commit as the render; the two captions stay end to end from 0 to `Length`, the marks inside the
  zoom hold.
- Commit together (recipe rule): `clip.md`, `scenario.mjs`, `stage/_schema/note.schema.yaml`,
  `stage/notes/release-note.md`, `okf-schema-bundle-frontmatter.mp4`, `.webm`, `.gif` (Git LFS
  through `.gitattributes`), `poster.png`, `contact-sheet.png`, `first-last.png`, `frames/*.png`,
  `check.json`.

### 5. Tests (no kit code change)

Each reads the shipped files from the repository, path from the test file's own location, at the
head under test, never a copy. Node built-ins only in the kit tests. Run by `just clip-kit-test`
inside `just check`:

- `docs/demo-video/clip-kit/lib/storyboard.test.mjs` gains "the shipped okf-schema-bundle-frontmatter
  clip.md reads as the clip the owner reviews", modelled on the slash-menu-grid case: `parseClip`
  gives 1280x720, 15 fps, `Length` at most 12, the two captions (`**` aside) "The schema types each
  field: pick a valid value" and "Studio validates the value: the error is gone", end to end from 0
  to `Length`; badges `["save"]`; zoom `table`; marks `1`, `2` in turn inside the hold;
  `validateStory` passes on `win32` and `darwin` with a take of one press `save`, zoom `table`,
  marks `1` and `2`; the "Expected result" block equals the scenario's `EXPECTED`.
- Same file: "the stage of the okf-schema-bundle-frontmatter clip differs from the expected page by
  the status line only": the shipped `stage/notes/release-note.md` holds the line `TYPO` exactly
  once, and replacing it by `FIXED` gives `EXPECTED` plus one newline; and the shipped
  `stage/_schema/note.schema.yaml` holds, as text, the `status` enum `draft`, `published`,
  `retired` and no `publshed` (the clip's claim "the typo is invalid and `published` is valid",
  checked on the shipped files).
- `docs/demo-video/clip-kit/lib/check.test.mjs`: the test "the shipped scenarios declare their
  checks ..." gains `okf-schema-bundle-frontmatter`: `resolveChecks` gives
  `{ editMode: "on", paste: false }` (its title names the bundle frontmatter clip too).
- `test/site/siteClips.test.ts`: "the shipped OKF page plays the schema bundle frontmatter clip as
  video", modelled on "the shipped slash menu page plays the grid clip as video": reads the shipped
  `docs/user/okf.md`, renders it with `renderMyst` and `clipVideos`, asserts
  `<video src="../demo-video/clips/okf-schema-bundle-frontmatter/okf-schema-bundle-frontmatter.webm"`
  and that the `.webm`, `.gif` and `poster.png` exist; marker
  `// @tests_req SwRS-MDOKFSTUDIO-CORE-095` (an added test of an existing SwRS, no SwRS text
  change); then `just requirements-update`.

### 6. Docs

- `docs/user/okf.md`: after the paragraph "Studio makes that metadata comfortable to use. ... The
  Markdown body remains a live, editable MyST preview.", the image
  `![A note in an OKF Schema bundle: its frontmatter table shows a Description column and type icons, the status row is red for the value "publshed"; a click opens a select with the schema's values, published is picked and saved, the error goes away and the page body reads Status: published](../demo-video/clips/okf-schema-bundle-frontmatter/okf-schema-bundle-frontmatter.gif)`
  (the recipe, section 4: the GIF under the entry of the feature). If the twin's GIF already sits
  under that paragraph on the base, this image goes right after it, so the standard clip comes
  first.
- No change to the recipe, the glossary, the writing skill, `README.md`, `CHANGELOG.md` or
  `docs/releases-notes/` (no `feat` or `fix` commit).

### 7. Commits and the pull request

- Commits by area (Conventional Commits; no scope on `docs` or `test`):
  `docs: add the schema bundle frontmatter feature clip` (clip folder, `docs/user/okf.md`),
  `test: check the schema bundle frontmatter clip's storyboard, stage and docs page` (the kit test
  cases, `siteClips.test.ts`, the files `just requirements-update` changes).
- The PR is opened as a draft (`gh pr create --draft`) and stays a draft until the owner approves
  the storyboard and the clip (bundle-fm-Q3); the agent does not mark it ready.
- The body follows `.github/PULL_REQUEST_TEMPLATE.md`, the PR guideline and the recipe's clip PR
  rule: the GIF inline from
  `https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/okf-schema-bundle-frontmatter/okf-schema-bundle-frontmatter.gif`,
  the MP4 and WebM linked in the same form at the same head; after each push of a new render the
  links move to the new head (`gh pr edit <n> --body-file <file>`); check that the GIF plays in the
  rendered PR page, else the recipe's `-assets` fallback.
- A section "Deviation from the feature clip process": the storyboard review moved from before the
  take into this PR (bundle-fm-Q3); the take filmed from the Griller's draft; an *(on screen)* row
  the owner changes is a render (`just clip okf-schema-bundle-frontmatter render` then `check`), a
  *(filmed)* row a retake, a follow-up of this CR. It links `clip.md` for the review, and names the
  twin clip's PR when it is open.
- What the clip proves (in a real VS Code window, a page with `type: note` in a bundle shows the
  schema table and the error on `status: publshed`; a click and two keys pick `published` in the
  schema's select; the save writes the one line and the error and badge go away: the take's `run`
  checks and `verify`) and what the owner judges (motion, rhythm, the loop as watched, the texts
  and their accent, the consistency with the twin).
- "Autonomous decisions": the differences from the draft (section 2), the pointer parked after the
  click, the key frame names, the measured times, whether the Escape of bundle-fm-Q8 was needed,
  the editor association pattern, `CLIP_SCRATCH` if used, any point where the twin's merged files
  were followed over this spec.

## Out of scope

- Any change to `src/`, to an SwRS text, to the writing skill or to the clip kit's code (beyond
  test cases); a change of the recipe.
- The other typed controls (date, list, checkbox, number), the row tooltip on hover, the badge's
  jump to the first issue, the Set to null button, reading mode, a missing required field, the
  `x-okf-link` annotations.
- A kit change for the native select popup (bundle-fm-Q8); a longer kit limit (bundle-fm-Q10).
- A macOS or Linux take; placing the clip in release notes or the announcement (a release CR does
  it); a retake after the owner's review (a follow-up of this CR, bundle-fm-Q3); marking the PR
  ready before the owner approves; the twin clip `okf-frontmatter` (its own CR).

## CI

No CI job changes. The new test cases run in `just check` through `just clip-kit-test`, inside the
existing `ci-static` job (Linux and Windows, `.github/workflows/ci.yml`); the site test runs where
`test/site/` tests run today.

- Environment: the CI machine set up by `just dev-ci` from the lock files, Node.js 24 from `.nvmrc`
  through `fnm`. Absent there and present locally: `ffmpeg`, the kit's scratch folder, the VS Code
  download, Remotion, a display. The new tests need none of them: the shipped `clip.md`,
  `scenario.mjs` (loaded, never run), `stage/notes/release-note.md` and
  `stage/_schema/note.schema.yaml`, the shipped `docs/user/okf.md` and the clip's committed files
  (Git LFS checked out as CI does for the merged clips' site tests).
- Before the push: `just clip-kit-test`, `just check` and `just ci-static` on Windows.
- Only the first CI run proves the Linux leg (the dynamic `import` of the scenario from a
  repository path, the line comparison of the stage files with LF endings).

No host and default matrix: the clip films Studio's defaults (edit mode is a toolbar choice, the
editor association only opens the file in Studio), and the schema lookup, validation and select do
not depend on the host or on a configured value. The take is on Windows only, where ArrowDown
changes a closed select in place; that is a property of the take, stated in the review notes.

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows; the storyboard, stage and checks tests
   read the shipped `clip.md`, `stage/notes/release-note.md`, `stage/_schema/note.schema.yaml` and
   `scenario.mjs` at the head under test; the site test reads the shipped `docs/user/okf.md`.
2. The trial's six points (section 4), with the frame that shows each of (a) to (d).
3. `just clip okf-schema-bundle-frontmatter all --vsix ...` passes; `check.json` shows
   `passed: true`, MP4 and WebM 1280x720 at 15 fps, MP4 duration equal to `Length` (at most 12 s)
   within one frame, GIF at most 960 px and 12 fps, loop seam SSIM in [0.98, 1.0), "Studio in edit
   mode at the start", no paste line, `verifyPassed: true`, playback rate inside 0.77 to 1.3,
   platform `win32`, extension source `vsix`.
4. The take's `setup` found the frame 0 state (schema table, one error on `status`, ✖ 1, body
   `publshed`); `run` passed steps 1, 3 and 4 (select with the schema's values, `draft` then
   `published`, no error and no badge after the save, body `published`); `verify` found
   `notes/release-note.md` equal to `EXPECTED` and the schema unchanged.
5. The agent looks at the contact sheet and every key frame: the schema table with Name, Value,
   Description and type icons, the red `status` row and ✖ 1 at frame 0, the select in the cell
   with "Choose a value..." then `published`, no native popup, no row tooltip, the row and badge
   cleared after the save, Text 1 during the pick and Text 2 during the zoom, the badge at the
   save, mark 1 on the `status` row and mark 2 on the "Status: published" line, no personal name
   or path, no dirty tab after the save. What was not checked (motion, rhythm, the loop as
   watched) is said.
6. `just requirements-update` leaves the tree clean after its commit; `just preflight` passes (on
   Windows, its static stage).
7. The PR is a draft; its body plays the GIF, links the MP4 and WebM at the head sha and holds the
   "Deviation from the feature clip process" section.

## Open questions

None: `02-answers.md` (bundle-fm-Q1 to Q10) and the code on `origin/main` settle every point this
specification needs.
