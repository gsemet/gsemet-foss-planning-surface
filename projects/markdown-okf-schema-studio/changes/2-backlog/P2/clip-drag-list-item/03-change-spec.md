# Feature clip: drag a list item by its handle

Short name: `clip-drag`. No tracker issue (verbal request of the owner, 2026-11-25).

## Goal

A second feature clip of Studio, made with the clip kit and the feature clip recipe as the CR
`short-demo-video-of-the-smart-raw-markdo` (short name `raw-copy-demo`) leaves them: in edit mode,
the reader drags a list item by its handle. The item moves with its sub-items, the numbering stays
1, 2, 3, 4, and the raw Markdown in the text editor beside the page follows at once. One continuous
shot, two captions in turn, one outline per drag on the moved item, 1280x720 at 15 fps, MP4, WebM
and GIF; the owner reviews the storyboard and the clip in the pull request, whose body plays the
clip.

The clip shows Studio's existing list item move (CR 432, `src/page/features/listItemMove.ts`,
`SwRS-MDOKFSTUDIO-BLOCK-262`); no behaviour of the extension changes.

## Dependency and base

This CR runs after `raw-copy-demo` (`depends.json`). That CR (not merged when this spec is
written) gives the kit: the Markdown storyboard contract (`## Clip` table, one `## <n>. <beat>`
section per beat with `Time`, `Shot *(filmed)*`, `Text <n> *(on screen)*`, `Zoom`, `Mark <id>`),
captions in turn, marks in turn, `Size` and `Frame rate` read from the storyboard, key frames
`frames/<NN>-mark-<id>.png`, the parser tests in `docs/demo-video/clip-kit/lib/storyboard.test.mjs`
run by `just clip-kit-test` inside `just check`, and the PR rule (the GIF inline from the PR's head,
the MP4 and WebM linked at the same head).

- Base: the branch of `raw-copy-demo` when the batch stacks the two, else `origin/main` once that
  CR is merged (fetch first: the local `main` is behind `origin/main`).
- Where `raw-copy-demo` lands differently from its spec (a field name, a frame name, a test file
  name), this CR follows what it merged, and says so in the PR's "Autonomous decisions".

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| Q1 | The recipe and kit as `raw-copy-demo` leaves them: live Markdown storyboard `clip.md` the owner reviews, stage, scenario, take, render to GIF, MP4 and WebM, 1280x720 at 15 fps, a PR whose review plays the clip | whole spec |
| Q2 | Edit mode; an ordered list of four items, one with two sub-items; drag the last item above the one with sub-items (numbering stays 1 to 4), then a second drag moves the item with its sub-items; the raw Markdown beside the page shows the new order | sections 2, 3 |
| Q3 | Two captions in turn, English: "Drag an item by its handle" (first drag), "Sub-items follow; the numbering stays in order" (second drag); a mark outlines the moving item; no opening or end card | section 2 |
| Q4 | Filmed on Windows by the batch, VSIX built at the take (the branch's `src/` is `main`'s), throwaway `--extensions-dir` and profile; the drag is real input through CDP, drawn by the kit's own pointer; the owner reviews storyboard and clip in the PR; a retake after review is a follow-up of this CR | sections 4, 7 |
| Q5 | `docs/demo-video/clips/drag-list-item/` and the docs the recipe says to link; no change to `src/` | sections 1 to 6 (and the kit gap of section 5) |
| Q6 | The PR body embeds the clip, links the MP4 and WebM (the `raw-copy-demo` rules), states what the clip proves and what the owner judges (motion, rhythm) | section 8 |

Q4 also moves the owner's storyboard review, which the recipe places before the take, to the PR:
tonight the storyboard is written by the agent with pictures from the batch's own take, committed
with `status: draft`, and the owner approves or corrects it in the PR.

## What changes

All paths are relative to the repository root.

### 1. The stage: `docs/demo-video/clips/drag-list-item/stage/steps.md`

Exactly this text (LF line endings, a final newline):

```markdown
# Release steps

1. Update the changelog
2. Run the checks
   - unit tests
   - end-to-end tests
3. Publish the release
4. Bump the version
```

After the first drag ("Bump the version" above "Run the checks"):

