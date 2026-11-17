# T38 — Toolbar state: anchor without an editor, persisted edit mode, clearer icon

| Field | Value |
| --- | --- |
| Fixes | [UX-33](../../07-discoverability-and-chrome/UX-33-toolbar-state-in-open-with-editor.md) |
| Decisions | D-16 |
| Depends on | T37 |
| Gate | `unit trusted reload` |
| Risk | Medium (P-L3 reload restoration of edit mode; P-N2 anchor toggle) |
| Commit message | `fix(vscode): reflect scroll pairing in the toolbar and remember edit mode` |

## Goal

- **Anchor button.** It is **disabled**, with the tooltip `No text editor shows this file`, when no
  visible text editor shows the previewed document (typically the Open With editor alone). It
  becomes enabled again as soon as one does.
- **Edit mode survives reopening.** Toggling edit mode stores the choice per workspace. A **new**
  webview (a new preview, or Open With) starts in that mode. An existing webview's own saved state
  (reload restoration) still wins. Read-only previews never start in edit mode.
- **Anchor icon.** A chain-link icon replaces the padlock; the tooltips are unchanged.

## Context to read first

- `src/webview/scrollSync.ts`:
  - `savedState`, `let editMode = savedState?.editMode === true`, `applyEditMode`;
  - `applyAnchorMode`, `anchorButton`;
  - the edit toggle's click listener.
- `src/extension.ts`:
  - `scrollContext` (it adds runtime context fields);
  - `previewDescriptionStorage` / `previewThemeModeStorage` (the pattern for `workspaceState`);
  - `visibleEditorFor`, `activate` (event subscriptions);
  - `isPreviewSyncMessage`.
- `src/preview/previewToolbar.ts` → `ANCHOR_BUTTON`.

## Allowed files

- `src/webview/scrollSync.ts`
- `src/extension.ts`
- `src/preview/previewToolbar.ts`
- `test/webview/scrollSync.test.ts`, `test/webview/previewStyles.test.ts` (only if it asserts the
  anchor icon markup)
- `test/integration/realInput.test.ts` (add RI-T38; and the teardown change below)

**Added after the T02 review (F3).** Once edit mode persists per workspace, a suite that leaves it
on changes how the next suite starts. In `realInput.test.ts`, every scenario's `finally` block must
call `setEditMode(page, false)` before `closeAllEditors()`. Check also that the checkbox suite and
`previewEditing.test.ts` do not depend on edit mode being off at start; if one does, STOP and
report it (those files are not in the allowed list).
- `README.md` (one sentence)

## Steps

1. **Pairing.**
   - Add `pairedTextEditor?: boolean` to `PreviewRuntimeContext`. `scrollContext` sets it to
     `visibleEditorFor(preview) !== undefined`; pass the preview, or the value, to `scrollContext`.
   - In `activate`, subscribe to `vscode.window.onDidChangeVisibleTextEditors`. For each preview
     with a stage, post
     `{ type: "previewPairing", documentId, documentVersion, requestId, pairedTextEditor }`.
   - Runtime, `applyPairing(paired)`:
     - `anchorButton.disabled = !paired`;
     - when not paired, set `title`, `data-tooltip` and `aria-label` to
       `No text editor shows this file`;
     - when paired, restore them via `applyAnchorMode(anchorToEditor)`.

     Call it at init with `context.pairedTextEditor !== false`, and on `previewPairing`.
2. **Edit mode persistence.**
   - Add `initialEditMode?: boolean` to the context. The host reads it from
     `workspaceState.get("markdownOkfSchemaStudio.editMode")` and passes it only when
     `!preview.readOnly`.
   - Runtime:
     `let editMode = editModeButton ? (typeof savedState?.editMode === "boolean" ? savedState.editMode : context.initialEditMode === true) : false;`.
   - On toggle, post `{ type: "previewEditModeChanged", …ids, editMode }`. Validate it in
     `isPreviewSyncMessage`: a boolean, on this type only. The host stores it with
     `workspaceState.update`.
3. **Icon.** Replace the padlock SVG in `ANCHOR_BUTTON` with a chain-link icon: two rounded links,
   24×24 viewBox, the same stroke style as the other toolbar icons.
4. README, near the toolbar description: "The anchor button is disabled when no text editor shows
   the file. Edit mode is remembered for the workspace."

## Tests

**Unit:**

- `pairedTextEditor: false` → the anchor button is disabled, with the tooltip; a `previewPairing`
  message with `true` re-enables it.
- No saved state and `initialEditMode: true` → edit mode is on at start.
- Saved state `editMode: false` wins over `initialEditMode: true`.
- No edit toggle (read-only) → edit mode off, whatever the context says.
- Toggling posts `previewEditModeChanged`.

**Real-input E2E**, scenario **RI-T38**:

- Open a fixture with `openStudioEditor` while no text editor shows it: close the text editor tab
  first. The anchor button is disabled.
- Then show the text editor beside → the anchor button becomes enabled.
- Turn edit mode on in a side preview, close the preview, reopen it → edit mode is on.

**Reload gate:** restoration of edit mode after Reload Window must still pass unchanged.

## Expected changes to existing tests

- Any assertion on the anchor button's padlock SVG markup. List it.
- No other expected changes.

