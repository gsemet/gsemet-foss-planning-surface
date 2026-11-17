# Report — myst-tab-item-edit-source

Status: **done** (2026-10-28, branch `fix/tab-item-edit-source`,
PR [#166](https://github.com/gsemet/markdown-okf-schema-studio/pull/166), rebase-merged to main as `d100ea3d`; main head `67ccf8c9`).

## Delivered

| Task | Change | Commit |
| --- | --- | --- |
| T1 | A click on the shown panel of a `{tab-item}` in edit mode opens the whole tab item, not the inner paragraph; tables, code, cards, grids and nested tab sets inside an item are no blocks of their own; comments, TODOs and THREADs keep their lines. SwRS-MDOKFSTUDIO-MYST-098 text unchanged (implementation fixed). | `d100ea3d` |

## Proof of completion

- Tests: test/core/render/cardsTabs.test.ts, visual scenarios `myst/v44` (light) and `v45` (dark),
  real window test/integration/mystBlocksWindow.ts.
- Local gate (stack top, all three CRs): `just check` green (3095 + 69 tests, 0 fail),
  `okfreq validate --check-links` 1059 requirements, 0 errors.
- CI: pre-stack normal run [40692673108](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40692673108) green; heavy [40693008426](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40693008426)
  stopped at the findInPreview regression of main (fixed by [#172](https://github.com/gsemet/markdown-okf-schema-studio/pull/172)). Main after merge:
  [40700143893](https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40700143893).
- Screenshots: branch `fix/tab-item-edit-source-assets` (commit `86248d7b`).
- Rounds: 3/3 (reviews in [reviews/](work/reviews)).
- Landed together with CRs [156](../156-empty-document-keyboard-start/delivery.md) and
  [157](../157-structural-keyboard-navigation/delivery.md): the user merged #170 into #171, #171 into
  #166, then #166 into main.

## Open items

- None for this CR. Keyboard follow-ups of 156/157:
  [02-backlog/P3/keyboard-nav-followups](../../2-backlog/P3/keyboard-nav-followups/01-intent.md).
