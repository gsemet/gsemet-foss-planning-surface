# T25 — Custom keys, and a new field opens its editor

| Field | Value |
| --- | --- |
| Fixes | [UX-21](../../03-frontmatter-editing/UX-21-add-remove-field-flow.md) (part 2) |
| Decisions | D-08 |
| Depends on | T24 |
| Gate | `unit trusted` |
| Risk | Low–medium |
| Commit message | `feat(vscode): add custom frontmatter keys and edit new fields immediately` |

## Goal

- **Custom keys.** The add picker (`select` variant) offers a last option, `Custom key…`, when the
  matched schema does **not** declare `additionalProperties: false`. Choosing it shows a text input
  for the key name; Enter adds the field with value `""` after the current row (T24).
- **Immediate editing.** After **any** successful add, schema or custom, the re-rendered preview
  immediately opens the new field's value editor, so adding a field is "one choice, then type the
  value".

## Context to read first

- `src/frontmatter/okfFrontmatter.ts` → `analyzeFrontmatter`, `FrontmatterResult`, and where the
  schema root is available.
- `src/frontmatter/propertiesTable.ts` → the `<section data-okf-properties …>` attributes.
- `src/webview/scrollSync.ts`:
  - `createFrontmatterMenu` picker (T24 state);
  - `postFrontmatterAction`, `receiveFrontmatterResult`;
  - `rememberPendingBlockNavigation` / `clearPendingBlockNavigation` / `resumePendingBlockNavigation`,
    the pattern to copy for a pending frontmatter edit;
  - `stateSnapshot` (it persists `pendingBlockNavigation`).

## Allowed files

- `src/frontmatter/okfFrontmatter.ts` (`FrontmatterResult.additionalPropertiesAllowed?: boolean`)
- `src/frontmatter/propertiesTable.ts`
- `src/webview/scrollSync.ts`
- `test/frontmatter/okfFrontmatter.test.ts`, `test/frontmatter/propertiesTable.test.ts`,
  `test/webview/scrollSync.test.ts` (add tests)
- `test/integration/realInput.test.ts` (add RI-T25)
- `README.md` (one sentence)

## Steps

1. Write the tests first and record the failures.
2. `analyzeFrontmatter`: set `additionalPropertiesAllowed` to `false` only when the schema root
   (after `$ref` resolution, as used for `effective`) has `additionalProperties === false`.
   Otherwise set it to `true`; with no schema, it is `true`. Note: the
   `strictAdditionalProperties` setting only adds warnings; it does not forbid keys. Leave it
   unchanged.
3. Section attribute `data-okf-additional-properties="false"` when not allowed. Absent otherwise.
4. Picker:
   - unless the section says `false`, append `<option value="__custom__">Custom key…</option>`;
   - on `change` to `__custom__`, show a text input (aria-label `New field name`) after the select,
     focus it, and do not post anything;
   - on `Enter` in it, validate the name: non-empty, no leading or trailing spaces, no line break,
     not an existing field. Show the error in the editor status if invalid. When valid, call
     `postFrontmatterAction(edit, "add", name, "", edit.fieldName)`.
5. **Pending edit.** When posting an `add`, store `pendingFrontmatterEdit = { fieldName }` in the
   webview state, alongside `pendingBlockNavigation`.
   - On an error result (`receiveFrontmatterResult` with an error), clear it.
   - At load, after `restoreState` and only in edit mode, if a pending edit exists: clear it, find
     `tr[data-okf-field="<name>"]`, and if it is editable, call `openFrontmatterEditor(row)`.
6. README, "Edit mode" paragraph: "Adding a field opens its editor right away; custom keys are
   available unless the schema forbids additional properties."

## Tests

**Unit:**

- `additionalPropertiesAllowed` is `false` for a schema with `additionalProperties: false`, and
  `true` otherwise and with no schema.
- The picker has `Custom key…` only when allowed.
- Choosing it shows the input; Enter with a valid name posts `add` with `fieldValue: ""` and
  `afterField`; an invalid name shows an error and posts nothing.
- Pending edit: a runtime created with saved state `{ editMode: true, pendingFrontmatterEdit: { fieldName: "x" } }`
  and a row `x` opens the editor for `x`, then clears the state.

**Real-input E2E**, scenario **RI-T25** (the T24 fixture, with the schema allowing additional
properties):

- Open `scope`, click **Add field**, choose `Custom key…` (`selectOption`, the documented
  exception).
- Type `reviewer`, press `Enter` → after the re-render, the `reviewer` editor is open and focused.
- Type `Ana`, press `Enter` → the buffer has `reviewer: Ana` right after `scope:`.
- Add `depends_on` → its list editor opens.

## Expected changes to existing tests

**Amended by the orchestrator after round 1 (STOP, direct consequence of D-08).**
`scrollSync.test.ts` → "frontmatter field toolbar adds and removes fields" asserts the picker
options are exactly `["", "status", "owner"]`. Its fixture schema does not set
`additionalProperties: false`, so the new `Custom key…` option is expected: change that one
assertion to the exact list `["", "status", "owner", "__custom__"]` (use the sentinel value the
implementation uses). Do not set `data-okf-additional-properties` on that harness to avoid it.
List it in the report. No other existing assertion changes.

## Must not change

- The T24 behaviour, key rename, required-field protection, and schema validation on save.

## Done when

- The `unit` and `trusted` gates pass; RI-T25 passes.
