# Before and after: line marker precision (CR-457)

Before: eb3b6ecc (origin/main, the base, 1.11.0 plus later fixes), detached worktree. Only the new visual fixture
`94-line-marker-precision.md`, `lineMarkerScenarios.ts` and `scenarioIds.ts` of the head were copied in so the same
page and scenarios run on the old renderer and page code (the old code fails the new assertions, as expected).
After: 3778f00a996a2f0c753492c368bef3e447c44973.

Same fixture, same 900 px pane, same reveal request (`previewRevealLine`), each in light and dark.
All images show made-up content only (no path, no username).

| Pair | Reveal line | Before | After |
| --- | --- | --- | --- |
| Table row, top level | 15 (`beta`) | before-table-row-{light,dark}.png: band on the table top (header row) | after-table-row-{light,dark}.png: band and arrow on the `beta` row |
| Table row in a quote | 20 (`second`) | before-table-row-quote-{light,dark}.png: band on the top of the quote block | after-table-row-quote-{light,dark}.png: band on the `second` row |
| Hidden tab, wrapped paragraph | 36 | before-hidden-tab-paragraph-{light,dark}.png: tab set top, tab "First" still shown, text not visible | after-hidden-tab-paragraph-{light,dark}.png: tab "Second" shown, band on the third source line (wrapped line) |
| Hidden tab, code line | 39 | before-hidden-tab-code-{light,dark}.png: same as above | after-hidden-tab-code-{light,dark}.png: tab shown, band on `second_tab_code` line |
| Front matter row | 4 (`owner`) | before-frontmatter-row-{light,dark}.png: band on the "Frontmatter properties" title row | after-frontmatter-row-{light,dark}.png: band on the `owner` row |

Reproduce (in each worktree): `npm run visual:render`, then rewrite `out/reports/visual/manifest.json` to the 10
scenarios `lifecycle-sync/ev-*` (one per case and theme, a clone of v14, v15, v17, v18, v20 with the reveal line and
theme page changed; script kept outside the repository), then
`python test/visual/capture.py --workers 2 --group lifecycle-sync`. Screenshots are in
`out/reports/e2e/screenshots/visual/lifecycle-sync/`. After: 10 passed. Before: 10 failed on the new assertions.