```markdown
# Release steps

1. Update the changelog
2. Bump the version
3. Run the checks
   - unit tests
   - end-to-end tests
4. Publish the release
```

After the second drag ("Run the checks", with its sub-items, above "Update the changelog"), the
expected text the scenario's `verify` checks:

```markdown
# Release steps

1. Run the checks
   - unit tests
   - end-to-end tests
2. Update the changelog
3. Bump the version
4. Publish the release
```

The sub-list gets its own two handles (it is a list of two items): they are on screen, not used.

### 2. The live storyboard: `docs/demo-video/clips/drag-list-item/clip.md`

Written in the storyboard format of `raw-copy-demo` (its recipe section 2). Times below are the
plan; the batch's take sets the final ones (section 4), written in the same commit as the render.
The content:

````markdown
---
title: Feature clip drag-list-item
status: draft
date: <the day of the commit>
---

# Feature clip: drag-list-item

**This is the live storyboard.** The clip is built from this file: edit any row marked
*(on screen)*, save, and run `just clip drag-list-item render`, then `check`. Rows marked
*(filmed)* describe the take: changing them means a new take. The clip is one continuous shot with
two texts in turn; `**bold**` in a text takes the orange accent.

## Clip

| Field | Content |
| --- | --- |
| Length | 11 s |
| Size *(on screen)* | 1280x720 16:9 |
| Frame rate *(on screen)* | 15 fps |
| Outputs | silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | none: every setting at its default |
| Filmed on | Windows, VS Code <version from check.json>, extension <version> VSIX built from the branch |
| Stage | `stage/steps.md`, in the text editor (left) and in Studio's side preview in edit mode (right) |

## 1. Drag an item by its handle

![The last item dragged by its handle above "Run the checks": the drop line shows where it lands](frames/drag-1.png)

![The item at its new place, outlined; the numbering and the raw text follow](frames/04-mark-1.png)

| Field | Content |
| --- | --- |
| Time | 0 to 5.0 s (zoom from 0.2 s; pointer on the handle of "Bump the version" at 1.1 s; drag 1.5 to 2.9 s; outline 3.6 to 4.8 s) |
| Shot *(filmed)* | `steps.md` in the text editor on the left, Studio's side preview in edit mode on the right, a gentle zoom on the two lists. The pointer takes the handle of item 4, "Bump the version", and drags it above item 2, "Run the checks". The page shows it as item 2, the numbers stay 1 to 4, and the text editor shows the same order. |
| Zoom | lists, hold to 9.8 s |
| Text 1 *(on screen)* | Drag an item by its **handle** |
| Mark 1 *(on screen)* | Orange outline around the moved item "Bump the version" at its new place, 3.6 to 4.8 s |

## 2. Sub-items follow

![The item with sub-items dragged above the first item](frames/drag-2.png)

![The item and its two sub-items at the top, outlined](frames/05-mark-2.png)

| Field | Content |
| --- | --- |
| Time | 5.0 to 11.0 s (pointer on the handle of "Run the checks" at 5.7 s; drag 6.1 to 7.4 s; outline 8.1 to 9.5 s; zoom out from 9.8 s, back to the start for the loop) |
| Shot *(filmed)* | The pointer takes the handle of "Run the checks", now item 3, and drags it above item 1. It moves with "unit tests" and "end-to-end tests"; the numbers stay 1 to 4; the text editor shows the three lines moved together. |
| Text 2 *(on screen)* | **Sub-items** follow; the numbering stays in order |
| Mark 2 *(on screen)* | Orange outline around "Run the checks" and its two sub-items at the top, 8.1 to 9.5 s |

Expected text, the scenario's check (`steps.md` on disk after the two drags):

```markdown
# Release steps

1. Run the checks
   - unit tests
   - end-to-end tests
2. Update the changelog
3. Bump the version
4. Publish the release
```

## Review notes

- The drag goes through CDP mouse events: no floating copy of the item follows the pointer. The
  drag shows as the dragged item faded in place and a line where it will land; the item jumps there
  on release.
- The raw screencast runs at about <rawFps from check.json> frames per second: the pointer is drawn
  smooth by the kit, but the drop line and the page change by steps.
- The keyboard move (Alt+Up, Alt+Down on a focused handle) is not filmed.
````

