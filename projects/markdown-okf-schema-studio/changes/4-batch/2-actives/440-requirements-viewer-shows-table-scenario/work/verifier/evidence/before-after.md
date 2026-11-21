# Before and after, CR-440

Before: a18bcac12a3fe47cf16f4f5455e6d1cde096d4cb (base, detached worktree, removed at the end).
After: 8d99cd1e393fac6a7e978f442c1af80b1e5831e9 (pushed head).

Reproduce: `just requirements-report`, then `fnm exec -- npm run site`, in each tree; then
`node work/verifier/shoot.cjs <worktree>/out/site <outDir> <tag>` (Playwright, Chromium, desktop 1100 px).
Captures show page content only, no path, no username (looked at each one).

| Pair | Before | After | Shows |
|---|---|---|---|
| BLOCK-130, first card (table Input/Outcome, 4 rows) | before-block130-first-card.png | after-block130-first-card.png | before: three empty columns GIVEN/WHEN/THEN; after: the table, no Given/When/Then |
| BLOCK-130, card "The move chord in the text box ..." | before-block130-chord-card.png | after-block130-chord-card.png | after: note paragraph above a 2-row table |
| BLOCK-130, card "A refused keyboard move can be retried" | before-block130-retry-card.png | after-block130-retry-card.png | Given/When/Then columns, same in both |
| GFM-021, first card | before-gfm021-first-card.png | after-gfm021-first-card.png | list card, same in both |
| BLOCK-130 at 390 px | before-block130-phone.png | after-block130-phone.png | tables fit, page width 390 = viewport |

Measured (shoot-before.log, shoot-after.log): on BLOCK-130, 6 of 7 cards were empty GWT grids before, 0 after.

Notes, not guesses:
- SwRS-MDOKFSTUDIO-GFM-021 is not list-only: its cards 1-3 are list scenarios and are byte-identical
  in markup before and after (gfm021-cards-*.log, same length and gwt count); its cards 4-8 are table
  scenarios and now show a table instead of an empty grid. The spec's step 5 wording is off, the behaviour is right.
- Phone width: no page of the bundle has a table wider than its card (scan-phone-head.log: 0 of 409 pages with an
  inner-scrolling table wrapper). The scroll was proved with a probe that widens one cell at 390 px on the head
  build (probe-wide.log): the `table` (display block, overflow-x auto from the site's own rule) has scrollWidth 1721
  for clientWidth 340 and scrolls (scrollLeft 300); the document stays 390 wide. 13 pages are wider than 390 px
  both before and after, the same 13 (scan2-base.log, scan2-head.log), 10 of them before any card is opened: a
  page-level cause that predates this change, not caused by it.
