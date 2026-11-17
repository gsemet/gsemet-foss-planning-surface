# T39 implementation — round 1

STATUS: DONE

## Summary

The group lock and RI-T39 are implemented. After the amendment, `stockCoexistence.test.ts` has one
changed assertion and the `full` gate passes. Case B (Explorer entry) still opens the file in the
preview's group, so it is logged as an open point, not asserted.

## Files changed

- `src/extension.ts`: new `lockNewPreviewGroup(panel)`, called in
  `openPreview` right after `createPreview` in the new-panel branch, before the first render.
  - It polls up to 250 ms for the panel's tab group to appear.
  - It runs `workbench.action.lockEditorGroup` only when `panel.active` and the group has exactly
    one tab.
  - The whole body is in `try`/`catch`, so a failure never blocks the preview.
  - The existing-side-preview branch, `resolvePreviewEditor` (Open With) and deserialization are
    untouched.
- `test/integration/realInput.test.ts`: imports `COMMAND_ID`, adds
  `scenarioPreviewGroupLock` (RI-T39), and calls it at the end of `run()`.
- `test/integration/stockCoexistence.test.ts`: the one amended
  assertion (see below).
- `README.md`: one sentence in "Use the Preview".

## Tests written first (failing before the fix)

RI-T39 was written and run against the unchanged `extension.ts` with `gate.sh T39-red trusted`.
Log: `logs/T39-red-trusted.log`.

```
Real-input integration failed: AssertionError [ERR_ASSERTION]: Quick Open opened the file in the preview's group
  at scenarioPreviewGroupLock (out/test/integration/realInput.test.js:1943:20)
```

This is the Quick Open case (Case A). The suite stops at its first failure, so the red run did not
reach Case B (the Explorer entry).

## Tests added or changed

RI-T39 (`scenarioPreviewGroupLock`):

- Setup: three fixtures. I open the side preview on `smoke.md` and click inside the preview with
  `page.mouse`, then assert `panel.active`.
- Case A: `Meta+P`, type `other-t39.md`, `Enter`. It asserts:
  - the file opened in a column other than the preview's;
  - the preview is still the active tab of its group;
  - `getActivePreviewForTests()` follows the new document.
- Case B (the T36 follow-up): re-focus the preview, run `executeCommand(COMMAND_ID, thirdUri)`, and
  assert the same two things.
- `finally`: reveal the preview, run `workbench.action.unlockEditorGroup`, close all editors.
- Screenshot `39-quick-open-beside-preview`.

## Existing assertions changed

Authorised by the "Amendment after round 1 STOP" in the task file.

- `test/integration/stockCoexistence.test.ts`, delayed Open With check.
  - Old: `assert.equal(customEditorTabs(EDITOR_VIEW_TYPE)[0].isActive, true);`
  - New: the same assertion, but on the tab whose `TabInputCustom.uri` equals
    `delayedDocument.uri` (`.find(...)?.isActive`).
  - Reason: with the group lock, the earlier MyST editor shares the neighbouring group with the
    delayed one, so `[0]` is the earlier, inactive tab. The delayed tab is the one under test.
  - No other line of the file changed.

## Verification

- Earlier gate `T39-impl` (`unit types full visual`): unit PASS, types PASS, visual PASS vs
  baseline, full FAIL at the delayed Open With assertion (cause above).
- Final gate `T39-impl3 types full`: types PASS, **full PASS** (218 s), including RI-T39, lifecycle,
  coexistence, standalone and reload. The log is `logs/T39-impl3-full.log`.
- The intermediate run `T39-impl2` failed only at RI-T39 Case B (below); RI-T39 Case A had passed.
- Screen unlocked and no gate running before each run.

## Evidence for reviewers

- Red log: `logs/T39-red-trusted.log`.
- Impl logs: `logs/T39-impl-{compile,unit,types,full,visual}.log`.
- Visual screenshots copy: `logs/visual-T39-impl/`.
- The remaining `Code Helper` processes belong to the user's own VS Code. I started no background
  command.

## Open points / STOP reason

No STOP. One open point, from the orchestrator's extra sub-case (T36 follow-up):

- **RI-T39 Case B fails even with the lock.** With the preview focused,
  `executeCommand(COMMAND_ID, otherUri)` opens the file in the preview's group and the preview
  stops being the active tab. Observed: `opened in preview group = true, preview still active tab =
  false`.
  - The cause is `openPreview`'s `showTextDocument(opened, { preview: false })` with no
    `viewColumn`. Per the orchestrator's note I did not change it.
  - The test therefore logs the Case B outcome with `console.log` (see `logs/T39-impl3-full.log`)
    and does not assert it. Case A (Quick Open) is asserted and passes.
  - A follow-up could pass an explicit `viewColumn` (the source group) in that call and then turn
    the log into assertions.
