# T20 — One click toggles a boolean frontmatter field

| Field | Value |
| --- | --- |
| Fixes | [UX-18](../../03-frontmatter-editing/UX-18-boolean-needs-two-clicks.md) |
| Depends on | T05 |
| Gate | `unit trusted` |
| Risk | Low |
| Commit message | `fix(vscode): toggle boolean frontmatter fields with one click` |

## Goal

In edit mode, one mouse click on a boolean field's value cell (the checkbox or its `true`/`false`
label) toggles the value and saves it, with the usual validation and status messages. The keyboard
path stays as today: Enter or Space opens the editor, then Space toggles.

## Context to read first

- `src/frontmatter/propertiesTable.ts` → `formatBooleanValue`: the read-mode display checkbox,
  `aria-disabled="true"`, `tabindex="-1"`.
- `src/webview/scrollSync.ts`:
  - the document click listener that opens frontmatter editors (`closest("[data-okf-edit-cell]")`,
    `openFrontmatterEditor(row)`);
  - `openFrontmatterEditor`: the `fieldType === "checkbox"` branch, `saveValue`, and the checkbox
    `change` listener.

## Allowed files

- `src/webview/scrollSync.ts`
- `test/webview/scrollSync.test.ts`
- `test/integration/realInput.test.ts` (add RI-T20)
- `test/visual/capture.py` (only the `frontmatter-boolean` opening step; added by the orchestrator
  after round 1)

## Steps

1. Write the tests first and record the failures.
2. Change the signature to `openFrontmatterEditor(row, options)`, where `options` may be
   `undefined` or `{ toggleBoolean: true }`. At the end of the function, when
   `options?.toggleBoolean && fieldType === "checkbox" && schemaFound`:
   - set `control.checked = value !== true`;
   - update `checkboxValueLabel.textContent`;
   - call `saveValue()`.
3. In the click listener, when `editMode`, the clicked cell is the **value** cell, and
   `row.getAttribute("data-okf-type") === "checkbox"`: call
   `openFrontmatterEditor(row, { toggleBoolean: true })`. The listener already calls
   `event.preventDefault()`, which cancels the native toggle of the read-mode checkbox. Keep that.
4. Leave the keyboard listener unchanged.

## Tests

**Unit:**

- Edit mode, a boolean row with value `false`: clicking the value cell posts
  `previewFrontmatterSave` with `fieldValue: true`; the editor shows "Saving frontmatter…".
- Clicking the **name** cell still opens the key editor.
- Reading mode: clicking does nothing (no message).
- The existing "boolean frontmatter values use a checkbox and save on change" test keeps all its
  assertions (see the amendment below).

**Real-input E2E**, scenario **RI-T20**:

- A schema bundle with `annotation_exemption: boolean` = `false`. Edit mode; **one** click on the
  checkbox in the value cell.
- Assert that the buffer line becomes `annotation_exemption: true` (one-line diff) and that no
  editor stays open after the re-render.

## Expected changes to existing tests

**Amended by the orchestrator after round 1 (STOP, test mechanics only).** Two existing checks open
the boolean editor with a **mouse click** on the value cell and then assert the editor's checkbox
state. With this task a click toggles directly, while the keyboard path (Enter or Space opens the
editor, then Space toggles) is unchanged, so these checks now cover that keyboard path:

1. `scrollSync.test.ts` → "boolean frontmatter values use a checkbox and save on change": replace
   only the opening click with the keyboard activation the runtime supports (a `keydown` Enter on
   the value cell, the way the existing keyboard frontmatter tests do it). Keep every assertion.
2. `test/visual/capture.py` → the `frontmatter-boolean` branch: open the editor with the keyboard
   (focus the value cell, then `page.keyboard.press("Enter")`) instead of `target.click()`. Keep
   every check that follows (editor visible, checkbox visible, starts checked, class, toggles on
   click, posts the `false` save).

List both in the report. No other existing assertion changes.

## Must not change

- The null button for nullable booleans, the keyboard flow, validation errors (the editor stays
  open with the error), and read-mode display.

## Done when

- The `unit` and `trusted` gates pass; RI-T20 passes.