Bold words in the two texts: Q3 gives the texts, not their accent; the accent on "handle" and
"Sub-items" is this spec's choice, listed in "Autonomous decisions" (the owner removes it by
deleting the `**`). The texts' words are exactly Q3's.

The mark `<what>` texts hold no comma (the parser reads `<what>, <from> to <to> s`).

### 3. The scenario: `docs/demo-video/clips/drag-list-item/scenario.mjs`

In the style of `clips/raw-copy-balance-edges/scenario.mjs`; the header comment says what is
filmed and that every text and time is in `clip.md`. Selectors and attributes are Studio's own
(`src/page/features/listItemMove.ts`, `src/page/runtime.ts`).

- `stage = { "stage/steps.md": "steps.md" }`; `open = ["steps.md"]` (it opens in the text editor:
  Studio's custom editor `markdown-okf-schema-studio.editor` has priority `option`, and no
  `workbench.editorAssociations` is set); `settings = {}`.
- `checks = { editMode: "on", paste: false }` (section 5).
- `EXPECTED_AFTER_FIRST` and `EXPECTED` hold the texts of section 1 (the lines joined with `\n`, a
  final `\n`).
- Helpers, local to the scenario:
  - `editorLines(page)`: the texts of the non-empty `.monaco-editor .view-lines .view-line` of the
    left editor, top to bottom, non-breaking spaces turned into spaces, trailing spaces dropped;
    and their rectangles (as `raw-copy-balance-edges`' `editorLines`).
  - `itemBox(t, text)`: in the preview frame, the `#sphinx-myst-preview-content li` whose own
    first text starts with `text` (the integration test's `handleOf` way, `test/integration/listItemMoves.ts`),
    its rectangle in page coordinates (`frame.locator(...).boundingBox()`), its first line's top
    and height, and its `data-sphinx-source-line`.
  - `handleOf(t, text)`: the handle `[data-okf-list-handle-layer] .okf-list-item-handle[data-okf-list-item-line="<line>"]`
    of that item, its centre in page coordinates.
  - `pageOrder(t)`: the own first texts of the top-level `ol`'s `li` children, in order.
- `setup(t)`, off camera:
  1. focus the text editor (`page.locator(".monaco-editor").first().click()`), then the chord of
     "Open Preview to Side" (`markdown-okf-schema-studio.openPreview`, keybinding `ctrl+k shift+v`):
     `page.keyboard.press("ControlOrMeta+K")`, then `page.keyboard.press("Shift+V")`; wait for
     `t.frameOf()`;
  2. turn edit mode on: click `[data-sphinx-preview-edit-toggle]` in the frame, poll
     `document.documentElement.getAttribute("data-sphinx-preview-edit-mode")` (re-reading the
     frame, as `readingMode` does in the raw copy scenario) until it is `"on"`, then until the frame
     holds 6 handles (`[data-okf-list-handle-layer] .okf-list-item-handle`: 4 items, 2 sub-items);
     `t.record("readingMode", mode)` (the key keeps its name: it holds the value of
     `data-sphinx-preview-edit-mode`, `"on"` here); throw when it is not `"on"`;
  3. park the pointer in the preview's blank area below the list, off every block (for example
     120 px below the bottom of the `ol` and 200 px right of its left edge, read from the frame),
     with `t.moveTo(x, y, 0.1)`, then `t.sleep(500)`: frame 0 and the last frame show no hover.
- `run(t)`, the filmed action, timed with `until(seconds)` as in the raw copy scenario (the times of
  section 2):
  1. at 0.2 s, `t.zoom("lists", rect)`: the union of the left editor's 9 lines (heading to item 4)
     and of the preview's heading and `ol` (page coordinates), padded by 24 px;
  2. at 0.4 s, `t.moveTo` (0.7 s) to the centre of the handle of "Bump the version"; at 1.5 s, the
     drag: `t.ev("click", t.pointer)` (the kit's ripple on the press), `await t.page.mouse.down()`,
     `t.moveTo(x + 6, y + 8, 0.1)` (the move that starts an HTML5 drag, as the integration test's
     `dragTo`), then `t.moveTo` (0.9 s) to the point 40 px right of the left edge of the item
     "Run the checks" and a quarter of its first line's height below its top (the upper half of
     its first line: the drop line shows before it); `t.keyFrame("drag-1")` (section 5);
     `t.sleep(250)`; `await t.page.mouse.up()`;
  3. wait, at most 2 s, until `editorLines` reads `EXPECTED_AFTER_FIRST`'s non-empty lines and
     `pageOrder` reads "Update the changelog", "Bump the version", "Run the checks", "Publish the
     release"; else throw with what both show (a finding against the feature, never a scenario
     fix);
  4. at 3.6 s, `t.mark("1", rect)`: the box of the item "Bump the version", its left edge 2em
     (the item's computed font size) further left so its number is inside, with 6 px and 3 px of
     air as in the raw copy scenario; at 4.8 s, `t.unmark("1")`;
  5. at 5.0 s, `t.moveTo` (0.7 s) to the handle of "Run the checks"; at 6.1 s, the same drag to the
     upper quarter of the first line of "Update the changelog"; `t.keyFrame("drag-2")`; release;
  6. wait, at most 2 s, until `editorLines` reads `EXPECTED`'s non-empty lines and `pageOrder`
     reads "Run the checks", "Update the changelog", "Bump the version", "Publish the release",
     and the `li` "Run the checks" holds the two sub-items; else throw as in 3;
  7. at 8.1 s, `t.mark("2", rect)`: the whole box of the `li` "Run the checks" (its sub-items
     inside), with its number and the same air; at 9.5 s, `t.unmark("2")`;
  8. at 9.8 s, `t.unzoom("lists")` and `t.moveTo(home.x, home.y, 0.6)`; `until(11.0)`.
- `verify(t)`: poll `t.workspaceFile("steps.md")` for up to 3 s (auto-save is `afterDelay`) and
  throw `steps.md does not hold the expected text. On disk: ${JSON.stringify(text)}` when it never
  equals `EXPECTED`; return `{ text }`.

### 4. Take and render

On Windows, on this machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`):

```bash
just dev
just package                                   # out/reports/package/markdown-okf-schema-studio.vsix
just clip drag-list-item doctor
just clip drag-list-item all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

- A trial first (recipe section 1), adapted to this clip: (a) the preview webview is in the frames;
  (b) the CDP mouse drag by the handle moves the item (step 3 of `run` passes); (c) the raw text
  follows (same step); (d) the retimed rate is at least the storyboard's frame rate. If (b) fails,
  stop and report: neither a keyboard move (Alt+Up) nor a scripted call stands in for the drag the
  clip shows, and never OS-level input or capture.
- `Length` and every time in `clip.md` follow the take (playback rate inside 0.77 to 1.3), in the
  same commit as the render; the two captions stay end to end from 0 to `Length`, the marks inside
  the zoom hold.
- Commit together (recipe rule): `clip.md`, `scenario.mjs`, `stage/steps.md`, `drag-list-item.mp4`,
  `.webm`, `.gif` (Git LFS through `.gitattributes`), `poster.png`, `contact-sheet.png`,
  `first-last.png`, `frames/*.png`, `check.json`.

### 5. The kit gaps this clip needs: `docs/demo-video/clip-kit/`

The kit, as merged and as `raw-copy-demo` leaves it, cannot make this clip, for three reasons read
in the code of `origin/main`:

- `lib/check.mjs` always wants "no paste-options widget after the paste"
  (`verify.notes.pasteWidgets === 0`) and "Studio in reading mode at the start"
  (`verify.notes.readingMode === "off"`): an edit-mode clip with no paste fails `check`.
- `lib/encode.mjs` takes its key frames from `take.presses[0]` and `take.presses.at(-1)`: a take
  with no key press throws in `render`.
- The kit's key frames have no picture of a drag in progress, which the storyboard shows (one
  picture per key moment, `raw-copy-demo` Q40).

