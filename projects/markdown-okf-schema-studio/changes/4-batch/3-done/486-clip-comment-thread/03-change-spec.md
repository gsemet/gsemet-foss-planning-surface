# Feature clip: a comment thread on a passage

Short name: `clip-comment`. No tracker issue (verbal request of the owner, 2026-11-25).

## Goal

The next feature clip of Studio, on review in the page itself: in the preview, a sentence is
selected, the small **Comment** button is pressed, a comment is written and saved; the passage is
highlighted, and a click on it opens the thread with its Reply box and its Resolve and Delete
buttons. The thread is stored in the comments file next to the document, versioned in Git with the
Markdown, with no server. Reviewing what an agent wrote and leaving it notes is the use the clip
sells.

It is made with the clip kit (`docs/demo-video/clip-kit/`) and the feature clip recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`) exactly as the CR
`short-demo-video-of-the-smart-raw-markdo` (short name `raw-copy-demo`) leaves them
(`depends.json`): a live Markdown storyboard `clip.md` with a `## Clip` table and one
`## <n>. <beat>` section per beat, `Text <n>` captions in turn, `Size` and `Frame rate` fields,
combined key badges `Ctrl+… / ⌘…`, several `Mark <id>` rows in turn, key frames `frames/01-selected.png`,
`02-pasted.png`, `03-zoomed.png` and one `frames/<NN>-mark-<id>.png` per mark, and the PR rule that
plays the clip in the PR. That CR's spec is `03-change-spec.md` in its folder of the planning
surface (`changes/2-backlog/P1/short-demo-video-of-the-smart-raw-markdo/`, or wherever the batch
moved it). Where the kit or the recipe as merged differ from that spec, the merged files win.

The clip's approved shape is the Griller's storyboard draft `work/storyboard/clip.md` of this CR's
folder, with its stage `work/storyboard/stage/proposal.md`. This spec carries it; the section
"Where this spec differs from the draft" lists every change and its reason.

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| Q1 | Filed from the owner's request: one CR per clip, this clip among seven | Goal |
| Q2 | The captions, stage and timing are the Griller's proposal, the storyboard draft; the owner reviews them at the recipe's storyboard gate | sections 1 to 4 |
| Q3 | The batch does not wait for the storyboard approval before the take: it films the trial take from the draft, puts its pictures in the storyboard, renders the clip and opens the PR with the clip watchable; the owner reviews the storyboard and the clip on that PR, which stays a draft until the owner approves; the deviation from the recipe's order is reported in this spec and in the PR body; a retake after the review is a follow-up of this CR | "The storyboard gate, moved after the take", section 6 |

## The storyboard gate, moved after the take

The recipe, as `raw-copy-demo` leaves it (section "The storyboard first"), has the maintainer
approve the storyboard draft before the take. Q3 moves that gate after the take, into the pull
request; it does not drop it. This is a deviation from a project guideline, decided by the Chief of
Staff under the owner's overnight autonomy, and reported as such:

- the batch films a trial take from the draft, puts its pictures and measured times in the
  storyboard, moves it to `docs/demo-video/clips/comment-thread/clip.md` with `status: draft`,
  films the take, renders and opens the PR;
- the PR is a draft (`gh pr create --draft`) until the owner approves the storyboard and the clip
  in it; the PR body has a line "Deviation from the feature clip process" saying that the storyboard
  was reviewed after the take (Q3) and how a review lands: an *(on screen)* row changed by the owner
  is a render (`just clip comment-thread render` then `check`), a *(filmed)* row is the follow-up
  retake;
- the recipe itself is not changed.

## What the code settles

Facts of Studio on `origin/main`, read to name the real controls (no choice made here):

- **The comments file** is `<stem>.comments.json` next to the document (`sidecarNameFor`,
  `src/core/comments/commentModel.ts`): `proposal.md` gets `proposal.comments.json` in the take's
  workspace, as the draft says.
- **The Comment button** is `button[data-okf-comment-create]`, text "Comment", shown beside the
  selection after the mouse is released (`src/page/modules/commentCompose.ts`); its mousedown keeps
  the selection. It opens the box `[data-okf-comment-compose]` with the text area
  `[data-okf-comment-compose-input]` (placeholder "Write a comment"), **Save** and **Cancel**.
  Cmd/Ctrl+Enter saves. On the host's answer the box closes and the selection is cleared.
