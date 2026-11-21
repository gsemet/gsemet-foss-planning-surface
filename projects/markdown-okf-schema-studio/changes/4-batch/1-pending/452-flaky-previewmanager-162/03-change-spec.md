# Change Specification: the join-window and hidden-panel tests control time instead of waiting

Origin: verbal. A flake noted during CR-432 (batch-06) and seen again in the CR-443 gate
(batch-07). No GitHub issue.

## Premise note

`intake/request.md`, `01-intent.md` and pm-Q1 in `02-answers.md` name the test "a hidden panel
does not render until it is shown, then renders once". That premise was wrong. node:test reports
lines of the compiled JavaScript, because the unit run has no source maps. In
`out/test/session/previewManager.test.js`, line 162 is the assertion
`assert.equal(f.renders.length, 1, "the second preview joined the first render")` of the test "a
page refresh inside the join window renders again instead of joining the shared render" (TS line
137 at `origin/main` 5a84db8b). The CR-443 gate log shows it: planning surface
`changes/4-batch/3-done/443-requirements-share-cards/work/gates/20261121-020805.log`, lines
3967-3969 and 4257-4271, a full `just unit` run under load. There, the join-window test fails with
`2 !== 1` at `previewManager.test.js:162:16`, and the hidden-panel test passes. pm-Q2 confirms the
decision on the real premise and replaces pm-Q1. The owner's quoted answers are not edited.

## Goal

The two time-dependent tests of `test/session/previewManager.test.ts` give the same result on a
loaded machine as on an idle one: "a page refresh inside the join window renders again instead of
joining the shared render" (the test that flaked) and "a hidden panel does not render until it is
shown, then renders once". Each test controls time itself (fake timers, or an injectable window or
clock with the same value) instead of waiting fixed times. The product's behaviour does not change.

## Decisions carried from the grill (`02-answers.md`)

- pm-Q2 (on the real premise), owner: "Corriger le test seul". Only the test changes. The test
  controls time (fake timers) instead of waiting. The product does not change: a request that
  arrives more than 250 ms after the shared render ended rendering again stays accepted.
- pm-Q3, owner: "Oui, même CR". The hidden-panel test is converted too, so no fixed wait is left
  in either test.
- From the Chief of Staff, giving the owner's pm-Q2 terms: the SwRS text does not change, no entry
  goes in `requirements/tiers/log.md`, and both tests keep their `@tests_req` markers
  (SwRS-MDOKFSTUDIO-LIFE-039 on both, SwRS-MDOKFSTUDIO-LIFE-032 on the join-window test).
- pm-Q1 (fix the product if it renders twice when a hidden panel is shown) was answered on the
  wrong premise, and pm-Q2 replaces it. This spec carries no product fix for it.
- Owner, 2026-11-21: once final and ready, the CR joins the running batch-07.

## The race (proved)

The Fable spec critic reproduced it with
`C:/Users/gaeta/AppData/Local/Temp/claude/78bc118259cc4dd6/d5e1995b-c12d-4b5f-a287-f3bf80096868/scratchpad/repro.test.cjs`.
That script is the fixture of the join-window test, with `host.paths.sourceExists` stubbed to
busy-wait once for a given number of milliseconds.

1. `await f.manager.requestDocument(b.session, f.document)`: b's queue debounces 40 ms
   (`debounceMs: 40` in `src/session/sessionFactory.ts`). Then `SharedRenders.acquire`
   (`src/session/sharedRenders.ts`) starts the render. When it ends, the entry arms a real
   `setTimeout(..., SHARED_RENDER_WINDOW_MS)` (250 ms, `unref()`ed). While that timer runs, the
   entry can still be joined.
2. `await f.manager.requestDocument(a.session, f.document)` runs `sourceAvailable` first
   (`previewManager.ts`, synchronous file-system calls through `host.paths`). Then it waits for a's
   own 40 ms debounce before `acquire`.
3. If the machine stalls for more than about 210 ms between b's end and a's `acquire` (210 ms plus
   the 40 ms debounce makes 250 ms), the window has closed and the entry is gone. a renders again,
   and `f.renders.length` is 2. Measured: no stall gives 1 render, a 150 ms stall gives 1, a
   260 ms stall gives 2.

That 2 is the product working as SwRS-MDOKFSTUDIO-LIFE-039 and `sharedRenders.ts` describe it: a
render can be joined during the 250 ms window after it ends, not later. The fault is in the test,
which depends on wall-clock time. Its later `f.wait(100)` after `previewRefresh` has the same
fault. So do the hidden-panel test's `f.wait(150)` and `f.wait(200)`.

Hardening note (R2, not the cause): the fixture counts renders through
`setRenderOverrideForTests` (`src/core/render/renderPipeline.ts`). That hook is a module-level
variable, read each time a render runs, so `renders` counts the renders of every manager in the
process. The converted tests also assert `f.manager.sharedRenders.started`, which counts only the
renders this manager started; its comment calls it "a probe for tests". A late render left over
from another test can then not be mistaken for one of this test's.

## What changes

### `test/session/previewManager.test.ts`

The fixture (`renderFixture`):

