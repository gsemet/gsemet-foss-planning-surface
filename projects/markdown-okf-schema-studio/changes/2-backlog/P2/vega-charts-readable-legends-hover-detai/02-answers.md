# Answers

1. vega-Q1 (2026-11-25, the owner, relayed by the Chief of Staff): **Filed from the owner's own request.** Legend text is very small. The owner asks for 2 or 3 candidate renderings judged by a Fable critic, an answer on a default hover detail, and the removal of "Chart source" in the extension's preview.
2. vega-Q2 (2026-11-25, Chief of Staff): **Routine points are the Griller's; a behaviour choice that truly needs the owner goes to the Chief of Staff.**
3. vega-Q3 (2026-11-25, decided by the Griller): **The sizes change in the chart config Studio gives every chart, so the author's own config still wins.** Today `chartConfig` (`src/page/modules/vegaChart.ts`) sets colours and fonts only, so every size is Vega's default: axis and legend labels 10 px, their titles 11 px, the chart title 13 px. That is far under the page text. The new sizes go in the same config, for Vega-Lite (compile config) and for full Vega (parse config). A spec that sets its own `config` or sizes keeps them.
4. vega-Q4 (2026-11-25, decided by the Griller from the code): **A hover detail can be on by default, fully for Vega-Lite and only where the spec asks for one for full Vega, but only if the chart becomes a live drawing.**
   - Why there is none today: `drawChart` runs the view with `renderer: "none"` and `view.toSVG()`, and `vegaPreview.ts` shows the result as an `<img>` (data URL). A picture gets no pointer events, so no tooltip of any kind can show, whatever the spec says.
   - Vega-Lite: `config.mark.tooltip: true` (in effect `{ "content": "encoding" }`) gives every mark a tooltip of its encoded fields, with no change to the author's spec. An author's `tooltip` encoding, or `"tooltip": null`, still wins.
   - Full Vega: a config cannot add a tooltip. Only marks whose `encode` carries a `tooltip` show one. Adding `tooltip: {signal: "datum"}` to every mark would rewrite the author's spec and show raw rows (a line mark's datum is its first point). So the default is to show the tooltips the spec defines, and add none.
   - Handler: Vega's built-in default handler (`defaultTooltip` in vega-view) sets the `title` attribute of the drawn element, which gives a native browser tooltip. It needs no extra package (vega-tooltip is not a dependency) and no inline style, so the page's CSP is unchanged. A themed tooltip box (the critic's verdict, Q7) is the alternative, at the cost of a small handler of Studio's own.
   - Cost: the preview draws a live Vega view (the SVG renderer into the figure) in place of the `<img>`. The PERF-07 drawing cache keys and the reuse of drawings need care. The HTML export keeps a static picture: the export takes a snapshot of the page, so it embeds the drawn SVG with no tooltip (`src/page/modules/exportSnapshot.ts`, DIAGRAM_SELECTOR).
   - The take proves that the live SVG renderer causes no CSP violation (chartCsp test). If it does, the fallback is the native `title` handler on a canvas renderer, reported in the PR.
5. vega-Q5 (2026-11-25, decided by the Griller): **The preview shows no Chart source section, in reading and edit mode, for a drawn chart and for a chart in error. The HTML export keeps its closed Chart source.**
   - In the preview the source is the document: one Edit click opens it in the block editor, and the raw text is beside it. An error keeps its message and reason in place (DIAG-123).
   - The exported file has no editor, so the closed section is the only place its reader finds the spec and the data. The export is a snapshot of the page DOM, so the section stays in the rendered HTML: the preview's styles hide it and the export shows it.
   - Mermaid's and PlantUML's "Diagram source" are not part of this request and stay as they are.
6. vega-Q6 (2026-11-25, decided by the Griller): **The exploration.** Three candidates were drawn by the real preview page (`test/page/chartPage.ts`, with its CSP, headless Chromium) on one showcase: a Vega-Lite line chart with a legend, a Vega-Lite grouped bar chart with a legend, and a full Vega chart with a legend. Each was drawn in Cream, light and dark, plus a hover mock for B and C.
   - A: today's config.
   - B: fixed readable sizes.
   - C: sizes that follow the page's body text size.
   Exact values and images: `work/exploration/`.
7. vega-Q7 (2026-11-25, the Fable critic's verdict, adopted by the Griller): **The default is C, sizes that follow the page text size, with its legend raised to B's size.** The critic read all 13 images and was not told which candidate was preferred.
   - Ranking: C's mechanism with B's legend sizes, then B, then C as drawn, then A.
   - Why:
     - A whispers: 10 px labels beside 14 px text, the owner's complaint, in every theme.
     - B is the most readable as drawn.
     - C as drawn only half-fixes the legend (11.9 px).
     - Only C follows the `markdownOkfSchemaStudio` Markdown font-size setting and the preview zoom; B would whisper again at an 18 px body.
   - The default, as multiples of the body font size (`getComputedStyle(document.body).fontSize`, 14 px by default, fallback 13), given to `chartThemeFrom` as `ChartTheme.fontSize`:
     - legend labels 0.93× (13 px at 14), legend title 0.95×, legend symbol about 120 at 14 px (0.7 × label², rounded), legend row padding 0.4 × label;
     - stroke legends (lines) get a longer, thicker swatch: `symbolStrokeWidth` 2.5, the symbol scaled to match;
     - axis labels 0.85×, axis titles 0.95× with title padding 0.5 × label;
     - chart title 1.15×, subtitle 0.9×;
     - axis, legend and chart titles bold (the rotated y titles look light at 600).
   - The same config goes to Vega-Lite and to full Vega. Exact first values and images: `work/exploration/README.md`.
8. vega-Q8 (2026-11-25, decided by the Griller on the critic's verdict): **The hover detail is a themed box of Studio's own, not the native `title` tooltip.**
   - The native tooltip shows after a delay, in the OS style at a fixed small size, and ignores theme and zoom: the same smallness again.
   - The box is a small tooltip handler given to the Vega view (`tooltip` option). It is drawn in the page:
     - page background and text colours, the chart font at the legend label size;
     - key/value rows, muted key and strong value;
     - a 1 px border, strengthened in dark;
     - offset from the pointer so it does not cover the neighbouring mark.
   - It uses no inline style attribute: CSSOM or a class only, since the CSP has no `unsafe-inline` for styles. It needs no new dependency (vega-tooltip is not one).
   - Vega-Lite marks get `config.mark.tooltip: true`. Full Vega shows the tooltips its spec defines (Q4).
9. vega-Q9 (2026-11-25, decided by the Griller on the critic's notes): **Two more default fixes ride in this CR, one is left out.**
   - In: discrete x-axis labels are horizontal (`labelAngle: 0` with label overlap handling) instead of rotated.
   - In: the subtitle takes the label colour, since the muted grey has low contrast in dark.
   - Out: the cream gridlines are a little heavy. They come from the page border colour, a theme change, not a chart default.
10. vega-Q10 (2026-11-25, decided by the Griller): **Requirements, docs and skill.**
    - DIAG-123 gains the readable, page-relative sizes and the hover detail.
    - DIAG-121 loses the Chart source section in the preview and keeps it in the export.
    - `docs/user/charts.md` drops its "Chart source" sentence for the preview, and says how a spec's own config and `"tooltip": null` override the defaults.
    - The writing skill gets the same two lines if it covers charts.
    - New screenshots of the charts in `images/readme/charts-*.png`.

Grilled enough (2026-11-25): by the Griller with the Fable critic's verdict, on the owner's request relayed by the Chief of Staff. Routine points decided here; the owner's one behaviour question (a default hover detail) is answered by Q4 and Q8.
Destination: running batch batch-09, as its own CR after the clips in the stack (bug day rule: same stack). Critic: yes (Fable, on the rendered candidates, Q7).
