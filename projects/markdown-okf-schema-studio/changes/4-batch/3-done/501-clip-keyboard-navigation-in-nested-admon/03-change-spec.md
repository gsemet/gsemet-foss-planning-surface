# Clip: keyboard navigation in nested admonitions and lists

Short name: `keyboard-nav`. No tracker issue (verbal request of the owner, relayed by the Chief of
Staff, 2026-11-25).

## Goal

A feature clip that shows a writer editing a nested part of a page without touching the mouse,
made with the merged clip kit (`docs/demo-video/clip-kit/`) and the feature clip recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`). A release plan opens in Studio in
reading mode. `E` turns edit mode on; Down, Down select the heading then the `note` admonition;
Enter opens the whole admonition in its source editor and Escape closes it unchanged. A zoom on the
admonition: Right goes inside it (its sentence), Down reaches its list, Right goes inside the list
(its first item). Enter opens that item alone, Ctrl+Backspace (Option+Backspace on macOS) deletes
its last word "Friday", "Thursday" is typed, and Ctrl/Cmd+Enter saves; an orange mark outlines the
saved item. Eleven key presses, each shown as a badge in its Windows and macOS forms. One continuous
shot of 20.0 s, three captions in turn, one zoom, one mark, 1280x720 at 15 fps, no card, the logo
top right, a loop; MP4, WebM and GIF. The pull request plays the clip and the owner reviews the
storyboard and the clip there.

The clip shows existing behaviour: `E` from reading mode (`SwRS-MDOKFSTUDIO-LIFE-172`,
`src/page/features/editMode.ts`), Up/Down selection and Enter (`SwRS-MDOKFSTUDIO-BLOCK-004`,
`stepSelection` in `src/page/features/blockSelectionView.ts`), Right and Left through the levels
(`SwRS-MDOKFSTUDIO-BLOCK-254`, `src/page/features/structuralNavigationView.ts`,
`src/page/modules/structuralCursor.ts`, `mappedChildren` in `src/page/features/mappedBlocks.ts`),
the caret at the end of an opened editor (`focusTextControlAtLastContent`,
`src/page/features/blockSourceEditor.ts`), and `docs/user/editing.md` ("Keyboard only",
"Structure", "A list has three levels"). No behaviour of the extension changes and no rendered
syntax changes, so the writing skill `skills/writing-for-markdown-okf-schema-studio/` is not
touched.

## Dependency and base

- `depends.json`: `{"after": ["clip-the-advanced-renderings-tour"]}` (keyboard-nav-Q5). That CR's
  first commit, `build: let a feature clip run up to 30 seconds`, raises the kit's `MAX_LENGTH`
  (`docs/demo-video/clip-kit/lib/storyboard.mjs`) from 12 to 30 and the recipe's "5 to 12" to
  "5 to 30". This 20 s clip is refused by the kit without it.
- keyboard-nav-Q4 ("built on main, alone, no `depends.json`") is superseded on that point by Q5,
  written after it: the branch stacks on the branch of `clip-the-advanced-renderings-tour` in the
  batch-09 stack (`.agents/guidelines/stacked-prs.guidelines.md`), never on a copy of its kit
  change. It depends on no other clip of the round. Fetch first: the local `main` is behind
  `origin/main`.
- What `origin/main` already holds and this clip uses: the storyboard contract and parser
  (`lib/storyboard.mjs`, combined badges `<Ctrl form> / <⌘ form>`), `t.press(chord, badgeId)`,
  `t.keyFrame(name)` (`lib/take.mjs`; frames by `keyFrameTimes` in `lib/encode.mjs`),
  `checks = { editMode, paste }` (`resolveChecks` in `lib/check.mjs`), and the merged
  `comment-thread` and `slash-menu-grid` clips, the closest models (reading-mode `setup`, typed text
  with no badge, `ControlOrMeta+Enter` save with a badge).
- This CR makes **no kit code change** (keyboard-nav-Q5, Q9; see "The badge of the word delete").

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| keyboard-nav-Q1 | The owner's wish: keyboard navigation in nested admonitions and lists, mouse never used, longer than usual; the request's scenario | whole spec |
| keyboard-nav-Q2 | The captions, stage and timing of the Griller's storyboard draft are the clip's shape | sections 1, 2, 3 |
| keyboard-nav-Q3 | The batch films a trial take from the draft, puts its pictures in the storyboard, renders, opens the PR with the clip watchable (GIF inline, MP4 and WebM linked at the head); the PR stays a draft until the owner approves; the deviation from the recipe's order is reported here and in the PR body; a retake after review is a follow-up of this CR | "The storyboard gate, moved after the take", sections 4, 7 |
| keyboard-nav-Q4 | The clip depends on none of the other clips of the round; its "no `depends.json`" is superseded by Q5 | "Dependency and base" |
| keyboard-nav-Q5 | 20.0 s; the 30 s limit comes from `clip-the-advanced-renderings-tour` (`depends.json` after it); no kit change of this CR's own | "Dependency and base", sections 2, 3 |
| keyboard-nav-Q6 | `E` pressed first to turn edit mode on; Enter opens the list item (step 6 of the request) | sections 2, 3 (`run` steps 1, 9), 7 |
| keyboard-nav-Q7 | Down selects the list; the second Right selects its first item, which is the item edited | sections 2, 3 (`run` steps 7, 8) |
| keyboard-nav-Q8 | The clip starts in reading mode; the keyboard focus is given off camera by one margin click in `setup`; the first Down selects the heading, the second the admonition; the pointer never moves | section 3 (`setup`, `run` steps 2, 3) |
| keyboard-nav-Q9 | The word changed is the item's last, "Friday" to "Thursday", deleted with Ctrl+Backspace (Option+Backspace on macOS), badge `Ctrl+⌫ / ⌥⌫`, typed with no badge per letter; filmed on Windows | sections 2, 3 (`run` steps 10, 11), "The badge of the word delete" |
| keyboard-nav-Q10 | Stage: heading, `note` admonition "Before the release" with a sentence and a list of three items (one with two sub-items), closing sentence; badges `E`, `↓`, `→`, `Esc`, `Enter / ↩`, `Ctrl+Enter / ⌘↩`; three captions, one zoom on the admonition, one mark on the saved item; fallback for the loop seam: a last Escape | sections 1, 2, 3, 4 |

## The storyboard gate, moved after the take

The recipe (section "The storyboard first") has the maintainer review the storyboard draft before
the take. keyboard-nav-Q3 moves that gate after the take, into the pull request; it does not drop
it:

- the batch films a trial take from the draft, puts its pictures and measured times in the
  storyboard, moves it to `docs/demo-video/clips/keyboard-navigation/clip.md`, films the take (the
  trial may be the take when it is clean), renders and opens the PR;
- the PR is a draft (`gh pr create --draft`) until the owner approves the storyboard and the clip;
  the agent never marks it ready; the PR body reports the deviation (section 7);
- the recipe is not changed by this CR.

## The badge of the word delete

The kit's `validateStory` (`lib/storyboard.mjs`) refuses a badge naming the other platform's
modifier unless `isCombinedBadge` reads it as `<Ctrl form> / <⌘ form>`. `Ctrl+⌫ / ⌥⌫` is not a
combined badge for the kit (its second group has `⌥`, not `⌘`), so:

- filmed on Windows (`win32`), `wrongModifier` finds no `⌘` or `Cmd` in it and the badge passes;
- filmed on macOS (`darwin`), it is refused ("names Ctrl").

Decision of this spec, from keyboard-nav-Q9 ("filmed on Windows; a macOS take would need the kit to
accept `⌥`") and Q5 ("no kit change of its own"): **keep the badge, film on Windows, change no kit
code.** The badge is not avoided (Q9 and Q10 name it), and `isCombinedBadge` is not changed here.
The storyboard test (section 5) pins both facts: the shipped story validates on `win32`, and on
`darwin` it is refused for the badge `delete-word` only. A macOS take is out of scope; the change it
would need (accept `⌥` as well as `⌘` in the second group of `isCombinedBadge`, with a test, and the
`darwin` assertion of section 5 turned into a pass) is a follow-up, or this CR's if the Chief of
Staff says so (open question 1).

Keycaps (`remotion/src/Clip.tsx`, `keysOf`): `Ctrl+⌫` shows two keys, `⌥⌫` one key (a group splits
on `⌘` only); the review notes say so, as `block-editor-modes` says it of `⇧⌘M`.

## What changes

All paths are relative to the repository root.

### 1. The stage: `docs/demo-video/clips/keyboard-navigation/stage/release-plan.md`

Copied byte for byte from `work/storyboard/stage/release-plan.md` of this CR's folder (in the
planning surface,
`C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/2-backlog/P2/clip-keyboard-navigation-in-nested-admon/`,
or wherever the batch moved the folder), LF line endings, ending with one newline:

```markdown
# Release plan

