## Summary

Edit mode could only be driven fully with the mouse. This change lets you work through a document with the keyboard alone: move between blocks, open one, edit, save or cancel, and carry on with the next block.

## Deliverables

Keyboard flow in edit mode (no editor open, then inside an editor):

| Key | Effect |
| --- | --- |
| Up / Down | Select a block (first press picks the block nearest the top of the viewport), then move to the previous or next block |
| Enter | Open the selected block in its editor |
| Cmd/Ctrl+Enter | Save the edit and close the editor |
| Esc | Cancel the edit and close the editor |

After saving or cancelling, the edited block stays selected, so Up/Down continue from there. The selection reuses the existing themed outline, is focused and announced to assistive technology, and scrolls into view.

Before / after (a paragraph selected with Down, opened with Enter, closed with Esc):

| | Cream theme | Dark theme |
| --- | --- | --- |
| Before | ![before cream](SHOT_URL/before-cream.png) | ![before dark](SHOT_URL/before-dark.png) |
| After | ![after cream](SHOT_URL/after-cream.png) | ![after dark](SHOT_URL/after-dark.png) |

## Changes

- Plain Up/Down/Enter handling and selection stepping in the block selection view; Esc and Cmd/Ctrl+Enter in the block source editor now hand the selection back.
- New requirement, user documentation and changelog entry.
- 8 new unit tests (7 fail without the change) and 2 new visual scenarios (cream and dark).

## Impacts

Edit mode only. Table-cell editors and new-block (insert bar) editors keep their own Esc / Cmd+Enter behaviour and do not return to a selection.

## Blast radius

1 (edit-mode key handling in the preview page).

## Test plan

- `just check`: unit 2692 pass, requirements lint 0 errors.
- Visual group `block-editing`: 19 scenarios pass.
- Not verified in a real VS Code window (key forwarding into the webview).

## Autonomous decisions

- Esc closes any open box; Up/Down move a visible selection when no editor is open; Enter opens the selected block; Cmd/Ctrl+Enter saves; Esc cancels.
- The selection starts at the block nearest the top of the viewport.
- Keys are handled inside the page rather than through VS Code keybindings with a `when` clause: plain Up/Down/Enter/Esc as global keybindings would steal keys from the text editor.

## Internal references

CR 120 (backlog item edition-with-only-keyboard); sibling CR 119 for the shortcut pattern.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
