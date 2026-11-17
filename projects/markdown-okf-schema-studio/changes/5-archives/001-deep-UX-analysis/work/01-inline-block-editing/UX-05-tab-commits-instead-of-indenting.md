# UX-05 — Tab in the inline editor commits and closes it instead of indenting

| Field | Value |
| --- | --- |
| Severity | Medium |
| Confidence | Reproduced |
| Area | Inline block editing |
| Evidence | [u17-tab-in-block.jpg](../../evidence/u17-tab-in-block.jpg) |

## Use case

An author wants to indent or outdent a list item, or insert indentation in a code block, inside
the inline editor.

## Steps to reproduce

1. Open any list block inline (for example "Dry goods" in `fixtures-visual/04-code-and-tables.md`).
2. Move the caret to the start of a line and press Tab.

## Expected

Tab indents the current line (or the selected lines) by the list indentation; Shift+Tab outdents.
In code fences, Tab inserts the indentation unit. A documented key (for example Escape then Tab)
leaves the editor for keyboard users.

## Observed

Focus moves out of the textarea. The `blur` handler commits the block (`saveBlockEdit`) and closes
the editor. Nothing is indented. Combined with [UX-04](UX-04-enter-breaks-list-structure.md),
there is no way to fix a list's nesting from the preview.

## Where it comes from

`src/webview/scrollSync.ts` L1720 (`textarea.addEventListener("blur", saveBlockEdit)`) and no Tab
handling in the keydown handler (L1727-L1736).

## Suggested direction

Intercept Tab/Shift+Tab in the block textarea and indent/outdent the affected lines. Keep a
keyboard escape route for accessibility (Escape focuses the block, Tab moves on), and document it
in the editor status line.

## Test to add

E2E: open a list block, press Tab at the start of an item, assert the textarea is still focused
and the line gained the list indentation; Shift+Tab reverses it.

## Done when

Indentation can be changed from the inline editor without leaving it.
