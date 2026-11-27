# Diagnosis: untrusted-suite "Timed out waiting for the comments file" (heavy CI run 45220156258)

Verdict: TEST race, exposed by the async port of 2026-11-23 (commit 20b12216). Not a product
regression. Not caused by CR-479's change. No runtime repro was run (a real VS Code window on the
owner's desktop was not started); the proof is the code path plus the CI history below.

## Failure
- Log: work/ci-45220156258.log lines 581-593. `untrusted-suite` starts 16:48:45, fails 16:49:07
  (22 s = about 2 s of earlier steps + the 20 s `waitFor` default), at
  `test/integration/commentWrite.test.ts:239` (`await waitFor("the comments file", () => fs.existsSync(sidecar))`).
- The wait at lines 230-234 ("the preview to show the current document") PASSED, so the test
  considered the preview current. The message sent just after it never wrote the sidecar.

## Cause (proved by reading the code path)
1. `runUntrusted` (commentWrite.test.ts:226-239) waits for `getActivePreviewForTests()` to have
   `phase === "ready"` and `documentVersion === document.version`. Both come from the BUILD QUEUE
   state (`src/host-vscode/testHooks.ts:142-148`: `phase: state.phase`,
   `requestId: state.request?.requestId`, `documentVersion: state.request?.documentVersion`).
2. `send()` (commentWrite.test.ts:24-32) posts `previewCommentCreate` with `requestId` taken from that
   queue state (`getActivePreviewForTests()?.requestId`).
3. Host side, the "comment" gate (`src/session/pageMessages.ts:127-130`) calls
   `manager.matchesCurrent` (`src/session/previewManager.ts:170-186`), which requires
   `message.requestId === session.stage.requestId`. A message that does not match is dropped with no
   answer: `handle` returns `undefined`, no write, no `previewCommentResult`. So no sidecar, ever.
4. `session.stage` is NOT set when the queue reaches `ready`. Since 20b12216 (09:13 on 11-23,
   "read conf.py, toctree and resources via the async port") `RenderingController.updatePreview`
   is asynchronous: `handleQueueState` (rendering.ts:401-420) fires `updatePreview` and returns, and
   `showPreview` assigns `preview.stage = result.stage` only at rendering.ts:289, AFTER
   `await previewLocalResourceRoots(...)` (:207) and `await buildPreviewWebviewHtml(...)` (:242),
   which run file-system lookups (realpath, resource priming). Updates of one session are chained
   (`updates` WeakMap), so after the block-move and block-clipboard Restricted Mode steps (which
   edit and undo the document and queue several renders) the last show can still be pending.
5. In that window: queue says `ready` for request N and version V, `stage.requestId` is still the
   previous render's id. The test sends requestId N, the gate compares with the old stage id, drops
   the message. Before the port `updatePreview` was synchronous, so `stage` and `ready` changed in
   the same tick and the window did not exist. CR-479 has the same root cause for the preview-smoke
   test (a reader that looks at the page before the pending show ends): `pendingShow` is the new
   host-side wait for it.

## Why it was hidden and why it is not CR-479's doing
- Last green heavy run of main: 45142308892 at d9b3cd6b (11-23 08:53), untrusted-suite done in
  6.3 s (integration) and 22.5 s (stress job). The next commit is the async port (20b12216, 09:13).
  Every heavy run of main since (45156102152, 45187475612, 45211958522) and of the batch branches
  (45204248156, 45217679420, 45220283841) is red at `preview-smoke` (`/admonition/iu`), a step that
  runs BEFORE `untrusted-suite`, so the untrusted suite never ran after the port until CR-479 let
  the run go further. Command used:
  `gh run view <id> --log-failed | grep -E "STEP failed"` for each id above (all say preview-smoke).
- The "preview-smoke" fix of CR-479 only adds `await this.rendering.pendingShow(session)` at the end
  of the open command (previewManager.ts, after line 424); it does not touch the comment path.
  The failure at origin/main cannot be observed (preview-smoke stops the run first), but the code
  path above is the same at origin/main: `git diff d9b3cd6b..HEAD -- src/session/features/comments.ts`
  is only an import change (`node:path` to `hostPath`, same module re-exported), and
  `src/host-vscode/headBaseline.ts` (git author lookup) is unchanged.

## Not a product regression
A real page only posts messages with the `requestId` of the stage the host gave it, so the gate
matches. The race is the test reading the queue state instead of the shown stage. The comment write
path itself is unchanged (writeComment, sidecar store, hostPath is a pass-through of `node:path`).
Same exposure exists in the other untrusted steps that wait on `phase === "ready"` /
`webviewReady && documentVersion === document.version` (blockMove.test.ts:29,224,
blockClipboard.test.ts:28,164); they only passed by timing, and are worth checking too.

## Smallest fix proposal (not applied)
Make the test wait for the SHOWN stage, not the queue:
1. `src/host-vscode/testHooks.ts`: add `shownRequestId?: number` to the returned type (near line 67)
   and the object (near line 175): `shownRequestId: preview.stage?.requestId`. (Test hook only.)
2. `test/integration/commentWrite.test.ts:230-234`: wait for
   `current.shownRequestId === current.requestId` in addition to the existing conditions, and make
   `send()` (line 29) use `shownRequestId ?? requestId` as the message `requestId`.
   Alternative with the same effect and no new field: have the hook expose the host's
   `rendering.pendingShow(preview)` (e.g. `await settleShowForTests()` in testHooks) and await it
   after the `waitFor` and before `send`.
3. Apply the same wait in `blockMove.test.ts` / `blockClipboard.test.ts` untrusted waits (lines 29,
   28) to remove the same latent race. Add an `@tests_req` unchanged; no SwRS change needed.

