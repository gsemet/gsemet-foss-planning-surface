# Vega charts: readable legends, hover detail, no Chart source

## Goal

Vega-Lite and Vega charts in the preview get readable text by default: the legend, axis and title
sizes follow the page's body text size, so they also follow the Markdown font-size setting and the
preview zoom. Chart marks show a themed hover detail box of Studio's own. The preview no longer
shows the collapsed **Chart source** section under a chart; the HTML export keeps it.

This spec is self-contained: the decisions it carries come from `02-answers.md` (Q1 to Q10) and the
values from `work/exploration/README.md`. Both are restated here where they are needed.

The project rules apply as they stand. Read `.agents/constitution.md` and
`requirements/guidelines/requirements.guidelines.md` with `requirements/guidelines/project.guidelines.md`
("During a change") before the change. This spec does not restate them.

## Today

- `chartConfig(theme)` in `src/page/modules/vegaChart.ts` sets colours and fonts only. Every size is
  Vega's default: axis and legend labels 10 px, their titles 11 px, chart title 13 px, subtitle 11 px,
  legend symbolSize 100, rowPadding 2, axis titlePadding 4. The page body text is 14 px in all themes.
- `drawChart` runs a headless view (`renderer: "none"`), calls `view.toSVG()`, and `vegaPreview.ts`
  shows the result as `<img class="myst-vega-image">` with an SVG data URL. An image gets no pointer
  events, so no tooltip can show, whatever the spec says.
- `normalizeDiagram` (`src/core/render/mystNormalize.ts`) builds the figure with
  `div.myst-vega-diagram` (aria-label "Chart diagram") and a collapsed `details.myst-vega-source`
  (summary "Chart source", the spec in pre/code). The preview and the HTML export both show it.
- The page CSP has no `unsafe-eval`, no `unsafe-inline` and `connect-src 'none'`. Expressions run
  through vega-interpreter (`ast: true`, DIAG-124). CSSOM (`el.style.setProperty`) is allowed; a
  `style` attribute is not.

## What changes

### 1. Default chart config: page-relative sizes (Q3, Q7, Q9)

- `ChartTheme` gains `fontSize: number`, the body font size in px.
- `chartThemeFrom(read, backgroundColor, fontSize?)` in `src/page/modules/chartTheme.ts` takes a
  third argument: the string from `getComputedStyle(document.body).fontSize`. A value that does not
  parse to a number above 0 falls back to 13.
- `vegaPreview.ts` passes the body font size when it reads the theme.
- `chartConfig(theme)` adds the size keys below. With `b = theme.fontSize`, `round1` = rounding to one
  decimal, `legendLabel = round1(b * 0.93)`, `axisLabel = round1(b * 0.85)`:

  | Key | Value | At 14 px |
  | --- | --- | --- |
  | `legend.labelFontSize` | `legendLabel` (0.93x) | 13 |
  | `legend.titleFontSize` | `round1(b * 0.95)` | 13.3 |
  | `legend.titleFontWeight` | `"bold"` | bold |
  | `legend.symbolSize` | `round(0.7 * legendLabel^2)` | 118 |
  | `legend.symbolStrokeWidth` | 2.5 | 2.5 |
  | `legend.rowPadding` | `round1(0.4 * legendLabel)` | 5.2 |
  | `legend.titlePadding` | `round1(0.4 * axisLabel)` (candidate C) | 4.8 |
  | `axis.labelFontSize` | `axisLabel` (0.85x) | 11.9 |
  | `axis.titleFontSize` | `round1(b * 0.95)` | 13.3 |
  | `axis.titleFontWeight` | `"bold"` | bold |
  | `axis.titlePadding` | `round1(0.5 * axisLabel)` | 6 |
  | `title.fontSize` | `round1(b * 1.15)` | 16.1 |
  | `title.fontWeight` | `"bold"` | bold |
  | `title.subtitleFontSize` | `round1(b * 0.9)` | 12.6 |
  | `header.labelFontSize` | `axisLabel` (candidate C) | 11.9 |
  | `header.titleFontSize` | `round1(b * 0.95)` (candidate C) | 13.3 |

