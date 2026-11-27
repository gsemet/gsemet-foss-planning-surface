# Vega charts: readable text, no Chart source in the preview

Vega-Lite and Vega chart text (legends, axes, titles) follows the page text size; discrete x labels
are horizontal and the subtitle takes the label colour. The preview hides the **Chart source**
section under a chart; the HTML export keeps it. The chart stays a picture (`img`) in this CR: the
live view with a hover detail is a separate CR that comes after this one in the stack (Q11).

## Goal

The owner finds chart text too small in the preview, legends first. After this change the legend,
axis and title sizes of every chart follow the page's body text size, so they also follow the
Markdown font-size setting and the preview zoom, in Cream, light and dark. The preview no longer
shows the collapsed **Chart source** section under a chart, since the source is the document itself;
the HTML export, which has no editor, keeps it.

This spec is self-contained. Its decisions come from `02-answers.md` (Q3, Q5, Q7, Q9, Q10, narrowed
by Q11 to Q13) and its first values from `work/exploration/README.md`. Both are restated here where
they are needed.

The project rules apply as they stand. Read `.agents/constitution.md`,
`requirements/guidelines/requirements.guidelines.md` and `requirements/guidelines/project.guidelines.md`
("During a change") before the change. This spec does not restate them.

## Today

- `chartConfig(theme)` in `src/page/modules/vegaChart.ts` sets colours and fonts only. Every size is
  Vega's default: axis and legend labels 10 px, their titles 11 px, chart title 13 px, subtitle 11 px,
  legend symbolSize 100, rowPadding 2, axis titlePadding 4. The page body text is 14 px in all themes.
- `chartThemeFrom(read, backgroundColor)` (`src/page/modules/chartTheme.ts`) builds the `ChartTheme`
  from the page's CSS variables; `renderCharts` in `src/page/modules/vegaPreview.ts` calls it, keys
  each drawing on `JSON.stringify(theme)` with the source and data (PERF-07), and shows the result as
  `<img class="myst-vega-image">` with an SVG data URL. A `MutationObserver` on `html` and `body`
  attributes (`class`, `style`, theme attributes) redraws the charts; the zoom sets
  `--sphinx-preview-zoom` on the root `style`, and `html, body` take
  `font-size: var(--sphinx-preview-zoomed-font-size)` (`contentLayoutStyles.ts`), so the body font
  size already follows the Markdown font size and the zoom.
- `normalizeDiagram` (`src/core/render/mystNormalize.ts`) builds the figure with
  `div.myst-vega-diagram` (aria-label "Chart diagram") and a collapsed `details.myst-vega-source`
  (summary "Chart source", the spec in pre/code). Its styles are in
  `src/core/preview/styles/contentBlockStyles.ts` (around line 373). The preview and the HTML export
  both show it.
- `showChartError` (`src/page/modules/chartError.ts`) writes "Unable to render the chart. Its source
  remains available below." with a details section holding the reason.
- The find bar (`src/page/modules/findIndex.ts`, `SKIPPED_SELECTOR`) keeps folded sections searchable,
  so today the Chart source text is a find match.

## What changes

### 1. Default chart config: page-relative sizes (Q3, Q7, Q9)

- `ChartTheme` gains `fontSize: number`, the body font size in px.
- `chartThemeFrom(read, backgroundColor, fontSize?)` takes a third argument: the string from
  `getComputedStyle(document.body).fontSize`. A value that does not parse to a number above 0 falls
  back to 13.
- `renderCharts` in `vegaPreview.ts` passes the body font size. Since the key holds
  `JSON.stringify(theme)`, a change of the Markdown font size or of the zoom gives a new key and the
  existing observer redraws the charts; no new trigger is needed.
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
  follows `symbolSize`, its width `symbolStrokeWidth` (Q7). `symbolStrokeWidth: 2.5` stays unless the
  new screenshots show bloated filled swatches (bars, points); in that case the key is dropped and the
  PR says so (Q12, last sentence).
- `title.subtitleColor` becomes `theme.foreground` (the label colour) in place of `theme.muted` (Q9).
- Discrete x-axis labels are horizontal: `axisXDiscrete: { labelAngle: 0, labelOverlap: true }` for
  Vega-Lite (Q9). Full Vega has no discrete-axis config: its specs set their own angles.
- The same config object goes to Vega-Lite (`compile(spec, { config })`) and to full Vega
  (`parse(spec, config)`) (Q7). In both, a spec's own `config` and its own mark or axis properties win
  over Studio's (Q3); no code is needed for that beyond keeping Studio's config as the base, which a
  test proves.
