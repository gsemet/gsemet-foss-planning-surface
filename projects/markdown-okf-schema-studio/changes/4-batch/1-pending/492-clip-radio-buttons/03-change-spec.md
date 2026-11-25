# Feature clip: pick an option, the file follows

Short name: `clip-radio`. No tracker issue (verbal request of the owner, relayed by the Chief of
Staff, 2026-11-25).

## Goal

A feature clip of Studio's radio choice lists, made with the merged clip kit
(`docs/demo-video/clip-kit/`) and the feature clip recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`). A short plan, open in Studio in
reading mode on the left and as raw text on the right, asks its reader to pick one of three
options. The pointer clicks the second option: the page selects it at once and the `x` moves in the
Markdown file, two characters on two lines. Then a zoom on the raw text marks the new `(x)` and the
old option, now `( )`. One continuous shot of about 10.5 s, two captions in turn, two marks in turn,
1280x720 at 15 fps, no card, the logo top right, a loop; MP4, WebM and GIF. The pull request plays
the clip and the owner reviews the storyboard and the clip there.

The clip shows the existing feature (`src/core/render/radioMarkers.ts`,
`src/core/render/radioGroups.ts`, `src/page/features/checkboxes.ts`,
`SwRS-MDOKFSTUDIO-GFM-040` render and `SwRS-MDOKFSTUDIO-GFM-041` choice); no behaviour of the
extension changes, and no rendered syntax changes (so the writing skill
`skills/writing-for-markdown-okf-schema-studio/` is not touched).

## Dependency and base

Built on `origin/main`, alone (radio-Q4): no `depends.json`, no dependency on the other clips of
this round. Fetch first: the local `main` is behind `origin/main`. `origin/main` already holds what
this clip uses: the storyboard contract and parser (`lib/storyboard.mjs`), the scenario export
`checks = { editMode, paste }` (`resolveChecks`, `takeLines` in `lib/check.mjs`), the helper
`t.keyFrame(name)` (`lib/take.mjs`, frames written by `keyFrameTimes` in `lib/encode.mjs`), and the
merged `drag-list-item` clip whose split layout this clip reuses. This CR makes **no kit change**.

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| radio-Q1 | The owner's wish: a clip of radio buttons; one CR for this clip | whole spec |
| radio-Q2 | The captions, stage and timing of the Griller's storyboard draft are the clip's shape | sections 1, 2, 3 |
| radio-Q3 | The batch films a trial take from the draft, puts its pictures in the storyboard, renders, and opens the PR with the clip watchable (GIF inline, MP4 and WebM linked at the head); the PR stays a draft until the owner approves storyboard and clip; the deviation from the recipe's order is reported here and in the PR body; a retake after the owner's review is a follow-up of this CR | "The storyboard gate, moved after the take", sections 4, 7 |
| radio-Q4 | Built on `origin/main`, alone, no `depends.json` | "Dependency and base" |
| radio-Q5 | Studio on the left in reading mode, the same file as raw text on the right, the layout of the merged `drag-list-item` clip | sections 2, 3 |
| radio-Q6 | The stage is a short plan with one bulleted group of three options, the first preselected; the clip clicks the second; numbered and nested groups, the keyboard and the undo are not filmed | sections 1, 3, "Out of scope" |
| radio-Q7 | Two beats: the click, then a zoom on the raw text with two marks (the new `(x)`, then the old option now `( )`), 10.5 s | sections 2, 3 |
| radio-Q8 | The loop seam is the kit's return to the start, with no click back | sections 2, 3 |

## The storyboard gate, moved after the take

The recipe (a project guideline, section "The storyboard first") has the maintainer review the
storyboard draft before the take. radio-Q3 moves that gate after the take, into the pull request;
it does not drop it:

- the batch films a trial take from the draft, puts its pictures and measured times in the
  storyboard, moves it to `docs/demo-video/clips/radio-buttons/clip.md` with `status: draft`, films
  the take (the trial may be the take when it is clean), renders and opens the PR;
- the PR is a draft (`gh pr create --draft`) until the owner approves the storyboard and the clip;
  the agent never marks it ready; the PR body reports the deviation (section 7);
- the recipe is not changed by this CR.

## What changes

All paths are relative to the repository root.

### 1. The stage: `docs/demo-video/clips/radio-buttons/stage/plan.md`

Copied byte for byte from `work/storyboard/stage/plan.md` of this CR's folder (in the planning
surface,
`C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/2-backlog/P2/clip-radio-buttons/`,
or wherever the batch moved the folder), LF line endings, ending with one newline:

```markdown
# Plan: faster preview start