- Stroke legends (lines) get the longer, thicker swatch from the same keys: a stroke symbol's length
  follows `symbolSize`, its width `symbolStrokeWidth` (Q7).
- `title.subtitleColor` becomes `theme.foreground` (the label colour) in place of `theme.muted` (Q9).
- Discrete x-axis labels are horizontal: `axisXDiscrete: { labelAngle: 0, labelOverlap: true }` for
  Vega-Lite (Q9). Full Vega has no discrete-axis config: its specs set their own angles.
- The same config object goes to Vega-Lite (`compile(spec, { config })`) and to full Vega
  (`parse(spec, config)`) (Q7). In both, a spec's own `config` and its own mark or axis properties win
  over Studio's (Q3); no code is needed for that beyond keeping the config as the base, which this spec
  proves by a test.
- Colours, fonts and the cream gridlines stay as they are (Q9: the gridline weight is a theme change,
  out of scope).

### 2. Live chart view in the preview (Q4)

- The preview draws a live Vega view with the SVG renderer in place of the `<img>`.
- `src/page/modules/vegaChart.ts` is split so each part stays testable and under the file limits:
  - a shared runtime step: compile (Vega-Lite) or take the spec (Vega), then `parse` with the config;
  - `drawChart` stays the headless SVG-string path used by unit tests;
  - a new mount function builds `new View(runtime, { renderer: "svg", loader, expr:
    expressionInterpreter, logLevel: Error, tooltip })`, calls `initialize(host)` on a detached
    `div.myst-vega-view`, then `await view.runAsync()`.
- The view mounts into the child host, never into `div.myst-vega-diagram` itself: `View.initialize`
  clears its element and sets `role="graphics-document"` and an aria-label, which would overwrite the
  diagram's "Chart diagram" label and data attributes.
- On success `vegaPreview.ts` puts the host in the diagram (`replaceChildren(host)`) and sets the
  render state "rendered", as today. On failure it finalizes the view and calls `showChartError`.
- `config.events.bind` is `"none"` (see open question 1).
- DIAG-122 (data only from allowed folders, `href` refused by `sanitize`) and DIAG-124 (no eval) keep
  their behaviour on the live view: the same loader and interpreter are used.
- Drawing cache (PERF-07, DIAG-009): the cache keeps detached live views by key, at most 16, and
  finalizes a view when it is evicted while detached. A view is reused only when its host is not
  connected (a keyed morph that replaced the block); otherwise a new one is drawn, so two identical
  charts on one page each get their own view. A late result for a key that is no longer shown is cached
  and not shown, as today. The key gains the body font size through `theme`, so a font-size or zoom
  change redraws.
- The keyed morph (`contentMorph.ts`) keeps an unchanged chart block, so its view survives a content
  patch.
- If the SVG renderer causes a CSP violation, the fallback is the native `title` handler on a canvas
  renderer, reported in the PR (Q4). See open question 2.

### 3. Themed hover detail (Q4, Q8)

- Vega-Lite: `config.mark.tooltip: true` gives every mark a tooltip of its encoded fields. A spec's own
  `tooltip` encoding or `"tooltip": null` wins.
- Full Vega: no config adds a tooltip; marks whose `encode` has a `tooltip` show one, others none.
  Studio adds none (Q4).
- The box is a tooltip handler of Studio's own, given to the view as its `tooltip` option, in a new
  module `src/page/modules/chartTooltip.ts`:
  - one shared element on `document.body`, outside `#sphinx-myst-preview-content` (so the export and
    the morph never see it), `role="tooltip"`, class `myst-vega-tooltip`, shown and hidden with the
    `hidden` attribute;
  - rows built with `textContent` only: an object value gives one row per key (muted key, strong
    value); a plain value gives one row;
  - placed at the pointer plus 10 px with `style.setProperty` (CSSOM), flipped to the other side at a
    viewport edge so it does not cover the neighbouring mark;
  - hidden on a null value, on scroll, on `studio:content-replaced` and when its chart is redrawn.
