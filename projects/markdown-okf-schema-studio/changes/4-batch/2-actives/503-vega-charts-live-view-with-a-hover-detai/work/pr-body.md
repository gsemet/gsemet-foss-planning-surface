## Summary

A Vega-Lite or Vega chart in the preview was an `img`, which gets no mouse event, so no hover detail could show. Each chart is now a live Vega SVG view. Hovering a Vega-Lite mark shows its fields as key and value rows in a box that follows the page theme, text size and zoom. `"tooltip": null` on a mark turns it off; a full Vega spec shows only the tooltips its marks define. The HTML export keeps a static picture: the drawn inline SVG, with no hover box and no script.

Stacked on the chart text pull request (#520).

## Deliverables

Hover detail on the grouped bar chart, Cream and Dark (pictures taken before the restack onto the current base; the chart code is unchanged since; the pointer is on the first bar):

| Cream | Dark |
| --- | --- |
| ![Hover detail on the grouped bar chart, Cream theme](https://github.com/user-attachments/assets/c8a8acc7-6941-4312-8dc8-94d5f0616b20) | ![Hover detail on the grouped bar chart, Dark theme](https://github.com/user-attachments/assets/8bbc11dd-17ef-4479-87ad-a1ae436013d1) |

```mermaid
flowchart LR
  spec[chart source] --> rt[chartRuntime]
  rt --> draw[drawChart: headless SVG string]
  rt --> mount[mountChart: live svg view in div.myst-vega-view]
  mount --> tip[chartTooltip: div.myst-vega-tooltip on body]
  mount --> cache[chartViewCache: 16 detached views]
```

## Changes

- `vegaView.ts` holds `chartRuntime`, `drawChart` (unchanged result) and `mountChart`; the loader and expression interpreter are shared, so data loading and the security rules are unchanged. `chartConfig` gains `events.bind: "none"`; only the Vega-Lite config gets `mark.tooltip: true`.
- `chartViewCache.ts`: keeps at most 16 detached live views; a view is reused only when detached, so two identical charts each get their own; evicted detached views are finalized.
- `chartTooltip.ts` and `chartTooltipStyles.ts`: one shared box on `body`, rows built as text, positioned through the CSSOM, hidden on scroll, content replacement, redraw and finalize.
- Find skips `.myst-vega-view`; the export rewrites gradient `url(<page>#id)` references to `url(#id)`.
- The theme-switch clip, the showcase scenario, docs, skill row, glossary, changelog and requirements follow the new markup; a real-window `live-chart` scenario is added.

## Impacts

Visible: hover detail on charts in the preview. No change to the exported HTML apart from the chart being inline SVG as before for static content.

## Blast radius

Grade: 2. Charts are drawn through a different renderer and cache; revert restores the image chart.

## Test plan

- [x] New or changed tests (they fail on the previous code)
- [x] Requirements: DIAG-123, DIAG-128, DIAG-009 and StRS DIAG-015 updated, markers in code and tests, `just requirements-update`
- [x] Changelog: one user-facing line under `## Unreleased` in `CHANGELOG.md`
- [x] Local gates: `just preflight` (static stage, Windows) passes at 1f209e1
- [x] Real window: the `live-chart` scenario passes in the heavy run [45706313890](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45706313890) at 1f209e1 (`PASS real-input screenshot: diagrams/r01-live-chart-hover`)
- [x] Review: approved before the restack; the move to 1f209e1 reviewed (one commit, clip changes left out, see Autonomous decisions)
- [x] CI green: static, static-windows, visual, viewer-graph, checks and report pass at 1f209e1 (pull request run)

## Autonomous decisions

- Restacked off the clip changes: this branch no longer edits the advanced renderings tour clip (not in its base) or the export-html clip (its base holds the older clip, which reads no chart). Both edits belong with the clip pull requests that sit above, which must follow the live chart markup; no export-html clip take covers this head.

## Known gaps

- The `integration` job of the heavy run [45706313890](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45706313890) at 1f209e1 failed on its first attempt on a launch timeout of the trusted suite (step `diff-preview-scroll`), not this change; the default branch's own heavy run [45580228461](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/45580228461) failed the same way (at `lifecycle`). Its stress and viewer-graph jobs pass.
- The hover box and the chart's SVG root get their position and size through the CSSOM, which Chromium shows as a `style` attribute; no Content Security Policy violation is raised, which the `live-chart` scenario checks.

## Internal references

- CR-503 (batch-09), after CR-502.

