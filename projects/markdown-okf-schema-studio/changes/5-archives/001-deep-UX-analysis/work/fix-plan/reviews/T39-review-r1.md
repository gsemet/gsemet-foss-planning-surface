# T39 review — round 1

Base: 0c5c352 · Reviewed diff: 4 files, +110/-2 (extension.ts, realInput.test.ts,
stockCoexistence.test.ts, README.md)

## Gates
- compile, unit, types: PASS (`logs/T39-{compile,unit,types}.log`).
- full: PASS, 218 s (`logs/T39-full.log`). It logs
  `RI-T39 case B (Explorer entry): opened in preview group = true, preview still active tab = false`.
- visual: PASS vs baseline, 0 new failure lines (`logs/T39-visual.log`).
- Red run: `logs/T39-red-trusted.log` fails at "Quick Open opened the file in the preview's group".
  This is the right failure.

The gates are green, but the screenshots show a regression that no gate checks (finding 1).

## Done-when
- [x] unit and full gates pass. Evidence: gate summary.
- [~] RI-T39 passes, but Case A asserts too little. It only checks "not the preview's column", so
  it passes when the file opens in a **new third group**. The RI-T39 screenshot shows exactly that
  (finding 1).
- [x] README sentence added, worded as the task asks.

## Protected features checked
- P-L1 (the side preview follows the active Markdown editor): RI-T39 Case A waits for
  `getActivePreviewForTests()` to follow `other-t39.md`. The screenshot shows
  "Studio · other-t39.md". Lifecycle and reload suites pass.
- P-L2 / P-L3 (reveal of an existing preview, restore): the existing-side-preview branch and
  deserialization are untouched. Reload suite passes.
- Custom editor flow: `resolvePreviewEditor` is untouched. stockCoexistence passes with the one
  amended assertion.

## Findings

1. **[BLOCKER]** `src/extension.ts`: `lockNewPreviewGroup`. **The lock outlives the preview and
   ends up on ordinary text-editor groups.**
   - Evidence 1: in `.artifacts/real-input-SlcpuC/38-edit-mode-remembered.png`, captured
     **before** RI-T39 runs, the left group holding `smoke.md` shows the lock icon. The preview group
     shows it too.
   - Evidence 2: in `39-quick-open-beside-preview.png`, both the `smoke.md` group and the preview
     group are locked. So Quick Open created a **third** group on the right, instead of using the
     source group. D-17 intends "land beside it", in the existing editor group.
   - Likely cause: earlier scenarios lock their new preview groups. When editors close, a locked
     group stays behind, for example as the last remaining group, and VS Code does not unlock it
     when its webview closes. Later, text editors open into that locked group.
   - User impact: a user who opens the preview, then closes the source editor and the preview, is
     left with a locked group. From then on, every file opened from that group creates a new split.
     This breaks normal editing, and nothing in the UI explains it beyond the small lock icon.
   - The RI-T39 `finally` block only unlocks the preview's group, so other locked groups remain for
     later suites.

   **Fix:**
   - In `lockNewPreviewGroup`, record that the extension locked the group: store `panel.viewColumn`
     on the preview, for example `preview.lockedColumn`, only when the lock command ran.
   - Unlock that group when the preview leaves it:
     - In the panel's `onDidDispose`, if `lockedColumn` is set and a group with that column still
       exists: remember the active group's column, focus the locked group with
       `workbench.action.focusNthEditorGroup` (or the `focusFirst…`/`focusSecond…` group commands,
       by column), run `workbench.action.unlockEditorGroup`, then restore focus to the remembered
       group. Wrap all of this in `try`/`catch`.
     - Do the same when `onDidChangeViewState` reports a new `panel.viewColumn`, which means the
       user dragged the preview elsewhere. Clear `lockedColumn` afterwards.
   - Tests, in RI-T39:
     - **(a)** At the start of the scenario, after opening `smoke.md` and before opening the
       preview, assert that Quick Open of a file from the `smoke.md` editor opens it **in the same
       group** and that `vscode.window.tabGroups.all.length` does not grow. This catches lock
       leaks from earlier scenarios.
     - **(b)** In Case A, replace `notEqual(openedIn, previewColumn)` with
       `equal(openedIn, sourceColumn)`, where `sourceColumn` is the column of `smoke.md`. Also
       assert `tabGroups.all.length === 2`.
     - **(c)** After Case A, close the preview tab, then run Quick Open again from the remaining
       editor. Assert that the file opens in that group and that no new group appears.
   - Optional (d): in `closeAllEditors`, the test helper, run `workbench.action.unlockEditorGroup`
     in every group, so one failing scenario cannot poison the next ones. Do this only as a backstop
     for (a)–(c), not instead of them.

2. **[MINOR]** `src/extension.ts`: the poll in `lockNewPreviewGroup`. It awaits up to 10 × 25 ms
   (250 ms) **before** `requestPreviewDocument`, so it can delay the first render and the return of
   `openPreview`.
   - In practice the group exists synchronously after `createWebviewPanel`, so the loop exits at
     once. Only the awaited `lockEditorGroup` command adds a round-trip. That is acceptable.
   - Fix: none required. Optionally, start the first render first and run the lock concurrently:
     `void lockNewPreviewGroup(panel)` before `await requestPreviewDocument(...)`.
   - The `try`/`catch` is correct: any error is swallowed and the render proceeds.

3. **[MINOR → follow-up, outside T39]** Case B (T36 Explorer entry), in `openPreview`. When the
   preview is focused, `showTextDocument(opened, { preview: false })` has no `viewColumn`, so it
   opens the file **in the preview's (locked) group** and covers the preview. Then
   `sidePreview.panel.reveal(vscode.ViewColumn.Beside)` runs relative to that now-active group.
   - Severity for a user: **medium**. Right-clicking a file in the Explorer and choosing the Studio
     preview is a primary entry point. Doing it while the preview has focus, which is common right
     after reading in it, buries the preview or shuffles it to another split. That is exactly what
     T39 claims to fix for Quick Open.
   - Logging instead of asserting is acceptable for T39: Case B's cause is T36 code outside the
     task's allowed scope, and the Quick Open path is the task's subject.
   - Follow-up fix:
     - In `openPreview`, when a side preview exists, pass
       `viewColumn: <the column of the most recent non-preview text editor group>` (fall back to
       `ViewColumn.One`) to `showTextDocument`.
     - Reveal the existing preview in its own `panel.viewColumn` with `preserveFocus: true`, not in
       `Beside`.
     - Turn the Case B `console.log` into two assertions: the file is not in the preview column,
       and the preview is still the active tab of its group.

4. **[NIT]** `realInput.test.ts`: `scenarioPreviewGroupLock` uses bare `setTimeout` sleeps (300,
   500, 200 ms). Prefer `waitFor` conditions where one exists, for example waiting for the Quick
   Open input to be visible.

## Existing assertions changed
- `stockCoexistence.test.ts`: the delayed Open With check uses `.find(... delayedDocument.uri ...)
  ?.isActive` instead of `[0].isActive`. This matches the amendment exactly; there are 6 changed
  lines, all in this hunk, and nothing else changed. **OK.**
- `realInput.test.ts`: additions only, plus the `COMMAND_ID` import. **OK.**

## Scope
- All files are allowed: three by the task, and stockCoexistence by the amendment. No churn.
- The lock is only applied in the new-panel branch, after `createWebviewPanel`, when `panel.active`
  is true and the group has exactly 1 tab. It is never applied for Open With, existing groups or
  deserialization. Correct as designed; the defect is the missing unlock (finding 1).

VERDICT: CHANGES REQUESTED
