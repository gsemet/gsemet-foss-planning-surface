# Feature clip: drag a list item by its handle

Short name: `clip-drag-list`. No tracker issue (verbal request of the owner, 2026-11-25).

## Goal

The owner asked for clips like the raw copy clip on the best features of Studio, one CR per
clip; this is one of them. In edit mode the reader drags a list item by its handle: the item moves
with its sub-items, the ordered list keeps its numbers in order, and the raw text of the same file,
open beside the page, changes to match, which shows that the move is a clean edit of the source.
One continuous shot: the drag in Studio on the left, then a zoom on the raw text on the right; two
captions in turn, two orange marks in turn, 1280x720 at 15 fps, no card, the logo top right, a
loop; MP4, WebM and GIF; a PR whose description plays the clip.

The clip shows Studio's existing list item move (CR 432, `src/page/features/listItemMove.ts`,
`src/page/modules/listItemMove.ts`, `SwRS-MDOKFSTUDIO-BLOCK-262`); no behaviour of the extension
changes.

## Dependency and base

This CR runs after `short-demo-video-of-the-smart-raw-markdo` (CR-484, short name
`raw-copy-demo`, `depends.json`). That CR gives the kit and the recipe this clip uses: the Markdown
storyboard contract (`## Clip` table with `Length`, `Size`, `Frame rate`, `Outputs`, `Cards`,
`Logo`, `Setting filmed`, `Filmed on`, `Stage`; one `## <n>. <beat>` section per beat with `Time`,
`Shot *(filmed)*`, `Text <n> *(on screen)*`, `Zoom`, `Mark <id>`), captions in turn, marks in turn,
`Size` and `Frame rate` read from the storyboard, key frames `frames/<NN>-mark-<id>.png`, the parser
tests `docs/demo-video/clip-kit/lib/storyboard.test.mjs` run by `just clip-kit-test` inside
`just check`, and the clip PR rule (the GIF inline from the PR's head, the MP4 and WebM linked at the
same head).

- Base: CR-484's branch while it is not merged (stacked), else `origin/main` once it holds it
  (fetch first: the local `main` is behind `origin/main`).
- Where CR-484 lands differently from its spec (a field name, a frame name, a test file name), this
  CR follows what it merged and says so in the PR's "Autonomous decisions".

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| clip-drag-list-Q1 | Filed from the owner's request: one CR per clip, this clip among seven | Goal |
| clip-drag-list-Q2 | The captions, stage and timing are the Griller's proposal, the storyboard draft `work/storyboard/clip.md` with its stage `work/storyboard/stage/release-steps.md`; the owner reviews them at the recipe's storyboard gate | "Where this spec differs from the draft", sections 1 to 4 |
| clip-drag-list-Q3 | The batch does not wait for the storyboard approval before the take: it films the trial take from the draft, puts its pictures in the storyboard, renders the clip and opens the PR with the clip watchable; the owner reviews the storyboard and the clip on that PR, which stays a draft until the owner approves (the gate is moved after the take, not dropped); the deviation from the recipe's order is reported in this spec and in the PR body; a retake after the owner's review is a follow-up of this CR | "The storyboard gate, moved after the take", section 8, "Out of scope" |

From `01-intent.md` and the draft: 1280x720 at 15 fps, two captions in turn, several marks in turn,
no card, the logo top right, a loop, the clip in `docs/demo-video/clips/drag-list-item/`.

## The storyboard gate, moved after the take

The recipe `docs/demo-video/guidelines/feature-clip-process.guidelines.md`, a project guideline, as
CR-484 leaves it (section "The storyboard first"), has the maintainer review and edit the storyboard
draft before the take. Q3 moves that gate after the take, into the pull request; it does not drop
it. This is a deviation from a project guideline, decided by the Chief of Staff under the owner's
overnight autonomy, and reported as such:

- the batch films a trial take from the draft, puts its pictures and measured times in the
  storyboard, moves it to `docs/demo-video/clips/drag-list-item/clip.md` with `status: draft`,
  films the take, renders and opens the PR;
- the PR is a draft (`gh pr create --draft`) until the owner approves the storyboard and the clip in
  it; the agent never marks it ready; the PR body reports the deviation (section 8);
- the recipe's storyboard order is not changed by this CR.

## What the code settles

Facts of Studio on `origin/main`, read to name the real controls (no choice made here):

