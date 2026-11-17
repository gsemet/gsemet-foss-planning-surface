# README diagram crop cuts the bottom of the fleet-loop figure

Type: docs · Priority: P3 · Filed 2026-10-31 from the review of the taller demo capture

## Today

`test/shared/captureRegistry.ts:174` crops `lifecycle-sync/r08-edit-mode-remembered` into the README image
`myst-diagrams-and-figure.png` with the box [790,460,1315,860]. Since the narrow-toolbar fix, the boxes start about 85 px
lower, and the SVG figure ends near y=975. The next README regeneration will cut off the bottom of the figure.

## Expected

The capture is now 1400x1040, so move the crop bottom to about 1000 and check the regenerated README image.
