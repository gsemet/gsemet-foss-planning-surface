## Summary

The build queue test "still renders a build whose buffer already moved on, and cleans up on
dispose" failed once in a `just check` run (`false !== true`) and passed before and after. The
cause is in the test, not in the queue: the test read the real clock for the build time and the
mocked clock for the debounce. This change makes both tests that share that flaw read one clock,
and makes the flaw fail every run instead of once in a while.

## Deliverables

The queue sets its next wait from the last build's time, read with `Date.now()`
(`src/core/render/buildQueue.ts`). The test mocked only `setTimeout`, so on a loaded machine a
first build of 10 ms of real time made the second request wait 20 ms or more on the mocked clock.
`tick(0)` then did not start it, `dispose()` cancelled it as pending, and nothing was aborted.

| | Clock of the debounce | Clock of the build time | Second request at `tick(0)` |
| --- | --- | --- | --- |
| Before | mocked | real | pending when a build takes 10 ms or more of real time |
| After | mocked | mocked | started: the build takes no time on the test's clock |

## Changes

- `test/node-services/build/buildQueue.test.ts`, tests "still renders a build whose buffer
  already moved on, and cleans up on dispose" and "retains a successful result as stale after a
  failed newer build": mock `["setTimeout", "Date"]` instead of `["setTimeout"]`, with a comment
  saying why.
- In both tests the build stub busy-waits 15 ms of real time (`performance.now()`) before it
  returns, so removing `"Date"` from the mock fails both tests at once.
- No assertion, test name or requirement marker changes; no product code changes.

## Impacts

No user-facing change; the test suite no longer depends on the machine's load for these two
tests.

## Blast radius

Grade: 1. One test file; a plain `git revert` restores the previous tests.

## Test plan

- [x] New or changed tests (they fail on the previous code), verified at cc3a627: with the
      busy-wait alone (only `setTimeout` mocked),
      `node --test out/test/node-services/build/buildQueue.test.js` fails both tests (2 of 12:
      `false !== true`, and `assert.ok(pending.has(2))`); with the full change the file passes
      20 runs in a row.
- [x] Requirements: No behaviour change.
- [x] Changelog: No user-facing change.
- [x] Local gates (Windows) at cc3a627: `just check`; `just preflight` (static stage, which runs
      `just check`).
- [x] Review: approved at cc3a627 (carried from ac487ff: same patch, rebased onto `main`)
- [x] CI green at cc3a627: checks, static, static-windows, visual and report pass; the real
      VS Code jobs (integration, stress) do not run on a pull request.

## Known gaps

None.

## Internal references

- CR-426 flaky-buildqueue-test; verification at cc3a627: `work/verify.md`, with the logs
  `work/verifier/before-busywait-setTimeout-only.log` and `work/verifier/after-20-runs.log`.
