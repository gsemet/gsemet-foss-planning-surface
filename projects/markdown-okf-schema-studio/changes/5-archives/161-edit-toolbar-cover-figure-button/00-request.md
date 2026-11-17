# 161 — Heavy CI regression: the five-row toolbar covers the figure "Edit figure" button (HOTFIX)

Type: fix · Priority: P1 · Source: Chief of Staff relaying the user, 2026-10-28 · From fresh
`origin/main`, one small separate PR, not stacked (runs in parallel with CR 160 and CR 162).

## Problem

Heavy CI integration fails on `main` d48739d7 (PR #167, five-row toolbar, 102 x 166 px) in
`test/integration/editToolbarCover.test.ts` (compiled line 224, step "(b) The figure form: hover
the figure, Edit figure"): `locator('[data-sphinx-figure-edit]').click()` times out after 30 s;
Playwright reports, on every retry, that the "Fold all sections" button (row 5 of the toolbar)
intercepts the pointer. Deterministic (≈60 retries), so not a flake.

Evidence: heavy run https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40716533723
(job 122915663443, head ff9f9c1e = merged d48739d7). The previous heavy run on the four-row head
(https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40700884217) passed integration.

## Decisions

- Fix forward from main; no revert of the five-row layout (user decision in #167).
- Diagnose first: product (the floating toolbar must not cover block edit controls the user needs:
  check what `editToolbarCover` and its SwRS promise) or test aim. If the product promise holds,
  fix the product; if the test aims at a spot the product never promised to keep clear, fix the
  test's pointer path and say why. No retry loop, no weakened assertion, no `force: true` click.
- Keep green: tableMoves handle strip, banner and palette reserves, 360 px visual checks.
- Requirements traceability as usual (`--lifecycle proposed` for new IDs, log entry).
- Gate: `just check`, normal CI green, then heavy CI with integration green (stress ignored).
