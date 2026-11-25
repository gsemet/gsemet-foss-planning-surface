# Vega charts: live view with a hover detail

Each Vega-Lite or Vega chart in the preview is drawn as a live Vega SVG view instead of an `img`.
Hovering a Vega-Lite mark shows a small box in the page's own colours; a full Vega spec shows only
the tooltips it defines. The HTML export keeps a static picture: the drawn inline SVG, with no hover
box and no script.

## Goal

The owner wants a hover detail on charts by default (live-Q1). Today a chart is an image, which
gets no mouse event, so no hover detail can show. After this change, hovering a Vega-Lite bar,
point or line shows its fields as key and value rows in a box that follows the page theme, text
size and zoom. A writer turns it off for a mark with `"tooltip": null`. Chart data loading and the
page's security rules (no eval, no network, no inline style attribute) are unchanged.

This CR comes after CR-502 "Vega charts: readable text, no Chart source in the preview"
(`vega-charts-readable-legends-hover-detai`) in the batch-09 stack, and after the clip CRs CR-493 and
CR-500. It builds on what CR-502 ships and does not repeat it: page-relative chart sizes
(`ChartTheme.fontSize`, the size keys of `chartConfig`), the Chart source hidden in the preview and
shown in the export, the message "Unable to render the chart.", and `.myst-vega-source` skipped by
find. Where this spec says "today", it means `origin/main` with CR-502 merged on top.

Its decisions come from `02-answers.md` (live-Q1 to live-Q13). The first specification this CR was
split from is kept at `work/first-spec.md`; sections 2, 3 and 5 of it are this CR's, corrected by
the spec critic's findings (live-Q4, live-Q7, live-Q8, live-Q10, live-Q12). This spec supersedes it
where they differ.

The project rules apply as they stand: read `.agents/constitution.md`,
`requirements/guidelines/requirements.guidelines.md` and `requirements/guidelines/project.guidelines.md`
("During a change") before the change. This spec does not restate them.

## Today

- `drawChart(kind, source, theme, chart)` in `src/page/modules/vegaChart.ts` parses the source,
  inlines the files, compiles Vega-Lite with `compile(spec, { config })` or takes the Vega spec,
  runs `vega.parse(spec, config, { ast: true })`, then a headless `new vega.View(runtime, { expr:
  expressionInterpreter, loader: createChartLoader(chart), renderer: "none", logLevel: vega.Error })`,
  and returns `view.toSVG()`.
- `renderCharts` in `src/page/modules/vegaPreview.ts` turns that SVG into a data URL and shows it as
  `<img class="myst-vega-image" alt="Chart">` with `replaceChildren` (`showImage`), then sets
  `data-render-state="rendered"`. Drawings are kept by key in `createMermaidCache()`
  (`src/page/modules/mermaidCache.ts`, 64 strings, `plan` gives keep / reuse / render). The key is
  `diagramKey({ theme: JSON.stringify(theme) }, JSON.stringify([kind, source, files]))`, so it
  already carries the body font size through `theme` (CR-502). A result whose key is no longer the
  node's key is stored and not shown.
- Vega's default tooltip handler is the native `title` tooltip; no tooltip shows today since the
  image gets no pointer event. `chartConfig` has no `mark.tooltip` and no `events` key.
- `takeExportSnapshot` (`src/page/modules/exportSnapshot.ts`) clones `#sphinx-myst-preview-content`;
  `whenDiagramsSettled` waits for every `.myst-vega-diagram` to leave its pending state (DIAG-128).
  The export keeps a `style` attribute unless it points into the host (`guardAttributes`,
  `src/core/export/exportContent.ts`); the exported file has no Content Security Policy.
- The preview CSS for charts is in `src/core/preview/styles/contentBlockStyles.ts` (around line 355:
  `.myst-vega-diagram` with `white-space: pre-wrap` and a monospace font for the source text, and
  `.myst-vega-image` with `max-width: 100%`, `height: auto`, centred). The file has 740 lines on
  `origin/main` (limit 800).
