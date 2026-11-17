# T25 review — round 2

Base: d67a757 · Focus: round-1 Finding 1 (editor reopened after its value was saved).
Round-1 Findings 2 and 3 are accepted as follow-ups and not re-raised.

## Gates
- compile, unit, types, contracts, trusted (61 s), visual (0 new failure lines vs baseline): PASS
  (logs `T25r2-*`).

## Finding 1 fix, verified by reading `src/webview/scrollSync.ts`
- `consumePendingFrontmatterEdit()` (guarded by `pendingEditorOpen`) runs before each of the three
  `previewFrontmatterSave` posts: `postFrontmatterAction` (add / remove; an `add` then stores its own
  entry through `rememberPendingFrontmatterEdit`), the key-rename post, and the value-save post in
  `saveValue`. Set-null (`saveValue(null)`) and every list-editor change also go through `saveValue`,
  so they are covered.
- `resumePendingFrontmatterEdit`: records `pendingEditOpenedIn = context.requestId` and persists
  `pendingFrontmatterEditOpenedIn`. A load with another `requestId` clears the pending edit; a
  repeated load of the same render can still reopen it. The reload-of-posting-render guard (deviation 1)
  is kept. `clearPendingFrontmatterEdit` removes both state keys, and `stateSnapshot` keeps the
  marker only while a pending edit exists.
- Integrity: the diff adds no early `return;`, `if (false)`, `debugger` or `console.*`. The round-1
  feature is still present: the Custom key picker, the `additionalPropertiesAllowed` gating, and
  `openFrontmatterEditor(row, { newField: true })`. The §2 template rules still hold in the new code.

## Tests
- Unit: "saving a value from the pending edit's editor consumes the pending edit" and "a later
  render does not reopen an editor that was already opened for the pending edit". The report shows
  both failing before the fix (logs/T25-impl2-pre-unit.log).
- RI-T25: after the buffer holds `reviewer: "Ana"`, the test calls `waitForRender(document)` and then
  waits until the `reviewer` row exists and no `[data-okf-frontmatter-editor]` is open. This cannot
  pass before the render, because the pre-render page still has the saving editor open. With the
  round-1 code, the post-render page would reopen the editor and the wait would time out. The
  assertion is meaningful, although it was not shown red.
- No existing assertion was changed.

## Visual
- `.artifacts/real-input-NDHNOu/33-custom-key-added.png`: the `reviewer` row shows `Ana` with no
  open editor or field-actions menu. Nothing is clipped, and the dark theme is readable.
  Observation only, not a T25 regression: the table lists `reviewer (unknown)` last, while the buffer
  has it right after `scope`. This is existing table ordering for unknown keys; the T24 buffer-order
  assertion still holds.

## Protected features checked
- T24 insertion after the current row: the RI-T25 buffer assertion.
- P-S2: the version fields in the posts are unchanged.
- P-E8: resume is still gated on `editMode` and `data-okf-editable="true"`.
- Key rename, set-null, list edits: the paths are unchanged apart from the consume call, and the
  existing unit and RI tests pass.

## Findings
None.

VERDICT: PASS
