# CR-426 Change Specification: the build queue tests read the real clock

## Goal

`just check` failed once on `test/node-services/build/buildQueue.test.ts`, test "still renders a
build whose buffer already moved on, and cleans up on dispose" (reported at compiled line 116,
`false !== true`), and passed before and after. The owner wants the flake gone: when the cause
lies in the product code, the code is fixed; when it lies in the test, the test is fixed.

## Cause (found and reproduced while writing this specification)

The cause is in the test, not in the product code.

- Line 116 of `out/test/node-services/build/buildQueue.test.js` is the line that declares the test
  (the `node:test` reporter gives the test's location, not the assertion's). In that test, the
  only assertion that prints `false !== true` is the last one, `assert.equal(aborted, true)`
  (line 122 of the `.ts` file). `assert.ok(...)` prints another message.
- The test mocks only `setTimeout` (`context.mock.timers.enable({ apis: ["setTimeout"] })`);
  `Date` stays the real clock.
- `BuildQueue.run` (`src/core/render/buildQueue.ts`) records the wall time of the first build,
  `Date.now() - active.startedAt`, as `lastBuildMs`. `currentDebounceMs()` then returns twice that
  time once it reaches `MIN_ADAPTIVE_BUILD_MS` (10 ms). On a loaded machine (a full `just check`,
  a garbage collection), 10 ms of real time can pass between the build's start and the end of its
  microtasks.
- The test's second request then waits 20 ms or more on the mocked clock. `tick(0)` does not
  start it, so no build is running when `queue.dispose()` is called: the request is canceled as
  pending (the assertion before passes), nothing is aborted, and `aborted` stays `false`.
- The queue does what SwRS-MDOKFSTUDIO-LIFE-039 says (the wait adapts to the last build's time).
  The fault is the test mixing two clocks: a debounce on the mocked clock, a build time from the
  real clock. `test/host/renderClock.ts` describes and fixes the same clash for the host
  harnesses.
- Reproduction (scratch script, compiled queue from `out/src/core/render/buildQueue.js`): the
  same test, with a build stub that busy-waits 15 ms of real time before it returns its promise,
  fails with `false !== true` (the debounce printed is 30 ms) when only `setTimeout` is mocked,
  and passes when `["setTimeout", "Date"]` are mocked (the debounce printed is 0 ms).
- The test "retains a successful result as stale after a failed newer build" in the same file has
  the same flaw: after its first build, `tick(0)` must start the second build, and
  `assert.ok(pending.has(2))` fails when the first build took 10 ms or more of real time.
  The other tests of the file either mock `Date` already or finish no build before a debounce
  they rely on.

The owner's answer covers a real race in the product code ("fix the code in this CR, with its
SwRS and a test that fails before the fix"). This cause is not one, so no product code changes.
The answer stays binding: if the Driver's own reproduction shows a product race after all, the
Driver fixes the code in this CR, with its SwRS and a test that fails before the fix, and says so
in the PR.

## What changes

Only `test/node-services/build/buildQueue.test.ts`.

1. "still renders a build whose buffer already moved on, and cleans up on dispose": mock the clock
   the queue reads, `context.mock.timers.enable({ apis: ["setTimeout", "Date"] })`. A build then
   takes no time on the test's clock, the second request's wait stays at `debounceMs: 0`, and
   `tick(0)` starts it before `dispose()`.
2. "retains a successful result as stale after a failed newer build": the same change, for the
   same reason.
3. In both tests the build stub spends at least 15 ms of real time before it returns its promise
   (a busy host, a short busy-wait on `performance.now()`), with a one-line comment saying why. On
   the old setup each run then fails, as the flake did once; on the new setup each run passes. The
   test thus guards the fix: removing `"Date"` from the mock fails it at once.
4. A short comment at the first of these mock lines says why `Date` is mocked: the queue's
   adaptive wait reads `Date.now()`, and the test's debounce runs on the mocked clock.

No assertion changes: same values, same intent (constitution, section 3). The two tests' names
stay as they are.

## Requirements

No SwRS changes: the queue's behaviour does not change. The `@tests_req` markers of the file stay
as they are (the second test keeps `SwRS-MDOKFSTUDIO-CORE-025` and `SwRS-MDOKFSTUDIO-LIFE-049`;
the first has none and gets none). No entry in `requirements/tiers/log.md`: the change is not a
substantive requirements change.

## Out of scope

- Any change to `src/core/render/buildQueue.ts` or `src/node-services/build/buildQueue.ts`
  (unless the Driver's reproduction finds a product race, see "Cause").
- The other test files using the queue (`test/host/renderClock.ts`, `test/session/nodeHostPorts.ts`)
  and the other flakes of batch-06 (CR-425 and others).
- Adding a `@tests_req` marker or an SwRS for the queue's disposal.

## Evidence

- Before the fix, at the branch's base: with step 3 applied alone (busy host, only `setTimeout`
  mocked), `fnm exec -- npm run compile` then
  `node --test out/test/node-services/build/buildQueue.test.js` fails both tests (the first with
  `false !== true`, the second at `assert.ok(pending.has(2))`). The Driver records the output.
- After the fix: the same command passes the whole file, run 20 times in a row
  (`for i in $(seq 20); do node --test out/test/node-services/build/buildQueue.test.js || break; done`),
  output recorded.
- `just check` passes; `just preflight` passes (on Windows, its static stage; constitution,
  section 4).
- The PR names the cause in a sentence (the test read the real clock for the build time and the
  mocked one for the debounce) and the commit is of type `test:` (no scope, per
  `.agents/guidelines/git-commit-allowed-scopes.md`).

## Open questions

None.