- Facts of the Vega build in `node_modules` that this spec relies on:
  - `View.initialize(el)` clears `el` and sets `role="graphics-document"`,
    `aria-roleDescription="visualization"` and an aria-label from the spec's description.
  - The live SVG renderer sets styles through the CSSOM (`el.style.setProperty`), which the page's
    CSP allows. Its `svg()` / `view.toSVG()` on a live view removes and re-sets the `style` attribute
    with `setAttribute`, which the CSP refuses: the live view never calls them.
  - A gradient fill is written as `fill="url(<page URL>#gradient_N)"` (the page URL from
    `window.location`), so it breaks once copied into another file. Clip paths are written as
    `url(#id)` already.
  - The SVG event handler finds the hovered item from the event target, so hover works on an SVG
    scaled down by CSS (`max-width: 100%`).

## What changes

### 1. The live chart view (live-Q3, live-Q6, live-Q7)

- `src/page/modules/vegaChart.ts` is split so each part stays small and testable:
  - a shared step, `chartRuntime(kind, source, theme, chart)`: parse, inline the files, compile
    (Vega-Lite) or take the spec (Vega), and `vega.parse(..., { ast: true })` with the config, as
    `drawChart` does today. The `@implements_req SwRS-MDOKFSTUDIO-DIAG-124` marker moves with the
    `parse` call.
  - `drawChart` keeps its signature and stays the headless SVG-string path used by the unit tests
    (`renderer: "none"`, `toSVG()`), on top of `chartRuntime`.
  - a new `mountChart(kind, source, theme, chart, tooltip)` builds
    `new vega.View(runtime, { renderer: "svg", loader: createChartLoader(chart), expr:
    expressionInterpreter, logLevel: vega.Error, tooltip })`, creates a detached
    `div.myst-vega-view`, calls `view.initialize(host)`, then `await view.runAsync()`, and returns
    `{ view, host }`. It finalizes the view and rethrows when `runAsync` fails.
  - The loader and `createChartLoader` (DIAG-122) are unchanged and keep their marker; the same
    loader and interpreter serve the live view, so data comes only from the allowed files, `href`
    is refused by `sanitize`, and no expression is compiled to JavaScript (DIAG-124).
  - Put `chartRuntime`, `drawChart` and `mountChart` where the file limits and import boundaries
    allow (for example `vegaChart.ts` keeps the config and the loader, a new `vegaView.ts` holds the
    runtime and the two drawing paths). The markers move with the code (at most 3 IDs per block).
- The view mounts into the child `div.myst-vega-view`, never into `div.myst-vega-diagram` itself:
  `initialize` would clear it and overwrite its aria-label "Chart diagram" and data attributes.
- `chartConfig(theme)` gains `events: { bind: "none" }` (live-Q6): a spec's `bind` input widgets are
  not created. Vega's own pointer interactions (selections, hover encodings, zoom and pan from the
  spec's signals) run in the live view. `href` stays refused.
- `vegaPreview.ts`: `showImage` is replaced by a `showView(chart, host)` that calls
  `chart.replaceChildren(host)` and sets `data-render-state="rendered"`, as today. On failure it
  calls `showChartError` and sets `"error"`, as today. The live view never calls `view.toSVG()` or
  `renderer.svg()`.
- No canvas fallback (live-Q7). If the SVG renderer causes a CSP violation (in the Chromium test
  page or in the VS Code webview), the Driver stops and reports to the Chief of Staff instead of
  shipping: a canvas would export an empty chart, since the export clones the DOM.

### 2. The drawing cache keeps detached live views (live-Q9)

- A new pure module, for example `src/page/modules/chartViewCache.ts`, replaces the use of
  `createMermaidCache` for charts (Mermaid keeps `mermaidCache.ts` unchanged). It is generic over an
  entry `{ isDetached(): boolean; finalize(): void }` so it is unit-tested without Vega. Rules:
  - It holds at most 16 entries by key (least recently used first out).
  - `plan(drawnKey, key)`: `keep` when the node's key is unchanged; `reuse` only when an entry for
    `key` exists **and** its host is detached (`!host.isConnected`), which happens after a keyed
    morph replaced the block or a redraw moved the node to another key; `render` otherwise. So two
    identical charts on one page each get their own view.
  - Storing an entry under a key that holds another entry, or evicting an entry past 16, finalizes
    the old view only when its host is detached; an attached view is dropped from the cache and
    left to its chart.
- `vegaPreview.ts` keeps the view each chart node shows (a `WeakMap<HTMLElement, View>`). On a
  redraw of a node (a new key), its previous view stays if it is the cache entry of its key (it is
  now detached, ready for reuse, for example back to the earlier theme); otherwise it is finalized.