- **The thread does not open by itself after Save**: `openThread` is called nowhere in `src/`. The
  quote becomes `mark[data-okf-comment-thread]`; a click on it opens the popover
  `[data-okf-comment-popover]` (`src/page/modules/commentThreads.ts`): author, date, the comment,
  the actions row `[data-okf-comment-thread-actions]` with **Resolve** (`[data-okf-comment-resolve]`)
  and **Delete**, then the reply box `[data-okf-comment-reply]` (text area "Reply", button
  **Reply**). The draft's click on the highlight at 5.4 s therefore stays (its first review note is
  answered).
- **A press outside the popover closes it** when its reply box is blank (`pointerdown` and
  `mousedown` handlers, `src/page/modules/commentThreads.ts`); Escape does the same.
- **A highlight needs the quote in one text node** of the commented block; the filmed sentence is
  plain text in its paragraph, so it is highlighted, not badged.
- **The author** is the kit profile's `markdownOkfSchemaStudio.comments.authorName`, `Reviewer`
  (`docs/demo-video/clip-kit/lib/profile.mjs`).
- **Comments are written for any saved file**, trusted or not (`src/session/features/comments.ts`);
  the kit profile's `security.workspace.trust.enabled: false` changes nothing.

## Where this spec differs from the draft

| Draft | This spec | Why |
| --- | --- | --- |
| `Format` row (size, rate, outputs in one cell) | `Size *(on screen)*` = `1280x720 16:9`, `Frame rate *(on screen)*` = `15 fps`, `Outputs` = the rest | the kit, as `raw-copy-demo` leaves it, reads `Size` and `Frame rate` as their own fields |
| The zoom described in the `Time` and `Shot` rows only | a row `Zoom` = `thread, hold to 9.8 s` (or the take's hold) in section 2 | the kit reads the zoom from a `Zoom` row |
| "the thread closed with Escape at 10.0 s" | a click on an empty place of the page, beside the paragraph, at about 10.0 s | every `press` of a take needs a `Badge` row (the parser refuses a press without one), and the kit takes `frames/02-pasted.png` just after the last press: an Escape would add an unwanted badge and move that frame to the end of the clip. A press outside closes the popover the same way (above) |
| "Pictures: from the batch's trial take" | the kit's key frames: section 1 `frames/01-selected.png` (just before the save chord: the selection and the typed comment) and `frames/02-pasted.png` (just after it: the box closing, the highlight appearing); section 2 `frames/03-zoomed.png`, `frames/04-mark-1.png`, `frames/05-mark-2.png` | the storyboard shows the kit's frames, as the raw copy clip does; `01-selected` and `02-pasted` are the kit's fixed names (first and last press), said in the review notes |
| Status "draft for the owner's review", opening paragraph of a review draft | `status: draft`, the opening paragraph of a live storyboard | the file becomes the live storyboard in the clip folder (recipe) |
| `Filmed on`: "to be filmed by the batch" | Windows, the VS Code version of `check.json`, the extension version, "VSIX built from the branch" | the batch's take |
| Review note "If the thread opens by itself after Save …" | replaced by "The thread opens on a click on the highlight (Studio opens no thread by itself)" | settled by the code |
| Times 10.8 s, 5.0 s, marks 6.3 to 7.5 s and 7.5 to 8.9 s | the take's own times, same beats and order | the recipe: the storyboard follows the take |

Everything else is carried as written: the texts, the stage, the shot, the badge, the marks, the
expected result, and the notes on the date, the fresh workspace, the reply not filmed and the
selection on the sentence's own characters. The file name `proposal.comments.json` and the single
Ctrl+Enter chord already match the code; no reply and no Resolve are filmed (the draft's note: a
typed reply would push the clip past 12 s).

## What changes

All paths are relative to the repository root, on the batch's branch for this CR: stacked on
`raw-copy-demo`'s branch while it is not merged, else from `origin/main` once it holds it (fetch
first). Nothing else changes: no file of `docs/demo-video/clip-kit/`, no recipe, no `src/`, no
`package.json` or lock file.

### 1. The live storyboard: `docs/demo-video/clips/comment-thread/clip.md`

The draft `work/storyboard/clip.md`, with only the changes of the table above:

