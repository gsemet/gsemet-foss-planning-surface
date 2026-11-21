## Summary

Two tests of the preview manager depended on wall-clock time: a join-window test that sometimes failed with `2 !== 1` on a loaded machine, and a hidden-panel test that waited fixed times. A render can be joined during the 250 ms window after it ends, so a stall of about 210 ms between two requests closed the window and the second preview rendered again. That is the product working as specified; the fault was in the test.

The tests now control time with node:test fake timers instead of waiting, so a loaded machine gives the same result as an idle one. The product does not change.

## Deliverables

Test-only change in `test/session/previewManager.test.ts`.

| Test | Before | After |
| --- | --- | --- |
| a page refresh inside the join window renders again instead of joining the shared render | real timers, `requestDocument` awaited, `wait(100)` | fake timers, `advance(40)` steps, asserts `renders.length` and `sharedRenders.started` |
| a hidden panel does not render until it is shown, then renders once | `wait(150)`, `wait(200)` | no tick while hidden, then ticks past the 1000 ms max debounce and the 250 ms window, counts renders, `started` and results |
| a stalled machine between two requests does not close the join window (new) | none | the same scenario with `sourceExists` busy-waiting 260 ms of real time once |

The fixture's `wait(ms)` helper is gone; `advance(ms)` moves the fake clock and lets promise chains settle with event-loop turns, never a timed sleep.

## Blast radius

Grade: 1. Only a test file changes; `git revert` restores the previous test.

## Autonomous decisions

- Fake timers (`mock.timers`) rather than an injectable window: no `src/` change was needed.
- Added a permanent stall test, so the file proves on its own that a stall cannot change the outcome.

## Known gaps

- **UNVERIFIED:** the three local mutation checks (a double render after the first refresh of a shown hidden panel, `deferWhileHidden` returning false, and `invalidate()` at the start of `requestDocument`) did not run: the automated permission check refused the edits to `src/`. The proof that the tests catch a real regression is test-side: the old test fails with `2 !== 1` under a 260 ms stall, the new one passes, and 20 parallel runs gave 0 failures.

<details>
<summary>Details</summary>

## Changes

- `renderFixture` enables fake `setTimeout` and `Date`, resets them in `cleanup()`, and exposes `settle` and `advance`.
- The join-window scenario is shared by the original test and the stall test; it also asserts `manager.sharedRenders.started`, which counts only this manager's renders.
- The hidden-panel test asserts no render before and after ticking past every timer while hidden, then exactly one render, one result and a clean `renderDirty` once shown.

## Impacts

No visual change; no product change. The tests no longer flake under load.

## Test plan

- [ ] New or changed tests (the join-window test fails at the base under a 260 ms stall with `2 !== 1`, and passes now with a 270 ms stall)
- [ ] Requirements: No behaviour change (SwRS text and markers unchanged)
- [ ] Changelog: No user-facing change
- [ ] Local gates at `d0e9689` (carried from `e77cf0b`): `just check` exit 0; `just preflight` pass; compiled test file 9 pass, 0 fail; 20 parallel runs of the compiled file, 20 ok, 0 fail; no `wait(` or sleep left in the file
- [ ] Evidence: before at `f5d1637`, after at `d0e9689`
- [ ] Review: approved at `d0e9689` (carried from `078e283`)
- [ ] Verified at `d0e9689`
- [ ] CI green at `d0e9689`

## Internal references

CR-452 the join-window and hidden-panel tests control time instead of waiting.

</details>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