- CSS in `src/core/preview/styles/contentBlockStyles.ts`:
  - `position: fixed`, `pointer-events: none`, a z-index above the content;
  - background `var(--studio-editor-background)`, colour the editor foreground;
  - font `var(--sphinx-preview-font)` at the legend label size (0.93em of the body);
  - key in `var(--studio-descriptionForeground)`, value weight bold;
  - 1 px border in `--sphinx-preview-border`, stronger in dark (both dark selectors:
    `html[data-sphinx-preview-theme-mode="dark"]` and
    `html[data-sphinx-preview-theme-mode="current"] body:is(.vscode-dark, .vscode-high-contrast)`);
  - radius 4 px and a light shadow, as in the hover mock the critic judged.
- No `style` attribute anywhere, no new dependency (vega-tooltip is not one).

### 4. Chart source: hidden in the preview, shown in the export (Q5)

- A preview rule in `contentBlockStyles.ts` hides `details.myst-vega-source` (`display: none`), in
  reading and edit mode, for a drawn chart and a chart in error.
- `exportSheet` in `src/core/export/exportStyles.ts` shows it again (`display: block`); it is written
  after the preview sheet in the exported file, so it wins. The section stays closed in the export.
- `normalizeDiagram` is unchanged: the section stays in the rendered HTML.
- Mermaid and PlantUML "Diagram source" sections are unchanged.
- The error message in `src/page/modules/chartError.ts`, "Unable to render the chart. Its source
  remains available below.", becomes "Unable to render the chart." since the source is no longer
  shown below it. The reason line is unchanged. Mermaid's message is unchanged.
