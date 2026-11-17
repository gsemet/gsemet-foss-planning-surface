# UX-17 — Enter in a one-line text field adds a newline and saves `title: |`

| Field | Value |
| --- | --- |
| Severity | High |
| Confidence | Reproduced |
| Area | Frontmatter properties table editing (text fields) |
| Evidence | [r3-fm-title-saved.jpg](../evidence/r3-fm-title-saved.jpg) |

## Use case

An author edits the `title` value and presses Enter to confirm, as in any form field.

## Steps to reproduce

1. Edit mode on `SwRS-CORE-001.md`, click the `title` value.
2. Select all, type `Write CSV output: with quotes "and" colons`, press Enter.
3. Click outside the table.

## Observed

- Enter inserts a newline inside the textarea; nothing is saved and nothing indicates how to save.
- On blur, the value with its trailing newline is written as a YAML literal block:

  ```yaml
  title: |
    Write CSV output: with quotes "and" colons
  ```

  The title now ends with `\n`. Schema validation passes (`type: string`), so no warning is shown.
- Enter behaves differently in each editor: newline in block and frontmatter text editors, save
  in table cells, nothing in list items ([UX-19](UX-19-list-editor-keyboard-and-completion.md)).

## Expected

For scalar text fields without line breaks in their current value, Enter commits and
Shift+Enter inserts a newline. Values are trimmed of trailing newlines unless the user explicitly
asks for a multi-line string.

## Where it comes from

`src/webview/scrollSync.ts` frontmatter value keydown (around L1324-L1331): Enter commits only when
`control.tagName !== "TEXTAREA"`, and text fields use a textarea.

## Done when

Pressing Enter in a one-line text field saves the value and never adds a newline to it.
