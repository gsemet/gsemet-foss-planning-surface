# Aligned images, figures and tables no longer turn off the toolbar float for the whole page

Type: fix · Priority: P3 · Filed 2026-10-31 from the narrow-toolbar fix (SwRS-MDOKFSTUDIO-LAYOUT-043, known issue 2)

## Currently

The preview keeps the first lines of text clear of the floating toolbar with an invisible right
float at the top of the column, and moves boxes (tables, figures, code, notes) below the toolbar's
reach. In a document with any aligned image, figure or table (MyST `:align:` or raw `align=`), the
whole page keeps the old layout: no float, no box moved, so text can run under the toolbar again.

## Expected

A precise and fast CSS rule: only the blocks that follow an aligned float are exempt from the box
`clear: right` (so they do not clear a right-aligned figure), and the toolbar float stays on for the
rest of the page.

## Why it was not done

The precise variant (`:not(<aligned float> ~ *)` together with `:has()`) made the huge-document
visual scenario rendering-core v20 time out in 2 of 2 runs, so the fix shipped with the page-wide
exception. Look for a selector or runtime flag (e.g. a class set once by the runtime on blocks after
an aligned float) that does not cost a `:has()` match per block.

Proof: v20 within its usual time; a scenario with a right-aligned figure lower in the page and text
clear of the toolbar at 393 px; aligned-figure scenarios myst v17-v19 unchanged.

## Also

The page-wide "aligned" detector also matches `table.align-left|right` and `figure > img.align-*`,
which do not float (`src/core/directives/figure.ts`), so those pages lose the toolbar float for
nothing. The heading clear rule (`contentBlockStyles.ts`, page-wide `:has(<aligned float>)`) should
be revisited with the same precise rule.