- **The handles** are `button.okf-list-editor-handle.okf-list-item-handle` in the layer
  `[data-okf-list-handle-layer]`, one per item of every list of two items or more, in edit mode only;
  each has `data-okf-list-item-line` (the item's `data-sphinx-source-line`), `aria-label` "Move
  list item", `title` "Drag to move item (Alt+Up, Alt+Down)" and `draggable="true"`
  (`src/page/features/listItemMove.ts`). They are visible as soon as edit mode is on, not only on
  hover: no rule of `src/core/preview/styles/` hides them (`frontmatterEditorStyles.ts` gives them
  the description colour, `editModeStyles.ts` places them).
- **The drag is HTML drag and drop**: `dragstart` on the handle, `dragover` and `drop` on the
  document. While dragging, the item gets `data-okf-list-item-dragging` (opacity 0.45) and the
  sibling under the pointer gets `data-okf-list-item-drop="before"` or `"after"` (a 2 px line in the
  focus colour); the half of the sibling's box decides before or after. On drop the page asks the
  host for the list's lines, moves the item with all its lines (`moveListItem`), renumbers an
  ordered list and saves the whole list as one edit; the page renders anew.
- **A real CDP mouse drag reaches it in a real window**: `test/integration/listItemMoves.ts`
  (`dragTo`: press on the handle's centre, a small move of 6 and 8 px, then the move to the target,
  150 ms, release) moves an item with its sub-list. No floating copy of the item follows the pointer
  in a CDP drag.
- **Edit mode** is off in a fresh profile (`src/page/runtime.ts`: the saved choice, else off); the
  toggle is `[data-sphinx-preview-edit-toggle]`, the state `data-sphinx-preview-edit-mode` on the
  frame's `html` (`"on"` or `"off"`).
- **Studio's custom editor** `markdown-okf-schema-studio.editor` has priority `option`: a `.md` file
  opened by path opens in the text editor. Studio declares no `supportsMultipleEditorsPerDocument`,
  so the same file cannot show in two Studio tabs; a Studio tab and a text editor of the same file
  can show side by side, and an edit made by the page shows at once in the text editor (one
  document).

## Where this spec differs from the draft

| Draft | This spec | Why |
| --- | --- | --- |
| `Format` row (size, rate, outputs in one cell) | `Size *(on screen)*` = `1280x720 16:9`, `Frame rate *(on screen)*` = `15 fps`, `Outputs` = the rest | the kit, as CR-484 leaves it, reads `Size` and `Frame rate` as their own fields |
| The zoom described in the `Time` and `Shot` rows only | a row `Zoom` = `raw, hold to 9.5 s` (or the take's hold) in section 2 | the kit reads the zoom from a `Zoom` row |
| "Pictures: from the batch's trial take" | section 1: `frames/drag.png` (the pointer over "Tag the release.", the drop line shown) and `frames/dropped.png` (the new order in the page and the raw text); section 2: `frames/04-mark-1.png`, `frames/05-mark-2.png` | the clip has no key press, so the kit's `01-selected` and `02-pasted` frames do not exist; the scenario names its own key frames with `t.keyFrame` (section 5) |
| Mark 1 "around the moved lines, "1. Build the packages." and its two sub-items" | the same words without the comma after "lines" | a `Mark` row reads `<what>, <from> to <to> s`: a comma inside `<what>` risks a misread |
| Status "draft for the owner's review", the opening paragraph of a review draft | `status: draft`, the opening paragraph of a live storyboard | the file becomes the live storyboard in the clip folder (recipe) |
| `Filmed on`: "to be filmed by the batch"; `Setting filmed`: "none" | Windows, the VS Code version of `check.json`, the extension version, "VSIX built from the branch"; "none: every setting at its default" | the batch's take |
| Review note "The handle shows on hover in edit mode only" | "The handles show as soon as edit mode is on; the pointer reaches the handle before the press" | settled by the code (above) |
| Review note on HTML drag and drop: "whether Chromium turns that mouse drag into drag events there is the first thing the trial proves" | kept as the trial's first proof (section 4), with the integration test as the evidence that it works in a real window; the storyboard's note says the CDP drag shows no floating copy of the item | settled by the code and the tests |
| Review note "Reopen Editor With, in the second group" | the off-camera layout of section 3: the file opens as text, `Split Editor Right`, then the left group is reopened with Studio (`Reopen Editor With...`) | the same two editors; the order of steps that gives Studio on the left and the text on the right |
| Times 10.5 s, 0.9, 1.2, 2.6, 3.0, 4.2, 4.4, 9.5 s, marks 5.0 to 6.6 s and 6.6 to 8.2 s | the take's own times, same beats and order | the recipe: the storyboard follows the take |

Everything else is carried as written: the stage, the one drag, the layout (Studio left in edit
mode, the text editor right), the zoom on the raw list with the heading in view, the two texts with
their accents, the two marks and their order, the expected result, and the loop note.

## What changes

All paths are relative to the repository root.

### 1. The stage: `docs/demo-video/clips/drag-list-item/stage/release-steps.md`

The draft's stage, exactly (LF line endings, a final newline):

```markdown
# Release steps

1. Tag the release.
2. Build the packages.
   - Linux and macOS
   - Windows
3. Run the smoke tests.
4. Publish the notes.
```

The expected text after the drag (the scenario's `verify`, and the storyboard's "Expected result"):

```markdown
# Release steps

1. Build the packages.
   - Linux and macOS
   - Windows
2. Tag the release.
3. Run the smoke tests.
4. Publish the notes.
```

The sub-list has its own two handles (a list of two items): they are on screen, not used.

### 2. The live storyboard: `docs/demo-video/clips/drag-list-item/clip.md`

The draft `work/storyboard/clip.md`, changed only as "Where this spec differs from the draft"
says; times are the draft's until the take sets them (section 4), in the same commit as the
render. The content:

````markdown
---
title: Feature clip drag-list-item
status: draft
date: <the day of the commit>
---

# Feature clip: drag-list-item

**This is the live storyboard.** The clip is built from this file: edit any row marked
*(on screen)*, save, and run `just clip drag-list-item render`, then `check`. Rows marked
*(filmed)* describe the footage of the take: changing them means a new take. `**bold**` in a text
takes the orange accent.

The clip is one continuous shot: the drag in the page on the left, then a zoom on the raw text on
the right. It shows two texts in turn.

## Clip

| Field | Content |
| --- | --- |
| Length | 10.5 s |
| Size *(on screen)* | 1280x720 16:9 |
| Frame rate *(on screen)* | 15 fps |
| Outputs | silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | none: every setting at its default |
| Filmed on | Windows, VS Code <version from check.json>, extension <version> VSIX built from the branch |
| Stage | `stage/release-steps.md` opened twice: in Studio (left, edit mode) and in the built-in text editor (right) |

## 1. Drag the item by its handle

![The item "Build the packages." dragged by its handle above "Tag the release.": the drop line shows where it lands](frames/drag.png)

![The new order in the page and in the raw text](frames/dropped.png)

| Field | Content |
| --- | --- |
| Time | 0 to 4.2 s (pointer on the handle at 0.9 s, press at 1.2 s, drag 1.2 to 2.6 s, drop at 2.6 s, the raw text changes about 3.0 s) |
| Shot *(filmed)* | Studio in edit mode on `release-steps.md` (left), the same file as raw text (right). The pointer moves to the handle left of item 2, "Build the packages." (title "Drag to move item (Alt+Up, Alt+Down)"), presses and drags it up above item 1, "Tag the release.", then drops. The item moves with its two sub-items; the page shows 1 Build the packages, 2 Tag the release, 3 Run the smoke tests, 4 Publish the notes. The raw text on the right changes to the same order. |
| Text 1 *(on screen)* | Drag a list item by its **handle**, sub-items come along |

## 2. Zoom on the raw text

![Mark 1 on the moved lines in the raw text](frames/04-mark-1.png)

![Mark 2 on the numbers 1. to 4.](frames/05-mark-2.png)

| Field | Content |
| --- | --- |
| Time | 4.2 to 10.5 s (zoom from 4.4 s, held to 9.5 s, then back to the start for the loop) |
| Shot *(filmed)* | Zoom (at most 2x) on the list in the text editor (right), the heading in view. |
| Zoom | raw, hold to 9.5 s |
| Mark 1 *(on screen)* | Orange outline around the moved lines "1. Build the packages." and its two sub-items, 5.0 to 6.6 s |
| Mark 2 *(on screen)* | Orange outline around the numbers 1. to 4., 6.6 to 8.2 s |
| Text 2 *(on screen)* | The **raw text** follows, numbers kept in order |

Expected result, the scenario's check: `release-steps.md` on disk (auto-save is on) is exactly this
text:

```markdown
# Release steps

1. Build the packages.
   - Linux and macOS
   - Windows
2. Tag the release.
3. Run the smoke tests.
4. Publish the notes.
```

## Review notes

- The handle uses HTML drag and drop (`draggable`, `dragstart`, `dragover`); the kit's mouse goes
  through CDP into the preview webview. A CDP drag shows no floating copy of the item: the drag
  shows as the item faded in place and a line where it will land; the item moves there on release.
- The handles show as soon as edit mode is on; the pointer reaches the handle before the press, and
  `setup` checks edit mode is on.
- Opening the same file in the text editor beside Studio is done off camera; both show one file, so
  the raw text updates as soon as the page writes.
- The raw screencast runs at about <rawFps from check.json> frames per second: the pointer is drawn
  smooth by the kit, but the drop line and the page change by steps.
- The clip ends with the new order and starts with the old one: the loop seam relies on the kit's
  return to the start.
````

### 3. The scenario: `docs/demo-video/clips/drag-list-item/scenario.mjs`

In the style of `clips/raw-copy-balance-edges/scenario.mjs`; the header comment says what is filmed
and that every text and time is in `clip.md`. Selectors and attributes are Studio's own (section
"What the code settles").

- `stage = { "stage/release-steps.md": "release-steps.md" }`; `open = ["release-steps.md"]` (it
  opens in the text editor: priority `option`, no `workbench.editorAssociations`); `settings = {}`.
- `checks = { editMode: "on", paste: false }` (section 5).
- `EXPECTED` holds the expected text of section 1 (lines joined with `\n`, a final `\n`).
- Helpers, local to the scenario:
  - `editorLines(page)`: the texts and rectangles of the non-empty
    `.monaco-editor .view-lines .view-line` of the right editor (the text editor; Studio's tab has
    no Monaco view lines of the document), top to bottom, non-breaking spaces turned into spaces;
  - `lineSpan(page, n, start, end)`: the rectangle of the characters `[start, end)` of the n-th
    non-empty line of that editor (as the raw copy trial's `lineSpan`);
  - `itemBox(frame, text)`: the `#sphinx-myst-preview-content li` whose own first text starts with
    `text` (the way of `handleOf` in `test/integration/listItemMoves.ts`), its box in page
    coordinates (`locator.boundingBox()`), its first line's top and height, and its
    `data-sphinx-source-line`;
  - `handleOf(frame, text)`: the centre, in page coordinates, of
    `[data-okf-list-handle-layer] .okf-list-item-handle[data-okf-list-item-line="<line>"]` of that
    item;
  - `pageOrder(frame)`: the own first texts of the top-level `ol`'s `li` children, in order.
- `setup(t)`, off camera:
  1. the layout: focus the text editor (`page.locator(".monaco-editor").first().click()`); `Split
     Editor Right` (`page.keyboard.press("ControlOrMeta+Backslash")`; the same file as text in a
     second group on the right); focus the first group (`ControlOrMeta+1`); the Command Palette
     (`ControlOrMeta+Shift+P`), type `Reopen Editor With`, Enter, type `Markdown OKF-Schema Studio`,
     Enter; wait for `t.frameOf()`. Then Studio is on the left, the text editor on the right. Each
     step that does not give its result throws, naming the step (the take writes `failure.png`);
  2. edit mode on: click `[data-sphinx-preview-edit-toggle]` in the frame, poll the frame's
     `data-sphinx-preview-edit-mode` (re-reading the frame, as `readingMode` does in the raw copy
     scenario) until `"on"`, then until the frame holds 6 handles (4 items, 2 sub-items);
     `t.record("readingMode", mode)` (the key keeps its name: it holds the value of
     `data-sphinx-preview-edit-mode`, `"on"` here); throw when it is not `"on"`;
  3. park the pointer in Studio's blank area below the list, off every block (for example 120 px
     below the bottom of the `ol` and 200 px right of its left edge, read from the frame), with
     `t.moveTo(x, y, 0.1)`, then `t.sleep(500)`: frame 0 and the last frame show no hover.
- `run(t)`, the filmed action, timed with `until(seconds)` as in the raw copy scenario (the draft's
  times):
  1. at 0.3 s, `t.moveTo` (0.6 s) to the centre of the handle of "Build the packages.";
  2. at 1.2 s, the press: `t.ev("click", t.pointer)` (the kit's ripple), `await t.page.mouse.down()`,
     `t.moveTo(x + 6, y + 8, 0.1)` (the move that starts an HTML drag, as `dragTo`), then `t.moveTo`
     (about 1.1 s, to end by 2.4 s) to the point 40 px right of the left edge of the item "Tag the
     release." and a quarter of its first line's height below its top (the upper half of its box:
     the drop line shows before it); `t.keyFrame("drag")` (section 5); at 2.6 s,
     `await t.page.mouse.up()`;
  3. wait, at most 2 s, until `editorLines` reads the non-empty lines of `EXPECTED` and `pageOrder`
     reads "Build the packages.", "Tag the release.", "Run the smoke tests.", "Publish the notes.",
     with the two sub-items inside the `li` "Build the packages."; else throw with what both show (a
     finding against the feature, never a scenario fix); `t.keyFrame("dropped")` at about 3.6 s;
  4. at 4.4 s, `t.zoom("raw", rect)`: the rectangles of the editor's non-empty lines (the heading
     to "4. Publish the notes."), padded by 24 px;
  5. at 5.0 s, `t.mark("1", rect)`: the union of the editor lines "1. Build the packages.",
     "   - Linux and macOS" and "   - Windows", with 6 px and 3 px of air as in the raw copy
     scenario; at 6.6 s, `t.unmark("1")`;
  6. at 6.6 s, `t.mark("2", rect)`: from the left edge of `lineSpan` of "1." (characters 0 to 2 of
     the line "1. Build the packages.") to the bottom of `lineSpan` of "4." (the line "4. Publish the
     notes."), as wide as the two characters, with the same air (the column of the numbers; the
     sub-items' dashes, at column 3, stay outside); at 8.2 s, `t.unmark("2")`;
  7. at 9.5 s, `t.unzoom("raw")` and `t.moveTo(home.x, home.y, 0.6)`; `until(10.5)`.
- `verify(t)`: poll `t.workspaceFile("release-steps.md")` for up to 3 s (auto-save is
  `afterDelay`) and throw `release-steps.md does not hold the expected text. On disk:
  ${JSON.stringify(text)}` when it never equals `EXPECTED`; return `{ text }`.

### 4. Trial take, take and render

On Windows, on this machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`):

```bash
just dev
just package                                   # out/reports/package/markdown-okf-schema-studio.vsix
just clip drag-list-item doctor
just clip drag-list-item all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

- The trial take (recipe section 1, adapted): (a) the preview webview is in the frames; (b) the
  CDP mouse drag by the handle moves the item (step 3 of `run` passes); (c) the raw text follows
  (same step); (d) the retimed rate is at least the storyboard's frame rate. If (b) fails, stop and
  report: neither Alt+Up on the focused handle nor a scripted call stands in for the drag the clip
  shows, and never OS-level input or capture.
- The trial take's pictures and measured times go into `clip.md` (Q3); when the trial is clean it
  may be the take.
- `Length` and every time in `clip.md` follow the take (playback rate inside 0.77 to 1.3), in the
  same commit as the render; the two captions stay end to end from 0 to `Length`, the marks inside
  the zoom hold.
- Commit together (recipe rule): `clip.md`, `scenario.mjs`, `stage/release-steps.md`,
  `drag-list-item.mp4`, `.webm`, `.gif` (Git LFS through `.gitattributes`), `poster.png`,
  `contact-sheet.png`, `first-last.png`, `frames/*.png`, `check.json`.

### 5. The kit gaps this clip needs: `docs/demo-video/clip-kit/`

The kit, as merged and as CR-484 leaves it, cannot make this clip, for three reasons read in the
code of `origin/main`:

- `lib/check.mjs` always wants "no paste-options widget after the paste"
  (`verify.notes.pasteWidgets === 0`) and "Studio in reading mode at the start"
  (`verify.notes.readingMode === "off"`): an edit-mode clip with no paste fails `check`.
- `lib/encode.mjs` takes its key frames from `take.presses[0]` and `take.presses.at(-1)`: a take
  with no key press throws in `render`.
- The kit's key frames have no picture of a drag in progress or of the result before the zoom,
  which the storyboard shows (one picture per key moment).

So this CR changes the kit, the least the clip needs, with the raw copy clip unchanged
(`check.json` lines, key frame names and outputs as before). Every refusal names the scenario or
`clip.md`, as the kit's messages do.

This CR owns these generic kit changes (the scenario `checks` and the helper `t.keyFrame`, with
`resolveChecks`, `takeLines`, `keyFrameTimes` and their tests): the clips `diff-side-by-side` and
`export-html` reuse them from this CR and do not write their own. They hold whether or not a take
has a key press.

- **Scenario checks.** A scenario may export `checks = { editMode, paste }`: `editMode` `"off"`
  (default) or `"on"`, `paste` `true` (default) or `false`. A pure exported function
  `resolveChecks(checks)` in `lib/check.mjs` applies the defaults and refuses another key or value
  (`scenario.mjs: checks.editMode must be "on" or "off", got ...`). `lib/take.mjs` calls it before
  the window opens and writes the result as `checks` in `verify.json`. A pure exported function
  `takeLines(verify)` in `lib/check.mjs` gives the take's lines, used by `checkClip`:
  "scenario verify passed"; "Studio in reading mode at the start" when `editMode` is `"off"`, or
  "Studio in edit mode at the start" when `"on"`, true when `verify.notes.readingMode` equals
  `editMode`; "no paste-options widget after the paste" only when `paste` is true. `check.json`'s
  `take` gains `checks`; `pasteWidgets` is written only when `paste` is true.
- **Key frames.** A helper `t.keyFrame(name)` in `lib/take.mjs` logs `{ type: "keyframe", name }`;
  `lib/prepare.mjs` writes them in `take.json` as `keyFrames: [{ name, t }]`. A pure exported
  function `keyFrameTimes(take, story)` in `lib/encode.mjs` gives the list `{ file, at }` the step
  writes: `01-selected.png` and `02-pasted.png` only when the take logged a press (as today when it
  did), `03-zoomed.png` when there is a zoom, `<NN>-mark-<id>.png` per mark as CR-484 numbers them,
  and `<name>.png` at `t / story.rate` per key frame. A name must match `^[a-z][a-z0-9-]*$` (it
  starts with a letter, so it never takes a numbered kit name) and be unique, else `render` fails
  naming it.
- **Tests**, in `docs/demo-video/clip-kit/lib/` (`node:test`, Node built-ins only, run by
  `just clip-kit-test` inside `just check`):
  - `check.test.mjs`: `resolveChecks(undefined)` gives `{ editMode: "off", paste: true }`;
    `resolveChecks({ editMode: "on", paste: false })` keeps them; an unknown key, `editMode: "edit"`
    and `paste: "no"` are refused (prepared values: refusal cases no shipped scenario holds).
    `takeLines` on a raw-copy-like `verify` gives the three lines of today, all passing; on a
    drag-like one (`checks` on/false, `readingMode: "on"`) gives "scenario verify passed" and
    "Studio in edit mode at the start", no paste line; `readingMode: "off"` with `editMode: "on"`
    fails its line.
  - `encode.test.mjs` (or the file name the kit's test style gives): `keyFrameTimes` on a take
    with presses, a zoom and three marks gives today's names and the mark frames; on a take with no
    press, a zoom, two marks and the key frames `drag`, `dropped` gives `drag.png`, `dropped.png`,
    `03-zoomed.png`, `04-mark-1.png`, `05-mark-2.png` and no `01-selected.png`; on a take with
    presses and a key frame, both the press frames and the key frame; a name `01-x` or a repeated
    name is refused.
  - `storyboard.test.mjs` (from CR-484) gains a case that reads the shipped
    `docs/demo-video/clips/drag-list-item/clip.md` from the repository (path from the test file's
    own location, at the head under test, never a copy) with `parseClip` and asserts: size
    1280x720, 15 fps, two captions with the draft's words (`**` aside) end to end from 0 to
    `Length`, no badge, zoom `raw`, marks `1` and `2` in turn inside the hold, each with the times of
    its row; and `validateStory` passes with a `take` object with no press, zoom `raw` and marks
    `1`, `2`, on `win32`. If the merged parser misreads a `Mark` row of the shipped file, the row's
    `<what>` words are reworded (never its times, never the parser to fit), said in the PR.
  - A test that reads the shipped `scenario.mjs` of each clip (dynamic `import` from the repository
    path) and passes its `checks` to `resolveChecks`: `drag-list-item` gives on/false,
    `raw-copy-balance-edges` the defaults.

### 6. Docs

- `docs/user/editing.md`: under the paragraph "In edit mode each list item also has a handle on its
  left ... the handles sit left of the box." (inside the "Inline editing" item, indented two spaces
  as `docs/user/settings.md` does for the raw copy clip), the image
  `![In edit mode, the second item of an ordered list is dragged by its handle above the first and moves with its two sub-items: the numbers stay in order and the raw Markdown beside follows](../demo-video/clips/drag-list-item/drag-list-item.gif)`.
- `test/site/siteClips.test.ts`: a test "the shipped editing page plays the list drag clip as
  video", modelled on the settings page one: it reads the shipped `docs/user/editing.md`, renders
  it with `renderMyst` and `clipVideos`, asserts the
  `<video src="../demo-video/clips/drag-list-item/drag-list-item.webm"` and that
  `drag-list-item.webm`, `.gif` and `poster.png` exist; marker
  `// @tests_req SwRS-MDOKFSTUDIO-CORE-095` (an added test of an existing SwRS, no SwRS text
  change); then `just requirements-update`.
- `docs/demo-video/guidelines/feature-clip-process.guidelines.md` (as CR-484 leaves it), in the
  guideline's words ("the agent", "the maintainer", no chantier role, no CR), for the kit changes of
  section 5 only:
  - section 1, the scenario's exports: `checks` (`editMode`, `paste`, defaults) and the helper
    `keyFrame(name)`; a scenario may drive a drag with the exposed `ev("click", ...)`,
    `page.mouse.down()`, `moveTo` and `page.mouse.up()`; "A trial first": (b) and (c) read for a
    drag clip as "the CDP drag moves what the clip shows" and "the result shows on screen";
  - section 2: a picture may be a scenario key frame `frames/<name>.png`;
  - section 6: the reading mode line becomes "Studio in the mode the scenario declares at the
    start", the paste widget line "when the scenario pastes".
  The storyboard order ("The storyboard first") is not changed (Q3 is this clip's deviation).
- `.agents/glossary/common.md`: no change (the "Feature clip" entry of CR-484 holds).
- No change to `README.md`, `CHANGELOG.md` or `docs/releases-notes/` (no `feat` or `fix` commit).

### 7. Host and default matrix

The clip films defaults only (no setting), with a mouse drag; the platform changes only the window
and the off-camera chords of the layout.

| Host | VS Code | Settings | Expected | Proof |
| --- | --- | --- | --- | --- |
| Windows 11, CDP mouse drag | pinned `DEFAULT_CODE_VERSION` (1.147.0 unless moved) | defaults | `release-steps.md` equals the expected text; page and editor show the new order | the take's `run` checks and `verify`, `check.json` ("scenario verify passed") |
| macOS | same | defaults | same | not proved (no macOS take) |
| Linux | same | defaults | same | not proved |

The kit's new tests run on Windows locally and on Linux and Windows in `ci-static`.

### 8. Commits and the pull request

- Commits by area (Conventional Commits; no scope on `build`, `docs` or `test`):
  `build: let a feature clip declare its start mode and its own key frames` (kit and its tests),
  `docs: add the drag a list item feature clip` (clip folder, `docs/user/editing.md`, recipe),
  `test: play the list drag clip on the editing page of the docs site` (`siteClips.test.ts`, the
  files `just requirements-update` changes).
- The PR is opened as a draft (`gh pr create --draft`) and stays a draft until the owner approves
  the storyboard and the clip in it (Q3); the agent does not mark it ready.
- The PR body follows `.github/PULL_REQUEST_TEMPLATE.md`, the PR guideline and the clip PR rule of
  CR-484: the GIF inline from
  `https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/drag-list-item/drag-list-item.gif`,
  the MP4 and WebM linked with the same form at the same head; after each push of a new render the
  links move to the new head (`gh pr edit <n> --body-file <file>`); check that the GIF plays in the
  rendered PR page (if not, the fallback CR-484 settled for its own open question 1).
- The body has a section "Deviation from the feature clip process": the recipe's storyboard review
  before the take was moved after it, into this PR, by the Chief of Staff's decision under the
  owner's overnight autonomy; the take was filmed from the Griller's draft; how a review lands: an
  *(on screen)* row changed by the owner is a render (`just clip drag-list-item render` then
  `check`), a *(filmed)* row is a retake, a follow-up of this CR.
- The body states what the clip proves (a real drag by the handle in a real VS Code window moves an
  item with its sub-items, the numbers stay 1 to 4, the raw text follows: the take's checks and
  `verify`) and what the owner judges (motion, rhythm, the loop as watched, the absence of a floating
  drag image, the texts); it links `clip.md` for the storyboard review.
- "Autonomous decisions": the differences from the draft (section above); the off-camera layout
  steps; the key frame names; the kit changes of section 5 and their shape (needed for any
  edit-mode or keyless clip, reused by the `diff-side-by-side` and `export-html` clips); the times.

## Out of scope

- Any change to `src/` or to an SwRS text; the keyboard move (Alt+Up, Alt+Down); a drag across
  lists or inside an alert or admonition.
- A floating drag image (the CDP drag has none): written in the storyboard's review notes, not
  fixed.
- A macOS or Linux take; placing the clip in release notes or the announcement (a release CR does
  it).
- A retake after the owner's review (a follow-up of this CR, Q3); marking the PR ready before the
  owner approves the storyboard and the clip (Q3); a change of the recipe's storyboard order.
- Other kit changes than section 5 (no `drag` helper: the exposed helpers do it).

## CI

No CI job changes. The kit's new tests run in `just check` through `just clip-kit-test`, inside the
existing `ci-static` job (Linux and Windows, `.github/workflows/ci.yml`); the site test runs where
`test/site/` tests run today.

- Environment: the CI machine set up by `just dev-ci` from the lock files, Node.js 24 from `.nvmrc`
  through `fnm`. Absent there and present locally: `ffmpeg`, the kit's scratch folder, the VS Code
  download, Remotion, a display. The new tests need none of them: pure functions, the shipped
  `clip.md` and `scenario.mjs` files read from the repository, the shipped `docs/user/editing.md`
  and the clip's committed files (Git LFS checked out as CI does for the raw copy clip's site test).
- Before the push: `just clip-kit-test`, `just check` and `just ci-static` on Windows.
- Only the first CI run proves the Linux leg (the dynamic `import` of the scenarios from a
  repository path, path handling).

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows; the storyboard and scenario tests read the
   shipped `clip.md` and `scenario.mjs` at the head under test; the site test reads the shipped
   `docs/user/editing.md`.
2. The raw copy clip is unchanged by section 5: the tests of section 5 prove its lines and frame
   names (`takeLines` on a raw-copy-like `verify`, `keyFrameTimes` on a take with presses, its
   shipped `scenario.mjs` resolving to the defaults); when its take is still in the kit's scratch
   folder, `just clip raw-copy-balance-edges render` then `check` also pass with the same
   `check.json` lines as committed, and the regenerated outputs are not committed.
3. `just clip drag-list-item all --vsix ...` passes; `check.json` shows `passed: true`, MP4 and WebM
   1280x720 at 15 fps, MP4 duration equal to `Length` within one frame, GIF at most 960 px and
   12 fps, loop seam SSIM in [0.98, 1.0), "Studio in edit mode at the start", no paste line,
   `verifyPassed: true`, playback rate inside 0.77 to 1.3, platform `win32`, extension source
   `vsix`.
4. The agent looks at the contact sheet and every key frame: Studio on the left in edit mode with
   its handles, the text editor on the right, the drop line before "Tag the release." (`drag`), the
   new order in the page and in the raw text (`dropped`), mark 1 on the three moved lines and mark 2
   on the numbers 1. to 4. in the zoomed raw text, Text 1 during the drag and Text 2 during the
   zoom, no tooltip (the handle's `title` must not show), no personal name or path, no dirty tab.
   What was not checked (motion, rhythm, the loop as watched) is said.
5. `just requirements-update` leaves the tree clean after its commit; `just preflight` passes (on
   Windows, its static stage).
6. The PR is a draft; its body plays the GIF, links the MP4 and WebM at the head sha and holds the
   "Deviation from the feature clip process" section.

## Open questions

None for the owner: the answers, the draft and the code settle the clip.
