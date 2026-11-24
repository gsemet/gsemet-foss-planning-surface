# Feature clip: switch the theme in one click

Short name: `clip-theme`. No tracker issue (verbal request of the owner, 2026-11-25).

## Goal

The owner asked for clips like the raw copy clip on the best features of Studio, one CR per clip;
this is one of them. One button changes the whole page: the Theme button of the floating toolbar
cycles the preview through its theme modes (the current VS Code theme, Dark, White, Cream), and the
Mermaid diagram and the Vega-Lite chart are drawn again in the new colours, not left in the old
ones. One continuous shot of about 10.5 s: two clicks (Dark to White to Cream), then a zoom on the
diagram and the chart; two captions in turn, two orange marks in turn, 1280x720 at 15 fps, no card,
the logo top right, a loop; MP4, WebM and GIF; a draft PR whose description plays the clip.

The clip shows Studio's existing theme button (`src/page/features/themeMode.ts`,
`SwRS-MDOKFSTUDIO-THEME-001`) and the theme-driven redraw of diagrams and charts
(`src/page/modules/mermaidPreview.ts`, `src/page/modules/vegaPreview.ts`,
`SwRS-MDOKFSTUDIO-DIAG-123`); no behaviour of the extension changes.

## Dependency and base

- `depends.json` names `short-demo-video-of-the-smart-raw-markdo` (CR-484, the storyboard contract:
  `## Clip` table with `Length`, `Size`, `Frame rate`, `Outputs`, `Cards`, `Logo`, `Setting filmed`,
  `Filmed on`, `Stage`; one `## <n>. <beat>` section per beat with `Time`, `Shot *(filmed)*`,
  `Text <n> *(on screen)*`, `Zoom`, `Mark <id>`; captions and marks in turn; key frames
  `frames/<NN>-mark-<id>.png`; `docs/demo-video/clip-kit/lib/storyboard.test.mjs` run by
  `just clip-kit-test` inside `just check`; the clip PR rule).
