# 168 — Heavy CI regression: the table menu "Delete selected column" is covered by the row handle strip (HOTFIX)

Type: fix · Priority: P1 · Release 1.0.0 blocker · Approved by the user via the Chief of Staff,
2026-10-28 ("finish the CRs, make sure CI passes, focus on 1.0.0"; a release-blocker fix is in scope)
· From `origin/main` b71fac7c, one small PR, not stacked.

## Problem

Heavy CI on main `b71fac7c` (https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40732349085,
integration job) fails in the real-input table structure scenario
(`test/integration/tableStructureReal.ts`, compiled line 98, `pressButton`):
`locator('[data-sphinx-table-operation="Delete selected column"]').click()` times out after 30 s;
on every retry Playwright reports that the row-1 drag handle
(`button[data-okf-row-handle][data-okf-row="1"][data-okf-row-table="3"]`, "Move table row")
intercepts the pointer. Deterministic. 37 real-input scenarios passed before it, including
`scenarioTableToolbar` (fixed by #178). Saved log: `reports/heavy-main-b71fac7c-integration.log`.

Hypotheses (unproven): the table menu now sits over the row handle strip, either since the five-row
toolbar (#167; no heavy run reached this scenario since) or because #178 clears the toolbar first
and the menu lands lower; or the handle strip's z-order is above the menu.

## Decisions (user, via Chief of Staff)

- Fix forward from b71fac7c; no weakened assertion, no `force: true` click, no retry loop.
- Check first whether a real user hits it: geometry of the menu vs the row handles at the
  integration window size, and whether a real pointer press on that button lands on the handle.
  If yes, fix the product (menu above handles in z-order, or placed clear of the strip); if the test
  aims at a spot the product never promised, fix the test's aim and say why.
- Keep green: tableMoves handle strip, TABLE-064 (#178), the five rows, palette/banner reserves,
  Edit figure clearance (#174), motion.
- Before/after screenshot of the table menu in the PR (`-assets` branch).
- Other failures of the same heavy run (visual, stress) that share the cause go into this CR;
  separate failures are reported to the Foreman, not fixed here.
- Requirements traceability as usual. Gate: `just check`, normal CI, heavy CI with integration
  green (stress ignored).
