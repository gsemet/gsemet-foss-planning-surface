# Feature clip: diff since the last commit, then side by side

Short name: `clip-diff`. No tracker issue (verbal request of the owner, 2026-11-25).

## Goal

The owner wants short clips of Studio's most interesting features, made with the feature clip kit and
recipe. This clip shows the review pair of the toolbar, in one continuous shot: a Markdown file with
uncommitted changes is open in Studio; the **Diff** button marks the blocks changed since the last
Git commit with a green bar; then the **Side-by-side** button turns each changed block into a card,
the block at the last commit on the left and as it is now on the right, with the changed words
marked.

The clip is made with the kit and the recipe **as the CR `short-demo-video-of-the-smart-raw-markdo`
(CR 484, in batch-09) leaves them**: a live Markdown storyboard `clip.md`, captions and marks read
from it, 1280x720 at 15 fps, combined badges, the PR rule that the review plays the clip. That CR is
not merged when this one starts: this change sits above it in the batch's stack (see "Branch and
PR"). Every reference below to "the kit" or "the recipe" means the files as CR 484 leaves them:
`docs/demo-video/clip-kit/` and `docs/demo-video/guidelines/feature-clip-process.guidelines.md`.

The kit as CR 484 leaves it cannot film this clip as is. Three small kit changes are part of this
CR (section 2): the scenario makes the Git history of its workspace before the window opens, key
frames for a clip with no key press, and the paste-widget line of `check` for a clip that pastes
nothing.

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| clip-diff-Q1 | Recipe and kit as CR 484 leaves them: live `clip.md`, stage, scenario, take, render to GIF, MP4 and WebM at 1280x720, 15 fps, PR whose review plays the clip; this CR depends on CR 484 (`depends.json`) | whole spec, "Branch and PR" |
| clip-diff-Q2 | One shot: a Markdown file of a throwaway Git stage folder, committed and then edited (a changed sentence, an added paragraph, a changed table cell); open in Studio, Diff on, then Side-by-side | sections 1, 3 |
| clip-diff-Q3 | Two captions in turn, in English: "Changed blocks, marked" during Diff, "Before and after, word by word" during Side-by-side; one mark may outline a changed word in the side-by-side view; no opening or end card | section 1 (storyboard) |
| clip-diff-Q4 | Filmed on Windows by the batch, a VSIX built at the take from the branch (no `src/` change, so `main`'s code), in the kit's throwaway `--extensions-dir` and profile; the owner reviews the storyboard and the clip in the PR; a retake after review is a follow-up, not a question now | section 4, open question 1 |
| clip-diff-Q5 | Files: `docs/demo-video/clips/diff-side-by-side/` and the docs the recipe says to link; no change to `src/`; the stage's Git history (a `git init` and two commits) is made by the scenario in a temporary folder, never inside the repository | sections 1 to 5 |
| clip-diff-Q6 | The PR body embeds the clip, links the MP4 and WebM (CR 484's rules), and states what the clip proves and what the owner judges (motion, rhythm) | "Branch and PR" |

## What changes

Paths are relative to the repository root. No change to `src/`, `test/`, `requirements/`,
`package.json` or the lock files; no new dependency.

### 1. The clip folder: `docs/demo-video/clips/diff-side-by-side/`

```text
docs/demo-video/clips/diff-side-by-side/
├── clip.md                              the live storyboard (below)
├── scenario.mjs                         stage, settings, prepareWorkspace, setup, run, verify
├── stage/
│   ├── release-checklist.md             the text now (uncommitted edits)
│   └── history/
│       ├── 1-release-checklist.md       the first commit
│       └── 2-release-checklist.md       the last commit (HEAD)
├── diff-side-by-side.mp4, .webm, .gif   outputs (Git LFS)
├── poster.png, contact-sheet.png, first-last.png, frames/*.png, check.json
```

#### The stage document

Three versions of one file. The history has two commits so the clip shows "since the **last**
commit": the paragraph added by the first-to-second commit is not marked, only what changed after
HEAD is.

`stage/history/1-release-checklist.md` (first commit, "Add the release checklist"):

```markdown
# Release checklist

Tag the release from `main` once the nightly build is green.

| Step | Owner |
| --- | --- |
| Build the package | CI |
| Sign the package | Release manager |
| Publish | Release manager |
```

`stage/history/2-release-checklist.md` (second commit, HEAD, "Add the release notes step"): the
first version plus, after the table, the paragraph
`Write the release notes before you publish, from the merged pull requests.`

`stage/release-checklist.md` (the text now, never committed):

```markdown
# Release checklist

Tag the release from `main` once the nightly build and the end-to-end tests are green.

| Step | Owner |
| --- | --- |
| Build the package | CI |
| Sign the package | Security team |
| Publish | Release manager |

Write the release notes before you publish, from the merged pull requests.

Announce the release in the team channel with a link to the notes.
```

Against HEAD: a changed sentence (the first paragraph), a changed table cell ("Release manager" to
"Security team" on the "Sign the package" row), an unchanged paragraph (the release notes line) and
an added paragraph (the announcement). Each file ends with one newline. If the cards do not fit in
the window (the `run` check of section 3 fails), shorten the texts, keeping the three kinds of
change and the unchanged paragraph, and update this storyboard in the same commit.

#### The storyboard: `clip.md`

Written in the format CR 484's recipe gives (section 2 of the recipe: front matter, `## Clip`
table, one `## <n>. <beat>` section per beat with its pictures and table, annotations *(on screen)*
and *(filmed)*, "Review notes"). The texts below are the decided ones (Q3), character for character;
the times are the proposal, and follow the batch's take in the same commit as the render (the
recipe's rule). The pictures are the kit's key frames (section 2.2).

```markdown
---
title: Feature clip diff-side-by-side
status: draft
date: <the day of the commit>
---

# Feature clip: diff-side-by-side

**This is the live storyboard.** The clip is built from this file: edit any row marked
*(on screen)*, save, and run `just clip diff-side-by-side render`, then `check`. Rows marked
*(filmed)* describe the take: changing them means a new take.

One continuous shot: Studio on a Markdown file with uncommitted changes; the Diff button marks the
changed blocks, then the Side-by-side button shows each as before and after. Two texts in turn.

## Clip

| Field | Content |
| --- | --- |
| Length | 9.6 s |
| Size *(on screen)* | 1280x720 16:9 |
| Frame rate *(on screen)* | 15 fps |
| Outputs | silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | `markdownOkfSchemaStudio.preview.showIncomingChanges`: on (the default) |
| Filmed on | Windows, VS Code <version of check.json>, extension <version> VSIX built from the branch |
| Stage | `stage/release-checklist.md` opened in Studio, in a Git folder the scenario makes: two commits from `stage/history/`, then the text now, not committed |

## 1. Diff: the changed blocks

![Diff on: a green bar beside the changed sentence, the table and the added paragraph](frames/01-first-click.png)

| Field | Content |
| --- | --- |
| Time | 0 to 4.4 s (pointer to the Diff button 0.3 to 1.1 s, click at 1.5 s, bars at once; pointer to the page margin; pointer to the Side-by-side button 3.2 to 4.0 s, click at 4.4 s) |
| Shot *(filmed)* | Studio in reading mode on `release-checklist.md`, the toolbar's four rows shown, Diff and Side-by-side off. The pointer clicks Diff in the toolbar's Review row: a green bar shows beside the changed first paragraph, the table and the added last paragraph; the release notes paragraph, unchanged since the last commit, has none. The pointer moves to Side-by-side and clicks. |
| Text 1 *(on screen)* | Changed blocks, marked |

## 2. Side by side: before and after

![Side-by-side on: three cards, Last commit on the left, Now on the right](frames/02-last-click.png)

![Zoom on the table card, mark 1 on the added words "Security team"](frames/04-mark-1.png)

| Field | Content |
| --- | --- |
| Time | 4.4 to 9.6 s (cards at once; zoom from 5.4 s, held to 8.6 s, then back to the start for the loop) |
| Shot *(filmed)* | Each changed block becomes a card: "Last commit" on the left, "Now" on the right, the removed words struck through and the added words underlined; the added paragraph has an empty left side. Zoom (at most 2x) on the table card. |
| Zoom | card, hold to 8.6 s |
| Mark 1 *(on screen)* | Orange outline around the added words "Security team" on the Now side, 6.2 to 7.8 s |
| Text 2 *(on screen)* | Before and after, word by word |

## Review notes

- The release notes paragraph was added by the last commit: it is not marked, which shows the
  comparison is with the last commit, not the first.
- The toolbar's own tooltip shows while the pointer is on a button it clicks ("Show changes since
  last commit", then "Show side-by-side changes since last commit"): it is Studio's look, filmed as
  is.
- With `preview.showIncomingChanges` off, neither button is offered. That case is not filmed.
- The raw screencast's frame rate (`rawFps` of `check.json`): <the batch's measured value>.
```

The captions carry no `**bold**`: Q3 gives the texts plain.

#### The scenario: `scenario.mjs`

In the style of the raw copy clip's scenario (header comment naming the scene; imports nothing, so a
test can load it without VS Code; every text, badge and time lives in `clip.md`).