- The find bar (`src/page/modules/findIndex.ts`) skips `.myst-vega-source` (hidden text must not be a
  match) and `.myst-vega-view` (the live SVG's text was not searchable as an image either).

### 5. HTML export (Q4, Q5)

- The export clones the page content, so a chart is exported as its drawn inline SVG, without the
  hover box and with no script. The Chart source section is shown, closed.
- `whenDiagramsSettled` (DIAG-128) still waits for every chart: the render state is set as today.

### 6. Edit mode

- A click on a mapped chart in edit mode still opens the block editor (the DIAG-127 pattern in
  `src/page/features/pageInput.ts`). The live view must not stop that click; the test proves it.

### 7. Requirements (all touched SwRS are `proposed`; no approved item changes)

- SwRS-MDOKFSTUDIO-DIAG-123: the chart is drawn as a live themed SVG view; its text sizes follow the
  body text size; Vega-Lite marks show a themed hover detail box, full Vega marks the ones the spec
  defines; an error shows in place with no source section. The scenario "the Chart source section
  still shows the text" is replaced.
- SwRS-MDOKFSTUDIO-DIAG-121: the figure keeps the collapsed source section in the HTML, hidden in the
  preview and shown in the HTML export.
- SwRS-MDOKFSTUDIO-DIAG-128: a Vega chart is exported as its drawn inline SVG with no hover detail, and
  its Chart source is shown.
- SwRS-MDOKFSTUDIO-DIAG-009: a chart is reused only when its earlier view is detached; two identical
  charts on one page each get a view.
- StRS-MDOKFSTUDIO-DIAG-015, Path 1 step 3: the line "the chart is a themed SVG picture" becomes "the
  chart is a themed live SVG with hover detail". Step 1: "with a collapsed source section" becomes
  "with a source section kept for the export". Editorial, the StRS is proposed.
- DIAG-124, DIAG-122 markers move with the code into the split modules (at most 3 IDs per block).
- After the change: `just requirements-update`, and a dated entry under `## 2026-11-25` in
  `requirements/tiers/log.md`.

### 8. Docs, skill, glossary, screenshots

- `docs/user/charts.md`:
  - the intro says the chart is a live SVG that follows the page theme and text size;
  - the Errors paragraph drops the **Chart source** sentence for the preview; the HTML export keeps the
    section;
  - a new paragraph: a spec's own `config` overrides Studio's sizes and colours; `"tooltip": null` in a
    Vega-Lite mark turns the hover detail off; full Vega shows the tooltips its marks define;
  - the Limits line "tooltips ... not available: the chart is a static picture" is rewritten per open
    question 1.
- `skills/writing-for-markdown-okf-schema-studio/SKILL.md`: the Charts row of the table gains the two
  overrides (own `config`, `"tooltip": null`), inside the existing row: the file is at 158 of 160 lines.
  CORE-073 (the skill test) still passes.
- `.agents/glossary/common.md`: a "hover detail" entry (the themed box shown over a chart mark).
- `images/readme/charts-cream.png` and `charts-dark.png` are shot again with
  `node out/test/probe/chartShots.js <folder>`; the README Charts section keeps its links.
- `CHANGELOG.md` `## Unreleased`: one feat line ending "(CR-<n> vega-charts-readable-legends, PR #<n>)".

## Out of scope

- The cream gridline weight (Q9).
- Adding tooltips to full Vega marks that do not define one (Q4).
- Mermaid and PlantUML source sections and their errors (Q5).
- vega-tooltip or any new dependency (Q8).
- Colour and font-family defaults of charts.
- `href` links on marks: still refused (DIAG-122).

## Evidence

Every test below fails on the code before the change. Where an existing assertion changes, the PR
says why in the test and in the body (constitution: no silent intent change).

### Showcase and test page

- `CHART_DOCUMENT` (`test/page/chartPage.ts`) gains the exploration's Vega-Lite grouped bar chart
  (xOffset, colour legend, subtitle "Grouped bars, in k$", tooltip fields Quarter, Product, Revenue
  (k$)) before the broken chart. Chart counts move from 3 to 4 (showcase: 2 to 3).
- The full Vega chart's symbol mark gets `tooltip: {signal: "datum"}` in its `encode`; its line mark
  gets none. So one Vega mark shows a detail and the other shows none.

### Unit (node, `test/page/modules/vegaChart.test.ts`, `chartTheme` tests)

- `chartConfig` at 14 px gives the table values; at 18 px each value scales (legend label 16.7,
  axis label 15.3, title 20.7); `chartThemeFrom` with "", "abc" or "0px" gives 13.
- `title.subtitleColor` equals `foreground`; `axisXDiscrete.labelAngle` is 0; `mark.tooltip` is true.
- A Vega-Lite spec with its own `config.legend.labelFontSize: 9` draws its legend at 9
  (`drawChart` SVG text); a full Vega spec with its own config keeps it too.
- A Vega-Lite mark with `"tooltip": null` compiles with no tooltip encoding; one with no tooltip gets
  the encoded fields.
- `chartTooltip`: a FakeDocument test (`test/page/modules/fakeDom.ts`) shows key/value rows built as
  text (a value holding `<b>` stays text), hides on null, and sets position with `setProperty` only.
- `chartError.test.ts`: the assertion on the `.myst-vega-image` CSS rule moves to `.myst-vega-view
  svg`, because the image no longer exists; the new message text is asserted.

### Chromium with the real CSP (`test/page/chartCsp.test.ts`, `test/page/chartPage.ts`)

- Every drawn chart is `.myst-vega-diagram > .myst-vega-view > svg`; no `img.myst-vega-image`; the
  diagram keeps aria-label "Chart diagram". (Today's data-URL assertions move to the inline SVG; reason:
  the chart is live now.)
- No CSP violation and no console problem on the page.
- The drawn legend label text has a font size of 13 at the 14 px body (read from the SVG `font-size`).
- Hovering a bar shows `.myst-vega-tooltip` visible, with rows "Quarter", "Product", "Revenue (k$)",
  no `style` attribute on it, and a computed background equal to the page background.
- Hovering the Vega symbol mark shows the box; hovering the Vega line shows none.
- Moving off the mark hides the box.
- `details.myst-vega-source` has computed `display: none` for a drawn chart and for the broken chart;
  the broken chart shows "Unable to render the chart." and its reason.
- Setting `--studio-markdown-font-size: 18px` on the root, then a zoom of 150 % (viewControls), redraws
  the charts with bigger legend text (larger SVG `font-size` each time).
- A theme change redraws, as today.
- In edit mode, a click on a mapped chart posts `previewEditOpen` and no reveal (as in
  `test/page/diagReq.svgClick.requirements.test.ts`).
- Find: searching a word of the hidden source finds no match; searching body text still works.

### Export

- A test takes the page snapshot from the Chromium chart page and builds the file with
  `buildHtmlExport`: the file holds each chart as an inline `svg`, no `.myst-vega-tooltip`, no script,
  and `details.myst-vega-source` closed with computed `display: block` when the file is loaded.

### Checks read the shipped files

- The CSS checks load `PREVIEW_THEME_CSS` and `exportSheet` imported from `src/`, the way the page
  and the export build them, not a copy.
- The chart tests run the real bundle of `src/page/modules/vegaChart.ts` (`vegaBundle.ts`, esbuild)
  and the page built by `buildPreviewWebviewHtml` with the real CSP.
- The skill check reads `skills/writing-for-markdown-okf-schema-studio/SKILL.md` from the repository.
- `test/visual/releaseShowcaseScenarios.ts` (line 40) asserts the live `svg` in place of
  `img.myst-vega-image`; reason: the chart is live now.

### Host and default matrix (one line per cell)

- Cream theme, 14 px body: legend label 13, title bold, hover box on cream background.
- White (light) theme, 14 px body: same sizes, hover box on white.
- Dark theme, 14 px body: same sizes, subtitle in the label colour, box border stronger.
- "current" mode with a VS Code dark body class: same as Dark (second dark selector).
- Markdown font size set to 18 px: legend label 16.7, axis label 15.3.
- Preview zoom 150 % at 14 px: legend label 19.5.
- Body font size unreadable: fallback 13, legend label 12.1.
- Spec with its own `config` sizes: the spec's sizes win.
- Vega-Lite mark with `"tooltip": null`: no box.
- Full Vega mark without a `tooltip` encode: no box.
- Chart in error: message in place, no source shown in the preview.
- HTML export: inline SVG, no box, Chart source shown closed.
- VS Code webview: covered by the same page build and CSP as the Chromium test page; the real-window
  CI job (integration, on push to main) runs the existing chart scenario on the live SVG.
- Chromium test page: every line above is asserted there.

### Scenario steps for the reviewer

1. Open a document with the grouped bar chart in Cream: the legend reads at the paragraph size; the
   Quarter labels are horizontal.
2. Hover a bar: a box with Quarter, Product and Revenue (k$) shows beside the pointer in page colours.
3. Switch to Dark: same sizes, the box border is visible, the subtitle reads in the label colour.
4. Raise the Markdown font size, then zoom: the chart text grows with the page.
5. No Chart source under any chart, in reading and edit mode; click a chart in edit mode: the block
   editor opens.
6. Export HTML: the charts are pictures with no hover box, each with a closed Chart source.

## Open questions

1. The live view brings Vega interactions besides tooltips: selections, hover encodings, zoom and pan
   from a spec's signals. Proposal: pointer interactions run; input widgets are off
   (`config.events.bind: "none"`); `href` stays refused. The Limits line of `docs/user/charts.md` then
   says "input bindings and links are not available". To confirm.
2. The Q4 fallback (canvas renderer with native `title`) would export an empty chart, since the export
   clones the DOM and a canvas has no content there. Proposal: if the SVG renderer violates the CSP,
   stop and report to the Chief of Staff rather than ship the fallback.
3. `legend.symbolStrokeWidth: 2.5` may also thicken the outline of filled legend symbols (bars,
   points); a Vega config cannot target stroke legends alone. Proposal: keep the key if the new
   screenshots show no bloated filled swatch; otherwise drop it from the config and report the choice
   in the PR.
4. The error message rewording ("Unable to render the chart.") follows from Q5 but was not decided by
   name. Proposed as written in section 4.