:::{note} Before the release
Run these steps in order, one person per step.

- Tag the release on Friday
- Build the packages
  - the VSIX
  - the docs site
- Post the announcement
:::

The release owner signs off in the team channel.
```

"Friday" occurs once. The admonition (lines 3 to 12, one-based) is the block opened at Enter, its
sentence (line 4) the first inner block, the list (lines 6 to 11) the second, "Tag the release on
Friday" (line 6) the item edited.

### 2. The live storyboard: `docs/demo-video/clips/keyboard-navigation/clip.md`

The draft `work/storyboard/clip.md` of this CR's folder, adapted only as follows; every row marked
*(on screen)* keeps its text, and the times follow the take:

- Front matter: `title: Feature clip keyboard-navigation`, `status: draft for the owner's review`
  (keyboard-nav-Q3), `date:` the day of the commit.
- Opening paragraphs as drafted (the live storyboard sentence with
  `just clip keyboard-navigation render`, then `check`; the one continuous shot, the pointer still,
  eleven presses, three texts in turn).
- `## Clip` table as drafted: `Length` `20.0 s` (or the take's value, within the kit's 5 to 30 s),
  `Size *(on screen)*` `1280x720 16:9`, `Frame rate *(on screen)*` `15 fps`, `Outputs`, `Cards`
  `none`, `Logo` `top right`, `Setting filmed` `none: every setting at its default`, `Filmed on`
  "Windows, VS Code <version>, extension <version> VSIX built from the branch" (the versions
  `check.json` writes), `Stage` as drafted.
