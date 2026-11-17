# Before / after

- before-v05-sticky-wrapped-growth-dark-460.png (origin/main cb968299) vs after-v05-sticky-long-path-ellipsis-dark-460.png (head 352077d): long path wrapped onto extra lines vs one line per level with ellipsis.
- after-v44-sticky-long-title-zoom-160-cream-900.png: new scenario, no before (does not exist at base): band is one line cut with "...", first section text not covered.

Reproduce: `fnm exec -- npm run visual:render && uv run --no-sync --group docs python test/visual/capture.py --group toolbar-navigation`; PNGs in out/reports/e2e/screenshots/visual/toolbar-navigation/.
