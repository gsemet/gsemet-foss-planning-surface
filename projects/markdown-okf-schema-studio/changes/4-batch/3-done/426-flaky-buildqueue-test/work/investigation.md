# CR-426 investigation: flaky build queue test

Base: `origin/chantier/batch-06/cr-351-...` at 80940a3, worktree `batch-06-CR-426`. Read only; nothing run.

## Files and entry points

- `src/core/render/buildQueue.ts`: the queue. `startPending()` sets `startedAt: Date.now()` (l. 364)
  then calls `run()`, which calls `build()` synchronously; on success `run()` sets
  `lastBuildMs = Date.now() - active.startedAt` (l. 420-422, no `durationOf` in these tests).
  `currentDebounceMs()` (l. 180-183) returns `2 * lastBuildMs` once it is >= 10 ms
  (`MIN_ADAPTIVE_BUILD_MS`), and `request()` arms its timer with that wait (l. 216-219).
- `src/node-services/build/buildQueue.ts`: a subclass that only adds `canonicalize`; no clock code.
- `test/node-services/build/buildQueue.test.ts`: the only file to change.

## Cause confirmed

The spec's cause is correct at this base. Test "still renders a build whose buffer already moved
on..." (l. 93-123) mocks only `setTimeout` (l. 94). If 10 ms or more of real time pass between
`startedAt` and the `Date.now()` in `run()` after the first build resolves, the second request's
timer is armed at 20 ms+ on the mocked clock; `tick(0)` (l. 119) does not fire it, so `dispose()`
finds it pending (l. 121 passes) and no build is active to abort: `assert.equal(aborted, true)`
(l. 122) fails with `false !== true`.

## No product race

In production `Date.now()` and `setTimeout` run on the same real clock: a 20 ms+ wait after a
10 ms+ build is SwRS-MDOKFSTUDIO-LIFE-039's adaptive wait, and canceling a pending request at
dispose is correct. The failure needs the two clocks to disagree, which only the test does. The
owner's "fix the code" answer does not apply; no `src/` change.

## Other tests of the file (same two-clock flaw?)

Only `setTimeout` is mocked in tests at l. 25, 64, 93, 126, 142, 165, 197. Checked each:

- l. 64 "retains a successful result as stale...": same flaw (spec names it). After build 1 is
  ready, request 2 arms `currentDebounceMs()`; `tick(0)` at l. 83 then may not start it and
  `assert.ok(pending.has(2))` (l. 84) fails.
- l. 25 "lets an in-flight build finish...": safe. Requests 2 and 3 are made while build 1 runs,
  before any `lastBuildMs`, so their wait is 0; request 3's timer fires at l. 44, `startPending`
  returns (no overrun limit yet), and `drainPending()` starts it when build 1 ends: no new wait.
- l. 126, 197: one build, no request after it relies on a wait (l. 216 is after dispose).
- l. 142: no build ever runs.
- l. 165: build 1 is canceled, so `run()` returns before setting `lastBuildMs`; request 2 waits 0.
- l. 220, 254, 291, 344, 366 already mock `["setTimeout", "Date"]`.

So exactly the two tests the spec names; no third.

## Smallest change

As the spec's "What changes": in the tests at l. 64 and l. 93, `apis: ["setTimeout", "Date"]`, a
one-line comment at the first such line (the adaptive wait reads `Date.now()`; the debounce runs on
the mocked clock), and a busy-wait of >= 15 ms on `performance.now()` in each build stub before it
returns its promise (counted, since `build()` is called synchronously after `startedAt`), with a
one-line comment. No assertion, name or `@tests_req` change. `performance` is a Node global
(not touched by the `Date` mock), so no import is needed; check the tsconfig `lib` accepts it if
the compile complains.

## Risks

- None on values other code measures from: no product value changes.
- The busy-wait adds about 30-60 ms to the file's run (two builds per test, two tests).
- Mocking `Date` sets the mocked epoch to 0; neither test reads dates, so no effect.

## Questions for the user

None.

## Evidence plan

Kind: test-only fix of a flake; nothing to see in the UI. Shown by command output, recorded in a
`*.log` under `work/gates/` and summarised in `evidence/`:

1. Before: at the base, step 3 alone (busy-wait in the two stubs, only `setTimeout` mocked):
   `fnm exec -- npm run compile`, then `node --test out/test/node-services/build/buildQueue.test.js`;
   expected: both tests fail (`false !== true` for l. 93's test, `pending.has(2)` for l. 64's).
2. After: full change, recompile, the same command 20 times in a row
   (`for i in $(seq 20); do node --test out/test/node-services/build/buildQueue.test.js || break; done`),
   all pass.
3. `just check` passes.
4. `just preflight`, its static stage on Windows (constitution, section 4), passes.

Cannot be shown: that the original once-in-a-run flake will never recur under other load; the
busy-wait makes the old failure deterministic and stands in for it.