- The key is unchanged: it carries the theme, which carries the body font size (CR-502), so a change
  of theme, Markdown font size or zoom redraws the chart.
- A late result for a key the node no longer has is stored in the cache, detached and not shown, as
  today (PERF-07, DIAG-009).
- The keyed morph (`src/page/modules/contentMorph.ts`) keeps an unchanged chart block, so its live
  view survives a content patch with no redraw (unchanged code; the tests prove it).

### 3. The hover detail (live-Q4, live-Q5)

- Vega-Lite only: the config given to `compile` adds `mark: { ..., tooltip: true }`, so every
  Vega-Lite mark shows its encoded fields. A spec's own `tooltip` encoding, or `"tooltip": null` on
  a mark, wins (Vega-Lite merges the spec over the config).
- Full Vega never gets it: the config given to `vega.parse` for a `vega` chart has no
  `mark.tooltip` (build the two configs so the key cannot leak into the Vega one). Marks whose
  `encode` defines `tooltip` show one; the others show none. Studio rewrites no spec.
- A new module `src/page/modules/chartTooltip.ts` is the view's `tooltip` handler
  (`(handler, event, item, value) => void`, the Vega tooltip handler signature):
  - one shared element, created on first use and appended to `document.body`, outside
    `#sphinx-myst-preview-content`, so the export snapshot and the morph never see it:
    `div.myst-vega-tooltip`, `role="tooltip"`, shown and hidden with the `hidden` attribute;
  - rows built with `createElement` and `textContent` only (never `innerHTML`): an object value
    gives one row per key, `span.myst-vega-tooltip-key` (muted) and `span.myst-vega-tooltip-value`
    (bold); a plain value gives one row with the value only; a nested object or array value is
    written as its JSON text;
  - placed at the pointer (`event.clientX`, `event.clientY`) offset by 10 px right and down, with
    `style.setProperty("left" | "top", "<n>px")` (CSSOM, no `style` attribute); when the box would
    pass the right or bottom edge of the viewport it goes to the left or above the pointer, so it
    does not cover the neighbouring mark;
  - hidden on a `null` or `undefined` value, on a `scroll` event (capture, on `window`), on
    `studio:content-replaced`, and when its chart is redrawn or its view finalized
    (`vegaPreview.ts` calls an exported `hideChartTooltip()` there).
