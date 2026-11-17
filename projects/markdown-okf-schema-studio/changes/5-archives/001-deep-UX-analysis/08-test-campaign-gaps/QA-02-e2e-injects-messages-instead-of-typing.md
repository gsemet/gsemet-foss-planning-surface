# QA-02 — E2E suites inject messages and fill fields instead of typing like a user

| Field | Value |
| --- | --- |
| Severity | High (test gap) |
| Confidence | Counted in `test/integration/*.ts` and `test/visual/*.ts` |
| Area | Integration / E2E campaign |

## Observed

| Input technique in the suites | Occurrences |
| --- | --- |
| `sendPreviewMessageForTests(...)` (synthetic webview messages) | 51 |
| `locator.fill(...)` (sets the whole value at once) | 2 |
| `textarea.press(...)` / `keyboard.press(...)` | 7 |
| `keyboard.type(...)` (real per-character typing) | 0 |
| Undo/redo (`Meta+Z`, `Control+Z`) | 0 |
| `Escape` | 1 (reload suite) |

Because no test types character by character, the per-keystroke autosave path is never exercised
end to end. That path produces one undo step per character
([UX-02](../01-inline-block-editing/UX-02-one-undo-stop-per-keystroke.md)), has Escape revert
already-saved text ([UX-01](../01-inline-block-editing/UX-01-escape-discards-autosaved-text.md)),
and breaks under document undo in the Open With editor
([UX-03](../01-inline-block-editing/UX-03-open-with-undo-closes-inline-editor.md)). Injected
messages also bypass the real focus, blur, and keydown handlers
([UX-05](../01-inline-block-editing/UX-05-tab-commits-instead-of-indenting.md),
[UX-13](../02-table-editing/UX-13-tab-leaves-dangling-cell-editor.md),
[UX-17](../03-frontmatter-editing/UX-17-enter-in-text-field-creates-block-scalar.md)).

## Suggested change

Add a "real input" E2E tier that only uses `page.mouse` and `page.keyboard` (no test hooks for
actions; hooks allowed for reading state):

1. inline paragraph edit: type, Escape, Cmd+Z, Cmd+Enter, blur;
2. list edit: Enter, Tab, Shift+Tab;
3. table: type, Tab, Enter, Escape;
4. frontmatter: text Enter, boolean single click, list Enter;
5. Open With editor: the same flows plus Cmd+S and Cmd+Z.

Each step asserts the buffer text (through `vscode.workspace` in the test host) and captures a
screenshot.

## Done when

Every bug in groups 01-03 of this report has a failing real-input E2E test.
