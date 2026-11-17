# T41 — Add field: source position, one-line custom keys, Escape cancels

| Field | Value |
| --- | --- |
| Fixes | Remaining gaps of [UX-21](../../03-frontmatter-editing/UX-21-add-remove-field-flow.md), from `replay/UX-21.md` |
| Decisions | D-21 (and D-08 for the add/remove flow) |
| Depends on | T42 |
| Gate | `unit types trusted full visual` |
| Risk | Medium (frontmatter writes; P-F protected features) |
| Commit message | `fix(vscode): place new fields where the table shows them and keep custom keys on one line` |

## Goal

1. **Position (D-21 a).** "Add field" inserts the new key in the source at the position its row
   takes in the properties table, so the table and the file agree.
   - Today the key goes after the clicked row in the source, while the table shows it elsewhere.
     Seen in the replay: `depends_on` was inserted after `scope` but shown after `derived_by`, in
     schema order. A custom key `reviewer` was added from `priority` but shown after `owner`.
2. **One-line custom keys (D-21 b).**
   - Enter in a new custom key's value editor saves it. Shift+Enter inserts a line break.
   - The value is written as a plain YAML scalar when that is safe: `approver: Ann`, not
     `approver: "Ann"`.
   - It is quoted only when YAML requires it, for example for `yes`, `null`, `123`, `a: b`, a
     leading `#`, or leading or trailing spaces.
3. **Escape (D-21 c).** Escape cancels the open frontmatter edit wherever the focus is inside the
   properties section, for example on the field picker or a header cell. It does what Escape
   already does inside the field control (`cancelled = true; closeFrontmatterEditor()`): nothing
   is written.

## Context to read first

- `PLAN/replay/UX-21.md`: the observed behaviour and the scenario files under
  `replay/scenarios/UX-21-*.json`.
- `src/webview/scrollSync.ts`:
  - the "Add field" picker and the key editor (around the `saveKey` / `newFieldName` code near
    line 1255);
  - the field value editor (`keydown` near line 1760, with `isTextField` and `multiline`);
  - `closeFrontmatterEditor`.
- The host side that writes frontmatter edits: find it from the `newFieldName` and `fieldValue`
  message fields in `src/extension.ts`, and from the frontmatter writer under `src/frontmatter/`.
  Find there how a new key's insertion point is chosen and how a value is serialized (the
  quoting).
- The code that orders the properties table rows: `src/frontmatter/propertiesTable.ts` and
  related files.
  - The insertion point for (1) **must be derived from that same ordering**: the key goes right
    after the source line of the row that precedes it in the table, or before the row that follows
    it when it comes first.
  - Do not invent a second ordering rule.

## Allowed files

- `src/webview/scrollSync.ts`
- `src/extension.ts`, only for the frontmatter edit handling
- `src/frontmatter/*.ts`
- the matching unit tests under `test/frontmatter/` and `test/webview/scrollSync.test.ts`
- `test/integration/realInput.test.ts`, to add RI-T41

## Steps

1. Write the tests first and record that they fail.
2. **Position.** Compute the insertion point from the table order as described above. This
   applies to both schema fields and custom keys.
3. **Custom key value.**
   - Treat a new custom key as a one-line text field, with the same Enter, Shift+Enter and
     Cmd+Enter rules as an existing one-line text field.
   - Serialize it as a plain scalar when YAML-safe. Reuse the existing serializer's safety check if
     one exists. Never change how existing values are written.
4. **Escape.** Add one `keydown` listener for Escape at the properties-section level, or reuse the
   document-level pattern near line 2078. When a frontmatter editor is open and the event target
   is inside the properties section but outside the control, cancel exactly as the control's own
   Escape does. Do not change the block or table-cell Escape behaviour; it belongs to another
   request.

## Tests

**Unit:**
- the insertion point for a schema field missing from the source: between its schema neighbours;
- the insertion point for a custom key: where the table lists non-schema keys;
- scalar safety: `Ann` and `two words` are plain; `yes`, `null`, `123`, `a: b`, `#x` and ` lead`
  are quoted.

**Real-input E2E, scenario RI-T41,** on a fixture with schema fields and extra keys, edit mode on:
- Add a schema field from a row that is not its table neighbour. Its source line sits between its
  table neighbours, as a one-line diff, and its row appears in the same place.
- Add a custom key `approver`, type `Ann`, press Enter. The editor closes, and the diff is the
  single line `approver: Ann`.
- Open a field editor, click "Add field" so focus moves to the picker, press Escape. The editor
  and the picker close, and the buffer is unchanged (`spy`-style diff against the disk, or the
  buffer text).

## Expected changes to existing tests

- Any test that asserts the old position (after the clicked row) or the quoted form for a new
  custom key. List each one with its reason. No other changes.

## Must not change

- Writing existing fields: one-line diffs, comments kept, the folded or flow style kept (UX-16
  and part 2).
- Required fields cannot be removed (D-08).
- Escape and Enter in existing field controls.
