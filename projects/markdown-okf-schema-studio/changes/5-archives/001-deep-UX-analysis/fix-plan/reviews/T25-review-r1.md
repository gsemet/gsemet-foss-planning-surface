# T25 review — round 1

Base: d67a757 · Reviewed diff: 8 T25 files, ~+351/-21 (the `book/chapters/05-skills.md` hunk in
`diff.sh` output is a pre-existing working-tree change, present before T25 started; not T25 scope).

## Gates
- compile, unit, types, contracts: PASS (logs/T25-*.log).
- trusted: FAIL once (RI-T10 undo timeout, BODY focus — area not touched by T25), PASS on rerun
  (logs/T25-rerun-trusted.log). One failure + one clean rerun; not attributable to T25. Accepted.
- visual: PASS vs baseline (0 new failure lines).

## Done-when
- [x] `additionalPropertiesAllowed` false only for `additionalProperties: false` — okfFrontmatter.test.ts.
- [x] Section attribute only when not allowed — propertiesTable.test.ts.
- [x] `Custom key…` offered only when allowed; input, valid Enter posts `add` with `""` + `afterField`;
  invalid name posts nothing — scrollSync.test.ts.
- [x] New field's editor opens after add (custom and schema) — RI-T25, unit pending-edit test.
- [ ] D-08 "after adding, the new field's editor opens" — met, but the editor also **reopens after
  its value has been saved** (Finding 1). Not acceptable.

## Protected features checked
- T24 add-after-current-row: RI-T25 asserts `reviewer` inserted right after `scope`.
- Key rename / required-field protection / schema validation on save: no code change in those
  paths; existing unit + RI tests pass.
- P-S2 version checks: `postFrontmatterAction` unchanged in message versioning.
- P-E8 read-only: resume is gated on `editMode` and `data-okf-editable="true"`.
- §2 template rules: `'""\\n'` and `/\\r?\\n/u` correctly doubled; no backticks / `${`.

## Findings
1. [MAJOR] src/webview/scrollSync.ts: `resumePendingFrontmatterEdit` / `receiveFrontmatterResult` /
   `closeFrontmatterEditor` — **confirmed: the new field's editor reopens after its value is saved.**
   Trace: add posted from render R1 stores `{fieldName:"reviewer", requestId:R1}`. Render R2 loads
   (full `webview.html` replace, extension.ts), opens the editor, sets `pendingEditorOpen=true`
   (in-memory only). User types `Ana` and saves; `receiveFrontmatterResult(saved:true)` keeps the
   editor open and does not clear the pending state; the page is then replaced by render R3, so
   `closeFrontmatterEditor` never runs. R3 restores `pendingFrontmatterEdit` (requestId R1 ≠ R3,
   row exists, editable) and calls `openFrontmatterEditor` again. The code comment even states "a
   repeated load of it opens the editor again". Evidence: screenshot
   `.artifacts/real-input-YKl3Rx/33-custom-key-added.png` (taken after saving `Ana`) shows the
   `reviewer` row with the field-actions menu (Add field / Remove field) open again. RI-T25 masks
   it because it next clicks `scope`, which closes the reopened editor.
   The same happens for any action posted from that editor (remove, rename, another add).
   Fix:
   - In `postFrontmatterAction` (and the value save path, `saveValue` / whatever posts
     `previewFrontmatterSave` for a value or key rename), when the posting edit is the one opened
     from the pending state (`pendingEditorOpen === true`), call `clearPendingFrontmatterEdit()`
     and set `pendingEditorOpen=false` **before** posting — except when the action itself is a new
     `add`, which then stores its own new pending entry via `rememberPendingFrontmatterEdit`.
     Simplest robust rule: clear the pending edit as soon as *any* frontmatter message is posted,
     then `rememberPendingFrontmatterEdit` for `add`.
   - Consume-once semantics: once `resumePendingFrontmatterEdit` has opened the editor in a render
     with requestId ≠ pending.requestId, mark the entry consumed (e.g. store
     `openedInRequestId: context.requestId` in state) so that a later render with a *different*
     requestId drops it instead of reopening. A reload of the same render (same requestId as
     `openedInRequestId`) may reopen it, preserving deviation 1's purpose.
   - Unit test (scrollSync.test.ts): runtime with saved state
     `{editMode:true, pendingFrontmatterEdit:{fieldName:"x", requestId:"old"}}`, row `x`; editor
     opens; trigger a value save; assert `getState().pendingFrontmatterEdit` is undefined. Second
     test: create a new runtime with the state from that run plus a new requestId and row `x`;
     assert no frontmatter editor is open.
   - RI-T25: after saving `Ana` and `waitForRender`, assert no `[data-okf-frontmatter-editor]` exists
     (before clicking `scope`); retake screenshot 33 so it shows the closed row.
2. [MINOR] Deviation 3 — buffer gets `reviewer: "Ana"` instead of the task's `reviewer: Ana`.
   Valid YAML, value equal; caused by existing quote-preservation. Acceptable; log as follow-up.
3. [NIT] In screenshot 33 the table lists `reviewer` after `owner` though the buffer has it after
   `scope` (unknown keys appear sorted last). Pre-existing ordering; not T25 scope.

## Deviations (open points)
1. Pending edit not cleared at load, keyed by requestId — needed (the host reloads the posting
   render and a status page first). Safe for Escape (closeFrontmatterEditor clears) and edit-mode
   off (resume clears when `editMode` false). **Unsafe as written for the post-save render** —
   see Finding 1.
2. New-field editor starts empty; `'""\n'` → `""` only when `options.newField`, which is set only by
   `resumePendingFrontmatterEdit`. It cannot clear a non-empty existing value (exact-match guard),
   and an unchanged empty value is treated as unchanged. Cmd/Ctrl+Enter matches the existing
   generic YAML editor. OK — but once Finding 1 is fixed, `newField` is also never applied to an
   existing `""` field on an unrelated render.
3. Quoted output — see Finding 2. OK.

## Existing assertions changed
- scrollSync.test.ts "frontmatter field toolbar adds and removes fields": picker options now
  `["", "status", "owner", "__custom__"]` — OK (amended in task).
- Harness extension (`savedState`, `tr[data-okf-field]` querySelectorAll) — not an assertion; OK.

VERDICT: CHANGES REQUESTED
