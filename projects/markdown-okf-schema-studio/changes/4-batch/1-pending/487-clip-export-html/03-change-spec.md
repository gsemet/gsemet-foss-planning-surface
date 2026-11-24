# Feature clip: export the page to one HTML file

Short name: `clip-export`. No tracker issue (verbal request of the owner, 2026-11-25).

## Goal

A feature clip of Studio's Export to HTML, made with the clip kit and the feature clip recipe as the
CRs `short-demo-video-of-the-smart-raw-markdo` (short name `raw-copy-demo`, CR-484) and
`clip-drag-list-item` (CR-485) leave them: from a page in the Dark theme, the reader clicks Export,
saves `team-handbook.html`, opens it in a browser inside the filmed VS Code window and clicks a tab.
The browser shows the same themed page, with its Mermaid flowchart and working tabs. One continuous
shot, two captions in turn, two marks in turn, 1280x720 at 15 fps, MP4, WebM and GIF; the pull
request plays the clip and the owner reviews the storyboard and the clip there.

The clip shows the existing export (`src/session/features/htmlExport.ts`, `src/core/export/`,
`SwRS-MDOKFSTUDIO-TOOLBAR-134` to `-137`); no behaviour of the extension changes.

## Dependency and base

`depends.json`: after `short-demo-video-of-the-smart-raw-markdo` and `clip-drag-list-item`.
Neither is merged when this spec is written.

- From `raw-copy-demo` (its `03-change-spec.md`): the Markdown storyboard contract (`## Clip` table
  with `Length`, `Size`, `Frame rate`, `Outputs`, `Cards`, `Logo`, `Setting filmed`, `Filmed on`,
  `Stage`; one `## <n>. <beat>` section per beat with `Time`, `Shot *(filmed)*`, at most one
  `Text <n> *(on screen)*`, `Badge <id>`, `Zoom`, `Mark <id>`), captions in turn, marks in turn,
  combined badges `<Ctrl form> / <⌘ form>`, `Size` and `Frame rate` read from the storyboard, the
  key frames `frames/03-zoomed.png` and `frames/<NN>-mark-<id>.png`, the parser tests in
  `docs/demo-video/clip-kit/lib/storyboard.test.mjs` run by `just clip-kit-test` inside
  `just check`, and the clip PR rule (GIF inline from the PR's head, MP4 and WebM linked at the same
  head, `-assets` fallback).
- From `clip-drag-list-item` (its `03-change-spec.md`, section 5): a scenario may export
  `checks = { editMode, paste }`, resolved by `resolveChecks(checks)` and turned into the take's
  `check.json` lines by `takeLines(verify)` (both in `lib/check.mjs`); the helper
  `t.keyFrame(name)` (`lib/take.mjs`), written to `take.json` as `keyFrames` and turned into
  `frames/<name>.png` by `keyFrameTimes(take, story)` (`lib/encode.mjs`); and its test that loads
  each shipped `scenario.mjs` and passes its `checks` to `resolveChecks`.
- This CR makes **no kit change**: it reuses those. Base: the branch of `clip-drag-list-item` when
  the batch stacks the three, else `origin/main` once both are merged (fetch first: the local `main`
  is behind `origin/main`). Where either CR lands differently from its spec (a field name, a frame
  name, a test file name), this CR follows what it merged and says so in the PR's "Autonomous
  decisions".

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| clip-export-Q1 | One CR per clip, this one the export clip, made with the kit and recipe as the CRs it depends on leave them | whole spec |
| clip-export-Q2 | The captions, stage and timing of the Griller's storyboard draft are the clip's shape; the owner reviews them | sections 1, 2 |
| clip-export-Q3 | The batch does not wait for a storyboard approval before the take: it films a trial take from the draft, puts its pictures in the storyboard, renders, and opens the PR with the clip watchable; the PR stays a draft until the owner approves storyboard and clip; the deviation from the recipe's order is reported here and in the PR body; a retake after the owner's review is a follow-up of this CR | sections 1, 4, 7, "Deviations" |
| clip-export-Q4 | If the trial cannot show the Integrated Browser's page in the frames and reach it over CDP, the Driver tries in this order, in this CR only: (a) an older VS Code pinned for this clip through `DEMO_CODE`, if its Simple Browser is a webview the kit films; (b) a preview extension that shows the page in a webview, installed in the throwaway profile; (c) a second half that keeps the export and shows the exported file's opening lines in the text editor, captions adjusted; never OS-level capture, no kit change beyond `clip-drag-list-item`'s; the PR says which way was taken; the CR stops and reports only if all three fail | section 4 (the trial's gate), section 7 |

