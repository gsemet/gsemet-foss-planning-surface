# Round 2: Coder report (CR 199)

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-199 (uncommitted on top of 128e436e).

## Symptom
Heavy run 40810582100, integration job: `ENOENT ... moved.comments.json` at
test/integration/commentAnchors.test.ts:149, right after `waitFor("the sidecar to move", existsSync)` had passed.

## Root cause: a product bug (option a)
On rename, `CommentsController.moveSidecars` moves the sidecar (`rename`, overwrite false), then rewrites
its `document` field through the comment store. The store writes a temporary file and renames it onto the
sidecar (`writeAtomically`, SwRS-REVIEW-054: "readers never see a partial file"). In the VS Code host, that
rename used `vscode.workspace.fs.rename(..., { overwrite: true })`. VS Code's FileService.doMoveCopy
**deletes an existing target first** (`if (exists && overwrite) await this.del(target)`), then renames
(checked in the shipped VS Code 1.143.1 workbench bundle). So every comment write left the sidecar missing for
a short time. The test hit that window between its two waits. The same window also affects users: watchers,
Git, and other tools could see a delete and then a create.

## Fix
- src/host-vscode/vscodeHost.ts: `rename` with `overwrite: true` now uses Node's `fs.rename`, which replaces
  the target in one step (rename(2) / MoveFileEx REPLACE_EXISTING). Renames that must not replace still go
  through `workspace.fs.rename` (overwrite false). The only caller with overwrite true is the comment store's
  temporary-file rename. The host already uses Node for `isSymbolicLink`/`realpath`, and the paths are always
  `Uri.file` (local disk).
- src/host-api/fileSystem.ts: the port contract now says that a rename with `overwrite` replaces `to` in one
  step.
- test/integration/commentAnchors.test.ts: unchanged. The race came from the product, so every assertion stays
  strict. I added no tolerant reader: it would only hide the bug.

## Tests (reproduce first)
- test/host/fakeVscode.ts: the fake `workspace.fs` gains `rename`, which works like VS Code's FileService
  (deletes an existing target when `overwrite` is set and records it in `controls.targetsDeletedByRename`;
  refuses without `overwrite`).
- test/host-vscode/fileRename.test.ts (new, 3 tests): an overwriting rename never deletes the target; a
  non-overwriting rename refuses an existing target and moves onto a free one; a comment store rewrite through
  the VS Code host never leaves the sidecar missing and leaves no temporary file.
  Before the fix, tests 1 and 3 failed ("the target is never missing during the rename", "the comments file is
  replaced, not deleted then written"). After the fix, all 3 pass.
- requirements/.../SwRS-MDOKFSTUDIO-REVIEW-054.md: generated coverage lines only (`just requirements-update`):
  + src/host-vscode/vscodeHost.ts, + test/host-vscode/fileRename.test.ts. This is a SwRS, not a locked StRS.

## Gates
- `just check`: exit 0 (unit 3191 pass / 0 fail, security 69 pass, pytest 80 passed, requirements: 1067, 0 errors,
  0 indexes / 0 files would change). Log: /private/tmp/claude-502/cr199-driver/round2-check.log
- I ran no local real-window tests. Heavy CI is the proof for the integration scenario.

## Files changed
- src/host-vscode/vscodeHost.ts
- src/host-api/fileSystem.ts
- test/host/fakeVscode.ts
- test/host-vscode/fileRename.test.ts (new)
- requirements/tiers/swrs/review-annotations/SwRS-MDOKFSTUDIO-REVIEW-054.md (generated)
