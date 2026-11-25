# Vega chart style candidates

Shot from the real preview page (CSP on, headless Chromium, `test/page/chartPage.ts`) at 820 px
wide, from a detached worktree of origin/main (4a47151e). Three charts per shot: a Vega-Lite line
chart (3 series, colour legend), a Vega-Lite grouped bar chart (xOffset, legend, subtitle), a full
Vega line chart (stroke legend, axis titles). No CSP violation, no console error, no chart in
error, in any shot.

Only the size keys differ between candidates; the colour and font keys are today's for all three.
The same config object is passed to Vega-Lite (`compile`) and to full Vega (`vega.parse`), so full
Vega gets the same sizes.

## A, today

No size key: Vega defaults (axis and legend labels 10, axis and legend titles 11 bold, title 13
bold, subtitle 11, legend symbolSize 100, rowPadding 2, axis titlePadding 4).

## B, fixed readable sizes

```json
{
  "title":  { "fontSize": 16, "fontWeight": 600, "subtitleFontSize": 13 },
  "axis":   { "labelFontSize": 12, "titleFontSize": 13, "titleFontWeight": 600, "titlePadding": 8 },
  "legend": { "labelFontSize": 13, "titleFontSize": 13, "titleFontWeight": 600, "symbolSize": 120, "rowPadding": 6 },
  "header": { "labelFontSize": 13, "titleFontSize": 13 }
}
```

## C, sizes follow the page's text size

`ChartTheme.fontSize` (optional) = `parseFloat(getComputedStyle(document.body).fontSize)`, passed by
`vegaPreview.ts` as a third argument of `chartThemeFrom`. With `body` the body size (fallback 13),
`label = round1(body * 0.85)`, `heading = round1(body * 0.95)`, `chartTitle = round1(body * 1.15)`:

```json
{
  "title":  { "fontSize": "chartTitle", "fontWeight": 600, "subtitleFontSize": "label" },
  "axis":   { "labelFontSize": "label", "titleFontSize": "heading", "titleFontWeight": 600, "titlePadding": "round1(label * 0.5)" },
  "legend": { "labelFontSize": "label", "titleFontSize": "heading", "titleFontWeight": 600,
              "symbolSize": "round(label^2 * 0.7)", "rowPadding": "round1(label * 0.35)", "titlePadding": "round1(label * 0.4)" },
  "header": { "labelFontSize": "label", "titleFontSize": "heading" }
}
```

Resolved at the measured 14 px body:

```json
{
  "title":  { "fontSize": 16.1, "fontWeight": 600, "subtitleFontSize": 11.9 },
  "axis":   { "labelFontSize": 11.9, "titleFontSize": 13.3, "titleFontWeight": 600, "titlePadding": 6 },
  "legend": { "labelFontSize": 11.9, "titleFontSize": 13.3, "titleFontWeight": 600, "symbolSize": 99, "rowPadding": 4.2, "titlePadding": 4.8 },
  "header": { "labelFontSize": 11.9, "titleFontSize": 13.3 }
}
```

## Measured body font size

| Theme | body font-size | paragraph font-size | background |
| ----- | -------------- | ------------------- | ---------- |
| cream (light + cream mode) | 14px | 14px | rgb(245, 241, 232) |
| dark | 14px | 14px | rgb(31, 31, 31) |
| light | 14px | 14px | rgb(255, 255, 255) |

The page font size comes from `--studio-markdown-font-size` (default 14px) times the preview
zoom (`pageChromeStyles.ts`), so in C the chart text would follow the user's Markdown font size
setting and the zoom; at the default it lands close to B.

## Hover mock (B and C, cream and dark)

Native Vega tooltips (`title`) do not show headless. The probe injects a box over the Q3
"Cloud sync" bar: page background and text colour, page font at the axis label size read from the
drawn SVG (12px in B, 11.9px in C), 1px border in `--sphinx-preview-border`, radius 4, a light
shadow, rows "Quarter: Q3", "Product: Cloud sync", "Revenue (k$): 39".

## Tuning

None of the sizes was tuned: no clipped text and no legend overlap in any shot. Choices the brief
left open: C's paddings (axis titlePadding 0.5 x label, legend rowPadding 0.35 x label, legend
titlePadding 0.4 x label) and symbolSize 0.7 x label squared. Probe fix only: the hover rows are the
bar's tooltip fields, not its aria-label (the aria-label repeats the xOffset field as
"product: Cloud sync").

Observation (all candidates, not changed): Vega-Lite draws the discrete x labels (Jan..Jun,
Q1..Q4) rotated vertical.