## Deviations

- **From the recipe** (`docs/demo-video/guidelines/feature-clip-process.guidelines.md`, "The
  storyboard first", as `raw-copy-demo` writes it): the maintainer's storyboard review moves from
  before the take to the pull request (clip-export-Q3). The committed `clip.md` keeps
  `status: draft for the owner's review`; the PR stays a draft until the owner approves. The PR body
  says so in one sentence under "Autonomous decisions".
- **From the storyboard draft** (`work/storyboard/clip.md` of this CR's folder): the draft opens
  the exported file in VS Code's **Simple Browser** ("Simple Browser: Show" typed in the command
  palette). The pinned VS Code 1.147.0 (`DEFAULT_CODE_VERSION`) does not offer it, read in its
  built-in `extensions/simple-browser`:
  - its `package.json` shows `simpleBrowser.show` in the command palette only `when: isWeb`, so it
    is absent from the desktop palette;
  - its `dist/extension.js` sends `simpleBrowser.show` (and `simpleBrowser.api.open`) to
    `workbench.action.browser.open` whenever that command exists, which it does in 1.147.0: the
    **Integrated Browser** ("Browser: Open Integrated Browser", category `Browser`, `f1`, no
    precondition, in `out/vs/workbench/workbench.desktop.main.js`).

  So the clip uses the Integrated Browser in place of the Simple Browser. Only rows marked
  *(filmed)* and the review notes change; every row marked *(on screen)* (both texts, the badge, the
  marks and their times) stays as the draft has it. The Integrated Browser draws its page in a
  browser view of its own (the workbench names it `browserView`, with a `dimOnOverlay` setting for
  overlays drawn over it), which may not be in the CDP screencast of the workbench page: the trial of
  section 4 proves it first, and a failure takes the fallbacks of clip-export-Q4.

## What changes

All paths are relative to the repository root.

### 1. The stage: `docs/demo-video/clips/export-html/stage/team-handbook.md`

Copied byte for byte from `work/storyboard/stage/team-handbook.md` of this CR's folder (in the
planning surface,
`C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/2-backlog/P2/clip-export-html/`,
or wherever the batch moved the folder): the heading "Team handbook", the sentence "How a change goes
from an idea to a release.", a Mermaid `flowchart LR` (Idea, Review, Merge, Release) and a
`tab-set` of two tabs, "Review" ("Every change gets one approving review.") and "Release" ("We
release on Thursday, after the smoke tests."). It has no link to another file (so the export asks no
link question, `removedLinksWarning`) and no image.

### 2. The live storyboard: `docs/demo-video/clips/export-html/clip.md`

The draft `work/storyboard/clip.md`, adapted only as follows; every *(on screen)* text and time
stays as drafted:

- Front matter: `title: Feature clip export-html`, `status: draft for the owner's review`
  (clip-export-Q3), `date:` the day of the commit.
