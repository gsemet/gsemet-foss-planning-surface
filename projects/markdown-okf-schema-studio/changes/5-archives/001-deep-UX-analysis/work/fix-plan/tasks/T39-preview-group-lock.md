# T39 — Files opened while the preview has focus do not bury it

| Field | Value |
| --- | --- |
| Fixes | [UX-27](../../05-preview-lifecycle/UX-27-quick-open-covers-preview.md) |
| Decisions | D-17 |
| Depends on | T38 |
| Gate | `unit full` |
| Risk | Medium (changes the editor-group behaviour users see; P-L1) |
| Commit message | `fix(vscode): lock the side preview's editor group` |

## Goal

When the side preview creates its own editor group, that group is **locked** with VS Code's
standard "Lock Group" feature. Files opened while the preview has focus (Cmd+P, links, explorer)
then land in another group, and the preview stays visible. The user can unlock it from the group's
lock icon.

## Context to read first

- `src/extension.ts` → `openPreview` (the `createWebviewPanel(… ViewColumn.Beside …)` branch, and
  the branch revealing an existing side preview).
- VS Code commands: `workbench.action.lockEditorGroup` locks the **active** group. Right after
  `createWebviewPanel` with focus, the active group is the panel's group.

## Allowed files

- `src/extension.ts`
- `test/integration/realInput.test.ts` (add RI-T39)
- `README.md` (one sentence)

## Steps

1. Write RI-T39 first and record the failure.
2. In `openPreview`, after a **new** side panel is created and before awaiting the first render:
   - when the panel's group contains only this panel
     (`vscode.window.tabGroups.all.find((group) => group.viewColumn === panel.viewColumn)?.tabs.length === 1`)
     **and** the panel is active (`panel.active`), call
     `await vscode.commands.executeCommand("workbench.action.lockEditorGroup")`;
   - wrap it in `try`/`catch`: a failure must never block the preview.

   Do not lock groups for the Open With custom editor, for existing groups, or on deserialization:
   VS Code restores lock state itself.
3. README, "Use the Preview": "The side preview locks its editor group so files you open land
   beside it; click the lock icon on the group to unlock it."

## Tests

**Real-input E2E**, scenario **RI-T39**:

- Open the side preview on fixture A, and click inside the preview to give it focus.
- Press `${MOD}+P`, type the fixture B file name, press `Enter`.
- Assert:
  - B opened in a group **other** than the preview's;
  - the preview's group still has the preview as its active tab;
  - `getActivePreviewForTests()` shows B, because the side preview follows the active Markdown
    editor (P-L1).

**Full integration gate:** lifecycle, coexistence, standalone and reload suites must pass
unchanged. Some tests open documents in `ViewColumn.Beside` or `Active`. If one now behaves
differently because of the lock, STOP and report: the lock may conflict with test assumptions or
with real workflows.

## Expected changes to existing tests

None expected.

## Must not change

- P-L1 to P-L3. The custom editor flow.

## Done when

- The `unit` and `full` gates pass; RI-T39 passes.

## Amendment after round 1 STOP (orchestrator, 2026-10-13)

The orchestrator probed `stockCoexistence.test.ts` in a scratch worktree, with and without the
lock, and dumped `vscode.window.tabGroups` (logs `scratchpad/probe-t39-*.log`, not committed).
- **Without the lock**, the first `vscode.openWith(preview.md)` lands in the side preview's own
  group and covers it. That is the UX-27 bug.
- **With the lock**, it lands in the neighbouring group, and the side preview stays visible. That
  is the intended D-17 behaviour.
- The failing assertion is the **delayed** Open With check:
  `assert.equal(customEditorTabs(EDITOR_VIEW_TYPE)[0].isActive, true);`, just after
  `const delayedPreview = getActivePreviewForTests(); assert.ok(delayedPreview);`.
  With the lock, the earlier MyST editor of `preview.md` shares group 2 with the delayed one, so
  `[0]` is that earlier, inactive tab. The delayed `preview-other.md` MyST tab is active in both
  runs.

Add `test/integration/stockCoexistence.test.ts` to the Allowed files for this one change only.
That assertion must target the delayed document's tab:

```ts
assert.equal(
  customEditorTabs(EDITOR_VIEW_TYPE).find((tab) =>
    (tab.input as vscode.TabInputCustom).uri.toString() === delayedDocument.uri.toString())?.isActive,
  true,
);
```

Keep every other line of that file unchanged, including the first Open With check, where
`length === 1` makes `[0]` correct. List the change in the report. Any other failure in an existing
suite is still a STOP.

## Amendment after the round-1 review (orchestrator, 2026-10-13)

Review r1 (`reviews/T39-review-r1.md`) found a lock leak. The orchestrator confirmed it on
`.artifacts/real-input-SlcpuC/38-edit-mode-remembered.png`: the `smoke.md` group shows the lock icon
before RI-T39 even runs. Here is how it happens:
- the preview's group is the last group left (the source editor was closed first, or
  `closeAllEditors` ran);
- the preview then closes;
- VS Code keeps that empty group, and it stays locked;
- every later file opens in a new split.

Round 2 must do all of the following. `src/extension.ts`, `test/integration/realInput.test.ts` and
`README.md` stay the only files you change, apart from the stockCoexistence line already allowed.