The preview takes two seconds to open on large files.

Approach:

- (x) Render the visible blocks first
- ( ) Cache the page between sessions
- ( ) Leave as is
```

Lines 7, 8 and 9 (one-based) are the three options; "Approach:" (line 5) is the paragraph just
above the list, so it labels the group (`radioGroups.ts`, `labelId`).

### 2. The live storyboard: `docs/demo-video/clips/radio-buttons/clip.md`

The draft `work/storyboard/clip.md` of this CR's folder, adapted only as follows; every row marked
*(on screen)* keeps its text, and the times follow the take:

- Front matter: `title: Feature clip radio-buttons`, `status: draft`, `date:` the day of the commit.
- Opening paragraph: worded as the merged `drag-list-item/clip.md` ("**This is the live
  storyboard.** The clip is built from this file: edit any row marked *(on screen)*, save, and run
  `just clip radio-buttons render`, then `check`. Rows marked *(filmed)* describe the footage of the
  take: changing them means a new take. `**bold**` in a text takes the orange accent."), then "The
  clip is one continuous shot: one click on an option of the radio group in the page on the left,
  then a zoom on the raw text on the right. It shows two texts in turn." Drop "draft for review",
  "Once approved, this file becomes ..." and "The times below are the Griller's proposal ...".
- `## Clip` table as drafted: `Length` `10.5 s` (or the take's value), `Size *(on screen)*`
  `1280x720 16:9`, `Frame rate *(on screen)*` `15 fps`, `Outputs` as drafted, `Cards` `none`,
  `Logo` `top right`, `Setting filmed` `none: every setting at its default`, `Filmed on` written as
  the drag clip does ("Windows, VS Code <version>, extension <version> VSIX built from the branch",
  the versions from `check.json`), `Stage` as drafted.
- The "Off camera (`setup`)" paragraph: removed from the committed file, as the merged drag clip has
  none (its content goes to the review notes, below).
