# UX-03 — In the Open With editor, Cmd+Z closes the inline editor and undoes one character

| Field | Value |
| --- | --- |
| Severity | High |
| Confidence | Reproduced |
| Area | Inline block editing in the custom editor (Open With → Markdown OKF-Schema Studio) |
| Evidence | [r2-ce-undo.jpg](../evidence/r2-ce-undo.jpg) |

## Use case

An author uses the Studio editor as their only view of the file, edits a paragraph, makes a typo,
and presses Cmd+Z, the reflex in any text field.

## Steps to reproduce

1. Open `fixtures-visual/01-handbook-overview.md` with **View: Reopen Editor With… → Markdown
   OKF-Schema Studio**.
2. Toggle edit mode, click the paragraph "The dispatch path is the only component…".
3. Type ` Second sentence.` and press Cmd+Z.

## Expected

The textarea undoes the last typing chunk and stays open with the caret in place, as it does in
the side preview (see [UX-02](UX-02-one-undo-stop-per-keystroke.md), where Cmd+Z in the textarea
is the browser's native undo).

## Observed

VS Code routes Cmd+Z to the custom text editor's document undo. One character is removed from the
buffer (`Second sentence.` → `Second sentence`). The document change is not an inline save, so the
host drops the inline edit lock and re-renders. The textarea disappears and focus returns to the
page body. Each further Cmd+Z removes one more character.

## Impact

The same shortcut does two different things depending on how the file was opened. In the Studio
editor, it destroys the editing session the user is in and leaves them hunting for their place.

## Where it comes from

- Custom text editors receive workbench undo/redo while the webview has focus.
- `src/extension.ts` `refreshPreview` (L2201-L2220) clears `activeBlockEdit` on any document
  change that is not an in-flight inline save, then renders a full new webview document.

## Suggested direction

While an inline editor is focused, keep undo/redo inside the textarea (intercept the keydown in the
webview and stop propagation) or, if document undo is kept, apply it without destroying the
editor: re-sync the textarea from the new block text and keep focus.

## Test to add

E2E in Open With mode: type inline, press Meta+Z with `page.keyboard`, assert that a textarea still
has focus and that its value lost only the last typing chunk.

## Done when

Cmd+Z / Cmd+Shift+Z behave the same in the side preview and the Open With editor, and never close
an inline editor.
