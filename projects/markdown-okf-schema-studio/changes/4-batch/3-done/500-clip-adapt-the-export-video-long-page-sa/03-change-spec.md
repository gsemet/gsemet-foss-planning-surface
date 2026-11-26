# Clip: export a long report page, same render in the browser

Short name: `clip-export-long`. No tracker issue (verbal request of the owner, relayed by the Chief
of Staff, 2026-11-25).

## Goal

Rework the merged `export-html` feature clip (CR-487, PR 508) into a stronger story. Studio shows a
long report page in its default Cream theme: card grids, a very wide table, a small table, two
Mermaid diagrams, a Vega-Lite chart and a full Vega chart. The wide table breaks out of the centred
text column (the Auto width mode). The clip scrolls through the page, exports it with the Export
button, then opens the exported file in a browser: the same page, the wide table still breaking
out, the diagrams and charts drawn. What the clip sells: a reader with no editor gets the page
exactly as the writer sees it.

The clip is made with the merged clip kit (`docs/demo-video/clip-kit/`) and the feature clip recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`): one continuous shot of about
18 s in three beats, three captions in turn, one zoom with three marks in turn, 1280x720 at 15 fps,
no card, the logo top right, a loop; MP4, WebM and GIF. It **replaces in place** the storyboard,
scenario and stage of `docs/demo-video/clips/export-html/` (same clip folder, same output file
names) and updates what points at the old clip. The pull request plays the clip and the owner
reviews the storyboard and the clip there.

The clip shows existing features: the export (`src/core/export/exportSnapshot.ts`,
`src/core/export/exportContent.ts`), the Auto width mode (`src/page/modules/widthMode.ts`), Mermaid
and Vega drawing (`src/page/modules/mermaidPreview.ts`, `src/page/modules/vegaPreview.ts`,
`ChartKind = "vega-lite" | "vega"` in `src/core/render/chartData.ts`). No behaviour of the extension
changes and no rendered syntax changes (the writing skill
`skills/writing-for-markdown-okf-schema-studio/` is not touched).

## Dependency and base

- `depends.json`: `{"after": ["clip-the-advanced-renderings-tour"]}` (export-long-Q5). That CR owns
  the kit change that lets a clip run up to 30 s (`MAX_LENGTH` 12 to 30 in
  `docs/demo-video/clip-kit/lib/storyboard.mjs`, the duration line of `lib/check.mjs`, the recipe and
  the glossary). This clip runs 18 s, so it cannot parse or pass `check` without it. **This CR makes
  no kit change of its own.**
- Base: the branch of `clip-the-advanced-renderings-tour` in the batch-09 stack (its first commit,
  `build: let a feature clip run up to 30 seconds`, is enough), or `origin/main` once that CR is
  merged. Fetch first: the local `main` is behind `origin/main`.
- export-long-Q4 ("built on main, alone, no `depends.json`") is superseded on this one point by
  export-long-Q5 and the `depends.json` the Griller wrote after it; Q4 still holds for the other
  four clips of the round: this CR depends on none of them.
- The merged clips' committed files stay as they are, `export-html/check.json` excepted (it is
  rewritten by this CR's take).

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| export-long-Q1 | The owner's wish: Cream; a long page with tables, card grids, Mermaid and Vega; one table very wide, breaking out of the centred column (Auto); view 1 scrolls the page then exports; view 2 shows the exported HTML renders the same, diagrams drawn; it reworks the merged `export-html` clip | whole spec |
| export-long-Q2 | The captions, stage and timing of the Griller's storyboard draft are the clip's shape | sections 1, 2, 3 |
| export-long-Q3 | The batch films a trial take from the draft, puts its pictures in the storyboard, renders, opens the PR with the clip watchable (GIF inline, MP4 and WebM linked at the head); the PR stays a draft until the owner approves; the deviation is reported here and in the PR body; a retake after review is a follow-up of this CR | "The storyboard gate, moved after the take", sections 5, 8 |
| export-long-Q4 | Built from the merged kit and recipe; depends on none of the other clips of the round except as Q5 says | "Dependency and base" |
| export-long-Q5 | 18.0 s, three beats with a caption each: the scroll in Studio (0 to 5.8 s), the export and the browser opening (5.8 to 10.0 s), the same page in the browser with three marks (10.0 to 18.0 s); the 30 s limit comes from `clip-the-advanced-renderings-tour`; no kit change here | "Dependency and base", sections 2, 3 |
| export-long-Q6 | New stage `platform-report.md` replaces `team-handbook.md`: a heading, two card grids, a 16-column table, a 3-column table, two Mermaid diagrams (flowchart, sequence), two charts | section 1 |
| export-long-Q7 | Width mode Auto, set off camera with the Width button; `preview.maxContentWidth` 720 for the clip | sections 2, 3 |
| export-long-Q8 | Cream filmed as the default (no Theme click); the tab set and its click are dropped; the PR says the clip no longer claims a forced theme or JavaScript-free tabs; the GIF's alt text in `docs/user/toolbar.md` and the kit tests that read the shipped clip are updated | sections 1, 3, 6, 7, 8 |
| export-long-Q9 | The browser is the Integrated Browser over the local server, opened from the command palette in the same editor group, as in the merged clip; opening it off camera stays an option in the review notes | sections 2, 3 |
| export-long-Q10 | The scroll is a CDP mouse wheel in small steps, in Studio and in the browser; fallback a smooth `scrollTo` in the page, reported in the PR | section 3 |
| export-long-Q11 | The one zoom is on the browser part, three marks in turn: the wide table, the flowchart, the bar chart; Studio's breakout is shown unzoomed in beat 1 | sections 2, 3 |
| export-long-Q12 | Studio's sticky heading band left at its default; the captions say "same page", not "same window" | sections 2, 3 |
| export-long-Q13 | The bar chart is a `vega-lite` fence, the line chart a full `vega` fence | sections 1, 3 |

## The storyboard gate, moved after the take

The recipe ("The storyboard first") has the maintainer review the storyboard before the take.
export-long-Q3 moves that gate into the pull request; it does not drop it:

- the batch films a trial take from the draft, puts its pictures and measured times in the
  storyboard, replaces `docs/demo-video/clips/export-html/clip.md` with it (`status: draft for the
  owner's review`), films the take (the trial may be the take when it is clean), renders and opens
  the PR;
