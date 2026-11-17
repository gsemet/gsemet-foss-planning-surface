# Round 2: Inspector review (CR 199)

Worktree: /Users/az02065/Projects/DevTools/markdown-okf-schema-studio-wt-199 (uncommitted on top of 128e436e).

## Verdict: APPROVE

## Root cause: verified

1. **The failure matches the explanation.** The compiled `commentAnchors.test.js:170` is the second `waitFor`
   ("the document name"). Its predicate calls `readFileSync` without a guard, so an ENOENT there
   ends the test at once. The first `waitFor` had already seen `moved.comments.json`. The file was
   there, then missing, then there again. A delete-then-create write explains this.
2. **VS Code's behaviour is confirmed in the shipped code** (VS Code 1.143.1,
   `/Applications/Visual Studio Code.app`):
   - `extensionHostProcess.js`: `workspace.fs.rename` has no local shortcut (unlike `writeFile` and
     `delete`). It always calls `_proxy.$rename(...)`, which reaches the main-thread FileService.
   - `workbench.desktop.main.js`, `doMoveCopy`: `if(c&&!l&&a&&await this.del(n,{recursive:!0}), ...,
     e===i ? await e.rename(t,n,{overwrite:a}) ...`. If the target exists and `overwrite` is set,
     VS Code deletes the target first and renames afterwards. The coder's claim is correct.
3. The path that fails is `moveSidecars`. It does `rename(old, new, {overwrite:false})`, then
   `store.update(..., {renameDocument:true})`, then `writeAtomically`, then
   `rename(tmp, sidecar, {overwrite:true})`. That last rename deletes the sidecar, which opens the
   window where the file is missing.

## Fix in `src/host-vscode/vscodeHost.ts`: correct

4. A rename with `overwrite: true` now goes through Node's `fs.rename`. On POSIX this is `rename(2)`,
   which replaces the target in one step. On Windows it is libuv `MoveFileExW` with
   `MOVEFILE_REPLACE_EXISTING`. Renames with `overwrite: false` still go through `workspace.fs` and
   behave as before.
5. **Callers are unaffected.** There are three callers of `files.rename`:
   - The comment store's temp-file rename (`comments.ts:89`) is the only caller with `overwrite: true`.
   - The sidecar move (`comments.ts:345`) and the download (`hostRequests.ts:65`) use
     `overwrite: false`, so nothing changes for them.
6. **Local files only.** Every path is built with `Uri.file`. The host already uses Node for
   `realpath` and `isSymbolicLink`. The extension has no `browser` entry. If the extension runs in a
   remote extension host, Node's fs is that host's own disk, which is the right one.
7. **Error handling parity.** `writeAtomically` catches the error, removes the temp file and
   rethrows. `step` turns the error into `reason: error.message`. No caller checks the error code of
   a rename, so a Node error (EPERM, ENOENT) and a `FileSystemError` give the same behaviour. Only
   the wording of the message differs.
8. **Events and watchers.** The extension's sidecar watcher and VS Code's disk watcher still see the
   change on disk. They now get one change or create event instead of a delete followed by a
   create, which is better. The main-thread `onDidRunOperation(MOVE)` event no longer fires for
   this internal temp-file rename. No code in the repo listens for it. `workspace.fs` operations never
   fired `onDidRenameFiles`.
9. **Windows (advisory, not a regression).** `MoveFileExW` can fail with EPERM or EBUSY when another
   process holds the target open without `FILE_SHARE_DELETE`. The old path would fail in the same
   case, because its delete step would fail. The write is then reported as failed and the temp file
   is removed. There is no data loss.

## Fake and tests: sound

10. **The fake models VS Code correctly.** `fakeVscode.ts` `workspace.fs.rename` mirrors `doMoveCopy`:
    - it deletes the target, then renames, when `overwrite` is set;
    - it refuses an existing target with code `FileExists` when `overwrite` is not set.

    `targetsDeletedByRename` records each delete. With the old code, the overwrite path would go
    through this fake rename and record the delete, so tests 1 and 3 would fail. The coder's
    reproduce-first claim holds.
11. **The tests are strict.** `test/host-vscode/fileRename.test.ts` passes: 3 of 3 alone, and inside
    `just check`.
    - Test 3 runs the real comment store through the VS Code host. It checks the content, that the
      target was never deleted, and that no temp file is left.
    - Test 1 proves which path the rename takes. It does not prove the OS rename is atomic, which is
      OS behaviour and acceptable.
    - The integration test is unchanged: no assertion was weakened, no timeout raised, no retry
      added.
12. **The coverage lines are legitimate.** `SwRS-MDOKFSTUDIO-REVIEW-054` is a SwRS with
    `lifecycle: proposed`. It is not on the list of locked StRS. Its description already requires
    "writing through a temporary file renamed onto" the sidecar. The two added lines are generated
    and match the new `@implements_req` and `@tests_req` tags.
13. `just check`: exit 0.
    - unit: 3191 passed, 0 failed
    - security: 69 passed
    - pytest: 80 passed
    - requirements: 1067, with 0 errors and 0 warnings
    - indexes and coverage: 0 would change

    Log: /private/tmp/claude-502/cr199-driver/round2-inspector-check.log

## Remaining flakiness in commentAnchors (advisory, no change requested)

14. With the sidecar now replaced in one step, every later `readFileSync` and `JSON.parse` in the
    rename section reads either the old file or the new one. The race above is gone.
15. The section "Rename onto an existing sidecar" uses `pause(1000)` and then checks that nothing
    changed. A slow runner can let it pass when it should fail, but it cannot make it fail when it
    should pass. It is not a flake source.
16. Heavy CI (integration) is still the proof for the real-window scenario. Dispatch it on this
    branch, because the CR touches code that integration exercises.