- `stage = { "stage/release-checklist.md": "release-checklist.md" }`; `open = ["release-checklist.md"]`.
- `settings`: `"workbench.editorAssociations": { "release-checklist.md": "markdown-okf-schema-studio.editor" }`
  (Studio opens the file, as in the raw copy clip) and `"git.decorations.enabled": false` (the tab
  title is not coloured as modified). `markdownOkfSchemaStudio.preview.showIncomingChanges` is not set:
  the clip films the default.
- `export async function prepareWorkspace(w)` (the kit hook of section 2.1), with
  `export const HISTORY` listing the two commits so the test reads the same list:
  1. `await w.git(["init", "-b", "main"])`;
  2. local config: `user.name` `Studio Demo`, `user.email` `demo@example.invalid`,
     `core.autocrlf` `false`, `commit.gpgsign` `false` (the window's Git extension reads the same
     repository config; no personal name reaches Studio);
  3. `w.copy("stage/history/1-release-checklist.md", "release-checklist.md")`, `git add`,
     `git commit -m "Add the release checklist"` with the date `2026-11-02T09:00:00Z`;
  4. the same with `2-release-checklist.md`, "Add the release notes step", `2026-11-16T09:00:00Z`;
  5. `w.copy("stage/release-checklist.md", "release-checklist.md")`: the text now, not committed.
