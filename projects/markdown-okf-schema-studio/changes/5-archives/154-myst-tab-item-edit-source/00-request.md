# 154 — Clicking inside a MyST tab panel edits the whole tab item

Type: fix · Priority: P2 · From backlog: `02-backlog/P2/myst-tab-item-edit-source` (promoted 2026-10-28)

## Intent

See [01-intent.md](01-intent.md). Already coded outside the factory: PR
https://github.com/gsemet/markdown-okf-schema-studio/pull/166, branch `fix/tab-item-edit-source`
(keep the name), worktree `../markdown-okf-schema-studio-wt-148`.

## Decisions (user, 2026-10-28)

- Bottom of the new stack. Do not rename the branch.
- Before/after screenshots (light and dark) on branch `fix/tab-item-edit-source-assets`; the before
  shot reproduces the bug (click in a tab panel opens an editor on one inner block only).
- Body rewritten for an external reader: the bug; the fix (`noSourceLine` flag in
  `mystGridToctree.ts` and `mystNormalize.ts`, so blocks inside a tab panel stay unmapped and a click
  edits the whole tab item); a small sketch; the test.
- Normal CI green + heavy CI dispatched. `tableMoves` may stay red until #167 lands: report it.
- When #166 merges: `report.md`, move to `04-archives/`.
