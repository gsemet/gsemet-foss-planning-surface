# T13 — The side preview ignores non-Markdown editors

| Field | Value |
| --- | --- |
| Fixes | [UX-25](../../05-preview-lifecycle/UX-25-preview-blanked-by-non-markdown-editor.md) |
| Depends on | T00 |
| Gate | `unit full` |
| Risk | Low–medium (P-L1, P-L4) |
| Commit message | `fix(vscode): keep the side preview on its Markdown file when another editor is active` |

## Goal

Like VS Code's built-in Markdown preview, the side preview keeps showing the last Markdown
document while a non-Markdown editor is active: a code file opened from an x-okf-link, settings
JSON, a schema YAML, a diff editor, an untitled file. It switches only when another **eligible
Markdown** editor becomes active.

The "missing source" page stays reserved for a previewed file that disappears (P-L4).

## Context to read first

- `src/extension.ts`: `followActiveEditor`, `showUnavailableDocument`, `switchPreviewDocument`,
  `isDocumentEligible`, `setMissingSource`, `handleRenames`, and the dependency watcher's
  `onDidDelete` in `createPreview`.
- `test/integration/lifecycle.test.ts`, the block that opens `package.json`. It currently asserts
  the bug.

## Allowed files

- `src/extension.ts`
- `test/integration/lifecycle.test.ts`
- `test/integration/realInput.test.ts` (add RI-T13)
- `README.md` (one sentence in "Use the Preview")

## Steps

1. Write RI-T13 and the new lifecycle expectations first. Record the failure.
2. `followActiveEditor`: when `!isDocumentEligible(document)`, **return** without changing the
   preview. Delete `showUnavailableDocument` if nothing else uses it
   (`rg -n showUnavailableDocument src`).
3. Leave every other caller of `setMissingSource` unchanged.
4. README, "Use the Preview": "The side preview follows the active Markdown editor and keeps its
   document while you work in other kinds of files."

## Tests

**Lifecycle** (`lifecycle.test.ts`). Replace the block from
`const nonMarkdownDocument = …` up to, and including, the "returning to a Markdown editor" wait:

- Record `before = getActivePreviewForTests()`, with its `requestId`, `documentUri` and `status`.
- Show `package.json` in column One. Wait 750 ms. A bounded sleep is acceptable here because we
  assert that **nothing** happens.
- Assert: `documentUri` is unchanged (the second document); `status` is `recovery` or `success`;
  `html` still includes `Lifecycle edit marker`; `outputDirectory` is defined; `requestId` is
  unchanged.
- Show `secondDocument` again → wait for `phase === "ready"`. Assert that `requestId` is
  **unchanged**: no new render was needed.

**Real-input E2E**, scenario **RI-T13**:

- Side preview on a Markdown fixture. Open a `.py` file of the fixture in column One by clicking
  nothing: use `vscode.window.showTextDocument`, which is an editor action, not a preview action.
- Assert that the preview frame still shows the Markdown heading text, and that the panel title
  still names the Markdown file (read it with `getActivePreviewPanelForTests()?.title`, exported by
  `extensionApi`).
- Then reveal a **second** Markdown file → the preview switches to it (P-L1 still works).

## Expected changes to existing tests

- `lifecycle.test.ts`: the `package.json` block described above. Its old assertions
  (`status === "missing-source"`, `documentUri === package.json`, content gone) encode the bug and
  are replaced.

## Must not change

- Deleted or renamed previewed file → the missing-source page (P-L4). Recovery when it comes back.
- The Open With editor (`followsActiveEditor === false`) stays on its file (P-L2).
- Restoration after reload (P-L3).

## Done when

- The `unit` and `full` gates pass; RI-T13 passes.
- No user-visible "Open a Markdown file to use the Sphinx preview." remains: the string disappears
  with `showUnavailableDocument`.
