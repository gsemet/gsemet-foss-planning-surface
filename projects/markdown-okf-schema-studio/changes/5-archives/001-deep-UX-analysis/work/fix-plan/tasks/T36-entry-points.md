# T36 — Title-bar button, explorer entry and keybinding

| Field | Value |
| --- | --- |
| Fixes | [UX-30](../../07-discoverability-and-chrome/UX-30-no-entry-point-besides-palette.md) |
| Decisions | D-13 |
| Depends on | T35 |
| Gate | `unit trusted` |
| Risk | Low–medium (P-L9 opt-in posture; contract test changes deliberately) |
| Commit message | `feat(vscode): open the Studio preview from the editor title bar and explorer` |

## Goal

A first-time user finds the preview from the editor title bar of any Markdown file. The extension
still never touches `markdown.*` settings and does not replace the built-in preview commands.

## Changes

### 1. `package.json`

- `commands[openPreview].icon = "$(book)"`.
- `menus["editor/title"]`:

  ```json
  { "command": "markdown-okf-schema-studio.openPreview",
    "when": "resourceExtname == .md && activeEditor == workbench.editors.files.textFileEditor",
    "group": "navigation" }
  ```

- `menus["explorer/context"]`:

  ```json
  { "command": "markdown-okf-schema-studio.openPreview", "when": "resourceExtname == .md", "group": "navigation" }
  ```

- `keybindings`:

  ```json
  { "command": "markdown-okf-schema-studio.openPreview", "key": "ctrl+k shift+v",
    "mac": "cmd+k shift+v", "when": "editorTextFocus && resourceExtname == .md" }
  ```

- The command palette entries stay unchanged.

### 2. `openPreview(uri?: vscode.Uri)` (`src/extension.ts`)

Menus pass the resource URI. When `uri` is a `vscode.Uri` with scheme `file` and differs from the
active text editor's document:

- `await vscode.workspace.openTextDocument(uri)`;
- `await vscode.window.showTextDocument(doc, { preview: false })`;
- continue with the existing logic.

Without `uri`, behaviour is unchanged. Ignore non-`Uri` arguments: the palette passes none, and
some menus may pass other objects.

### 3. README

In "Use the Preview", add the title-bar button, the explorer entry, and `Cmd/Ctrl+K Shift+V`.

## Allowed files

- `package.json`
- `src/extension.ts` (`openPreview` signature and the start of its body)
- `test/security/package-contract.test.ts`
- `test/integration/lifecycle.test.ts`, or `realInput.test.ts` (add the new test)
- `README.md`

## Tests

- **`package-contract.test.ts`** (expected change):
  - add `icon: "$(book)"` to the openPreview entry;
  - replace `assert.equal(menus["editor/title"], undefined)` with deep-equality on the exact
    editor/title and explorer/context entries above;
  - assert the exact `keybindings` array;
  - **keep** `assert.doesNotMatch(serialized, /markdown\./u)`, and every other assertion.
- **Integration:** `executeCommand(COMMAND_ID, otherUri)` while another Markdown file is active →
  the preview shows `otherUri`, and it is the active text editor.
- **Real-input E2E**, scenario **RI-T36**: with a Markdown file active, click the title-bar action
  (`page.locator('.editor-actions [aria-label*="Open Preview to Side"]')`, picking the Studio one by
  its `book` icon class, `codicon-book`) → the side preview opens.

## Expected changes to existing tests

`package-contract.test.ts` as described above. Nothing else.

## Must not change

- The built-in Markdown preview commands and icons. `Text Editor` stays the default editor.
- Activation events: the existing `onCommand` events cover the menus.

## Done when

- The `unit` and `trusted` gates pass; RI-T36 passes.
