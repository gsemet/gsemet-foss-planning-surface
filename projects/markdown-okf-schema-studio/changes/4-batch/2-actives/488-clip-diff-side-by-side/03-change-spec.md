# Feature clip: diff since the last commit, then side by side

Short name: `clip-diff`. No tracker issue (verbal request of the owner, 2026-11-25).

## Goal

The owner asked for clips of Studio's most interesting features, one CR per clip (Q1). This clip
shows the review pair of the preview toolbar in one continuous shot: a Markdown file with
uncommitted changes is open in Studio; the **Diff** button marks the blocks changed since the last
Git commit with a green bar; then the **Side-by-side** button turns each changed block into a card,
the block at the last commit on the left and as it is now on the right, the removed words struck
through and the added words underlined. Two captions in turn, outlines in turn, 1280x720 at 15 fps,
MP4, WebM and GIF; the PR's body plays the clip and the owner reviews the storyboard and the clip
there (Q3).

The clip shows existing behaviour (CR 147 side-by-side, `src/page/modules/sideBySide.ts`,
`src/page/modules/incomingToggle.ts`, `src/core/mapping/wordDiff.ts`; `SwRS-MDOKFSTUDIO-REVIEW-008`,
`-009`, `-214`); no behaviour of the extension changes.

## Dependencies and base

`depends.json`: after `short-demo-video-of-the-smart-raw-markdo` (CR 484, short name
`raw-copy-demo`) and `clip-drag-list-item` (CR 485, short name `clip-drag`). Neither is merged when
this spec is written. "The kit" and "the recipe" below mean `docs/demo-video/clip-kit/` and
`docs/demo-video/guidelines/feature-clip-process.guidelines.md` as those two CRs leave them:

- from CR 484: the Markdown storyboard contract (`## Clip` table with `Length`, `Size`,
  `Frame rate`, `Outputs`, `Cards`, `Logo`, `Setting filmed`, `Filmed on`, `Stage`; one
  `## <n>. <beat>` section per beat with `Time`, `Shot *(filmed)*`, `Text <n> *(on screen)*`,
  `Zoom`, `Mark <id>`), captions in turn, marks in turn, size and frame rate from the storyboard,
  the mark key frames `frames/<NN>-mark-<id>.png`, `storyboard.test.mjs` run by
  `just clip-kit-test` in `just check`, and the clip PR rule (GIF inline from the PR's head, MP4 and
  WebM linked at the same head, the `-assets` fallback);
- from CR 485, section 5 of its spec: the scenario export `checks = { editMode, paste }` with
  `resolveChecks` and `takeLines` in `lib/check.mjs` (a clip with no paste has no paste line), and
  the helper `t.keyFrame(name)` with `keyFrameTimes` in `lib/encode.mjs` (a take with no key press
  renders; a key frame `frames/<name>.png` per logged name).

**This CR makes no kit change.** Everything it needs beyond those two CRs is in its own
`scenario.mjs` (the Git repository is made by `setup`, off camera, as the storyboard draft says).

- Base: the branch of CR 485 in batch-09's stack (`.agents/guidelines/stacked-prs.guidelines.md`;
  the PR targets that branch until it merges), else `origin/main` once both are merged (fetch first).
- Where CR 484 or CR 485 lands differently from its spec (a field name, a frame name, a test file
  name, a helper's signature), this CR follows what landed, and says so in the PR's "Autonomous
  decisions".

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| clip-diff-Q1 | Filed from the owner's request for 6 to 7 clips of the most interesting features; this clip is one of the seven, one CR per clip | Goal |
| clip-diff-Q2 | The captions, stage and timing are the Griller's storyboard draft (`work/storyboard/clip.md` and `work/storyboard/stage/` of this CR's folder): carried as the clip's shape, the owner reviews them at the storyboard gate | sections 1 to 3, "Where this spec differs from the draft" |
| clip-diff-Q3 | The owner's storyboard review moves to the PR: the batch films the trial take from the draft, puts its pictures in the storyboard, renders, opens the PR with the clip watchable; the PR stays a draft until the owner approves it; the deviation from the recipe's order is reported in this spec and in the PR body; a retake after review is a follow-up of this CR | "Deviation from the recipe", section 4, section 7 |

