# 169 — Find in preview: late block editor steals focus (HOTFIX) — report

Landed 2026-10-28. PR https://github.com/gsemet/markdown-okf-schema-studio/pull/183, squash
`cad03b4d` on main. Release 1.0.0 blocker.

## Outcome

- Cause: in edit mode a click on a block opens the block editor; its Markdown textarea arrives
  after a host round trip and took focus unconditionally. If Cmd/Ctrl+F was pressed meanwhile, the
  late textarea stole focus from the find field: typed text went into the source (run 40743462032,
  match count timeout) or the edit stayed open and Replace was refused (run 40744401718).
- The Chief of Staff's lead (#181 table menu `z-index: 3`) was excluded: that menu exists only in
  a table-cell editor, which the find test never opens.
- Fix (product): a late block-source textarea no longer takes focus once focus moved to a text
  field outside the editor (`blockEditor.ts`, `blockSourceEditor.ts`, `pageRuntime.ts`); new
  requirement SwRS-MDOKFSTUDIO-BLOCK-255 (proposed); headless unit test failing on old code
  (verified by the Inspector) + normal-path test.
- Fix (test): `findInPreview.test.ts` closes the editor its click opened before the shortcut; state
  dumps on failure; fail-fast `assertReplaceAllowed`. No weakened assertion, no retry.

## Rounds and evidence

- Round 1: test-only fix; Opus Inspector CHANGES REQUESTED (product bug, unit test). Round 2: Opus
  APPROVE. Reviews in `reviews/`.
- Normal CI green: run 40750901896. Heavy #1 run 40752707297 cancelled: integration hung after the
  coexistence check (30 min timeout, before findInPreview); not reproduced. Heavy #2 run
  40757704889 fully green (integration, stress, visual, static).

## Follow-ups (backlog P2, after 1.0.0)

- `real-input-click-then-find-race` — real-window proof of the product fix.
- `find-in-preview-stress-coverage`.
- `table-cell-editor-late-focus`.
- Watch for the post-coexistence integration hang; file an item if it recurs.