- It controls time for the timers that decide the outcome: the queue debounce and overrun timers
  (`src/core/render/buildQueue.ts`) and the shared-render window (`sharedRenders.ts`). Use one of
  two means:
  - node:test fake timers (`mock.timers.enable({ apis: ["setTimeout", "Date"] })`, reset in
    `cleanup()`). The Driver checks that the object a mocked `setTimeout` returns accepts the
    `unref()` call `sharedRenders.ts` makes, and that `clearTimeout` works on it. If it does not,
    use the second means.
  - An injectable window or clock: for example an optional `SharedRenders` constructor parameter
    whose default is `SHARED_RENDER_WINDOW_MS`, so the shipped value stays 250 ms. This is the only
    `src/` change allowed. The product's behaviour and the value stay the same.
- Between two tick steps, the fixture lets the promise chains of the queue and of `acquire` settle
  (a helper that drains pending microtasks or yields one event-loop turn, never a sleep of a set
  time).
- The fixture's `wait(ms)` helper goes away. No test of the file sleeps for a set time.

"a page refresh inside the join window renders again instead of joining the shared render" keeps
its title and its markers (`@tests_req SwRS-MDOKFSTUDIO-LIFE-039`, `@tests_req
SwRS-MDOKFSTUDIO-LIFE-032`):

1. b requests the document. Tick past the 40 ms debounce and let b's render settle: one render.
2. a requests the document. Tick less than the 250 ms window measured from b's end (the 40 ms
   debounce is enough) and let it settle. Assert `f.renders.length === 1` and
   `f.manager.sharedRenders.started === 1`: a joined.
3. Dispatch `previewRefresh` to a, as today, then tick past the debounce instead of
   `f.wait(100)` and let it settle. Assert 2 renders: the Refresh button renders again.

"a hidden panel does not render until it is shown, then renders once" keeps its title and its
marker (`@tests_req SwRS-MDOKFSTUDIO-LIFE-039`):

1. Make the three calls made while hidden, as today. Without ticking, assert that no render ran
   (`renders` and `started` are 0) and `renderDirty === true`. Then advance time past every timer
   the queue could have armed (more than its `maxDebounceMs` of 1000 ms plus the 250 ms window) and
   assert 0 renders again.
2. `hidden.show()`. Advance time past the debounce, let the render settle, then advance past the
   longest debounce and the 250 ms window, so that any later request would have run its render.
   Then count: `renders` and `started` are 1, `finished` has one entry, and
   `renderDirty === false`.
   - The test does not use "await the first ready, then assert once": a second request made after
     that point would not be seen.
   - The test does not use `queue.getState().phase === "ready"` as proof that no request is
     pending: `BuildQueue.run` publishes `ready` and only then calls `drainPending`, so the phase
     proves nothing.

### Product

No behaviour change. `src/` changes only if the injectable window or clock above is chosen, with
the same default value.

### Requirements

The SwRS text does not change, and no entry goes in `requirements/tiers/log.md`. The markers stay
on both tests. Run `just requirements-update` only if a marker line moves (it does not when the
tests keep their place).

## Out of scope

- Changing the 250 ms window value, the 40 ms debounce or the overrun rule. An injectable window
  for tests with the same value is allowed.
- Changing a render that arrives after the window closes: rendering again stays accepted.
- Fixed waits in other test files.

## Evidence

- Regression, proved without a stress run: stub `host.paths.sourceExists` in the fixture to
  busy-wait 260 ms once, before a's request in the join-window test, as `repro.test.cjs` does.
  With the old test (real timers, at `origin/main`) it fails `2 !== 1`. With the new test it
  passes, because the stall moves the wall clock and not the controlled time. Report both runs in
  the PR. The stall stub is evidence only and is not committed, unless the Driver keeps it as a
  permanent case of the test. That is allowed: the test then proves on its own that a stall cannot
  change the outcome.
- Each test catches a real double render. These are local mutations, reported in the PR and not
  committed:
  - Hidden-panel test: in `renderIfDirty`, once the first refresh resolves (the build is ready),
    call `manager.sharedRenders.invalidate()` and then `refreshPreviewDocument` again. That really
    renders twice, and the test must fail on `renders`/`started === 1`. Separately, make
    `deferWhileHidden` return false: the test must fail in the hidden phase.
  - Join-window test: call `manager.sharedRenders.invalidate()` at the start of `requestDocument`.
    a then cannot join, and the test must fail on "the second preview joined the first render".
- A grep showing no `wait(` call and no `setTimeout`-based sleep left in
  `test/session/previewManager.test.ts`.
- A stress run at the head under real load (for example `just unit` alongside another heavy job,
  or 20 parallel runs of the compiled file after `just compile`): zero failures, with the counts.
  This adds confidence; it does not prove the fix.
- `just check`, then `just preflight` (on Windows the static stage; CI runs the others), as the
  constitution requires.

The Spec-writer's earlier stress result does not count as evidence that the flake is absent: 80
runs without a failure (16 in parallel, 5 times each), on a stale local `out/` build of 2026-11-06,
with no other load.

## Open questions for the owner

None. pm-Q2 and pm-Q3 settle the behaviour, and the earlier Q1 to Q3 are closed.
