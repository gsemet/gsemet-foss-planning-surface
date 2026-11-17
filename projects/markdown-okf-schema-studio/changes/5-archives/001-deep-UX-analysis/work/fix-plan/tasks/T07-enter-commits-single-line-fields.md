# T07 — Enter commits one-line frontmatter text fields

| Field | Value |
| --- | --- |
| Fixes | [UX-17](../../03-frontmatter-editing/UX-17-enter-in-text-field-creates-block-scalar.md) |
| Decisions | D-06 |
| Depends on | T05 (a minimal patch makes the RI test diff clean), T02 |
| Gate | `unit trusted` |
| Risk | Low |
| Commit message | `fix(vscode): save one-line frontmatter text on Enter` |

## Goal

In a frontmatter **text** field (a `textarea` with `data-okf-text-value`):

- **The current value has no line break:** Enter saves, and Shift+Enter inserts a line break.
- **The value contains a line break:** Enter inserts a line break, and Cmd/Ctrl+Enter saves.
- On save, trailing line breaks are removed, unless the field's original value ended with one.
- The YAML editor textarea (objects, unknown types, schema-free values) keeps Enter as a line break
  and also gains Cmd/Ctrl+Enter to save.

## Context to read first

- `src/webview/scrollSync.ts` → `openFrontmatterEditor(row)`: `useTextarea`, `useYamlEditor`,
  `fieldType === "text"` branch, `saveValue(forcedValue)`, and the `control.addEventListener("keydown", …)`
  that handles Escape and Enter.
- `conventions.md` §2: you are editing inside the runtime template literal. Double the backslashes
  in the regex: the TS source `/(?:\\r?\\n)+$/u` becomes `/(?:\r?\n)+$/u` in the webview.

## Allowed files

- `src/webview/scrollSync.ts`
- `test/webview/scrollSync.test.ts` (add tests; extend the fake DOM only if needed)
- `test/integration/realInput.test.ts` (add RI-T07)
- `README.md` (one sentence in the "Edit mode" paragraph)

## Steps

1. Write the tests first (below) and record their failures.
2. In the keydown handler of `openFrontmatterEditor`, replace the Enter branch with logic equivalent
   to:

   ```js
   } else if (!useListEditorValue && event.key === "Enter" && !event.isComposing) {
     const commitShortcut = event.metaKey || event.ctrlKey;
     const isTextField = control.tagName === "TEXTAREA" && fieldType === "text" && !useYamlEditor;
     const multiline = String(control.value).includes("\n");   // inside the template: "\\n"
     if (control.tagName !== "TEXTAREA"
       || commitShortcut
       || (isTextField && !multiline && !event.shiftKey && !event.altKey)) {
       event.preventDefault?.();
       saveValue();
     }
   }
   ```

   Keep the Escape branch exactly as it is: frontmatter Escape still cancels (D-01).
3. In `saveValue`, for text fields (`fieldType === "text"` and not the YAML editor, with no
   `forcedValue`): if `typeof value !== "string" || !value.endsWith("\n")`, strip trailing
   `\r?\n` sequences from `control.value` before computing `fieldValue` and `unchanged`.
4. Add `aria-keyshortcuts="Enter Shift+Enter"` and a `title` to the text-field textarea:
   `Enter saves · Shift+Enter adds a line`.
5. README, "Edit mode" paragraph: add one sentence. "In a one-line text field, Enter saves and
   Shift+Enter starts a new line; in multi-line values, Cmd/Ctrl+Enter saves."

## Tests

**Unit** (`scrollSync.test.ts`; follow the pattern of "text frontmatter values use a wrapping textarea that grows with its content"):

1. A text field with value `"Alpha"`. Set `control.value = "Beta"` and dispatch a keydown `Enter` →
   one `previewFrontmatterSave` with `fieldValue: "Beta"`, and `preventDefault` called.
2. Same with `shiftKey: true` → no save message, `preventDefault` not called.
3. Value `"a\nb"`, keydown `Enter` → no save. Keydown `Enter` with `metaKey: true` → save with
   `"a\nb"`.
4. Value `"Beta\n"`, saved through blur → `fieldValue: "Beta"`.
5. YAML editor: keydown `Enter` → no save; `ctrlKey: true` → save.

**Real-input E2E**, scenario **RI-T07**:

- A schema bundle with `title: string`. In edit mode, click the `title` value, press `${MOD}+A`,
  type `Write CSV output: with quotes "and" colons`, press `Enter`.
- Assert that the editor is closed, and that the frontmatter, parsed with `yaml`, has
  `title === 'Write CSV output: with quotes "and" colons'`, with no line break.
- Then reopen `title`, type `a`, press `Shift+Enter`, type `b`, press `${MOD}+Enter` → the title
  ends with `a\nb` (a multi-line value, saved).

Both must fail before the fix.

## Expected changes to existing tests

None expected. If an existing test dispatches Enter on a text textarea and expects no save, STOP:
that is a behaviour this task changes on purpose, so ask the orchestrator to amend the task.

## Must not change

- The list editor (T21), enum, date, number and checkbox controls, the key editor (Enter already
  saves), and Escape semantics.

## Done when

- The `unit` and `trusted` gates pass; RI-T07 passes.
- A one-line text field can no longer be saved with a stray trailing line break.