- This clip also needs the generic kit changes of `clip-drag-list-item` (CR-485, its
  `03-change-spec.md`, section 5): the scenario export `checks = { editMode, paste }` (this clip
  pastes nothing, so the kit's paste-widget line must be off) and the helper `t.keyFrame(name)` (this
  clip presses no key, so the kit's `01-selected`/`02-pasted` frames do not exist). This CR makes
  **no kit change**: it reuses those. `depends.json` does not name CR-485 yet (open question 1).
- Base: the branch of CR-485 while it is not merged (stacked on CR-484's), else `origin/main` once
  it holds both (fetch first: the local `main` is behind `origin/main`).
- Where CR-484 or CR-485 lands differently from its spec (a field name, a frame name, a helper or a
  test file name), this CR follows what was merged and says so in the PR's "Autonomous decisions".

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| clip-theme-Q1 | Filed from the owner's request: one CR per clip, this clip among seven | Goal |
| clip-theme-Q2 | The captions, stage and timing are the Griller's proposal, the draft `work/storyboard/clip.md` with its stage `work/storyboard/stage/handbook.md`; the owner reviews them at the recipe's storyboard gate | "Where this spec differs from the draft", sections 1 to 3 |
| clip-theme-Q3 | The batch does not wait for the storyboard approval before the take: it films the trial take from the draft, puts its pictures in the storyboard, renders the clip and opens the PR with the clip watchable; the owner reviews the storyboard and the clip on that PR, which stays a draft until the owner approves (the gate is moved after the take, not dropped); the deviation from the recipe's order is reported in this spec and in the PR body; a retake after the owner's review is a follow-up of this CR | "The storyboard gate, moved after the take", section 7, "Out of scope" |

From `01-intent.md` and the draft: 1280x720 at 15 fps, two captions in turn, several marks in turn,
no card, the logo top right, a loop, Dark to White to Cream, about 10.5 s, the clip in
`docs/demo-video/clips/theme-switch/`.

## The storyboard gate, moved after the take

The recipe `docs/demo-video/guidelines/feature-clip-process.guidelines.md`, a project guideline, as
CR-484 leaves it (section "The storyboard first"), has the maintainer review and edit the storyboard
draft before the take. Q3 moves that gate after the take, into the pull request; it does not drop
it. This is a deviation from a project guideline, decided by the Chief of Staff under the owner's
overnight autonomy, and reported as such:

- the batch films a trial take from the draft, puts its pictures and measured times in the
  storyboard, moves it to `docs/demo-video/clips/theme-switch/clip.md` with `status: draft`, films
  the take, renders and opens the PR;
- the PR is a draft (`gh pr create --draft`) until the owner approves the storyboard and the clip in
  it; the agent never marks it ready; the PR body reports the deviation (section 7);
- the recipe's storyboard order is not changed by this CR.

## What the code settles

Facts of Studio on `origin/main`, read to name the real controls (no choice made here):

- **The Theme button** is `[data-sphinx-preview-theme-toggle]`, the second button of toolbar row 2
  (`data-sphinx-preview-toolbar-row="navigation"`: Anchor, Theme, Back, Next;
  `src/core/preview/previewToolbar.ts`). A click cycles `current`, `dark`, `white`, `cream`, then
  `current` again (`PREVIEW_THEME_MODES`, `src/page/features/themeMode.ts`). The shown mode is
  `data-sphinx-preview-theme-mode` on the frame's `html` and `data-theme-mode` on the button; its
  `title` and `data-tooltip` read `<Mode> theme (click for <next mode> theme)` in lower case after
  "for": "Dark theme (click for white theme)", "White theme (click for cream theme)", "Cream theme
  (click for current theme)", "Current theme (click for dark theme)"; `aria-label` reads
  "Preview theme: <Mode> theme".
- **The default** theme mode is `cream` (`DEFAULT_PREVIEW_THEME_MODE`,
  `src/core/state/previewTheme.ts`); the choice is kept per workspace (glossary, "Fresh workspace").
  In the kit's throwaway profile the VS Code theme is `Default Light Modern`
  (`docs/demo-video/clip-kit/lib/profile.mjs`, `BASE_SETTINGS`), so `current` looks close to White.
- **The colour fade**: a click sets `data-sphinx-preview-theme-switching="true"` until the body's
  `background-color` transition ends, with a 400 ms fallback (`src/page/modules/motion.ts`).
- **The redraw**: both runtimes watch `data-sphinx-preview-theme-mode` on `html` with a
  `MutationObserver` and draw every diagram (`.myst-mermaid-diagram`) and chart
  (`.myst-vega-diagram`) again. Each drawing is an `<img>` (`img.myst-mermaid-image`,
  `img.myst-vega-image`) whose `src` is a `data:image/svg+xml` URL of the SVG drawn with the page's
  colours; a drawing already made for the same colours is reused from a cache at once, a new one is
  drawn (a few hundred ms at most for this stage). So "drawn again in the new colours" is visible as
  a change of each `img`'s `src`.
- **The toolbar** starts collapsed in a fresh workspace (`DEFAULT_VIEW_PREFERENCES.toolbarCollapsed`);
  the collapse button is `[data-sphinx-preview-toolbar-collapse]`, the state
  `data-sphinx-preview-toolbar-state` on `html` (`"collapsed"`, `"expanded"`). A panel that opens
  collapsed plays a load hint once (the rows unroll for 700 ms and roll up;
  `src/page/modules/toolbarCollapse.ts`).
- **Edit mode** is off in a fresh profile; the state is `data-sphinx-preview-edit-mode` on `html`.
- **The loop seam**: `lib/check.mjs` wants an SSIM of at least 0.98 between frame 0 and the last
  frame; the composition's last frame is 8/9 frame 0 and 1/9 the last scene (`SEAM = 8`,
  `remotion/src/Clip.tsx`). A clip that starts in Dark and ends in Cream blends a light page over a
  dark one in its last frame, which very likely fails that line (an estimate; the trial measures
  it). Any clip with a number of clicks that is not a multiple of four ends in another theme mode
  than it starts in, so the draft's fallback (start in Cream, go to Dark through the current theme)
  has the same seam (section 3, "The seam").

## Where this spec differs from the draft

| Draft | This spec | Why |
| --- | --- | --- |
| `Format` row (size, rate, outputs in one cell) | `Size *(on screen)*` = `1280x720 16:9`, `Frame rate *(on screen)*` = `15 fps`, `Outputs` = the rest | the kit, as CR-484 leaves it, reads `Size` and `Frame rate` as their own fields |
| The zoom described in the `Time` and `Shot` rows only | a row `Zoom` = `charts, hold to 9.5 s` (or the take's hold) in section 2 | the kit reads the zoom from a `Zoom` row |
| "Pictures: from the batch's trial take" | section 1: `frames/white.png` (the page in White, redrawn) and `frames/cream.png` (the page in Cream, the pointer off the toolbar); section 2: `frames/04-mark-1.png`, `frames/05-mark-2.png` | no key press, so no `01-selected`/`02-pasted`; the scenario names its key frames with `t.keyFrame` (CR-485) |
| Status "draft for the owner's review", the opening paragraph of a review draft | `status: draft`, the opening paragraph of a live storyboard | the file becomes the live storyboard in the clip folder (recipe) |
| `Filmed on`: "to be filmed by the batch"; `Setting filmed`: "none (the theme is a view choice ...)" | Windows, the VS Code version of `check.json`, the extension version, "VSIX built from the branch"; "none: every setting at its default (the theme mode is a view choice, set off camera)" | the batch's take |
| Expected result: "their fill and text colours differ from the ones read at frame 0" | each drawing's `img` `src` differs from the one of the mode before, after each click | the drawings are `data:` SVG images (above); a new `src` is what "drawn again" means in the page, read without decoding colours |
| Review note on the seam: "if the SSIM check refuses ... the clip would start in Cream and go to Dark through the current theme instead (owner's choice at the gate)" | the seam rule of section 3: the draft's version first; if the seam line fails, the four-click version | the draft's fallback ends in another mode than it starts in too (above); Q3 has the batch render before the owner's gate, so the Driver needs a version that passes `check` (open question 2) |
| Times 10.5 s, clicks 1.0 and 2.6 s, zoom 4.2 to 9.5 s, marks 4.8 to 6.6 s and 6.6 to 8.4 s | the take's own times, same beats and order | the recipe: the storyboard follows the take |

Everything else is carried as written: the stage, Studio in the whole window in reading mode, the
toolbar expanded off camera, frame 0 in Dark, the two clicks, the pointer leaving the toolbar after
the second click, the zoom (at most 2x) on the flowchart and the bar chart in Cream, the two texts
with their accents, the two marks and their order, the expected result, the review notes on the
redraw before the zoom, the tooltip and the skipped current theme.

## What changes

All paths are relative to the repository root.

### 1. The stage: `docs/demo-video/clips/theme-switch/stage/handbook.md`

The draft's `work/storyboard/stage/handbook.md`, exactly (LF line endings, a final newline): the
heading "Support handbook", the sentence, the `:::{tip}` admonition, the `mermaid` flowchart
`A[Triage] --> B[Reproduce] --> C[Fix] --> D[Release]` and the `vega-lite` bar chart (width 360,
height 110, tags bug 14, question 9, feature 5). Copy the file; do not retype it.

### 2. The live storyboard: `docs/demo-video/clips/theme-switch/clip.md`

The draft `work/storyboard/clip.md`, changed only as "Where this spec differs from the draft" says;
times are the draft's until the take sets them (section 4), in the same commit as the render. The
content (draft's version; the four-click version of section 3 changes only what that section says):

````markdown
---
title: Feature clip theme-switch
status: draft
date: <the day of the commit>
---

# Feature clip: theme-switch

**This is the live storyboard.** The clip is built from this file: edit any row marked
*(on screen)*, save, and run `just clip theme-switch render`, then `check`. Rows marked *(filmed)*
describe the footage of the take: changing them means a new take. `**bold**` in a text takes the
orange accent.

The clip is one continuous shot: two clicks on the Theme button, then a zoom on the diagram and the
chart. It shows two texts in turn.

## Clip

| Field | Content |
| --- | --- |
| Length | 10.5 s |
| Size *(on screen)* | 1280x720 16:9 |
| Frame rate *(on screen)* | 15 fps |
| Outputs | silent, loops; MP4 (X, release), WebM (docs site), GIF 960 px (release notes, docs page) |
| Cards | none |
| Logo | top right |
| Setting filmed | none: every setting at its default (the theme mode is a view choice, set off camera) |
| Filmed on | Windows, VS Code <version from check.json>, extension <version> VSIX built from the branch |
| Stage | `stage/handbook.md` (Studio, the whole window, reading mode): a heading, a sentence, a `tip` admonition, a Mermaid flowchart and a Vega-Lite bar chart, all in view |

Off camera (`setup`): the toolbar expanded (a new workspace starts collapsed), reading mode, and the
Theme button clicked from Cream (the default) through the current theme to Dark, so frame 0 is Dark.
The button cycles current, Dark, White, Cream.

## 1. Two clicks, three palettes

![The whole page, the admonition, the diagram and the chart in the White theme after the first click](frames/white.png)

![The page in the Cream theme after the second click, the pointer off the toolbar](frames/cream.png)

| Field | Content |
| --- | --- |
| Time | 0 to 4.0 s (click at 1.0 s: White; click at 2.6 s: Cream; each fade about 0.2 s) |
| Shot *(filmed)* | Studio on `handbook.md` in Dark. The pointer moves to the Theme button of row 2 and clicks: the whole page, the admonition, the diagram and the chart turn White. It clicks again: Cream. The pointer then moves off the toolbar. |
| Text 1 *(on screen)* | One click turns the **whole page** to another theme |

## 2. Zoom on the diagram and the chart

![Mark 1 around the flowchart in the Cream theme](frames/04-mark-1.png)

![Mark 2 around the bar chart in the Cream theme](frames/05-mark-2.png)

| Field | Content |
| --- | --- |
| Time | 4.0 to 10.5 s (zoom from 4.2 s, held to 9.5 s, then back to the start for the loop) |
| Shot *(filmed)* | Zoom (at most 2x) on the flowchart and the bar chart, in Cream: the boxes, arrows, bars and axis labels in the Cream palette. |
| Zoom | charts, hold to 9.5 s |
| Mark 1 *(on screen)* | Orange outline around the flowchart, 4.8 to 6.6 s |
| Mark 2 *(on screen)* | Orange outline around the bar chart, 6.6 to 8.4 s |
| Text 2 *(on screen)* | Diagrams and charts **follow** the theme |

Expected result, the scenario's check (visible state, read from the preview; the file is never
changed):

- After the first click the page's theme mode is White, after the second Cream (the theme button's
  label reads "Cream theme (click for current theme)").
- After each click, the Mermaid diagram and the Vega-Lite chart were drawn again: the `src` of each
  drawing differs from the one of the mode before.
- `handbook.md` on disk is byte for byte `stage/handbook.md`.

## Review notes

- The diagram and the chart are drawn again after each switch; the take waits for both new
  drawings before the next step, so the zoom never shows the old colours.
- The toolbar tooltip slides in on hover; the pointer leaves the button after the second click so it
  does not stay in the zoom.
- The current VS Code theme is the kit's Default Light Modern, close to White: that is why the clip
  skips it.
- <the seam note of section 3: the measured SSIM, and which version was rendered>
````

### 3. The scenario: `docs/demo-video/clips/theme-switch/scenario.mjs`

In the style of `clips/raw-copy-balance-edges/scenario.mjs`; the header comment says what is filmed
and that every text and time is in `clip.md`. It imports nothing (the kit's tests load it without
VS Code).

- `stage = { "stage/handbook.md": "handbook.md" }`; `open = ["handbook.md"]`;
  `settings = { "workbench.editorAssociations": { "handbook.md": "markdown-okf-schema-studio.editor" } }`
  (Studio opens the file, alone in the window, as the raw copy scenario does for its runbook).
- `checks = { editMode: "off", paste: false }` (CR-485).
- `export const STAGE`: the stage's text, character for character (LF, final newline), for `verify`
  and for the test of section 5 that compares it with the shipped stage file.
- Helpers, local to the scenario:
  - `pageState(t)`: re-reads the frame (`t.frameOf()`, retried as `readingMode` in the raw copy
    scenario) and returns `{ frame, mode, title, editMode, toolbar, diagram, chart }`: the `html`
    attributes `data-sphinx-preview-theme-mode`, `data-sphinx-preview-edit-mode`,
    `data-sphinx-preview-toolbar-state`, the theme button's `title`, and the `src` of
    `.myst-mermaid-diagram img.myst-mermaid-image` and `.myst-vega-diagram img.myst-vega-image`
    (`null` when absent);
  - `waitForMode(t, mode, before, seconds)`: polls `pageState` every 50 ms until `mode` is shown,
    both `src` are present and both differ from `before.diagram` and `before.chart`; throws after
    `seconds` with the state it read (`the page did not draw the diagram and the chart again in
    <mode>: ...`), a finding against the feature, never a scenario fix;
  - `themeButton(frame)`: the centre of `[data-sphinx-preview-theme-toggle]` in page coordinates
    (`locator.boundingBox()`);
  - `drawingBox(frame, selector)`: the box of a drawing's `img` in page coordinates.
- `setup(t)`, off camera:
  1. wait for the frame and 1.5 s (the load hint ends); when the toolbar state is `"collapsed"`,
     click `[data-sphinx-preview-toolbar-collapse]` and poll until `"expanded"`; else throw;
  2. edit mode must be `"off"`: if it is `"on"`, click `[data-sphinx-preview-edit-toggle]` and poll,
     as the raw copy scenario does; `t.record("readingMode", mode)`; throw when not `"off"`;
  3. the start mode: click the Theme button (`frame.locator(...).click()`) until the mode is `dark`
     (four clicks at most, each followed by `waitForMode` with 3 s), whatever mode the workspace
     stored; the four-click version stops at `cream` instead (a fresh workspace is already there,
     no click);
  4. both drawings rendered (`data-render-state="rendered"` on both containers) and both `src`
     present; else throw;
  5. park the pointer in the blank right part of the page, off the toolbar and off every block (for
     example the content's right edge plus 120 px, at the height of the heading, read from the
     frame), with `t.moveTo(x, y, 0.1)`, then `t.sleep(800)` (the tooltip goes): frame 0 and the
     last frame show no hover.
- `run(t)`, the filmed action, timed with `until(seconds)` as in the raw copy scenario (the draft's
  times):
  1. `before = await pageState(t)`; at 0.3 s, `t.moveTo` (0.6 s) to the Theme button's centre;
  2. at 1.0 s, `t.click()`; `waitForMode(t, "white", before, 1.5)`; then the title must read "White
     theme (click for cream theme)"; `t.keyFrame("white")` once the fade is over (about 1.6 s);
  3. at 2.6 s, `t.click()`; `waitForMode(t, "cream", white, 1.5)`; the title must read "Cream theme
     (click for current theme)"; then `t.moveTo` (0.5 s) back to the parked point (off the
     toolbar); `t.keyFrame("cream")` at about 3.6 s;
  4. at 4.2 s, `t.zoom("charts", rect)`: the union of `drawingBox` of the diagram and of the chart,
     padded by 24 px (the kit caps the zoom at 2x);
  5. at 4.8 s, `t.mark("1", rect)`: the diagram's box with 8 px of air; at 6.6 s, `t.unmark("1")`;
  6. at 6.6 s, `t.mark("2", rect)`: the chart's box with 8 px of air; at 8.4 s, `t.unmark("2")`;
  7. at 9.5 s, `t.unzoom("charts")`; `until(10.5)`;
  8. `t.record("themeModes", ["dark", "white", "cream"])` (the modes shown, in order) for the PR.
