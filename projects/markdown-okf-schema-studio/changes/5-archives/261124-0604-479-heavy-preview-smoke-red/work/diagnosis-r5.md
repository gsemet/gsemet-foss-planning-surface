# Diagnosis round 5: real-input RI-T34 "the slow render was applied as a content patch" (heavy run 45232328831)

Verdict: a test race on the same root cause as CR-479 (the build queue says "ready" before the show
of the render ends). It is NOT caused by this CR's change (`sendPreviewMessageForTests`,
`hasPendingShow`, `pendingShow` in `previewManager`). It was hidden on main by earlier red steps.
No runtime repro was run (needs a real VS Code window); proof is the code path plus CI history.

## Failing assertion
- Source `test/integration/realInput/renderPatching.ts:371` (compiled `out/.../renderPatching.js:357`):
  `assert.ok(contentPatchCount() > patches1, "the slow render was applied as a content patch")`
  in `scenarioContentPatchedInPlace` (RI-T34), fixture `realinput-t34`. Log lines 1776, 1874-1897.
- RI-T34's first half passed (log: "RI-T34 typing: 0 html assignments, 20 content patches", 18:02:53);
  the failure is at 18:02:59, in the slow-render half (`setRenderDelayForTests(5_000)`, type "yz").
- The preceding `assert.equal(htmlAssignmentCount(), a1)` (line 370) passed: no document assignment, but
  also no patch counted yet.

## Mechanism
1. After the slow render ends, `RenderingController.handleQueueState` (rendering.ts:414-434) on phase
   `ready` calls `endPendingOverlay` (overlay gone, posted to the page) and then fires
   `updatePreview` without awaiting it (`fireAndForget`).
2. `showPreview` (rendering.ts:197-337) is asynchronous since 20b12216 (2026-11-23 09:13, "read conf.py,
   toctree and resources via the async port"): it awaits `previewLocalResourceRoots` (:220) and
   `buildPreviewWebviewHtml` (:255) before deciding patch vs. assign. `preview.probe.contentPatches += 1`
   happens only in `postContentPatch` (pageDocument.ts:241), called at rendering.ts:322, after those awaits.
3. The test's wait chain (renderPatching.ts:366-369) reads only state that is already true when the
   queue is ready: `waitForRender` = queue `phase==="ready"` and `documentVersion` (harness.ts:109,
   from the queue state), `webviewReady` = `preview.stage !== undefined && ...` (testHooks.ts:178; the
   OLD stage is still set), overlay gone (set by `endPendingOverlay` in step 1). All three hold while the
   show is still pending, so line 371 reads `contentPatchCount()` before the patch is posted: equals
   `patches1`, assertion fails. Slower CI I/O (this run: real-input took 371 s) widens the window.
4. The next wait (renderPatching.ts:373, typed text "yz" in the page) is a real wait on the page and
   would have passed; only the counter assertions at 370-371 read too early.
5. Nothing in the failure involves a test message: RI-T34 types with `page.keyboard` (`typeText`) and does
   not call `sendPreviewMessageForTests` (grep of test/integration/realInput: no use). The CR's hooks are
   not on this path, and the CR's src change (`pending` counter, extra `await pendingShow` at the end of
   `openPreviewForDocument`, previewManager.ts:427) only adds bookkeeping, no ordering change to a patch.

## Is it already on main?
Yes, the race exists on main since 20b12216. Evidence (gh):
- main run 45142308892 at d9b3cd6b (08:55, the commit before the async port) is green, real-input
  included. Every main push after the port is red: 45156102152 (d762a732), 45187475612 (2e2efa6c),
  45211958522 (dcc84def), each at `preview-smoke` (the CR-479 failure, "/admonition/iu"), a step that
  runs BEFORE real-input (real-input starts at 17:56:48 in the failing run, after preview-smoke passed).
- So no heavy run since the port has reached real-input: this is the first, not a regression of this
  CR. The other CR-branch heavy runs also stop earlier: 45228154497 and 45220156258 (preview-editing
  / untrusted-suite), 45220342674 (preview-editing timeout), 45220283841, 45204248156, 45217679420
  (preview-smoke). Each fix of CR-479 unmasks the next step that shares the same ready-before-shown gap
  (untrusted-suite comments: diagnosis.md; preview-editing; now RI-T34).

## Smallest fix, and whether it belongs to this CR
Test side, in `renderPatching.ts` around 366-371: wait for the shown stage instead of the queue before
the counter assertions, e.g. replace the three waits by
`await waitFor("the slow render to be patched into the page", () => contentPatchCount() > patches1)`
(keep the overlay-gone and typed-text waits after it), or wait on `shownRequestId === requestId`
(`shownRequestId` was added to `getActivePreviewForTests` by this CR for exactly this). Same for the
first-half assertion at :330-331, which passed only because 600 ms of sleep (:327) covers the window.
No product change needed. It belongs to CR-479 as its stated class ("a reader that looks at the page
before the pending show ends") and is needed to make heavy CI green; but it is a new, separate
test-only spot: a sweep of other `htmlAssignmentCount`/`contentPatchCount` assertions that follow
`waitForRender` in realInput (e.g. `renderPatching.ts`, `performanceProbe.ts:155`) is advisable in the
same CR, since the next heavy run will otherwise stop at the next one. If the Driver wants it out of
scope, file a follow-up CR, but heavy stays red until it lands.

Reproduction: `gh workflow run ci.yml --ref <branch> -f heavy=true`; locally `just ci-integration`
needs a real VS Code (not run here).