- Opening paragraph: speaks of the repository, as `raw-copy-demo` words it for its clip ("This is
  the live storyboard. The clip is built from this file: edit any row marked *(on screen)*, save,
  and run `just clip export-html render`, then `check`. Rows marked *(filmed)* describe the take:
  changing them means a new take."), plus one sentence: the owner reviews this file and the clip in
  the pull request; the times and pictures come from the batch's take. Drop "Once approved, this
  file becomes ..." and "The times below are the Griller's proposal ...". Keep: one continuous shot,
  two texts in turn, `**bold**` takes the orange accent.
- The paragraph on the browser is rewritten for the Integrated Browser: it is VS Code's own browser,
  opened from the command palette inside the filmed window; `setup` starts a small static server on
  `http://localhost:5170/` over the workspace (Node.js, off camera), so the address bar shows no
  file path; the server never holds the kit's process open.
- `## Clip` table: the `Format` row split as the contract asks: `Size *(on screen)*` =
  `1280x720 16:9`, `Frame rate *(on screen)*` = `15 fps`, `Outputs` = "silent, loops; MP4 (X,
  release), WebM (docs site), GIF 960 px (release notes, docs page)". `Length` `12.0 s` unless the
  take needs another value (section 4). `Cards` `none`, `Logo` `top right`. `Setting filmed`:
  `files.simpleDialog.enable`: on (the save dialog is VS Code's own, inside the window). `Filmed
  on`: Windows, the VS Code version and the extension version written in `check.json`, "VSIX built
  from the branch". `Stage` as drafted (Studio, the whole window, reading mode, Dark theme).
- "Off camera (`setup`)" line as drafted, the server's address included.
- `## 1. Export, then open the file`: `Time` as drafted, with "command palette at 2.8 s, "Browser:
  Open Integrated Browser" chosen at 4.0 s, the address entered at 5.0 s, the page shown at 5.6 s";
  `Shot *(filmed)*`: as drafted up to the command palette, then "Browser: Open Integrated Browser"
  is typed and chosen, `http://localhost:5170/team-handbook.html` is typed in its address bar, Enter,
  and the Integrated Browser shows the exported page in Dark (where VS Code opens it: the take says
  where, and the row says it). `Text 1 *(on screen)*` = `**Export** the page to one HTML file`.
  `Badge palette *(on screen)*` = `Ctrl+Shift+P / ⇧⌘P`.
- `## 2. The same page in the browser`: `Time` as drafted; `Shot *(filmed)*` with "Integrated
  Browser" for "Simple Browser"; add the row `Zoom | page, hold to 11.0 s` (the hold the `Time` row
  states: the kit reads the zoom from this row, and refuses a mark without a zoom). `Mark 1 *(on
  screen)*` = `Orange outline around the flowchart, 6.6 to 8.0 s`; `Mark 2 *(on screen)*` =
  `Orange outline around the tab set, after the click, 8.6 to 10.2 s`; `Text 2 *(on screen)*` =
  `Any browser shows the **same themed page**`.
- Pictures (the lines "Pictures: from the batch's trial take."): links to the take's key frames in
  `frames/`: section 1 shows `frames/save-dialog.png` and `frames/exported.png`; section 2 shows
  `frames/04-mark-1.png` and `frames/05-mark-2.png` (`t.keyFrame` names, section 3; mark frames as
  `raw-copy-demo` numbers them), each with an alt text saying what it shows. No `images/` folder, no
  JPEG.
- "Expected result" list kept, with the Integrated Browser for the Simple Browser and the panel
  check worded as section 3 does it (the exported tab set uses radio inputs and labels,
  `src/core/export/exportTabs.ts`, so a panel is shown or hidden by the file's style sheet, not by
  `hidden`).
- "Review notes": keep the palette-time option (for the owner's review in the PR, with the
  Integrated Browser opened off camera on the address that does not exist yet and only reloaded in
  the clip), the note on `files.simpleDialog.enable`, the note on the port and the note on the loop
  seam. Replace the Simple Browser note by: the Simple Browser is not in the desktop palette of VS
  Code 1.147.0 and opens the Integrated Browser, so the clip films the Integrated Browser; the trial
  proved its page is in the screencast frames (with the measured fact). Add: Studio's information
  message "Exported to `team-handbook.html`." shows at the bottom right after the save and is kept
  as filmed (it is the feature's own confirmation); the badge `⇧⌘P` is drawn as one keycap (the
  kit splits a `⌘` group only when it starts with `⌘`).

### 3. The scenario: `docs/demo-video/clips/export-html/scenario.mjs`

In the style of `clips/raw-copy-balance-edges/scenario.mjs`; the header comment says what is filmed
and that every text and time is in `clip.md`. It imports Node built-ins only (`node:http`,
`node:fs`, `node:os`, `node:path`) and does nothing at import, so the kit's test can load it.

- `stage = { "stage/team-handbook.md": "team-handbook.md" }`; `open = ["team-handbook.md"]`.
- `settings`: `"workbench.editorAssociations": { "team-handbook.md":
  "markdown-okf-schema-studio.editor" }` (it opens in Studio, as `runbook.md` in the raw copy clip)
  and `"files.simpleDialog.enable": true`.
- `checks = { editMode: "off", paste: false }` (from `clip-drag-list-item`): reading mode at the
  start, no paste line.
