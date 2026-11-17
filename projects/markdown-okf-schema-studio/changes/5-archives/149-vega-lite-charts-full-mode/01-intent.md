# Vega-Lite (and Vega) charts, and a new "Full" palette mode

Type: feat · Priority: P1 · Requested 2026-10-27 by the user

## Intent (user, translated)

"I would very much like Vega-Lite charts, as Markdown Preview Enhanced has them
(<https://shd101wyy.github.io/markdown-preview-enhanced/#/diagrams?id=vega-and-vega-lite>), if it
can all be JavaScript inside the extension, with no external executable. Same syntax:
```` ```vega-lite ````. Put it in a new mode **Full**, which is MyST (so GFM included) plus other
extensions we will define together. Add Vega too if it costs the same JavaScript size."

## Size check (main session, 2026-10-27)

| Package | Version | Minified | Gzip |
| --- | --- | --- | --- |
| `vega` (runtime, parser, renderer) | 6.4.0 | 521 KB | 180 KB |
| `vega-lite` (compiler Vega-Lite → Vega) | 6.5.0 | 258 KB | 82 KB |
| `vega-interpreter` (CSP-safe expressions) | 2.3.2 | 6 KB | 2 KB |

Vega-Lite only *compiles* to a Vega spec; drawing it needs the Vega runtime anyway. **Supporting
```` ```vega ```` as well costs nothing extra.** Total ≈ 785 KB minified (≈ 265 KB gzip), loaded
only when a page contains a chart (same lazy loading as Mermaid, whose runtime is about 5 MB).

## Expected

- ```` ```vega-lite ```` and ```` ```vega ```` fenced blocks (JSON spec; YAML accepted if Markdown
  Preview Enhanced accepts it) render as charts in the preview, SVG renderer, following the theme
  (cream, white, dark, VS Code theme: background, text, axis and mark colours from the page
  palette).
- Everything runs in the webview: no external executable, no network. **CSP:** keep the page
  CSP without `unsafe-eval`; use `vega-interpreter` (`ast: true`) for expressions. Data: inline
  `values` only, plus `url` relative to the document resolved through the existing resource policy
  (workspace root, Restricted Mode rules, CR 133's rules); remote URLs are refused with a message
  (`connect-src 'none'` stays).
- An invalid spec shows the error message in place of the chart (like Mermaid errors), the source
  is never changed.
- Lazy loading: the chart runtime is loaded only on pages that contain a chart; cached diagrams
  survive content patches like Mermaid ones.
- **Palette mode "Full"**: the modes become Strict, GFM, MyST and **Full**. Full is MyST plus the
  extensions we will define with the user later; its first extension is the chart commands:
  "Vega-Lite chart" (inserts a small bar-chart template) and "Vega chart", in the palette and the
  slash menu (`/chart`, `/vega`). Charts **render in every mode** (a fence is harmless elsewhere);
  only the insert commands are Full-only. Settings, docs and SwRS updated.
- Docs: a user guide page with examples; a README line and a screenshot of a chart in two themes.
- Dependencies: adding `vega`, `vega-lite`, `vega-interpreter` (exact versions above, or the
  latest patch) is **allowed by this CR**; lock file committed. Bundle sizes before/after in the PR.

## Proof

Unit tests (spec parsing, error path, resource policy for `url`), a webview test rendering a
Vega-Lite and a Vega chart under the real CSP (no eval violation in the console), real-window
screenshots (cream + dark), bundle size report.
