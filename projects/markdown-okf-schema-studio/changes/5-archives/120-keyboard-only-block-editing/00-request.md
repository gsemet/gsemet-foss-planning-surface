# 120 — Keyboard-only block editing

Type: feat · Priority: P1 · From backlog: `02-backlog/P1/edition-with-only-keyboard`

## Intent (user)

From the creation of a new file and switching the Edit mode i would like to be able to write only using keyboard:

- `esc` to switch close the active edition box
- `up` `down` to select the paragraph/box to edit
- `enter` to enter in the edition of this paragraph
- (edit)
- `Ctrl/Cmd + Enter` to validate (or `esc` to cancel)
- `up` / `down` to focus another box to edit
...

## Autonomous decisions

- Decided by the main session on 2026-10-26 under the user's instruction "pas de questions, full autonome". List these in the PR body under "Autonomous decisions".
- Esc closes any open box; Up/Down move a visible block selection when no editor is open; Enter opens the selected block; Cmd/Ctrl+Enter validates; Esc cancels.
- The selection is a focus ring that follows the theme and scrolls into view; it starts at the block nearest the top of the viewport.
- Shortcuts go through VS Code keybindings with a `when` clause like CR 119. Document them in the docs and the SwRS.
