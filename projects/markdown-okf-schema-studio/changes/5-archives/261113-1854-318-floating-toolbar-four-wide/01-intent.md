# Reorganise the preview's floating toolbar into four columns

Type: feat (UI layout). Filed 2026-11-13 by the Chief of Staff.

## Owner's words

> j'aimerais reorg le menu flottant en 4 icones de large

with an annotated screenshot (`intake/floating-toolbar-annotated.png`), then the owner's table
(`02-answers.md`).

## Scope

The toolbar of `renderPreviewToolbar()` (`src/core/preview/previewToolbar.ts`) goes from a main row
of four plus four rows of three to a 4 × 4 grid, in the order of the table in `02-answers.md`
("mapped to the code"). Same 16 buttons, same behaviour, same collapse (rows 2 to 4 stay in the
group the collapse button hides); only the order and the rows change. The styles, the Tab order,
the tests and the SwRS that describe the rows follow.