**Amended by the orchestrator after round 1 (STOP, test mechanics).** Step 2 makes every
edit-toggle click post `previewEditModeChanged`. In `test/webview/scrollSync.test.ts`, test
"turning edit mode off saves a changed block editor and ignores an unchanged one", replace only
`assert.equal(unchanged.messages.length, messageCount);` with:

```ts
assert.deepEqual(
  unchanged.messages.slice(messageCount).map((message) => message.type),
  ["previewEditModeChanged"],
);
```

The test still proves that no save or cancel is posted for an unchanged editor. It also checks that
the only new message is the mode change. Leave every other assertion in that test unchanged. Keep
the synchronous post; do not defer it with a timer.

## Must not change

- Anchor toggle semantics when enabled (P-N2), reload restoration (P-L3), and the read-only
  posture (P-E8).

## Done when

- The `unit`, `trusted` and `reload` gates pass; RI-T38 passes.

## Amendment after round 1 STOP 2 (orchestrator, 2026-10-13)

The scroll suite's solo half (`test/integration/scroll-sync-suite.ts`, loop
`for (const withSource of [false, true])`, `withSource === false`: Open With editor only, no
visible text editor) clicks the anchor button in `solo-*-anchored`. With D-16 that button is
disabled there, by design. In the solo half, "anchored" asserts nothing beyond the button state:
there is no source to follow. Add `test/integration/scroll-sync-suite.ts` to the Allowed files for
these changes only:

- `if (anchored) await anchorButton.click();` becomes
  `if (anchored && withSource) await anchorButton.click();`.
- `assert.equal(await anchorButton.getAttribute("aria-pressed"), String(anchored));` keeps its
  exact form when `withSource` is true. When `withSource` is false, assert instead:
  - `await anchorButton.isDisabled() === true`;
  - `await anchorButton.getAttribute("title") === "No text editor shows this file"`;
  - `aria-pressed === "false"`.
- Keep the scenario names, the scrolling loop, the captures and every other assertion unchanged.
  List the change in the report.

Any other failure in an existing suite is still a STOP.

## Amendment after round 1 STOP 3 (orchestrator, 2026-10-13)

Same class as STOP 2. In the runtime, `anchorToEditor` only decides whether the preview leads a
text editor (`leadsEditor`). With no visible text editor it has no effect. T38 keeps the internal
state and restores it through `applyAnchorMode` once a text editor shows the file again. Every
anchor click or anchor-state assertion in `test/integration/scroll-sync-suite.ts` that runs while
no visible text editor shows the document follows the D-16 rule. Allowed changes, in that file
only:

- `capture()`, check "checkpoint sync control": the expected value becomes
  `String(!scenario.includes("independent") && vscode.window.visibleTextEditors.length > 0)`.
  Keep the message text. The `sync:` field written into the checkpoint stays derived from
  `state.anchored`.
- `runBlockNavigation`: replace
  `if (await anchorButton.getAttribute("aria-pressed") !== "true") await anchorButton.click();`
  with `assert.equal(await anchorButton.isDisabled(), true);`. The fixture is opened with Open With
  only.
- The keyboard-navigation callback:
  `assert.equal(await keyboardFrame.locator("[data-sphinx-preview-anchor]").getAttribute("aria-pressed"), "true");`
  becomes `"false"`. Add `assert.equal(await keyboardFrame.locator("[data-sphinx-preview-anchor]").isDisabled(), true);`.
- Nothing else in that file changes. If another anchor-related assertion in a paired (text editor
  visible) context fails, that is a STOP.

## Amendment after the round-1 gate (orchestrator, 2026-10-13)

Step 2 said to validate `editMode` as "a boolean, on this type only". That is wrong. The runtime's
`stateSnapshot()` has always put `editMode` (a boolean) into every `previewState` message.
Round 1's `validEditMode` (`editMode === undefined` for every other type) makes
`isPreviewSyncMessage` reject every `previewState`. The host then loses `descriptionsCollapsed`,
`scrollTop`, `sourceLine` and the rest. The full gate shows it: `previewEditing.test.ts`,
"Timed out waiting for the host to record Description visibility" (`logs/T38-full.log`). The
correct rule, the same as `anchorToEditor`:

- `previewEditModeChanged`: `editMode` must be a boolean;
- any other type: `editMode === undefined || typeof editMode === "boolean"`.

Add a unit or contract test that fails with round 1's rule:
- a `previewState` message carrying `editMode: true` (plus `descriptionsCollapsed: true`) passes
  `isPreviewSyncMessage`;
- it is applied by the host, if a seam exists. The contract tests in `test/contracts` already
  exercise `isPreviewSyncMessage`; check there first.

Also check every other field that round 1 added to validation for the same mistake.

Test precision (orchestrator): `isPreviewSyncMessage` is not exported, and no unit or contract test
reaches it. Do not add an export or a new seam. The regression test is:
- the existing `previewEditing.test.ts` description scenario: it fails with round 1's rule
  (`logs/T38-full.log`) and must pass after the fix;
- a new assertion in RI-T38. With edit mode on in a side preview, scroll the preview by a mouse
  wheel. Then `waitFor` until `getActivePreviewForTests()?.scrollTop` reflects the new position
  (> 0). This proves a `previewState` carrying `editMode: true` is accepted.