- `setup(t)`, off camera, leaves a known state whatever the previous take left in the profile (the
  toolbar, Diff and Side-by-side states are kept per workspace):
  - `t.frameOf()`, wait for the page;
  - reading mode: if `<html data-sphinx-preview-edit-mode>` is `on`, click
    `[data-sphinx-preview-edit-toggle]` and wait for `off` (as the raw copy scenario does);
    `t.record("readingMode", mode)`, throw unless `off` (Side-by-side is disabled in edit mode);
  - toolbar: if `<html data-sphinx-preview-toolbar-state>` is `collapsed`, click
    `[data-sphinx-preview-toolbar-collapse]` and wait for `expanded` (the Review row holds both
    buttons; the toolbar starts collapsed);
  - Side-by-side: if `<html data-sphinx-preview-sbs>` is `on`, click `[data-sphinx-preview-sbs-toggle]`
    and wait for `off`;
  - Git proof: if `<html data-sphinx-preview-incoming>` is `off`, click
    `[data-sphinx-preview-diff-toggle]`; wait up to 30 s for at least three
    `[data-sphinx-preview-changed]` blocks, clicking `[data-sphinx-preview-refresh]` once at 15 s if
    none; none: throw "no change marks: the Git extension did not open the stage repository";
  - then click `[data-sphinx-preview-diff-toggle]` and wait for `data-sphinx-preview-incoming` = `off`;
  - park the pointer at a rest point in the page's empty right margin, not over the toolbar, a
    green bar or a block (the clip starts and ends there).
