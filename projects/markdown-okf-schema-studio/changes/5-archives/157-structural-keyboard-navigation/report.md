# Report — structural-keyboard-navigation

Status: **done** (2026-10-28, branch `change-requests/157-structural-keyboard-navigation`,
PR [#170](https://github.com/gsemet/markdown-okf-schema-studio/pull/170) merged into `change-requests/156-empty-document-keyboard-start`, landed on
main with PR [#166](https://github.com/gsemet/markdown-okf-schema-studio/pull/166) as `67ccf8c9`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | Right goes one level down (table to first cell, admonition/card/tab to first inner block, page to first block), Left and Escape go up; arrows walk table cells without wrapping; Enter opens the cell editor; selected cell outlined and announced. New SwRS-MDOKFSTUDIO-BLOCK-254 (`proposed`, renumbered from BLOCK-253 to avoid the clash with CR 156; squashed to one commit at restack). | `67ccf8c9` |

## Proof of completion

- Tests: test/page/modules/structuralCursor.test.ts, test/page/runtimeStructuralNavigation.test.ts,
  visual scenarios `block-editing/v20` (light) and `v21` (dark), real-window step in
  test/integration/realInput/blockKeys.ts (not run locally).
- Local gate at the stack top (`886bf47f`, same tree as main `67ccf8c9`): `just check` green
  (3095 + 69 tests), `okfreq validate --check-links` 1059 requirements, 0 errors; BLOCK-253 and
  BLOCK-254 unique; visual scenario count 400.
- CI: last pre-stack normal run [40694098886](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40694098886) green; heavy on the stack top
  [40700084682](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40700084682) (dispatched before the merge). Main after merge:
  [40700143893](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40700143893).
- Screenshots: branch `change-requests/157-structural-keyboard-navigation-assets`.
- Rounds: 2/3.

## Open items

- Non-blocking review notes:
  [02-backlog/P3/keyboard-nav-followups](../../2-backlog/P3/keyboard-nav-followups/01-intent.md).
