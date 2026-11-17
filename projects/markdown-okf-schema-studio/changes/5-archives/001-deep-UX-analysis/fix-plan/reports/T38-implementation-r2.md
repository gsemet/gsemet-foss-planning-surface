# T38 implementation — round 2

STATUS: DONE

## Summary
Fixed `validEditMode` in `isPreviewSyncMessage` (`src/extension.ts`). It now requires a boolean `editMode` on
`previewEditModeChanged` and accepts `undefined` or a boolean on every other type (same rule as
`anchorToEditor`), so `previewState` messages (which always carry `editMode`) are accepted again.
I checked every other validation rule round 1 added: only the `previewEditModeChanged` type entry and
`validEditMode` were added; no other rule had the mistake.

## Files changed
- `src/extension.ts` (`validEditMode` only)
- `test/integration/realInput.test.ts` (RI-T38 assertion)

## Tests written first (failing before the fix)
The existing `previewEditing.test.ts` description scenario failed with round 1's rule (`logs/T38-full.log`:
"Timed out waiting for the host to record Description visibility"). The new RI-T38 assertion exercises the
same path. I did not reproduce the old behaviour again (no source swapping), so the new assertion was not
run red.

## Tests added or changed
RI-T38 (`scenarioToolbarState`): new step on the long-chapter fixture. Open a side preview, turn edit mode
on, wheel the preview with the mouse, then `waitFor` `getActivePreviewForTests()?.scrollTop > 0`. This proves
a `previewState` carrying `editMode: true` is accepted by the host.

## Existing assertions changed
None in this round (earlier amendments unchanged).

## Verification
`gate.sh T38-impl5 unit types contracts full`: compile, unit, types, contracts-compile, contracts and full
all PASS (full 213 s; log `logs/T38-impl5-full.log`). previewEditing and RI-T38 pass. The screen was
unlocked and no gate was running beforehand.

## Evidence for reviewers
`git diff src/extension.ts` around `validEditMode`; `logs/T38-impl5-full.log`.

## Feedback addressed (rounds 2–3)
Amendment "after the round-1 gate": validation rule corrected; RI-T38 scroll assertion added; other
round-1 validation checked.

## Open points / STOP reason
None.
