# T1 — B5: visual scenarios for extension states (gate B)

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-029 (branch `test/visual-extension-states` from origin/main). Work ONLY there;
`node_modules`/`.venv` are symlinks to the main checkout: never delete or stage them. Read
`00-request.md`, `rules.md`, and the plan /Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/archives/021-feature-session-007-020/p9-e2e/plan.md sections 0, 3, 6 "B4" (harness options) and
"B5" (the table of scenarios). The B4 harness (per-scenario render options in the page-cache key) is
already on main: check it before adding options.

## Change

Add the B5 scenarios of the plan table to `test/visual/scenarios.ts` (+ fixtures and harness
options as needed), EXCEPT the high-contrast row (decision 2):
- theme-zoom: forced-dark-handbook light 900; zoom-70 light 900, zoom-200 light 900, zoom-150 light
  460 (text and column scale together, no horizontal scroll).
- trust-security: read-only-page dark 900, light 460, read-only-no-hover-outline (assertion only).
- review-annotations: incoming-bars light 900, dark 900, incoming-diff-off (A); review-thread-open,
  review-thread-resolved, orphaned-list light 900, comment-chips-hidden (A). The change bar was just
  reworked on main (PR #19, one column at the left margin, square ends): lock that geometry.
- toolbar-navigation: back-enabled-after-anchor, mark-editor-selection light 900.
- block-editing: block-selection light 900. palette-slash: slash-gfm light 360.
- layout-width: max-width-setting light 2000.
Ids: `<group>/vNN-<slug>-<theme>-<width>`, NN = next free number in each group ON CURRENT MAIN
(the plan's numbers may be stale). Every scenario has group, description and `locks` metadata like
its neighbours, and content assertions for what the lock claims. Mock-host messages for incoming
changes and review threads go through the harness, never by patching product code.
Two commits worth of work, kept reviewable: (a) theme/zoom/layout/toolbar/block/palette/trust rows,
(b) review-annotations rows. You do not commit; just keep the report split in (a) and (b).
A scenario that reveals a product bug: mark it `knownIssue` with a new id, describe it in the
report (it becomes a backlog item); do not fix the product in this CR.

## Tests

- New scenarios must fail before their harness/fixture support exists (show it for one per group).
- Existing scenarios produce byte-identical pages and PNGs (diff before/after any harness change).
- Unit tests stay green (invariants test: ids, groups, locks, no duplicate PNG).

## Docs

CHANGELOG only if a user-visible change happens (none expected). Update the inventory if the
tooling is still valid (`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/archives/021-feature-session-007-020/p9-e2e/tools/build_inventory.mjs`), otherwise say so in the report.

## Gates (foreground, windowless only)

`npx tsc -p .`, `npm run test:unit`, `just check`, `just visual` (full; report counts: scenarios,
PNGs, assertion-only). No integration/e2e/preflight locally.

## Screenshots for the PR

A small set from `just visual`: incoming-bars light, review-thread-open, zoom-200, read-only-page
dark, slash-gfm 360. List their paths in the report.

## Report

`/Users/az02065/Projects/DevTools/markdown-okf-schema-studio/.agents/changes/requests/029-e2e-b5-extension-states/reports/T1-r<round>.md`.