- `verify(t)`: `t.workspaceFile("handbook.md")` must equal `STAGE`, else throw `handbook.md changed
  on disk: ${JSON.stringify(text)}`; return `{ modes: ..., unchanged: true }`.

**The seam.** The trial take (section 4) films the draft's version. When its `check` passes every
line, the draft's version is the clip. When only the line "loop seam SSIM at least 0.98 and below
1.0" fails, the batch films the **four-click version**, the smallest change that ends where it
starts:

- `setup` leaves the page in Cream (the default); `run` clicks four times, about 0.8 s apart
  (current, Dark, White, Cream; for example at 0.9, 1.7, 2.5 and 3.3 s), each with `waitForMode`
  against the mode before (the `src` pairs that follow each other all differ: Cream and current,
  current and Dark, Dark and White, White and Cream), the pointer leaves the toolbar, then the zoom,
  marks and unzoom as above, shifted by the take; `Length` stays at most 12 s.
- `clip.md`: section 1 is "1. Four clicks, four palettes"; its `Time` and `Shot` rows name the four
  clicks, from Cream back to Cream; the `setup` paragraph says frame 0 is Cream and no click is made
  off camera; the review note on the skipped current theme becomes "the current VS Code theme, the
  kit's Default Light Modern, shows for 0.8 s: it is close to White"; key frames
  `frames/dark.png`, `frames/white.png` and `frames/cream.png`. Text 1, Text 2, the zoom, the marks
  and the expected result's wording otherwise stay; the expected result lists the four modes.