- Front matter `title: Feature clip comment-thread`, `status: draft`, `date:` the day of the commit.
- Opening paragraph, as in the raw copy clip's live storyboard: edit any row marked *(on screen)*,
  save, run `just clip comment-thread render`, then `check`; rows marked *(filmed)* describe the
  take, changing them means a new take. Keep: one continuous shot, two texts in turn, the meaning of
  `**bold**`. Drop "Once approved, this file becomes …" and "The times below are the Griller's
  proposal …".
- `## Clip`: `Length` (the take's, proposal 10.8 s), `Size *(on screen)*` `1280x720 16:9`,
  `Frame rate *(on screen)*` `15 fps`, `Outputs` "silent, loops; MP4 (X, release), WebM (docs
  site), GIF 960 px (release notes, docs page)", `Cards` `none`, `Logo` `top right`,
  `Setting filmed` as in the draft, `Filmed on` (above), `Stage` as in the draft.
- `## 1. Select a sentence and comment`: the two pictures; `Time` `0 to <t1> s (…)` with the take's
  action times; `Shot *(filmed)*` as in the draft; `Text 1 *(on screen)*` =
  `Select a passage and **comment** on it in the page`; `Badge save *(on screen)*` =
  `Ctrl+Enter / ⌘Enter`.
- `## 2. The thread, zoomed`: the three pictures; `Time` `<t1> to <Length> s (…)`, the close now "a
  click beside the paragraph closes the thread"; `Shot *(filmed)*` as in the draft; `Zoom` =
  `thread, hold to <s> s`; `Mark 1 *(on screen)*` = `Orange outline around the highlighted
  sentence, <from> to <to> s`; `Mark 2 *(on screen)*` = `Orange outline around the Reply box and
  the Resolve button, <from> to <to> s`; `Text 2 *(on screen)*` =
  `Threads live in **.comments.json**, next to the file`.
- The captions run end to end from 0 to `Length` (`t1` is where section 1 ends); both marks lie
  inside the zoom hold, one after the other.
- The "Expected result" block as in the draft (`proposal.comments.json`, one thread, the quote
  "We drop support for Node 18 in this release.", `resolved: false`, one comment by `Reviewer`,
  body "Can we keep it one more release?"; `proposal.md` unchanged).
- "Review notes": the draft's notes minus the settled first one, plus: the thread opens on the
  click on the highlight; `01-selected` and `02-pasted` are the kit's fixed key frame names; the
  measured raw screencast rate (`rawFps`); the storyboard reviewed in the PR after the take (Q3).

### 2. The stage: `docs/demo-video/clips/comment-thread/stage/proposal.md`

The draft's `work/storyboard/stage/proposal.md`, byte for byte. No `proposal.comments.json` in
`stage/`.

### 3. The scenario: `docs/demo-video/clips/comment-thread/scenario.mjs`

In the shape of `docs/demo-video/clips/raw-copy-balance-edges/scenario.mjs` (exports `stage`,
`open`, `settings`, `setup`, `run`, `verify`), with the kit's helpers only (`t.moveTo`, `t.click`,
`t.selectText`, `t.rectOf`, `t.press`, `t.zoom`, `t.unzoom`, `t.mark`, `t.unmark`, `t.sleep`,
`t.frameOf`, `t.workspaceFile`, `t.record`, `t.page`). `t.rectOf(frame.locator(…))` gives an element
of the preview webview in page coordinates (Playwright's `boundingBox` is relative to the main
frame).

- Header comment: the scene, and that every caption, badge and time is in `clip.md`.
- `stage = { "stage/proposal.md": "proposal.md" }`; `open = ["proposal.md"]`; `settings` =
  `"workbench.editorAssociations": { "proposal.md": "markdown-okf-schema-studio.editor" }`.