- `run(t)`, the filmed action, on the `until(seconds)` schedule of the raw copy scenario, with the
  storyboard's proposed times (moves of 600 to 900 ms, 400 ms before a click, the recipe's pacing):
  - move to the Diff button (`t.rectOf(frame.locator("[data-sphinx-preview-diff-toggle]"))`, its
    centre), `t.click()`; wait up to 3 s for `data-sphinx-preview-incoming` = `on` and three
    `[data-sphinx-preview-changed]` blocks; `t.record("changedBlocks", n)`; throw unless 3;
  - move back to the rest point (no hover on a bar: its tooltip and its click open a single card);
  - move to the Side-by-side button, `t.click()`; wait up to 5 s for `data-sphinx-preview-sbs` =
    `on` and three `[data-okf-sbs-card]`; record their kinds in page order
    (`t.record("cards", [...])`) and throw unless `["changed", "changed", "added"]`;
  - record the text of `[data-okf-sbs-word="added"]` and `[data-okf-sbs-word="removed"]` spans; throw
    unless the added words contain "Security team" and "end-to-end", and the removed words contain
    "Release manager";
  - throw if a card's rectangle is not inside the preview frame's visible area or overlaps the
    toolbar `[data-sphinx-preview-toolbar]` ("the cards do not fit: shorten the stage");
  - move back to the rest point; `t.zoom("card", rect)` on the card that holds a `table`, padded by
    24 px; `t.mark("1", rect)` on the added word span(s) of the "Security team" cell of the Now side
    (`[data-okf-sbs-side="current"] [data-okf-sbs-word="added"]` inside that cell; the union rectangle
    when the words are split, a little air around it), then `t.unmark("1")`, `t.unzoom("card")`, end
    at the rest point.
- `verify(t)`: the feature never changes the file. Read `release-checklist.md` with
  `t.workspaceFile`; throw unless it equals the shipped `stage/release-checklist.md` (read from the
  clip folder). Return `{ changedBlocks, cards, addedWords, removedWords }` from the recorded notes.
  A difference is a finding against the feature (recipe, section 6), never "fixed" in the scenario.

### 2. The kit: `docs/demo-video/clip-kit/`

In the kit's style, every refusal message naming its source as today. Each change comes with a test
that fails on the kit as CR 484 leaves it (constitution, section 3).

#### 2.1 A Git history in the workspace: `prepareWorkspace`

- New file `lib/workspace.mjs`: `workspaceTools(ctx)` returns `w = { workspace, clipDir, git(args,
  { date } = {}), copy(from, to) }`.
  - `git` runs `git -C <workspace> ...args` synchronously and returns its stdout; its environment is
    `cleanEnv()` plus `GIT_CONFIG_NOSYSTEM=1` and `GIT_CONFIG_GLOBAL` pointing at an empty file the
    kit writes in the clip's scratch work folder (the maintainer's global config, hooks and
    templates never apply); `date` sets `GIT_AUTHOR_DATE` and `GIT_COMMITTER_DATE`. A failure throws
    with the git command and its stderr. `git` not found throws "git is not on PATH: a scenario
    with prepareWorkspace needs it".
  - `copy(from, to)` copies a clip-relative file over a workspace-relative one.
  - `prepareStage(ctx, scenario)`: when the scenario exports `prepareWorkspace`, first refuses a
    workspace inside a Git work tree (`git -C <workspace's parent folder> rev-parse
    --is-inside-work-tree` succeeds: "the clip workspace is inside a Git work tree; set CLIP_SCRATCH
    to a folder outside any repository"), then removes `<workspace>/.git`, then calls
    `await scenario.prepareWorkspace(workspaceTools(ctx))`. Without the export it does nothing.
- `lib/profile.mjs` (`setupProfile`) and `lib/take.mjs` (`runTake`) call `prepareStage` after their
  stage copy and before the window opens, so every take starts from the same history.
- `clip.mjs`, `doctor`: loads the scenario (as `setup` does); reports `git --version` as `ok`; git
  absent is `FAIL` when the scenario exports `prepareWorkspace` (fix: install Git, `scoop install
  git` on Windows), a `todo` line otherwise.

#### 2.2 Key frames of a clip with no key press

- Move the choice of the key frames out of `lib/encode.mjs` into a pure function
  `keyFrames(take, story)` in a new `lib/keyframes.mjs` (no ffmpeg, no file access), returning
  `[{ name, seconds }]` in output seconds; `encode.mjs` extracts each with ffmpeg as today, after
  emptying `frames/`.
- A take with key presses: the names and times CR 484 gives, unchanged (`01-selected`, `02-pasted`,
  `03-zoomed`, then `<NN>-mark-<id>` from 04).
- A take with no press and at least two clicks: `01-first-click` midway between the first click and
  the next click, `02-last-click` midway between the last click and the zoom's start (or the clip's
  end with no zoom), then `03-zoomed` and the marks as above. For this clip: `01-first-click.png`
  (bars shown), `02-last-click.png` (cards shown), `03-zoomed.png`, `04-mark-1.png`.
