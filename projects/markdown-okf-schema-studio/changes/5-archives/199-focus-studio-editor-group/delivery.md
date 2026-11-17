# 199 — Slash-menu undo race and focus dump before cleanup (merged)

- PR: https://github.com/gsemet/markdown-okf-schema-studio/pull/221 (replaces #219, base #220), merged 2026-10-29T06:46Z.
- Finding: the request's diagnosis (empty first editor group steals focus) did not hold; the dump
  was read after cleanup. No "focus the Studio group" helper was needed.
- Delivered:
  - harness uses `waitForActiveSourceEditor` instead of `focusFirstEditorGroup`
    (including `checkboxToggle.test.ts`);
  - `undoOneStep` / `undoUntil` wait for each undo before the next key (likely cause of the
    slash-menu flake, inferred);
  - focus dump read at the failing step, before cleanup;
  - ALERT-PICK-PROBE runs once in integration, not in stress;
  - product fix: overwriting renames in `src/host-vscode/vscodeHost.ts` use Node's single-step
    `fs.rename`, so the comments file no longer briefly disappears on save
    (`test/host-vscode/fileRename.test.ts`).
- CI: heavy runs https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40813565971 and https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40813568599 (pre-rebase) and
  https://github.com/gsemet/markdown-okf-schema-studio/actions/runs/40828891957 (v2 head) all green. Inspector APPROVE rounds 1, 2 and v2 range-diff.
