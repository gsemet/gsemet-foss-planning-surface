# Change Specification: a hidden preview shown renders once, and its test proves it without fixed waits

Origin: verbal. A flake noted during CR-432 (batch-06): no GitHub issue.

## Goal

When a hidden Studio preview panel is shown, the preview renders the document exactly once. The
unit test that guards this, `test/session/previewManager.test.ts` "a hidden panel does not render
until it is shown, then renders once" (`@tests_req SwRS-MDOKFSTUDIO-LIFE-039`), failed once at
commit `a4110666` with `2 !== 1` on line 162 ("one render when the panel is shown") and passed on
rerun. CR-432 did not touch it. This CR finds where the second render came from, fixes the product
if the product renders twice, and makes the test deterministic: it waits on an event or a render
count, never on a fixed time.

## Decisions carried from the grill (`02-answers.md`)

- pm-Q1, owner: "Corriger aussi le produit". Find the race. If the product renders twice when a
  hidden panel is shown, fix the product. The test waits on an event or a render count, never on
  fixed times (the current `f.wait(150)` and `f.wait(200)` go).

Nothing else was decided; the open questions are at the end.

## The code involved (read at `origin/main` 5a84db8b)

The rendering path of a hidden panel, as it is today:

- `PreviewManager.requestDocument` (`src/session/previewManager.ts`, around line 406): it sets
  `session.document`, then returns early when `rendering.deferWhileHidden(session)` is true. No
  queue request is made.
- `RenderingController.refreshOpenDocument` (`src/session/features/rendering.ts`, around line
  501): when `needsRefresh(...)` holds, it calls `refreshPreviewDocument` fire-and-forget.
- `RenderingController.refreshPreviewDocument` (around line 460): it also returns early through
  `deferWhileHidden`, else calls `preview.queue.refresh(document, options)`.
- `deferWhileHidden` (around line 481): `panel.visible` gives `renderDirty = false` and false;
  a hidden panel gives `renderDirty = true` and true. The deferral is synchronous.
- The show: `SessionFactory.createSession` (`src/session/sessionFactory.ts`, around line 184)
  subscribes to `panel.onDidChangeViewState`. A `wasVisible` flag keeps only a hidden-to-visible
  change. On that change it calls `scroll.restorePreviewState(session)`, then
  `rendering.renderIfDirty(session)`.
- `renderIfDirty` (rendering.ts, around line 492): when `renderDirty` is set it clears it, then
  calls `refreshPreviewDocument` fire-and-forget. This is the one render on show.
- The queue (`src/core/render/buildQueue.ts`, built through `host.renderQueues`, `debounceMs: 40`
  in `sessionFactory.ts`): requests that arrive during the debounce merge into one
  (`supersedePending`). A request that arrives while a build runs waits for that build to end, then
  builds again. The queue never retries a build on its own.
- `SharedRenders.acquire` (`src/session/sharedRenders.ts`): a request with the same key
  (document id, revision, workspace root, restricted reads, trust, PlantUML jar and engine) joins
  the render in flight, and keeps joining for `SHARED_RENDER_WINDOW_MS` (250 ms) after it ends.
  `invalidate()` (called by `prepareRefresh` and by `hostEvents.ts` on a file or setting change)
  ends the joins. `sharedRenders.started` counts the renders this manager started; its comment
  says it is "a probe for tests and diagnostics".
- The test counts renders through `setRenderOverrideForTests` (`src/core/render/renderPipeline.ts`).
  That override is a module-level variable, read each time `renderPreviewDocument` runs. Its
  `renders` array therefore counts every override call in the test process, from any manager,
  whichever test started the render.

## Races the Driver must prove or rule out

Reading the code found no second render path on show. Each item below gets a verdict in the PR
body (proved, with the reproduction, or ruled out, with the reason and the evidence). A guess is
not a verdict.

1. **R1, product: a second request after the show that does not join the first render.** For a
   second render, the session must make a second queue request after the panel became visible,
   and that request must either come after the build started, then miss the join (an
   `invalidate()` came in between, or the key changed), or come more than 250 ms after the first
   render ended. The candidates are a second hidden-to-visible change reaching `renderIfDirty`
   (the `wasVisible` guard should stop it), or a refresh from another source arriving at the same
   time as the show (`refreshOpenDocument`, a follow-the-editor switch at `previewManager.ts` line
   622 or so, a `hostEvents` refresh followed by `invalidate()`). In the unit fixture, `watcher`
   returns no events, `handleQueueState` and `restorePreviewState` are stubbed, and no host
   document events are wired. So prove R1 at product level as well (the real `handleQueueState`
   and the VS Code view-state sequence of a panel shown in its group), not only in the fixture.