1. **Unlock on dispose.**
   - Add `lockedColumn?: vscode.ViewColumn` to the preview record. Set it only when
     `lockNewPreviewGroup` actually ran `workbench.action.lockEditorGroup`.
   - In the existing `onDidChangeViewState` handling, keep `lockedColumn` equal to
     `panel.viewColumn` whenever it is defined. The column shifts when a group on the left closes,
     but the locked group is the same one.
   - In the panel's dispose path:
     - if `lockedColumn` is set, wait one tick (`setTimeout` 0);
     - if `vscode.window.tabGroups.all` still has a group with that `viewColumn`:
       - remember the active group's `viewColumn`;
       - focus the locked group with the `workbench.action.focusFirstEditorGroup` …
         `focusEighthEditorGroup` command matching its column (columns above 8: skip);
       - run `workbench.action.unlockEditorGroup`;
       - focus the remembered column again the same way, if it differs.
     - Wrap all of it in `try`/`catch`; never throw from dispose.
   - `unlockEditorGroup` is idempotent, so running it on a group that is not locked is harmless.
   - Do not add any other unlock trigger, such as drag handling.
2. **Explorer / menu path (Case B; T39's goal lists "explorer").** In `openPreview`, when `uri` must
   be opened and a side preview exists (`latestPreview((preview) => preview.followsActiveEditor)`),
   pass a `viewColumn` to `showTextDocument`, chosen in this order:
   - the `viewColumn` of the first `vscode.window.visibleTextEditors` entry whose column is not the
     side preview's `panel.viewColumn`;
   - otherwise the first `tabGroups.all` group whose column is not the preview's;
   - otherwise `vscode.ViewColumn.Beside`.

   With no side preview, keep `{ preview: false }` exactly as today.

   In the existing-side-preview branch, change `sidePreview.panel.reveal(vscode.ViewColumn.Beside)`
   to `sidePreview.panel.reveal(sidePreview.panel.viewColumn ?? vscode.ViewColumn.Beside)`.
   `Beside` is relative to the active group: with the preview focused, it moves the preview into a
   new group. Do not add `preserveFocus`.
3. **Optional:** start the first render without waiting for the lock. You may call
   `void lockNewPreviewGroup(panel, preview)` before `await requestPreviewDocument(...)`. Make sure
   `lockedColumn` is still set correctly.

### Tests (RI-T39, in `realInput.test.ts`)

- **(a) Leak canary.** At the start, after `smoke.md` is open and before the preview opens, use
  Quick Open from the `smoke.md` editor to open another fixture. Assert that it opens in the same
  group and that `tabGroups.all.length` does not grow. Close it again.
- **(b) Case A precision.**
  - Replace `notEqual(openedIn, previewColumn)` with `equal(openedIn, sourceColumn)`, where
    `sourceColumn` is the column of `smoke.md`.
  - Assert `tabGroups.all.length === 2`.
- **(c) Case B asserted.** Turn the Case B log into assertions:
  - the file is not in the preview's column;
  - the preview is still the active tab of its group;
  - `tabGroups.all.length === 2`.
- **(d) Unlock after close.**
  - Close the preview tab.
  - Run Quick Open from the remaining editor: the file opens in that group, with no new group.
  - Then also check the last-group case: close every text editor so the preview's group is the
    only one left, close the preview, open a fixture with `showTextDocument`. Assert
    `tabGroups.all.length === 1`.
- **(e) Backstop.** In the `finally` block, keep the unlock. Replace bare `setTimeout` sleeps with
  `waitFor` conditions where one exists (review NIT 4).

Do not add an unlock to the shared `closeAllEditors` helper: (a) must stay able to catch a leak.
Write the tests first and record that (a) or (d) fails against round 1.

Any other failure in an existing suite is still a STOP.

## Amendment after the round-2 review (orchestrator, 2026-10-13) — round 3, the last round

Apply `reviews/T39-review-r2.md` findings 1 to 5 as written, with the precisions below. The files
stay the same: `src/extension.ts`, `test/integration/realInput.test.ts` and `README.md`. Do not touch
`reload-suite.ts` or `serializer.test.ts`.

- **Finding 1: only empty groups are ever unlocked.**
  - The poll waits only while the group at `column` still holds a `TabInputWebview` tab of the
    preview's own view type (`PANEL_VIEW_TYPE`). Match on `viewType` with `includes`, because VS
    Code prefixes it.
  - Targets are the group at `column` if it has 0 tabs. Otherwise they are every group with 0 tabs
    and no live preview.
  - Remove `adoptGroupLock`. Add RI-T39 (f) exactly as the review describes.
- **Finding 2: restored previews.**
  - In `deserializePreviewPanel`, once the restored record exists and is a side preview
    (`followsActiveEditor`), set `lockedColumn = panel.viewColumn` when it is defined.
  - Test it in RI-T39, without a window reload, through the existing
    `deserializePreviewPanelForTests` seam:
    1. Create a webview panel of `PANEL_VIEW_TYPE` in `ViewColumn.Beside`.
    2. Lock its group with `lockEditorGroup`, as the workbench would restore it.
    3. Call `deserializePreviewPanelForTests(panel, <a valid state for smoke.md>)`. Build the state
       the way the existing tests build one; look in `serializer.test.ts` and the reload suite.
    4. Close every text editor so the panel's group is the last group, then close the panel.
    5. `showTextDocument` a fixture and assert `tabGroups.all.length === 1`.
  - Record that this sub-case fails without the `deserializePreviewPanel` change.
  - If the seam cannot build a side preview this way, STOP and explain. Do not add a new export.
- **Finding 3:** skip the focus restore when `remembered` was a target, and add the comment.
- **Finding 4:** in (d), assert `=== sourceColumn` and add the settle-wait comment.
  - Show that the last-group sub-case of (d) fails against round 1's unlock-less code: run it once
    with canary (a) commented out, then restore (a).
  - Record the log path. Do not leave (a) commented out.
- **Finding 5:** add the README sentence. The lock is released when the preview closes.

Verification: `PLAN/scripts/gate.sh T39-impl3 unit types full`. This is the last allowed round. If
something cannot be made green without touching more files, STOP and report, rather than widening
the scope.
