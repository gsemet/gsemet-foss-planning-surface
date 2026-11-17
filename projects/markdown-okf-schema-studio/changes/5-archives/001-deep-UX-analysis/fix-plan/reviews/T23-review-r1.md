# T23 review — round 1

Base: cf66e90 · Reviewed diff: 7 files, +217/-107

## Gates
compile/unit/types/trusted: PASS; visual: PASS vs T00 baseline (0 new failure lines; orchestrator summary, logs in `logs/`).
The RI-T21 failure in an earlier trusted run is a link-open focus timeout, outside this diff. The final run passed.

## Done-when
- [x] The actions render inside the editing cell, in normal flow. Evidence: unit test "frontmatter field actions render inside the edited row" (name and value editors; `menu.parentElement === editor`, last child, not in body); RI-T23 (`inEditor`, `position: static`); capture.py placement check.
- [x] Labels `Add field` / `Remove field` / `Add`. Evidence: unit test labels deepEqual; RI-T23; screenshots.
- [x] The pseudo-tooltip is disabled and native `title`/`aria-label` are kept. Evidence: previewStyles test (`content: none`, no hover/focus selectors); `createButton` still sets `title`, `aria-label` and `data-tooltip`.
- [x] Text values open a one-row textarea that grows. Evidence: unit test "frontmatter text values open a one-row textarea"; RI-T23 `rows === 1`. `resizeTextarea` still runs on `input` and after open (sets height from `scrollHeight`), so the textarea still grows.
- [x] RI-T23 at a 540 px frame (frame width asserted between 480 and 620 px). The required overlay checks PASS on both captures.
- [x] Machine checks were added to all five frontmatter `editTarget` scenarios and pass.
- [ ] Unit test "the blur of the control with `relatedTarget` inside the menu still does not save". The task requires it, and it does not exist. See finding 1.

## Protected features checked
- P-E7 (add/remove/picker/blur-save):
  - Add and remove still post the same messages: "frontmatter field toolbar adds and removes fields" is unchanged apart from the placement lines, and capture.py's Add flow posts an add save.
  - Focus: the Add button still focuses `fieldControl`. No focus calls changed.
  - Clicks inside the menu now bubble through the editor. The document click handler returns early on `closest("[data-okf-frontmatter-editor]")`. `openMappedEditor` returns early on `[data-okf-properties]`. No handler reopens or closes the editor.
  - The blur guards (key editor line ~1027, value editor ~1543, list `focusout` ~1535) still match `[data-okf-frontmatter-menu]` through `closest`, and the menu still carries that attribute. Logic is correct, but no unit test covers it (finding 1).
- P-E8: the menu is only created from the open-editor paths, which are gated by `editMode`. No change there.
- P-S4: the labels use `textContent`. The icons are constant SVG.
- T07 (Shift+Enter multi-line): the keydown logic is unchanged. Shift+Enter inserts a newline natively, `input` fires, and `resizeTextarea` grows the textarea. `rows = 1` is explicitly task step 5. No conflict.
- Table toolbar (T18) and link tooltips: the shared tooltip rules lost only their frontmatter selectors. The table-menu selectors are unchanged.
- Webview template (conventions §2): the new code has no backticks and no `${`. No new timers or listeners. The scroll and resize listeners were removed, along with their cleanup. The `frontmatterMenuPositionListener` field is set to `undefined`.

## Findings
1. [MAJOR] test/webview/scrollSync.test.ts — the unit test that the task requires is missing: "blur of the control with relatedTarget inside the menu still does not save". This is the main P-E7 risk of moving the menu into the editor. Fix: add the test `frontmatter blur toward the field actions does not save`, for both the value editor and the key editor (harness `mapFrontmatter: true`).
   1. Open the editor and change the control value.
   2. Find the button with `data-okf-frontmatter-operation="add"` in `harness.createdElements`.
   3. Dispatch `control.dispatch("blur", { relatedTarget: addButton })`.
   4. Assert that no `previewFrontmatterSave` / rename message was posted and that the editor is still open (`menu.parentElement === editor`).
   5. Then dispatch `blur` with `relatedTarget: null` and assert that exactly one save is posted.
   6. For a list-valued row, do the same with `editor.dispatch("focusout", { relatedTarget: <picker select> })` → no save.
   If the harness `closest` does not resolve ancestors for created elements, use it as-is if it does. Otherwise give the button a `closest` stub that returns the menu for `[data-okf-frontmatter-menu]`.
2. [MINOR] src/webview/scrollSync.ts — list-editor `focusout` behaviour changes. The picker is now inside `editor`, so when focus leaves the picker `<select>` for somewhere outside the row, the list editor's `focusout` now saves. Before, the picker was outside the editor and did not trigger a save. This matches blur-save semantics and is acceptable. Record it in followups. No code change is required.
3. [MINOR] The report shows no failing-before evidence for RI-T23 or the previewStyles test. That is acceptable, because the old `position: fixed` rule makes the new assertions fail by construction.
4. [NIT] At a 540 px frame, Add field and Remove field stack vertically (screenshot 31). This is readable and inside the row, so it is acceptable.

## Visual
- `logs/visual-T23/edit-frontmatter-value-dark.png`: the actions sit inside the status row under the select. The row height grows, they cover no other row, and the labels are readable.
- `.artifacts/real-input-kxxpOS/31-frontmatter-actions-picker.png` (540 px frame): the menu and the picker are inside the scope row. Owner stays below it and nothing is clipped. The disabled `Add` button is dim but legible.

## Existing assertions changed
- scrollSync "frontmatter floating bar follows…" → renamed "frontmatter field actions render inside the edited row": OK. The task lists this change, and the new assertions are stronger (parent, last child, no position properties after scroll/resize).
- scrollSync "frontmatter field toolbar adds and removes fields": `data-placement` "below"/top/left → null/"": OK. This is the direct consequence of removing `positionMenu`. The add/remove message assertions are untouched.
- previewStyles: the removed `flex-wrap: nowrap` assertion on the frontmatter menu: OK. The task's CSS step requires `wrap`, and the new test asserts it.
- realInput RI-T05/T06: `[data-okf-frontmatter-editor] select|input` → `> select|input`: OK. The picker's select/input now lives inside the editor, so the descendant selector would also match the picker. The control is a direct child of the editor (`editor.appendChild(control)`), so the narrowed selector targets the same element. This is not a weakening.
- capture.py: "editor has no buttons" → "no buttons outside `[data-okf-frontmatter-menu]`": OK. This is required by the menu moving inside the editor, and the check still catches stray buttons. The new placement, clipping and label checks strengthen it.

VERDICT: CHANGES REQUESTED