- the PR is a draft (`gh pr create --draft`) until the owner approves the storyboard and the clip;
  the agent never marks it ready; the PR body reports the deviation (section 8);
- the recipe is not changed by this CR.

## What changes

All paths are relative to the repository root. The clip folder is
`docs/demo-video/clips/export-html/`.

### 1. The stage: `stage/platform-report.md` replaces `stage/team-handbook.md`

- `git rm docs/demo-video/clips/export-html/stage/team-handbook.md`.
- Add `stage/platform-report.md`, copied byte for byte from `work/storyboard/stage/platform-report.md`
  of this CR's folder (in the planning surface,
  `C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/2-backlog/P2/clip-adapt-the-export-video-long-page-sa/`,
  or wherever the batch moved the folder), LF line endings, ending with one newline. In order: the
  heading "Platform report, 2026", one sentence, a `{grid} 1 1 3 3` of three `grid-item-card`s
  (Uptime, Deploys, Incidents); `## Deploys by service` and the 16-column table (Service, Team,
  Region, Tier, Jan to Dec right-aligned; five rows checkout-api, search-index, notifications,
  media-store, auth-gateway); `## How a change ships`, a `mermaid` `flowchart LR` (Pull request,
  Review, Canary, Release) and a `vega-lite` bar chart (deploys per quarter, width 520, height 120);
  `## Incident response`, a `mermaid` `sequenceDiagram` (Pager, On-call, Team) and a `vega` line
  chart (minutes to restore, six months, width 520, height 120); `## On-call` and a 3-column table
  (Week, Primary, Backup; two rows); `## Next year` and a second grid of three cards. It links no
  file and reads no data file.
- **The shared table.** The 16-column table is the table shared with the CR
  `clip-the-auto-margin-mode-on-a-very-wide` (CR-498, clip `wide-table-auto-width`, stage
  `stage/deploys.md`): that clip's table is this one plus a last Total column, cell for cell. When
  CR-498 is merged on this CR's base (or in the same stack) and its trial changed its table
  (dropped Total, or dropped month columns from the end), this stage's table is aligned to it: the
  same rows and cells, without Total. Any such change, and any change this CR's own trial makes
  (section 5: month columns dropped from the end, Dec first, only if the table needs a sideways
  scroll of its own in the editor), is named in the storyboard's review notes and in the PR's
  "Autonomous decisions". This CR does not edit CR-498's folder or clip.
