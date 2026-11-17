# UX-01 — Escape silently reverts text that is already in the document

| Field | Value |
| --- | --- |
| Severity | High |
| Confidence | Reproduced in a real VS Code window (real keyboard input) |
| Area | Inline block editing (preview edit mode) |
| Modes | Side preview; Open With editor uses the same runtime |
| Evidence | [u08-escape-discards.jpg](../evidence/u08-escape-discards.jpg) |

## Use case

An author clicks a paragraph in edit mode, types a sentence, and presses Escape to "leave" the
editor, the same gesture they use in Obsidian, Notion, Typora, or VS Code's own inline widgets.

## Steps to reproduce

1. Open `book/chapters/02-foundations.md`, run **Open Preview to Side**, toggle the pencil button.
2. Click the paragraph that starts with "Training and deploying an LLM".
3. Type ` KEEP ME PLEASE.` and watch the source editor: the text appears there (autosave).
4. Press Escape.

## Expected

Escape leaves the editor and keeps the text, or asks before discarding it. If Escape means
"discard", the UI says so before the user presses it and confirms after.

## Observed

The inline editor closes and the source buffer is reverted to the text it had when the block was
opened. No toast, status, or undo hint is shown. The text was visible in the source editor a moment
earlier, so the author sees their sentence disappear from both panes.

Recovery is possible only by focusing the source editor and pressing Cmd+Z once per character
(see [UX-02](UX-02-one-undo-stop-per-keystroke.md)).

## Impact

Silent loss of authored text on the most common exit gesture. Because autosave already wrote the
text into the buffer, the revert is also a second, unexpected document edit.

## Where it comes from

- `src/webview/scrollSync.ts` textarea keydown (around L1727-L1735): Escape calls
  `closeBlockEdit(true)`, which posts `previewEditCancel` (L535-L550).
- `src/extension.ts` `handlePreviewEditCancel` (L1207-L1224) sets `pendingText = originalText`
  and drains it as a `WorkspaceEdit`.

## Suggested direction

Pick one model and make it visible. Either Escape = "close and keep" (autosave already applied the
text) with an explicit **Revert block** action, or Escape = "discard" with a confirmation when the
block has autosaved changes and a status line such as "Changes discarded — Cmd+Z in the source to
restore".

## Test to add

E2E with real input: open a block, `page.keyboard.type(...)`, press Escape, assert the buffer
still contains the typed text (or assert the confirmation UI if "discard" is kept).

## Done when

No path closes an inline editor and removes user-typed text without an explicit, visible choice.