- `setup(t)`, off camera: wait for the preview frame; reading mode as in the raw copy scenario
  (`[data-sphinx-preview-edit-toggle]` until `data-sphinx-preview-edit-mode` is `off`,
  `t.record("readingMode", mode)`, throw otherwise); throw if `proposal.comments.json` exists in the
  workspace or a `mark[data-okf-comment-thread]` is in the page (the draft's "no comments file at
  frame 0"); keep the text of `proposal.md` for `verify`; park the pointer.
- `run(t)`, with an `until(seconds)` clock; the draft's times are the targets (recipe pacing: moves
  of 600 to 900 ms, 400 ms before a click or a chord):
  1. 0.3 s: `t.selectText(frame, "We drop", "release.")`; record the page selection; throw unless
     it is exactly "We drop support for Node 18 in this release." (whitespace collapsed).
  2. Wait for `[data-okf-comment-create]` (throw after 2 s); move to it; click at about 2.6 s.
  3. Wait for `[data-okf-comment-compose-input]`; from about 2.9 s type
     `Can we keep it one more release?` with `t.page.keyboard.type(text, { delay: 40 })`.
  4. About 4.6 s: `t.press("ControlOrMeta+Enter", "save")`. Wait for the box to close and for
     `mark[data-okf-comment-thread]` holding the sentence (throw after 3 s, with any
     `[data-okf-comment-error]` text in the message).
  5. Move to the highlight; click at about 5.4 s; wait for `[data-okf-comment-popover]` (throw
     after 2 s).
  6. About 5.8 s: `t.zoom("thread", rect)`, the union of the highlight and the popover, padded
     24 px (the kit limits the zoom to 2x).
  7. `t.mark("1", rect)` around the highlight (a few pixels of air), `t.unmark("1")`; then
     `t.mark("2", rect)` around the union of `[data-okf-comment-reply]` and
     `[data-okf-comment-resolve]`, `t.unmark("2")`; at the storyboard's mark times.
  8. About 9.8 s: `t.unzoom("thread")`. About 10.0 s: move to an empty place of the page beside the
     paragraph and click; wait for the popover to be gone (throw after 2 s).
  9. Move the pointer back to where it started; end near the length.
  10. Record `pasteWidgets` as the count of `.post-edit-widget` in the workbench (0): the kit's
      `check` requires the field; the clip pastes nothing, and the count is still true of the
      window.
- `verify(t)`: after `t.sleep(800)`, read `proposal.comments.json` with `t.workspaceFile`,
  `JSON.parse` it, and throw (with the file's text in the message) unless: `version` 1; `document`
  `proposal.md`; one thread; `anchor.quote` the sentence; `resolved` `false`; one comment, author
  `Reviewer`, body `Can we keep it one more release?`. Throw too if `proposal.md` differs from the
  text kept in `setup`. Return `{ comments: <the parsed file> }`. A difference is a finding against
  the feature, reported with the file's text, never fixed in the scenario (recipe, section 6).

### 4. Trial take, take and render

On Windows, this machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`):

```bash
just dev
just package                    # out/reports/package/markdown-okf-schema-studio.vsix
just clip comment-thread doctor
just clip comment-thread all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

- The trial take (recipe, section 1) proves its four points, plus: (e) the typed text reaches the
  comment box; (f) `ControlOrMeta+Enter` saves it. If (e) or (f) fails, stop and report: no script
  that sets the text area's value or calls a page function stands in for the filmed action.
- Its pictures and measured times go into `clip.md` (Q3), then the take that ships. `Length` (5 to
  12 s, playback rate inside 0.77 to 1.3), section times, zoom hold and mark times follow it, in
  the same commit as the render.
- If the parser refuses `⌘Enter`, or the keycaps do not read `Ctrl` `Enter` and `⌘` `Enter`, write
  the macOS group `⌘+Enter` (a render, not a take). If the kit as merged cannot film or render this
  clip without a change to the kit, stop and report: the kit is not changed here.
- Commit together (the recipe): `clip.md`, `scenario.mjs`, `stage/proposal.md`, the outputs
  `comment-thread.mp4`, `.webm`, `.gif` (Git LFS through `.gitattributes`), `poster.png`,
  `contact-sheet.png`, `first-last.png`, `frames/*.png`, `check.json`.

### 5. The docs page: `docs/user/review-comments.md`

The recipe's section 4 (the GIF under the feature's entry). After the paragraph that starts "To
start a thread, select text in the preview", add:

```markdown
![A sentence is selected in the preview, the Comment button pressed, a comment typed and saved with Ctrl+Enter / ⌘Enter: the sentence is highlighted and a click opens its thread with Reply, Resolve and Delete](../demo-video/clips/comment-thread/comment-thread.gif)
```