- The committed stage is the filmed one.

### 2. The live storyboard: `clip.md` replaced

The draft `work/storyboard/clip.md` of this CR's folder replaces the merged `clip.md`, adapted only
as follows; every row marked *(on screen)* keeps its text, and the times follow the take:

- Front matter: `title: Feature clip export-html`, `status: draft for the owner's review`, `date:`
  the day of the commit.
- Opening paragraph: as the merged `export-html/clip.md` words it ("**This is the live
  storyboard.** The clip is built from this file: edit any row marked *(on screen)*, save, and run
  `just clip export-html render`, then `check`. Rows marked *(filmed)* describe the take: changing
  them means a new take. The owner reviews this file and the clip in the pull request; the times and
  pictures come from the batch's take. `**bold**` in a text takes the orange accent."). Then the
  draft's paragraph on the three beats and the paragraph on the Integrated Browser and the local
  server, as drafted. Drop "draft for review", "Once the trial take has added its pictures, this
  file replaces ..." and "The times below are the Griller's proposal ...".
- `## Clip` table as drafted: `Length` `18.0 s` (or the take's value, within the kit's 5 to 30 s),
  `Size *(on screen)*` `1280x720 16:9`, `Frame rate *(on screen)*` `15 fps`, `Outputs` as drafted,
  `Cards` `none`, `Logo` `top right`, `Setting filmed` as drafted (`preview.maxContentWidth` 720,
  `files.simpleDialog.enable` on), `Filmed on` as the merged clip words it, `Stage` as drafted.
- "Off camera (`setup`)" paragraph as drafted (reading mode; Cream, the default, no Theme click;
  toolbar expanded, Width clicked from Margin to Auto, toolbar collapsed; the local server started;
  the page at the top; the pointer parked).
- Three sections, each with its `Time`, `Shot *(filmed)*` and texts as drafted; the line
  "Pictures: ..." of each keeps its links, to the frames the take writes (section 3), each with its
  alt text:
  1. `## 1. A long page in Studio`: `frames/top.png`, `frames/wide-table.png`,
     `frames/diagrams.png`; `Text 1 *(on screen)*` = `A long page, with a **wide table**, diagrams and charts`.
  2. `## 2. Export, then open the file`: `frames/save-dialog.png`, `frames/browser-opened.png`,
     `frames/exported.png`; `Text 2 *(on screen)*` = `**Export** it to one HTML file`;
     `Badge palette *(on screen)*` = `Ctrl+Shift+P / ⇧⌘P`.
  3. `## 3. The same page in the browser`: `frames/03-zoomed.png`, `frames/04-mark-1.png`,
     `frames/05-mark-2.png`, `frames/06-mark-3.png`; `Zoom` = `page, hold to 17.0 s` (or the
     take's hold); `Mark 1 *(on screen)*` around the wide table, `Mark 2 *(on screen)*` around the
     flowchart, `Mark 3 *(on screen)*` around the bar chart, at the drafted times (11.8 to 13.0,
     14.0 to 15.2, 15.4 to 16.6 s) or the take's; `Text 3 *(on screen)*` =
     `The browser shows the **same page**, diagrams drawn`.
- "Expected result" list as drafted (Studio before the export, the file on disk, the Integrated
  Browser, the stage unchanged). No "Expected paste" block.
- "Review notes" as drafted, brought up to date with the take: the note "Length past 12 s" says
  the kit allows up to 30 s since `clip-the-advanced-renderings-tour`; the note "Scrolling" says
  which way each scroll used (`wheel` or `scrollTo`, from the take's notes); the note "Why Auto
  width and a narrower column" says what the trial measured (the wide table's width, the column's
  width, whether a month column was dropped); the note "The GIF budget" gives the ladder step the
  render used (`check.json`); add the measured times of the take and the key frame list with "Not
  checked by the author: motion, rhythm, the loop as watched." Keep the notes on what changes from
  the merged clip, why the export keeps the layout, the diagrams in the file, the sticky band
  (export-long-Q12), the palette option (export-long-Q9), the information message, `CLIP_SCRATCH`,
  the `⇧⌘P` keycap and the loop seam. Carry over from the merged clip the still-true notes on the
  Simple Browser, `files.simpleDialog.enable`, the port and the thin strip of the title bar at the
  top of the zoom, when the take confirms them.

### 3. The scenario: `scenario.mjs` reworked

Start from the merged `export-html/scenario.mjs` (keep `startServer`, `stopServer`, `readingMode`,
`centreOf`, `browserPage`, `browserArea`, `inWorkbench`, the save dialog, the toast dismissal and
the address bar handling, the user name guard on the workspace path and on the save dialog). Node
built-ins only; nothing runs at import (the kit's tests load it). The header comment says what is
filmed (a long page in Cream and Auto width scrolled, exported, opened in the Integrated Browser,
the same layout and drawings) and that every caption and time is in `clip.md`.

- `stage = { "stage/platform-report.md": "platform-report.md" }`; `open = ["platform-report.md"]`.
- `settings`: `"workbench.editorAssociations": { "platform-report.md": "markdown-okf-schema-studio.editor" }`,
  `"files.simpleDialog.enable": true`, `"markdownOkfSchemaStudio.preview.maxContentWidth": 720`
  (export-long-Q7).
- `checks = { editMode: "off", paste: false }` (unchanged).
- Remove `SHOWN`, `HIDDEN`, `panelShown` and the tab click (export-long-Q8). `STAGE_FILE` points at
  `stage/platform-report.md`; every `team-handbook` becomes `platform-report`; the heading waited for
  in the browser is "Platform report, 2026".
- Helpers:
  - `wideOf(frame or page)`: in `#sphinx-myst-preview-content`, the top-level wrapper (the ancestor
    whose parent is the content) of the table whose first header cell is "Service", and of the one
    whose first header cell is "Week"; returns for each its width, whether it carries
    `data-sphinx-preview-wide`, the width of the first paragraph of the content, and the wide
    table's right edge against the view's width (`innerWidth`) and its own `scrollWidth` against
    `clientWidth` (no sideways scroll of its own). Evaluated in the preview frame and, unchanged, in
    the browser page.
  - `drawn(frame)`: the two `.myst-mermaid-diagram` and the two `.myst-vega-diagram` blocks have
    `data-render-state="rendered"` and their `img` (`img.myst-mermaid-image`, `img.myst-vega-image`),
    one Vega block with `data-myst-chart-kind="vega-lite"` and one with `"vega"`; any other value
    throws with what was found (a finding against the feature, not a scenario fix).
  - `scrollBy(t, target, distance, seconds)`: wheel steps of about 60 px with the pointer over the
    page (`t.page.mouse.wheel` for Studio's webview, the browser page's `mouse.wheel` for the
    Integrated Browser: CDP input, no OS input), spread over `seconds`. When the page's
    `scrollY` has not moved after the first two steps, it uses a smooth `scrollTo` in that page
    instead (`behavior: "smooth"`), and records which way was used
    (`t.record("scrollStudio" | "scrollBrowser", "wheel" | "scrollTo")`). It waits for the scroll to
    settle (two equal reads of `scrollY` 100 ms apart) before any box is read.
- `setup(t)`, off camera: the user name guard (`CLIP_SCRATCH`) and the removal of a left
  `platform-report.html` as in the merged scenario; reading mode as merged (`t.record("readingMode",
  ...)`, throw when not `"off"`); **no Theme click**: read `data-sphinx-preview-theme-mode`, record
  it as `themeMode`, throw when it is not `"cream"` (the shipped default,
  `DEFAULT_PREVIEW_THEME_MODE` in `src/core/state/previewTheme.ts`); expand the toolbar
  (`[data-sphinx-preview-toolbar-collapse]` when `aria-expanded="false"`), click
  `[data-sphinx-preview-width-toggle]` until `document.documentElement`'s
  `data-sphinx-preview-width` is `"auto"` (at most three clicks, a fresh frame read between
  clicks), record `widthMode`, throw when not `"auto"`; collapse the toolbar again (the Export
  button stays in row 1); wait (at most 30 s) until `drawn(frame)` holds; read `wideOf` and throw
  unless the Service table's wrapper carries `data-sphinx-preview-wide`, is wider than the
  paragraph and has no sideways scroll of its own, and the Week table's wrapper does not carry it
  (record `studioWide`); scroll the page to the top; start the local server and fetch
  `platform-report.md` as merged; park the pointer over the page off the toolbar and every block
  (the blank right side of the content), `t.sleep(800)`.
- `run(t)`, timed with `until(seconds)` as merged, at the storyboard's times:
  1. Beat 1: at 0.6 s, scroll Studio down so the wide table sits in the middle of the view by 1.6 s;
     `t.keyFrame("top")` before it (at about 0.3 s), `t.keyFrame("wide-table")` at about 2.0 s; at
     2.4 s scroll on so the flowchart and the bar chart are in view by 3.2 s,
     `t.keyFrame("diagrams")` at about 3.5 s; at 3.8 s scroll on to the end of the page by 5.0 s.
     No mark and no zoom in beat 1 (export-long-Q11).
  2. Beat 2, as merged with the new times: at 5.0 s move to the Export button (`centreOf(frame,
     "[data-sphinx-preview-export]")`, read after the scroll settled), click at 6.0 s; the save
     dialog proposes `platform-report.html` (`t.keyFrame("save-dialog")`), Enter at 7.0 s; wait for
     the file; dismiss Studio's information message; pointer away from the toolbar; palette chord at
     7.6 s (`t.press("ControlOrMeta+Shift+P", "palette")`); "Open Integrated Browser" typed and
     chosen at 8.6 s (`t.keyFrame("browser-opened")`); the address
     `http://localhost:<port>/platform-report.html` typed and entered at 9.4 s; the page loaded with
     its heading by 9.8 s (`t.keyFrame("exported")`); `t.record("timing", ...)` as merged. The
     browser opens as a tab of the same editor group (the palette's default), full width.
  3. In the browser page, before the zoom: `drawn`-like check of the four `img` (`complete` and
     `naturalWidth > 0`), and `wideOf(view)`: the Service wrapper carries `data-sphinx-preview-wide`,
     its width equals Studio's (`studioWide`) within 2 px, is wider than the paragraph, and its right
     edge is inside the view; record `browserWide`; else throw with both measures.
  4. Beat 3: the zoom rect is the browser's content area (`browserArea`) narrowed so the wide table
     fits whole, about 1.25x, at most 2x (the kit caps it), kept inside the window; at 10.2 s
     `t.zoom("page", rect)`. At 10.8 s `scrollBy` the browser page to bring the wide table into the
     zoom rect by 11.6 s; at 11.8 s `t.mark("1", air(wide table))`, at 13.0 s `t.unmark("1")`; at
     13.2 s scroll to the flowchart and the bar chart by 13.8 s; at 14.0 s `t.mark("2", air(flowchart
     img))`, `t.unmark("2")` at 15.2 s; at 15.4 s `t.mark("3", air(vega-lite img))`, `t.unmark("3")`
     at 16.6 s. Each mark's rect is read with `inWorkbench` after the scroll settled and must lie
     inside the zoom rect, else throw "mark <n> is outside the zoom: <rects>". No mark during a
     scroll. `air` as merged (6 px).
  5. At 17.0 s `t.unzoom("page")` and the pointer back home; `until(18.0)` (or the take's
     `Length`). The loop seam is the kit's return to the start, as merged.
- `verify(t)`, keeping the merged structure (and `stopServer` in `finally`):
  - the workspace holds exactly `platform-report.md` and `platform-report.html`;
  - the file holds no `<script`, no `<link`, no `@import`, no `src` or `href` other than `#...` or
    `data:`;
  - its `<html>` carries `data-sphinx-preview-theme-mode="cream"` and
    `data-sphinx-preview-width="auto"`; the file holds `data-sphinx-preview-wide` (the wide table's
    wrapper);
  - it holds two `img` with class `myst-mermaid-image` and two with class `myst-vega-image`, each
    `src` starting with `data:image/svg+xml`;
  - the Integrated Browser page is still open, its four images loaded, `wideOf(view)` as in run
    step 3;
  - `platform-report.md` on disk equals `stage/platform-report.md` byte for byte;
  - returns `{ size, themeMode, widthMode, studioWide, browserWide, port }`.

### 4. Old outputs removed

The kit writes its outputs over the old ones but does not clear `frames/`. After the render, `git
rm` every file of the clip folder that this take did not write: at least
`frames/release.png` (the tab click is gone) and `stage/team-handbook.md`. `frames/01-selected.png`
and `frames/02-pasted.png` stay (the kit writes them for the palette press). The folder then holds
only this take's files.

### 5. Trial take, take and render

On Windows, on this machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`), the scratch folder outside the user's profile
(the save dialog shows the workspace path):

```bash
just dev
just package                                   # out/reports/package/markdown-okf-schema-studio.vsix
CLIP_SCRATCH=C:/okfclip just clip export-html doctor
CLIP_SCRATCH=C:/okfclip just clip export-html all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

(PowerShell: `$env:CLIP_SCRATCH = "C:/okfclip"` first.)

- **The trial first** (recipe section 1): (a) Studio's webview and, later, the Integrated Browser's
  page are in the screencast frames (the toast dismissed); (b) Cream and Auto at the start, the wide
  table breaks out of the 720 px column and fits the editor with no sideways scroll of its own (else
  drop month columns from the end, Dec first, in the stage, section 1, and retry); (c) the wheel
  reaches Studio's webview and the browser page, or the `scrollTo` way is used; (d) the browser's
  wide table equals Studio's within 2 px; (e) each mark lies inside the zoom rect; (f) the retimed
  rate is at least 15 fps.
- `Length` and every time in `clip.md` follow the take (playback rate inside 0.77 to 1.3), in the
  same commit as the render; the three captions stay end to end from 0 to `Length`, the three marks
  in turn inside the zoom hold.
- GIF over 3 MB at the ladder's last step: shorten the scroll in Studio (beat 1) in `clip.md` and
  `run`, and retake; never ship it heavier.
- Commit together (recipe rule): `clip.md`, `scenario.mjs`, `stage/platform-report.md`,
  `export-html.mp4`, `.webm`, `.gif` (Git LFS through `.gitattributes`), `poster.png`,
  `contact-sheet.png`, `first-last.png`, `frames/*.png`, `check.json`, and the removals of section 4.

### 6. Tests (no kit code change)

Each reads the shipped files from the repository, path from the test file's location, at the head
under test, never a copy. Run by `just clip-kit-test` inside `just check`:

- `docs/demo-video/clip-kit/lib/storyboard.test.mjs`, the case "the shipped export-html clip.md
  reads as the clip the owner reviews", rewritten: `parseClip` gives 1280x720, 15 fps, a `Length`
  above 12 and at most 30 (the committed value); the three captions (`**` stripped) "A long page,
  with a wide table, diagrams and charts", "Export it to one HTML file", "The browser shows the same
  page, diagrams drawn", end to end from 0 to `Length`; badges exactly `{ palette: "Ctrl+Shift+P /
  ⇧⌘P" }`; `expectedPaste` null; zoom `page` with the committed hold; marks `1`, `2`, `3` with the
  committed times, in turn, inside the hold; `validateStory` passes with
  `{ filmed: length, presses: [{ id: "palette", t: <committed palette time> }], zooms: [{ id: "page", t: <committed zoom time> }], marks: [1, 2, 3] }`
  on `win32` and on `darwin`.
- Same file, a new case "the stage of the export-html clip holds the page the clip claims": the
  shipped `stage/platform-report.md` has two `{grid}` blocks, exactly two `mermaid` fences (one
  `flowchart`, one `sequenceDiagram`), one `vega-lite` fence and one `vega` fence, a table whose
  header row has 16 cells (or the trial's count, at least 13) starting with "Service", and a table
  whose header row has 3 cells starting with "Week"; and the scenario's `stage` maps
  `stage/platform-report.md` to `platform-report.md` and its `settings` set
  `markdownOkfSchemaStudio.preview.maxContentWidth` to 720.
- `docs/demo-video/clip-kit/lib/check.test.mjs`: the shipped scenarios' checks case keeps
  `export-html` at `{ editMode: "off", paste: false }` (unchanged; it now loads the reworked
  scenario).
- `test/site/siteClips.test.ts` "the shipped toolbar page plays the export clip as video" is
  unchanged and keeps passing (the file names stay `export-html.*`).
- Run `just requirements-update` (no marker moves; it must leave the tree clean).

### 7. Docs

- `docs/user/toolbar.md`, "Export to HTML": the GIF's alt text becomes
  `![A long report page in Cream, with a wide table breaking out of the column, diagrams and charts, scrolled in Studio and exported with Export; opened in VS Code's Integrated Browser, the file shows the same page, the wide table and the drawings](../demo-video/clips/export-html/export-html.gif)`
  (export-long-Q8). The rest of the section is unchanged: its bullets stay true (the export still
  keeps a forced theme and the tabs still work without JavaScript; the clip just no longer shows
  them).
- No change to the recipe, the glossary, the writing skill, `docs/user/wide-tables.md`,
  `README.md`, `CHANGELOG.md` or `docs/releases-notes/` (no `feat` or `fix` commit).

### 8. Commits and the pull request

- Commits by area (Conventional Commits; no scope on `docs` or `test`):
  1. `docs: rework the export clip on a long report page` (the clip folder with its removals,
     `docs/user/toolbar.md`);
  2. `test: check the reworked export clip's storyboard and stage` (the kit test cases, and the
     files `just requirements-update` changes, if any).
- The PR is opened as a draft and stays one until the owner approves the storyboard and the clip
  (export-long-Q3); the agent does not mark it ready. Body per `.github/PULL_REQUEST_TEMPLATE.md`,
  `.agents/guidelines/pull-request.guidelines.md` and the recipe's clip PR rule: the GIF inline from
  `https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/export-html/export-html.gif`,
  the MP4 and WebM linked the same way at the same head; after each push of a new render the links
  move to the new head (`gh pr edit <n> --body-file <file>`); check that the GIF plays in the
  rendered PR page, else the recipe's `-assets` fallback.
- A section "Deviation from the feature clip process": the storyboard review moved from before the
  take into this PR (export-long-Q3); the take filmed from the Griller's draft; an *(on screen)* row
  the owner changes is a render (`just clip export-html render` then `check`), a *(filmed)* row a
  retake, a follow-up of this CR. It links `clip.md`.
- What changes from the merged clip (export-long-Q8): Cream, the default, instead of a forced Dark,
  so the clip no longer shows that a forced theme is kept; the tab set and its click are gone, so it
  no longer shows tabs working without JavaScript (both stay true and documented in
  `docs/user/toolbar.md`); 12 s to 18 s, two captions to three, two marks to three; the stage
  replaced.
- What the clip proves (a real export in a real VS Code window keeps Cream, Auto width, the
  breakout at the same pixel width and the four drawings, with no script: the take's `run` checks
  and `verify`) and what the owner judges (motion, rhythm, the scroll speed, the loop as watched,
  the texts and their accent).
- "Autonomous decisions": the differences from the draft (section 2), the scroll ways used, any
  table change and why (section 1), the ladder step, the removed old frames, `CLIP_SCRATCH`.
- The PR sits above `clip-the-advanced-renderings-tour` in the batch-09 stack while that CR is not
  merged (its kit change makes the 18 s clip valid).

## Out of scope

- Any change to `src/`, to an SwRS text, to the writing skill, to the clip kit's code or to the
  recipe (the 30 s bound is `clip-the-advanced-renderings-tour`'s).
- A forced theme, the Theme button, tabs (export-long-Q8); Margin or Full width; the default 960 px
  column (export-long-Q7); hiding the sticky heading band (export-long-Q12).
- An outside browser, a file URL in the address bar, opening the browser off camera (an option for
  the owner, export-long-Q9).
- Editing CR-498's folder or its `wide-table-auto-width` clip; renaming the clip folder or its
  outputs.
- A macOS or Linux take; the clip in release notes or the announcement (a release CR does it); a
  retake after the owner's review (a follow-up, export-long-Q3); marking the PR ready.

## CI

No CI job changes. The changed and new test cases run in `just check` through `just clip-kit-test`,
inside the existing `ci-static` job (Linux and Windows, `.github/workflows/ci.yml`); the site test
runs where `test/site/` tests run today.

- Environment: the CI machine set up by `just dev-ci` from the lock files, Node.js 24 from `.nvmrc`.
  Absent there and present locally: `ffmpeg`, the kit's scratch folder, the VS Code download,
  Remotion, a display. The tests need none of them: they read the shipped `clip.md` and
  `stage/platform-report.md`, load the shipped `scenario.mjs` (never run), and the site test reads
  the shipped `docs/user/toolbar.md` and the committed clip files (Git LFS checked out as CI does
  for the other clips).
- Before the push: `just clip-kit-test`, `just check` and `just ci-static` on Windows.
- Only the first CI run proves the Linux leg (loading the reworked scenario from a repository path,
  the stage read with LF endings).

## Host and default matrix

What the clip films depends on shipped defaults and one configured value: the theme mode
(`cream` by default, `src/core/state/previewTheme.ts`), the width mode (`margin` by default,
`src/core/state/previewViewPreferences.ts`, switched to Auto by the Width button off camera) and
`markdownOkfSchemaStudio.preview.maxContentWidth` (default 960, filmed at 720).

| Host | VS Code | Settings | Expected | Proof |
| --- | --- | --- | --- | --- |
| Windows 11, CDP input | pinned `DEFAULT_CODE_VERSION` (1.147.0 unless moved) | Cream default, Width clicked to Auto, `maxContentWidth` 720, `files.simpleDialog.enable` on | the wide table breaks out in Studio and in the browser at the same width (2 px), four drawings embedded and loaded, no script, file unchanged | the take's `setup`/`run` checks and `verify`, `check.json` ("scenario verify passed") |
| Windows 11 | same | Width left at Margin (default) | the wide table scrolls inside its box, no breakout | not filmed (export-long-Q7; the CR-498 clip's story) |
| Windows 11 | same | `maxContentWidth` 960 (default) | breakout less visible next to a 1280 px window | not filmed (export-long-Q7) |
| macOS, Linux | same | as the first row | same | not proved (no take there) |

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows; the storyboard and stage cases read the
   shipped `clip.md`, `stage/platform-report.md` and `scenario.mjs` at the head under test; the site
   test reads the shipped `docs/user/toolbar.md`. On a base without the tour's kit change the
   storyboard case fails on the length (expected: the reason for `depends.json`).
2. The trial's six points (section 5), with what was seen (frame names) and the scroll ways used.
3. `CLIP_SCRATCH=C:/okfclip just clip export-html all --vsix ...` passes; `check.json` shows
   `passed: true`, the duration line within 5 to 30 s ok, MP4 and WebM 1280x720 at 15 fps, MP4
   duration equal to `Length` within one frame, GIF within 3 MB with its ladder step, loop seam
   SSIM in [0.98, 1.0), "Studio in reading mode at the start", no paste line, `verifyPassed: true`,
   playback rate inside 0.77 to 1.3, platform `win32`, extension source `vsix`.
4. The take's notes hold `themeMode: "cream"`, `widthMode: "auto"`, `studioWide` and `browserWide`
   (the widths equal within 2 px, wider than the paragraph), the four images loaded, and `verify`'s
   file checks (root attributes, `data-sphinx-preview-wide`, four `data:image/svg+xml` images, no
   script or link, stage unchanged).
5. The agent looks at the contact sheet and every key frame (`top`, `wide-table`, `diagrams`,
   `save-dialog`, `browser-opened`, `exported`, `03-zoomed`, `04-mark-1` to `06-mark-3`): Cream,
   reading mode, the wide table broken out of the column in Studio and in the browser, the small
   table inside the column, the diagrams and charts drawn, each mark on its block inside the zoom,
   the right caption with each beat, no tooltip at frame 0 and at the seam, no personal name or
   path, no dirty tab, no notification over the browser. What was not checked (motion, rhythm, the
   loop as watched) is said.
6. `git ls-files docs/demo-video/clips/export-html` lists no file the take did not write (no
   `release.png`, no `team-handbook.md`); `git grep -n team-handbook` finds nothing.
7. `just requirements-update` leaves the tree clean; `just preflight` passes (on Windows, its static
   stage).
8. The draft PR plays the GIF and links the MP4 and WebM at the head sha (or the `-assets`
   fallback), and holds the "Deviation from the feature clip process" section.

## Open questions

None: `02-answers.md` (export-long-Q1 to Q13), `depends.json` and the code on `origin/main` settle
every point this specification needs. (The one tension, Q4's "no `depends.json`" against Q5 and the
`depends.json` written after it, is read in favour of Q5: the 18 s length needs the tour's kit
change.)