- The "Off camera (`setup`)" paragraph: kept as drafted, worded as section 3's `setup` does it.
- Three sections, `## 1. E for edit mode, the arrows pick a block`, `## 2. Right goes one level
  deeper`, `## 3. Edit one item, save`, each with its `Time` (the take's measured times, same shape
  as drafted), `Shot *(filmed)*` as drafted, and these *(on screen)* rows, exactly:
  - section 1: `Text 1` = `Press **E**, then the arrows pick a block`; `Badge edit` = `E`;
    `Badge down` = `↓`; `Badge enter` = `Enter / ↩`; `Badge escape` = `Esc`;
  - section 2: `Zoom` = `admonition, hold to 19.2 s` (the take's hold); `Text 2` = `**Right** goes
    one level deeper`; `Badge right` = `→`;
  - section 3: `Mark 1` = `Orange outline around the saved item, 17.4 to 19.0 s` (the take's times,
    inside the hold); `Text 3` = `Change a word and **save**, no mouse at all`;
    `Badge delete-word` = `Ctrl+⌫ / ⌥⌫`; `Badge save` = `Ctrl+Enter / ⌘↩`.
- Pictures: the "Pictures:" line of each section links the key frames the scenario names
  (section 3: `frames/edit-on.png`, `frames/admonition-selected.png`,
  `frames/admonition-editor.png`, `frames/admonition-back.png`; `frames/sentence-selected.png`,
  `frames/list-selected.png`, `frames/item-selected.png`; `frames/item-editor.png`,
  `frames/word-changed.png`) and the kit's `frames/03-zoomed.png` (section 2) and
  `frames/04-mark-1.png` (section 3), each with an alt text saying what it shows. `01-selected.png`
  and `02-pasted.png` are the kit's fixed names (just before `E`, just after Ctrl+Enter), kept and
  not linked.
- "Expected result" list as drafted (a list, not a `markdown` block: the parser's `expectedPaste`
  stays `null`), with what the take recorded (the editor's text of the item, see `run` step 9).
- "Review notes": keep the draft's notes (the `E` and Enter keys with Q6 called out as the owner's
  to confirm, what Right selects, the first block without the mouse, the admonition title, changing
  one word, the badge of the word delete, length, loop seam, pointer, the stage restored per run).
  Change: the "badge of the word delete" note says the kit was left unchanged (this spec) and that
  `⌥⌫` shows as one keycap; the "Length" note says the kit allows 30 s since
  `clip-the-advanced-renderings-tour` and gives the GIF ladder step `check.json` reports; the "loop
  seam" note gives the measured SSIM and whether the fallback Escape was filmed; the "admonition
  title" note says what the trial saw. Add the measured times of the take (as the `slash-menu-grid`
  "Measured by the take" note, with `rawFps`), the key frame list, and "Not checked by the author:
  motion, rhythm, the loop as watched."

### 3. The scenario: `docs/demo-video/clips/keyboard-navigation/scenario.mjs`

Modelled on `docs/demo-video/clips/comment-thread/scenario.mjs` (its `readingMode` and `waitFor`
helpers) and `slash-menu-grid/scenario.mjs` (`until(seconds)`, the save press). Node built-ins only;
nothing runs at import (the kit's tests load it). The header comment says what is filmed and that
every caption, badge and time is in `clip.md`.

- `stage = { "stage/release-plan.md": "release-plan.md" }`; `open = ["release-plan.md"]`.
- `settings = { "workbench.editorAssociations": { "release-plan.md": "markdown-okf-schema-studio.editor" } }`;
  no Studio setting.
- `checks = { editMode: "off", paste: false }`.
- `export const STAGE`: the text of `stage/release-plan.md`, lines joined with `\n`, ending with one
  newline. `export const EXPECTED = STAGE.replace("on Friday", "on Thursday")`.
- Constants: `BOX = "[data-sphinx-preview-block-editor] textarea"`,
  `SELECTED = '#sphinx-myst-preview-content [data-sphinx-preview-block-selected="true"]'`,
  `SENTENCE = "Run these steps in order, one person per step."`.
- `selected(frame)`: the selected elements (`SELECTED`), each as `{ tag, classes, text }` (text
  normalised, first 80 characters), and whether a `BOX` is open; used after every press and in
  every error message.
- `DELETE_WORD = process.platform === "darwin" ? "Alt+Backspace" : "Control+Backspace"` (never
  `ControlOrMeta`, which is Cmd+Backspace on macOS, keyboard-nav-Q9).
- `setup(t)`, off camera:
  1. `release-plan.md` in the workspace equals `STAGE`, else throw.
  2. Reading mode as `comment-thread`'s `setup` (click `[data-sphinx-preview-edit-toggle]` while
     `data-sphinx-preview-edit-mode` is `"on"`); `t.record("readingMode", mode)`; throw when not
     `"off"`.
  3. The toolbar expanded, as `diff-side-by-side`'s `setup` (click
     `[data-sphinx-preview-toolbar-collapse]` when `data-sphinx-preview-toolbar-state` is
     `"collapsed"`, wait for `"expanded"`, else throw), so the Edit toggle is in view.
  4. Scrolled to the top; no element matches `SELECTED`, else throw.
  5. The keyboard focus (keyboard-nav-Q8): one `t.click()` in the blank right margin of the page
     (`#sphinx-myst-preview-content` box: `x = right edge + 40` clamped inside the webview, `y` at
     its middle); then `selected(frame)` is still empty and the mode still `"off"`, else throw.
  6. Park the pointer in the bottom right corner of the page, off every block, the toolbar and the
     zoom rect of `run` step 5; `t.sleep(800)`.