- Constants: no copy of the stage text: `verify` compares the workspace file with the clip's
  own `stage/team-handbook.md`, read from the clip folder (`new URL("stage/team-handbook.md",
  import.meta.url)`). `SHOWN = "We release on Thursday, after the smoke tests."`, `HIDDEN = "Every
  change gets one approving review."`.
- A local static server: `node:http` `createServer` serving the files of `t.workspace` (path joined
  and checked to stay inside it; `.html` as `text/html; charset=utf-8`, 404 otherwise) on
  `127.0.0.1`, port 5170, else the next free port up to 5179 (the typed address uses the port
  bound); `server.unref()` so a failed take never keeps `just clip` running; closed at the end of
  `verify` (and on any throw of `verify`).
- `setup(t)`, off camera:
  1. Refuse a personal path: when `t.workspace` contains `os.userInfo().username` (case
     insensitive), throw "the save dialog would show the workspace path with your user name: run
     the take with CLIP_SCRATCH set to a folder without it (for example C:/okfclip)". The simple
     save dialog shows the target's full path inside the filmed window.
  2. `await t.frameOf()`; reading mode as in the raw copy scenario (`readingMode(t)`, click
     `[data-sphinx-preview-edit-toggle]` when it is `"on"`); `t.record("readingMode", mode)`; throw
     when not `"off"`.
  3. Expand the toolbar only when `[data-sphinx-preview-toolbar-collapse]` has
     `aria-expanded="false"` (collapsed is the default, `toolbarCollapsed: true` in
     `src/core/state/previewViewPreferences.ts`); then click `[data-sphinx-preview-theme-toggle]`
     until `document.documentElement` has `data-sphinx-preview-theme-mode="dark"` (at most four
     clicks: the cycle is current, dark, white, cream, `src/page/features/themeMode.ts`; the default
     is cream, and a second take finds the stored mode), re-reading the frame between clicks; throw
     when it is not dark.
  4. Start the server; check `GET /team-handbook.md` answers 200 (the server works before the
     take).
  5. Park the pointer off the toolbar and off every block, `t.moveTo(900, 420, 0.1)`, `t.sleep(500)`
     (no tooltip at frame 0 or at the loop seam).
