# Clip: the advanced renderings tour, and clips up to 30 s

Short name: `renderings-tour`. No tracker issue (verbal request of the owner, relayed by the Chief
of Staff, 2026-11-25).

## Goal

A feature clip that answers "what can I put in my document?" in a few seconds: one design note in
Studio's reading mode, in Cream, shows every advanced rendering Studio draws in its preview, a
Mermaid flowchart, a PlantUML sequence, a Vega-Lite line chart, a full Vega bar chart, a display
equation typeset by KaTeX and an inline SVG drawing in the page colours. Each gets an orange mark
and its own caption naming it. Everything is built in and works offline: PlantUML draws with no
Java, the charts with no server.

The clip is made with the merged clip kit (`docs/demo-video/clip-kit/`) and recipe
(`docs/demo-video/guidelines/feature-clip-process.guidelines.md`): 1280x720 at 15 fps, no card, the
logo top right, one zoom, marks in turn, a loop, MP4, WebM and GIF. It differs from the recipe's
usual clip in two points: six captions in turn (one per renderer) and a length of 16 s. The second
needs a kit change, which this CR owns for the whole round: **the maximum clip length goes from
12 s to 30 s**.

The clip shows existing renderers (`src/page/modules/mermaidPreview.ts`,
`src/page/modules/plantumlPreview.ts` and `plantumlDiagram.ts`, `src/page/modules/vegaPreview.ts`,
`src/core/render/chartData.ts`, `src/core/render/mathRenderer.ts`, `src/core/render/svgPictures.ts`);
no behaviour of the extension changes.

## Base and stack

- Base: `origin/main` (fetch first: the local `main` is behind it). The kit, the recipe and the
  eight merged clips (`raw-copy-balance-edges`, `drag-list-item`, `comment-thread`,
  `export-html`, `diff-side-by-side`, `paste-spreadsheet-cells`, `slash-menu-grid`,
  `theme-switch`) are merged there. No `depends.json` (renderings-tour-Q4).
- This CR sits at the **bottom of the batch-09 stack** (renderings-tour-Q12): every other clip of the
  round longer than 12 s lists it in its `depends.json`. So the kit change is its **first commit**,
  self-contained (code, tests, recipe, glossary), so the CRs above can build on it before this
  clip's take is done.

## Decisions carried from `02-answers.md`

