# T24 — Required fields cannot be removed; new fields go after the current row

| Field | Value |
| --- | --- |
| Fixes | [UX-21](../../03-frontmatter-editing/UX-21-add-remove-field-flow.md) (part 1) |
| Decisions | D-08 |
| Depends on | T06, T23 |
| Gate | `unit trusted` |
| Risk | Medium (P-E7, message protocol P-S2) |
| Commit message | `fix(vscode): protect required fields and insert new fields after the current row` |

## Goal

- ⊟ **Remove field** is **disabled** on fields the schema marks as required, with the tooltip
  `Required by the schema; it cannot be removed`. The host's existing refusal stays as a safety net.
- Choosing a field in the add picker (`select` variant) **adds it immediately**. The separate
  confirm click disappears for that variant. The free-text variant (no schema) confirms with Enter,
  or with its confirm button.
- The new field is inserted **right after the row whose ⊞ was used**, using T06's `afterField`.

## Context to read first

- `src/frontmatter/okfFrontmatter.ts` → `analyzeFrontmatter`. It knows `effective.required`.
  `FieldEntry` has no `required` flag yet.
- `src/frontmatter/propertiesTable.ts` → row attributes.
- `src/webview/scrollSync.ts` → `createFrontmatterMenu` (picker, confirm, remove button) and
  `postFrontmatterAction(edit, action, fieldName, fieldValue)`.
- `src/extension.ts` → `PreviewSyncMessage`, `isPreviewSyncMessage`, `handleFrontmatterSave` (add
  path: `createFrontmatterFieldPatch(sourceText, fieldName, fieldValue)`).

## Allowed files

- `src/frontmatter/okfFrontmatter.ts` (`FieldEntry.required?: boolean`)
- `src/frontmatter/propertiesTable.ts`
- `src/webview/scrollSync.ts`
- `src/extension.ts`
- `test/frontmatter/okfFrontmatter.test.ts`, `test/frontmatter/propertiesTable.test.ts`,
  `test/webview/scrollSync.test.ts`, `test/integration/previewEditing.test.ts` (add tests only)
- `test/integration/realInput.test.ts` (add RI-T24)
- `test/visual/capture.py` (only the Add-field block of `check_preview_edit_mode`; added by the
  orchestrator after round 1)

## Steps

1. Write the tests first and record the failures.
2. `FieldEntry.required?: boolean`: set it to `true` in `analyzeFrontmatter` for fields in the
   effective `required` set. Leave it absent otherwise; tests that build `FieldEntry` by hand keep
   compiling.
3. Row attribute `data-okf-required="true"` when `field.required`.
4. Webview, `createFrontmatterMenu`: when the row (`edit.row`, or the name cell's row for the key
   editor) has `data-okf-required="true"`:
   - `removeButton.disabled = true`;
   - set `title`, `aria-label` and `data-tooltip` to
     `Required by the schema; it cannot be removed`.
5. Picker, `select` variant:
   - on `change`, if the value is non-empty, call `postFrontmatterAction(edit, "add", name, defaultValue, edit.fieldName)`;
   - hide the confirm button (`confirm.hidden = true`) for this variant.

   Text-input variant: keep the confirm button, and add a `keydown` `Enter` → confirm.
6. `postFrontmatterAction(edit, action, fieldName, fieldValue, afterField)`: include
   `afterField` in the message when `action === "add"` and it is a non-empty string.
7. Host:
   - add `afterField?: string` to `PreviewSyncMessage`;
   - in `isPreviewSyncMessage`, accept it only when `type === "previewFrontmatterSave"` and
     `frontmatterAction === "add"`, as a string of 1–1024 characters without `\r` or `\n`;
   - in `handleFrontmatterSave` (add path), pass
     `{ afterField: message.afterField }` to `createFrontmatterFieldPatch` when the named field
     exists in `preview.frontmatter.fields`.

## Tests

**Unit:**

- `analyzeFrontmatter` sets `required` from the schema.
- The table renders `data-okf-required`.
- Webview: the remove button is disabled for a required row; it is enabled for an optional row.
- Select `change` posts an `add` message with `afterField` equal to the open field's name.
- Text-input Enter posts the add message.

**Host validation** (`previewEditing.test.ts`, which already validates messages through
`sendPreviewMessageForTests`): an add with a valid `afterField` inserts after it. An `afterField`
containing a line break is rejected by validation (no edit).

**Real-input E2E**, scenario **RI-T24**:

- F1-like bundle whose schema has optional `depends_on` (array) and required `scope`. Edit mode.
- Open the `scope` value → **Remove field** is disabled.
- Click **Add field** → choose `depends_on`. Native `<select>` popups cannot be driven through
  CDP, so `locator.selectOption("depends_on")` is the **one allowed exception** to the real-input
  rule; document it in the note.
- Assert that the buffer has exactly one new line `depends_on: []` directly after the `scope:`
  line.

## Expected changes to existing tests

None expected. If an existing test relies on the confirm click in the `select` variant, update it
to the `change` flow and list it.

**Amended by the orchestrator after round 1 (STOP, test mechanics).** `capture.py` →
`check_preview_edit_mode`, Add-field block: after `field_picker.select_option(values[0])` it requires
an enabled `confirm-add` button and clicks it; the select variant now hides that button (D-08).
Replace that block with checks of the new flow, no weaker than before:

1. `page.wait_for_function` (timeout 2000 ms) for a `previewFrontmatterSave` message with
   `frontmatterAction === 'add'`, `fieldName === values[0]` and `afterField === 'status'` (the
   field whose editor is open). On timeout, append "frontmatter Add field selection did not post an
   add save after the open field".
2. The `confirm-add` button of the select variant is not visible (`count() == 0 or not
   is_visible()`); otherwise append "frontmatter Add confirmation is still shown for the select
   picker".

Keep everything before and after that block unchanged. List it in the report.

## Must not change

- Removal of optional fields, the host refusal message for required fields, key rename, and value
  editing.

## Done when

- The `unit` and `trusted` gates pass; RI-T24 passes.