So this CR changes the kit, the least the clip needs, with the raw copy clip unchanged
(`check.json` lines, key frame names and outputs as before). Every refusal names the scenario or
`clip.md`, as the kit's messages do.

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
  did), `03-zoomed.png` when there is a zoom, `<NN>-mark-<id>.png` per mark as `raw-copy-demo`
  numbers them, and `<name>.png` at `t / story.rate` per key frame. A name must match
  `^[a-z][a-z0-9-]*$` (it starts with a letter, so it never takes a numbered kit name) and be
  unique, else `render` fails naming it.
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
    press, a zoom, two marks and the key frames `drag-1`, `drag-2` gives `drag-1.png`,
    `drag-2.png`, `03-zoomed.png`, `04-mark-1.png`, `05-mark-2.png` and no `01-selected.png`; a name
    `01-x` or a repeated name is refused.
  - `storyboard.test.mjs` (from `raw-copy-demo`) gains a case that reads the shipped
    `docs/demo-video/clips/drag-list-item/clip.md` from the repository (path from the test file's
    own location, at the head under test, never a copy) with `parseClip` and asserts: size
    1280x720, 15 fps, two captions with Q3's words (`**` aside) end to end from 0 to `Length`, no
    badge, zoom `lists`, marks `1` and `2` in turn inside the hold; and `validateStory` passes with a
    `take` object with no press, zoom `lists` and marks `1`, `2`, on `win32`.
  - A test that reads the shipped `scenario.mjs` of each clip (dynamic `import` from the repository
    path) and passes its `checks` to `resolveChecks`: `drag-list-item` gives on/false,
    `raw-copy-balance-edges` the defaults.