### Deviation from the recipe (reported, not asked)

The recipe as CR 484 leaves it ("The storyboard first") has the maintainer review and correct the
storyboard draft, with a picture per key moment from a trial take, **before** the take. Here the
take comes first and the owner's review happens on the PR, which stays a draft until the owner
approves the storyboard and the clip (Q3). The recipe is a project guideline and ranks above a
decision of the process (`AGENTS.md`, "Instruction precedence"): this deviation is the Chief of
Staff's decision under the owner's overnight autonomy, and the PR body says so in its own words
("the storyboard review the guideline places before the take is done on this pull request; it stays
a draft until the maintainer approves it").

## What changes

Paths are relative to the repository root. No change to `src/`, `requirements/` texts,
`package.json` or the lock files; no new dependency; no change under `docs/demo-video/clip-kit/`.

### 1. The stage: `docs/demo-video/clips/diff-side-by-side/stage/`

Copied from the draft, exactly (LF line endings, a final newline):

`stage/deploy-guide.committed.md` (the text of the last commit; never copied to the workspace):

```markdown
# Deploy guide

Deploy on Tuesday morning, after the nightly build is green.

1. Run the database migrations.
2. Restart the workers one at a time.
3. Watch the error rate for ten minutes.

Roll back by redeploying the previous tag.
```

`stage/deploy-guide.md` (the text now, saved, not committed):

```markdown
# Deploy guide

Deploy on Wednesday morning, after the nightly build and the smoke tests are green.

1. Run the database migrations.
2. Restart the workers two at a time.
3. Watch the error rate for thirty minutes.

Roll back by redeploying the previous tag.
```

Two changed blocks (the paragraph, the list); the heading and the last paragraph do not change.

### 2. The live storyboard: `docs/demo-video/clips/diff-side-by-side/clip.md`

The draft `work/storyboard/clip.md`, adapted only as listed in "Where this spec differs from the
draft"; every on-screen text, shot and mark of the draft stays. The file, before the take sets the
times and the pictures:

```markdown
---
title: Feature clip diff-side-by-side
status: draft
date: <the day of the commit>
---

# Feature clip: diff-side-by-side

**This is the live storyboard.** The clip is built from this file: edit any row marked
*(on screen)* (the text is the clip's exact text; `**bold**` takes the orange accent), save, and run
`just clip diff-side-by-side render`, then `check`. Rows marked *(filmed)* describe the take:
changing them means a new take. The maintainer reviews this storyboard and the clip in the pull
request that adds them.

One continuous shot: the two toolbar clicks, then a zoom on one diff card. Two texts in turn.

## Clip

| Field | Content |
| --- | --- |
| Length | 11.0 s |
| Size *(on screen)* | 1280x720 16:9 |
| Frame rate *(on screen)* | 15 fps |
| Outputs | silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | none (defaults: `markdownOkfSchemaStudio.preview.showIncomingChanges` on) |
| Filmed on | Windows, VS Code <version in check.json>, extension <version> VSIX built from the branch |
| Stage | `stage/deploy-guide.md` (Studio, the whole window, reading mode), in a workspace that is a Git repository whose last commit holds `stage/deploy-guide.committed.md` as `deploy-guide.md` |

Stage, what changes since the commit (two blocks; the heading and the last paragraph do not change):

- Paragraph: "Tuesday" becomes "Wednesday", and "and the smoke tests" is added after "nightly build"
  ("is green" becomes "are green").
- Ordered list: "one at a time" becomes "two at a time" (item 2), "ten minutes" becomes "thirty
  minutes" (item 3).

Off camera (`setup`): the Git repository and its one commit, the working copy left uncommitted;
the toolbar expanded (a new workspace starts collapsed), reading mode, Side-by-side off, the Diff
button switched off so the green bars are hidden at frame 0.

## 1. Diff marks the changed blocks

![Diff on: a green bar left of the paragraph and of the list](frames/diff-on.png)

![Mark 1 around the two green bars](frames/04-mark-1.png)

| Field | Content |
| --- | --- |
| Time | 0 to 3.4 s (click Diff at 1.2 s, the green bars at 1.4 s) |
| Shot *(filmed)* | Studio in reading mode on `deploy-guide.md`, the toolbar open top right. The pointer moves to the Diff button of row 4 ("Show changes since last commit") and clicks. A green bar appears left of the paragraph and of the list; the heading and the last paragraph get none. |
| Text 1 *(on screen)* | Diff marks every block **changed** since the last commit |
| Mark 1 *(on screen)* | Orange outline around the two green bars, 1.8 to 3.2 s |

## 2. Side-by-side, then zoom on a card

![Side-by-side on: the paragraph and the list each a card, last commit left, now right](frames/side-by-side.png)

![Zoom on the paragraph's card, mark 2 on the struck "Tuesday"](frames/05-mark-2.png)

![Mark 3 on the underlined "Wednesday"](frames/06-mark-3.png)

![Mark 4 on the underlined "and the smoke tests are"](frames/07-mark-4.png)

| Field | Content |
| --- | --- |
| Time | 3.4 to 11.0 s (click Side-by-side at 3.4 s, zoom from 4.6 s, held to 10.0 s, then back to the start for the loop) |
| Shot *(filmed)* | The pointer moves one button left, to Side-by-side ("Show side-by-side changes since last commit"), and clicks. The paragraph and the list each become a card: the block at the last commit on the left, as it is now on the right. Zoom (at most 2x) on the paragraph's card. |
| Zoom | card, hold to 10.0 s |
| Mark 2 *(on screen)* | Orange outline around the struck "Tuesday" (left), 5.4 to 6.8 s |
| Mark 3 *(on screen)* | Orange outline around the underlined "Wednesday" (right), 6.8 to 8.2 s |
| Mark 4 *(on screen)* | Orange outline around the underlined "and the smoke tests are" (right), 8.2 to 9.6 s |
| Text 2 *(on screen)* | Side-by-side shows **before and after**, word by word |

Expected result, the scenario's check (visible state, read from the preview; the file is never
changed):

- Two diff cards, no more: the paragraph and the list.
- Paragraph card: "Tuesday" and "is" struck on the left; "Wednesday" and "and the smoke tests are"
  underlined on the right (consecutive changed words form one marked range).
- List card: "one" and "ten" struck on the left; "two" and "thirty" underlined on the right.
- `deploy-guide.md` on disk is byte for byte `stage/deploy-guide.md`, and `git status` shows it
  modified only.

## Review notes

- The kit has no Git step: the scenario's `setup` makes the repository and the commit off camera
  (Git on `PATH`, a neutral `user.name` and `user.email` set in the repository only, so no personal
  name shows).
- The green bars need a trusted workspace and a file known to Git: the kit's profile turns workspace
  trust off, so the workspace counts as trusted.
- The Diff and Side-by-side choices are kept per workspace: `setup` switches both off after the
  page opens, so frame 0 has no bars and no cards. The toolbar tooltips slide in on hover: the
  pointer leaves the buttons before the zoom.
- The clip ends with the cards shown and starts without them: the kit's last frames cross-fade to
  frame 0 for the loop.
- Mark 1 is shown before the zoom; the other marks during it.
- The raw screencast's frame rate (`rawFps` in `check.json`): <the batch's measured value>.
```

The `Time` rows, the mark and zoom times and `Length` follow the batch's take in the same commit as
the render (playback rate inside 0.77 to 1.3; the two captions end to end from 0 to `Length`; every
mark ends at or before the zoom hold's end, CR 484's rule). The pictures are the kit's key frames of
the batch's take (section 3's `t.keyFrame` names and CR 484's mark frames): without a zoom before
4.6 s, the zoom frame `03-zoomed.png` is also written; it is not linked.

### 3. The scenario: `docs/demo-video/clips/diff-side-by-side/scenario.mjs`

In the style of `clips/raw-copy-balance-edges/scenario.mjs`: a header comment saying what is filmed
and that every text and time is in `clip.md`; it imports only Node built-ins (`node:child_process`,
`node:fs`, `node:path`, `node:url`), so a test can load it without VS Code. Selectors and attributes
are Studio's own (`src/core/preview/previewToolbar.ts`, `src/page/modules/incomingToggle.ts`,
`src/page/modules/sideBySide.ts`, `src/page/modules/toolbarCollapse.ts`).