- A take with no press and fewer than two clicks is refused: "key frames need two key presses or two
  clicks in the take".

#### 2.3 The paste-widget line of `check`

`lib/check.mjs`'s "no paste-options widget after the paste" line: when the take logged no press with
the id `paste` and the scenario recorded no `pasteWidgets`, it passes and reads `n/a (the clip
pastes nothing)`; otherwise as today (a clip that pastes must record `pasteWidgets` = 0). The
decision is a pure exported function the test imports without ffmpeg (in `check.mjs` if its imports
allow it, else in `lib/keyframes.mjs`'s neighbour `lib/checklines.mjs`). The "reading mode at the
start" line is unchanged (this scenario records it).

#### 2.4 Tests, run by CR 484's `just clip-kit-test` (in `just check`)

`node:test` and `node:assert/strict`, Node built-ins only, beside the kit's files
(`docs/demo-video/clip-kit/lib/*.test.mjs`, the pattern CR 484's recipe runs):

- `storyboard.test.mjs` (CR 484's file) gains a case on the **shipped**
  `docs/demo-video/clips/diff-side-by-side/clip.md`, read from the repository at the head under
  test (path from the test file's location, never a copy), with `parseClip`: length equal to the
  committed value, size 1280x720, 15 fps, exactly two captions with the texts "Changed blocks,
  marked" and "Before and after, word by word" in that order, end to end from 0 to the length, no
  badge, zoom `card`, one mark `1` inside the hold, no expected paste; `validateStory` with a take
  of no press, zoom `card` and mark `1` passes for `win32` and `darwin`.
- New `workspace.test.mjs`: copies the shipped clip's stage as `setupProfile` does into a fresh
  `mkdtemp` folder under `os.tmpdir()` (outside the repository), runs `prepareStage` with the
  **shipped** `scenario.mjs`, and asserts: `git rev-list --count HEAD` is 2; `git show
  HEAD:release-checklist.md` equals the shipped `stage/history/2-release-checklist.md` and
  `HEAD~1:` the shipped `1-…`; the working file equals the shipped `stage/release-checklist.md`;
  `git status --porcelain` is exactly ` M release-checklist.md`; `git log --format=%an` gives only
  `Studio Demo`; a second run gives the same HEAD commit id (fixed dates, `.git` removed first).
  Refusal case, a prepared folder the shipped files cannot be: a workspace created inside a
  temporary `git init` folder is refused with the "inside a Git work tree" message. The test
  removes its temporary folders.
- New `keyframes.test.mjs`: the raw copy shape (two presses, one zoom, three marks) keeps CR 484's
  names; this clip's shape (no press, two clicks, zoom `card`, mark `1`) gives `01-first-click`,
  `02-last-click`, `03-zoomed`, `04-mark-1` at the midpoints above; no press and one click is
  refused; the paste-widget decision of 2.3 (no paste: passes with `n/a`; a paste with 0: passes;
  a paste with no record or 1: fails).
- `just check` and `just format`; if a size or unused-export script scans a new file and fails, fix
  the file, not the script.

### 3. The recipe: `docs/demo-video/guidelines/feature-clip-process.guidelines.md`

It names no process role and no CR (constitution, section 8): "the maintainer" and "the agent".

- "Where things live": `stage/` may also hold files the scenario commits (for example
  `stage/history/`).
- Section 1, `scenario.mjs`: add the optional export `prepareWorkspace(w)`: run after the stage copy
  and before the window opens, in `setup` and in every `take`, after the workspace's `.git` is
  removed; `w.git(args, { date })` runs Git in the workspace with no system or global config,
  `w.copy(from, to)` copies a stage file; the kit refuses a workspace inside a Git work tree, so a
  clip's history is never made in the repository. Use it for a feature that reads Git (fixed
  commit dates and a neutral author, so two takes film the same history).
- Section 1, `doctor`: `git`, required when the scenario exports `prepareWorkspace`.
- The key frames rule: a clip with no key press takes `01-first-click` and `02-last-click` from its
  first and last clicks; it needs two presses or two clicks.
- Section 6, `check`: the paste-widget line reads `n/a` for a clip that pastes nothing.

### 4. Take and render

On Windows, on the batch's machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`), Git on `PATH`:

```bash
just dev
just package          # out/reports/package/markdown-okf-schema-studio.vsix, from the branch
just clip diff-side-by-side doctor
just clip diff-side-by-side all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

- The take films section 1's shot. `verify` must pass and `run`'s checks must hold (three bars,
  cards `changed`, `changed`, `added`, the words). A failure is reported with what Studio showed
  (`failure.png`, the recorded notes), as a finding against the feature, and the clip waits.
- `Length` and every time in `clip.md` follow the take (playback rate inside 0.77 to 1.3), in the
  same commit as the render.
- Commit together (the recipe's rule): `clip.md`, `scenario.mjs`, `stage/`, the three outputs (Git
  LFS), `poster.png`, `contact-sheet.png`, `first-last.png`, `frames/*.png`, `check.json`.

### 5. The docs page

`docs/user/toolbar.md`: after the paragraph on the **Side-by-side** toggle, the clip's GIF (the
recipe's section 4):

`![The Diff button marks the blocks changed since the last commit with a green bar, then the Side-by-side button shows each as a card, the last commit on the left and now on the right, with the changed words marked](../demo-video/clips/diff-side-by-side/diff-side-by-side.gif)`

The site turns it into a video of the WebM (`SwRS-MDOKFSTUDIO-CORE-095`, unchanged). No change to
`README.md` (the recipe), `docs/releases-notes/`, `CHANGELOG.md` (no `feat` or `fix` commit) or the
writing skill (no rendered syntax changes).

## Branch and PR

- The branch sits on CR 484's branch in batch-09's stack
  (`.agents/guidelines/stacked-prs.guidelines.md`): the PR targets CR 484's branch until it merges,
  and is restacked by the agent that owns the stack.
- Commits by area, Conventional Commits (`.agents/guidelines/git-commit-message.guidelines.md`), no
  scope on `build` or `docs`:
  1. `build: let a clip make a Git history and film a clip with no key press` (sections 2.1 to 2.4);
  2. `docs: add the Git history and the click key frames to the feature clip process` (section 3);
  3. `docs: add the diff and side-by-side feature clip` (section 1, section 5, the outputs).
- The PR body follows `.github/PULL_REQUEST_TEMPLATE.md` and the PR guideline, with CR 484's rules
  (now in the recipe): Impacts shows the GIF inline from the file committed at the PR's head
  (`https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/diff-side-by-side/diff-side-by-side.gif`)
  and links the MP4 and WebM by the same form; each render pushed moves the links to the new head
  (`gh pr edit <n> --body-file <file>`); if GitHub does not play the GIF from the head, the three
  files go to the `-assets` side branch as the recipe says, and the body says so.
- The body states what the clip proves: on Windows, Studio marks exactly the three blocks changed
  since the last commit (not the one changed by the previous commit), Side-by-side shows three cards
  with the changed words marked, and the file is never changed (the take's checks and `verify`,
  `check.json`). It states what the owner judges: motion, rhythm, the loop as watched, the
  storyboard's texts and times. It says the storyboard is `status: draft`, for the owner's review in
  this PR (Q4).
- "Autonomous decisions" lists the choices this spec made where the answers are silent: the stage
  document and its two commit messages and dates; the file name `release-checklist.md`; the zoom on
  the table card (the kit refuses a mark without a zoom) and the mark on "Security team"; the
  proposed times and `Length`; `git.decorations.enabled` off; the toolbar tooltips filmed as they
  are; the kit's `prepareWorkspace` hook, the click key frames and the `n/a` paste line; the test
  files; the docs page and alt text.

## Out of scope

- Any change to the extension (`src/`), to an SwRS or to a test marker; the feature is filmed as it
  behaves.
- The single card opened by a click on a green bar, edit mode, the front matter field bars, the
  setting off: not filmed.
- A macOS or Linux take; a retake after the owner's review (a follow-up of this CR, Q4).
- Placing the clip in release notes, an announcement or the README.
- The other planned feature clips (their own CRs).

## CI

The only CI effect is that the new kit tests run in `just check` through CR 484's
`just clip-kit-test`, inside the existing `ci-static` job (Linux and Windows,
`.github/workflows/ci.yml`); no workflow file changes.

- Environment: a CI runner set up by `just dev-ci` from the lock files, Node.js 24 through `fnm`,
  Git present (the job checks the repository out with it). Absent there and present locally:
  `ffmpeg`, the kit's scratch folder, the VS Code download, Remotion, a display, the maintainer's
  global Git config. The tests need none of them: parsing committed files, a pure key frame
  function, and `git` in a temporary folder with no system or global config.
- Before the push: `just clip-kit-test` alone and `just check` pass on Windows; `just ci-static` on
  Windows; the outputs go in the evidence.
- Only the first CI run proves: the runners' Git version accepting `GIT_CONFIG_GLOBAL` pointing at
  an empty file and `git init -b`, the Linux temporary folder outside any work tree, and the
  Windows runner's line endings on the stage files (the test compares the files Git commits with
  the same files read back, so CRLF or LF does not matter, but this is not proved locally on Linux).

## Host and default matrix

The clip depends on the host (Windows filmed), on a shipped default (`preview.showIncomingChanges`,
on by default, not set by the scenario) and on Git (the built-in Git extension and `git` on `PATH`).

| Host | VS Code | showIncomingChanges | Git | Expected | Proof |
| --- | --- | --- | --- | --- | --- |
| Windows 11 | pinned `DEFAULT_CODE_VERSION` | on (default) | `git` on PATH, built-in Git extension, stage repository | three bars, then three cards (`changed`, `changed`, `added`) with the words marked; the file unchanged | the take's `run` checks, `verify`, `check.json` |
| macOS | same | on (default) | same | same | not proved (no macOS take) |
| Linux | same | on (default) | same | same | not proved |
| any | same | off | any | no Diff and no Side-by-side button | not filmed (documented in `docs/user/settings.md`) |
| any | same | on | file not in Git, or no Git | no bar, no card | not filmed |

The kit tests run on Windows locally and on Linux and Windows in `ci-static`.

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows. The storyboard and workspace tests read
   the shipped `clip.md`, `scenario.mjs` and `stage/` files at the head under test; the prepared
   texts are only the refusal cases named in 2.4.
2. `just clip diff-side-by-side doctor` passes, then `all --vsix …`: `check.json` shows `passed:
   true`, MP4 and WebM 1280x720 at 15 fps, the MP4 duration equal to `Length` within one frame, GIF
   at most 960 px and 12 fps, loop seam SSIM in [0.98, 1.0), `verifyPassed: true`, `readingMode:
   off`, the paste-widget line `n/a`, playback rate inside 0.77 to 1.3, platform `win32`, extension
   source `vsix`.
3. The agent looks at the contact sheet and every key frame: Text 1 during the bars and Text 2
   during the cards; bars beside the first paragraph, the table and the last paragraph, none beside
   the release notes line; three cards with "Last commit" and "Now"; the mark on "Security team"
   during the zoom; no card under the toolbar or the logo; no personal name or path; no dirty tab.
   The toolbar tooltips during a click are expected (Review notes). What was not checked (motion,
   rhythm, the loop as watched) is said.
4. The raw copy clip is not broken by the kit changes: `keyframes.test.mjs` keeps its frame names;
   if its take is still in the scratch folder, `just clip raw-copy-balance-edges render` then
   `check` pass; if not, the report says it was not performed.
5. `just preflight` passes (on Windows, its static stage).
6. The PR body plays the GIF and links the MP4 and WebM at the head sha (or on the `-assets` branch,
   said so).

## Open questions

1. The recipe as CR 484 leaves it ("The storyboard first") has the maintainer edit the storyboard
   draft, with a picture per key moment from a trial take, **before** the take; Q4 has the owner
   review the storyboard and the clip in the PR instead, after the take, with a retake as a
   follow-up. A project guideline ranks above an answer (`AGENTS.md`, "Instruction precedence"), so
   the conflict is reported: this specification follows Q4 (the storyboard above is the draft,
   written outside the repository before any branch, without trial pictures; the PR holds it as
   `status: draft`). Does the owner accept the review in the PR for this clip, or want the draft
   with trial pictures reviewed before the take?