| Answer | Decision | Where in this spec |
| --- | --- | --- |
| renderings-tour-Q1 | The owner's wish: a tour of the advanced renderings, Mermaid, PlantUML, Vega, Vega-Lite and all the others | Goal, section 3 |
| renderings-tour-Q2 | The captions, stage and timing of the Griller's storyboard draft are the clip's shape | sections 2, 3 |
| renderings-tour-Q3 | The batch films a trial take from the draft, puts its pictures in the storyboard, renders, opens the PR with the clip watchable (GIF inline, MP4 and WebM linked at the PR's head); the PR stays a draft until the owner approves; the deviation from the recipe's order is reported here and in the PR body; a retake after review is a follow-up of this CR | sections 3, 5, 8, "Deviations" |
| renderings-tour-Q4 | Built on `origin/main`, alone: no `depends.json`, no dependency on the other clips of the round | "Base and stack" |
| renderings-tour-Q5 | Six renderers: Mermaid, PlantUML, Vega-Lite, Vega, math (KaTeX), inline SVG; Graphviz left out (Studio has no Graphviz renderer) | sections 2, 3 |
| renderings-tour-Q6 | PlantUML filmed with the built-in engine, the default; the kit needs no Java and no JAR | sections 3, 4, "Host and default matrix" |
| renderings-tour-Q7 | The clip runs 16 s, with a kit change in the same PR; its 20 s bound is replaced by Q12's 30 s; its 12 s fallback is settled away by Q12 | sections 1, 3 |
| renderings-tour-Q8 | Six captions in turn, one per renderer, each naming it in bold | section 3 |
| renderings-tour-Q9 | One design note (`search-design.md`) in two views of three renderings, one zoom held over the whole tour, the page scrolled once under it | sections 2, 3, 4 |
| renderings-tour-Q10 | Order Mermaid, PlantUML, Vega-Lite, then Vega, math, SVG; Cream; reading mode | sections 3, 4 |
| renderings-tour-Q11 | The `{uml} file.puml` and `{mermaid}` directive forms and chart data from a CSV file are not filmed | "Out of scope", section 3 (review notes) |
| renderings-tour-Q12 | This CR owns the kit's length change for the whole round: 12 s to 30 s, in `storyboard.mjs`, `check.mjs`, their tests and the recipe; bottom of the batch-09 stack; this clip still runs 16 s, no 12 s cut | section 1, "Base and stack" |

## Deviations

- **From the recipe's order** ("The storyboard first"): the maintainer's storyboard review moves
  from before the take to the pull request (renderings-tour-Q3). The committed `clip.md` keeps
  `status: draft for the owner's review`; the PR stays a draft until the owner approves. The PR
  body says so in one sentence under "Autonomous decisions".
- **From the recipe's usual shape**: six captions instead of two. The kit already allows one caption
  per section and any number of sections; no kit change for it.
- **Length**: 16 s, allowed by the kit change of section 1.

## What changes

All paths are relative to the repository root.

### 1. The kit: a clip may run up to 30 s (first commit)

- `docs/demo-video/clip-kit/lib/storyboard.mjs`: `MAX_LENGTH` goes from `12` to `30`. The refusal
  message stays built from the constants (`Length <n> s is outside 5 to 30 s`).
- `docs/demo-video/clip-kit/lib/check.mjs`: the MP4 duration line stops hard-coding 5 and 12. It
  imports `MIN_LENGTH` and `MAX_LENGTH` from `./storyboard.mjs` (one shared bound, as the draft's
  review note asks) and a new exported pure function gives the line:
  `durationLine(seconds)` returns `{ name: "mp4 duration within 5 to 30 s", ok, value: "<s.sss> s" }`,
  the name built from the constants, `ok` when `MIN_LENGTH <= seconds <= MAX_LENGTH`. `checkClip`
  calls `want(...)` with it, so `check.json` keeps the same line shape, with the new name.
- Tests, run by `just clip-kit-test` inside `just check`:
  - `lib/storyboard.test.mjs`: two refusal cases on the prepared text (a `Length` of `4.9 s` and of
    `30.1 s`, each refused with `/^clip\.md: Length .* s is outside 5 to 30 s/u`; there is no length
    refusal case today), and one prepared text whose `Length` and last caption end are `30.0 s`
    that parses (the bound is inclusive). Prepared texts are right here: they are the parser's
    refusals and bounds, which no shipped file holds; the shipped `clip.md` of section 3 is checked
    by its own case.
  - `lib/check.test.mjs`: `durationLine` is ok at 5, 16 and 30, not ok at 4.9 and 30.1, and its
    name reads `mp4 duration within 5 to 30 s`.
- `docs/demo-video/guidelines/feature-clip-process.guidelines.md`: every "5 to 12" becomes "5 to 30"
  (line 10 "plays 5 to 12 seconds", line 137 "`Length` (seconds, 5 to 12)", line 167 "a `Length`
  missing or outside 5 to 12 s", line 256 "MP4 duration 5 to 12 s"), and one sentence after the
  opening paragraph's first sentence: most clips run under 12 s; a clip may run up to 30 s when its
  story needs it, and its storyboard says why in its review notes.
- `.agents/glossary/common.md`, "Feature clip": "a video of 5 to 12 seconds" becomes "5 to 30
  seconds" (the glossary must match the recipe; not named by Q12, a direct consequence, said in the
  PR's "Autonomous decisions").
- The shipped `check.json` of the merged clips keep their old line name: they are evidence of their
  take, not regenerated.
- Commit: `build: let a feature clip run up to 30 seconds` (the kit's earlier commits use `build`;
  no scope on `build`).

### 2. The stage: `docs/demo-video/clips/advanced-renderings-tour/stage/search-design.md`

Copied byte for byte from `work/storyboard/stage/search-design.md` of this CR's folder (in the
planning surface,
`C:/Users/gaeta/Projets/gsemet-foss-planning-surface/projects/markdown-okf-schema-studio/changes/2-backlog/P2/clip-the-advanced-renderings-tour/`,
or wherever the batch moved the folder): the heading "Search service: design note", one sentence, a
`mermaid` `flowchart LR` (Query, Parse, Index, Results), a `plantuml` sequence (Reader, Search,
Index, three messages), a `vega-lite` line chart (five weeks of p95 latency, height 90), a
`## Capacity` heading, a `vega` bar chart (three regions, height 100), a `$$` display equation and an
`svg` fence (Box, Service, Index, colours as `var(--...)`). It links no file and reads no data file.

If the trial (section 5) finds that a view does not hold its three renderings inside the zoom rect,
the charts' `height` is lowered first (draft review note "Fit"), in the stage and nowhere else; the
committed stage is the filmed one.

### 3. The live storyboard: `docs/demo-video/clips/advanced-renderings-tour/clip.md`

The draft `work/storyboard/clip.md`, adapted only as follows; every *(on screen)* text stays as
drafted, and the times follow the take:

- Front matter: `title: Feature clip advanced-renderings-tour`,
  `status: draft for the owner's review` (renderings-tour-Q3), `date:` the day of the commit.
- Opening paragraph: as the merged clips word it ("This is the live storyboard. The clip is built
  from this file: edit any row marked *(on screen)*, save, and run
  `just clip advanced-renderings-tour render`, then `check`. Rows marked *(filmed)* describe the
  footage of the take: changing them means a new take. `**bold**` in a text takes the orange
  accent."), plus one sentence: the owner reviews this file and the clip in the pull request.
  Keep the paragraph on the shot (one note, one zoom, six marks in turn, one scroll, back to the
  top). Drop "draft for review", "Once approved, this file becomes ...", "The times below are the
  Griller's proposal ...", and the sentence "The clip runs 16 s, past the kit's 12 s limit ..."
  (replaced by one review note, below).
- `## Clip` table as drafted: `Length` `16.0 s` (or the take's value, within the kit's 5 to 30 s),
  `Size *(on screen)*` `1280x720 16:9`, `Frame rate *(on screen)*` `15 fps`, `Outputs`, `Cards`
  `none`, `Logo` `top right`, `Setting filmed` as drafted (every setting at its default, PlantUML on
  the built-in engine, `plantuml.useJar` off), `Filmed on`: "Windows, VS Code <version>, extension
  <version> VSIX built from the branch" (the versions `check.json` writes), `Stage` as drafted.
- "Off camera (`setup`)" as drafted.
- Six sections `## 1. Mermaid` to `## 6. SVG, then back to the top`, each with its `Time`,
  `Shot *(filmed)*`, `Mark <n> *(on screen)*` and `Text <n> *(on screen)*` as drafted; section 1
  holds the only `Zoom` row, `tour, hold to 15.0 s` (or the take's hold). The six texts, exactly:
  1. `**Mermaid** diagrams, drawn in the page`
  2. `**PlantUML** built in, with no Java`
  3. `**Vega-Lite** charts from a few lines`
  4. `Full **Vega** specs for custom charts`
  5. `**Math** typeset by KaTeX`
  6. `**SVG** drawn in the page colours`
- Pictures: each section shows its mark's key frame, `frames/04-mark-1.png` to
  `frames/09-mark-6.png` (the kit's names, `keyFrameTimes` in `lib/encode.mjs`), each with an alt
  text saying what it shows; section 1 also shows `frames/03-zoomed.png`. No `images/` folder.
- "Expected result" list as drafted (all six drawn at the start and before each mark, no
  `.myst-plantuml-error`, each mark inside the zoom rect, the file unchanged on disk). No "Expected
  paste" block.
- "Review notes" as drafted, with these changes: the note "Kit change needed: the length" becomes
  "The length": the clip runs 16 s, past the usual 12 s, which the kit allows up to 30 s since this
  CR (the six beats need about 2 s each, a scroll and the return to the top); drop its 12 s
  fallback (settled by Q12). The note on the scroll says which way the take used (the CDP wheel or
  the smooth `scrollTo`). The "Fit" note says what the trial found. The "GIF budget" note gives the
  ladder step the render used (`check.json`). Keep the notes on PlantUML with no Java, the list of
  renderers (Graphviz absent, the directive forms and CSV data not filmed), six captions, the loop
  seam and Cream only.

### 4. The scenario: `docs/demo-video/clips/advanced-renderings-tour/scenario.mjs`

In the style of `clips/theme-switch/scenario.mjs`; the header comment says what is filmed and that
every text and time is in `clip.md`. Node built-ins only, nothing done at import (the kit's tests
load it).

- `stage = { "stage/search-design.md": "search-design.md" }`; `open = ["search-design.md"]`.
- `settings = { "workbench.editorAssociations": { "search-design.md": "markdown-okf-schema-studio.editor" } }`:
  no Studio setting, so PlantUML runs on its default built-in engine (renderings-tour-Q6).
- `checks = { editMode: "off", paste: false }`.
- No copy of the stage text: `verify` compares the workspace file with the clip's own
  `stage/search-design.md`, read from `new URL("stage/search-design.md", import.meta.url)` (as
  `export-html` does).
- The drawings, by selector, in order (marks 1 to 6):
  1. Mermaid: `.myst-mermaid-diagram img.myst-mermaid-image`;
  2. PlantUML: `.myst-plantuml-diagram img.myst-plantuml-image`;
  3. Vega-Lite: `.myst-vega-diagram[data-myst-chart-kind="vega-lite"] img.myst-vega-image`;
  4. Vega: `.myst-vega-diagram[data-myst-chart-kind="vega"] img.myst-vega-image`;
  5. math: `.math-display .katex-display` (else `.math-display .katex`);
  6. SVG: `figure.myst-svg-figure > svg`.
- A helper `drawn(frame)` reads in the preview frame: `data-render-state` of the Mermaid, PlantUML and
  both Vega blocks (all `"rendered"`, each with its `img`), a `.katex` inside `.math-display`, an
  `svg` inside `figure.myst-svg-figure`, and the count of `.myst-plantuml-error` (0). Any other value
  throws with what was found (a finding against the feature, never retried by a setting).
- `setup(t)`, off camera, as `theme-switch` does it: `t.frameOf()`, reading mode (click
  `[data-sphinx-preview-edit-toggle]` when `data-sphinx-preview-edit-mode` is `"on"`;
  `t.record("readingMode", ...)`; throw when not `"off"`); the toolbar left as it is (collapsed in a
  fresh workspace: the draft does not expand it); the page in Cream (click
  `[data-sphinx-preview-theme-toggle]` until `data-sphinx-preview-theme-mode` is `"cream"`, at most
  four clicks, for a workspace that stored another mode); scrolled to the top; wait (at most 30 s)
  until `drawn(frame)` holds; park the pointer in the blank right part of the page, off the toolbar
  and every block (as `theme-switch` computes it), and sleep 800 ms.
- `run(t)`, timed with `until(seconds)` as the merged scenarios do, at the storyboard's times:
  1. Read the six drawing boxes of the first view (Mermaid, PlantUML, Vega-Lite) and the `Capacity`
     heading's position. The zoom rect: the content column's box (`#sphinx-myst-preview-content`)
     narrowed to the union of the three first drawings, padded by 24 px, at most 2x of the window
     (the rect may be widened to keep 16:9 and the 2x limit). At 0.4 s, `t.zoom("tour", rect)`.
  2. Marks 1 to 3 at their drafted times, each `t.mark(id, air(box))` (8 px of air, as
     `theme-switch`), `t.unmark` at its end; `drawn(frame)` is checked before each mark. Each mark's
     rect must lie inside the zoom rect, else throw "mark <n> is outside the zoom: <rects>".
  3. At 7.4 s, the scroll: the page goes down by the distance that brings the `Capacity` heading to
     the top of the zoom rect, smoothly over about 0.8 s, by `t.page.mouse.wheel` steps with the
     pointer over the preview (a CDP wheel, not an OS input). When the preview's scroll position has
     not moved after the first steps, the scenario uses a smooth `scrollTo` in the preview frame
     instead (the same picture), and records which way was used (`t.record("scroll", "wheel" | "scrollTo")`).
     Wait for the scroll to settle (two equal reads 100 ms apart) before reading any box.
  4. Read the boxes of the Vega chart, the equation and the SVG after the scroll settled; marks 4 to 6
     at their drafted times, inside the zoom rect as in step 2. No mark is shown during a scroll.
  5. At 14.4 s, scroll back to the top the same way over 0.6 s; at 15.0 s, `t.unzoom("tour")`; the
     page is at the top, unzoomed and still for the last frames, so the last frame matches frame 0;
     `until(16.0)` (or the take's `Length`).
  6. `t.record("marks", [...])` with the six rects and `t.record("zoom", rect)`.
- `verify(t)`: `search-design.md` on disk equals the clip's `stage/search-design.md` byte for byte
  (`t.workspaceFile`); the workspace holds no new file; `drawn(frame)` holds at the end (no
  `.myst-plantuml-error`); returns `{ scroll, unchanged: true }`. Each failure throws with what was
  found.

### 5. Take and render

On Windows, on this machine, screen unlocked, no other change running app-window tests
(`.agents/guidelines/local-worktree.guidelines.md`), the scratch folder outside the user's profile
(no frame shows the user name):

```bash
just dev
just package                                   # out/reports/package/markdown-okf-schema-studio.vsix
CLIP_SCRATCH=C:/okfclip just clip advanced-renderings-tour doctor
CLIP_SCRATCH=C:/okfclip just clip advanced-renderings-tour all --vsix out/reports/package/markdown-okf-schema-studio.vsix
```

(PowerShell: `$env:CLIP_SCRATCH = "C:/okfclip"` first.) No Java and no PlantUML JAR are installed or
configured for the take (renderings-tour-Q6).

- **A trial first** (recipe section 1): (a) the six drawings are in the screencast frames; (b) the
  first view's three drawings fit inside the zoom rect, and after the scroll the second view's three
  do (else lower the charts' `height` in the stage, section 2, and retry); (c) the scroll reaches the
  webview (the wheel) or the `scrollTo` way is used; (d) the retimed rate is at least 15 fps.
- `Length` and every time in `clip.md` follow the take (playback rate inside 0.77 to 1.3), in the
  same commit as the render; the captions stay end to end from 0 to `Length`, the six marks in turn
  inside the zoom hold.
- GIF over 3 MB at the ladder's last step: shorten the clip in `clip.md` and retake, never ship it
  heavier (draft review note "GIF budget").
- Commit together (recipe rule): `clip.md`, `scenario.mjs`, `stage/search-design.md`,
  `advanced-renderings-tour.mp4`, `.webm`, `.gif` (Git LFS through `.gitattributes`), `poster.png`,
  `contact-sheet.png`, `first-last.png`, `frames/*.png`, `check.json`.

### 6. Tests of the clip (no kit code change beyond section 1)

In `docs/demo-video/clip-kit/lib/`, run by `just clip-kit-test` inside `just check`:

- `storyboard.test.mjs` gains "the shipped advanced-renderings-tour clip.md reads as the clip the
  owner reviews": it reads the shipped `docs/demo-video/clips/advanced-renderings-tour/clip.md`
  from the repository (path from the test file's location, at the head under test, never a copy)
  with `parseClip` and asserts: size 1280x720, 15 fps, `Length` above 12 and at most 30 (the
  committed value, the first shipped clip past the old bound), the six caption texts of section 3
  (bold stripped) end to end from 0 to `Length`, no badge, zoom `tour`, marks `1` to `6` in turn
  inside the hold, `expectedPaste` null; `validateStory` passes with a take
  `{ filmed: length, presses: [], zooms: [{ id: "tour", t: 0.4 }], marks: [1..6] }` on `win32` and
  on `darwin`.
- `check.test.mjs`: the test of the shipped scenarios' checks gains `advanced-renderings-tour`
  (its title names it): `resolveChecks(checks)` gives `{ editMode: "off", paste: false }`.

### 7. Docs

- `docs/user/editing.md`, the "**MyST rendering:**" bullet (it lists math, Mermaid and PlantUML):
  after its text, indented as the drag clip's image is in its bullet, the image
  `![One design note in reading mode, zoomed: a Mermaid flowchart, a PlantUML sequence, a Vega-Lite line chart, then after a scroll a Vega bar chart, a KaTeX equation and an inline SVG drawing, each outlined in turn and named by a caption](../demo-video/clips/advanced-renderings-tour/advanced-renderings-tour.gif)`
  (the recipe: the GIF goes to the feature's docs page; the tour spans several pages' features, so it
  goes to the page that lists them all).
- `test/site/siteClips.test.ts`: "the shipped editing page plays the renderings tour clip as video",
  modelled on the list drag one: reads the shipped `docs/user/editing.md`, `renderMyst`,
  `clipVideos`, asserts the
  `<video src="../demo-video/clips/advanced-renderings-tour/advanced-renderings-tour.webm"` and that
  the `.webm`, `.gif` and `poster.png` exist; marker `// @tests_req SwRS-MDOKFSTUDIO-CORE-095` (an
  added test of an existing SwRS, no SwRS text change); then `just requirements-update`.
- No change to `README.md`, `CHANGELOG.md` or `docs/releases-notes/` (no `feat` or `fix` commit).
  The writing skill does not change (no rendered syntax changes).

### 8. Commits and the pull request

- Commits, in this order (Conventional Commits; no scope on `build`, `docs` or `test`):
  1. `build: let a feature clip run up to 30 seconds` (section 1: kit code, kit tests, recipe,
     glossary);
  2. `docs: add the advanced renderings tour feature clip` (the clip folder, `docs/user/editing.md`);
  3. `test: check the renderings tour storyboard and play it on the editing page` (the kit test
     cases of section 6, `siteClips.test.ts`, the files `just requirements-update` changes).
- The PR is opened as a **draft** and stays one until the owner approves the storyboard and the clip
  (renderings-tour-Q3). Its body follows `.github/PULL_REQUEST_TEMPLATE.md` and
  `.agents/guidelines/pull-request.guidelines.md`, and the clip PR rule of the merged clips: the GIF
  inline from
  `https://github.com/gsemet/markdown-okf-schema-studio/raw/<head sha>/docs/demo-video/clips/advanced-renderings-tour/advanced-renderings-tour.gif`,
  the MP4 and WebM linked the same way at the same head; after each push of a new render the links
  move to the new head (`gh pr edit <n> --body-file <file>`); check that the GIF plays in the
  rendered PR page, else the `-assets` fallback.
- The body says: the kit change (12 s to 30 s, for the whole round, the other clips of batch-09
  stack on it); what the clip proves (the six renderers drawn in a real VS Code window, PlantUML on
  the built-in engine with no Java, the file unchanged: the take's `run` checks and `verify`); what
  the owner judges (motion, rhythm, six captions in 16 s, the scroll under the zoom, the loop as
  watched); a link to `clip.md` for the storyboard review; a retake after review is a follow-up of
  this CR.
- "Autonomous decisions": the recipe order moved to the PR (renderings-tour-Q3); the glossary line
  changed with the recipe; `durationLine` exported to test the bound; the docs placement on the
  editing page; the scroll way used; any stage `height` change from the trial.

## Out of scope

- Any change to `src/`, to an SwRS text, or to the kit beyond the length bound (section 1).
- Graphviz (not a Studio renderer); the `{uml} file.puml`, `{plantuml}` and `{mermaid}` directive
  forms; chart data from a CSV file (renderings-tour-Q11); the PlantUML JAR pipeline
  (`plantuml.useJar`); a theme other than Cream (the `theme-switch` clip's story); edit mode.
- Regenerating the merged clips' `check.json`; a macOS or Linux take; the clip in release notes or the
  announcement (a release CR does it); a retake after the owner's review (a follow-up, Q3).

## CI

No CI job changes. The new and changed tests run in `just check` through `just clip-kit-test`, in the
existing `ci-static` job (Linux and Windows, `.github/workflows/ci.yml`); the site test runs where
`test/site/` tests run today.

- Environment: the CI machine set up by `just dev-ci` from the lock files, Node.js 24 from `.nvmrc`.
  Absent there and present locally: `ffmpeg`, the kit's scratch folder, the VS Code download,
  Remotion, a display. The tests need none of them: `durationLine` is pure, the storyboard case reads
  the shipped `clip.md`, the checks case loads the shipped `scenario.mjs` (never run), the site test
  reads the shipped `docs/user/editing.md` and the committed clip files (Git LFS checked out as CI
  does for the other clips).
- Before the push: `just clip-kit-test`, `just check` and `just ci-static` on Windows.
- Only the first CI run proves the Linux leg (loading the new scenario from a repository path).

## Host and default matrix

What the clip films depends on one shipped default: `markdownOkfSchemaStudio.plantuml.useJar` off,
so PlantUML draws with the bundled JavaScript engine (`resolvePlantUmlEngine`,
`src/core/configuration/plantUmlConfiguration.ts`). The kit's profile does not set it.

| Host | VS Code | Settings | Expected | Proof |
| --- | --- | --- | --- | --- |
| Windows 11, CDP input | pinned `DEFAULT_CODE_VERSION` (1.147.0 unless moved) | every setting at its default (`plantuml.useJar` off), no Java or JAR configured | six drawings rendered, no `.myst-plantuml-error`, file unchanged | the take's `run` checks and `verify`, `check.json` ("scenario verify passed") |
| macOS | same | same | same | not proved (no macOS take) |
| Linux | same | same | same | not proved |
| any | same | `plantuml.useJar` on | the JAR pipeline draws the sequence | not filmed (out of scope) |

## Evidence

1. `just clip-kit-test` and `just check` pass on Windows: the length refusals at 4.9 s and 30.1 s,
   30.0 s accepted, `durationLine` at its bounds; the storyboard case reads the shipped `clip.md`,
   the checks case loads the shipped `scenario.mjs`, the site test reads the shipped
   `docs/user/editing.md`, all at the head under test.
2. `git grep -n "5 to 12"` finds nothing left in the kit, the recipe or the glossary (the merged
   clips' `check.json` excepted).
3. The trial's four points, with what was seen (frame names) and the scroll way used.
4. `CLIP_SCRATCH=C:/okfclip just clip advanced-renderings-tour all --vsix ...` passes; `check.json`
   shows `passed: true`, the line "mp4 duration within 5 to 30 s" ok, MP4 and WebM 1280x720 at
   15 fps, MP4 duration equal to `Length` within one frame, GIF within 3 MB with its ladder step,
   loop seam SSIM in [0.98, 1.0), "Studio in reading mode at the start", no paste line,
   `verifyPassed: true`, playback rate inside 0.77 to 1.3, platform `win32`, extension source `vsix`.
5. The agent looks at the contact sheet and every key frame (`03-zoomed`, `04-mark-1` to
   `09-mark-6`): Studio in Cream, reading mode, each mark on its drawing in turn and inside the zoom,
   the right caption with each mark, the PlantUML sequence drawn (no error text), no tooltip, no
   personal name or path, no dirty tab. What was not checked (motion, rhythm, the loop as watched)
   is said.
6. `just requirements-update` leaves the tree clean after its commit; `just preflight` passes (on
   Windows, its static stage).
7. The draft PR plays the GIF and links the MP4 and WebM at the head sha (or the `-assets`
   fallback), and says the storyboard review is the owner's, in that PR.

## Open questions

None: `02-answers.md` (renderings-tour-Q1 to Q12) and the code settle every point this
specification needs.