### 6. Docs

- `docs/user/editing.md`: under the paragraph "In edit mode each list item also has a handle on
  its left ... the handles sit left of the box." (inside the "Inline editing" item, indented two
  spaces as `docs/user/settings.md` does for the raw copy clip), the image
  `![In edit mode, the last item of an ordered list is dragged by its handle above the second, then the item with two sub-items is dragged to the top: the numbers stay in order and the Markdown beside follows](../demo-video/clips/drag-list-item/drag-list-item.gif)`.
- `test/site/siteClips.test.ts`: a test "the shipped editing page plays the list drag clip as
  video", modelled on the settings page one: it reads the shipped `docs/user/editing.md`, renders it
  with `renderMyst` and `clipVideos`, asserts the `<video src="../demo-video/clips/drag-list-item/drag-list-item.webm"`
  and that `drag-list-item.webm`, `.gif` and `poster.png` exist; marker
  `// @tests_req SwRS-MDOKFSTUDIO-CORE-095` (an added test of an existing SwRS, no SwRS text
  change); then `just requirements-update`.
- `docs/demo-video/guidelines/feature-clip-process.guidelines.md` (as `raw-copy-demo` leaves it),
  in the guideline's words ("the agent", "the maintainer", no chantier role, no CR):
  - section 1, the scenario's exports: `checks` (`editMode`, `paste`, defaults) and the helper
    `keyFrame(name)`; the scenario may drive a drag with the exposed `ev("click", ...)`,
    `page.mouse.down()`, `moveTo` and `page.mouse.up()`, as the list drag clip does; "A trial
    first": (b) and (c) read for a drag clip as "the CDP drag moves what the clip shows" and "the
    result shows on screen";
  - section 2: a picture may be a scenario key frame `frames/<name>.png`;
  - section 6: the reading mode line becomes "Studio in the mode the scenario declares at the
    start", the paste widget line "when the scenario pastes".
- `.agents/glossary/common.md`: no change (the "Feature clip" entry of `raw-copy-demo` holds).
- No change to `README.md`, `CHANGELOG.md` or `docs/releases-notes/` (no `feat` or `fix` commit).

### 7. Host and default matrix

The clip films defaults only (no setting), with a mouse drag; the platform changes only the
window and the chord that opens the side preview off camera.

| Host | VS Code | Settings | Expected | Proof |
| --- | --- | --- | --- | --- |
| Windows 11, CDP mouse drag | pinned `DEFAULT_CODE_VERSION` (1.147.0 unless moved) | defaults | `steps.md` equals the expected text; page and editor show the order after each drag | the take's `run` checks and `verify`, `check.json` ("scenario verify passed") |
| macOS | same | defaults | same | not proved (no macOS take, Q4) |
| Linux | same | defaults | same | not proved |

The kit's new tests run on Windows locally and on Linux and Windows in `ci-static`.

### 8. Commits and the pull request

