# Report — release-showcase-capture

Status: **done** (2026-10-28, branch `change-requests/166-release-showcase-capture`, PR [#180](https://github.com/gsemet/markdown-okf-schema-studio/pull/180), head
`1898d971` (rebased on b9bd1d8d), merged as `d956002f`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | "Depot throughput review" fixture (prose, captioned SVG figure, 4-row table, 12-column table breaking out in Auto width, Vega-Lite chart, Mermaid flowchart, conclusion); headless visual scenario (Cream, 1200 px, Auto width, toolbar collapsed, reduced motion); `images/readme/release-showcase.png` (1200x3120) via the README generator `--visual-only`. Test harness only: Vega runtime in headless pages, wait for charts, `widthModeSwitch` scenario field. No product code. | `d956002f` |

## Proof of completion

- One round, reviewer APPROVE (opened the PNG); the Foreman also opened it: nothing clipped, wide
  table out of the column inside the pane, chart and diagram fully drawn, no motion frame.
- Local: `just check` (3118 unit); visual 402/402; README generator `--visual-only` 18 images.
- CI: normal [40734479382](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40734479382) pass on 375b239c; the rebased head was
  merged by the user during the rebase round.
- Picture in the PR from `change-requests/166-release-showcase-capture-assets`.

## Open items

- Mermaid anti-aliasing differs by a few pixels between machines (also `showcase-diagrams-cream.png`);
  no CI byte-compare today.
- Not removed yet: worktree `../markdown-okf-schema-studio-wt-166` and its branch.