- `## 1. Click an option`: the line "Pictures: ..." replaced by links to the key frames
  `frames/chosen.png` (and `frames/pointed.png`, section 3), each with an alt text saying what it
  shows; `Time` with the take's measured times; `Shot *(filmed)*` as drafted; `Text 1 *(on
  screen)*` = `Lists of ( ) and (x) become a **radio group**`.
- `## 2. Zoom on the raw text`: the line "Pictures: ..." replaced by links to `frames/04-mark-1.png`
  and `frames/05-mark-2.png`; `Time`, `Shot *(filmed)*` as drafted; `Zoom` = `raw, hold to 9.5 s`;
  `Mark 1 *(on screen)*` = `Orange outline around the new (x) of "Cache the page between sessions",
  5.0 to 6.6 s`; `Mark 2 *(on screen)*` = `Orange outline around the old option, now ( ), of "Render
  the visible blocks first", 6.6 to 8.2 s`; `Text 2 *(on screen)*` = `One click moves the **(x)**
  in the file`. (The draft writes the markers of the mark rows in backticks; keep them if
  `parseClip` reads the row unchanged, else drop the backticks and say so in "Autonomous
  decisions".)
- "Expected result" paragraph and its `markdown` block as drafted (the `aria-checked` sentence kept):
  the block is the scenario's `EXPECTED`, character for character.
- "Review notes": keep the draft's notes on reading mode, on the focus ring after a mouse click
  (with what the frames showed), on the loop seam and on what is not filmed; move the off-camera
  layout there in one note ("Opening the same file in the text editor beside Studio is done off
  camera"); replace the note on the missing kit `README` by nothing; add the measured times of the
  take (as the drag clip's "Measured by the trial take" note) and the key frame list with "Not
  checked by the author: motion, rhythm, the loop as watched."

### 3. The scenario: `docs/demo-video/clips/radio-buttons/scenario.mjs`

Modelled on `docs/demo-video/clips/drag-list-item/scenario.mjs` (copy its layout helpers: `step`,
the right-editor reading `RIGHT_EDITOR`, `editorLines`, `lineSpan`, the mode reading of `editMode`).
No Node import beyond built-ins; nothing runs at import, so the kit's tests can load it. The header
comment says what is filmed and that every caption and time is in `clip.md`.

- `stage = { "stage/plan.md": "plan.md" }`; `open = ["plan.md"]`; `settings = {}`.
- `checks = { editMode: "off", paste: false }`.
- `export const EXPECTED`: the text of section 2's "Expected result" block, joined with `\n`,
  ending with one newline (as `drag-list-item`).
- `setup(t)`, off camera, as `drag-list-item`'s `setup` (split right, `Ctrl+1`, "Reopen Editor
  With..." then "Markdown OKF-Schema Studio", one text editor beside Studio), except:
  - reading mode: when `data-sphinx-preview-edit-mode` is `"on"`, click
    `[data-sphinx-preview-edit-toggle]` until it is `"off"`; `t.record("readingMode", mode)`; throw
    when it is not `"off"`;
  - wait (at most 10 s) until the page shows exactly three `.myst-radio` controls in one
    `data-myst-radio-group`, with `aria-checked` `"true"`, `"false"`, `"false"` in the order of
    `data-myst-radio-line` 7, 8, 9; else throw with what was found;
  - park the pointer in the blank area below the list (`ul` box of `#sphinx-myst-preview-content`,
    as the drag clip parks it below its `ol`), `t.sleep(500)`.
- `run(t)`, timed with `until(seconds)` as `drag-list-item`:
  1. at 0.3 s, `t.moveTo` (0.6 s) to the centre of
     `#sphinx-myst-preview-content .myst-radio[data-myst-radio-line="8"]` (its
     `frame.locator(...).boundingBox()`, page coordinates); `t.keyFrame("pointed")` on arrival;
  2. at 1.3 s, `t.click()` (a real CDP click: the kit draws the ripple);
  3. poll, at most 2 s, until the page shows `aria-checked="true"` on line 8 and `"false"` on lines
     7 and 9 (re-read `t.frameOf()` between polls: the page may re-render), and the right editor's
     non-empty lines equal the non-empty lines of `EXPECTED` (`trimEnd`); `t.record("rawLines", …)`
     and `t.record("pageChoice", …)`; else throw with what the page and the raw text show (a
     failure here is a finding against the feature, not a scenario fix);
  4. at 3.4 s, `t.keyFrame("chosen")`;
  5. at 4.4 s, `t.zoom("raw", rect)`: the box of the right editor's non-empty lines 2 to 5
     ("Approach:" to "- ( ) Leave as is"), padded by 24 px, at most 2x (the kit caps it);
  6. at 5.0 s, `t.mark("1", air(lineSpan(page, 4, 2, 5)))` (the `(x)` of "Cache the page between
     sessions", non-empty line index 4, characters 2 to 5); at 6.6 s, `t.unmark("1")` and
     `t.mark("2", air(lineSpan(page, 3, 2, 5)))` (the `( )` of "Render the visible blocks first");
     at 8.2 s, `t.unmark("2")`; `air` pads as the drag clip does;
  7. at 9.5 s, `t.unzoom("raw")` and `t.moveTo(home.x, home.y, 0.6)`; `until(10.5)`. No click back
     (radio-Q8).
- `verify(t)`: `plan.md` on disk (`t.workspaceFile`, auto-save on), polled up to 3 s, equals
  `EXPECTED`; else throw with the text on disk. Returns `{ text }`.

### 4. Trial take, take and render

On Windows, on this machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`):

```bash
just dev
just package                                   # out/reports/package/markdown-okf-schema-studio.vsix
just clip radio-buttons doctor
just clip radio-buttons all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

When the workspace path shown anywhere in the frames holds the user name, run with
`CLIP_SCRATCH=C:/okfclip` (PowerShell: `$env:CLIP_SCRATCH = "C:/okfclip"`) as the export clip did.

- The trial take (recipe section 1, adapted): (a) the preview webview and the text editor are both
  in the frames; (b) the CDP click selects the option and the raw text changes (step 3 of `run`
  passes); (c) no focus ring on the clicked control in the frames after the click (it is drawn on
  `:focus-visible` only); if one shows, keep it as filmed and say so in the review notes and the PR;
  (d) the retimed rate is at least the storyboard's frame rate; (e) the loop seam SSIM in
  [0.98, 1.0).
- The trial's pictures and measured times go into `clip.md` (radio-Q3); `Length` and every time
  follow the take (playback rate inside 0.77 to 1.3), in the same commit as the render; the two
  captions stay end to end from 0 to `Length`, the marks inside the zoom hold.
- Commit together (recipe rule): `clip.md`, `scenario.mjs`, `stage/plan.md`, `radio-buttons.mp4`,
  `.webm`, `.gif` (Git LFS through `.gitattributes`), `poster.png`, `contact-sheet.png`,
  `first-last.png`, `frames/*.png`, `check.json`.

### 5. Tests (no kit code change)

Each reads the shipped files from the repository, path from the test file's own location, at the
head under test, never a copy. Run by `just clip-kit-test` inside `just check`:

- `docs/demo-video/clip-kit/lib/storyboard.test.mjs` gains "the shipped radio-buttons clip.md reads
  as the clip the owner reviews", modelled on the drag-list-item case: `parseClip` gives 1280x720,
  15 fps, the two captions (`**` aside) "Lists of ( ) and (x) become a radio group" and "One click
  moves the (x) in the file", end to end from 0 to `Length`; no badge; zoom `raw` with the committed
  hold; marks `1`, `2` in turn inside the hold with the committed times; the "Expected result"
  block equals the scenario's `EXPECTED`; `validateStory` passes with a `take` of no press, zoom
  `raw`, marks `1` and `2`, on `win32`.
- Same file: "the stage of the radio-buttons clip differs from the expected text by the moved x
  only": the shipped `stage/plan.md` and `EXPECTED` have the same lines except lines 7 and 8, where
  `(x)` and `( )` swap (the clip's claim "two characters on two lines", checked on the shipped
  files).
- `docs/demo-video/clip-kit/lib/check.test.mjs`: the test "the shipped scenarios declare their
  checks ..." gains `radio-buttons`: `resolveChecks` gives `{ editMode: "off", paste: false }` (its
  title names the radio clip too).
- `test/site/siteClips.test.ts`: "the shipped editing page plays the radio clip as video", modelled
  on "the shipped editing page plays the list drag clip as video": reads the shipped
  `docs/user/editing.md`, renders it with `renderMyst` and `clipVideos`, asserts
  `<video src="../demo-video/clips/radio-buttons/radio-buttons.webm"` and that
  `radio-buttons.webm`, `.gif` and `poster.png` exist; marker
  `// @tests_req SwRS-MDOKFSTUDIO-CORE-095` (an added test of an existing SwRS, no SwRS text
  change); then `just requirements-update`.

### 6. Docs

- `docs/user/editing.md`, the radio choice list paragraphs: after the paragraph that ends "On GitHub
  and in plain editors the `( )` and `(x)` text stays readable.", the image
  `![A plan asks to pick one of three options: a click on the second option selects it in the page, and in the raw Markdown beside the x moves from the first option to the second](../demo-video/clips/radio-buttons/radio-buttons.gif)`
  (the recipe, section 4: the GIF under the entry of the feature).
- No change to the recipe, the glossary, the writing skill, `README.md`, `CHANGELOG.md` or
  `docs/releases-notes/` (no `feat` or `fix` commit).

### 7. Commits and the pull request

- Commits by area (Conventional Commits; no scope on `docs` or `test`):
  `docs: add the radio choice feature clip` (clip folder, `docs/user/editing.md`),
  `test: check the radio clip's storyboard, stage and docs page` (the kit test cases,
  `siteClips.test.ts`, the files `just requirements-update` changes).
- The PR is opened as a draft (`gh pr create --draft`) and stays a draft until the owner approves
  the storyboard and the clip (radio-Q3); the agent does not mark it ready.
- The body follows `.github/PULL_REQUEST_TEMPLATE.md`, the PR guideline and the recipe's clip PR
  rule: the GIF inline from
  `https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/radio-buttons/radio-buttons.gif`,
  the MP4 and WebM linked in the same form at the same head; after each push of a new render the
  links move to the new head (`gh pr edit <n> --body-file <file>`); check that the GIF plays in the
  rendered PR page, else the recipe's `-assets` fallback.
- A section "Deviation from the feature clip process": the storyboard review moved from before the
  take into this PR (radio-Q3); the take filmed from the Griller's draft; an *(on screen)* row the
  owner changes is a render (`just clip radio-buttons render` then `check`), a *(filmed)* row a
  retake, a follow-up of this CR. It links `clip.md` for the review.
- What the clip proves (a real click on a radio option in a real VS Code window selects it at once
  and moves the `x` on two lines of the file: the take's `run` checks and `verify`) and what the
  owner judges (motion, rhythm, the loop as watched, the texts and their accent).
- "Autonomous decisions": the differences from the draft (section 2), the key frame names, the
  measured times, the focus ring as seen, `CLIP_SCRATCH` if used.

## Out of scope

- Any change to `src/`, to an SwRS text, to the writing skill or to the clip kit's code (beyond
  test cases); a change of the recipe.
- Numbered and nested groups, the keyboard (Space, Enter, arrows), the undo, the refusal while a
  block editor is open, edit mode (radio-Q6).
- A click back to the first option at the end (radio-Q8).
- A macOS or Linux take; placing the clip in release notes or the announcement (a release CR does
  it); a retake after the owner's review (a follow-up of this CR, radio-Q3); marking the PR ready
  before the owner approves.

## CI

No CI job changes. The new test cases run in `just check` through `just clip-kit-test`, inside the
existing `ci-static` job (Linux and Windows, `.github/workflows/ci.yml`); the site test runs where
`test/site/` tests run today.

- Environment: the CI machine set up by `just dev-ci` from the lock files, Node.js 24 from `.nvmrc`
  through `fnm`. Absent there and present locally: `ffmpeg`, the kit's scratch folder, the VS Code
  download, Remotion, a display. The new tests need none of them: the shipped `clip.md`,
  `scenario.mjs` (loaded, never run) and `stage/plan.md`, the shipped `docs/user/editing.md` and the
  clip's committed files (Git LFS checked out as CI does for the merged clips' site tests).
- Before the push: `just clip-kit-test`, `just check` and `just ci-static` on Windows.
- Only the first CI run proves the Linux leg (the dynamic `import` of the scenario from a
  repository path, the line comparison of the stage with LF endings).

No host and default matrix: the clip films every setting at its default, and the radio rendering
and choice do not depend on the host or on a configured value.

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows; the storyboard, stage and checks tests
   read the shipped `clip.md`, `stage/plan.md` and `scenario.mjs` at the head under test; the site
   test reads the shipped `docs/user/editing.md`.
2. The trial's five points (section 4), with what was seen for (a) and (c) (frame names).
3. `just clip radio-buttons all --vsix ...` passes; `check.json` shows `passed: true`, MP4 and WebM
   1280x720 at 15 fps, MP4 duration equal to `Length` within one frame, GIF at most 960 px and
   12 fps, loop seam SSIM in [0.98, 1.0), "Studio in reading mode at the start", no paste line,
   `verifyPassed: true`, playback rate inside 0.77 to 1.3, platform `win32`, extension source
   `vsix`.
4. The take's `run` passed step 3 (page `aria-checked` and raw lines as expected within 2 s) and
   `verify` found `plan.md` equal to `EXPECTED`.
5. The agent looks at the contact sheet and every key frame: Studio in reading mode on the left
   (no edit handles, no block outlines), the raw text on the right, three round controls with the
   first selected at frame 0 and the second after the click, the raw lines 7 and 8 swapped, Text 1
   during the click and Text 2 during the zoom, mark 1 on the new `(x)` and mark 2 on the old
   `( )`, no tooltip or hover at frame 0 and at the seam, no personal name or path, no dirty tab.
   What was not checked (motion, rhythm, the loop as watched) is said.
6. `just requirements-update` leaves the tree clean after its commit; `just preflight` passes (on
   Windows, its static stage).
7. The PR is a draft; its body plays the GIF, links the MP4 and WebM at the head sha and holds the
   "Deviation from the feature clip process" section.

## Open questions

None: `02-answers.md` (radio-Q1 to Q8) and the code on `origin/main` settle every point this
specification needs.
