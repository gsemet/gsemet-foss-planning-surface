Head: 4404b98bee05b7a42e1578db02f31555919be2c6

NOT VERIFIED

Claims, all judged at 4404b98 (worktree clean before and after; clip media under out/ and C:/okfclip503, nothing to restore).

1. Unit and Chromium page tests: `npx tsc -p .` then `node scripts/node-test.mjs unit "out/test/page/**/*.test.js"`
   -> tests 2364, pass 2364, fail 0 (log: work/verifier/unit-page.log). The new hover, tooltip null, bind,
   narrow page, error chart, two identical charts, export gradient and cache tests are in it. PASS.
2. `git grep -n myst-vega-image` at head -> no output. PASS.
3. Clip `theme-switch take` (CLIP_PORT=9503, CLIP_SCRATCH=C:/okfclip503, `--vsix` of `just package` at head,
   because the default setup installs the marketplace 1.12.1 and fails on the old image markup):
   `filmed 10.94 s ... done`, setup and verify pass. PASS (log: clip-theme-switch.log).
4. Clip `advanced-renderings-tour take`, same env: `filmed 16.05 s ... done`. PASS (log: clip-advanced-renderings-tour.log).
5. Clip `export-html take`, same env: FAILED at verify,
   `Error: the exported file holds a chart hover box` (scenario.mjs:531, `/myst-vega-tooltip/iu.test(html)`).
   Cause: the exported file holds the hover box CSS rules (`.myst-vega-tooltip {`, `.myst-vega-tooltip[hidden] {`,
   `.myst-vega-tooltip-key`, ... found with grep in C:/okfclip503/export-html/workspace/platform-report.html) and no
   element (`class="myst-vega-tooltip` count 0, `role="tooltip"` count 0). The scenario's check is too broad.
   FAIL: the spec's claim "export-html take passes setup and verify" is false at this head. (log: clip-export-html.log)
6. PR description: images (cream, dark hover shots) opened: legible, show the hover box with Quarter, Revenue (k$),
   Product, Product line rows, themed; no username or home folder. PASS.
7. PR description Known gaps: the third bullet says the clip takes were "not run by the change", which is true of
   the change but the export-html take now fails; the gap must state it (or the check be fixed). FAIL until then.
8. Review box: log note "r3 approved at 3df0c86..., committed as 4404b98..." matches the box. PASS.
9. Heavy run and CI: read from the Driver's note only (green PR CI, live-chart PASS, integration timeout also on main); not re-run here.