2. **R2, test: the global render counter.** The test cannot tell a render of its own session from
   a render of another manager in the same process that runs after its
   `setRenderOverrideForTests`. The earlier tests of the file ("two previews ... share one
   render", "a page refresh inside the join window ...") call `cleanup()`, which resets the hooks
   and disposes every session, and so every queue (`disposeSession` calls `queue.dispose()`, which
   clears the debounce and overrun timers and aborts the active build). In theory no build of
   theirs can start later. The Driver confirms this, or shows the leak. Either way the new test no
   longer counts through the process-wide override alone (see "What changes").
3. **R3, test: the fixed waits.** A wait that is too short would give `0 !== 1`, not `2 !== 1`, so
   a short wait does not explain the seen failure. A longer wait can only let in more late work.
   Making the waits longer is not a fix. The fixed waits go whatever R1 and R2 show.
4. **R4, product: work queued while hidden that fires after the show.** All three calls made
   while hidden defer synchronously, so the queue should stay `idle` with no request until the
   show. The new test asserts this directly (queue state), with no wait.

Evidence to start from (Spec-writer, read-only, 2026-11-21): 80 runs of the compiled test file
(16 in parallel, 5 times each) at a local build of 2026-11-06, whose rendering path matches
`origin/main` (`git diff a4110666 origin/main` touches no file of this path), gave no failure. The
race is rare. The Driver needs a deterministic reproduction, not a stress run alone, before
claiming R1.

## What changes

### Test: `test/session/previewManager.test.ts`

- The test "a hidden panel does not render until it is shown, then renders once" keeps its title
  and its `@tests_req SwRS-MDOKFSTUDIO-LIFE-039` marker, and no longer calls `f.wait`.
- Hidden phase: right after `requestDocument`, `refreshOpenDocument` and `refreshPreviewDocument`,
  assert synchronously that `f.manager.sharedRenders.started === 0`, that `f.renders.length === 0`,
  that `hidden.session.renderDirty === true`, and that `hidden.session.queue.getState().phase` is
  `"idle"` with no `request`. This proves no deferred request is armed (R4), with no wait.
- Shown phase: the fixture gives a promise that resolves on the next `"ready"` queue state of a
  session (the `handleQueueState` stub already sees it; today it only pushes to `finished`). The
  test calls `hidden.show()` and awaits that promise. Then it asserts:
  `f.manager.sharedRenders.started === 1` (this manager's renders, immune to R2),
  `f.renders.length === 1`, one entry in `finished` with `requestId === 1` (the session made one
  queue request), `hidden.session.queue.getState().phase === "ready"` (no second request pending
  or building), and `hidden.session.renderDirty === false`.
- The awaited promise can hang if no render ever comes. The test fails then on the node:test
  timeout it sets (`{ timeout: ... }` on the test), not on a fixed wait in the body.
- The fixture's `wait` stays only as long as another test still uses it (see open question Q1).

### Product: `src/session/` (only if R1 is proved)

- When R1 is proved: fix the race in the rendering path of a shown panel (`rendering.ts`
  `renderIfDirty` / `refreshPreviewDocument` / `deferWhileHidden`, `sessionFactory.ts` view-state
  handler, or the source of the second request), so that a panel shown once renders once for one
  document revision. Keep the shared-render and debounce behaviours of SwRS-MDOKFSTUDIO-LIFE-039
  unchanged.
- Add a regression test that reproduces the proved race deterministically (fake timers or a render
  override whose promise the test resolves itself, with the triggering events in the order that
  made the double render). It fails without the fix and passes with it.
- When R1 is ruled out: no change under `src/`.

### Requirements

- SwRS-MDOKFSTUDIO-LIFE-039 already says "a preview whose panel is hidden SHALL not render until
  the panel is shown". Its text does not change. The `@tests_req` and `@implements_req` markers
  stay with the code they mark.
- Run `just requirements-update` when a marker moves or a test is added. Add a dated entry in
  `requirements/tiers/log.md` only when the product changes (R1 proved).

## Out of scope

- The other fixed waits of the file (`f.wait(100)` in "a page refresh inside the join window
  renders again ...") and of other test files, unless the owner says otherwise (Q1).
- Any change to the debounce (40 ms), the shared-render window (250 ms) or the overrun rule.
- The real VS Code integration and e2e tests.

## Evidence

- The verdict on R1 to R4 in the PR body. A proved race comes with its deterministic reproduction.
  A ruled-out one comes with its reason (code path and test).
- The new test catches a double render: with a temporary local change that makes the show render
  twice (for example a second `refreshPreviewDocument` after `sharedRenders.invalidate()` in
  `renderIfDirty`), the test fails on `started`/`renders` and passes once the change is reverted.
  With `deferWhileHidden` made to return false, it fails in the hidden phase. Both are reported in
  the PR, not committed.
- A stress run of the file at the head (for example 20 processes in parallel, 10 times each, with
  `node --import ./scripts/register-myst-patches.mjs --test out/test/session/previewManager.test.js`
  after `just compile`): zero failures, counts reported.
- A `grep` showing no `wait(` call left in the hidden-panel test.
- `just check` passes, and `just preflight` passes (on Windows its static stage; CI runs the
  others), as the constitution requires.

## Open questions for the owner

- Q1. The fixture's `f.wait(100)` in "a page refresh inside the join window renders again instead
  of joining the shared render" is the same kind of fixed wait, in the same fixture. Should this
  CR convert it to an event wait too, or keep the scope to the test named in the flake?
- Q2. A test that waits on an event needs a bound when the event never comes. Is a node:test
  `timeout` on the test (it fails the test, it is not a wait in the body) acceptable as that
  bound?
- Q3. Suppose R1 cannot be reproduced deterministically and is not ruled out by code either (a
  second request from a VS Code event order the unit fixture cannot drive). Should the CR still
  add a product guard, such as "a shown panel makes at most one render request per document
  revision until a new change arrives", or deliver only the deterministic test and the evidence?