- CSS: a new style module, for example `src/core/preview/styles/chartTooltipStyles.ts`, appended in
  `src/core/preview/previewStyles.ts` next to `CONTENT_BLOCK_CSS` (so `contentBlockStyles.ts` stays
  under its limit after CR-502's rules). The rules select `.myst-vega-tooltip` at body level:
  - `position: fixed`, `pointer-events: none`, a z-index above the content, taken from the
    z-index scale the page CSS already uses;
  - background `var(--studio-editor-background)`, colour the editor foreground, font
    `var(--sphinx-preview-font)` at the legend label size (`0.93em` of the body, the CR-502 legend
    label ratio), a small padding;
  - key colour `var(--studio-descriptionForeground)`, value `font-weight: bold`;
  - a 1 px border in `var(--sphinx-preview-border)`, stronger in dark under both dark selectors
    (`html[data-sphinx-preview-theme-mode="dark"]` and
    `html[data-sphinx-preview-theme-mode="current"] body:is(.vscode-dark, .vscode-high-contrast)`),
    for example the description foreground colour;
  - `border-radius: 4px` and a light shadow, as in the hover mock the Fable critic judged
    (`C-cream-hover.png`, `C-dark-hover.png` in the source CR's `work/exploration/`);
  - `[hidden]` keeps `display: none`.
- The chart CSS in `contentBlockStyles.ts`: the `.myst-vega-image` rule becomes
  `.myst-vega-view` (`display: block`, `white-space: normal`, centred) and `.myst-vega-view > svg`
  (`display: block`, `max-width: 100%`, `height: auto`, `margin-inline: auto`).
- No `style` attribute anywhere, no new dependency (vega-tooltip is not one, live-Q5).

### 4. Find and edit mode

- The find bar (`src/page/modules/findIndex.ts`) adds `.myst-vega-view` to `SKIPPED_SELECTOR`: the
  chart text was not a match while the chart was an image, and stays so.
- A click on a mapped chart in edit mode still opens the block editor (the DIAG-127 handler in
  `src/page/features/pageInput.ts`); a click in reading mode still reveals the lines. No code change
  is expected; the live view must not stop that click, and a test proves it.

### 5. HTML export (live-Q8)

- The export clones the page content, so a drawn chart is exported as its inline
  `div.myst-vega-view > svg`, with no hover box (it is outside the content) and no script.
- `takeExportSnapshot` rewrites, in the clone, every `fill` and `stroke` attribute inside
  `.myst-vega-view svg` whose value is `url(<anything>#<id>)` into `url(#<id>)`, so the gradients
  resolve in the exported file. Mark it `@implements_req SwRS-MDOKFSTUDIO-DIAG-128`.
- `whenDiagramsSettled` (DIAG-128) still waits for every chart; the render state is set as today.
- Mermaid and PlantUML exports are unchanged.

### 6. Clip scenarios that select the chart image (live-Q12)

The chart image no longer exists, so each clip scenario that selects `img.myst-vega-image` is
updated in this CR, on the stack base as merged by then:

- `docs/demo-video/clips/theme-switch/scenario.mjs`: `CHART` becomes
  `".myst-vega-diagram .myst-vega-view > svg"`. `pageState` reads the chart's `outerHTML` in place of
  its `src`, so `waitForMode` still proves the chart was drawn again in the new colours (the markup
  differs per theme). `drawingBox(frame, CHART)` boxes the `svg`. Comments that say "img" or "src"
  for the chart are corrected.
- `docs/demo-video/clips/advanced-renderings-tour/scenario.mjs` (CR-493): marks 3 and 4 select
  `.myst-vega-diagram[data-myst-chart-kind="vega-lite"] .myst-vega-view > svg` and
  `.myst-vega-diagram[data-myst-chart-kind="vega"] .myst-vega-view > svg`; `drawn(frame)` asks each
  Vega block for its `svg` in place of its `img`.
- `docs/demo-video/clips/export-html/scenario.mjs` (CR-500): `drawn(frame)` asks the two Vega blocks
  for `.myst-vega-view > svg`; `verify` expects in the exported file two `img.myst-mermaid-image`
  with a `data:image/svg+xml` source and two `.myst-vega-view > svg` (no `img.myst-vega-image`); the
  check of the Integrated Browser page counts two Mermaid images loaded and two chart `svg`.
- `test/visual/releaseShowcaseScenarios.ts` (line 40): "the chart is drawn as an image" becomes "the
  chart is drawn as a live SVG", selector `... .myst-vega-diagram[data-render-state="rendered"]
  .myst-vega-view > svg`.
- Any other `img.myst-vega-image` left in `test/`, `docs/` or `src/` on the stack base is updated the
  same way (`git grep myst-vega-image` finds nothing at the end).
- The clips' media (video, gif, frames, contact sheets) are not re-rendered in this CR.

### 7. Requirements (live-Q13; every touched item is `proposed`, no approved item changes)

- SwRS-MDOKFSTUDIO-DIAG-123 (as CR-502 left it): the title, statement and nominal scenario say each
  chart element holds one `div.myst-vega-view` with a live SVG view (max-width 100%, centred) in the
  page colours; add the hover part: a Vega-Lite mark shows a themed hover detail with its fields as
  key and value rows, `"tooltip": null` on a mark shows none, a full Vega mark shows only the tooltip
  its `encode` defines; input bindings are not created. Verification notes name the new tests.
- SwRS-MDOKFSTUDIO-DIAG-128: a Vega chart is exported as its drawn inline SVG with no hover detail
  and no script, its gradient references local to the file; Mermaid and PlantUML stay images. The
  verification notes name the new export test.
- SwRS-MDOKFSTUDIO-DIAG-009: for a chart, an earlier drawing is reused only when its view is
  detached (a node a keyed morph replaced, or an earlier theme); two identical charts on one page
  each get a view; at most 16 chart views are kept and an evicted detached view is finalized. The
  row "A chart is drawn, a newer theme replaces it while it runs: the result is cached and not
  shown" stays.
- StRS-MDOKFSTUDIO-DIAG-015, Path 1 step 3: "the chart is a themed SVG picture" becomes "the chart is
  a themed live SVG with hover detail". Editorial: the StRS is `proposed`.
- Markers: `@implements_req SwRS-MDOKFSTUDIO-DIAG-123` on `mountChart`, on the Vega-Lite tooltip
  config and in `chartTooltip.ts`, and in the companion `*.markers.ts` of the new style module if its
  rules live in a template string; `@implements_req SwRS-MDOKFSTUDIO-DIAG-009` on the new cache;
  `@implements_req SwRS-MDOKFSTUDIO-DIAG-128` on the gradient rewrite; DIAG-122 and DIAG-124 move
  with the code. Each new test carries `@tests_req` for what it proves.
- After the change: `just requirements-update`, and a dated entry under `## 2026-11-25` (or the day
  of the change) in `requirements/tiers/log.md`.

### 8. Docs, skill, glossary, screenshots, changelog

- `docs/user/charts.md`:
  - the intro calls the chart a live SVG drawing that follows the page theme and text size (in
    place of "an SVG picture");
  - a paragraph on the hover detail: hovering a Vega-Lite mark shows its fields in a small box;
    `"tooltip": null` on a mark turns it off; a full Vega spec shows only the tooltips its marks
    define;
  - the Limits line "Vega interactions (tooltips, selections, links) ... the chart is a static
    picture" becomes: input bindings and links are not available; `image` marks that load a URL are
    not drawn (data URIs are). Selections, zoom and pan defined by the spec work.
  - the export paragraph (if any, else the Errors one) says the HTML export holds the drawn chart
    with no hover detail.
- `skills/writing-for-markdown-okf-schema-studio/SKILL.md`: the Charts row of the table gains, inside
  the row, "hover detail on Vega-Lite marks, `"tooltip": null` to turn it off; Vega shows its own
  tooltips". The file must stay at or under its line limit (160): no new line. The skill test
  (CORE-073, `test/core/render/writingSkill.test.ts`) still passes.
- `.agents/glossary/common.md`: a **Hover detail** entry: the themed box shown over a chart mark
  (`div.myst-vega-tooltip`, `src/page/modules/chartTooltip.ts`); and **Live chart view**: the Vega
  SVG view drawn in `div.myst-vega-view`.
- Screenshots: `test/probe/chartShots.ts` also writes `chart-hover-cream.png` and
  `chart-hover-dark.png` (the pointer on a bar of the grouped bar chart, the box shown). They go in
  the PR body (Impacts). `images/readme/charts-cream.png` and `charts-dark.png` are shot again with
  `node out/test/probe/chartShots.js <folder>` since the chart is now drawn inline (live-Q11: if
  the legend swatches of filled marks look bloated with `legend.symbolStrokeWidth: 2.5`, the key is
  dropped from `chartConfig` and the PR says so).
- `CHANGELOG.md` `## Unreleased`: one feat line, "Charts in the preview are live: hovering a
  Vega-Lite mark shows its values in a themed box" ending "(CR-<n> vega-charts-live-view, PR #<n>)".

## Out of scope

- Everything CR-502 ships (sizes, Chart source, error message, `.myst-vega-source` find skip).
- Adding tooltips to full Vega marks that define none (live-Q4).
- A canvas renderer or the native `title` tooltip (live-Q5, live-Q7).
- vega-tooltip or any new dependency.
- Input bindings (`bind`) and `href` links on marks.
- Re-rendering the clips' media; the clips' storyboards and timings.
- Mermaid and PlantUML drawing, cache and export.

## Evidence

Every new test fails on the code before the change. Where an existing assertion changes, the PR
says why in the test and in the body (constitution, section 3: the chart is live now).

### Test page and documents

- `test/page/chartPage.ts`: in `CHART_DOCUMENT` the full Vega chart's `symbol` mark gets
  `tooltip: { signal: "datum" }` in its `encode.enter`; its `line` mark gets none. So one Vega mark
  shows a detail and the other none. The grouped bar chart CR-502 added (tooltip fields Quarter,
  Product, Revenue (k$) from its encoding titles) is the Vega-Lite hover target.
- `openPreviewPage` gains an option to also serve the page runtime: it writes `out/bundle/preview.js`
  from `pageRuntimeScript()` (`test/page/runtimeHarness.ts`, as `test/page/svgBreakout.test.ts`
  does) and lets `bundleUri` serve both `preview.js` and `vegaPreview.js`. The zoom, edit-click and
  find tests below use it (live-Q10).
- An export document: `CHART_SHOWCASE_DOCUMENT` plus a Vega-Lite area chart with a linear gradient
  fill (`mark: { type: "area", color: { gradient: "linear", x1: 1, y1: 1, x2: 1, y2: 0, stops: [...] } }`).

### Unit (node)

- `test/page/modules/vegaChart.test.ts` (or the test of the new module):
  - the Vega-Lite config has `mark.tooltip: true`; the config used for a full Vega chart has no
    `mark.tooltip`; both have `events.bind: "none"`;
  - a Vega-Lite bar with no tooltip compiles to a mark whose encode has a `tooltip` of its fields; a
    Vega-Lite mark with `"tooltip": null` compiles with none;
  - a full Vega mark with no tooltip encode, once run (`drawChart` path or a headless view from
    `chartRuntime`), has a null tooltip on its scene items (live-Q4);
  - `drawChart` still returns the same SVG text for the existing cases.
- `test/page/modules/chartViewCache.test.ts` (fake entries): keep / reuse / render; reuse only of a
  detached entry; an attached entry gives `render`; at most 16 entries; an evicted or replaced
  detached entry is finalized, an attached one is not.
- `test/page/modules/chartTooltip.test.ts` (FakeDocument of `test/page/modules/fakeDom.ts`): an
  object value gives key and value rows built as text (a value holding `<b>x</b>` stays text, no
  element `b`); a plain value gives one row; `null` hides; position is set with `setProperty`
  only (no `style` attribute); at a viewport edge the box goes to the other side of the pointer;
  one shared element across two calls; it is a child of `body`, not of the content.
- `test/page/modules/exportSnapshot.test.ts`: a clone holding `.myst-vega-view svg` with
  `fill="url(vscode-webview://x/index.html#gradient_1)"` comes out with `fill="url(#gradient_1)"`;
  an `url(#clip1)` and attributes outside `.myst-vega-view` are unchanged.
- `test/page/modules/chartError.test.ts`: the `.myst-vega-image` CSS assertion moves to
  `.myst-vega-view > svg` (`max-width: 100%`, `height: auto`); reason: the image no longer exists.
- A CSS test reads `PREVIEW_THEME_CSS` as shipped (imported from `src/`): `.myst-vega-tooltip` has
  `position: fixed` and `pointer-events: none`, both dark selectors give it a border rule.

### Chromium with the real CSP (`test/page/chartCsp.test.ts`)

- Every drawn chart is `.myst-vega-diagram > .myst-vega-view > svg`; no `img.myst-vega-image`; the
  diagram keeps aria-label "Chart diagram" and its data attributes. Today's data-URL assertions
  (lines 33 and 42) move to the inline SVG; reason: the chart is live now.
- No CSP violation (`window.__violations`) and no console problem, after the first draw, a hover and
  a theme change.
- Hovering a bar of the grouped bar chart (`page.mouse.move` on the bar's `path`) shows
  `.myst-vega-tooltip` visible, with rows "Quarter", "Product", "Revenue (k$)" and their values, no
  `style` attribute, a computed background equal to the page's background and a font size equal to
  the legend label size; moving off the marks hides it.
- Hovering the Vega `symbol` mark shows the box; hovering the Vega `line` mark shows none.
- A Vega-Lite chart whose mark has `"tooltip": null` shows no box.
- Scrolling the page with the box shown hides it.
- In dark (`mode` dark), the box's computed border colour differs from the Cream one and from its
  background.
- A theme change draws the charts again (a new `svg` element, new colours) and a change back reuses
  the earlier detached view (the same `svg` element as before the first change).
- With two identical charts on one page, each diagram holds its own `svg` (two distinct elements,
  both shown).
- On the page with the page runtime (option above):
  - setting `--studio-markdown-font-size: 18px` on the root, then a 150 % zoom through the view
    controls, draws the charts again with a larger legend `font-size` each time, and the hover box
    font grows too;
  - in edit mode, a click on a mapped chart's `svg` posts `previewEditOpen` and no reveal; in
    reading mode it posts a reveal (the DIAG-127 behaviour, as in
    `test/page/diagReq.svgClick.requirements.test.ts`);
  - find: a word that appears only in a chart's axis title finds no match; a word of the body text
    still finds one;
  - a content patch that keeps the chart block keeps the same `svg` element (keyed morph).

### Export

- A test takes the snapshot on the Chromium chart page (the export document with the gradient chart)
  with `takeExportSnapshot`, builds the file with `buildHtmlExport`, writes it and loads it in
  Chromium: each chart is an inline `.myst-vega-view > svg`, the file holds no `.myst-vega-tooltip`
  and no `<script`, every `url(` reference in a chart's `fill` or `stroke` is `url(#id)` and the
  element with that id is in the same file (a `linearGradient`), and the area's `path` has a
  computed `fill` that is that gradient.

### Real VS Code window (live-Q10)

- A new real-input scenario, for example `scenarioLiveChart` in a new
  `test/integration/realInput/liveChart.ts`, added to the sequence and to the `single` map of
  `test/integration/realInput/run.ts` (`"live-chart"`), with its capture id registered in
  `test/shared/captureRegistry.ts` (group `diagrams`): it opens a document with a Vega-Lite bar
  chart in the Studio editor, waits for the render, installs a `securitypolicyviolation` listener in
  the preview frame, toggles the theme once (a redraw under the listener), then checks a
  `.myst-vega-view > svg` in each chart, moves the pointer over a bar and sees `.myst-vega-tooltip`
  visible with its rows, and finds no violation recorded. It captures the window with the box shown.
- This runs in the CI integration job, which runs on a push to `main` and not on a pull request.
  Before marking the PR ready, run it on the branch with
  `gh workflow run ci.yml --ref <branch> -f heavy=true` and link the run in the PR. Locally on
  Windows, run the single scenario if the screen can be held (see "local-worktree" guideline for
  unattended app-window tests).

### Clips

- `just clip-kit-test` passes (it imports the shipped scenarios).
- `just clip theme-switch take`, `just clip advanced-renderings-tour take` and
  `just clip export-html take` each run once in a real window and pass their `setup` and `verify`
  with the new selectors; their media outputs are not committed (restore them with `git restore`).

### Checks read the shipped files

- The CSS checks load `PREVIEW_THEME_CSS` and `exportSheet` imported from `src/`, the way the page
  and the export build them, not a copy.
- The chart tests run the real esbuild bundle of `src/page/modules/vegaPreview.ts` and the page built
  by `buildPreviewWebviewHtml` with the real CSP; the page-runtime tests add the real
  `pageRuntimeScript()`.
- The export test builds the file with the shipped `buildHtmlExport` from a snapshot the shipped
  `takeExportSnapshot` took on that page.
- The skill check reads `skills/writing-for-markdown-okf-schema-studio/SKILL.md` from the repository.
- The clip checks import the shipped `scenario.mjs` files.

### Host and default matrix (one line per cell)

- Chromium test page, Cream, 14 px body: live SVG, hover box on cream with the legend label size.
- Chromium test page, White: hover box on white.
- Chromium test page, Dark: hover box on dark with the stronger border.
- "current" mode with a VS Code dark body class: same as Dark (second dark selector).
- Markdown font size 18 px, then zoom 150 %: chart redrawn larger, box font larger.
- Vega-Lite mark with no `tooltip`: box with its encoded fields (default on).
- Vega-Lite mark with `"tooltip": null`: no box.
- Full Vega mark with a `tooltip` encode: box. Without: no box.
- Spec with a `bind` input: no input widget drawn.
- Narrow page where the chart is scaled down: hover still finds the mark.
- Chart in error: the error in place, no view, no box.
- HTML export: inline SVG, gradients local, no box, no script.
- VS Code webview, real window (integration job, heavy run on the branch): live SVG, hover box, no
  CSP violation.

### Scenario steps for the reviewer

1. Open a document with the grouped bar chart in Cream; hover a bar: a box with Quarter, Product and
   Revenue (k$) shows beside the pointer in the page colours. Move off: it hides.
2. Hover near the right edge of the preview: the box flips to the left of the pointer.
3. Switch to Dark: the chart redraws, the box border is visible.
4. Add `"tooltip": null` to the mark: no box. In a full Vega chart, only marks with a tooltip encode
   show one.
5. Zoom the preview: the chart and the box text grow.
6. Edit mode: click a chart, the block editor opens.
7. Export HTML: the charts are pictures (gradient included) with no hover box.

## Open questions

None. The first specification's open questions are answered by live-Q6 (interactions), live-Q7 (no
canvas fallback) and live-Q11 (swatch stroke width); the error message moved to CR-502.