- Commits by area (Conventional Commits; no scope on `build`, `docs` or `test`):
  `build: let a feature clip declare its start mode and its own key frames` (kit and its tests),
  `docs: add the drag a list item feature clip` (clip folder, `docs/user/editing.md`, recipe),
  `test: play the list drag clip on the editing page of the docs site` (`siteClips.test.ts`,
  requirements files `just requirements-update` changes).
- The PR body follows `.github/PULL_REQUEST_TEMPLATE.md`, the PR guideline and the clip PR rule of
  `raw-copy-demo`: the GIF inline from
  `https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/drag-list-item/drag-list-item.gif`,
  the MP4 and WebM linked with the same form at the same head; after each push of a new render the
  links move to the new head (`gh pr edit <n> --body-file <file>`); check that the GIF plays in the
  rendered PR page (if not, the fallback `raw-copy-demo` settled for its own open question 1).
- The body states what the clip proves (a real drag by the handle in a real VS Code window moves an
  item and an item with its sub-items, the numbers stay 1 to 4, the raw text follows: the take's
  checks and `verify`) and what the owner judges (motion, rhythm, the loop as watched, the absence
  of a floating drag image, the texts and their accent); it links `clip.md` for the storyboard
  review (Q4) and says a retake after review is a follow-up of this CR.
- "Autonomous decisions": the stage text; the side preview layout (text left, Studio right); the
  gentle zoom (the kit refuses a mark without a zoom); one mark per drag, on the moved item at its
  new place; the accent words; the kit gaps of section 5 and their shape (beyond Q5's file list,
  needed for any edit-mode or keyless clip); the times.

## Out of scope

- Any change to `src/` or to an SwRS text; the keyboard move (Alt+Up, Alt+Down); a drag across
  lists or inside an alert or admonition.
- A floating drag image (the CDP drag has none): written in the storyboard's review notes, not
  fixed.
- A macOS or Linux take; placing the clip in release notes or the announcement (a release CR does
  it); a retake after the owner's review (a follow-up of this CR, Q4).
- Other kit changes than section 5 (no `drag` helper: the exposed helpers do it).

## CI

No CI job changes. The kit's new tests run in `just check` through `just clip-kit-test`, inside
the existing `ci-static` job (Linux and Windows, `.github/workflows/ci.yml`); the site test runs
where `test/site/` tests run today.

- Environment: the CI machine set up by `just dev-ci` from the lock files, Node.js 24 from
  `.nvmrc` through `fnm`. Absent there and present locally: `ffmpeg`, the kit's scratch folder, the
  VS Code download, Remotion, a display. The new tests need none of them: pure functions, the
  shipped `clip.md` and `scenario.mjs` files read from the repository, the shipped
  `docs/user/editing.md` and the clip's committed files (Git LFS checked out as CI does for the
  raw copy clip's site test).
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
3. `just clip drag-list-item all --vsix ...` passes; `check.json` shows `passed: true`, MP4 and
   WebM 1280x720 at 15 fps, MP4 duration equal to `Length` within one frame, GIF at most 960 px and
   12 fps, loop seam SSIM in [0.98, 1.0), "Studio in edit mode at the start", no paste line,
   `verifyPassed: true`, playback rate inside 0.77 to 1.3, platform `win32`, extension source
   `vsix`.
4. The agent looks at the contact sheet and every key frame: the handles left of the list, the drop
   line before "Run the checks" (`drag-1`) and before "Update the changelog" (`drag-2`), each
   outline on the moved item with its number (and the two sub-items for mark 2), the numbers 1 to 4
   in the page, the editor's lines in the same order, Text 1 during the first drag and Text 2 during
   the second, no tooltip (the handle's `title` "Drag to move item (Alt+Up, Alt+Down)" must not
   show), no personal name or path, no dirty tab. What was not checked (motion, rhythm, the loop as
   watched) is said.
5. `just requirements-update` leaves the tree clean after its commit; `just preflight` passes (on
   Windows, its static stage).
6. The PR body plays the GIF and links the MP4 and WebM at the head sha.

## Open questions

None for the owner: the answers and the code settle the clip. The kit gaps of section 5 go beyond
Q5's file list because the code requires them; the Chief of Staff may move them into
`raw-copy-demo` instead if that batch is still open, with no change to this spec's clip.
