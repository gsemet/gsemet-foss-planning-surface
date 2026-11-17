## Summary

Adds Vega-Lite and Vega charts to the Markdown preview, as in Markdown Preview Enhanced: a fenced
```vega-lite or ```vega block (JSON or YAML) renders as an SVG chart that follows the page theme. Everything runs in
the webview with no external executable and no network. A new palette mode, **Full** (MyST plus extras), carries the
chart insert commands. Charts render in every mode.

## Deliverables

Cream and dark themes (headless Chromium capture; real-window proof comes from the heavy CI job):

![Chart, cream](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/change-requests/149-vega-lite-charts-full-mode-assets/chart-cream.png)
![Chart, dark](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/change-requests/149-vega-lite-charts-full-mode-assets/chart-dark.png)
![Invalid spec shows its error in place](https://raw.githubusercontent.com/gsemet/markdown-okf-schema-studio/change-requests/149-vega-lite-charts-full-mode-assets/chart-error-cream.png)

Bundle sizes (minified, gzip):

| Bundle | Before | After |
| --- | --- | --- |
| vegaPreview.js (new, lazy) | none | 887 863 B, gzip 302 160 B |
| preview.js | 329 603 B, gzip 104 034 B | 331 813 B, gzip 104 732 B |
| extension.js | 4 285 418 B, gzip 822 652 B | 4 290 146 B, gzip 823 689 B |

The chart runtime loads only on pages that contain a chart; Mermaid and PlantUML bundles are unchanged.

## Changes

- Chart runtime (`vega`, `vega-lite`, `vega-interpreter`) in its own lazy bundle; expressions use the CSP-safe interpreter, the page CSP keeps no `unsafe-eval`.
- Data: inline values or a document-relative file resolved through the existing resource policy; remote URLs are refused with a message. CSV/TSV/JSON are parsed on our side because Vega's CSV parser needs `new Function`.
- An invalid spec shows its error in place of the chart; the source is never changed.
- Palette modes become Strict, GFM, MyST and Full; Full adds "Vega-Lite chart" and "Vega chart" (`/chart`, `/vega`).
- Docs: new user guide page on charts, settings and slash-menu pages updated, README section with screenshots.

## Impacts

New dependencies (exact versions in the lock file). Palette mode setting gains a value. Blast radius: 2.

## Test plan

- `just check`: unit 2918, contracts 2, security 67, release tests 45, requirements 0 errors.
- Headless Chromium test under the real page CSP: a Vega-Lite and a Vega chart drawn, 0 CSP violations, 0 console errors.
- Visual groups diagrams and palette-slash: 44 pass; 2 palette-slash scenarios fail identically on the base branch (pre-existing).
- Real-window suites not run locally (screen locked); run the heavy CI job.

### Requirements traceability

| ID | Source | Tests |
| --- | --- | --- |
| DIAG-121..124 (chart rendering, data policy, error, lazy load) | src/core/render/chartData.ts, chartInline.ts, src/page/modules/vegaChart.ts, vegaPreview.ts, chartError.ts | test/core/render/chartData.test.ts, chartRendering.test.ts, test/page/chartCsp.test.ts, test/page/modules/vegaChart.test.ts, chartError.test.ts, test/session/diagReq.chart.requirements.test.ts |
| PALETTE-004 (Full mode chart commands) | src/core/palette/paletteActions.ts, src/page/modules/slashMenu.ts | test/core/palette/paletteActions.test.ts, test/page/modules/chartActions.test.ts, slashMenu.test.ts |
| PALETTE-001, PALETTE-010, LIFE-169, LIFE-170 (four modes) | src/core/configuration/settingsRegistry.ts, src/core/protocol/pageToHost.ts | test/core/configuration/editingConfiguration.test.ts, test/core/protocol/pageToHost.test.ts |

## Autonomous decisions

- Parse CSV/TSV/JSON data files in our code and inline the rows, since Vega's parser would need eval.
- README images come from a probe script (`test/probe/chartShots.ts`), not registered visual scenarios.
- Two lock-file cosmetic differences from npm 11 were normalised (`libc` lines kept).

## Internal references

CR 149 (stacked on CR 148).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