- No `mark.tooltip` key in this CR: the hover detail belongs to the next CR (Q11).
- Colours (other than the subtitle), fonts and the cream gridlines stay as they are (Q9: the gridline
  weight is a theme change, out of scope).

### 2. Chart source: hidden in the preview, shown in the export (Q5)

- A preview rule in `contentBlockStyles.ts` hides `details.myst-vega-source` (`display: none`), in
  reading and edit mode, for a drawn chart and for a chart in error.
- `exportSheet` in `src/core/export/exportStyles.ts` shows it again (`display: block`); it is written
  after the preview sheet in the exported file, so it wins. The section stays closed in the export.
- `normalizeDiagram` is unchanged: the section stays in the rendered HTML, and the export snapshot
  (`src/page/modules/exportSnapshot.ts`) carries it as today.
- Mermaid and PlantUML "Diagram source" sections and Mermaid's error message are unchanged.
- The message in `src/page/modules/chartError.ts` becomes "Unable to render the chart." since the
  source is no longer shown below it (Q11). The reason details section is unchanged.
- The find bar skips `.myst-vega-source`: `findIndex.ts` adds it to `SKIPPED_SELECTOR`, since hidden
  text must not be a match.

### 3. Requirements (every touched item is `proposed`; no approved item changes)

- SwRS-MDOKFSTUDIO-DIAG-123: the chart text sizes follow the body text size (legend label 0.93x, axis
  label 0.85x, title 1.15x of the body), discrete x labels are horizontal, the subtitle takes the label
  colour, and a spec's own config wins. The error scenario reads "one paragraph Unable to render the
  chart." and its last clause "the Chart source section still shows the text" becomes "no Chart source
  section is shown in the preview".
- SwRS-MDOKFSTUDIO-DIAG-121: the figure keeps the collapsed Chart source section in the HTML; the
  preview hides it and the HTML export shows it (closed). Statement, scenario and criteria follow.
- StRS-MDOKFSTUDIO-DIAG-015, Path 1 step 1: "with a collapsed source section" becomes "with a source
  section kept for the HTML export". Editorial, the StRS is proposed. Step 3 ("a themed SVG picture")
  is unchanged.
- DIAG-009, DIAG-128 and DIAG-123's hover part are not touched here (Q11: next CR).
- The markers: `@implements_req SwRS-MDOKFSTUDIO-DIAG-123` on `chartConfig` / `chartThemeFrom` where
  the sizes are, `@implements_req SwRS-MDOKFSTUDIO-DIAG-121` on the preview and export CSS rules and on
  the find skip; the new tests carry `@tests_req` for the item they prove.
- After the change: `just requirements-update`, and a dated entry under `## 2026-11-25` in
  `requirements/tiers/log.md`.

### 4. Docs, skill, screenshots, changelog

- `docs/user/charts.md`:
  - the intro says the chart text follows the page theme and text size;
  - the Errors paragraph (line 87) drops the **Chart source** sentence for the preview and says the
    HTML export keeps the section;
  - a new paragraph: a spec's own `config` overrides Studio's sizes and colours.
  - The Limits line "Vega interactions (tooltips, selections, links) ... the chart is a static
    picture" (line 100) is unchanged: it stays true in this CR.
- `skills/writing-for-markdown-okf-schema-studio/SKILL.md`: the Charts row of the table (line 44) gains
  the override (own `config` sets sizes and colours), inside the existing row: the file is at 158 of
  160 lines. CORE-073 (the skill test) still passes.
- `images/readme/charts-cream.png` and `charts-dark.png` are shot again with
  `node out/test/probe/chartShots.js <folder>`; the README Charts section keeps its links.
- `CHANGELOG.md` `## Unreleased`: one feat line ending "(CR-<n> vega-charts-readable-legends, PR #<n>)".

## Out of scope

- The live Vega view, the hover detail box, `config.mark.tooltip`, the view cache, the export of a
  live SVG, DIAG-009, DIAG-128 and the "hover detail" glossary entry: the next CR, "Vega charts: live
  view with a hover detail" (Q11, Q12).
- The clip scenarios that select `img.myst-vega-image` (theme-switch, CR-493, CR-500): the chart stays
  an image here, so they are untouched (Q13).
- The cream gridline weight (Q9).
- Mermaid and PlantUML source sections and their errors (Q5).
- Colour and font-family defaults of charts, apart from the subtitle colour.

## Evidence

Every new test below fails on the code before the change. Where an existing assertion changes, the PR
says why in the test and in the body (constitution: no silent intent change).

### Showcase and test page