- `stage = { "stage/deploy-guide.md": "deploy-guide.md" }`; `open = ["deploy-guide.md"]`.
- `settings = { "workbench.editorAssociations": { "deploy-guide.md": "markdown-okf-schema-studio.editor" },
  "git.decorations.enabled": false }`: Studio opens the file in the whole window, as the raw copy
  clip's association does; the tab title is not coloured as modified.
  `markdownOkfSchemaStudio.preview.showIncomingChanges` is not set: the clip films the default.
- `checks = { editMode: "off", paste: false }` (CR 485's export): reading mode at the start, no
  paste line.
- `COMMITTED` is read from `new URL("stage/deploy-guide.committed.md", import.meta.url)` and `NOW`
  from `stage/deploy-guide.md` the same way; both exported for the test.
- `export function makeRepository(workspace)`: off camera, idempotent, never deletes anything:
  - `git(args, input)`: `execFileSync("git", ["-C", workspace, ...args], { input, encoding: "utf8" })`
    with the environment plus `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL` pointing at an empty
    file the function writes beside the workspace (`join(workspace, "..", "gitconfig-empty")`, the
    kit's scratch work folder, outside the workspace), and fixed `GIT_AUTHOR_DATE` and
    `GIT_COMMITTER_DATE` (`2026-11-16T09:00:00Z`): the maintainer's global config, hooks and
    templates never apply, and two takes make the same commit. Git not found throws "git is not on
    PATH: this clip makes a Git repository".
  - When `<workspace>/.git` is absent: refuse a workspace inside another work tree (`git -C
    <workspace> rev-parse --is-inside-work-tree` succeeds before the init: "the clip workspace is
    inside a Git work tree; set CLIP_SCRATCH outside any repository"); `git init -b main`; local
    config `user.name` `Studio Demo`, `user.email` `demo@example.invalid`, `core.autocrlf` `false`,
    `commit.gpgsign` `false`; commit `COMMITTED` as `deploy-guide.md` without touching the working
    file: `git hash-object -w --stdin` (input `COMMITTED`), `git update-index --add --cacheinfo
    100644,<sha>,deploy-guide.md`, `git commit -m "Add the deploy guide"`.
  - When `.git` is present (a later `take`: the kit re-copies the stage but keeps the workspace):
    keep it when `git show HEAD:deploy-guide.md` equals `COMMITTED` and `git rev-list --count HEAD`
    is 1; else throw "the workspace holds another repository: run `just clip diff-side-by-side
    setup` again". (Deleting `.git` while the window's Git extension watches it can fail on
    Windows; `setup` of the kit rebuilds the workspace from nothing.)
  - Returns the HEAD commit id.
- `setup(t)`, off camera, leaving a known state whatever the previous take left (the toolbar, Diff
  and Side-by-side choices are kept per workspace):
  1. `makeRepository(t.workspace)`; `t.record("headCommit", id)`;
  2. `t.frameOf()`; reading mode as the raw copy scenario does: if `<html
     data-sphinx-preview-edit-mode>` is `on`, click `[data-sphinx-preview-edit-toggle]`, wait for
     `off`; `t.record("readingMode", mode)`; throw unless `off` (Side-by-side is disabled in edit
     mode);
  3. toolbar: if `<html data-sphinx-preview-toolbar-state>` is `collapsed`, click
     `[data-sphinx-preview-toolbar-collapse]` and wait for `expanded` (row 4 holds both buttons);
  4. Side-by-side: if `<html data-sphinx-preview-sbs>` is `on`, click
     `[data-sphinx-preview-sbs-toggle]` and wait for `off`;
  5. Git proof: if `<html data-sphinx-preview-incoming>` is `off`, click
     `[data-sphinx-preview-diff-toggle]`; wait up to 30 s for exactly two
     `[data-sphinx-preview-changed]` blocks, clicking `[data-sphinx-preview-refresh]` every 5 s
     while there are none (the window's Git extension finds a repository made after the window
     opened only after a few seconds, and Studio reads `HEAD` again on a render); none: throw "no
     change marks: the Git extension did not open the stage repository";
  6. click `[data-sphinx-preview-diff-toggle]` and wait for `data-sphinx-preview-incoming` = `off`;
  7. park the pointer at a rest point in the page's blank area right of the text, off the toolbar,
     every block and every bar, `t.moveTo(x, y, 0.1)`, `t.sleep(500)`: frame 0 and the last frame
     show no hover.
- `run(t)`, the filmed action, on the `until(seconds)` schedule of the raw copy scenario with the
  storyboard's times (moves of 600 to 900 ms, 400 ms before a click):
  1. move to the centre of `[data-sphinx-preview-diff-toggle]` (`t.rectOf(frame.locator(...))`),
     `t.click()` at 1.2 s; wait at most 2 s for `data-sphinx-preview-incoming` = `on` and two
     `[data-sphinx-preview-changed]` blocks, the paragraph and the `ol` (the heading and the last
     paragraph unmarked); else throw with what the page shows (a finding against the feature, never
     a scenario fix); `t.record("changedBlocks", 2)`;
  2. move off the button, toward the rest point, without crossing a bar (a bar's tooltip shows on
     hover and its click opens a single card); `t.keyFrame("diff-on")`;
  3. at 1.8 s, `t.mark("1", rect)`: the union of the two bars' rectangles (`[data-sphinx-preview-change-layer]
     > span`, page coordinates), with 6 px and 3 px of air as in the raw copy scenario; at 3.2 s,
     `t.unmark("1")`;
  4. move to `[data-sphinx-preview-sbs-toggle]` (one button left of Diff), `t.click()` at 3.4 s;
     wait at most 5 s for `data-sphinx-preview-sbs` = `on` and exactly two `[data-okf-sbs-card="changed"]`
     (no `added` or `removed` card); then read, per card, the texts of its
     `[data-okf-sbs-side="base"] [data-okf-sbs-word="removed"]` and
     `[data-okf-sbs-side="current"] [data-okf-sbs-word="added"]` spans, spaces normalised; throw
     unless the paragraph card gives removed `["Tuesday", "is"]` and added
     `["Wednesday", "and the smoke tests are"]`, and the list card removed `["one", "ten"]` and added
     `["two", "thirty"]`; `t.record("cards", ...)` with those lists;
  5. move back to the rest point; `t.keyFrame("side-by-side")`;
  6. at 4.6 s, `t.zoom("card", rect)`: the paragraph's card, padded by 24 px;
  7. `t.mark("2", ...)` on "Tuesday" (left) 5.4 to 6.8 s, `t.mark("3", ...)` on "Wednesday" (right)
     6.8 to 8.2 s, `t.mark("4", ...)` on "and the smoke tests are" (right) 8.2 to 9.6 s, each the
     span's rectangle with the same air, each followed by its `t.unmark`;
  8. at 10.0 s, `t.unzoom("card")`, `t.moveTo(home.x, home.y, 0.6)`; `until(11.0)`.
- `verify(t)`: the feature never changes the file. Throw unless `t.workspaceFile("deploy-guide.md")`
  equals `NOW`, and unless `git status --porcelain` (same environment) is exactly
  ` M deploy-guide.md`. Return `{ headCommit, changedBlocks, cards }` from the recorded notes.

### 4. Take and render

On Windows, on the batch's machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`), Git on `PATH`:

```bash
just dev
just package                                   # out/reports/package/markdown-okf-schema-studio.vsix
just clip diff-side-by-side doctor
just clip diff-side-by-side all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

- The take is the trial take of Q3 (recipe section 1's trial, adapted): (a) the preview webview is
  in the frames; (b) the clicks on the two toolbar buttons reach the page (steps 1 and 4 of `run`
  pass); (c) the bars and the cards show what the storyboard says (same steps); (d) the retimed rate
  is at least the storyboard's frame rate. A failure of (b) or (c) stops the work and is reported
  with `failure.png` and the recorded notes: never a scripted toggle, an OS-level input or capture.
- The take's pictures go in the storyboard (Q3) and its times replace the draft's (section 2).
- Commit together (the recipe's rule): `clip.md`, `scenario.mjs`, `stage/`, `diff-side-by-side.mp4`,
  `.webm`, `.gif` (Git LFS through `.gitattributes`), `poster.png`, `contact-sheet.png`,
  `first-last.png`, `frames/*.png`, `check.json`.

### 5. Tests

`node:test` and `node:assert/strict`, Node built-ins only, run by `just clip-kit-test` in
`just check` (the files CR 484 and CR 485 create):

- `storyboard.test.mjs` gains a case reading the **shipped**
  `docs/demo-video/clips/diff-side-by-side/clip.md` from the repository (path from the test file's
  location, at the head under test, never a copy) with `parseClip`: size 1280x720, 15 fps, exactly
  two captions with the draft's texts ("Diff marks every block **changed** since the last commit",
  "Side-by-side shows **before and after**, word by word", with or without the `**` as CR 484's
  parser returns them) in that order, end to end from 0 to `Length`; no badge; zoom `card`; marks
  `1` to `4` in turn, none ending after the hold; no expected paste; and `validateStory` passes
  with a take of no press, zoom `card` and marks `1` to `4`, on `win32`.
- CR 485's test that resolves the `checks` of each shipped scenario gains `diff-side-by-side`:
  `{ editMode: "off", paste: false }`.
- A new case (in the kit's test folder, file name in the kit's test style, for example
  `scenarioRepository.test.mjs`) on the **shipped** `scenario.mjs`: in a fresh `mkdtemp` folder
  under `os.tmpdir()` (outside the repository) with a `workspace` subfolder holding a copy of the
  shipped `stage/deploy-guide.md`, `makeRepository` gives: `git rev-list --count HEAD` 1;
  `git show HEAD:deploy-guide.md` equal to the shipped `deploy-guide.committed.md`; the working
  file still equal to the shipped `deploy-guide.md`; `git status --porcelain` exactly
  ` M deploy-guide.md`; `git log --format=%an` only `Studio Demo`; a second call keeps the same
  commit id. Refusal cases, prepared folders the shipped files cannot be: a workspace inside a
  temporary `git init` folder is refused ("inside a Git work tree"); a workspace whose repository
  has another `HEAD` text is refused ("another repository"). The test removes its folders.
- `test/site/siteClips.test.ts`: a test "the shipped toolbar page plays the diff clip as video",
  modelled on the settings page one (and CR 485's editing page one): it reads the shipped
  `docs/user/toolbar.md`, renders it as the existing tests do, asserts
  `<video src="../demo-video/clips/diff-side-by-side/diff-side-by-side.webm"` and that
  `diff-side-by-side.webm`, `.gif` and `poster.png` exist; marker
  `// @tests_req SwRS-MDOKFSTUDIO-CORE-095` (an added test of an existing SwRS, no SwRS text
  change); then `just requirements-update`.
- `just check` and `just format`; if a size or unused-export script scans a new file and fails, fix
  the file, not the script.

### 6. Docs

- `docs/user/toolbar.md`: after the paragraph on the **Side-by-side** toggle, the image
  `![The Diff button marks the blocks changed since the last commit with a green bar, then the Side-by-side button shows each as a card, the last commit on the left and now on the right, with the removed words struck and the added words underlined](../demo-video/clips/diff-side-by-side/diff-side-by-side.gif)`
  (the recipe's section 4: under the feature's entry).
- The recipe: no change (CR 484 and CR 485 already describe everything this clip uses; the Git
  repository is a scenario's own `setup` work).
- No change to `README.md` (the recipe keeps it), `CHANGELOG.md`, `docs/releases-notes/` (no `feat`
  or `fix` commit), the glossary or the writing skill (no rendered syntax changes).

### 7. Commits and the pull request

- Commits by area (Conventional Commits, `.agents/guidelines/git-commit-message.guidelines.md`; no
  scope on `docs` or `test`):
  1. `docs: add the diff and side-by-side feature clip` (clip folder, `docs/user/toolbar.md`, the
     kit test cases on the shipped clip files);
  2. `test: play the diff clip on the toolbar page of the docs site` (`siteClips.test.ts`, the
     requirements files `just requirements-update` changes).
- The PR is opened as a **draft** and stays one until the owner approves the storyboard and the clip
  (Q3); it is linked into batch-09's stack above CR 485.
- The body follows `.github/PULL_REQUEST_TEMPLATE.md`, the PR guideline and the recipe's clip PR
  rule: the GIF inline from
  `https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/diff-side-by-side/diff-side-by-side.gif`,
  the MP4 and WebM linked with the same form at the same head; after each push of a new render the
  links move to the new head (`gh pr edit <n> --body-file <file>`); if GitHub does not play the GIF
  from the head, the three files go to the `-assets` side branch and the body says so.
- The body states what the clip proves (in a real VS Code window on Windows, Diff marks exactly the
  two blocks changed since the last commit; Side-by-side shows two cards with the words of section 2
  marked; the file is never changed: the take's checks and `verify`, `check.json`) and what the owner
  judges (motion, rhythm, the loop as watched, the texts and their accent, the times); it links
  `clip.md` for the storyboard review, reports the deviation from the recipe's order (see above),
  and says a retake after review is a follow-up of this CR.
- "Autonomous decisions": the differences from the draft listed below; `git.decorations.enabled`
  off; the repository made without touching the working file and kept across takes; the key frame
  names `diff-on` and `side-by-side`; the test cases and the site test; the docs page and alt text.

## Where this spec differs from the draft

The draft `work/storyboard/clip.md` and its `stage/` are the clip's approved shape (Q2). This spec
changes only:

1. **`Format` split** into `Size`, `Frame rate` and `Outputs`, the fields CR 484's parser reads; the
   values are the draft's.
2. **`status: draft`** and an opening paragraph about the live file and the review in the PR (Q3),
   instead of "draft for the owner's review ... Once approved, this file becomes ...".
3. **Mark 4 and the expected words**: the draft expects "and the smoke tests" and "are" as two
   marks. Studio marks consecutive changed words as one range (`rangesOf` in
   `src/core/mapping/wordDiff.ts`: "consecutive changed words form one range"), so the right side
   shows one underlined range "and the smoke tests are". Mark 4 outlines that range and the expected
   result lists it as one; the draft's own review note foresaw this ("a finding to read, not a
   scenario fix"): it is read here from the code, not a change of behaviour.
4. **A `Zoom` row** (`card, hold to 10.0 s`) in section 2, the field CR 484's parser reads, from the
   draft's own Time row.
5. **Pictures**: the draft's "Pictures: from the batch's trial take" become the kit's key frames
   (`frames/diff-on.png`, `frames/side-by-side.png`, `frames/04-mark-1.png` to `07-mark-4.png`).
6. **The Git step**: the draft's `setup` makes the repository; here it does so idempotently across
   takes (kept when it holds the right commit, never deleted with the window open), commits without
   touching the working file, and refreshes the page until the bars show. The draft's
   "check it in the trial" note on trust becomes a statement (the kit turns trust off).
7. **Loop seam**: the draft's fallback (clicking Side-by-side and Diff off at the end if the SSIM
   check refuses) is dropped: the kit's last frames cross-fade toward frame 0
   (`remotion/src/Clip.tsx`, `SEAM`), which is how the raw copy clip, ending on a different picture,
   passes. If `check` still refuses the seam, the batch reports it rather than adding filmed steps.

Mark 1 stays as the draft has it, before the zoom (1.8 to 3.2 s): CR 484's parser refuses a mark
only when the clip has no zoom, when marks overlap, or when a mark ends after the hold. If the kit
draws it wrongly outside the zoom (the `04-mark-1.png` frame shows it), the batch reports it as a
kit finding; the storyboard is not changed to hide it.

## Out of scope

- Any change to the extension (`src/`), to an SwRS text or to the kit.
- The single card opened by a click on a bar, edit mode, the front matter bars, the setting off: not
  filmed.
- A macOS or Linux take; a retake after the owner's review (a follow-up of this CR, Q3); placing the
  clip in release notes, an announcement or the README; the other planned clips.

## CI

No CI job changes. The new test cases run in `just check` through `just clip-kit-test`, inside the
existing `ci-static` job (Linux and Windows, `.github/workflows/ci.yml`); the site test runs where
`test/site/` tests run today.

- Environment: a runner set up by `just dev-ci` from the lock files, Node.js 24 through `fnm`, Git
  present (the job checks the repository out with it), Git LFS files checked out as for the raw copy
  clip's site test. Absent there and present locally: `ffmpeg`, the kit's scratch folder, the VS Code
  download, Remotion, a display, the maintainer's global Git config. The tests need none of them:
  committed files read from the repository and `git` in a temporary folder with no system or global
  config.
- Before the push: `just clip-kit-test`, `just check` and `just ci-static` on Windows.
- Only the first CI run proves: the runners' Git accepting `GIT_CONFIG_GLOBAL` at an empty file and
  `git init -b`; the Linux temporary folder outside any work tree; the Windows runner's line endings
  on the stage files (the test commits and compares the same files read back, so CRLF or LF does not
  change the outcome, but it is not proved locally on Linux).

## Host and default matrix

The clip films a shipped default (`preview.showIncomingChanges` on, not set by the scenario) and
depends on Git (the built-in Git extension, `git` on `PATH`) and on the host (Windows filmed).

| Host | VS Code | showIncomingChanges | Git | Expected | Proof |
| --- | --- | --- | --- | --- | --- |
| Windows 11 | pinned `DEFAULT_CODE_VERSION` | on (default) | `git` on PATH, built-in Git extension, the stage repository | two bars, then two `changed` cards with the words of section 2; the file unchanged | the take's `run` checks, `verify`, `check.json` |
| macOS | same | on (default) | same | same | not proved (no macOS take) |
| Linux | same | on (default) | same | same | not proved |
| any | same | off | any | no Diff and no Side-by-side button | not filmed (`docs/user/settings.md`) |
| any | same | on | file not in Git | no bar, no card | not filmed |

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows; the storyboard, `checks` and repository
   cases read the shipped `clip.md`, `scenario.mjs` and `stage/` files at the head under test; the
   prepared folders are only the refusal cases named in section 5. The site test reads the shipped
   `docs/user/toolbar.md`.
2. `just clip diff-side-by-side doctor` passes, then `all --vsix …`: `check.json` shows `passed:
   true`, MP4 and WebM 1280x720 at 15 fps, the MP4 duration equal to `Length` within one frame, GIF
   at most 960 px and 12 fps, loop seam SSIM in [0.98, 1.0), "Studio in reading mode at the start",
   no paste line, `verifyPassed: true`, playback rate inside 0.77 to 1.3, platform `win32`, extension
   source `vsix`.
3. The agent looks at the contact sheet and every key frame: Text 1 during the bars and Text 2 during
   the cards; bars left of the paragraph and the list only; mark 1 around both bars; two cards with
   "Last commit" and "Now"; marks 2 to 4 on their words during the zoom; no card under the toolbar
   or the logo; no tooltip during the zoom; no personal name or path; no dirty or coloured tab. What
   was not checked (motion, rhythm, the loop as watched) is said.
4. `just requirements-update` leaves the tree clean after its commit; `just preflight` passes (on
   Windows, its static stage).
5. The draft PR body plays the GIF and links the MP4 and WebM at the head sha (or on the `-assets`
   branch, said so), and reports the deviation from the recipe's order.

## Open questions

None: `02-answers.md`, the draft storyboard and the code settle every point this specification
needs.