Verification of the fix: `just ci-integration` in CI with heavy=true (the run must pass
`untrusted-suite` after `preview-smoke`); locally the unit gate `just check` only.

## Evidence (commands run in the worktree)
- `grep -n "Timed out\|STEP" work/ci-45220156258.log` (lines 581-593 above).
- `git diff d9b3cd6b..HEAD -- src/session/features/rendering.ts` (async `updatePreview`,
  `preview.stage = result.stage` moved after two awaits).
- `sed -n 170,186p src/session/previewManager.ts` (`message.requestId === stage.requestId`).
- `gh run list --workflow ci.yml --branch main` and `gh run view <id> --log-failed` as listed above.

---

# Addendum: CR-477 heavy run 45220342674, preview-editing "schema-valid boolean value to be written"

Verdict: the SAME stage.requestId race (a second victim), not caused by CR-479's change, and its
fix belongs in CR-479 (same root cause, same helper `pendingShow`).

Evidence
- Log (CR-477 work/ci-45220342674.log): `STEP start: preview-editing` 17:01:20.92, `STEP failed:
  preview-editing (28716 ms): Timed out waiting for the schema-valid boolean value to be written`
  17:01:49.63. Everything before it passed (real-input 445 s). The red line after it is VS Code
  EACCES noise on /tmp, unrelated.
- Test: `test/integration/previewEditing.test.ts:396-407`: `await waitForCurrentPreview(document)`,
  then `currentContext(document)` and `sendPreviewMessageForTests({type:"previewFrontmatterSave", ...})`,
  then `waitFor("the schema-valid boolean value to be written")` (5 s default of
  previewEditingHelpers.waitFor).
- `waitForCurrentPreview` (previewEditingHelpers.ts:16-30) and `currentContext` (:55-70) read only
  the QUEUE state (`phase`, `documentVersion`, `requestId` from `state.request`), as in the first case.
- Host: `previewFrontmatterSave` is gate "page-state" (pageMessages.ts:61): `handlePageState` ->
  `manager.matchesCurrent` (requires `message.requestId === stage.requestId`, previewManager.ts:185);
  on mismatch `reportStaleEdit` only posts an edit error to the page and the save is dropped
  (pageMessages.ts:258, :309-311). The text is therefore never written, hence the timeout.
  `stage` is assigned after the awaits of `showPreview` (rendering.ts:289) since 20b12216.
- The step just before (lines 376-396) forces several renders in quick succession (slow frontmatter
  edits and a document replace), so the last show can still be pending when `waitForCurrentPreview`
  returns: the exact window described above.
- Not CR-479's doing: it only appends `await pendingShow` to the open command; the run is on a
  head that contains it, but the preview-editing step was unreachable before (preview-smoke was red
  earlier in the same run family). Same pre-port/post-port history: green before 20b12216.

## Every wait that sends a page message with the queue's requestId (exposed)
All build `requestId` from `getActivePreviewForTests()` (queue) after a wait on `phase`/`documentVersion`/
`webviewReady`, none checks the shown stage:
- test/integration/previewEditingHelpers.ts: `currentContext` (:55-70) + `waitForCurrentPreview` (:16);
  used by previewEditing.test.ts (39 call sites), detachedSaveWindow.ts:16 and others through the helper.
- commentWrite.test.ts:24-32 (`send`), :226-239 (the failing one) and :126.
- blockMove.test.ts:64, 163, 205, 231; blockClipboard.test.ts:45, 175-202.
- blankLines.test.ts:51; emptyBlocks.test.ts:42, 104; inlineThread.test.ts:87; labelRename.test.ts:53, 83;
  updateGlow.test.ts:91; previewHistory.test.ts:25; genericMarkdown.test.ts:22-35, 59.
- imagePaste.test.ts:63, 76, 106; imagePicker.test.ts:78; paletteMode.test.ts:66, 78, 90;
  lifecycle.test.ts:82, 116, 129, 153 (captured earlier: risky only if a show is pending).
- untrusted-suite.ts:195, 208, 222; standalone-suite.ts:137; realInput/flushBeforeNavigate.ts:129;
  realWindowGaps.ts:288 (reads only).
Not exposed: test/visual/renderFixtures.ts (uses the page's own message.requestId), sourceMapping.test.ts
:94/:111 (deliberate stale id), test/probe/previewProbe.ts (probe), and reads-only traces
(harness.ts:224, tableInsertSlash.ts:75, scenarioTrace.ts:33).

## One-round fix (recommended, replaces the per-test proposal above)
Fix it once, in the test hook, with the CR's own host wait:
- `src/host-vscode/testHooks.ts:224` `sendPreviewMessageForTests`: before
  `current.manager.handlePageMessage(preview, message)`, `await current.manager.rendering.pendingShow(preview)`
  (return a promise; the signature is already `PromiseLike<void> | undefined`). Every test then
  sends after the show that the queue's `ready` announced has finished, so `stage.requestId` equals the
  queue's `requestId`. A deliberately stale id (sourceMapping:111) stays stale.
- Also expose the same wait for the tests that read html/webviewReady (optional): `shownRequestId`
  in `getActivePreviewForTests`, and make `waitForCurrentPreview` require
  `shownRequestId === requestId`, so reads of `preview.html` are of the shown page too.
- Add a host test in test/host/openCompletes.test.ts style: queue `ready` while the show is held;
  `sendPreviewMessageForTests` of a comment must still write. Requirement: SwRS-MDOKFSTUDIO-LIFE-003
  marker already on the CR's change; no new SwRS.