- The PR's "Autonomous decisions" says which version was rendered, with the trial's measured SSIM.

Any other failing `check` line is fixed in the scenario or the storyboard (framing, times), never
by changing a check.

### 4. Trial take, take and render

On Windows, on this machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`):

```bash
just dev
just package                                   # out/reports/package/markdown-okf-schema-studio.vsix
just clip theme-switch doctor
just clip theme-switch all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

- The trial take (recipe section 1, adapted): (a) the preview webview is in the frames; (b) the CDP
  click on the Theme button switches the mode (step 2 of `run` passes); (c) the diagram and the
  chart are drawn again before the next step (`waitForMode` passes within 1.5 s; if a new drawing
  takes longer, the click times move apart, never the wait removed); (d) the retimed rate is at
  least the storyboard's frame rate; (e) the loop seam (above).
- The trial take's pictures and measured times go into `clip.md` (Q3); when the trial is clean it
  may be the take.
- `Length` and every time in `clip.md` follow the take (playback rate inside 0.77 to 1.3), in the
  same commit as the render; the two captions stay end to end from 0 to `Length`, the marks inside
  the zoom hold.
- Commit together (recipe rule): `clip.md`, `scenario.mjs`, `stage/handbook.md`, `theme-switch.mp4`,
  `.webm`, `.gif` (Git LFS through `.gitattributes`), `poster.png`, `contact-sheet.png`,
  `first-last.png`, `frames/*.png`, `check.json`.

