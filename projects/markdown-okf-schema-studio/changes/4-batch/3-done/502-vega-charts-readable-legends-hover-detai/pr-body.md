## Summary

Chart text (legends, axes, titles) was too small in the preview, legends first, because Vega's defaults (10 px labels) ignore the page text size. Chart text now scales from the page body text size, so it also follows the Markdown font-size setting and the preview zoom, in Cream, light and dark. The preview no longer shows the collapsed "Chart source" section under a chart (the source is the document itself); the HTML export, which has no editor, keeps it. The chart is still a picture: the live view with a hover detail comes in a following change.

## Deliverables

Chart text sizes, as a multiple of the body text size (14 px body shown), shared by Vega-Lite and Vega:

| Item | Before | After |
| --- | --- | --- |
| Legend label | 10 | 13 (0.93x) |
| Axis label | 10 | 11.9 (0.85x) |
| Legend and axis titles | 11 | 13.3, bold |
| Chart title | 13 | 16.1, bold |
| Subtitle | 11, muted colour | 12.6, label colour |
| Discrete x labels | may rotate | horizontal |

- The refreshed `charts-cream.png` and `charts-dark.png` in the README show larger legend and axis text; filled swatches (bars) are not bloated, so `symbolStrokeWidth` stays. **UNVERIFIED:** the longer, thicker line legend swatches (neither README shot has a line chart with a legend).
- A spec's own `config` and its own mark or axis properties still win over these defaults.
- Chart source: hidden by a preview rule, shown again (closed) by the export sheet; the find bar skips it so hidden text is never a match.
- The chart error message is now "Unable to render the chart." followed by its reason.

## Blast radius

Grade: 1. It touches chart config values, two CSS rules and a message; a plain revert restores the previous look.

## Autonomous decisions

- `symbolStrokeWidth: 2.5` kept, since the new screenshots show no bloated filled swatches (the specification allowed dropping it).
- The export check builds its snapshot from the page content by hand and the zoom is set through the zoom CSS variable on the root, because the chart test page has no toolbar.

## Known gaps

- The find-bar check is a unit test on the find index (the chart test page has no find bar), not a Chromium test.
- **UNVERIFIED:** longer, thicker swatches of line legends are not shown by a screenshot (the README charts have no line legend); the keys are set and tested in the config.

<details>
<summary>Details</summary>

## Changes

- `chartConfig` (`src/page/modules/vegaChart.ts`) adds legend, axis, title and header size keys derived from the body font size; `chartThemeFrom` takes the body font size (fallback 13) and `renderCharts` passes it, so a font-size or zoom change redraws through the existing key and observer.
- `contentBlockStyles.ts` hides `details.myst-vega-source`; `exportStyles.ts` shows it again; `findIndex.ts` skips it; `chartError.ts` message shortened.
- Requirements DIAG-121, DIAG-123 and StRS DIAG-015 updated, with a log entry; `docs/user/charts.md`, the writing skill's Charts row and the changelog follow.

## Human decisions

- Sizes are relative to the page text size and live in the shared config used by both Vega-Lite and Vega.
- The preview hides the Chart source section; the HTML export keeps it, closed.
- The error message no longer points to a source below it.
- Discrete x labels are horizontal and the subtitle takes the label colour.
- The live view and hover detail are a separate, later change.

## Impacts

Charts read at paragraph size and scale with font size and zoom; no Chart source under charts in the preview.

## Test plan

- [x] New or changed tests (they fail on the previous code): config table at 14 and 18 px, fallback, own-config precedence, exact error message, Chromium sizes, horizontal labels, zoom, hidden source, export, find skip
- [x] Requirements: SwRS DIAG-121 and DIAG-123 and StRS DIAG-015 updated, `@implements_req` and `@tests_req` markers placed, `just requirements-update` run
- [x] Changelog: one user-facing line under `## Unreleased` (PR number filled once the PR exists)
- [x] Local gates at `756d856`: `just preflight` (static stage on Windows) pass; the later commit only fills the changelog PR number
- [x] Evidence: README shots re-taken at `756d856`
- [x] Review: approved at `3df0c86`
- [x] Verified at `3df0c86`
- [x] CI green at `3df0c86`: static, static-windows, visual, viewer-graph, checks, report pass

## Internal references

- CR-502 vega-charts-readable-legends

</details>