- `run(t)`, timed with `until(seconds)` at the storyboard's times. Each press is `t.press(chord, id)`
  with the badge id of section 2; after each, poll at most 1 s for the expected state, else throw
  with `selected(frame)` (a failure is a finding against the feature, not a scenario fix; re-read
  `t.frameOf()` between polls, the page may re-render):
  1. 0.6 s, `t.press("e", "edit")`: `data-sphinx-preview-edit-mode` is `"on"`;
     `t.keyFrame("edit-on")` at 1.4 s.
  2. 2.2 s, `t.press("ArrowDown", "down")`: one selected element, the `h1` "Release plan".
  3. 3.6 s, `t.press("ArrowDown", "down")`: one selected element, the admonition (class
     `admonition`, its text starts with "Before the release"); `t.keyFrame("admonition-selected")`
     at 4.4 s.
  4. 5.2 s, `t.press("Enter", "enter")`: a `BOX` opens; its value starts with
     `:::{note} Before the release` and ends (trimmed) with `:::`; `t.keyFrame("admonition-editor")`
     at 6.2 s. 7.0 s, `t.press("Escape", "escape")`: no `BOX`, the admonition selected,
     `release-plan.md` on disk equals `STAGE`; `t.keyFrame("admonition-back")` at 7.5 s.
  5. 8.0 s, `t.zoom("admonition", rect)`: the admonition's box padded by 24 px, at most 2x (the kit
     caps it).
  6. 8.6 s, `t.press("ArrowRight", "right")`: the selected element's text is `SENTENCE`. When the
     admonition title is selected instead, throw "Right selected the admonition title, not its first
     inner block" with `selected(frame)`: the Driver stops and reports it as a finding against
     `SwRS-MDOKFSTUDIO-BLOCK-254` (draft review note "The admonition title"); the clip waits.
     `t.keyFrame("sentence-selected")` at 9.4 s.
  7. 10.2 s, `t.press("ArrowDown", "down")`: the selected element is the `ul` inside the admonition
     (it holds "Tag the release on Friday" and "Post the announcement");
     `t.keyFrame("list-selected")` at 11.0 s.
  8. 11.8 s, `t.press("ArrowRight", "right")`: the selected element is the first `li`, its own text
     "Tag the release on Friday" (keyboard-nav-Q7); `t.keyFrame("item-selected")` at 12.4 s.
  9. 13.4 s, `t.press("Enter", "enter")`: a `BOX` opens holding the first item only (its value, with
     or without the list marker, contains "Tag the release on Friday" and neither "Build the
     packages" nor ":::"); the box is focused and its caret is at the end of its text content
     (`selectionStart === selectionEnd`, at the trimmed end); `t.record("itemEditor", value)`;
     `t.keyFrame("item-editor")` at 14.2 s.
  10. 15.0 s, `t.press(DELETE_WORD, "delete-word")`: the value no longer holds "Friday" and ends
      (trimmed) with "on"; anything else deleted throws.
  11. 15.4 s, `t.page.keyboard.type("Thursday", { delay: 75 })` (no badge, as `comment-thread` types
      its comment); the value contains "Tag the release on Thursday"; `t.keyFrame("word-changed")`
      at 16.2 s.
  12. 16.8 s, `t.press("ControlOrMeta+Enter", "save")`: within 3 s no `BOX` is open and one selected
      element, the first `li`, reads "Tag the release on Thursday".
  13. 17.4 s, `t.mark("1", box of that li, padded by 6 px)`; 19.0 s, `t.unmark("1")`; 19.2 s,
      `t.unzoom("admonition")`; `until(20.0)`. The pointer never moves in `run`.
  14. Loop seam fallback (keyboard-nav-Q10), only when the trial's seam SSIM fails: 19.4 s,
      `t.press("Escape", "escape")` (the same `Badge escape` row), the selection goes up to the list;
      the review notes and the PR say it was used.
- `verify(t)`: no `BOX` open; `release-plan.md` on disk (`t.workspaceFile`, after the auto-save),
  polled up to 3 s, equals `EXPECTED` byte for byte; else throw with the text on disk. Returns
  `{ itemEditor }` from `t.notes`.

### 4. Trial take, take and render

On Windows, on this machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`), the scratch folder outside the user's profile:

```bash
just dev
just package                                   # out/reports/package/markdown-okf-schema-studio.vsix
CLIP_SCRATCH=C:/okfclip just clip keyboard-navigation doctor
CLIP_SCRATCH=C:/okfclip just clip keyboard-navigation all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

(PowerShell: `$env:CLIP_SCRATCH = "C:/okfclip"` first.)

- The trial take (recipe section 1, adapted): (a) the webview and the toolbar's Edit toggle are in
  the frames; (b) after the margin click, `E` turns edit mode on (`run` step 1); (c) Right on the
  admonition selects the sentence, not the title (step 6); (d) Right on the list selects its first
  item (step 8); (e) Enter on the item opens it alone, caret at the end (step 9); (f) Ctrl+Backspace
  deletes "Friday" only (step 10: a native text box key Studio does not take); (g) no badge
  overlaps another in the frames (a badge shows 1.2 s and fades over 0.33 s); (h) the retimed rate
  is at least 15 fps; (i) the loop seam SSIM in [0.98, 1.0), else the fallback of `run` step 14,
  and if still failing, the PR says so and the owner decides on a retake (Q10).
  A failure of (b) to (f) is a finding against the feature: the Driver stops and reports it with
  the frames and `selected(frame)`, and does not change the scenario around it. The other failures
  follow the recipe.
- The trial's pictures and measured times go into `clip.md` (keyboard-nav-Q3); `Length` and every
  time follow the take (playback rate inside 0.77 to 1.3), in the same commit as the render; the
  three captions stay end to end from 0 to `Length`, the mark inside the zoom hold.
- GIF over 3 MB at the ladder's last step: shorten `Length` in `clip.md` and retake, never ship it
  heavier.
- Commit together (recipe rule): `clip.md`, `scenario.mjs`, `stage/release-plan.md`,
  `keyboard-navigation.mp4`, `.webm`, `.gif` (Git LFS through `.gitattributes`), `poster.png`,
  `contact-sheet.png`, `first-last.png`, `frames/*.png`, `check.json`.

### 5. Tests (no kit code change)

Each reads the shipped files from the repository, path from the test file's own location, at the
head under test, never a copy. Run by `just clip-kit-test` inside `just check`:

- `docs/demo-video/clip-kit/lib/storyboard.test.mjs` gains "the shipped keyboard-navigation clip.md
  reads as the clip the owner reviews", modelled on the `slash-menu-grid` case: `parseClip` gives
  1280x720, 15 fps, a `Length` above 12 and at most 30 (the committed value); the three captions
  (`**` stripped) "Press E, then the arrows pick a block", "Right goes one level deeper", "Change a
  word and save, no mouse at all", end to end from 0 to `Length`; `badges` deep-equal to
  `{ edit: "E", down: "↓", enter: "Enter / ↩", escape: "Esc", right: "→", "delete-word": "Ctrl+⌫ / ⌥⌫", save: "Ctrl+Enter / ⌘↩" }`;
  zoom `admonition`; one mark `1` inside the hold; `expectedPaste` null. With a take of the eleven
  presses in order (`edit`, `down`, `down`, `enter`, `escape`, `right`, `down`, `right`, `enter`,
  `delete-word`, `save`, plus `escape` when the fallback was filmed), zoom `admonition`, mark `1`:
  `validateStory` passes on `win32`, and on `darwin` throws
  `/the badge "delete-word" reads "Ctrl\+⌫ \/ ⌥⌫", which names Ctrl/u` (keyboard-nav-Q9; the
  assertion's comment names the follow-up of "The badge of the word delete").
- Same file: "the stage of the keyboard-navigation scenario is the shipped stage file, and the save
  changes one word": the shipped `stage/release-plan.md` equals the scenario's `STAGE` byte for byte
  (as the `theme-switch` case); `STAGE` holds "Friday" once; `EXPECTED` differs from `STAGE` on line
  6 only, "Tag the release on Friday" to "Tag the release on Thursday".
- `docs/demo-video/clip-kit/lib/check.test.mjs`: "the shipped scenarios declare their checks ..."
  gains `keyboard-navigation` (its title names it): `resolveChecks` gives
  `{ editMode: "off", paste: false }`.
- `test/site/siteClips.test.ts`: "the shipped editing page plays the keyboard navigation clip as
  video", modelled on "the shipped editing page plays the list drag clip as video": reads the
  shipped `docs/user/editing.md`, renders it with `renderMyst` and `clipVideos`, asserts
  `<video src="../demo-video/clips/keyboard-navigation/keyboard-navigation.webm"` and that
  `keyboard-navigation.webm`, `.gif` and `poster.png` exist; marker
  `// @tests_req SwRS-MDOKFSTUDIO-CORE-095` (an added test of an existing SwRS, no SwRS text
  change); then `just requirements-update`.

### 6. Docs

- `docs/user/editing.md`: after the paragraph "A list has three levels: ... whose editor then
  opens.", indented as the drag clip's image is in its bullet, the image
  `![In edit mode, from the keyboard only: E turns edit mode on, Down selects a note admonition, Enter opens it and Escape closes it, Right goes inside it, Down reaches its list, Right selects the first item, Enter opens it, one word is changed and Ctrl+Enter saves](../demo-video/clips/keyboard-navigation/keyboard-navigation.gif)`
  (the recipe: the GIF under the entry of the feature).
- No change to the recipe, the glossary, the writing skill, `README.md`, `CHANGELOG.md` or
  `docs/releases-notes/` (no `feat` or `fix` commit).

### 7. Commits and the pull request

- Commits by area (Conventional Commits; no scope on `docs` or `test`):
  `docs: add the keyboard navigation feature clip` (clip folder, `docs/user/editing.md`),
  `test: check the keyboard navigation clip's storyboard, stage and docs page` (the kit test cases,
  `siteClips.test.ts`, the files `just requirements-update` changes).
- The PR's base is the branch of `clip-the-advanced-renderings-tour` in the batch-09 stack; it is
  opened as a draft (`gh pr create --draft`) and stays a draft until the owner approves the
  storyboard and the clip (keyboard-nav-Q3); the agent does not mark it ready.
- The body follows `.github/PULL_REQUEST_TEMPLATE.md`, `.agents/guidelines/pull-request.guidelines.md`
  and the recipe's clip PR rule: the GIF inline from
  `https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/keyboard-navigation/keyboard-navigation.gif`,
  the MP4 and WebM linked the same way at the same head; after each push of a new render the links
  move to the new head (`gh pr edit <n> --body-file <file>`); check that the GIF plays in the
  rendered PR page, else the recipe's `-assets` fallback.
- A section "Deviation from the feature clip process": the storyboard review moved from before the
  take into this PR (keyboard-nav-Q3); the take filmed from the Griller's draft; an *(on screen)*
  row the owner changes is a render (`just clip keyboard-navigation render` then `check`), a
  *(filmed)* row a retake, a follow-up of this CR. It links `clip.md` for the review.
- What the clip proves (eleven real key presses in a real VS Code window, no pointer move: edit mode
  on, the selection through three levels, the item edited and saved, the file changed by one word:
  the take's `run` checks and `verify`) and what the owner judges (motion, rhythm, 20 s, the badges'
  pace, the loop as watched).
- "Autonomous decisions" names for the owner: `E` turns edit mode on and Enter opens the item, where
  the request pressed `e` (keyboard-nav-Q6, the owner's to confirm); the second Right selects the
  first item, not the list (Q7); the `Ctrl+⌫ / ⌥⌫` badge passes the kit on Windows only, no kit
  change (Q9, this spec); the docs placement; the key frame names; the measured times; the loop
  seam fallback if used; `CLIP_SCRATCH`.

## Out of scope

- Any change to `src/`, to an SwRS text, to the writing skill, to the recipe or to the clip kit's
  code (beyond test cases); the length bound (owned by `clip-the-advanced-renderings-tour`).
- `isCombinedBadge` accepting `⌥` and a macOS or Linux take (open question 1).
- Left, Up, Shift selection, Alt+Up/Down moves, the item editor's Down at its end, tables and cells,
  the mouse.
- The clip in release notes or the announcement (a release CR does it); a retake after the owner's
  review (a follow-up, Q3); marking the PR ready before the owner approves.

## CI

No CI job changes. The new test cases run in `just check` through `just clip-kit-test`, inside the
existing `ci-static` job (Linux and Windows, `.github/workflows/ci.yml`); the site test runs where
`test/site/` tests run today.

- Environment: the CI machine set up by `just dev-ci` from the lock files, Node.js 24 from `.nvmrc`
  through `fnm`. Absent there and present locally: `ffmpeg`, the kit's scratch folder, the VS Code
  download, Remotion, a display. The new tests need none of them: the shipped `clip.md`,
  `scenario.mjs` (loaded, never run; `DELETE_WORD` reads `process.platform` at import, a constant,
  no side effect) and `stage/release-plan.md`, the shipped `docs/user/editing.md` and the committed
  clip files (Git LFS checked out as CI does for the merged clips' site tests).
- Before the push: `just clip-kit-test`, `just check` and `just ci-static` on Windows.
- Only the first CI run proves the Linux leg (the dynamic `import` of the scenario from a
  repository path, the byte comparison of the stage with LF endings).

## Host and default matrix

The keys depend on the host (the save modifier, the word-delete chord, the badge the kit accepts),
and the start mode depends on the document's saved state (LIFE-172).

| Host | Settings and state | Expected | Proof |
| --- | --- | --- | --- |
| Windows 11, CDP keys | every setting at its default, saved state not in edit mode | reading mode at frame 0; the eleven presses as `run`; `release-plan.md` = `EXPECTED` | the take's `run` checks and `verify`, `check.json` ("Studio in reading mode at the start", "scenario verify passed") |
| Windows 11 | a saved state in edit mode left by an earlier take | `setup` turns reading mode on before frame 0 | `setup`'s throw when the mode is not `"off"` |
| macOS | same | Cmd+Enter saves, Option+Backspace deletes the word; the kit refuses the badge `delete-word` | not filmed; the `darwin` refusal is asserted by section 5 |
| Linux | same | as Windows (Ctrl+Backspace, Ctrl+Enter) | not proved |

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows; the storyboard, stage and checks cases
   read the shipped `clip.md`, `stage/release-plan.md` and `scenario.mjs` at the head under test
   (including the `win32` pass and the `darwin` refusal of `delete-word`); the site test reads the
   shipped `docs/user/editing.md`.
2. The trial's nine points (section 4), with what was seen for (b) to (g) (frame names, the
   recorded `itemEditor`).
3. `CLIP_SCRATCH=C:/okfclip just clip keyboard-navigation all --vsix ...` passes; `check.json` shows
   `passed: true`, the line "mp4 duration within 5 to 30 s" ok, MP4 and WebM 1280x720 at 15 fps,
   MP4 duration equal to `Length` within one frame, GIF within 3 MB with its ladder step, loop seam
   SSIM in [0.98, 1.0), "Studio in reading mode at the start", no paste line, `verifyPassed: true`,
   playback rate inside 0.77 to 1.3, platform `win32`, extension source `vsix`.
4. The take's `run` passed steps 1 to 12 and `verify` found `release-plan.md` equal to `EXPECTED`.
5. The agent looks at the contact sheet and every key frame: reading mode at frame 0 with no
   selection ring and no hover, the Edit toggle on after `E`, the ring on the heading, the
   admonition, its sentence, its list, its first item in turn, the admonition editor then the item
   editor, "Thursday" in the item, the badges (`E`, `↓`, `Enter / ↩`, `Esc`, `→`, `Ctrl+⌫ / ⌥⌫`,
   `Ctrl+Enter / ⌘↩`) readable and never two at once, the three texts in turn, mark 1 on the saved
   item inside the zoom, the pointer never moving, no personal name or path, no dirty tab. What was
   not checked (motion, rhythm, the loop as watched) is said.
6. `just requirements-update` leaves the tree clean after its commit; `just preflight` passes (on
   Windows, its static stage).
7. The PR is a draft on the tour CR's branch; its body plays the GIF, links the MP4 and WebM at the
   head sha and holds the "Deviation from the feature clip process" section.

## Open questions

None. The one question of the first draft is answered (keyboard-nav-Q11, decided by the Chief of
Staff): keep `Ctrl+⌫ / ⌥⌫` with no kit change and a Windows take only, as this specification does.
The macOS acceptance of `⌥` in `isCombinedBadge` is a separate follow-up.
