# T31 implementation — round 3

## Change (review r2, finding 1, option a)
- `src/extension.ts`: new `ActivePreview.restoreCalls` (initialised to 0 in `createPreview`).
  `restorePreviewState` increments it as its first statement, so **every call is counted**, including
  calls where `scrollPreviewWithEditor` is off or no editor is visible. Exposed as
  `restorePreviewStateCalls: number` in `getActivePreviewForTests()`. Test hook only; no behaviour change.
- `test/integration/realInput.test.ts` (additions only, no existing assertion modified):
  - RI-T31b: counter recorded before `panel.reveal`; after the panel is visible the test
    `waitFor`s `restorePreviewStateCalls >= before + 1`. The anchor-distance assertion is kept.
  - RI-T31 case A: counter recorded before the click into the editor; after click and typing,
    `assert.strictEqual(count, before)`.
- No temporary source edits were made.

## Why the assertions have failing power (by reasoning)
- RI-T31b: the only caller of `restorePreviewState` on a hidden to visible transition is the
  `becameVisible` branch of `onDidChangeViewState`. The other caller (~line 2558) is an unrelated
  path that does not run in this scenario. If the branch were removed, the counter would not
  increase after `panel.reveal`, so the `waitFor` would time out and the test would fail, whatever
  the hidden webview received via `sourceScroll`.
- Case A: the old code called `restorePreviewState` on every `onDidChangeViewState` where the panel
  is visible, and clicking into the editor deactivates the panel (active true to false), which fires
  that event while `visible` stays true. The counter would then rise by at least 1, so the
  `strictEqual` would fail. With H1 the counter stays unchanged. It did not increase in the run
  (no STOP condition).

## Gate
`PLAN/scripts/gate.sh T31-impl3 unit types full`: compile, unit, types, full all PASS
(logs `logs/T31-impl3-*.log`). Screen was unlocked.
