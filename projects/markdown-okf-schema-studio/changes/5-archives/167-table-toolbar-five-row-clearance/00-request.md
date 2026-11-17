# 167 — Heavy CI regression: table toolbar reveal moves the selected cell (five-row toolbar) (HOTFIX)

Type: fix · Priority: P1 · Release 1.0.0 blocker · Source: Foreman, from the 1.0.0 proof run,
2026-10-28 · From fresh `origin/main`, one small PR, not stacked.

## Problem

Heavy CI on main `2577039e` (https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40728621051,
integration job) fails in the real-input suite, `scenarioTableToolbar`
(`test/integration/realInput/editorWidgets.ts`, compiled line 724):

    AssertionError: the selected cell moved 105.484375 px; toolbar clearance
    {"controlsBottom":178,"menuHeight":118.28125,"menuTop":141.96875,"readingOffset":81.8,
     "scrollY":32,"maxScroll":360}

`controlsBottom` 178 = the five-row floating toolbar (12 + 166 px, PR #167). The table toolbar
reveal now scrolls the page to clear the taller toolbar, and the selected cell moves by 105 px.
Everything before it passed in that run: the trusted suite (editToolbarCover, checkboxToggle) and
real-input scenarios up to `scenarioShortcuts` and `scenarioPreviewKeepsMarkdown`. Saved log:
`reports/heavy-main-2577039e-integration.log` (failure near lines 1520–1545).

## Decisions

- Fix forward; keep the five-row toolbar and the motion (PR #175, now on main `f39a0aa5`).
- Diagnose first: what does the requirement behind `scenarioTableToolbar` promise (the selected cell
  stays put when the table menu opens; the menu clears the floating toolbar)? With
  `maxScroll` 360 and the menu needing room below a 178 px toolbar, decide whether the product
  should place the menu differently (e.g. below the cell, or beside the toolbar) instead of
  scrolling, or whether the test's tolerance/geometry no longer matches a promise the product never
  made. Never weaken an assertion's intent; no retry loop.
- Keep green: tableMoves handle strip, palette and banner reserves, Edit figure clearance (#174),
  360 px visual checks, motion (reduced motion respected).
- Requirements traceability as usual. Gate: `just check`, normal CI, heavy CI with integration
  green (stress ignored). If a later real-input scenario then fails, report it at once.
