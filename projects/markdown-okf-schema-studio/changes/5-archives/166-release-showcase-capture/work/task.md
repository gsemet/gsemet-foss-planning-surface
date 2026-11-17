# Task T1 — Long showcase capture for the 1.0.0 release notes

Implement `00-request.md` in `../markdown-okf-schema-studio-wt-166` on branch
`change-requests/166-release-showcase-capture` (from `origin/main` 2577039e, own `npm ci`,
`playwright install chromium`). Part of release 1.0.0 (CR 163). No product code.

## Definition of done

- New fixture (real prose, captioned local SVG figure, small table, 10+ column table breaking out in
  Auto width, Vega-Lite chart with inline data, Mermaid diagram, conclusion).
- New headless visual scenario: full page, Cream, ~1200 px, Auto width, toolbar collapsed, static
  (no motion frame; CR 162's load hint is not on main, but the capture must wait for a settled
  state anyway).
- README picture `images/readme/release-showcase.png` via the README generator `--visual-only`
  (added by #177); at most one README line near the top. LFS as today.
- Reviewer opens the PNG: nothing clipped, wide table leaves the column, chart and diagram drawn.

## Gates

- `just check`; the visual scenario passes (`npm run test:visual` or its focused form); the README
  generator `--visual-only` (and `--check` if it exists). Normal CI green.
