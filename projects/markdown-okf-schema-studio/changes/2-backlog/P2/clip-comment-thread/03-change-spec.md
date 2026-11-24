# Feature clip: a comment thread on a passage

Short name: `clip-comment`. No tracker issue (verbal request of the owner, 2026-11-25).

## Goal

Studio's next feature clip, made with the clip kit and the feature clip recipe exactly as the CR
`short-demo-video-of-the-smart-raw-markdo` (short name `raw-copy-demo`) leaves them: in the
preview, a sentence is selected and commented; the passage is highlighted, its thread opens, gets a
reply and is resolved. One continuous shot, 5 to 12 seconds, looping, silent, two captions in turn,
rendered to MP4, WebM and GIF at 1280x720 and 15 fps, and a pull request whose review plays the
clip.

This CR comes after `raw-copy-demo` (`depends.json`). Everything below names the kit and the recipe
as that CR's `03-change-spec.md` specifies them (planning surface,
`changes/2-backlog/P1/short-demo-video-of-the-smart-raw-markdo/03-change-spec.md`, or wherever the
batch moved that folder): the Markdown storyboard `clip.md` with `## Clip` and one `## <n>. <beat>`
section per beat, `Text <n>` captions in turn, `Size` and `Frame rate` fields, combined key badges
`Ctrl+… / ⌘…`, zero or more `Mark <id>` rows, the parser tests in `just check`, and the PR rule of
its Q42. Where the kit or the recipe merged by that CR differs from its spec, the merged files win.

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| Q1 | The kit and the recipe as `raw-copy-demo` leaves them: a live Markdown storyboard `clip.md`, a stage document, a scenario, a take, a render to GIF, MP4 and WebM at 1280x720, 15 fps, a PR whose review plays the clip; this CR depends on `raw-copy-demo` | whole spec, "Conflict with the recipe" |
| Q2 | One shot: select a sentence in the preview, press the Comment button, type a short comment, submit; the passage is highlighted and its thread opens; a reply; Resolve. The comment lands in the stage folder's comments file, never in the repository | sections 2 and 3 |
| Q3 | Two captions in turn, English, short: Text 1 "Select a passage and comment" during the action, Text 2 "Reply, then resolve" during the thread; a key badge only for a chord the scenario uses; no opening or end card | section 1 |
| Q4 | Filmed on Windows by the batch, VSIX built from the branch at the take, the kit's throwaway `--extensions-dir` and profile; the owner reviews the storyboard and the clip in the PR; a retake after review is a follow-up CR | sections 4 and 6, "Conflict with the recipe" |
| Q5 | Files: `docs/demo-video/clips/comment-thread/` and the docs the recipe says to link; no change to `src/`; anything else the recipe lists done as it says | "What changes", "Out of scope" |
| Q6 | The PR body embeds the clip, links the MP4 and WebM, states what the clip proves and what the owner judges (motion, rhythm) | section 6 |

What the code settles where the answers speak loosely (no choice made, only the facts of Studio on
`origin/main`):

- **The comments file.** Studio stores threads in `<stem>.comments.json` next to the document
  (`sidecarNameFor` in `src/core/comments/commentModel.ts`): the stage document
  `release-checklist.md` gets `release-checklist.comments.json` in the take's workspace.
- **"Submit".** The comment box (`src/page/modules/commentCompose.ts`) has a **Save** button and
  saves on Cmd/Ctrl+Enter; the reply box of a thread (`src/page/modules/commentThreads.ts`) has a
  **Reply** button and sends on Cmd/Ctrl+Enter. The clip submits both with `ControlOrMeta+Enter`
  (section 3, why), so it uses a chord and shows its badge (Q3).
- **"Its thread opens".** After Save the box closes and the quote becomes a highlight
  (`mark[data-okf-comment-thread]`), but no code opens the popover by itself (`openThread` is called
  nowhere): the thread opens on a click on the highlight. The scenario clicks it.
- **Resolve.** The popover's **Resolve** button (`[data-okf-comment-resolve]`) turns into
  **Reopen**, the popover gains a "Resolved" line (`[data-okf-comment-state="resolved"]`) and stays
  open across the re-render; the highlight turns into a dotted underline
  (`data-okf-comment-resolved="true"`, `src/core/preview/styles/commentStyles.ts`).
- **A highlight needs one text node.** The page wraps the first occurrence of the quote found inside
  one text node of the commented block; a quote that spans bold, code or a link gets a badge
  instead. The filmed sentence is plain text in its paragraph (section 2).