- `run(t)`, timed with `until(seconds)` as in the raw copy scenario, at the draft's times:
  1. at 0.2 s, `t.moveTo` (0.6 s) to the centre of `[data-sphinx-preview-export]` (the frame's
     element box plus the frame's offset, as `textEdges` does); at 0.8 s, `t.click()` (a real click:
     the host accepts the export only with a user gesture, `HtmlExportController.handle`);
  2. wait for the simple save dialog (`.quick-input-widget` visible, its input's value ending with
     `team-handbook.html`); throw when the value contains the user name; `t.keyFrame("save-dialog")`;
     at 2.0 s, `t.page.keyboard.press("Enter")` (not `t.press`: no badge); poll for
     `team-handbook.html` in the workspace, at most 5 s;
  3. move the pointer away from the Export button (so its `data-tooltip` does not show); at 2.8 s,
     `t.press("ControlOrMeta+Shift+P", "palette")`; type "Open Integrated Browser" with
     `t.page.keyboard.type(text, { delay: 40 })`; at 4.0 s, Enter;
  4. type `http://localhost:<port>/team-handbook.html` in the Integrated Browser's address bar
     (focused on open; the trial confirms), Enter at 5.0 s; wait for the browser view's page
     (section 4, trial (b)): a page of `t.context.pages()` whose URL is that address, loaded;
     `t.keyFrame("exported")` once its heading is shown;
  5. at 6.0 s, `t.zoom("page", rect)`: the browser's content area in workbench page coordinates
     (the bounds of the Integrated Browser's editor pane in the workbench DOM), padded by 24 px,
     at most 2x;
  6. at 6.6 s, `t.mark("1", rect)` around the flowchart's SVG (its box read in the browser view's
     page, mapped to workbench coordinates by the pane's offset and the view's zoom); at 8.0 s,
     `t.unmark("1")`;
  7. at 7.6 s, `t.moveTo` (0.7 s) to the label "Release" (`label.myst-tab` with text "Release",
     mapped the same way); at 8.4 s, `t.ev("click", t.pointer)` (the kit draws the ripple) and the
     click dispatched to the browser view's page at the label's own coordinates
     (`browserPage.mouse.click(x, y)`), since a click on the workbench page does not reach a browser
     view of its own; then poll that `SHOWN` is visible and `HIDDEN` is not (`checkVisibility()` of
     their panels), at most 1 s, else throw (a finding against the feature);
  8. at 8.6 s, `t.mark("2", rect)` around the tab set (`.sd-tab-set` or the element holding the
     radios and labels, as the exported file names it); at 10.2 s, `t.unmark("2")`;
  9. at 11.0 s, `t.unzoom("page")` and `t.moveTo(home.x, home.y, 0.6)`; `until(12.0)`.

  When the Integrated Browser opens in Studio's editor group rather than beside it, the scenario
  keeps that placement (it is VS Code's own), and the `Shot` row says it.
- `verify(t)`: read from disk and from the browser view's page:
  - `team-handbook.html` exists next to `team-handbook.md`, and the workspace holds no other new
    file (the set of files equals the stage's plus `team-handbook.html`);
  - its text has no `<script`, no `<link`, no `@import`; every `src` and `href` attribute value
    starts with `#` or `data:`; it holds an `<svg` (the flowchart embedded);
  - its `<html>` element carries `data-sphinx-preview-theme-mode="dark"`;
  - in the browser view's page, `SHOWN` is visible and `HIDDEN` hidden (as in step 7);
  - `team-handbook.md` on disk equals the clip's `stage/team-handbook.md` byte for byte;
  - each failure throws with what was found; returns `{ size, themeMode, port }`.

### 4. Take and render

On Windows, on this machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`), with the scratch folder outside the user's
profile, so no frame shows the user name:

```bash
just dev
just package                                   # out/reports/package/markdown-okf-schema-studio.vsix
CLIP_SCRATCH=C:/okfclip just clip export-html doctor
CLIP_SCRATCH=C:/okfclip just clip export-html all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

(PowerShell: `$env:CLIP_SCRATCH = "C:/okfclip"` first.) The new scratch folder downloads the pinned
VS Code and Remotion once.

- **A trial first** (recipe section 1), adapted to this clip, before the full clip is judged:
  (a) the preview webview, the simple save dialog **and the Integrated Browser's page** are in the
  screencast frames (look at the frames after "exported"); (b) the Integrated Browser's page is
  reachable as a page of `t.context.pages()` (marks, click, `verify`); (c) the click on "Release"
  switches the panel; (d) the retimed rate is at least the storyboard's frame rate.
  If (a) fails for the Integrated Browser (its area blank, black or frozen in the frames) or (b)
  fails, the Driver keeps the failing frames as evidence and tries, in this order and in this CR
  only (clip-export-Q4), each with a new trial of the same points:
  1. an older VS Code pinned for this clip through `DEMO_CODE` (a local install of that version),
     if its Simple Browser is a webview in the workbench page that the kit films; the scenario then
     opens it as the draft has it ("Simple Browser: Show", the address typed), and `check.json`
     writes the version used;
  2. a preview extension that shows the page in a webview, installed in the throwaway profile;
  3. a second half of the storyboard that keeps the export and shows the opening lines of
     `team-handbook.html` in the text editor, with the captions, marks and `Expected result` of
     section 2 adjusted to it (the *(on screen)* rows change: the owner reviews them in the PR).

  Never OS-level capture or input, and no change to the clip kit beyond what `clip-drag-list-item`
  owns: a fallback that would need one counts as failed. The first fallback whose trial passes is
  filmed; `clip.md`, the scenario, the docs alt text, the matrix's VS Code cell and the PR follow
  it. Only when all three fail does the work stop and report, with the frames of each try. The
  other trial failures follow the recipe.
- `Length` and every time in `clip.md` follow the take (playback rate inside 0.77 to 1.3), in the
  same commit as the render; the captions stay end to end from 0 to `Length`, the marks inside the
  zoom hold.
- Commit together (recipe rule): `clip.md`, `scenario.mjs`, `stage/team-handbook.md`,
  `export-html.mp4`, `.webm`, `.gif` (Git LFS through `.gitattributes`), `poster.png`,
  `contact-sheet.png`, `first-last.png`, `frames/*.png`, `check.json`. `frames/` also holds
  `01-selected.png` and `02-pasted.png`, which `keyFrameTimes` writes at the take's one press (the
  palette chord); they are kept as the kit writes them and not linked from `clip.md`.

### 5. Tests (no kit code change)

In `docs/demo-video/clip-kit/lib/`, run by `just clip-kit-test` inside `just check`:

- `storyboard.test.mjs` gains a case that reads the shipped
  `docs/demo-video/clips/export-html/clip.md` from the repository (path from the test file's own
  location, at the head under test, never a copy) with `parseClip` and asserts: `Length` the
  committed value, size 1280x720, 15 fps, two captions with the exact texts of section 2 end to end
  from 0 to `Length`, badge `palette` = `Ctrl+Shift+P / ⇧⌘P`, zoom `page`, marks `1` and `2` in
  turn inside the hold, no "Expected paste" block (`expectedPaste` is `null`); and `validateStory`
  passes with a `take` object with press `palette`, zoom `page` and marks `1`, `2`, once on `win32`
  and once on `darwin` (the combined badge).
- The test of `clip-drag-list-item` that loads each shipped `scenario.mjs` gains
  `export-html`: its `checks` resolve to `{ editMode: "off", paste: false }`.

### 6. Docs

- `docs/user/toolbar.md`, section "Export to HTML": after its first paragraph ("The Export button,
  or the command **Export to HTML** ... Cancel writes nothing."), the image
  `![From a page in the Dark theme, Export saves team-handbook.html; opened in VS Code's Integrated Browser, it shows the same dark page with its flowchart, and a click on a tab shows its panel](../demo-video/clips/export-html/export-html.gif)`
  (the recipe: the GIF goes to the feature's docs page).
- `test/site/siteClips.test.ts`: a test "the shipped toolbar page plays the export clip as video",
  modelled on the settings page one: it reads the shipped `docs/user/toolbar.md`, renders it with
  `renderMyst` and `clipVideos`, asserts the `<video src="../demo-video/clips/export-html/export-html.webm"`
  and that `export-html.webm`, `.gif` and `poster.png` exist; marker
  `// @tests_req SwRS-MDOKFSTUDIO-CORE-095` (an added test of an existing SwRS, no SwRS text
  change); then `just requirements-update`.
- No change to the recipe, the glossary, `README.md`, `CHANGELOG.md` or `docs/releases-notes/` (no
  `feat` or `fix` commit). The deviation of clip-export-Q3 is not written into the recipe.

### 7. Commits and the pull request

- Commits by area (Conventional Commits; no scope on `docs` or `test`):
  `docs: add the export to HTML feature clip` (clip folder, `docs/user/toolbar.md`),
  `test: check the export clip's storyboard and play it on the toolbar page` (the kit test cases,
  `siteClips.test.ts`, the files `just requirements-update` changes).
- The PR is opened as a **draft** and stays one until the owner approves the storyboard and the
  clip (clip-export-Q3). Its body follows `.github/PULL_REQUEST_TEMPLATE.md`, the PR guideline and
  the clip PR rule of `raw-copy-demo`: the GIF inline from
  `https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/export-html/export-html.gif`,
  the MP4 and WebM linked with the same form at the same head; after each push of a new render the
  links move to the new head (`gh pr edit <n> --body-file <file>`); check that the GIF plays in the
  rendered PR page, else the `-assets` fallback.
- The body states what the clip proves (a real click on Export in a real VS Code window writes one
  self-contained file in the Dark mode of the page; a browser shows it with its flowchart and a
  working tab: the take's `run` checks and `verify`) and what the owner judges (motion, rhythm, the
  loop as watched, the slow palette beat and its option, the texts and their accent); it links
  `clip.md` for the storyboard review and says a retake after review is a follow-up of this CR.
- The body says which way the browser part was filmed: the Integrated Browser, or the fallback of
  clip-export-Q4 taken ((a), (b) or (c)), with why the earlier ways failed (the trial frames).
- "Autonomous decisions": the recipe order moved to the PR (clip-export-Q3); the Integrated Browser
  in place of the Simple Browser, with the code facts of "Deviations"; the address typed with
  `http://`; the browser's placement as VS Code gives it; the `Zoom` row; the take under
  `CLIP_SCRATCH`; the information message kept as filmed; `⇧⌘P` as one keycap; the docs placement;
  the frames `01-selected` and `02-pasted` left as the kit writes them.

## Out of scope

- Any change to `src/`, to an SwRS text or to the kit's code (`docs/demo-video/clip-kit/` beyond
  test cases); a change of the recipe.
- A browser outside the VS Code window, an OS-level capture or input, a kit change beyond
  `clip-drag-list-item`'s (such as a second screencast composited by the kit), clip-export-Q4.
- A macOS or Linux take; placing the clip in release notes or the announcement (a release CR does
  it); a retake after the owner's review (a follow-up of this CR, clip-export-Q3).

## CI

No CI job changes. The new test cases run in `just check` through `just clip-kit-test`, inside the
existing `ci-static` job (Linux and Windows, `.github/workflows/ci.yml`); the site test runs where
`test/site/` tests run today.

- Environment: the CI machine set up by `just dev-ci` from the lock files, Node.js 24 from `.nvmrc`
  through `fnm`. Absent there and present locally: `ffmpeg`, the kit's scratch folder, the VS Code
  download, Remotion, a display. The tests need none of them: the shipped `clip.md`, `scenario.mjs`
  (loaded, never run) and `docs/user/toolbar.md`, and the clip's committed files (Git LFS checked
  out as CI does for the raw copy clip's site test).
- Before the push: `just clip-kit-test`, `just check` and `just ci-static` on Windows.
- Only the first CI run proves the Linux leg (loading the scenario, which imports `node:http` and
  `node:os`, from a repository path).

## Host and default matrix

The clip films a configured value of a VS Code setting (`files.simpleDialog.enable` on: off, the
system save dialog is outside the filmed page) and Studio's defaults otherwise (the Dark mode is a
toolbar choice, not a setting).

| Host | VS Code | Settings | Expected | Proof |
| --- | --- | --- | --- | --- |
| Windows 11, CDP click and keys | pinned `DEFAULT_CODE_VERSION` (1.147.0 unless moved) | `files.simpleDialog.enable` on | one self-contained `team-handbook.html` in Dark; the Integrated Browser shows it and the tab click works | the take's `run` checks and `verify`, `check.json` ("scenario verify passed") |
| macOS | same | same | same | not proved (no macOS take) |
| Linux | same | same | same | not proved |
| any | same | `files.simpleDialog.enable` off (default) | the system save dialog, outside the filmed page | not filmed; stated in the review notes |

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows; the storyboard case reads the shipped
   `clip.md`, the scenario case loads the shipped `scenario.mjs`, the site test reads the shipped
   `docs/user/toolbar.md`, all at the head under test.
2. The trial's four points, with what was seen for (a) and (b) (the frame names).
3. `CLIP_SCRATCH=C:/okfclip just clip export-html all --vsix ...` passes; `check.json` shows
   `passed: true`, MP4 and WebM 1280x720 at 15 fps, MP4 duration equal to `Length` within one
   frame, GIF at most 960 px and 12 fps, loop seam SSIM in [0.98, 1.0), "Studio in reading mode at
   the start", no paste line, `verifyPassed: true`, playback rate inside 0.77 to 1.3, platform
   `win32`, extension source `vsix`.
4. The agent looks at the contact sheet and every key frame: Studio in Dark with the expanded
   toolbar, the save dialog with `team-handbook.html` and no user name in its path, the palette
   with the badge `Ctrl+Shift+P / ⇧⌘P`, the browser page in Dark with the flowchart and the tab set,
   Text 1 during the export and Text 2 during the zoom, each mark on its element in turn, the panel
   "Release" shown after the click, no tooltip (the Export button's "Export to HTML"), no personal
   name or path, no dirty tab. What was not checked (motion, rhythm, the loop as watched) is said.
5. `just requirements-update` leaves the tree clean after its commit; `just preflight` passes (on
   Windows, its static stage).
6. The draft PR plays the GIF and links the MP4 and WebM at the head sha (or the `-assets`
   fallback), and says the storyboard review is the owner's, in that PR.

## Open questions

None: `02-answers.md` (clip-export-Q1 to Q4) and the code settle every point this specification
needs.