- `CHART_DOCUMENT` (`test/page/chartPage.ts`) gains the exploration's Vega-Lite grouped bar chart
  (xOffset, a colour legend, a discrete Quarter x axis, subtitle "Grouped bars, in k$") before the
  broken chart. Chart counts move from 3 to 4 (showcase: 2 to 3); `chartCsp.test.ts` line 48 and the
  other counts follow, with the reason (a new showcase chart).

### Unit (node: `test/page/modules/vegaChart.test.ts`, the `chartTheme` tests, `chartError.test.ts`)

- `chartConfig` at 14 px gives the table values; at 18 px each value scales (legend label 16.7, axis
  label 15.3, title 20.7); `chartThemeFrom` with "", "abc" or "0px" gives `fontSize` 13 and
  "18px" gives 18.
- `title.subtitleColor` equals `foreground`; `axisXDiscrete.labelAngle` is 0 and `labelOverlap` true;
  the config has no `mark.tooltip`.
- A Vega-Lite spec with its own `config.legend.labelFontSize: 9` draws its legend at 9 (`drawChart`
  SVG text); a full Vega spec given its own legend font size keeps it too.
- `chartError.test.ts`: the message is exactly "Unable to render the chart." (the existing
  `/Unable to render the chart/` match is tightened, with the reason). The `.myst-vega-image` CSS
  assertion stays: the image is unchanged.

### Chromium with the real CSP (`test/page/chartCsp.test.ts`, `test/page/chartPage.ts`)

- Every drawn chart is still `img.myst-vega-image`; no CSP violation and no console problem.
- The drawn legend label text has `font-size` 13 at the 14 px body, read from the SVG of the image's
  data URL.
- The grouped bar chart's Quarter labels are horizontal (no `rotate` transform on the x label text in
  that SVG).
- Setting `--studio-markdown-font-size: 18px` on the root, then a zoom of 150 % (`viewControls`),
  redraws the charts with bigger legend text (larger SVG `font-size` each time).
- A theme change redraws, as today.
- `details.myst-vega-source` has computed `display: none` for a drawn chart and for the broken chart,
  in reading and edit mode; the broken chart shows "Unable to render the chart." and its reason.
- Find: searching a word present only in a chart's source finds no match; searching body text still
  finds it.

### Export

- A test takes the page snapshot from the Chromium chart page and builds the file with
  `buildHtmlExport`: when the file is loaded, each `details.myst-vega-source` is closed and has computed
  `display: block`, and the charts are still images.

### Checks read the shipped files

- The CSS checks load `PREVIEW_THEME_CSS` and `exportSheet` imported from `src/`, the way the page and
  the export build them, not a copy.
- The chart tests run the real bundle of `src/page/modules/vegaChart.ts` (`vegaBundle.ts`, esbuild)
  and the page built by `buildPreviewWebviewHtml` with the real CSP.
- The skill check reads `skills/writing-for-markdown-okf-schema-studio/SKILL.md` from the repository.
- `test/visual/releaseShowcaseScenarios.ts` (line 40) is unchanged: it still selects
  `img.myst-vega-image`.

### Host and default matrix (one line per cell)

- Cream theme, 14 px body: legend label 13, titles bold, Quarter labels horizontal.
- White (light) theme, 14 px body: same sizes.
- Dark theme, 14 px body: same sizes, subtitle in the label colour.
- "current" mode with a VS Code dark body class: same as Dark.
- Markdown font size set to 18 px: legend label 16.7, axis label 15.3.
- Preview zoom 150 % at 14 px: legend label 19.5.
- Body font size unreadable: fallback 13, legend label 12.1.
- Spec with its own `config` sizes: the spec's sizes win.
- Chart in error: "Unable to render the chart." with its reason in place, no source shown in the
  preview.
- HTML export: the Chart source section shown, closed.
- VS Code webview: covered by the same page build and CSP as the Chromium test page; the real-window
  CI job (integration, on push to main) runs the existing chart scenario unchanged.

### Scenario steps for the reviewer

1. Open a document with the grouped bar chart in Cream: the legend reads at the paragraph size; the
   Quarter labels are horizontal.
2. Switch to Dark: same sizes, the subtitle reads in the label colour.
3. Raise the Markdown font size, then zoom: the chart text grows with the page.
4. No Chart source under any chart, in reading and edit mode, also under a broken chart, which says
   "Unable to render the chart." with its reason.
5. Find a word of a chart's source: no match.
6. Export HTML: each chart has a closed Chart source that opens on the spec.
7. Look at the new `images/readme/charts-*.png`: line legend swatches are longer and thicker; filled
   swatches are not bloated (otherwise `symbolStrokeWidth` is dropped, per section 1).

## Open questions

None. The first run's questions on the live view and the canvas fallback moved to the next CR (Q11,
Q12); the swatch stroke width is decided by Q12; the error message is decided by Q11.