- **The author shown** is the kit profile's `markdownOkfSchemaStudio.comments.authorName`,
  `Reviewer` (`docs/demo-video/clip-kit/lib/profile.mjs`): no personal name in any frame.
- **Comments in Restricted Mode.** Studio writes comments for any saved file, trusted or not
  (`src/session/features/comments.ts`); the kit profile's `security.workspace.trust.enabled: false`
  changes nothing.

## Conflict with the recipe

The recipe as `raw-copy-demo` leaves it (`feature-clip-process.guidelines.md`, new section "The
storyboard first") asks the maintainer to edit and approve the storyboard draft, outside the
repository, before the take. Q4 moves that review into the pull request (the owner is asleep; the
batch films tonight). The recipe is a project guideline and ranks above the process
(constitution, section 8), so this conflict is reported here and in the PR, and listed as open
question 1. This spec follows Q4 and keeps from the recipe all it can without the owner:

- the batch writes the storyboard from its own trial take (the recipe's "A trial first"), with its
  pictures, before the final take, and puts it in the clip folder as the live `clip.md` with
  `status: draft`;
- the PR stays a draft until the owner approved the storyboard and the clip in it; an owner's change
  of an *(on screen)* row is a render only (`just clip comment-thread render`), a change of a
  *(filmed)* row is the follow-up retake of Q4.

## What changes

All paths are relative to the repository root, on the batch's branch for this CR: stacked on
`raw-copy-demo`'s branch while it is not merged, else from `origin/main` once it holds
`raw-copy-demo` (fetch first). Nothing outside the files below changes; in particular no file of
`docs/demo-video/clip-kit/`, no `src/`, no `package.json` or lock file.

### 1. The live storyboard: `docs/demo-video/clips/comment-thread/clip.md`

In the format of the recipe's section 2 (as `raw-copy-demo` writes it), modelled on
`docs/demo-video/clips/raw-copy-balance-edges/clip.md` as that CR leaves it:

- Front matter: `title: Feature clip comment-thread`, `status: draft`, `date:` the day of the
  commit.
- The opening paragraph of the live storyboard, as in the raw copy clip: edit a row marked
  *(on screen)*, save, run `just clip comment-thread render` then `check`; a row marked *(filmed)*
  means a new take. One continuous shot, two texts in turn.
- `## Clip` table:

  | Field | Content |
  | --- | --- |
  | Length | the take's value (proposal 12 s, section 4) |
  | Size *(on screen)* | `1280x720 16:9` |
  | Frame rate *(on screen)* | `15 fps` |
  | Outputs | silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
  | Cards | `none` |
  | Logo | `top right` |
  | Setting filmed | none beyond the kit profile; the author name is the profile's `Reviewer` |
  | Filmed on | Windows, the VS Code version written in `check.json`, the extension version, "VSIX built from the branch" |
  | Stage | `stage/release-checklist.md`, opened in Studio, alone in the window |

- `## 1. Select a passage and comment`: pictures `frames/01-selected.png` (the kit takes it just
  before the first chord: the selected sentence and the comment box with the typed comment) and its
  alt text saying so; table rows `Time` (`0 to <t1> s`, then the action times), `Shot *(filmed)*`
  (the mouse drags over "Announce the freeze in the team channel one day before."; the floating
  **Comment** button; a click; the comment "Which channel?" typed; Ctrl+Enter; the sentence
  highlighted; the pointer clicks the highlight and the thread opens), `Text 1 *(on screen)*` =
  `Select a passage and comment`, `Badge save *(on screen)*` = `Ctrl+Enter / ⌘Enter`.
- `## 2. Reply, then resolve`: pictures `frames/02-pasted.png` (the kit takes it just after the last
  chord: the thread with the comment and the reply) and `frames/03-zoomed.png` (mid zoom hold), with
  alt texts naming what each shows; rows `Time` (`<t1> to <Length> s`), `Shot *(filmed)*` (zoom on
  the highlight and its popover; a click in the reply box; "The #releases channel." typed;
  Ctrl+Enter; the reply under the comment; a click on **Resolve**: "Resolved", **Reopen**, the
  highlight dotted), `Text 2 *(on screen)*` = `Reply, then resolve`, `Badge reply *(on screen)*` =
  `Ctrl+Enter / ⌘Enter`, `Zoom` = `thread, hold to <seconds> s`. No `Mark` row.
- `t1` is the clip time at which the popover opens (end of section 1): the two captions run end to
  end from 0 to `Length` (the parser refuses a gap).
- A block "Expected comments file, the scenario's check": the fields `verify` asserts (section 3),
  written as a short JSON excerpt (`version`, `document`, one thread with its `quote`, `resolved:
  true`, two comments with their author and body; ids and dates omitted and said so).
- "Review notes": the frame names `01-selected` and `02-pasted` are the kit's fixed key frame names
  (first and last chord), not a description of this clip; with `comments.authorName` empty (the
  default) the author shown would be the Git `user.name` (not filmed); the measured raw screencast
  rate (`rawFps` of `check.json`); the conflict with the recipe (the storyboard reviewed in the PR,
  Q4).
- Times and pictures come from the batch's take and render, in the same commit as the outputs.

The texts typed in the take ("Which channel?", "The #releases channel.") are *(filmed)*: changing
them is a retake.

### 2. The stage: `docs/demo-video/clips/comment-thread/stage/release-checklist.md`

A short document whose whole width fits the 1280x720 window, with no front matter, no admonition,
nothing that renders a toolbar of its own:

```markdown
# Release checklist

Run these steps in order before each release.

## Prepare

Tag the release from the main branch after the last merge. Announce the freeze in the team channel one day before.

## Deploy

Run the database migrations first, then restart the workers one at a time.

## Verify

Open the dashboard and check that every worker reports the new version.
```

The filmed sentence "Announce the freeze in the team channel one day before." is plain text (one
text node) and appears once. No `release-checklist.comments.json` in `stage/`: the take starts with
no thread, and Studio creates the file in the take's workspace (the kit's scratch folder).

### 3. The scenario: `docs/demo-video/clips/comment-thread/scenario.mjs`

In the shape of `docs/demo-video/clips/raw-copy-balance-edges/scenario.mjs` (exports `stage`,
`open`, `settings`, `setup`, `run`, `verify`), using only the helpers the kit gives (`t.moveTo`,
`t.click`, `t.selectText`, `t.textEdges`, `t.rectOf`, `t.press`, `t.zoom`, `t.unzoom`, `t.sleep`,
`t.frameOf`, `t.workspaceFile`, `t.record`, `t.page`). `t.rectOf(frame.locator(...))` gives an
element of the preview webview in page coordinates (Playwright's `boundingBox` is relative to the
main frame).

- Header comment: the scene (a comment on a sentence, its thread, a reply, Resolve) and that every
  caption, badge and time is in `clip.md`.
- `stage = { "stage/release-checklist.md": "release-checklist.md" }`;
  `open = ["release-checklist.md"]`.
- `settings`: `"workbench.editorAssociations": { "release-checklist.md":
  "markdown-okf-schema-studio.editor" }` only (comments are on by default; the author name comes
  from the kit profile).
- `setup(t)`, off camera: wait for the preview frame; put Studio in reading mode as the raw copy
  scenario does (toggle `[data-sphinx-preview-edit-toggle]` until `data-sphinx-preview-edit-mode`
  is `off`, `t.record("readingMode", mode)`, throw otherwise); check that no
  `mark[data-okf-comment-thread]` exists (throw otherwise); park the pointer.
- `run(t)`, the filmed action, with an `until(seconds)` clock as in the raw copy scenario. Proposed
  filmed times (the recipe's pacing: moves of 600 to 900 ms, 400 ms before a click or a chord):
  1. 0.3 s: `t.selectText(frame, "Announce", "before.")`; record the page selection and throw unless
     it is exactly "Announce the freeze in the team channel one day before." (whitespace collapsed).
  2. About 2.2 s: wait for `[data-okf-comment-create]` (the floating Comment button) to be visible
     (throw after 2 s), move to its centre, click at about 3.2 s.
  3. Wait for `[data-okf-comment-compose-input]`; type `Which channel?` with
     `t.page.keyboard.type(text, { delay: 50 })`.
  4. About 4.5 s: `t.press("ControlOrMeta+Enter", "save")`. Wait for the box to close and for
     `mark[data-okf-comment-thread]` whose text is the sentence (throw after 3 s, with any
     `[data-okf-comment-error]` text in the message).
  5. Move to the highlight, click at about 6.1 s; wait for `[data-okf-comment-popover]` (throw after
     2 s). Log `t.zoom("thread", rect)` with the union of the highlight and the popover, padded
     24 px, extended downward by the height of one `[data-okf-comment-entry]` and one more line, so
     the reply and the "Resolved" line stay inside it (the kit limits the zoom to 2x).
  6. Move to `[data-okf-comment-reply-input]`, click, type `The #releases channel.` (delay 45 ms);
     about 9.2 s: `t.press("ControlOrMeta+Enter", "reply")`. Wait for two
     `[data-okf-comment-entry]` in the popover (throw after 3 s).
  7. Move to `[data-okf-comment-resolve]` (text "Resolve"), click at about 10.7 s; wait for
     `[data-okf-comment-state="resolved"]` in the popover and `data-okf-comment-resolved="true"` on
     the highlight (throw after 3 s).
  8. Hold about 1.2 s, `t.unzoom("thread")`, move the pointer back to where it started, end about
     13.5 s.
  9. Record `pasteWidgets` as the count of `.post-edit-widget` in the workbench at the end (0): the
     kit's `check` requires the field ("no paste-options widget"); the clip pastes nothing, and the
     count is still true of the window.

  Why the chords: the kit, as `raw-copy-demo` leaves it, takes `frames/01-selected.png` and
  `frames/02-pasted.png` at the take's first and last `press`, so a take with no chord cannot be
  rendered; Q2's "submit" and Studio's documented Cmd/Ctrl+Enter give two real chords, and Q3 allows
  their badges. The Comment button stays a click (Q2).
- `verify(t)`: after `t.sleep(800)`, read `release-checklist.comments.json` with
  `t.workspaceFile`, `JSON.parse` it and throw (with the file's text in the message) unless:
  `version` is 1; `document` is `release-checklist.md`; exactly one thread; its `anchor.quote` is
  the sentence; `resolved` is `true`; exactly two comments, bodies `Which channel?` then `The
  #releases channel.`, both authors `Reviewer`. Return `{ comments: <the parsed file> }`. A
  difference is a finding against the feature, reported with the file's text, never fixed in the
  scenario (recipe, section 6).

### 4. Take and render

On Windows, this machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`):

```bash
just dev
just package                    # out/reports/package/markdown-okf-schema-studio.vsix
just clip comment-thread doctor
just clip comment-thread all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

- A trial first (recipe, section 1): the four proofs, plus two of this clip: (e) the typed text
  reaches the comment box and the reply box; (f) `ControlOrMeta+Enter` saves the comment and sends
  the reply. If (e) or (f) fails, stop and report: no script that sets a textarea's value or calls a
  page function stands in for the filmed action.
- The proposed filmed length is about 13.5 s, so `Length` 12 s gives a playback rate near 1.13
  (inside 0.77 to 1.3). `Length` (5 to 12 s), section times, the zoom hold and `t1` follow the
  take, in the same commit as the render. If the take needs more than 15.6 s, shorten the waits or
  the typed texts' delay, never drop a beat of Q2.
- If the storyboard parser refuses the badge `⌘Enter`, or the keycaps do not read `Ctrl` `Enter`
  and `⌘` `Enter`, write the macOS group `⌘+Enter` (a render, not a take). If the kit as merged
  cannot film or render this clip without a change to the kit, stop and report it: the kit is not
  changed in this CR.
- Commit together (the recipe's rule): `clip.md`, `scenario.mjs`, `stage/release-checklist.md`, the
  outputs `comment-thread.mp4`, `comment-thread.webm`, `comment-thread.gif` (Git LFS through
  `.gitattributes`), `poster.png`, `contact-sheet.png`, `first-last.png`, `frames/*.png` and
  `check.json`.

### 5. Docs that show the clip: `docs/user/review-comments.md`

The recipe's section 4: the feature's docs page embeds the GIF with a plain Markdown image under the
feature's entry. Add, after the paragraph that starts "A thread popover also has **Resolve**":

```markdown
![A sentence is selected in the preview and commented with the Comment button and Ctrl+Enter / ⌘Enter: the passage is highlighted, its thread opens, gets a reply and is resolved](../demo-video/clips/comment-thread/comment-thread.gif)
```

The existing screenshot at the top of the page stays. The site build turns the GIF into a looping
video because the WebM is beside it (`SwRS-MDOKFSTUDIO-CORE-095`, unchanged). The recipe lists no
clip index; no other page, no `README.md`, no `docs/releases-notes/`, no `CHANGELOG.md` change (a
`docs` commit; placing the clip in a release is the release CR's).

### 6. The pull request

- One commit, `docs: add the comment thread feature clip` (no scope: allowed scopes are for `feat`
  and `fix`), message per `.agents/guidelines/git-commit-message.guidelines.md`.
- Opened as a draft (`gh pr create --draft`), body per `.github/PULL_REQUEST_TEMPLATE.md` and the PR
  guideline; in a stack, per `.agents/guidelines/stacked-prs.guidelines.md`.
- Impacts plays the clip: the GIF inline as `![…](https://github.com/gsemet/markdown-okf-schema-studio/raw/<head
  sha>/docs/demo-video/clips/comment-thread/comment-thread.gif)` and the MP4 and WebM linked with
  the same form at the same head sha (the recipe's rule from `raw-copy-demo` Q42; if that CR's open
  question on Git LFS was answered otherwise, its answer applies). Every push of a new render moves
  the three links to the new head (`gh pr edit <n> --body-file <file>`). Check in the rendered PR
  page that the GIF plays.
- The body says what the clip proves (the take's `verify`: one thread in
  `release-checklist.comments.json` with the filmed quote, the comment and the reply, resolved; the
  `check.json` lines) and what the owner judges: motion, rhythm, the loop as watched, the caption
  texts and times, the typed texts.
- "Autonomous decisions": the stage document and sentence; the typed comment and reply; the two
  `ControlOrMeta+Enter` chords and their badges; the zoom on the thread and no mark; the proposed
  length and times; the GIF's place in `review-comments.md` and its alt text; the storyboard
  reviewed in the PR instead of before the take (Q4, the conflict with the recipe).

## Out of scope

- Any change to `src/`, to an SwRS or to a marker (Q5): the clip is documentation.
- Any change to the clip kit (`docs/demo-video/clip-kit/`), its tests or the recipe: they are
  `raw-copy-demo`'s.
- A macOS or Linux take, Delete, Reopen, orphaned comments, the Comments toolbar toggle, the
  Ctrl+Alt+M shortcut.
- The retake after the owner's review (a follow-up CR, Q4); placing the clip in release notes or an
  announcement.

## Host and default matrix

The clip depends on the host (the submit chord) and on one configured value (the author name, set
by the kit profile; its default is empty).

| Host | VS Code | `comments.authorName` | Expected | Proof |
| --- | --- | --- | --- | --- |
| Windows 11, `Ctrl+Enter` through CDP | pinned `DEFAULT_CODE_VERSION` | `Reviewer` (kit profile) | one thread with the quote, comment and reply by `Reviewer`, resolved | the take's `verify`; `check.json` "scenario verify passed" |
| macOS, `⌘Enter` | same | `Reviewer` | same | not proved (no macOS take) |
| Linux | same | `Reviewer` | same | not proved |
| any | same | empty (default) | the Git `user.name` shown as author | not filmed (would show personal data); stated in the review notes |

## Evidence

1. `just clip comment-thread all --vsix …` passes; `check.json` shows `passed: true`, MP4 and WebM
   1280x720 at 15 fps, the MP4 duration equal to `Length` within one frame, GIF at most 960 px and
   12 fps, loop seam SSIM in [0.98, 1.0), `verifyPassed: true`, `readingMode: off`,
   `pasteWidgets: 0`, playback rate inside 0.77 to 1.3, platform `win32`, extension source `vsix`.
2. The take's `verify.json` holds the parsed `release-checklist.comments.json` (section 3's fields).
3. The agent looks at the contact sheet and every key frame: the selection on the whole sentence,
   the Comment button, the box with "Which channel?", the highlight, the popover with author
   `Reviewer`, the reply, "Resolved" and **Reopen**, the dotted highlight, Text 1 during section 1
   and Text 2 during section 2, both badges reading `Ctrl+Enter / ⌘Enter`, the zoom keeping the
   whole popover in view, no tooltip, no personal name or path, no dirty tab. What was not checked
   (motion, rhythm, the loop as watched) is said.
4. `just check` passes (it runs `raw-copy-demo`'s parser tests, which read the shipped raw copy
   storyboard; this CR's `clip.md` is parsed from the repository at the head by `just clip
   comment-thread render`, step 1).
5. `just preflight` passes (on Windows, its static stage).
6. The PR body plays the GIF and links the MP4 and WebM at the head sha.

## Open questions

1. The recipe (a project guideline, as `raw-copy-demo` leaves it) asks the maintainer to approve the
   storyboard before the take; Q4 moves that review into the PR. The spec follows Q4, writes the
   storyboard from the batch's trial take before the final take, keeps the PR a draft until the
   owner approves, and reports the conflict in the PR. Is this deviation accepted for this clip (and
   the other clips planned the same night), or must the batch stop after the storyboard and wait
   for the owner's approval before the take?
