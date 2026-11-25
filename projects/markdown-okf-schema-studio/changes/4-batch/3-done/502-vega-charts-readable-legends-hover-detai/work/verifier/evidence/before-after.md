# Before and after (CR-502)

Before: base chantier/batch-09/cr-500-clip-export-a-long-report-page-same-rend (images/readme at that branch, LFS smudged). After: 3df0c86187ed0367b2fcff44529cc5279cb85f37.
Reproduce: `node out/test/probe/chartShots.js <folder>` after `just compile`.

- before-charts-cream.png / after-charts-cream.png: README Charts shot, Cream. After: bigger title, horizontal labels, no Chart source, a third grouped chart with a legend.
- before-charts-dark.png / after-charts-dark.png: same, Dark.

Both images show no username or home path. The after shots hold no chart with a line legend, so "line legend swatches longer and thicker" is not visible in them.