### 5. Tests

In `docs/demo-video/clip-kit/lib/` (`node:test`, Node built-ins only, run by `just clip-kit-test`
inside `just check`), each reading the shipped files from the repository, path from the test
file's own location, at the head under test, never a copy:

- `storyboard.test.mjs` (CR-484) gains a case for the shipped
  `docs/demo-video/clips/theme-switch/clip.md`: `parseClip` gives size 1280x720, 15 fps, two
  captions with the draft's words (`**` aside) end to end from 0 to `Length`, no badge, zoom
  `charts`, marks `1` and `2` in turn inside the hold, each with the times of its row; and
  `validateStory` passes with a `take` object with no press, zoom `charts` and marks `1`, `2`, on
  `win32`.
- The test of CR-485 that loads each shipped `scenario.mjs` and passes its `checks` to
  `resolveChecks` gains `theme-switch`: `{ editMode: "off", paste: false }`.
- A case (in the same file as the previous one, or in `storyboard.test.mjs`) that imports the
  shipped `theme-switch/scenario.mjs` and asserts its `STAGE` equals the shipped
  `theme-switch/stage/handbook.md` byte for byte.
- `test/site/siteClips.test.ts`: a test "the shipped themes page plays the theme switch clip as
  video", modelled on "the shipped settings page plays the raw copy clip as video": it reads the
  shipped `docs/user/themes-and-motion.md`, renders it with `renderMyst` and `clipVideos`, asserts
  the `<video src="../demo-video/clips/theme-switch/theme-switch.webm"` and that
  `theme-switch.webm`, `.gif` and `poster.png` exist; marker
  `// @tests_req SwRS-MDOKFSTUDIO-CORE-095` (an added test of an existing SwRS, no SwRS text
  change); then `just requirements-update`.

