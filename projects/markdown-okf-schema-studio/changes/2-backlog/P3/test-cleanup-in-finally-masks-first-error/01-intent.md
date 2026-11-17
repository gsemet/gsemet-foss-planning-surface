# Test cleanup in `finally` can mask the first error

Type: test hygiene · Priority: P3 · Filed 2026-11-01 from CR 222 and CR 228 reviews

## Today

Cleanup steps that click and wait inside `finally` can throw their own timeout and replace the
original assertion error in the report. Known places:
- `test/integration/radioChoice.test.ts` around :196-197: `setEditMode(page, true)` in the `finally`
  (CR 222 reviews also named the `openEditorGuard` `finally`, which presses Escape and waits for the
  editor to close).
- `wideTableTab.ts:171-174` (`setWidthMode(page, "margin")`) and the c7-1 inner `finally`
  (`clickToolbarCollapse`) in `qa210Replays.ts`.
- Other places with the same pattern: details to confirm with a grep for `finally` in
  `test/integration`.

## Expected

A shared helper runs the cleanup, logs its own error, and rethrows the first error. Or skip the
cleanup when the body already threw.

Proof: a scenario that fails on purpose reports its own assertion, not the cleanup timeout.