The screenshot at the top of the page stays. The site build turns the GIF into a looping video
because the WebM is beside it (`SwRS-MDOKFSTUDIO-CORE-095`, unchanged). The recipe lists no clip
index; no change to `README.md`, `docs/releases-notes/` or `CHANGELOG.md` (a `docs` commit; the
release CR places clips in a release).

### 6. The pull request

- One commit, `docs: add the comment thread feature clip` (no scope: allowed scopes are for `feat`
  and `fix`), message per `.agents/guidelines/git-commit-message.guidelines.md`.
- A draft PR (`gh pr create --draft`) until the owner approves (Q3), body per
  `.github/PULL_REQUEST_TEMPLATE.md` and the PR guideline; in the stack, per
  `.agents/guidelines/stacked-prs.guidelines.md`.
- Impacts plays the clip: the GIF inline as `![…](https://github.com/gsemet/markdown-okf-schema-studio/raw/<head
  sha>/docs/demo-video/clips/comment-thread/comment-thread.gif)`, the MP4 and WebM linked in the
  same form at the same head sha (the recipe's rule from `raw-copy-demo`; if that CR settled Git
  LFS playback otherwise, its way applies). Each push of a new render moves the three links to the
  new head (`gh pr edit <n> --body-file <file>`). Check in the rendered PR page that the GIF plays.
- The body states what the clip proves (the take's `verify`: one thread in
  `proposal.comments.json` with the filmed quote and comment, `proposal.md` unchanged; the
  `check.json` lines) and what the owner judges (motion, rhythm, the loop as watched, the caption
  texts and times); the line "Deviation from the feature clip process" (above); and "Autonomous
  decisions": the close by a click instead of Escape, the storyboard field split and `Zoom` row,
  the GIF's place and alt text in `review-comments.md`.

## Out of scope

- Any change to `src/`, an SwRS or a marker; any change to the clip kit, its tests or the recipe
  (`raw-copy-demo`'s).
- A typed reply, Resolve, Delete, Reopen, orphaned comments, the Comments toolbar toggle, the
  Ctrl+Alt+M shortcut, showing the comments file on screen (the draft's notes).
- A macOS or Linux take; the retake after the owner's review (a follow-up, Q3); placing the clip in
  release notes or an announcement.

## Host and default matrix

The clip depends on the host (the save chord) and on one configured value (the author name, set by
the kit profile; its default is empty).

| Host | VS Code | `comments.authorName` | Expected | Proof |
| --- | --- | --- | --- | --- |
| Windows 11, `Ctrl+Enter` through CDP | pinned `DEFAULT_CODE_VERSION` | `Reviewer` (kit profile) | one thread with the quote and the comment by `Reviewer`, highlighted, its popover opened by a click | the take's `verify`; `check.json` "scenario verify passed" |
| macOS, `⌘Enter` | same | `Reviewer` | same | not proved (no macOS take) |
| Linux | same | `Reviewer` | same | not proved |
| any | same | empty (default) | the Git `user.name` shown as author | not filmed (it would show personal data); stated in the review notes |

## Evidence

1. `just clip comment-thread all --vsix …` passes; `check.json` shows `passed: true`, MP4 and WebM
   1280x720 at 15 fps, the MP4 duration equal to `Length` within one frame, GIF at most 960 px and
   12 fps, loop seam SSIM in [0.98, 1.0), `verifyPassed: true`, `readingMode: off`,
   `pasteWidgets: 0`, playback rate inside 0.77 to 1.3, platform `win32`, extension source `vsix`.
2. The take's `verify.json` holds the parsed `proposal.comments.json` with the fields of section 3.
3. The agent looks at the contact sheet and each key frame: the selection on the whole sentence,
   the Comment button, the box with the typed comment, the highlight, the popover with `Reviewer`,
   the comment, Resolve, Delete and the Reply box, mark 1 on the highlight and mark 2 on the Reply
   box and Resolve in turn, Text 1 in section 1 and Text 2 in section 2, the badge reading
   `Ctrl+Enter / ⌘Enter`, the popover closed before the loop, no tooltip, no personal name or path,
   no dirty tab. What was not checked (motion, rhythm, the loop as watched) is said.
4. `just check` passes; `clip.md` is parsed from the repository at the head by
   `just clip comment-thread render` (step 1).
5. `just preflight` passes (on Windows, its static stage).
6. The PR body plays the GIF, links the MP4 and WebM at the head sha, and carries the deviation line.