### 6. Docs

- `docs/user/themes-and-motion.md`: under the first paragraph (before the table of the three
  captures), the image
  `![The Theme button is clicked twice: the whole page, the admonition, the Mermaid diagram and the Vega-Lite chart turn from Dark to White, then to Cream, and the diagram and the chart are drawn again in the new colours](../demo-video/clips/theme-switch/theme-switch.gif)`
  (for the four-click version: "clicked four times ... from Cream through the current theme, Dark
  and White back to Cream"). The same paragraph says "the third toolbar row" while the Theme button
  is on row 2 (`renderPreviewToolbar`, `docs/user/toolbar.md`): it becomes "the second toolbar row"
  (a fact on the page the clip sits in, said in "Autonomous decisions").
- No recipe change (CR-485 documents `checks` and `keyFrame`); no glossary change ("Theme mode" and
  "Feature clip" hold); no change to `README.md`, `CHANGELOG.md` or `docs/releases-notes/` (no
  `feat` or `fix` commit).

### 7. Host and default matrix

The clip depends on the shipped default theme mode (`cream`) versus a stored workspace choice, and
the mode `current` on the VS Code theme of the host profile.

| Host | VS Code theme | Stored theme mode | Expected | Proof |
| --- | --- | --- | --- | --- |
| Windows 11, kit profile | Default Light Modern (kit default) | none (fresh workspace: `cream`) | `setup` reaches the start mode; the filmed clicks show the modes in order, each drawing redrawn | the take's `setup` and `run` checks, `check.json` "scenario verify passed" |
| Windows 11, kit profile | Default Light Modern | a stored mode (a rerun in the same workspace) | `setup` clicks until the start mode whatever was stored; same film | `setup` step 3 (not filmed separately; the kit's workspace is fresh per take) |
| macOS, Linux | same | same | same | not proved (no take there) |

The new tests run on Windows locally and on Linux and Windows in `ci-static`.

### 8. Commits and the pull request

- Commits by area (Conventional Commits; no scope on `docs` or `test`):
  `docs: add the theme switch feature clip` (clip folder, `docs/user/themes-and-motion.md`),
  `test: check the theme switch clip's storyboard, stage and docs page` (the kit test cases,
  `siteClips.test.ts`, the files `just requirements-update` changes).
- The PR is opened as a draft (`gh pr create --draft`) and stays a draft until the owner approves
  the storyboard and the clip in it (Q3); the agent does not mark it ready.
- The PR body follows `.github/PULL_REQUEST_TEMPLATE.md`, the PR guideline and the clip PR rule of
  CR-484: the GIF inline from
  `https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/theme-switch/theme-switch.gif`,
  the MP4 and WebM linked with the same form at the same head; after each push of a new render the
  links move to the new head (`gh pr edit <n> --body-file <file>`); check that the GIF plays in the
  rendered PR page (if not, the fallback CR-484 settled).
- The body has a section "Deviation from the feature clip process": the recipe's storyboard review
  before the take was moved after it, into this PR, by the Chief of Staff's decision under the
  owner's overnight autonomy; the take was filmed from the Griller's draft; how a review lands: an
  *(on screen)* row changed by the owner is a render (`just clip theme-switch render` then
  `check`), a *(filmed)* row is a retake, a follow-up of this CR.
- The body states what the clip proves (real clicks on the Theme button in a real VS Code window
  switch the theme mode in order, and the diagram and the chart are drawn again for each mode before
  the next step: the take's checks and `verify`) and what the owner judges (motion, the fade, rhythm,
  the loop as watched, the texts, the version rendered); it links `clip.md` for the storyboard
  review.
- "Autonomous decisions": the differences from the draft (section above); the version rendered and
  the measured seam SSIM; the key frame names; the redraw check by `src`; the "second toolbar row"
  correction; the times.

## Out of scope

- Any change to `src/`, to an SwRS text or to the clip kit (CR-485 owns the kit changes this clip
  uses).
- The VS Code theme itself (no take with another `workbench.colorTheme`), high-contrast themes,
  reduced motion.
- A macOS or Linux take; placing the clip in release notes or the announcement (a release CR does
  it); replacing the three still captures of `docs/user/themes-and-motion.md`.
- A retake after the owner's review (a follow-up of this CR, Q3); marking the PR ready before the
  owner approves the storyboard and the clip (Q3); a change of the recipe's storyboard order.

## CI

No CI job changes. The new test cases run in `just check` through `just clip-kit-test`, inside the
existing `ci-static` job (Linux and Windows, `.github/workflows/ci.yml`); the site test runs where
`test/site/` tests run today.

- Environment: the CI machine set up by `just dev-ci` from the lock files, Node.js 24 from `.nvmrc`
  through `fnm`. Absent there and present locally: `ffmpeg`, the kit's scratch folder, the VS Code
  download, Remotion, a display. The new tests need none of them: the shipped `clip.md`,
  `scenario.mjs` and `stage/handbook.md` read from the repository, the shipped
  `docs/user/themes-and-motion.md` and the clip's committed files (Git LFS checked out as CI does
  for the raw copy clip's site test).
- Before the push: `just clip-kit-test`, `just check` and `just ci-static` on Windows.
- Only the first CI run proves the Linux leg (the dynamic `import` of the scenario from a repository
  path, the byte comparison of the stage with LF endings on both systems).

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows; the storyboard, scenario and stage tests
   read the shipped `clip.md`, `scenario.mjs` and `stage/handbook.md` at the head under test; the
   site test reads the shipped `docs/user/themes-and-motion.md`.
2. `just clip theme-switch all --vsix ...` passes; `check.json` shows `passed: true`, MP4 and WebM
   1280x720 at 15 fps, MP4 duration equal to `Length` within one frame, GIF at most 960 px and
   12 fps, loop seam SSIM in [0.98, 1.0), "Studio in reading mode at the start", no paste line,
   `verifyPassed: true`, playback rate inside 0.77 to 1.3, platform `win32`, extension source
   `vsix`.
3. The take's `run` passed: after each click the theme mode, the button's title and both drawings'
   `src` changed as section 3 says, within 1.5 s; `verify` found `handbook.md` unchanged.
4. The agent looks at the contact sheet and every key frame: Studio alone in the window in reading
   mode, the toolbar expanded, frame 0 in Dark (or Cream for the four-click version), the page,
   admonition, diagram and chart in White (`white`) and in Cream (`cream`) with no part left in the
   old colours, mark 1 on the flowchart and mark 2 on the bar chart in the zoom, Text 1 during the
   clicks and Text 2 during the zoom, no tooltip in the zoom or at the seam, no personal name or
   path, no dirty tab. What was not checked (motion, the fade, rhythm, the loop as watched) is said.
5. `just requirements-update` leaves the tree clean after its commit; `just preflight` passes (on
   Windows, its static stage).
6. The PR is a draft; its body plays the GIF, links the MP4 and WebM at the head sha and holds the
   "Deviation from the feature clip process" section.

## Open questions

None. The dependency on CR 485 is settled by clip-theme-Q4 (`depends.json` names it), and the loop back to the start by clip-theme-Q5 (the default above, picked by the take's `check`).
